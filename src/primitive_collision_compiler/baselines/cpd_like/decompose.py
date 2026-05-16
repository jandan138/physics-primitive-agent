from __future__ import annotations

from dataclasses import dataclass, replace
import math
from typing import Mapping

from primitive_collision_compiler.baselines.cpd_like.primitives import PrimitiveFit, fit_best_primitive
from primitive_collision_compiler.geometry.mesh import TriangleMesh

COMPONENT_MERGE_TOPOLOGY_ONLY = "topology_only"
COMPONENT_MERGE_VIRTUAL_PAIRWISE = "virtual_pairwise"
MERGE_SEARCH_TOPOLOGY_THEN_VIRTUAL = "topology_then_virtual"
MERGE_SEARCH_COST_GUIDED_PAIRWISE = "cost_guided_pairwise"
MERGE_SEARCH_TWO_STEP_LOOKAHEAD = "two_step_lookahead"
REPORT_MERGE_TRACE_SUMMARY = "summary"
REPORT_MERGE_TRACE_STEPS = "steps"
REPORT_MERGE_TRACE_NONE = "none"
MIN_NORMALIZATION_VOLUME = 1e-12
TWO_STEP_LOOKAHEAD_MAX_FACE_COUNT = 6


@dataclass(frozen=True)
class _MergeCandidate:
    left_id: int
    right_id: int
    merged_fit: PrimitiveFit
    excess_volume: float
    normalized_excess_volume: float
    is_virtual_component_merge: bool
    projected_followup_normalized_excess_volume: float | None = None
    projected_total_normalized_excess_volume: float | None = None


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
    merge_trace: tuple[dict[str, object], ...]
    primitive_score_multipliers: dict[str, float]

    def to_dict(self) -> dict[str, object]:
        payload = {
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
        if self.merge_trace:
            payload["merge_trace"] = [dict(step) for step in self.merge_trace]
        if self.primitive_score_multipliers:
            payload["primitive_score_multipliers"] = dict(self.primitive_score_multipliers)
        return payload


def decompose_mesh(
    mesh: TriangleMesh,
    max_primitives: int,
    primitive_subset: tuple[str, ...],
    *,
    component_merge: str = COMPONENT_MERGE_TOPOLOGY_ONLY,
    merge_search_policy: str = MERGE_SEARCH_TOPOLOGY_THEN_VIRTUAL,
    excess_volume_threshold_fraction: float | None = None,
    report_merge_trace: str = REPORT_MERGE_TRACE_SUMMARY,
    primitive_score_multipliers: Mapping[str, float] | None = None,
) -> CPDLikeDecompositionReport:
    if max_primitives < 1:
        raise ValueError("max_primitives must be at least 1")
    _validate_component_merge_options(
        component_merge=component_merge,
        merge_search_policy=merge_search_policy,
        excess_volume_threshold_fraction=excess_volume_threshold_fraction,
        report_merge_trace=report_merge_trace,
    )
    if (
        merge_search_policy == MERGE_SEARCH_TWO_STEP_LOOKAHEAD
        and mesh.face_count > TWO_STEP_LOOKAHEAD_MAX_FACE_COUNT
    ):
        raise ValueError(
            "two_step_lookahead supports at most 6 faces in this synthetic diagnostic"
        )
    threshold_fraction = (
        None if excess_volume_threshold_fraction is None else float(excess_volume_threshold_fraction)
    )
    score_multipliers = _validated_primitive_score_multipliers(primitive_score_multipliers)

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
            _fit_best_primitive_with_optional_scores(
                mesh,
                face_ids,
                primitive_subset,
                primitive_score_multipliers=score_multipliers,
            ),
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
    accepted_eq4_costs: list[float] = []
    blocked_eq4_costs: list[float] = []
    merge_trace: list[dict[str, object]] = []

    while len(clusters) > max_primitives:
        if merge_search_policy in {
            MERGE_SEARCH_COST_GUIDED_PAIRWISE,
            MERGE_SEARCH_TWO_STEP_LOOKAHEAD,
        }:
            if merge_search_policy == MERGE_SEARCH_TWO_STEP_LOOKAHEAD:
                merge_candidate = _best_two_step_lookahead_merge(
                    mesh,
                    clusters,
                    fits,
                    component_ids,
                    connected_component_ids,
                    face_adjacency,
                    primitive_subset,
                    normalizer_volume,
                    primitive_score_multipliers=score_multipliers,
                    max_primitives=max_primitives,
                    next_cluster_id=next_cluster_id,
                )
            else:
                merge_candidate = _best_cost_guided_merge(
                    mesh,
                    clusters,
                    fits,
                    component_ids,
                    connected_component_ids,
                    face_adjacency,
                    primitive_subset,
                    normalizer_volume,
                    primitive_score_multipliers=score_multipliers,
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
                blocked_eq4_costs.append(merge_candidate.excess_volume)
                _append_merge_trace(
                    merge_trace,
                    report_merge_trace=report_merge_trace,
                    candidate=merge_candidate,
                    clusters=clusters,
                    fits=fits,
                    component_ids=component_ids,
                    connected_component_ids=connected_component_ids,
                    decision="blocked",
                    blocked_reason=fallback_reason,
                )
                break
            _append_merge_trace(
                merge_trace,
                report_merge_trace=report_merge_trace,
                candidate=merge_candidate,
                clusters=clusters,
                fits=fits,
                component_ids=component_ids,
                connected_component_ids=connected_component_ids,
                decision="accepted",
            )
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
            accepted_eq4_costs.append(merge_candidate.excess_volume)
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
            primitive_score_multipliers=score_multipliers,
            require_adjacency=True,
        )
        if topology_candidate is not None:
            _append_merge_trace(
                merge_trace,
                report_merge_trace=report_merge_trace,
                candidate=topology_candidate,
                clusters=clusters,
                fits=fits,
                component_ids=component_ids,
                connected_component_ids=connected_component_ids,
                decision="accepted",
            )
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
            accepted_eq4_costs.append(topology_candidate.excess_volume)
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
            primitive_score_multipliers=score_multipliers,
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
            blocked_eq4_costs.append(virtual_candidate.excess_volume)
            _append_merge_trace(
                merge_trace,
                report_merge_trace=report_merge_trace,
                candidate=virtual_candidate,
                clusters=clusters,
                fits=fits,
                component_ids=component_ids,
                connected_component_ids=connected_component_ids,
                decision="blocked",
                blocked_reason=fallback_reason,
            )
            break
        _append_merge_trace(
            merge_trace,
            report_merge_trace=report_merge_trace,
            candidate=virtual_candidate,
            clusters=clusters,
            fits=fits,
            component_ids=component_ids,
            connected_component_ids=connected_component_ids,
            decision="accepted",
        )
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
        accepted_eq4_costs.append(virtual_candidate.excess_volume)

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
            if merge_search_policy
            in {MERGE_SEARCH_COST_GUIDED_PAIRWISE, MERGE_SEARCH_TWO_STEP_LOOKAHEAD}
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
            accepted_eq4_costs,
            blocked_eq4_costs,
            normalizer_volume,
            report_merge_trace,
        ),
        merge_trace=tuple(merge_trace),
        primitive_score_multipliers=score_multipliers,
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
    primitive_score_multipliers: Mapping[str, float],
    *,
    require_adjacency: bool,
) -> _MergeCandidate | None:
    candidates = _all_merge_candidates(
        mesh,
        clusters,
        fits,
        component_ids,
        connected_component_ids,
        face_adjacency,
        primitive_subset,
        normalizer_volume,
        primitive_score_multipliers=primitive_score_multipliers,
        require_adjacency=require_adjacency,
    )
    if not candidates:
        return None
    return min(
        candidates,
        key=lambda candidate: (
            candidate.excess_volume,
            candidate.left_id,
            candidate.right_id,
        ),
    )


def _all_merge_candidates(
    mesh: TriangleMesh,
    clusters: dict[int, frozenset[int]],
    fits: dict[int, PrimitiveFit],
    component_ids: dict[int, frozenset[int]],
    connected_component_ids: dict[int, frozenset[int]],
    face_adjacency: dict[int, set[int]],
    primitive_subset: tuple[str, ...],
    normalizer_volume: float,
    primitive_score_multipliers: Mapping[str, float],
    *,
    require_adjacency: bool | None,
) -> list[_MergeCandidate]:
    candidates: list[_MergeCandidate] = []
    cluster_ids = sorted(clusters)
    for left_index, left_id in enumerate(cluster_ids):
        for right_id in cluster_ids[left_index + 1 :]:
            clusters_are_adjacent = _clusters_are_adjacent(
                clusters[left_id],
                clusters[right_id],
                face_adjacency,
            )
            if require_adjacency is True and not clusters_are_adjacent:
                continue
            if require_adjacency is False and clusters_are_adjacent:
                continue
            if not clusters_are_adjacent and (
                connected_component_ids[left_id] & connected_component_ids[right_id]
            ):
                continue
            merged_faces = clusters[left_id] | clusters[right_id]
            merged_component_ids = component_ids[left_id] | component_ids[right_id]
            merged_fit = _fit_best_primitive_with_optional_scores(
                mesh,
                merged_faces,
                primitive_subset,
                primitive_score_multipliers=primitive_score_multipliers,
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
            candidates.append(
                _MergeCandidate(
                    left_id=left_id,
                    right_id=right_id,
                    merged_fit=candidate_fit,
                    excess_volume=float(excess_volume),
                    normalized_excess_volume=normalized_excess_volume,
                    is_virtual_component_merge=not clusters_are_adjacent,
                )
            )
    return candidates


def _best_cost_guided_merge(
    mesh: TriangleMesh,
    clusters: dict[int, frozenset[int]],
    fits: dict[int, PrimitiveFit],
    component_ids: dict[int, frozenset[int]],
    connected_component_ids: dict[int, frozenset[int]],
    face_adjacency: dict[int, set[int]],
    primitive_subset: tuple[str, ...],
    normalizer_volume: float,
    primitive_score_multipliers: Mapping[str, float],
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
        primitive_score_multipliers=primitive_score_multipliers,
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
        primitive_score_multipliers=primitive_score_multipliers,
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


def _best_two_step_lookahead_merge(
    mesh: TriangleMesh,
    clusters: dict[int, frozenset[int]],
    fits: dict[int, PrimitiveFit],
    component_ids: dict[int, frozenset[int]],
    connected_component_ids: dict[int, frozenset[int]],
    face_adjacency: dict[int, set[int]],
    primitive_subset: tuple[str, ...],
    normalizer_volume: float,
    primitive_score_multipliers: Mapping[str, float],
    *,
    max_primitives: int,
    next_cluster_id: int,
) -> _MergeCandidate | None:
    candidates = _all_merge_candidates(
        mesh,
        clusters,
        fits,
        component_ids,
        connected_component_ids,
        face_adjacency,
        primitive_subset,
        normalizer_volume,
        primitive_score_multipliers=primitive_score_multipliers,
        require_adjacency=None,
    )
    if not candidates:
        return None

    scored_candidates: list[tuple[float, float, int, int, int, _MergeCandidate]] = []
    for candidate in candidates:
        projected_followup = _projected_followup_merge(
            candidate,
            mesh=mesh,
            clusters=clusters,
            fits=fits,
            component_ids=component_ids,
            connected_component_ids=connected_component_ids,
            face_adjacency=face_adjacency,
            primitive_subset=primitive_subset,
            normalizer_volume=normalizer_volume,
            primitive_score_multipliers=primitive_score_multipliers,
            max_primitives=max_primitives,
            next_cluster_id=next_cluster_id,
        )
        followup_cost = (
            None if projected_followup is None else projected_followup.normalized_excess_volume
        )
        projected_total = candidate.normalized_excess_volume + (
            0.0 if followup_cost is None else followup_cost
        )
        annotated = replace(
            candidate,
            projected_followup_normalized_excess_volume=followup_cost,
            projected_total_normalized_excess_volume=projected_total,
        )
        scored_candidates.append(
            (
                projected_total,
                candidate.normalized_excess_volume,
                int(candidate.is_virtual_component_merge),
                candidate.left_id,
                candidate.right_id,
                annotated,
            )
        )
    return min(scored_candidates, key=lambda row: row[:5])[5]


def _projected_followup_merge(
    candidate: _MergeCandidate,
    *,
    mesh: TriangleMesh,
    clusters: dict[int, frozenset[int]],
    fits: dict[int, PrimitiveFit],
    component_ids: dict[int, frozenset[int]],
    connected_component_ids: dict[int, frozenset[int]],
    face_adjacency: dict[int, set[int]],
    primitive_subset: tuple[str, ...],
    normalizer_volume: float,
    primitive_score_multipliers: Mapping[str, float],
    max_primitives: int,
    next_cluster_id: int,
) -> _MergeCandidate | None:
    projected_clusters = dict(clusters)
    projected_fits = dict(fits)
    projected_component_ids = dict(component_ids)
    projected_connected_component_ids = dict(connected_component_ids)
    projected_next_cluster_id = _accept_merge(
        candidate,
        projected_clusters,
        projected_fits,
        projected_component_ids,
        projected_connected_component_ids,
        next_cluster_id,
    )
    if len(projected_clusters) <= max_primitives:
        return None
    return _best_two_step_followup_candidate(
        mesh,
        projected_clusters,
        projected_fits,
        projected_component_ids,
        projected_connected_component_ids,
        face_adjacency,
        primitive_subset,
        normalizer_volume,
        primitive_score_multipliers=primitive_score_multipliers,
        next_cluster_id=projected_next_cluster_id,
    )


def _best_two_step_followup_candidate(
    mesh: TriangleMesh,
    clusters: dict[int, frozenset[int]],
    fits: dict[int, PrimitiveFit],
    component_ids: dict[int, frozenset[int]],
    connected_component_ids: dict[int, frozenset[int]],
    face_adjacency: dict[int, set[int]],
    primitive_subset: tuple[str, ...],
    normalizer_volume: float,
    primitive_score_multipliers: Mapping[str, float],
    *,
    next_cluster_id: int,
) -> _MergeCandidate | None:
    del next_cluster_id
    candidates = _all_merge_candidates(
        mesh,
        clusters,
        fits,
        component_ids,
        connected_component_ids,
        face_adjacency,
        primitive_subset,
        normalizer_volume,
        primitive_score_multipliers=primitive_score_multipliers,
        require_adjacency=None,
    )
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


def _append_merge_trace(
    trace: list[dict[str, object]],
    *,
    report_merge_trace: str,
    candidate: _MergeCandidate,
    clusters: dict[int, frozenset[int]],
    fits: dict[int, PrimitiveFit],
    component_ids: dict[int, frozenset[int]],
    connected_component_ids: dict[int, frozenset[int]],
    decision: str,
    blocked_reason: str | None = None,
) -> None:
    if report_merge_trace != REPORT_MERGE_TRACE_STEPS:
        return
    left_id = candidate.left_id
    right_id = candidate.right_id
    left_faces = clusters[left_id]
    right_faces = clusters[right_id]
    left_components = component_ids[left_id]
    right_components = component_ids[right_id]
    left_connected_components = connected_component_ids[left_id]
    right_connected_components = connected_component_ids[right_id]
    row = {
        "step_index": len(trace) + 1,
        "decision": decision,
        "blocked_reason": blocked_reason,
        "merge_kind": (
            "virtual_component" if candidate.is_virtual_component_merge else "topology"
        ),
        "left_cluster_id": left_id,
        "right_cluster_id": right_id,
        "left_source_faces": sorted(left_faces),
        "right_source_faces": sorted(right_faces),
        "merged_source_faces": sorted(left_faces | right_faces),
        "left_source_component_ids": sorted(left_components),
        "right_source_component_ids": sorted(right_components),
        "merged_source_component_ids": sorted(left_components | right_components),
        "left_connected_component_ids": sorted(left_connected_components),
        "right_connected_component_ids": sorted(right_connected_components),
        "merged_connected_component_ids": sorted(
            left_connected_components | right_connected_components
        ),
        "merged_primitive_type": candidate.merged_fit.primitive_type,
        "left_weighted_volume": fits[left_id].weighted_volume,
        "right_weighted_volume": fits[right_id].weighted_volume,
        "merged_weighted_volume": candidate.merged_fit.weighted_volume,
        "excess_volume": candidate.excess_volume,
        "normalized_excess_volume": candidate.normalized_excess_volume,
    }
    if candidate.projected_followup_normalized_excess_volume is not None:
        row["projected_followup_normalized_excess_volume"] = (
            candidate.projected_followup_normalized_excess_volume
        )
    if candidate.projected_total_normalized_excess_volume is not None:
        row["projected_total_normalized_excess_volume"] = (
            candidate.projected_total_normalized_excess_volume
        )
    trace.append(row)


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


def _fit_best_primitive_with_optional_scores(
    mesh: TriangleMesh,
    face_ids: frozenset[int],
    primitive_subset: tuple[str, ...],
    *,
    primitive_score_multipliers: Mapping[str, float],
) -> PrimitiveFit:
    if not primitive_score_multipliers:
        return fit_best_primitive(mesh, face_ids, primitive_subset)
    return fit_best_primitive(
        mesh,
        face_ids,
        primitive_subset,
        primitive_score_multipliers=primitive_score_multipliers,
    )


def _validated_primitive_score_multipliers(
    primitive_score_multipliers: Mapping[str, float] | None,
) -> dict[str, float]:
    if primitive_score_multipliers is None:
        return {}
    multipliers: dict[str, float] = {}
    for primitive_type, multiplier in primitive_score_multipliers.items():
        value = float(multiplier)
        if not math.isfinite(value) or value <= 0.0:
            raise ValueError("primitive score multipliers must be finite and positive")
        multipliers[str(primitive_type)] = value
    return multipliers


def _merge_cost_summary(
    accepted_costs: list[float],
    blocked_costs: list[float],
    accepted_eq4_costs: list[float],
    blocked_eq4_costs: list[float],
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
        "accepted_eq4_cost_min": _min_or_none(accepted_eq4_costs),
        "accepted_eq4_cost_max": _max_or_none(accepted_eq4_costs),
        "accepted_eq4_cost_sum": float(sum(accepted_eq4_costs)),
        "blocked_merge_count": len(blocked_costs),
        "blocked_normalized_excess_min": _min_or_none(blocked_costs),
        "blocked_normalized_excess_max": _max_or_none(blocked_costs),
        "blocked_eq4_cost_min": _min_or_none(blocked_eq4_costs),
        "blocked_eq4_cost_max": _max_or_none(blocked_eq4_costs),
        "blocked_eq4_cost_sum": float(sum(blocked_eq4_costs)),
        "normalizer_volume": normalizer_volume,
        "normalization": {
            "kind": "source_mesh_aabb_volume",
            "floor": MIN_NORMALIZATION_VOLUME,
            "normalizer_volume": normalizer_volume,
            "applied_to": [
                "accepted_normalized_excess",
                "blocked_normalized_excess",
                "excess_volume_threshold_fraction",
            ],
        },
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
        MERGE_SEARCH_TWO_STEP_LOOKAHEAD,
    }:
        raise ValueError(
            "merge_search_policy must be topology_then_virtual, cost_guided_pairwise, "
            "or two_step_lookahead"
        )
    if (
        merge_search_policy
        in {MERGE_SEARCH_COST_GUIDED_PAIRWISE, MERGE_SEARCH_TWO_STEP_LOOKAHEAD}
        and component_merge != COMPONENT_MERGE_VIRTUAL_PAIRWISE
    ):
        raise ValueError(
            f"merge_search_policy {merge_search_policy} requires component_merge virtual_pairwise"
        )
    if report_merge_trace not in {
        REPORT_MERGE_TRACE_SUMMARY,
        REPORT_MERGE_TRACE_STEPS,
        REPORT_MERGE_TRACE_NONE,
    }:
        raise ValueError("report_merge_trace must be summary, steps, or none")
    if excess_volume_threshold_fraction is None:
        return
    threshold = float(excess_volume_threshold_fraction)
    if not math.isfinite(threshold) or threshold < 0.0:
        raise ValueError("excess_volume_threshold_fraction must be a finite non-negative number")
