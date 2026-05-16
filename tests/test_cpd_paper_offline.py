import json

from primitive_collision_compiler.baselines.cpd_paper.offline import (
    CPD_PAPER_OFFLINE_CLAIM_BOUNDARY,
    build_cpd_paper_offline_report,
)


def test_cpd_paper_offline_report_covers_first_toy_slice():
    report = build_cpd_paper_offline_report()

    assert report["stage"] == "cpd_paper_offline_report"
    assert report["status"] == "partial"
    assert report["report_generation_status"] == "smoke_passed"
    assert report["claim_boundary"] == CPD_PAPER_OFFLINE_CLAIM_BOUNDARY
    assert report["newton_runtime_triggered"] is False
    assert report["real_usd_triggered"] is False
    assert report["benchmark_triggered"] is False
    assert report["paper_faithful_offline_supported"] is False
    assert report["paper_faithfulness"]["status"] == "partial"
    assert report["source_scope"] == "synthetic_toy_fixtures_only"
    assert set(report["failure_labels"]) == {
        "polygon_and_quad_face_policy_missing",
        "paper_flat_capped_cylinder_fit_missing",
        "frustum_fit_missing",
        "trapezoidal_prism_fit_missing",
        "full_priority_queue_trace_missing",
        "component_pair_edge_insertion_missing",
        "postprocess_enclosed_primitive_culling_missing",
    }
    assert report["next_required_gate"] == "frustum_and_trapezoidal_prism_fit_audit"

    cases = {case["case_id"]: case for case in report["cases"]}
    assert set(cases) == {"paper_single_box", "paper_two_face_merge"}

    single_box = cases["paper_single_box"]
    assert single_box["source_mesh"]["face_arity_policy"] == "triangle_only_fixture"
    assert single_box["source_mesh"]["connected_component_count"] == 1
    assert single_box["source_mesh"]["source_face_remap"] == "identity"
    assert single_box["operator_audit"]["epsilon"] == 1e-6
    assert single_box["operator_audit"]["faces"][0]["q_matrix"]
    assert single_box["operator_audit"]["merged_group"]["eigenvalues"]
    assert abs(single_box["primitive_fit_audit"]["selected"]["volume"] - 1.0) < 3e-6

    primitive_types = {
        row["paper_primitive"] for row in single_box["primitive_fit_audit"]["candidates"]
    }
    assert primitive_types == {
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
    }
    box = [
        row
        for row in single_box["primitive_fit_audit"]["candidates"]
        if row["paper_primitive"] == "oriented_bounding_box"
    ][0]
    assert box["implementation_status"] == "current_surrogate_not_paper_faithful"
    assert box["fit_model"] == "current_cpd_like_surrogate_fit"
    assert box["primitive_parameter_lower_clamp"] == 1e-6
    capped = [
        row
        for row in single_box["primitive_fit_audit"]["candidates"]
        if row["paper_primitive"] == "capped_cylinder"
    ][0]
    assert capped["implementation_status"] == "current_proxy_not_paper_faithful"
    assert capped["fit_model"] == "current_axis_span_radial_proxy_with_hemisphere_caps"
    assert capped["newton_runtime_kind"] == "unmapped_current_proxy"
    assert "frustum" in single_box["primitive_fit_audit"]["missing_paper_primitives"]
    assert "trapezoidal_prism" in single_box["primitive_fit_audit"]["missing_paper_primitives"]

    merge_case = cases["paper_two_face_merge"]
    assert [
        audit["source_faces"] for audit in merge_case["primitive_fit_audits"]
    ] == [[0], [1], [0, 1]]
    assert merge_case["collapse_trace"]["edge_source"] == "topology"
    assert merge_case["collapse_trace"]["accepted"] is True
    assert merge_case["collapse_trace"]["stop_reason"] == "target_count_reached"
    assert merge_case["collapse_trace"]["lookahead_used"] is False
    cost = merge_case["collapse_cost_audit"]
    assert cost["paper_base_cost"] == cost["merged_volume"] - (
        cost["left_volume"] + cost["right_volume"]
    )
    assert cost["weighted_priority_cost"] == cost["merged_weighted_volume"] - (
        cost["left_weighted_volume"] + cost["right_weighted_volume"]
    )
    assert cost["primary_cost_normalized_by_aabb"] is False
    assert cost["intersection_volume_term_included"] is False
    assert cost["paper_weights"]["capped_cylinder"] == 1.05
    assert cost["priority_queue_policy"] == "greedy_single_pop_fixture"
    assert cost["left_fit_audit"]["source_faces"] == [0]
    assert cost["right_fit_audit"]["source_faces"] == [1]
    assert cost["merged_fit_audit"]["source_faces"] == [0, 1]
    assert cost["left_fit_audit"]["candidates"]
    assert cost["right_fit_audit"]["candidates"]
    assert cost["merged_fit_audit"]["candidates"]


def test_cpd_paper_offline_report_is_strict_json_serializable():
    report = build_cpd_paper_offline_report()

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_paper_offline_report" in encoded
