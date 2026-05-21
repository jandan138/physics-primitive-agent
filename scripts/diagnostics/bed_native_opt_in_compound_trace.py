#!/usr/bin/env python
from __future__ import annotations

import argparse
import contextlib
from dataclasses import replace
import json
import math
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import numpy as np

from primitive_collision_compiler.baselines.cpd_like.real_usd_comparison import (
    build_real_usd_native_artifacts,
)
from primitive_collision_compiler.cli import (
    _expand_env_path,
    _newton_drop_settle_options,
    _real_usd_native_comparison_options,
)
from primitive_collision_compiler.config import load_compile_config
from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.newton.diagnostics import _import_newton_runtime
from primitive_collision_compiler.newton.drop_settle import (
    DropSettleOptions,
    _add_dynamic_shape,
    _estimated_support_height,
    _package_anchor,
    evaluate_drop_settle_trace,
)
from primitive_collision_compiler.newton.shapes import map_package_shapes
from primitive_collision_compiler.reports.schema import NewtonShapeMapping


DEFAULT_CONFIG = Path("configs/experiments/bed_native_opt_in_probe.yaml")
DEFAULT_TARGET_INDEX = 6
DEFAULT_SOURCE_DIR_ENV = "$NEWTON_SOURCE_DIR"
CLAIM_BOUNDARY = (
    "bed_native_opt_in_compound_trace_diagnostic_not_collision_quality_or_root_cause_proof"
)
_INERTIAL_FIELDS = (
    "body_mass",
    "body_inv_mass",
    "body_com",
    "body_inertia",
    "body_inv_inertia",
)
_INERTIAL_COMPONENT_VARIANTS = {
    "native_opt_in_cylinder_with_native_box_mass": ("body_mass", "body_inv_mass"),
    "native_opt_in_cylinder_with_native_box_inertia_tensor": (
        "body_inertia",
        "body_inv_inertia",
    ),
    "native_opt_in_cylinder_with_native_box_mass_inertia": (
        "body_mass",
        "body_inv_mass",
        "body_inertia",
        "body_inv_inertia",
    ),
}


def _fraction_token(fraction: float) -> str:
    return f"{fraction:.6f}".rstrip("0").rstrip(".").replace(".", "")


_COM_AXIS_VARIANTS = {
    "native_opt_in_cylinder_with_native_box_com_x": (0,),
    "native_opt_in_cylinder_with_native_box_com_y": (1,),
    "native_opt_in_cylinder_with_native_box_com_z": (2,),
    "native_opt_in_cylinder_with_native_box_com_xy": (0, 1),
    "native_opt_in_cylinder_with_native_box_com_xz": (0, 2),
    "native_opt_in_cylinder_with_native_box_com_yz": (1, 2),
}
_COM_BLEND_FRACTIONS = (0.0, 0.25, 0.5, 0.75, 1.0)
_COM_BLEND_VARIANTS = {
    f"native_opt_in_cylinder_with_native_box_com_blend_{int(fraction * 100):03d}": {
        "axes": (0, 1, 2),
        "fraction": fraction,
    }
    for fraction in _COM_BLEND_FRACTIONS
} | {
    f"native_opt_in_cylinder_with_native_box_com_xz_blend_{int(fraction * 100):03d}": {
        "axes": (0, 2),
        "fraction": fraction,
    }
    for fraction in _COM_BLEND_FRACTIONS
}
_COM_BLEND_REFINEMENT_FRACTIONS = (0.75, 0.875, 0.9375, 0.96875, 0.984375, 1.0)
_COM_BLEND_REFINEMENT_VARIANTS = {
    f"native_opt_in_cylinder_with_native_box_com_refine_{_fraction_token(fraction)}": {
        "axes": (0, 1, 2),
        "fraction": fraction,
    }
    for fraction in _COM_BLEND_REFINEMENT_FRACTIONS
} | {
    f"native_opt_in_cylinder_with_native_box_com_xz_refine_{_fraction_token(fraction)}": {
        "axes": (0, 2),
        "fraction": fraction,
    }
    for fraction in _COM_BLEND_REFINEMENT_FRACTIONS
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run the capped-bed full-compound Newton body/contact trace for the fixed "
            "primitive-6 native-vs-opt-in variants."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="bed opt-in config")
    parser.add_argument("--source-dir", default=DEFAULT_SOURCE_DIR_ENV)
    parser.add_argument("--device", default=None)
    parser.add_argument("--target-index", type=int, default=DEFAULT_TARGET_INDEX)
    parser.add_argument("--sample-every-steps", type=int, default=240)
    parser.add_argument("--tail-steps", type=int, default=480)
    parser.add_argument("--max-contact-details", type=int, default=16)
    parser.add_argument(
        "--run-inertia-counterfactual",
        action="store_true",
        help="also run the opt-in cylinder geometry with native all-box inertial arrays",
    )
    parser.add_argument(
        "--run-inertia-field-ablation",
        action="store_true",
        help="also run the opt-in cylinder geometry with only native all-box COM applied",
    )
    parser.add_argument(
        "--run-com-axis-ablation",
        action="store_true",
        help=(
            "also run opt-in cylinder geometry with fixed single-axis and pairwise "
            "native all-box COM subsets applied"
        ),
    )
    parser.add_argument(
        "--run-com-blend-ablation",
        action="store_true",
        help=(
            "also run opt-in cylinder geometry with fixed fractional native all-box COM "
            "blends applied to xyz and xz axes"
        ),
    )
    parser.add_argument(
        "--run-com-blend-refinement",
        action="store_true",
        help=(
            "also run opt-in cylinder geometry with fixed near-endpoint native all-box COM "
            "blends applied to xyz and xz axes"
        ),
    )
    parser.add_argument(
        "--run-inertial-component-ablation",
        action="store_true",
        help=(
            "also run opt-in cylinder geometry with native all-box mass-only, "
            "inertia-only, and mass+inertia fields while retaining opt-in COM"
        ),
    )
    parser.add_argument(
        "--run-model-build-audit",
        action="store_true",
        help="also record full/target/rest Newton model mass, COM, and inertia before solver creation",
    )
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        source_dir = _expand_env_path(str(args.source_dir), "source_dir")
        with contextlib.redirect_stdout(sys.stderr):
            report = build_compound_trace_report(
                config_path=args.config,
                source_dir=source_dir,
                device=args.device,
                target_index=args.target_index,
                sample_every_steps=args.sample_every_steps,
                tail_steps=args.tail_steps,
                max_contact_details=args.max_contact_details,
                run_inertia_counterfactual=args.run_inertia_counterfactual,
                run_inertia_field_ablation=args.run_inertia_field_ablation,
                run_com_axis_ablation=args.run_com_axis_ablation,
                run_com_blend_ablation=args.run_com_blend_ablation,
                run_com_blend_refinement=args.run_com_blend_refinement,
                run_inertial_component_ablation=args.run_inertial_component_ablation,
                run_model_build_audit=args.run_model_build_audit,
            )
    except Exception as exc:
        report = {
            "stage": "bed_native_opt_in_compound_trace_diagnostic",
            "status": "runtime_failure",
            "claim_boundary": CLAIM_BOUNDARY,
            "fallback_reason": f"{type(exc).__name__}: {exc}",
        }
        print(json.dumps(report, sort_keys=True, allow_nan=False))
        return 2

    report = _json_safe(report)
    encoded = json.dumps(report, sort_keys=True, allow_nan=False)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    print(encoded)
    return 0 if report["status"] == "diagnostic_recorded" else 2


def build_compound_trace_report(
    *,
    config_path: Path,
    source_dir: str,
    device: str | None,
    target_index: int,
    sample_every_steps: int,
    tail_steps: int,
    max_contact_details: int,
    run_inertia_counterfactual: bool = False,
    run_inertia_field_ablation: bool = False,
    run_com_axis_ablation: bool = False,
    run_com_blend_ablation: bool = False,
    run_com_blend_refinement: bool = False,
    run_inertial_component_ablation: bool = False,
    run_model_build_audit: bool = False,
) -> dict[str, object]:
    if sample_every_steps <= 0:
        raise ValueError("sample_every_steps must be positive")
    if tail_steps < 0:
        raise ValueError("tail_steps must be non-negative")
    if max_contact_details < 0:
        raise ValueError("max_contact_details must be non-negative")

    config = load_compile_config(config_path)
    comparison_options = _real_usd_native_comparison_options(config)
    diagnostic_section = config.protocol.get("newton_diagnostic", {})
    if not isinstance(diagnostic_section, dict):
        diagnostic_section = {}
    run_device = str(device or diagnostic_section.get("device", "cpu"))
    drop_options = _newton_drop_settle_options(
        {**diagnostic_section, "probe_type": "drop_settle"}
    )["options"]

    artifacts = build_real_usd_native_artifacts(**comparison_options)
    if len(artifacts) != 1:
        raise ValueError("bed trace expects exactly one configured asset role")
    artifact = artifacts[0]
    if artifact.native_opt_in is None:
        raise ValueError("bed trace requires native_opt_in package")
    native_package = artifact.native.package
    opt_in_package = artifact.native_opt_in.package
    variants = _build_variants(
        native_package=native_package,
        opt_in_package=opt_in_package,
        target_index=target_index,
    )

    runtime = _import_newton_runtime(source_dir)
    model_build_audit = None
    if run_model_build_audit:
        model_build_audit = _build_model_build_audit(
            native_package=native_package,
            opt_in_package=opt_in_package,
            target_index=target_index,
            runtime=runtime,
            device=run_device,
        )
    inertial_override = None
    if (
        run_inertia_counterfactual
        or run_inertia_field_ablation
        or run_com_axis_ablation
        or run_com_blend_ablation
        or run_com_blend_refinement
        or run_inertial_component_ablation
    ):
        inertial_override = _snapshot_inertial_override(
            variants["native_control_box"],
            runtime=runtime,
            device=run_device,
            source_variant="native_control_box",
        )
    if run_inertia_counterfactual:
        variants["native_opt_in_cylinder_with_native_box_inertia"] = opt_in_package
    if run_inertia_field_ablation:
        variants["native_opt_in_cylinder_with_native_box_com"] = opt_in_package
    if run_com_axis_ablation:
        for variant_name in _COM_AXIS_VARIANTS:
            variants[variant_name] = opt_in_package
    if run_com_blend_ablation:
        for variant_name in _COM_BLEND_VARIANTS:
            variants[variant_name] = opt_in_package
    if run_com_blend_refinement:
        for variant_name in _COM_BLEND_REFINEMENT_VARIANTS:
            variants[variant_name] = opt_in_package
    if run_inertial_component_ablation:
        for variant_name in _INERTIAL_COMPONENT_VARIANTS:
            variants[variant_name] = opt_in_package

    variant_reports: dict[str, object] = {}
    for variant_name, package in variants.items():
        override_fields = None
        override_com_axes = None
        override_com_blend_fraction = None
        if variant_name == "native_opt_in_cylinder_with_native_box_inertia":
            override_fields = _INERTIAL_FIELDS
        elif variant_name == "native_opt_in_cylinder_with_native_box_com":
            override_fields = ("body_com",)
        elif variant_name in _COM_AXIS_VARIANTS:
            override_fields = ("body_com",)
            override_com_axes = _COM_AXIS_VARIANTS[variant_name]
        elif variant_name in _COM_BLEND_VARIANTS:
            override_fields = ("body_com",)
            blend_spec = _COM_BLEND_VARIANTS[variant_name]
            override_com_axes = blend_spec["axes"]
            override_com_blend_fraction = blend_spec["fraction"]
        elif variant_name in _COM_BLEND_REFINEMENT_VARIANTS:
            override_fields = ("body_com",)
            blend_spec = _COM_BLEND_REFINEMENT_VARIANTS[variant_name]
            override_com_axes = blend_spec["axes"]
            override_com_blend_fraction = blend_spec["fraction"]
        elif variant_name in _INERTIAL_COMPONENT_VARIANTS:
            override_fields = _INERTIAL_COMPONENT_VARIANTS[variant_name]
        variant_reports[variant_name] = _trace_package(
            package,
            source_dir=source_dir,
            runtime=runtime,
            device=run_device,
            options=drop_options,
            sample_every_steps=sample_every_steps,
            tail_steps=tail_steps,
            max_contact_details=max_contact_details,
            inertial_override=inertial_override if override_fields is not None else None,
            inertial_override_fields=override_fields,
            inertial_override_com_axes=override_com_axes,
            inertial_override_com_blend_fraction=override_com_blend_fraction,
        )

    return {
        "stage": "bed_native_opt_in_compound_trace_diagnostic",
        "status": "diagnostic_recorded",
        "claim_boundary": CLAIM_BOUNDARY,
        "artifact_scope": (
            "capped_bed_first_mesh_32_primitive_full_compound_fixed_primitive6_variants"
        ),
        "config": str(config_path),
        "source_dir": source_dir,
        "device": run_device,
        "target_index": target_index,
        "target_source_faces": list(native_package.primitives[target_index].source_faces),
        "drop_settle_options": drop_options.to_solver_dict()
        | drop_options.to_initial_conditions(),
        "sampling": {
            "sample_every_steps": sample_every_steps,
            "tail_steps": tail_steps,
            "max_contact_details": max_contact_details,
            "tail_window_seconds": tail_steps * drop_options.step_dt_seconds,
        },
        "counterfactuals": {
            "inertia_counterfactual_enabled": run_inertia_counterfactual,
            "inertia_counterfactual_variant": (
                "native_opt_in_cylinder_with_native_box_inertia"
                if run_inertia_counterfactual
                else None
            ),
            "inertia_override_fields": list(_INERTIAL_FIELDS)
            if run_inertia_counterfactual
            else [],
            "inertia_field_ablation_enabled": run_inertia_field_ablation,
            "inertia_field_ablation_variants": {
                "native_opt_in_cylinder_with_native_box_com": ["body_com"],
            }
            if run_inertia_field_ablation
            else {},
            "com_axis_ablation_enabled": run_com_axis_ablation,
            "com_axis_ablation_variants": {
                name: {"field": "body_com", "axes": list(axes)}
                for name, axes in _COM_AXIS_VARIANTS.items()
            }
            if run_com_axis_ablation
            else {},
            "com_blend_ablation_enabled": run_com_blend_ablation,
            "com_blend_ablation_variants": {
                name: {
                    "field": "body_com",
                    "axes": list(spec["axes"]),
                    "fraction": spec["fraction"],
                }
                for name, spec in _COM_BLEND_VARIANTS.items()
            }
            if run_com_blend_ablation
            else {},
            "com_blend_refinement_enabled": run_com_blend_refinement,
            "com_blend_refinement_variants": {
                name: {
                    "field": "body_com",
                    "axes": list(spec["axes"]),
                    "fraction": spec["fraction"],
                }
                for name, spec in _COM_BLEND_REFINEMENT_VARIANTS.items()
            }
            if run_com_blend_refinement
            else {},
            "inertial_component_ablation_enabled": run_inertial_component_ablation,
            "inertial_component_ablation_variants": {
                name: list(fields)
                for name, fields in _INERTIAL_COMPONENT_VARIANTS.items()
            }
            if run_inertial_component_ablation
            else {},
            "model_build_audit_enabled": run_model_build_audit,
        },
        "model_build_audit": model_build_audit,
        "variant_summary": {
            name: _variant_summary(payload) for name, payload in variant_reports.items()
        },
        "variants": variant_reports,
        "interpretation_boundary": (
            "Trace diagnostics expose Newton body, support-height, and contact-manifold "
            "differences for this recorded bed full-compound task only. The optional inertia "
            "counterfactual, inertial-component controls, COM field/blend ablations, and "
            "model-build audit are one-config sensitivity controls, not physically validated "
            "collision packages. These diagnostics do not prove general cylinder quality, "
            "benchmark behavior, root cause, or an automatic repair policy."
        ),
    }


def _build_variants(
    *,
    native_package: CollisionPackage,
    opt_in_package: CollisionPackage,
    target_index: int,
) -> dict[str, CollisionPackage]:
    if target_index < 0 or target_index >= len(native_package.primitives):
        raise ValueError("target_index out of range")
    if len(native_package.primitives) != len(opt_in_package.primitives):
        raise ValueError("native and opt-in packages must have equal primitive counts")

    native_target = native_package.primitives[target_index]
    opt_in_target = opt_in_package.primitives[target_index]
    if tuple(native_target.source_faces) != tuple(opt_in_target.source_faces):
        raise ValueError("target source_faces differ across native and opt-in packages")

    reverted = _replace_primitive(
        opt_in_package,
        target_index,
        replace(
            native_target,
            primitive_id=f"{opt_in_package.asset_id}:primitive:{target_index}:reverted_box",
        ),
        package_id=f"{opt_in_package.package_id}:primitive6_reverted_box",
    )
    box_at_cylinder_center = _replace_primitive(
        opt_in_package,
        target_index,
        replace(
            native_target,
            center=opt_in_target.center,
            primitive_id=(
                f"{opt_in_package.asset_id}:primitive:{target_index}:box_at_cylinder_center"
            ),
        ),
        package_id=f"{opt_in_package.package_id}:primitive6_box_at_cylinder_center",
    )
    cylinder_at_box_center = _replace_primitive(
        opt_in_package,
        target_index,
        replace(
            opt_in_target,
            center=native_target.center,
            primitive_id=(
                f"{opt_in_package.asset_id}:primitive:{target_index}:cylinder_at_box_center"
            ),
        ),
        package_id=f"{opt_in_package.package_id}:primitive6_cylinder_at_box_center",
    )
    return {
        "native_control_box": native_package,
        "native_opt_in_cylinder": opt_in_package,
        "native_opt_in_cylinder_reverted": reverted,
        "box_at_cylinder_center": box_at_cylinder_center,
        "cylinder_at_box_center": cylinder_at_box_center,
    }


def _replace_primitive(
    package: CollisionPackage,
    index: int,
    primitive: PrimitiveSpec,
    *,
    package_id: str,
) -> CollisionPackage:
    primitives = list(package.primitives)
    primitives[index] = primitive
    return replace(package, primitives=tuple(primitives), package_id=package_id)


def _snapshot_inertial_override(
    package: CollisionPackage,
    *,
    runtime: Any,
    device: str,
    source_variant: str,
) -> dict[str, object]:
    if runtime.status != "smoke_passed":
        raise ValueError(f"cannot snapshot inertial override from runtime status {runtime.status}")
    mappings = map_package_shapes(package)
    if len(tuple(mapping for mapping in mappings if mapping.status == "mapped")) != len(
        package.primitives
    ):
        raise ValueError("inertial override source package must be fully mapped")
    anchor, bounds = _package_anchor(mappings)
    newton = runtime.newton
    wp = runtime.warp
    with wp.ScopedDevice(device):
        builder = newton.ModelBuilder(gravity=0.0, up_axis=newton.Axis.Z)
        builder.add_ground_plane(height=0.0)
        body = builder.add_body(
            xform=wp.transform(
                wp.vec3(0.0, 0.0, 0.0),
                wp.quat_identity(),
            )
        )
        for mapping in mappings:
            _add_dynamic_shape(builder, mapping, wp, body, anchor)
        model = builder.finalize(device=device)
        return {
            "source_variant": source_variant,
            "source_package_id": package.package_id,
            "source_anchor": list(anchor),
            "source_bounds": {"min": list(bounds[0]), "max": list(bounds[1])},
            "source_model_summary": _model_summary(model),
            "arrays": {
                field: getattr(model, field).numpy().copy() for field in _INERTIAL_FIELDS
            },
        }


def _build_model_build_audit(
    *,
    native_package: CollisionPackage,
    opt_in_package: CollisionPackage,
    target_index: int,
    runtime: Any,
    device: str,
) -> dict[str, object]:
    if runtime.status != "smoke_passed":
        return {
            "status": runtime.status,
            "fallback_reason": runtime.environment.status,
            "environment": runtime.environment.to_dict(),
        }
    native_mappings = map_package_shapes(native_package)
    opt_in_mappings = map_package_shapes(opt_in_package)
    native_mapping_status_counts = _count_values(mapping.status for mapping in native_mappings)
    opt_in_mapping_status_counts = _count_values(
        mapping.status for mapping in opt_in_mappings
    )
    native_mapped_count = native_mapping_status_counts.get("mapped", 0)
    opt_in_mapped_count = opt_in_mapping_status_counts.get("mapped", 0)
    if (
        native_mapped_count != len(native_package.primitives)
        or opt_in_mapped_count != len(opt_in_package.primitives)
        or native_mapped_count == 0
        or opt_in_mapped_count == 0
    ):
        return {
            "status": "mapping_gap",
            "fallback_reason": "full_package_shape_coverage_required",
            "target_index": target_index,
            "native_mapping_status_counts": native_mapping_status_counts,
            "native_opt_in_mapping_status_counts": opt_in_mapping_status_counts,
        }
    native_mapped = _require_full_mapping(native_mappings, "native")
    opt_in_mapped = _require_full_mapping(opt_in_mappings, "native_opt_in")
    if target_index < 0 or target_index >= len(native_mapped):
        raise ValueError("target_index out of range")
    native_anchor, native_bounds = _package_anchor(native_mapped)
    opt_in_anchor, opt_in_bounds = _package_anchor(opt_in_mapped)
    target_native = (native_mapped[target_index],)
    target_opt_in = (opt_in_mapped[target_index],)
    rest_native = tuple(
        mapping for index, mapping in enumerate(native_mapped) if index != target_index
    )
    rest_opt_in = tuple(
        mapping for index, mapping in enumerate(opt_in_mapped) if index != target_index
    )

    pieces = {
        "native_full": _model_build_piece(
            native_mapped, anchor=native_anchor, runtime=runtime, device=device
        ),
        "native_target_full_anchor": _model_build_piece(
            target_native, anchor=native_anchor, runtime=runtime, device=device
        ),
        "native_rest_without_target_full_anchor": _model_build_piece(
            rest_native, anchor=native_anchor, runtime=runtime, device=device
        ),
        "native_opt_in_full": _model_build_piece(
            opt_in_mapped, anchor=opt_in_anchor, runtime=runtime, device=device
        ),
        "native_opt_in_target_full_anchor": _model_build_piece(
            target_opt_in, anchor=opt_in_anchor, runtime=runtime, device=device
        ),
        "native_opt_in_rest_without_target_full_anchor": _model_build_piece(
            rest_opt_in, anchor=opt_in_anchor, runtime=runtime, device=device
        ),
    }
    anchor_match = _anchors_match(list(native_anchor), opt_in_anchor)
    return {
        "status": "diagnostic_recorded",
        "scope": (
            "pre_solver_newton_model_build_mass_com_inertia_audit_for_full_target_and_rest"
        ),
        "target_index": target_index,
        "target_source_faces": list(native_package.primitives[target_index].source_faces),
        "native_anchor": list(native_anchor),
        "native_bounds": {"min": list(native_bounds[0]), "max": list(native_bounds[1])},
        "native_opt_in_anchor": list(opt_in_anchor),
        "native_opt_in_bounds": {
            "min": list(opt_in_bounds[0]),
            "max": list(opt_in_bounds[1]),
        },
        "anchor_match": anchor_match,
        "pieces": pieces,
        "delta_summary": _model_build_delta_summary(
            pieces,
            anchor_match=anchor_match,
            native_anchor=list(native_anchor),
            opt_in_anchor=list(opt_in_anchor),
        ),
        "interpretation_boundary": (
            "This audit records Newton model mass/COM/inertia immediately after builder "
            "finalization and before solver creation. Target/rest pieces are built under the "
            "full-package anchor to inspect model-build accounting only; they are not task "
            "smokes, standalone package validation, or a repair policy."
        ),
    }


def _require_full_mapping(
    mappings: tuple[NewtonShapeMapping, ...], lane: str
) -> tuple[NewtonShapeMapping, ...]:
    mapped = tuple(mapping for mapping in mappings if mapping.status == "mapped")
    if len(mapped) != len(mappings) or not mapped:
        raise ValueError(f"{lane} package must be fully mapped for model-build audit")
    return mapped


def _model_build_piece(
    mappings: tuple[NewtonShapeMapping, ...],
    *,
    anchor: tuple[float, float, float],
    runtime: Any,
    device: str,
) -> dict[str, object]:
    newton = runtime.newton
    wp = runtime.warp
    with wp.ScopedDevice(device):
        builder = newton.ModelBuilder(gravity=0.0, up_axis=newton.Axis.Z)
        body = builder.add_body(
            xform=wp.transform(
                wp.vec3(0.0, 0.0, 0.0),
                wp.quat_identity(),
            )
        )
        for mapping in mappings:
            _add_dynamic_shape(builder, mapping, wp, body, anchor)
        model = builder.finalize(device=device)
        return {
            "primitive_count": len(mappings),
            "primitive_ids": [mapping.primitive_id for mapping in mappings],
            "anchor": list(anchor),
            "model_summary": _model_summary(model),
        }


def _model_build_delta_summary(
    pieces: dict[str, object],
    *,
    anchor_match: bool,
    native_anchor: object,
    opt_in_anchor: object,
) -> dict[str, object]:
    if not anchor_match:
        return {
            "status": "anchor_mismatch",
            "fallback_reason": "model_build_delta_requires_matching_package_anchors",
            "native_anchor": _json_safe(native_anchor),
            "native_opt_in_anchor": _json_safe(opt_in_anchor),
        }
    pairs = {
        "full_opt_in_minus_native": ("native_opt_in_full", "native_full"),
        "target_opt_in_minus_native": (
            "native_opt_in_target_full_anchor",
            "native_target_full_anchor",
        ),
        "rest_opt_in_minus_native": (
            "native_opt_in_rest_without_target_full_anchor",
            "native_rest_without_target_full_anchor",
        ),
    }
    return {
        name: _model_piece_delta(
            pieces[left],
            pieces[right],
        )
        for name, (left, right) in pairs.items()
    }


def _model_piece_delta(left: object, right: object) -> dict[str, object]:
    if not isinstance(left, dict) or not isinstance(right, dict):
        return {"status": "malformed"}
    left_summary = left.get("model_summary")
    right_summary = right.get("model_summary")
    if not isinstance(left_summary, dict) or not isinstance(right_summary, dict):
        return {"status": "missing_model_summary"}
    return {
        "body_mass_delta": _vector_delta(
            _first_model_value(left_summary, "body_mass"),
            _first_model_value(right_summary, "body_mass"),
        ),
        "body_com_delta": _vector_delta(
            _first_model_value(left_summary, "body_com"),
            _first_model_value(right_summary, "body_com"),
        ),
        "body_inertia_row0_delta": _vector_delta(
            _first_model_value(left_summary, "body_inertia", nested=True),
            _first_model_value(right_summary, "body_inertia", nested=True),
        ),
    }


def _first_model_value(
    summary: dict[str, object], field: str, *, nested: bool = False
) -> object:
    value = summary.get(field)
    if not isinstance(value, list) or not value:
        return None
    first = value[0]
    if nested:
        if not isinstance(first, list) or not first:
            return None
        return first[0]
    return first


def _vector_delta(left: object, right: object) -> object:
    if left is None or right is None:
        return None
    left_array = np.asarray(left, dtype=float)
    right_array = np.asarray(right, dtype=float)
    return _json_safe((left_array - right_array).tolist())


def _apply_inertial_override(
    model: Any,
    *,
    inertial_override: dict[str, object],
    target_anchor: tuple[float, float, float],
    fields: tuple[str, ...],
    body_com_axes: tuple[int, ...] | None = None,
    body_com_blend_fraction: float | None = None,
) -> dict[str, object]:
    if body_com_blend_fraction is not None and body_com_axes is None:
        raise ValueError("body_com blend requires explicit axes")
    before = _model_summary(model)
    arrays = inertial_override.get("arrays")
    if not isinstance(arrays, dict):
        raise ValueError("inertial override missing arrays")
    for field in fields:
        if field not in _INERTIAL_FIELDS:
            raise ValueError(f"unsupported inertial override field: {field}")
        if field not in arrays:
            raise ValueError(f"inertial override missing {field}")
        source_array = np.asarray(arrays[field])
        if field == "body_com" and body_com_blend_fraction is not None:
            target_array = getattr(model, field).numpy().copy()
            blended_array = _body_com_blend_array(
                target_array=target_array,
                source_array=source_array,
                axes=body_com_axes or (),
                fraction=body_com_blend_fraction,
            )
            getattr(model, field).assign(blended_array)
        elif field == "body_com" and body_com_axes is not None:
            target_array = getattr(model, field).numpy().copy()
            for axis in body_com_axes:
                if axis < 0 or axis >= target_array.shape[1]:
                    raise ValueError(f"unsupported body_com axis: {axis}")
                target_array[:, axis] = source_array[:, axis]
            getattr(model, field).assign(target_array)
        else:
            getattr(model, field).assign(source_array)
    after = _model_summary(model)
    return {
        "status": "applied",
        "source_variant": inertial_override.get("source_variant"),
        "source_package_id": inertial_override.get("source_package_id"),
        "source_anchor": inertial_override.get("source_anchor"),
        "target_anchor": list(target_anchor),
        "anchor_match": _anchors_match(
            inertial_override.get("source_anchor"),
            target_anchor,
        ),
        "override_applied_before_solver_creation": True,
        "fields": list(fields),
        "body_com_axes": list(body_com_axes) if body_com_axes is not None else None,
        "body_com_blend_fraction": body_com_blend_fraction,
        "available_fields": list(_INERTIAL_FIELDS),
        "before": before,
        "after": after,
        "frame_caveat": (
            "This diagnostic directly copies Newton model inertial arrays between packages. "
            "It is interpretable here because the recorded source and target package anchors "
            "match; it is not a general inertial-repair procedure."
        ),
    }


def _body_com_blend_array(
    *,
    target_array: object,
    source_array: object,
    axes: tuple[int, ...],
    fraction: float,
) -> np.ndarray:
    if fraction < 0.0 or fraction > 1.0:
        raise ValueError("body_com blend fraction must be in [0, 1]")
    target = np.asarray(target_array, dtype=float).copy()
    source = np.asarray(source_array, dtype=float)
    if target.shape != source.shape:
        raise ValueError("body_com blend source/target shapes differ")
    if target.ndim != 2:
        raise ValueError("body_com blend expects a rank-2 array")
    for axis in axes:
        if axis < 0 or axis >= target.shape[1]:
            raise ValueError(f"unsupported body_com axis: {axis}")
        target[:, axis] = target[:, axis] + fraction * (source[:, axis] - target[:, axis])
    return target


def _anchors_match(source_anchor: object, target_anchor: tuple[float, float, float]) -> bool:
    if not isinstance(source_anchor, list | tuple) or len(source_anchor) != 3:
        return False
    source = np.asarray(source_anchor, dtype=float)
    target = np.asarray(target_anchor, dtype=float)
    return bool(np.allclose(source, target, atol=1.0e-9, rtol=0.0))


def _trace_package(
    package: CollisionPackage,
    *,
    source_dir: str,
    runtime: Any,
    device: str,
    options: DropSettleOptions,
    sample_every_steps: int,
    tail_steps: int,
    max_contact_details: int,
    inertial_override: dict[str, object] | None = None,
    inertial_override_fields: tuple[str, ...] | None = None,
    inertial_override_com_axes: tuple[int, ...] | None = None,
    inertial_override_com_blend_fraction: float | None = None,
) -> dict[str, object]:
    mappings = map_package_shapes(package)
    mapped = tuple(mapping for mapping in mappings if mapping.status == "mapped")
    if len(mapped) != len(package.primitives) or not mapped:
        return {
            "status": "mapping_gap",
            "package_id": package.package_id,
            "mapping_status_counts": _count_values(mapping.status for mapping in mappings),
            "fallback_reason": "full_package_shape_coverage_required",
        }
    if runtime.status != "smoke_passed":
        return {
            "status": runtime.status,
            "package_id": package.package_id,
            "fallback_reason": runtime.environment.status,
            "environment": runtime.environment.to_dict(),
        }
    trace = _run_drop_trace(
        mapped,
        newton=runtime.newton,
        wp=runtime.warp,
        device=device,
        options=options,
        sample_every_steps=sample_every_steps,
        tail_steps=tail_steps,
        max_contact_details=max_contact_details,
        inertial_override=inertial_override,
        inertial_override_fields=inertial_override_fields,
        inertial_override_com_axes=inertial_override_com_axes,
        inertial_override_com_blend_fraction=inertial_override_com_blend_fraction,
    )
    return {
        "status": trace["drop_settle_run"]["status"],
        "package_id": package.package_id,
        "asset_id": package.asset_id,
        "primitive_count": len(package.primitives),
        "type_counts": _count_values(primitive.kind for primitive in package.primitives),
        "mapping_status_counts": _count_values(mapping.status for mapping in mappings),
        "environment": runtime.environment.to_dict(),
        **trace,
    }


def _run_drop_trace(
    mappings: tuple[NewtonShapeMapping, ...],
    *,
    newton: ModuleType,
    wp: ModuleType,
    device: str,
    options: DropSettleOptions,
    sample_every_steps: int,
    tail_steps: int,
    max_contact_details: int,
    inertial_override: dict[str, object] | None = None,
    inertial_override_fields: tuple[str, ...] | None = None,
    inertial_override_com_axes: tuple[int, ...] | None = None,
    inertial_override_com_blend_fraction: float | None = None,
) -> dict[str, object]:
    anchor, bounds = _package_anchor(mappings)
    primitive_ids = tuple(mapping.primitive_id for mapping in mappings)
    sample_steps = _sample_steps(options.total_steps, sample_every_steps, tail_steps)
    samples: list[dict[str, object]] = []

    with wp.ScopedDevice(device):
        builder = newton.ModelBuilder(gravity=options.gravity_mps2, up_axis=newton.Axis.Z)
        builder.default_shape_cfg.mu = options.friction
        builder.add_ground_plane(height=options.ground_height_m)
        body = builder.add_body(
            xform=wp.transform(
                wp.vec3(0.0, 0.0, options.ground_height_m + options.height_m),
                wp.quat_identity(),
            )
        )
        for mapping in mappings:
            _add_dynamic_shape(builder, mapping, wp, body, anchor)
        model = builder.finalize(device=device)
        override_report = None
        if inertial_override is not None:
            override_report = _apply_inertial_override(
                model,
                inertial_override=inertial_override,
                target_anchor=anchor,
                fields=inertial_override_fields or _INERTIAL_FIELDS,
                body_com_axes=inertial_override_com_axes,
                body_com_blend_fraction=inertial_override_com_blend_fraction,
            )
        solver = newton.solvers.SolverXPBD(model, iterations=options.iterations)
        state_0 = model.state()
        state_1 = model.state()
        control = model.control()
        contacts = model.contacts()

        shape_lookup = _shape_lookup(model, mappings)
        initial_body_q = state_0.body_q.numpy()[body].copy()
        initial_height = float(initial_body_q[2])
        initial_support_height = _estimated_support_height(mappings, anchor, initial_body_q)
        final_height = initial_height
        min_height = initial_height
        final_support_height = initial_support_height
        min_support_height = initial_support_height
        final_linear_velocity = (0.0, 0.0, 0.0)
        max_contact_count = 0
        completed_steps = 0
        finite_state = True

        model.collide(state_0, contacts)
        if 0 in sample_steps:
            samples.append(
                _sample_state(
                    step=0,
                    body=body,
                    state=state_0,
                    contacts=contacts,
                    mappings=mappings,
                    anchor=anchor,
                    shape_lookup=shape_lookup,
                    max_contact_details=max_contact_details,
                    phase="initial",
                )
            )

        for _ in range(options.frames):
            for _ in range(options.substeps):
                state_0.clear_forces()
                model.collide(state_0, contacts)
                max_contact_count = max(
                    max_contact_count,
                    int(contacts.rigid_contact_count.numpy()[0]),
                )
                solver.step(state_0, state_1, control, contacts, options.step_dt_seconds)
                state_0, state_1 = state_1, state_0
                completed_steps += 1
                body_q = state_0.body_q.numpy()
                body_qd = state_0.body_qd.numpy()
                final_height = float(body_q[body, 2])
                min_height = min(min_height, final_height)
                final_support_height = _estimated_support_height(mappings, anchor, body_q[body])
                min_support_height = min(min_support_height, final_support_height)
                final_linear_velocity = tuple(float(value) for value in body_qd[body, :3])
                if completed_steps in sample_steps:
                    model.collide(state_0, contacts)
                    samples.append(
                        _sample_state(
                            step=completed_steps,
                            body=body,
                            state=state_0,
                            contacts=contacts,
                            mappings=mappings,
                            anchor=anchor,
                            shape_lookup=shape_lookup,
                            max_contact_details=max_contact_details,
                            phase="post_step",
                        )
                    )
                if not np.all(np.isfinite(body_q)) or not np.all(np.isfinite(body_qd)):
                    finite_state = False
                    break
            if not finite_state:
                break

        model.collide(state_0, contacts)
        final_contact_count = int(contacts.rigid_contact_count.numpy()[0])
        max_contact_count = max(max_contact_count, final_contact_count)
        if completed_steps not in sample_steps:
            samples.append(
                _sample_state(
                    step=completed_steps,
                    body=body,
                    state=state_0,
                    contacts=contacts,
                    mappings=mappings,
                    anchor=anchor,
                    shape_lookup=shape_lookup,
                    max_contact_details=max_contact_details,
                    phase="final",
                )
            )

        drop_run = evaluate_drop_settle_trace(
            primitive_ids=primitive_ids,
            completed_steps=completed_steps,
            initial_height=initial_height,
            final_height=final_height,
            min_height=min_height,
            final_linear_velocity=final_linear_velocity,
            max_contact_count=max_contact_count,
            final_contact_count=final_contact_count,
            finite_state=finite_state,
            min_descent_m=options.min_descent_m,
            final_support_height=final_support_height,
            min_support_height=min_support_height,
            min_allowed_support_height=options.ground_height_m - options.max_floor_breach_m,
            max_settle_linear_speed_mps=options.max_settle_linear_speed_mps,
        )

        model_summary = _model_summary(model)

    return {
        "package_anchor": list(anchor),
        "package_bounds": {
            "min": list(bounds[0]),
            "max": list(bounds[1]),
        },
        "shape_lookup": shape_lookup,
        "model_summary": model_summary,
        "inertial_override": override_report,
        "drop_settle_run": drop_run.to_dict(),
        "tail_linear_speed_summary": _tail_linear_speed_summary(
            samples,
            tail_start_step=max(0, options.total_steps - tail_steps),
            step_dt_seconds=options.step_dt_seconds,
            max_settle_linear_speed_mps=options.max_settle_linear_speed_mps,
        ),
        "trace_samples": samples,
    }


def _sample_steps(total_steps: int, sample_every_steps: int, tail_steps: int) -> set[int]:
    steps = set(range(0, total_steps + 1, sample_every_steps))
    tail_start = max(0, total_steps - tail_steps)
    steps.update(range(tail_start, total_steps + 1))
    steps.add(total_steps)
    return steps


def _sample_state(
    *,
    step: int,
    body: int,
    state: Any,
    contacts: Any,
    mappings: tuple[NewtonShapeMapping, ...],
    anchor: tuple[float, float, float],
    shape_lookup: dict[str, object],
    max_contact_details: int,
    phase: str,
) -> dict[str, object]:
    body_q = state.body_q.numpy()[body]
    body_qd = state.body_qd.numpy()[body]
    contact_count = int(contacts.rigid_contact_count.numpy()[0])
    support_height = _estimated_support_height(mappings, anchor, body_q)
    qd_values = [float(value) for value in body_qd.tolist()]
    return {
        "step": step,
        "phase": phase,
        "body_position": _float_list(body_q[:3]),
        "body_rotation_xyzw": _float_list(body_q[3:7]),
        "body_qd_raw": _float_list(body_qd),
        "linear_velocity_mps": qd_values[:3],
        "angular_velocity_raw": qd_values[3:],
        "linear_speed_mps": float(np.linalg.norm(np.asarray(qd_values[:3], dtype=float))),
        "support_height": float(support_height),
        "contact_count": contact_count,
        "contact_details": _contact_details(contacts, contact_count, shape_lookup, max_contact_details),
    }


def _contact_details(
    contacts: Any,
    contact_count: int,
    shape_lookup: dict[str, object],
    max_contact_details: int,
) -> list[dict[str, object]]:
    if max_contact_details == 0 or contact_count == 0:
        return []
    count = min(contact_count, max_contact_details)
    shape0 = contacts.rigid_contact_shape0.numpy()
    shape1 = contacts.rigid_contact_shape1.numpy()
    normal = contacts.rigid_contact_normal.numpy()
    force = contacts.rigid_contact_force.numpy()
    point0 = contacts.rigid_contact_point0.numpy()
    point1 = contacts.rigid_contact_point1.numpy()
    offset0 = contacts.rigid_contact_offset0.numpy()
    offset1 = contacts.rigid_contact_offset1.numpy()
    details = []
    for index in range(count):
        s0 = int(shape0[index])
        s1 = int(shape1[index])
        details.append(
            {
                "index": index,
                "shape0": s0,
                "shape1": s1,
                "shape0_label": _shape_label(shape_lookup, s0),
                "shape1_label": _shape_label(shape_lookup, s1),
                "normal": _float_list(normal[index]),
                "force": _float_list(force[index]),
                "force_norm": float(np.linalg.norm(force[index])),
                "point0": _float_list(point0[index]),
                "point1": _float_list(point1[index]),
                "offset0": _float_list(offset0[index]),
                "offset1": _float_list(offset1[index]),
            }
        )
    return details


def _shape_lookup(model: Any, mappings: tuple[NewtonShapeMapping, ...]) -> dict[str, object]:
    labels: dict[str, object] = {"-1": "none", "0": "ground_plane"}
    primitive_by_shape: dict[str, str] = {}
    for offset, mapping in enumerate(mappings, start=1):
        labels[str(offset)] = mapping.primitive_id
        primitive_by_shape[str(offset)] = mapping.primitive_id
    model_labels = getattr(model, "shape_label", None)
    return {
        "labels": labels,
        "primitive_by_shape": primitive_by_shape,
        "model_shape_label": list(model_labels) if isinstance(model_labels, list) else None,
    }


def _shape_label(shape_lookup: dict[str, object], shape_index: int) -> object:
    labels = shape_lookup.get("labels")
    if isinstance(labels, dict):
        return labels.get(str(shape_index), "unknown")
    return "unknown"


def _model_summary(model: Any) -> dict[str, object]:
    return {
        "body_count": int(getattr(model, "body_count")),
        "shape_count": int(getattr(model, "shape_count")),
        "body_mass": _array_sample(getattr(model, "body_mass"), limit=4),
        "body_inv_mass": _array_sample(getattr(model, "body_inv_mass"), limit=4),
        "body_com": _array_sample(getattr(model, "body_com"), limit=4),
        "body_inertia": _array_sample(getattr(model, "body_inertia"), limit=4),
        "body_inv_inertia": _array_sample(getattr(model, "body_inv_inertia"), limit=4),
        "shape_body": _array_sample(getattr(model, "shape_body"), limit=40),
        "shape_scale": _array_sample(getattr(model, "shape_scale"), limit=40),
        "shape_material_mu": _array_sample(getattr(model, "shape_material_mu"), limit=40),
    }


def _array_sample(value: Any, *, limit: int) -> object:
    if not hasattr(value, "numpy"):
        return "unavailable"
    array = value.numpy()
    if array.ndim == 0:
        return _json_safe_scalar(array.item())
    return _json_safe(array[: min(len(array), limit)].tolist())


def _variant_summary(payload: object) -> dict[str, object]:
    if not isinstance(payload, dict):
        return {"status": "malformed"}
    run = payload.get("drop_settle_run")
    if not isinstance(run, dict):
        return {
            "status": payload.get("status"),
            "fallback_reason": payload.get("fallback_reason"),
        }
    return {
        "status": payload.get("status"),
        "failure_labels": run.get("failure_labels", []),
        "final_linear_speed_mps": run.get("final_linear_speed_mps"),
        "final_contact_count": run.get("final_contact_count"),
        "final_support_height": run.get("final_support_height"),
        "max_contact_count": run.get("max_contact_count"),
        "tail_linear_speed_summary": payload.get("tail_linear_speed_summary"),
        "type_counts": payload.get("type_counts"),
        "body_mass": (
            payload.get("model_summary", {})
            .get("body_mass", [[None]])[0]
            if isinstance(payload.get("model_summary"), dict)
            else None
        ),
        "body_com": (
            payload.get("model_summary", {})
            .get("body_com", [[None]])[0]
            if isinstance(payload.get("model_summary"), dict)
            else None
        ),
    }


def _tail_linear_speed_summary(
    samples: object,
    *,
    tail_start_step: int,
    step_dt_seconds: float,
    max_settle_linear_speed_mps: float,
) -> dict[str, object]:
    if not isinstance(samples, list):
        return {"sample_count": 0}
    tail_samples: list[tuple[int, float]] = []
    for sample in samples:
        if not isinstance(sample, dict):
            continue
        step = sample.get("step")
        speed = sample.get("linear_speed_mps")
        if not isinstance(step, int) or step < tail_start_step:
            continue
        if not isinstance(speed, int | float) or not math.isfinite(float(speed)):
            continue
        tail_samples.append((step, float(speed)))
    tail_samples.sort(key=lambda item: item[0])
    speeds = [speed for _, speed in tail_samples]
    if not speeds:
        return {
            "sample_count": 0,
            "final_below_settle_threshold_sample_count": 0,
            "final_below_settle_threshold_seconds": 0.0,
            "max_settle_linear_speed_mps": max_settle_linear_speed_mps,
        }
    speed_array = np.asarray(speeds, dtype=float)
    final_below_count = 0
    for speed in reversed(speeds):
        if speed > max_settle_linear_speed_mps:
            break
        final_below_count += 1
    return {
        "sample_count": len(speeds),
        "max_linear_speed_mps": float(np.max(speed_array)),
        "mean_linear_speed_mps": float(np.mean(speed_array)),
        "min_linear_speed_mps": float(np.min(speed_array)),
        "over_settle_threshold_count": int(
            np.count_nonzero(speed_array > max_settle_linear_speed_mps)
        ),
        "final_below_settle_threshold_sample_count": final_below_count,
        "final_below_settle_threshold_seconds": float(final_below_count * step_dt_seconds),
        "max_settle_linear_speed_mps": max_settle_linear_speed_mps,
    }


def _count_values(values: Any) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        key = str(value)
        counts[key] = counts.get(key, 0) + 1
    return counts


def _float_list(values: Any) -> list[float]:
    return [float(value) for value in values]


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return _json_safe_scalar(value)


def _json_safe_scalar(value: Any) -> Any:
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float):
        if not math.isfinite(value):
            return None
        return value
    if isinstance(value, (int, str, bool)) or value is None:
        return value
    return value


if __name__ == "__main__":
    raise SystemExit(main())
