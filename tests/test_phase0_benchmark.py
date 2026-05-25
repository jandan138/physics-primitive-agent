import json
import hashlib
from pathlib import Path

import pytest
import yaml

from primitive_collision_compiler.contracts import CollisionPackage
from primitive_collision_compiler.phase0 import build_phase0_rigid_benchmark_report
from primitive_collision_compiler.reports.schema import NewtonDiagnosticReport


def test_phase0_report_records_all_assets_baselines_and_probe_outcomes(tmp_path, monkeypatch):
    manifest_path = _write_phase0_manifest(tmp_path)
    config_path = _write_phase0_config(tmp_path, manifest_path)
    calls = {"contact": [], "drop": [], "sphere": []}

    def fake_contact(package, *, source_dir, device, claim_boundary):
        calls["contact"].append(package.asset_id)
        return _diagnostic_report(
            package,
            stage="newton_contact_smoke",
            probe_type="contact_canary",
            status="smoke_passed",
            claim_boundary=claim_boundary,
        )

    def fake_drop(package, *, source_dir, device, options, claim_boundary):
        calls["drop"].append(package.asset_id)
        return _diagnostic_report(
            package,
            stage="newton_drop_settle",
            probe_type="drop_settle",
            status="smoke_passed",
            claim_boundary=claim_boundary,
        )

    def fake_sphere(package, *, source_dir, device, options, claim_boundary):
        calls["sphere"].append(package.asset_id)
        return _diagnostic_report(
            package,
            stage="newton_sphere_rain",
            probe_type="sphere_rain",
            status="smoke_passed",
            claim_boundary=claim_boundary,
        )

    import primitive_collision_compiler.phase0 as phase0

    monkeypatch.setattr(phase0, "run_newton_contact_smoke", fake_contact)
    monkeypatch.setattr(phase0, "run_newton_drop_settle", fake_drop)
    monkeypatch.setattr(phase0, "run_newton_sphere_rain", fake_sphere)

    report = build_phase0_rigid_benchmark_report(config_path)

    assert report["stage"] == "phase0_rigid_asset_benchmark"
    assert report["status"] == "partial"
    assert report["asset_count"] == 2
    assert report["roles"] == ["rigid_prop", "precision_negative_control"]
    assert set(report["outcome_counts"]) >= {
        "accept",
        "fallback",
        "dependency_gap",
        "failure",
        "not_applicable",
    }
    assert report["outcome_counts"]["accept"] > 0
    assert report["outcome_counts"]["fallback"] > 0

    first = report["cases"][0]
    assert first["asset_role"] == "rigid_prop"
    assert first["asset_gate"]["outcome"] == "accept"
    assert set(first["baseline_results"]) == {
        "bounding_primitive",
        "single_convex_hull",
        "coacd_or_vhacd_if_available",
        "cpd_style_primitive_candidate_if_available",
    }
    assert first["baseline_results"]["bounding_primitive"]["outcome"] == "accept"
    assert first["baseline_results"]["bounding_primitive"]["collision_package"][
        "source_sha256"
    ] == first["asset_hashes"]["source_sha256"]
    assert first["baseline_results"]["cpd_style_primitive_candidate_if_available"][
        "objective_report"
    ]["stage"] == "cpd_like_offline_objective"
    assert first["baseline_results"]["single_convex_hull"]["outcome"] == "fallback"
    assert (
        first["baseline_results"]["coacd_or_vhacd_if_available"]["outcome"]
        == "dependency_gap"
    )
    assert first["probe_results"]["bounding_primitive"]["body_state_drop_settle"][
        "outcome"
    ] == "accept"
    assert first["probe_results"]["bounding_primitive"]["sphere_rain"]["outcome"] == "accept"
    assert first["probe_results"]["bounding_primitive"]["stack_or_slide"]["outcome"] == (
        "fallback"
    )
    assert first["probe_results"]["bounding_primitive"]["link_boundary_audit"][
        "outcome"
    ] == "not_applicable"
    assert first["probe_results"]["bounding_primitive"]["articulation_smoke_if_robot"][
        "status"
    ] == "not_applicable"

    precision = report["cases"][1]
    assert precision["asset_role"] == "precision_negative_control"
    assert precision["probe_results"]["bounding_primitive"]["precision_rejection"][
        "outcome"
    ] == "fallback"
    assert calls["contact"] == [
        "rigid_prop_bounding_primitive",
        "rigid_prop_cpd_style_primitive_candidate_if_available",
        "precision_negative_control_bounding_primitive",
        "precision_negative_control_cpd_style_primitive_candidate_if_available",
    ]


def test_phase0_report_gates_hash_mismatch_before_generating_packages(tmp_path):
    manifest_path = _write_phase0_manifest(tmp_path)
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["assets"][0]["local_sha256"] = "0" * 64
    manifest_path.write_text(yaml.safe_dump(manifest), encoding="utf-8")
    config_path = _write_phase0_config(tmp_path, manifest_path, source_dir=None)

    report = build_phase0_rigid_benchmark_report(config_path)

    case = report["cases"][0]

    assert case["asset_role"] == "rigid_prop"
    assert case["asset_gate"]["status"] == "hash_mismatch"
    assert case["asset_gate"]["outcome"] == "failure"
    assert case["baseline_results"]["bounding_primitive"]["status"] == (
        "blocked_by_asset_smoke"
    )
    assert case["baseline_results"]["bounding_primitive"]["outcome"] == "failure"
    assert "collision_package" not in case["baseline_results"]["bounding_primitive"]
    assert case["probe_results"]["bounding_primitive"]["contact_canary"]["status"] == (
        "blocked_by_baseline"
    )


def test_phase0_report_is_strict_json_serializable_without_newton_source(tmp_path):
    manifest_path = _write_phase0_manifest(tmp_path)
    config_path = _write_phase0_config(tmp_path, manifest_path, source_dir=None)

    report = build_phase0_rigid_benchmark_report(config_path)

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "phase0_rigid_asset_benchmark" in encoded
    first = report["cases"][0]
    assert first["probe_results"]["bounding_primitive"]["body_state_drop_settle"][
        "outcome"
    ] == "dependency_gap"
    assert first["probe_results"]["bounding_primitive"]["sphere_rain"]["outcome"] == (
        "dependency_gap"
    )


def _write_phase0_manifest(tmp_path: Path) -> Path:
    rigid_path = tmp_path / "rigid.usda"
    precision_path = tmp_path / "keyboard.usda"
    _write_mesh_usd(
        rigid_path,
        points=[
            (0, 0, 0),
            (1, 0, 0),
            (1, 1, 0),
            (0, 1, 0),
            (0, 0, 0.5),
            (1, 0, 0.5),
            (1, 1, 0.5),
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
        precision_path,
        points=[(0, 0, 0), (2, 0, 0), (2, 0.1, 0), (0, 0.1, 0)],
        face_vertex_counts=[4],
        face_vertex_indices=[0, 1, 2, 3],
    )
    manifest_path = tmp_path / "phase0_assets.yaml"
    manifest_path.write_text(
        yaml.safe_dump(
            {
                "manifest_id": "phase0_fixture",
                "assets": [
                    {
                        "id": "fixture_rigid",
                        "role": "rigid_prop",
                        "path": str(rigid_path),
                        "local_path": str(rigid_path),
                        "source_path": str(rigid_path),
                        "sha256": _sha256_file(rigid_path),
                        "local_sha256": _sha256_file(rigid_path),
                        "source_sha256": "1" * 64,
                    },
                    {
                        "id": "fixture_precision",
                        "role": "precision_negative_control",
                        "path": str(precision_path),
                        "local_path": str(precision_path),
                        "source_path": str(precision_path),
                        "sha256": _sha256_file(precision_path),
                        "local_sha256": _sha256_file(precision_path),
                        "source_sha256": "2" * 64,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    return manifest_path


def _write_phase0_config(
    tmp_path: Path,
    manifest_path: Path,
    *,
    source_dir: str | None = "/tmp/newton-source",
) -> Path:
    config = {
        "asset": {"id": "phase0_fixture", "path": str(manifest_path)},
        "task": {"primary": "phase0_simulation_checked_diagnostic"},
        "compile": {
            "method": "simulation_checked_primitive_candidates",
            "max_primitives": 2,
            "allowed_fallback": ["coacd", "vhacd", "convex_mesh", "manual_review"],
            "verify": [
                "body_state_drop_settle",
                "stack_or_slide",
                "sphere_rain",
                "link_boundary_audit",
                "articulation_smoke_if_robot",
                "precision_rejection",
            ],
        },
        "phase0_defaults": {
            "asset_manifest": str(manifest_path),
            "seeds": 1,
            "duration_seconds": 2,
            "baselines": [
                {"id": "bounding_primitive", "method": "bbox_or_sphere", "required": True},
                {
                    "id": "single_convex_hull",
                    "method": "single_convex_hull",
                    "required": True,
                },
                {
                    "id": "coacd_or_vhacd_if_available",
                    "method": "coacd_or_vhacd",
                    "required": False,
                    "fallback_if_unavailable": "record_dependency_gap",
                },
                {
                    "id": "cpd_style_primitive_candidate_if_available",
                    "method": "cpd_style_primitive_candidate",
                    "required": False,
                    "fallback_if_unavailable": "record_dependency_gap",
                },
            ],
            "probes": {
                "body_state_drop_settle": {"initial_conditions": {"height_m": 0.25}},
                "stack_or_slide": {"initial_conditions": {"lateral_velocity_mps": 0.1}},
                "sphere_rain": {
                    "initial_conditions": {
                        "sphere_count": 4,
                        "sphere_radius_m": 0.025,
                    }
                },
                "link_boundary_audit": {"initial_conditions": {"simulation_required": False}},
                "articulation_smoke_if_robot": {
                    "initial_conditions": {"simulation_required": False}
                },
                "precision_rejection": {"initial_conditions": {"simulation_required": False}},
            },
            "required_metrics": ["primitive_or_hull_count", "fallback_ratio"],
        },
    }
    if source_dir is not None:
        config["newton"] = {"source_dir": source_dir}
    config_path = tmp_path / "phase0_config.yaml"
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
    return config_path


def _write_mesh_usd(path: Path, points, face_vertex_counts, face_vertex_indices):
    Usd = pytest.importorskip("pxr.Usd")
    UsdGeom = pytest.importorskip("pxr.UsdGeom")
    stage = Usd.Stage.CreateNew(str(path))
    mesh = UsdGeom.Mesh.Define(stage, "/Mesh")
    mesh.CreatePointsAttr(points)
    mesh.CreateFaceVertexCountsAttr(face_vertex_counts)
    mesh.CreateFaceVertexIndicesAttr(face_vertex_indices)
    stage.GetRootLayer().Save()


def _diagnostic_report(
    package: CollisionPackage,
    *,
    stage: str,
    probe_type: str,
    status: str,
    claim_boundary: str,
) -> NewtonDiagnosticReport:
    return NewtonDiagnosticReport(
        stage=stage,
        status=status,
        asset_id=package.asset_id,
        package_id=package.package_id,
        probe_type=probe_type,
        device="cpu",
        environment=None,
        primitive_count=len(package.primitives),
        type_counts={},
        shape_mappings=(),
        contact_canaries=(),
        claim_boundary=claim_boundary,
    )


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()
