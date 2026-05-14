from __future__ import annotations

from dataclasses import dataclass
import math
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
            "center": _json_safe(list(self.center)),
            "axes": _json_safe([list(axis) for axis in self.axes]),
            "dimensions": _json_safe(dict(self.dimensions)),
        }


@dataclass(frozen=True)
class NewtonContactCanary:
    primitive_id: str
    kind: str
    status: str
    contact_count: int
    detail: str

    def to_dict(self) -> dict[str, object]:
        return {
            "primitive_id": self.primitive_id,
            "kind": self.kind,
            "status": self.status,
            "contact_count": self.contact_count,
            "detail": self.detail,
        }


@dataclass(frozen=True)
class NewtonDiagnosticReport:
    stage: str
    status: str
    asset_id: str
    package_id: str
    probe_type: str
    device: str
    environment: EnvironmentReport | None
    primitive_count: int
    type_counts: dict[str, int]
    shape_mappings: tuple[NewtonShapeMapping, ...]
    contact_canaries: tuple[NewtonContactCanary, ...]
    claim_boundary: str
    metrics: dict[str, object] | None = None
    fallback_reason: str | None = None
    evidence_level: str = "newton_contact_canary_smoke"

    @property
    def shape_status_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for mapping in self.shape_mappings:
            counts[mapping.status] = counts.get(mapping.status, 0) + 1
        return counts

    def to_dict(self) -> dict[str, object]:
        return {
            "stage": self.stage,
            "status": self.status,
            "asset_id": self.asset_id,
            "package_id": self.package_id,
            "probe_type": self.probe_type,
            "device": self.device,
            "environment": self.environment.to_dict() if self.environment else None,
            "primitive_count": self.primitive_count,
            "type_counts": dict(self.type_counts),
            "shape_status_counts": self.shape_status_counts,
            "shape_mappings": [mapping.to_dict() for mapping in self.shape_mappings],
            "contact_canaries": [canary.to_dict() for canary in self.contact_canaries],
            "claim_boundary": self.claim_boundary,
            "metrics": dict(self.metrics or {}),
            "fallback_reason": self.fallback_reason,
            "evidence_level": self.evidence_level,
        }


def _json_safe(value: object) -> object:
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, list | tuple):
        return [_json_safe(item) for item in value]
    return value
