from pathlib import Path

import pytest
import yaml

from primitive_collision_compiler.assets.usd_smoke import inspect_usd_asset, load_asset_manifest
from primitive_collision_compiler.reports.schema import AssetSmokeReport, EnvironmentCheck


def _write_tiny_usd(path: Path):
    Usd = pytest.importorskip("pxr.Usd")
    UsdGeom = pytest.importorskip("pxr.UsdGeom")
    stage = Usd.Stage.CreateNew(str(path))
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)
    root = stage.DefinePrim("/Root", "Xform")
    stage.SetDefaultPrim(root)
    stage.GetRootLayer().Save()


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


def test_load_asset_manifest_returns_assets(tmp_path):
    asset_path = tmp_path / "asset.usda"
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump(
            {
                "manifest_id": "fixture",
                "assets": [
                    {
                        "role": "fixture_asset",
                        "path": str(asset_path),
                        "sha256": "",
                        "include_in_cpd_like_aggregate": False,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    assets = load_asset_manifest(manifest_path)

    assert assets == [
        {
            "role": "fixture_asset",
            "path": str(asset_path),
            "sha256": "",
            "include_in_cpd_like_aggregate": False,
        }
    ]


def test_load_asset_manifest_rejects_malformed_asset_entry(tmp_path):
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump({"assets": [{"role": "fixture_asset", "path": "/tmp/a.usda"}, "bad-entry"]}),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="asset manifest entry 1 must be a mapping"):
        load_asset_manifest(manifest_path)


def test_inspect_usd_asset_reports_smoke_passed_for_openable_stage(tmp_path):
    asset_path = tmp_path / "asset.usda"
    _write_tiny_usd(asset_path)

    report = inspect_usd_asset({"role": "fixture_asset", "path": str(asset_path)})

    assert report.status == "smoke_passed"
    assert report.metadata["default_prim"] == "/Root"
    assert report.metadata["prim_count"] == 1
    assert report.metadata["up_axis"] == "Z"
    assert report.metadata["meters_per_unit"] == 1.0


def test_inspect_usd_asset_reports_missing_asset(tmp_path):
    missing_path = tmp_path / "missing.usd"

    report = inspect_usd_asset({"role": "fixture_asset", "path": str(missing_path)})

    assert report.status == "missing_asset"
    assert report.checks[0].name == "asset_path"


def test_inspect_usd_asset_reports_read_error_for_directory_hash(tmp_path):
    asset_dir = tmp_path / "asset_dir.usd"
    asset_dir.mkdir()

    report = inspect_usd_asset({"role": "fixture_asset", "path": str(asset_dir), "sha256": "abc"})

    assert report.status == "read_error"
    assert any(check.name == "sha256" and check.status == "read_error" for check in report.checks)
