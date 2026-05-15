from pathlib import Path

import pytest
import yaml

from primitive_collision_compiler.assets.materialization import (
    build_asset_materialization_report,
)


def test_build_asset_materialization_report_localizes_usd_layer_closure(tmp_path):
    pytest.importorskip("pxr.Usd")
    root_path = tmp_path / "source" / "root.usda"
    child_path = tmp_path / "source" / "child.usda"
    root_path.parent.mkdir()
    _write_tiny_usd(child_path, "/Child")
    _write_root_with_sublayer(root_path, "./child.usda")
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump(
            {
                "manifest_id": "fixture_manifest",
                "assets": [
                    {
                        "role": "fixture_asset",
                        "path": str(root_path),
                        "sha256": "",
                        "provenance_status": "fixture",
                        "license_context": "fixture",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    report = build_asset_materialization_report(
        manifest_path,
        mirror_root=tmp_path / "mirror",
    )

    assert report["stage"] == "asset_materialization"
    assert report["status"] == "materialized"
    case = report["assets"][0]
    assert case["role"] == "fixture_asset"
    assert case["status"] == "materialized"
    assert Path(case["local_path"]).exists()
    assert case["local_sha256"]
    assert case["dependency_summary"]["layer_count"] == 2
    assert case["local_file_summary"]["file_count"] == 2
    assert case["local_open_report"]["status"] == "smoke_passed"


def test_build_asset_materialization_report_fails_source_hash_mismatch(tmp_path):
    pytest.importorskip("pxr.Usd")
    root_path = tmp_path / "source" / "root.usda"
    root_path.parent.mkdir()
    _write_tiny_usd(root_path, "/Root")
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump(
            {
                "manifest_id": "fixture_manifest",
                "assets": [
                    {
                        "role": "fixture_asset",
                        "path": str(root_path),
                        "sha256": "0" * 64,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    report = build_asset_materialization_report(
        manifest_path,
        mirror_root=tmp_path / "mirror",
    )

    assert report["status"] == "failed"
    assert report["assets"][0]["status"] == "source_hash_mismatch"
    assert not (tmp_path / "mirror" / "fixture_manifest" / "fixture_asset" / "root.usda").exists()


def test_build_asset_materialization_report_rejects_unsafe_role(tmp_path):
    pytest.importorskip("pxr.Usd")
    root_path = tmp_path / "source" / "root.usda"
    root_path.parent.mkdir()
    _write_tiny_usd(root_path, "/Root")
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump(
            {
                "manifest_id": "fixture_manifest",
                "assets": [
                    {
                        "role": "../escape",
                        "path": str(root_path),
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    report = build_asset_materialization_report(
        manifest_path,
        mirror_root=tmp_path / "mirror",
    )

    assert report["status"] == "failed"
    assert report["assets"][0]["status"] == "unsafe_asset_role"
    assert not (tmp_path / "mirror" / "escape").exists()


def test_build_asset_materialization_report_handles_missing_path(tmp_path):
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump(
            {
                "manifest_id": "fixture_manifest",
                "assets": [
                    {
                        "role": "fixture_asset",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    report = build_asset_materialization_report(
        manifest_path,
        mirror_root=tmp_path / "mirror",
    )

    assert report["status"] == "failed"
    assert report["assets"][0]["status"] == "missing_asset_path"


def _write_tiny_usd(path: Path, prim_path: str):
    Usd = pytest.importorskip("pxr.Usd")
    UsdGeom = pytest.importorskip("pxr.UsdGeom")
    stage = Usd.Stage.CreateNew(str(path))
    root = stage.DefinePrim(prim_path, "Xform")
    stage.SetDefaultPrim(root)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)
    stage.GetRootLayer().Save()


def _write_root_with_sublayer(path: Path, sublayer: str):
    Usd = pytest.importorskip("pxr.Usd")
    UsdGeom = pytest.importorskip("pxr.UsdGeom")
    stage = Usd.Stage.CreateNew(str(path))
    root = stage.DefinePrim("/Root", "Xform")
    stage.SetDefaultPrim(root)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)
    layer = stage.GetRootLayer()
    layer.subLayerPaths.append(sublayer)
    layer.Save()
