import json
from pathlib import Path

import pytest
import yaml

from primitive_collision_compiler import cli
from primitive_collision_compiler.contracts import CollisionPackage
from primitive_collision_compiler.reports.schema import NewtonDiagnosticReport

FIXTURE_CONFIG = Path(__file__).parent / "fixtures" / "dry_run_mvp.yaml"


def _newton_native_fitting_comparison_payload(
    *,
    status="smoke_passed",
    claim_boundary="newton_native_fitting_comparison_not_collision_quality_validation",
    evidence_level="offline_newton_native_fitting_comparison_smoke",
    legacy_primitive_subset=None,
):
    return {
        "stage": "cpd_like_newton_native_fitting_comparison",
        "status": status,
        "claim_boundary": claim_boundary,
        "evidence_level": evidence_level,
        "legacy_primitive_subset": list(
            legacy_primitive_subset or ("box", "sphere", "capsule")
        ),
        "cases": [
            {
                "case_id": "cylindrical_rod",
                "expectation_status": "matched"
                if status == "smoke_passed"
                else "mismatched",
                "native": {
                    "selected_primitive_kind": "cylinder",
                    "selection_policy": "support_aware_min_weighted_volume_surrogate_v1",
                    "candidate_audit": [
                        {
                            "primitive_type": "cylinder",
                            "selected": True,
                        }
                    ],
                },
                "comparison": {
                    "native_selected_kind_cost_explained": True,
                    "native_selected_newton_extension": status == "smoke_passed",
                },
            }
        ],
        "real_usd_scope": {
            "assets": [
                {"role": "bed_dev_smoke"},
                {"role": "franka_import_smoke"},
            ],
        },
    }


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


def test_cli_run_phase0_benchmark_emits_json_for_partial_record(tmp_path, capsys, monkeypatch):
    config_path = tmp_path / "phase0.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: phase0_fixture",
                "  path: assets/manifests/phase0_assets.yaml",
                "task:",
                "  primary: phase0_simulation_checked_diagnostic",
            ]
        ),
        encoding="utf-8",
    )
    calls = []

    def fake_report(config_path_arg):
        calls.append(str(config_path_arg))
        return {
            "stage": "phase0_rigid_asset_benchmark",
            "status": "partial",
            "outcome_counts": {
                "accept": 1,
                "fallback": 1,
                "dependency_gap": 0,
                "failure": 0,
            },
        }

    monkeypatch.setattr(cli, "build_phase0_rigid_benchmark_report", fake_report, raising=False)

    assert cli.main(["--config", str(config_path), "--run-phase0-benchmark"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "phase0_rigid_asset_benchmark"
    assert payload["status"] == "partial"
    assert calls == [str(config_path)]


def test_cli_run_phase0_benchmark_returns_zero_for_recorded_failures(
    tmp_path,
    capsys,
    monkeypatch,
):
    config_path = tmp_path / "phase0.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: phase0_fixture",
                "  path: assets/manifests/phase0_assets.yaml",
                "task:",
                "  primary: phase0_simulation_checked_diagnostic",
            ]
        ),
        encoding="utf-8",
    )

    def fake_report(config_path_arg):
        return {
            "stage": "phase0_rigid_asset_benchmark",
            "status": "completed_with_recorded_failures",
            "outcome_counts": {
                "accept": 1,
                "fallback": 0,
                "dependency_gap": 0,
                "failure": 1,
            },
        }

    monkeypatch.setattr(cli, "build_phase0_rigid_benchmark_report", fake_report, raising=False)

    assert cli.main(["--config", str(config_path), "--run-phase0-benchmark"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["outcome_counts"]["failure"] == 1


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


def test_cli_run_newton_native_fitting_comparison_emits_json_without_config(
    capsys,
    monkeypatch,
):
    monkeypatch.setattr(
        cli,
        "build_newton_native_fitting_comparison_report",
        _newton_native_fitting_comparison_payload,
    )

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


def test_cli_run_newton_native_fitting_comparison_reads_config_subsets(
    tmp_path,
    capsys,
    monkeypatch,
):
    calls = []

    def fake_report_builder(*, legacy_subset, native_subset, objective_options):
        calls.append(
            {
                "legacy_subset": legacy_subset,
                "native_subset": native_subset,
                "objective_options": objective_options,
            }
        )
        return _newton_native_fitting_comparison_payload(
            status="partial",
            claim_boundary=objective_options.claim_boundary,
            evidence_level=objective_options.evidence_level,
            legacy_primitive_subset=legacy_subset,
        )

    monkeypatch.setattr(
        cli,
        "build_newton_native_fitting_comparison_report",
        fake_report_builder,
    )

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
    assert calls[0]["legacy_subset"] == ("box", "sphere", "capsule", "cylinder")
    assert calls[0]["native_subset"] == (
        "box",
        "sphere",
        "capsule",
        "cylinder",
        "cone",
        "ellipsoid",
    )


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


def test_cli_run_real_usd_native_fitting_comparison_reads_score_multipliers(
    tmp_path,
    capsys,
):
    manifest_path = _write_two_mesh_manifest(tmp_path)
    config_path = _write_real_usd_native_config(tmp_path, manifest_path)
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    config["cpd_like"]["native_opt_in_primitive_score_multipliers"] = {"cylinder": 0.5}
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")

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

    assert payload["cases"][0]["native"].get("primitive_score_multipliers", {}) == {}
    assert payload["cases"][0]["native_opt_in"]["primitive_score_multipliers"] == {
        "cylinder": 0.5
    }


def test_cli_run_real_usd_native_fitting_comparison_reads_selection_guard(
    tmp_path,
    capsys,
):
    manifest_path = _write_two_mesh_manifest(tmp_path)
    config_path = _write_real_usd_native_config(tmp_path, manifest_path)
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    config["cpd_like"]["native_opt_in_primitive_score_multipliers"] = {"cylinder": 0.5}
    config["cpd_like"]["native_opt_in_selection_guard"] = {
        "enabled": True,
        "mode": "reject",
        "target_primitives": ["cylinder"],
        "max_cylinder_radius": 0.5,
        "min_cylinder_half_height_radius_ratio": 0.1,
        "claim_boundary": "diagnostic_selection_guard_not_collision_quality_validation",
    }
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")

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

    assert "primitive_selection_guard" not in payload["cases"][0]["native"]
    assert payload["cases"][0]["native_opt_in"]["primitive_selection_guard"] == {
        "claim_boundary": "diagnostic_selection_guard_not_collision_quality_validation",
        "enabled": True,
        "max_cylinder_radius": 0.5,
        "min_cylinder_half_height_radius_ratio": 0.1,
        "mode": "reject",
        "target_primitives": ["cylinder"],
    }


def test_cli_run_real_usd_native_fitting_comparison_reads_support_thresholds(
    tmp_path,
    capsys,
):
    manifest_path = _write_two_mesh_manifest(tmp_path)
    config_path = _write_real_usd_native_config(tmp_path, manifest_path)
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    config["cpd_like"]["native_opt_in_extension_support_thresholds"] = {
        "min_extension_source_faces": 2,
        "min_extension_unique_points": 4,
        "claim_boundary": "diagnostic_support_threshold_relaxation_not_collision_quality",
    }
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")

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

    assert "primitive_selection_support_thresholds" not in payload["cases"][0]["native"]
    assert payload["cases"][0]["native_opt_in"][
        "primitive_selection_support_thresholds"
    ] == {
        "claim_boundary": "diagnostic_support_threshold_relaxation_not_collision_quality",
        "min_extension_source_faces": 2,
        "min_extension_unique_points": 4,
    }


def test_cli_run_real_usd_native_fitting_comparison_reads_opt_in_merge_search_policy(
    tmp_path,
    capsys,
):
    manifest_path = _write_two_mesh_manifest(tmp_path)
    config_path = _write_real_usd_native_config(tmp_path, manifest_path)
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    config["cpd_like"]["merge_search_policy"] = "topology_then_virtual"
    config["cpd_like"]["native_opt_in_merge_search_policy"] = "cost_guided_pairwise"
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")

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

    assert payload["cases"][0]["native"]["component_accounting"][
        "merge_search_policy"
    ] == "topology_then_virtual"
    assert payload["cases"][0]["native_opt_in"]["component_accounting"][
        "merge_search_policy"
    ] == "cost_guided_pairwise"


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


@pytest.mark.paper_offline
def test_cli_run_cpd_paper_offline_report_emits_json(capsys):
    assert cli.main(["--run-cpd-paper-offline-report"]) == 0

    captured = capsys.readouterr()
    assert captured.err == ""
    payload = json.loads(captured.out)

    assert payload["stage"] == "cpd_paper_offline_report"
    assert payload["status"] == "partial"
    assert payload["report_generation_status"] == "smoke_passed"
    assert payload["paper_faithfulness"]["status"] == "partial"
    assert payload["failure_labels"] == [
        (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_"
            "configured_runtime_run_contract_missing"
        ),
    ]
    assert (
        payload["next_required_gate"]
        == (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_"
            "configured_runtime_run_contract"
        )
    )
    assert payload["generated_collision_package_count"] == 1
    assert payload["runtime_admissibility_check_count"] == 1
    assert payload["paper_faithfulness"]["implemented_generalization_scope"] == [
        "paper_generalization_batch_a_source_policy",
        "paper_generalization_batch_b_primitive_fit_engine",
        "paper_generalization_batch_c_search_engine",
        "paper_generalization_batch_d_postprocess_policy",
        "paper_generalization_batch_e_package_boundary_readiness",
    ]
    assert payload["paper_faithfulness"]["missing_before_paper_faithful_offline"] == [
        "source_mesh_and_preprocessing_policy",
        "source_face_intake_policy",
        "operator_q_audit",
        "primitive_vocabulary_and_fit",
        "paper_collapse_cost_and_weighting",
        "greedy_priority_queue_trace",
        "target_count_and_threshold_stop",
        "component_pair_edge_handling",
        "enclosed_primitive_postprocess",
    ]
    assert payload["paper_faithfulness"]["runtime_lane_remaining_gates"] == [
        (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_"
            "configured_runtime_run_contract"
        ),
    ]
    assert payload["paper_faithfulness"]["implemented_output_contract_scope"] == [
        "paper_offline_changed_decomposition_output_contract",
        "paper_package_adapter_contract",
        "paper_package_adapter_unsupported_primitive_policy",
        "paper_package_conversion_mapped_subset_plan",
        "paper_mapped_subset_conversion_candidate_matrix",
        "paper_mapped_subset_adapter_preflight_contract",
        "paper_mapped_subset_primitivespec_dry_run_contract",
        "paper_mapped_subset_primitivespec_validation_contract",
        "paper_mapped_subset_primitivespec_generation_preflight_contract",
        "paper_mapped_subset_primitivespec_generation_contract",
        "paper_mapped_subset_primitivespec_candidate_source_contract",
        "paper_mapped_subset_native_current_fixture_contract",
        "paper_mapped_subset_primitivespec_native_fixture_generation_contract",
        "paper_mapped_subset_primitivespec_native_fixture_serialization_contract",
        "paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract",
        "paper_mapped_subset_primitivespec_runtime_construction_contract",
        "paper_mapped_subset_collision_package_generation_preflight_contract",
        "paper_mapped_subset_collision_package_generation_contract",
        "paper_mapped_subset_runtime_admissibility_preflight_contract",
        "paper_mapped_subset_runtime_admissibility_contract",
        "paper_mapped_subset_newton_shape_mapping_preflight_contract",
        "paper_mapped_subset_newton_shape_mapping_contract",
        "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract",
        "paper_mapped_subset_newton_shape_runtime_construction_contract",
        "paper_mapped_subset_newton_shape_runtime_builder_preflight_contract",
        "paper_mapped_subset_newton_shape_runtime_builder_construction_contract",
        "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract",
        "paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract",
        "paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract",
        "paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract",
        "paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract",
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract",
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract",
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract",
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract",
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_validation_contract",
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract",
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract",
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract",
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract",
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract",
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review_contract",
    ]
    builder_construction = payload[
        "paper_mapped_subset_newton_shape_runtime_builder_construction_contract"
    ]
    assert builder_construction["recording_builder_shape_call_count"] == 1
    assert builder_construction["recorded_builder_call_count"] == 1
    assert builder_construction["repo_local_static_shape_helper_call_count"] == 1
    assert builder_construction["newton_builder_shape_call_count"] == 0
    assert builder_construction["newton_engine_shape_object_count"] == 0
    assert builder_construction["newton_runtime_execution_count"] == 0
    boundary_preflight = payload[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract"
    ]
    assert (
        boundary_preflight[
            "newton_shape_runtime_engine_builder_boundary_preflight_row_count"
        ]
        == 1
    )
    assert boundary_preflight["recorded_builder_call_count"] == 1
    assert boundary_preflight["real_newton_import_count"] == 0
    assert boundary_preflight["newton_model_builder_instantiated_count"] == 0
    assert boundary_preflight["newton_engine_shape_object_count"] == 0
    assert boundary_preflight["newton_builder_shape_call_count"] == 0
    assert boundary_preflight["newton_runtime_execution_count"] == 0
    environment_probe = payload[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract"
    ]
    assert (
        environment_probe[
            "newton_shape_runtime_engine_builder_environment_probe_row_count"
        ]
        == 1
    )
    assert environment_probe["module_probe_row_count"] == 2
    assert environment_probe["source_dir_configured_count"] == 0
    assert environment_probe["real_newton_import_count"] == 0
    assert environment_probe["real_warp_import_count"] == 0
    assert environment_probe["newton_model_builder_instantiated_count"] == 0
    assert environment_probe["newton_engine_shape_object_count"] == 0
    assert environment_probe["newton_builder_shape_call_count"] == 0
    assert environment_probe["newton_runtime_execution_count"] == 0
    api_surface = payload[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"
    ]
    assert (
        api_surface["gate_id"]
        == "paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"
    )
    assert (
        api_surface["input_gate_id"]
        == "paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract"
    )
    assert (
        api_surface["next_required_gate"]
        == "paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"
    )
    assert api_surface["newton_shape_runtime_engine_builder_api_surface_row_count"] == 1
    assert api_surface["api_surface_probe_count"] == 1
    assert api_surface["source_dir_configured_count"] == 0
    assert api_surface["newton_model_builder_symbol_found_count"] == 0
    assert api_surface["newton_add_shape_box_symbol_found_count"] == 0
    assert api_surface["real_newton_import_count"] == 0
    assert api_surface["real_warp_import_count"] == 0
    assert api_surface["newton_model_builder_instantiated_count"] == 0
    assert api_surface["newton_engine_shape_object_count"] == 0
    assert api_surface["newton_builder_shape_call_count"] == 0
    assert api_surface["newton_runtime_execution_count"] == 0
    entry = payload[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"
    ]
    assert (
        entry["gate_id"]
        == "paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"
    )
    assert (
        entry["input_gate_id"]
        == "paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"
    )
    assert (
        entry["next_required_gate"]
        == "paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"
    )
    assert entry["entry_decision"] == "defer_real_runtime_entry"
    assert entry["runtime_entry_allowed_count"] == 0
    assert entry["runtime_entry_attempted_count"] == 0
    assert entry["real_newton_import_count"] == 0
    assert entry["real_warp_import_count"] == 0
    assert entry["newton_model_builder_instantiated_count"] == 0
    assert entry["newton_builder_shape_call_count"] == 0
    assert entry["newton_model_finalized_count"] == 0
    assert entry["newton_engine_shape_object_count"] == 0
    assert entry["newton_collision_pipeline_created_count"] == 0
    assert entry["newton_collision_pipeline_collide_count"] == 0
    assert entry["newton_runtime_execution_count"] == 0
    smoke = payload[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"
    ]
    assert (
        smoke["gate_id"]
        == "paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"
    )
    assert (
        smoke["input_gate_id"]
        == "paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"
    )
    assert (
        smoke["next_required_gate"]
        == (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_"
            "runtime_execution_contract"
        )
    )
    assert smoke["smoke_decision"] == "skip_real_runtime_smoke"
    assert smoke["runtime_smoke_allowed_count"] == 0
    assert smoke["runtime_smoke_attempted_count"] == 0
    assert smoke["runtime_smoke_passed_count"] == 0
    assert smoke["real_newton_import_count"] == 0
    assert smoke["real_warp_import_count"] == 0
    assert smoke["newton_model_builder_instantiated_count"] == 0
    assert smoke["newton_builder_shape_call_count"] == 0
    assert smoke["newton_model_finalized_count"] == 0
    assert smoke["newton_engine_shape_object_count"] == 0
    assert smoke["newton_collision_pipeline_created_count"] == 0
    assert smoke["newton_collision_pipeline_collide_count"] == 0
    assert smoke["newton_runtime_execution_count"] == 0
    runtime_execution = payload[
        (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_"
            "runtime_execution_contract"
        )
    ]
    assert runtime_execution["gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "runtime_execution_contract"
    )
    assert runtime_execution["input_gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"
    )
    assert runtime_execution["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "runtime_lane_review_contract"
    )
    assert runtime_execution["runtime_execution_decision"] == (
        "skip_real_runtime_execution"
    )
    assert runtime_execution["runtime_execution_allowed_count"] == 0
    assert runtime_execution["runtime_execution_attempted_count"] == 0
    assert runtime_execution["runtime_execution_passed_count"] == 0
    assert runtime_execution["real_newton_import_count"] == 0
    assert runtime_execution["real_warp_import_count"] == 0
    assert runtime_execution["newton_model_builder_instantiated_count"] == 0
    assert runtime_execution["newton_engine_shape_object_count"] == 0
    assert runtime_execution["newton_builder_shape_call_count"] == 0
    assert runtime_execution["newton_model_finalized_count"] == 0
    assert runtime_execution["newton_collision_pipeline_created_count"] == 0
    assert runtime_execution["newton_collision_pipeline_collide_count"] == 0
    assert runtime_execution["newton_runtime_execution_count"] == 0
    runtime_lane_review = payload[
        (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_"
            "runtime_lane_review_contract"
        )
    ]
    assert runtime_lane_review["gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "runtime_lane_review_contract"
    )
    assert runtime_lane_review["input_gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "runtime_execution_contract"
    )
    assert runtime_lane_review["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_design_contract"
    )
    assert (
        runtime_lane_review["runtime_lane_review_decision"]
        == "keep_real_runtime_execution_blocked"
    )
    assert (
        runtime_lane_review["runtime_lane_review_status"]
        == "claim_boundary_preserved"
    )
    assert runtime_lane_review["real_runtime_execution_evidence"] is False
    assert runtime_lane_review["runtime_compatibility_validated"] is False
    assert runtime_lane_review["runtime_lane_review_recorded_count"] == 1
    assert runtime_lane_review["runtime_lane_claim_boundary_preserved_count"] == 1
    assert runtime_lane_review["real_newton_import_count"] == 0
    assert runtime_lane_review["real_warp_import_count"] == 0
    assert runtime_lane_review["newton_model_builder_instantiated_count"] == 0
    assert runtime_lane_review["newton_engine_shape_object_count"] == 0
    assert runtime_lane_review["newton_builder_shape_call_count"] == 0
    assert runtime_lane_review["newton_model_finalized_count"] == 0
    assert runtime_lane_review["newton_collision_pipeline_created_count"] == 0
    assert runtime_lane_review["newton_collision_pipeline_collide_count"] == 0
    assert runtime_lane_review["newton_runtime_execution_count"] == 0
    configured_runtime_design = payload[
        (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_"
            "configured_runtime_design_contract"
        )
    ]
    assert configured_runtime_design["gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_design_contract"
    )
    assert configured_runtime_design["input_gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "runtime_lane_review_contract"
    )
    assert configured_runtime_design["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_preflight_contract"
    )
    assert configured_runtime_design["configured_runtime_design_decision"] == (
        "define_configured_runtime_inputs_keep_real_runtime_blocked"
    )
    assert configured_runtime_design["configured_runtime_design_status"] == (
        "input_design_recorded"
    )
    assert configured_runtime_design["configured_runtime_design_recorded_count"] == 1
    assert configured_runtime_design["configured_runtime_preflight_ready_count"] == 0
    assert configured_runtime_design["required_config_keys"] == [
        "newton.source_dir",
        "newton_diagnostic.device",
    ]
    assert configured_runtime_design["required_runtime_input_count"] == 6
    assert configured_runtime_design["real_newton_import_count"] == 0
    assert configured_runtime_design["real_warp_import_count"] == 0
    assert configured_runtime_design["newton_model_builder_instantiated_count"] == 0
    assert configured_runtime_design["newton_engine_shape_object_count"] == 0
    assert configured_runtime_design["newton_builder_shape_call_count"] == 0
    assert configured_runtime_design["newton_model_finalized_count"] == 0
    assert configured_runtime_design["newton_collision_pipeline_created_count"] == 0
    assert configured_runtime_design["newton_collision_pipeline_collide_count"] == 0
    assert configured_runtime_design["newton_runtime_execution_count"] == 0
    configured_runtime_preflight = payload[
        (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_"
            "configured_runtime_preflight_contract"
        )
    ]
    assert configured_runtime_preflight["gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_preflight_contract"
    )
    assert configured_runtime_preflight["input_gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_design_contract"
    )
    assert configured_runtime_preflight["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_validation_contract"
    )
    assert configured_runtime_preflight["configured_runtime_preflight_decision"] == (
        "record_configured_runtime_preflight_keep_real_runtime_blocked"
    )
    assert configured_runtime_preflight["configured_runtime_preflight_recorded_count"] == 1
    assert configured_runtime_preflight["configured_runtime_preflight_passed_count"] == 1
    assert configured_runtime_preflight["configured_runtime_validation_ready_count"] == 0
    assert configured_runtime_preflight["runtime_config_validated"] is False
    assert configured_runtime_preflight["runtime_source_config_resolved"] is False
    assert configured_runtime_preflight["runtime_device_config_resolved"] is False
    assert configured_runtime_preflight["real_newton_import_count"] == 0
    assert configured_runtime_preflight["real_warp_import_count"] == 0
    assert (
        configured_runtime_preflight["newton_model_builder_instantiated_count"]
        == 0
    )
    assert configured_runtime_preflight["newton_engine_shape_object_count"] == 0
    assert configured_runtime_preflight["newton_builder_shape_call_count"] == 0
    assert configured_runtime_preflight["newton_model_finalized_count"] == 0
    assert (
        configured_runtime_preflight[
            "newton_collision_pipeline_created_count"
        ]
        == 0
    )
    assert (
        configured_runtime_preflight[
            "newton_collision_pipeline_collide_count"
        ]
        == 0
    )
    assert configured_runtime_preflight["newton_runtime_execution_count"] == 0
    configured_runtime_validation = payload[
        (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_"
            "configured_runtime_validation_contract"
        )
    ]
    assert configured_runtime_validation["gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_validation_contract"
    )
    assert configured_runtime_validation["input_gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_preflight_contract"
    )
    assert configured_runtime_validation["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_source_resolution_contract"
    )
    assert configured_runtime_validation["configured_runtime_validation_decision"] == (
        "record_configured_runtime_validation_keep_real_runtime_blocked"
    )
    assert configured_runtime_validation["configured_runtime_validation_recorded_count"] == 1
    assert configured_runtime_validation["configured_runtime_validation_passed_count"] == 0
    assert configured_runtime_validation["configured_runtime_validation_failed_count"] == 1
    assert configured_runtime_validation["runtime_config_validated"] is False
    assert configured_runtime_validation["runtime_source_config_resolved"] is False
    assert configured_runtime_validation["runtime_device_config_resolved"] is False
    assert configured_runtime_validation["newton_source_dir_configured"] is False
    assert configured_runtime_validation["newton_diagnostic_device_configured"] is False
    assert configured_runtime_validation["real_newton_import_count"] == 0
    assert configured_runtime_validation["real_warp_import_count"] == 0
    assert (
        configured_runtime_validation["newton_model_builder_instantiated_count"]
        == 0
    )
    assert configured_runtime_validation["newton_engine_shape_object_count"] == 0
    assert configured_runtime_validation["newton_builder_shape_call_count"] == 0
    assert configured_runtime_validation["newton_model_finalized_count"] == 0
    assert (
        configured_runtime_validation[
            "newton_collision_pipeline_created_count"
        ]
        == 0
    )
    assert (
        configured_runtime_validation[
            "newton_collision_pipeline_collide_count"
        ]
        == 0
    )
    assert configured_runtime_validation["newton_runtime_execution_count"] == 0
    configured_runtime_source_resolution = payload[
        (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_"
            "configured_runtime_source_resolution_contract"
        )
    ]
    assert configured_runtime_source_resolution["gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_source_resolution_contract"
    )
    assert configured_runtime_source_resolution["input_gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_validation_contract"
    )
    assert configured_runtime_source_resolution["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_device_resolution_contract"
    )
    assert configured_runtime_source_resolution[
        "configured_runtime_source_resolution_decision"
    ] == "record_configured_runtime_source_resolution_keep_real_runtime_blocked"
    assert configured_runtime_source_resolution[
        "configured_runtime_source_resolution_recorded_count"
    ] == 1
    assert configured_runtime_source_resolution[
        "configured_runtime_source_resolution_passed_count"
    ] == 0
    assert configured_runtime_source_resolution[
        "configured_runtime_source_resolution_failed_count"
    ] == 1
    assert configured_runtime_source_resolution[
        "newton_source_dir_resolution_attempted_count"
    ] == 0
    assert configured_runtime_source_resolution[
        "runtime_source_config_resolved"
    ] is False
    assert configured_runtime_source_resolution[
        "runtime_device_config_resolved"
    ] is False
    assert configured_runtime_source_resolution[
        "newton_source_dir_resolution_attempted"
    ] is False
    assert configured_runtime_source_resolution[
        "newton_source_dir_filesystem_probe_allowed"
    ] is False
    assert configured_runtime_source_resolution["newton_source_dir_exists"] is None
    assert configured_runtime_source_resolution["real_newton_import_count"] == 0
    assert configured_runtime_source_resolution["real_warp_import_count"] == 0
    assert (
        configured_runtime_source_resolution[
            "newton_model_builder_instantiated_count"
        ]
        == 0
    )
    assert (
        configured_runtime_source_resolution["newton_engine_shape_object_count"]
        == 0
    )
    assert configured_runtime_source_resolution["newton_builder_shape_call_count"] == 0
    assert configured_runtime_source_resolution["newton_model_finalized_count"] == 0
    assert (
        configured_runtime_source_resolution[
            "newton_collision_pipeline_created_count"
        ]
        == 0
    )
    assert (
        configured_runtime_source_resolution[
            "newton_collision_pipeline_collide_count"
        ]
        == 0
    )
    assert configured_runtime_source_resolution["newton_runtime_execution_count"] == 0
    configured_runtime_device_resolution = payload[
        (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_"
            "configured_runtime_device_resolution_contract"
        )
    ]
    assert configured_runtime_device_resolution["gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_device_resolution_contract"
    )
    assert configured_runtime_device_resolution["input_gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_source_resolution_contract"
    )
    assert configured_runtime_device_resolution["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_entry_decision_contract"
    )
    assert configured_runtime_device_resolution[
        "configured_runtime_device_resolution_decision"
    ] == "record_configured_runtime_device_resolution_keep_real_runtime_blocked"
    assert configured_runtime_device_resolution[
        "configured_runtime_device_resolution_recorded_count"
    ] == 1
    assert configured_runtime_device_resolution[
        "configured_runtime_device_resolution_passed_count"
    ] == 0
    assert configured_runtime_device_resolution[
        "configured_runtime_device_resolution_failed_count"
    ] == 1
    assert configured_runtime_device_resolution[
        "newton_diagnostic_device_resolution_attempted_count"
    ] == 0
    assert configured_runtime_device_resolution[
        "runtime_source_config_resolved"
    ] is False
    assert configured_runtime_device_resolution[
        "runtime_device_config_resolved"
    ] is False
    assert configured_runtime_device_resolution[
        "newton_diagnostic_device_resolution_attempted"
    ] is False
    assert configured_runtime_device_resolution[
        "newton_diagnostic_device_resolution_status"
    ] == "not_attempted_missing_config"
    assert configured_runtime_device_resolution["newton_diagnostic_device"] is None
    assert configured_runtime_device_resolution["real_newton_import_count"] == 0
    assert configured_runtime_device_resolution["real_warp_import_count"] == 0
    assert (
        configured_runtime_device_resolution[
            "newton_model_builder_instantiated_count"
        ]
        == 0
    )
    assert (
        configured_runtime_device_resolution["newton_engine_shape_object_count"]
        == 0
    )
    assert configured_runtime_device_resolution["newton_builder_shape_call_count"] == 0
    assert configured_runtime_device_resolution["newton_model_finalized_count"] == 0
    assert (
        configured_runtime_device_resolution[
            "newton_collision_pipeline_created_count"
        ]
        == 0
    )
    assert (
        configured_runtime_device_resolution[
            "newton_collision_pipeline_collide_count"
        ]
        == 0
    )
    assert configured_runtime_device_resolution["newton_runtime_execution_count"] == 0
    configured_runtime_entry_decision = payload[
        (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_"
            "configured_runtime_entry_decision_contract"
        )
    ]
    assert configured_runtime_entry_decision["gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_entry_decision_contract"
    )
    assert configured_runtime_entry_decision["input_gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_device_resolution_contract"
    )
    assert configured_runtime_entry_decision["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_smoke_contract"
    )
    assert configured_runtime_entry_decision[
        "configured_runtime_entry_decision"
    ] == "defer_real_runtime_entry_missing_configured_runtime_source_or_device"
    assert configured_runtime_entry_decision[
        "configured_runtime_entry_decision_recorded_count"
    ] == 1
    assert configured_runtime_entry_decision[
        "configured_runtime_entry_decision_passed_count"
    ] == 0
    assert configured_runtime_entry_decision[
        "configured_runtime_entry_decision_failed_count"
    ] == 1
    assert configured_runtime_entry_decision["runtime_entry_allowed_count"] == 0
    assert configured_runtime_entry_decision["runtime_entry_attempted_count"] == 0
    assert configured_runtime_entry_decision["runtime_entry_passed_count"] == 0
    assert configured_runtime_entry_decision["runtime_entry_allowed"] is False
    assert configured_runtime_entry_decision["runtime_entry_attempted"] is False
    assert configured_runtime_entry_decision["runtime_entry_passed"] is False
    assert configured_runtime_entry_decision["runtime_source_config_resolved"] is False
    assert configured_runtime_entry_decision["runtime_device_config_resolved"] is False
    assert configured_runtime_entry_decision["newton_source_dir"] is None
    assert configured_runtime_entry_decision["newton_diagnostic_device"] is None
    assert configured_runtime_entry_decision["real_newton_import_count"] == 0
    assert configured_runtime_entry_decision["real_warp_import_count"] == 0
    assert (
        configured_runtime_entry_decision["newton_model_builder_instantiated_count"]
        == 0
    )
    assert configured_runtime_entry_decision["newton_engine_shape_object_count"] == 0
    assert configured_runtime_entry_decision["newton_builder_shape_call_count"] == 0
    assert configured_runtime_entry_decision["newton_model_finalized_count"] == 0
    assert (
        configured_runtime_entry_decision[
            "newton_collision_pipeline_created_count"
        ]
        == 0
    )
    assert (
        configured_runtime_entry_decision[
            "newton_collision_pipeline_collide_count"
        ]
        == 0
    )
    assert configured_runtime_entry_decision["newton_runtime_execution_count"] == 0
    configured_runtime_smoke = payload[
        (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_"
            "configured_runtime_smoke_contract"
        )
    ]
    assert configured_runtime_smoke["gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_smoke_contract"
    )
    assert configured_runtime_smoke["input_gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_entry_decision_contract"
    )
    assert configured_runtime_smoke["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_execution_contract"
    )
    assert configured_runtime_smoke[
        "configured_runtime_smoke_decision"
    ] == "skip_real_runtime_smoke_missing_configured_runtime_entry"
    assert configured_runtime_smoke[
        "configured_runtime_smoke_recorded_count"
    ] == 1
    assert configured_runtime_smoke[
        "configured_runtime_smoke_passed_count"
    ] == 0
    assert configured_runtime_smoke[
        "configured_runtime_smoke_failed_count"
    ] == 1
    assert configured_runtime_smoke["configured_runtime_smoke_allowed_count"] == 0
    assert configured_runtime_smoke["configured_runtime_smoke_attempted_count"] == 0
    assert configured_runtime_smoke["runtime_entry_allowed_count"] == 0
    assert configured_runtime_smoke["runtime_entry_attempted_count"] == 0
    assert configured_runtime_smoke["runtime_entry_passed_count"] == 0
    assert configured_runtime_smoke["configured_runtime_smoke_allowed"] is False
    assert configured_runtime_smoke["configured_runtime_smoke_attempted"] is False
    assert configured_runtime_smoke["configured_runtime_smoke_passed"] is False
    assert configured_runtime_smoke["runtime_entry_allowed"] is False
    assert configured_runtime_smoke["runtime_entry_attempted"] is False
    assert configured_runtime_smoke["runtime_entry_passed"] is False
    assert configured_runtime_smoke["runtime_source_config_resolved"] is False
    assert configured_runtime_smoke["runtime_device_config_resolved"] is False
    assert configured_runtime_smoke["newton_source_dir"] is None
    assert configured_runtime_smoke["newton_diagnostic_device"] is None
    assert configured_runtime_smoke["real_newton_import_count"] == 0
    assert configured_runtime_smoke["real_warp_import_count"] == 0
    assert configured_runtime_smoke["newton_model_builder_instantiated_count"] == 0
    assert configured_runtime_smoke["newton_engine_shape_object_count"] == 0
    assert configured_runtime_smoke["newton_builder_shape_call_count"] == 0
    assert configured_runtime_smoke["newton_model_finalized_count"] == 0
    assert (
        configured_runtime_smoke["newton_collision_pipeline_created_count"]
        == 0
    )
    assert (
        configured_runtime_smoke["newton_collision_pipeline_collide_count"]
        == 0
    )
    assert configured_runtime_smoke["newton_runtime_execution_count"] == 0
    configured_runtime_execution = payload[
        (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_"
            "configured_runtime_execution_contract"
        )
    ]
    assert configured_runtime_execution["gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_execution_contract"
    )
    assert configured_runtime_execution["input_gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_smoke_contract"
    )
    assert configured_runtime_execution["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_lane_review_contract"
    )
    assert configured_runtime_execution[
        "configured_runtime_execution_decision"
    ] == "skip_real_runtime_execution_configured_runtime_smoke_not_allowed"
    assert configured_runtime_execution[
        "configured_runtime_execution_recorded_count"
    ] == 1
    assert configured_runtime_execution[
        "configured_runtime_execution_passed_count"
    ] == 0
    assert configured_runtime_execution[
        "configured_runtime_execution_failed_count"
    ] == 1
    assert (
        configured_runtime_execution["configured_runtime_execution_allowed_count"]
        == 0
    )
    assert (
        configured_runtime_execution[
            "configured_runtime_execution_attempted_count"
        ]
        == 0
    )
    assert configured_runtime_execution[
        "configured_runtime_execution_allowed"
    ] is False
    assert configured_runtime_execution[
        "configured_runtime_execution_attempted"
    ] is False
    assert configured_runtime_execution[
        "configured_runtime_execution_passed"
    ] is False
    assert configured_runtime_execution["configured_runtime_smoke_allowed"] is False
    assert (
        configured_runtime_execution["configured_runtime_smoke_attempted"]
        is False
    )
    assert configured_runtime_execution["configured_runtime_smoke_passed"] is False
    assert configured_runtime_execution["runtime_entry_allowed"] is False
    assert configured_runtime_execution["runtime_entry_attempted"] is False
    assert configured_runtime_execution["runtime_entry_passed"] is False
    assert configured_runtime_execution["runtime_source_config_resolved"] is False
    assert configured_runtime_execution["runtime_device_config_resolved"] is False
    assert configured_runtime_execution["newton_source_dir"] is None
    assert configured_runtime_execution["newton_diagnostic_device"] is None
    assert configured_runtime_execution["real_newton_import_count"] == 0
    assert configured_runtime_execution["real_warp_import_count"] == 0
    assert (
        configured_runtime_execution["newton_model_builder_instantiated_count"]
        == 0
    )
    assert configured_runtime_execution["newton_engine_shape_object_count"] == 0
    assert configured_runtime_execution["newton_builder_shape_call_count"] == 0
    assert configured_runtime_execution["newton_model_finalized_count"] == 0
    assert (
        configured_runtime_execution["newton_collision_pipeline_created_count"]
        == 0
    )
    assert (
        configured_runtime_execution["newton_collision_pipeline_collide_count"]
        == 0
    )
    assert configured_runtime_execution["newton_runtime_execution_count"] == 0
    configured_runtime_lane_review = payload[
        (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_"
            "configured_runtime_lane_review_contract"
        )
    ]
    assert configured_runtime_lane_review["gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_lane_review_contract"
    )
    assert configured_runtime_lane_review["input_gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_execution_contract"
    )
    assert configured_runtime_lane_review["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_"
        "configured_runtime_run_contract"
    )
    assert configured_runtime_lane_review[
        "configured_runtime_lane_review_decision"
    ] == (
        "keep_real_runtime_execution_blocked_after_configured_runtime_"
        "execution_review"
    )
    assert configured_runtime_lane_review[
        "configured_runtime_lane_review_recorded_count"
    ] == 1
    assert configured_runtime_lane_review[
        "configured_runtime_lane_claim_boundary_preserved_count"
    ] == 1
    assert configured_runtime_lane_review[
        "real_runtime_execution_evidence_count"
    ] == 0
    assert configured_runtime_lane_review[
        "runtime_compatibility_validated_count"
    ] == 0
    assert configured_runtime_lane_review["configured_runtime_run_allowed"] is False
    assert (
        configured_runtime_lane_review["configured_runtime_run_attempted"]
        is False
    )
    assert configured_runtime_lane_review["configured_runtime_run_passed"] is False
    assert (
        configured_runtime_lane_review["real_runtime_execution_evidence"]
        is False
    )
    assert (
        configured_runtime_lane_review["runtime_compatibility_validated"]
        is False
    )
    assert configured_runtime_lane_review["real_newton_import_count"] == 0
    assert configured_runtime_lane_review["real_warp_import_count"] == 0
    assert (
        configured_runtime_lane_review["newton_model_builder_instantiated_count"]
        == 0
    )
    assert (
        configured_runtime_lane_review["newton_engine_shape_object_count"] == 0
    )
    assert configured_runtime_lane_review["newton_builder_shape_call_count"] == 0
    assert configured_runtime_lane_review["newton_model_finalized_count"] == 0
    assert (
        configured_runtime_lane_review["newton_collision_pipeline_created_count"]
        == 0
    )
    assert (
        configured_runtime_lane_review["newton_collision_pipeline_collide_count"]
        == 0
    )
    assert configured_runtime_lane_review["newton_runtime_execution_count"] == 0
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
    assert payload["collision_quality_measured"] is False
    assert payload["deployment_or_certification_claimed"] is False
    plan = payload["paper_faithful_offline_generalization_plan"]
    assert plan["closed_gate"] == "paper_faithful_offline_generalization_plan"
    assert plan["generalization_plan_complete"] is True
    assert plan["paper_faithful_offline_allowed"] is False
    assert plan["next_required_gate"] == "paper_package_adapter_contract"
    assert [batch["batch_id"] for batch in plan["planned_batches"]] == [
        "paper_generalization_batch_a_source_policy",
        "paper_generalization_batch_b_primitive_fit_engine",
        "paper_generalization_batch_c_search_engine",
        "paper_generalization_batch_d_postprocess_policy",
        "paper_generalization_batch_e_package_boundary_readiness",
    ]
    assert plan["package_generation_triggered"] is False
    assert plan["newton_runtime_triggered"] is False
    assert plan["real_usd_triggered"] is False
    assert plan["benchmark_triggered"] is False
    source_policy = payload["paper_generalization_batch_a_source_policy"]
    assert source_policy["gate_id"] == "paper_generalization_batch_a_source_policy"
    assert source_policy["gate_status"] == "implemented_offline_report_only_partial"
    assert source_policy["closed_gate"] == "paper_generalization_batch_a_source_policy"
    assert (
        source_policy["next_required_gate"]
        == "paper_generalization_batch_b_primitive_fit_engine"
    )
    assert source_policy["decision"] == "remain_partial"
    assert source_policy["paper_faithful_offline_allowed"] is False
    assert (
        source_policy["implementation_boundary"]
        == "offline_report_only_no_package_or_newton"
    )
    assert [row["policy_row_id"] for row in source_policy["policy_matrix"]] == [
        "accepted_mixed_triangle_quad_polygon_exact_dedup",
        "accepted_degenerate_after_exact_dedup_drop",
        "rejected_concave_polygon",
    ]
    assert source_policy["package_generation_triggered"] is False
    assert source_policy["newton_runtime_triggered"] is False
    assert source_policy["real_usd_triggered"] is False
    assert source_policy["benchmark_triggered"] is False
    primitive_fit = payload["paper_generalization_batch_b_primitive_fit_engine"]
    assert primitive_fit["gate_id"] == "paper_generalization_batch_b_primitive_fit_engine"
    assert primitive_fit["gate_status"] == "implemented_offline_report_only_partial"
    assert (
        primitive_fit["closed_gate"]
        == "paper_generalization_batch_b_primitive_fit_engine"
    )
    assert primitive_fit["next_required_gate"] == "paper_generalization_batch_c_search_engine"
    assert primitive_fit["decision"] == "remain_partial"
    assert primitive_fit["paper_faithful_offline_allowed"] is False
    assert (
        primitive_fit["implementation_boundary"]
        == "offline_report_only_no_package_or_newton"
    )
    assert primitive_fit["coverage_summary"]["primitive_count"] == 6
    assert primitive_fit["coverage_summary"]["generated_probe_count"] == 6
    assert primitive_fit["coverage_summary"]["candidate_row_count"] == 36
    assert len(primitive_fit["primitive_family_matrix"]) == 6
    assert primitive_fit["package_generation_triggered"] is False
    assert primitive_fit["newton_runtime_triggered"] is False
    assert primitive_fit["real_usd_triggered"] is False
    assert primitive_fit["benchmark_triggered"] is False
    search_engine = payload["paper_generalization_batch_c_search_engine"]
    assert search_engine["gate_id"] == "paper_generalization_batch_c_search_engine"
    assert search_engine["gate_status"] == "implemented_offline_report_only_partial"
    assert search_engine["closed_gate"] == "paper_generalization_batch_c_search_engine"
    assert (
        search_engine["next_required_gate"]
        == "paper_generalization_batch_d_postprocess_policy"
    )
    assert search_engine["decision"] == "remain_partial"
    assert search_engine["paper_faithful_offline_allowed"] is False
    assert (
        search_engine["implementation_boundary"]
        == "offline_report_only_no_package_or_newton"
    )
    assert search_engine["coverage_summary"]["search_trace_row_count"] == 8
    assert search_engine["coverage_summary"]["closed_gate_count"] == 3
    assert search_engine["coverage_summary"]["remaining_generalization_gate_count"] == 2
    assert len(search_engine["search_trace_matrix"]) == 8
    assert search_engine["package_generation_triggered"] is False
    assert search_engine["newton_runtime_triggered"] is False
    assert search_engine["real_usd_triggered"] is False
    assert search_engine["benchmark_triggered"] is False
    postprocess_policy = payload["paper_generalization_batch_d_postprocess_policy"]
    assert postprocess_policy["gate_id"] == "paper_generalization_batch_d_postprocess_policy"
    assert postprocess_policy["gate_status"] == "implemented_offline_report_only_partial"
    assert (
        postprocess_policy["closed_gate"]
        == "paper_generalization_batch_d_postprocess_policy"
    )
    assert (
        postprocess_policy["next_required_gate"]
        == "paper_generalization_batch_e_package_boundary_readiness"
    )
    assert postprocess_policy["decision"] == "remain_partial"
    assert postprocess_policy["paper_faithful_offline_allowed"] is False
    assert (
        postprocess_policy["implementation_boundary"]
        == "offline_report_only_no_package_or_newton"
    )
    assert postprocess_policy["coverage_summary"]["postprocess_row_count"] == 3
    assert postprocess_policy["coverage_summary"]["closed_gate_count"] == 4
    assert (
        postprocess_policy["coverage_summary"]["remaining_generalization_gate_count"]
        == 1
    )
    assert len(postprocess_policy["postprocess_policy_matrix"]) == 3
    assert postprocess_policy["package_generation_triggered"] is False
    assert postprocess_policy["newton_runtime_triggered"] is False
    assert postprocess_policy["real_usd_triggered"] is False
    assert postprocess_policy["benchmark_triggered"] is False
    package_boundary = payload["paper_generalization_batch_e_package_boundary_readiness"]
    assert (
        package_boundary["gate_id"]
        == "paper_generalization_batch_e_package_boundary_readiness"
    )
    assert package_boundary["gate_status"] == "implemented_planning_only_partial"
    assert (
        package_boundary["next_required_gate"]
        == "paper_offline_changed_decomposition_output_contract"
    )
    assert package_boundary["package_generation_allowed"] is False
    assert package_boundary["paper_faithful_offline_allowed"] is False
    assert package_boundary["coverage_summary"]["boundary_review_row_count"] == 5
    assert package_boundary["coverage_summary"]["closed_gate_count"] == 5
    assert (
        package_boundary["coverage_summary"]["remaining_generalization_gate_count"]
        == 0
    )
    assert len(package_boundary["boundary_review_matrix"]) == 5
    assert package_boundary["package_generation_triggered"] is False
    assert package_boundary["newton_runtime_triggered"] is False
    assert package_boundary["real_usd_triggered"] is False
    assert package_boundary["benchmark_triggered"] is False
    changed_contract = payload["paper_offline_changed_decomposition_output_contract"]
    assert changed_contract["gate_id"] == "paper_offline_changed_decomposition_output_contract"
    assert changed_contract["gate_status"] == "implemented_offline_contract_only_partial"
    assert changed_contract["next_required_gate"] == "paper_package_adapter_contract"
    assert (
        changed_contract["artifact_kind"]
        == "offline_changed_decomposition_output_not_collision_package"
    )
    assert changed_contract["package_generation_allowed"] is False
    assert changed_contract["coverage_summary"]["decomposition_output_row_count"] == 9
    assert changed_contract["coverage_summary"]["primitive_record_count"] == 16
    assert changed_contract["coverage_summary"]["postprocess_state_row_count"] == 3
    assert len(changed_contract["decomposition_output_rows"]) == 9
    assert len(changed_contract["postprocess_state_rows"]) == 3
    assert changed_contract["package_generation_triggered"] is False
    assert changed_contract["newton_runtime_triggered"] is False
    adapter_contract = payload["paper_package_adapter_contract"]
    assert adapter_contract["gate_id"] == "paper_package_adapter_contract"
    assert (
        adapter_contract["gate_status"]
        == "implemented_offline_adapter_contract_only_partial"
    )
    assert (
        adapter_contract["input_gate_id"]
        == "paper_offline_changed_decomposition_output_contract"
    )
    assert (
        adapter_contract["next_required_gate"]
        == "paper_package_adapter_unsupported_primitive_policy"
    )
    assert (
        adapter_contract["artifact_kind"]
        == "offline_package_adapter_contract_not_collision_package"
    )
    assert adapter_contract["package_generation_allowed"] is False
    assert (
        adapter_contract["coverage_summary"]["primitive_decision_row_count"]
        == changed_contract["coverage_summary"]["primitive_record_count"]
        == 16
    )
    assert adapter_contract["coverage_summary"]["adapter_eligible_record_count"] == 0
    assert adapter_contract["coverage_summary"]["blocked_record_count"] == 0
    assert (
        adapter_contract["coverage_summary"]["later_policy_required_record_count"]
        == 16
    )
    assert (
        adapter_contract["coverage_summary"]["offline_only_unmapped_record_count"]
        == 16
    )
    assert len(adapter_contract["primitive_adapter_decision_rows"]) == 16
    assert adapter_contract["package_generation_triggered"] is False
    assert adapter_contract["newton_runtime_triggered"] is False
    assert adapter_contract["real_usd_triggered"] is False
    assert adapter_contract["benchmark_triggered"] is False
    unsupported_policy = payload["paper_package_adapter_unsupported_primitive_policy"]
    assert (
        unsupported_policy["gate_id"]
        == "paper_package_adapter_unsupported_primitive_policy"
    )
    assert (
        unsupported_policy["gate_status"]
        == "implemented_offline_unsupported_primitive_policy_only_partial"
    )
    assert unsupported_policy["input_gate_id"] == "paper_package_adapter_contract"
    assert (
        unsupported_policy["next_required_gate"]
        == "paper_package_conversion_mapped_subset_plan"
    )
    assert unsupported_policy["package_generation_allowed"] is False
    assert (
        unsupported_policy["coverage_summary"]["paper_primitive_family_policy_row_count"]
        == 6
    )
    assert (
        unsupported_policy["coverage_summary"][
            "current_adapter_decision_policy_row_count"
        ]
        == 16
    )
    assert (
        unsupported_policy["coverage_summary"]["unsupported_policy_blocked_record_count"]
        == 16
    )
    assert (
        unsupported_policy["coverage_summary"]["adapter_contract_blocked_record_count"]
        == 0
    )
    assert unsupported_policy["coverage_summary"]["package_candidate_record_count"] == 0
    assert len(unsupported_policy["paper_primitive_family_policy_rows"]) == 6
    assert len(unsupported_policy["current_adapter_decision_policy_rows"]) == 16
    assert unsupported_policy["package_generation_triggered"] is False
    assert unsupported_policy["newton_runtime_triggered"] is False
    assert unsupported_policy["real_usd_triggered"] is False
    assert unsupported_policy["benchmark_triggered"] is False
    conversion_plan = payload["paper_package_conversion_mapped_subset_plan"]
    assert conversion_plan["gate_id"] == "paper_package_conversion_mapped_subset_plan"
    assert (
        conversion_plan["gate_status"]
        == "implemented_offline_mapped_subset_plan_only_partial"
    )
    assert (
        conversion_plan["input_gate_id"]
        == "paper_package_adapter_unsupported_primitive_policy"
    )
    assert (
        conversion_plan["next_required_gate"]
        == "paper_mapped_subset_conversion_candidate_matrix"
    )
    assert conversion_plan["package_generation_allowed"] is False
    assert (
        conversion_plan["coverage_summary"][
            "paper_primitive_family_conversion_plan_row_count"
        ]
        == 6
    )
    assert (
        conversion_plan["coverage_summary"]["current_row_conversion_plan_row_count"]
        == 16
    )
    assert (
        conversion_plan["coverage_summary"][
            "direct_mapped_current_candidate_record_count"
        ]
        == 0
    )
    assert (
        conversion_plan["coverage_summary"]["excluded_requires_policy_record_count"]
        == 16
    )
    assert conversion_plan["coverage_summary"]["package_candidate_record_count"] == 0
    assert len(conversion_plan["paper_primitive_family_conversion_plan_rows"]) == 6
    assert len(conversion_plan["current_row_conversion_plan_rows"]) == 16
    assert conversion_plan["package_generation_triggered"] is False
    assert conversion_plan["newton_runtime_triggered"] is False
    assert conversion_plan["real_usd_triggered"] is False
    assert conversion_plan["benchmark_triggered"] is False
    candidate_matrix = payload["paper_mapped_subset_conversion_candidate_matrix"]
    assert (
        candidate_matrix["gate_id"]
        == "paper_mapped_subset_conversion_candidate_matrix"
    )
    assert (
        candidate_matrix["input_gate_id"]
        == "paper_package_conversion_mapped_subset_plan"
    )
    assert (
        candidate_matrix["next_required_gate"]
        == "paper_mapped_subset_adapter_preflight_contract"
    )
    assert candidate_matrix["package_generation_allowed"] is False
    assert (
        candidate_matrix["coverage_summary"][
            "future_family_candidate_matrix_row_count"
        ]
        == 6
    )
    assert (
        candidate_matrix["coverage_summary"]["future_family_review_candidate_count"]
        == 3
    )
    assert (
        candidate_matrix["coverage_summary"]["current_row_candidate_matrix_row_count"]
        == 16
    )
    assert (
        candidate_matrix["coverage_summary"][
            "current_package_conversion_candidate_count"
        ]
        == 0
    )
    assert candidate_matrix["primitive_spec_generated"] is False
    assert candidate_matrix["collision_package_generated"] is False
    assert candidate_matrix["runtime_admissibility_checked"] is False
    assert candidate_matrix["newton_support_claimed"] is False
    assert candidate_matrix["package_generation_triggered"] is False
    assert candidate_matrix["newton_runtime_triggered"] is False
    assert candidate_matrix["real_usd_triggered"] is False
    assert candidate_matrix["benchmark_triggered"] is False
    preflight = payload["paper_mapped_subset_adapter_preflight_contract"]
    assert preflight["gate_id"] == "paper_mapped_subset_adapter_preflight_contract"
    assert (
        preflight["input_gate_id"]
        == "paper_mapped_subset_conversion_candidate_matrix"
    )
    assert (
        preflight["next_required_gate"]
        == "paper_mapped_subset_primitivespec_dry_run_contract"
    )
    assert preflight["package_generation_allowed"] is False
    assert (
        preflight["coverage_summary"]["family_preflight_requirement_row_count"]
        == 6
    )
    assert (
        preflight["coverage_summary"]["future_native_family_preflight_record_count"]
        == 3
    )
    assert (
        preflight["coverage_summary"]["current_row_adapter_preflight_row_count"]
        == 16
    )
    assert (
        preflight["coverage_summary"]["current_preflight_pass_record_count"]
        == 0
    )
    assert (
        preflight["coverage_summary"]["current_package_conversion_candidate_count"]
        == 0
    )
    assert preflight["primitive_spec_generated"] is False
    assert preflight["collision_package_generated"] is False
    assert preflight["runtime_admissibility_checked"] is False
    assert preflight["newton_support_claimed"] is False
    assert preflight["package_generation_triggered"] is False
    assert preflight["newton_runtime_triggered"] is False
    assert preflight["real_usd_triggered"] is False
    assert preflight["benchmark_triggered"] is False
    dry_run = payload["paper_mapped_subset_primitivespec_dry_run_contract"]
    assert dry_run["gate_id"] == "paper_mapped_subset_primitivespec_dry_run_contract"
    assert (
        dry_run["input_gate_id"]
        == "paper_mapped_subset_adapter_preflight_contract"
    )
    assert (
        dry_run["next_required_gate"]
        == "paper_mapped_subset_primitivespec_validation_contract"
    )
    assert dry_run["package_generation_allowed"] is False
    assert dry_run["generated_primitive_spec_count"] == 0
    assert (
        dry_run["coverage_summary"]["primitive_spec_requirement_row_count"]
        == 6
    )
    assert (
        dry_run["coverage_summary"][
            "future_native_primitivespec_shape_record_count"
        ]
        == 3
    )
    assert (
        dry_run["coverage_summary"]["current_row_primitivespec_dry_run_row_count"]
        == 16
    )
    assert (
        dry_run["coverage_summary"]["primitive_spec_candidate_record_count"]
        == 0
    )
    assert dry_run["primitive_spec_generated"] is False
    assert dry_run["collision_package_generated"] is False
    assert dry_run["runtime_admissibility_checked"] is False
    assert dry_run["newton_support_claimed"] is False
    assert dry_run["package_generation_triggered"] is False
    assert dry_run["newton_runtime_triggered"] is False
    assert dry_run["real_usd_triggered"] is False
    assert dry_run["benchmark_triggered"] is False
    validation = payload["paper_mapped_subset_primitivespec_validation_contract"]
    assert (
        validation["gate_id"]
        == "paper_mapped_subset_primitivespec_validation_contract"
    )
    assert (
        validation["input_gate_id"]
        == "paper_mapped_subset_primitivespec_dry_run_contract"
    )
    assert (
        validation["next_required_gate"]
        == "paper_mapped_subset_primitivespec_generation_preflight_contract"
    )
    assert validation["package_generation_allowed"] is False
    assert validation["validated_primitive_spec_candidate_count"] == 0
    assert validation["generated_primitive_spec_count"] == 0
    assert (
        validation["coverage_summary"][
            "primitive_spec_validation_requirement_row_count"
        ]
        == 6
    )
    assert (
        validation["coverage_summary"][
            "future_native_primitivespec_shape_validation_count"
        ]
        == 3
    )
    assert (
        validation["coverage_summary"][
            "current_row_primitivespec_validation_row_count"
        ]
        == 16
    )
    assert (
        validation["coverage_summary"][
            "validated_primitive_spec_candidate_record_count"
        ]
        == 0
    )
    assert validation["primitive_spec_generated"] is False
    assert validation["collision_package_generated"] is False
    assert validation["runtime_admissibility_checked"] is False
    assert validation["newton_support_claimed"] is False
    assert validation["package_generation_triggered"] is False
    assert validation["newton_runtime_triggered"] is False
    assert validation["real_usd_triggered"] is False
    assert validation["benchmark_triggered"] is False
    generation_preflight = payload[
        "paper_mapped_subset_primitivespec_generation_preflight_contract"
    ]
    assert (
        generation_preflight["gate_id"]
        == "paper_mapped_subset_primitivespec_generation_preflight_contract"
    )
    assert (
        generation_preflight["input_gate_id"]
        == "paper_mapped_subset_primitivespec_validation_contract"
    )
    assert (
        generation_preflight["next_required_gate"]
        == "paper_mapped_subset_primitivespec_generation_contract"
    )
    assert generation_preflight["generation_preflight_candidate_count"] == 0
    assert generation_preflight["generated_primitive_spec_count"] == 0
    assert generation_preflight["generated_collision_package_count"] == 0
    assert generation_preflight["runtime_admissibility_check_count"] == 0
    assert (
        generation_preflight["coverage_summary"][
            "primitive_spec_generation_preflight_requirement_row_count"
        ]
        == 6
    )
    assert (
        generation_preflight["coverage_summary"][
            "future_native_primitivespec_generation_preflight_count"
        ]
        == 3
    )
    assert (
        generation_preflight["coverage_summary"][
            "current_row_primitivespec_generation_preflight_row_count"
        ]
        == 16
    )
    assert (
        generation_preflight["coverage_summary"][
            "generation_preflight_candidate_record_count"
        ]
        == 0
    )
    family_rows = {
        row["paper_primitive"]: row
        for row in generation_preflight[
            "primitive_spec_generation_preflight_requirement_rows"
        ]
    }
    assert list(family_rows) == [
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
    assert family_rows["oriented_bounding_box"][
        "primitive_spec_generation_preflight_decision"
    ] == "future_native_family_generation_requirement_preflighted"
    assert (
        family_rows["oriented_bounding_box"]["validated_future_primitive_spec_kind"]
        == "box"
    )
    assert (
        family_rows["capped_cylinder"][
            "primitive_spec_generation_preflight_decision"
        ]
        == "blocked_approximation_policy_generation_preflight_recorded"
    )
    assert (
        family_rows["trapezoidal_prism"][
            "primitive_spec_generation_preflight_decision"
        ]
        == "noop_unmapped_family_generation_preflight_recorded"
    )
    current_rows = generation_preflight[
        "current_row_primitivespec_generation_preflight_rows"
    ]
    assert len(current_rows) == 16
    for row in current_rows:
        assert row["primitive_spec_generation_preflight_decision"] == (
            "skip_unmapped_current_row_preflighted"
        )
        assert row["primitive_spec_generation_preflight_action"] == "keep_offline"
        assert row["primitive_spec_generation_candidate"] is False
        assert row["generated_primitive_spec"] is None
        assert (
            row["required_later_gate"]
            == "paper_mapped_subset_primitivespec_generation_contract"
        )
        assert row["primitive_spec_generation_triggered"] is False
        assert row["collision_package_generation_triggered"] is False
        assert row["runtime_admissibility_triggered"] is False
    assert generation_preflight["primitive_spec_generated"] is False
    assert generation_preflight["collision_package_generated"] is False
    assert generation_preflight["runtime_admissibility_checked"] is False
    assert generation_preflight["newton_support_claimed"] is False
    assert generation_preflight["package_generation_triggered"] is False
    assert generation_preflight["newton_runtime_triggered"] is False
    assert generation_preflight["real_usd_triggered"] is False
    assert generation_preflight["benchmark_triggered"] is False
    generation = payload["paper_mapped_subset_primitivespec_generation_contract"]
    assert (
        generation["gate_id"]
        == "paper_mapped_subset_primitivespec_generation_contract"
    )
    assert (
        generation["input_gate_id"]
        == "paper_mapped_subset_primitivespec_generation_preflight_contract"
    )
    assert (
        generation["next_required_gate"]
        == "paper_mapped_subset_primitivespec_candidate_source_contract"
    )
    assert generation["primitive_spec_generation_candidate_count"] == 0
    assert generation["offline_primitivespec_template_count"] == 3
    assert generation["generated_primitive_spec_count"] == 0
    assert generation["generated_collision_package_count"] == 0
    assert generation["runtime_admissibility_check_count"] == 0
    assert len(generation["native_family_primitivespec_template_rows"]) == 3
    assert len(generation["blocked_primitivespec_generation_requirement_rows"]) == 2
    assert len(generation["noop_primitivespec_generation_requirement_rows"]) == 1
    assert len(generation["current_row_primitivespec_generation_rows"]) == 16
    assert (
        generation["coverage_summary"][
            "primitive_spec_generation_requirement_row_count"
        ]
        == 6
    )
    assert (
        generation["coverage_summary"]["current_row_primitivespec_generation_row_count"]
        == 16
    )
    assert (
        generation["coverage_summary"][
            "primitive_spec_generation_candidate_record_count"
        ]
        == 0
    )
    assert (
        generation["coverage_summary"]["offline_primitivespec_template_record_count"]
        == 3
    )
    assert generation["primitive_spec_generated"] is False
    assert generation["collision_package_generated"] is False
    assert generation["runtime_admissibility_checked"] is False
    assert generation["newton_support_claimed"] is False
    assert generation["package_generation_triggered"] is False
    assert generation["newton_runtime_triggered"] is False
    assert generation["real_usd_triggered"] is False
    assert generation["benchmark_triggered"] is False
    candidate_source = payload[
        "paper_mapped_subset_primitivespec_candidate_source_contract"
    ]
    assert (
        candidate_source["gate_id"]
        == "paper_mapped_subset_primitivespec_candidate_source_contract"
    )
    assert (
        candidate_source["input_gate_id"]
        == "paper_mapped_subset_primitivespec_generation_contract"
    )
    assert (
        candidate_source["next_required_gate"]
        == "paper_mapped_subset_native_current_fixture_contract"
    )
    assert candidate_source["eligible_current_candidate_source_count"] == 0
    assert candidate_source["primitive_spec_generation_candidate_count"] == 0
    assert candidate_source["generated_primitive_spec_count"] == 0
    assert candidate_source["generated_collision_package_count"] == 0
    assert candidate_source["runtime_admissibility_check_count"] == 0
    assert len(candidate_source["native_template_candidate_source_audit_rows"]) == 3
    assert len(candidate_source["blocked_family_candidate_source_audit_rows"]) == 2
    assert len(candidate_source["noop_family_candidate_source_audit_rows"]) == 1
    assert len(candidate_source["current_row_candidate_source_audit_rows"]) == 16
    assert (
        candidate_source["coverage_summary"]["eligible_current_candidate_source_count"]
        == 0
    )
    assert (
        candidate_source["coverage_summary"][
            "current_row_candidate_source_audit_row_count"
        ]
        == 16
    )
    assert candidate_source["primitive_spec_generated"] is False
    assert candidate_source["collision_package_generated"] is False
    assert candidate_source["runtime_admissibility_checked"] is False
    assert candidate_source["newton_support_claimed"] is False
    assert candidate_source["package_generation_triggered"] is False
    assert candidate_source["newton_runtime_triggered"] is False
    assert candidate_source["real_usd_triggered"] is False
    assert candidate_source["benchmark_triggered"] is False
    native_fixture = payload["paper_mapped_subset_native_current_fixture_contract"]
    assert (
        native_fixture["gate_id"]
        == "paper_mapped_subset_native_current_fixture_contract"
    )
    assert (
        native_fixture["input_gate_id"]
        == "paper_mapped_subset_primitivespec_candidate_source_contract"
    )
    assert (
        native_fixture["next_required_gate"]
        == "paper_mapped_subset_primitivespec_native_fixture_generation_contract"
    )
    assert native_fixture["eligible_current_candidate_source_count"] == 1
    assert native_fixture["primitive_spec_generation_candidate_count"] == 1
    assert native_fixture["generated_primitive_spec_count"] == 0
    assert native_fixture["generated_collision_package_count"] == 0
    assert native_fixture["runtime_admissibility_check_count"] == 0
    assert len(native_fixture["native_current_fixture_source_rows"]) == 1
    native_fixture_row = native_fixture["native_current_fixture_source_rows"][0]
    assert native_fixture_row["fixture_id"] == "paper_single_box"
    assert native_fixture_row["paper_primitive"] == "oriented_bounding_box"
    assert native_fixture_row["primitive_spec_kind"] == "box"
    assert native_fixture_row["candidate_mapping_label"] == "box"
    assert native_fixture_row["newton_runtime_kind"] == "box"
    assert native_fixture_row["eligible_current_candidate_source"] is True
    assert native_fixture_row["primitive_spec_generation_candidate"] is True
    assert native_fixture_row["generated_primitive_spec"] is None
    assert native_fixture["primitive_spec_generated"] is False
    assert native_fixture["collision_package_generated"] is False
    assert native_fixture["runtime_admissibility_checked"] is False
    assert native_fixture["newton_support_claimed"] is False
    assert native_fixture["package_generation_triggered"] is False
    assert native_fixture["newton_runtime_triggered"] is False
    assert native_fixture["real_usd_triggered"] is False
    assert native_fixture["benchmark_triggered"] is False
    native_generation = payload[
        "paper_mapped_subset_primitivespec_native_fixture_generation_contract"
    ]
    assert (
        native_generation["gate_id"]
        == "paper_mapped_subset_primitivespec_native_fixture_generation_contract"
    )
    assert (
        native_generation["input_gate_id"]
        == "paper_mapped_subset_native_current_fixture_contract"
    )
    assert (
        native_generation["next_required_gate"]
        == "paper_mapped_subset_primitivespec_native_fixture_serialization_contract"
    )
    assert native_generation["primitive_spec_generation_candidate_count"] == 1
    assert native_generation["offline_serialized_primitivespec_like_dict_count"] == 1
    assert native_generation["generated_runtime_primitive_spec_count"] == 0
    assert native_generation["generated_primitive_spec_count"] == 0
    assert native_generation["generated_collision_package_count"] == 0
    assert native_generation["runtime_admissibility_check_count"] == 0
    assert len(native_generation["native_fixture_primitivespec_generation_rows"]) == 1
    native_generation_row = native_generation[
        "native_fixture_primitivespec_generation_rows"
    ][0]
    generated_spec = native_generation_row[
        "offline_serialized_primitivespec_like_dict"
    ]
    assert native_generation_row["fixture_id"] == "paper_single_box"
    assert native_generation_row["primitive_spec_kind"] == "box"
    assert native_generation_row["generated_primitive_spec"] is None
    assert native_generation_row["runtime_instance_generated"] is False
    assert generated_spec["primitive_id"] == "paper_single_box__oriented_bounding_box__box"
    assert generated_spec["kind"] == "box"
    assert generated_spec["pose"] == []
    assert generated_spec["frame"] == "asset"
    assert generated_spec["dimensions"] == {
        "half_extents": native_fixture_row["half_extents"]
    }
    assert generated_spec["center"] == native_fixture_row["center"]
    assert generated_spec["axes"] == native_fixture_row["axes"]
    assert generated_spec["source_faces"] == native_fixture_row["fixture_source_faces"]
    assert generated_spec["contains_assigned_points"] is True
    assert generated_spec["conversion_status"] == (
        "report_only_offline_serialized_primitivespec_like_dict_not_runtime_object"
    )
    assert native_generation["primitive_spec_generated"] is False
    assert native_generation["collision_package_generated"] is False
    assert native_generation["runtime_admissibility_checked"] is False
    assert native_generation["newton_support_claimed"] is False
    assert native_generation["package_generation_triggered"] is False
    assert native_generation["newton_runtime_triggered"] is False
    assert native_generation["real_usd_triggered"] is False
    assert native_generation["benchmark_triggered"] is False
    native_serialization = payload[
        "paper_mapped_subset_primitivespec_native_fixture_serialization_contract"
    ]
    assert (
        native_serialization["gate_id"]
        == "paper_mapped_subset_primitivespec_native_fixture_serialization_contract"
    )
    assert (
        native_serialization["input_gate_id"]
        == "paper_mapped_subset_primitivespec_native_fixture_generation_contract"
    )
    assert (
        native_serialization["next_required_gate"]
        == "paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract"
    )
    assert native_serialization["serialized_primitivespec_like_dict_count"] == 1
    assert native_serialization["json_serialization_check_count"] == 1
    assert native_serialization["json_round_trip_match_count"] == 1
    assert native_serialization["schema_stability_check_count"] == 1
    assert native_serialization["generated_runtime_primitive_spec_count"] == 0
    assert native_serialization["generated_primitive_spec_count"] == 0
    assert native_serialization["generated_collision_package_count"] == 0
    assert native_serialization["runtime_admissibility_check_count"] == 0
    assert len(native_serialization["serialization_rows"]) == 1
    native_serialization_row = native_serialization["serialization_rows"][0]
    assert native_serialization_row["fixture_id"] == "paper_single_box"
    assert native_serialization_row["primitive_spec_kind"] == "box"
    assert native_serialization_row["generated_primitive_spec"] is None
    assert native_serialization_row["runtime_instance_generated"] is False
    assert native_serialization_row["serialized_payload"] == generated_spec
    assert json.loads(
        native_serialization_row["canonical_primitivespec_json"]
    ) == generated_spec
    assert native_serialization_row["json_round_trip_equal"] is True
    assert native_serialization_row["canonical_json_stable"] is True
    assert native_serialization["primitive_spec_generated"] is False
    assert native_serialization["collision_package_generated"] is False
    assert native_serialization["runtime_admissibility_checked"] is False
    assert native_serialization["newton_support_claimed"] is False
    assert native_serialization["package_generation_triggered"] is False
    assert native_serialization["newton_runtime_triggered"] is False
    assert native_serialization["real_usd_triggered"] is False
    assert native_serialization["benchmark_triggered"] is False
    runtime_boundary = payload[
        "paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract"
    ]
    assert (
        runtime_boundary["gate_id"]
        == "paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract"
    )
    assert (
        runtime_boundary["input_gate_id"]
        == "paper_mapped_subset_primitivespec_native_fixture_serialization_contract"
    )
    assert (
        runtime_boundary["next_required_gate"]
        == "paper_mapped_subset_primitivespec_runtime_construction_contract"
    )
    assert runtime_boundary["runtime_boundary_preflight_row_count"] == 1
    assert (
        runtime_boundary["later_runtime_primitivespec_construction_candidate_count"]
        == 1
    )
    assert runtime_boundary["runtime_construction_allowed_in_current_gate"] is False
    assert runtime_boundary["generated_runtime_primitive_spec_count"] == 0
    assert runtime_boundary["generated_primitive_spec_count"] == 0
    assert runtime_boundary["generated_collision_package_count"] == 0
    assert runtime_boundary["runtime_admissibility_check_count"] == 0
    assert len(runtime_boundary["runtime_boundary_preflight_rows"]) == 1
    runtime_boundary_row = runtime_boundary["runtime_boundary_preflight_rows"][0]
    assert runtime_boundary_row["fixture_id"] == "paper_single_box"
    assert runtime_boundary_row["primitive_spec_kind"] == "box"
    assert runtime_boundary_row["later_runtime_primitivespec_construction_candidate"] is True
    assert runtime_boundary_row["runtime_construction_allowed_in_current_gate"] is False
    assert (
        runtime_boundary_row["required_later_gate"]
        == "paper_mapped_subset_primitivespec_runtime_construction_contract"
    )
    assert runtime_boundary_row["generated_primitive_spec"] is None
    assert runtime_boundary_row["runtime_instance_generated"] is False
    assert runtime_boundary["primitive_spec_generated"] is False
    assert runtime_boundary["collision_package_generated"] is False
    assert runtime_boundary["runtime_admissibility_checked"] is False
    assert runtime_boundary["newton_support_claimed"] is False
    assert runtime_boundary["package_generation_triggered"] is False
    assert runtime_boundary["newton_runtime_triggered"] is False
    assert runtime_boundary["real_usd_triggered"] is False
    assert runtime_boundary["benchmark_triggered"] is False
    runtime_construction = payload[
        "paper_mapped_subset_primitivespec_runtime_construction_contract"
    ]
    assert (
        runtime_construction["gate_id"]
        == "paper_mapped_subset_primitivespec_runtime_construction_contract"
    )
    assert (
        runtime_construction["input_gate_id"]
        == "paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract"
    )
    assert (
        runtime_construction["next_required_gate"]
        == "paper_mapped_subset_collision_package_generation_preflight_contract"
    )
    assert runtime_construction["runtime_construction_row_count"] == 1
    assert runtime_construction["constructed_runtime_primitivespec_count"] == 1
    assert runtime_construction["generated_runtime_primitive_spec_count"] == 1
    assert runtime_construction["generated_primitive_spec_count"] == 1
    assert runtime_construction["generated_collision_package_count"] == 0
    assert runtime_construction["runtime_admissibility_check_count"] == 0
    runtime_construction_row = runtime_construction["runtime_construction_rows"][0]
    expected_constructed_spec = {
        **generated_spec,
        "conversion_status": (
            "runtime_primitivespec_constructed_from_canonical_preflight_payload"
        ),
    }
    assert runtime_construction_row["loaded_primitivespec_payload"] == generated_spec
    assert (
        runtime_construction_row["constructed_primitivespec_dict"]
        == expected_constructed_spec
    )
    assert runtime_construction_row["generated_primitive_spec"] == expected_constructed_spec
    assert runtime_construction_row["runtime_instance_generated"] is True
    assert runtime_construction["collision_package_generated"] is False
    assert runtime_construction["runtime_admissibility_checked"] is False
    assert runtime_construction["newton_support_claimed"] is False
    assert runtime_construction["package_generation_triggered"] is False
    assert runtime_construction["newton_runtime_triggered"] is False
    assert runtime_construction["real_usd_triggered"] is False
    assert runtime_construction["benchmark_triggered"] is False
    package_preflight = payload[
        "paper_mapped_subset_collision_package_generation_preflight_contract"
    ]
    assert package_preflight["gate_id"] == (
        "paper_mapped_subset_collision_package_generation_preflight_contract"
    )
    assert package_preflight["input_gate_id"] == (
        "paper_mapped_subset_primitivespec_runtime_construction_contract"
    )
    assert package_preflight["next_required_gate"] == (
        "paper_mapped_subset_collision_package_generation_contract"
    )
    assert package_preflight["package_generation_preflight_row_count"] == 1
    assert package_preflight["later_collision_package_generation_candidate_count"] == 1
    assert package_preflight["package_generation_allowed_in_current_gate"] is False
    assert package_preflight["generated_runtime_primitive_spec_count"] == 1
    assert package_preflight["generated_primitive_spec_count"] == 1
    assert package_preflight["generated_collision_package_count"] == 0
    assert package_preflight["runtime_admissibility_check_count"] == 0
    package_preflight_row = package_preflight["package_generation_preflight_rows"][0]
    assert package_preflight_row["candidate_primitivespec_dict"] == (
        runtime_construction_row["generated_primitive_spec"]
    )
    assert package_preflight_row["candidate_package_primitive_kind"] == "box"
    assert package_preflight_row["later_collision_package_generation_candidate"] is True
    assert package_preflight_row["package_generation_allowed_in_current_gate"] is False
    assert package_preflight_row["generated_collision_package"] is None
    assert package_preflight["collision_package_generated"] is False
    assert package_preflight["runtime_admissibility_checked"] is False
    assert package_preflight["newton_support_claimed"] is False
    assert package_preflight["package_generation_triggered"] is False
    assert package_preflight["newton_runtime_triggered"] is False
    assert package_preflight["real_usd_triggered"] is False
    assert package_preflight["benchmark_triggered"] is False
    package_generation = payload[
        "paper_mapped_subset_collision_package_generation_contract"
    ]
    assert package_generation["gate_id"] == (
        "paper_mapped_subset_collision_package_generation_contract"
    )
    assert package_generation["input_gate_id"] == (
        "paper_mapped_subset_collision_package_generation_preflight_contract"
    )
    assert package_generation["next_required_gate"] == (
        "paper_mapped_subset_runtime_admissibility_preflight_contract"
    )
    assert package_generation["collision_package_generation_row_count"] == 1
    assert package_generation["generated_collision_package_count"] == 1
    assert package_generation["runtime_admissibility_check_count"] == 0
    package_generation_row = package_generation["collision_package_generation_rows"][0]
    generated_package = package_generation_row["generated_collision_package"]
    assert generated_package["asset_id"] == "paper_single_box"
    assert generated_package["status"] == (
        "offline_synthetic_candidate_runtime_admissibility_not_checked"
    )
    assert generated_package["primitive_subset"] == ["box"]
    assert generated_package["unsupported_primitives"] == []
    assert "not_paper_vocabulary" in generated_package["claim_boundary"]
    assert generated_package["primitives"] == [
        package_preflight_row["candidate_primitivespec_dict"]
    ]
    assert package_generation["collision_package_generated"] is True
    assert package_generation["runtime_admissibility_checked"] is False
    assert package_generation["newton_support_claimed"] is False
    assert package_generation["newton_runtime_triggered"] is False
    assert package_generation["real_usd_triggered"] is False
    assert package_generation["benchmark_triggered"] is False
    runtime_preflight = payload[
        "paper_mapped_subset_runtime_admissibility_preflight_contract"
    ]
    assert runtime_preflight["gate_id"] == (
        "paper_mapped_subset_runtime_admissibility_preflight_contract"
    )
    assert runtime_preflight["input_gate_id"] == (
        "paper_mapped_subset_collision_package_generation_contract"
    )
    assert runtime_preflight["next_required_gate"] == (
        "paper_mapped_subset_runtime_admissibility_contract"
    )
    assert runtime_preflight["runtime_admissibility_preflight_row_count"] == 1
    assert runtime_preflight["later_runtime_admissibility_candidate_count"] == 1
    assert runtime_preflight["generated_collision_package_count"] == 1
    assert runtime_preflight["runtime_admissibility_check_count"] == 0
    runtime_preflight_row = runtime_preflight[
        "runtime_admissibility_preflight_rows"
    ][0]
    assert runtime_preflight_row["source_package_id"] == (
        generated_package["package_id"]
    )
    assert runtime_preflight_row["source_asset_id"] == "paper_single_box"
    assert runtime_preflight_row["source_package_status"] == (
        "offline_synthetic_candidate_runtime_admissibility_not_checked"
    )
    assert runtime_preflight_row["source_package_primitive_subset"] == ["box"]
    assert runtime_preflight_row["source_package_unsupported_primitives"] == []
    assert runtime_preflight_row["later_runtime_admissibility_candidate"] is True
    assert runtime_preflight["source_collision_package_available"] is True
    assert runtime_preflight["runtime_admissibility_checked"] is False
    assert runtime_preflight["runtime_admissibility_triggered"] is False
    assert runtime_preflight["runtime_admissibility_supported"] is False
    assert runtime_preflight["newton_support_claimed"] is False
    assert runtime_preflight["newton_runtime_triggered"] is False
    assert runtime_preflight["real_usd_triggered"] is False
    assert runtime_preflight["benchmark_triggered"] is False
    runtime_admissibility = payload[
        "paper_mapped_subset_runtime_admissibility_contract"
    ]
    assert runtime_admissibility["gate_id"] == (
        "paper_mapped_subset_runtime_admissibility_contract"
    )
    assert runtime_admissibility["input_gate_id"] == (
        "paper_mapped_subset_runtime_admissibility_preflight_contract"
    )
    assert runtime_admissibility["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_mapping_preflight_contract"
    )
    assert runtime_admissibility["runtime_admissibility_row_count"] == 1
    assert (
        runtime_admissibility[
            "offline_static_runtime_admissibility_check_count"
        ]
        == 1
    )
    assert runtime_admissibility["runtime_admissibility_check_count"] == 1
    assert runtime_admissibility["runtime_execution_count"] == 0
    assert runtime_admissibility["newton_mapping_record_count"] == 0
    assert runtime_admissibility["newton_runtime_execution_count"] == 0
    runtime_admissibility_row = runtime_admissibility[
        "runtime_admissibility_rows"
    ][0]
    assert runtime_admissibility_row["source_package_id"] == (
        generated_package["package_id"]
    )
    assert (
        runtime_admissibility_row[
            "offline_static_runtime_admissibility_check_passed"
        ]
        is True
    )
    assert (
        runtime_admissibility_row["runtime_admissibility_status"]
        == "offline_static_admissible_for_later_newton_shape_mapping_preflight"
    )
    assert runtime_admissibility["newton_support_claimed"] is False
    assert runtime_admissibility["newton_runtime_triggered"] is False
    assert runtime_admissibility["real_usd_triggered"] is False
    assert runtime_admissibility["benchmark_triggered"] is False
    mapping_preflight = payload[
        "paper_mapped_subset_newton_shape_mapping_preflight_contract"
    ]
    assert mapping_preflight["gate_id"] == (
        "paper_mapped_subset_newton_shape_mapping_preflight_contract"
    )
    assert mapping_preflight["input_gate_id"] == (
        "paper_mapped_subset_runtime_admissibility_contract"
    )
    assert mapping_preflight["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_mapping_contract"
    )
    assert mapping_preflight["newton_shape_mapping_preflight_row_count"] == 1
    assert mapping_preflight["mapping_attempt_count"] == 0
    assert mapping_preflight["newton_mapping_record_count"] == 0
    assert mapping_preflight["newton_runtime_execution_count"] == 0
    assert (
        mapping_preflight["newton_shape_mapping_preflight_rows"][0][
            "target_newton_shape_kind"
        ]
        == "box"
    )
    assert (
        mapping_preflight["newton_shape_mapping_preflight_rows"][0][
            "newton_shape_support_evidence_status"
        ]
        == "pending_later_mapping_contract_no_support_claim"
    )
    mapping_contract = payload[
        "paper_mapped_subset_newton_shape_mapping_contract"
    ]
    assert mapping_contract["gate_id"] == (
        "paper_mapped_subset_newton_shape_mapping_contract"
    )
    assert mapping_contract["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"
    )
    assert mapping_contract["shape_mapping_contract_row_count"] == 1
    assert mapping_contract["report_scoped_newton_shape_descriptor_count"] == 1
    assert mapping_contract["newton_shape_object_count"] == 0
    runtime_boundary = payload[
        "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"
    ]
    assert runtime_boundary["gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"
    )
    assert runtime_boundary["input_gate_id"] == (
        "paper_mapped_subset_newton_shape_mapping_contract"
    )
    assert runtime_boundary["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_construction_contract"
    )
    assert (
        runtime_boundary[
            "newton_shape_runtime_boundary_preflight_row_count"
        ]
        == 1
    )
    assert (
        runtime_boundary[
            "later_newton_shape_runtime_construction_candidate_count"
        ]
        == 1
    )
    assert runtime_boundary["mapping_attempt_count"] == 0
    assert runtime_boundary["newton_mapping_record_count"] == 0
    assert runtime_boundary["newton_shape_object_count"] == 0
    assert runtime_boundary["newton_runtime_execution_count"] == 0
    assert (
        runtime_boundary["newton_shape_runtime_boundary_preflight_rows"][0][
            "target_newton_shape_kind"
        ]
        == "box"
    )
    runtime_construction = payload[
        "paper_mapped_subset_newton_shape_runtime_construction_contract"
    ]
    assert runtime_construction["gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_construction_contract"
    )
    assert runtime_construction["input_gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"
    )
    assert runtime_construction["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_builder_preflight_contract"
    )
    assert runtime_construction["newton_shape_runtime_construction_row_count"] == 1
    assert runtime_construction["constructed_newton_shape_mapping_record_count"] == 1
    assert runtime_construction["newton_mapping_record_count"] == 1
    assert runtime_construction["newton_mapper_call_count"] == 0
    assert runtime_construction["newton_shape_object_count"] == 0
    assert runtime_construction["newton_engine_shape_object_count"] == 0
    assert runtime_construction["newton_builder_shape_call_count"] == 0
    assert runtime_construction["newton_runtime_execution_count"] == 0
    assert runtime_construction["newton_shape_runtime_construction_rows"][0][
        "constructed_newton_shape_mapping_dict"
    ]["kind"] == "box"
    assert changed_contract["real_usd_triggered"] is False
    assert changed_contract["benchmark_triggered"] is False
    review = payload["paper_fixture_breadth_completion_review"]
    assert review["closed_gate"] == "paper_fixture_breadth_expansion"
    assert review["fixture_breadth_plan_complete"] is True
    assert review["paper_faithful_offline_allowed"] is False
    assert review["next_required_gate"] == "paper_faithful_offline_generalization_plan"
    assert [batch["batch_id"] for batch in review["completed_batches"]] == [
        "paper_fixture_breadth_batch_a",
        "paper_fixture_breadth_batch_b",
        "paper_fixture_breadth_batch_c",
        "paper_fixture_breadth_batch_d",
        "paper_fixture_breadth_batch_e",
    ]
    assert review["package_generation_triggered"] is False
    assert review["newton_runtime_triggered"] is False
    assert review["real_usd_triggered"] is False
    assert review["benchmark_triggered"] is False
    scope_audit = payload["paper_faithful_offline_scope_audit"]
    assert scope_audit["decision"] == "remain_partial"
    assert scope_audit["paper_faithful_offline_allowed"] is False
    assert [row["criterion_id"] for row in scope_audit["criteria"]] == [
        "source_mesh_and_preprocessing_policy",
        "source_face_intake_policy",
        "operator_q_audit",
        "primitive_vocabulary_and_fit",
        "paper_collapse_cost_and_weighting",
        "greedy_priority_queue_trace",
        "target_count_and_threshold_stop",
        "component_pair_edge_handling",
        "enclosed_primitive_postprocess",
        "report_schema_tests_and_records",
        "package_generation_boundary",
        "newton_runtime_boundary",
        "real_usd_boundary",
        "benchmark_evaluation_boundary",
    ]
    case_ids = [case["case_id"] for case in payload["cases"]]
    assert {
        "paper_single_box",
        "paper_two_face_merge",
        "paper_three_face_chain",
        "paper_disconnected_components",
        "paper_component_pair_threshold_blocked",
        "paper_tiny_sphere_clamp",
        "paper_duplicate_vertex_preprocessing",
        "paper_frustum_like",
        "paper_trapezoid_prism_like",
        "paper_nested_primitive",
        "paper_quad_face_intake",
        "paper_polygon_face_intake",
        "paper_mixed_face_preprocess_operator",
        "paper_degenerate_preprocess_face_drop",
        "paper_concave_polygon_rejected",
        "paper_rotated_box_fit",
        "paper_offset_sphere_fit",
        "paper_off_axis_capsule_fit",
        "paper_flat_capped_cylinder_axis_fit",
        "paper_tapered_frustum_fit",
        "paper_asymmetric_trapezoid_fit",
        "paper_branching_cost_order",
        "paper_equal_cost_queue_tie",
        "paper_nonzero_threshold_block",
        "paper_component_pair_multi_candidate_order",
        "paper_component_pair_cap_skipped",
        "paper_rotated_nested_primitive",
        "paper_cross_type_enclosure_boundary",
    }.issubset(set(case_ids))
    assert case_ids[:15] == [
        "paper_single_box",
        "paper_two_face_merge",
        "paper_three_face_chain",
        "paper_disconnected_components",
        "paper_component_pair_threshold_blocked",
        "paper_tiny_sphere_clamp",
        "paper_duplicate_vertex_preprocessing",
        "paper_frustum_like",
        "paper_trapezoid_prism_like",
        "paper_nested_primitive",
        "paper_quad_face_intake",
        "paper_polygon_face_intake",
        "paper_mixed_face_preprocess_operator",
        "paper_degenerate_preprocess_face_drop",
        "paper_concave_polygon_rejected",
    ]
    single_box = payload["cases"][0]
    candidate_names = [
        row["paper_primitive"]
        for row in single_box["primitive_fit_audit"]["candidates"]
    ]
    assert len(candidate_names) == len(set(candidate_names))
    candidates = {row["paper_primitive"]: row for row in single_box["primitive_fit_audit"]["candidates"]}
    assert candidates["oriented_bounding_box"]["implementation_status"] == (
        "paper_shaped_offline_fit_audit"
    )
    assert candidates["oriented_bounding_box"]["axis_matrix_layout"] == "rows_are_axes"
    assert candidates["oriented_bounding_box"]["primitive_parameter_lower_clamp"] == 1e-3
    assert candidates["oriented_bounding_box"]["center"]
    assert candidates["oriented_bounding_box"]["axes"]
    obb_dims = candidates["oriented_bounding_box"]["dimensions"]
    assert obb_dims["lower_bounds"]
    assert obb_dims["upper_bounds"]
    assert obb_dims["paper_center_local"]
    assert obb_dims["paper_center_world"] == candidates["oriented_bounding_box"]["center"]
    assert obb_dims["axis_order_policy"] == "descending_abs_q_eigenvalue"
    assert obb_dims["volume_formula"] == "8*hx*hy*hz"
    assert candidates["sphere"]["implementation_status"] == "paper_shaped_offline_fit_audit"
    assert candidates["sphere"]["primitive_parameter_lower_clamp"] == 1e-3
    assert candidates["sphere"]["center"] == candidates["oriented_bounding_box"]["center"]
    assert candidates["sphere"]["axes"] == candidates["oriented_bounding_box"]["axes"]
    sphere_dims = candidates["sphere"]["dimensions"]
    assert sphere_dims["radius"]
    assert sphere_dims["unclamped_radius"]
    assert sphere_dims["center_source"] == "paper_obb_center"
    assert sphere_dims["radius_source"] == "max_distance_from_obb_center_clamped"
    assert sphere_dims["volume_formula"] == "4/3*pi*r^3"

    duplicate_case = [
        case
        for case in payload["cases"]
        if case["case_id"] == "paper_duplicate_vertex_preprocessing"
    ][0]
    duplicate_audit = duplicate_case["preprocessing_audit"]
    assert duplicate_audit["preprocessing_policy"] == (
        "exact_coordinate_deduplication_for_fixture"
    )
    assert duplicate_audit["input_vertex_count"] == 6
    assert duplicate_audit["deduplicated_vertex_count"] == 4
    assert duplicate_audit["duplicate_clusters"] == [[0, 3], [1, 4]]
    assert duplicate_audit["original_to_deduplicated_vertex_ids"] == [
        0,
        1,
        2,
        0,
        1,
        3,
    ]
    assert duplicate_audit["connected_component_count_before"] == 2
    assert duplicate_audit["connected_component_count_after"] == 1
    assert duplicate_audit["topology_changed"] is True
    assert duplicate_case["source_mesh"]["source_face_remap"] == (
        "duplicate_vertex_preprocessing_face_id_preserving"
    )
    assert duplicate_case["collapse_trace"]["preprocessing_boundary"] == (
        "exact_coordinate_duplicate_vertex_fixture"
    )
    assert duplicate_case["collapse_trace"]["initial_edge_count"] == 1

    batch_a_cases = {
        case["case_id"]: case
        for case in payload["cases"]
        if case["case_id"]
        in {
            "paper_mixed_face_preprocess_operator",
            "paper_degenerate_preprocess_face_drop",
            "paper_concave_polygon_rejected",
        }
    }
    assert set(batch_a_cases) == {
        "paper_mixed_face_preprocess_operator",
        "paper_degenerate_preprocess_face_drop",
        "paper_concave_polygon_rejected",
    }
    assert batch_a_cases["paper_mixed_face_preprocess_operator"][
        "fixture_breadth_batch"
    ] == "paper_fixture_breadth_batch_a"
    mixed_aggregate = batch_a_cases["paper_mixed_face_preprocess_operator"][
        "operator_audit"
    ]["source_face_operator_aggregates"][0]
    assert mixed_aggregate["eigenvalues"]
    assert mixed_aggregate["eigenvector_matrix_layout"] == "columns_are_eigenvectors"
    assert batch_a_cases["paper_degenerate_preprocess_face_drop"][
        "preprocessing_audit"
    ]["degenerate_face_dropped_count"] == 1
    assert batch_a_cases["paper_degenerate_preprocess_face_drop"][
        "primitive_fit_audit"
    ]["source_faces"] == [1]
    concave_case = batch_a_cases["paper_concave_polygon_rejected"]
    assert concave_case["case_status"] == "unsupported_fixture_policy"
    assert concave_case["mesh_intake_policy_audit"]["failure_label"] == (
        "source_face_intake_unsupported_concave_polygon"
    )
    assert "primitive_fit_audits" not in concave_case

    batch_b_cases = {
        case["case_id"]: case
        for case in payload["cases"]
        if case["case_id"]
        in {
            "paper_rotated_box_fit",
            "paper_offset_sphere_fit",
            "paper_off_axis_capsule_fit",
            "paper_flat_capped_cylinder_axis_fit",
            "paper_tapered_frustum_fit",
            "paper_asymmetric_trapezoid_fit",
        }
    }
    assert set(batch_b_cases) == {
        "paper_rotated_box_fit",
        "paper_offset_sphere_fit",
        "paper_off_axis_capsule_fit",
        "paper_flat_capped_cylinder_axis_fit",
        "paper_tapered_frustum_fit",
        "paper_asymmetric_trapezoid_fit",
    }
    for case in batch_b_cases.values():
        assert case["fixture_breadth_batch"] == "paper_fixture_breadth_batch_b"
        assert case["package_generation_triggered"] is False
        assert case["newton_runtime_triggered"] is False
        assert case["real_usd_triggered"] is False
        assert case["benchmark_triggered"] is False
        assert case["primitive_fit_audit"]["missing_paper_primitives"] == []

    batch_c_cases = {
        case["case_id"]: case
        for case in payload["cases"]
        if case["case_id"]
        in {
            "paper_branching_cost_order",
            "paper_equal_cost_queue_tie",
            "paper_nonzero_threshold_block",
        }
    }
    assert set(batch_c_cases) == {
        "paper_branching_cost_order",
        "paper_equal_cost_queue_tie",
        "paper_nonzero_threshold_block",
    }
    for case in batch_c_cases.values():
        assert case["fixture_breadth_batch"] == "paper_fixture_breadth_batch_c"
        assert case["package_generation_triggered"] is False
        assert case["newton_runtime_triggered"] is False
        assert case["real_usd_triggered"] is False
        assert case["benchmark_triggered"] is False

    assert batch_c_cases["paper_branching_cost_order"]["collapse_trace"][
        "accepted_merge_count"
    ] == 1
    assert batch_c_cases["paper_equal_cost_queue_tie"]["collapse_trace"][
        "stale_entry_skipped_count"
    ] >= 1
    assert batch_c_cases["paper_nonzero_threshold_block"]["collapse_trace"][
        "excess_volume_threshold"
    ] == 1e-6

    batch_d_cases = {
        case["case_id"]: case
        for case in payload["cases"]
        if case["case_id"]
        in {
            "paper_component_pair_multi_candidate_order",
            "paper_component_pair_cap_skipped",
        }
    }
    assert set(batch_d_cases) == {
        "paper_component_pair_multi_candidate_order",
        "paper_component_pair_cap_skipped",
    }
    for case in batch_d_cases.values():
        trace = case["collapse_trace"]
        assert case["fixture_breadth_batch"] == "paper_fixture_breadth_batch_d"
        assert trace["component_pair_edge_insertion_triggered"] is True
        assert trace["component_pair_candidate_count"] > 1
        assert trace["component_pair_available_pair_count"] >= trace[
            "component_pair_candidate_count"
        ]
        assert trace["component_pair_candidates"]
        assert case["package_generation_triggered"] is False
        assert case["newton_runtime_triggered"] is False
        assert case["real_usd_triggered"] is False
        assert case["benchmark_triggered"] is False

    batch_e_cases = {
        case["case_id"]: case
        for case in payload["cases"]
        if case["case_id"]
        in {
            "paper_rotated_nested_primitive",
            "paper_cross_type_enclosure_boundary",
        }
    }
    assert set(batch_e_cases) == {
        "paper_rotated_nested_primitive",
        "paper_cross_type_enclosure_boundary",
    }
    assert batch_e_cases["paper_rotated_nested_primitive"]["postprocess_audit"][
        "output_primitive_count"
    ] == 1
    assert batch_e_cases["paper_cross_type_enclosure_boundary"]["postprocess_audit"][
        "cross_type_culling_supported"
    ] is False
    for case in batch_e_cases.values():
        assert case["fixture_breadth_batch"] == "paper_fixture_breadth_batch_e"
        assert case["package_generation_triggered"] is False
        assert case["newton_runtime_triggered"] is False
        assert case["real_usd_triggered"] is False
        assert case["benchmark_triggered"] is False


@pytest.mark.paper_offline
def test_cli_run_cpd_paper_offline_report_serialization_json_is_deterministic(capsys):
    assert cli.main(["--run-cpd-paper-offline-report"]) == 0
    first_payload = json.loads(capsys.readouterr().out)

    assert cli.main(["--run-cpd-paper-offline-report"]) == 0
    second_payload = json.loads(capsys.readouterr().out)

    first_json = first_payload[
        "paper_mapped_subset_primitivespec_native_fixture_serialization_contract"
    ]["serialization_rows"][0]["canonical_primitivespec_json"]
    second_json = second_payload[
        "paper_mapped_subset_primitivespec_native_fixture_serialization_contract"
    ]["serialization_rows"][0]["canonical_primitivespec_json"]
    assert first_json == second_json


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


def test_cli_run_real_usd_native_task_comparison_reads_package_body_state_guard(
    tmp_path,
    capsys,
    monkeypatch,
):
    config_path = _write_real_usd_native_config(tmp_path, _write_two_mesh_manifest(tmp_path))

    def fake_task_report(**kwargs):
        assert kwargs["native_opt_in_package_body_state_guard"] == {
            "enabled": True,
            "mode": "fallback_to_native_package",
            "thresholds": {"min_large_cylinder_radius_m": 0.25},
            "claim_boundary": "diagnostic_package_body_state_guard_not_collision_quality",
        }
        return {
            "stage": "newton_real_usd_native_task_comparison",
            "status": "smoke_passed",
            "cases": [],
        }

    monkeypatch.setattr(cli, "build_real_usd_native_task_comparison_report", fake_task_report)

    config_data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    config_data["cpd_like"]["native_opt_in_package_body_state_guard"] = {
        "enabled": True,
        "mode": "fallback_to_native_package",
        "thresholds": {"min_large_cylinder_radius_m": 0.25},
        "claim_boundary": "diagnostic_package_body_state_guard_not_collision_quality",
    }
    config_path.write_text(yaml.safe_dump(config_data), encoding="utf-8")

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
