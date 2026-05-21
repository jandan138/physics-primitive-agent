from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


STAGE = "cylinder_clean_control_probe"
CLAIM_BOUNDARY = "cylinder_clean_control_probe_not_root_cause_proof_or_validated_repair"
EVIDENCE_LEVEL = "real_newton_compact_cylinder_clean_control_probe"


def build_cylinder_clean_control_report(
    *,
    single_controls: Mapping[str, Mapping[str, Any]],
    pair_controls: Sequence[Mapping[str, Any]],
    full_package_evidence: Mapping[str, Mapping[str, Any]],
    prior_evidence: Mapping[str, Any] | None = None,
    run_metadata: Mapping[str, Any] | None = None,
) -> dict[str, object]:
    prior_evidence = prior_evidence or {}
    cause_assessment = _cause_assessment(
        single_controls=single_controls,
        pair_controls=pair_controls,
        full_package_evidence=full_package_evidence,
        prior_evidence=prior_evidence,
    )
    return {
        "stage": STAGE,
        "status": "diagnostic_recorded",
        "claim_boundary": CLAIM_BOUNDARY,
        "evidence_level": EVIDENCE_LEVEL,
        "run_metadata": dict(run_metadata or {}),
        "single_controls": {
            name: _run_summary(payload) for name, payload in single_controls.items()
        },
        "pair_controls": [_pair_summary(pair) for pair in pair_controls],
        "full_package_evidence": {
            name: _run_summary(payload) for name, payload in full_package_evidence.items()
        },
        "prior_evidence": dict(prior_evidence),
        "cause_assessment": cause_assessment,
        "current_interpretation": _current_interpretation(cause_assessment),
        "interpretation_boundary": (
            "This compact-control probe is diagnostic accounting over selected Newton task-smoke "
            "runs. It is not root-cause proof, not a validated inertial repair, not a selector "
            "policy, not cylinder-quality validation, and not safety evidence."
        ),
    }


def _cause_assessment(
    *,
    single_controls: Mapping[str, Mapping[str, Any]],
    pair_controls: Sequence[Mapping[str, Any]],
    full_package_evidence: Mapping[str, Mapping[str, Any]],
    prior_evidence: Mapping[str, Any],
) -> dict[str, object]:
    bed_cylinder_single_passed = _status(
        single_controls.get("bed_cylinder_only_actual_axes")
    ) == "smoke_passed"
    franka_cylinder_single_passed = _status(
        single_controls.get("franka_largest_cylinder_only")
    ) == "smoke_passed"
    bed_full_failed_not_settled = _has_label(
        full_package_evidence.get("bed_native_opt_in_drop"),
        "not_settled",
    )
    bed_native_passed = _status(full_package_evidence.get("bed_native_drop")) == "smoke_passed"
    franka_full_passed = (
        _status(full_package_evidence.get("franka_native_opt_in_drop")) == "smoke_passed"
    )
    pair_classes = _pair_classes(pair_controls)
    cylinder_only_failures = pair_classes["cylinder_only_failure_count"]
    cylinder_only_floor = pair_classes["cylinder_only_floor_breach_count"]
    both_failures = pair_classes["both_failure_count"]
    both_pass = pair_classes["both_pass_count"]

    return {
        "geometry_alone": {
            "assessment": "insufficient_as_sole_cause"
            if bed_cylinder_single_passed
            and franka_cylinder_single_passed
            and bed_full_failed_not_settled
            else "open",
            "evidence": {
                "bed_cylinder_only_status": _status(
                    single_controls.get("bed_cylinder_only_actual_axes")
                ),
                "franka_largest_cylinder_only_status": _status(
                    single_controls.get("franka_largest_cylinder_only")
                ),
                "bed_full_opt_in_labels": _labels(
                    full_package_evidence.get("bed_native_opt_in_drop")
                ),
            },
        },
        "compound_context": {
            "assessment": "required_for_recorded_not_settled"
            if bed_cylinder_single_passed and bed_full_failed_not_settled and bed_native_passed
            else "open",
            "evidence": {
                "bed_single_cylinder_passed": bed_cylinder_single_passed,
                "bed_native_passed": bed_native_passed,
                "bed_full_opt_in_failed_not_settled": bed_full_failed_not_settled,
            },
        },
        "pair_context": {
            "assessment": "mixed"
            if (both_failures and cylinder_only_failures and both_pass)
            else "same_target_shape_failure"
            if both_failures and not cylinder_only_failures
            else "target_shape_specific_failure"
            if cylinder_only_failures and not both_failures
            else "open",
            "evidence": pair_classes,
        },
        "contact_or_floor_interaction": {
            "assessment": "open_for_pair_controls_not_recorded_full_failure"
            if cylinder_only_floor and bed_full_failed_not_settled
            else "open",
            "evidence": {
                "cylinder_only_floor_breach_pair_count": cylinder_only_floor,
                "bed_full_opt_in_labels": _labels(
                    full_package_evidence.get("bed_native_opt_in_drop")
                ),
            },
        },
        "franka_context": {
            "assessment": "recorded_context_passes"
            if franka_cylinder_single_passed and franka_full_passed
            else "open",
            "evidence": {
                "franka_largest_cylinder_only_status": _status(
                    single_controls.get("franka_largest_cylinder_only")
                ),
                "franka_native_opt_in_drop_status": _status(
                    full_package_evidence.get("franka_native_opt_in_drop")
                ),
            },
        },
        "com_inertia_body_state": {
            "assessment": "still_strongest_current_hypothesis"
            if (
                prior_evidence.get("native_body_com_clears_bed_failure") is True
                and prior_evidence.get("native_inertia_only_clears_bed_failure") is True
                and prior_evidence.get("mass_only_clears_bed_failure") is False
                and bed_full_failed_not_settled
            )
            else "open",
            "evidence": (
                "Prior one-config controls report COM-only and inertia-only clearing the "
                "bed final-speed label while mass-only does not; compact controls show "
                "geometry alone is insufficient."
            ),
        },
    }


def _current_interpretation(cause_assessment: Mapping[str, Any]) -> str:
    if (
        _assessment(cause_assessment, "geometry_alone") == "insufficient_as_sole_cause"
        and _assessment(cause_assessment, "compound_context")
        == "required_for_recorded_not_settled"
        and _assessment(cause_assessment, "com_inertia_body_state")
        == "still_strongest_current_hypothesis"
    ):
        return (
            "The compact controls point away from large-flat cylinder geometry alone and toward "
            "full-compound body-state sensitivity as necessary for the recorded bed not_settled "
            "failure. Pair controls remain mixed, so contact/floor interaction is still an open "
            "secondary factor rather than the current recorded full-package explanation."
        )
    return "The compact controls do not yet support a narrowed mechanism interpretation."


def _pair_classes(pair_controls: Sequence[Mapping[str, Any]]) -> dict[str, object]:
    both_failure = []
    cylinder_only_failure = []
    box_only_failure = []
    both_pass = []
    cylinder_only_floor_breach = []
    for pair in pair_controls:
        box = pair.get("box")
        cylinder = pair.get("cylinder")
        box_failed = _status(box) != "smoke_passed"
        cylinder_failed = _status(cylinder) != "smoke_passed"
        if box_failed and cylinder_failed:
            both_failure.append(pair.get("rest_index"))
        elif cylinder_failed:
            cylinder_only_failure.append(pair.get("rest_index"))
            if _has_label(cylinder, "floor_breach"):
                cylinder_only_floor_breach.append(pair.get("rest_index"))
        elif box_failed:
            box_only_failure.append(pair.get("rest_index"))
        else:
            both_pass.append(pair.get("rest_index"))
    return {
        "sampled_pair_count": len(pair_controls),
        "both_failure_count": len(both_failure),
        "cylinder_only_failure_count": len(cylinder_only_failure),
        "box_only_failure_count": len(box_only_failure),
        "both_pass_count": len(both_pass),
        "cylinder_only_floor_breach_count": len(cylinder_only_floor_breach),
        "both_failure_rest_indices": both_failure,
        "cylinder_only_failure_rest_indices": cylinder_only_failure,
        "box_only_failure_rest_indices": box_only_failure,
        "both_pass_rest_indices": both_pass,
        "cylinder_only_floor_breach_rest_indices": cylinder_only_floor_breach,
    }


def _pair_summary(pair: Mapping[str, Any]) -> dict[str, object]:
    return {
        "rest_index": pair.get("rest_index"),
        "rest_source_faces": _list_or_empty(pair.get("rest_source_faces")),
        "box": _run_summary(pair.get("box")),
        "cylinder": _run_summary(pair.get("cylinder")),
    }


def _run_summary(payload: object) -> dict[str, object]:
    if not isinstance(payload, Mapping):
        return {
            "status": None,
            "failure_labels": [],
            "final_linear_speed_mps": None,
            "final_contact_count": None,
            "final_support_height": None,
        }
    return {
        "status": payload.get("status"),
        "failure_labels": _labels(payload),
        "final_linear_speed_mps": payload.get("final_linear_speed_mps"),
        "final_contact_count": payload.get("final_contact_count"),
        "final_support_height": payload.get("final_support_height"),
    }


def _assessment(cause_assessment: Mapping[str, Any], key: str) -> object:
    item = cause_assessment.get(key)
    if not isinstance(item, Mapping):
        return None
    return item.get("assessment")


def _status(payload: object) -> object:
    return payload.get("status") if isinstance(payload, Mapping) else None


def _has_label(payload: object, label: str) -> bool:
    return label in _labels(payload)


def _labels(payload: object) -> list[object]:
    if not isinstance(payload, Mapping):
        return []
    return _list_or_empty(payload.get("failure_labels"))


def _list_or_empty(value: object) -> list[object]:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return list(value)
    return []

