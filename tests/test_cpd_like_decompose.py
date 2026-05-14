import numpy as np

from primitive_collision_compiler.baselines.cpd_like.decompose import decompose_mesh
from primitive_collision_compiler.baselines.cpd_like.primitives import fit_best_primitive
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
    assert payload["contains_assigned_points"] is True
    assert len(payload["dimensions"]["half_extents"]) == 3


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
    mesh = TriangleMesh(
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

    report = decompose_mesh(mesh, max_primitives=1, primitive_subset=("box",))

    assert report.status == "partial"
    assert report.primitive_count == 2
    assert report.fallback_reason == "no_adjacent_clusters_remaining"
