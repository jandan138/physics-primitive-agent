from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CompileConfig:
    asset_path: str
    task: str
    method: str = "primitive_first"
    max_primitives: int = 16
    allowed_fallback: tuple[str, ...] = ("coacd", "sdf")
    verify: tuple[str, ...] = ("drop", "stack", "sphere_rain")
    keep_visual: bool = True


@dataclass(frozen=True)
class PrimitiveSpec:
    kind: str
    pose: tuple[float, ...] = ()
    dimensions: tuple[float, ...] = ()


@dataclass(frozen=True)
class FallbackSpec:
    method: str
    reason: str = ""


@dataclass(frozen=True)
class CollisionPackage:
    asset_id: str
    primitives: tuple[PrimitiveSpec, ...] = ()
    fallback: FallbackSpec | None = None


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
