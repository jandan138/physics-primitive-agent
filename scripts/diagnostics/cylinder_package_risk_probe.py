#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from primitive_collision_compiler.contracts import CollisionPackage, FallbackSpec, PrimitiveSpec
from primitive_collision_compiler.diagnostics.cylinder_package_risk import (
    build_cylinder_package_body_state_risk_report,
)


DEFAULT_BED_TASK_REPORT = Path("reports/generated/cylinder_stability_mechanism/bed_task.json")
DEFAULT_FRANKA_TASK_REPORT = Path(
    "reports/generated/cylinder_stability_mechanism/franka_cost_guided_task.json"
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build a bed/Franka cylinder package body-state risk report from existing task "
            "reports without importing Newton or copying Newton model arrays."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--bed-task-report", type=Path, default=DEFAULT_BED_TASK_REPORT)
    parser.add_argument("--franka-task-report", type=Path, default=DEFAULT_FRANKA_TASK_REPORT)
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = build_package_risk_probe_report(
            bed_task_report_path=args.bed_task_report,
            franka_task_report_path=args.franka_task_report,
        )
    except Exception as exc:
        report = {
            "stage": "cylinder_package_body_state_risk_probe",
            "status": "runtime_failure",
            "fallback_reason": f"{type(exc).__name__}: {exc}",
        }
        print(json.dumps(_json_safe(report), sort_keys=True, allow_nan=False))
        return 2

    safe_report = _json_safe(report)
    encoded = json.dumps(safe_report, sort_keys=True, allow_nan=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    print(encoded)
    return 0 if safe_report.get("status") == "diagnostic_recorded" else 2


def build_package_risk_probe_report(
    *,
    bed_task_report_path: Path,
    franka_task_report_path: Path,
) -> dict[str, object]:
    bed_case = _case_for_role(_load_json(bed_task_report_path), "bed")
    franka_case = _case_for_role(_load_json(franka_task_report_path), "franka")
    return build_cylinder_package_body_state_risk_report(
        cases={
            "bed": {
                "native": _package_from_payload(bed_case["native"]["collision_package"]),
                "native_opt_in": _package_from_payload(
                    bed_case["native_opt_in"]["collision_package"]
                ),
                "native_drop_evidence": _drop_summary(bed_case.get("native_tasks", {})),
                "native_opt_in_drop_evidence": _drop_summary(
                    bed_case["native_opt_in_tasks"]
                ),
            },
            "franka": {
                "native": _package_from_payload(franka_case["native"]["collision_package"]),
                "native_opt_in": _package_from_payload(
                    franka_case["native_opt_in"]["collision_package"]
                ),
                "native_drop_evidence": _drop_summary(franka_case.get("native_tasks", {})),
                "native_opt_in_drop_evidence": _drop_summary(
                    franka_case["native_opt_in_tasks"]
                ),
            },
        },
    )


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"task report must be a JSON object: {path}")
    return payload


def _case_for_role(report: dict[str, Any], role_marker: str) -> dict[str, Any]:
    cases = report.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("task report must contain cases")
    matches = [
        case
        for case in cases
        if isinstance(case, dict) and role_marker in str(case.get("asset_role", "")).lower()
    ]
    if len(matches) == 1:
        return matches[0]
    if len(cases) == 1 and isinstance(cases[0], dict):
        return cases[0]
    raise ValueError(f"task report must contain exactly one {role_marker!r} case")


def _package_from_payload(payload: dict[str, Any]) -> CollisionPackage:
    fallback_payload = payload.get("fallback")
    fallback = None
    if isinstance(fallback_payload, dict):
        fallback = FallbackSpec(
            method=str(fallback_payload.get("method", "")),
            reason=str(fallback_payload.get("reason", "")),
        )
    return CollisionPackage(
        asset_id=str(payload.get("asset_id", "")),
        package_id=str(payload.get("package_id", "")),
        primitives=tuple(_primitive_from_payload(item) for item in payload.get("primitives", [])),
        fallback=fallback,
        source_path=str(payload.get("source_path", "")),
        source_sha256=str(payload.get("source_sha256", "")),
        method=str(payload.get("method", "primitive_first")),
        stage=str(payload.get("stage", "")),
        status=str(payload.get("status", "candidate")),
        claim_boundary=str(payload.get("claim_boundary", "")),
        mesh_point_count=int(payload.get("mesh_point_count") or 0),
        mesh_face_count=int(payload.get("mesh_face_count") or 0),
        max_source_faces=payload.get("max_source_faces"),
        primitive_subset=tuple(payload.get("primitive_subset") or ()),
        unsupported_primitives=tuple(payload.get("unsupported_primitives") or ()),
    )


def _primitive_from_payload(payload: dict[str, Any]) -> PrimitiveSpec:
    return PrimitiveSpec(
        kind=str(payload.get("kind", "")),
        pose=tuple(payload.get("pose") or ()),
        dimensions=payload.get("dimensions") or {},
        primitive_id=str(payload.get("primitive_id", "")),
        center=tuple(payload.get("center") or (0.0, 0.0, 0.0)),
        axes=tuple(tuple(axis) for axis in (payload.get("axes") or ())),
        frame=str(payload.get("frame", "asset")),
        source_faces=tuple(payload.get("source_faces") or ()),
        contains_assigned_points=payload.get("contains_assigned_points"),
        volume=payload.get("volume"),
        weighted_volume=payload.get("weighted_volume"),
        conversion_status=str(payload.get("conversion_status", "candidate")),
    )


def _drop_summary(tasks: dict[str, Any]) -> dict[str, object]:
    drop = tasks.get("drop_settle", {})
    runs = drop.get("drop_settle_runs", []) if isinstance(drop, dict) else []
    run = runs[0] if runs and isinstance(runs[0], dict) else {}
    return {
        "status": drop.get("status") if isinstance(drop, dict) else None,
        "failure_labels": _list_or_empty(run.get("failure_labels")),
        "final_linear_speed_mps": run.get("final_linear_speed_mps"),
    }


def _list_or_empty(value: object) -> list[object]:
    if isinstance(value, (list, tuple)) and not isinstance(value, (str, bytes)):
        return list(value)
    return []


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, (int, str, bool)) or value is None:
        return value
    return value


if __name__ == "__main__":
    raise SystemExit(main())
