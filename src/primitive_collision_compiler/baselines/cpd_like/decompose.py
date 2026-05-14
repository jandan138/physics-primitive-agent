from __future__ import annotations

from dataclasses import dataclass

from primitive_collision_compiler.baselines.cpd_like.primitives import PrimitiveFit, fit_best_primitive
from primitive_collision_compiler.geometry.mesh import TriangleMesh


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
        }


def decompose_mesh(
    mesh: TriangleMesh,
    max_primitives: int,
    primitive_subset: tuple[str, ...],
) -> CPDLikeDecompositionReport:
    if max_primitives < 1:
        raise ValueError("max_primitives must be at least 1")

    clusters: dict[int, frozenset[int]] = {
        face_index: frozenset({face_index}) for face_index in range(mesh.face_count)
    }
    fits: dict[int, PrimitiveFit] = {
        cluster_id: fit_best_primitive(mesh, face_ids, primitive_subset)
        for cluster_id, face_ids in clusters.items()
    }
    face_adjacency = mesh.adjacent_faces()
    next_cluster_id = mesh.face_count
    fallback_reason = None

    while len(clusters) > max_primitives:
        merge = _best_merge(mesh, clusters, fits, face_adjacency, primitive_subset)
        if merge is None:
            fallback_reason = "no_adjacent_clusters_remaining"
            break
        left_id, right_id, merged_fit = merge
        merged_faces = clusters[left_id] | clusters[right_id]
        del clusters[left_id]
        del clusters[right_id]
        del fits[left_id]
        del fits[right_id]
        clusters[next_cluster_id] = merged_faces
        fits[next_cluster_id] = merged_fit
        next_cluster_id += 1

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
    return CPDLikeDecompositionReport(
        stage="cpd_like_face_merge",
        status=status,
        primitive_count=len(primitives),
        max_primitives=max_primitives,
        mesh_point_count=int(mesh.points.shape[0]),
        mesh_face_count=mesh.face_count,
        primitive_subset=tuple(primitive_subset),
        unsupported_primitives=unsupported,
        primitives=primitives,
        total_weighted_volume=float(sum(primitive.weighted_volume for primitive in primitives)),
        fallback_reason=fallback_reason,
    )


def _best_merge(
    mesh: TriangleMesh,
    clusters: dict[int, frozenset[int]],
    fits: dict[int, PrimitiveFit],
    face_adjacency: dict[int, set[int]],
    primitive_subset: tuple[str, ...],
) -> tuple[int, int, PrimitiveFit] | None:
    best: tuple[float, int, int, PrimitiveFit] | None = None
    cluster_ids = sorted(clusters)
    for left_index, left_id in enumerate(cluster_ids):
        for right_id in cluster_ids[left_index + 1 :]:
            if not _clusters_are_adjacent(clusters[left_id], clusters[right_id], face_adjacency):
                continue
            merged_fit = fit_best_primitive(
                mesh,
                clusters[left_id] | clusters[right_id],
                primitive_subset,
            )
            excess_volume = (
                merged_fit.weighted_volume
                - fits[left_id].weighted_volume
                - fits[right_id].weighted_volume
            )
            candidate = (excess_volume, left_id, right_id, merged_fit)
            if best is None or candidate[:3] < best[:3]:
                best = candidate
    if best is None:
        return None
    _, left_id, right_id, merged_fit = best
    return left_id, right_id, merged_fit


def _clusters_are_adjacent(
    left_faces: frozenset[int],
    right_faces: frozenset[int],
    face_adjacency: dict[int, set[int]],
) -> bool:
    return any(face_adjacency[left_face] & right_faces for left_face in left_faces)
