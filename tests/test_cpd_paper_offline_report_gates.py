import pytest

from tests.cpd_paper_offline_shared import *

pytestmark = pytest.mark.paper_offline


def test_cpd_paper_offline_report_failure_labels_point_to_newton_shape_runtime_boundary_gap(
    cpd_paper_report,
):
    report = cpd_paper_report

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS


def test_cpd_paper_offline_report_next_gate_is_newton_shape_runtime_boundary_preflight_contract(
    cpd_paper_report,
):
    report = cpd_paper_report

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE


def test_cpd_paper_offline_report_records_polygon_quad_intake_policy(cpd_paper_report):
    report = cpd_paper_report
    cases = {case["case_id"]: case for case in report["cases"]}

    _assert_intake_case(
        cases["paper_quad_face_intake"],
        arity=4,
        generated_triangles=[(0, 1, 2), (0, 2, 3)],
    )
    _assert_intake_case(
        cases["paper_polygon_face_intake"],
        arity=5,
        generated_triangles=[(0, 1, 2), (0, 2, 3), (0, 3, 4)],
    )


def test_cpd_paper_offline_report_records_fixture_breadth_batch_a(cpd_paper_report):
    report = cpd_paper_report
    cases = {case["case_id"]: case for case in report["cases"]}

    mixed = cases["paper_mixed_face_preprocess_operator"]
    assert mixed["fixture_breadth_batch"] == "paper_fixture_breadth_batch_a"
    assert mixed["source_mesh"]["source_face_arities"] == [3, 4, 5]
    assert mixed["source_mesh"]["duplicate_vertex_preprocessing"] == (
        "exact_coordinate_deduplication_for_fixture"
    )
    assert mixed["preprocessing_audit"]["duplicate_cluster_count"] == 1
    assert mixed["preprocessing_audit"]["degenerate_face_dropped_count"] == 0
    assert mixed["mesh_intake_policy_audit"]["source_face_arities"] == [3, 4, 5]
    assert mixed["mesh_intake_policy_audit"]["triangulated_face_count"] == 6
    assert mixed["operator_audit"]["face_scope"] == "triangle_subfaces_from_source_face"
    assert len(mixed["operator_audit"]["source_face_operator_aggregates"]) == 3
    for aggregate in mixed["operator_audit"]["source_face_operator_aggregates"]:
        assert aggregate["q_matrix"]
        assert len(aggregate["eigenvalues"]) == 3
        assert aggregate["eigenvector_matrix_layout"] == "columns_are_eigenvectors"
        assert isinstance(aggregate["degeneracy_labels"], list)

    degenerate = cases["paper_degenerate_preprocess_face_drop"]
    assert degenerate["fixture_breadth_batch"] == "paper_fixture_breadth_batch_a"
    degenerate_audit = degenerate["preprocessing_audit"]
    assert degenerate_audit["degenerate_face_dropped_count"] == 1
    assert degenerate_audit["dropped_source_face_ids"] == [0]
    assert degenerate_audit["retained_source_face_ids"] == [1]
    assert degenerate_audit["preprocessing_source_face_remap"][0]["drop_reason"] == (
        "degenerate_after_deduplication"
    )
    assert degenerate_audit["executable_deduplicated_faces"] == [[2, 3, 4]]
    assert degenerate["source_mesh"]["face_count"] == 1
    assert degenerate["operator_audit"]["preprocessing_degeneracy_labels"] == [
        "dropped_degenerate_faces_after_preprocessing"
    ]
    assert degenerate["operator_audit"]["faces"][0]["source_face_id"] == 1
    assert degenerate["operator_audit"]["merged_group"]["source_faces"] == [1]
    assert degenerate["primitive_fit_audit"]["source_faces"] == [1]
    assert degenerate["primitive_fit_audit"]["source_face_ids"] == [1]
    assert degenerate["primitive_fit_audit"]["generated_triangle_face_ids"] == [0]

    concave = cases["paper_concave_polygon_rejected"]
    assert concave["fixture_breadth_batch"] == "paper_fixture_breadth_batch_a"
    assert concave["case_status"] == "unsupported_fixture_policy"
    intake = concave["mesh_intake_policy_audit"]
    assert intake["failure_label"] == "source_face_intake_unsupported_concave_polygon"
    assert intake["source_face_arities"] == [5]
    assert intake["generated_triangle_face_ids"] == []
    assert intake["triangulated_face_count"] == 0
    assert intake["top_level_failure_label"] is False
    assert "primitive_fit_audits" not in concave
    assert concave["package_generation_triggered"] is False
    assert concave["newton_runtime_triggered"] is False
    assert concave["real_usd_triggered"] is False
    assert concave["benchmark_triggered"] is False


def test_cpd_paper_offline_report_records_fixture_breadth_batch_b(cpd_paper_report):
    report = cpd_paper_report
    cases = {case["case_id"]: case for case in report["cases"]}

    expected_case_ids = {
        "paper_rotated_box_fit",
        "paper_offset_sphere_fit",
        "paper_off_axis_capsule_fit",
        "paper_flat_capped_cylinder_axis_fit",
        "paper_tapered_frustum_fit",
        "paper_asymmetric_trapezoid_fit",
    }
    assert expected_case_ids.issubset(cases)
    for case_id in expected_case_ids:
        case = cases[case_id]
        assert case["fixture_breadth_batch"] == "paper_fixture_breadth_batch_b"
        assert case["package_generation_triggered"] is False
        assert case["newton_runtime_triggered"] is False
        assert case["real_usd_triggered"] is False
        assert case["benchmark_triggered"] is False
        assert case["primitive_fit_audit"]["missing_paper_primitives"] == []

    rotated_box = cases["paper_rotated_box_fit"]
    obb = _candidate_by_paper_primitive(
        rotated_box["primitive_fit_audit"],
        "oriented_bounding_box",
    )
    assert _candidate_has_common_fit_fields(obb)
    assert obb["contains_assigned_points"] is True
    assert obb["dimensions"]["volume_formula"] == "8*hx*hy*hz"
    assert obb["dimensions"]["axis_order_policy"] == "descending_abs_q_eigenvalue"
    assert obb["dimensions"]["lower_bounds"]
    assert obb["dimensions"]["upper_bounds"]
    assert obb["dimensions"]["paper_center_local"]
    assert obb["dimensions"]["paper_center_world"] == obb["center"]
    assert obb["dimensions"]["half_extents"]
    assert obb["newton_runtime_kind"] == "box"
    assert _axes_are_orthonormal(obb["axes"])
    assert not _axes_are_world_aligned(obb["axes"])

    offset_sphere = cases["paper_offset_sphere_fit"]
    sphere = _candidate_by_paper_primitive(
        offset_sphere["primitive_fit_audit"],
        "sphere",
    )
    assert _candidate_has_common_fit_fields(sphere)
    assert sphere["contains_assigned_points"] is True
    assert sphere["dimensions"]["center_source"] == "paper_obb_center"
    assert sphere["dimensions"]["radius"] >= 1e-3
    assert sphere["dimensions"]["unclamped_radius"] > 0.0
    assert sphere["dimensions"]["volume_formula"] == "4/3*pi*r^3"
    assert sphere["dimensions"]["fixture_center_relation"] == "differs_from_point_centroid"
    assert sphere["dimensions"]["center_differs_from_point_centroid"] is True
    assert sphere["dimensions"]["center_centroid_distance"] > 1e-3
    assert sphere["newton_runtime_kind"] == "sphere"

    off_axis_capsule = cases["paper_off_axis_capsule_fit"]
    capsule = _candidate_by_paper_primitive(
        off_axis_capsule["primitive_fit_audit"],
        "capsule",
    )
    assert _candidate_has_common_fit_fields(capsule)
    assert capsule["contains_assigned_points"] is True
    assert capsule["dimensions"]["axis_selection_policy"] == "min_volume_capsule_axis"
    assert len(capsule["dimensions"]["paper_capsule_axis_candidates"]) == 3
    assert capsule["dimensions"]["height"] > 0.0
    assert capsule["dimensions"]["radius"] > 0.0
    selected_capsule_axis = capsule["axes"][capsule["dimensions"]["selected_axis_index"]]
    assert not _axis_is_world_basis(selected_capsule_axis)

    flat_cylinder = cases["paper_flat_capped_cylinder_axis_fit"]
    capped = _candidate_by_paper_primitive(
        flat_cylinder["primitive_fit_audit"],
        "capped_cylinder",
    )
    assert _candidate_has_common_fit_fields(capped)
    assert capped["contains_assigned_points"] is True
    assert capped["newton_runtime_kind"] == "offline_only_unmapped"
    assert capped["dimensions"]["cap_model"] == "flat_caps"
    assert capped["dimensions"]["volume_formula"] == "pi*r^2*h"
    assert len(capped["dimensions"]["flat_cylinder_axis_candidates"]) == 3
    assert capped["dimensions"]["radius"] > 0.0
    assert capped["dimensions"]["height"] > 0.0
    selected_capped_axis = capped["axes"][capped["dimensions"]["selected_axis_index"]]
    assert not _axis_is_world_basis(selected_capped_axis)

    tapered = cases["paper_tapered_frustum_fit"]
    frustum = _candidate_by_paper_primitive(
        tapered["primitive_fit_audit"],
        "frustum",
    )
    assert _candidate_has_common_fit_fields(frustum)
    assert frustum["contains_assigned_points"] is True
    assert frustum["newton_runtime_kind"] == "offline_only_unmapped"
    assert abs(frustum["dimensions"]["top_radius"] - frustum["dimensions"]["bottom_radius"]) > 0.05
    assert frustum["dimensions"]["height"] > 0.0
    assert frustum["dimensions"]["top_center"]
    assert frustum["dimensions"]["bottom_center"]
    assert frustum["dimensions"]["volume_formula"] == "pi*h/3*(rt^2 + rt*rb + rb^2)"

    trapezoid = cases["paper_asymmetric_trapezoid_fit"]
    prism = _candidate_by_paper_primitive(
        trapezoid["primitive_fit_audit"],
        "trapezoidal_prism",
    )
    assert _candidate_has_common_fit_fields(prism)
    assert prism["contains_assigned_points"] is True
    assert prism["newton_runtime_kind"] == "offline_only_unmapped"
    assert prism["dimensions"]["axis_order_attempt_count"] == 6
    assert len(prism["dimensions"]["axis_order_attempts"]) == 6
    assert prism["dimensions"]["axis_order"]
    assert prism["dimensions"]["h_x"] > 0.0
    assert prism["dimensions"]["h_y"] > 0.0
    assert prism["dimensions"]["h_zt"] > 0.0
    assert prism["dimensions"]["h_zb"] > 0.0
    assert prism["dimensions"]["volume_formula"] == "4*h_x*h_y*(h_zt + h_zb)"


def test_cpd_paper_offline_report_records_fixture_breadth_batch_c(cpd_paper_report):
    report = cpd_paper_report
    report_again = _fresh_independent_cpd_paper_offline_report_for_determinism_check()
    assert report_again is not report
    cases = {case["case_id"]: case for case in report["cases"]}
    cases_again = {case["case_id"]: case for case in report_again["cases"]}

    expected_case_ids = {
        "paper_branching_cost_order",
        "paper_equal_cost_queue_tie",
        "paper_nonzero_threshold_block",
    }
    assert expected_case_ids.issubset(cases)
    for case_id in expected_case_ids:
        case = cases[case_id]
        assert case["fixture_breadth_batch"] == "paper_fixture_breadth_batch_c"
        assert case["package_generation_triggered"] is False
        assert case["newton_runtime_triggered"] is False
        assert case["real_usd_triggered"] is False
        assert case["benchmark_triggered"] is False
        assert case["collapse_trace"]["package_generation_triggered"] is False
        assert case["collapse_trace"]["newton_runtime_triggered"] is False
        assert case["collapse_trace"]["real_usd_triggered"] is False
        assert case["collapse_trace"]["benchmark_triggered"] is False
        for candidate in case["collapse_trace"]["initial_candidates"]:
            assert isfinite(candidate["paper_base_cost"])
            assert isfinite(candidate["weighted_priority_cost"])
            assert isfinite(candidate["queue_key"][0])
            assert isfinite(candidate["queue_key"][1])
        for event in case["collapse_trace"]["events"]:
            assert isfinite(event["paper_base_cost"])
            assert isfinite(event["weighted_priority_cost"])
            assert isfinite(event["queue_key"][0])
            assert isfinite(event["queue_key"][1])

    branching = cases["paper_branching_cost_order"]["collapse_trace"]
    assert branching["trace_scope"] == "topology_priority_queue_trace_fixture"
    assert branching["initial_edge_count"] == 2
    assert branching["target_primitive_count"] == 3
    assert branching["threshold_policy"] == "disabled"
    assert len(branching["initial_candidates"]) == 2
    assert all(
        candidate["edge_source"] == "topology" for candidate in branching["initial_candidates"]
    )
    assert all("paper_base_cost" in candidate for candidate in branching["initial_candidates"])
    assert all(
        "weighted_priority_cost" in candidate for candidate in branching["initial_candidates"]
    )
    first_accepted = [event for event in branching["events"] if event["accepted"]][0]
    assert first_accepted["weighted_priority_cost"] == min(
        candidate["weighted_priority_cost"] for candidate in branching["initial_candidates"]
    )
    assert first_accepted["queue_key"] == min(
        candidate["queue_key"] for candidate in branching["initial_candidates"]
    )
    min_base_candidate = min(
        branching["initial_candidates"],
        key=lambda candidate: candidate["paper_base_cost"],
    )
    min_weighted_candidate = min(
        branching["initial_candidates"],
        key=lambda candidate: candidate["weighted_priority_cost"],
    )
    assert (
        min_base_candidate["source_faces_merged"] != min_weighted_candidate["source_faces_merged"]
    )
    assert first_accepted["source_faces_merged"] == min_weighted_candidate["source_faces_merged"]
    assert first_accepted["source_faces_merged"] != min_base_candidate["source_faces_merged"]
    assert first_accepted["queue_key"][0] == first_accepted["weighted_priority_cost"]
    assert first_accepted["queue_key"][1] == first_accepted["paper_base_cost"]
    assert first_accepted["updated_neighbor_insertion_count"] == 1
    assert branching["accepted_merge_count"] == 1
    assert branching["stop_reason"] == "target_count_reached"

    tie = cases["paper_equal_cost_queue_tie"]["collapse_trace"]
    tie_again = cases_again["paper_equal_cost_queue_tie"]["collapse_trace"]
    assert tie["trace_scope"] == "topology_priority_queue_trace_fixture"
    assert tie["initial_edge_count"] == 2
    assert tie["target_primitive_count"] == 1
    first_candidate, second_candidate = tie["initial_candidates"]
    assert first_candidate["weighted_priority_cost"] == second_candidate["weighted_priority_cost"]
    assert first_candidate["paper_base_cost"] == second_candidate["paper_base_cost"]
    assert first_candidate["queue_key"][2:] < second_candidate["queue_key"][2:]
    assert first_candidate["left_primitive"] == second_candidate["left_primitive"]
    assert first_candidate["right_primitive"] == second_candidate["right_primitive"]
    assert first_candidate["merged_primitive"] == second_candidate["merged_primitive"]
    assert tie["events"][0]["event_kind"] == "accepted_merge"
    assert tie["events"][0]["source_faces_left"] == [0]
    assert tie["events"][0]["source_faces_right"] == [1]
    assert tie["events"][1]["event_kind"] == "eager_stale_prune"
    assert tie["events"][1]["stale_entry"] is True
    assert tie["events"][1]["source_faces_left"] == [0]
    assert tie["events"][1]["source_faces_right"] == [2]
    assert tie["events"][2]["event_kind"] == "accepted_merge"
    assert tie["events"][2]["source_faces_left"] == [0, 1]
    assert tie["events"][2]["source_faces_right"] == [2]
    assert len(tie["events"]) == 3
    assert tie["accepted_merge_count"] == 2
    assert tie["stale_entry_skipped_count"] == 1
    assert tie["final_active_groups"] == [[0, 1, 2]]
    assert _event_signature(tie) == [
        ("accepted_merge", [0], [1], True, False, False),
        ("eager_stale_prune", [0], [2], False, True, False),
        ("accepted_merge", [0, 1], [2], True, False, False),
    ]
    assert _event_signature(tie) == _event_signature(tie_again)

    blocked = cases["paper_nonzero_threshold_block"]["collapse_trace"]
    assert blocked["trace_scope"] == "component_pair_priority_queue_trace_fixture"
    assert blocked["component_pair_edge_insertion_triggered"] is True
    assert blocked["topology_queue_exhausted_before_component_pair_insertion"] is True
    assert blocked["threshold_policy"] == "component_pair_paper_base_cost_lte_threshold"
    assert blocked["excess_volume_threshold"] == 1e-6
    assert blocked["accepted_merge_count"] == 0
    assert blocked["blocked_merge_count"] == 1
    assert blocked["stop_reason"] == "all_remaining_edges_blocked_by_threshold"
    blocked_events = [
        event for event in blocked["events"] if event["event_kind"] == "blocked_by_threshold"
    ]
    assert len(blocked_events) == 1
    blocked_event = blocked_events[0]
    assert blocked_event["edge_source"] == "component_pair"
    assert blocked_event["threshold_metric"] == "paper_base_cost"
    assert blocked_event["threshold_value"] == 1e-6
    assert blocked_event["paper_base_cost"] > blocked_event["threshold_value"] > 0.0
    assert blocked_event["blocked_reason"] == "component_pair_threshold_exceeded"


def test_cpd_paper_offline_report_records_fixture_breadth_batch_d(cpd_paper_report):
    report = cpd_paper_report
    cases = {case["case_id"]: case for case in report["cases"]}

    expected_case_ids = {
        "paper_component_pair_multi_candidate_order",
        "paper_component_pair_cap_skipped",
    }
    assert expected_case_ids.issubset(cases)
    for case_id in expected_case_ids:
        case = cases[case_id]
        assert case["fixture_breadth_batch"] == "paper_fixture_breadth_batch_d"
        assert case["package_generation_triggered"] is False
        assert case["newton_runtime_triggered"] is False
        assert case["real_usd_triggered"] is False
        assert case["benchmark_triggered"] is False
        trace = case["collapse_trace"]
        assert trace["trace_scope"] == "component_pair_priority_queue_trace_fixture"
        assert trace["component_pair_edge_insertion_triggered"] is True
        assert trace["topology_queue_exhausted_before_component_pair_insertion"] is True
        assert trace["initial_edge_count"] == 0
        assert trace["initial_candidates"] == []
        assert trace["package_generation_triggered"] is False
        assert trace["newton_runtime_triggered"] is False
        assert trace["real_usd_triggered"] is False
        assert trace["benchmark_triggered"] is False

    multi = cases["paper_component_pair_multi_candidate_order"]["collapse_trace"]
    assert multi["target_primitive_count"] == 2
    assert multi["threshold_policy"] == "disabled"
    assert multi["component_pair_candidate_cap"] == "all_pairs_for_fixture"
    assert multi["component_pair_available_pair_count"] == 3
    assert multi["component_pair_candidate_count"] == 3
    assert multi["skipped_component_pair_count"] == 0
    assert multi["skipped_component_pair_keys"] == []
    assert len(multi["component_pair_candidates"]) == 3
    assert all(
        candidate["edge_source"] == "component_pair"
        for candidate in multi["component_pair_candidates"]
    )
    selected = [event for event in multi["events"] if event["accepted"]][0]
    min_candidate = min(
        multi["component_pair_candidates"],
        key=lambda candidate: candidate["queue_key"],
    )
    assert selected["queue_key"] == min_candidate["queue_key"]
    assert selected["source_faces_merged"] == min_candidate["source_faces_merged"]
    assert multi["accepted_merge_count"] == 1
    assert multi["blocked_merge_count"] == 0
    assert multi["component_pair_attempted_pair_count"] == 1
    assert multi["stop_reason"] == "target_count_reached"
    assert len(multi["final_active_groups"]) == 2

    capped = cases["paper_component_pair_cap_skipped"]["collapse_trace"]
    assert capped["target_primitive_count"] == 3
    assert capped["threshold_policy"] == "disabled"
    assert capped["component_pair_candidate_cap"] == 2
    assert capped["component_pair_available_pair_count"] == 6
    assert capped["component_pair_candidate_count"] == 2
    assert capped["skipped_component_pair_count"] == 4
    assert len(capped["skipped_component_pair_keys"]) == 4
    assert len(capped["component_pair_candidates"]) == 2
    assert all(
        candidate["edge_source"] == "component_pair"
        for candidate in capped["component_pair_candidates"]
    )
    assert all(
        skipped["skip_reason"] == "component_pair_candidate_cap_reached"
        for skipped in capped["skipped_component_pair_keys"]
    )
    assert capped["component_pair_attempted_pair_count"] == 1
    assert capped["accepted_merge_count"] == 1
    assert capped["blocked_merge_count"] == 0
    assert capped["stop_reason"] == "target_count_reached"
    assert len(capped["final_active_groups"]) == 3


def test_cpd_paper_offline_report_records_fixture_breadth_batch_e(cpd_paper_report):
    report = cpd_paper_report
    cases = {case["case_id"]: case for case in report["cases"]}

    expected_case_ids = {
        "paper_rotated_nested_primitive",
        "paper_cross_type_enclosure_boundary",
    }
    assert expected_case_ids.issubset(cases)
    for case_id in expected_case_ids:
        case = cases[case_id]
        assert case["fixture_breadth_batch"] == "paper_fixture_breadth_batch_e"
        assert case["package_generation_triggered"] is False
        assert case["newton_runtime_triggered"] is False
        assert case["real_usd_triggered"] is False
        assert case["benchmark_triggered"] is False
        postprocess = case["postprocess_audit"]
        assert postprocess["package_generation_triggered"] is False
        assert postprocess["newton_runtime_triggered"] is False
        assert postprocess["real_usd_triggered"] is False
        assert postprocess["benchmark_triggered"] is False

    rotated = cases["paper_rotated_nested_primitive"]["postprocess_audit"]
    assert rotated["audit_scope"] == "enclosed_primitive_culling_fixture"
    assert rotated["fixture_variant"] == "rotated_nested_obb"
    assert rotated["containment_test_type"] == "obb_corners_inside_obb"
    assert rotated["axis_policy"] == "shared_rotated_axes"
    assert rotated["input_primitive_count"] == 2
    assert rotated["output_primitive_count"] == 1
    assert rotated["culled_primitive_ids"] == [1]
    assert rotated["kept_primitive_ids"] == [0]
    assert rotated["rotation_degrees_about_z"] == 30.0
    assert rotated["rotated_axes_non_identity"] is True
    assert rotated["input_primitives"][0]["axes"] == rotated["input_primitives"][1]["axes"]
    assert rotated["input_primitives"][0]["axes"] != [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ]
    assert rotated["cull_records"] == [
        {
            "culled_primitive_id": 1,
            "enclosing_primitive_id": 0,
            "cull_reason": "primitive_enclosed_by_larger_primitive",
            "containment_passed": True,
            "tested_corner_count": 8,
        }
    ]

    cross_type = cases["paper_cross_type_enclosure_boundary"]["postprocess_audit"]
    assert cross_type["audit_scope"] == "enclosed_primitive_cross_type_boundary_fixture"
    assert cross_type["fixture_variant"] == "cross_type_unsupported_boundary"
    assert cross_type["containment_test_type"] == "cross_type_containment_unsupported"
    assert cross_type["cross_type_culling_supported"] is False
    assert cross_type["unsupported_containment_label"] == (
        "cross_type_enclosure_boundary_not_supported"
    )
    assert cross_type["top_level_failure_label"] is False
    assert cross_type["input_primitive_count"] == 2
    assert cross_type["output_primitive_count"] == 2
    assert cross_type["culled_primitive_ids"] == []
    assert cross_type["kept_primitive_ids"] == [0, 1]
    assert cross_type["cull_records"] == []
    assert cross_type["unsupported_records"] == [
        {
            "candidate_primitive_id": 1,
            "enclosing_primitive_id": 0,
            "candidate_kind": "sphere",
            "enclosing_kind": "oriented_bounding_box",
            "unsupported_reason": "cross_type_containment_not_implemented_for_fixture",
        }
    ]


def test_cpd_paper_offline_report_records_fixture_breadth_completion_review(cpd_paper_report):
    report = cpd_paper_report

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert (
        "paper_fixture_breadth_completion_review"
        in report["paper_faithfulness"]["implemented_fixture_scope"]
    )

    review = report["paper_fixture_breadth_completion_review"]
    assert review["review_scope"] == "synthetic_fixture_breadth_batches_a_to_e"
    assert review["closed_gate"] == "paper_fixture_breadth_expansion"
    assert review["decision"] == "remain_partial"
    assert review["decision_reason"] == "fixture_breadth_complete_but_generalization_missing"
    assert review["fixture_breadth_plan_complete"] is True
    assert review["paper_faithful_offline_allowed"] is False
    assert review["next_required_gate"] == "paper_faithful_offline_generalization_plan"
    assert review["package_generation_triggered"] is False
    assert review["newton_runtime_triggered"] is False
    assert review["real_usd_triggered"] is False
    assert review["benchmark_triggered"] is False

    expected_batches = [
        {
            "batch_id": "paper_fixture_breadth_batch_a",
            "purpose": "source_preprocess_intake_operator_breadth",
            "case_ids": [
                "paper_mixed_face_preprocess_operator",
                "paper_degenerate_preprocess_face_drop",
                "paper_concave_polygon_rejected",
            ],
            "primary_criteria": [
                "source_mesh_and_preprocessing_policy",
                "source_face_intake_policy",
                "operator_q_audit",
            ],
        },
        {
            "batch_id": "paper_fixture_breadth_batch_b",
            "purpose": "primitive_fit_breadth",
            "case_ids": [
                "paper_rotated_box_fit",
                "paper_offset_sphere_fit",
                "paper_off_axis_capsule_fit",
                "paper_flat_capped_cylinder_axis_fit",
                "paper_tapered_frustum_fit",
                "paper_asymmetric_trapezoid_fit",
            ],
            "primary_criteria": [
                "primitive_vocabulary_and_fit",
            ],
        },
        {
            "batch_id": "paper_fixture_breadth_batch_c",
            "purpose": "cost_search_stop_breadth",
            "case_ids": [
                "paper_branching_cost_order",
                "paper_equal_cost_queue_tie",
                "paper_nonzero_threshold_block",
            ],
            "primary_criteria": [
                "paper_collapse_cost_and_weighting",
                "greedy_priority_queue_trace",
                "target_count_and_threshold_stop",
            ],
        },
        {
            "batch_id": "paper_fixture_breadth_batch_d",
            "purpose": "component_pair_breadth",
            "case_ids": [
                "paper_component_pair_multi_candidate_order",
                "paper_component_pair_cap_skipped",
            ],
            "primary_criteria": [
                "component_pair_edge_handling",
                "target_count_and_threshold_stop",
            ],
        },
        {
            "batch_id": "paper_fixture_breadth_batch_e",
            "purpose": "postprocess_breadth",
            "case_ids": [
                "paper_rotated_nested_primitive",
                "paper_cross_type_enclosure_boundary",
            ],
            "primary_criteria": [
                "enclosed_primitive_postprocess",
            ],
        },
    ]
    assert review["completed_batches"] == expected_batches
    cases_by_batch = {}
    for case in report["cases"]:
        batch = case.get("fixture_breadth_batch")
        if batch is not None:
            cases_by_batch.setdefault(batch, []).append(case["case_id"])
    assert cases_by_batch == {batch["batch_id"]: batch["case_ids"] for batch in expected_batches}
    assert review["remaining_blocking_criteria_ids"] == EXPECTED_SCOPE_AUDIT_BLOCKERS
    assert [row["criterion_id"] for row in review["criteria_after_completion"]] == (
        EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert all(
        row["status_after_completion"] == "partial_fixture_scope"
        for row in review["criteria_after_completion"]
    )
    assert all(
        row["remaining_gap"] == "paper_faithful_offline_generalization"
        for row in review["criteria_after_completion"]
    )


def test_cpd_paper_offline_report_records_generalization_plan_gate(cpd_paper_report):
    report = cpd_paper_report

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert (
        "paper_faithful_offline_generalization_plan"
        not in report["paper_faithfulness"]["implemented_fixture_scope"]
    )
    assert (
        "paper_faithful_offline_generalization_plan"
        in report["paper_faithfulness"]["implemented_planning_scope"]
    )

    plan = report["paper_faithful_offline_generalization_plan"]
    assert plan["plan_scope"] == "offline_algorithm_generalization_beyond_named_toy_fixtures"
    assert plan["closed_gate"] == "paper_faithful_offline_generalization_plan"
    assert plan["decision"] == "remain_partial"
    assert (
        plan["decision_reason"]
        == "changed_decomposition_output_contract_complete_package_adapter_contract_missing"
    )
    assert plan["generalization_plan_complete"] is True
    assert plan["paper_faithful_offline_allowed"] is False
    assert plan["next_required_gate"] == EXPECTED_PACKAGE_ADAPTER_CONTRACT
    assert plan["package_generation_triggered"] is False
    assert plan["newton_runtime_triggered"] is False
    assert plan["real_usd_triggered"] is False
    assert plan["benchmark_triggered"] is False

    expected_batches = [
        {
            "batch_id": "paper_generalization_batch_a_source_policy",
            "purpose": "generalize_source_mesh_preprocess_intake_operator_policy",
            "primary_criteria": [
                "source_mesh_and_preprocessing_policy",
                "source_face_intake_policy",
                "operator_q_audit",
            ],
            "implementation_boundary": "offline_report_only_no_package_or_newton",
            "required_output": "source_policy_generalization_report",
        },
        {
            "batch_id": "paper_generalization_batch_b_primitive_fit_engine",
            "purpose": "generalize_paper_primitive_fit_engine_beyond_named_cases",
            "primary_criteria": [
                "primitive_vocabulary_and_fit",
            ],
            "implementation_boundary": "offline_report_only_no_package_or_newton",
            "required_output": "primitive_fit_engine_generalization_report",
        },
        {
            "batch_id": "paper_generalization_batch_c_search_engine",
            "purpose": "generalize_cost_queue_threshold_and_component_pair_search",
            "primary_criteria": [
                "paper_collapse_cost_and_weighting",
                "greedy_priority_queue_trace",
                "target_count_and_threshold_stop",
                "component_pair_edge_handling",
            ],
            "implementation_boundary": "offline_report_only_no_package_or_newton",
            "required_output": "search_engine_generalization_report",
        },
        {
            "batch_id": "paper_generalization_batch_d_postprocess_policy",
            "purpose": "generalize_enclosed_primitive_postprocess_policy",
            "primary_criteria": [
                "enclosed_primitive_postprocess",
            ],
            "implementation_boundary": "offline_report_only_no_package_or_newton",
            "required_output": "postprocess_policy_generalization_report",
        },
        {
            "batch_id": "paper_generalization_batch_e_package_boundary_readiness",
            "purpose": "review_offline_package_boundary_readiness_after_changed_decomposition",
            "primary_criteria": [
                "package_generation_boundary",
                "newton_runtime_boundary",
                "real_usd_boundary",
                "benchmark_evaluation_boundary",
            ],
            "implementation_boundary": "planning_only_no_package_or_newton",
            "required_output": "package_boundary_readiness_review",
        },
    ]
    assert plan["planned_batches"] == expected_batches
    assert plan["first_unresolved_gate"] == EXPECTED_PACKAGE_ADAPTER_CONTRACT
    assert plan["remaining_generalization_gates"] == []
    assert plan["blocked_runtime_gates"] == [
        "package_generation_boundary",
        "newton_runtime_boundary",
        "real_usd_boundary",
        "benchmark_evaluation_boundary",
    ]


def test_cpd_paper_offline_report_records_source_policy_generalization_gate(cpd_paper_report):
    report = cpd_paper_report

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert (
        EXPECTED_CLOSED_SOURCE_POLICY_GATE
        in report["paper_faithfulness"]["implemented_generalization_scope"]
    )
    assert (
        EXPECTED_CLOSED_PRIMITIVE_FIT_GATE
        in report["paper_faithfulness"]["implemented_generalization_scope"]
    )
    assert (
        EXPECTED_CLOSED_SEARCH_ENGINE_GATE
        in report["paper_faithfulness"]["implemented_generalization_scope"]
    )
    assert report["paper_faithful_offline_supported"] is False
    assert report["status"] == "partial"

    payload = report["paper_generalization_batch_a_source_policy"]
    assert payload["gate_id"] == "paper_generalization_batch_a_source_policy"
    assert payload["gate_status"] == "implemented_offline_report_only_partial"
    assert payload["closed_gate"] == "paper_generalization_batch_a_source_policy"
    assert payload["next_required_gate"] == "paper_generalization_batch_b_primitive_fit_engine"
    assert payload["decision"] == "remain_partial"
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["source_scope"] == "synthetic_in_memory_source_mesh_policy_matrix"
    assert payload["implementation_boundary"] == "offline_report_only_no_package_or_newton"
    assert payload["source_mesh_contract"] == {
        "accepted_source_representation": "vertices_plus_variable_arity_source_faces",
        "source_face_id_policy": "preserve_source_face_ids_distinct_from_generated_triangle_ids",
        "general_mesh_cleanup_supported": False,
    }
    assert payload["preprocessing_policy"]["deduplication_policy"] == (
        "exact_coordinate_first_occurrence_only"
    )
    assert payload["preprocessing_policy"]["distance_tolerance"] == 0.0
    assert payload["preprocessing_policy"]["degenerate_face_policy"] == (
        "drop_after_exact_deduplication_from_executable_rows"
    )
    assert payload["source_face_intake_policy"]["accepted_preconditions"] == [
        "planar",
        "convex",
        "non_degenerate",
        "consistently_wound",
    ]
    assert payload["source_face_intake_policy"]["triangulation_policy"] == ("fan_from_first_vertex")
    assert payload["source_face_intake_policy"]["unsupported_policy"] == (
        "reject_concave_polygon_without_top_level_failure_label"
    )
    assert payload["operator_policy"]["triangle_operator_policy"] == (
        "compute_q_on_executable_triangles"
    )
    assert payload["operator_policy"]["source_face_aggregate_policy"] == (
        "sum_generated_triangle_q_rows_to_source_face"
    )
    assert [row["policy_row_id"] for row in payload["policy_matrix"]] == [
        "accepted_mixed_triangle_quad_polygon_exact_dedup",
        "accepted_degenerate_after_exact_dedup_drop",
        "rejected_concave_polygon",
    ]
    assert payload["coverage_summary"] == {
        "evidence_case_count": 3,
        "accepted_policy_row_count": 2,
        "unsupported_policy_row_count": 1,
        "closed_gate_count": 1,
        "remaining_generalization_gate_count": 4,
    }
    assert payload["remaining_gaps"] == EXPECTED_SOURCE_POLICY_REMAINING_GAPS
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False


def test_cpd_paper_offline_report_records_primitive_fit_engine_generalization_gate(
    cpd_paper_report,
):
    report = cpd_paper_report

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert (
        report["paper_faithfulness"]["implemented_generalization_scope"]
        == EXPECTED_CLOSED_GENERALIZATION_GATES
    )
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert report["paper_faithful_offline_supported"] is False
    assert report["status"] == "partial"

    payload = report["paper_generalization_batch_b_primitive_fit_engine"]
    assert payload["gate_id"] == EXPECTED_CLOSED_PRIMITIVE_FIT_GATE
    assert payload["gate_status"] == "implemented_offline_report_only_partial"
    assert payload["closed_gate"] == EXPECTED_CLOSED_PRIMITIVE_FIT_GATE
    assert payload["next_required_gate"] == "paper_generalization_batch_c_search_engine"
    assert payload["decision"] == "remain_partial"
    assert (
        payload["decision_reason"]
        == "primitive_fit_engine_generalization_complete_search_engine_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["source_scope"] == "deterministic_in_memory_parametric_primitive_fit_probes"
    assert payload["implementation_boundary"] == "offline_report_only_no_package_or_newton"
    assert payload["engine_contract"] == {
        "input_contract": "TriangleMesh_plus_face_group",
        "candidate_set": [
            "oriented_bounding_box",
            "sphere",
            "capsule",
            "capped_cylinder",
            "frustum",
            "trapezoidal_prism",
        ],
        "candidate_evaluation_policy": "evaluate_all_candidates_no_runtime_mapping",
        "selection_rule": "min_paper_weighted_volume_then_candidate_order",
        "containment_scope": "assigned_vertices_only_not_surface_or_collision_quality",
        "axis_policy": "paper_q_eigenbasis_with_candidate_axis_enumeration",
        "offline_only_unmapped_primitives": [
            "capped_cylinder",
            "frustum",
            "trapezoidal_prism",
        ],
    }
    assert payload["coverage_summary"] == {
        "primitive_count": 6,
        "probe_family_count": 6,
        "generated_probe_count": 6,
        "candidate_row_count": 36,
        "closed_gate_count": 2,
        "remaining_generalization_gate_count": 3,
    }
    assert payload["remaining_gaps"] == EXPECTED_PRIMITIVE_FIT_REMAINING_GAPS
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
    assert "timing" not in payload
    assert "surface_distance" not in payload
    assert "collision_quality" not in payload
    assert "benchmark" not in payload

    expected_target_primitives = [
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
    rows = payload["primitive_family_matrix"]
    assert [row["target_paper_primitive"] for row in rows] == expected_target_primitives
    assert {row["probe_id"] for row in rows} == {
        "paper_fit_engine_rotated_obb_probe",
        "paper_fit_engine_offset_sphere_probe",
        "paper_fit_engine_off_axis_capsule_probe",
        "paper_fit_engine_flat_capped_cylinder_probe",
        "paper_fit_engine_tapered_frustum_probe",
        "paper_fit_engine_asymmetric_trapezoid_probe",
    }
    for row in rows:
        assert row["candidate_row_count"] == 6
        assert row["candidate_order"] == expected_target_primitives
        assert row["missing_paper_primitives"] == []
        assert row["target_candidate"]["paper_primitive"] == row["target_paper_primitive"]
        assert row["selected_candidate"]["paper_primitive"] in expected_target_primitives
        assert "target_candidate_selected" in row
        assert row["contains_assigned_points"] is True
        assert row["finite_numeric_fields"] is True
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False
        assert _axes_are_orthonormal(row["target_candidate"]["axes"])

    runtime_by_primitive = {
        row["target_paper_primitive"]: row["newton_runtime_kind"] for row in rows
    }
    assert runtime_by_primitive["oriented_bounding_box"] == "box"
    assert runtime_by_primitive["sphere"] == "sphere"
    assert runtime_by_primitive["capsule"] == "capsule"
    assert runtime_by_primitive["capped_cylinder"] == "offline_only_unmapped"
    assert runtime_by_primitive["frustum"] == "offline_only_unmapped"
    assert runtime_by_primitive["trapezoidal_prism"] == "offline_only_unmapped"


def test_cpd_paper_offline_report_records_search_engine_generalization_gate(cpd_paper_report):
    report = cpd_paper_report

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert (
        report["paper_faithfulness"]["implemented_generalization_scope"]
        == EXPECTED_CLOSED_GENERALIZATION_GATES
    )
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert report["paper_faithful_offline_supported"] is False
    assert report["status"] == "partial"

    payload = report["paper_generalization_batch_c_search_engine"]
    assert payload["gate_id"] == EXPECTED_CLOSED_SEARCH_ENGINE_GATE
    assert payload["gate_status"] == "implemented_offline_report_only_partial"
    assert payload["closed_gate"] == EXPECTED_CLOSED_SEARCH_ENGINE_GATE
    assert payload["next_required_gate"] == "paper_generalization_batch_d_postprocess_policy"
    assert payload["decision"] == "remain_partial"
    assert (
        payload["decision_reason"]
        == "search_engine_generalization_complete_postprocess_policy_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["source_scope"] == "deterministic_in_memory_search_trace_probes"
    assert payload["implementation_boundary"] == "offline_report_only_no_package_or_newton"
    assert payload["search_engine_contract"] == {
        "input_contract": ("TriangleMesh_plus_initial_face_groups_target_count_and_search_policy"),
        "primary_policy": "paper_greedy_min_weighted_priority_cost_no_lookahead",
        "cost_fields": ["paper_base_cost", "weighted_priority_cost"],
        "queue_key_fields": [
            "weighted_priority_cost",
            "paper_base_cost",
            "source_faces_left",
            "source_faces_right",
            "insertion_order",
        ],
        "candidate_sources": ["topology", "component_pair"],
        "component_pair_insertion_policy": ("insert_when_topology_queue_exhausted_before_target"),
        "threshold_metric": "paper_base_cost",
        "stop_reasons": [
            "target_count_reached",
            "all_remaining_edges_blocked_by_threshold",
            "queue_exhausted_before_target_count",
        ],
        "lookahead_used": False,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
    }
    assert payload["coverage_summary"] == {
        "search_trace_row_count": 8,
        "topology_trace_row_count": 3,
        "component_pair_trace_row_count": 5,
        "threshold_blocked_row_count": 2,
        "closed_gate_count": 3,
        "remaining_generalization_gate_count": 2,
    }
    assert payload["remaining_gaps"] == EXPECTED_SEARCH_ENGINE_REMAINING_GAPS
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
    assert "timing" not in payload
    assert "surface_distance" not in payload
    assert "collision_quality" not in payload
    assert "benchmark" not in payload

    assert [row["row_id"] for row in payload["search_trace_matrix"]] == [
        "topology_chain_target_count",
        "weighted_priority_over_base_cost",
        "equal_cost_queue_tie",
        "component_pair_threshold_disabled_accept",
        "component_pair_zero_threshold_block",
        "component_pair_positive_threshold_block",
        "component_pair_multi_candidate_order",
        "component_pair_candidate_cap_skipped",
    ]
    for row in payload["search_trace_matrix"]:
        assert row["row_status"] == "implemented_offline_search_trace_fixture"
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False


def test_cpd_paper_search_engine_generalization_rows_match_case_payloads(cpd_paper_report):
    report = cpd_paper_report
    report_again = _fresh_independent_cpd_paper_offline_report_for_determinism_check()
    assert report_again is not report
    cases = {case["case_id"]: case for case in report["cases"]}
    rows = {
        row["row_id"]: row
        for row in report["paper_generalization_batch_c_search_engine"]["search_trace_matrix"]
    }

    expected_case_by_row = {
        "topology_chain_target_count": "paper_three_face_chain",
        "weighted_priority_over_base_cost": "paper_branching_cost_order",
        "equal_cost_queue_tie": "paper_equal_cost_queue_tie",
        "component_pair_threshold_disabled_accept": "paper_disconnected_components",
        "component_pair_zero_threshold_block": "paper_component_pair_threshold_blocked",
        "component_pair_positive_threshold_block": "paper_nonzero_threshold_block",
        "component_pair_multi_candidate_order": ("paper_component_pair_multi_candidate_order"),
        "component_pair_candidate_cap_skipped": "paper_component_pair_cap_skipped",
    }
    assert set(rows) == set(expected_case_by_row)

    for row_id, case_id in expected_case_by_row.items():
        row = rows[row_id]
        trace = cases[case_id]["collapse_trace"]
        assert row["evidence_case_id"] == case_id
        assert row["trace_scope"] == trace["trace_scope"]
        assert row["priority_queue_policy"] == trace["priority_queue_policy"]
        assert row["target_primitive_count"] == trace["target_primitive_count"]
        assert row["initial_edge_count"] == trace["initial_edge_count"]
        assert row["initial_candidate_count"] == len(trace["initial_candidates"])
        assert row["component_pair_candidate_count"] == trace["component_pair_candidate_count"]
        assert (
            row["component_pair_available_pair_count"]
            == trace["component_pair_available_pair_count"]
        )
        assert row["component_pair_candidate_cap"] == trace["component_pair_candidate_cap"]
        assert row["skipped_component_pair_count"] == trace["skipped_component_pair_count"]
        assert row["threshold_policy"] == trace["threshold_policy"]
        assert row["excess_volume_threshold"] == trace["excess_volume_threshold"]
        assert row["accepted_merge_count"] == trace["accepted_merge_count"]
        assert row["blocked_merge_count"] == trace["blocked_merge_count"]
        assert row["stale_entry_skipped_count"] == trace["stale_entry_skipped_count"]
        assert row["event_count"] == len(trace["events"])
        assert row["event_kinds"] == [event["event_kind"] for event in trace["events"]]
        assert row["stop_reason"] == trace["stop_reason"]
        assert row["final_active_groups"] == trace["final_active_groups"]
        assert (
            row["component_pair_edge_insertion_triggered"]
            == trace["component_pair_edge_insertion_triggered"]
        )
        assert (
            row["topology_queue_exhausted_before_component_pair_insertion"]
            == (trace["topology_queue_exhausted_before_component_pair_insertion"])
        )
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False

        first_accepted = next((event for event in trace["events"] if event["accepted"]), None)
        if first_accepted is None:
            assert row["first_accepted_queue_key"] is None
        else:
            assert row["first_accepted_queue_key"] == first_accepted["queue_key"]

        blocked_events = [
            event for event in trace["events"] if event["event_kind"] == "blocked_by_threshold"
        ]
        assert row["threshold_metric"] == (
            blocked_events[0]["threshold_metric"] if blocked_events else None
        )
        for candidate in [
            *trace["initial_candidates"],
            *trace["component_pair_candidates"],
            *trace["events"],
        ]:
            _assert_queue_key_contract(candidate)
            assert isfinite(candidate["paper_base_cost"])
            assert isfinite(candidate["weighted_priority_cost"])
        for event in trace["events"]:
            if event["accepted"]:
                assert event["resulting_source_faces"]
            if event["event_kind"] == "blocked_by_threshold":
                assert event["threshold_metric"] == "paper_base_cost"
                assert (
                    event["active_primitive_count_before"] == event["active_primitive_count_after"]
                )
                assert "resulting_source_faces" not in event

    branching = cases["paper_branching_cost_order"]["collapse_trace"]
    first_accepted = [event for event in branching["events"] if event["accepted"]][0]
    min_weighted = min(
        branching["initial_candidates"], key=lambda candidate: candidate["queue_key"]
    )
    min_base = min(
        branching["initial_candidates"],
        key=lambda candidate: candidate["paper_base_cost"],
    )
    assert first_accepted["queue_key"] == min_weighted["queue_key"]
    assert min_weighted["queue_key"] != min_base["queue_key"]

    equal_cost = cases["paper_equal_cost_queue_tie"]["collapse_trace"]
    equal_cost_again = {case["case_id"]: case for case in report_again["cases"]}[
        "paper_equal_cost_queue_tie"
    ]["collapse_trace"]
    assert "eager_stale_prune" in rows["equal_cost_queue_tie"]["event_kinds"]
    assert _event_signature(equal_cost) == _event_signature(equal_cost_again)

    nonzero_block = rows["component_pair_positive_threshold_block"]
    assert nonzero_block["threshold_metric"] == "paper_base_cost"
    assert nonzero_block["first_accepted_queue_key"] is None
    assert nonzero_block["blocked_merge_count"] == 1
    assert nonzero_block["stop_reason"] == "all_remaining_edges_blocked_by_threshold"

    zero_block = rows["component_pair_zero_threshold_block"]
    assert zero_block["threshold_metric"] == "paper_base_cost"
    assert zero_block["first_accepted_queue_key"] is None
    assert zero_block["blocked_merge_count"] == 1

    multi_candidate = rows["component_pair_multi_candidate_order"]
    assert multi_candidate["component_pair_candidate_count"] == 3
    assert multi_candidate["component_pair_available_pair_count"] == 3
    assert multi_candidate["topology_queue_exhausted_before_component_pair_insertion"] is True

    capped = rows["component_pair_candidate_cap_skipped"]
    assert capped["component_pair_candidate_cap"] == 2
    assert capped["component_pair_candidate_count"] == 2
    assert capped["skipped_component_pair_count"] == 4


def test_cpd_paper_offline_report_records_postprocess_policy_generalization_gate(cpd_paper_report):
    report = cpd_paper_report

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert (
        report["paper_faithfulness"]["implemented_generalization_scope"]
        == EXPECTED_CLOSED_GENERALIZATION_GATES
    )
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert report["paper_faithful_offline_supported"] is False
    assert report["status"] == "partial"

    payload = report["paper_generalization_batch_d_postprocess_policy"]
    assert payload["gate_id"] == EXPECTED_CLOSED_POSTPROCESS_POLICY_GATE
    assert payload["gate_status"] == "implemented_offline_report_only_partial"
    assert payload["closed_gate"] == EXPECTED_CLOSED_POSTPROCESS_POLICY_GATE
    assert (
        payload["next_required_gate"] == "paper_generalization_batch_e_package_boundary_readiness"
    )
    assert payload["decision"] == "remain_partial"
    assert (
        payload["decision_reason"]
        == "postprocess_policy_generalization_complete_package_boundary_readiness_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["source_scope"] == "deterministic_in_memory_postprocess_audit_fixtures"
    assert payload["implementation_boundary"] == "offline_report_only_no_package_or_newton"
    assert payload["postprocess_policy_contract"] == {
        "input_contract": "explicit_offline_postprocess_audit_primitives_not_search_output",
        "supported_containment_tests": ["obb_corners_inside_obb"],
        "supported_axis_policies": ["shared_identity_axes", "shared_rotated_axes"],
        "unsupported_boundary_policy": "record_cross_type_unsupported_without_silent_cull",
        "unsupported_boundary_label": "cross_type_enclosure_boundary_not_supported",
        "output_accounting_fields": [
            "input_primitive_count",
            "output_primitive_count",
            "kept_primitive_ids",
            "culled_primitive_ids",
            "cull_records",
            "unsupported_records",
        ],
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
    }
    assert payload["coverage_summary"] == {
        "postprocess_row_count": 3,
        "obb_cull_row_count": 2,
        "rotated_obb_row_count": 1,
        "unsupported_cross_type_row_count": 1,
        "cull_record_count": 2,
        "unsupported_record_count": 1,
        "closed_gate_count": 4,
        "remaining_generalization_gate_count": 1,
    }
    assert payload["remaining_gaps"] == EXPECTED_POSTPROCESS_POLICY_REMAINING_GAPS
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
    assert "timing" not in payload
    assert "surface_distance" not in payload
    assert "collision_quality" not in payload
    assert "benchmark" not in payload

    assert [row["row_id"] for row in payload["postprocess_policy_matrix"]] == [
        "identity_nested_obb_cull",
        "rotated_nested_obb_cull",
        "cross_type_enclosure_no_silent_cull_boundary",
    ]
    for row in payload["postprocess_policy_matrix"]:
        assert row["row_status"] == "implemented_offline_postprocess_fixture"
        assert (
            row["claim_boundary"]
            == "summarizes_named_postprocess_audits_not_general_containment_library"
        )
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False
        assert "input_primitives" not in row


def test_cpd_paper_postprocess_policy_generalization_rows_match_case_payloads(cpd_paper_report):
    report = cpd_paper_report
    cases = {case["case_id"]: case for case in report["cases"]}
    rows = {
        row["row_id"]: row
        for row in report["paper_generalization_batch_d_postprocess_policy"][
            "postprocess_policy_matrix"
        ]
    }

    expected_case_by_row = {
        "identity_nested_obb_cull": "paper_nested_primitive",
        "rotated_nested_obb_cull": "paper_rotated_nested_primitive",
        "cross_type_enclosure_no_silent_cull_boundary": ("paper_cross_type_enclosure_boundary"),
    }
    assert set(rows) == set(expected_case_by_row)

    for row_id, case_id in expected_case_by_row.items():
        row = rows[row_id]
        postprocess = cases[case_id]["postprocess_audit"]
        assert row["evidence_case_id"] == case_id
        assert row["audit_scope"] == postprocess["audit_scope"]
        assert row["fixture_variant"] == postprocess["fixture_variant"]
        assert row["postprocess_input_source"] == postprocess["postprocess_input_source"]
        assert row["postprocess_policy"] == postprocess["postprocess_policy"]
        assert row["containment_test_type"] == postprocess["containment_test_type"]
        assert row["axis_policy"] == postprocess.get("axis_policy")
        assert row["rotation_degrees_about_z"] == postprocess.get("rotation_degrees_about_z")
        assert row["rotated_axes_non_identity"] == postprocess.get("rotated_axes_non_identity")
        assert row["cross_type_culling_supported"] == postprocess.get(
            "cross_type_culling_supported"
        )
        assert row["unsupported_containment_label"] == postprocess.get(
            "unsupported_containment_label"
        )
        assert row["input_primitive_count"] == postprocess["input_primitive_count"]
        assert row["output_primitive_count"] == postprocess["output_primitive_count"]
        assert row["culled_primitive_ids"] == postprocess["culled_primitive_ids"]
        assert row["kept_primitive_ids"] == postprocess["kept_primitive_ids"]
        assert row["enclosed_primitive_ids"] == postprocess["enclosed_primitive_ids"]
        assert row["enclosing_primitive_ids"] == postprocess["enclosing_primitive_ids"]
        assert row["cull_record_count"] == len(postprocess["cull_records"])
        assert row["unsupported_record_count"] == len(postprocess.get("unsupported_records", []))
        assert row["top_level_failure_label"] == postprocess.get("top_level_failure_label", False)
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False

    identity = rows["identity_nested_obb_cull"]
    assert identity["axis_policy"] == "shared_identity_axes"
    assert identity["cull_record_count"] == 1
    assert identity["culled_primitive_ids"] == [1]
    assert identity["output_primitive_count"] == identity["input_primitive_count"] - 1

    rotated = rows["rotated_nested_obb_cull"]
    assert rotated["axis_policy"] == "shared_rotated_axes"
    assert rotated["rotated_axes_non_identity"] is True
    assert rotated["rotation_degrees_about_z"] == 30.0
    assert rotated["cull_record_count"] == 1
    assert rotated["culled_primitive_ids"] == [1]

    cross_type = rows["cross_type_enclosure_no_silent_cull_boundary"]
    assert cross_type["cross_type_culling_supported"] is False
    assert (
        cross_type["unsupported_containment_label"] == "cross_type_enclosure_boundary_not_supported"
    )
    assert cross_type["cull_record_count"] == 0
    assert cross_type["unsupported_record_count"] == 1
    assert cross_type["top_level_failure_label"] is False
    assert cross_type["culled_primitive_ids"] == []
    assert cross_type["kept_primitive_ids"] == [0, 1]


def test_cpd_paper_offline_report_records_package_boundary_readiness_gate(cpd_paper_report):
    report = cpd_paper_report

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert (
        report["paper_faithfulness"]["implemented_generalization_scope"]
        == EXPECTED_CLOSED_GENERALIZATION_GATES
    )
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert report["paper_faithful_offline_supported"] is False
    assert report["status"] == "partial"
    assert (
        "paper_generalization_batch_e_package_boundary_readiness_missing"
        not in (report["failure_labels"])
    )

    payload = report["paper_generalization_batch_e_package_boundary_readiness"]
    assert payload["gate_id"] == EXPECTED_CLOSED_PACKAGE_BOUNDARY_GATE
    assert payload["gate_status"] == "implemented_planning_only_partial"
    assert payload["closed_gate"] == EXPECTED_CLOSED_PACKAGE_BOUNDARY_GATE
    assert payload["next_required_gate"] == EXPECTED_NEXT_AFTER_PACKAGE_BOUNDARY
    assert payload["decision"] == "remain_partial"
    assert (
        payload["decision_reason"]
        == "package_boundary_readiness_review_complete_changed_decomposition_output_contract_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["source_scope"] == "offline_generalization_payloads_after_batches_a_to_d"
    assert payload["implementation_boundary"] == "planning_only_no_package_or_newton"
    assert payload["boundary_review_contract"] == {
        "input_scope": "implemented_offline_generalization_payloads_a_to_d",
        "review_output": "package_boundary_readiness_matrix_not_package_generation",
        "changed_decomposition_output_contract_required": True,
        "package_generation_contract_required": True,
        "runtime_admissibility_required_after_package_conversion": True,
        "package_generation_allowed": False,
        "newton_runtime_allowed": False,
        "real_usd_allowed": False,
        "benchmark_allowed": False,
    }
    assert payload["coverage_summary"] == {
        "boundary_review_row_count": 5,
        "blocked_row_count": 5,
        "closed_gate_count": 5,
        "remaining_generalization_gate_count": 0,
        "package_generation_allowed_row_count": 0,
        "newton_runtime_allowed_row_count": 0,
        "real_usd_allowed_row_count": 0,
        "benchmark_allowed_row_count": 0,
    }
    assert payload["remaining_gaps"] == EXPECTED_PACKAGE_BOUNDARY_REMAINING_GAPS
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
    assert "collision_quality" not in payload
    assert "surface_distance" not in payload
    assert "timing" not in payload

    assert [row["row_id"] for row in payload["boundary_review_matrix"]] == [
        "changed_decomposition_output_contract",
        "package_generation_boundary",
        "newton_runtime_boundary",
        "real_usd_boundary",
        "benchmark_evaluation_boundary",
    ]


def test_cpd_paper_package_boundary_readiness_keeps_runtime_work_blocked(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_generalization_batch_e_package_boundary_readiness"]

    forbidden_statuses = {
        "package_ready",
        "newton_ready",
        "runtime_ready",
        "benchmark_ready",
        "paper_faithful_offline",
    }
    for row in payload["boundary_review_matrix"]:
        assert row["row_status"] not in forbidden_statuses
        assert row["required_before_unlock"]
        assert row["current_evidence"]
        assert row["blocked_reason"]
        assert row["next_gate_if_blocked"]
        assert row["claim_boundary"]
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False

    rows = {row["row_id"]: row for row in payload["boundary_review_matrix"]}
    assert rows["changed_decomposition_output_contract"]["next_gate_if_blocked"] == (
        EXPECTED_NEXT_AFTER_PACKAGE_BOUNDARY
    )
    assert rows["package_generation_boundary"]["next_gate_if_blocked"] == (
        EXPECTED_PACKAGE_GENERATION_CONTRACT
    )
    assert rows["newton_runtime_boundary"]["next_gate_if_blocked"] == (
        "paper_newton_runtime_admissibility_gate"
    )
    assert rows["real_usd_boundary"]["next_gate_if_blocked"] == ("paper_real_usd_asset_scope_gate")
    assert rows["benchmark_evaluation_boundary"]["next_gate_if_blocked"] == (
        "paper_benchmark_evaluation_design_gate"
    )


def test_cpd_paper_offline_report_records_changed_decomposition_output_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert report["paper_faithfulness"]["implemented_output_contract_scope"] == [
        EXPECTED_CLOSED_CHANGED_DECOMPOSITION_CONTRACT,
        EXPECTED_PACKAGE_ADAPTER_CONTRACT,
        EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY,
        EXPECTED_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN,
        EXPECTED_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX,
        EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_SERIALIZATION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_CONTRACT,
    ]
    assert (
        report["paper_faithfulness"]["implemented_generalization_scope"]
        == EXPECTED_CLOSED_GENERALIZATION_GATES
    )
    assert report["paper_faithful_offline_supported"] is False
    assert report["status"] == "partial"
    assert (
        "paper_offline_changed_decomposition_output_contract_missing"
        not in (report["failure_labels"])
    )

    payload = report["paper_offline_changed_decomposition_output_contract"]
    assert payload["gate_id"] == EXPECTED_CLOSED_CHANGED_DECOMPOSITION_CONTRACT
    assert payload["gate_status"] == "implemented_offline_contract_only_partial"
    assert payload["closed_gate"] == EXPECTED_CLOSED_CHANGED_DECOMPOSITION_CONTRACT
    assert payload["next_required_gate"] == EXPECTED_PACKAGE_ADAPTER_CONTRACT
    assert payload["decision"] == "remain_partial"
    assert (
        payload["decision_reason"]
        == "changed_decomposition_output_contract_complete_package_adapter_contract_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == "offline_changed_decomposition_output_not_collision_package"
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert (
        payload["implementation_boundary"]
        == "offline_report_contract_no_collision_package_no_newton"
    )
    assert payload["output_contract"] == {
        "required_output_fields": [
            "output_id",
            "evidence_case_id",
            "source_mesh_summary",
            "search_summary",
            "primitive_records",
            "postprocess_state",
            "unsupported_boundaries",
            "claim_boundary",
        ],
        "primitive_record_fields": [
            "offline_primitive_id",
            "source_faces",
            "generated_triangle_face_ids",
            "source_face_ids",
            "paper_primitive",
            "center",
            "axes",
            "dimensions",
            "volume",
            "paper_weight",
            "weighted_volume",
            "contains_assigned_points",
            "newton_runtime_kind",
            "conversion_status",
        ],
        "conversion_status": "offline_contract_only_not_package_candidate",
    }
    assert payload["coverage_summary"] == {
        "decomposition_output_row_count": 9,
        "primitive_record_count": 16,
        "postprocess_state_row_count": 3,
        "source_policy_summary_row_count": 3,
        "primitive_family_count": 6,
        "search_trace_summary_row_count": 8,
        "package_boundary_row_count": 5,
    }
    assert payload["remaining_gaps"] == [EXPECTED_PACKAGE_ADAPTER_CONTRACT]
    assert len(payload["decomposition_output_rows"]) == 9
    assert len(payload["postprocess_state_rows"]) == 3
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
    assert "CollisionPackage" not in payload
    assert "PrimitiveSpec" not in payload
    assert "collision_quality" not in payload
    assert "surface_distance" not in payload
    assert "timing" not in payload


def test_cpd_paper_changed_decomposition_output_rows_match_search_case_payloads(cpd_paper_report):
    report = cpd_paper_report
    cases = {case["case_id"]: case for case in report["cases"]}
    payload = report["paper_offline_changed_decomposition_output_contract"]
    rows = payload["decomposition_output_rows"]

    assert [row["evidence_case_id"] for row in rows] == [
        "paper_three_face_chain",
        "paper_disconnected_components",
        "paper_component_pair_threshold_blocked",
        "paper_duplicate_vertex_preprocessing",
        "paper_branching_cost_order",
        "paper_equal_cost_queue_tie",
        "paper_nonzero_threshold_block",
        "paper_component_pair_multi_candidate_order",
        "paper_component_pair_cap_skipped",
    ]

    for row in rows:
        case = cases[row["evidence_case_id"]]
        trace = case["collapse_trace"]
        selected = case["primitive_fit_audit"]["selected"]
        assert row["output_id"] == f"{case['case_id']}:changed_decomposition_output"
        assert row["row_status"] == "implemented_offline_contract_row"
        assert row["source_mesh_summary"]["vertex_count"] == case["source_mesh"]["vertex_count"]
        assert row["source_mesh_summary"]["face_count"] == case["source_mesh"]["face_count"]
        assert (
            row["source_mesh_summary"]["connected_component_count"]
            == case["source_mesh"]["connected_component_count"]
        )
        assert row["search_summary"]["final_active_groups"] == trace["final_active_groups"]
        assert row["search_summary"]["target_primitive_count"] == trace["target_primitive_count"]
        assert row["search_summary"]["stop_reason"] == trace["stop_reason"]
        assert row["search_summary"]["accepted_merge_count"] == trace["accepted_merge_count"]
        assert row["search_summary"]["blocked_merge_count"] == trace["blocked_merge_count"]
        assert len(row["primitive_records"]) == len(trace["final_active_groups"])
        for index, primitive in enumerate(row["primitive_records"]):
            final_group = trace["final_active_groups"][index]
            assert primitive["offline_primitive_id"] == (
                f"{case['case_id']}:offline_primitive:{index}"
            )
            assert primitive["source_faces"] == final_group
            assert primitive["generated_triangle_face_ids"] == final_group
            assert primitive["source_face_ids"] == final_group
            assert primitive["paper_primitive"] == selected["paper_primitive"]
            assert primitive["center"] == selected["center"]
            assert primitive["axes"] == selected["axes"]
            assert primitive["dimensions"] == selected["dimensions"]
            assert primitive["volume"] == selected["volume"]
            assert primitive["paper_weight"] == selected["paper_weight"]
            assert primitive["weighted_volume"] == selected["weighted_volume"]
            assert primitive["contains_assigned_points"] == selected["contains_assigned_points"]
            assert primitive["newton_runtime_kind"] == selected["newton_runtime_kind"]
            assert (
                primitive["primitive_fit_scope"]
                == "case_selected_candidate_reused_for_contract_row_not_group_refit"
            )
            assert primitive["conversion_status"] == "offline_contract_only_not_package_candidate"
        assert row["postprocess_state"] == "not_applied_to_search_output"
        assert row["unsupported_boundaries"]["package_adapter_contract_required"] is True
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False


def test_cpd_paper_changed_decomposition_contract_records_postprocess_state_without_applying_to_search_output(
    cpd_paper_report,
):
    report = cpd_paper_report
    cases = {case["case_id"]: case for case in report["cases"]}
    payload = report["paper_offline_changed_decomposition_output_contract"]
    rows = {row["evidence_case_id"]: row for row in payload["postprocess_state_rows"]}

    assert set(rows) == {
        "paper_nested_primitive",
        "paper_rotated_nested_primitive",
        "paper_cross_type_enclosure_boundary",
    }
    for case_id, row in rows.items():
        postprocess = cases[case_id]["postprocess_audit"]
        assert row["state_id"] == f"{case_id}:postprocess_state"
        assert row["state_scope"] == "explicit_postprocess_audit_fixture_not_search_output"
        assert row["postprocess_input_source"] == postprocess["postprocess_input_source"]
        assert row["postprocess_policy"] == postprocess["postprocess_policy"]
        assert row["kept_primitive_ids"] == postprocess["kept_primitive_ids"]
        assert row["culled_primitive_ids"] == postprocess["culled_primitive_ids"]
        assert row["cull_record_count"] == len(postprocess["cull_records"])
        assert row["unsupported_record_count"] == len(postprocess.get("unsupported_records", []))
        assert row["unsupported_containment_label"] == postprocess.get(
            "unsupported_containment_label"
        )
        assert "input_primitives" not in row
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False


def test_cpd_paper_offline_report_records_package_adapter_contract_gate(cpd_paper_report):
    report = cpd_paper_report

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert report["paper_faithfulness"]["implemented_output_contract_scope"] == [
        EXPECTED_CLOSED_CHANGED_DECOMPOSITION_CONTRACT,
        EXPECTED_PACKAGE_ADAPTER_CONTRACT,
        EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY,
        EXPECTED_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN,
        EXPECTED_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX,
        EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_SERIALIZATION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_CONTRACT,
    ]
    assert report["paper_faithful_offline_supported"] is False
    assert report["status"] == "partial"
    assert "paper_package_adapter_contract_missing" not in report["failure_labels"]

    payload = report["paper_package_adapter_contract"]
    assert payload["gate_id"] == EXPECTED_PACKAGE_ADAPTER_CONTRACT
    assert payload["gate_status"] == "implemented_offline_adapter_contract_only_partial"
    assert payload["closed_gate"] == EXPECTED_PACKAGE_ADAPTER_CONTRACT
    assert payload["input_gate_id"] == EXPECTED_CLOSED_CHANGED_DECOMPOSITION_CONTRACT
    assert payload["next_required_gate"] == EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY
    assert payload["decision"] == "remain_partial"
    assert (
        payload["decision_reason"]
        == "package_adapter_contract_complete_unsupported_primitive_policy_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == "offline_package_adapter_contract_not_collision_package"
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert (
        payload["implementation_boundary"]
        == "offline_adapter_contract_no_collision_package_no_newton"
    )
    assert payload["remaining_gaps"] == EXPECTED_PACKAGE_ADAPTER_REMAINING_GAPS
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
    assert "CollisionPackage" not in payload
    assert "PrimitiveSpec" not in payload


def test_cpd_paper_package_adapter_contract_summarizes_changed_decomposition_contract(
    cpd_paper_report,
):
    report = cpd_paper_report
    changed = report["paper_offline_changed_decomposition_output_contract"]
    adapter = report["paper_package_adapter_contract"]

    assert adapter["input_contract_summary"] == {
        "input_gate_id": EXPECTED_CLOSED_CHANGED_DECOMPOSITION_CONTRACT,
        "input_artifact_kind": "offline_changed_decomposition_output_not_collision_package",
        "decomposition_output_row_count": changed["coverage_summary"][
            "decomposition_output_row_count"
        ],
        "primitive_record_count": changed["coverage_summary"]["primitive_record_count"],
        "postprocess_state_row_count": changed["coverage_summary"]["postprocess_state_row_count"],
    }
    assert adapter["adapter_decision_contract"] == {
        "decision_values": [
            "adapter_eligible",
            "blocked",
            "later_policy_required",
        ],
        "current_direct_adapter_policy": "none_for_current_changed_decomposition_rows",
        "unsupported_primitive_policy_required": True,
        "package_generation_allowed": False,
    }
    assert adapter["coverage_summary"]["decomposition_output_row_count"] == len(
        changed["decomposition_output_rows"]
    )
    assert adapter["coverage_summary"]["primitive_decision_row_count"] == 16
    assert len(adapter["primitive_adapter_decision_rows"]) == 16


def test_cpd_paper_package_adapter_decision_counts_partition_current_records(cpd_paper_report):
    report = cpd_paper_report
    adapter = report["paper_package_adapter_contract"]
    summary = adapter["coverage_summary"]

    assert summary["adapter_eligible_record_count"] == 0
    assert summary["blocked_record_count"] == 0
    assert summary["later_policy_required_record_count"] == 16
    assert summary["offline_only_unmapped_record_count"] == 16
    assert (
        summary["adapter_eligible_record_count"]
        + summary["blocked_record_count"]
        + summary["later_policy_required_record_count"]
        == summary["primitive_decision_row_count"]
    )
    assert summary["primitive_decision_row_count"] == len(
        adapter["primitive_adapter_decision_rows"]
    )

    expected_source_ids = {
        primitive["offline_primitive_id"]
        for output_row in report["paper_offline_changed_decomposition_output_contract"][
            "decomposition_output_rows"
        ]
        for primitive in output_row["primitive_records"]
    }
    adapter_source_ids = {
        row["offline_primitive_id"] for row in adapter["primitive_adapter_decision_rows"]
    }
    assert adapter_source_ids == expected_source_ids

    for row in adapter["primitive_adapter_decision_rows"]:
        assert row["adapter_decision_id"] == (f"{row['offline_primitive_id']}:adapter_decision")
        assert row["paper_primitive"] == "trapezoidal_prism"
        assert row["offline_runtime_kind_label"] == "offline_only_unmapped"
        assert row["record_field_status"] == "complete"
        assert row["postprocess_state"] == "not_applied_to_search_output"
        assert row["adapter_decision"] == "later_policy_required"
        assert (
            row["adapter_decision_reason"] == "unsupported_paper_primitive_requires_adapter_policy"
        )
        assert row["required_later_gate"] == EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY


def test_cpd_paper_package_adapter_contract_stays_report_only(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_package_adapter_contract"]

    assert payload["package_generation_allowed"] is False
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
    forbidden_keys = {
        "CollisionPackage",
        "PrimitiveSpec",
        "runtime_result",
        "usd_asset_path",
        "benchmark_metric",
        "timing",
        "surface_distance",
        "collision_quality",
    }
    assert forbidden_keys.isdisjoint(payload)
    for row in payload["primitive_adapter_decision_rows"]:
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False
        assert forbidden_keys.isdisjoint(row)


def test_cpd_paper_records_unsupported_primitive_policy_gate(cpd_paper_report):
    report = cpd_paper_report

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert (
        EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )

    payload = report["paper_package_adapter_unsupported_primitive_policy"]
    assert payload["gate_id"] == EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY
    assert payload["gate_status"] == "implemented_offline_unsupported_primitive_policy_only_partial"
    assert payload["closed_gate"] == EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY
    assert payload["input_gate_id"] == EXPECTED_PACKAGE_ADAPTER_CONTRACT
    assert payload["next_required_gate"] == EXPECTED_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN
    assert payload["decision"] == "remain_partial"
    assert (
        payload["decision_reason"]
        == "unsupported_primitive_policy_complete_mapped_subset_plan_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == (
        "offline_unsupported_primitive_policy_not_collision_package"
    )
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["implementation_boundary"] == (
        "offline_unsupported_primitive_policy_no_collision_package_no_newton"
    )
    assert payload["remaining_gaps"] == EXPECTED_UNSUPPORTED_POLICY_REMAINING_GAPS
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False


def test_cpd_paper_unsupported_primitive_policy_classifies_paper_families(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_package_adapter_unsupported_primitive_policy"]
    rows = {row["paper_primitive"]: row for row in payload["paper_primitive_family_policy_rows"]}

    assert list(rows) == [
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
    assert rows["oriented_bounding_box"]["newton_runtime_kind"] == "box"
    assert rows["sphere"]["newton_runtime_kind"] == "sphere"
    assert rows["capsule"]["newton_runtime_kind"] == "capsule"
    for primitive_name in ("oriented_bounding_box", "sphere", "capsule"):
        row = rows[primitive_name]
        assert row["paper_family_status"] == "direct_newton_native_candidate"
        assert row["adapter_policy"] == "candidate_for_mapped_subset_plan"
        assert row["direct_adapter_allowed_after_mapped_subset_plan"] is True
        assert row["package_conversion_enabled_by_this_gate"] is False
        assert row["fallback_generation_allowed"] is False
        assert row["drop_allowed"] is False

    for primitive_name in ("capped_cylinder", "frustum", "trapezoidal_prism"):
        row = rows[primitive_name]
        assert row["paper_family_status"] == "offline_only_unmapped"
        assert row["newton_runtime_kind"] == "offline_only_unmapped"
        assert (
            row["adapter_policy"] == "keep_offline_until_explicit_mapping_or_approximation_policy"
        )
        assert row["direct_adapter_allowed_after_mapped_subset_plan"] is False
        assert row["package_conversion_enabled_by_this_gate"] is False
        assert row["requires_explicit_mapping_or_approximation_policy"] is True
        assert row["fallback_generation_allowed"] is False
        assert row["drop_allowed"] is False

    assert rows["trapezoidal_prism"]["current_row_evidence_count"] == 16
    assert rows["capped_cylinder"]["current_row_evidence_count"] == 0
    assert rows["frustum"]["current_row_evidence_count"] == 0


def test_cpd_paper_unsupported_primitive_policy_blocks_current_unmapped_rows(cpd_paper_report):
    report = cpd_paper_report
    adapter = report["paper_package_adapter_contract"]
    payload = report["paper_package_adapter_unsupported_primitive_policy"]
    summary = payload["coverage_summary"]
    rows = payload["current_adapter_decision_policy_rows"]

    assert summary["decomposition_output_row_count"] == 9
    assert summary["primitive_decision_row_count"] == 16
    assert summary["paper_primitive_family_policy_row_count"] == 6
    assert summary["current_adapter_decision_policy_row_count"] == 16
    assert summary["direct_policy_eligible_record_count"] == 0
    assert summary["unsupported_policy_blocked_record_count"] == 16
    assert summary["adapter_contract_blocked_record_count"] == 0
    assert summary["dropped_record_count"] == 0
    assert summary["package_candidate_record_count"] == 0
    assert summary["current_paper_primitive_distribution"] == {
        "trapezoidal_prism": 16,
    }
    assert summary["current_runtime_kind_distribution"] == {
        "offline_only_unmapped": 16,
    }
    assert (
        summary["direct_policy_eligible_record_count"]
        + summary["unsupported_policy_blocked_record_count"]
        + summary["adapter_contract_blocked_record_count"]
        + summary["dropped_record_count"]
        == summary["current_adapter_decision_policy_row_count"]
    )

    assert len(rows) == len(adapter["primitive_adapter_decision_rows"]) == 16
    for row, adapter_row in zip(rows, adapter["primitive_adapter_decision_rows"]):
        assert row["policy_decision_id"] == (
            f"{adapter_row['adapter_decision_id']}:unsupported_policy"
        )
        assert row["source_adapter_decision_id"] == adapter_row["adapter_decision_id"]
        assert row["source_output_id"] == adapter_row["source_output_id"]
        assert row["evidence_case_id"] == adapter_row["evidence_case_id"]
        assert row["offline_primitive_id"] == adapter_row["offline_primitive_id"]
        assert row["paper_primitive"] == "trapezoidal_prism"
        assert row["offline_runtime_kind_label"] == "offline_only_unmapped"
        assert row["input_adapter_decision"] == "later_policy_required"
        assert row["unsupported_policy_decision"] == "block_package_conversion"
        assert row["adapter_action"] == "keep_offline"
        assert row["package_candidate_status"] == ("not_package_candidate_unsupported_policy_block")
        assert row["required_later_gate"] == EXPECTED_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False


def test_cpd_paper_unsupported_primitive_policy_stays_report_only(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_package_adapter_unsupported_primitive_policy"]

    forbidden_keys = {
        "CollisionPackage",
        "PrimitiveSpec",
        "runtime_result",
        "usd_asset_path",
        "benchmark_metric",
        "timing",
        "surface_distance",
        "collision_quality",
    }
    assert forbidden_keys.isdisjoint(payload)
    for row in payload["paper_primitive_family_policy_rows"]:
        assert forbidden_keys.isdisjoint(row)
    for row in payload["current_adapter_decision_policy_rows"]:
        assert forbidden_keys.isdisjoint(row)


def test_cpd_paper_records_package_conversion_mapped_subset_plan_gate(cpd_paper_report):
    report = cpd_paper_report

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert (
        EXPECTED_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )

    payload = report["paper_package_conversion_mapped_subset_plan"]
    assert payload["gate_id"] == EXPECTED_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN
    assert payload["gate_status"] == "implemented_offline_mapped_subset_plan_only_partial"
    assert payload["closed_gate"] == EXPECTED_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN
    assert payload["input_gate_id"] == EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY
    assert payload["next_required_gate"] == EXPECTED_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == "mapped_subset_plan_complete_candidate_matrix_missing"
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == ("offline_mapped_subset_plan_not_collision_package")
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["implementation_boundary"] == (
        "offline_conversion_plan_no_collision_package_no_primitivespec_no_newton"
    )
    assert payload["remaining_gaps"] == EXPECTED_CONVERSION_MAPPED_SUBSET_REMAINING_GAPS
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False


def test_cpd_paper_mapped_subset_plan_classifies_paper_families(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_package_conversion_mapped_subset_plan"]
    rows = {
        row["paper_primitive"]: row
        for row in payload["paper_primitive_family_conversion_plan_rows"]
    }

    assert list(rows) == [
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
    expected_native = {
        "oriented_bounding_box": "box",
        "sphere": "sphere",
        "capsule": "capsule",
    }
    for primitive_name, runtime_kind in expected_native.items():
        row = rows[primitive_name]
        assert row["planned_runtime_kind"] == runtime_kind
        assert row["conversion_plan_decision"] == "plan_direct_native_mapping_later"
        assert row["package_candidate_status"] == ("future_candidate_family_no_current_rows")
        assert row["current_row_evidence_count"] == 0
        assert row["package_conversion_enabled_by_this_gate"] is False

    for primitive_name in ("capped_cylinder", "frustum", "trapezoidal_prism"):
        row = rows[primitive_name]
        assert row["planned_runtime_kind"] == "offline_only_unmapped"
        assert row["conversion_plan_decision"] == (
            "exclude_requires_explicit_mapping_or_approximation_policy"
        )
        assert row["package_candidate_status"] == ("not_package_candidate_unsupported_policy_block")
        assert row["package_conversion_enabled_by_this_gate"] is False
        assert row["requires_explicit_mapping_or_approximation_policy"] is True
    assert rows["trapezoidal_prism"]["current_row_evidence_count"] == 16


def test_cpd_paper_mapped_subset_plan_excludes_current_unmapped_rows(cpd_paper_report):
    report = cpd_paper_report
    unsupported = report["paper_package_adapter_unsupported_primitive_policy"]
    payload = report["paper_package_conversion_mapped_subset_plan"]
    summary = payload["coverage_summary"]
    rows = payload["current_row_conversion_plan_rows"]

    assert summary["decomposition_output_row_count"] == 9
    assert summary["primitive_decision_row_count"] == 16
    assert summary["paper_primitive_family_conversion_plan_row_count"] == 6
    assert summary["current_row_conversion_plan_row_count"] == 16
    assert summary["direct_mapped_current_candidate_record_count"] == 0
    assert summary["future_candidate_family_without_current_rows_count"] == 3
    assert summary["excluded_requires_policy_record_count"] == 16
    assert summary["adapter_contract_blocked_record_count"] == 0
    assert summary["package_candidate_record_count"] == 0
    assert summary["dropped_record_count"] == 0
    assert summary["current_paper_primitive_distribution"] == {
        "trapezoidal_prism": 16,
    }
    assert summary["current_runtime_kind_distribution"] == {
        "offline_only_unmapped": 16,
    }
    assert (
        summary["direct_mapped_current_candidate_record_count"]
        + summary["excluded_requires_policy_record_count"]
        + summary["adapter_contract_blocked_record_count"]
        + summary["dropped_record_count"]
        == summary["current_row_conversion_plan_row_count"]
    )

    unsupported_rows = unsupported["current_adapter_decision_policy_rows"]
    assert len(rows) == len(unsupported_rows) == 16
    for row, upstream_row in zip(rows, unsupported_rows):
        assert row["conversion_plan_row_id"] == (
            f"{upstream_row['policy_decision_id']}:mapped_subset_plan"
        )
        assert row["source_policy_decision_id"] == upstream_row["policy_decision_id"]
        assert row["source_adapter_decision_id"] == (upstream_row["source_adapter_decision_id"])
        assert row["source_output_id"] == upstream_row["source_output_id"]
        assert row["offline_primitive_id"] == upstream_row["offline_primitive_id"]
        assert row["paper_primitive"] == "trapezoidal_prism"
        assert row["offline_runtime_kind_label"] == "offline_only_unmapped"
        assert row["input_unsupported_policy_decision"] == "block_package_conversion"
        assert row["conversion_plan_decision"] == (
            "exclude_requires_explicit_mapping_or_approximation_policy"
        )
        assert row["conversion_plan_action"] == "keep_offline"
        assert row["package_conversion_candidate"] is False
        assert row["package_candidate_status"] == ("not_package_candidate_unsupported_policy_block")
        assert row["required_later_gate"] == (EXPECTED_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX)
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False


def test_cpd_paper_mapped_subset_plan_stays_report_only(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_package_conversion_mapped_subset_plan"]

    forbidden_keys = {
        "CollisionPackage",
        "PrimitiveSpec",
        "runtime_result",
        "usd_asset_path",
        "benchmark_metric",
        "timing",
        "surface_distance",
        "collision_quality",
    }
    assert forbidden_keys.isdisjoint(payload)
    assert payload["mapped_subset_plan_contract"]["primitive_spec_generation_allowed"] is False
    assert payload["mapped_subset_plan_contract"]["collision_package_generation_allowed"] is False
    assert payload["mapped_subset_plan_contract"]["newton_runtime_allowed"] is False
    assert payload["mapped_subset_plan_contract"]["runtime_admissibility_supported"] is False
    for row in payload["paper_primitive_family_conversion_plan_rows"]:
        assert forbidden_keys.isdisjoint(row)
    for row in payload["current_row_conversion_plan_rows"]:
        assert forbidden_keys.isdisjoint(row)


def test_cpd_paper_records_mapped_subset_conversion_candidate_matrix_gate(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_conversion_candidate_matrix"]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )

    assert payload["gate_id"] == EXPECTED_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX
    assert payload["gate_status"] == "implemented_offline_candidate_matrix_only_partial"
    assert payload["closed_gate"] == EXPECTED_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX
    assert payload["input_gate_id"] == EXPECTED_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN
    assert payload["next_required_gate"] == EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT
    assert payload["decision"] == "remain_partial"
    assert (
        payload["decision_reason"] == "candidate_matrix_complete_adapter_preflight_contract_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == (
        "offline_mapped_subset_candidate_matrix_not_collision_package"
    )
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["implementation_boundary"] == (
        "offline_candidate_matrix_no_primitivespec_no_collision_package_no_newton"
    )
    assert payload["remaining_gaps"] == EXPECTED_CANDIDATE_MATRIX_REMAINING_GAPS
    assert payload["primitive_spec_generated"] is False
    assert payload["collision_package_generated"] is False
    assert payload["runtime_admissibility_checked"] is False
    assert payload["newton_support_claimed"] is False
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False


def test_cpd_paper_candidate_matrix_records_future_family_review_rows(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_conversion_candidate_matrix"]
    rows = {row["paper_primitive"]: row for row in payload["future_family_candidate_matrix_rows"]}

    assert list(rows) == [
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
    expected_native = {
        "oriented_bounding_box": "box",
        "sphere": "sphere",
        "capsule": "capsule",
    }
    for primitive_name, runtime_kind in expected_native.items():
        row = rows[primitive_name]
        assert row["candidate_runtime_kind"] == runtime_kind
        assert row["candidate_matrix_decision"] == "native_family_review_only"
        assert row["future_family_review_candidate"] is True
        assert row["current_row_evidence_count"] == 0
        assert row["current_package_conversion_candidate_count"] == 0
        assert row["package_candidate_status"] == ("future_family_review_candidate_no_current_rows")
        assert row["package_conversion_enabled_by_this_gate"] is False
        assert row["primitive_spec_generation_triggered"] is False
        assert row["collision_package_generation_triggered"] is False
        assert row["runtime_admissibility_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False

    for primitive_name in ("capped_cylinder", "frustum"):
        row = rows[primitive_name]
        assert row["candidate_runtime_kind"] == "offline_only_unmapped"
        assert row["candidate_matrix_decision"] == "blocked_approximation_policy_missing"
        assert row["future_family_review_candidate"] is False
        assert row["package_candidate_status"] == (
            "not_current_candidate_mapping_or_approximation_missing"
        )
        assert row["package_conversion_enabled_by_this_gate"] is False

    trapezoid = rows["trapezoidal_prism"]
    assert trapezoid["candidate_runtime_kind"] == "offline_only_unmapped"
    assert trapezoid["candidate_matrix_decision"] == "blocked_unmapped_current_rows"
    assert trapezoid["future_family_review_candidate"] is False
    assert trapezoid["current_row_evidence_count"] == 16
    assert trapezoid["current_package_conversion_candidate_count"] == 0
    assert trapezoid["package_candidate_status"] == (
        "not_current_candidate_unsupported_policy_block"
    )


def test_cpd_paper_candidate_matrix_blocks_current_unmapped_rows(cpd_paper_report):
    report = cpd_paper_report
    plan = report["paper_package_conversion_mapped_subset_plan"]
    payload = report["paper_mapped_subset_conversion_candidate_matrix"]
    summary = payload["coverage_summary"]
    rows = payload["current_row_candidate_matrix_rows"]

    assert summary["future_family_candidate_matrix_row_count"] == 6
    assert summary["future_family_review_candidate_count"] == 3
    assert summary["excluded_family_review_row_count"] == 3
    assert summary["current_row_candidate_matrix_row_count"] == 16
    assert summary["current_package_conversion_candidate_count"] == 0
    assert summary["current_blocked_requires_policy_count"] == 16
    assert summary["package_candidate_record_count"] == 0
    assert summary["current_paper_primitive_distribution"] == {
        "trapezoidal_prism": 16,
    }
    assert summary["current_runtime_kind_distribution"] == {
        "offline_only_unmapped": 16,
    }
    assert (
        summary["current_package_conversion_candidate_count"]
        + summary["current_blocked_requires_policy_count"]
        == summary["current_row_candidate_matrix_row_count"]
    )

    plan_rows = plan["current_row_conversion_plan_rows"]
    assert len(rows) == len(plan_rows) == 16
    for row, upstream_row in zip(rows, plan_rows):
        assert row["source_conversion_plan_row_id"] == (upstream_row["conversion_plan_row_id"])
        assert row["source_policy_decision_id"] == upstream_row["source_policy_decision_id"]
        assert row["source_adapter_decision_id"] == (upstream_row["source_adapter_decision_id"])
        assert row["source_output_id"] == upstream_row["source_output_id"]
        assert row["offline_primitive_id"] == upstream_row["offline_primitive_id"]
        assert row["paper_primitive"] == "trapezoidal_prism"
        assert row["offline_runtime_kind_label"] == "offline_only_unmapped"
        assert row["input_conversion_plan_decision"] == (
            "exclude_requires_explicit_mapping_or_approximation_policy"
        )
        assert row["candidate_matrix_decision"] == "blocked_unmapped_current_rows"
        assert row["candidate_matrix_action"] == "keep_offline"
        assert row["current_package_conversion_candidate"] is False
        assert row["package_candidate_status"] == ("not_current_candidate_unsupported_policy_block")
        assert row["required_later_gate"] == (EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT)
        assert row["required_future_policy"] == (
            "explicit_mapping_or_approximation_policy_before_package_generation"
        )
        assert row["primitive_spec_generation_triggered"] is False
        assert row["collision_package_generation_triggered"] is False
        assert row["runtime_admissibility_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False


def test_cpd_paper_candidate_matrix_stays_report_only(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_conversion_candidate_matrix"]

    forbidden_keys = {
        "CollisionPackage",
        "PrimitiveSpec",
        "runtime_result",
        "usd_asset_path",
        "benchmark_metric",
        "timing",
        "surface_distance",
        "collision_quality",
    }
    assert forbidden_keys.isdisjoint(payload)
    assert payload["candidate_matrix_contract"]["primitive_spec_generation_allowed"] is False
    assert payload["candidate_matrix_contract"]["collision_package_generation_allowed"] is False
    assert payload["candidate_matrix_contract"]["newton_runtime_allowed"] is False
    assert payload["candidate_matrix_contract"]["runtime_admissibility_supported"] is False
    for row in payload["future_family_candidate_matrix_rows"]:
        assert forbidden_keys.isdisjoint(row)
    for row in payload["current_row_candidate_matrix_rows"]:
        assert forbidden_keys.isdisjoint(row)


def test_cpd_paper_records_mapped_subset_adapter_preflight_contract_gate(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_adapter_preflight_contract"]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )

    assert payload["gate_id"] == EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT
    assert payload["gate_status"] == "implemented_offline_adapter_preflight_contract_only_partial"
    assert payload["closed_gate"] == EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT
    assert payload["input_gate_id"] == EXPECTED_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX
    assert payload["next_required_gate"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT
    assert payload["decision"] == "remain_partial"
    assert (
        payload["decision_reason"]
        == "adapter_preflight_contract_complete_primitivespec_dry_run_contract_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == (
        "offline_adapter_preflight_contract_not_primitivespec_not_collision_package"
    )
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["implementation_boundary"] == (
        "offline_adapter_preflight_no_primitivespec_no_collision_package_no_newton"
    )
    assert payload["candidate_count_at_preflight"] == 0
    assert payload["preflight_action"] == "no_op_keep_offline"
    assert payload["remaining_gaps"] == EXPECTED_PREFLIGHT_REMAINING_GAPS


def test_cpd_paper_adapter_preflight_records_family_requirements(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_adapter_preflight_contract"]
    rows = {row["paper_primitive"]: row for row in payload["adapter_preflight_requirement_rows"]}

    assert list(rows) == [
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
    expected_native = {
        "oriented_bounding_box": "box",
        "sphere": "sphere",
        "capsule": "capsule",
    }
    for primitive_name, runtime_kind in expected_native.items():
        row = rows[primitive_name]
        assert row["candidate_runtime_kind"] == runtime_kind
        assert row["adapter_preflight_decision"] == "future_native_family_preflight_recorded_only"
        assert row["future_native_family_preflight_recorded"] is True
        assert row["current_row_evidence_count"] == 0
        assert row["current_package_conversion_candidate_count"] == 0
        assert row["package_generation_enabled_by_this_gate"] is False
        assert row["primitive_spec_generation_triggered"] is False
        assert row["collision_package_generation_triggered"] is False
        assert row["runtime_admissibility_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False

    for primitive_name in ("capped_cylinder", "frustum"):
        row = rows[primitive_name]
        assert row["candidate_runtime_kind"] == "offline_only_unmapped"
        assert row["adapter_preflight_decision"] == "blocked_approximation_policy_missing"
        assert row["future_native_family_preflight_recorded"] is False
        assert row["package_generation_enabled_by_this_gate"] is False

    trapezoid = rows["trapezoidal_prism"]
    assert trapezoid["candidate_runtime_kind"] == "offline_only_unmapped"
    assert trapezoid["adapter_preflight_decision"] == "noop_current_unmapped_rows_keep_offline"
    assert trapezoid["future_native_family_preflight_recorded"] is False
    assert trapezoid["current_row_evidence_count"] == 16
    assert trapezoid["current_package_conversion_candidate_count"] == 0


def test_cpd_paper_adapter_preflight_noops_current_unmapped_rows(cpd_paper_report):
    report = cpd_paper_report
    matrix = report["paper_mapped_subset_conversion_candidate_matrix"]
    payload = report["paper_mapped_subset_adapter_preflight_contract"]
    summary = payload["coverage_summary"]
    rows = payload["current_row_adapter_preflight_rows"]

    assert summary["family_preflight_requirement_row_count"] == 6
    assert summary["future_native_family_preflight_record_count"] == 3
    assert summary["blocked_family_preflight_record_count"] == 3
    assert summary["current_row_adapter_preflight_row_count"] == 16
    assert summary["current_preflight_pass_record_count"] == 0
    assert summary["current_preflight_noop_record_count"] == 16
    assert summary["current_package_conversion_candidate_count"] == 0
    assert summary["package_candidate_record_count"] == 0
    assert summary["current_paper_primitive_distribution"] == {
        "trapezoidal_prism": 16,
    }
    assert summary["current_runtime_kind_distribution"] == {
        "offline_only_unmapped": 16,
    }

    matrix_rows = matrix["current_row_candidate_matrix_rows"]
    assert len(rows) == len(matrix_rows) == 16
    for row, upstream_row in zip(rows, matrix_rows):
        assert row["source_candidate_matrix_row_id"] == (upstream_row["candidate_matrix_row_id"])
        assert (
            row["source_conversion_plan_row_id"] == (upstream_row["source_conversion_plan_row_id"])
        )
        assert row["source_policy_decision_id"] == upstream_row["source_policy_decision_id"]
        assert row["source_adapter_decision_id"] == (upstream_row["source_adapter_decision_id"])
        assert row["source_output_id"] == upstream_row["source_output_id"]
        assert row["evidence_case_id"] == upstream_row["evidence_case_id"]
        assert row["offline_primitive_id"] == upstream_row["offline_primitive_id"]
        assert row["paper_primitive"] == "trapezoidal_prism"
        assert row["offline_runtime_kind_label"] == "offline_only_unmapped"
        assert row["input_candidate_matrix_decision"] == "blocked_unmapped_current_rows"
        assert row["adapter_preflight_decision"] == "noop_keep_offline_unmapped_current_row"
        assert row["adapter_preflight_action"] == "keep_offline"
        assert row["current_package_conversion_candidate"] is False
        assert row["adapter_preflight_passed"] is False
        assert row["package_generation_enabled_by_this_gate"] is False
        assert row["required_later_gate"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT
        assert row["required_future_policy"] == upstream_row["required_future_policy"]
        assert row["primitive_spec_generation_triggered"] is False
        assert row["collision_package_generation_triggered"] is False
        assert row["runtime_admissibility_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False


def test_cpd_paper_adapter_preflight_stays_report_only(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_adapter_preflight_contract"]

    forbidden_keys = {
        "CollisionPackage",
        "PrimitiveSpec",
        "runtime_result",
        "usd_asset_path",
        "benchmark_metric",
        "timing",
        "surface_distance",
        "collision_quality",
    }
    assert forbidden_keys.isdisjoint(payload)
    assert payload["primitive_spec_generation_allowed"] is False
    assert payload["collision_package_generation_allowed"] is False
    assert payload["newton_runtime_allowed"] is False
    assert payload["runtime_admissibility_supported"] is False
    assert payload["approximation_policy_enabled"] is False
    assert payload["silent_drop_allowed"] is False
    assert payload["adapter_preflight_contract"]["primitive_spec_generation_allowed"] is False
    assert payload["adapter_preflight_contract"]["collision_package_generation_allowed"] is False
    assert payload["adapter_preflight_contract"]["newton_runtime_allowed"] is False
    assert payload["adapter_preflight_contract"]["runtime_admissibility_supported"] is False
    assert payload["adapter_preflight_contract"]["silent_drop_allowed"] is False
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    assert payload["primitive_spec_generated"] is False
    assert payload["collision_package_generated"] is False
    assert payload["runtime_admissibility_checked"] is False
    assert payload["newton_support_claimed"] is False
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
    for row in payload["adapter_preflight_requirement_rows"]:
        assert forbidden_keys.isdisjoint(row)
    for row in payload["current_row_adapter_preflight_rows"]:
        assert forbidden_keys.isdisjoint(row)


def test_cpd_paper_adapter_preflight_rejects_wrong_candidate_matrix_gate(cpd_paper_report):
    report = cpd_paper_report
    candidate_matrix = dict(report["paper_mapped_subset_conversion_candidate_matrix"])
    candidate_matrix["gate_id"] = "stale_gate"

    with pytest.raises(ValueError, match="candidate_matrix_gate_id_mismatch"):
        _paper_mapped_subset_adapter_preflight_contract_payload(candidate_matrix)


def test_cpd_paper_adapter_preflight_rejects_true_input_trigger_flags(cpd_paper_report):
    report = cpd_paper_report
    candidate_matrix = dict(report["paper_mapped_subset_conversion_candidate_matrix"])
    candidate_matrix["package_generation_triggered"] = True

    with pytest.raises(ValueError, match="input_trigger_flag_true"):
        _paper_mapped_subset_adapter_preflight_contract_payload(candidate_matrix)


def test_cpd_paper_adapter_preflight_rejects_nonzero_input_candidates(cpd_paper_report):
    report = cpd_paper_report
    candidate_matrix = dict(report["paper_mapped_subset_conversion_candidate_matrix"])
    candidate_matrix["coverage_summary"] = {
        **candidate_matrix["coverage_summary"],
        "current_package_conversion_candidate_count": 1,
    }

    with pytest.raises(ValueError, match="input_package_candidate_count_nonzero"):
        _paper_mapped_subset_adapter_preflight_contract_payload(candidate_matrix)


def test_cpd_paper_adapter_preflight_rejects_row_level_current_candidate(cpd_paper_report):
    report = cpd_paper_report
    candidate_matrix = dict(report["paper_mapped_subset_conversion_candidate_matrix"])
    current_rows = [dict(row) for row in candidate_matrix["current_row_candidate_matrix_rows"]]
    current_rows[0]["current_package_conversion_candidate"] = True
    candidate_matrix["current_row_candidate_matrix_rows"] = current_rows

    with pytest.raises(ValueError, match="input_package_candidate_count_nonzero"):
        _paper_mapped_subset_adapter_preflight_contract_payload(candidate_matrix)


def test_cpd_paper_adapter_preflight_rejects_family_level_candidate_count(cpd_paper_report):
    report = cpd_paper_report
    candidate_matrix = dict(report["paper_mapped_subset_conversion_candidate_matrix"])
    family_rows = [dict(row) for row in candidate_matrix["future_family_candidate_matrix_rows"]]
    family_rows[0]["current_package_conversion_candidate_count"] = 1
    candidate_matrix["future_family_candidate_matrix_rows"] = family_rows

    with pytest.raises(ValueError, match="input_package_candidate_count_nonzero"):
        _paper_mapped_subset_adapter_preflight_contract_payload(candidate_matrix)


def test_cpd_paper_adapter_preflight_rejects_unknown_family_decision(cpd_paper_report):
    report = cpd_paper_report
    candidate_matrix = dict(report["paper_mapped_subset_conversion_candidate_matrix"])
    family_rows = [dict(row) for row in candidate_matrix["future_family_candidate_matrix_rows"]]
    family_rows[0]["candidate_matrix_decision"] = "misspelled_decision"
    candidate_matrix["future_family_candidate_matrix_rows"] = family_rows

    with pytest.raises(ValueError, match="unknown_family_candidate_matrix_decision"):
        _paper_mapped_subset_adapter_preflight_contract_payload(candidate_matrix)


def test_cpd_paper_adapter_preflight_rejects_duplicate_input_row_ids(cpd_paper_report):
    report = cpd_paper_report
    candidate_matrix = dict(report["paper_mapped_subset_conversion_candidate_matrix"])
    current_rows = [dict(row) for row in candidate_matrix["current_row_candidate_matrix_rows"]]
    current_rows[1]["candidate_matrix_row_id"] = current_rows[0]["candidate_matrix_row_id"]
    candidate_matrix["current_row_candidate_matrix_rows"] = current_rows

    with pytest.raises(ValueError, match="duplicate_candidate_matrix_row_id"):
        _paper_mapped_subset_adapter_preflight_contract_payload(candidate_matrix)


def test_cpd_paper_records_mapped_subset_primitivespec_dry_run_contract_gate(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_primitivespec_dry_run_contract"]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )

    assert payload["gate_id"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT
    assert (
        payload["gate_status"] == "implemented_offline_primitivespec_dry_run_contract_only_partial"
    )
    assert payload["closed_gate"] == (EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT)
    assert payload["input_gate_id"] == EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT
    assert payload["next_required_gate"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "primitivespec_dry_run_contract_complete_primitivespec_validation_contract_missing"
    )
    assert payload["remaining_gaps"] == EXPECTED_PRIMITIVESPEC_REMAINING_GAPS
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == (
        "offline_primitivespec_dry_run_contract_not_primitivespec_not_collision_package"
    )
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["implementation_boundary"] == (
        "offline_primitivespec_dry_run_no_primitivespec_no_collision_package_no_newton"
    )
    assert payload["candidate_count_at_dry_run"] == 0
    assert payload["dry_run_action"] == "no_op_keep_offline"
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_PRIMITIVESPEC_REMAINING_GAPS


def test_cpd_paper_primitivespec_dry_run_records_family_requirements(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_primitivespec_dry_run_contract"]
    rows = {
        row["paper_primitive"]: row for row in payload["primitive_spec_dry_run_requirement_rows"]
    }

    assert list(rows) == [
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
    expected_native = {
        "oriented_bounding_box": "box",
        "sphere": "sphere",
        "capsule": "capsule",
    }
    expected_fields = [
        "primitive_id",
        "kind",
        "center",
        "axes",
        "dimensions",
        "frame",
        "source_faces",
        "contains_assigned_points",
        "volume",
        "weighted_volume",
        "conversion_status",
    ]
    for primitive_name, primitive_kind in expected_native.items():
        row = rows[primitive_name]
        assert row["candidate_runtime_kind"] == primitive_kind
        assert row["future_primitive_spec_kind"] == primitive_kind
        assert row["primitive_spec_dry_run_decision"] == (
            "future_native_family_primitivespec_shape_recorded_only"
        )
        assert row["future_primitive_spec_shape_recorded"] is True
        assert row["required_primitive_spec_fields"] == expected_fields
        assert row["primitive_spec_generation_triggered"] is False
        assert row["collision_package_generation_triggered"] is False
        assert row["runtime_admissibility_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False

    for primitive_name in ("capped_cylinder", "frustum"):
        row = rows[primitive_name]
        assert row["candidate_runtime_kind"] == "offline_only_unmapped"
        assert row["future_primitive_spec_kind"] is None
        assert row["primitive_spec_dry_run_decision"] == "blocked_approximation_policy_missing"
        assert row["future_primitive_spec_shape_recorded"] is False

    trapezoid = rows["trapezoidal_prism"]
    assert trapezoid["candidate_runtime_kind"] == "offline_only_unmapped"
    assert trapezoid["future_primitive_spec_kind"] is None
    assert trapezoid["primitive_spec_dry_run_decision"] == "noop_current_unmapped_rows_keep_offline"
    assert trapezoid["future_primitive_spec_shape_recorded"] is False
    assert trapezoid["current_row_evidence_count"] == 16


def test_cpd_paper_primitivespec_dry_run_noops_current_unmapped_rows(cpd_paper_report):
    report = cpd_paper_report
    preflight = report["paper_mapped_subset_adapter_preflight_contract"]
    payload = report["paper_mapped_subset_primitivespec_dry_run_contract"]
    summary = payload["coverage_summary"]
    rows = payload["current_row_primitivespec_dry_run_rows"]

    assert summary["primitive_spec_requirement_row_count"] == 6
    assert summary["future_native_primitivespec_shape_record_count"] == 3
    assert summary["blocked_primitivespec_requirement_row_count"] == 2
    assert summary["noop_primitivespec_requirement_row_count"] == 1
    assert summary["current_row_primitivespec_dry_run_row_count"] == 16
    assert summary["current_primitivespec_dry_run_pass_record_count"] == 0
    assert summary["current_primitivespec_noop_record_count"] == 16
    assert summary["primitive_spec_candidate_record_count"] == 0
    assert summary["generated_primitive_spec_record_count"] == 0
    assert summary["current_paper_primitive_distribution"] == {
        "trapezoidal_prism": 16,
    }
    assert summary["current_runtime_kind_distribution"] == {
        "offline_only_unmapped": 16,
    }

    preflight_rows = preflight["current_row_adapter_preflight_rows"]
    assert len(rows) == len(preflight_rows) == 16
    for row, upstream_row in zip(rows, preflight_rows):
        assert row["source_adapter_preflight_row_id"] == (upstream_row["adapter_preflight_row_id"])
        assert (
            row["source_candidate_matrix_row_id"]
            == (upstream_row["source_candidate_matrix_row_id"])
        )
        assert (
            row["source_conversion_plan_row_id"] == (upstream_row["source_conversion_plan_row_id"])
        )
        assert row["source_policy_decision_id"] == upstream_row["source_policy_decision_id"]
        assert row["source_adapter_decision_id"] == (upstream_row["source_adapter_decision_id"])
        assert row["source_output_id"] == upstream_row["source_output_id"]
        assert row["evidence_case_id"] == upstream_row["evidence_case_id"]
        assert row["offline_primitive_id"] == upstream_row["offline_primitive_id"]
        assert row["paper_primitive"] == "trapezoidal_prism"
        assert row["offline_runtime_kind_label"] == "offline_only_unmapped"
        assert row["input_adapter_preflight_decision"] == ("noop_keep_offline_unmapped_current_row")
        assert row["primitive_spec_dry_run_decision"] == "skip_unmapped_current_row"
        assert row["primitive_spec_dry_run_action"] == "keep_offline"
        assert row["primitive_spec_dry_run_passed"] is False
        assert row["primitive_spec_candidate"] is False
        assert row["generated_primitive_spec"] is None
        assert row["primitive_spec_generation_triggered"] is False
        assert row["collision_package_generation_triggered"] is False
        assert row["runtime_admissibility_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False


def test_cpd_paper_primitivespec_dry_run_stays_report_only(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_primitivespec_dry_run_contract"]

    forbidden_keys = {
        "CollisionPackage",
        "PrimitiveSpec",
        "runtime_result",
        "usd_asset_path",
        "benchmark_metric",
        "timing",
        "surface_distance",
        "collision_quality",
    }
    assert forbidden_keys.isdisjoint(payload)
    assert payload["primitive_spec_generation_allowed"] is False
    assert payload["collision_package_generation_allowed"] is False
    assert payload["newton_runtime_allowed"] is False
    assert payload["runtime_admissibility_supported"] is False
    assert payload["approximation_policy_enabled"] is False
    assert payload["silent_drop_allowed"] is False
    assert payload["primitive_spec_dry_run_contract"]["primitive_spec_generation_allowed"] is False
    assert (
        payload["primitive_spec_dry_run_contract"]["collision_package_generation_allowed"] is False
    )
    assert payload["primitive_spec_generated"] is False
    assert payload["collision_package_generated"] is False
    assert payload["runtime_admissibility_checked"] is False
    assert payload["newton_support_claimed"] is False
    assert payload["approximation_policy_applied"] is False
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
    assert payload["collision_quality_measured"] is False
    assert payload["deployment_or_certification_claimed"] is False
    for row in payload["primitive_spec_dry_run_requirement_rows"]:
        assert forbidden_keys.isdisjoint(row)
    for row in payload["current_row_primitivespec_dry_run_rows"]:
        assert forbidden_keys.isdisjoint(row)


def test_cpd_paper_primitivespec_dry_run_rejects_wrong_input_gate(cpd_paper_report):
    report = cpd_paper_report
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    preflight["gate_id"] = "stale_gate"

    with pytest.raises(
        ValueError,
        match="primitivespec_dry_run_input_gate_id_mismatch",
    ):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_true_input_trigger_flags(cpd_paper_report):
    report = cpd_paper_report
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    preflight["package_generation_triggered"] = True

    with pytest.raises(ValueError, match="input_trigger_flag_true"):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_nonzero_input_candidates(cpd_paper_report):
    report = cpd_paper_report
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    preflight["candidate_count_at_preflight"] = 1

    with pytest.raises(
        ValueError,
        match="input_primitivespec_candidate_count_nonzero",
    ):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_preflight_pass_count(cpd_paper_report):
    report = cpd_paper_report
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    preflight["coverage_summary"] = {
        **preflight["coverage_summary"],
        "current_preflight_pass_record_count": 1,
    }

    with pytest.raises(ValueError, match="input_preflight_pass_count_nonzero"):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_row_level_preflight_pass(cpd_paper_report):
    report = cpd_paper_report
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    current_rows = [dict(row) for row in preflight["current_row_adapter_preflight_rows"]]
    current_rows[0]["adapter_preflight_passed"] = True
    preflight["current_row_adapter_preflight_rows"] = current_rows

    with pytest.raises(ValueError, match="input_preflight_pass_count_nonzero"):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_row_level_candidate(cpd_paper_report):
    report = cpd_paper_report
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    current_rows = [dict(row) for row in preflight["current_row_adapter_preflight_rows"]]
    current_rows[0]["current_package_conversion_candidate"] = True
    preflight["current_row_adapter_preflight_rows"] = current_rows

    with pytest.raises(
        ValueError,
        match="input_primitivespec_candidate_count_nonzero",
    ):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_family_real_usd_flag(cpd_paper_report):
    report = cpd_paper_report
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    family_rows = [dict(row) for row in preflight["adapter_preflight_requirement_rows"]]
    family_rows[0]["real_usd_loaded"] = True
    preflight["adapter_preflight_requirement_rows"] = family_rows

    with pytest.raises(ValueError, match="input_trigger_flag_true:real_usd_loaded"):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_current_benchmark_flag(cpd_paper_report):
    report = cpd_paper_report
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    current_rows = [dict(row) for row in preflight["current_row_adapter_preflight_rows"]]
    current_rows[0]["benchmark_run"] = True
    preflight["current_row_adapter_preflight_rows"] = current_rows

    with pytest.raises(ValueError, match="input_trigger_flag_true:benchmark_run"):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_duplicate_preflight_row_ids(cpd_paper_report):
    report = cpd_paper_report
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    current_rows = [dict(row) for row in preflight["current_row_adapter_preflight_rows"]]
    current_rows[1]["adapter_preflight_row_id"] = current_rows[0]["adapter_preflight_row_id"]
    preflight["current_row_adapter_preflight_rows"] = current_rows

    with pytest.raises(ValueError, match="duplicate_adapter_preflight_row_id"):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_unknown_family_decision(cpd_paper_report):
    report = cpd_paper_report
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    family_rows = [dict(row) for row in preflight["adapter_preflight_requirement_rows"]]
    family_rows[0]["adapter_preflight_decision"] = "misspelled_decision"
    preflight["adapter_preflight_requirement_rows"] = family_rows

    with pytest.raises(ValueError, match="unknown_adapter_preflight_family_decision"):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_missing_current_source_id(cpd_paper_report):
    report = cpd_paper_report
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    current_rows = [dict(row) for row in preflight["current_row_adapter_preflight_rows"]]
    current_rows[0].pop("source_output_id")
    preflight["current_row_adapter_preflight_rows"] = current_rows

    with pytest.raises(ValueError, match="missing_current_row_source_id"):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_blank_current_source_id(cpd_paper_report):
    report = cpd_paper_report
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    current_rows = [dict(row) for row in preflight["current_row_adapter_preflight_rows"]]
    current_rows[0]["source_output_id"] = " "
    preflight["current_row_adapter_preflight_rows"] = current_rows

    with pytest.raises(ValueError, match="missing_current_row_source_id"):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_wrong_required_later_gate(cpd_paper_report):
    report = cpd_paper_report
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    current_rows = [dict(row) for row in preflight["current_row_adapter_preflight_rows"]]
    current_rows[0]["required_later_gate"] = "stale_gate"
    preflight["current_row_adapter_preflight_rows"] = current_rows

    with pytest.raises(ValueError, match="current_row_required_later_gate_mismatch"):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_records_mapped_subset_primitivespec_validation_contract_gate(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_primitivespec_validation_contract"]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert payload["gate_id"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT
    assert payload["gate_status"] == (
        "implemented_offline_primitivespec_validation_contract_only_partial"
    )
    assert payload["closed_gate"] == (EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT)
    assert payload["input_gate_id"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT
    assert (
        payload["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "primitivespec_validation_contract_complete_"
        "primitivespec_generation_preflight_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "offline_primitivespec_validation_contract_not_primitivespec_not_collision_package"
    )
    assert payload["validated_primitive_spec_candidate_count"] == 0
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_VALIDATION_REMAINING_GAPS


def test_cpd_paper_primitivespec_validation_records_family_requirements(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_primitivespec_validation_contract"]
    rows = {
        row["paper_primitive"]: row for row in payload["primitive_spec_validation_requirement_rows"]
    }

    assert list(rows) == [
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
    assert (
        rows["oriented_bounding_box"]["primitive_spec_validation_decision"]
        == "future_native_family_primitivespec_shape_requirement_validated"
    )
    assert rows["oriented_bounding_box"]["validated_future_primitive_spec_kind"] == "box"
    assert rows["sphere"]["validated_future_primitive_spec_kind"] == "sphere"
    assert rows["capsule"]["validated_future_primitive_spec_kind"] == "capsule"
    assert rows["capped_cylinder"]["primitive_spec_validation_decision"] == (
        "blocked_approximation_policy_validation_recorded"
    )
    assert rows["frustum"]["primitive_spec_validation_decision"] == (
        "blocked_approximation_policy_validation_recorded"
    )
    assert rows["trapezoidal_prism"]["primitive_spec_validation_decision"] == (
        "noop_unmapped_family_validation_recorded"
    )
    for primitive_name in ("capped_cylinder", "frustum", "trapezoidal_prism"):
        assert rows[primitive_name]["validated_future_primitive_spec_kind"] is None
        assert rows[primitive_name]["primitive_spec_generation_triggered"] is False
        assert rows[primitive_name]["collision_package_generation_triggered"] is False
        assert rows[primitive_name]["runtime_admissibility_triggered"] is False
        assert rows[primitive_name]["newton_runtime_triggered"] is False
        assert rows[primitive_name]["real_usd_triggered"] is False
        assert rows[primitive_name]["benchmark_triggered"] is False


def test_cpd_paper_primitivespec_validation_noops_current_unmapped_rows(cpd_paper_report):
    report = cpd_paper_report
    dry_run = report["paper_mapped_subset_primitivespec_dry_run_contract"]
    payload = report["paper_mapped_subset_primitivespec_validation_contract"]
    summary = payload["coverage_summary"]
    rows = payload["current_row_primitivespec_validation_rows"]

    assert summary["primitive_spec_validation_requirement_row_count"] == 6
    assert summary["future_native_primitivespec_shape_validation_count"] == 3
    assert summary["blocked_primitivespec_validation_requirement_count"] == 2
    assert summary["noop_primitivespec_validation_requirement_count"] == 1
    assert summary["current_row_primitivespec_validation_row_count"] == 16
    assert summary["current_primitivespec_validation_pass_record_count"] == 0
    assert summary["current_primitivespec_validation_noop_record_count"] == 16
    assert summary["validated_primitive_spec_candidate_record_count"] == 0
    assert summary["generated_primitive_spec_record_count"] == 0

    dry_run_rows = dry_run["current_row_primitivespec_dry_run_rows"]
    assert len(rows) == len(dry_run_rows) == 16
    for row, upstream_row in zip(rows, dry_run_rows):
        assert (
            row["source_primitivespec_dry_run_row_id"]
            == (upstream_row["primitive_spec_dry_run_row_id"])
        )
        assert (
            row["source_adapter_preflight_row_id"]
            == (upstream_row["source_adapter_preflight_row_id"])
        )
        assert (
            row["source_candidate_matrix_row_id"]
            == (upstream_row["source_candidate_matrix_row_id"])
        )
        assert (
            row["source_conversion_plan_row_id"] == (upstream_row["source_conversion_plan_row_id"])
        )
        assert row["source_policy_decision_id"] == upstream_row["source_policy_decision_id"]
        assert row["source_adapter_decision_id"] == (upstream_row["source_adapter_decision_id"])
        assert row["source_output_id"] == upstream_row["source_output_id"]
        assert row["evidence_case_id"] == upstream_row["evidence_case_id"]
        assert row["offline_primitive_id"] == upstream_row["offline_primitive_id"]
        assert row["primitive_spec_validation_decision"] == ("skip_unmapped_current_row_validated")
        assert row["primitive_spec_validation_action"] == "keep_offline"
        assert row["primitive_spec_validation_passed"] is False
        assert row["primitive_spec_candidate"] is False
        assert row["generated_primitive_spec"] is None
        assert row["silent_drop_detected"] is False
        assert row["primitive_spec_generation_triggered"] is False
        assert row["collision_package_generation_triggered"] is False
        assert row["runtime_admissibility_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False


def test_cpd_paper_primitivespec_validation_stays_report_only(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_primitivespec_validation_contract"]

    forbidden_keys = {
        "CollisionPackage",
        "PrimitiveSpec",
        "runtime_result",
        "usd_asset_path",
        "benchmark_metric",
        "timing",
        "surface_distance",
        "collision_quality",
    }
    assert forbidden_keys.isdisjoint(payload)
    assert payload["primitive_spec_generation_allowed"] is False
    assert payload["collision_package_generation_allowed"] is False
    assert payload["newton_runtime_allowed"] is False
    assert payload["runtime_admissibility_supported"] is False
    assert payload["approximation_policy_enabled"] is False
    assert payload["silent_drop_allowed"] is False
    assert (
        payload["primitive_spec_validation_contract"]["primitive_spec_generation_allowed"] is False
    )
    assert (
        payload["primitive_spec_validation_contract"]["collision_package_generation_allowed"]
        is False
    )
    assert payload["primitive_spec_generated"] is False
    assert payload["collision_package_generated"] is False
    assert payload["runtime_admissibility_checked"] is False
    assert payload["newton_support_claimed"] is False
    assert payload["approximation_policy_applied"] is False
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
    assert payload["collision_quality_measured"] is False
    assert payload["deployment_or_certification_claimed"] is False
    for row in payload["primitive_spec_validation_requirement_rows"]:
        assert forbidden_keys.isdisjoint(row)
    for row in payload["current_row_primitivespec_validation_rows"]:
        assert forbidden_keys.isdisjoint(row)


def test_cpd_paper_primitivespec_validation_rejects_wrong_input_gate(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    dry_run["gate_id"] = "stale_gate"

    with pytest.raises(
        ValueError,
        match="primitivespec_validation_input_gate_id_mismatch",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_true_input_trigger_flags(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    dry_run["newton_runtime_triggered"] = True

    with pytest.raises(ValueError, match="validation_input_trigger_flag_true"):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_nonzero_input_candidates(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    dry_run["candidate_count_at_dry_run"] = 1

    with pytest.raises(
        ValueError,
        match="validation_input_candidate_count_nonzero",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_required_field_mismatch(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    contract = dict(dry_run["primitive_spec_dry_run_contract"])
    contract["required_primitive_spec_fields"] = contract["required_primitive_spec_fields"][:-1]
    dry_run["primitive_spec_dry_run_contract"] = contract

    with pytest.raises(ValueError, match="validation_required_fields_mismatch"):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_allowed_kind_mismatch(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    contract = dict(dry_run["primitive_spec_dry_run_contract"])
    contract["allowed_future_runtime_kinds"] = [
        *contract["allowed_future_runtime_kinds"],
        "cylinder",
    ]
    dry_run["primitive_spec_dry_run_contract"] = contract

    with pytest.raises(ValueError, match="validation_allowed_runtime_kinds_mismatch"):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_coverage_count_mismatch(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    coverage = dict(dry_run["coverage_summary"])
    coverage["current_row_primitivespec_dry_run_row_count"] = 15
    dry_run["coverage_summary"] = coverage

    with pytest.raises(ValueError, match="validation_coverage_count_mismatch"):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_duplicate_dry_run_row_ids(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    current_rows = [dict(row) for row in dry_run["current_row_primitivespec_dry_run_rows"]]
    current_rows[1]["primitive_spec_dry_run_row_id"] = current_rows[0][
        "primitive_spec_dry_run_row_id"
    ]
    dry_run["current_row_primitivespec_dry_run_rows"] = current_rows

    with pytest.raises(ValueError, match="duplicate_primitivespec_dry_run_row_id"):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_unknown_family_decision(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    requirement_rows = [dict(row) for row in dry_run["primitive_spec_dry_run_requirement_rows"]]
    requirement_rows[0]["primitive_spec_dry_run_decision"] = "misspelled_decision"
    dry_run["primitive_spec_dry_run_requirement_rows"] = requirement_rows

    with pytest.raises(
        ValueError,
        match="unknown_primitivespec_dry_run_family_decision",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_missing_future_native_kind(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    requirement_rows = [dict(row) for row in dry_run["primitive_spec_dry_run_requirement_rows"]]
    requirement_rows[0]["future_primitive_spec_kind"] = None
    dry_run["primitive_spec_dry_run_requirement_rows"] = requirement_rows

    with pytest.raises(ValueError, match="future_native_primitivespec_kind_missing"):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_mutated_family_semantics(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    requirement_rows = [dict(row) for row in dry_run["primitive_spec_dry_run_requirement_rows"]]
    capped_cylinder = next(
        row for row in requirement_rows if row["paper_primitive"] == "capped_cylinder"
    )
    capped_cylinder["primitive_spec_dry_run_decision"] = (
        "future_native_family_primitivespec_shape_recorded_only"
    )
    capped_cylinder["candidate_runtime_kind"] = "box"
    capped_cylinder["future_primitive_spec_kind"] = "box"
    dry_run["primitive_spec_dry_run_requirement_rows"] = requirement_rows

    with pytest.raises(
        ValueError,
        match="validation_family_contract_mismatch:capped_cylinder",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_duplicate_family_identity(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    requirement_rows = [dict(row) for row in dry_run["primitive_spec_dry_run_requirement_rows"]]
    requirement_rows[1]["paper_primitive"] = "oriented_bounding_box"
    dry_run["primitive_spec_dry_run_requirement_rows"] = requirement_rows

    with pytest.raises(
        ValueError,
        match="validation_family_primitive_sequence_mismatch",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_future_mapping_label_mismatch(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    requirement_rows = [dict(row) for row in dry_run["primitive_spec_dry_run_requirement_rows"]]
    requirement_rows[0]["candidate_runtime_kind"] = "offline_only_unmapped"
    dry_run["primitive_spec_dry_run_requirement_rows"] = requirement_rows

    with pytest.raises(
        ValueError,
        match="validation_future_mapping_label_mismatch:oriented_bounding_box",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_blank_requirement_source_id(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    requirement_rows = [dict(row) for row in dry_run["primitive_spec_dry_run_requirement_rows"]]
    requirement_rows[0]["source_adapter_preflight_row_id"] = ""
    dry_run["primitive_spec_dry_run_requirement_rows"] = requirement_rows

    with pytest.raises(
        ValueError,
        match="validation_missing_requirement_row_source_id",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_whitespace_requirement_source_id(
    cpd_paper_report,
):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    requirement_rows = [dict(row) for row in dry_run["primitive_spec_dry_run_requirement_rows"]]
    requirement_rows[0]["source_adapter_preflight_row_id"] = "   "
    dry_run["primitive_spec_dry_run_requirement_rows"] = requirement_rows

    with pytest.raises(
        ValueError,
        match="validation_missing_requirement_row_source_id",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_blank_requirement_row_id(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    requirement_rows = [dict(row) for row in dry_run["primitive_spec_dry_run_requirement_rows"]]
    requirement_rows[0]["primitive_spec_dry_run_row_id"] = " "
    dry_run["primitive_spec_dry_run_requirement_rows"] = requirement_rows

    with pytest.raises(
        ValueError,
        match="validation_missing_primitivespec_dry_run_row_id",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_requirement_real_usd_flag(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    requirement_rows = [dict(row) for row in dry_run["primitive_spec_dry_run_requirement_rows"]]
    requirement_rows[0]["real_usd_loaded"] = True
    dry_run["primitive_spec_dry_run_requirement_rows"] = requirement_rows

    with pytest.raises(
        ValueError,
        match="validation_input_trigger_flag_true:real_usd_loaded",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_blank_current_source_id(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    current_rows = [dict(row) for row in dry_run["current_row_primitivespec_dry_run_rows"]]
    current_rows[0]["source_output_id"] = ""
    dry_run["current_row_primitivespec_dry_run_rows"] = current_rows

    with pytest.raises(
        ValueError,
        match="validation_missing_current_row_source_id",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_whitespace_current_source_id(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    current_rows = [dict(row) for row in dry_run["current_row_primitivespec_dry_run_rows"]]
    current_rows[0]["source_output_id"] = " "
    dry_run["current_row_primitivespec_dry_run_rows"] = current_rows

    with pytest.raises(
        ValueError,
        match="validation_missing_current_row_source_id",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_blank_current_row_id(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    current_rows = [dict(row) for row in dry_run["current_row_primitivespec_dry_run_rows"]]
    current_rows[0]["primitive_spec_dry_run_row_id"] = ""
    dry_run["current_row_primitivespec_dry_run_rows"] = current_rows

    with pytest.raises(
        ValueError,
        match="validation_missing_primitivespec_dry_run_row_id",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_current_benchmark_flag(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    current_rows = [dict(row) for row in dry_run["current_row_primitivespec_dry_run_rows"]]
    current_rows[0]["benchmark_run"] = True
    dry_run["current_row_primitivespec_dry_run_rows"] = current_rows

    with pytest.raises(
        ValueError,
        match="validation_input_trigger_flag_true:benchmark_run",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_generated_collision_package_count(
    cpd_paper_report,
):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    dry_run["generated_collision_package_count"] = 1

    with pytest.raises(
        ValueError,
        match="validation_input_generated_collision_package_nonzero",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_row_level_pass(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    current_rows = [dict(row) for row in dry_run["current_row_primitivespec_dry_run_rows"]]
    current_rows[0]["primitive_spec_dry_run_passed"] = True
    dry_run["current_row_primitivespec_dry_run_rows"] = current_rows

    with pytest.raises(ValueError, match="validation_input_pass_count_nonzero"):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_row_level_candidate(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    current_rows = [dict(row) for row in dry_run["current_row_primitivespec_dry_run_rows"]]
    current_rows[0]["primitive_spec_candidate"] = True
    dry_run["current_row_primitivespec_dry_run_rows"] = current_rows

    with pytest.raises(
        ValueError,
        match="validation_input_candidate_count_nonzero",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_generated_spec(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    current_rows = [dict(row) for row in dry_run["current_row_primitivespec_dry_run_rows"]]
    current_rows[0]["generated_primitive_spec"] = {"kind": "box"}
    dry_run["current_row_primitivespec_dry_run_rows"] = current_rows

    with pytest.raises(
        ValueError,
        match="validation_input_generated_spec_nonzero",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_missing_current_source_id(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    current_rows = [dict(row) for row in dry_run["current_row_primitivespec_dry_run_rows"]]
    current_rows[0].pop("source_output_id")
    dry_run["current_row_primitivespec_dry_run_rows"] = current_rows

    with pytest.raises(
        ValueError,
        match="validation_missing_current_row_source_id",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_wrong_required_later_gate(cpd_paper_report):
    report = cpd_paper_report
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    current_rows = [dict(row) for row in dry_run["current_row_primitivespec_dry_run_rows"]]
    current_rows[0]["required_later_gate"] = "stale_gate"
    dry_run["current_row_primitivespec_dry_run_rows"] = current_rows

    with pytest.raises(
        ValueError,
        match="validation_current_row_required_later_gate_mismatch",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)
