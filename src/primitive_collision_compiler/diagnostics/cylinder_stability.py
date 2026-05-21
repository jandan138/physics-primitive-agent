from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from primitive_collision_compiler.contracts import CollisionPackage
from primitive_collision_compiler.newton.shapes import map_package_shapes


STAGE = "cylinder_stability_mechanism_diagnosis"
CLAIM_BOUNDARY = (
    "cylinder_stability_mechanism_diagnostic_not_collision_quality_or_validated_repair"
)
EVIDENCE_LEVEL = "real_newton_bed_franka_cylinder_stability_mechanism_diagnostic"


def cylinder_geometry_from_package(package: CollisionPackage) -> list[dict[str, object]]:
    mappings = map_package_shapes(package)
    cylinders: list[dict[str, object]] = []
    for index, (primitive, mapping) in enumerate(zip(package.primitives, mappings)):
        if primitive.kind != "cylinder":
            continue
        radius = _float_or_none(mapping.dimensions.get("radius"))
        half_height = _float_or_none(mapping.dimensions.get("half_height"))
        cylinders.append(
            {
                "primitive_index": index,
                "primitive_id": primitive.primitive_id,
                "source_faces": list(primitive.source_faces),
                "radius": radius,
                "half_height": half_height,
                "half_height_radius_ratio": None
                if radius in (None, 0.0) or half_height is None
                else half_height / radius,
                "axis_index": mapping.dimensions.get("axis_index", 2),
                "mapping_status": mapping.status,
            }
        )
    return cylinders


def build_cylinder_stability_mechanism_report(
    *,
    bed_task_report: Mapping[str, Any],
    franka_task_report: Mapping[str, Any],
    bed_cylinders: Sequence[Mapping[str, Any]],
    franka_cylinders: Sequence[Mapping[str, Any]],
    prior_evidence: Mapping[str, Any] | None = None,
) -> dict[str, object]:
    prior_evidence = prior_evidence or {}
    bed_case = _case_for_role(bed_task_report, "bed_task_report", "bed")
    franka_case = _case_for_role(franka_task_report, "franka_task_report", "franka")
    observed_pattern = {
        "bed": _case_pattern(bed_case),
        "franka": _case_pattern(franka_case),
    }
    geometry_contrast = _geometry_contrast(bed_cylinders, franka_cylinders)
    cause_assessment = _cause_assessment(
        observed_pattern=observed_pattern,
        geometry_contrast=geometry_contrast,
        prior_evidence=prior_evidence,
    )
    current_hypothesis_status, current_hypothesis = _current_hypothesis(cause_assessment)
    return {
        "stage": STAGE,
        "status": "diagnostic_recorded",
        "claim_boundary": CLAIM_BOUNDARY,
        "evidence_level": EVIDENCE_LEVEL,
        "observed_pattern": observed_pattern,
        "geometry_contrast": geometry_contrast,
        "prior_evidence": dict(prior_evidence),
        "cause_assessment": cause_assessment,
        "current_hypothesis_status": current_hypothesis_status,
        "current_hypothesis": current_hypothesis,
        "missing_evidence": [
            "compact clean-control reproducer independent of the large real-USD package",
            "sustained-settle criterion beyond the existing final-speed task label",
            "causal contact-manifold analysis beyond matching final support-contact labels",
            "evidence that Newton inertia-correction warnings are or are not material",
            "validated selector or inertial repair policy across more than this recorded slice",
        ],
        "interpretation_boundary": (
            "This is a diagnostic synthesis over recorded Newton task smokes, package geometry, "
            "and one-config sensitivity controls. It is not a validated repair, not cylinder "
            "quality validation, not a default selector policy, and not safety evidence."
        ),
    }


def _case_for_role(
    report: Mapping[str, Any],
    report_name: str,
    role_marker: str,
) -> Mapping[str, Any]:
    cases = report.get("cases")
    if not isinstance(cases, Sequence) or isinstance(cases, (str, bytes)) or not cases:
        raise ValueError(f"{report_name} must contain at least one case")
    mapping_cases = []
    for index, case in enumerate(cases):
        if not isinstance(case, Mapping):
            raise ValueError(f"{report_name} case {index} must be a mapping")
        mapping_cases.append(case)
    matching_cases = [
        case
        for case in mapping_cases
        if role_marker in str(case.get("asset_role", "")).lower()
    ]
    if len(matching_cases) == 1:
        return matching_cases[0]
    if len(mapping_cases) == 1 and not matching_cases:
        return mapping_cases[0]
    if matching_cases:
        raise ValueError(f"{report_name} contains multiple {role_marker!r} cases")
    raise ValueError(f"{report_name} contains multiple cases but no {role_marker!r} asset_role")


def _case_pattern(case: Mapping[str, Any]) -> dict[str, object]:
    pattern: dict[str, object] = {
        "asset_role": case.get("asset_role"),
        "asset_path": case.get("asset_path"),
    }
    for lane in ("legacy", "native", "native_opt_in"):
        lane_payload = case.get(lane)
        if isinstance(lane_payload, Mapping):
            pattern[f"{lane}_primitive_kind_counts"] = _mapping_or_empty(
                lane_payload.get("primitive_kind_counts")
            )
        contact = case.get(f"{lane}_contact")
        if isinstance(contact, Mapping):
            pattern[f"{lane}_contact_status"] = contact.get("status")
        tasks = case.get(f"{lane}_tasks")
        if isinstance(tasks, Mapping):
            drop = tasks.get("drop_settle")
            sphere = tasks.get("sphere_rain")
            if isinstance(drop, Mapping):
                pattern[f"{lane}_drop"] = _drop_summary(drop)
            if isinstance(sphere, Mapping):
                pattern[f"{lane}_sphere_rain_status"] = sphere.get("status")
    return pattern


def _drop_summary(drop: Mapping[str, Any]) -> dict[str, object]:
    runs = drop.get("drop_settle_runs")
    run = runs[0] if isinstance(runs, Sequence) and runs else {}
    if not isinstance(run, Mapping):
        run = {}
    return {
        "status": drop.get("status"),
        "failure_labels": _list_or_empty(run.get("failure_labels")),
        "final_linear_speed_mps": run.get("final_linear_speed_mps"),
        "final_contact_count": run.get("final_contact_count"),
        "final_support_height": run.get("final_support_height"),
    }


def _geometry_contrast(
    bed_cylinders: Sequence[Mapping[str, Any]],
    franka_cylinders: Sequence[Mapping[str, Any]],
) -> dict[str, object]:
    bed_radius = _max_float(bed_cylinders, "radius")
    franka_radius = _max_float(franka_cylinders, "radius")
    return {
        "bed_cylinder_count": len(bed_cylinders),
        "franka_cylinder_count": len(franka_cylinders),
        "bed_max_cylinder_radius_m": bed_radius,
        "franka_max_cylinder_radius_m": franka_radius,
        "bed_min_half_height_radius_ratio": _min_float(
            bed_cylinders,
            "half_height_radius_ratio",
        ),
        "franka_min_half_height_radius_ratio": _min_float(
            franka_cylinders,
            "half_height_radius_ratio",
        ),
        "bed_max_to_franka_max_radius_ratio": (
            None
            if bed_radius is None or franka_radius in (None, 0.0)
            else bed_radius / franka_radius
        ),
        "bed_cylinders": [dict(cylinder) for cylinder in bed_cylinders],
        "franka_cylinders": [dict(cylinder) for cylinder in franka_cylinders],
    }


def _cause_assessment(
    *,
    observed_pattern: Mapping[str, Any],
    geometry_contrast: Mapping[str, Any],
    prior_evidence: Mapping[str, Any],
) -> dict[str, object]:
    bed = observed_pattern["bed"]
    franka = observed_pattern["franka"]
    bed_opt_drop = bed.get("native_opt_in_drop", {})
    franka_opt_drop = franka.get("native_opt_in_drop", {})
    bed_native_drop = bed.get("native_drop", {})
    bed_contact_passed = bed.get("native_opt_in_contact_status") == "smoke_passed"
    franka_contact_passed = franka.get("native_opt_in_contact_status") == "smoke_passed"
    bed_drop_failure_labels = (
        bed_opt_drop.get("failure_labels", []) if isinstance(bed_opt_drop, Mapping) else []
    )
    bed_native_passed = (
        isinstance(bed_native_drop, Mapping) and bed_native_drop.get("status") == "smoke_passed"
    )
    franka_opt_passed = (
        isinstance(franka_opt_drop, Mapping)
        and franka_opt_drop.get("status") == "smoke_passed"
    )
    return {
        "mapping_or_contact_gap": {
            "assessment": "unlikely" if bed_contact_passed and franka_contact_passed else "open",
            "evidence": (
                "Bed and Franka opt-in lanes both pass representative contact canaries; bed "
                "failure occurs downstream in drop/settle."
            ),
        },
        "cylinder_primitive_unsupported": {
            "assessment": "unlikely" if franka_opt_passed else "open",
            "evidence": (
                "Franka native_opt_in contains cylinders and passes the recorded Newton task "
                "smokes, so cylinder mapping is not categorically unsupported."
            ),
        },
        "drop_final_speed_gate": {
            "assessment": (
                "direct_failure_mode" if "not_settled" in bed_drop_failure_labels else "open"
            ),
            "evidence": {
                "bed_native_opt_in_final_speed_mps": bed_opt_drop.get("final_linear_speed_mps")
                if isinstance(bed_opt_drop, Mapping)
                else None,
                "franka_native_opt_in_final_speed_mps": franka_opt_drop.get(
                    "final_linear_speed_mps"
                )
                if isinstance(franka_opt_drop, Mapping)
                else None,
                "failure_labels": list(bed_drop_failure_labels),
            },
        },
        "geometry_large_flat_cylinder": {
            "assessment": "supported"
            if _supports_large_flat_cylinder_contrast(geometry_contrast)
            else "open",
            "evidence": {
                "bed_cylinder_count": geometry_contrast.get("bed_cylinder_count"),
                "franka_cylinder_count": geometry_contrast.get("franka_cylinder_count"),
                "bed_min_half_height_radius_ratio": geometry_contrast.get(
                    "bed_min_half_height_radius_ratio"
                ),
                "bed_max_to_franka_max_radius_ratio": geometry_contrast.get(
                    "bed_max_to_franka_max_radius_ratio"
                ),
            },
        },
        "center_shift_alone": {
            "assessment": "unlikely"
            if prior_evidence.get("center_shift_alone_reproduces_failure") is False
            else "open",
            "evidence": "Recorded center/shape controls keep cylinder-at-box-center failing while box-at-cylinder-center passes.",
        },
        "support_contact_labels": {
            "assessment": "unlikely_as_sole_cause"
            if prior_evidence.get("final_support_contact_labels_match_controls") is True
            else "open",
            "evidence": "Recorded clean-frame blocker audit reports matching final support-contact primitive suffixes.",
        },
        "full_compound_context": {
            "assessment": "supported"
            if (
                bed_native_passed
                and prior_evidence.get("target_only_cylinder_reproduces_failure") is False
            )
            else "open",
            "evidence": (
                "The isolated target cylinder passes in prior diagnostics, while the full bed "
                "opt-in package fails and the all-box/native controls pass."
            ),
        },
        "com_inertia_body_state": {
            "assessment": "strongest_current_hypothesis"
            if (
                prior_evidence.get("native_body_com_clears_bed_failure") is True
                and prior_evidence.get("native_inertia_only_clears_bed_failure") is True
                and prior_evidence.get("mass_only_clears_bed_failure") is False
            )
            else "open",
            "evidence": (
                "Prior one-config ablations report COM-only and inertia-only clearing the bed "
                "final-speed label, while mass-only does not."
            ),
        },
    }


def _current_hypothesis(cause_assessment: Mapping[str, Any]) -> tuple[str, str]:
    if (
        _assessment(cause_assessment, "drop_final_speed_gate") == "direct_failure_mode"
        and _assessment(cause_assessment, "geometry_large_flat_cylinder") == "supported"
        and _assessment(cause_assessment, "full_compound_context") == "supported"
        and _assessment(cause_assessment, "com_inertia_body_state")
        == "strongest_current_hypothesis"
    ):
        return (
            "strongest_current_hypothesis",
            "The capped bed blocker is best explained as a full-compound body-state sensitivity "
            "introduced by selecting one large, flat cylinder: the package still maps and contacts, "
            "but the cylinder package delta changes aggregate COM/inertia enough that the recorded "
            "drop/settle final-speed gate stays above threshold. The recorded Franka cylinders pass "
            "because they are a much smaller cylinder class in a different compound package context.",
        )
    return (
        "open",
        "The recorded evidence is not sufficient to assign the bed/Franka cylinder contrast to "
        "the large-flat-cylinder full-compound COM/inertia hypothesis.",
    )


def _assessment(cause_assessment: Mapping[str, Any], key: str) -> object:
    item = cause_assessment.get(key)
    if not isinstance(item, Mapping):
        return None
    return item.get("assessment")


def _supports_large_flat_cylinder_contrast(
    geometry_contrast: Mapping[str, Any],
) -> bool:
    bed_count = _int_or_zero(geometry_contrast.get("bed_cylinder_count"))
    franka_count = _int_or_zero(geometry_contrast.get("franka_cylinder_count"))
    bed_flatness = _float_or_none(geometry_contrast.get("bed_min_half_height_radius_ratio"))
    radius_ratio = _float_or_none(geometry_contrast.get("bed_max_to_franka_max_radius_ratio"))
    return (
        bed_count > 0
        and franka_count > 0
        and bed_flatness is not None
        and bed_flatness < 0.1
        and radius_ratio is not None
        and radius_ratio > 1000.0
    )


def _mapping_or_empty(value: object) -> dict[str, object]:
    return dict(value) if isinstance(value, Mapping) else {}


def _list_or_empty(value: object) -> list[object]:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return list(value)
    return []


def _int_or_zero(value: object) -> int:
    try:
        return int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0


def _max_float(items: Sequence[Mapping[str, Any]], key: str) -> float | None:
    values = _finite_floats(items, key)
    return max(values) if values else None


def _min_float(items: Sequence[Mapping[str, Any]], key: str) -> float | None:
    values = _finite_floats(items, key)
    return min(values) if values else None


def _finite_floats(items: Sequence[Mapping[str, Any]], key: str) -> list[float]:
    values = []
    for item in items:
        try:
            value = float(item[key])
        except (KeyError, TypeError, ValueError):
            continue
        if value == value and value not in {float("inf"), float("-inf")}:
            values.append(value)
    return values


def _float_or_none(value: object) -> float | None:
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
