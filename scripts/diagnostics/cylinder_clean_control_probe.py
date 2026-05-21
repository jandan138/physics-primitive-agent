#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
import io
import json
import math
import os
from dataclasses import replace
from pathlib import Path
from typing import Any

import numpy as np

from primitive_collision_compiler.contracts import CollisionPackage, FallbackSpec, PrimitiveSpec
from primitive_collision_compiler.diagnostics.cylinder_clean_controls import (
    build_cylinder_clean_control_report,
)
from primitive_collision_compiler.newton.drop_settle import (
    DropSettleOptions,
    run_newton_drop_settle,
)


DEFAULT_PAIR_REST_INDICES = (0, 3, 10, 16, 17, 24)
DEFAULT_BED_TASK_REPORT = Path("reports/generated/cylinder_stability_mechanism/bed_task.json")
DEFAULT_FRANKA_TASK_REPORT = Path(
    "reports/generated/cylinder_stability_mechanism/franka_cost_guided_task.json"
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a compact bed/Franka cylinder clean-control Newton probe.",
    )
    parser.add_argument("--bed-task-report", type=Path, default=DEFAULT_BED_TASK_REPORT)
    parser.add_argument("--franka-task-report", type=Path, default=DEFAULT_FRANKA_TASK_REPORT)
    parser.add_argument("--source-dir", default=os.environ.get("NEWTON_SOURCE_DIR", ""))
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--frames", type=int, default=360)
    parser.add_argument("--substeps", type=int, default=8)
    parser.add_argument("--iterations", type=int, default=2)
    parser.add_argument(
        "--pair-rest-index",
        type=int,
        action="append",
        default=None,
        help="Bed rest primitive index to pair with the target box/cylinder. Repeatable.",
    )
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    pair_rest_indices = tuple(args.pair_rest_index or DEFAULT_PAIR_REST_INDICES)
    report = run_probe(
        bed_task_report_path=args.bed_task_report,
        franka_task_report_path=args.franka_task_report,
        source_dir=args.source_dir,
        device=args.device,
        options=DropSettleOptions(
            frames=args.frames,
            substeps=args.substeps,
            iterations=args.iterations,
        ),
        pair_rest_indices=pair_rest_indices,
    )
    safe_report = _json_safe(report)
    encoded = json.dumps(safe_report, sort_keys=True, allow_nan=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n")
    else:
        print(encoded)
    return 0


def run_probe(
    *,
    bed_task_report_path: Path,
    franka_task_report_path: Path,
    source_dir: str,
    device: str,
    options: DropSettleOptions,
    pair_rest_indices: tuple[int, ...],
) -> dict[str, object]:
    if not source_dir:
        raise ValueError("--source-dir or NEWTON_SOURCE_DIR is required")
    bed_task_report = _load_json(bed_task_report_path)
    franka_task_report = _load_json(franka_task_report_path)
    bed_case = _case_for_role(bed_task_report, "bed")
    franka_case = _case_for_role(franka_task_report, "franka")
    bed_native = _package_from_payload(bed_case["native"]["collision_package"])
    bed_opt_in = _package_from_payload(bed_case["native_opt_in"]["collision_package"])
    franka_opt_in = _package_from_payload(franka_case["native_opt_in"]["collision_package"])

    bed_box_target = replace(bed_native.primitives[6], primitive_id="bed_target_box")
    bed_cylinder_target = replace(bed_opt_in.primitives[6], primitive_id="bed_target_cylinder")
    franka_cylinder_target = _largest_cylinder(franka_opt_in)

    single_controls = {
        "bed_cylinder_only_actual_axes": _run_package(
            _single_package("bed_cylinder_only_actual_axes", bed_cylinder_target),
            source_dir=source_dir,
            device=device,
            options=options,
        ),
        "bed_box_only_actual_axes": _run_package(
            _single_package("bed_box_only_actual_axes", bed_box_target),
            source_dir=source_dir,
            device=device,
            options=options,
        ),
        "franka_largest_cylinder_only": _run_package(
            _single_package(
                "franka_largest_cylinder_only",
                replace(franka_cylinder_target, primitive_id="franka_largest_cylinder"),
            ),
            source_dir=source_dir,
            device=device,
            options=options,
        ),
    }

    pair_controls = []
    for rest_index in pair_rest_indices:
        if rest_index == 6:
            raise ValueError("pair-rest-index 6 is the bed target primitive")
        if rest_index < 0 or rest_index >= len(bed_opt_in.primitives):
            raise ValueError(f"pair-rest-index out of range: {rest_index}")
        rest = bed_opt_in.primitives[rest_index]
        pair_controls.append(
            {
                "rest_index": rest_index,
                "rest_source_faces": list(rest.source_faces),
                "box": _run_package(
                    _pair_package(
                        "bed_box_pair",
                        bed_box_target,
                        rest,
                        rest_index=rest_index,
                    ),
                    source_dir=source_dir,
                    device=device,
                    options=options,
                ),
                "cylinder": _run_package(
                    _pair_package(
                        "bed_cylinder_pair",
                        bed_cylinder_target,
                        rest,
                        rest_index=rest_index,
                    ),
                    source_dir=source_dir,
                    device=device,
                    options=options,
                ),
            }
        )

    return build_cylinder_clean_control_report(
        single_controls=single_controls,
        pair_controls=pair_controls,
        full_package_evidence={
            "bed_native_opt_in_drop": _drop_summary(bed_case["native_opt_in_tasks"]),
            "bed_native_drop": _drop_summary(bed_case["native_tasks"]),
            "franka_native_opt_in_drop": _drop_summary(franka_case["native_opt_in_tasks"]),
        },
        prior_evidence={
            "native_body_com_clears_bed_failure": True,
            "native_inertia_only_clears_bed_failure": True,
            "mass_only_clears_bed_failure": False,
        },
        run_metadata={
            "bed_task_report": str(bed_task_report_path),
            "franka_task_report": str(franka_task_report_path),
            "source_dir": source_dir,
            "device": device,
            "frames": options.frames,
            "substeps": options.substeps,
            "iterations": options.iterations,
            "pair_rest_indices": list(pair_rest_indices),
        },
    )


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


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


def _largest_cylinder(package: CollisionPackage) -> PrimitiveSpec:
    cylinders = [primitive for primitive in package.primitives if primitive.kind == "cylinder"]
    if not cylinders:
        raise ValueError("package contains no cylinder primitives")
    return max(cylinders, key=lambda primitive: float(primitive.dimensions["radius"]))


def _single_package(package_id: str, primitive: PrimitiveSpec) -> CollisionPackage:
    return CollisionPackage(
        asset_id=package_id,
        package_id=package_id,
        primitives=(primitive,),
        claim_boundary="compact_clean_control_not_collision_quality_validation",
    )


def _pair_package(
    prefix: str,
    target: PrimitiveSpec,
    rest: PrimitiveSpec,
    *,
    rest_index: int,
) -> CollisionPackage:
    return CollisionPackage(
        asset_id=prefix,
        package_id=f"{prefix}_target_plus_{rest_index}",
        primitives=(
            target,
            replace(rest, primitive_id=f"bed_rest_{rest_index}_{rest.kind}"),
        ),
        claim_boundary="compact_clean_control_not_collision_quality_validation",
    )


def _run_package(
    package: CollisionPackage,
    *,
    source_dir: str,
    device: str,
    options: DropSettleOptions,
) -> dict[str, object]:
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture), contextlib.redirect_stderr(capture):
        report = run_newton_drop_settle(
            package,
            source_dir=source_dir,
            device=device,
            options=options,
        )
    run = report.drop_settle_runs[0]
    return {
        "status": run.status,
        "failure_labels": list(run.failure_labels),
        "final_linear_speed_mps": run.final_linear_speed_mps,
        "final_contact_count": run.final_contact_count,
        "final_support_height": run.final_support_height,
    }


def _drop_summary(tasks: dict[str, Any]) -> dict[str, object]:
    drop = tasks.get("drop_settle", {})
    runs = drop.get("drop_settle_runs", []) if isinstance(drop, dict) else []
    run = runs[0] if runs and isinstance(runs[0], dict) else {}
    return {
        "status": drop.get("status") if isinstance(drop, dict) else None,
        "failure_labels": _list_or_empty(run.get("failure_labels")),
        "final_linear_speed_mps": run.get("final_linear_speed_mps"),
        "final_contact_count": run.get("final_contact_count"),
        "final_support_height": run.get("final_support_height"),
    }


def _list_or_empty(value: object) -> list[object]:
    if isinstance(value, list | tuple) and not isinstance(value, (str, bytes)):
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

