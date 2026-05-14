import json
from pathlib import Path

import yaml
from pxr import Usd, UsdGeom

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
