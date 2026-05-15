import json
import math

import numpy as np

import primitive_collision_compiler.baselines.cpd_like.synthetic as cpd_synthetic
from primitive_collision_compiler.baselines.cpd_like.primitives import fit_best_primitive
from primitive_collision_compiler.baselines.cpd_like.synthetic import (
    EXPECTED_FAILURE_WORKBENCH_CLAIM_BOUNDARY,
    NEWTON_NATIVE_FITTING_COMPARISON_CLAIM_BOUNDARY,
    SYNTHETIC_COMPARISON_CLAIM_BOUNDARY,
    build_cpd_like_cost_guided_synthetic_comparison_report,
    build_cpd_like_expected_failure_synthetic_workbench_report,
    build_cpd_like_synthetic_comparison_report,
    build_newton_native_fitting_comparison_report,
)
from primitive_collision_compiler.geometry.mesh import TriangleMesh


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


def test_synthetic_comparison_report_is_strict_json_serializable():
    report = build_cpd_like_synthetic_comparison_report()

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_like_synthetic_objective_comparison" in encoded


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


def test_newton_native_fitting_comparison_selects_native_primitives():
    report = build_newton_native_fitting_comparison_report()

    assert report["stage"] == "cpd_like_newton_native_fitting_comparison"
    assert report["status"] == "smoke_passed"
    assert report["claim_boundary"] == NEWTON_NATIVE_FITTING_COMPARISON_CLAIM_BOUNDARY
    assert [case["case_id"] for case in report["cases"]] == [
        "cylindrical_rod",
        "tapered_cone",
        "ellipsoid_blob",
    ]

    expected_native = {
        "cylindrical_rod": "cylinder",
        "tapered_cone": "cone",
        "ellipsoid_blob": "ellipsoid",
    }
    for case in report["cases"]:
        case_id = case["case_id"]
        assert case["expectation_status"] == "matched"
        assert case["expected_native_primitive"] == expected_native[case_id]
        assert case["legacy"]["selected_primitive_kind"] in {"box", "sphere", "capsule"}
        assert case["native"]["selected_primitive_kind"] == expected_native[case_id]
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
