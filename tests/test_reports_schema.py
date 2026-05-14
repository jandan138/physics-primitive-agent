from primitive_collision_compiler.reports.schema import EnvironmentCheck, EnvironmentReport


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
