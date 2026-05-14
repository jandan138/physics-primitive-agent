import json
from pathlib import Path

import pytest
import yaml

from primitive_collision_compiler import cli

FIXTURE_CONFIG = Path(__file__).parent / "fixtures" / "dry_run_mvp.yaml"


def _write_newton_check_config(path: Path, source_dir: Path):
    path.write_text(
        "\n".join(
            [
                "asset:",
                "  path: assets/example.usda",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "newton:",
                f"  source_dir: {source_dir}",
            ]
        ),
        encoding="utf-8",
    )


def _write_tiny_usd(path: Path):
    Usd = pytest.importorskip("pxr.Usd")
    UsdGeom = pytest.importorskip("pxr.UsdGeom")
    stage = Usd.Stage.CreateNew(str(path))
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    root = stage.DefinePrim("/Root", "Xform")
    stage.SetDefaultPrim(root)
    stage.GetRootLayer().Save()


def test_help_mentions_project(capsys):
    assert cli.main(["--help"]) == 0

    output = capsys.readouterr().out
    assert "Newton Primitive Collision Compiler" in output


def test_config_dry_run_emits_json_report(capsys):
    assert cli.main(["--config", str(FIXTURE_CONFIG), "--dry-run"]) == 0

    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "dry_run"
    assert report["compiled"] is False
    assert report["task"] == "grasping"


def test_config_dry_run_uses_configured_asset_id(capsys):
    config_path = Path(__file__).resolve().parents[1] / "configs" / "deepdive" / "mvp.yaml"

    assert cli.main(["--config", str(config_path), "--dry-run"]) == 0

    report = json.loads(capsys.readouterr().out)
    assert report["asset_id"] == "handle_gap_mvp"


def test_config_rejects_scalar_allowed_fallback(tmp_path, capsys):
    config_path = tmp_path / "bad.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  path: assets/example.usda",
                "task:",
                "  primary: grasping",
                "compile:",
                "  allowed_fallback: coacd",
            ]
        ),
        encoding="utf-8",
    )

    assert cli.main(["--config", str(config_path), "--dry-run"]) == 2
    assert "compile.allowed_fallback must be a list of strings" in capsys.readouterr().err


def test_missing_config_reports_clean_error(capsys):
    assert cli.main(["--config", "missing.yaml", "--dry-run"]) == 2
    captured = capsys.readouterr()
    assert "missing.yaml" in captured.err
    assert "Traceback" not in captured.err


def test_check_newton_emits_environment_report(tmp_path, capsys):
    source_dir = tmp_path / "newton-source"
    source_dir.mkdir()
    config_path = tmp_path / "newton_check.yaml"
    _write_newton_check_config(config_path, source_dir)

    assert cli.main(["--config", str(config_path), "--check-newton"]) == 0

    report = json.loads(capsys.readouterr().out)
    assert report["stage"] == "newton_import"
    assert report["source_dir"] == str(source_dir)
    assert report["status"] == "dependency_gap"
    assert any(check["name"] == "newton_import" for check in report["checks"])


def test_check_newton_returns_error_for_missing_source(tmp_path, capsys):
    config_path = tmp_path / "newton_check.yaml"
    missing_source = tmp_path / "missing-newton"
    _write_newton_check_config(config_path, missing_source)

    assert cli.main(["--config", str(config_path), "--check-newton"]) == 2

    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "missing_source"
    assert report["source_dir"] == str(missing_source)


def test_check_newton_expands_source_dir_environment_variable(tmp_path, capsys, monkeypatch):
    source_dir = tmp_path / "newton-source"
    source_dir.mkdir()
    monkeypatch.setenv("TEST_NEWTON_SOURCE_DIR", str(source_dir))
    config_path = tmp_path / "newton_check.yaml"
    _write_newton_check_config(config_path, Path("$TEST_NEWTON_SOURCE_DIR"))

    assert cli.main(["--config", str(config_path), "--check-newton"]) == 0

    report = json.loads(capsys.readouterr().out)
    assert report["source_dir"] == str(source_dir)


def test_check_assets_emits_manifest_reports(tmp_path, capsys):
    asset_path = tmp_path / "asset.usda"
    _write_tiny_usd(asset_path)
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump({"assets": [{"role": "fixture_asset", "path": str(asset_path)}]}),
        encoding="utf-8",
    )
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                f"  path: {manifest_path}",
                "task:",
                "  primary: collision_proxy_diagnostic",
            ]
        ),
        encoding="utf-8",
    )

    assert cli.main(["--config", str(config_path), "--check-assets"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "asset_usd_open"
    assert payload["status"] == "smoke_passed"
    assert payload["reports"][0]["role"] == "fixture_asset"
    assert payload["reports"][0]["metadata"]["default_prim"] == "/Root"


def test_check_assets_prefers_cpd_like_manifest_over_seed_asset(tmp_path, capsys):
    seed_asset_path = tmp_path / "seed.usda"
    manifest_asset_path = tmp_path / "manifest_asset.usda"
    _write_tiny_usd(seed_asset_path)
    _write_tiny_usd(manifest_asset_path)
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump({"assets": [{"role": "manifest_asset", "path": str(manifest_asset_path)}]}),
        encoding="utf-8",
    )
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                f"  path: {seed_asset_path}",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "cpd_like:",
                f"  asset_manifest: {manifest_path}",
            ]
        ),
        encoding="utf-8",
    )

    assert cli.main(["--config", str(config_path), "--check-assets"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert [report["role"] for report in payload["reports"]] == ["manifest_asset"]


def test_check_assets_reports_clean_error_for_malformed_manifest(tmp_path, capsys):
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump({"assets": [{"role": "fixture_asset", "path": "/tmp/a.usda"}, "bad-entry"]}),
        encoding="utf-8",
    )
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                f"  path: {manifest_path}",
                "task:",
                "  primary: collision_proxy_diagnostic",
            ]
        ),
        encoding="utf-8",
    )

    assert cli.main(["--config", str(config_path), "--check-assets"]) == 2

    captured = capsys.readouterr()
    assert "asset manifest entry 1 must be a mapping" in captured.err
    assert "Traceback" not in captured.err


def test_check_assets_returns_json_for_asset_read_error(tmp_path, capsys):
    asset_dir = tmp_path / "asset_dir.usd"
    asset_dir.mkdir()
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump({"assets": [{"role": "fixture_asset", "path": str(asset_dir), "sha256": "abc"}]}),
        encoding="utf-8",
    )
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                f"  path: {manifest_path}",
                "task:",
                "  primary: collision_proxy_diagnostic",
            ]
        ),
        encoding="utf-8",
    )

    assert cli.main(["--config", str(config_path), "--check-assets"]) == 2

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "smoke_failed"
    assert payload["reports"][0]["status"] == "read_error"


def test_cli_run_cpd_like_emits_report_for_tiny_usd(tmp_path, capsys):
    Usd = pytest.importorskip("pxr.Usd")
    UsdGeom = pytest.importorskip("pxr.UsdGeom")
    asset_path = tmp_path / "quad.usda"
    stage = Usd.Stage.CreateNew(str(asset_path))
    mesh = UsdGeom.Mesh.Define(stage, "/Quad")
    mesh.CreatePointsAttr([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
    mesh.CreateFaceVertexCountsAttr([4])
    mesh.CreateFaceVertexIndicesAttr([0, 1, 2, 3])
    stage.GetRootLayer().Save()
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: tiny_quad",
                f"  path: {asset_path}",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "compile:",
                "  method: cpd_like_baseline",
                "  max_primitives: 1",
                "  allowed_fallback:",
                "    - convex_hull",
                "  verify:",
                "    - geometry_only",
                "cpd_like:",
                "  primitive_subset:",
                "    - box",
                "    - sphere",
                "    - capsule",
                "  max_source_faces: 8",
            ]
        ),
        encoding="utf-8",
    )

    assert cli.main(["--config", str(config_path), "--run-cpd-like"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "cpd_like_face_merge"
    assert payload["status"] == "smoke_passed"
    assert payload["asset_id"] == "tiny_quad"
    assert payload["source_path"] == str(asset_path)
    assert payload["primitive_count"] == 1


def test_cli_run_cpd_like_resolves_manifest_asset_role(tmp_path, capsys):
    Usd = pytest.importorskip("pxr.Usd")
    UsdGeom = pytest.importorskip("pxr.UsdGeom")
    asset_path = tmp_path / "manifest_quad.usda"
    stage = Usd.Stage.CreateNew(str(asset_path))
    mesh = UsdGeom.Mesh.Define(stage, "/Quad")
    mesh.CreatePointsAttr([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
    mesh.CreateFaceVertexCountsAttr([4])
    mesh.CreateFaceVertexIndicesAttr([0, 1, 2, 3])
    stage.GetRootLayer().Save()
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump({"assets": [{"role": "bed_dev_smoke", "path": str(asset_path)}]}),
        encoding="utf-8",
    )
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: manifest_quad",
                f"  path: {manifest_path}",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "compile:",
                "  max_primitives: 1",
                "  allowed_fallback:",
                "    - convex_hull",
                "  verify:",
                "    - geometry_only",
                "cpd_like:",
                f"  asset_manifest: {manifest_path}",
                "  asset_role: bed_dev_smoke",
                "  max_source_faces: 8",
            ]
        ),
        encoding="utf-8",
    )

    assert cli.main(["--config", str(config_path), "--run-cpd-like"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["source_path"] == str(asset_path)
    assert payload["primitive_count"] == 1


def test_cli_run_cpd_like_reports_clean_error_for_bad_subset(tmp_path, capsys):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: bad_subset",
                "  path: missing.usda",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "cpd_like:",
                "  primitive_subset: box",
            ]
        ),
        encoding="utf-8",
    )

    assert cli.main(["--config", str(config_path), "--run-cpd-like"]) == 2

    captured = capsys.readouterr()
    assert "cpd_like.primitive_subset must be a list of strings" in captured.err
    assert "Traceback" not in captured.err


def test_cli_run_cpd_like_reports_clean_error_for_bad_face_cap(tmp_path, capsys):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: bad_face_cap",
                "  path: missing.usda",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "cpd_like:",
                "  max_source_faces:",
                "    - 4",
            ]
        ),
        encoding="utf-8",
    )

    assert cli.main(["--config", str(config_path), "--run-cpd-like"]) == 2

    captured = capsys.readouterr()
    assert "cpd_like.max_source_faces must be an integer" in captured.err
    assert "Traceback" not in captured.err


def test_cli_run_cpd_like_returns_json_for_invalid_usd(tmp_path, capsys):
    asset_path = tmp_path / "invalid.usda"
    asset_path.write_text("not a usd file", encoding="utf-8")
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: invalid_usd",
                f"  path: {asset_path}",
                "task:",
                "  primary: collision_proxy_diagnostic",
            ]
        ),
        encoding="utf-8",
    )

    assert cli.main(["--config", str(config_path), "--run-cpd-like"]) == 2

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "cpd_like_face_merge"
    assert payload["status"] == "smoke_failed"
    assert payload["asset_id"] == "invalid_usd"
    assert "usd_open_failed" in payload["fallback_reason"]
