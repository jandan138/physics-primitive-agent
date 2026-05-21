from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any

import numpy as np

from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec


STAGE = "cylinder_package_body_state_risk_probe"
CLAIM_BOUNDARY = (
    "cylinder_package_body_state_risk_probe_not_root_cause_proof_or_validated_repair"
)
EVIDENCE_LEVEL = "package_geometry_proxy_bed_franka_cylinder_body_state_risk"

DEFAULT_THRESHOLDS = {
    "min_large_cylinder_radius_m": 0.5,
    "max_flat_half_height_radius_ratio": 0.1,
    "min_com_delta_norm_m": 0.05,
    "min_inertia_frobenius_delta": 1.0,
}


def package_body_state_proxy(package: CollisionPackage) -> dict[str, object]:
    state = _body_state_arrays(package)
    return {
        "package_id": package.package_id,
        "asset_id": package.asset_id,
        "primitive_count": len(package.primitives),
        "mass_proxy": state["mass"],
        "com_proxy": _list3(state["com"]),
        "inertia_proxy_matrix": _matrix3(state["inertia"]),
        "inertia_proxy_trace": float(np.trace(state["inertia"])),
        "inertia_proxy_frobenius_norm": float(np.linalg.norm(state["inertia"])),
        "cylinder_summary": _cylinder_summary(package),
        "evidence_inputs": _evidence_inputs(),
    }


def build_cylinder_package_body_state_risk_report(
    *,
    cases: Mapping[str, Mapping[str, Any]],
    thresholds: Mapping[str, float] | None = None,
) -> dict[str, object]:
    active_thresholds = dict(DEFAULT_THRESHOLDS)
    active_thresholds.update(thresholds or {})
    case_assessments = {
        name: _case_assessment(name, payload, active_thresholds)
        for name, payload in cases.items()
    }
    return {
        "stage": STAGE,
        "status": "diagnostic_recorded",
        "claim_boundary": CLAIM_BOUNDARY,
        "evidence_level": EVIDENCE_LEVEL,
        "thresholds": active_thresholds,
        "evidence_inputs": _evidence_inputs(),
        "case_assessments": case_assessments,
        "contrast_assessment": _contrast_assessment(case_assessments),
        "interpretation_boundary": (
            "This report is a package-geometry proxy over volume-weighted COM and inertia "
            "features. It does not read or copy Newton model arrays. It is not a validated "
            "repair, not a default selector policy, not collision-quality validation, and not "
            "safety evidence."
        ),
    }


def _case_assessment(
    case_name: str,
    payload: Mapping[str, Any],
    thresholds: Mapping[str, float],
) -> dict[str, object]:
    native = payload.get("native")
    opt_in = payload.get("native_opt_in")
    if not isinstance(native, CollisionPackage) or not isinstance(opt_in, CollisionPackage):
        raise ValueError(f"{case_name} requires native and native_opt_in CollisionPackage values")
    native_state = _body_state_arrays(native)
    opt_in_state = _body_state_arrays(opt_in)
    delta = _body_state_delta(native_state, opt_in_state)
    cylinder_summary = _cylinder_summary(opt_in)
    risk_flags = _risk_flags(cylinder_summary, delta, thresholds)
    drop_evidence = _drop_evidence(payload.get("drop_evidence"))
    return {
        "native_package_id": native.package_id,
        "native_opt_in_package_id": opt_in.package_id,
        "native_proxy": package_body_state_proxy(native),
        "native_opt_in_proxy": package_body_state_proxy(opt_in),
        "package_delta_proxy": delta,
        "risk_flags": risk_flags,
        "package_risk_class": _package_risk_class(risk_flags),
        "drop_evidence": drop_evidence,
    }


def _body_state_arrays(package: CollisionPackage) -> dict[str, Any]:
    primitive_masses = [_mass_proxy(primitive) for primitive in package.primitives]
    total_mass = float(sum(primitive_masses))
    if total_mass <= 0.0:
        return {"mass": 0.0, "com": np.zeros(3), "inertia": np.zeros((3, 3))}

    centers = [_center(primitive) for primitive in package.primitives]
    com = sum(
        (mass * center for mass, center in zip(primitive_masses, centers, strict=True)),
        start=np.zeros(3),
    ) / total_mass
    inertia_about_origin = sum(
        (
            _primitive_inertia_about_origin(primitive, mass, center)
            for primitive, mass, center in zip(
                package.primitives,
                primitive_masses,
                centers,
                strict=True,
            )
        ),
        start=np.zeros((3, 3)),
    )
    inertia_about_com = inertia_about_origin - total_mass * (
        float(np.dot(com, com)) * np.eye(3) - np.outer(com, com)
    )
    return {"mass": total_mass, "com": com, "inertia": inertia_about_com}


def _primitive_inertia_about_origin(
    primitive: PrimitiveSpec,
    mass: float,
    center: np.ndarray,
) -> np.ndarray:
    local = _primitive_local_inertia(primitive, mass)
    rotation = _axes_matrix(primitive)
    inertia_about_center = rotation @ local @ rotation.T
    return inertia_about_center + mass * (
        float(np.dot(center, center)) * np.eye(3) - np.outer(center, center)
    )


def _primitive_local_inertia(primitive: PrimitiveSpec, mass: float) -> np.ndarray:
    dimensions = primitive.dimensions if isinstance(primitive.dimensions, Mapping) else {}
    if primitive.kind == "box":
        half_extents = _float_sequence(dimensions.get("half_extents"), expected=3)
        if half_extents is None:
            return np.zeros((3, 3))
        hx, hy, hz = half_extents
        return np.diag(
            [
                mass * (hy * hy + hz * hz) / 3.0,
                mass * (hx * hx + hz * hz) / 3.0,
                mass * (hx * hx + hy * hy) / 3.0,
            ]
        )
    if primitive.kind == "cylinder":
        radius = _float_or_none(dimensions.get("radius"))
        half_height = _float_or_none(dimensions.get("half_height"))
        axis_index = _axis_index(dimensions.get("axis_index"))
        if radius is None or half_height is None:
            return np.zeros((3, 3))
        axial = 0.5 * mass * radius * radius
        transverse = mass * (0.25 * radius * radius + half_height * half_height / 3.0)
        diagonal = [transverse, transverse, transverse]
        diagonal[axis_index] = axial
        return np.diag(diagonal)
    return np.zeros((3, 3))


def _mass_proxy(primitive: PrimitiveSpec) -> float:
    for value in (primitive.weighted_volume, primitive.volume, _dimension_volume(primitive)):
        numeric = _float_or_none(value)
        if numeric is not None and numeric > 0.0:
            return numeric
    return 0.0


def _dimension_volume(primitive: PrimitiveSpec) -> float | None:
    dimensions = primitive.dimensions if isinstance(primitive.dimensions, Mapping) else {}
    if primitive.kind == "box":
        half_extents = _float_sequence(dimensions.get("half_extents"), expected=3)
        if half_extents is None:
            return None
        return 8.0 * math.prod(half_extents)
    if primitive.kind == "cylinder":
        radius = _float_or_none(dimensions.get("radius"))
        half_height = _float_or_none(dimensions.get("half_height"))
        if radius is None or half_height is None:
            return None
        return 2.0 * math.pi * radius * radius * half_height
    return None


def _body_state_delta(
    native_state: Mapping[str, Any],
    opt_in_state: Mapping[str, Any],
) -> dict[str, object]:
    native_com = np.asarray(native_state["com"], dtype=float)
    opt_in_com = np.asarray(opt_in_state["com"], dtype=float)
    native_inertia = np.asarray(native_state["inertia"], dtype=float)
    opt_in_inertia = np.asarray(opt_in_state["inertia"], dtype=float)
    com_delta = opt_in_com - native_com
    inertia_delta = opt_in_inertia - native_inertia
    native_inertia_norm = float(np.linalg.norm(native_inertia))
    return {
        "mass_delta": float(opt_in_state["mass"] - native_state["mass"]),
        "mass_relative_delta": _relative_delta(opt_in_state["mass"], native_state["mass"]),
        "com_delta": _list3(com_delta),
        "com_delta_norm_m": float(np.linalg.norm(com_delta)),
        "inertia_delta_matrix": _matrix3(inertia_delta),
        "inertia_frobenius_delta": float(np.linalg.norm(inertia_delta)),
        "inertia_relative_frobenius_delta": (
            None
            if native_inertia_norm <= 0.0
            else float(np.linalg.norm(inertia_delta) / native_inertia_norm)
        ),
    }


def _risk_flags(
    cylinder_summary: Mapping[str, object],
    delta: Mapping[str, object],
    thresholds: Mapping[str, float],
) -> dict[str, bool]:
    max_radius = _float_or_none(cylinder_summary.get("max_radius_m"))
    min_ratio = _float_or_none(cylinder_summary.get("min_half_height_radius_ratio"))
    com_delta = _float_or_none(delta.get("com_delta_norm_m"))
    inertia_delta = _float_or_none(delta.get("inertia_frobenius_delta"))
    large_absolute = (
        max_radius is not None and max_radius >= thresholds["min_large_cylinder_radius_m"]
    )
    return {
        "large_absolute_cylinder": large_absolute,
        "large_flat_cylinder": (
            large_absolute
            and min_ratio is not None
            and min_ratio <= thresholds["max_flat_half_height_radius_ratio"]
        ),
        "package_com_delta": (
            com_delta is not None and com_delta >= thresholds["min_com_delta_norm_m"]
        ),
        "package_inertia_delta": (
            inertia_delta is not None
            and inertia_delta >= thresholds["min_inertia_frobenius_delta"]
        ),
    }


def _package_risk_class(risk_flags: Mapping[str, bool]) -> str:
    if all(risk_flags.values()):
        return "large_flat_cylinder_body_state_delta_risk"
    return "not_flagged"


def _contrast_assessment(case_assessments: Mapping[str, Mapping[str, Any]]) -> dict[str, object]:
    bed = case_assessments.get("bed", {})
    franka = case_assessments.get("franka", {})
    bed_flagged = bed.get("package_risk_class") == "large_flat_cylinder_body_state_delta_risk"
    franka_flagged = (
        franka.get("package_risk_class") == "large_flat_cylinder_body_state_delta_risk"
    )
    bed_failed = _has_label(bed.get("drop_evidence"), "not_settled")
    franka_passed = _status(franka.get("drop_evidence")) == "smoke_passed"
    if bed_flagged and not franka_flagged and bed_failed and franka_passed:
        assessment = "bed_flagged_franka_not_flagged_matches_recorded_drop_contrast"
    elif bed_flagged and not franka_flagged:
        assessment = "bed_flagged_franka_not_flagged_without_complete_drop_contrast"
    else:
        assessment = "open"
    return {
        "assessment": assessment,
        "bed_package_risk_class": bed.get("package_risk_class"),
        "franka_package_risk_class": franka.get("package_risk_class"),
        "bed_drop_labels": _labels(bed.get("drop_evidence")),
        "franka_drop_status": _status(franka.get("drop_evidence")),
    }


def _cylinder_summary(package: CollisionPackage) -> dict[str, object]:
    cylinders = [primitive for primitive in package.primitives if primitive.kind == "cylinder"]
    ratios = []
    radii = []
    volume = 0.0
    for primitive in cylinders:
        dimensions = primitive.dimensions if isinstance(primitive.dimensions, Mapping) else {}
        radius = _float_or_none(dimensions.get("radius"))
        half_height = _float_or_none(dimensions.get("half_height"))
        if radius is not None:
            radii.append(radius)
        if radius not in (None, 0.0) and half_height is not None:
            ratios.append(half_height / radius)
        volume += _mass_proxy(primitive)
    total_mass = sum(_mass_proxy(primitive) for primitive in package.primitives)
    return {
        "cylinder_count": len(cylinders),
        "max_radius_m": max(radii) if radii else None,
        "min_half_height_radius_ratio": min(ratios) if ratios else None,
        "cylinder_mass_proxy": volume,
        "cylinder_mass_proxy_share": None if total_mass <= 0.0 else volume / total_mass,
    }


def _drop_evidence(payload: object) -> dict[str, object]:
    if not isinstance(payload, Mapping):
        return {"status": None, "failure_labels": [], "final_linear_speed_mps": None}
    return {
        "status": payload.get("status"),
        "failure_labels": _labels(payload),
        "final_linear_speed_mps": payload.get("final_linear_speed_mps"),
    }


def _evidence_inputs() -> dict[str, object]:
    return {
        "uses_package_geometry": True,
        "uses_volume_weighted_proxy": True,
        "uses_newton_model_arrays": False,
    }


def _has_label(payload: object, label: str) -> bool:
    return label in _labels(payload)


def _labels(payload: object) -> list[object]:
    if not isinstance(payload, Mapping):
        return []
    value = payload.get("failure_labels")
    if isinstance(value, (list, tuple)) and not isinstance(value, (str, bytes)):
        return list(value)
    return []


def _status(payload: object) -> object:
    return payload.get("status") if isinstance(payload, Mapping) else None


def _relative_delta(value: object, reference: object) -> float | None:
    value_float = _float_or_none(value)
    reference_float = _float_or_none(reference)
    if value_float is None or reference_float in (None, 0.0):
        return None
    return (value_float - reference_float) / reference_float


def _center(primitive: PrimitiveSpec) -> np.ndarray:
    center = _float_sequence(primitive.center, expected=3)
    return np.asarray(center or (0.0, 0.0, 0.0), dtype=float)


def _axes_matrix(primitive: PrimitiveSpec) -> np.ndarray:
    try:
        matrix = np.asarray(primitive.axes, dtype=float)
    except (TypeError, ValueError):
        return np.eye(3)
    if matrix.shape != (3, 3):
        return np.eye(3)
    return matrix


def _axis_index(value: object) -> int:
    try:
        axis = int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 2
    return axis if axis in (0, 1, 2) else 2


def _float_sequence(value: object, *, expected: int) -> tuple[float, ...] | None:
    if not isinstance(value, (list, tuple)) or isinstance(value, (str, bytes)):
        return None
    if len(value) != expected:
        return None
    floats = tuple(_float_or_none(item) for item in value)
    if any(item is None for item in floats):
        return None
    return floats  # type: ignore[return-value]


def _float_or_none(value: object) -> float | None:
    try:
        numeric = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    return numeric if math.isfinite(numeric) else None


def _list3(vector: np.ndarray) -> list[float]:
    return [float(value) for value in vector.tolist()]


def _matrix3(matrix: np.ndarray) -> list[list[float]]:
    return [[float(value) for value in row] for row in matrix.tolist()]
