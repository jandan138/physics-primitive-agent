import numpy as np

from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.newton.drop_settle import (
    DROP_SETTLE_CLAIM_BOUNDARY,
    DropSettleOptions,
    _add_dynamic_shape,
    _support_extent_z,
    _world_half_extents,
    evaluate_drop_settle_trace,
    run_newton_drop_settle,
)
from primitive_collision_compiler.reports.schema import NewtonShapeMapping


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
        {"frames": 1.5},
        {"substeps": 0},
        {"substeps": True},
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


def test_evaluate_drop_settle_trace_requires_final_contact():
    run = evaluate_drop_settle_trace(
        primitive_ids=("box",),
        completed_steps=16,
        initial_height=0.25,
        final_height=0.02,
        min_height=0.01,
        final_linear_velocity=(0.0, 0.0, 0.0),
        max_contact_count=2,
        final_contact_count=0,
        finite_state=True,
    )

    assert run.status == "runtime_failure"
    assert "no_final_contact" in run.failure_labels


def test_evaluate_drop_settle_trace_reports_unsettled_final_speed():
    run = evaluate_drop_settle_trace(
        primitive_ids=("box",),
        completed_steps=16,
        initial_height=0.25,
        final_height=0.02,
        min_height=0.01,
        final_linear_velocity=(0.5, 0.0, 0.0),
        max_contact_count=2,
        final_contact_count=1,
        finite_state=True,
        max_settle_linear_speed_mps=0.05,
    )

    assert run.status == "runtime_failure"
    assert "not_settled" in run.failure_labels


def test_evaluate_drop_settle_trace_reports_floor_breach_from_support_height():
    run = evaluate_drop_settle_trace(
        primitive_ids=("box",),
        completed_steps=16,
        initial_height=0.25,
        final_height=0.02,
        min_height=0.01,
        final_linear_velocity=(0.0, 0.0, 0.0),
        max_contact_count=2,
        final_contact_count=1,
        finite_state=True,
        final_support_height=-0.02,
        min_support_height=-0.20,
        min_allowed_support_height=-0.05,
    )

    assert run.status == "runtime_failure"
    assert run.contact_observed is True
    assert "floor_breach" in run.failure_labels
    assert run.final_support_height == -0.02
    assert run.min_support_height == -0.20


def test_drop_settle_builds_newton_native_dynamic_shapes():
    builder = _RecordingBuilder()
    wp = _FakeWarp()
    anchor = (1.0, 2.0, 3.0)
    mappings = (
        _mapping(
            "cylinder0",
            "cylinder",
            {"radius": 0.3, "half_height": 0.8, "axis_index": 1},
            center=(1.0, 2.0, 4.0),
        ),
        _mapping(
            "cone0",
            "cone",
            {"radius": 0.4, "half_height": 0.9, "axis_index": 0},
            center=(2.0, 2.0, 3.0),
        ),
        _mapping(
            "ellipsoid0",
            "ellipsoid",
            {"radii": [0.2, 0.4, 0.6]},
            center=(1.0, 3.0, 3.0),
        ),
    )

    for mapping in mappings:
        _add_dynamic_shape(builder, mapping, wp, body=7, anchor=anchor)

    assert [call[0] for call in builder.calls] == ["cylinder", "cone", "ellipsoid"]
    assert builder.calls[0][1]["body"] == 7
    assert builder.calls[0][1]["half_height"] == 0.8
    assert builder.calls[1][1]["radius"] == 0.4
    assert builder.calls[2][1]["rz"] == 0.6


def test_drop_settle_native_world_extents_and_support_height_are_conservative():
    cylinder = _mapping(
        "cylinder0",
        "cylinder",
        {"radius": 0.3, "half_height": 0.8, "axis_index": 2},
    )
    cone = _mapping("cone0", "cone", {"radius": 0.4, "half_height": 0.9, "axis_index": 2})
    ellipsoid = _mapping("ellipsoid0", "ellipsoid", {"radii": [0.2, 0.4, 0.6]})
    world_axes = np.eye(3, dtype=float)

    np.testing.assert_allclose(_world_half_extents(cylinder), [0.3, 0.3, 0.8])
    np.testing.assert_allclose(_world_half_extents(cone), [0.4, 0.4, 0.9])
    np.testing.assert_allclose(_world_half_extents(ellipsoid), [0.2, 0.4, 0.6])
    assert _support_extent_z(cylinder, world_axes) == 0.8
    assert _support_extent_z(cone, world_axes) == 0.9
    assert _support_extent_z(ellipsoid, world_axes) == 0.6


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

    def add_shape_cone(self, *, body, xform, radius, half_height):
        self.calls.append(
            ("cone", {"body": body, "xform": xform, "radius": radius, "half_height": half_height})
        )

    def add_shape_ellipsoid(self, *, body, xform, rx, ry, rz):
        self.calls.append(("ellipsoid", {"body": body, "xform": xform, "rx": rx, "ry": ry, "rz": rz}))


class _FakeWarp:
    def vec3(self, x: float, y: float, z: float) -> tuple[float, float, float]:
        return (x, y, z)

    def matrix_from_cols(self, *cols):
        return cols

    def quat_from_matrix(self, matrix):
        return ("quat", matrix)

    def transform(self, position, rotation):
        return {"position": position, "rotation": rotation}
