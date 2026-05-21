import json
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

import primitive_collision_compiler.baselines.cpd_like.real_usd_comparison as real_usd_comparison
import primitive_collision_compiler.baselines.cpd_like.synthetic as cpd_synthetic
from primitive_collision_compiler.baselines.cpd_like.primitives import PrimitiveFit
from primitive_collision_compiler.baselines.cpd_like.real_usd_comparison import (
    build_real_usd_candidate_loss_diagnosis_report,
    build_real_usd_native_contact_comparison_report,
    build_real_usd_native_fitting_comparison_report,
    build_real_usd_native_task_comparison_report,
)
from primitive_collision_compiler.reports.schema import NewtonDiagnosticReport


def test_real_usd_native_fitting_report_runs_roles_from_manifest(tmp_path):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)

    report = build_real_usd_native_fitting_comparison_report(
        manifest_path=str(manifest_path),
        roles=("bed_dev_smoke", "franka_import_smoke"),
        max_primitives=1,
        legacy_subset=("box", "sphere", "capsule"),
        native_subset=("box", "sphere", "capsule", "cylinder", "cone", "ellipsoid"),
        max_source_faces_by_role={"bed_dev_smoke": 8, "franka_import_smoke": 4},
        component_merge_options={"component_merge": "virtual_pairwise"},
    )

    assert report["stage"] == "cpd_like_real_usd_native_fitting_comparison"
    assert report["status"] == "smoke_passed"
    assert report["claim_boundary"] == (
        "real_usd_native_fitting_comparison_not_collision_quality_validation"
    )
    assert [case["asset_role"] for case in report["cases"]] == [
        "bed_dev_smoke",
        "franka_import_smoke",
    ]
    assert report["cases"][0]["legacy"]["max_source_faces"] == 8
    assert report["cases"][1]["native"]["max_source_faces"] == 4
    assert "primitive_kind_counts" in report["cases"][0]["legacy"]
    assert "package_mapping" in report["cases"][0]["native"]
    assert "native_normalized_volume_delta" in report["cases"][0]["comparison"]
    native_audit = report["cases"][0]["native"]["candidate_audit_summary"]
    assert native_audit["scope"] == "per_selected_cluster"
    assert native_audit["cluster_count"] == report["cases"][0]["native"]["primitive_count"]
    assert native_audit["primitive_subset"] == [
        "box",
        "sphere",
        "capsule",
        "cylinder",
        "cone",
        "ellipsoid",
    ]
    assert native_audit["extension_candidate_kinds"] == ["cylinder", "cone", "ellipsoid"]
    assert "box_selected_cluster_count" in native_audit
    assert "clusters_with_extension_best" in native_audit
    assert "selected_rank_counts" in native_audit


def test_real_usd_native_fitting_report_adds_opt_in_lane_without_changing_default(tmp_path):
    manifest_path = _write_manifest_with_cylinder_near_miss(tmp_path)

    report = build_real_usd_native_fitting_comparison_report(
        manifest_path=str(manifest_path),
        roles=("bed_dev_smoke",),
        max_primitives=1,
        legacy_subset=("box",),
        native_subset=("box", "cylinder"),
        max_source_faces_by_role={"bed_dev_smoke": 8},
        component_merge_options={"component_merge": "virtual_pairwise"},
        native_opt_in_score_multipliers={"cylinder": 0.5},
    )

    case = report["cases"][0]

    assert case["native"]["primitive_kind_counts"] == {"box": 1}
    assert case["native"].get("primitive_score_multipliers", {}) == {}
    assert case["native_opt_in"]["primitive_kind_counts"] == {"cylinder": 1}
    assert case["native_opt_in"]["primitive_score_multipliers"] == {"cylinder": 0.5}
    assert case["native_opt_in"]["package_mapping"]["fully_mapped"] is True
    assert case["native_opt_in_comparison"]["native_uses_extended_primitive"] is True


def test_real_usd_native_fitting_report_applies_opt_in_selection_guard(tmp_path):
    manifest_path = _write_manifest_with_cylinder_near_miss(tmp_path)

    report = build_real_usd_native_fitting_comparison_report(
        manifest_path=str(manifest_path),
        roles=("bed_dev_smoke",),
        max_primitives=1,
        legacy_subset=("box",),
        native_subset=("box", "cylinder"),
        max_source_faces_by_role={"bed_dev_smoke": 8},
        component_merge_options={"component_merge": "virtual_pairwise"},
        native_opt_in_score_multipliers={"cylinder": 0.5},
        native_opt_in_selection_guard={
            "enabled": True,
            "mode": "reject",
            "target_primitives": ["cylinder"],
            "max_cylinder_radius": 0.0,
            "min_cylinder_half_height_radius_ratio": 999.0,
        },
    )

    case = report["cases"][0]
    assert case["native"]["primitive_kind_counts"] == {"box": 1}
    assert "primitive_selection_guard" not in case["native"]
    assert case["native_opt_in"]["primitive_kind_counts"] == {"box": 1}
    assert case["native_opt_in"]["primitive_score_multipliers"] == {"cylinder": 0.5}
    assert case["native_opt_in"]["primitive_selection_guard"]["target_primitives"] == [
        "cylinder"
    ]
    audit = case["native_opt_in"]["candidate_audit_summary"]
    assert audit["primitive_selection_guard"]["max_cylinder_radius"] == 0.0
    assert audit["diagnostic_guard_rejected_extension_count"] >= 1


def test_real_usd_native_fitting_report_applies_opt_in_support_threshold_relaxation(
    tmp_path,
):
    manifest_path = _write_manifest_with_low_support_patch(tmp_path)

    report = build_real_usd_native_fitting_comparison_report(
        manifest_path=str(manifest_path),
        roles=("franka_import_smoke",),
        max_primitives=1,
        legacy_subset=("box",),
        native_subset=("box", "cylinder"),
        max_source_faces_by_role={"franka_import_smoke": 4},
        component_merge_options={"component_merge": "virtual_pairwise"},
        native_opt_in_support_thresholds={
            "min_extension_source_faces": 2,
            "min_extension_unique_points": 4,
            "claim_boundary": "diagnostic_support_threshold_relaxation_not_collision_quality",
        },
    )

    case = report["cases"][0]

    assert case["native"]["primitive_kind_counts"] == {"box": 1}
    assert "primitive_selection_support_thresholds" not in case["native"]
    assert case["native_opt_in"]["primitive_kind_counts"] == {"cylinder": 1}
    assert case["native_opt_in"]["primitive_selection_support_thresholds"] == {
        "claim_boundary": "diagnostic_support_threshold_relaxation_not_collision_quality",
        "min_extension_source_faces": 2,
        "min_extension_unique_points": 4,
    }
    audit = case["native_opt_in"]["candidate_audit_summary"]
    assert audit["primitive_selection_support_thresholds"] == (
        case["native_opt_in"]["primitive_selection_support_thresholds"]
    )
    assert audit["support_blocked_extension_count"] == 0
    assert audit["selected_kind_counts"] == {"cylinder": 1}


def test_real_usd_native_fitting_report_applies_opt_in_merge_search_policy_only_to_opt_in_lane(
    tmp_path,
):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)

    report = build_real_usd_native_fitting_comparison_report(
        manifest_path=str(manifest_path),
        roles=("bed_dev_smoke",),
        max_primitives=1,
        legacy_subset=("box", "sphere", "capsule"),
        native_subset=("box", "sphere", "capsule", "cylinder"),
        max_source_faces_by_role={"bed_dev_smoke": 8},
        component_merge_options={
            "component_merge": "virtual_pairwise",
            "merge_search_policy": "topology_then_virtual",
        },
        native_opt_in_merge_search_policy="cost_guided_pairwise",
    )

    case = report["cases"][0]

    assert case["native"]["component_accounting"]["merge_search_policy"] == (
        "topology_then_virtual"
    )
    assert case["native_opt_in"]["component_accounting"]["merge_search_policy"] == (
        "cost_guided_pairwise"
    )


def test_real_usd_native_fitting_report_prefers_materialized_manifest_path(tmp_path):
    local_path = tmp_path / "local_bed.usda"
    missing_source_path = tmp_path / "missing_bed.usda"
    _write_mesh_usd(
        local_path,
        points=[(0, 0, 0), (1, 0, 0), (0, 1, 0)],
        face_vertex_counts=[3],
        face_vertex_indices=[0, 1, 2],
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

    report = build_real_usd_native_fitting_comparison_report(
        manifest_path=str(manifest_path),
        roles=("bed_dev_smoke",),
        max_primitives=1,
        legacy_subset=("box", "sphere", "capsule"),
        native_subset=("box", "sphere", "capsule", "cylinder", "cone", "ellipsoid"),
        max_source_faces_by_role={"bed_dev_smoke": 8},
    )

    assert report["status"] == "smoke_passed"
    assert report["cases"][0]["asset_path"] == str(local_path)
    assert report["cases"][0]["legacy"]["asset_path"] == str(local_path)


def test_real_usd_native_fitting_report_is_strict_json_serializable(tmp_path):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)

    report = build_real_usd_native_fitting_comparison_report(
        manifest_path=str(manifest_path),
        roles=("bed_dev_smoke",),
        max_primitives=1,
        legacy_subset=("box", "sphere", "capsule"),
        native_subset=("box", "sphere", "capsule", "cylinder", "cone", "ellipsoid"),
        max_source_faces_by_role={"bed_dev_smoke": 8},
        component_merge_options={"component_merge": "virtual_pairwise"},
    )

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_like_real_usd_native_fitting_comparison" in encoded


def test_real_usd_candidate_audit_reports_selected_rank_two_margin(tmp_path, monkeypatch):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)

    def fake_candidates(mesh, face_ids, primitive_subset):
        return (
            _primitive_fit("box", tuple(sorted(face_ids)), 2.0),
            _primitive_fit("cylinder", tuple(sorted(face_ids)), 1.0),
            _primitive_fit("cone", tuple(sorted(face_ids)), 3.0),
        )

    monkeypatch.setattr(real_usd_comparison, "fit_primitive_candidates", fake_candidates)

    report = build_real_usd_native_fitting_comparison_report(
        manifest_path=str(manifest_path),
        roles=("bed_dev_smoke",),
        max_primitives=1,
        legacy_subset=("box",),
        native_subset=("box", "cylinder", "cone"),
        max_source_faces_by_role={"bed_dev_smoke": 8},
        component_merge_options={"component_merge": "virtual_pairwise"},
    )

    audit = report["cases"][0]["native"]["candidate_audit_summary"]

    assert audit["selected_rank_counts"] == {"2": 1}
    assert audit["clusters_with_extension_best"] == 1
    assert audit["extension_best_kind_counts"] == {"cylinder": 1}
    assert audit["clusters_where_extension_beats_selected"] == 1
    assert audit["margin_sign_convention"] == "selected_cost_minus_comparator_cost"
    assert audit["mean_selected_minus_best_nonselected_cost"] > 0.0
    assert audit["mean_selected_minus_best_extension_cost"] > 0.0


def test_real_usd_candidate_loss_diagnosis_reports_box_loss_reasons(
    tmp_path,
    monkeypatch,
):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)

    def fake_candidates(mesh, face_ids, primitive_subset):
        source_faces = tuple(sorted(face_ids))
        return (
            _primitive_fit("box", source_faces, 1.0),
            _primitive_fit("cylinder", source_faces, 1.25),
            _primitive_fit("ellipsoid", source_faces, 1.75),
        )

    monkeypatch.setattr(real_usd_comparison, "fit_primitive_candidates", fake_candidates)

    report = build_real_usd_candidate_loss_diagnosis_report(
        manifest_path=str(manifest_path),
        roles=("bed_dev_smoke",),
        max_primitives=1,
        legacy_subset=("box",),
        native_subset=("box", "cylinder", "ellipsoid"),
        max_source_faces_by_role={"bed_dev_smoke": 8},
        component_merge_options={"component_merge": "virtual_pairwise"},
    )

    assert report["stage"] == "cpd_like_real_usd_candidate_loss_diagnosis"
    assert report["status"] == "smoke_passed"
    assert report["claim_boundary"] == (
        "candidate_loss_diagnosis_not_collision_quality_validation"
    )
    case = report["cases"][0]
    assert case["baseline_lock"]["legacy_primitive_kind_counts"] == {"box": 1}
    assert case["baseline_lock"]["native_primitive_kind_counts"] == {"box": 1}
    assert case["baseline_lock"]["native_uses_extended_primitive"] is False

    diagnosis = case["native_candidate_loss_diagnosis"]
    assert diagnosis["scope"] == "per_selected_cluster_candidate_loss"
    assert diagnosis["cluster_count"] == 1
    assert diagnosis["extension_candidate_kinds"] == ["cylinder", "ellipsoid"]
    assert diagnosis["diagnosis_summary"]["likely_bottleneck_counts"] == {
        "extension_fit_or_objective_cost": 1
    }
    cluster = diagnosis["clusters"][0]
    assert cluster["selected_primitive_type"] == "box"
    assert cluster["selected_rank"] == 1
    assert cluster["best_extension_candidate"]["primitive_type"] == "cylinder"
    assert cluster["best_extension_candidate"]["rank"] == 2
    assert cluster["selected_minus_best_extension_cost"] == pytest.approx(-0.25)
    assert "extension_fit_cost_higher_than_selected" in cluster["diagnosis_labels"]
    assert cluster["likely_bottleneck"] == "extension_fit_or_objective_cost"
    assert cluster["cluster_geometry"]["face_count"] > 0
    assert cluster["cluster_geometry"]["point_count"] > 0


def test_real_usd_candidate_loss_diagnosis_remains_native_only_with_opt_in_merge_policy(
    tmp_path,
    monkeypatch,
):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)
    real_decompose_mesh = real_usd_comparison.decompose_mesh
    merge_search_policies = []

    def spy_decompose_mesh(mesh, **kwargs):
        merge_search_policies.append(kwargs.get("merge_search_policy"))
        return real_decompose_mesh(mesh, **kwargs)

    monkeypatch.setattr(real_usd_comparison, "decompose_mesh", spy_decompose_mesh)

    report = build_real_usd_candidate_loss_diagnosis_report(
        manifest_path=str(manifest_path),
        roles=("bed_dev_smoke",),
        max_primitives=1,
        legacy_subset=("box",),
        native_subset=("box", "cylinder"),
        max_source_faces_by_role={"bed_dev_smoke": 8},
        component_merge_options={
            "component_merge": "virtual_pairwise",
            "merge_search_policy": "topology_then_virtual",
        },
        native_opt_in_merge_search_policy="cost_guided_pairwise",
    )

    assert merge_search_policies == ["topology_then_virtual", "topology_then_virtual"]
    assert "native_opt_in" not in report["cases"][0]
    assert report["cases"][0]["native"]["component_accounting"][
        "merge_search_policy"
    ] == "topology_then_virtual"


def test_real_usd_candidate_loss_diagnosis_treats_near_equal_extension_cost_as_tie(
    tmp_path,
    monkeypatch,
):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)

    def fake_candidates(mesh, face_ids, primitive_subset):
        source_faces = tuple(sorted(face_ids))
        return (
            _primitive_fit("box", source_faces, 1.0),
            _primitive_fit("cylinder", source_faces, 1.0 + 1e-13),
        )

    monkeypatch.setattr(real_usd_comparison, "fit_primitive_candidates", fake_candidates)

    report = build_real_usd_candidate_loss_diagnosis_report(
        manifest_path=str(manifest_path),
        roles=("bed_dev_smoke",),
        max_primitives=1,
        legacy_subset=("box",),
        native_subset=("box", "cylinder"),
        max_source_faces_by_role={"bed_dev_smoke": 8},
        component_merge_options={"component_merge": "virtual_pairwise"},
    )

    cluster = report["cases"][0]["native_candidate_loss_diagnosis"]["clusters"][0]

    assert cluster["diagnosis_labels"] == ["selected_box", "extension_tied_selected"]
    assert cluster["likely_bottleneck"] == "tie_or_subset_order"
    triage = report["cases"][0]["native_candidate_loss_diagnosis"]["triage"]
    assert triage["near_miss_cluster_count"] == 0
    assert triage["recommended_next_slice"]["target_type"] == "no_ranked_target"


def test_real_usd_candidate_loss_diagnosis_explains_support_blocked_extension(
    monkeypatch,
):
    mesh = real_usd_comparison.TriangleMesh(
        points=[
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (1.0, 1.0, 0.0),
            (0.0, 1.0, 0.0),
        ],
        faces=[
            (0, 1, 2),
            (0, 2, 3),
        ],
    )
    decomposition = SimpleNamespace(
        primitive_count=1,
        primitive_subset=("box", "cylinder"),
        primitives=(
            _primitive_fit("box", (0, 1), 2.0),
        ),
    )

    def fake_candidates(mesh, face_ids, primitive_subset):
        source_faces = tuple(sorted(face_ids))
        return (
            _primitive_fit("box", source_faces, 2.0),
            _primitive_fit("cylinder", source_faces, 1.0),
        )

    monkeypatch.setattr(real_usd_comparison, "fit_primitive_candidates", fake_candidates)

    diagnosis = real_usd_comparison._candidate_loss_diagnosis(
        mesh,
        decomposition,
        normalizer_volume=1.0,
    )

    cluster = diagnosis["clusters"][0]

    assert cluster["selected_primitive_type"] == "box"
    assert cluster["best_extension_candidate"]["primitive_type"] == "cylinder"
    assert cluster["best_extension_candidate"]["raw_cost_rank"] == 1
    assert cluster["best_extension_candidate"]["rank"] == 2
    assert cluster["best_extension_candidate"]["selection_admissible"] is False
    assert cluster["best_extension_candidate"]["selection_admissibility_reason"] == (
        "insufficient_extension_support"
    )
    assert "extension_candidate_blocked_by_support" in cluster["diagnosis_labels"]
    assert cluster["likely_bottleneck"] == "extension_support_admissibility"


def test_real_usd_candidate_audit_summary_reports_support_blocked_raw_cost_winner(
    monkeypatch,
):
    mesh = real_usd_comparison.TriangleMesh(
        points=[
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (1.0, 1.0, 0.0),
            (0.0, 1.0, 0.0),
        ],
        faces=[
            (0, 1, 2),
            (0, 2, 3),
        ],
    )
    decomposition = SimpleNamespace(
        primitive_count=1,
        primitive_subset=("box", "cylinder"),
        primitives=(
            _primitive_fit("box", (0, 1), 2.0),
        ),
    )

    def fake_candidates(mesh, face_ids, primitive_subset):
        source_faces = tuple(sorted(face_ids))
        return (
            _primitive_fit("box", source_faces, 2.0),
            _primitive_fit("cylinder", source_faces, 1.0),
        )

    monkeypatch.setattr(real_usd_comparison, "fit_primitive_candidates", fake_candidates)

    audit = real_usd_comparison._candidate_audit_summary(
        mesh,
        decomposition,
        normalizer_volume=1.0,
    )

    assert audit["ranking_semantics"] == {
        "rank": "support_aware_selection_rank",
        "raw_cost_rank": "cost_only_weighted_volume_rank",
    }
    assert audit["clusters_with_extension_best"] == 1
    assert audit["clusters_with_support_blocked_raw_cost_extension_best"] == 1
    assert audit["support_blocked_extension_count"] == 1
    assert audit["support_blocked_extension_kind_counts"] == {"cylinder": 1}
    target = audit["support_blocked_extension_targets"][0]
    assert target["cluster_index"] == 0
    assert target["selected_primitive_type"] == "box"
    assert target["blocked_extension_primitive_type"] == "cylinder"
    assert target["raw_cost_rank"] == 1
    assert target["selection_rank"] == 2
    assert target["selection_admissibility_reason"] == "insufficient_extension_support"
    assert target["selection_support"]["source_face_count"] == 2
    assert target["selection_support"]["unique_point_count"] == 4


def test_real_usd_candidate_loss_diagnosis_triages_low_support_native_extension(
    tmp_path,
    monkeypatch,
):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)

    def fake_candidates(mesh, face_ids, primitive_subset):
        source_faces = tuple(sorted(face_ids))
        if "cylinder" in primitive_subset:
            return (_primitive_fit("cylinder", source_faces, 1.0),)
        return (_primitive_fit("box", source_faces, 1.5),)

    monkeypatch.setattr(real_usd_comparison, "fit_primitive_candidates", fake_candidates)

    report = build_real_usd_candidate_loss_diagnosis_report(
        manifest_path=str(manifest_path),
        roles=("franka_import_smoke",),
        max_primitives=1,
        legacy_subset=("box",),
        native_subset=("cylinder",),
        max_source_faces_by_role={"franka_import_smoke": 4},
        component_merge_options={"component_merge": "virtual_pairwise"},
    )

    triage = report["cases"][0]["native_candidate_loss_diagnosis"]["triage"]

    assert triage["near_miss_cluster_count"] == 0
    assert triage["low_support_native_extension_count"] == 1
    assert triage["low_support_native_extension_kind_counts"] == {"cylinder": 1}
    target = triage["low_support_native_extension_targets"][0]
    assert target["selected_extension_primitive_type"] == "cylinder"
    assert target["source_face_count"] == 4
    assert target["point_count"] == 4
    assert target["suggested_next_slice"] == "native_extension_admissibility_fixture"
    assert triage["recommended_next_slice"] == {
        "target_type": "native_extension_low_support_admissibility",
        "extension_kind": "cylinder",
        "suggested_synthetic_fixture": "low_support_native_extension_patch",
        "claim_boundary": "diagnostic_triage_not_collision_quality",
    }


def test_real_usd_candidate_loss_diagnosis_triages_near_miss_extension_targets(
    tmp_path,
    monkeypatch,
):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)

    def fake_candidates(mesh, face_ids, primitive_subset):
        source_faces = tuple(sorted(face_ids))
        return (
            _primitive_fit("box", source_faces, 1.0),
            _primitive_fit("cylinder", source_faces, 1.08),
            _primitive_fit("ellipsoid", source_faces, 1.60),
        )

    monkeypatch.setattr(real_usd_comparison, "fit_primitive_candidates", fake_candidates)

    report = build_real_usd_candidate_loss_diagnosis_report(
        manifest_path=str(manifest_path),
        roles=("bed_dev_smoke",),
        max_primitives=1,
        legacy_subset=("box",),
        native_subset=("box", "cylinder", "ellipsoid"),
        max_source_faces_by_role={"bed_dev_smoke": 8},
        component_merge_options={"component_merge": "virtual_pairwise"},
    )

    triage = report["cases"][0]["native_candidate_loss_diagnosis"]["triage"]

    assert triage["scope"] == "candidate_loss_next_slice_triage"
    assert triage["near_miss_relative_gap_threshold"] == pytest.approx(0.25)
    assert triage["near_miss_cluster_count"] == 1
    assert triage["near_miss_kind_counts"] == {"cylinder": 1}
    target = triage["top_near_miss_targets"][0]
    assert target["cluster_index"] == 0
    assert target["best_extension_primitive_type"] == "cylinder"
    assert target["relative_extension_gap"] == pytest.approx(0.08)
    assert target["suggested_next_slice"] == "primitive_fitting_near_miss_fixture"
    assert triage["recommended_next_slice"] == {
        "target_type": "primitive_fitting_near_miss",
        "extension_kind": "cylinder",
        "suggested_synthetic_fixture": "cylinder_near_miss_cluster",
        "claim_boundary": "diagnostic_triage_not_collision_quality",
    }


def test_real_usd_candidate_loss_diagnosis_report_is_strict_json_serializable(tmp_path):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)

    report = build_real_usd_candidate_loss_diagnosis_report(
        manifest_path=str(manifest_path),
        roles=("bed_dev_smoke",),
        max_primitives=1,
        legacy_subset=("box",),
        native_subset=("box", "cylinder", "ellipsoid"),
        max_source_faces_by_role={"bed_dev_smoke": 8},
        component_merge_options={"component_merge": "virtual_pairwise"},
    )

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_like_real_usd_candidate_loss_diagnosis" in encoded


def test_real_usd_native_fitting_report_rejects_missing_role(tmp_path):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)

    with pytest.raises(ValueError, match="asset role 'missing_role' not found"):
        build_real_usd_native_fitting_comparison_report(
            manifest_path=str(manifest_path),
            roles=("missing_role",),
            max_primitives=1,
            legacy_subset=("box", "sphere", "capsule"),
            native_subset=("box", "sphere", "capsule", "cylinder", "cone", "ellipsoid"),
            max_source_faces_by_role={"missing_role": 8},
            component_merge_options={"component_merge": "virtual_pairwise"},
        )


def test_real_usd_native_fitting_report_rejects_empty_roles(tmp_path):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)

    with pytest.raises(ValueError, match="roles must contain at least one asset role"):
        build_real_usd_native_fitting_comparison_report(
            manifest_path=str(manifest_path),
            roles=(),
            max_primitives=1,
            legacy_subset=("box", "sphere", "capsule"),
            native_subset=("box", "sphere", "capsule", "cylinder", "cone", "ellipsoid"),
            max_source_faces_by_role={},
            component_merge_options={"component_merge": "virtual_pairwise"},
        )


def test_real_usd_native_contact_comparison_runs_each_fully_mapped_lane(
    tmp_path,
    monkeypatch,
):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)
    calls = []

    def fake_contact(package, *, source_dir, device, claim_boundary):
        calls.append((package.asset_id, source_dir, device, claim_boundary))
        return _diagnostic_report(
            stage="newton_contact_smoke",
            status="smoke_passed",
            asset_id=package.asset_id,
            package_id=package.package_id,
            probe_type="contact_canary",
            claim_boundary=claim_boundary,
        )

    monkeypatch.setattr(real_usd_comparison, "run_newton_contact_smoke", fake_contact)

    report = build_real_usd_native_contact_comparison_report(
        manifest_path=str(manifest_path),
        roles=("bed_dev_smoke", "franka_import_smoke"),
        max_primitives=1,
        legacy_subset=("box", "sphere", "capsule"),
        native_subset=("box", "sphere", "capsule", "cylinder", "cone", "ellipsoid"),
        max_source_faces_by_role={"bed_dev_smoke": 8, "franka_import_smoke": 4},
        component_merge_options={"component_merge": "virtual_pairwise"},
        source_dir="/tmp/newton-source",
        device="cpu",
    )

    assert report["stage"] == "newton_real_usd_native_contact_comparison"
    assert report["status"] == "smoke_passed"
    assert len(calls) == 4
    assert calls[0][1:] == (
        "/tmp/newton-source",
        "cpu",
        "real_usd_native_contact_canary_not_collision_quality_validation",
    )
    assert report["cases"][0]["legacy_contact"]["stage"] == "newton_contact_smoke"
    assert report["cases"][0]["native_contact"]["status"] == "smoke_passed"


def test_real_usd_native_contact_comparison_blocks_unmapped_lane_before_newton(
    tmp_path,
    monkeypatch,
):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)
    calls = []

    def fake_contact(package, *, source_dir, device, claim_boundary):
        calls.append(package.asset_id)
        return _diagnostic_report(
            stage="newton_contact_smoke",
            status="smoke_passed",
            asset_id=package.asset_id,
            package_id=package.package_id,
            probe_type="contact_canary",
            claim_boundary=claim_boundary,
        )

    monkeypatch.setattr(real_usd_comparison, "run_newton_contact_smoke", fake_contact)

    report = build_real_usd_native_contact_comparison_report(
        manifest_path=str(manifest_path),
        roles=("bed_dev_smoke",),
        max_primitives=1,
        legacy_subset=("capped_cylinder",),
        native_subset=("box", "sphere", "capsule", "cylinder", "cone", "ellipsoid"),
        max_source_faces_by_role={"bed_dev_smoke": 8},
        component_merge_options={"component_merge": "virtual_pairwise"},
        source_dir="/tmp/newton-source",
        device="cpu",
    )

    assert report["status"] == "partial"
    assert report["cases"][0]["legacy_contact"]["status"] == "mapping_gap"
    assert report["cases"][0]["legacy_contact"]["fallback_reason"] == (
        "full_package_shape_coverage_required"
    )
    assert calls == ["bed_dev_smoke_native"]


def test_real_usd_native_task_comparison_runs_tasks_after_contact_passes(
    tmp_path,
    monkeypatch,
):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)
    calls = {"contact": 0, "drop": 0, "sphere": 0}

    def fake_contact(package, *, source_dir, device, claim_boundary):
        calls["contact"] += 1
        return _diagnostic_report(
            stage="newton_contact_smoke",
            status="smoke_passed",
            asset_id=package.asset_id,
            package_id=package.package_id,
            probe_type="contact_canary",
            claim_boundary=claim_boundary,
        )

    def fake_drop(package, *, source_dir, device, options, claim_boundary):
        calls["drop"] += 1
        assert claim_boundary == "custom_task_boundary"
        return _diagnostic_report(
            stage="newton_drop_settle",
            status="smoke_passed",
            asset_id=package.asset_id,
            package_id=package.package_id,
            probe_type="drop_settle",
            claim_boundary=claim_boundary,
        )

    def fake_sphere(package, *, source_dir, device, options, claim_boundary):
        calls["sphere"] += 1
        assert claim_boundary == "custom_task_boundary"
        return _diagnostic_report(
            stage="newton_sphere_rain",
            status="smoke_passed",
            asset_id=package.asset_id,
            package_id=package.package_id,
            probe_type="sphere_rain",
            claim_boundary=claim_boundary,
        )

    monkeypatch.setattr(real_usd_comparison, "run_newton_contact_smoke", fake_contact)
    monkeypatch.setattr(real_usd_comparison, "run_newton_drop_settle", fake_drop)
    monkeypatch.setattr(real_usd_comparison, "run_newton_sphere_rain", fake_sphere)

    report = build_real_usd_native_task_comparison_report(
        manifest_path=str(manifest_path),
        roles=("bed_dev_smoke",),
        max_primitives=1,
        legacy_subset=("box", "sphere", "capsule"),
        native_subset=("box", "sphere", "capsule", "cylinder", "cone", "ellipsoid"),
        max_source_faces_by_role={"bed_dev_smoke": 8},
        component_merge_options={"component_merge": "virtual_pairwise"},
        source_dir="/tmp/newton-source",
        device="cpu",
        claim_boundary="custom_task_boundary",
    )

    assert report["stage"] == "newton_real_usd_native_task_comparison"
    assert report["status"] == "smoke_passed"
    assert calls == {"contact": 2, "drop": 2, "sphere": 2}
    assert report["cases"][0]["legacy_tasks"]["drop_settle"]["status"] == "smoke_passed"
    assert report["cases"][0]["legacy_tasks"]["sphere_rain"]["status"] == "smoke_passed"


def test_real_usd_native_task_comparison_runs_opt_in_lane_when_configured(
    tmp_path,
    monkeypatch,
):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)
    calls = {"contact": [], "drop": [], "sphere": []}

    def fake_contact(package, *, source_dir, device, claim_boundary):
        calls["contact"].append(package.asset_id)
        return _diagnostic_report(
            stage="newton_contact_smoke",
            status="smoke_passed",
            asset_id=package.asset_id,
            package_id=package.package_id,
            probe_type="contact_canary",
            claim_boundary=claim_boundary,
        )

    def fake_drop(package, *, source_dir, device, options, claim_boundary):
        calls["drop"].append(package.asset_id)
        return _diagnostic_report(
            stage="newton_drop_settle",
            status="smoke_passed",
            asset_id=package.asset_id,
            package_id=package.package_id,
            probe_type="drop_settle",
            claim_boundary=claim_boundary,
        )

    def fake_sphere(package, *, source_dir, device, options, claim_boundary):
        calls["sphere"].append(package.asset_id)
        return _diagnostic_report(
            stage="newton_sphere_rain",
            status="smoke_passed",
            asset_id=package.asset_id,
            package_id=package.package_id,
            probe_type="sphere_rain",
            claim_boundary=claim_boundary,
        )

    monkeypatch.setattr(real_usd_comparison, "run_newton_contact_smoke", fake_contact)
    monkeypatch.setattr(real_usd_comparison, "run_newton_drop_settle", fake_drop)
    monkeypatch.setattr(real_usd_comparison, "run_newton_sphere_rain", fake_sphere)

    report = build_real_usd_native_task_comparison_report(
        manifest_path=str(manifest_path),
        roles=("bed_dev_smoke",),
        max_primitives=1,
        legacy_subset=("box", "sphere", "capsule"),
        native_subset=("box", "sphere", "capsule", "cylinder", "cone", "ellipsoid"),
        max_source_faces_by_role={"bed_dev_smoke": 8},
        component_merge_options={"component_merge": "virtual_pairwise"},
        native_opt_in_score_multipliers={"cylinder": 0.5},
        source_dir="/tmp/newton-source",
        device="cpu",
    )

    assert report["status"] == "smoke_passed"
    assert calls == {
        "contact": [
            "bed_dev_smoke_legacy",
            "bed_dev_smoke_native",
            "bed_dev_smoke_native_opt_in",
        ],
        "drop": [
            "bed_dev_smoke_legacy",
            "bed_dev_smoke_native",
            "bed_dev_smoke_native_opt_in",
        ],
        "sphere": [
            "bed_dev_smoke_legacy",
            "bed_dev_smoke_native",
            "bed_dev_smoke_native_opt_in",
        ],
    }
    assert report["cases"][0]["native_opt_in_contact"]["status"] == "smoke_passed"
    assert report["cases"][0]["native_opt_in_tasks"]["drop_settle"]["status"] == "smoke_passed"


def test_real_usd_native_task_comparison_threads_opt_in_selection_guard(
    tmp_path,
    monkeypatch,
):
    manifest_path = _write_manifest_with_cylinder_near_miss(tmp_path)

    def fake_contact(package, *, source_dir, device, claim_boundary):
        return _diagnostic_report(
            stage="newton_contact_smoke",
            status="smoke_passed",
            asset_id=package.asset_id,
            package_id=package.package_id,
            probe_type="contact_canary",
            claim_boundary=claim_boundary,
        )

    def fake_task(package, *, source_dir, device, options, claim_boundary):
        return _diagnostic_report(
            stage="newton_task_smoke",
            status="smoke_passed",
            asset_id=package.asset_id,
            package_id=package.package_id,
            probe_type="task_smoke",
            claim_boundary=claim_boundary,
        )

    monkeypatch.setattr(real_usd_comparison, "run_newton_contact_smoke", fake_contact)
    monkeypatch.setattr(real_usd_comparison, "run_newton_drop_settle", fake_task)
    monkeypatch.setattr(real_usd_comparison, "run_newton_sphere_rain", fake_task)

    report = build_real_usd_native_task_comparison_report(
        manifest_path=str(manifest_path),
        roles=("bed_dev_smoke",),
        max_primitives=1,
        legacy_subset=("box",),
        native_subset=("box", "cylinder"),
        max_source_faces_by_role={"bed_dev_smoke": 8},
        component_merge_options={"component_merge": "virtual_pairwise"},
        native_opt_in_score_multipliers={"cylinder": 0.5},
        native_opt_in_selection_guard={
            "enabled": True,
            "mode": "reject",
            "target_primitives": ["cylinder"],
            "max_cylinder_radius": 0.0,
            "min_cylinder_half_height_radius_ratio": 999.0,
        },
        source_dir="/tmp/newton-source",
        device="cpu",
    )

    opt_in = report["cases"][0]["native_opt_in"]
    assert opt_in["primitive_kind_counts"] == {"box": 1}
    assert opt_in["primitive_selection_guard"]["mode"] == "reject"
    assert report["cases"][0]["native_opt_in_contact"]["type_counts"] == {"box": 1}


def test_real_usd_native_task_comparison_applies_opt_in_package_body_state_guard(
    tmp_path,
    monkeypatch,
):
    manifest_path = _write_manifest_with_cylinder_near_miss(tmp_path)
    calls = {"contact": [], "drop": [], "sphere": []}

    def fake_contact(package, *, source_dir, device, claim_boundary):
        calls["contact"].append(package.asset_id)
        return _diagnostic_report(
            stage="newton_contact_smoke",
            status="smoke_passed",
            asset_id=package.asset_id,
            package_id=package.package_id,
            probe_type="contact_canary",
            claim_boundary=claim_boundary,
        )

    def fake_drop(package, *, source_dir, device, options, claim_boundary):
        calls["drop"].append(package.asset_id)
        return _diagnostic_report(
            stage="newton_drop_settle",
            status="smoke_passed",
            asset_id=package.asset_id,
            package_id=package.package_id,
            probe_type="drop_settle",
            claim_boundary=claim_boundary,
        )

    def fake_sphere(package, *, source_dir, device, options, claim_boundary):
        calls["sphere"].append(package.asset_id)
        return _diagnostic_report(
            stage="newton_sphere_rain",
            status="smoke_passed",
            asset_id=package.asset_id,
            package_id=package.package_id,
            probe_type="sphere_rain",
            claim_boundary=claim_boundary,
        )

    monkeypatch.setattr(real_usd_comparison, "run_newton_contact_smoke", fake_contact)
    monkeypatch.setattr(real_usd_comparison, "run_newton_drop_settle", fake_drop)
    monkeypatch.setattr(real_usd_comparison, "run_newton_sphere_rain", fake_sphere)

    report = build_real_usd_native_task_comparison_report(
        manifest_path=str(manifest_path),
        roles=("bed_dev_smoke",),
        max_primitives=1,
        legacy_subset=("box",),
        native_subset=("box", "cylinder"),
        max_source_faces_by_role={"bed_dev_smoke": 8},
        component_merge_options={"component_merge": "virtual_pairwise"},
        native_opt_in_score_multipliers={"cylinder": 0.5},
        native_opt_in_package_body_state_guard={
            "enabled": True,
            "thresholds": {
                "min_large_cylinder_radius_m": 0.0,
                "max_flat_half_height_radius_ratio": 999.0,
                "min_com_delta_norm_m": 0.0,
                "min_inertia_frobenius_delta": 0.0,
            },
        },
        source_dir="/tmp/newton-source",
        device="cpu",
    )

    assert calls["contact"] == [
        "bed_dev_smoke_legacy",
        "bed_dev_smoke_native",
        "bed_dev_smoke_native",
    ]
    assert calls["drop"][-1] == "bed_dev_smoke_native"
    assert calls["sphere"][-1] == "bed_dev_smoke_native"
    case = report["cases"][0]
    assert case["native_opt_in"]["primitive_kind_counts"] == {"cylinder": 1}
    guard = case["native_opt_in_package_body_state_guard"]
    assert guard["decision"] == "fallback_to_native_package"
    assert guard["effective_lane"] == "native"
    assert guard["effective_package_id"] == case["native"]["collision_package"]["package_id"]
    assert guard["candidate_package_id"] == case["native_opt_in"]["collision_package"][
        "package_id"
    ]
    assert case["native_opt_in_contact"]["asset_id"] == "bed_dev_smoke_native"
    assert case["native_opt_in_tasks"]["drop_settle"]["asset_id"] == "bed_dev_smoke_native"


def test_real_usd_native_task_comparison_package_body_state_guard_keeps_unflagged_opt_in(
    tmp_path,
    monkeypatch,
):
    manifest_path = _write_manifest_with_low_support_patch(tmp_path)
    calls = {"contact": [], "drop": [], "sphere": []}

    def fake_contact(package, *, source_dir, device, claim_boundary):
        calls["contact"].append(package.asset_id)
        return _diagnostic_report(
            stage="newton_contact_smoke",
            status="smoke_passed",
            asset_id=package.asset_id,
            package_id=package.package_id,
            probe_type="contact_canary",
            claim_boundary=claim_boundary,
        )

    def fake_task(package, *, source_dir, device, options, claim_boundary):
        calls["drop"].append(package.asset_id)
        calls["sphere"].append(package.asset_id)
        return _diagnostic_report(
            stage="newton_task_smoke",
            status="smoke_passed",
            asset_id=package.asset_id,
            package_id=package.package_id,
            probe_type="task_smoke",
            claim_boundary=claim_boundary,
        )

    monkeypatch.setattr(real_usd_comparison, "run_newton_contact_smoke", fake_contact)
    monkeypatch.setattr(real_usd_comparison, "run_newton_drop_settle", fake_task)
    monkeypatch.setattr(real_usd_comparison, "run_newton_sphere_rain", fake_task)

    report = build_real_usd_native_task_comparison_report(
        manifest_path=str(manifest_path),
        roles=("franka_import_smoke",),
        max_primitives=1,
        legacy_subset=("box",),
        native_subset=("box", "cylinder"),
        max_source_faces_by_role={"franka_import_smoke": 4},
        component_merge_options={"component_merge": "virtual_pairwise"},
        native_opt_in_support_thresholds={
            "min_extension_source_faces": 2,
            "min_extension_unique_points": 4,
        },
        native_opt_in_package_body_state_guard={"enabled": True},
        source_dir="/tmp/newton-source",
        device="cpu",
    )

    assert calls["contact"][-1] == "franka_import_smoke_native_opt_in"
    assert calls["drop"][-1] == "franka_import_smoke_native_opt_in"
    case = report["cases"][0]
    assert case["native_opt_in"]["primitive_kind_counts"] == {"cylinder": 1}
    guard = case["native_opt_in_package_body_state_guard"]
    assert guard["decision"] == "keep_native_opt_in_package"
    assert guard["effective_lane"] == "native_opt_in"
    assert guard["effective_package_id"] == case["native_opt_in"]["collision_package"][
        "package_id"
    ]


def test_real_usd_native_task_comparison_threads_opt_in_support_thresholds(
    tmp_path,
    monkeypatch,
):
    manifest_path = _write_manifest_with_low_support_patch(tmp_path)

    def fake_contact(package, *, source_dir, device, claim_boundary):
        return _diagnostic_report(
            stage="newton_contact_smoke",
            status="smoke_passed",
            asset_id=package.asset_id,
            package_id=package.package_id,
            probe_type="contact_canary",
            claim_boundary=claim_boundary,
        )

    def fake_task(package, *, source_dir, device, options, claim_boundary):
        return _diagnostic_report(
            stage="newton_task_smoke",
            status="smoke_passed",
            asset_id=package.asset_id,
            package_id=package.package_id,
            probe_type="task_smoke",
            claim_boundary=claim_boundary,
        )

    monkeypatch.setattr(real_usd_comparison, "run_newton_contact_smoke", fake_contact)
    monkeypatch.setattr(real_usd_comparison, "run_newton_drop_settle", fake_task)
    monkeypatch.setattr(real_usd_comparison, "run_newton_sphere_rain", fake_task)

    report = build_real_usd_native_task_comparison_report(
        manifest_path=str(manifest_path),
        roles=("franka_import_smoke",),
        max_primitives=1,
        legacy_subset=("box",),
        native_subset=("box", "cylinder"),
        max_source_faces_by_role={"franka_import_smoke": 4},
        component_merge_options={"component_merge": "virtual_pairwise"},
        native_opt_in_support_thresholds={
            "min_extension_source_faces": 2,
            "min_extension_unique_points": 4,
            "claim_boundary": "diagnostic_support_threshold_relaxation_not_collision_quality",
        },
        source_dir="/tmp/newton-source",
        device="cpu",
    )

    case = report["cases"][0]
    assert "primitive_selection_support_thresholds" not in case["native"]
    assert case["native_opt_in"]["primitive_kind_counts"] == {"cylinder": 1}
    assert case["native_opt_in"]["primitive_selection_support_thresholds"] == {
        "claim_boundary": "diagnostic_support_threshold_relaxation_not_collision_quality",
        "min_extension_source_faces": 2,
        "min_extension_unique_points": 4,
    }
    assert case["native_opt_in_tasks"]["drop_settle"]["status"] == "smoke_passed"
    assert case["native_opt_in_tasks"]["sphere_rain"]["status"] == "smoke_passed"


def test_real_usd_native_task_comparison_blocks_tasks_when_contact_fails(
    tmp_path,
    monkeypatch,
):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)

    def fake_contact(package, *, source_dir, device, claim_boundary):
        return _diagnostic_report(
            stage="newton_contact_smoke",
            status="dependency_gap",
            asset_id=package.asset_id,
            package_id=package.package_id,
            probe_type="contact_canary",
            claim_boundary=claim_boundary,
            fallback_reason="newton_missing",
        )

    def fail_task(*args, **kwargs):
        raise AssertionError("task probes must be gated by contact canary")

    monkeypatch.setattr(real_usd_comparison, "run_newton_contact_smoke", fake_contact)
    monkeypatch.setattr(real_usd_comparison, "run_newton_drop_settle", fail_task)
    monkeypatch.setattr(real_usd_comparison, "run_newton_sphere_rain", fail_task)

    report = build_real_usd_native_task_comparison_report(
        manifest_path=str(manifest_path),
        roles=("bed_dev_smoke",),
        max_primitives=1,
        legacy_subset=("box", "sphere", "capsule"),
        native_subset=("box", "sphere", "capsule", "cylinder", "cone", "ellipsoid"),
        max_source_faces_by_role={"bed_dev_smoke": 8},
        component_merge_options={"component_merge": "virtual_pairwise"},
        source_dir="/tmp/newton-source",
        device="cpu",
    )

    assert report["status"] == "dependency_gap"
    assert report["cases"][0]["legacy_tasks"]["drop_settle"]["status"] == (
        "blocked_by_contact_canary"
    )
    assert report["cases"][0]["legacy_tasks"]["sphere_rain"]["status"] == (
        "blocked_by_contact_canary"
    )


def _write_manifest_with_two_meshes(tmp_path: Path) -> Path:
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


def _write_manifest_with_cylinder_near_miss(tmp_path: Path) -> Path:
    mesh = cpd_synthetic._cylinder_near_miss_cluster_mesh()
    usd_path = tmp_path / "cylinder_near_miss.usda"
    _write_mesh_usd(
        usd_path,
        points=[tuple(point) for point in mesh.points],
        face_vertex_counts=[len(face) for face in mesh.faces],
        face_vertex_indices=[
            int(point_index) for face in mesh.faces for point_index in face
        ],
    )
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump(
            {
                "manifest_id": "test_cylinder_near_miss_manifest",
                "assets": [{"role": "bed_dev_smoke", "path": str(usd_path)}],
            }
        ),
        encoding="utf-8",
    )
    return manifest_path


def _write_manifest_with_low_support_patch(tmp_path: Path) -> Path:
    franka_path = tmp_path / "franka_low_support_patch.usda"
    _write_mesh_usd(
        franka_path,
        points=[
            (0, 0, 0),
            (1, 0, 0),
            (1, 1, 0),
            (0, 1, 0),
        ],
        face_vertex_counts=[3, 3],
        face_vertex_indices=[0, 1, 2, 0, 2, 3],
    )
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump(
            {
                "manifest_id": "test_low_support_patch_manifest",
                "assets": [
                    {"role": "franka_import_smoke", "path": str(franka_path)},
                ],
            }
        ),
        encoding="utf-8",
    )
    return manifest_path


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
    *,
    stage: str,
    status: str,
    asset_id: str,
    package_id: str,
    probe_type: str,
    claim_boundary: str,
    fallback_reason: str | None = None,
) -> NewtonDiagnosticReport:
    return NewtonDiagnosticReport(
        stage=stage,
        status=status,
        asset_id=asset_id,
        package_id=package_id,
        probe_type=probe_type,
        device="cpu",
        environment=None,
        primitive_count=1,
        type_counts={"box": 1},
        shape_mappings=(),
        contact_canaries=(),
        claim_boundary=claim_boundary,
        fallback_reason=fallback_reason,
    )


def _primitive_fit(primitive_type: str, source_faces: tuple[int, ...], cost: float) -> PrimitiveFit:
    return PrimitiveFit(
        primitive_type=primitive_type,
        source_faces=source_faces,
        center=(0.0, 0.0, 0.0),
        axes=((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
        dimensions={"test": primitive_type},
        volume=cost,
        weighted_volume=cost,
        contains_assigned_points=True,
    )
