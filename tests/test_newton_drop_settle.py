from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.newton.drop_settle import (
    DROP_SETTLE_CLAIM_BOUNDARY,
    DropSettleOptions,
    evaluate_drop_settle_trace,
    run_newton_drop_settle,
)


def test_drop_settle_blocks_partial_shape_mapping():
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

    report = run_newton_drop_settle(package, source_dir="/missing/newton", device="cpu")

    assert report.stage == "newton_drop_settle"
    assert report.probe_type == "drop_settle"
    assert report.status == "mapping_gap"
    assert report.claim_boundary == DROP_SETTLE_CLAIM_BOUNDARY
    assert report.metrics["full_package_shape_coverage"] is False
    assert report.drop_settle_runs == ()


def test_drop_settle_reports_dependency_gap_after_full_mapping_passes(tmp_path):
    source_dir = tmp_path / "newton-source"
    source_dir.mkdir()
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(
            PrimitiveSpec(
                primitive_id="sphere",
                kind="sphere",
                dimensions={"radius": 0.25},
            ),
        ),
    )

    report = run_newton_drop_settle(package, source_dir=str(source_dir), device="cpu")

    assert report.status in {"dependency_gap", "runtime_failure", "smoke_passed"}
    assert report.stage == "newton_drop_settle"
    assert report.probe_type == "drop_settle"
    assert report.metrics["full_package_shape_coverage"] is True
    assert report.solver["solver"] == "xpbd"


def test_drop_settle_options_reject_non_positive_values():
    for kwargs in (
        {"frames": 0},
        {"substeps": 0},
        {"frame_dt_seconds": 0.0},
        {"height_m": -0.1},
        {"iterations": 0},
    ):
        try:
            DropSettleOptions(**kwargs)
        except ValueError as exc:
            assert next(iter(kwargs)) in str(exc)
        else:
            raise AssertionError(f"{kwargs} should be rejected")


def test_evaluate_drop_settle_trace_reports_missing_contact():
    run = evaluate_drop_settle_trace(
        primitive_ids=("box",),
        completed_steps=16,
        initial_height=0.25,
        final_height=0.20,
        min_height=0.20,
        final_linear_velocity=(0.0, 0.0, -0.1),
        max_contact_count=0,
        final_contact_count=0,
        finite_state=True,
    )

    assert run.status == "runtime_failure"
    assert run.descended is True
    assert run.contact_observed is False
    assert "no_contact_observed" in run.failure_labels


def test_evaluate_drop_settle_trace_reports_smoke_passed_for_descent_and_contact():
    run = evaluate_drop_settle_trace(
        primitive_ids=("box", "sphere"),
        completed_steps=16,
        initial_height=0.25,
        final_height=0.02,
        min_height=0.01,
        final_linear_velocity=(0.0, 0.0, 0.0),
        max_contact_count=2,
        final_contact_count=1,
        finite_state=True,
    )

    assert run.status == "smoke_passed"
    assert run.descended is True
    assert run.contact_observed is True
    assert run.failure_labels == ()
