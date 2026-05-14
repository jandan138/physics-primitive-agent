from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EnvironmentCheck:
    name: str
    status: str
    detail: str

    def to_dict(self) -> dict[str, str]:
        return {"name": self.name, "status": self.status, "detail": self.detail}


@dataclass(frozen=True)
class EnvironmentReport:
    stage: str
    status: str
    source_dir: str
    source_commit: str | None
    checks: tuple[EnvironmentCheck, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "stage": self.stage,
            "status": self.status,
            "source_dir": self.source_dir,
            "source_commit": self.source_commit,
            "checks": [check.to_dict() for check in self.checks],
        }


@dataclass(frozen=True)
class AssetSmokeReport:
    stage: str
    status: str
    role: str
    path: str
    checks: tuple[EnvironmentCheck, ...]
    metadata: dict[str, object]

    def to_dict(self) -> dict[str, object]:
        return {
            "stage": self.stage,
            "status": self.status,
            "role": self.role,
            "path": self.path,
            "checks": [check.to_dict() for check in self.checks],
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class NewtonShapeMapping:
    primitive_id: str
    kind: str
    status: str
    detail: str
    center: tuple[float, float, float]
    dimensions: dict[str, Any]
    axes: tuple[tuple[float, float, float], ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "primitive_id": self.primitive_id,
            "kind": self.kind,
            "status": self.status,
            "detail": self.detail,
            "center": list(self.center),
            "axes": [list(axis) for axis in self.axes],
            "dimensions": dict(self.dimensions),
        }
