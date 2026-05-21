import numpy as np
import pytest

import primitive_collision_compiler.baselines.cpd_like.synthetic as cpd_synthetic
from primitive_collision_compiler.baselines.cpd_like.decompose import decompose_mesh
from primitive_collision_compiler.baselines.cpd_like.primitives import PrimitiveFit, fit_best_primitive
from primitive_collision_compiler.geometry.mesh import TriangleMesh


def _square_mesh() -> TriangleMesh:
    return TriangleMesh(
        points=np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [1.0, 1.0, 0.0],
                [0.0, 1.0, 0.0],
            ]
        ),
        faces=np.array([[0, 1, 2], [0, 2, 3]]),
    )


def _disconnected_triangles_mesh() -> TriangleMesh:
    return TriangleMesh(
        points=np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [4.0, 0.0, 0.0],
                [5.0, 0.0, 0.0],
                [4.0, 1.0, 0.0],
            ]
        ),
        faces=np.array([[0, 1, 2], [3, 4, 5]]),
    )


def _cost_guided_pair_choice_mesh() -> TriangleMesh:
    return TriangleMesh(
        points=np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [10.0, 10.0, 10.0],
                [0.05, 0.05, 0.05],
                [1.05, 0.05, 0.05],
                [0.05, 1.05, 0.05],
            ]
        ),
        faces=np.array([[0, 1, 2], [1, 2, 3], [4, 5, 6]]),
    )


def _lookahead_merge_trap_mesh() -> TriangleMesh:
    centers = [
        (8.444218515250482, 7.579544029403024, 1.261714742492535),
        (2.5891675029296337, 5.112747213686085, 1.2148024123512429),
        (7.837985890347726, 3.0331272607892745, 1.4297908624570674),
        (5.833820394550312, 9.081128851953352, 1.5140605674521708),
    ]
    points = []
    faces = []
    for x, y, z in centers:
        base = len(points)
        points.extend(
            [
                (x, y, z),
                (x + 0.05, y, z),
                (x, y + 0.05, z),
            ]
        )
        faces.append((base, base + 1, base + 2))
    return TriangleMesh(points=np.array(points), faces=np.array(faces))


def _seven_disconnected_triangles_mesh() -> TriangleMesh:
    points = []
    faces = []
    for index in range(7):
        base = len(points)
        x = float(index * 3)
        points.extend(
            [
                (x, 0.0, 0.0),
                (x + 1.0, 0.0, 0.0),
                (x, 1.0, 0.0),
            ]
        )
        faces.append((base, base + 1, base + 2))
    return TriangleMesh(points=np.array(points), faces=np.array(faces))


def _nonplanar_adjacent_pair_mesh() -> TriangleMesh:
    return TriangleMesh(
        points=np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 1.0, 1.0],
            ]
        ),
        faces=np.array([[0, 1, 2], [0, 2, 3]]),
    )


def _long_bar_mesh() -> TriangleMesh:
    return TriangleMesh(
        points=np.array(
            [
                [0.0, -0.1, -0.1],
                [4.0, -0.1, -0.1],
                [4.0, 0.1, -0.1],
                [0.0, 0.1, -0.1],
                [0.0, -0.1, 0.1],
                [4.0, -0.1, 0.1],
                [4.0, 0.1, 0.1],
                [0.0, 0.1, 0.1],
            ]
        ),
        faces=np.array(
            [
                [0, 1, 2],
                [0, 2, 3],
                [4, 5, 6],
                [4, 6, 7],
            ]
        ),
    )


def test_fit_best_primitive_records_supported_and_unsupported_types():
    fit = fit_best_primitive(_square_mesh(), frozenset({0, 1}), ("box", "sphere", "capsule"))

    assert fit.primitive_type in {"box", "sphere", "capsule"}
    assert fit.source_faces == (0, 1)
    assert fit.contains_assigned_points is True
    assert fit.volume > 0
    assert fit.weighted_volume > 0
    assert "capped_cylinder" in fit.unsupported_primitives
    assert "frustum" in fit.unsupported_primitives
    assert "trapezoidal_prism" in fit.unsupported_primitives


def test_fit_best_primitive_serializes_box_dimensions():
    fit = fit_best_primitive(_square_mesh(), frozenset({0, 1}), ("box",))
    payload = fit.to_dict()

    assert payload["primitive_type"] == "box"
    assert payload["source_faces"] == [0, 1]
    assert payload["source_face_count"] == 2
    assert payload["source_component_ids"] == []
    assert payload["cost_weight"] == 0.0
    assert payload["contains_assigned_points"] is True
    assert len(payload["dimensions"]["half_extents"]) == 3


def test_capsule_fitting_uses_translated_group_center():
    mesh = TriangleMesh(
        points=np.array(
            [
                [0.0, 10.0, 0.0],
                [4.0, 10.0, 0.0],
                [4.0, 10.1, 0.0],
                [0.0, 10.1, 0.0],
            ]
        ),
        faces=np.array([[0, 1, 2], [0, 2, 3]]),
    )

    fit = fit_best_primitive(mesh, frozenset({0, 1}), ("capsule",))

    assert fit.primitive_type == "capsule"
    assert fit.contains_assigned_points is True
    assert fit.dimensions["radius"] < 0.11


def test_fit_best_primitive_supports_capped_cylinder_proxy():
    fit = fit_best_primitive(_long_bar_mesh(), frozenset({0, 1, 2, 3}), ("capped_cylinder",))

    assert fit.primitive_type == "capped_cylinder"
    assert fit.contains_assigned_points is True
    assert fit.dimensions["radius"] > 0.0
    assert fit.dimensions["half_height"] > 0.0
    assert fit.dimensions["axis_index"] in (0, 1, 2)
    assert fit.dimensions["cap_model"] == "hemisphere_caps"
    assert fit.dimensions["proxy_fit"] == "axis_span_radial_proxy"
    assert fit.volume > 0.0
    assert fit.weighted_volume == fit.volume
    assert fit.unsupported_primitives == ("frustum", "trapezoidal_prism")


def test_fit_best_primitive_tracks_requested_capped_cylinder_support():
    box_only = fit_best_primitive(_square_mesh(), frozenset({0, 1}), ("box",))
    mixed = fit_best_primitive(_square_mesh(), frozenset({0, 1}), ("box", "capped_cylinder"))

    assert box_only.unsupported_primitives == (
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    )
    assert mixed.unsupported_primitives == ("frustum", "trapezoidal_prism")


def test_fit_best_primitive_uses_subset_order_to_break_equal_proxy_ties():
    mesh = _long_bar_mesh()

    capped_first = fit_best_primitive(
        mesh,
        frozenset({0, 1, 2, 3}),
        ("capped_cylinder", "capsule"),
    )
    capsule_first = fit_best_primitive(
        mesh,
        frozenset({0, 1, 2, 3}),
        ("capsule", "capped_cylinder"),
    )

    assert capped_first.primitive_type == "capped_cylinder"
    assert capsule_first.primitive_type == "capsule"


def test_decompose_mesh_merges_adjacent_square_to_requested_count():
    report = decompose_mesh(
        _square_mesh(),
        max_primitives=1,
        primitive_subset=("box", "sphere", "capsule"),
    )

    assert report.stage == "cpd_like_face_merge"
    assert report.status == "smoke_passed"
    assert report.primitive_count == 1
    assert report.max_primitives == 1
    assert report.mesh_face_count == 2
    assert report.primitives[0].source_faces == (0, 1)
    assert report.primitives[0].contains_assigned_points is True
    assert report.to_dict()["primitive_count"] == 1


def test_decompose_mesh_records_unmerged_disconnected_components():
    mesh = _disconnected_triangles_mesh()

    report = decompose_mesh(mesh, max_primitives=1, primitive_subset=("box",))

    assert report.status == "partial"
    assert report.primitive_count == 2
    assert report.fallback_reason == "no_adjacent_clusters_remaining"
    assert report.merge_policy == "topology_only"
    assert report.initial_component_count == 2
    assert report.topology_merge_count == 0
    assert report.virtual_component_merge_count == 0
    assert report.blocked_merge_count == 0
    assert report.final_component_count == 2


def test_decompose_mesh_component_merge_gate_can_merge_disconnected_components():
    mesh = _disconnected_triangles_mesh()

    report = decompose_mesh(
        mesh,
        max_primitives=1,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
    )

    assert report.stage == "cpd_like_component_merge_gate"
    assert report.status == "smoke_passed"
    assert report.primitive_count == 1
    assert report.merge_policy == "virtual_pairwise"
    assert report.initial_component_count == 2
    assert report.topology_merge_count == 0
    assert report.virtual_component_merge_count == 1
    assert report.blocked_merge_count == 0
    assert report.final_component_count == 1
    assert report.fallback_reason is None
    assert report.primitives[0].source_faces == (0, 1)
    assert report.primitives[0].source_component_ids == (0, 1)
    payload = report.to_dict()
    assert payload["merge_cost_summary"]["accepted_merge_count"] == 1
    assert payload["primitives"][0]["source_face_count"] == 2
    assert payload["primitives"][0]["source_component_ids"] == [0, 1]


def test_decompose_mesh_component_merge_gate_blocks_excessive_virtual_merge_cost():
    mesh = _disconnected_triangles_mesh()

    report = decompose_mesh(
        mesh,
        max_primitives=1,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        excess_volume_threshold_fraction=0.001,
    )

    assert report.status == "partial"
    assert report.primitive_count == 2
    assert report.virtual_component_merge_count == 0
    assert report.blocked_merge_count == 1
    assert report.fallback_reason == "component_merge_threshold_blocked"
    assert report.merge_cost_summary["blocked_merge_count"] == 1


def test_decompose_mesh_default_merge_search_keeps_topology_before_virtual():
    report = decompose_mesh(
        _cost_guided_pair_choice_mesh(),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
    )

    assert report.status == "smoke_passed"
    assert report.merge_search_policy == "topology_then_virtual"
    assert report.topology_merge_count == 1
    assert report.virtual_component_merge_count == 0
    assert report.primitives[0].source_component_ids == (0, 1)


def test_decompose_mesh_records_raw_eq4_cost_and_normalized_cost():
    mesh = _cost_guided_pair_choice_mesh()
    report = decompose_mesh(
        mesh,
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
    )
    left = fit_best_primitive(mesh, frozenset({0}), ("box",))
    right = fit_best_primitive(mesh, frozenset({1}), ("box",))
    merged = fit_best_primitive(mesh, frozenset({0, 1}), ("box",))
    expected_raw_cost = merged.weighted_volume - left.weighted_volume - right.weighted_volume
    expected_normalized_cost = expected_raw_cost / report.merge_cost_summary["normalizer_volume"]

    assert report.merge_cost_summary["accepted_eq4_cost_sum"] == pytest.approx(
        expected_raw_cost
    )
    assert report.merge_cost_summary["accepted_eq4_cost_min"] == pytest.approx(
        expected_raw_cost
    )
    assert report.merge_cost_summary["accepted_eq4_cost_max"] == pytest.approx(
        expected_raw_cost
    )
    assert report.merge_cost_summary["accepted_normalized_excess_sum"] == pytest.approx(
        expected_normalized_cost
    )
    assert report.merge_cost_summary["normalization"] == {
        "kind": "source_mesh_aabb_volume",
        "floor": 1e-12,
        "normalizer_volume": report.merge_cost_summary["normalizer_volume"],
        "applied_to": [
            "accepted_normalized_excess",
            "blocked_normalized_excess",
            "excess_volume_threshold_fraction",
        ],
    }


def test_decompose_mesh_serializes_negative_raw_eq4_cost(monkeypatch):
    def fake_fit(mesh, face_ids, primitive_subset):
        source_faces = tuple(sorted(face_ids))
        weighted_volumes = {
            (0,): 10.0,
            (1,): 10.0,
            (0, 1): 5.0,
        }
        volume = weighted_volumes[source_faces]
        return PrimitiveFit(
            primitive_type="box",
            source_faces=source_faces,
            center=(0.0, 0.0, 0.0),
            axes=((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
            dimensions={"half_extents": [1.0, 1.0, 1.0]},
            volume=volume,
            weighted_volume=volume,
            contains_assigned_points=True,
        )

    monkeypatch.setattr(
        "primitive_collision_compiler.baselines.cpd_like.decompose.fit_best_primitive",
        fake_fit,
    )

    report = decompose_mesh(
        _nonplanar_adjacent_pair_mesh(),
        max_primitives=1,
        primitive_subset=("box",),
    )

    assert report.status == "smoke_passed"
    assert report.merge_cost_summary["accepted_eq4_cost_sum"] == -15.0
    assert report.merge_cost_summary["accepted_normalized_excess_sum"] == -15.0


def test_decompose_mesh_cost_guided_pairwise_can_choose_virtual_before_topology():
    default_report = decompose_mesh(
        _cost_guided_pair_choice_mesh(),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
    )
    cost_guided_report = decompose_mesh(
        _cost_guided_pair_choice_mesh(),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        merge_search_policy="cost_guided_pairwise",
    )

    assert cost_guided_report.stage == "cpd_like_cost_guided_merge_smoke"
    assert cost_guided_report.status == "smoke_passed"
    assert cost_guided_report.merge_search_policy == "cost_guided_pairwise"
    assert cost_guided_report.topology_merge_count == 0
    assert cost_guided_report.virtual_component_merge_count == 1
    assert cost_guided_report.primitives[0].source_component_ids == (0, 2)
    assert (
        cost_guided_report.merge_cost_summary["accepted_normalized_excess_sum"]
        < default_report.merge_cost_summary["accepted_normalized_excess_sum"]
    )


def test_decompose_mesh_steps_trace_records_cost_guided_virtual_merge():
    report = decompose_mesh(
        _cost_guided_pair_choice_mesh(),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        merge_search_policy="cost_guided_pairwise",
        report_merge_trace="steps",
    )

    assert len(report.merge_trace) == 1
    step = report.merge_trace[0]
    assert step["step_index"] == 1
    assert step["decision"] == "accepted"
    assert step["merge_kind"] == "virtual_component"
    assert step["left_source_faces"] == [0]
    assert step["right_source_faces"] == [2]
    assert step["merged_source_faces"] == [0, 2]
    assert step["merged_source_component_ids"] == [0, 2]
    assert step["merged_primitive_type"] == "box"
    assert step["normalized_excess_volume"] == pytest.approx(
        report.merge_cost_summary["accepted_normalized_excess_sum"]
    )
    assert report.to_dict()["merge_trace"] == list(report.merge_trace)


def test_decompose_mesh_two_step_lookahead_changes_first_merge_on_trap():
    greedy = decompose_mesh(
        _lookahead_merge_trap_mesh(),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        merge_search_policy="cost_guided_pairwise",
        report_merge_trace="steps",
    )
    lookahead = decompose_mesh(
        _lookahead_merge_trap_mesh(),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        merge_search_policy="two_step_lookahead",
        report_merge_trace="steps",
    )

    greedy_groups = tuple(sorted(tuple(primitive.source_faces) for primitive in greedy.primitives))
    lookahead_groups = tuple(
        sorted(tuple(primitive.source_faces) for primitive in lookahead.primitives)
    )

    assert greedy_groups == ((0, 2, 3), (1,))
    assert lookahead_groups == ((0, 1), (2, 3))
    assert lookahead.merge_search_policy == "two_step_lookahead"
    assert lookahead.merge_cost_summary["accepted_normalized_excess_sum"] < (
        greedy.merge_cost_summary["accepted_normalized_excess_sum"]
    )
    first_step = lookahead.merge_trace[0]
    assert first_step["merged_source_faces"] == [0, 1]
    assert first_step["projected_followup_normalized_excess_volume"] > 0.0
    assert first_step["projected_total_normalized_excess_volume"] == pytest.approx(
        lookahead.merge_cost_summary["accepted_normalized_excess_sum"]
    )


def test_decompose_mesh_two_step_lookahead_requires_virtual_pairwise():
    with pytest.raises(ValueError, match="two_step_lookahead requires component_merge"):
        decompose_mesh(
            _lookahead_merge_trap_mesh(),
            max_primitives=2,
            primitive_subset=("box",),
            merge_search_policy="two_step_lookahead",
        )


def test_decompose_mesh_two_step_lookahead_rejects_non_tiny_mesh():
    with pytest.raises(ValueError, match="two_step_lookahead supports at most 6 faces"):
        decompose_mesh(
            _seven_disconnected_triangles_mesh(),
            max_primitives=2,
            primitive_subset=("box",),
            component_merge="virtual_pairwise",
            merge_search_policy="two_step_lookahead",
        )


def test_decompose_mesh_two_step_lookahead_preserves_virtual_threshold_block():
    report = decompose_mesh(
        _lookahead_merge_trap_mesh(),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        merge_search_policy="two_step_lookahead",
        excess_volume_threshold_fraction=0.01,
        report_merge_trace="steps",
    )

    assert report.status == "partial"
    assert report.fallback_reason == "component_merge_threshold_blocked"
    assert report.blocked_merge_count == 1
    assert report.merge_trace[0]["decision"] == "blocked"
    assert report.merge_trace[0]["merged_source_faces"] == [0, 1]


def test_decompose_mesh_applies_opt_in_primitive_score_multipliers():
    mesh = cpd_synthetic._cylinder_near_miss_cluster_mesh()

    default_report = decompose_mesh(
        mesh,
        max_primitives=1,
        primitive_subset=("box", "cylinder"),
    )
    opt_in_report = decompose_mesh(
        mesh,
        max_primitives=1,
        primitive_subset=("box", "cylinder"),
        primitive_score_multipliers={"cylinder": 0.88},
    )

    assert default_report.primitives[0].primitive_type == "box"
    assert default_report.primitive_score_multipliers == {}
    assert "primitive_score_multipliers" not in default_report.to_dict()
    assert opt_in_report.primitives[0].primitive_type == "cylinder"
    assert opt_in_report.primitive_score_multipliers == {"cylinder": 0.88}
    assert opt_in_report.to_dict()["primitive_score_multipliers"] == {"cylinder": 0.88}


def test_decompose_mesh_applies_opt_in_primitive_selection_guard():
    mesh = cpd_synthetic._cylinder_near_miss_cluster_mesh()

    unguarded_report = decompose_mesh(
        mesh,
        max_primitives=1,
        primitive_subset=("box", "cylinder"),
        primitive_score_multipliers={"cylinder": 0.88},
    )
    guarded_report = decompose_mesh(
        mesh,
        max_primitives=1,
        primitive_subset=("box", "cylinder"),
        primitive_score_multipliers={"cylinder": 0.88},
        primitive_selection_guard={
            "enabled": True,
            "mode": "reject",
            "target_primitives": ["cylinder"],
            "max_cylinder_radius": 0.0,
            "min_cylinder_half_height_radius_ratio": 999.0,
        },
    )

    assert unguarded_report.primitives[0].primitive_type == "cylinder"
    assert guarded_report.primitives[0].primitive_type == "box"
    assert guarded_report.primitive_selection_guard == {
        "enabled": True,
        "mode": "reject",
        "target_primitives": ["cylinder"],
        "max_cylinder_radius": 0.0,
        "min_cylinder_half_height_radius_ratio": 999.0,
    }
    assert guarded_report.to_dict()["primitive_selection_guard"] == (
        guarded_report.primitive_selection_guard
    )


def test_decompose_mesh_rejects_bad_primitive_score_multipliers():
    with pytest.raises(ValueError, match="primitive score multipliers"):
        decompose_mesh(
            cpd_synthetic._cylinder_near_miss_cluster_mesh(),
            max_primitives=1,
            primitive_subset=("box", "cylinder"),
            primitive_score_multipliers={"cylinder": 0.0},
        )


def test_decompose_mesh_rejects_bad_primitive_selection_guard():
    with pytest.raises(ValueError, match="primitive selection guard"):
        decompose_mesh(
            cpd_synthetic._cylinder_near_miss_cluster_mesh(),
            max_primitives=1,
            primitive_subset=("box", "cylinder"),
            primitive_selection_guard={"enabled": True, "mode": "rerank"},
        )


def test_decompose_mesh_default_and_none_trace_modes_do_not_serialize_merge_trace():
    summary_report = decompose_mesh(
        _cost_guided_pair_choice_mesh(),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        merge_search_policy="cost_guided_pairwise",
    )
    none_report = decompose_mesh(
        _cost_guided_pair_choice_mesh(),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        merge_search_policy="cost_guided_pairwise",
        report_merge_trace="none",
    )

    assert summary_report.merge_trace == ()
    assert none_report.merge_trace == ()
    assert "merge_trace" not in summary_report.to_dict()
    assert "merge_trace" not in none_report.to_dict()


def test_decompose_mesh_steps_trace_records_blocked_virtual_merge():
    report = decompose_mesh(
        _cost_guided_pair_choice_mesh(),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        merge_search_policy="cost_guided_pairwise",
        excess_volume_threshold_fraction=0.0,
        report_merge_trace="steps",
    )

    assert report.status == "partial"
    assert len(report.merge_trace) == 1
    assert report.merge_trace[0]["decision"] == "blocked"
    assert report.merge_trace[0]["merge_kind"] == "virtual_component"
    assert report.merge_trace[0]["blocked_reason"] == "component_merge_threshold_blocked"
    assert report.merge_cost_summary["blocked_merge_count"] == 1


def test_decompose_mesh_cost_guided_pairwise_keeps_virtual_threshold_gate():
    report = decompose_mesh(
        _cost_guided_pair_choice_mesh(),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        merge_search_policy="cost_guided_pairwise",
        excess_volume_threshold_fraction=0.0,
    )

    assert report.status == "partial"
    assert report.topology_merge_count == 0
    assert report.virtual_component_merge_count == 0
    assert report.blocked_merge_count == 1
    assert report.fallback_reason == "component_merge_threshold_blocked"


def test_decompose_mesh_cost_guided_pairwise_skips_virtual_merge_inside_connected_component(
    monkeypatch,
):
    def fake_fit(mesh, face_ids, primitive_subset):
        source_faces = tuple(sorted(face_ids))
        weighted_volumes = {
            (0,): 10.0,
            (1,): 10.0,
            (2,): 10.0,
            (0, 1): 100.0,
            (1, 2): 100.0,
            (0, 2): 1.0,
        }
        volume = weighted_volumes[source_faces]
        return PrimitiveFit(
            primitive_type="box",
            source_faces=source_faces,
            center=(0.0, 0.0, 0.0),
            axes=((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
            dimensions={"half_extents": [1.0, 1.0, 1.0]},
            volume=volume,
            weighted_volume=volume,
            contains_assigned_points=True,
        )

    monkeypatch.setattr(
        "primitive_collision_compiler.baselines.cpd_like.decompose.fit_best_primitive",
        fake_fit,
    )

    report = decompose_mesh(
        TriangleMesh(
            points=np.array(
                [
                    [0.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0],
                    [1.0, 1.0, 0.0],
                    [0.0, 2.0, 0.0],
                ]
            ),
            faces=np.array([[0, 1, 2], [1, 2, 3], [2, 3, 4]]),
        ),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        merge_search_policy="cost_guided_pairwise",
    )

    assert report.topology_merge_count == 1
    assert report.virtual_component_merge_count == 0
    assert report.primitives[0].source_component_ids == (0, 1)


def test_decompose_mesh_rejects_unknown_merge_search_policy():
    try:
        decompose_mesh(
            _square_mesh(),
            max_primitives=1,
            primitive_subset=("box",),
            merge_search_policy="paper_optimizer",
        )
    except ValueError as exc:
        assert "merge_search_policy" in str(exc)
    else:
        raise AssertionError("unknown merge_search_policy should be rejected")


def test_decompose_mesh_component_merge_gate_validates_options():
    mesh = _square_mesh()

    for kwargs in (
        {"component_merge": "all_pairs"},
        {"report_merge_trace": "full"},
        {"excess_volume_threshold_fraction": -0.1},
        {"excess_volume_threshold_fraction": float("inf")},
    ):
        try:
            decompose_mesh(mesh, max_primitives=1, primitive_subset=("box",), **kwargs)
        except ValueError as exc:
            assert next(iter(kwargs)) in str(exc)
        else:
            raise AssertionError(f"{kwargs} should be rejected")


def test_decompose_mesh_component_merge_gate_normalizes_string_threshold():
    report = decompose_mesh(
        _disconnected_triangles_mesh(),
        max_primitives=1,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        excess_volume_threshold_fraction="1.0",
    )

    assert report.status == "partial"
    assert report.excess_volume_threshold_fraction == 1.0
    assert report.fallback_reason == "component_merge_threshold_blocked"
