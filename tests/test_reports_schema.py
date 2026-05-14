from primitive_collision_compiler.reports.schema import (
    EnvironmentCheck,
    EnvironmentReport,
    NewtonContactCanary,
    NewtonDiagnosticReport,
    NewtonDropSettleRun,
    NewtonShapeMapping,
)


def test_environment_report_serializes_dependency_gap():
    report = EnvironmentReport(
        stage="newton_import",
        status="dependency_gap",
        source_dir="/cpfs/user/zhuzihou/dev/newton",
        source_commit="96713fa965463b69c229a4d30582c733ff3526bb",
        checks=(
            EnvironmentCheck(
                name="newton_import",
                status="dependency_gap",
                detail="No module named 'warp'",
            ),
        ),
    )

    payload = report.to_dict()

    assert payload["stage"] == "newton_import"
    assert payload["status"] == "dependency_gap"
    assert payload["source_commit"] == "96713fa965463b69c229a4d30582c733ff3526bb"
    assert payload["checks"][0]["name"] == "newton_import"
    assert payload["checks"][0]["status"] == "dependency_gap"
    assert payload["checks"][0]["detail"] == "No module named 'warp'"


def test_newton_shape_mapping_serializes_mapping_gap():
    mapping = NewtonShapeMapping(
        primitive_id="bad",
        kind="sphere",
        status="mapping_gap",
        detail="sphere radius is required",
        center=(0.0, 0.0, 0.0),
        dimensions={},
    )

    payload = mapping.to_dict()

    assert payload["primitive_id"] == "bad"
    assert payload["status"] == "mapping_gap"
    assert payload["detail"] == "sphere radius is required"
    assert payload["center"] == [0.0, 0.0, 0.0]


def test_newton_diagnostic_report_serializes_contact_canary_and_environment():
    report = NewtonDiagnosticReport(
        stage="newton_contact_smoke",
        status="smoke_passed",
        asset_id="asset",
        package_id="pkg",
        probe_type="contact_canary",
        device="cpu",
        environment=EnvironmentReport(
            stage="newton_import",
            status="smoke_passed",
            source_dir="/cpfs/user/zhuzihou/dev/newton",
            source_commit="abc123",
            checks=(EnvironmentCheck("newton_import", "smoke_passed", "import newton succeeded"),),
        ),
        primitive_count=3,
        type_counts={"sphere": 1, "box": 1, "capsule": 1},
        shape_mappings=(
            NewtonShapeMapping(
                primitive_id="sphere",
                kind="sphere",
                status="mapped",
                detail="mapped",
                center=(0.0, 0.0, 0.0),
                dimensions={"radius": 0.5},
            ),
        ),
        contact_canaries=(
            NewtonContactCanary(
                primitive_id="sphere",
                kind="sphere",
                status="smoke_passed",
                contact_count=1,
                detail="contact produced",
            ),
        ),
        claim_boundary="contact_canary_only_not_quality",
    )

    payload = report.to_dict()

    assert payload["stage"] == "newton_contact_smoke"
    assert payload["status"] == "smoke_passed"
    assert payload["environment"]["status"] == "smoke_passed"
    assert payload["contact_canaries"][0]["contact_count"] == 1
    assert payload["metrics"] == {}


def test_newton_diagnostic_report_serializes_drop_settle_run():
    run = NewtonDropSettleRun(
        run_id="seed0",
        status="smoke_passed",
        primitive_ids=("box",),
        completed_steps=16,
        initial_height=0.25,
        final_height=0.0,
        min_height=0.0,
        final_linear_velocity=(0.0, 0.0, 0.0),
        max_contact_count=1,
        final_contact_count=1,
        finite_state=True,
        descended=True,
        contact_observed=True,
        failure_labels=(),
    )
    report = NewtonDiagnosticReport(
        stage="newton_drop_settle",
        status="smoke_passed",
        asset_id="asset",
        package_id="pkg",
        probe_type="drop_settle",
        device="cpu",
        environment=None,
        primitive_count=1,
        type_counts={"box": 1},
        shape_mappings=(),
        contact_canaries=(),
        drop_settle_runs=(run,),
        task_scope="single_asset_drop_settle_static_plane",
        initial_conditions={"height_m": 0.25},
        solver={"solver": "xpbd", "frames": 120},
        claim_boundary="drop_settle_task_smoke_not_collision_quality_or_safety",
        evidence_level="newton_drop_settle_task_smoke",
    )

    payload = report.to_dict()

    assert payload["stage"] == "newton_drop_settle"
    assert payload["probe_type"] == "drop_settle"
    assert payload["drop_settle_runs"][0]["run_id"] == "seed0"
    assert payload["drop_settle_runs"][0]["primitive_ids"] == ["box"]
    assert payload["task_scope"] == "single_asset_drop_settle_static_plane"
    assert payload["initial_conditions"] == {"height_m": 0.25}
    assert payload["solver"] == {"solver": "xpbd", "frames": 120}
    assert payload["evidence_level"] == "newton_drop_settle_task_smoke"
