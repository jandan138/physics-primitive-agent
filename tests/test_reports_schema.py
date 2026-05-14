from primitive_collision_compiler.reports.schema import (
    EnvironmentCheck,
    EnvironmentReport,
    NewtonContactCanary,
    NewtonDiagnosticReport,
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
