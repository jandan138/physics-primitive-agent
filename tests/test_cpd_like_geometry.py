import numpy as np
import pytest

from primitive_collision_compiler.geometry.mesh import TriangleMesh


def test_triangle_mesh_builds_shared_edge_adjacency():
    mesh = TriangleMesh(
        points=np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [1.0, 1.0, 0.0],
                [0.0, 1.0, 0.0],
                [3.0, 0.0, 0.0],
                [4.0, 0.0, 0.0],
                [3.0, 1.0, 0.0],
            ]
        ),
        faces=np.array([[0, 1, 2], [0, 2, 3], [4, 5, 6]]),
    )

    assert mesh.face_count == 3
    assert mesh.adjacent_faces() == {0: {1}, 1: {0}, 2: set()}


def test_triangle_mesh_face_operator_is_area_weighted():
    mesh = TriangleMesh(
        points=np.array([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0], [0.0, 1.0, 0.0]]),
        faces=np.array([[0, 1, 2]]),
    )

    assert mesh.face_area(0) == pytest.approx(1.0)
    operator = mesh.face_operator(0)
    assert operator.shape == (3, 3)
    assert operator[2, 2] > 0.99


def test_triangle_mesh_rejects_non_triangular_faces():
    with pytest.raises(ValueError, match="faces must have shape"):
        TriangleMesh(
            points=np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]]),
            faces=np.array([[0, 1, 2, 0]]),
        )
