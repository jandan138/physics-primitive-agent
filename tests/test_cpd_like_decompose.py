import numpy as np

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
