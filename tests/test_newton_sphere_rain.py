import numpy as np

from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.newton.sphere_rain import (
    SPHERE_RAIN_CLAIM_BOUNDARY,
    SphereRainOptions,
    _add_static_shape,
    _package_contact_metrics,
    _package_bounds,
    evaluate_sphere_rain_trace,
    run_newton_sphere_rain,
)
from primitive_collision_compiler.reports.schema import NewtonShapeMapping


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
        {"sphere_count_x": 1.5},
        {"sphere_count_y": 0},
        {"sphere_radius_m": 0.0},
        {"spawn_height_m": -0.1},
        {"frames": 0},
        {"frames": True},
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


def test_sphere_rain_builds_newton_native_static_shapes():
    builder = _RecordingBuilder()
    wp = _FakeWarp()

    for mapping in (
        _mapping("cylinder0", "cylinder", {"radius": 0.3, "half_height": 0.8}),
        _mapping("cone0", "cone", {"radius": 0.4, "half_height": 0.9}),
        _mapping("ellipsoid0", "ellipsoid", {"radii": [0.2, 0.4, 0.6]}),
    ):
        _add_static_shape(builder, mapping, wp)

    assert [call[0] for call in builder.calls] == ["cylinder", "cone", "ellipsoid"]
    assert builder.calls[0][1]["body"] == -1
    assert builder.calls[1][1]["radius"] == 0.4
    assert builder.calls[2][1]["rz"] == 0.6


def test_sphere_rain_package_bounds_include_native_primitives():
    bounds_min, bounds_max = _package_bounds(
        (
            _mapping(
                "cylinder0",
                "cylinder",
                {"radius": 0.3, "half_height": 0.8},
                center=(0.0, 0.0, 0.0),
            ),
            _mapping(
                "ellipsoid0",
                "ellipsoid",
                {"radii": [0.2, 0.4, 0.6]},
                center=(1.0, 0.0, 0.0),
            ),
        )
    )

    np.testing.assert_allclose(bounds_min, [-0.3, -0.4, -0.8])
    np.testing.assert_allclose(bounds_max, [1.2, 0.4, 0.8])


def _mapping(
    primitive_id: str,
    kind: str,
    dimensions: dict[str, object],
    *,
    center: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> NewtonShapeMapping:
    return NewtonShapeMapping(
        primitive_id=primitive_id,
        kind=kind,
        status="mapped",
        detail="mapped",
        center=center,
        axes=((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
        dimensions=dimensions,
    )


class _RecordingBuilder:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, object]]] = []

    def add_shape_cylinder(self, *, body, xform, radius, half_height):
        self.calls.append(
            ("cylinder", {"body": body, "xform": xform, "radius": radius, "half_height": half_height})
        )
        return len(self.calls)

    def add_shape_cone(self, *, body, xform, radius, half_height):
        self.calls.append(
            ("cone", {"body": body, "xform": xform, "radius": radius, "half_height": half_height})
        )
        return len(self.calls)

    def add_shape_ellipsoid(self, *, body, xform, rx, ry, rz):
        self.calls.append(("ellipsoid", {"body": body, "xform": xform, "rx": rx, "ry": ry, "rz": rz}))
        return len(self.calls)


class _FakeWarp:
    def vec3(self, x: float, y: float, z: float) -> tuple[float, float, float]:
        return (x, y, z)

    def matrix_from_cols(self, *cols):
        return cols

    def quat_from_matrix(self, matrix):
        return ("quat", matrix)

    def transform(self, position, rotation):
        return {"position": position, "rotation": rotation}


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
