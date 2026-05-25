from primitive_collision_compiler.newton.articulation_smoke import (
    ARTICULATION_SMOKE_CLAIM_BOUNDARY,
    ArticulationSmokeOptions,
    evaluate_articulation_smoke,
    run_newton_articulation_smoke,
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
