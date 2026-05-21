#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


DEFAULT_VARIANT_LABELS = (
    "native_control_box",
    "native_opt_in_cylinder_reverted",
)
CLAIM_BOUNDARY = (
    "bed_native_opt_in_frame_transition_audit_not_root_cause_or_fix_or_stability_evidence"
)
INTERPRETATION_BOUNDARY = (
    "frame_transition_audit_records_adjacent_final_speed_gate_behavior_only; "
    "it is not sustained-settle evidence, a validated fix, root-cause proof, "
    "or collision-quality validation"
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Compare two existing capped-bed frame-window Newton reports for adjacent "
            "final-speed gate transition auditing."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--clean-report", type=Path, required=True)
    parser.add_argument("--dirty-report", type=Path, required=True)
    parser.add_argument(
        "--variant-label",
        action="append",
        dest="variant_labels",
        help="variant label to compare; repeat to compare multiple labels",
    )
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    labels = tuple(args.variant_labels or DEFAULT_VARIANT_LABELS)
    try:
        report = build_frame_transition_audit_report(
            clean_report_path=args.clean_report,
            dirty_report_path=args.dirty_report,
            variant_labels=labels,
        )
    except Exception as exc:
        report = {
            "stage": "bed_native_opt_in_frame_transition_audit",
            "status": "runtime_failure",
            "claim_boundary": CLAIM_BOUNDARY,
            "fallback_reason": f"{type(exc).__name__}: {exc}",
        }
        print(json.dumps(_json_safe(report), sort_keys=True, allow_nan=False))
        return 2

    report = _json_safe(report)
    encoded = json.dumps(report, sort_keys=True, allow_nan=False)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    print(encoded)
    return 0 if report["status"] == "frame_transition_audit_recorded" else 2


def build_frame_transition_audit_report(
    *,
    clean_report_path: Path,
    dirty_report_path: Path,
    variant_labels: tuple[str, ...] = DEFAULT_VARIANT_LABELS,
) -> dict[str, object]:
    clean_report = _load_report(clean_report_path)
    dirty_report = _load_report(dirty_report_path)
    clean_frame = _frame_count(clean_report)
    dirty_frame = _frame_count(dirty_report)

    variant_audits = {
        label: _variant_transition_audit(clean_report, dirty_report, label)
        for label in variant_labels
    }
    all_model_invariants_equal = all(
        all(audit["model_invariants"].values()) for audit in variant_audits.values()
    )
    all_final_contact_shape_labels_equal = all(
        audit["contact_invariants"]["final_contact_shape1_labels_equal"]
        for audit in variant_audits.values()
    )
    clean_to_dirty = all(
        audit["clean"]["status"] == "smoke_passed"
        and audit["dirty"]["status"] == "runtime_failure"
        for audit in variant_audits.values()
    )

    return {
        "stage": "bed_native_opt_in_frame_transition_audit",
        "status": "frame_transition_audit_recorded",
        "claim_boundary": CLAIM_BOUNDARY,
        "interpretation_boundary": INTERPRETATION_BOUNDARY,
        "clean_report": str(clean_report_path),
        "dirty_report": str(dirty_report_path),
        "clean_frame": clean_frame,
        "dirty_frame": dirty_frame,
        "transition_summary": {
            "status": (
                "clean_to_dirty_control_transition_recorded"
                if clean_to_dirty
                else "frame_transition_recorded"
            ),
            "variant_count": len(variant_audits),
            "all_model_invariants_equal": all_model_invariants_equal,
            "all_final_contact_shape_labels_equal": all_final_contact_shape_labels_equal,
        },
        "variant_audits": variant_audits,
    }


def _load_report(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        report = json.load(handle)
    if not isinstance(report, dict):
        raise ValueError(f"report must be a JSON object: {path}")
    if report.get("status") != "diagnostic_recorded":
        raise ValueError(f"report must have status diagnostic_recorded: {path}")
    return report


def _frame_count(report: dict[str, Any]) -> int:
    drop_options = report.get("drop_settle_options")
    if not isinstance(drop_options, dict) or not isinstance(drop_options.get("frames"), int):
        raise ValueError("report missing integer drop_settle_options.frames")
    return int(drop_options["frames"])


def _variant_transition_audit(
    clean_report: dict[str, Any],
    dirty_report: dict[str, Any],
    label: str,
) -> dict[str, object]:
    clean_variant = _variant_payload(clean_report, label)
    dirty_variant = _variant_payload(dirty_report, label)
    clean_state = _state_summary(clean_variant)
    dirty_state = _state_summary(dirty_variant)
    clean_contact_labels = _final_contact_shape1_labels(clean_variant)
    dirty_contact_labels = _final_contact_shape1_labels(dirty_variant)
    return {
        "clean": clean_state,
        "dirty": dirty_state,
        "deltas": {
            "completed_steps_delta": _delta(
                dirty_state.get("completed_steps"),
                clean_state.get("completed_steps"),
            ),
            "final_linear_speed_delta_mps": _delta(
                dirty_state.get("final_linear_speed_mps"),
                clean_state.get("final_linear_speed_mps"),
            ),
            "final_linear_velocity_delta": _vector_delta(
                dirty_state.get("final_linear_velocity"),
                clean_state.get("final_linear_velocity"),
            ),
            "final_support_height_delta": _delta(
                dirty_state.get("final_support_height"),
                clean_state.get("final_support_height"),
            ),
            "final_body_position_delta": _vector_delta(
                dirty_state.get("final_body_position"),
                clean_state.get("final_body_position"),
            ),
            "final_angular_velocity_delta": _vector_delta(
                dirty_state.get("final_angular_velocity_raw"),
                clean_state.get("final_angular_velocity_raw"),
            ),
        },
        "aligned_final_window_rows": _aligned_final_window_rows(
            clean_variant,
            dirty_variant,
            clean_state,
            dirty_state,
        ),
        "model_invariants": _model_invariants(clean_variant, dirty_variant),
        "contact_invariants": {
            "final_contact_count_equal": clean_state.get("final_contact_count")
            == dirty_state.get("final_contact_count"),
            "final_contact_shape1_labels_equal": clean_contact_labels == dirty_contact_labels,
            "clean_final_contact_shape1_labels": clean_contact_labels,
            "dirty_final_contact_shape1_labels": dirty_contact_labels,
        },
        "interpretation": (
            "adjacent_frame_final_speed_transition_with_model_and_contact_label_audit_only"
        ),
    }


def _variant_payload(report: dict[str, Any], label: str) -> dict[str, Any]:
    variants = report.get("variants")
    if not isinstance(variants, dict):
        raise ValueError("report missing variants mapping")
    payload = variants.get(label)
    if not isinstance(payload, dict):
        raise ValueError(f"report missing variant: {label}")
    return payload


def _state_summary(variant: dict[str, Any]) -> dict[str, object]:
    run = variant.get("drop_settle_run")
    if not isinstance(run, dict):
        raise ValueError("variant missing drop_settle_run")
    final_sample = _final_trace_sample(variant)
    return {
        "status": run.get("status", variant.get("status")),
        "failure_labels": list(run.get("failure_labels") or []),
        "completed_steps": run.get("completed_steps"),
        "final_linear_speed_mps": run.get("final_linear_speed_mps"),
        "final_linear_velocity": run.get("final_linear_velocity"),
        "final_support_height": run.get("final_support_height"),
        "final_contact_count": run.get("final_contact_count"),
        "final_body_position": final_sample.get("body_position"),
        "final_angular_velocity_raw": final_sample.get("angular_velocity_raw"),
    }


def _final_trace_sample(variant: dict[str, Any]) -> dict[str, Any]:
    samples = variant.get("trace_samples")
    if not isinstance(samples, list) or not samples:
        return {}
    dict_samples = [sample for sample in samples if isinstance(sample, dict)]
    if not dict_samples:
        return {}
    return max(dict_samples, key=lambda sample: int(sample.get("step", -1)))


def _aligned_final_window_rows(
    clean_variant: dict[str, Any],
    dirty_variant: dict[str, Any],
    clean_state: dict[str, object],
    dirty_state: dict[str, object],
    *,
    max_rows: int = 3,
) -> list[dict[str, object]]:
    clean_completed_steps = clean_state.get("completed_steps")
    dirty_completed_steps = dirty_state.get("completed_steps")
    if not isinstance(clean_completed_steps, int | float) or not isinstance(
        dirty_completed_steps,
        int | float,
    ):
        return []

    clean_samples = _samples_by_steps_from_final(clean_variant, int(clean_completed_steps))
    dirty_samples = _samples_by_steps_from_final(dirty_variant, int(dirty_completed_steps))
    common_offsets = sorted(
        offset for offset in set(clean_samples) & set(dirty_samples) if offset <= 0
    )
    rows = []
    for offset in common_offsets[-max_rows:]:
        clean_sample = clean_samples[offset]
        dirty_sample = dirty_samples[offset]
        rows.append(
            {
                "steps_from_final": offset,
                "clean_step": clean_sample.get("step"),
                "dirty_step": dirty_sample.get("step"),
                "clean_linear_speed_mps": clean_sample.get("linear_speed_mps"),
                "dirty_linear_speed_mps": dirty_sample.get("linear_speed_mps"),
                "linear_speed_delta_mps": _delta(
                    dirty_sample.get("linear_speed_mps"),
                    clean_sample.get("linear_speed_mps"),
                ),
                "clean_support_height": clean_sample.get("support_height"),
                "dirty_support_height": dirty_sample.get("support_height"),
                "support_height_delta": _delta(
                    dirty_sample.get("support_height"),
                    clean_sample.get("support_height"),
                ),
                "clean_contact_count": clean_sample.get("contact_count"),
                "dirty_contact_count": dirty_sample.get("contact_count"),
                "clean_body_position": clean_sample.get("body_position"),
                "dirty_body_position": dirty_sample.get("body_position"),
                "body_position_delta": _vector_delta(
                    dirty_sample.get("body_position"),
                    clean_sample.get("body_position"),
                ),
            }
        )
    return rows


def _samples_by_steps_from_final(
    variant: dict[str, Any],
    completed_steps: int,
) -> dict[int, dict[str, Any]]:
    samples = variant.get("trace_samples")
    if not isinstance(samples, list):
        return {}
    result = {}
    for sample in samples:
        if not isinstance(sample, dict) or not isinstance(sample.get("step"), int | float):
            continue
        result[int(sample["step"]) - completed_steps] = sample
    return result


def _final_contact_shape1_labels(variant: dict[str, Any]) -> list[str]:
    sample = _final_trace_sample(variant)
    details = sample.get("contact_details")
    if not isinstance(details, list):
        return []
    labels = []
    for detail in details:
        if isinstance(detail, dict) and isinstance(detail.get("shape1_label"), str):
            labels.append(detail["shape1_label"])
    return labels


def _model_invariants(
    clean_variant: dict[str, Any],
    dirty_variant: dict[str, Any],
) -> dict[str, bool]:
    clean_model = clean_variant.get("model_summary") or {}
    dirty_model = dirty_variant.get("model_summary") or {}
    if not isinstance(clean_model, dict):
        clean_model = {}
    if not isinstance(dirty_model, dict):
        dirty_model = {}
    return {
        "body_mass_equal": clean_model.get("body_mass") == dirty_model.get("body_mass"),
        "body_inv_mass_equal": clean_model.get("body_inv_mass") == dirty_model.get("body_inv_mass"),
        "body_com_equal": clean_model.get("body_com") == dirty_model.get("body_com"),
        "body_inertia_equal": clean_model.get("body_inertia") == dirty_model.get("body_inertia"),
        "body_inv_inertia_equal": clean_model.get("body_inv_inertia")
        == dirty_model.get("body_inv_inertia"),
        "package_anchor_equal": clean_variant.get("package_anchor") == dirty_variant.get("package_anchor"),
        "type_counts_equal": clean_variant.get("type_counts") == dirty_variant.get("type_counts"),
    }


def _delta(left: object, right: object) -> object:
    if not isinstance(left, int | float) or not isinstance(right, int | float):
        return None
    return _round_float(float(left) - float(right))


def _vector_delta(left: object, right: object) -> object:
    if not isinstance(left, list) or not isinstance(right, list) or len(left) != len(right):
        return None
    result = []
    for left_value, right_value in zip(left, right, strict=True):
        if not isinstance(left_value, int | float) or not isinstance(right_value, int | float):
            return None
        result.append(_round_float(float(left_value) - float(right_value)))
    return result


def _round_float(value: float) -> float:
    return round(value, 12)


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


if __name__ == "__main__":
    raise SystemExit(main())
