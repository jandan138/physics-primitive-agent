from __future__ import annotations

from dataclasses import dataclass, replace
import math

from primitive_collision_compiler.baselines.cpd_like.primitives import PrimitiveFit, fit_best_primitive
from primitive_collision_compiler.geometry.mesh import TriangleMesh

COMPONENT_MERGE_TOPOLOGY_ONLY = "topology_only"
COMPONENT_MERGE_VIRTUAL_PAIRWISE = "virtual_pairwise"
MERGE_SEARCH_TOPOLOGY_THEN_VIRTUAL = "topology_then_virtual"
MERGE_SEARCH_COST_GUIDED_PAIRWISE = "cost_guided_pairwise"
REPORT_MERGE_TRACE_SUMMARY = "summary"
REPORT_MERGE_TRACE_NONE = "none"
MIN_NORMALIZATION_VOLUME = 1e-12


@dataclass(frozen=True)
class _MergeCandidate:
    left_id: int
    right_id: int
    merged_fit: PrimitiveFit
    excess_volume: float
    normalized_excess_volume: float
    is_virtual_component_merge: bool


@dataclass(frozen=True)
class CPDLikeDecompositionReport:
    stage: str
    status: str
    primitive_count: int
    max_primitives: int
    mesh_point_count: int
    mesh_face_count: int
    primitive_subset: tuple[str, ...]
    unsupported_primitives: tuple[str, ...]
    primitives: tuple[PrimitiveFit, ...]
    total_weighted_volume: float
    fallback_reason: str | None
    merge_policy: str
    merge_search_policy: str
    mesh_aabb_volume: float
    target_primitive_count: int
    initial_component_count: int
    topology_merge_count: int
    virtual_component_merge_count: int
    blocked_merge_count: int
    final_component_count: int
    excess_volume_threshold_fraction: float | None
    normalized_total_weighted_volume: float
    merge_cost_summary: dict[str, object]

    def to_dict(self) -> dict[str, object]:
        return {
            "stage": self.stage,
            "status": self.status,
            "primitive_count": self.primitive_count,
            "max_primitives": self.max_primitives,
            "mesh_point_count": self.mesh_point_count,
            "mesh_face_count": self.mesh_face_count,
            "primitive_subset": list(self.primitive_subset),
            "unsupported_primitives": list(self.unsupported_primitives),
            "primitives": [primitive.to_dict() for primitive in self.primitives],
            "total_weighted_volume": self.total_weighted_volume,
            "fallback_reason": self.fallback_reason,
            "merge_policy": self.merge_policy,
            "merge_search_policy": self.merge_search_policy,
            "mesh_aabb_volume": self.mesh_aabb_volume,
            "target_primitive_count": self.target_primitive_count,
            "initial_component_count": self.initial_component_count,
            "topology_merge_count": self.topology_merge_count,
            "virtual_component_merge_count": self.virtual_component_merge_count,
            "blocked_merge_count": self.blocked_merge_count,
            "final_component_count": self.final_component_count,
            "excess_volume_threshold_fraction": self.excess_volume_threshold_fraction,
            "normalized_total_weighted_volume": self.normalized_total_weighted_volume,
            "merge_cost_summary": dict(self.merge_cost_summary),
        }


def decompose_mesh(
    mesh: TriangleMesh,
    max_primitives: int,
    primitive_subset: tuple[str, ...],
    *,
    component_merge: str = COMPONENT_MERGE_TOPOLOGY_ONLY,
    merge_search_policy: str = MERGE_SEARCH_TOPOLOGY_THEN_VIRTUAL,
    excess_volume_threshold_fraction: float | None = None,
    report_merge_trace: str = REPORT_MERGE_TRACE_SUMMARY,
) -> CPDLikeDecompositionReport:
    if max_primitives < 1:
        raise ValueError("max_primitives must be at least 1")
    _validate_component_merge_options(
        component_merge=component_merge,
        merge_search_policy=merge_search_policy,
        excess_volume_threshold_fraction=excess_volume_threshold_fraction,
        report_merge_trace=report_merge_trace,
    )
    threshold_fraction = (
        None if excess_volume_threshold_fraction is None else float(excess_volume_threshold_fraction)
    )

    clusters: dict[int, frozenset[int]] = {
        face_index: frozenset({face_index}) for face_index in range(mesh.face_count)
    }
    component_ids: dict[int, frozenset[int]] = {
        face_index: frozenset({face_index}) for face_index in range(mesh.face_count)
    }
    face_adjacency = mesh.adjacent_faces()
    face_connected_component_ids = _face_connected_component_ids(face_adjacency)
    connected_component_ids: dict[int, frozenset[int]] = {
        face_index: frozenset({face_connected_component_ids[face_index]})
        for face_index in range(mesh.face_count)
    }
    fits: dict[int, PrimitiveFit] = {
        cluster_id: _with_merge_metadata(
            fit_best_primitive(mesh, face_ids, primitive_subset),
            component_ids[cluster_id],
        )
        for cluster_id, face_ids in clusters.items()
    }
    mesh_aabb_volume = _mesh_aabb_volume(mesh)
    normalizer_volume = max(mesh_aabb_volume, MIN_NORMALIZATION_VOLUME)
    next_cluster_id = mesh.face_count
    fallback_reason = None
    topology_merge_count = 0
    virtual_component_merge_count = 0
    blocked_merge_count = 0
    accepted_merge_costs: list[float] = []
    blocked_merge_costs: list[float] = []

    while len(clusters) > max_primitives:
        if merge_search_policy == MERGE_SEARCH_COST_GUIDED_PAIRWISE:
            merge_candidate = _best_cost_guided_merge(
                mesh,
                clusters,
                fits,
                component_ids,
                connected_component_ids,
                face_adjacency,
                primitive_subset,
                normalizer_volume,
            )
            if merge_candidate is None:
                fallback_reason = "no_merge_candidates_remaining"
                break
            if (
                merge_candidate.is_virtual_component_merge
                and threshold_fraction is not None
                and merge_candidate.normalized_excess_volume > threshold_fraction
            ):
                fallback_reason = "component_merge_threshold_blocked"
                blocked_merge_count += 1
                blocked_merge_costs.append(merge_candidate.normalized_excess_volume)
                break
            next_cluster_id = _accept_merge(
                merge_candidate,
                clusters,
                fits,
                component_ids,
                connected_component_ids,
                next_cluster_id,
            )
            if merge_candidate.is_virtual_component_merge:
                virtual_component_merge_count += 1
            else:
                topology_merge_count += 1
            accepted_merge_costs.append(merge_candidate.normalized_excess_volume)
            continue

        topology_candidate = _best_merge(
            mesh,
            clusters,
            fits,
            component_ids,
            connected_component_ids,
            face_adjacency,
            primitive_subset,
            normalizer_volume,
            require_adjacency=True,
        )
        if topology_candidate is not None:
            next_cluster_id = _accept_merge(
                topology_candidate,
                clusters,
                fits,
                component_ids,
                connected_component_ids,
                next_cluster_id,
            )
            topology_merge_count += 1
            accepted_merge_costs.append(topology_candidate.normalized_excess_volume)
            continue

        if component_merge != COMPONENT_MERGE_VIRTUAL_PAIRWISE:
            fallback_reason = "no_adjacent_clusters_remaining"
            break

        virtual_candidate = _best_merge(
            mesh,
            clusters,
            fits,
            component_ids,
            connected_component_ids,
            face_adjacency,
            primitive_subset,
            normalizer_volume,
            require_adjacency=False,
        )
        if virtual_candidate is None:
            fallback_reason = "no_component_pairs_remaining"
            break
        if (
            threshold_fraction is not None
            and virtual_candidate.normalized_excess_volume > threshold_fraction
        ):
            fallback_reason = "component_merge_threshold_blocked"
            blocked_merge_count += 1
            blocked_merge_costs.append(virtual_candidate.normalized_excess_volume)
            break
        next_cluster_id = _accept_merge(
            virtual_candidate,
            clusters,
            fits,
            component_ids,
            connected_component_ids,
            next_cluster_id,
        )
        virtual_component_merge_count += 1
        accepted_merge_costs.append(virtual_candidate.normalized_excess_volume)

    primitives = tuple(
        sorted(
            fits.values(),
            key=lambda fit: (fit.source_faces[0], len(fit.source_faces), fit.primitive_type),
        )
    )
    unsupported = tuple(
        dict.fromkeys(
            unsupported
            for primitive in primitives
            for unsupported in primitive.unsupported_primitives
        )
    )
    status = "smoke_passed" if len(primitives) <= max_primitives else "partial"
    total_weighted_volume = float(sum(primitive.weighted_volume for primitive in primitives))
    return CPDLikeDecompositionReport(
        stage=(
            "cpd_like_cost_guided_merge_smoke"
            if merge_search_policy == MERGE_SEARCH_COST_GUIDED_PAIRWISE
            else (
                "cpd_like_component_merge_gate"
                if component_merge == COMPONENT_MERGE_VIRTUAL_PAIRWISE
                else "cpd_like_face_merge"
            )
        ),
        status=status,
        primitive_count=len(primitives),
        max_primitives=max_primitives,
        mesh_point_count=int(mesh.points.shape[0]),
        mesh_face_count=mesh.face_count,
        primitive_subset=tuple(primitive_subset),
        unsupported_primitives=unsupported,
        primitives=primitives,
        total_weighted_volume=total_weighted_volume,
        fallback_reason=fallback_reason,
        merge_policy=component_merge,
        merge_search_policy=merge_search_policy,
        mesh_aabb_volume=mesh_aabb_volume,
        target_primitive_count=max_primitives,
        initial_component_count=mesh.face_count,
        topology_merge_count=topology_merge_count,
        virtual_component_merge_count=virtual_component_merge_count,
        blocked_merge_count=blocked_merge_count,
        final_component_count=len(clusters),
        excess_volume_threshold_fraction=threshold_fraction,
        normalized_total_weighted_volume=float(total_weighted_volume / normalizer_volume),
        merge_cost_summary=_merge_cost_summary(
            accepted_merge_costs,
            blocked_merge_costs,
            normalizer_volume,
            report_merge_trace,
        ),
    )


def _best_merge(
    mesh: TriangleMesh,
    clusters: dict[int, frozenset[int]],
    fits: dict[int, PrimitiveFit],
    component_ids: dict[int, frozenset[int]],
    connected_component_ids: dict[int, frozenset[int]],
    face_adjacency: dict[int, set[int]],
    primitive_subset: tuple[str, ...],
    normalizer_volume: float,
    *,
    require_adjacency: bool,
) -> _MergeCandidate | None:
    best: tuple[float, int, int, _MergeCandidate] | None = None
    cluster_ids = sorted(clusters)
    for left_index, left_id in enumerate(cluster_ids):
        for right_id in cluster_ids[left_index + 1 :]:
            if require_adjacency and not _clusters_are_adjacent(
                clusters[left_id],
                clusters[right_id],
                face_adjacency,
            ):
                continue
            if not require_adjacency and _clusters_are_adjacent(
                clusters[left_id],
                clusters[right_id],
                face_adjacency,
            ):
                continue
            if not require_adjacency and (
                connected_component_ids[left_id] & connected_component_ids[right_id]
            ):
                continue
            merged_faces = clusters[left_id] | clusters[right_id]
            merged_component_ids = component_ids[left_id] | component_ids[right_id]
            merged_fit = fit_best_primitive(
                mesh,
                merged_faces,
                primitive_subset,
            )
            excess_volume = (
                merged_fit.weighted_volume
                - fits[left_id].weighted_volume
                - fits[right_id].weighted_volume
            )
            normalized_excess_volume = float(excess_volume / normalizer_volume)
            candidate_fit = _with_merge_metadata(
                merged_fit,
                merged_component_ids,
                cost_weight=normalized_excess_volume,
            )
            merge_candidate = _MergeCandidate(
                left_id=left_id,
                right_id=right_id,
                merged_fit=candidate_fit,
                excess_volume=float(excess_volume),
                normalized_excess_volume=normalized_excess_volume,
                is_virtual_component_merge=not require_adjacency,
            )
            candidate = (excess_volume, left_id, right_id, merge_candidate)
            if best is None or candidate[:3] < best[:3]:
                best = candidate
    if best is None:
        return None
    return best[3]


def _best_cost_guided_merge(
    mesh: TriangleMesh,
    clusters: dict[int, frozenset[int]],
    fits: dict[int, PrimitiveFit],
    component_ids: dict[int, frozenset[int]],
    connected_component_ids: dict[int, frozenset[int]],
    face_adjacency: dict[int, set[int]],
    primitive_subset: tuple[str, ...],
    normalizer_volume: float,
) -> _MergeCandidate | None:
    topology_candidate = _best_merge(
        mesh,
        clusters,
        fits,
        component_ids,
        connected_component_ids,
        face_adjacency,
        primitive_subset,
        normalizer_volume,
        require_adjacency=True,
    )
    virtual_candidate = _best_merge(
        mesh,
        clusters,
        fits,
        component_ids,
        connected_component_ids,
        face_adjacency,
        primitive_subset,
        normalizer_volume,
        require_adjacency=False,
    )
    candidates = [candidate for candidate in (topology_candidate, virtual_candidate) if candidate]
    if not candidates:
        return None
    return min(
        candidates,
        key=lambda candidate: (
            candidate.normalized_excess_volume,
            int(candidate.is_virtual_component_merge),
            candidate.left_id,
            candidate.right_id,
        ),
    )


def _accept_merge(
    candidate: _MergeCandidate,
    clusters: dict[int, frozenset[int]],
    fits: dict[int, PrimitiveFit],
    component_ids: dict[int, frozenset[int]],
    connected_component_ids: dict[int, frozenset[int]],
    next_cluster_id: int,
) -> int:
    left_id = candidate.left_id
    right_id = candidate.right_id
    merged_faces = clusters[left_id] | clusters[right_id]
    merged_component_ids = component_ids[left_id] | component_ids[right_id]
    merged_connected_component_ids = (
        connected_component_ids[left_id] | connected_component_ids[right_id]
    )
    del clusters[left_id]
    del clusters[right_id]
    del fits[left_id]
    del fits[right_id]
    del component_ids[left_id]
    del component_ids[right_id]
    del connected_component_ids[left_id]
    del connected_component_ids[right_id]
    clusters[next_cluster_id] = merged_faces
    component_ids[next_cluster_id] = merged_component_ids
    connected_component_ids[next_cluster_id] = merged_connected_component_ids
    fits[next_cluster_id] = candidate.merged_fit
    return next_cluster_id + 1


def _clusters_are_adjacent(
    left_faces: frozenset[int],
    right_faces: frozenset[int],
    face_adjacency: dict[int, set[int]],
) -> bool:
    return any(face_adjacency[left_face] & right_faces for left_face in left_faces)


def _face_connected_component_ids(face_adjacency: dict[int, set[int]]) -> dict[int, int]:
    component_ids: dict[int, int] = {}
    next_component_id = 0
    for face_index in sorted(face_adjacency):
        if face_index in component_ids:
            continue
        stack = [face_index]
        while stack:
            current = stack.pop()
            if current in component_ids:
                continue
            component_ids[current] = next_component_id
            stack.extend(sorted(face_adjacency[current] - component_ids.keys(), reverse=True))
        next_component_id += 1
    return component_ids


def _with_merge_metadata(
    fit: PrimitiveFit,
    source_component_ids: frozenset[int],
    *,
    cost_weight: float = 0.0,
) -> PrimitiveFit:
    return replace(
        fit,
        source_component_ids=tuple(sorted(source_component_ids)),
        cost_weight=float(cost_weight),
    )


def _mesh_aabb_volume(mesh: TriangleMesh) -> float:
    extent = mesh.points.max(axis=0) - mesh.points.min(axis=0)
    return float(math.prod(max(float(value), 0.0) for value in extent))


def _merge_cost_summary(
    accepted_costs: list[float],
    blocked_costs: list[float],
    normalizer_volume: float,
    report_merge_trace: str,
) -> dict[str, object]:
    if report_merge_trace == REPORT_MERGE_TRACE_NONE:
        return {}
    return {
        "accepted_merge_count": len(accepted_costs),
        "accepted_normalized_excess_min": _min_or_none(accepted_costs),
        "accepted_normalized_excess_max": _max_or_none(accepted_costs),
        "accepted_normalized_excess_sum": float(sum(accepted_costs)),
        "blocked_merge_count": len(blocked_costs),
        "blocked_normalized_excess_min": _min_or_none(blocked_costs),
        "blocked_normalized_excess_max": _max_or_none(blocked_costs),
        "normalizer_volume": normalizer_volume,
    }


def _min_or_none(values: list[float]) -> float | None:
    return float(min(values)) if values else None


def _max_or_none(values: list[float]) -> float | None:
    return float(max(values)) if values else None


def _validate_component_merge_options(
    *,
    component_merge: str,
    merge_search_policy: str,
    excess_volume_threshold_fraction: float | None,
    report_merge_trace: str,
) -> None:
    if component_merge not in {COMPONENT_MERGE_TOPOLOGY_ONLY, COMPONENT_MERGE_VIRTUAL_PAIRWISE}:
        raise ValueError("component_merge must be topology_only or virtual_pairwise")
    if merge_search_policy not in {
        MERGE_SEARCH_TOPOLOGY_THEN_VIRTUAL,
        MERGE_SEARCH_COST_GUIDED_PAIRWISE,
    }:
        raise ValueError("merge_search_policy must be topology_then_virtual or cost_guided_pairwise")
    if (
        merge_search_policy == MERGE_SEARCH_COST_GUIDED_PAIRWISE
        and component_merge != COMPONENT_MERGE_VIRTUAL_PAIRWISE
    ):
        raise ValueError(
            "merge_search_policy cost_guided_pairwise requires component_merge virtual_pairwise"
        )
    if report_merge_trace not in {REPORT_MERGE_TRACE_SUMMARY, REPORT_MERGE_TRACE_NONE}:
        raise ValueError("report_merge_trace must be summary or none")
    if excess_volume_threshold_fraction is None:
        return
    threshold = float(excess_volume_threshold_fraction)
    if not math.isfinite(threshold) or threshold < 0.0:
        raise ValueError("excess_volume_threshold_fraction must be a finite non-negative number")
