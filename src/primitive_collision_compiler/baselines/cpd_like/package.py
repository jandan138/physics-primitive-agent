from __future__ import annotations

from primitive_collision_compiler.baselines.cpd_like.decompose import CPDLikeDecompositionReport
from primitive_collision_compiler.contracts import CollisionPackage, FallbackSpec, PrimitiveSpec


def package_from_cpd_like_report(
    report: CPDLikeDecompositionReport,
    *,
    asset_id: str,
    source_path: str,
    claim_boundary: str,
    source_sha256: str = "",
    max_source_faces: int | None = None,
) -> CollisionPackage:
    primitives = tuple(
        PrimitiveSpec(
            primitive_id=f"{asset_id}:primitive:{index}",
            kind=fit.primitive_type,
            dimensions=dict(fit.dimensions),
            center=fit.center,
            axes=fit.axes,
            source_faces=fit.source_faces,
            contains_assigned_points=fit.contains_assigned_points,
            volume=fit.volume,
            weighted_volume=fit.weighted_volume,
            conversion_status="candidate",
        )
        for index, fit in enumerate(report.primitives)
    )
    fallback = None
    if report.fallback_reason:
        fallback = FallbackSpec(method="convex_hull", reason=report.fallback_reason)
    return CollisionPackage(
        package_id=f"{asset_id}:{report.stage}",
        asset_id=asset_id,
        source_path=source_path,
        source_sha256=source_sha256,
        method="cpd_like_baseline",
        stage=report.stage,
        status=report.status,
        claim_boundary=claim_boundary,
        mesh_point_count=report.mesh_point_count,
        mesh_face_count=report.mesh_face_count,
        max_source_faces=max_source_faces,
        primitive_subset=report.primitive_subset,
        unsupported_primitives=report.unsupported_primitives,
        primitives=primitives,
        fallback=fallback,
    )
