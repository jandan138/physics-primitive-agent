#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


DEFAULT_BASELINE_LABELS = (
    "native_control_box",
    "native_opt_in_cylinder_reverted",
)
DEFAULT_TARGET_LABEL = "native_opt_in_cylinder"
CLAIM_BOUNDARY = (
    "bed_native_opt_in_clean_frame_blocker_audit_not_root_cause_or_fix_or_stability_evidence"
)
INTERPRETATION_BOUNDARY = (
    "clean_frame_blocker_audit_records_one_report_control_vs_target_behavior_only; "
    "it is not sustained-settle evidence, a validated fix, root-cause proof, "
    "or collision-quality validation"
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Compare a failing capped-bed opt-in cylinder variant against clean controls "
            "inside one frame-window Newton report."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--target-label", default=DEFAULT_TARGET_LABEL)
    parser.add_argument(
        "--baseline-label",
        action="append",
        dest="baseline_labels",
        help="clean baseline variant label to compare; repeat to compare multiple baselines",
    )
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    baseline_labels = tuple(args.baseline_labels or DEFAULT_BASELINE_LABELS)
    try:
        report = build_clean_frame_blocker_audit_report(
            report_path=args.report,
            target_label=args.target_label,
            baseline_labels=baseline_labels,
        )
    except Exception as exc:
        report = {
            "stage": "bed_native_opt_in_clean_frame_blocker_audit",
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
    return 0 if report["status"] == "clean_frame_blocker_audit_recorded" else 2


def build_clean_frame_blocker_audit_report(
    *,
    report_path: Path,
    target_label: str = DEFAULT_TARGET_LABEL,
    baseline_labels: tuple[str, ...] = DEFAULT_BASELINE_LABELS,
) -> dict[str, object]:
    source_report = _load_report(report_path)
    frame = _frame_count(source_report)
    target_variant = _variant_payload(source_report, target_label)
    target_state = _state_summary(target_variant)
    baseline_audits = {
        label: _baseline_audit(
            baseline_variant=_variant_payload(source_report, label),
            target_variant=target_variant,
        )
        for label in baseline_labels
    }
    return {
        "stage": "bed_native_opt_in_clean_frame_blocker_audit",
        "status": "clean_frame_blocker_audit_recorded",
        "claim_boundary": CLAIM_BOUNDARY,
        "interpretation_boundary": INTERPRETATION_BOUNDARY,
        "report": str(report_path),
        "frame": frame,
        "target_label": target_label,
        "baseline_labels": list(baseline_labels),
        "summary": {
            "target_status": target_state.get("status"),
            "target_failure_labels": target_state.get("failure_labels"),
            "baseline_count": len(baseline_audits),
            "all_baselines_smoke_passed": all(
                audit["baseline"]["status"] == "smoke_passed"
                for audit in baseline_audits.values()
            ),
            "all_final_contact_counts_equal": all(
                audit["contact_invariants"]["final_contact_count_equal"]
                for audit in baseline_audits.values()
            ),
            "all_final_contact_primitive_suffixes_equal": all(
                audit["contact_invariants"]["final_contact_primitive_suffixes_equal"]
                for audit in baseline_audits.values()
            ),
        },
        "baseline_audits": baseline_audits,
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


def _variant_payload(report: dict[str, Any], label: str) -> dict[str, Any]:
    variants = report.get("variants")
    if not isinstance(variants, dict):
        raise ValueError("report missing variants mapping")
    payload = variants.get(label)
    if not isinstance(payload, dict):
        raise ValueError(f"report missing variant: {label}")
    return payload


def _baseline_audit(
    *,
    baseline_variant: dict[str, Any],
    target_variant: dict[str, Any],
) -> dict[str, object]:
    baseline_state = _state_summary(baseline_variant)
    target_state = _state_summary(target_variant)
    baseline_labels = _final_contact_shape1_labels(baseline_variant)
    target_labels = _final_contact_shape1_labels(target_variant)
    baseline_suffixes = [_primitive_suffix(label) for label in baseline_labels]
    target_suffixes = [_primitive_suffix(label) for label in target_labels]
    return {
        "baseline": baseline_state,
        "target": target_state,
        "deltas": {
            "completed_steps_delta": _delta(
                target_state.get("completed_steps"),
                baseline_state.get("completed_steps"),
            ),
            "final_linear_speed_delta_mps": _delta(
                target_state.get("final_linear_speed_mps"),
                baseline_state.get("final_linear_speed_mps"),
            ),
            "final_linear_velocity_delta": _vector_delta(
                target_state.get("final_linear_velocity"),
                baseline_state.get("final_linear_velocity"),
            ),
            "final_support_height_delta": _delta(
                target_state.get("final_support_height"),
                baseline_state.get("final_support_height"),
            ),
            "final_body_position_delta": _vector_delta(
                target_state.get("final_body_position"),
                baseline_state.get("final_body_position"),
            ),
            "final_angular_velocity_delta": _vector_delta(
                target_state.get("final_angular_velocity_raw"),
                baseline_state.get("final_angular_velocity_raw"),
            ),
        },
        "model_deltas": _model_deltas(baseline_variant, target_variant),
        "contact_invariants": {
            "final_contact_count_equal": baseline_state.get("final_contact_count")
            == target_state.get("final_contact_count"),
            "final_contact_primitive_suffixes_equal": baseline_suffixes == target_suffixes,
            "baseline_final_contact_shape1_labels": baseline_labels,
            "target_final_contact_shape1_labels": target_labels,
            "baseline_final_contact_primitive_suffixes": baseline_suffixes,
            "target_final_contact_primitive_suffixes": target_suffixes,
        },
        "aligned_final_window_rows": _aligned_final_window_rows(
            baseline_variant,
            target_variant,
            baseline_state,
            target_state,
        ),
        "interpretation": (
            "clean_frame_target_blocker_contrast_with_matching_final_contact_suffix_audit_only"
        ),
    }


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
        "tail_linear_speed_summary": variant.get("tail_linear_speed_summary"),
        "final_body_position": final_sample.get("body_position"),
        "final_angular_velocity_raw": final_sample.get("angular_velocity_raw"),
    }


def _model_deltas(
    baseline_variant: dict[str, Any],
    target_variant: dict[str, Any],
) -> dict[str, object]:
    baseline_model = baseline_variant.get("model_summary") or {}
    target_model = target_variant.get("model_summary") or {}
    if not isinstance(baseline_model, dict):
        baseline_model = {}
    if not isinstance(target_model, dict):
        target_model = {}
    return {
        "type_counts_equal": baseline_variant.get("type_counts") == target_variant.get("type_counts"),
        "package_anchor_equal": baseline_variant.get("package_anchor")
        == target_variant.get("package_anchor"),
        "body_mass_delta": _single_value_delta(
            target_model.get("body_mass"),
            baseline_model.get("body_mass"),
        ),
        "body_inv_mass_delta": _single_value_delta(
            target_model.get("body_inv_mass"),
            baseline_model.get("body_inv_mass"),
        ),
        "body_com_delta": _first_row_delta(
            target_model.get("body_com"),
            baseline_model.get("body_com"),
        ),
        "body_inertia_row0_delta": _matrix_row_delta(
            target_model.get("body_inertia"),
            baseline_model.get("body_inertia"),
            row_index=0,
        ),
        "body_inv_inertia_row0_delta": _matrix_row_delta(
            target_model.get("body_inv_inertia"),
            baseline_model.get("body_inv_inertia"),
            row_index=0,
        ),
    }


def _aligned_final_window_rows(
    baseline_variant: dict[str, Any],
    target_variant: dict[str, Any],
    baseline_state: dict[str, object],
    target_state: dict[str, object],
    *,
    max_rows: int = 3,
) -> list[dict[str, object]]:
    baseline_completed_steps = baseline_state.get("completed_steps")
    target_completed_steps = target_state.get("completed_steps")
    if not isinstance(baseline_completed_steps, int | float) or not isinstance(
        target_completed_steps,
        int | float,
    ):
        return []

    baseline_samples = _samples_by_steps_from_final(
        baseline_variant,
        int(baseline_completed_steps),
    )
    target_samples = _samples_by_steps_from_final(target_variant, int(target_completed_steps))
    common_offsets = sorted(
        offset for offset in set(baseline_samples) & set(target_samples) if offset <= 0
    )
    rows = []
    for offset in common_offsets[-max_rows:]:
        baseline_sample = baseline_samples[offset]
        target_sample = target_samples[offset]
        rows.append(
            {
                "steps_from_final": offset,
                "baseline_step": baseline_sample.get("step"),
                "target_step": target_sample.get("step"),
                "baseline_linear_speed_mps": baseline_sample.get("linear_speed_mps"),
                "target_linear_speed_mps": target_sample.get("linear_speed_mps"),
                "linear_speed_delta_mps": _delta(
                    target_sample.get("linear_speed_mps"),
                    baseline_sample.get("linear_speed_mps"),
                ),
                "baseline_support_height": baseline_sample.get("support_height"),
                "target_support_height": target_sample.get("support_height"),
                "support_height_delta": _delta(
                    target_sample.get("support_height"),
                    baseline_sample.get("support_height"),
                ),
                "baseline_contact_count": baseline_sample.get("contact_count"),
                "target_contact_count": target_sample.get("contact_count"),
                "baseline_body_position": baseline_sample.get("body_position"),
                "target_body_position": target_sample.get("body_position"),
                "body_position_delta": _vector_delta(
                    target_sample.get("body_position"),
                    baseline_sample.get("body_position"),
                ),
            }
        )
    return rows


def _final_trace_sample(variant: dict[str, Any]) -> dict[str, Any]:
    samples = variant.get("trace_samples")
    if not isinstance(samples, list) or not samples:
        return {}
    dict_samples = [sample for sample in samples if isinstance(sample, dict)]
    if not dict_samples:
        return {}
    return max(dict_samples, key=lambda sample: int(sample.get("step", -1)))


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


def _primitive_suffix(label: str) -> str:
    marker = ":primitive:"
    if marker not in label:
        return label
    return label.split(marker, maxsplit=1)[1]


def _single_value_delta(left: object, right: object) -> object:
    if (
        not isinstance(left, list)
        or not isinstance(right, list)
        or not left
        or not right
        or not isinstance(left[0], int | float)
        or not isinstance(right[0], int | float)
    ):
        return None
    return _round_float(float(left[0]) - float(right[0]))


def _first_row_delta(left: object, right: object) -> object:
    if not isinstance(left, list) or not isinstance(right, list) or not left or not right:
        return None
    return _vector_delta(left[0], right[0])


def _matrix_row_delta(left: object, right: object, *, row_index: int) -> object:
    if not isinstance(left, list) or not isinstance(right, list) or not left or not right:
        return None
    left_matrix = left[0]
    right_matrix = right[0]
    if not isinstance(left_matrix, list) or not isinstance(right_matrix, list):
        return None
    if len(left_matrix) <= row_index or len(right_matrix) <= row_index:
        return None
    return _vector_delta(left_matrix[row_index], right_matrix[row_index])


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
