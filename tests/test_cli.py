import json
from pathlib import Path

import pytest
import yaml

from primitive_collision_compiler import cli
from primitive_collision_compiler.contracts import CollisionPackage
from primitive_collision_compiler.reports.schema import NewtonDiagnosticReport

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


def _write_mesh_usd(path: Path, points, face_vertex_counts, face_vertex_indices):
    Usd = pytest.importorskip("pxr.Usd")
    UsdGeom = pytest.importorskip("pxr.UsdGeom")
    stage = Usd.Stage.CreateNew(str(path))
    mesh = UsdGeom.Mesh.Define(stage, "/Mesh")
    mesh.CreatePointsAttr(points)
    mesh.CreateFaceVertexCountsAttr(face_vertex_counts)
    mesh.CreateFaceVertexIndicesAttr(face_vertex_indices)
    stage.GetRootLayer().Save()


def _write_two_mesh_manifest(tmp_path: Path) -> Path:
    bed_path = tmp_path / "bed.usda"
    franka_path = tmp_path / "franka.usda"
    _write_mesh_usd(
        bed_path,
        points=[
            (0, 0, 0),
            (2, 0, 0),
            (2, 1, 0),
            (0, 1, 0),
            (0, 0, 0.5),
            (2, 0, 0.5),
            (2, 1, 0.5),
            (0, 1, 0.5),
        ],
        face_vertex_counts=[4, 4, 4, 4, 4, 4],
        face_vertex_indices=[
            0,
            1,
            2,
            3,
            4,
            7,
            6,
            5,
            0,
            4,
            5,
            1,
            1,
            5,
            6,
            2,
            2,
            6,
            7,
            3,
            3,
            7,
            4,
            0,
        ],
    )
    _write_mesh_usd(
        franka_path,
        points=[
            (0, 0, 0),
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
        ],
        face_vertex_counts=[3, 3, 3, 3],
        face_vertex_indices=[0, 1, 2, 0, 3, 1, 1, 3, 2, 2, 3, 0],
    )
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump(
            {
                "manifest_id": "test_manifest",
                "assets": [
                    {"role": "bed_dev_smoke", "path": str(bed_path)},
                    {"role": "franka_import_smoke", "path": str(franka_path)},
                ],
            }
        ),
        encoding="utf-8",
    )
    return manifest_path


def _write_real_usd_native_config(tmp_path: Path, manifest_path: Path) -> Path:
    config_path = tmp_path / "real_usd_native.yaml"
    config_path.write_text(
        yaml.safe_dump(
            {
                "asset": {
                    "id": "bed_franka_native_probe",
                    "path": str(manifest_path),
                },
                "task": {"primary": "native_primitive_fitting_comparison"},
                "compile": {"method": "cpd_like_baseline", "max_primitives": 1},
                "cpd_like": {
                    "asset_manifest": str(manifest_path),
                    "asset_roles": ["bed_dev_smoke", "franka_import_smoke"],
                    "legacy_primitive_subset": ["box", "sphere", "capsule"],
                    "native_primitive_subset": [
                        "box",
                        "sphere",
                        "capsule",
                        "cylinder",
                        "cone",
                        "ellipsoid",
                    ],
                    "max_source_faces_by_role": {
                        "bed_dev_smoke": 8,
                        "franka_import_smoke": 4,
                    },
                    "component_merge": "virtual_pairwise",
                    "report_merge_trace": "summary",
                },
                "native_fitting_comparison": {
                    "claim_boundary": (
                        "real_usd_native_fitting_comparison_not_collision_quality_validation"
                    ),
                    "evidence_level": "offline_real_usd_native_fitting_smoke",
                },
                "newton": {"source_dir": str(tmp_path / "newton")},
                "newton_diagnostic": {
                    "probe_type": "contact_canary",
                    "device": "cpu",
                    "drop_settle": {"frames": 12, "substeps": 2},
                    "sphere_rain": {"sphere_count_x": 2, "sphere_count_y": 2},
                },
            }
        ),
        encoding="utf-8",
    )
    return config_path


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


def test_cli_materialize_assets_emits_report(tmp_path, capsys, monkeypatch):
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump({"manifest_id": "fixture", "assets": []}),
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
    calls = []

    def fake_report(manifest_path_arg, *, mirror_root=None):
        calls.append((str(manifest_path_arg), mirror_root))
        return {"stage": "asset_materialization", "status": "materialized", "assets": []}

    monkeypatch.setattr(cli, "build_asset_materialization_report", fake_report, raising=False)

    assert cli.main(["--config", str(config_path), "--materialize-assets"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "asset_materialization"
    assert calls == [(str(manifest_path), None)]


def test_cli_materialize_assets_redirects_builder_stdout_to_stderr(tmp_path, capsys, monkeypatch):
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump({"manifest_id": "fixture", "assets": []}),
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

    def noisy_report(manifest_path_arg, *, mirror_root=None):
        print("NOISY USD OUTPUT")
        return {"stage": "asset_materialization", "status": "materialized", "assets": []}

    monkeypatch.setattr(cli, "build_asset_materialization_report", noisy_report, raising=False)

    assert cli.main(["--config", str(config_path), "--materialize-assets"]) == 0

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["stage"] == "asset_materialization"
    assert "NOISY USD OUTPUT" not in captured.out
    assert "NOISY USD OUTPUT" in captured.err


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


def test_cli_run_cpd_like_component_merge_gate_emits_merge_metrics(tmp_path, capsys):
    Usd = pytest.importorskip("pxr.Usd")
    UsdGeom = pytest.importorskip("pxr.UsdGeom")
    asset_path = tmp_path / "disconnected_triangles.usda"
    stage = Usd.Stage.CreateNew(str(asset_path))
    mesh = UsdGeom.Mesh.Define(stage, "/Disconnected")
    mesh.CreatePointsAttr(
        [
            (0, 0, 0),
            (1, 0, 0),
            (0, 1, 0),
            (4, 0, 0),
            (5, 0, 0),
            (4, 1, 0),
        ]
    )
    mesh.CreateFaceVertexCountsAttr([3, 3])
    mesh.CreateFaceVertexIndicesAttr([0, 1, 2, 3, 4, 5])
    stage.GetRootLayer().Save()
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: disconnected_triangles",
                f"  path: {asset_path}",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "compile:",
                "  method: cpd_like_baseline",
                "  max_primitives: 1",
                "cpd_like:",
                "  primitive_subset:",
                "    - box",
                "  max_source_faces: 8",
                "  component_merge: virtual_pairwise",
                "  report_merge_trace: summary",
                "  claim_boundary: component_merge_gate_not_cpd_reproduction",
            ]
        ),
        encoding="utf-8",
    )

    assert cli.main(["--config", str(config_path), "--run-cpd-like"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "cpd_like_component_merge_gate"
    assert payload["status"] == "smoke_passed"
    assert payload["merge_policy"] == "virtual_pairwise"
    assert payload["virtual_component_merge_count"] == 1
    assert payload["merge_cost_summary"]["accepted_merge_count"] == 1
    assert payload["primitives"][0]["source_component_ids"] == [0, 1]
    assert payload["claim_boundary"] == "component_merge_gate_not_cpd_reproduction"


def test_cli_run_cpd_like_accepts_cost_guided_merge_search_policy(tmp_path, capsys):
    asset_path = tmp_path / "cost_guided_pair_choice.usda"
    _write_mesh_usd(
        asset_path,
        [
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (10.0, 10.0, 10.0),
            (0.05, 0.05, 0.05),
            (1.05, 0.05, 0.05),
            (0.05, 1.05, 0.05),
        ],
        [3, 3, 3],
        [0, 1, 2, 1, 2, 3, 4, 5, 6],
    )
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: cost_guided_pair_choice",
                f"  path: {asset_path}",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "compile:",
                "  method: cpd_like_baseline",
                "  max_primitives: 2",
                "cpd_like:",
                "  primitive_subset:",
                "    - box",
                "  max_source_faces: 8",
                "  component_merge: virtual_pairwise",
                "  merge_search_policy: cost_guided_pairwise",
                "  report_merge_trace: steps",
            ]
        ),
        encoding="utf-8",
    )

    assert cli.main(["--config", str(config_path), "--run-cpd-like"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "cpd_like_cost_guided_merge_smoke"
    assert payload["merge_policy"] == "virtual_pairwise"
    assert payload["merge_search_policy"] == "cost_guided_pairwise"
    assert payload["topology_merge_count"] == 0
    assert payload["virtual_component_merge_count"] == 1
    assert payload["merge_trace"][0]["decision"] == "accepted"
    assert payload["merge_trace"][0]["merge_kind"] == "virtual_component"


def test_cli_run_cpd_like_summary_merge_trace_omits_trace_key(tmp_path, capsys):
    asset_path = tmp_path / "cost_guided_pair_choice.usda"
    _write_mesh_usd(
        asset_path,
        [
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (10.0, 10.0, 10.0),
            (0.05, 0.05, 0.05),
            (1.05, 0.05, 0.05),
            (0.05, 1.05, 0.05),
        ],
        [3, 3, 3],
        [0, 1, 2, 1, 2, 3, 4, 5, 6],
    )
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: cost_guided_pair_choice",
                f"  path: {asset_path}",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "compile:",
                "  method: cpd_like_baseline",
                "  max_primitives: 2",
                "cpd_like:",
                "  primitive_subset:",
                "    - box",
                "  max_source_faces: 8",
                "  component_merge: virtual_pairwise",
                "  merge_search_policy: cost_guided_pairwise",
            ]
        ),
        encoding="utf-8",
    )

    assert cli.main(["--config", str(config_path), "--run-cpd-like"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["merge_search_policy"] == "cost_guided_pairwise"
    assert "merge_trace" not in payload


def test_cli_run_cpd_like_objective_report_emits_json_for_tiny_usd(tmp_path, capsys):
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
                "  id: tiny_quad_objective",
                f"  path: {asset_path}",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "compile:",
                "  method: cpd_like_baseline",
                "  max_primitives: 1",
                "  verify:",
                "    - cpd_like_objective_report",
                "cpd_like:",
                "  primitive_subset:",
                "    - box",
                "  max_source_faces: 8",
                "cpd_like_objective:",
                "  objective_version: cpd_paper_aligned_surrogate_v0",
                "  claim_boundary: offline_objective_report_not_collision_quality_validation",
                "  evidence_level: offline_cpd_like_objective_surrogate_smoke",
                "  primitive_type_weights:",
                "    box: 1.0",
            ]
        ),
        encoding="utf-8",
    )

    assert cli.main(["--config", str(config_path), "--run-cpd-like-objective-report"]) == 0

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["stage"] == "cpd_like_offline_objective"
    assert payload["status"] == "smoke_passed"
    assert payload["asset_id"] == "tiny_quad_objective"
    assert payload["source_path"] == str(asset_path)
    assert payload["claim_boundary"] == "offline_objective_report_not_collision_quality_validation"
    assert payload["evidence_level"] == "offline_cpd_like_objective_surrogate_smoke"
    assert payload["metrics"]["primitive_budget"]["within_budget"] is True
    assert payload["metrics"]["geometric_excess_proxy"]["weighted_primitive_volume"] > 0.0
    assert payload["metrics"]["paper_alignment"]["paper_equation_id"] == "Eq.4"
    assert payload["metrics"]["paper_alignment"]["computes_paper_eq4"] is False
    assert captured.err == ""


def test_cli_run_cpd_like_objective_report_accepts_capped_cylinder_proxy(tmp_path, capsys):
    asset_path = tmp_path / "quad.usda"
    _write_mesh_usd(
        asset_path,
        [(0, 0, 0), (2, 0, 0), (2, 0.2, 0), (0, 0.2, 0)],
        [4],
        [0, 1, 2, 3],
    )
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: tiny_capped_cylinder_proxy",
                f"  path: {asset_path}",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "compile:",
                "  method: cpd_like_baseline",
                "  max_primitives: 1",
                "  verify:",
                "    - cpd_like_objective_report",
                "cpd_like:",
                "  primitive_subset:",
                "    - capped_cylinder",
                "  max_source_faces: 8",
                "cpd_like_objective:",
                "  objective_version: cpd_paper_aligned_surrogate_v0",
                "  claim_boundary: capped_cylinder_proxy_objective_not_collision_quality_validation",
                "  evidence_level: offline_cpd_like_capped_cylinder_proxy_smoke",
                "  primitive_type_weights:",
                "    capped_cylinder: 1.0",
            ]
        ),
        encoding="utf-8",
    )

    assert cli.main(["--config", str(config_path), "--run-cpd-like-objective-report"]) == 0

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["stage"] == "cpd_like_offline_objective"
    assert payload["metrics"]["paper_primitive_gap"]["unsupported_paper_primitive_count"] == 2
    assert payload["metrics"]["paper_primitive_gap"]["unsupported_paper_primitives"] == [
        "frustum",
        "trapezoidal_prism",
    ]
    assert payload["decomposition"]["primitive_count"] == 1
    assert captured.err == ""


def test_cli_run_cpd_like_objective_report_returns_json_for_partial_decomposition(
    tmp_path,
    capsys,
):
    asset_path = tmp_path / "disconnected.usda"
    _write_mesh_usd(
        asset_path,
        points=[
            (0, 0, 0),
            (1, 0, 0),
            (0, 1, 0),
            (4, 0, 0),
            (5, 0, 0),
            (4, 1, 0),
        ],
        face_vertex_counts=[3, 3],
        face_vertex_indices=[0, 1, 2, 3, 4, 5],
    )
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: disconnected_objective",
                f"  path: {asset_path}",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "compile:",
                "  method: cpd_like_baseline",
                "  max_primitives: 1",
                "cpd_like:",
                "  primitive_subset:",
                "    - box",
                "  max_source_faces: 8",
            ]
        ),
        encoding="utf-8",
    )

    assert cli.main(["--config", str(config_path), "--run-cpd-like-objective-report"]) == 2

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["stage"] == "cpd_like_offline_objective"
    assert payload["status"] == "partial"
    assert payload["failure_labels"] == [
        "source_decomposition_partial",
        "primitive_budget_not_met",
        "unmerged_components",
    ]
    assert payload["metrics"]["primitive_budget"]["over_budget_count"] == 1
    assert captured.err == ""


def test_cli_run_cpd_like_objective_report_rejects_non_finite_json(
    tmp_path,
    capsys,
    monkeypatch,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: non_finite_objective",
                "  path: assets/example.usda",
                "task:",
                "  primary: collision_proxy_diagnostic",
            ]
        ),
        encoding="utf-8",
    )

    class NonFiniteReport:
        status = "smoke_passed"

        def to_dict(self):
            return {
                "stage": "cpd_like_offline_objective",
                "status": "smoke_passed",
                "metrics": {"bad": float("nan")},
            }

    monkeypatch.setattr(cli, "_run_cpd_like_report", lambda config: (object(), "asset.usda", 8))
    monkeypatch.setattr(
        cli,
        "build_cpd_like_objective_report",
        lambda *args, **kwargs: NonFiniteReport(),
    )

    assert cli.main(["--config", str(config_path), "--run-cpd-like-objective-report"]) == 2

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "cpd_like_objective report contains non-finite JSON values" in captured.err
    assert "Traceback" not in captured.err


@pytest.mark.parametrize(
    ("objective_yaml", "message"),
    [
        (
            ["cpd_like_objective: box"],
            "cpd_like_objective must be a mapping",
        ),
        (
            ["cpd_like_objective:", "  primitive_type_weights: box"],
            "cpd_like_objective.primitive_type_weights must be a mapping",
        ),
        (
            ["cpd_like_objective:", "  primitive_type_weights:", '    "": 1.0'],
            "cpd_like_objective.primitive_type_weights keys must be non-empty",
        ),
        (
            ["cpd_like_objective:", "  primitive_type_weights:", "    box: -1.0"],
            "cpd_like_objective.primitive_type_weights values must be finite non-negative numbers",
        ),
        (
            ["cpd_like_objective:", "  primitive_type_weights:", "    box: .nan"],
            "cpd_like_objective.primitive_type_weights must be finite",
        ),
    ],
)
def test_cli_run_cpd_like_objective_report_rejects_malformed_objective_config(
    tmp_path,
    capsys,
    objective_yaml,
    message,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: bad_objective",
                "  path: assets/example.usda",
                "task:",
                "  primary: collision_proxy_diagnostic",
                *objective_yaml,
            ]
        ),
        encoding="utf-8",
    )

    assert cli.main(["--config", str(config_path), "--run-cpd-like-objective-report"]) == 2

    captured = capsys.readouterr()
    assert message in captured.err
    assert "Traceback" not in captured.err


def test_cli_run_cpd_like_objective_report_rejects_malformed_cpd_like_config(
    tmp_path,
    capsys,
):
    asset_path = tmp_path / "quad.usda"
    _write_mesh_usd(
        asset_path,
        points=[(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)],
        face_vertex_counts=[4],
        face_vertex_indices=[0, 1, 2, 3],
    )
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: bad_cpd_like",
                f"  path: {asset_path}",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "compile:",
                "  method: cpd_like_baseline",
                "  max_primitives: 1",
                "cpd_like:",
                "  primitive_subset:",
                "    - box",
                "  component_merge: unsupported",
            ]
        ),
        encoding="utf-8",
    )

    assert cli.main(["--config", str(config_path), "--run-cpd-like-objective-report"]) == 2

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "cpd_like_offline_objective"
    assert payload["status"] == "smoke_failed"
    assert "component_merge must be topology_only or virtual_pairwise" in payload["fallback_reason"]


def test_cli_run_cpd_like_synthetic_comparison_emits_json_without_config(capsys):
    assert cli.main(["--run-cpd-like-synthetic-comparison"]) == 0

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["stage"] == "cpd_like_synthetic_objective_comparison"
    assert payload["status"] == "smoke_passed"
    assert [case["case_id"] for case in payload["cases"]] == [
        "adjacent_square",
        "disconnected_pair",
        "blocked_disconnected_pair",
    ]
    assert captured.err == ""


def test_cli_run_cpd_like_synthetic_comparison_rejects_non_finite_json(
    capsys,
    monkeypatch,
):
    monkeypatch.setattr(
        cli,
        "build_cpd_like_synthetic_comparison_report",
        lambda: {
            "stage": "cpd_like_synthetic_objective_comparison",
            "status": "smoke_passed",
            "bad": float("nan"),
        },
    )

    assert cli.main(["--run-cpd-like-synthetic-comparison"]) == 2

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "cpd_like_synthetic_comparison report contains non-finite JSON values" in captured.err
    assert "Traceback" not in captured.err


def test_cli_run_cpd_like_cost_guided_synthetic_comparison_emits_json_without_config(capsys):
    assert cli.main(["--run-cpd-like-cost-guided-synthetic-comparison"]) == 0

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["stage"] == "cpd_like_cost_guided_synthetic_objective_comparison"
    assert payload["status"] == "smoke_passed"
    assert payload["cases"][0]["case_id"] == "cost_guided_pair_choice"
    assert captured.err == ""


def test_cli_run_cpd_like_cost_guided_synthetic_comparison_rejects_non_finite_json(
    capsys,
    monkeypatch,
):
    monkeypatch.setattr(
        cli,
        "build_cpd_like_cost_guided_synthetic_comparison_report",
        lambda: {
            "stage": "cpd_like_cost_guided_synthetic_objective_comparison",
            "status": "smoke_passed",
            "bad": float("nan"),
        },
    )

    assert cli.main(["--run-cpd-like-cost-guided-synthetic-comparison"]) == 2

    captured = capsys.readouterr()
    assert captured.out == ""
    assert (
        "cpd_like_cost_guided_synthetic_comparison report contains non-finite JSON values"
        in captured.err
    )
    assert "Traceback" not in captured.err


def test_cli_run_cpd_like_expected_failure_workbench_emits_json_without_config(capsys):
    assert cli.main(["--run-cpd-like-expected-failure-workbench"]) == 0

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["stage"] == "cpd_like_expected_failure_synthetic_workbench"
    assert payload["status"] == "smoke_passed"
    assert payload["status_semantics"] == (
        "expected_limitations_reported_not_decomposition_success"
    )
    assert payload["cases"][0]["case_id"] == "restricted_primitive_vocabulary_gap"
    assert captured.err == ""


def test_cli_run_cpd_like_expected_failure_workbench_rejects_non_finite_json(
    capsys,
    monkeypatch,
):
    monkeypatch.setattr(
        cli,
        "build_cpd_like_expected_failure_synthetic_workbench_report",
        lambda: {
            "stage": "cpd_like_expected_failure_synthetic_workbench",
            "status": "smoke_passed",
            "bad": float("nan"),
        },
    )

    assert cli.main(["--run-cpd-like-expected-failure-workbench"]) == 2

    captured = capsys.readouterr()
    assert captured.out == ""
    assert (
        "cpd_like_expected_failure_workbench report contains non-finite JSON values"
        in captured.err
    )
    assert "Traceback" not in captured.err


def test_cli_run_cpd_like_expected_failure_workbench_returns_nonzero_for_partial(
    capsys,
    monkeypatch,
):
    monkeypatch.setattr(
        cli,
        "build_cpd_like_expected_failure_synthetic_workbench_report",
        lambda: {
            "stage": "cpd_like_expected_failure_synthetic_workbench",
            "status": "partial",
            "cases": [],
        },
    )

    assert cli.main(["--run-cpd-like-expected-failure-workbench"]) == 2

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["status"] == "partial"
    assert captured.err == ""


def test_cli_run_newton_native_fitting_comparison_emits_json_without_config(capsys):
    assert cli.main(["--run-newton-native-fitting-comparison"]) == 0

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["stage"] == "cpd_like_newton_native_fitting_comparison"
    assert payload["status"] == "smoke_passed"
    assert payload["cases"][0]["native"]["selected_primitive_kind"] == "cylinder"
    assert payload["cases"][0]["native"]["selection_policy"] == (
        "support_aware_min_weighted_volume_surrogate_v1"
    )
    assert payload["cases"][0]["native"]["candidate_audit"][0]["primitive_type"] == "cylinder"
    assert payload["cases"][0]["native"]["candidate_audit"][0]["selected"] is True
    assert payload["cases"][0]["comparison"]["native_selected_kind_cost_explained"] is True
    assert [asset["role"] for asset in payload["real_usd_scope"]["assets"]] == [
        "bed_dev_smoke",
        "franka_import_smoke",
    ]
    assert captured.err == ""


def test_cli_run_newton_native_fitting_comparison_rejects_non_finite_json(
    capsys,
    monkeypatch,
):
    monkeypatch.setattr(
        cli,
        "build_newton_native_fitting_comparison_report",
        lambda: {
            "stage": "cpd_like_newton_native_fitting_comparison",
            "status": "smoke_passed",
            "bad": float("nan"),
        },
    )

    assert cli.main(["--run-newton-native-fitting-comparison"]) == 2

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "newton_native_fitting_comparison report contains non-finite JSON values" in captured.err
    assert "Traceback" not in captured.err


def test_cli_run_newton_native_fitting_comparison_reads_config_subsets(tmp_path, capsys):
    config_path = tmp_path / "native_compare.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: native_compare",
                "  path: assets/manifests/cpd_like_smoke_assets.yaml",
                "task:",
                "  primary: native_primitive_fitting_comparison",
                "cpd_like:",
                "  legacy_primitive_subset:",
                "    - box",
                "    - sphere",
                "    - capsule",
                "    - cylinder",
                "  native_primitive_subset:",
                "    - box",
                "    - sphere",
                "    - capsule",
                "    - cylinder",
                "    - cone",
                "    - ellipsoid",
                "native_fitting_comparison:",
                "  claim_boundary: custom_native_boundary",
                "  evidence_level: custom_native_evidence",
            ]
        ),
        encoding="utf-8",
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-newton-native-fitting-comparison",
            ]
        )
        == 2
    )

    payload = json.loads(capsys.readouterr().out)
    cylindrical = {
        case["case_id"]: case for case in payload["cases"]
    }["cylindrical_rod"]
    assert payload["status"] == "partial"
    assert payload["claim_boundary"] == "custom_native_boundary"
    assert payload["evidence_level"] == "custom_native_evidence"
    assert payload["legacy_primitive_subset"] == ["box", "sphere", "capsule", "cylinder"]
    assert cylindrical["comparison"]["native_selected_newton_extension"] is False


def test_cli_run_real_usd_native_fitting_comparison_reads_roles_from_config(tmp_path, capsys):
    manifest_path = _write_two_mesh_manifest(tmp_path)
    config_path = _write_real_usd_native_config(tmp_path, manifest_path)

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-real-usd-native-fitting-comparison",
            ]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "cpd_like_real_usd_native_fitting_comparison"
    assert payload["status"] == "smoke_passed"
    assert [case["asset_role"] for case in payload["cases"]] == [
        "bed_dev_smoke",
        "franka_import_smoke",
    ]
    assert payload["cases"][0]["legacy"]["max_source_faces"] == 8
    assert payload["cases"][1]["native"]["max_source_faces"] == 4


def test_cli_run_real_usd_candidate_loss_diagnosis_emits_json(
    tmp_path,
    capsys,
    monkeypatch,
):
    manifest_path = _write_two_mesh_manifest(tmp_path)
    config_path = _write_real_usd_native_config(tmp_path, manifest_path)

    def fake_diagnosis_report(**kwargs):
        assert kwargs["roles"] == ("bed_dev_smoke", "franka_import_smoke")
        assert kwargs["max_source_faces_by_role"] == {
            "bed_dev_smoke": 8,
            "franka_import_smoke": 4,
        }
        return {
            "stage": "cpd_like_real_usd_candidate_loss_diagnosis",
            "status": "smoke_passed",
            "cases": [],
        }

    monkeypatch.setattr(
        cli,
        "build_real_usd_candidate_loss_diagnosis_report",
        fake_diagnosis_report,
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-real-usd-candidate-loss-diagnosis",
            ]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "cpd_like_real_usd_candidate_loss_diagnosis"
    assert payload["status"] == "smoke_passed"


def test_cli_run_cpd_like_near_miss_workbench_emits_json(capsys):
    assert cli.main(["--run-cpd-like-near-miss-workbench"]) == 0

    payload = json.loads(capsys.readouterr().out)

    assert payload["stage"] == "cpd_like_near_miss_fixture_workbench"
    assert payload["status"] == "smoke_passed"
    assert payload["cases"][0]["case_id"] == "cylinder_near_miss_cluster"
    assert payload["cases"][0]["best_extension_candidate"]["primitive_type"] == "cylinder"


def test_cli_run_cpd_like_cylinder_near_miss_fit_ablation_emits_json(capsys):
    assert cli.main(["--run-cpd-like-cylinder-near-miss-fit-ablation"]) == 0

    payload = json.loads(capsys.readouterr().out)

    assert payload["stage"] == "cpd_like_cylinder_near_miss_fit_ablation"
    assert payload["status"] == "smoke_passed"
    assert payload["cases"][0]["case_id"] == "cylinder_near_miss_cluster"
    assert payload["cases"][0]["ablation"]["lower_bound_volume_beats_selected"] is False
    assert payload["cases"][0]["decision"]["recommended_next_component"] == (
        "scoring_or_merge_search_not_radial_center_refinement"
    )


def test_cli_run_cpd_like_cylinder_near_miss_fit_ablation_returns_nonzero_for_partial(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        cli,
        "build_cpd_like_cylinder_near_miss_fit_ablation_report",
        lambda: {
            "stage": "cpd_like_cylinder_near_miss_fit_ablation",
            "status": "partial",
            "cases": [],
        },
    )

    assert cli.main(["--run-cpd-like-cylinder-near-miss-fit-ablation"]) == 2

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "partial"


def test_cli_run_cpd_like_cylinder_near_miss_scoring_sensitivity_emits_json(capsys):
    assert cli.main(["--run-cpd-like-cylinder-near-miss-scoring-sensitivity"]) == 0

    payload = json.loads(capsys.readouterr().out)

    assert payload["stage"] == "cpd_like_cylinder_near_miss_scoring_sensitivity"
    assert payload["status"] == "smoke_passed"
    assert payload["cases"][0]["case_id"] == "cylinder_near_miss_cluster"
    assert (
        0.0
        < payload["cases"][0]["scoring_sensitivity"]["extension_score_multiplier_to_tie"]
        < 1.0
    )
    assert payload["cases"][0]["decision"]["newton_task_comparison_triggered"] is False


def test_cli_run_cpd_like_cylinder_near_miss_scoring_sensitivity_returns_nonzero_for_partial(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        cli,
        "build_cpd_like_cylinder_near_miss_scoring_sensitivity_report",
        lambda: {
            "stage": "cpd_like_cylinder_near_miss_scoring_sensitivity",
            "status": "partial",
            "cases": [],
        },
    )

    assert cli.main(["--run-cpd-like-cylinder-near-miss-scoring-sensitivity"]) == 2

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "partial"


def test_cli_run_cpd_like_cylinder_near_miss_scoring_policy_ablation_emits_json(capsys):
    assert cli.main(["--run-cpd-like-cylinder-near-miss-scoring-policy-ablation"]) == 0

    payload = json.loads(capsys.readouterr().out)

    assert payload["stage"] == "cpd_like_cylinder_near_miss_scoring_policy_ablation"
    assert payload["status"] == "smoke_passed"
    cases = {case["case_id"]: case for case in payload["cases"]}
    assert set(cases) == {"cylinder_near_miss_cluster", "boxy_cuboid_guardrail"}
    assert cases["cylinder_near_miss_cluster"]["default_selected_primitive_type"] == "box"
    assert (
        cases["cylinder_near_miss_cluster"]["counterfactual_selected_primitive_type"]
        == "cylinder"
    )
    assert cases["boxy_cuboid_guardrail"]["default_selected_primitive_type"] == "box"
    assert cases["boxy_cuboid_guardrail"]["counterfactual_selected_primitive_type"] == "box"
    assert (
        cases["cylinder_near_miss_cluster"]["selection_policy_applied_to_default_pipeline"]
        is False
    )


def test_cli_run_cpd_like_cylinder_near_miss_scoring_policy_ablation_returns_nonzero_for_partial(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        cli,
        "build_cpd_like_cylinder_near_miss_scoring_policy_ablation_report",
        lambda: {
            "stage": "cpd_like_cylinder_near_miss_scoring_policy_ablation",
            "status": "partial",
            "cases": [],
        },
    )

    assert cli.main(["--run-cpd-like-cylinder-near-miss-scoring-policy-ablation"]) == 2

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "partial"


def test_cli_run_cpd_like_cylinder_scoring_policy_selection_probe_emits_json(capsys):
    assert cli.main(["--run-cpd-like-cylinder-scoring-policy-selection-probe"]) == 0

    payload = json.loads(capsys.readouterr().out)
    cases = {case["case_id"]: case for case in payload["cases"]}

    assert payload["stage"] == "cpd_like_cylinder_scoring_policy_selection_probe"
    assert payload["status"] == "smoke_passed"
    assert cases["cylinder_near_miss_cluster"]["default_selected_primitive_type"] == "box"
    assert cases["cylinder_near_miss_cluster"]["opt_in_selected_primitive_type"] == "cylinder"
    assert cases["boxy_cuboid_guardrail"]["default_selected_primitive_type"] == "box"
    assert cases["boxy_cuboid_guardrail"]["opt_in_selected_primitive_type"] == "box"


def test_cli_run_cpd_like_cylinder_scoring_policy_selection_probe_returns_nonzero_for_partial(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        cli,
        "build_cpd_like_cylinder_scoring_policy_selection_probe_report",
        lambda: {
            "stage": "cpd_like_cylinder_scoring_policy_selection_probe",
            "status": "partial",
            "cases": [],
        },
    )

    assert cli.main(["--run-cpd-like-cylinder-scoring-policy-selection-probe"]) == 2

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "partial"


def test_cli_run_cpd_like_cylinder_scoring_policy_package_probe_emits_json(capsys):
    assert cli.main(["--run-cpd-like-cylinder-scoring-policy-package-probe"]) == 0

    payload = json.loads(capsys.readouterr().out)
    cases = {case["case_id"]: case for case in payload["cases"]}

    assert payload["stage"] == "cpd_like_cylinder_scoring_policy_package_probe"
    assert payload["status"] == "smoke_passed"
    assert cases["cylinder_near_miss_cluster"]["default_package"]["primitive_kinds"] == ["box"]
    assert cases["cylinder_near_miss_cluster"]["opt_in_package"]["primitive_kinds"] == [
        "cylinder"
    ]
    assert cases["cylinder_near_miss_cluster"]["opt_in_package_mapping"]["fully_mapped"] is True


def test_cli_run_cpd_like_cylinder_scoring_policy_package_probe_returns_nonzero_for_partial(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        cli,
        "build_cpd_like_cylinder_scoring_policy_package_probe_report",
        lambda: {
            "stage": "cpd_like_cylinder_scoring_policy_package_probe",
            "status": "partial",
            "cases": [],
        },
    )

    assert cli.main(["--run-cpd-like-cylinder-scoring-policy-package-probe"]) == 2

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "partial"


def test_cli_run_cpd_like_controlled_merge_search_package_probe_emits_json(capsys):
    assert cli.main(["--run-cpd-like-controlled-merge-search-package-probe"]) == 0

    payload = json.loads(capsys.readouterr().out)
    cases = {case["case_id"]: case for case in payload["cases"]}

    assert payload["stage"] == "cpd_like_controlled_merge_search_package_probe"
    assert payload["status"] == "smoke_passed"
    assert cases["cost_guided_pair_choice"]["opt_in_package_changed"] is True
    assert cases["cost_guided_pair_choice"]["opt_in_package_mapping"]["fully_mapped"] is True


def test_cli_run_cpd_like_controlled_merge_search_package_probe_returns_nonzero_for_partial(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        cli,
        "build_cpd_like_controlled_merge_search_package_probe_report",
        lambda: {
            "stage": "cpd_like_controlled_merge_search_package_probe",
            "status": "partial",
            "cases": [],
        },
    )

    assert cli.main(["--run-cpd-like-controlled-merge-search-package-probe"]) == 2

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "partial"


def test_cli_run_cpd_like_controlled_merge_search_package_probe_rejects_nonfinite_json(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        cli,
        "build_cpd_like_controlled_merge_search_package_probe_report",
        lambda: {
            "stage": "cpd_like_controlled_merge_search_package_probe",
            "status": "smoke_passed",
            "nonfinite": float("nan"),
        },
    )

    assert cli.main(["--run-cpd-like-controlled-merge-search-package-probe"]) == 2

    stderr = capsys.readouterr().err
    assert "contains non-finite JSON values" in stderr


def test_cli_run_cpd_like_cost_guided_lookahead_merge_report_emits_json(capsys):
    assert cli.main(["--run-cpd-like-cost-guided-lookahead-merge-report"]) == 0

    payload = json.loads(capsys.readouterr().out)
    case = payload["cases"][0]

    assert payload["stage"] == "cpd_like_cost_guided_lookahead_merge_report"
    assert payload["status"] == "smoke_passed"
    assert case["case_id"] == "lookahead_merge_trap"
    assert case["decision"]["lookahead_decision_changed"] is True
    assert case["decision"]["newton_task_comparison_triggered"] is False


def test_cli_run_cpd_like_cost_guided_lookahead_merge_report_rejects_nonfinite_json(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        cli,
        "build_cpd_like_cost_guided_lookahead_merge_report",
        lambda: {
            "stage": "cpd_like_cost_guided_lookahead_merge_report",
            "status": "smoke_passed",
            "nonfinite": float("nan"),
        },
    )

    assert cli.main(["--run-cpd-like-cost-guided-lookahead-merge-report"]) == 2

    stderr = capsys.readouterr().err
    assert "cpd_like_cost_guided_lookahead_merge_report" in stderr
    assert "contains non-finite JSON values" in stderr


def test_cli_run_cpd_paper_offline_report_emits_json(capsys):
    assert cli.main(["--run-cpd-paper-offline-report"]) == 0

    captured = capsys.readouterr()
    assert captured.err == ""
    payload = json.loads(captured.out)

    assert payload["stage"] == "cpd_paper_offline_report"
    assert payload["status"] == "partial"
    assert payload["report_generation_status"] == "smoke_passed"
    assert payload["paper_faithfulness"]["status"] == "partial"
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
    assert [case["case_id"] for case in payload["cases"]] == [
        "paper_single_box",
        "paper_two_face_merge",
        "paper_three_face_chain",
        "paper_disconnected_components",
        "paper_frustum_like",
        "paper_trapezoid_prism_like",
    ]


def test_cli_run_cpd_paper_offline_report_rejects_nonfinite_json(monkeypatch, capsys):
    monkeypatch.setattr(
        cli,
        "build_cpd_paper_offline_report",
        lambda: {
            "stage": "cpd_paper_offline_report",
            "status": "smoke_passed",
            "nonfinite": float("nan"),
        },
    )

    assert cli.main(["--run-cpd-paper-offline-report"]) == 2

    captured = capsys.readouterr()
    assert captured.out == ""
    stderr = captured.err
    assert "cpd_paper_offline_report" in stderr
    assert "contains non-finite JSON values" in stderr


def test_cli_run_cpd_like_cost_guided_lookahead_package_probe_emits_json(capsys):
    assert cli.main(["--run-cpd-like-cost-guided-lookahead-package-probe"]) == 0

    payload = json.loads(capsys.readouterr().out)
    case = payload["cases"][0]

    assert payload["stage"] == "cpd_like_cost_guided_lookahead_package_probe"
    assert payload["status"] == "smoke_passed"
    assert case["case_id"] == "lookahead_merge_trap"
    assert case["package_pair_changed"] is True
    assert case["lookahead_package_mapping"]["fully_mapped"] is True
    assert case["decision"]["newton_task_comparison_triggered"] is False


def test_cli_run_cpd_like_cost_guided_lookahead_package_probe_returns_nonzero_for_partial(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        cli,
        "build_cpd_like_cost_guided_lookahead_package_probe_report",
        lambda: {
            "stage": "cpd_like_cost_guided_lookahead_package_probe",
            "status": "partial",
            "cases": [],
        },
    )

    assert cli.main(["--run-cpd-like-cost-guided-lookahead-package-probe"]) == 2

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "partial"


def test_cli_run_cpd_like_cost_guided_lookahead_package_probe_rejects_nonfinite_json(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        cli,
        "build_cpd_like_cost_guided_lookahead_package_probe_report",
        lambda: {
            "stage": "cpd_like_cost_guided_lookahead_package_probe",
            "status": "smoke_passed",
            "nonfinite": float("nan"),
        },
    )

    assert cli.main(["--run-cpd-like-cost-guided-lookahead-package-probe"]) == 2

    stderr = capsys.readouterr().err
    assert "cpd_like_cost_guided_lookahead_package_probe" in stderr
    assert "contains non-finite JSON values" in stderr


def test_cli_run_cpd_like_cost_guided_lookahead_newton_probe_requires_config(capsys):
    assert cli.main(["--run-cpd-like-cost-guided-lookahead-newton-probe"]) == 2

    assert (
        "--run-cpd-like-cost-guided-lookahead-newton-probe requires --config"
        in capsys.readouterr().err
    )


def test_cli_run_cpd_like_cost_guided_lookahead_newton_probe_requires_source_dir(
    tmp_path,
    capsys,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  path: synthetic://lookahead_merge_trap",
                "task:",
                "  primary: synthetic_cost_guided_lookahead_newton_probe",
                "compile:",
                "  verify:",
                "    - cpd_like_cost_guided_lookahead_newton_probe",
            ]
        ),
        encoding="utf-8",
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-cpd-like-cost-guided-lookahead-newton-probe",
            ]
        )
        == 2
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "dependency_gap"
    assert "newton.source_dir" in payload["fallback_reason"]


def test_cli_run_cpd_like_cost_guided_lookahead_newton_probe_rejects_wrong_fixture(
    tmp_path,
    capsys,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  path: synthetic://cost_guided_pair_choice",
                "task:",
                "  primary: synthetic_cost_guided_lookahead_newton_probe",
                "compile:",
                "  verify:",
                "    - cpd_like_cost_guided_lookahead_newton_probe",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
            ]
        ),
        encoding="utf-8",
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-cpd-like-cost-guided-lookahead-newton-probe",
            ]
        )
        == 2
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "config_error"
    assert "synthetic://lookahead_merge_trap" in payload["fallback_reason"]


def test_cli_run_cpd_like_cost_guided_lookahead_newton_probe_rejects_wrong_task(
    tmp_path,
    capsys,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  path: synthetic://lookahead_merge_trap",
                "task:",
                "  primary: synthetic_controlled_merge_search_newton_probe",
                "compile:",
                "  verify:",
                "    - cpd_like_cost_guided_lookahead_newton_probe",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
            ]
        ),
        encoding="utf-8",
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-cpd-like-cost-guided-lookahead-newton-probe",
            ]
        )
        == 2
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "config_error"
    assert "synthetic_cost_guided_lookahead_newton_probe" in payload["fallback_reason"]


def test_cli_run_cpd_like_cost_guided_lookahead_newton_probe_rejects_missing_verify(
    tmp_path,
    capsys,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  path: synthetic://lookahead_merge_trap",
                "task:",
                "  primary: synthetic_cost_guided_lookahead_newton_probe",
                "compile:",
                "  verify:",
                "    - cpd_like_cost_guided_lookahead_package_probe",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
            ]
        ),
        encoding="utf-8",
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-cpd-like-cost-guided-lookahead-newton-probe",
            ]
        )
        == 2
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "config_error"
    assert "compile.verify" in payload["fallback_reason"]


def test_cli_run_cpd_like_cost_guided_lookahead_newton_probe_emits_json(
    tmp_path,
    capsys,
    monkeypatch,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: cost_guided_lookahead_newton_probe",
                "  path: synthetic://lookahead_merge_trap",
                "task:",
                "  primary: synthetic_cost_guided_lookahead_newton_probe",
                "compile:",
                "  verify:",
                "    - cpd_like_cost_guided_lookahead_newton_probe",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
                "newton_diagnostic:",
                "  device: cpu",
                "  synthetic_newton_probe_claim_boundary: custom_probe_boundary",
                "  contact_claim_boundary: custom_contact_boundary",
                "  claim_boundary: custom_task_boundary",
                "  drop_settle:",
                "    frames: 12",
                "  sphere_rain:",
                "    sphere_count_x: 2",
            ]
        ),
        encoding="utf-8",
    )

    def fake_report(**kwargs):
        assert kwargs["source_dir"] == str(tmp_path / "newton")
        assert kwargs["device"] == "cpu"
        assert kwargs["drop_settle_options"].frames == 12
        assert kwargs["sphere_rain_options"].sphere_count_x == 2
        assert kwargs["claim_boundary"] == "custom_probe_boundary"
        assert kwargs["contact_claim_boundary"] == "custom_contact_boundary"
        assert kwargs["task_claim_boundary"] == "custom_task_boundary"
        return {
            "stage": "cpd_like_cost_guided_lookahead_newton_probe",
            "status": "smoke_passed",
            "cases": [],
        }

    monkeypatch.setattr(
        cli,
        "build_cpd_like_cost_guided_lookahead_newton_probe_report",
        fake_report,
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-cpd-like-cost-guided-lookahead-newton-probe",
            ]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "cpd_like_cost_guided_lookahead_newton_probe"
    assert payload["status"] == "smoke_passed"


def test_cli_run_cpd_like_cost_guided_lookahead_newton_probe_rejects_nonfinite_json(
    tmp_path,
    capsys,
    monkeypatch,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  path: synthetic://lookahead_merge_trap",
                "task:",
                "  primary: synthetic_cost_guided_lookahead_newton_probe",
                "compile:",
                "  verify:",
                "    - cpd_like_cost_guided_lookahead_newton_probe",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        cli,
        "build_cpd_like_cost_guided_lookahead_newton_probe_report",
        lambda **kwargs: {
            "stage": "cpd_like_cost_guided_lookahead_newton_probe",
            "status": "smoke_passed",
            "nonfinite": float("nan"),
        },
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-cpd-like-cost-guided-lookahead-newton-probe",
            ]
        )
        == 2
    )

    assert "contains non-finite JSON values" in capsys.readouterr().err


def test_cli_run_cpd_like_cost_guided_lookahead_newton_probe_returns_nonzero_for_partial(
    tmp_path,
    capsys,
    monkeypatch,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  path: synthetic://lookahead_merge_trap",
                "task:",
                "  primary: synthetic_cost_guided_lookahead_newton_probe",
                "compile:",
                "  verify:",
                "    - cpd_like_cost_guided_lookahead_newton_probe",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        cli,
        "build_cpd_like_cost_guided_lookahead_newton_probe_report",
        lambda **kwargs: {
            "stage": "cpd_like_cost_guided_lookahead_newton_probe",
            "status": "partial",
            "cases": [],
        },
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-cpd-like-cost-guided-lookahead-newton-probe",
            ]
        )
        == 2
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "partial"


def test_cli_run_cpd_like_four_block_slice_report_emits_json(capsys):
    assert cli.main(["--run-cpd-like-four-block-slice-report"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "cpd_like_four_block_slice_report"
    assert payload["status"] == "smoke_passed"
    assert payload["slice_id"] == "cost_guided_lookahead"
    assert "greedy_contact" not in json.dumps(payload)


def test_cli_run_cpd_like_four_block_slice_report_does_not_call_runtime_helpers(
    monkeypatch,
    capsys,
):
    def unexpected_call(*args, **kwargs):
        raise AssertionError("four-block CLI must only emit the record-map report")

    for helper_name in (
        "decompose_mesh",
        "load_first_mesh",
        "package_from_cpd_like_report",
        "run_newton_contact_smoke",
        "run_newton_drop_settle",
        "run_newton_sphere_rain",
        "build_cpd_like_cost_guided_lookahead_merge_report",
        "build_cpd_like_cost_guided_lookahead_package_probe_report",
        "build_cpd_like_cost_guided_lookahead_newton_probe_report",
    ):
        monkeypatch.setattr(cli, helper_name, unexpected_call)

    assert cli.main(["--run-cpd-like-four-block-slice-report"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "cpd_like_four_block_slice_report"
    assert payload["status"] == "smoke_passed"


def test_cli_run_cpd_like_four_block_slice_report_returns_nonzero_for_partial(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        cli,
        "build_cpd_like_four_block_slice_report",
        lambda: {
            "stage": "cpd_like_four_block_slice_report",
            "status": "partial",
            "slice_id": "cost_guided_lookahead",
        },
    )

    assert cli.main(["--run-cpd-like-four-block-slice-report"]) == 2

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "partial"


def test_cli_run_cpd_like_four_block_slice_report_rejects_nonfinite_json(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        cli,
        "build_cpd_like_four_block_slice_report",
        lambda: {
            "stage": "cpd_like_four_block_slice_report",
            "status": "smoke_passed",
            "nonfinite": float("nan"),
        },
    )

    assert cli.main(["--run-cpd-like-four-block-slice-report"]) == 2

    stderr = capsys.readouterr().err
    assert "cpd_like_four_block_slice_report" in stderr
    assert "contains non-finite JSON values" in stderr


def test_cli_run_cpd_like_cylinder_scoring_policy_newton_probe_requires_config(capsys):
    assert cli.main(["--run-cpd-like-cylinder-scoring-policy-newton-probe"]) == 2

    assert (
        "--run-cpd-like-cylinder-scoring-policy-newton-probe requires --config"
        in capsys.readouterr().err
    )


def test_cli_run_cpd_like_cylinder_scoring_policy_newton_probe_requires_source_dir(
    tmp_path,
    capsys,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  path: synthetic://cylinder_near_miss_cluster",
                "task:",
                "  primary: synthetic_cylinder_scoring_policy_newton_probe",
                "compile:",
                "  verify:",
                "    - cpd_like_cylinder_scoring_policy_newton_probe",
            ]
        ),
        encoding="utf-8",
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-cpd-like-cylinder-scoring-policy-newton-probe",
            ]
        )
        == 2
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "dependency_gap"
    assert "newton.source_dir" in payload["fallback_reason"]


def test_cli_run_cpd_like_cylinder_scoring_policy_newton_probe_rejects_wrong_fixture(
    tmp_path,
    capsys,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  path: assets/bed.usd",
                "task:",
                "  primary: real_usd_native_task_comparison",
                "compile:",
                "  verify:",
                "    - newton_real_usd_native_task_comparison",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
            ]
        ),
        encoding="utf-8",
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-cpd-like-cylinder-scoring-policy-newton-probe",
            ]
        )
        == 2
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "config_error"
    assert "synthetic://cylinder_near_miss_cluster" in payload["fallback_reason"]


def test_cli_run_cpd_like_cylinder_scoring_policy_newton_probe_rejects_wrong_task(
    tmp_path,
    capsys,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  path: synthetic://cylinder_near_miss_cluster",
                "task:",
                "  primary: real_usd_native_task_comparison",
                "compile:",
                "  verify:",
                "    - cpd_like_cylinder_scoring_policy_newton_probe",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
            ]
        ),
        encoding="utf-8",
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-cpd-like-cylinder-scoring-policy-newton-probe",
            ]
        )
        == 2
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "config_error"
    assert "synthetic_cylinder_scoring_policy_newton_probe" in payload["fallback_reason"]


def test_cli_run_cpd_like_cylinder_scoring_policy_newton_probe_rejects_missing_verify(
    tmp_path,
    capsys,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  path: synthetic://cylinder_near_miss_cluster",
                "task:",
                "  primary: synthetic_cylinder_scoring_policy_newton_probe",
                "compile:",
                "  verify:",
                "    - newton_real_usd_native_task_comparison",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
            ]
        ),
        encoding="utf-8",
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-cpd-like-cylinder-scoring-policy-newton-probe",
            ]
        )
        == 2
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "config_error"
    assert "compile.verify" in payload["fallback_reason"]


def test_cli_run_cpd_like_cylinder_scoring_policy_newton_probe_emits_json(
    tmp_path,
    capsys,
    monkeypatch,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: synthetic_newton_probe",
                "  path: synthetic://cylinder_near_miss_cluster",
                "task:",
                "  primary: synthetic_cylinder_scoring_policy_newton_probe",
                "compile:",
                "  verify:",
                "    - cpd_like_cylinder_scoring_policy_newton_probe",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
                "newton_diagnostic:",
                "  device: cpu",
                "  synthetic_newton_probe_claim_boundary: custom_synthetic_probe_boundary",
                "  contact_claim_boundary: custom_contact_boundary",
                "  claim_boundary: custom_task_boundary",
                "  drop_settle:",
                "    frames: 12",
                "  sphere_rain:",
                "    sphere_count_x: 2",
            ]
        ),
        encoding="utf-8",
    )

    def fake_report(**kwargs):
        assert kwargs["source_dir"] == str(tmp_path / "newton")
        assert kwargs["device"] == "cpu"
        assert kwargs["drop_settle_options"].frames == 12
        assert kwargs["sphere_rain_options"].sphere_count_x == 2
        assert kwargs["claim_boundary"] == "custom_synthetic_probe_boundary"
        assert kwargs["contact_claim_boundary"] == "custom_contact_boundary"
        assert kwargs["task_claim_boundary"] == "custom_task_boundary"
        return {
            "stage": "cpd_like_cylinder_scoring_policy_newton_probe",
            "status": "smoke_passed",
            "cases": [],
        }

    monkeypatch.setattr(
        cli,
        "build_cpd_like_cylinder_scoring_policy_newton_probe_report",
        fake_report,
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-cpd-like-cylinder-scoring-policy-newton-probe",
            ]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "cpd_like_cylinder_scoring_policy_newton_probe"
    assert payload["status"] == "smoke_passed"


def test_cli_run_cpd_like_cylinder_scoring_policy_newton_probe_returns_nonzero_for_partial(
    tmp_path,
    capsys,
    monkeypatch,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  path: synthetic://cylinder_near_miss_cluster",
                "task:",
                "  primary: synthetic_cylinder_scoring_policy_newton_probe",
                "compile:",
                "  verify:",
                "    - cpd_like_cylinder_scoring_policy_newton_probe",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        cli,
        "build_cpd_like_cylinder_scoring_policy_newton_probe_report",
        lambda **kwargs: {
            "stage": "cpd_like_cylinder_scoring_policy_newton_probe",
            "status": "partial",
            "cases": [],
        },
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-cpd-like-cylinder-scoring-policy-newton-probe",
            ]
        )
        == 2
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "partial"


def test_cli_run_cpd_like_controlled_merge_search_newton_probe_requires_config(capsys):
    assert cli.main(["--run-cpd-like-controlled-merge-search-newton-probe"]) == 2

    assert (
        "--run-cpd-like-controlled-merge-search-newton-probe requires --config"
        in capsys.readouterr().err
    )


def test_cli_run_cpd_like_controlled_merge_search_newton_probe_requires_source_dir(
    tmp_path,
    capsys,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  path: synthetic://cost_guided_pair_choice",
                "task:",
                "  primary: synthetic_controlled_merge_search_newton_probe",
                "compile:",
                "  verify:",
                "    - cpd_like_controlled_merge_search_newton_probe",
            ]
        ),
        encoding="utf-8",
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-cpd-like-controlled-merge-search-newton-probe",
            ]
        )
        == 2
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "dependency_gap"
    assert "newton.source_dir" in payload["fallback_reason"]


def test_cli_run_cpd_like_controlled_merge_search_newton_probe_rejects_wrong_fixture(
    tmp_path,
    capsys,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  path: assets/bed.usd",
                "task:",
                "  primary: synthetic_controlled_merge_search_newton_probe",
                "compile:",
                "  verify:",
                "    - cpd_like_controlled_merge_search_newton_probe",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
            ]
        ),
        encoding="utf-8",
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-cpd-like-controlled-merge-search-newton-probe",
            ]
        )
        == 2
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "config_error"
    assert "synthetic://cost_guided_pair_choice" in payload["fallback_reason"]


def test_cli_run_cpd_like_controlled_merge_search_newton_probe_rejects_wrong_task(
    tmp_path,
    capsys,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  path: synthetic://cost_guided_pair_choice",
                "task:",
                "  primary: synthetic_cylinder_scoring_policy_newton_probe",
                "compile:",
                "  verify:",
                "    - cpd_like_controlled_merge_search_newton_probe",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
            ]
        ),
        encoding="utf-8",
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-cpd-like-controlled-merge-search-newton-probe",
            ]
        )
        == 2
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "config_error"
    assert "synthetic_controlled_merge_search_newton_probe" in payload["fallback_reason"]


def test_cli_run_cpd_like_controlled_merge_search_newton_probe_rejects_missing_verify(
    tmp_path,
    capsys,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  path: synthetic://cost_guided_pair_choice",
                "task:",
                "  primary: synthetic_controlled_merge_search_newton_probe",
                "compile:",
                "  verify:",
                "    - cpd_like_controlled_merge_search_package_probe",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
            ]
        ),
        encoding="utf-8",
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-cpd-like-controlled-merge-search-newton-probe",
            ]
        )
        == 2
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "config_error"
    assert "compile.verify" in payload["fallback_reason"]


def test_cli_run_cpd_like_controlled_merge_search_newton_probe_emits_json(
    tmp_path,
    capsys,
    monkeypatch,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: controlled_merge_search_newton_probe",
                "  path: synthetic://cost_guided_pair_choice",
                "task:",
                "  primary: synthetic_controlled_merge_search_newton_probe",
                "compile:",
                "  verify:",
                "    - cpd_like_controlled_merge_search_newton_probe",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
                "newton_diagnostic:",
                "  device: cpu",
                "  synthetic_newton_probe_claim_boundary: custom_probe_boundary",
                "  contact_claim_boundary: custom_contact_boundary",
                "  claim_boundary: custom_task_boundary",
                "  drop_settle:",
                "    frames: 12",
                "  sphere_rain:",
                "    sphere_count_x: 2",
            ]
        ),
        encoding="utf-8",
    )

    def fake_report(**kwargs):
        assert kwargs["source_dir"] == str(tmp_path / "newton")
        assert kwargs["device"] == "cpu"
        assert kwargs["drop_settle_options"].frames == 12
        assert kwargs["sphere_rain_options"].sphere_count_x == 2
        assert kwargs["claim_boundary"] == "custom_probe_boundary"
        assert kwargs["contact_claim_boundary"] == "custom_contact_boundary"
        assert kwargs["task_claim_boundary"] == "custom_task_boundary"
        return {
            "stage": "cpd_like_controlled_merge_search_newton_probe",
            "status": "smoke_passed",
            "cases": [],
        }

    monkeypatch.setattr(
        cli,
        "build_cpd_like_controlled_merge_search_newton_probe_report",
        fake_report,
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-cpd-like-controlled-merge-search-newton-probe",
            ]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "cpd_like_controlled_merge_search_newton_probe"
    assert payload["status"] == "smoke_passed"


def test_cli_run_cpd_like_controlled_merge_search_newton_probe_rejects_nonfinite_json(
    tmp_path,
    capsys,
    monkeypatch,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  path: synthetic://cost_guided_pair_choice",
                "task:",
                "  primary: synthetic_controlled_merge_search_newton_probe",
                "compile:",
                "  verify:",
                "    - cpd_like_controlled_merge_search_newton_probe",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        cli,
        "build_cpd_like_controlled_merge_search_newton_probe_report",
        lambda **kwargs: {
            "stage": "cpd_like_controlled_merge_search_newton_probe",
            "status": "smoke_passed",
            "nonfinite": float("nan"),
        },
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-cpd-like-controlled-merge-search-newton-probe",
            ]
        )
        == 2
    )

    assert "contains non-finite JSON values" in capsys.readouterr().err


def test_cli_run_cpd_like_controlled_merge_search_newton_probe_returns_nonzero_for_partial(
    tmp_path,
    capsys,
    monkeypatch,
):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  path: synthetic://cost_guided_pair_choice",
                "task:",
                "  primary: synthetic_controlled_merge_search_newton_probe",
                "compile:",
                "  verify:",
                "    - cpd_like_controlled_merge_search_newton_probe",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        cli,
        "build_cpd_like_controlled_merge_search_newton_probe_report",
        lambda **kwargs: {
            "stage": "cpd_like_controlled_merge_search_newton_probe",
            "status": "partial",
            "cases": [],
        },
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-cpd-like-controlled-merge-search-newton-probe",
            ]
        )
        == 2
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "partial"


def test_cli_run_real_usd_candidate_loss_diagnosis_reads_custom_metadata(
    tmp_path,
    capsys,
    monkeypatch,
):
    manifest_path = _write_two_mesh_manifest(tmp_path)
    config_path = _write_real_usd_native_config(tmp_path, manifest_path)
    config_data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    config_data["candidate_loss_diagnosis"] = {
        "objective_version": "candidate_loss_test_v1",
        "claim_boundary": "custom_candidate_loss_boundary",
        "evidence_level": "custom_candidate_loss_evidence",
    }
    config_path.write_text(yaml.safe_dump(config_data), encoding="utf-8")

    def fake_diagnosis_report(**kwargs):
        options = kwargs["objective_options"]
        return {
            "stage": "cpd_like_real_usd_candidate_loss_diagnosis",
            "status": "smoke_passed",
            "objective_version": options.objective_version,
            "claim_boundary": options.claim_boundary,
            "evidence_level": options.evidence_level,
            "cases": [],
        }

    monkeypatch.setattr(
        cli,
        "build_real_usd_candidate_loss_diagnosis_report",
        fake_diagnosis_report,
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-real-usd-candidate-loss-diagnosis",
            ]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["objective_version"] == "candidate_loss_test_v1"
    assert payload["claim_boundary"] == "custom_candidate_loss_boundary"
    assert payload["evidence_level"] == "custom_candidate_loss_evidence"


def test_cli_run_real_usd_candidate_loss_diagnosis_rejects_non_finite_json(
    tmp_path,
    capsys,
    monkeypatch,
):
    manifest_path = _write_two_mesh_manifest(tmp_path)
    config_path = _write_real_usd_native_config(tmp_path, manifest_path)
    monkeypatch.setattr(
        cli,
        "build_real_usd_candidate_loss_diagnosis_report",
        lambda **kwargs: {
            "stage": "cpd_like_real_usd_candidate_loss_diagnosis",
            "status": "smoke_passed",
            "bad": float("nan"),
        },
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-real-usd-candidate-loss-diagnosis",
            ]
        )
        == 2
    )

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "real_usd_candidate_loss_diagnosis report contains non-finite JSON values" in captured.err
    assert "Traceback" not in captured.err


def test_cli_run_real_usd_native_fitting_comparison_rejects_non_finite_json(
    tmp_path,
    capsys,
    monkeypatch,
):
    config_path = _write_real_usd_native_config(tmp_path, _write_two_mesh_manifest(tmp_path))
    monkeypatch.setattr(
        cli,
        "build_real_usd_native_fitting_comparison_report",
        lambda **kwargs: {
            "stage": "cpd_like_real_usd_native_fitting_comparison",
            "status": "smoke_passed",
            "bad": float("nan"),
        },
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-real-usd-native-fitting-comparison",
            ]
        )
        == 2
    )

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "real_usd_native_fitting_comparison report contains non-finite JSON values" in captured.err
    assert "Traceback" not in captured.err


def test_cli_run_real_usd_native_contact_comparison_requires_config(capsys):
    assert cli.main(["--run-real-usd-native-contact-comparison"]) == 2

    assert "--run-real-usd-native-contact-comparison requires --config" in capsys.readouterr().err


def test_cli_run_real_usd_native_contact_comparison_emits_json(
    tmp_path,
    capsys,
    monkeypatch,
):
    config_path = _write_real_usd_native_config(tmp_path, _write_two_mesh_manifest(tmp_path))

    def fake_contact_report(**kwargs):
        assert kwargs["source_dir"] == str(tmp_path / "newton")
        assert kwargs["device"] == "cpu"
        return {
            "stage": "newton_real_usd_native_contact_comparison",
            "status": "dependency_gap",
            "cases": [],
        }

    monkeypatch.setattr(cli, "build_real_usd_native_contact_comparison_report", fake_contact_report)

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-real-usd-native-contact-comparison",
            ]
        )
        == 2
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "newton_real_usd_native_contact_comparison"
    assert payload["status"] == "dependency_gap"


def test_cli_run_real_usd_native_task_comparison_gates_tasks(
    tmp_path,
    capsys,
    monkeypatch,
):
    config_path = _write_real_usd_native_config(tmp_path, _write_two_mesh_manifest(tmp_path))

    def fake_task_report(**kwargs):
        assert kwargs["drop_settle_options"].frames == 12
        assert kwargs["sphere_rain_options"].sphere_count_x == 2
        return {
            "stage": "newton_real_usd_native_task_comparison",
            "status": "smoke_passed",
            "cases": [],
        }

    monkeypatch.setattr(cli, "build_real_usd_native_task_comparison_report", fake_task_report)

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-real-usd-native-task-comparison",
            ]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "newton_real_usd_native_task_comparison"
    assert payload["status"] == "smoke_passed"


def test_cli_run_real_usd_native_contact_comparison_passes_custom_claim_boundary(
    tmp_path,
    capsys,
    monkeypatch,
):
    config_path = _write_real_usd_native_config(tmp_path, _write_two_mesh_manifest(tmp_path))

    def fake_contact_report(**kwargs):
        assert kwargs["claim_boundary"] == "custom_contact_boundary"
        return {
            "stage": "newton_real_usd_native_contact_comparison",
            "status": "smoke_passed",
            "cases": [],
        }

    monkeypatch.setattr(cli, "build_real_usd_native_contact_comparison_report", fake_contact_report)

    config_data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    config_data["newton_diagnostic"]["claim_boundary"] = "custom_contact_boundary"
    config_path.write_text(
        yaml.safe_dump(config_data),
        encoding="utf-8",
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-real-usd-native-contact-comparison",
            ]
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out)["status"] == "smoke_passed"


def test_cli_run_real_usd_native_task_comparison_passes_custom_claim_boundary(
    tmp_path,
    capsys,
    monkeypatch,
):
    config_path = _write_real_usd_native_config(tmp_path, _write_two_mesh_manifest(tmp_path))

    def fake_task_report(**kwargs):
        assert kwargs["claim_boundary"] == "custom_task_boundary"
        assert kwargs["contact_claim_boundary"] == "custom_task_boundary"
        return {
            "stage": "newton_real_usd_native_task_comparison",
            "status": "smoke_passed",
            "cases": [],
        }

    monkeypatch.setattr(cli, "build_real_usd_native_task_comparison_report", fake_task_report)

    config_data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    config_data["newton_diagnostic"]["claim_boundary"] = "custom_task_boundary"
    config_path.write_text(
        yaml.safe_dump(config_data),
        encoding="utf-8",
    )

    assert (
        cli.main(
            [
                "--config",
                str(config_path),
                "--run-real-usd-native-task-comparison",
            ]
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out)["status"] == "smoke_passed"


def test_cli_run_newton_contact_smoke_emits_report_for_tiny_usd(tmp_path, capsys):
    Usd = pytest.importorskip("pxr.Usd")
    UsdGeom = pytest.importorskip("pxr.UsdGeom")
    asset_path = tmp_path / "quad.usda"
    stage = Usd.Stage.CreateNew(str(asset_path))
    mesh = UsdGeom.Mesh.Define(stage, "/Quad")
    mesh.CreatePointsAttr([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
    mesh.CreateFaceVertexCountsAttr([4])
    mesh.CreateFaceVertexIndicesAttr([0, 1, 2, 3])
    stage.GetRootLayer().Save()
    source_dir = tmp_path / "newton-source"
    source_dir.mkdir()
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
                "    - newton_contact_smoke",
                "cpd_like:",
                "  primitive_subset:",
                "    - box",
                "    - sphere",
                "    - capsule",
                "  max_source_faces: 8",
                "newton:",
                f"  source_dir: {source_dir}",
                "newton_diagnostic:",
                "  probe_type: contact_canary",
                "  device: cpu",
            ]
        ),
        encoding="utf-8",
    )

    exit_code = cli.main(["--config", str(config_path), "--run-newton-contact-smoke"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code in {0, 2}
    assert payload["stage"] == "newton_contact_smoke"
    assert payload["asset_id"] == "tiny_quad"
    assert payload["package_id"] == "tiny_quad:cpd_like_face_merge"
    assert payload["probe_type"] == "contact_canary"
    assert payload["status"] in {"smoke_passed", "dependency_gap", "mapping_gap", "runtime_failure"}
    assert payload["primitive_count"] == 1
    assert payload["claim_boundary"] == "contact_canary_only_not_collision_quality"


def test_cli_run_newton_contact_smoke_keeps_stdout_json_only(tmp_path, capsys, monkeypatch):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: noisy_asset",
                "  path: assets/example.usda",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
                "newton_diagnostic:",
                "  probe_type: contact_canary",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        cli,
        "_run_cpd_like_report",
        lambda config: (object(), "assets/example.usda", 8),
    )
    monkeypatch.setattr(
        cli,
        "package_from_cpd_like_report",
        lambda *args, **kwargs: CollisionPackage("noisy_asset"),
    )

    def noisy_contact_smoke(*args, **kwargs):
        print("Warp 1.13.0 initialized:")
        return NewtonDiagnosticReport(
            stage="newton_contact_smoke",
            status="smoke_passed",
            asset_id="noisy_asset",
            package_id="noisy_asset:pkg",
            probe_type="contact_canary",
            device="cpu",
            environment=None,
            primitive_count=0,
            type_counts={},
            shape_mappings=(),
            contact_canaries=(),
            claim_boundary="contact_canary_only_not_collision_quality",
        )

    monkeypatch.setattr(cli, "run_newton_contact_smoke", noisy_contact_smoke)

    assert cli.main(["--config", str(config_path), "--run-newton-contact-smoke"]) == 0

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["stage"] == "newton_contact_smoke"
    assert captured.out.startswith("{")
    assert "Warp 1.13.0 initialized:" in captured.err


def test_cli_run_newton_drop_settle_emits_report_for_tiny_usd(tmp_path, capsys):
    Usd = pytest.importorskip("pxr.Usd")
    UsdGeom = pytest.importorskip("pxr.UsdGeom")
    asset_path = tmp_path / "quad.usda"
    stage = Usd.Stage.CreateNew(str(asset_path))
    mesh = UsdGeom.Mesh.Define(stage, "/Quad")
    mesh.CreatePointsAttr([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
    mesh.CreateFaceVertexCountsAttr([4])
    mesh.CreateFaceVertexIndicesAttr([0, 1, 2, 3])
    stage.GetRootLayer().Save()
    source_dir = tmp_path / "newton-source"
    source_dir.mkdir()
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
                "    - newton_drop_settle",
                "cpd_like:",
                "  primitive_subset:",
                "    - box",
                "    - sphere",
                "    - capsule",
                "  max_source_faces: 8",
                "newton:",
                f"  source_dir: {source_dir}",
                "newton_diagnostic:",
                "  probe_type: drop_settle",
                "  device: cpu",
            ]
        ),
        encoding="utf-8",
    )

    exit_code = cli.main(["--config", str(config_path), "--run-newton-drop-settle"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code in {0, 2}
    assert payload["stage"] == "newton_drop_settle"
    assert payload["asset_id"] == "tiny_quad"
    assert payload["package_id"] == "tiny_quad:cpd_like_face_merge"
    assert payload["probe_type"] == "drop_settle"
    assert payload["status"] in {"smoke_passed", "dependency_gap", "mapping_gap", "runtime_failure"}
    assert payload["primitive_count"] == 1
    assert payload["claim_boundary"] == "drop_settle_task_smoke_not_collision_quality_or_safety"


def test_cli_run_newton_drop_settle_keeps_stdout_json_only(tmp_path, capsys, monkeypatch):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: noisy_asset",
                "  path: assets/example.usda",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
                "newton_diagnostic:",
                "  probe_type: drop_settle",
                "  drop_settle:",
                "    max_floor_breach_m: 0.125",
                "    max_settle_linear_speed_mps: 0.25",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        cli,
        "_run_cpd_like_report",
        lambda config: (object(), "assets/example.usda", 8),
    )
    monkeypatch.setattr(
        cli,
        "package_from_cpd_like_report",
        lambda *args, **kwargs: CollisionPackage("noisy_asset"),
    )

    captured_options = {}

    def noisy_drop_settle(*args, **kwargs):
        captured_options["max_floor_breach_m"] = kwargs["options"].max_floor_breach_m
        captured_options["max_settle_linear_speed_mps"] = kwargs["options"].max_settle_linear_speed_mps
        print("Warp 1.13.0 initialized:")
        return NewtonDiagnosticReport(
            stage="newton_drop_settle",
            status="smoke_passed",
            asset_id="noisy_asset",
            package_id="noisy_asset:pkg",
            probe_type="drop_settle",
            device="cpu",
            environment=None,
            primitive_count=0,
            type_counts={},
            shape_mappings=(),
            contact_canaries=(),
            drop_settle_runs=(),
            task_scope="single_asset_drop_settle_static_plane",
            claim_boundary="drop_settle_task_smoke_not_collision_quality_or_safety",
            evidence_level="newton_drop_settle_task_smoke",
        )

    monkeypatch.setattr(cli, "run_newton_drop_settle", noisy_drop_settle)

    assert cli.main(["--config", str(config_path), "--run-newton-drop-settle"]) == 0

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["stage"] == "newton_drop_settle"
    assert captured.out.startswith("{")
    assert "Warp 1.13.0 initialized:" in captured.err
    assert captured_options["max_floor_breach_m"] == 0.125
    assert captured_options["max_settle_linear_speed_mps"] == 0.25


def test_cli_run_newton_sphere_rain_emits_report_for_tiny_usd(tmp_path, capsys):
    Usd = pytest.importorskip("pxr.Usd")
    UsdGeom = pytest.importorskip("pxr.UsdGeom")
    asset_path = tmp_path / "quad.usda"
    stage = Usd.Stage.CreateNew(str(asset_path))
    mesh = UsdGeom.Mesh.Define(stage, "/Quad")
    mesh.CreatePointsAttr([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
    mesh.CreateFaceVertexCountsAttr([4])
    mesh.CreateFaceVertexIndicesAttr([0, 1, 2, 3])
    stage.GetRootLayer().Save()
    source_dir = tmp_path / "newton-source"
    source_dir.mkdir()
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
                "    - newton_sphere_rain",
                "cpd_like:",
                "  primitive_subset:",
                "    - box",
                "    - sphere",
                "    - capsule",
                "  max_source_faces: 8",
                "newton:",
                f"  source_dir: {source_dir}",
                "newton_diagnostic:",
                "  probe_type: sphere_rain",
                "  device: cpu",
            ]
        ),
        encoding="utf-8",
    )

    exit_code = cli.main(["--config", str(config_path), "--run-newton-sphere-rain"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code in {0, 2}
    assert payload["stage"] == "newton_sphere_rain"
    assert payload["asset_id"] == "tiny_quad"
    assert payload["package_id"] == "tiny_quad:cpd_like_face_merge"
    assert payload["probe_type"] == "sphere_rain"
    assert payload["status"] in {"smoke_passed", "dependency_gap", "mapping_gap", "runtime_failure"}
    assert payload["primitive_count"] == 1
    assert payload["claim_boundary"] == "sphere_rain_task_smoke_not_collision_quality_or_safety"


def test_cli_run_newton_sphere_rain_keeps_stdout_json_only(tmp_path, capsys, monkeypatch):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: noisy_asset",
                "  path: assets/example.usda",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
                "newton_diagnostic:",
                "  probe_type: sphere_rain",
                "  sphere_rain:",
                "    sphere_count_x: 2",
                "    sphere_count_y: 3",
                "    sphere_radius_m: 0.125",
                "    min_contact_density: 0.25",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        cli,
        "_run_cpd_like_report",
        lambda config: (object(), "assets/example.usda", 8),
    )
    monkeypatch.setattr(
        cli,
        "package_from_cpd_like_report",
        lambda *args, **kwargs: CollisionPackage("noisy_asset"),
    )

    captured_options = {}

    def noisy_sphere_rain(*args, **kwargs):
        captured_options["sphere_count"] = kwargs["options"].sphere_count
        captured_options["sphere_radius_m"] = kwargs["options"].sphere_radius_m
        captured_options["min_contact_density"] = kwargs["options"].min_contact_density
        print("Warp 1.13.0 initialized:")
        return NewtonDiagnosticReport(
            stage="newton_sphere_rain",
            status="smoke_passed",
            asset_id="noisy_asset",
            package_id="noisy_asset:pkg",
            probe_type="sphere_rain",
            device="cpu",
            environment=None,
            primitive_count=0,
            type_counts={},
            shape_mappings=(),
            contact_canaries=(),
            sphere_rain_runs=(),
            task_scope="single_asset_sphere_rain_static_package",
            claim_boundary="sphere_rain_task_smoke_not_collision_quality_or_safety",
            evidence_level="newton_sphere_rain_task_smoke",
        )

    monkeypatch.setattr(cli, "run_newton_sphere_rain", noisy_sphere_rain)

    assert cli.main(["--config", str(config_path), "--run-newton-sphere-rain"]) == 0

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["stage"] == "newton_sphere_rain"
    assert captured.out.startswith("{")
    assert "Warp 1.13.0 initialized:" in captured.err
    assert captured_options["sphere_count"] == 6
    assert captured_options["sphere_radius_m"] == 0.125
    assert captured_options["min_contact_density"] == 0.25


def test_cli_run_newton_contact_smoke_rejects_unsupported_probe_type(tmp_path, capsys, monkeypatch):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: bad_probe",
                "  path: assets/example.usda",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
                "newton_diagnostic:",
                "  probe_type: drop",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        cli,
        "_run_cpd_like_report",
        lambda config: (object(), "assets/example.usda", 8),
    )

    assert cli.main(["--config", str(config_path), "--run-newton-contact-smoke"]) == 2

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "newton_contact_smoke"
    assert payload["status"] == "smoke_failed"
    assert "newton_diagnostic.probe_type" in payload["fallback_reason"]


def test_cli_run_newton_drop_settle_rejects_unsupported_probe_type(tmp_path, capsys, monkeypatch):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: bad_drop_probe",
                "  path: assets/example.usda",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
                "newton_diagnostic:",
                "  probe_type: contact_canary",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        cli,
        "_run_cpd_like_report",
        lambda config: (object(), "assets/example.usda", 8),
    )

    assert cli.main(["--config", str(config_path), "--run-newton-drop-settle"]) == 2

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "newton_drop_settle"
    assert payload["status"] == "runtime_failure"
    assert "newton_diagnostic.probe_type" in payload["fallback_reason"]


def test_cli_run_newton_sphere_rain_rejects_unsupported_probe_type(tmp_path, capsys, monkeypatch):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: bad_sphere_rain_probe",
                "  path: assets/example.usda",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
                "newton_diagnostic:",
                "  probe_type: contact_canary",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        cli,
        "_run_cpd_like_report",
        lambda config: (object(), "assets/example.usda", 8),
    )

    assert cli.main(["--config", str(config_path), "--run-newton-sphere-rain"]) == 2

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "newton_sphere_rain"
    assert payload["status"] == "runtime_failure"
    assert "newton_diagnostic.probe_type" in payload["fallback_reason"]


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


def test_cli_run_cpd_like_prefers_materialized_manifest_path(tmp_path, capsys):
    local_path = tmp_path / "local_quad.usda"
    missing_source_path = tmp_path / "missing_source.usda"
    _write_mesh_usd(
        local_path,
        points=[(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)],
        face_vertex_counts=[4],
        face_vertex_indices=[0, 1, 2, 3],
    )
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump(
            {
                "assets": [
                    {
                        "role": "bed_dev_smoke",
                        "path": str(missing_source_path),
                        "local_path": str(local_path),
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: local_manifest_quad",
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
    assert payload["source_path"] == str(local_path)
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


def test_cli_int_value_reports_non_finite_number_as_value_error():
    with pytest.raises(ValueError, match="newton_diagnostic.sphere_rain.frames must be an integer"):
        cli._int_value(float("inf"), "newton_diagnostic.sphere_rain.frames")


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
