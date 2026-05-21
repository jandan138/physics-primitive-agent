import json
import math

import numpy as np

import primitive_collision_compiler.baselines.cpd_like.synthetic as cpd_synthetic
import primitive_collision_compiler.baselines.cpd_like.primitives as cpd_primitives
from primitive_collision_compiler.baselines.cpd_like.primitives import (
    PrimitiveFit,
    fit_best_primitive,
    fit_primitive_candidates,
    rank_primitive_candidates_for_selection,
)
from primitive_collision_compiler.baselines.cpd_like.synthetic import (
    CYLINDER_NEAR_MISS_FIT_ABLATION_CLAIM_BOUNDARY,
    CYLINDER_NEAR_MISS_SCORING_POLICY_ABLATION_CLAIM_BOUNDARY,
    CYLINDER_NEAR_MISS_SCORING_SENSITIVITY_CLAIM_BOUNDARY,
    CYLINDER_SCORING_POLICY_PACKAGE_PROBE_CLAIM_BOUNDARY,
    CYLINDER_SCORING_POLICY_NEWTON_PROBE_CLAIM_BOUNDARY,
    COST_GUIDED_LOOKAHEAD_MERGE_CLAIM_BOUNDARY,
    COST_GUIDED_LOOKAHEAD_NEWTON_PROBE_CLAIM_BOUNDARY,
    COST_GUIDED_LOOKAHEAD_NEWTON_TASK_CLAIM_BOUNDARY,
    COST_GUIDED_LOOKAHEAD_PACKAGE_PROBE_CLAIM_BOUNDARY,
    CONTROLLED_MERGE_SEARCH_PACKAGE_PROBE_CLAIM_BOUNDARY,
    CONTROLLED_MERGE_SEARCH_NEWTON_PROBE_CLAIM_BOUNDARY,
    CONTROLLED_MERGE_SEARCH_NEWTON_TASK_CLAIM_BOUNDARY,
    EXPECTED_FAILURE_WORKBENCH_CLAIM_BOUNDARY,
    FOUR_BLOCK_SLICE_REPORT_CLAIM_BOUNDARY,
    NEAR_MISS_WORKBENCH_CLAIM_BOUNDARY,
    NEWTON_NATIVE_FITTING_COMPARISON_CLAIM_BOUNDARY,
    SYNTHETIC_COMPARISON_CLAIM_BOUNDARY,
    build_cpd_like_cylinder_near_miss_fit_ablation_report,
    build_cpd_like_cylinder_near_miss_scoring_policy_ablation_report,
    build_cpd_like_cylinder_near_miss_scoring_sensitivity_report,
    build_cpd_like_cylinder_scoring_policy_newton_probe_report,
    build_cpd_like_cylinder_scoring_policy_package_probe_report,
    build_cpd_like_controlled_merge_search_package_probe_report,
    build_cpd_like_controlled_merge_search_newton_probe_report,
    build_cpd_like_cost_guided_lookahead_merge_report,
    build_cpd_like_cost_guided_lookahead_newton_probe_report,
    build_cpd_like_cost_guided_lookahead_package_probe_report,
    build_cpd_like_cost_guided_synthetic_comparison_report,
    build_cpd_like_expected_failure_synthetic_workbench_report,
    build_cpd_like_four_block_slice_report,
    build_cpd_like_near_miss_workbench_report,
    build_cpd_like_synthetic_comparison_report,
    build_newton_native_fitting_comparison_report,
)
from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.geometry.mesh import TriangleMesh
from primitive_collision_compiler.reports.schema import NewtonDiagnosticReport


def test_synthetic_comparison_report_covers_inspectable_cases():
    report = build_cpd_like_synthetic_comparison_report()

    assert report["stage"] == "cpd_like_synthetic_objective_comparison"
    assert report["status"] == "smoke_passed"
    assert report["claim_boundary"] == SYNTHETIC_COMPARISON_CLAIM_BOUNDARY
    assert [case["case_id"] for case in report["cases"]] == [
        "adjacent_square",
        "disconnected_pair",
        "blocked_disconnected_pair",
    ]

    cases = {case["case_id"]: case for case in report["cases"]}
    assert cases["adjacent_square"]["policies"]["topology_only"]["status"] == "smoke_passed"
    assert "geometric_excess_proxy" not in cases["adjacent_square"]["policies"]["topology_only"]
    assert "paper_primitive_gap" not in cases["adjacent_square"]["policies"]["topology_only"]
    assert cases["adjacent_square"]["policies"]["virtual_pairwise"]["status"] == "smoke_passed"
    assert cases["adjacent_square"]["comparison"][
        "primitive_count_delta_virtual_minus_topology"
    ] == 0

    disconnected = cases["disconnected_pair"]
    assert disconnected["policies"]["topology_only"]["status"] == "partial"
    assert disconnected["policies"]["virtual_pairwise"]["status"] == "smoke_passed"
    assert disconnected["comparison"][
        "virtual_pairwise_omits_topology_unmerged_component_label"
    ] is True
    assert disconnected["comparison"]["primitive_count_delta_virtual_minus_topology"] == -1

    blocked = cases["blocked_disconnected_pair"]
    assert blocked["policies"]["topology_only"]["status"] == "partial"
    assert blocked["policies"]["virtual_pairwise"]["status"] == "partial"
    assert "component_merge_blocked" in blocked["policies"]["virtual_pairwise"][
        "failure_labels"
    ]
    assert "merge_trace" not in cases["adjacent_square"]["policies"]["topology_only"]


def test_synthetic_comparison_report_is_strict_json_serializable():
    report = build_cpd_like_synthetic_comparison_report()

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_like_synthetic_objective_comparison" in encoded


def test_selection_guard_rejects_oversized_native_extension_candidate():
    mesh = TriangleMesh(
        points=np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [1.0, 1.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
                [1.0, 0.0, 1.0],
                [1.0, 1.0, 1.0],
                [0.0, 1.0, 1.0],
            ]
        ),
        faces=np.array([[0, 1, 2], [0, 2, 3], [4, 5, 6], [4, 6, 7]]),
    )
    source_faces = (0, 1, 2, 3)
    box = PrimitiveFit(
        primitive_type="box",
        source_faces=source_faces,
        center=(0.5, 0.5, 0.5),
        axes=((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
        dimensions={"half_extents": [0.5, 0.5, 0.5]},
        volume=0.2,
        weighted_volume=0.2,
        contains_assigned_points=True,
    )
    cylinder = PrimitiveFit(
        primitive_type="cylinder",
        source_faces=source_faces,
        center=(0.5, 0.5, 0.5),
        axes=((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
        dimensions={"radius": 2.0, "half_height": 0.1, "axis_index": 0},
        volume=0.02,
        weighted_volume=0.02,
        contains_assigned_points=True,
    )

    unguarded = rank_primitive_candidates_for_selection(
        mesh,
        frozenset(source_faces),
        (box, cylinder),
        primitive_score_multipliers={"cylinder": 0.5},
    )
    guarded = rank_primitive_candidates_for_selection(
        mesh,
        frozenset(source_faces),
        (box, cylinder),
        primitive_score_multipliers={"cylinder": 0.5},
        primitive_selection_guard={
            "enabled": True,
            "mode": "reject",
            "target_primitives": ["cylinder"],
            "max_cylinder_radius": 0.5,
            "min_cylinder_half_height_radius_ratio": 0.1,
        },
    )

    assert unguarded[0].primitive_type == "cylinder"
    assert guarded[0].primitive_type == "box"
    cylinder_row = next(row for row in guarded if row.primitive_type == "cylinder")
    assert cylinder_row.raw_cost_rank == 1
    assert cylinder_row.selection_admissible is False
    assert cylinder_row.selection_admissibility_reason == "large_flat_cylinder_quarantine"


def test_selection_guard_reason_takes_precedence_over_low_support():
    mesh = TriangleMesh(
        points=np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
            ]
        ),
        faces=np.array([[0, 1, 2]]),
    )
    source_faces = (0,)
    box = PrimitiveFit(
        primitive_type="box",
        source_faces=source_faces,
        center=(0.5, 0.5, 0.0),
        axes=((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
        dimensions={"half_extents": [0.5, 0.5, 0.0]},
        volume=0.2,
        weighted_volume=0.2,
        contains_assigned_points=True,
    )
    cylinder = PrimitiveFit(
        primitive_type="cylinder",
        source_faces=source_faces,
        center=(0.5, 0.5, 0.0),
        axes=((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
        dimensions={"radius": 2.0, "half_height": 0.1, "axis_index": 0},
        volume=0.02,
        weighted_volume=0.02,
        contains_assigned_points=True,
    )

    guarded = rank_primitive_candidates_for_selection(
        mesh,
        frozenset(source_faces),
        (box, cylinder),
        primitive_selection_guard={
            "enabled": True,
            "mode": "reject",
            "target_primitives": ["cylinder"],
            "max_cylinder_radius": 0.5,
            "min_cylinder_half_height_radius_ratio": 0.1,
        },
    )

    cylinder_row = next(row for row in guarded if row.primitive_type == "cylinder")
    assert cylinder_row.selection_admissible is False
    assert cylinder_row.selection_admissibility_reason == "large_flat_cylinder_quarantine"


def test_cost_guided_synthetic_comparison_shows_old_new_merge_decision():
    report = build_cpd_like_cost_guided_synthetic_comparison_report()

    assert report["stage"] == "cpd_like_cost_guided_synthetic_objective_comparison"
    assert report["status"] == "smoke_passed"
    assert (
        report["claim_boundary"]
        == "cost_guided_synthetic_comparison_not_collision_quality_validation"
    )

    cases = {case["case_id"]: case for case in report["cases"]}
    assert list(cases) == ["cost_guided_pair_choice"]
    case = cases["cost_guided_pair_choice"]
    assert case["expectation_status"] == "matched"
    assert case["policies"]["topology_then_virtual"]["component_accounting"][
        "topology_merge_count"
    ] == 1
    assert case["policies"]["cost_guided_pairwise"]["component_accounting"][
        "virtual_component_merge_count"
    ] == 1
    assert case["comparison"]["cost_guided_chose_virtual_instead_of_topology"] is True
    assert case["comparison"]["cost_guided_accepted_excess_delta"] < 0.0
    trace = case["policies"]["cost_guided_pairwise"]["merge_trace"]
    assert trace[0]["decision"] == "accepted"
    assert trace[0]["merge_kind"] == "virtual_component"
    assert trace[0]["merged_source_component_ids"] == [0, 2]
    assert case["policies"]["topology_then_virtual"]["paper_alignment"]["paper_cost_name"] == (
        "collapse_excess_volume"
    )
    assert case["policies"]["cost_guided_pairwise"]["paper_alignment"][
        "paper_faithfulness"
    ] == "surrogate_not_paper_faithful"


def test_cost_guided_synthetic_comparison_report_is_strict_json_serializable():
    report = build_cpd_like_cost_guided_synthetic_comparison_report()

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_like_cost_guided_synthetic_objective_comparison" in encoded


def test_expected_failure_workbench_reports_known_cpd_gaps():
    report = build_cpd_like_expected_failure_synthetic_workbench_report()

    assert report["stage"] == "cpd_like_expected_failure_synthetic_workbench"
    assert report["status"] == "smoke_passed"
    assert report["status_semantics"] == (
        "expected_limitations_reported_not_decomposition_success"
    )
    assert report["claim_boundary"] == EXPECTED_FAILURE_WORKBENCH_CLAIM_BOUNDARY
    assert report["evidence_level"] == (
        "offline_cpd_like_expected_failure_workbench_smoke"
    )
    assert [case["case_id"] for case in report["cases"]] == [
        "restricted_primitive_vocabulary_gap",
        "single_proxy_wraps_disconnected_components",
        "threshold_blocks_component_merge",
    ]

    cases = {case["case_id"]: case for case in report["cases"]}
    restricted = cases["restricted_primitive_vocabulary_gap"]
    assert restricted["expectation_status"] == "matched"
    assert restricted["limitation_class"] == "expected_primitive_fit_gap"
    assert restricted["next_capability_needed"] == "primitive_fit_extension"
    assert restricted["paper_gap_tags"] == [
        "restricted_primitive_vocabulary",
        "paper_scope_primitive_fitting",
    ]
    assert restricted["fixture_geometry_summary"] == {
        "point_count": 4,
        "face_count": 2,
        "connected_component_count": 1,
        "mesh_aabb_volume": 0.0,
        "normalizer_floor_applied": True,
    }
    assert restricted["expected_diagnostic_flags"] == {
        "expected": [
            "unsupported_paper_primitives_present",
            "paper_alignment_surrogate_not_paper_faithful",
        ],
        "observed": [
            "unsupported_paper_primitives_present",
            "paper_alignment_surrogate_not_paper_faithful",
        ],
        "missing": [],
        "unexpected": [],
        "match_status": "matched",
    }
    assert restricted["metrics"]["paper_primitive_gap"][
        "unsupported_paper_primitive_count"
    ] == 3

    wrapped = cases["single_proxy_wraps_disconnected_components"]
    assert wrapped["expectation_status"] == "matched"
    assert wrapped["limitation_class"] == "expected_empty_wrapper_proxy"
    assert wrapped["next_capability_needed"] == "primitive_fit_extension"
    assert wrapped["fixture_geometry_summary"]["connected_component_count"] == 2
    assert wrapped["expected_diagnostic_flags"]["missing"] == []
    assert wrapped["expected_diagnostic_flags"]["unexpected"] == []
    assert "virtual_component_merge_used" in wrapped["expected_diagnostic_flags"]["observed"]
    assert "empty_space_wrap_proxy_present" in wrapped["expected_diagnostic_flags"]["observed"]
    assert wrapped["policy"]["status"] == "smoke_passed"
    assert wrapped["metrics"]["component_accounting"]["virtual_component_merge_count"] == 1
    assert wrapped["metrics"]["merge_excess_terms"]["accepted_eq4_cost_sum"] > 0.0

    blocked = cases["threshold_blocks_component_merge"]
    assert blocked["expectation_status"] == "matched"
    assert blocked["limitation_class"] == "expected_threshold_block"
    assert blocked["next_capability_needed"] == "merge_search_extension"
    assert blocked["policy"]["status"] == "partial"
    assert blocked["expected_diagnostic_flags"] == {
        "expected": [
            "unsupported_paper_primitives_present",
            "paper_alignment_surrogate_not_paper_faithful",
            "component_merge_blocked",
            "unmerged_components",
            "primitive_budget_not_met",
        ],
        "observed": [
            "unsupported_paper_primitives_present",
            "paper_alignment_surrogate_not_paper_faithful",
            "component_merge_blocked",
            "unmerged_components",
            "primitive_budget_not_met",
        ],
        "missing": [],
        "unexpected": [],
        "match_status": "matched",
    }


def test_expected_failure_workbench_report_is_strict_json_serializable():
    report = build_cpd_like_expected_failure_synthetic_workbench_report()

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_like_expected_failure_synthetic_workbench" in encoded


def test_expected_failure_workbench_reports_partial_when_expected_flags_are_missing(monkeypatch):
    monkeypatch.setattr(cpd_synthetic, "_diagnostic_flags", lambda policy: [])

    report = cpd_synthetic.build_cpd_like_expected_failure_synthetic_workbench_report()

    assert report["status"] == "partial"
    first_case = report["cases"][0]
    assert first_case["expectation_status"] == "mismatched"
    assert first_case["expected_diagnostic_flags"]["observed"] == []
    assert first_case["expected_diagnostic_flags"]["missing"] == [
        "unsupported_paper_primitives_present",
        "paper_alignment_surrogate_not_paper_faithful",
    ]


def test_near_miss_workbench_reports_cylinder_fixture():
    report = build_cpd_like_near_miss_workbench_report()

    assert report["stage"] == "cpd_like_near_miss_fixture_workbench"
    assert report["status"] == "smoke_passed"
    assert report["claim_boundary"] == NEAR_MISS_WORKBENCH_CLAIM_BOUNDARY
    assert report["status_semantics"] == "near_miss_targets_reported_not_quality_success"
    assert [case["case_id"] for case in report["cases"]] == [
        "cylinder_near_miss_cluster"
    ]

    cases = {case["case_id"]: case for case in report["cases"]}
    assert set(cases) == {"cylinder_near_miss_cluster"}

    case = cases["cylinder_near_miss_cluster"]
    assert case["expectation_status"] == "matched"
    assert case["selected_primitive_type"] == "box"
    assert case["best_extension_candidate"]["primitive_type"] == "cylinder"
    assert case["best_extension_candidate"]["raw_cost_rank"] == 2
    assert case["best_extension_candidate"]["selection_admissible"] is True
    assert case["best_extension_candidate"]["selection_admissibility_reason"] == (
        "support_thresholds_met"
    )
    assert 0.0 < case["near_miss"]["relative_extension_gap"] <= 0.25
    assert case["recommended_next_slice"] == {
        "target_type": "primitive_fitting_or_merge_search_near_miss",
        "extension_kind": "cylinder",
        "suggested_synthetic_fixture": "cylinder_near_miss_cluster",
        "claim_boundary": "diagnostic_triage_not_collision_quality",
    }


def test_newton_native_fitting_comparison_selects_native_primitives():
    report = build_newton_native_fitting_comparison_report()

    assert report["stage"] == "cpd_like_newton_native_fitting_comparison"
    assert report["status"] == "smoke_passed"
    assert report["claim_boundary"] == NEWTON_NATIVE_FITTING_COMPARISON_CLAIM_BOUNDARY
    assert [case["case_id"] for case in report["cases"]] == [
        "cylindrical_rod",
        "tapered_cone",
        "ellipsoid_blob",
        "squat_cylinder",
    ]

    expected_native = {
        "cylindrical_rod": "cylinder",
        "tapered_cone": "cone",
        "ellipsoid_blob": "ellipsoid",
        "squat_cylinder": "cylinder",
    }
    for case in report["cases"]:
        case_id = case["case_id"]
        assert case["expectation_status"] == "matched"
        assert case["expected_native_primitive"] == expected_native[case_id]
        assert case["legacy"]["selected_primitive_kind"] in {"box", "sphere", "capsule"}
        assert case["native"]["selected_primitive_kind"] == expected_native[case_id]
        native_candidates = case["native"]["candidate_audit"]
        legacy_candidates = case["legacy"]["candidate_audit"]
        assert native_candidates[0]["primitive_type"] == expected_native[case_id]
        assert native_candidates[0]["selected"] is True
        assert native_candidates[0]["rank"] == 1
        assert case["native"]["selected_candidate_rank"] == 1
        assert case["native"]["selection_policy"] == (
            "support_aware_min_weighted_volume_surrogate_v1"
        )
        assert case["native"]["selection_cost_name"] == "weighted_primitive_volume"
        assert case["native"]["selection_cost_units"] == "source_mesh_volume_units"
        assert case["native"]["candidate_audit_scope"] == "single_primitive_full_mesh_fixture"
        assert case["native"]["candidate_audit_face_count"] > 0
        assert case["native"]["candidate_audit_matches_selection_scope"] is True
        assert all(candidate["rank"] == index for index, candidate in enumerate(native_candidates, 1))
        assert len(legacy_candidates) == 3
        assert case["comparison"]["native_selected_kind_cost_explained"] is True
        assert case["comparison"]["native_selection_margin_vs_legacy_best"] <= 0.0
        assert case["comparison"]["selection_claim_boundary"] == (
            "synthetic_selection_audit_not_paper_optimizer_or_collision_quality"
        )
        assert case["comparison"]["native_selected_newton_extension"] is True
        assert case["comparison"]["native_normalized_volume_delta"] <= 0.0
        assert case["native"]["package_mapping"]["status_counts"] == {"mapped": 1}

    real_scope = report["real_usd_scope"]
    assert real_scope["status"] == "scope_declared_not_run"
    assert real_scope["manifest"] == "assets/manifests/cpd_like_smoke_assets.yaml"
    assert [asset["role"] for asset in real_scope["assets"]] == [
        "bed_dev_smoke",
        "franka_import_smoke",
    ]
    assert real_scope["assets"][0]["max_source_faces"] == 256
    assert real_scope["assets"][1]["max_source_faces"] == 128


def test_newton_native_fitting_comparison_report_is_strict_json_serializable():
    report = build_newton_native_fitting_comparison_report()

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_like_newton_native_fitting_comparison" in encoded


def test_cylinder_near_miss_cluster_exposes_box_selected_close_cylinder_loss():
    mesh = cpd_synthetic._cylinder_near_miss_cluster_mesh()
    face_ids = frozenset(range(mesh.face_count))

    fit = fit_best_primitive(mesh, face_ids, primitive_subset=("box", "cylinder"))
    ranked = rank_primitive_candidates_for_selection(
        mesh,
        face_ids,
        fit_primitive_candidates(mesh, face_ids, primitive_subset=("box", "cylinder")),
    )
    box = next(row for row in ranked if row.primitive_type == "box")
    cylinder = next(row for row in ranked if row.primitive_type == "cylinder")
    relative_gap = (
        cylinder.candidate.weighted_volume - box.candidate.weighted_volume
    ) / box.candidate.weighted_volume

    assert fit.primitive_type == "box"
    assert ranked[0].primitive_type == "box"
    assert box.selection_admissible is True
    assert cylinder.selection_admissible is True
    assert cylinder.selection_admissibility_reason == "support_thresholds_met"
    assert cylinder.candidate.weighted_volume > box.candidate.weighted_volume
    assert 0.0 < relative_gap <= 0.25
    assert cylinder.raw_cost_rank == 2


def test_cylinder_near_miss_fit_ablation_reports_radial_refinement_gate():
    report = build_cpd_like_cylinder_near_miss_fit_ablation_report()

    assert report["stage"] == "cpd_like_cylinder_near_miss_fit_ablation"
    assert report["status"] == "smoke_passed"
    assert report["claim_boundary"] == CYLINDER_NEAR_MISS_FIT_ABLATION_CLAIM_BOUNDARY
    assert report["status_semantics"] == "fit_ablation_triage_not_quality_success"

    cases = {case["case_id"]: case for case in report["cases"]}
    assert set(cases) == {"cylinder_near_miss_cluster"}

    case = cases["cylinder_near_miss_cluster"]
    assert case["case_id"] == "cylinder_near_miss_cluster"
    assert case["scope"] == "single_fixture_radial_fit_ablation"
    assert case["default_behavior_changed"] is False
    assert case["selected_primitive_type"] == "box"
    assert case["extension_primitive_type"] == "cylinder"
    assert case["ablation"]["kind"] == "pairwise_radial_lower_bound"
    assert case["ablation"]["current_cylinder_contains_assigned_points"] is True
    assert case["ablation"]["lower_bound_volume_beats_selected"] is False
    assert math.isclose(
        case["ablation"]["current_cylinder_radius"],
        case["ablation"]["pairwise_radius_lower_bound"],
        rel_tol=0.0,
        abs_tol=1e-12,
    )
    assert case["decision"]["recommended_next_component"] == (
        "scoring_or_merge_search_not_radial_center_refinement"
    )
    assert case["decision"]["newton_task_comparison_triggered"] is False
    assert case["decision"]["newton_task_comparison_gate"] == (
        "not_triggered_default_package_unchanged"
    )


def test_cylinder_near_miss_fit_ablation_derives_default_behavior_flag(monkeypatch):
    cylinder = PrimitiveFit(
        primitive_type="cylinder",
        source_faces=(),
        center=(0.0, 0.0, 0.0),
        axes=((0.0, 0.0, 1.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)),
        dimensions={"radius": 1.15, "half_height": 0.3, "axis_index": 0},
        volume=2.5,
        weighted_volume=2.5,
        contains_assigned_points=True,
    )
    box = PrimitiveFit(
        primitive_type="box",
        source_faces=(),
        center=(0.0, 0.0, 0.0),
        axes=((0.0, 0.0, 1.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)),
        dimensions={"half_extents": [0.3, 0.8, 1.15]},
        volume=2.2,
        weighted_volume=2.2,
        contains_assigned_points=True,
    )
    support = {
        "source_face_count": 20,
        "unique_point_count": 12,
        "min_extension_source_faces": 3,
        "min_extension_unique_points": 5,
    }
    ranked = (
        cpd_primitives.PrimitiveCandidateSelection(
            candidate=cylinder,
            candidate_order=1,
            raw_cost_rank=1,
            selection_admissible=True,
            selection_admissibility_reason="support_thresholds_met",
            support=support,
        ),
        cpd_primitives.PrimitiveCandidateSelection(
            candidate=box,
            candidate_order=0,
            raw_cost_rank=2,
            selection_admissible=True,
            selection_admissibility_reason="legacy_or_non_extension_primitive",
            support=support,
        ),
    )
    monkeypatch.setattr(cpd_synthetic, "fit_primitive_candidates", lambda *args, **kwargs: ())
    monkeypatch.setattr(
        cpd_synthetic,
        "rank_primitive_candidates_for_selection",
        lambda *args, **kwargs: ranked,
    )

    report = build_cpd_like_cylinder_near_miss_fit_ablation_report()

    cases = {case["case_id"]: case for case in report["cases"]}
    assert set(cases) == {"cylinder_near_miss_cluster"}

    case = cases["cylinder_near_miss_cluster"]
    assert case["selected_primitive_type"] == "cylinder"
    assert case["default_behavior_changed"] is True
    assert case["expectation_status"] == "mismatched"
    assert case["decision"]["newton_task_comparison_gate"] == (
        "not_triggered_ablation_mismatched_default_behavior_changed"
    )


def test_cylinder_near_miss_fit_ablation_report_is_strict_json_serializable():
    report = build_cpd_like_cylinder_near_miss_fit_ablation_report()

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_like_cylinder_near_miss_fit_ablation" in encoded


def test_cylinder_near_miss_scoring_sensitivity_reports_required_multiplier():
    report = build_cpd_like_cylinder_near_miss_scoring_sensitivity_report()

    assert report["stage"] == "cpd_like_cylinder_near_miss_scoring_sensitivity"
    assert report["status"] == "smoke_passed"
    assert report["claim_boundary"] == CYLINDER_NEAR_MISS_SCORING_SENSITIVITY_CLAIM_BOUNDARY
    assert report["status_semantics"] == "scoring_sensitivity_triage_not_quality_success"

    case = report["cases"][0]
    assert case["case_id"] == "cylinder_near_miss_cluster"
    assert case["scope"] == "single_fixture_scoring_sensitivity"
    assert case["selected_primitive_type"] == "box"
    assert case["extension_primitive_type"] == "cylinder"
    assert case["selection_policy_changed"] is False
    assert case["default_behavior_changed"] is False
    assert case["extension_candidate"]["raw_cost_rank"] == 2
    assert case["extension_candidate"]["selection_admissible"] is True
    sensitivity = case["scoring_sensitivity"]
    assert sensitivity["relative_gap_selected_denominator"] > 0.0
    assert sensitivity["selected_score_multiplier_for_extension_to_tie"] > 1.0
    assert 0.0 < sensitivity["extension_score_multiplier_to_tie"] < 1.0
    assert math.isclose(
        sensitivity["extension_weighted_volume"]
        * sensitivity["extension_score_multiplier_to_tie"],
        sensitivity["selected_weighted_volume"],
        rel_tol=0.0,
        abs_tol=1e-12,
    )
    assert math.isclose(
        sensitivity["extension_cost_reduction_fraction_to_tie"],
        1.0 - sensitivity["extension_score_multiplier_to_tie"],
        rel_tol=0.0,
        abs_tol=1e-12,
    )
    assert sensitivity["current_extension_multiplier"] == 1.0
    assert sensitivity["current_raw_cost_flips_under_default_multiplier"] is False
    assert sensitivity["extension_score_multiplier_to_beat_condition"] == (
        "multiplier_below_extension_score_multiplier_to_tie"
    )
    assert case["decision"]["diagnostic_conclusion"] == (
        "scoring_change_required_to_flip_current_surrogate"
    )
    assert case["decision"]["default_selection_changed"] is False
    assert case["decision"]["newton_task_comparison_triggered"] is False


def test_cylinder_near_miss_scoring_sensitivity_report_is_strict_json_serializable():
    report = build_cpd_like_cylinder_near_miss_scoring_sensitivity_report()

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_like_cylinder_near_miss_scoring_sensitivity" in encoded


def test_cylinder_near_miss_scoring_sensitivity_derives_default_behavior_gate(
    monkeypatch,
):
    cylinder = PrimitiveFit(
        primitive_type="cylinder",
        source_faces=(),
        center=(0.0, 0.0, 0.0),
        axes=((0.0, 0.0, 1.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)),
        dimensions={"radius": 1.15, "half_height": 0.3, "axis_index": 0},
        volume=2.0,
        weighted_volume=2.0,
        contains_assigned_points=True,
    )
    box = PrimitiveFit(
        primitive_type="box",
        source_faces=(),
        center=(0.0, 0.0, 0.0),
        axes=((0.0, 0.0, 1.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)),
        dimensions={"half_extents": [0.3, 0.8, 1.15]},
        volume=2.2,
        weighted_volume=2.2,
        contains_assigned_points=True,
    )
    support = {
        "source_face_count": 20,
        "unique_point_count": 12,
        "min_extension_source_faces": 3,
        "min_extension_unique_points": 5,
    }
    ranked = (
        cpd_primitives.PrimitiveCandidateSelection(
            candidate=cylinder,
            candidate_order=1,
            raw_cost_rank=1,
            selection_admissible=True,
            selection_admissibility_reason="support_thresholds_met",
            support=support,
        ),
        cpd_primitives.PrimitiveCandidateSelection(
            candidate=box,
            candidate_order=0,
            raw_cost_rank=2,
            selection_admissible=True,
            selection_admissibility_reason="legacy_or_non_extension_primitive",
            support=support,
        ),
    )
    monkeypatch.setattr(cpd_synthetic, "fit_primitive_candidates", lambda *args, **kwargs: ())
    monkeypatch.setattr(
        cpd_synthetic,
        "rank_primitive_candidates_for_selection",
        lambda *args, **kwargs: ranked,
    )

    report = build_cpd_like_cylinder_near_miss_scoring_sensitivity_report()

    case = report["cases"][0]
    assert case["selected_primitive_type"] == "cylinder"
    assert case["default_behavior_changed"] is True
    assert case["expectation_status"] == "mismatched"
    assert case["decision"]["default_selection_changed"] is True
    assert case["decision"]["newton_task_comparison_gate"] == (
        "not_triggered_sensitivity_mismatched_default_behavior_changed"
    )


def test_cylinder_near_miss_scoring_policy_ablation_reports_counterfactual_flip():
    report = build_cpd_like_cylinder_near_miss_scoring_policy_ablation_report()

    assert report["stage"] == "cpd_like_cylinder_near_miss_scoring_policy_ablation"
    assert report["status"] == "smoke_passed"
    assert report["claim_boundary"] == CYLINDER_NEAR_MISS_SCORING_POLICY_ABLATION_CLAIM_BOUNDARY
    assert report["status_semantics"] == "report_only_counterfactual_ablation_not_quality_success"

    cases = {case["case_id"]: case for case in report["cases"]}
    assert set(cases) == {"cylinder_near_miss_cluster", "boxy_cuboid_guardrail"}

    case = cases["cylinder_near_miss_cluster"]
    assert case["case_role"] == "expected_counterfactual_flip"
    assert case["case_id"] == "cylinder_near_miss_cluster"
    assert case["scope"] == "single_fixture_report_only_scoring_policy_ablation"
    assert case["selection_policy_applied_to_default_pipeline"] is False
    assert case["default_selected_primitive_type"] == "box"
    assert case["counterfactual_selected_primitive_type"] == "cylinder"
    assert case["default_selection_changed"] is False
    assert case["counterfactual_selection_changed"] is True
    assert case["counterfactual_ablation"]["report_only_extension_multiplier"] == 0.88
    assert (
        case["counterfactual_ablation"]["report_only_extension_multiplier"]
        < case["counterfactual_ablation"]["extension_score_multiplier_to_tie"]
    )
    assert case["counterfactual_ablation"]["default_package_changed"] is False
    counterfactual_cylinder = next(
        row
        for row in case["counterfactual_candidate_ranking"]
        if row["primitive_type"] == "cylinder"
    )
    assert counterfactual_cylinder["default_rank"] == 2
    assert counterfactual_cylinder["counterfactual_rank"] == 1
    assert "rank" not in counterfactual_cylinder
    assert case["decision"]["diagnostic_conclusion"] == (
        "report_only_counterfactual_multiplier_flips_synthetic_near_miss"
    )
    assert case["decision"]["newton_task_comparison_triggered"] is False

    mesh = cpd_synthetic._cylinder_near_miss_cluster_mesh()
    fit = fit_best_primitive(
        mesh,
        frozenset(range(mesh.face_count)),
        primitive_subset=("box", "cylinder"),
    )
    assert fit.primitive_type == "box"

    boxy = cases["boxy_cuboid_guardrail"]
    assert boxy["case_role"] == "boxy_no_flip_guardrail"
    assert boxy["default_selected_primitive_type"] == "box"
    assert boxy["counterfactual_selected_primitive_type"] == "box"
    assert boxy["counterfactual_selection_changed"] is False
    assert boxy["counterfactual_ablation"]["report_only_extension_multiplier"] == 0.88
    assert boxy["counterfactual_ablation"]["fixed_multiplier_below_tie_threshold"] is False
    boxy_cylinder = next(
        row
        for row in boxy["counterfactual_candidate_ranking"]
        if row["primitive_type"] == "cylinder"
    )
    assert boxy_cylinder["default_rank"] == 2
    assert boxy_cylinder["counterfactual_rank"] == 2

    boxy_mesh = cpd_synthetic._boxy_cuboid_guardrail_mesh()
    boxy_fit = fit_best_primitive(
        boxy_mesh,
        frozenset(range(boxy_mesh.face_count)),
        primitive_subset=("box", "cylinder"),
    )
    assert boxy_fit.primitive_type == "box"


def test_cylinder_near_miss_scoring_policy_ablation_report_is_strict_json_serializable():
    report = build_cpd_like_cylinder_near_miss_scoring_policy_ablation_report()

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_like_cylinder_near_miss_scoring_policy_ablation" in encoded


def test_cylinder_near_miss_scoring_policy_ablation_derives_default_behavior_gate(
    monkeypatch,
):
    cylinder = PrimitiveFit(
        primitive_type="cylinder",
        source_faces=(),
        center=(0.0, 0.0, 0.0),
        axes=((0.0, 0.0, 1.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)),
        dimensions={"radius": 1.15, "half_height": 0.3, "axis_index": 0},
        volume=2.0,
        weighted_volume=2.0,
        contains_assigned_points=True,
    )
    box = PrimitiveFit(
        primitive_type="box",
        source_faces=(),
        center=(0.0, 0.0, 0.0),
        axes=((0.0, 0.0, 1.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)),
        dimensions={"half_extents": [0.3, 0.8, 1.15]},
        volume=2.2,
        weighted_volume=2.2,
        contains_assigned_points=True,
    )
    support = {
        "source_face_count": 20,
        "unique_point_count": 12,
        "min_extension_source_faces": 3,
        "min_extension_unique_points": 5,
    }
    ranked = (
        cpd_primitives.PrimitiveCandidateSelection(
            candidate=cylinder,
            candidate_order=1,
            raw_cost_rank=1,
            selection_admissible=True,
            selection_admissibility_reason="support_thresholds_met",
            support=support,
        ),
        cpd_primitives.PrimitiveCandidateSelection(
            candidate=box,
            candidate_order=0,
            raw_cost_rank=2,
            selection_admissible=True,
            selection_admissibility_reason="legacy_or_non_extension_primitive",
            support=support,
        ),
    )
    monkeypatch.setattr(cpd_synthetic, "fit_primitive_candidates", lambda *args, **kwargs: ())
    monkeypatch.setattr(
        cpd_synthetic,
        "rank_primitive_candidates_for_selection",
        lambda *args, **kwargs: ranked,
    )

    report = build_cpd_like_cylinder_near_miss_scoring_policy_ablation_report()

    case = report["cases"][0]
    assert case["default_selected_primitive_type"] == "cylinder"
    assert case["default_behavior_changed"] is True
    assert case["default_selection_changed"] is True
    assert case["expectation_status"] == "mismatched"
    assert case["decision"]["newton_task_comparison_gate"] == (
        "not_triggered_ablation_mismatched_default_behavior_changed"
    )
    assert case["decision"]["diagnostic_conclusion"] == (
        "report_only_counterfactual_ablation_mismatched_default_behavior_changed"
    )


def test_opt_in_cylinder_multiplier_flips_near_miss_without_default_change():
    mesh = cpd_synthetic._cylinder_near_miss_cluster_mesh()
    face_ids = frozenset(range(mesh.face_count))

    default_fit = fit_best_primitive(mesh, face_ids, primitive_subset=("box", "cylinder"))
    opt_in_ranked = rank_primitive_candidates_for_selection(
        mesh,
        face_ids,
        fit_primitive_candidates(mesh, face_ids, primitive_subset=("box", "cylinder")),
        primitive_score_multipliers={"cylinder": 0.88},
    )
    opt_in_fit = fit_best_primitive(
        mesh,
        face_ids,
        primitive_subset=("box", "cylinder"),
        primitive_score_multipliers={"cylinder": 0.88},
    )

    assert default_fit.primitive_type == "box"
    assert opt_in_ranked[0].primitive_type == "cylinder"
    assert opt_in_ranked[0].effective_score < opt_in_ranked[1].effective_score
    assert opt_in_fit.primitive_type == "cylinder"


def test_opt_in_cylinder_multiplier_preserves_boxy_guardrail():
    mesh = cpd_synthetic._boxy_cuboid_guardrail_mesh()
    face_ids = frozenset(range(mesh.face_count))

    default_fit = fit_best_primitive(mesh, face_ids, primitive_subset=("box", "cylinder"))
    opt_in_ranked = rank_primitive_candidates_for_selection(
        mesh,
        face_ids,
        fit_primitive_candidates(mesh, face_ids, primitive_subset=("box", "cylinder")),
        primitive_score_multipliers={"cylinder": 0.88},
    )
    opt_in_fit = fit_best_primitive(
        mesh,
        face_ids,
        primitive_subset=("box", "cylinder"),
        primitive_score_multipliers={"cylinder": 0.88},
    )

    assert default_fit.primitive_type == "box"
    assert opt_in_ranked[0].primitive_type == "box"
    assert opt_in_fit.primitive_type == "box"


def test_cylinder_scoring_policy_selection_probe_reports_opt_in_selection():
    report = cpd_synthetic.build_cpd_like_cylinder_scoring_policy_selection_probe_report()

    assert report["stage"] == "cpd_like_cylinder_scoring_policy_selection_probe"
    assert report["status"] == "smoke_passed"
    assert report["status_semantics"] == "opt_in_selection_probe_not_quality_success"
    assert report["claim_boundary"] == (
        cpd_synthetic.CYLINDER_SCORING_POLICY_SELECTION_PROBE_CLAIM_BOUNDARY
    )

    cases = {case["case_id"]: case for case in report["cases"]}
    assert set(cases) == {"cylinder_near_miss_cluster", "boxy_cuboid_guardrail"}

    near_miss = cases["cylinder_near_miss_cluster"]
    assert near_miss["case_role"] == "expected_opt_in_flip"
    assert near_miss["default_selected_primitive_type"] == "box"
    assert near_miss["opt_in_selected_primitive_type"] == "cylinder"
    assert near_miss["default_behavior_changed"] is False
    assert near_miss["opt_in_selection_changed"] is True
    assert near_miss["selection_policy_applied_to_default_pipeline"] is False
    assert near_miss["opt_in_policy_applied_to_probe"] is True
    assert near_miss["decision"]["newton_task_comparison_triggered"] is False
    opt_in_cylinder = next(
        row for row in near_miss["opt_in_candidate_ranking"] if row["primitive_type"] == "cylinder"
    )
    assert opt_in_cylinder["default_rank"] == 2
    assert opt_in_cylinder["opt_in_rank"] == 1
    assert opt_in_cylinder["score_multiplier"] == 0.88

    boxy = cases["boxy_cuboid_guardrail"]
    assert boxy["case_role"] == "boxy_no_flip_guardrail"
    assert boxy["default_selected_primitive_type"] == "box"
    assert boxy["opt_in_selected_primitive_type"] == "box"
    assert boxy["default_behavior_changed"] is False
    assert boxy["opt_in_selection_changed"] is False


def test_cylinder_scoring_policy_selection_probe_report_is_strict_json_serializable():
    report = cpd_synthetic.build_cpd_like_cylinder_scoring_policy_selection_probe_report()

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_like_cylinder_scoring_policy_selection_probe" in encoded


def test_cylinder_scoring_policy_package_probe_outputs_mapped_opt_in_package():
    report = build_cpd_like_cylinder_scoring_policy_package_probe_report()

    assert report["stage"] == "cpd_like_cylinder_scoring_policy_package_probe"
    assert report["status"] == "smoke_passed"
    assert report["claim_boundary"] == CYLINDER_SCORING_POLICY_PACKAGE_PROBE_CLAIM_BOUNDARY
    assert report["default_pipeline_changed"] is False
    cases = {case["case_id"]: case for case in report["cases"]}

    near_miss = cases["cylinder_near_miss_cluster"]
    assert near_miss["default_package"]["primitive_kinds"] == ["box"]
    assert near_miss["opt_in_package"]["primitive_kinds"] == ["cylinder"]
    assert near_miss["opt_in_package_changed"] is True
    assert near_miss["opt_in_package_mapping"]["fully_mapped"] is True
    assert near_miss["opt_in_package_mapping"]["status_counts"] == {"mapped": 1}
    assert near_miss["decision"]["newton_task_comparison_triggered"] is False
    assert near_miss["decision"]["newton_task_comparison_gate"] == (
        "not_triggered_synthetic_package_probe_only"
    )

    guardrail = cases["boxy_cuboid_guardrail"]
    assert guardrail["default_package"]["primitive_kinds"] == ["box"]
    assert guardrail["opt_in_package"]["primitive_kinds"] == ["box"]
    assert guardrail["opt_in_package_changed"] is False
    assert guardrail["opt_in_package_mapping"]["fully_mapped"] is True


def test_cylinder_scoring_policy_package_probe_report_is_strict_json_serializable():
    report = build_cpd_like_cylinder_scoring_policy_package_probe_report()

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_like_cylinder_scoring_policy_package_probe" in encoded


def test_controlled_merge_search_package_probe_outputs_mapped_changed_package():
    report = build_cpd_like_controlled_merge_search_package_probe_report()

    assert report["stage"] == "cpd_like_controlled_merge_search_package_probe"
    assert report["status"] == "smoke_passed"
    assert report["claim_boundary"] == CONTROLLED_MERGE_SEARCH_PACKAGE_PROBE_CLAIM_BOUNDARY
    assert report["default_pipeline_changed"] is False
    assert report["newton_task_comparison_triggered"] is False

    cases = {case["case_id"]: case for case in report["cases"]}
    case = cases["cost_guided_pair_choice"]
    assert case["default_package"]["primitive_source_faces"] == [[0, 1], [2]]
    assert case["opt_in_package"]["primitive_source_faces"] == [[0, 2], [1]]
    assert case["opt_in_package_changed"] is True
    assert case["merge_search_behavior_changed"] is True
    assert case["default_package_mapping"]["fully_mapped"] is True
    assert case["opt_in_package_mapping"]["fully_mapped"] is True
    assert case["opt_in_package_mapping"]["status_counts"] == {"mapped": 2}
    assert case["decision"]["newton_task_comparison_gate"] == (
        "not_triggered_synthetic_package_probe_only"
    )
    assert case["decision"]["claim_boundary"] == (
        CONTROLLED_MERGE_SEARCH_PACKAGE_PROBE_CLAIM_BOUNDARY
    )
    assert case["comparison"]["accepted_normalized_excess_delta"] < 0.0


def test_controlled_merge_search_package_probe_report_is_strict_json_serializable():
    report = build_cpd_like_controlled_merge_search_package_probe_report()

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_like_controlled_merge_search_package_probe" in encoded


def test_controlled_merge_search_newton_probe_runs_contact_gated_tasks(monkeypatch):
    calls = []

    def fake_contact(package, **kwargs):
        calls.append(("contact", package.asset_id))
        return _newton_report(
            package,
            stage="newton_contact_smoke",
            probe_type="contact_canary",
            status="smoke_passed",
            claim_boundary=kwargs["claim_boundary"],
        )

    def fake_drop(package, **kwargs):
        calls.append(("drop", package.asset_id))
        return _newton_report(
            package,
            stage="newton_drop_settle",
            probe_type="drop_settle",
            status="smoke_passed",
            claim_boundary=kwargs["claim_boundary"],
        )

    def fake_sphere(package, **kwargs):
        calls.append(("sphere", package.asset_id))
        return _newton_report(
            package,
            stage="newton_sphere_rain",
            probe_type="sphere_rain",
            status="smoke_passed",
            claim_boundary=kwargs["claim_boundary"],
        )

    monkeypatch.setattr(cpd_synthetic, "run_newton_contact_smoke", fake_contact)
    monkeypatch.setattr(cpd_synthetic, "run_newton_drop_settle", fake_drop)
    monkeypatch.setattr(cpd_synthetic, "run_newton_sphere_rain", fake_sphere)

    report = build_cpd_like_controlled_merge_search_newton_probe_report(
        source_dir="/tmp/newton",
        device="cpu",
    )

    assert report["stage"] == "cpd_like_controlled_merge_search_newton_probe"
    assert report["status"] == "smoke_passed"
    assert report["claim_boundary"] == CONTROLLED_MERGE_SEARCH_NEWTON_PROBE_CLAIM_BOUNDARY
    assert report["real_usd_scope"] == "not_run_synthetic_only"
    assert calls == [
        ("contact", "cost_guided_pair_choice_topology_then_virtual"),
        ("drop", "cost_guided_pair_choice_topology_then_virtual"),
        ("sphere", "cost_guided_pair_choice_topology_then_virtual"),
        ("contact", "cost_guided_pair_choice_cost_guided_pairwise"),
        ("drop", "cost_guided_pair_choice_cost_guided_pairwise"),
        ("sphere", "cost_guided_pair_choice_cost_guided_pairwise"),
    ]
    case = report["cases"][0]
    assert case["case_id"] == "cost_guided_pair_choice"
    assert case["default_package"]["primitive_source_faces"] == [[0, 1], [2]]
    assert case["opt_in_package"]["primitive_source_faces"] == [[0, 2], [1]]
    assert case["default_contact"]["status"] == "smoke_passed"
    assert case["opt_in_contact"]["status"] == "smoke_passed"
    assert case["default_tasks"]["drop_settle"]["status"] == "smoke_passed"
    assert case["opt_in_tasks"]["sphere_rain"]["status"] == "smoke_passed"
    assert case["decision"]["claim_boundary"] == CONTROLLED_MERGE_SEARCH_NEWTON_TASK_CLAIM_BOUNDARY
    assert case["decision"]["collision_quality_claim_supported"] is False


def test_controlled_merge_search_newton_probe_blocks_tasks_when_contact_fails(
    monkeypatch,
):
    def fake_contact(package, **kwargs):
        return _newton_report(
            package,
            stage="newton_contact_smoke",
            probe_type="contact_canary",
            status="dependency_gap",
            claim_boundary=kwargs["claim_boundary"],
            fallback_reason="missing_source",
        )

    def unexpected_task(*args, **kwargs):
        raise AssertionError("tasks must be blocked when contact fails")

    monkeypatch.setattr(cpd_synthetic, "run_newton_contact_smoke", fake_contact)
    monkeypatch.setattr(cpd_synthetic, "run_newton_drop_settle", unexpected_task)
    monkeypatch.setattr(cpd_synthetic, "run_newton_sphere_rain", unexpected_task)

    report = build_cpd_like_controlled_merge_search_newton_probe_report(
        source_dir="/missing/newton",
    )

    assert report["status"] == "dependency_gap"
    case = report["cases"][0]
    assert case["decision"]["status_gate"] == "newton_tasks_blocked_or_failed"
    assert case["opt_in_tasks"]["drop_settle"]["status"] == "blocked_by_contact_canary"
    assert case["opt_in_tasks"]["sphere_rain"]["fallback_reason"] == "dependency_gap"


def test_controlled_merge_search_newton_probe_does_not_pass_when_pair_unchanged(
    monkeypatch,
):
    primitive = PrimitiveSpec(kind="box", primitive_id="box_0", source_faces=(0,))
    package = CollisionPackage(
        "unchanged",
        primitives=(primitive,),
        package_id="unchanged_box",
        status="candidate",
    )

    monkeypatch.setattr(
        cpd_synthetic,
        "_controlled_merge_search_package_pair",
        lambda **kwargs: (package, package),
    )

    def fake_contact(package, **kwargs):
        return _newton_report(
            package,
            stage="newton_contact_smoke",
            probe_type="contact_canary",
            status="smoke_passed",
            claim_boundary=kwargs["claim_boundary"],
        )

    def fake_task(package, **kwargs):
        return _newton_report(
            package,
            stage="newton_task",
            probe_type="task",
            status="smoke_passed",
            claim_boundary=kwargs["claim_boundary"],
        )

    monkeypatch.setattr(cpd_synthetic, "run_newton_contact_smoke", fake_contact)
    monkeypatch.setattr(cpd_synthetic, "run_newton_drop_settle", fake_task)
    monkeypatch.setattr(cpd_synthetic, "run_newton_sphere_rain", fake_task)

    report = build_cpd_like_controlled_merge_search_newton_probe_report(
        source_dir="/tmp/newton",
    )

    assert report["status"] == "partial"
    decision = report["cases"][0]["decision"]
    assert decision["package_pair_changed"] is False
    assert decision["status_gate"] == "opt_in_package_did_not_change"


def test_controlled_merge_search_newton_probe_report_is_strict_json_serializable(
    monkeypatch,
):
    def fake_contact(package, **kwargs):
        return _newton_report(
            package,
            stage="newton_contact_smoke",
            probe_type="contact_canary",
            status="dependency_gap",
            claim_boundary=kwargs["claim_boundary"],
        )

    monkeypatch.setattr(cpd_synthetic, "run_newton_contact_smoke", fake_contact)

    report = build_cpd_like_controlled_merge_search_newton_probe_report(
        source_dir="/missing/newton",
    )
    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_like_controlled_merge_search_newton_probe" in encoded


def test_cost_guided_lookahead_merge_report_compares_greedy_and_lookahead():
    report = build_cpd_like_cost_guided_lookahead_merge_report()

    assert report["stage"] == "cpd_like_cost_guided_lookahead_merge_report"
    assert report["status"] == "smoke_passed"
    assert report["claim_boundary"] == COST_GUIDED_LOOKAHEAD_MERGE_CLAIM_BOUNDARY
    assert report["default_pipeline_changed"] is False
    assert report["newton_task_comparison_triggered"] is False
    assert report["real_usd_rerun_triggered"] is False
    assert report["collision_quality_claim_supported"] is False
    assert report["merge_policy_superiority_claim_supported"] is False
    assert report["tiny_mesh_guard_applied"] is True

    case = report["cases"][0]
    assert case["case_id"] == "lookahead_merge_trap"
    assert case["greedy"]["merge_search_policy"] == "cost_guided_pairwise"
    assert case["lookahead"]["merge_search_policy"] == "two_step_lookahead"
    assert case["greedy"]["primitive_source_faces"] == [[0, 2, 3], [1]]
    assert case["lookahead"]["primitive_source_faces"] == [[0, 1], [2, 3]]
    assert case["decision"]["lookahead_decision_changed"] is True
    assert case["decision"]["projected_cost_improved"] is True
    assert case["decision"]["newton_task_comparison_triggered"] is False
    assert case["decision"]["real_usd_rerun_triggered"] is False
    assert case["decision"]["collision_quality_claim_supported"] is False
    assert case["decision"]["merge_policy_superiority_claim_supported"] is False
    first_step = case["lookahead"]["merge_trace"][0]
    assert first_step["projected_followup_normalized_excess_volume"] > 0.0
    assert first_step["projected_total_normalized_excess_volume"] == (
        case["lookahead"]["accepted_normalized_excess_sum"]
    )
    assert case["decision"]["greedy_projected_total_normalized_excess"] == (
        case["greedy"]["merge_trace"][0]["projected_total_normalized_excess_volume"]
    )
    assert case["decision"]["lookahead_projected_total_normalized_excess"] == (
        first_step["projected_total_normalized_excess_volume"]
    )


def test_cost_guided_lookahead_merge_report_is_strict_json_serializable():
    report = build_cpd_like_cost_guided_lookahead_merge_report()

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_like_cost_guided_lookahead_merge_report" in encoded


def test_cost_guided_lookahead_package_probe_outputs_mapped_changed_package():
    report = build_cpd_like_cost_guided_lookahead_package_probe_report()

    assert report["stage"] == "cpd_like_cost_guided_lookahead_package_probe"
    assert report["status"] == "smoke_passed"
    assert report["claim_boundary"] == COST_GUIDED_LOOKAHEAD_PACKAGE_PROBE_CLAIM_BOUNDARY
    assert report["default_pipeline_changed"] is False
    assert report["newton_task_comparison_triggered"] is False
    assert report["real_usd_rerun_triggered"] is False
    assert report["collision_quality_claim_supported"] is False
    assert report["merge_policy_superiority_claim_supported"] is False

    case = report["cases"][0]
    assert case["case_id"] == "lookahead_merge_trap"
    assert case["greedy_package"]["primitive_source_faces"] == [[0, 2, 3], [1]]
    assert case["lookahead_package"]["primitive_source_faces"] == [[0, 1], [2, 3]]
    assert case["package_pair_changed"] is True
    assert case["lookahead_package_changed"] is True
    assert case["merge_search_behavior_changed"] is True
    assert case["greedy_package_mapping"]["fully_mapped"] is True
    assert case["lookahead_package_mapping"]["fully_mapped"] is True
    assert case["lookahead_package_mapping"]["status_counts"] == {"mapped": 2}
    assert case["comparison"]["projected_total_normalized_excess_delta"] < 0.0
    assert case["decision"]["newton_mapping_summary_recorded"] is True
    assert case["decision"]["newton_task_comparison_triggered"] is False
    assert case["decision"]["newton_task_comparison_gate"] == (
        "not_triggered_synthetic_package_probe_only"
    )
    assert case["decision"]["claim_boundary"] == (
        COST_GUIDED_LOOKAHEAD_PACKAGE_PROBE_CLAIM_BOUNDARY
    )
    assert "greedy_contact" not in case
    assert "lookahead_tasks" not in case


def test_cost_guided_lookahead_package_probe_report_is_strict_json_serializable():
    report = build_cpd_like_cost_guided_lookahead_package_probe_report()

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_like_cost_guided_lookahead_package_probe" in encoded


def test_cost_guided_lookahead_newton_probe_runs_contact_gated_tasks(monkeypatch):
    calls = []

    def fake_contact(package, **kwargs):
        calls.append(("contact", package.asset_id))
        return _newton_report(
            package,
            stage="newton_contact_smoke",
            probe_type="contact_canary",
            status="smoke_passed",
            claim_boundary=kwargs["claim_boundary"],
        )

    def fake_drop(package, **kwargs):
        calls.append(("drop", package.asset_id))
        return _newton_report(
            package,
            stage="newton_drop_settle",
            probe_type="drop_settle",
            status="smoke_passed",
            claim_boundary=kwargs["claim_boundary"],
        )

    def fake_sphere(package, **kwargs):
        calls.append(("sphere", package.asset_id))
        return _newton_report(
            package,
            stage="newton_sphere_rain",
            probe_type="sphere_rain",
            status="smoke_passed",
            claim_boundary=kwargs["claim_boundary"],
        )

    monkeypatch.setattr(cpd_synthetic, "run_newton_contact_smoke", fake_contact)
    monkeypatch.setattr(cpd_synthetic, "run_newton_drop_settle", fake_drop)
    monkeypatch.setattr(cpd_synthetic, "run_newton_sphere_rain", fake_sphere)

    report = build_cpd_like_cost_guided_lookahead_newton_probe_report(
        source_dir="/tmp/newton",
        device="cpu",
    )

    assert report["stage"] == "cpd_like_cost_guided_lookahead_newton_probe"
    assert report["status"] == "smoke_passed"
    assert report["claim_boundary"] == COST_GUIDED_LOOKAHEAD_NEWTON_PROBE_CLAIM_BOUNDARY
    assert report["real_usd_scope"] == "not_run_synthetic_only"
    assert report["newton_task_comparison_triggered"] is True
    assert calls == [
        ("contact", "lookahead_merge_trap_cost_guided_pairwise"),
        ("drop", "lookahead_merge_trap_cost_guided_pairwise"),
        ("sphere", "lookahead_merge_trap_cost_guided_pairwise"),
        ("contact", "lookahead_merge_trap_two_step_lookahead"),
        ("drop", "lookahead_merge_trap_two_step_lookahead"),
        ("sphere", "lookahead_merge_trap_two_step_lookahead"),
    ]
    case = report["cases"][0]
    assert case["case_id"] == "lookahead_merge_trap"
    assert case["greedy_package"]["primitive_source_faces"] == [[0, 2, 3], [1]]
    assert case["lookahead_package"]["primitive_source_faces"] == [[0, 1], [2, 3]]
    assert case["greedy_contact"]["status"] == "smoke_passed"
    assert case["lookahead_contact"]["status"] == "smoke_passed"
    assert case["greedy_tasks"]["drop_settle"]["status"] == "smoke_passed"
    assert case["lookahead_tasks"]["sphere_rain"]["status"] == "smoke_passed"
    assert case["decision"]["claim_boundary"] == (
        COST_GUIDED_LOOKAHEAD_NEWTON_TASK_CLAIM_BOUNDARY
    )
    assert case["decision"]["collision_quality_claim_supported"] is False


def test_cost_guided_lookahead_newton_probe_blocks_tasks_when_contact_fails(
    monkeypatch,
):
    def fake_contact(package, **kwargs):
        return _newton_report(
            package,
            stage="newton_contact_smoke",
            probe_type="contact_canary",
            status="dependency_gap",
            claim_boundary=kwargs["claim_boundary"],
            fallback_reason="missing_source",
        )

    def unexpected_task(*args, **kwargs):
        raise AssertionError("tasks must be blocked when contact fails")

    monkeypatch.setattr(cpd_synthetic, "run_newton_contact_smoke", fake_contact)
    monkeypatch.setattr(cpd_synthetic, "run_newton_drop_settle", unexpected_task)
    monkeypatch.setattr(cpd_synthetic, "run_newton_sphere_rain", unexpected_task)

    report = build_cpd_like_cost_guided_lookahead_newton_probe_report(
        source_dir="/missing/newton",
    )

    assert report["status"] == "dependency_gap"
    case = report["cases"][0]
    assert case["decision"]["status_gate"] == "newton_tasks_blocked_or_failed"
    assert case["lookahead_tasks"]["drop_settle"]["status"] == (
        "blocked_by_contact_canary"
    )
    assert case["lookahead_tasks"]["sphere_rain"]["fallback_reason"] == "dependency_gap"


def test_cost_guided_lookahead_newton_probe_keeps_passing_lane_running(
    monkeypatch,
):
    calls = []

    def fake_contact(package, **kwargs):
        calls.append(("contact", package.asset_id))
        status = (
            "dependency_gap"
            if package.asset_id == "lookahead_merge_trap_cost_guided_pairwise"
            else "smoke_passed"
        )
        return _newton_report(
            package,
            stage="newton_contact_smoke",
            probe_type="contact_canary",
            status=status,
            claim_boundary=kwargs["claim_boundary"],
            fallback_reason="missing_source" if status != "smoke_passed" else None,
        )

    def fake_drop(package, **kwargs):
        calls.append(("drop", package.asset_id))
        return _newton_report(
            package,
            stage="newton_drop_settle",
            probe_type="drop_settle",
            status="smoke_passed",
            claim_boundary=kwargs["claim_boundary"],
        )

    def fake_sphere(package, **kwargs):
        calls.append(("sphere", package.asset_id))
        return _newton_report(
            package,
            stage="newton_sphere_rain",
            probe_type="sphere_rain",
            status="smoke_passed",
            claim_boundary=kwargs["claim_boundary"],
        )

    monkeypatch.setattr(cpd_synthetic, "run_newton_contact_smoke", fake_contact)
    monkeypatch.setattr(cpd_synthetic, "run_newton_drop_settle", fake_drop)
    monkeypatch.setattr(cpd_synthetic, "run_newton_sphere_rain", fake_sphere)

    report = build_cpd_like_cost_guided_lookahead_newton_probe_report(
        source_dir="/tmp/newton",
    )

    assert report["status"] == "dependency_gap"
    assert calls == [
        ("contact", "lookahead_merge_trap_cost_guided_pairwise"),
        ("contact", "lookahead_merge_trap_two_step_lookahead"),
        ("drop", "lookahead_merge_trap_two_step_lookahead"),
        ("sphere", "lookahead_merge_trap_two_step_lookahead"),
    ]
    case = report["cases"][0]
    assert case["greedy_tasks"]["drop_settle"]["status"] == "blocked_by_contact_canary"
    assert case["lookahead_tasks"]["drop_settle"]["status"] == "smoke_passed"


def test_cost_guided_lookahead_newton_probe_does_not_pass_when_pair_unchanged(
    monkeypatch,
):
    primitive = PrimitiveSpec(kind="box", primitive_id="box_0", source_faces=(0,))
    package = CollisionPackage(
        "unchanged",
        primitives=(primitive,),
        package_id="unchanged_box",
        status="candidate",
    )

    monkeypatch.setattr(
        cpd_synthetic,
        "_lookahead_merge_package_pair",
        lambda *args, **kwargs: (package, package),
    )

    def fake_contact(package, **kwargs):
        return _newton_report(
            package,
            stage="newton_contact_smoke",
            probe_type="contact_canary",
            status="smoke_passed",
            claim_boundary=kwargs["claim_boundary"],
        )

    def fake_task(package, **kwargs):
        return _newton_report(
            package,
            stage="newton_task",
            probe_type="task",
            status="smoke_passed",
            claim_boundary=kwargs["claim_boundary"],
        )

    monkeypatch.setattr(cpd_synthetic, "run_newton_contact_smoke", fake_contact)
    monkeypatch.setattr(cpd_synthetic, "run_newton_drop_settle", fake_task)
    monkeypatch.setattr(cpd_synthetic, "run_newton_sphere_rain", fake_task)

    report = build_cpd_like_cost_guided_lookahead_newton_probe_report(
        source_dir="/tmp/newton",
    )

    assert report["status"] == "partial"
    decision = report["cases"][0]["decision"]
    assert decision["package_pair_changed"] is False
    assert decision["status_gate"] == "lookahead_package_did_not_change"


def test_cost_guided_lookahead_newton_probe_does_not_pass_with_wrong_faces(
    monkeypatch,
):
    greedy_package = CollisionPackage(
        "wrong_greedy",
        primitives=(
            PrimitiveSpec(kind="box", primitive_id="box_0", source_faces=(0,)),
            PrimitiveSpec(kind="box", primitive_id="box_1", source_faces=(1,)),
        ),
        package_id="wrong_greedy_box",
        status="candidate",
    )
    lookahead_package = CollisionPackage(
        "wrong_lookahead",
        primitives=(
            PrimitiveSpec(kind="box", primitive_id="box_2", source_faces=(2,)),
            PrimitiveSpec(kind="box", primitive_id="box_3", source_faces=(3,)),
        ),
        package_id="wrong_lookahead_box",
        status="candidate",
    )

    monkeypatch.setattr(
        cpd_synthetic,
        "_lookahead_merge_package_pair",
        lambda *args, **kwargs: (greedy_package, lookahead_package),
    )

    def fake_contact(package, **kwargs):
        return _newton_report(
            package,
            stage="newton_contact_smoke",
            probe_type="contact_canary",
            status="smoke_passed",
            claim_boundary=kwargs["claim_boundary"],
        )

    def fake_task(package, **kwargs):
        return _newton_report(
            package,
            stage="newton_task",
            probe_type="task",
            status="smoke_passed",
            claim_boundary=kwargs["claim_boundary"],
        )

    monkeypatch.setattr(cpd_synthetic, "run_newton_contact_smoke", fake_contact)
    monkeypatch.setattr(cpd_synthetic, "run_newton_drop_settle", fake_task)
    monkeypatch.setattr(cpd_synthetic, "run_newton_sphere_rain", fake_task)

    report = build_cpd_like_cost_guided_lookahead_newton_probe_report(
        source_dir="/tmp/newton",
    )

    assert report["status"] == "partial"
    decision = report["cases"][0]["decision"]
    assert decision["package_pair_changed"] is True
    assert decision["expected_package_faces"] is False
    assert decision["status_gate"] == "lookahead_package_faces_unexpected"


def test_cost_guided_lookahead_newton_probe_report_is_strict_json_serializable(
    monkeypatch,
):
    def fake_contact(package, **kwargs):
        return _newton_report(
            package,
            stage="newton_contact_smoke",
            probe_type="contact_canary",
            status="dependency_gap",
            claim_boundary=kwargs["claim_boundary"],
        )

    monkeypatch.setattr(cpd_synthetic, "run_newton_contact_smoke", fake_contact)

    report = build_cpd_like_cost_guided_lookahead_newton_probe_report(
        source_dir="/missing/newton",
    )
    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_like_cost_guided_lookahead_newton_probe" in encoded


def test_four_block_slice_report_summarizes_cost_guided_lookahead():
    report = build_cpd_like_four_block_slice_report()

    assert report["stage"] == "cpd_like_four_block_slice_report"
    assert report["status"] == "smoke_passed"
    assert report["claim_boundary"] == FOUR_BLOCK_SLICE_REPORT_CLAIM_BOUNDARY
    assert report["slice_id"] == "cost_guided_lookahead"
    assert report["command_only"] is True
    assert report["synthetic_only"] is True
    assert report["real_usd_rerun_triggered"] is False
    assert report["newton_task_comparison_triggered"] is False
    assert report["report_newton_task_comparison_triggered"] is False

    blocks = {block["block_id"]: block for block in report["blocks"]}
    assert list(blocks) == [
        "primitive_fitting_selection",
        "merge_search",
        "offline_diagnostic_reports",
        "newton_task_comparison",
    ]
    assert blocks["primitive_fitting_selection"]["status"] == (
        "not_changed_for_this_slice"
    )
    assert blocks["merge_search"]["status"] == "complete"
    assert blocks["offline_diagnostic_reports"]["status"] == "complete"
    assert blocks["newton_task_comparison"]["status"] == "complete"
    for block in blocks.values():
        assert block["evidence_records"]
        assert all(record["exists"] is True for record in block["evidence_records"])
        if block["block_id"] == "newton_task_comparison":
            assert block["recorded_task_smoke_available"] is True

    assert report["summary"]["four_block_record_map_complete"] is True
    assert "workbench_mvp_gap_resolved" not in report["summary"]
    assert report["next_action"]["blocked_real_asset_rerun"] is True
    assert report["next_action"]["requires_separate_real_package_change"] is True
    assert report["next_action"]["required_real_asset_gates"] == [
        "full_mapping",
        "contact_canary",
        "task_gate",
        "dated_record",
    ]
    encoded = json.dumps(report, allow_nan=False, sort_keys=True)
    for forbidden_key in (
        "cases",
        "greedy_package",
        "lookahead_package",
        "greedy_contact",
        "lookahead_contact",
        "greedy_tasks",
        "lookahead_tasks",
        "source_dir",
        "device",
    ):
        assert forbidden_key not in encoded


def test_four_block_slice_report_returns_partial_when_record_missing(monkeypatch):
    monkeypatch.setattr(
        cpd_synthetic,
        "_FOUR_BLOCK_COST_GUIDED_LOOKAHEAD_RECORDS",
        {
            "merge_search": ("docs/records/does-not-exist.md",),
            "offline_diagnostic_reports": (),
            "newton_task_comparison": (),
            "primitive_fitting_selection": (),
        },
    )

    report = build_cpd_like_four_block_slice_report()

    assert report["status"] == "partial"
    assert report["missing_evidence_records"] == ["docs/records/does-not-exist.md"]
    blocks = {block["block_id"]: block for block in report["blocks"]}
    assert blocks["merge_search"]["status"] == "partial"
    assert blocks["merge_search"]["claim_supported"] == []
    assert "record-backed claim withheld until evidence records exist" in blocks[
        "merge_search"
    ]["claim_not_supported"]


def test_four_block_slice_report_does_not_rerun_source_reports(monkeypatch):
    def unexpected_call(*args, **kwargs):
        raise AssertionError("four-block report must only read record path metadata")

    monkeypatch.setattr(cpd_synthetic, "decompose_mesh", unexpected_call)
    monkeypatch.setattr(cpd_synthetic, "package_from_cpd_like_report", unexpected_call)
    monkeypatch.setattr(
        cpd_synthetic,
        "build_cpd_like_cost_guided_lookahead_merge_report",
        unexpected_call,
    )
    monkeypatch.setattr(
        cpd_synthetic,
        "build_cpd_like_cost_guided_lookahead_package_probe_report",
        unexpected_call,
    )
    monkeypatch.setattr(
        cpd_synthetic,
        "build_cpd_like_cost_guided_lookahead_newton_probe_report",
        unexpected_call,
    )
    monkeypatch.setattr(cpd_synthetic, "run_newton_contact_smoke", unexpected_call)
    monkeypatch.setattr(cpd_synthetic, "run_newton_drop_settle", unexpected_call)
    monkeypatch.setattr(cpd_synthetic, "run_newton_sphere_rain", unexpected_call)

    report = build_cpd_like_four_block_slice_report()

    assert report["status"] == "smoke_passed"


def test_four_block_slice_report_record_paths_are_cwd_independent(
    monkeypatch,
    tmp_path,
):
    monkeypatch.chdir(tmp_path)

    report = build_cpd_like_four_block_slice_report()

    assert report["status"] == "smoke_passed"


def test_four_block_slice_report_rejects_unsupported_slice():
    report = build_cpd_like_four_block_slice_report(slice_id="unknown")

    assert report["status"] == "partial"
    assert report["fallback_reason"] == "unsupported_slice"
    assert report["summary"]["four_block_record_map_complete"] is False
    assert "workbench_mvp_gap_resolved" not in report["summary"]


def test_four_block_slice_report_is_strict_json_serializable():
    report = build_cpd_like_four_block_slice_report()
    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_like_four_block_slice_report" in encoded


def test_cylinder_scoring_policy_newton_probe_runs_contact_gated_tasks(monkeypatch):
    calls = []

    def fake_contact(package, **kwargs):
        calls.append(("contact", package.primitives[0].kind))
        return _newton_report(
            package,
            stage="newton_contact_smoke",
            probe_type="contact_canary",
            status="smoke_passed",
            claim_boundary=kwargs["claim_boundary"],
        )

    def fake_drop(package, **kwargs):
        calls.append(("drop", package.primitives[0].kind))
        return _newton_report(
            package,
            stage="newton_drop_settle",
            probe_type="drop_settle",
            status="smoke_passed",
            claim_boundary=kwargs["claim_boundary"],
        )

    def fake_sphere(package, **kwargs):
        calls.append(("sphere", package.primitives[0].kind))
        return _newton_report(
            package,
            stage="newton_sphere_rain",
            probe_type="sphere_rain",
            status="smoke_passed",
            claim_boundary=kwargs["claim_boundary"],
        )

    monkeypatch.setattr(cpd_synthetic, "run_newton_contact_smoke", fake_contact)
    monkeypatch.setattr(cpd_synthetic, "run_newton_drop_settle", fake_drop)
    monkeypatch.setattr(cpd_synthetic, "run_newton_sphere_rain", fake_sphere)

    report = build_cpd_like_cylinder_scoring_policy_newton_probe_report(
        source_dir="/tmp/newton",
        device="cpu",
    )

    assert report["stage"] == "cpd_like_cylinder_scoring_policy_newton_probe"
    assert report["status"] == "smoke_passed"
    assert report["claim_boundary"] == CYLINDER_SCORING_POLICY_NEWTON_PROBE_CLAIM_BOUNDARY
    assert report["real_usd_scope"] == "not_run_synthetic_only"
    assert calls == [
        ("contact", "box"),
        ("drop", "box"),
        ("sphere", "box"),
        ("contact", "cylinder"),
        ("drop", "cylinder"),
        ("sphere", "cylinder"),
    ]
    case = report["cases"][0]
    assert case["case_id"] == "cylinder_near_miss_cluster"
    assert case["default_package"]["primitive_kinds"] == ["box"]
    assert case["opt_in_package"]["primitive_kinds"] == ["cylinder"]
    assert case["default_contact"]["status"] == "smoke_passed"
    assert case["opt_in_contact"]["status"] == "smoke_passed"
    assert case["default_tasks"]["drop_settle"]["status"] == "smoke_passed"
    assert case["opt_in_tasks"]["sphere_rain"]["status"] == "smoke_passed"
    assert case["decision"]["collision_quality_claim_supported"] is False


def test_cylinder_scoring_policy_newton_probe_blocks_tasks_when_contact_fails(monkeypatch):
    def fake_contact(package, **kwargs):
        return _newton_report(
            package,
            stage="newton_contact_smoke",
            probe_type="contact_canary",
            status="dependency_gap",
            claim_boundary=kwargs["claim_boundary"],
            fallback_reason="missing_source",
        )

    def unexpected_task(*args, **kwargs):
        raise AssertionError("tasks must be blocked when contact fails")

    monkeypatch.setattr(cpd_synthetic, "run_newton_contact_smoke", fake_contact)
    monkeypatch.setattr(cpd_synthetic, "run_newton_drop_settle", unexpected_task)
    monkeypatch.setattr(cpd_synthetic, "run_newton_sphere_rain", unexpected_task)

    report = build_cpd_like_cylinder_scoring_policy_newton_probe_report(
        source_dir="/missing/newton",
    )

    assert report["status"] == "dependency_gap"
    case = report["cases"][0]
    assert case["opt_in_tasks"]["drop_settle"]["status"] == "blocked_by_contact_canary"
    assert case["opt_in_tasks"]["sphere_rain"]["fallback_reason"] == "dependency_gap"


def test_cylinder_scoring_policy_newton_probe_does_not_claim_change_when_pair_unchanged(
    monkeypatch,
):
    primitive = PrimitiveSpec(kind="box", primitive_id="box_0")
    package = CollisionPackage(
        "unchanged",
        primitives=(primitive,),
        package_id="unchanged_box",
        status="candidate",
    )

    monkeypatch.setattr(
        cpd_synthetic,
        "_cylinder_scoring_policy_package_pair",
        lambda **kwargs: (package, package),
    )

    def fake_contact(package, **kwargs):
        return _newton_report(
            package,
            stage="newton_contact_smoke",
            probe_type="contact_canary",
            status="smoke_passed",
            claim_boundary=kwargs["claim_boundary"],
        )

    def fake_task(package, **kwargs):
        return _newton_report(
            package,
            stage="newton_task",
            probe_type="task",
            status="smoke_passed",
            claim_boundary=kwargs["claim_boundary"],
        )

    monkeypatch.setattr(cpd_synthetic, "run_newton_contact_smoke", fake_contact)
    monkeypatch.setattr(cpd_synthetic, "run_newton_drop_settle", fake_task)
    monkeypatch.setattr(cpd_synthetic, "run_newton_sphere_rain", fake_task)

    report = build_cpd_like_cylinder_scoring_policy_newton_probe_report(
        source_dir="/tmp/newton",
    )

    assert report["status"] == "partial"
    decision = report["cases"][0]["decision"]
    assert decision["opt_in_package_changed"] is False
    assert decision["package_pair_changed"] is False
    assert decision["status_gate"] == "opt_in_package_did_not_change"


def test_cylinder_scoring_policy_newton_probe_detects_same_kind_payload_change(
    monkeypatch,
):
    default_package = CollisionPackage(
        "default",
        primitives=(
            PrimitiveSpec(
                kind="box",
                primitive_id="default_box",
                dimensions={"extents": (1.0, 1.0, 1.0)},
                source_faces=(0, 1),
            ),
        ),
        package_id="default_box",
        status="candidate",
    )
    opt_in_package = CollisionPackage(
        "opt_in",
        primitives=(
            PrimitiveSpec(
                kind="box",
                primitive_id="opt_in_box",
                dimensions={"extents": (1.25, 1.0, 1.0)},
                source_faces=(0, 1),
            ),
        ),
        package_id="opt_in_box",
        status="candidate",
    )

    monkeypatch.setattr(
        cpd_synthetic,
        "_cylinder_scoring_policy_package_pair",
        lambda **kwargs: (default_package, opt_in_package),
    )

    def fake_contact(package, **kwargs):
        return _newton_report(
            package,
            stage="newton_contact_smoke",
            probe_type="contact_canary",
            status="smoke_passed",
            claim_boundary=kwargs["claim_boundary"],
        )

    def fake_task(package, **kwargs):
        return _newton_report(
            package,
            stage="newton_task",
            probe_type="task",
            status="smoke_passed",
            claim_boundary=kwargs["claim_boundary"],
        )

    monkeypatch.setattr(cpd_synthetic, "run_newton_contact_smoke", fake_contact)
    monkeypatch.setattr(cpd_synthetic, "run_newton_drop_settle", fake_task)
    monkeypatch.setattr(cpd_synthetic, "run_newton_sphere_rain", fake_task)

    report = build_cpd_like_cylinder_scoring_policy_newton_probe_report(
        source_dir="/tmp/newton",
    )

    assert report["status"] == "smoke_passed"
    decision = report["cases"][0]["decision"]
    assert decision["opt_in_package_changed"] is True
    assert decision["package_pair_changed"] is True
    assert decision["primitive_kind_changed"] is False


def test_cylinder_scoring_policy_newton_probe_report_is_strict_json_serializable(
    monkeypatch,
):
    def fake_contact(package, **kwargs):
        return _newton_report(
            package,
            stage="newton_contact_smoke",
            probe_type="contact_canary",
            status="dependency_gap",
            claim_boundary=kwargs["claim_boundary"],
        )

    monkeypatch.setattr(cpd_synthetic, "run_newton_contact_smoke", fake_contact)

    report = build_cpd_like_cylinder_scoring_policy_newton_probe_report(
        source_dir="/missing/newton",
    )
    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_like_cylinder_scoring_policy_newton_probe" in encoded


def test_cylinder_axis_search_selects_squat_cylinder_over_box():
    mesh = _squat_cylinder_mesh()

    fit = fit_best_primitive(
        mesh,
        frozenset(range(mesh.face_count)),
        primitive_subset=("box", "cylinder"),
    )
    candidates = {
        candidate.primitive_type: candidate
        for candidate in fit_primitive_candidates(
            mesh,
            frozenset(range(mesh.face_count)),
            primitive_subset=("box", "cylinder"),
        )
    }

    assert fit.primitive_type == "cylinder"
    assert candidates["cylinder"].weighted_volume < candidates["box"].weighted_volume
    assert candidates["cylinder"].dimensions["axis_selection"] == (
        "min_volume_over_candidate_axes"
    )


def test_fit_primitive_candidates_preserves_subset_order_and_paper_gap_metadata():
    mesh = cpd_synthetic._adjacent_square_mesh()

    candidates = fit_primitive_candidates(
        mesh,
        frozenset(range(mesh.face_count)),
        primitive_subset=("box", "box", "frustum", "capped_cylinder"),
    )

    assert [candidate.primitive_type for candidate in candidates] == [
        "box",
        "capped_cylinder",
    ]
    assert {candidate.source_faces for candidate in candidates} == {(0, 1)}
    assert all(
        candidate.unsupported_primitives == ("frustum", "trapezoidal_prism")
        for candidate in candidates
    )


def _newton_report(
    package,
    *,
    stage: str,
    probe_type: str,
    status: str,
    claim_boundary: str,
    fallback_reason: str | None = None,
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
        type_counts={package.primitives[0].kind: 1},
        shape_mappings=(),
        contact_canaries=(),
        claim_boundary=claim_boundary,
        fallback_reason=fallback_reason,
    )


def test_fit_best_primitive_breaks_equal_cost_ties_by_subset_order(monkeypatch):
    mesh = cpd_synthetic._adjacent_square_mesh()

    def fake_fit_primitive(primitive_type, points, axes, source_faces):
        return PrimitiveFit(
            primitive_type=primitive_type,
            source_faces=source_faces,
            center=(0.0, 0.0, 0.0),
            axes=((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
            dimensions={"test": primitive_type},
            volume=1.0,
            weighted_volume=1.0,
            contains_assigned_points=True,
        )

    monkeypatch.setattr(cpd_primitives, "_fit_primitive", fake_fit_primitive)

    first = fit_best_primitive(
        mesh,
        frozenset(range(mesh.face_count)),
        primitive_subset=("sphere", "box"),
    )
    second = fit_best_primitive(
        mesh,
        frozenset(range(mesh.face_count)),
        primitive_subset=("box", "sphere"),
    )

    assert first.primitive_type == "sphere"
    assert second.primitive_type == "box"


def test_fit_best_primitive_blocks_low_support_native_extension_when_fallback_exists(
    monkeypatch,
):
    mesh = cpd_synthetic._adjacent_square_mesh()

    def fake_fit_primitive(primitive_type, points, axes, source_faces):
        weighted_volumes = {
            "box": 2.0,
            "cylinder": 1.0,
        }
        volume = weighted_volumes[primitive_type]
        return PrimitiveFit(
            primitive_type=primitive_type,
            source_faces=source_faces,
            center=(0.0, 0.0, 0.0),
            axes=((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
            dimensions={"test": primitive_type},
            volume=volume,
            weighted_volume=volume,
            contains_assigned_points=True,
        )

    monkeypatch.setattr(cpd_primitives, "_fit_primitive", fake_fit_primitive)

    fit = fit_best_primitive(
        mesh,
        frozenset(range(mesh.face_count)),
        primitive_subset=("box", "cylinder"),
    )
    ranked = rank_primitive_candidates_for_selection(
        mesh,
        frozenset(range(mesh.face_count)),
        fit_primitive_candidates(
            mesh,
            frozenset(range(mesh.face_count)),
            primitive_subset=("box", "cylinder"),
        ),
    )

    assert fit.primitive_type == "box"
    assert [row.primitive_type for row in ranked] == ["box", "cylinder"]
    assert [row.raw_cost_rank for row in ranked] == [2, 1]
    assert ranked[0].selection_admissible is True
    assert ranked[1].selection_admissible is False
    assert ranked[1].selection_admissibility_reason == "insufficient_extension_support"
    assert ranked[1].support["source_face_count"] == 2
    assert ranked[1].support["unique_point_count"] == 4


def test_cone_proxy_stays_finite_when_forced_on_non_cone_fixture():
    mesh = cpd_synthetic._cylindrical_rod_mesh()

    fit = fit_best_primitive(
        mesh,
        frozenset(range(mesh.face_count)),
        primitive_subset=("cone",),
    )

    assert fit.primitive_type == "cone"
    assert math.isfinite(fit.volume)
    assert math.isfinite(fit.weighted_volume)
    json.dumps(fit.to_dict(), allow_nan=False)


def test_newton_native_fitting_comparison_respects_custom_legacy_subset():
    report = build_newton_native_fitting_comparison_report(
        legacy_subset=("box", "sphere", "capsule", "cylinder"),
    )

    cases = {case["case_id"]: case for case in report["cases"]}
    cylindrical = cases["cylindrical_rod"]

    assert report["status"] == "partial"
    assert cylindrical["legacy"]["selected_primitive_kind"] == "cylinder"
    assert cylindrical["native"]["selected_primitive_kind"] == "cylinder"
    assert cylindrical["comparison"]["native_selected_newton_extension"] is False
    assert cylindrical["expectation_status"] == "mismatched"


def test_cylinder_proxy_floors_zero_span_volume():
    mesh = TriangleMesh(
        points=np.array(
            [
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
            ]
        ),
        faces=np.array([[0, 1, 2]]),
    )

    fit = fit_best_primitive(mesh, frozenset({0}), primitive_subset=("cylinder",))

    assert fit.primitive_type == "cylinder"
    assert fit.dimensions["half_height"] > 0.0
    assert fit.volume > 0.0
    json.dumps(fit.to_dict(), allow_nan=False)


def _squat_cylinder_mesh(segment_count: int = 16) -> TriangleMesh:
    radius = 1.0
    height = 0.1
    points: list[list[float]] = []
    for z in (-height * 0.5, height * 0.5):
        for index in range(segment_count):
            angle = 2.0 * math.pi * index / segment_count
            points.append([radius * math.cos(angle), radius * math.sin(angle), z])
    bottom_center = len(points)
    points.append([0.0, 0.0, -height * 0.5])
    top_center = len(points)
    points.append([0.0, 0.0, height * 0.5])

    faces: list[list[int]] = []
    for index in range(segment_count):
        next_index = (index + 1) % segment_count
        bottom_left = index
        bottom_right = next_index
        top_left = segment_count + index
        top_right = segment_count + next_index
        faces.append([bottom_left, bottom_right, top_right])
        faces.append([bottom_left, top_right, top_left])
        faces.append([bottom_center, bottom_right, bottom_left])
        faces.append([top_center, top_left, top_right])

    return TriangleMesh(points=np.array(points, dtype=float), faces=np.array(faces, dtype=int))
