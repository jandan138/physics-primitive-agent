import numpy as np

from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.newton.sphere_rain import (
    SPHERE_RAIN_CLAIM_BOUNDARY,
    SphereRainOptions,
    _package_contact_metrics,
    evaluate_sphere_rain_trace,
    run_newton_sphere_rain,
)


def test_sphere_rain_blocks_partial_shape_mapping():
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

    report = run_newton_sphere_rain(package, source_dir="/missing/newton", device="cpu")

    assert report.stage == "newton_sphere_rain"
    assert report.probe_type == "sphere_rain"
    assert report.status == "mapping_gap"
    assert report.claim_boundary == SPHERE_RAIN_CLAIM_BOUNDARY
    assert report.metrics["full_package_shape_coverage"] is False
    assert report.sphere_rain_runs == ()


def test_sphere_rain_reports_dependency_gap_after_full_mapping_passes(tmp_path):
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

    report = run_newton_sphere_rain(package, source_dir=str(source_dir), device="cpu")

    assert report.status in {"dependency_gap", "runtime_failure"}
    assert report.stage == "newton_sphere_rain"
    assert report.probe_type == "sphere_rain"
    assert report.metrics["full_package_shape_coverage"] is True
    assert report.solver["solver"] == "xpbd"
    assert report.sphere_rain_runs == ()


def test_sphere_rain_options_reject_non_positive_values():
    for kwargs in (
        {"sphere_count_x": 0},
        {"sphere_count_y": 0},
        {"sphere_radius_m": 0.0},
        {"spawn_height_m": -0.1},
        {"frames": 0},
        {"substeps": 0},
        {"frame_dt_seconds": 0.0},
        {"iterations": 0},
        {"gravity_mps2": float("nan")},
        {"friction": float("inf")},
        {"min_contact_density": -0.1},
        {"min_contact_density": float("nan")},
        {"grid_spacing_m": float("inf")},
    ):
        try:
            SphereRainOptions(**kwargs)
        except ValueError as exc:
            assert next(iter(kwargs)) in str(exc)
        else:
            raise AssertionError(f"{kwargs} should be rejected")


def test_evaluate_sphere_rain_trace_reports_missing_contact():
    run = evaluate_sphere_rain_trace(
        primitive_ids=("box",),
        sphere_count=9,
        completed_steps=16,
        initial_min_height=0.50,
        final_min_height=0.20,
        min_height=0.20,
        max_contact_count=0,
        final_contact_count=0,
        finite_state=True,
        min_contact_density=0.05,
    )

    assert run.status == "runtime_failure"
    assert run.contact_observed is False
    assert run.contact_density == 0.0
    assert "no_contact_observed" in run.failure_labels


def test_evaluate_sphere_rain_trace_reports_smoke_passed_for_contact_density():
    run = evaluate_sphere_rain_trace(
        primitive_ids=("box", "sphere"),
        sphere_count=9,
        completed_steps=16,
        initial_min_height=0.50,
        final_min_height=0.20,
        min_height=0.20,
        max_contact_count=3,
        final_contact_count=0,
        max_contacted_probe_count=3,
        final_contacted_probe_count=0,
        finite_state=True,
        min_contact_density=0.20,
    )

    assert run.status == "smoke_passed"
    assert run.contact_observed is True
    assert run.final_contact_observed is False
    assert run.contact_density == 3 / 9
    assert run.failure_labels == ()


def test_evaluate_sphere_rain_trace_does_not_infer_unique_probe_count_from_raw_rows():
    run = evaluate_sphere_rain_trace(
        primitive_ids=("box",),
        sphere_count=9,
        completed_steps=16,
        initial_min_height=0.50,
        final_min_height=0.20,
        min_height=0.20,
        max_contact_count=9,
        final_contact_count=0,
        finite_state=True,
        min_contact_density=0.05,
    )

    assert run.status == "runtime_failure"
    assert run.contact_observed is True
    assert run.max_contact_count == 9
    assert run.max_contacted_probe_count == 0
    assert run.contact_density == 0.0
    assert "insufficient_contact_density" in run.failure_labels


def test_evaluate_sphere_rain_trace_uses_unique_contacted_probe_count_for_density():
    run = evaluate_sphere_rain_trace(
        primitive_ids=("box", "sphere"),
        sphere_count=9,
        completed_steps=16,
        initial_min_height=0.50,
        final_min_height=0.20,
        min_height=0.20,
        max_contact_count=3,
        final_contact_count=0,
        max_contacted_probe_count=1,
        final_contacted_probe_count=0,
        finite_state=True,
        min_contact_density=0.20,
    )

    assert run.status == "runtime_failure"
    assert run.max_contact_count == 3
    assert run.max_contacted_probe_count == 1
    assert run.contact_observed is True
    assert run.contact_density == 1 / 9
    assert "insufficient_contact_density" in run.failure_labels


def test_evaluate_sphere_rain_trace_can_require_final_contact():
    run = evaluate_sphere_rain_trace(
        primitive_ids=("box",),
        sphere_count=4,
        completed_steps=16,
        initial_min_height=0.50,
        final_min_height=0.20,
        min_height=0.20,
        max_contact_count=2,
        final_contact_count=0,
        max_contacted_probe_count=2,
        final_contacted_probe_count=0,
        finite_state=True,
        min_contact_density=0.25,
        require_final_contact=True,
    )

    assert run.status == "runtime_failure"
    assert "no_final_contact" in run.failure_labels


def test_evaluate_sphere_rain_trace_reports_insufficient_contact_density():
    run = evaluate_sphere_rain_trace(
        primitive_ids=("box",),
        sphere_count=16,
        completed_steps=16,
        initial_min_height=0.50,
        final_min_height=0.20,
        min_height=0.20,
        max_contact_count=1,
        final_contact_count=1,
        max_contacted_probe_count=1,
        final_contacted_probe_count=1,
        finite_state=True,
        min_contact_density=0.25,
    )

    assert run.status == "runtime_failure"
    assert "insufficient_contact_density" in run.failure_labels


def test_package_contact_metrics_counts_raw_rows_and_unique_probe_shapes():
    contacts = _FakeContacts(
        shape0=(1, 1, 10, 1, 10, 99, 1),
        shape1=(10, 10, 2, 2, 11, 10, 99),
    )

    raw_count, unique_probe_count = _package_contact_metrics(
        contacts,
        package_shapes={1, 2},
        probe_shapes={10, 11},
    )

    assert raw_count == 3
    assert unique_probe_count == 1


class _FakeContacts:
    rigid_contact_max = 16

    def __init__(self, *, shape0: tuple[int, ...], shape1: tuple[int, ...]) -> None:
        self.rigid_contact_count = _FakeArray((len(shape0),))
        self.rigid_contact_shape0 = _FakeArray(shape0)
        self.rigid_contact_shape1 = _FakeArray(shape1)


class _FakeArray:
    def __init__(self, values: tuple[int, ...]) -> None:
        self._values = np.asarray(values, dtype=np.int32)

    def numpy(self):
        return self._values
