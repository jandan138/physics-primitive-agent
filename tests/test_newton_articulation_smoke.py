from primitive_collision_compiler.newton.articulation_smoke import (
    ARTICULATION_SMOKE_CLAIM_BOUNDARY,
    GENERATED_PACKAGE_ROBOT_TASK_CLAIM_BOUNDARY,
    ArticulationSmokeOptions,
    _attach_generated_package_shapes,
    evaluate_articulation_smoke,
    evaluate_generated_package_robot_task_probe,
    run_newton_articulation_smoke,
    run_newton_generated_package_robot_task_probe,
)


def test_articulation_smoke_reports_dependency_gap_without_newton_source(tmp_path):
    asset_path = tmp_path / "robot.usda"
    asset_path.write_text("#usda 1.0\n", encoding="utf-8")

    report = run_newton_articulation_smoke(
        asset_path=str(asset_path),
        source_dir="",
        device="cpu",
    )

    assert report["stage"] == "newton_articulation_smoke"
    assert report["probe_type"] == "articulation_smoke_if_robot"
    assert report["status"] == "dependency_gap"
    assert report["outcome"] == "dependency_gap"
    assert report["claim_boundary"] == ARTICULATION_SMOKE_CLAIM_BOUNDARY


def test_generated_package_robot_task_reports_dependency_gap_without_newton_source(tmp_path):
    asset_path = tmp_path / "robot.usda"
    asset_path.write_text("#usda 1.0\n", encoding="utf-8")

    report = run_newton_generated_package_robot_task_probe(
        asset_path=str(asset_path),
        collision_package={
            "package_id": "robot:phase0_link_aware_bbox",
            "primitives": [
                {
                    "primitive_id": "link0-box",
                    "kind": "box",
                    "frame": "/Robot/link0",
                    "source_links": ["/Robot/link0"],
                    "center": [0.0, 0.0, 0.0],
                    "dimensions": {"half_extents": [0.1, 0.1, 0.1]},
                }
            ],
        },
        source_dir="",
        device="cpu",
    )

    assert report["stage"] == "newton_generated_package_robot_task_probe"
    assert report["probe_type"] == "generated_package_robot_task_if_robot"
    assert report["status"] == "dependency_gap"
    assert report["outcome"] == "dependency_gap"
    assert report["claim_boundary"] == GENERATED_PACKAGE_ROBOT_TASK_CLAIM_BOUNDARY


def test_articulation_smoke_options_reject_invalid_values():
    for kwargs in (
        {"hold_frames": 0},
        {"trajectory_delta_rad": -0.1},
        {"max_gravity_hold_joint_drift": -0.1},
        {"frame_dt_seconds": 0.0},
    ):
        try:
            ArticulationSmokeOptions(**kwargs)
        except ValueError as exc:
            assert next(iter(kwargs)) in str(exc)
        else:
            raise AssertionError(f"{kwargs} should be rejected")


def test_evaluate_articulation_smoke_passes_import_hold_and_trajectory():
    report = evaluate_articulation_smoke(
        asset_path="robot.usda",
        import_metrics={
            "articulation_count": 1,
            "joint_count": 3,
            "joint_dof_count": 2,
            "body_count": 4,
            "shape_count": 4,
        },
        gravity_hold_metrics={
            "finite_state": True,
            "max_joint_drift": 0.001,
        },
        trajectory_metrics={
            "finite_state": True,
            "commanded_joint_index": 0,
            "commanded_joint_delta": 0.05,
            "end_effector_pose_delta_m": 0.02,
        },
        options=ArticulationSmokeOptions(max_gravity_hold_joint_drift=0.01),
        environment=None,
        device="cpu",
    )

    assert report["status"] == "smoke_passed"
    assert report["outcome"] == "accept"
    assert report["metrics"]["joint_tree_import"] == "passed"
    assert report["metrics"]["trajectory_completion"] == "passed"


def test_evaluate_generated_package_robot_task_passes_when_package_is_consumed():
    report = evaluate_generated_package_robot_task_probe(
        asset_path="robot.usda",
        package_metrics={
            "package_id": "robot:phase0_link_aware_bbox",
            "package_primitive_count": 2,
            "source_link_count": 2,
            "generated_collision_shape_count": 2,
            "consumed_primitive_count": 2,
            "missing_body_link_count": 0,
            "source_usd_shape_count": 0,
            "unsupported_primitive_count": 0,
            "invalid_box_primitive_count": 0,
        },
        import_metrics={
            "articulation_count": 1,
            "joint_count": 2,
            "joint_dof_count": 1,
            "body_count": 2,
            "shape_count": 2,
        },
        gravity_hold_metrics={
            "finite_state": True,
            "max_joint_drift": 0.0,
        },
        trajectory_metrics={
            "finite_state": True,
            "commanded_joint_index": 0,
            "commanded_joint_delta": 0.05,
            "end_effector_pose_delta_m": 0.01,
        },
        options=ArticulationSmokeOptions(collapse_fixed_joints=False),
        environment=None,
        device="cpu",
    )

    assert report["stage"] == "newton_generated_package_robot_task_probe"
    assert report["probe_type"] == "generated_package_robot_task_if_robot"
    assert report["status"] == "smoke_passed"
    assert report["outcome"] == "accept"
    assert report["metrics"]["generated_package_consumed"] is True
    assert report["metrics"]["package_consumption"]["package_primitive_count"] == 2
    assert report["metrics"]["package_consumption"]["generated_collision_shape_count"] == 2
    assert report["evidence_level"] == "newton_generated_package_robot_task_smoke"


def test_evaluate_generated_package_robot_task_labels_package_consumption_gaps():
    report = evaluate_generated_package_robot_task_probe(
        asset_path="robot.usda",
        package_metrics={
            "package_id": "robot:phase0_link_aware_bbox",
            "package_primitive_count": 2,
            "source_link_count": 2,
            "generated_collision_shape_count": 1,
            "consumed_primitive_count": 1,
            "missing_body_link_count": 1,
            "source_usd_shape_count": 1,
            "unsupported_primitive_count": 0,
            "invalid_box_primitive_count": 0,
        },
        import_metrics={
            "articulation_count": 1,
            "joint_count": 2,
            "joint_dof_count": 1,
            "body_count": 2,
            "shape_count": 2,
        },
        gravity_hold_metrics={
            "finite_state": True,
            "max_joint_drift": 0.0,
        },
        trajectory_metrics={
            "finite_state": True,
            "commanded_joint_index": 0,
            "commanded_joint_delta": 0.05,
            "end_effector_pose_delta_m": 0.01,
        },
        options=ArticulationSmokeOptions(collapse_fixed_joints=False),
        environment=None,
        device="cpu",
    )

    assert report["status"] == "runtime_failure"
    assert report["outcome"] == "failure"
    assert report["metrics"]["generated_package_consumed"] is False
    assert "generated_package_shape_count_mismatch" in report["failure_labels"]
    assert "generated_package_missing_body_link" in report["failure_labels"]
    assert "source_usd_collision_shapes_not_suppressed" in report["failure_labels"]


def test_attach_generated_package_shapes_filters_generated_self_collisions_when_disabled():
    class FakeShapeConfig:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    class FakeModelBuilder:
        ShapeConfig = FakeShapeConfig

    class FakeNewton:
        ModelBuilder = FakeModelBuilder

    class FakeWarp:
        @staticmethod
        def vec3(*values):
            return values

        @staticmethod
        def quat_identity():
            return (0.0, 0.0, 0.0, 1.0)

        @staticmethod
        def transform(position, rotation):
            return (position, rotation)

    class FakeBuilder:
        def __init__(self):
            self.shapes = []
            self.filtered_pairs = []

        def add_shape_box(self, **kwargs):
            shape_id = len(self.shapes)
            self.shapes.append(kwargs)
            return shape_id

        def add_shape_collision_filter_pair(self, shape_a, shape_b):
            self.filtered_pairs.append((shape_a, shape_b))

    builder = FakeBuilder()
    metrics = _attach_generated_package_shapes(
        builder=builder,
        wp=FakeWarp,
        newton=FakeNewton,
        path_body_map={
            "/Robot/link0": 0,
            "/Robot/link1": 1,
            "/Robot/link2": 2,
        },
        collision_package={
            "package_id": "robot:phase0_link_aware_bbox",
            "primitives": [
                {
                    "primitive_id": "link0-box",
                    "kind": "box",
                    "frame": "/Robot/link0",
                    "source_links": ["/Robot/link0"],
                    "center": [0.0, 0.0, 0.0],
                    "dimensions": {"half_extents": [0.1, 0.1, 0.1]},
                },
                {
                    "primitive_id": "link1-box",
                    "kind": "box",
                    "frame": "/Robot/link1",
                    "source_links": ["/Robot/link1"],
                    "center": [0.0, 0.0, 0.0],
                    "dimensions": {"half_extents": [0.1, 0.1, 0.1]},
                },
                {
                    "primitive_id": "link2-box",
                    "kind": "box",
                    "frame": "/Robot/link2",
                    "source_links": ["/Robot/link2"],
                    "center": [0.0, 0.0, 0.0],
                    "dimensions": {"half_extents": [0.1, 0.1, 0.1]},
                },
            ],
        },
        source_shape_count=0,
        ignored_source_shape_paths=[],
        enable_self_collisions=False,
    )

    assert len(builder.shapes) == 3
    assert builder.filtered_pairs == [(0, 1), (0, 2), (1, 2)]
    assert metrics["generated_self_collision_filter_pair_count"] == 3


def test_attach_generated_package_shapes_rejects_static_body_mapping():
    class FakeShapeConfig:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    class FakeModelBuilder:
        ShapeConfig = FakeShapeConfig

    class FakeNewton:
        ModelBuilder = FakeModelBuilder

    class FakeWarp:
        @staticmethod
        def vec3(*values):
            return values

        @staticmethod
        def quat_identity():
            return (0.0, 0.0, 0.0, 1.0)

        @staticmethod
        def transform(position, rotation):
            return (position, rotation)

    class FakeBuilder:
        def __init__(self):
            self.shapes = []
            self.filtered_pairs = []

        def add_shape_box(self, **kwargs):
            shape_id = len(self.shapes)
            self.shapes.append(kwargs)
            return shape_id

        def add_shape_collision_filter_pair(self, shape_a, shape_b):
            self.filtered_pairs.append((shape_a, shape_b))

    builder = FakeBuilder()
    metrics = _attach_generated_package_shapes(
        builder=builder,
        wp=FakeWarp,
        newton=FakeNewton,
        path_body_map={"/Robot/link0": -1},
        collision_package={
            "package_id": "robot:phase0_link_aware_bbox",
            "primitives": [
                {
                    "primitive_id": "link0-box",
                    "kind": "box",
                    "frame": "/Robot/link0",
                    "source_links": ["/Robot/link0"],
                    "center": [0.0, 0.0, 0.0],
                    "dimensions": {"half_extents": [0.1, 0.1, 0.1]},
                },
            ],
        },
        source_shape_count=0,
        ignored_source_shape_paths=[],
        enable_self_collisions=False,
    )

    assert builder.shapes == []
    assert metrics["generated_collision_shape_count"] == 0
    assert metrics["missing_body_link_count"] == 1
    assert metrics["missing_body_links"] == ["/Robot/link0"]


def test_evaluate_articulation_smoke_labels_missing_articulation_and_drift():
    report = evaluate_articulation_smoke(
        asset_path="robot.usda",
        import_metrics={
            "articulation_count": 0,
            "joint_count": 0,
            "joint_dof_count": 0,
            "body_count": 1,
            "shape_count": 1,
        },
        gravity_hold_metrics={
            "finite_state": True,
            "max_joint_drift": 0.10,
        },
        trajectory_metrics={
            "finite_state": False,
            "commanded_joint_index": None,
            "commanded_joint_delta": 0.0,
            "end_effector_pose_delta_m": 0.0,
        },
        options=ArticulationSmokeOptions(max_gravity_hold_joint_drift=0.01),
        environment=None,
        device="cpu",
    )

    assert report["status"] == "runtime_failure"
    assert report["outcome"] == "failure"
    assert "joint_tree_import_failed" in report["failure_labels"]
    assert "gravity_hold_drift_exceeded" in report["failure_labels"]
    assert "trajectory_completion_failed" in report["failure_labels"]
