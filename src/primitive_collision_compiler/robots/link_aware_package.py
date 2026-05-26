from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np

from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec

LINK_AWARE_PACKAGE_CLAIM_BOUNDARY = (
    "link_aware_robot_package_generation_not_whole_robot_collision_quality_or_safety_validation"
)
LINK_BOUNDARY_AUDIT_CLAIM_BOUNDARY = (
    "link_boundary_audit_not_whole_robot_collision_quality_or_safety_validation"
)
LINK_AWARE_PACKAGE_EVIDENCE_LEVEL = "phase0_link_aware_robot_package_smoke"
MESHLESS_LINK_PLACEHOLDER_STATUS = "placeholder_meshless_link"
MESHLESS_LINK_PLACEHOLDER_HALF_EXTENT = 0.001


@dataclass(frozen=True)
class RobotLinkSummary:
    link_path: str
    mesh_paths: tuple[str, ...]
    primitive_count: int
    placeholder_primitive_count: int = 0

    def to_dict(self) -> dict[str, object]:
        return {
            "link_path": self.link_path,
            "mesh_paths": list(self.mesh_paths),
            "primitive_count": self.primitive_count,
            "placeholder_primitive_count": self.placeholder_primitive_count,
        }


@dataclass(frozen=True)
class RobotLinkPackageReport:
    status: str
    package: CollisionPackage
    links: tuple[RobotLinkSummary, ...]
    joint_edges: tuple[dict[str, object], ...]
    audit: dict[str, object]

    def to_dict(self) -> dict[str, object]:
        return {
            "stage": "phase0_link_aware_robot_package_generation",
            "status": self.status,
            "outcome": _outcome_for_status(self.status),
            "primitive_or_hull_count": len(self.package.primitives),
            "collision_package": self.package.to_dict(),
            "links": [link.to_dict() for link in self.links],
            "joint_edges": [dict(edge) for edge in self.joint_edges],
            "link_boundary_audit": self.audit,
            "claim_boundary": LINK_AWARE_PACKAGE_CLAIM_BOUNDARY,
            "evidence_level": LINK_AWARE_PACKAGE_EVIDENCE_LEVEL,
            "fallback_reason": None if self.status == "generated" else self.status,
        }


def build_link_aware_robot_package(
    *,
    asset_path: str | Path,
    asset_id: str,
    source_sha256: str = "",
) -> RobotLinkPackageReport:
    try:
        from pxr import Gf, Usd, UsdGeom, UsdPhysics
    except ModuleNotFoundError as exc:
        package = _empty_package(asset_id, str(asset_path), source_sha256, status="dependency_gap")
        audit = audit_link_boundaries(package, link_paths=())
        return RobotLinkPackageReport(
            status="dependency_gap",
            package=package,
            links=(),
            joint_edges=(),
            audit={**audit, "status": "dependency_gap", "outcome": "dependency_gap", "fallback_reason": str(exc)},
        )

    path = Path(asset_path)
    if not path.exists():
        raise FileNotFoundError(path)
    stage = Usd.Stage.Open(str(path))
    if stage is None:
        raise ValueError(f"usd_open_failed: {path}")

    link_paths = _discover_link_paths(stage, UsdPhysics)
    joint_edges = _discover_joint_edges(stage, UsdPhysics)
    link_mesh_points: dict[str, list[np.ndarray]] = {link_path: [] for link_path in link_paths}
    link_mesh_paths: dict[str, list[str]] = {link_path: [] for link_path in link_paths}
    xform_cache = UsdGeom.XformCache()
    link_to_world = {
        link_path: xform_cache.GetLocalToWorldTransform(stage.GetPrimAtPath(link_path))
        for link_path in link_paths
    }
    for prim in stage.Traverse():
        if not prim.IsA(UsdGeom.Mesh):
            continue
        link_path = _nearest_ancestor_link(str(prim.GetPath()), link_paths)
        if link_path is None:
            continue
        mesh = UsdGeom.Mesh(prim)
        points = _mesh_points_in_link_frame(
            mesh,
            mesh_to_world=xform_cache.GetLocalToWorldTransform(prim),
            link_to_world=link_to_world[link_path],
            gf=Gf,
        )
        if points.size == 0:
            continue
        link_mesh_points[link_path].append(points)
        link_mesh_paths[link_path].append(str(prim.GetPath()))

    primitives: list[PrimitiveSpec] = []
    links: list[RobotLinkSummary] = []
    for link_path in link_paths:
        mesh_paths = tuple(link_mesh_paths[link_path])
        point_blocks = link_mesh_points[link_path]
        primitive_count = 0
        placeholder_primitive_count = 0
        if point_blocks:
            points = np.concatenate(point_blocks, axis=0)
            primitives.append(_box_primitive_for_link(asset_id, link_path, len(primitives), points))
            primitive_count = 1
        else:
            primitives.append(_meshless_placeholder_primitive(asset_id, link_path, len(primitives)))
            primitive_count = 1
            placeholder_primitive_count = 1
        links.append(
            RobotLinkSummary(
                link_path=link_path,
                mesh_paths=mesh_paths,
                primitive_count=primitive_count,
                placeholder_primitive_count=placeholder_primitive_count,
            )
        )

    package = CollisionPackage(
        package_id=f"{asset_id}:phase0_link_aware_bbox",
        asset_id=asset_id,
        source_path=str(path),
        source_sha256=source_sha256,
        method="link_aware_bounding_boxes",
        stage="phase0_link_aware_robot_package_generation",
        status="smoke_passed" if primitives else "fallback",
        claim_boundary=LINK_AWARE_PACKAGE_CLAIM_BOUNDARY,
        primitive_subset=("box",),
        primitives=tuple(primitives),
    )
    audit = audit_link_boundaries(package, link_paths=tuple(link_paths))
    status = "generated" if primitives and audit["status"] == "smoke_passed" else "fallback"
    return RobotLinkPackageReport(
        status=status,
        package=package,
        links=tuple(links),
        joint_edges=joint_edges,
        audit=audit,
    )


def audit_link_boundaries(
    package: CollisionPackage,
    *,
    link_paths: Sequence[str],
) -> dict[str, object]:
    link_set = {str(path) for path in link_paths}
    per_link = {str(path): 0 for path in link_paths}
    cross_link_merge_count = 0
    missing_link_count = 0
    unknown_link_count = 0
    mismatched_frame_count = 0
    meshless_link_placeholder_count = 0

    for primitive in package.primitives:
        source_links = tuple(str(link) for link in primitive.source_links)
        if len(source_links) != 1:
            cross_link_merge_count += 1 if len(source_links) > 1 else 0
            missing_link_count += 1 if not source_links else 0
            continue
        link_path = source_links[0]
        if link_path not in link_set:
            unknown_link_count += 1
            continue
        if primitive.frame != link_path:
            mismatched_frame_count += 1
            continue
        per_link[link_path] += 1
        if primitive.conversion_status == MESHLESS_LINK_PLACEHOLDER_STATUS:
            meshless_link_placeholder_count += 1

    links_without_primitives = [
        link_path for link_path, primitive_count in per_link.items() if primitive_count == 0
    ]

    failure_labels: list[str] = []
    if cross_link_merge_count:
        failure_labels.append("cross_link_primitive_merge")
    if missing_link_count:
        failure_labels.append("primitive_missing_source_link")
    if unknown_link_count:
        failure_labels.append("primitive_unknown_source_link")
    if mismatched_frame_count:
        failure_labels.append("primitive_frame_source_link_mismatch")
    if links_without_primitives:
        failure_labels.append("link_without_primitive")
    if not link_paths:
        failure_labels.append("no_robot_links_detected")
    if not package.primitives:
        failure_labels.append("no_link_primitives_generated")

    status = "smoke_passed" if not failure_labels else "runtime_failure"
    return {
        "stage": "phase0_link_boundary_audit",
        "status": status,
        "probe_type": "link_boundary_audit",
        "outcome": "accept" if status == "smoke_passed" else "failure",
        "metrics": {
            "link_aware_package_generated": bool(package.primitives),
            "link_count": len(link_paths),
            "primitive_count": len(package.primitives),
            "cross_link_merge_count": cross_link_merge_count,
            "missing_link_primitive_count": missing_link_count,
            "unknown_link_primitive_count": unknown_link_count,
            "mismatched_frame_primitive_count": mismatched_frame_count,
            "links_without_primitive_count": len(links_without_primitives),
            "links_without_primitives": links_without_primitives,
            "meshless_link_placeholder_count": meshless_link_placeholder_count,
            "per_link_primitive_count": per_link,
        },
        "failure_labels": failure_labels,
        "claim_boundary": LINK_BOUNDARY_AUDIT_CLAIM_BOUNDARY,
        "evidence_level": LINK_AWARE_PACKAGE_EVIDENCE_LEVEL,
        "fallback_reason": None if status == "smoke_passed" else "link_boundary_audit_failed",
    }


def _discover_link_paths(stage: Any, usd_physics: Any) -> tuple[str, ...]:
    links = [
        str(prim.GetPath())
        for prim in stage.Traverse()
        if prim.HasAPI(usd_physics.RigidBodyAPI)
    ]
    return tuple(sorted(links, key=lambda value: (value.count("/"), value)))


def _discover_joint_edges(stage: Any, usd_physics: Any) -> tuple[dict[str, object], ...]:
    edges: list[dict[str, object]] = []
    for prim in stage.Traverse():
        if not prim.IsA(usd_physics.Joint):
            continue
        edges.append(
            {
                "joint_path": str(prim.GetPath()),
                "joint_type": str(prim.GetTypeName()),
                "body0": _relationship_target(prim, "physics:body0"),
                "body1": _relationship_target(prim, "physics:body1"),
            }
        )
    return tuple(edges)


def _relationship_target(prim: Any, name: str) -> str | None:
    targets = prim.GetRelationship(name).GetTargets()
    if not targets:
        return None
    return str(targets[0])


def _nearest_ancestor_link(prim_path: str, link_paths: Sequence[str]) -> str | None:
    candidates = [
        link_path
        for link_path in link_paths
        if prim_path == link_path or prim_path.startswith(f"{link_path}/")
    ]
    if not candidates:
        return None
    return max(candidates, key=len)


def _mesh_points_in_link_frame(
    mesh: Any,
    *,
    mesh_to_world: Any,
    link_to_world: Any,
    gf: Any,
) -> np.ndarray:
    points_attr = mesh.GetPointsAttr().Get()
    if points_attr is None:
        return np.empty((0, 3), dtype=np.float64)
    world_to_link = link_to_world.GetInverse()
    transformed = [
        world_to_link.Transform(
            mesh_to_world.Transform(
                gf.Vec3d(float(point[0]), float(point[1]), float(point[2]))
            )
        )
        for point in points_attr
    ]
    return np.asarray([[float(coord) for coord in point] for point in transformed], dtype=np.float64)


def _box_primitive_for_link(
    asset_id: str,
    link_path: str,
    index: int,
    points: np.ndarray,
) -> PrimitiveSpec:
    bounds_min = np.min(points, axis=0)
    bounds_max = np.max(points, axis=0)
    half_extents = np.maximum((bounds_max - bounds_min) * 0.5, 1.0e-6)
    center = (bounds_min + bounds_max) * 0.5
    link_id = link_path.strip("/").replace("/", "_")
    volume = float(8.0 * half_extents[0] * half_extents[1] * half_extents[2])
    return PrimitiveSpec(
        primitive_id=f"{asset_id}:{link_id}:primitive:{index}",
        kind="box",
        dimensions={"half_extents": [float(value) for value in half_extents]},
        center=tuple(float(value) for value in center),
        frame=link_path,
        source_links=(link_path,),
        volume=volume,
        weighted_volume=volume,
        conversion_status="candidate",
    )


def _meshless_placeholder_primitive(asset_id: str, link_path: str, index: int) -> PrimitiveSpec:
    link_id = link_path.strip("/").replace("/", "_")
    half_extents = [MESHLESS_LINK_PLACEHOLDER_HALF_EXTENT] * 3
    volume = float(8.0 * half_extents[0] * half_extents[1] * half_extents[2])
    return PrimitiveSpec(
        primitive_id=f"{asset_id}:{link_id}:primitive:{index}:meshless_placeholder",
        kind="box",
        dimensions={"half_extents": half_extents},
        center=(0.0, 0.0, 0.0),
        frame=link_path,
        source_links=(link_path,),
        contains_assigned_points=False,
        volume=volume,
        weighted_volume=volume,
        conversion_status=MESHLESS_LINK_PLACEHOLDER_STATUS,
    )


def _empty_package(
    asset_id: str,
    source_path: str,
    source_sha256: str,
    *,
    status: str,
) -> CollisionPackage:
    return CollisionPackage(
        package_id=f"{asset_id}:phase0_link_aware_bbox",
        asset_id=asset_id,
        source_path=source_path,
        source_sha256=source_sha256,
        method="link_aware_bounding_boxes",
        stage="phase0_link_aware_robot_package_generation",
        status=status,
        claim_boundary=LINK_AWARE_PACKAGE_CLAIM_BOUNDARY,
        primitive_subset=("box",),
    )


def _outcome_for_status(status: str) -> str:
    if status in {"generated", "smoke_passed"}:
        return "accept"
    if status == "dependency_gap":
        return "dependency_gap"
    if status in {"fallback", "blocked_by_asset_smoke"}:
        return "fallback"
    return "failure"
