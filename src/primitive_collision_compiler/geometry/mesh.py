from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class TriangleMesh:
    points: NDArray[np.float64]
    faces: NDArray[np.int64]

    def __post_init__(self) -> None:
        points = np.asarray(self.points, dtype=np.float64)
        faces = np.asarray(self.faces, dtype=np.int64)
        if points.ndim != 2 or points.shape[1] != 3:
            raise ValueError("points must have shape (N, 3)")
        if faces.ndim != 2 or faces.shape[1] != 3:
            raise ValueError("faces must have shape (M, 3)")
        if len(points) == 0:
            raise ValueError("points must not be empty")
        if len(faces) == 0:
            raise ValueError("faces must not be empty")
        if np.any(faces < 0) or np.any(faces >= len(points)):
            raise ValueError("faces contain point indices outside the points array")
        object.__setattr__(self, "points", points)
        object.__setattr__(self, "faces", faces)

    @property
    def face_count(self) -> int:
        return int(self.faces.shape[0])

    def face_points(self, face_index: int) -> NDArray[np.float64]:
        return self.points[self.faces[face_index]]

    def face_area(self, face_index: int) -> float:
        p0, p1, p2 = self.face_points(face_index)
        return float(np.linalg.norm(np.cross(p1 - p0, p2 - p0)) * 0.5)

    def face_operator(self, face_index: int, epsilon: float = 1e-6) -> NDArray[np.float64]:
        p0, p1, p2 = self.face_points(face_index)
        edge0 = p1 - p0
        edge1 = p2 - p0
        cross = np.cross(edge0, edge1)
        cross_norm = np.linalg.norm(cross)
        area = cross_norm * 0.5
        if cross_norm == 0.0:
            normal = np.array([0.0, 0.0, 1.0], dtype=np.float64)
        else:
            normal = cross / cross_norm

        edge0_norm = np.linalg.norm(edge0)
        if edge0_norm == 0.0:
            tangent = np.array([1.0, 0.0, 0.0], dtype=np.float64)
        else:
            tangent = edge0 / edge0_norm

        return area * (np.outer(normal, normal) + epsilon * np.outer(tangent, tangent))

    def adjacent_faces(self) -> dict[int, set[int]]:
        adjacency: dict[int, set[int]] = {face_index: set() for face_index in range(self.face_count)}
        edges: dict[tuple[int, int], list[int]] = {}
        for face_index, face in enumerate(self.faces):
            for start, end in ((face[0], face[1]), (face[1], face[2]), (face[2], face[0])):
                edge = tuple(sorted((int(start), int(end))))
                edges.setdefault(edge, []).append(face_index)

        for face_indices in edges.values():
            if len(face_indices) < 2:
                continue
            for left in face_indices:
                adjacency[left].update(right for right in face_indices if right != left)
        return adjacency
