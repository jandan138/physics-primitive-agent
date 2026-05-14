from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CompileConfig:
    asset_path: str
    task: str
    asset_id: str = ""
    method: str = "primitive_first"
    max_primitives: int = 16
    allowed_fallback: tuple[str, ...] = ("coacd", "sdf")
    verify: tuple[str, ...] = ("drop", "stack", "sphere_rain")
    keep_visual: bool = True
    protocol: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PrimitiveSpec:
    kind: str
    pose: tuple[float, ...] = ()
    dimensions: tuple[float, ...] | dict[str, Any] = ()
    primitive_id: str = ""
    center: tuple[float, float, float] = (0.0, 0.0, 0.0)
    axes: tuple[tuple[float, float, float], ...] = ()
    frame: str = "asset"
    source_faces: tuple[int, ...] = ()
    contains_assigned_points: bool | None = None
    volume: float | None = None
    weighted_volume: float | None = None
    conversion_status: str = "candidate"

    def to_dict(self) -> dict[str, Any]:
        dimensions: Any
        if isinstance(self.dimensions, dict):
            dimensions = dict(self.dimensions)
        else:
            dimensions = list(self.dimensions)
        return {
            "primitive_id": self.primitive_id,
            "kind": self.kind,
            "pose": list(self.pose),
            "center": list(self.center),
            "axes": [list(axis) for axis in self.axes],
            "dimensions": dimensions,
            "frame": self.frame,
            "source_faces": list(self.source_faces),
            "contains_assigned_points": self.contains_assigned_points,
            "volume": self.volume,
            "weighted_volume": self.weighted_volume,
            "conversion_status": self.conversion_status,
        }


@dataclass(frozen=True)
class FallbackSpec:
    method: str
    reason: str = ""

    def to_dict(self) -> dict[str, str]:
        return {"method": self.method, "reason": self.reason}


@dataclass(frozen=True)
class CollisionPackage:
    asset_id: str
    primitives: tuple[PrimitiveSpec, ...] = ()
    fallback: FallbackSpec | None = None
    package_id: str = ""
    source_path: str = ""
    source_sha256: str = ""
    method: str = "primitive_first"
    stage: str = ""
    status: str = "candidate"
    claim_boundary: str = ""
    mesh_point_count: int = 0
    mesh_face_count: int = 0
    max_source_faces: int | None = None
    primitive_subset: tuple[str, ...] = ()
    unsupported_primitives: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "package_id": self.package_id,
            "asset_id": self.asset_id,
            "source_path": self.source_path,
            "source_sha256": self.source_sha256,
            "method": self.method,
            "stage": self.stage,
            "status": self.status,
            "claim_boundary": self.claim_boundary,
            "mesh_point_count": self.mesh_point_count,
            "mesh_face_count": self.mesh_face_count,
            "max_source_faces": self.max_source_faces,
            "primitive_subset": list(self.primitive_subset),
            "unsupported_primitives": list(self.unsupported_primitives),
            "primitives": [primitive.to_dict() for primitive in self.primitives],
            "fallback": self.fallback.to_dict() if self.fallback else None,
        }


@dataclass(frozen=True)
class CompileReport:
    asset_id: str
    task: str
    dry_run: bool = True
    compiled: bool = False
    method: str = "primitive_first"
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        status = "dry_run" if self.dry_run else "compiled" if self.compiled else "not_compiled"
        return {
            "asset_id": self.asset_id,
            "task": self.task,
            "dry_run": self.dry_run,
            "compiled": self.compiled,
            "status": status,
            "method": self.method,
            "warnings": list(self.warnings),
        }
