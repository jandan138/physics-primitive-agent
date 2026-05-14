from primitive_collision_compiler.reports.schema import AssetSmokeReport, EnvironmentCheck


def test_asset_smoke_report_serializes_metadata_and_checks():
    report = AssetSmokeReport(
        stage="usd_open",
        status="smoke_passed",
        role="bed_dev_smoke",
        path="/tmp/bed.usd",
        checks=(EnvironmentCheck("usd_open", "smoke_passed", "opened stage"),),
        metadata={"prim_count": 3, "up_axis": "Z", "meters_per_unit": 1.0},
    )

    payload = report.to_dict()

    assert payload["stage"] == "usd_open"
    assert payload["status"] == "smoke_passed"
    assert payload["role"] == "bed_dev_smoke"
    assert payload["metadata"]["prim_count"] == 3
    assert payload["checks"][0]["name"] == "usd_open"
