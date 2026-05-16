import json
from math import isfinite, pi, sqrt

from primitive_collision_compiler.baselines.cpd_like.primitives import SUPPORTED_PRIMITIVES
from primitive_collision_compiler.baselines.cpd_paper.offline import (
    CPD_PAPER_OFFLINE_CLAIM_BOUNDARY,
    build_cpd_paper_offline_report,
)


def test_cpd_paper_offline_report_failure_labels_point_to_obb_sphere_fit_gap():
    report = build_cpd_paper_offline_report()

    assert report["failure_labels"] == ["paper_obb_sphere_fit_faithfulness_missing"]


def test_cpd_paper_offline_report_next_gate_is_obb_sphere_fit_audit():
    report = build_cpd_paper_offline_report()

    assert report["next_required_gate"] == "paper_obb_sphere_fit_faithfulness_audit"


def _assert_intake_case(case, *, arity, generated_triangles):
    expected_face_ids = list(range(len(generated_triangles)))
    expected_remap = [
        {
            "source_face_id": 0,
            "source_face_arity": arity,
            "source_vertex_ids": list(range(arity)),
            "generated_triangle_face_ids": expected_face_ids,
            "generated_triangle_vertex_ids": [list(triangle) for triangle in generated_triangles],
        }
    ]
    expected_preconditions = [
        "planar",
        "convex",
        "non_degenerate",
        "consistently_wound",
    ]

    source_mesh = case["source_mesh"]
    assert source_mesh["face_arity_policy"] == (
        "fan_triangulate_non_triangle_faces_preserve_source_face_remap"
    )
    assert source_mesh["source_face_count"] == 1
    assert source_mesh["source_face_arities"] == [arity]
    assert source_mesh["triangulated_face_count"] == len(generated_triangles)
    assert source_mesh["executable_triangle_face_count"] == len(generated_triangles)
    assert source_mesh["face_count"] == len(generated_triangles)
    assert source_mesh["executable_triangle_faces"] == [
        list(triangle) for triangle in generated_triangles
    ]
    assert source_mesh["source_face_remap"] == expected_remap
    for remap in source_mesh["source_face_remap"]:
        for generated_face_id, generated_triangle in zip(
            remap["generated_triangle_face_ids"],
            remap["generated_triangle_vertex_ids"],
            strict=True,
        ):
            assert source_mesh["executable_triangle_faces"][generated_face_id] == generated_triangle
    assert source_mesh["operator_ownership_policy"] == (
        "triangulated_subfaces_summed_to_source_face"
    )
    assert source_mesh["source_face_preconditions"] == expected_preconditions

    intake_audit = case["mesh_intake_policy_audit"]
    assert intake_audit["audit_scope"] == "polygon_quad_source_face_intake_policy_fixture"
    assert intake_audit["source_face_count"] == source_mesh["source_face_count"]
    assert intake_audit["source_face_arities"] == source_mesh["source_face_arities"]
    assert intake_audit["triangulated_face_count"] == source_mesh["triangulated_face_count"]
    assert intake_audit["executable_triangle_face_count"] == source_mesh[
        "executable_triangle_face_count"
    ]
    assert intake_audit["source_face_remap"] == source_mesh["source_face_remap"]
    assert intake_audit["source_face_preconditions"] == expected_preconditions
    assert intake_audit["source_face_policy"] == (
        "preserve_source_face_id_after_fan_triangulation"
    )
    assert intake_audit["triangulation_policy"] == "fan_from_first_vertex"
    assert intake_audit["operator_ownership_policy"] == (
        "triangulated_subfaces_summed_to_source_face"
    )
    assert intake_audit["normal_policy"] == (
        "triangle_normals_area_weighted_after_fan_triangulation"
    )
    assert intake_audit["tangent_policy"] == (
        "triangle_edge_tangents_area_weighted_after_fan_triangulation"
    )
    assert intake_audit["package_generation_triggered"] is False
    assert intake_audit["newton_runtime_triggered"] is False
    assert intake_audit["real_usd_triggered"] is False
    assert intake_audit["benchmark_triggered"] is False

    operator_audit = case["operator_audit"]
    assert operator_audit["face_scope"] == "triangle_subfaces_from_source_face"
    assert operator_audit["source_face_operator_aggregates"][0]["source_face_id"] == 0
    assert operator_audit["source_face_operator_aggregates"][0][
        "generated_triangle_face_ids"
    ] == expected_face_ids
    expected_q = [
        [
            sum(face["q_matrix"][row][col] for face in operator_audit["faces"])
            for col in range(3)
        ]
        for row in range(3)
    ]
    assert operator_audit["source_face_operator_aggregates"][0]["q_matrix"] == expected_q
    assert operator_audit["merged_group"]["source_faces"] == [0]
    assert operator_audit["merged_group"]["generated_triangle_face_ids"] == expected_face_ids
    assert operator_audit["merged_group"]["source_face_ids"] == [0]
    assert case["primitive_fit_audit"]["source_faces"] == [0]
    assert case["primitive_fit_audit"]["generated_triangle_face_ids"] == expected_face_ids
    assert case["primitive_fit_audit"]["source_face_ids"] == [0]


def test_cpd_paper_offline_report_records_polygon_quad_intake_policy():
    report = build_cpd_paper_offline_report()
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


def test_cpd_paper_offline_report_covers_first_toy_slice():
    report = build_cpd_paper_offline_report()

    assert report["stage"] == "cpd_paper_offline_report"
    assert report["status"] == "partial"
    assert report["report_generation_status"] == "smoke_passed"
    assert report["claim_boundary"] == CPD_PAPER_OFFLINE_CLAIM_BOUNDARY
    assert report["package_generation_triggered"] is False
    assert report["newton_runtime_triggered"] is False
    assert report["real_usd_triggered"] is False
    assert report["benchmark_triggered"] is False
    assert report["paper_faithful_offline_supported"] is False
    assert report["paper_faithfulness"]["status"] == "partial"
    assert report["source_scope"] == "synthetic_toy_fixtures_only"
    assert report["failure_labels"] == ["paper_obb_sphere_fit_faithfulness_missing"]
    assert report["next_required_gate"] == "paper_obb_sphere_fit_faithfulness_audit"
    assert "priority_queue_trace_audit_topology_only" in report["paper_faithfulness"][
        "implemented_fixture_scope"
    ]
    assert "component_pair_edge_insertion_audit_threshold_disabled" in report[
        "paper_faithfulness"
    ]["implemented_fixture_scope"]
    assert "component_pair_threshold_blocking_audit" in report["paper_faithfulness"][
        "implemented_fixture_scope"
    ]
    assert "postprocess_enclosed_primitive_culling_audit" in report[
        "paper_faithfulness"
    ]["implemented_fixture_scope"]
    assert "paper_polygon_quad_intake_policy_audit" in report[
        "paper_faithfulness"
    ]["implemented_fixture_scope"]

    cases = {case["case_id"]: case for case in report["cases"]}
    assert set(cases) == {
        "paper_single_box",
        "paper_two_face_merge",
        "paper_three_face_chain",
        "paper_disconnected_components",
        "paper_component_pair_threshold_blocked",
        "paper_frustum_like",
        "paper_trapezoid_prism_like",
        "paper_nested_primitive",
        "paper_quad_face_intake",
        "paper_polygon_face_intake",
    }
    assert all(case["package_generation_triggered"] is False for case in cases.values())

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
        "frustum",
        "trapezoidal_prism",
    }
    box = [
        row
        for row in single_box["primitive_fit_audit"]["candidates"]
        if row["paper_primitive"] == "oriented_bounding_box"
    ][0]
    assert box["implementation_status"] == "current_surrogate_not_paper_faithful"
    assert box["fit_model"] == "current_cpd_like_surrogate_fit"
    assert box["primitive_parameter_lower_clamp"] == 1e-6
    capsule = [
        row
        for row in single_box["primitive_fit_audit"]["candidates"]
        if row["paper_primitive"] == "capsule"
    ][0]
    assert capsule["implementation_status"] == "paper_shaped_offline_fit_audit"
    assert capsule["fit_model"] == "paper_capsule_min_volume_over_axes_with_spherical_cap_height"
    assert capsule["axis_selection_policy"] == "min_volume_capsule_axis"
    assert capsule["newton_runtime_kind"] == "capsule"
    assert capsule["contains_assigned_points"] is True
    assert capsule["fit_failure_reason"] is None
    capsule_dims = capsule["dimensions"]
    assert capsule_dims["axis_selection_policy"] == "min_volume_capsule_axis"
    assert capsule_dims["volume_formula"] == "pi*r^2*h + 4/3*pi*r^3"
    assert len(capsule_dims["paper_capsule_axis_candidates"]) == 3
    capsule_axis_volumes = [
        row["capsule_volume"]
        for row in capsule_dims["paper_capsule_axis_candidates"]
    ]
    capsule_selected_axis = capsule_dims["selected_axis_index"]
    capsule_selected_axis_row = [
        row
        for row in capsule_dims["paper_capsule_axis_candidates"]
        if row["axis_index"] == capsule_selected_axis
    ][0]
    assert capsule_selected_axis_row["capsule_volume"] == min(capsule_axis_volumes)
    assert capsule_selected_axis_row["capsule_volume"] == capsule["volume"]
    assert capsule_selected_axis_row["contains_assigned_points"] is True
    single_box_points = [
        [0.0, 0.0, 0.0],
        [2.0, 0.0, 0.0],
        [2.0, 1.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 0.5],
        [2.0, 0.0, 0.5],
        [2.0, 1.0, 0.5],
        [0.0, 1.0, 0.5],
    ]
    axis_point = box["center"]
    for candidate in capsule_dims["paper_capsule_axis_candidates"]:
        axis = capsule["axes"][candidate["axis_index"]]
        paper_heights = []
        for point in single_box_points:
            relative = [point[index] - axis_point[index] for index in range(3)]
            projected = sum(relative[index] * axis[index] for index in range(3))
            radial = [
                relative[index] - projected * axis[index]
                for index in range(3)
            ]
            radial_distance_squared = sum(value * value for value in radial)
            cap_allowance = sqrt(
                max(candidate["radius"] ** 2 - radial_distance_squared, 0.0)
            )
            paper_heights.append(projected - cap_allowance)
        assert abs(candidate["paper_height_min"] - min(paper_heights)) < 1e-7
        assert abs(candidate["paper_height_max"] - max(paper_heights)) < 1e-7
    expected_capsule_volume = (
        pi * capsule_dims["radius"] ** 2 * capsule_dims["height"]
        + (4.0 / 3.0) * pi * capsule_dims["radius"] ** 3
    )
    assert abs(capsule["volume"] - expected_capsule_volume) < 1e-9
    assert abs(capsule["weighted_volume"] - capsule["volume"]) < 1e-9
    capped = [
        row
        for row in single_box["primitive_fit_audit"]["candidates"]
        if row["paper_primitive"] == "capped_cylinder"
    ][0]
    assert capped["implementation_status"] == "paper_shaped_offline_fit_audit"
    assert capped["fit_model"] == "paper_flat_capped_cylinder_min_volume_over_axes"
    assert capped["newton_runtime_kind"] == "offline_only_unmapped"
    assert capped["contains_assigned_points"] is True
    assert capped["fit_failure_reason"] is None
    capped_dims = capped["dimensions"]
    assert capped_dims["cap_model"] == "flat_caps"
    assert capped_dims["axis_selection_policy"] == "min_volume_flat_cylinder_axis"
    assert len(capped_dims["flat_cylinder_axis_candidates"]) == 3
    capped_axis_volumes = [
        row["flat_cylinder_volume"]
        for row in capped_dims["flat_cylinder_axis_candidates"]
    ]
    capped_selected_axis = capped_dims["selected_axis_index"]
    capped_selected_axis_row = [
        row
        for row in capped_dims["flat_cylinder_axis_candidates"]
        if row["axis_index"] == capped_selected_axis
    ][0]
    assert capped_selected_axis_row["flat_cylinder_volume"] == min(capped_axis_volumes)
    assert abs(capped["volume"] - pi * capped_dims["radius"] ** 2 * capped_dims["height"]) < 1e-9
    assert abs(capped["weighted_volume"] - capped["volume"] * 1.05) < 1e-9
    assert single_box["primitive_fit_audit"]["missing_paper_primitives"] == []

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
    merge_frustum = [
        row
        for row in merge_case["primitive_fit_audit"]["candidates"]
        if row["paper_primitive"] == "frustum"
    ][0]
    assert merge_frustum["contains_assigned_points"] is True
    assert merge_frustum["fit_failure_reason"] is None

    queue_case = cases["paper_three_face_chain"]
    trace = queue_case["collapse_trace"]
    assert trace["trace_scope"] == "topology_priority_queue_trace_fixture"
    assert trace["priority_queue_policy"] == "paper_greedy_min_weighted_priority_cost"
    assert trace["target_primitive_count"] == 1
    assert trace["excess_volume_threshold"] == "default_inf"
    assert trace["threshold_policy"] == "disabled"
    assert trace["component_pair_edge_policy"] == "disabled"
    assert trace["component_pair_edge_insertion_triggered"] is False
    assert trace["topology_queue_exhausted_before_component_pair_insertion"] is False
    assert trace["component_pair_candidate_count"] == 0
    assert trace["component_pair_candidate_cap"] == "disabled"
    assert trace["initial_active_groups"] == [[0], [1], [2]]
    assert trace["initial_edge_count"] == 2
    assert trace["accepted_merge_count"] == 2
    assert trace["stale_entry_skipped_count"] >= 1
    assert trace["blocked_merge_count"] == 0
    assert trace["stop_reason"] == "target_count_reached"
    assert trace["final_active_groups"] == [[0, 1, 2]]
    assert trace["package_generation_triggered"] is False
    assert trace["newton_runtime_triggered"] is False
    assert trace["real_usd_triggered"] is False
    assert trace["benchmark_triggered"] is False
    events = trace["events"]
    accepted_events = [event for event in events if event["accepted"] is True]
    stale_events = [event for event in events if event["stale_entry"] is True]
    assert len(accepted_events) == 2
    assert stale_events
    assert [
        (
            event["event_kind"],
            event["source_faces_left"],
            event["source_faces_right"],
            event["accepted"],
            event["stale_entry"],
            event.get("resulting_source_faces"),
        )
        for event in events
    ] == [
        ("accepted_merge", [0], [1], True, False, [0, 1]),
        ("eager_stale_prune", [1], [2], False, True, None),
        ("accepted_merge", [0, 1], [2], True, False, [0, 1, 2]),
    ]
    for event in events:
        assert "event_kind" in event
        assert "paper_base_cost" in event
        assert "weighted_priority_cost" in event
        assert "queue_key" in event
        assert "source_faces_left" in event
        assert "source_faces_right" in event
        assert event["edge_source"] == "topology"
        assert "stale_entry" in event
        assert "accepted" in event
        assert event["blocked"] is False
        assert "active_primitive_count_before" in event
        assert "active_primitive_count_after" in event
        assert "updated_neighbor_insertion_count" in event
        if event["accepted"]:
            assert "resulting_source_faces" in event
    assert accepted_events[-1]["resulting_source_faces"] == [0, 1, 2]
    assert {event["edge_source"] for event in events} == {"topology"}

    disconnected_case = cases["paper_disconnected_components"]
    disconnected_trace = disconnected_case["collapse_trace"]
    assert disconnected_trace["trace_scope"] == "component_pair_priority_queue_trace_fixture"
    assert disconnected_trace["priority_queue_policy"] == "paper_greedy_min_weighted_priority_cost"
    assert disconnected_trace["target_primitive_count"] == 1
    assert disconnected_trace["excess_volume_threshold"] == "default_inf"
    assert disconnected_trace["threshold_policy"] == "disabled"
    assert disconnected_trace["initial_active_groups"] == [[0], [1]]
    assert disconnected_trace["initial_edge_count"] == 0
    assert disconnected_trace["initial_candidates"] == []
    assert disconnected_trace["component_pair_edge_policy"] == (
        "insert_when_topology_queue_exhausted_before_target"
    )
    assert disconnected_trace["topology_queue_exhausted_before_component_pair_insertion"] is True
    assert disconnected_trace["component_pair_edge_insertion_triggered"] is True
    assert disconnected_trace["component_pair_candidate_count"] == 1
    assert disconnected_trace["component_pair_candidate_cap"] == "all_pairs_for_fixture"
    assert disconnected_trace["skipped_component_pair_count"] == 0
    assert disconnected_trace["component_pair_attempted_pair_count"] == 1
    assert disconnected_trace["accepted_merge_count"] == 1
    assert disconnected_trace["stale_entry_skipped_count"] == 0
    assert disconnected_trace["blocked_merge_count"] == 0
    assert disconnected_trace["stop_reason"] == "target_count_reached"
    assert disconnected_trace["final_active_groups"] == [[0, 1]]
    assert disconnected_trace["package_generation_triggered"] is False
    assert disconnected_trace["newton_runtime_triggered"] is False
    assert disconnected_trace["real_usd_triggered"] is False
    assert disconnected_trace["benchmark_triggered"] is False
    assert len(disconnected_trace["events"]) == 1
    component_event = disconnected_trace["events"][0]
    assert component_event["event_kind"] == "accepted_merge"
    assert component_event["edge_source"] == "component_pair"
    assert component_event["source_faces_left"] == [0]
    assert component_event["source_faces_right"] == [1]
    assert component_event["source_faces_merged"] == [0, 1]
    assert isfinite(component_event["paper_base_cost"])
    assert isfinite(component_event["weighted_priority_cost"])
    assert component_event["queue_key"] == [
        component_event["weighted_priority_cost"],
        component_event["paper_base_cost"],
        [0],
        [1],
        component_event["insertion_order"],
    ]
    assert component_event["left_primitive"]
    assert component_event["right_primitive"]
    assert component_event["merged_primitive"]
    assert component_event["accepted"] is True
    assert component_event["blocked"] is False
    assert component_event["stale_entry"] is False
    assert component_event["active_primitive_count_before"] == 2
    assert component_event["active_primitive_count_after"] == 1
    assert component_event["updated_neighbor_insertion_count"] == 0
    assert component_event["resulting_source_faces"] == [0, 1]

    threshold_case = cases["paper_component_pair_threshold_blocked"]
    threshold_trace = threshold_case["collapse_trace"]
    assert threshold_trace["trace_scope"] == "component_pair_priority_queue_trace_fixture"
    assert threshold_trace["target_primitive_count"] == 1
    assert threshold_trace["excess_volume_threshold"] == 0.0
    assert threshold_trace["threshold_policy"] == "component_pair_paper_base_cost_lte_threshold"
    assert threshold_trace["initial_active_groups"] == [[0], [1]]
    assert threshold_trace["initial_edge_count"] == 0
    assert threshold_trace["component_pair_edge_insertion_triggered"] is True
    assert threshold_trace["component_pair_candidate_count"] == 1
    assert threshold_trace["component_pair_candidate_cap"] == "all_pairs_for_fixture"
    assert threshold_trace["skipped_component_pair_count"] == 0
    assert threshold_trace["component_pair_attempted_pair_count"] == 1
    assert threshold_trace["accepted_merge_count"] == 0
    assert threshold_trace["blocked_merge_count"] == 1
    assert threshold_trace["stale_entry_skipped_count"] == 0
    assert threshold_trace["stop_reason"] == "all_remaining_edges_blocked_by_threshold"
    assert threshold_trace["final_active_groups"] == [[0], [1]]
    assert threshold_trace["package_generation_triggered"] is False
    assert threshold_trace["newton_runtime_triggered"] is False
    assert threshold_trace["real_usd_triggered"] is False
    assert threshold_trace["benchmark_triggered"] is False
    assert len(threshold_trace["events"]) == 1
    blocked_event = threshold_trace["events"][0]
    assert blocked_event["event_kind"] == "blocked_by_threshold"
    assert blocked_event["edge_source"] == "component_pair"
    assert blocked_event["source_faces_left"] == [0]
    assert blocked_event["source_faces_right"] == [1]
    assert blocked_event["source_faces_merged"] == [0, 1]
    assert blocked_event["paper_base_cost"] > 0.0
    assert isfinite(blocked_event["paper_base_cost"])
    assert isfinite(blocked_event["weighted_priority_cost"])
    assert blocked_event["queue_key"] == [
        blocked_event["weighted_priority_cost"],
        blocked_event["paper_base_cost"],
        [0],
        [1],
        blocked_event["insertion_order"],
    ]
    assert blocked_event["accepted"] is False
    assert blocked_event["blocked"] is True
    assert blocked_event["blocked_reason"] == "component_pair_threshold_exceeded"
    assert blocked_event["threshold_value"] == 0.0
    assert blocked_event["threshold_metric"] == "paper_base_cost"
    assert blocked_event["stale_entry"] is False
    assert blocked_event["active_primitive_count_before"] == 2
    assert blocked_event["active_primitive_count_after"] == 2
    assert blocked_event["updated_neighbor_insertion_count"] == 0
    assert "resulting_source_faces" not in blocked_event

    nested_case = cases["paper_nested_primitive"]
    assert nested_case["package_generation_triggered"] is False
    assert nested_case["newton_runtime_triggered"] is False
    assert nested_case["real_usd_triggered"] is False
    assert nested_case["benchmark_triggered"] is False
    postprocess = nested_case["postprocess_audit"]
    assert postprocess["audit_scope"] == "enclosed_primitive_culling_fixture"
    assert (
        postprocess["postprocess_input_source"]
        == "explicit_audit_primitives_not_search_trace"
    )
    assert (
        postprocess["postprocess_policy"]
        == "remove_primitives_enclosed_by_another_primitive"
    )
    assert postprocess["containment_test_type"] == "obb_corners_inside_obb"
    assert postprocess["axis_policy"] == "shared_identity_axes"
    assert postprocess["input_primitive_count"] == 2
    assert postprocess["output_primitive_count"] == 1
    assert postprocess["enclosed_primitive_ids"] == [1]
    assert postprocess["enclosing_primitive_ids"] == [0]
    assert postprocess["culled_primitive_ids"] == [1]
    assert postprocess["kept_primitive_ids"] == [0]
    assert postprocess["package_generation_triggered"] is False
    assert postprocess["newton_runtime_triggered"] is False
    assert postprocess["real_usd_triggered"] is False
    assert postprocess["benchmark_triggered"] is False

    identity_axes = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    input_primitives = postprocess["input_primitives"]
    assert len(input_primitives) == postprocess["input_primitive_count"]
    assert input_primitives == [
        {
            "primitive_id": 0,
            "kind": "oriented_bounding_box",
            "center": [0.0, 0.0, 0.0],
            "half_extents": [1.0, 1.0, 1.0],
            "axes": identity_axes,
        },
        {
            "primitive_id": 1,
            "kind": "oriented_bounding_box",
            "center": [0.0, 0.0, 0.0],
            "half_extents": [0.25, 0.25, 0.25],
            "axes": identity_axes,
        },
    ]
    assert len(postprocess["kept_primitive_ids"]) == postprocess["output_primitive_count"]
    cull_records = postprocess["cull_records"]
    assert cull_records == [
        {
            "culled_primitive_id": 1,
            "enclosing_primitive_id": 0,
            "cull_reason": "primitive_enclosed_by_larger_primitive",
            "containment_passed": True,
            "tested_corner_count": 8,
        }
    ]
    assert postprocess["culled_primitive_ids"] == [
        record["culled_primitive_id"] for record in cull_records
    ]
    assert postprocess["enclosed_primitive_ids"] == [
        record["culled_primitive_id"] for record in cull_records
    ]
    assert postprocess["enclosing_primitive_ids"] == [
        record["enclosing_primitive_id"] for record in cull_records
    ]


def test_cpd_paper_offline_report_is_strict_json_serializable():
    report = build_cpd_paper_offline_report()

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_paper_offline_report" in encoded


def test_cpd_paper_offline_report_audits_frustum_and_trapezoidal_prism_candidates():
    report = build_cpd_paper_offline_report()
    cases = {case["case_id"]: case for case in report["cases"]}

    frustum_case = cases["paper_frustum_like"]
    frustum_rows = {
        row["paper_primitive"]: row
        for row in frustum_case["primitive_fit_audit"]["candidates"]
    }
    frustum = frustum_rows["frustum"]
    assert frustum["implementation_status"] == "paper_shaped_offline_fit_audit"
    assert frustum["fit_model"] == "paper_frustum_axis_from_min_cost_flat_cylinder"
    assert frustum["newton_runtime_kind"] == "offline_only_unmapped"
    assert frustum["contains_assigned_points"] is True
    assert frustum["paper_weight"] == 2.1
    frustum_dims = frustum["dimensions"]
    assert frustum_dims["axis_selection_policy"] == "min_volume_flat_cylinder_axis"
    assert frustum_dims["volume_formula"] == "pi*h/3*(rt^2 + rt*rb + rb^2)"
    assert len(frustum_dims["flat_cylinder_axis_candidates"]) == 3
    flat_volumes = [
        row["flat_cylinder_volume"]
        for row in frustum_dims["flat_cylinder_axis_candidates"]
    ]
    selected_axis = frustum_dims["selected_axis_index"]
    selected_flat = [
        row
        for row in frustum_dims["flat_cylinder_axis_candidates"]
        if row["axis_index"] == selected_axis
    ][0]
    assert selected_flat["flat_cylinder_volume"] == min(flat_volumes)
    assert frustum_dims["height"] > 0.0
    assert frustum_dims["top_radius"] > 0.0
    assert frustum_dims["bottom_radius"] > 0.0
    expected_frustum_volume = (
        pi
        * frustum_dims["height"]
        / 3.0
        * (
            frustum_dims["top_radius"] ** 2
            + frustum_dims["top_radius"] * frustum_dims["bottom_radius"]
            + frustum_dims["bottom_radius"] ** 2
        )
    )
    assert abs(frustum["volume"] - expected_frustum_volume) < 1e-9
    assert abs(frustum["weighted_volume"] - frustum["volume"] * 2.1) < 1e-9

    trap_case = cases["paper_trapezoid_prism_like"]
    trap_rows = {
        row["paper_primitive"]: row
        for row in trap_case["primitive_fit_audit"]["candidates"]
    }
    trap = trap_rows["trapezoidal_prism"]
    assert trap["implementation_status"] == "paper_shaped_offline_fit_audit"
    assert trap["fit_model"] == "paper_isosceles_trapezoidal_prism_six_axis_orders"
    assert trap["newton_runtime_kind"] == "offline_only_unmapped"
    assert trap["contains_assigned_points"] is True
    assert trap["paper_weight"] == 1.4
    trap_dims = trap["dimensions"]
    assert trap_dims["axis_order_attempt_count"] == 6
    assert sorted(trap_dims["axis_order"]) == [0, 1, 2]
    assert trap_dims["volume_formula"] == "4*h_x*h_y*(h_zt + h_zb)"
    axis_orders = [tuple(row["axis_order"]) for row in trap_dims["axis_order_attempts"]]
    assert set(axis_orders) == {
        (0, 1, 2),
        (0, 2, 1),
        (1, 0, 2),
        (1, 2, 0),
        (2, 0, 1),
        (2, 1, 0),
    }
    containing_attempts = [
        row for row in trap_dims["axis_order_attempts"] if row["contains_assigned_points"]
    ]
    assert tuple(trap_dims["axis_order"]) in {
        tuple(row["axis_order"])
        for row in containing_attempts
        if row["volume"] == min(attempt["volume"] for attempt in containing_attempts)
    }
    assert all(row["contains_assigned_points"] for row in trap_dims["axis_order_attempts"])
    assert trap_dims["h_x"] > 0.0
    assert trap_dims["h_y"] > 0.0
    assert trap_dims["h_zt"] > 0.0
    assert trap_dims["h_zb"] > 0.0
    expected_trap_volume = (
        4.0
        * trap_dims["h_x"]
        * trap_dims["h_y"]
        * (trap_dims["h_zt"] + trap_dims["h_zb"])
    )
    assert abs(trap["volume"] - expected_trap_volume) < 1e-9
    assert abs(trap["weighted_volume"] - trap["volume"] * 1.4) < 1e-9


def test_cpd_paper_frustum_and_trapezoidal_prism_stay_out_of_runtime_primitives():
    assert "frustum" not in SUPPORTED_PRIMITIVES
    assert "trapezoidal_prism" not in SUPPORTED_PRIMITIVES
