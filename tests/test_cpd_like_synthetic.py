import json

from primitive_collision_compiler.baselines.cpd_like.synthetic import (
    SYNTHETIC_COMPARISON_CLAIM_BOUNDARY,
    build_cpd_like_cost_guided_synthetic_comparison_report,
    build_cpd_like_synthetic_comparison_report,
)


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
