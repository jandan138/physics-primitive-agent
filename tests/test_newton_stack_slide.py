import pytest

from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.newton.stack_slide import (
    STACK_SLIDE_CLAIM_BOUNDARY,
    StackSlideOptions,
    evaluate_stack_slide_trace,
    run_newton_stack_slide,
)


def test_stack_slide_blocks_partial_shape_mapping():
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(
            PrimitiveSpec(
                primitive_id="box",
                kind="box",
                dimensions={"half_extents": [1.0, 1.0, 1.0]},
            ),
            PrimitiveSpec(primitive_id="mesh", kind="mesh", dimensions={}),
        ),
    )

    report = run_newton_stack_slide(package, source_dir="/missing/newton", device="cpu")

    assert report.stage == "newton_stack_slide"
    assert report.probe_type == "stack_or_slide"
    assert report.status == "mapping_gap"
    assert report.claim_boundary == STACK_SLIDE_CLAIM_BOUNDARY
    assert report.metrics["full_package_shape_coverage"] is False
    assert report.stack_slide_runs == ()


def test_stack_slide_reports_dependency_gap_after_full_mapping_passes(tmp_path):
    source_dir = tmp_path / "newton-source"
    source_dir.mkdir()
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(
            PrimitiveSpec(
                primitive_id="box",
                kind="box",
                dimensions={"half_extents": [1.0, 1.0, 0.1]},
            ),
        ),
    )

    report = run_newton_stack_slide(package, source_dir=str(source_dir), device="cpu")

    assert report.status in {"dependency_gap", "runtime_failure", "smoke_passed"}
    assert report.stage == "newton_stack_slide"
    assert report.probe_type == "stack_or_slide"
    assert report.metrics["full_package_shape_coverage"] is True
    assert report.solver["solver"] == "xpbd"


def test_stack_slide_options_reject_invalid_values():
    for kwargs in (
        {"probe_half_extents_m": (0.0, 0.05, 0.05)},
        {"lateral_velocity_mps": -0.01},
        {"frames": 0},
        {"substeps": True},
        {"frame_dt_seconds": 0.0},
        {"max_slide_distance_m": -0.1},
    ):
        with pytest.raises(ValueError, match=next(iter(kwargs))):
            StackSlideOptions(**kwargs)


def test_evaluate_stack_slide_trace_passes_for_contact_with_limited_slide():
    run = evaluate_stack_slide_trace(
        primitive_ids=("support",),
        completed_steps=16,
        initial_probe_position=(0.0, 0.0, 0.2),
        final_probe_position=(0.02, 0.0, 0.14),
        min_probe_height=0.12,
        support_top_height=0.10,
        final_linear_velocity=(0.01, 0.0, 0.0),
        max_contact_count=3,
        final_contact_count=1,
        finite_state=True,
        max_slide_distance_m=0.10,
        max_drop_below_support_m=0.05,
    )

    assert run.status == "smoke_passed"
    assert run.contact_observed is True
    assert run.horizontal_displacement_m == pytest.approx(0.02)
    assert run.failure_labels == ()


def test_evaluate_stack_slide_trace_labels_missing_contact_and_excess_slide():
    run = evaluate_stack_slide_trace(
        primitive_ids=("support",),
        completed_steps=16,
        initial_probe_position=(0.0, 0.0, 0.2),
        final_probe_position=(0.20, 0.0, 0.01),
        min_probe_height=0.0,
        support_top_height=0.10,
        final_linear_velocity=(0.50, 0.0, 0.0),
        max_contact_count=0,
        final_contact_count=0,
        finite_state=True,
        max_slide_distance_m=0.10,
        max_drop_below_support_m=0.05,
        max_settle_linear_speed_mps=0.05,
    )

    assert run.status == "runtime_failure"
    assert "no_contact_observed" in run.failure_labels
    assert "excess_horizontal_slide" in run.failure_labels
    assert "probe_below_support" in run.failure_labels
    assert "not_settled" in run.failure_labels
