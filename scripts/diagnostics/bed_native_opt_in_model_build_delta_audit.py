#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


CLAIM_BOUNDARY = (
    "bed_native_opt_in_model_build_delta_audit_not_root_cause_or_fix_or_stability_evidence"
)
INTERPRETATION_BOUNDARY = (
    "model_build_delta_audit_records_existing_pre_solver_model_accounting_only; "
    "it is not root-cause proof, a Newton mapping bug proof, a validated fix, "
    "stability evidence, scoring evidence, or collision-quality validation"
)
PIECE_LABELS = (
    "native_target_full_anchor",
    "native_opt_in_target_full_anchor",
    "native_rest_without_target_full_anchor",
    "native_opt_in_rest_without_target_full_anchor",
    "native_full",
    "native_opt_in_full",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Summarize the existing capped-bed primitive-6 model-build audit deltas "
            "without importing Newton or rerunning simulation."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = build_model_build_delta_audit_report(report_path=args.report)
    except Exception as exc:
        report = {
            "stage": "bed_native_opt_in_model_build_delta_audit",
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
    return 0 if report["status"] == "model_build_delta_audit_recorded" else 2


def build_model_build_delta_audit_report(*, report_path: Path) -> dict[str, object]:
    source_report = _load_report(report_path)
    model_build_audit = _model_build_audit(source_report)
    delta_summary = _dict_field(model_build_audit, "delta_summary")
    pieces = _dict_field(model_build_audit, "pieces")

    return {
        "stage": "bed_native_opt_in_model_build_delta_audit",
        "status": "model_build_delta_audit_recorded",
        "claim_boundary": CLAIM_BOUNDARY,
        "interpretation_boundary": INTERPRETATION_BOUNDARY,
        "report": str(report_path),
        "source_stage": source_report.get("stage"),
        "source_status": source_report.get("status"),
        "summary": {
            "anchor_match": bool(model_build_audit.get("anchor_match")),
            "target_index": model_build_audit.get(
                "target_index",
                source_report.get("target_index"),
            ),
            "target_source_faces": list(
                model_build_audit.get(
                    "target_source_faces",
                    source_report.get("target_source_faces") or [],
                )
                or []
            ),
            "rest_without_target_delta_zero": _all_numeric_zero(
                delta_summary.get("rest_opt_in_minus_native")
            ),
            "target_delta_nonzero": _any_numeric_nonzero(
                delta_summary.get("target_opt_in_minus_native")
            ),
            "full_delta_nonzero": _any_numeric_nonzero(
                delta_summary.get("full_opt_in_minus_native")
            ),
        },
        "target_shape_audit": _target_shape_audit(pieces),
        "delta_summary": delta_summary,
        "piece_summaries": {
            label: _piece_summary(piece)
            for label in PIECE_LABELS
            if isinstance((piece := pieces.get(label)), dict)
        },
    }


def _load_report(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        report = json.load(handle)
    if not isinstance(report, dict):
        raise ValueError(f"report must be a JSON object: {path}")
    if report.get("status") != "diagnostic_recorded":
        raise ValueError(f"report must have status diagnostic_recorded: {path}")
    return report


def _model_build_audit(report: dict[str, Any]) -> dict[str, Any]:
    audit = report.get("model_build_audit")
    if not isinstance(audit, dict):
        raise ValueError("report missing model_build_audit object")
    if audit.get("status") != "diagnostic_recorded":
        raise ValueError("model_build_audit must have status diagnostic_recorded")
    return audit


def _dict_field(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"model_build_audit missing {key} object")
    return value


def _target_shape_audit(pieces: dict[str, Any]) -> dict[str, object]:
    native = _piece_summary(_piece(pieces, "native_target_full_anchor"))
    opt_in = _piece_summary(_piece(pieces, "native_opt_in_target_full_anchor"))
    native_scale = native.get("shape_scale")
    opt_in_scale = opt_in.get("shape_scale")
    return {
        "native_target_primitive_id": _first_string(native.get("primitive_ids")),
        "native_opt_in_target_primitive_id": _first_string(opt_in.get("primitive_ids")),
        "native_target_shape_scale": native_scale,
        "native_opt_in_target_shape_scale": opt_in_scale,
        "target_shape_scale_delta": _vector_delta(opt_in_scale, native_scale),
    }


def _piece(pieces: dict[str, Any], label: str) -> dict[str, Any]:
    piece = pieces.get(label)
    if not isinstance(piece, dict):
        raise ValueError(f"model_build_audit missing piece: {label}")
    return piece


def _piece_summary(piece: dict[str, Any]) -> dict[str, object]:
    model_summary = piece.get("model_summary") or {}
    if not isinstance(model_summary, dict):
        model_summary = {}
    primitive_count = piece.get("primitive_count")
    return {
        "primitive_count": primitive_count,
        "primitive_ids": list(piece.get("primitive_ids") or []),
        "body_mass": _first_numeric(model_summary.get("body_mass")),
        "body_com": _first_row(model_summary.get("body_com")),
        "body_inertia_row0": _matrix_row(model_summary.get("body_inertia"), row_index=0),
        "shape_scale": (
            _first_row(model_summary.get("shape_scale")) if primitive_count == 1 else None
        ),
    }


def _first_string(value: object) -> object:
    if not isinstance(value, list) or not value or not isinstance(value[0], str):
        return None
    return value[0]


def _first_numeric(value: object) -> object:
    if not isinstance(value, list) or not value or not isinstance(value[0], int | float):
        return None
    return value[0]


def _first_row(value: object) -> object:
    if not isinstance(value, list) or not value or not isinstance(value[0], list):
        return None
    row = value[0]
    if not all(isinstance(item, int | float) for item in row):
        return None
    return list(row)


def _matrix_row(value: object, *, row_index: int) -> object:
    if not isinstance(value, list) or not value or not isinstance(value[0], list):
        return None
    matrix = value[0]
    if len(matrix) <= row_index or not isinstance(matrix[row_index], list):
        return None
    row = matrix[row_index]
    if not all(isinstance(item, int | float) for item in row):
        return None
    return list(row)


def _vector_delta(left: object, right: object) -> object:
    if not isinstance(left, list) or not isinstance(right, list) or len(left) != len(right):
        return None
    result = []
    for left_value, right_value in zip(left, right, strict=True):
        if not isinstance(left_value, int | float) or not isinstance(right_value, int | float):
            return None
        result.append(_round_float(float(left_value) - float(right_value)))
    return result


def _all_numeric_zero(value: object) -> bool:
    leaves = list(_numeric_leaves(value))
    return bool(leaves) and all(abs(leaf) <= 1e-12 for leaf in leaves)


def _any_numeric_nonzero(value: object) -> bool:
    return any(abs(leaf) > 1e-12 for leaf in _numeric_leaves(value))


def _numeric_leaves(value: object) -> list[float]:
    if isinstance(value, int | float):
        return [float(value)]
    if isinstance(value, dict):
        result: list[float] = []
        for item in value.values():
            result.extend(_numeric_leaves(item))
        return result
    if isinstance(value, list):
        result = []
        for item in value:
            result.extend(_numeric_leaves(item))
        return result
    return []


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
