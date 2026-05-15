import json

from primitive_collision_compiler.baselines.cpd_like.synthetic import (
    SYNTHETIC_COMPARISON_CLAIM_BOUNDARY,
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
