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
class NewtonDropSettleRun:
    run_id: str
    status: str
    primitive_ids: tuple[str, ...]
    completed_steps: int
    initial_height: float
    final_height: float
    min_height: float
    final_linear_velocity: tuple[float, float, float]
    max_contact_count: int
    final_contact_count: int
    finite_state: bool
    descended: bool
    contact_observed: bool
    failure_labels: tuple[str, ...]
    final_support_height: float | None = None
    min_support_height: float | None = None
    final_linear_speed_mps: float | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "status": self.status,
            "primitive_ids": list(self.primitive_ids),
            "completed_steps": self.completed_steps,
            "initial_height": _json_safe(self.initial_height),
            "final_height": _json_safe(self.final_height),
            "min_height": _json_safe(self.min_height),
            "final_linear_velocity": _json_safe(list(self.final_linear_velocity)),
            "final_linear_speed_mps": _json_safe(self.final_linear_speed_mps),
            "max_contact_count": self.max_contact_count,
            "final_contact_count": self.final_contact_count,
            "finite_state": self.finite_state,
            "descended": self.descended,
            "contact_observed": self.contact_observed,
            "failure_labels": list(self.failure_labels),
            "final_support_height": _json_safe(self.final_support_height),
            "min_support_height": _json_safe(self.min_support_height),
        }


@dataclass(frozen=True)
class NewtonSphereRainRun:
    run_id: str
    status: str
    primitive_ids: tuple[str, ...]
    sphere_count: int
    completed_steps: int
    initial_min_height: float
    final_min_height: float
    min_height: float
    max_contact_count: int
    final_contact_count: int
    max_contacted_probe_count: int
    final_contacted_probe_count: int
    contact_density: float
    finite_state: bool
    contact_observed: bool
    final_contact_observed: bool
    failure_labels: tuple[str, ...]
    sphere_radius_m: float | None = None
    total_steps: int | None = None
    package_contact_count_p95: float | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "status": self.status,
            "primitive_ids": list(self.primitive_ids),
            "sphere_count": self.sphere_count,
            "sphere_radius_m": _json_safe(self.sphere_radius_m),
            "completed_steps": self.completed_steps,
            "total_steps": self.total_steps,
            "initial_min_height": _json_safe(self.initial_min_height),
            "final_min_height": _json_safe(self.final_min_height),
            "min_height": _json_safe(self.min_height),
            "max_contact_count": self.max_contact_count,
            "final_contact_count": self.final_contact_count,
            "max_contacted_probe_count": self.max_contacted_probe_count,
            "final_contacted_probe_count": self.final_contacted_probe_count,
            "package_contact_count_p95": _json_safe(self.package_contact_count_p95),
            "contact_density": _json_safe(self.contact_density),
            "finite_state": self.finite_state,
            "contact_observed": self.contact_observed,
            "final_contact_observed": self.final_contact_observed,
            "failure_labels": list(self.failure_labels),
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
    drop_settle_runs: tuple[NewtonDropSettleRun, ...] = ()
    sphere_rain_runs: tuple[NewtonSphereRainRun, ...] = ()
    task_scope: str = ""
    initial_conditions: dict[str, object] | None = None
    solver: dict[str, object] | None = None
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
            "drop_settle_runs": [run.to_dict() for run in self.drop_settle_runs],
            "sphere_rain_runs": [run.to_dict() for run in self.sphere_rain_runs],
            "task_scope": self.task_scope,
            "initial_conditions": _json_safe(dict(self.initial_conditions or {})),
            "solver": _json_safe(dict(self.solver or {})),
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
