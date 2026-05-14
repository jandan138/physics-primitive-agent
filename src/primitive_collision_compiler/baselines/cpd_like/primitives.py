from __future__ import annotations

from dataclasses import dataclass
from math import pi

import numpy as np
from numpy.typing import NDArray

from primitive_collision_compiler.geometry.mesh import TriangleMesh

SUPPORTED_PRIMITIVES = ("box", "sphere", "capsule")
UNSUPPORTED_PAPER_PRIMITIVES = ("capped_cylinder", "frustum", "trapezoidal_prism")
MIN_DIMENSION = 1e-6
CONTAINMENT_TOLERANCE = 1e-8


@dataclass(frozen=True)
class PrimitiveFit:
    primitive_type: str
    source_faces: tuple[int, ...]
    center: tuple[float, float, float]
    axes: tuple[tuple[float, float, float], ...]
    dimensions: dict[str, object]
    volume: float
    weighted_volume: float
    contains_assigned_points: bool
    unsupported_primitives: tuple[str, ...] = UNSUPPORTED_PAPER_PRIMITIVES
    source_component_ids: tuple[int, ...] = ()
    cost_weight: float = 0.0

    def to_dict(self) -> dict[str, object]:
        return {
            "primitive_type": self.primitive_type,
            "source_faces": list(self.source_faces),
            "source_face_count": len(self.source_faces),
            "source_component_ids": list(self.source_component_ids),
            "cost_weight": self.cost_weight,
            "center": list(self.center),
            "axes": [list(axis) for axis in self.axes],
            "dimensions": self.dimensions,
            "volume": self.volume,
            "weighted_volume": self.weighted_volume,
            "contains_assigned_points": self.contains_assigned_points,
            "unsupported_primitives": list(self.unsupported_primitives),
        }


def fit_best_primitive(
    mesh: TriangleMesh,
    face_ids: frozenset[int],
    primitive_subset: tuple[str, ...],
) -> PrimitiveFit:
    if not face_ids:
        raise ValueError("face_ids must not be empty")

    requested = tuple(dict.fromkeys(primitive_subset))
    unsupported_requested = [primitive for primitive in requested if primitive not in SUPPORTED_PRIMITIVES]
    supported_requested = [primitive for primitive in requested if primitive in SUPPORTED_PRIMITIVES]
    if not supported_requested:
        raise ValueError("primitive_subset must include at least one supported primitive")

    points = _assigned_points(mesh, face_ids)
    axes = _candidate_axes(mesh, face_ids)
    candidates = [
        _fit_primitive(primitive, points, axes, tuple(sorted(face_ids)))
        for primitive in supported_requested
    ]
    best = min(candidates, key=lambda fit: (fit.weighted_volume, fit.primitive_type))
    if unsupported_requested:
        unsupported = tuple(dict.fromkeys((*best.unsupported_primitives, *unsupported_requested)))
        return PrimitiveFit(
            primitive_type=best.primitive_type,
            source_faces=best.source_faces,
            center=best.center,
            axes=best.axes,
            dimensions=best.dimensions,
            volume=best.volume,
            weighted_volume=best.weighted_volume,
            contains_assigned_points=best.contains_assigned_points,
            unsupported_primitives=unsupported,
            source_component_ids=best.source_component_ids,
            cost_weight=best.cost_weight,
        )
    return best


def _fit_primitive(
    primitive_type: str,
    points: NDArray[np.float64],
    axes: NDArray[np.float64],
    source_faces: tuple[int, ...],
) -> PrimitiveFit:
    if primitive_type == "box":
        return _fit_box(points, axes, source_faces)
    if primitive_type == "sphere":
        return _fit_sphere(points, axes, source_faces)
    if primitive_type == "capsule":
        return _fit_capsule(points, axes, source_faces)
    raise ValueError(f"unsupported primitive type: {primitive_type}")


def _assigned_points(mesh: TriangleMesh, face_ids: frozenset[int]) -> NDArray[np.float64]:
    point_indices: list[int] = []
    for face_id in sorted(face_ids):
        point_indices.extend(int(index) for index in mesh.faces[face_id])
    unique_indices = sorted(set(point_indices))
    return np.asarray(mesh.points[unique_indices], dtype=np.float64)


def _candidate_axes(mesh: TriangleMesh, face_ids: frozenset[int]) -> NDArray[np.float64]:
    operator = np.zeros((3, 3), dtype=np.float64)
    for face_id in face_ids:
        operator += mesh.face_operator(face_id)
    _, eigenvectors = np.linalg.eigh(operator)
    axes = eigenvectors[:, ::-1]
    if np.linalg.det(axes) < 0:
        axes[:, -1] *= -1.0
    return axes


def _fit_box(
    points: NDArray[np.float64],
    axes: NDArray[np.float64],
    source_faces: tuple[int, ...],
) -> PrimitiveFit:
    local = points @ axes
    local_min = local.min(axis=0)
    local_max = local.max(axis=0)
    local_center = (local_min + local_max) * 0.5
    half_extents = np.maximum((local_max - local_min) * 0.5, MIN_DIMENSION)
    center = axes @ local_center
    volume = float(8.0 * np.prod(half_extents))
    contains = bool(np.all(np.abs(local - local_center) <= half_extents + CONTAINMENT_TOLERANCE))
    return PrimitiveFit(
        primitive_type="box",
        source_faces=source_faces,
        center=_vector_to_tuple(center),
        axes=_axes_to_tuple(axes),
        dimensions={"half_extents": [float(value) for value in half_extents]},
        volume=volume,
        weighted_volume=volume,
        contains_assigned_points=contains,
    )


def _fit_sphere(
    points: NDArray[np.float64],
    axes: NDArray[np.float64],
    source_faces: tuple[int, ...],
) -> PrimitiveFit:
    local = points @ axes
    local_center = (local.min(axis=0) + local.max(axis=0)) * 0.5
    center = axes @ local_center
    distances = np.linalg.norm(points - center, axis=1)
    radius = max(float(distances.max(initial=0.0)), MIN_DIMENSION)
    volume = float((4.0 / 3.0) * pi * radius**3)
    contains = bool(np.all(distances <= radius + CONTAINMENT_TOLERANCE))
    return PrimitiveFit(
        primitive_type="sphere",
        source_faces=source_faces,
        center=_vector_to_tuple(center),
        axes=_axes_to_tuple(axes),
        dimensions={"radius": radius},
        volume=volume,
        weighted_volume=volume,
        contains_assigned_points=contains,
    )


def _fit_capsule(
    points: NDArray[np.float64],
    axes: NDArray[np.float64],
    source_faces: tuple[int, ...],
) -> PrimitiveFit:
    local = points @ axes
    spans = local.max(axis=0) - local.min(axis=0)
    axis_index = int(np.argmax(spans))
    axis = axes[:, axis_index]
    projections = points @ axis
    projection_min = float(projections.min())
    projection_max = float(projections.max())
    segment_center_projection = (projection_min + projection_max) * 0.5
    centroid = points.mean(axis=0)
    perpendicular_center = centroid - axis * float(centroid @ axis)
    center = perpendicular_center + axis * segment_center_projection
    axial_offsets = np.outer(projections - segment_center_projection, axis)
    radial_vectors = points - center - axial_offsets
    radial_distances = np.linalg.norm(radial_vectors, axis=1)
    radius = max(float(radial_distances.max(initial=0.0)), MIN_DIMENSION)
    half_height = max((projection_max - projection_min) * 0.5, 0.0)
    cylinder_length = half_height * 2.0
    volume = float(pi * radius**2 * cylinder_length + (4.0 / 3.0) * pi * radius**3)
    contains = bool(_capsule_contains(points, axis, center, half_height, radius))
    return PrimitiveFit(
        primitive_type="capsule",
        source_faces=source_faces,
        center=_vector_to_tuple(center),
        axes=_axes_to_tuple(axes),
        dimensions={"radius": radius, "half_height": half_height, "axis_index": axis_index},
        volume=volume,
        weighted_volume=volume,
        contains_assigned_points=contains,
    )


def _capsule_contains(
    points: NDArray[np.float64],
    axis: NDArray[np.float64],
    center: NDArray[np.float64],
    half_height: float,
    radius: float,
) -> bool:
    relative = points - center
    projected = relative @ axis
    clamped = np.clip(projected, -half_height, half_height)
    closest = center + np.outer(clamped, axis)
    distances = np.linalg.norm(points - closest, axis=1)
    return bool(np.all(distances <= radius + CONTAINMENT_TOLERANCE))


def _vector_to_tuple(vector: NDArray[np.float64]) -> tuple[float, float, float]:
    return tuple(float(value) for value in vector)


def _axes_to_tuple(axes: NDArray[np.float64]) -> tuple[tuple[float, float, float], ...]:
    return tuple(_vector_to_tuple(axes[:, index]) for index in range(axes.shape[1]))
