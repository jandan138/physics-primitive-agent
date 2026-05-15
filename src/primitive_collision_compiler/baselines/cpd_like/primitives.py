from __future__ import annotations

from dataclasses import dataclass, replace
from math import pi

import numpy as np
from numpy.typing import NDArray

from primitive_collision_compiler.geometry.mesh import TriangleMesh

SUPPORTED_PRIMITIVES = (
    "box",
    "sphere",
    "capsule",
    "cylinder",
    "cone",
    "ellipsoid",
    "capped_cylinder",
)
PAPER_SCOPE_PRIMITIVES = ("capped_cylinder", "frustum", "trapezoidal_prism")
UNSUPPORTED_PAPER_PRIMITIVES = PAPER_SCOPE_PRIMITIVES
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
    supported_requested = [primitive for primitive in requested if primitive in SUPPORTED_PRIMITIVES]
    if not supported_requested:
        raise ValueError("primitive_subset must include at least one supported primitive")

    points = _assigned_points(mesh, face_ids)
    axes = _candidate_axes(mesh, face_ids)
    candidates = [
        (
            order,
            _fit_primitive(primitive, points, axes, tuple(sorted(face_ids))),
        )
        for order, primitive in enumerate(supported_requested)
    ]
    best = min(candidates, key=lambda item: (item[1].weighted_volume, item[0]))[1]
    return replace(
        best,
        unsupported_primitives=_unsupported_paper_primitives_for_subset(requested),
    )


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
    if primitive_type == "cylinder":
        return _fit_cylinder(points, axes, source_faces)
    if primitive_type == "cone":
        return _fit_cone(points, axes, source_faces)
    if primitive_type == "ellipsoid":
        return _fit_ellipsoid(points, axes, source_faces)
    if primitive_type == "capped_cylinder":
        return _fit_capped_cylinder(points, axes, source_faces)
    raise ValueError(f"unsupported primitive type: {primitive_type}")


def _unsupported_paper_primitives_for_subset(requested: tuple[str, ...]) -> tuple[str, ...]:
    requested_set = set(requested)
    supported_set = set(SUPPORTED_PRIMITIVES)
    return tuple(
        primitive
        for primitive in PAPER_SCOPE_PRIMITIVES
        if primitive not in requested_set or primitive not in supported_set
    )


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
    axis_index, axis, center, half_height, radius = _axis_span_radial_parameters(points, axes)
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


def _fit_cylinder(
    points: NDArray[np.float64],
    axes: NDArray[np.float64],
    source_faces: tuple[int, ...],
) -> PrimitiveFit:
    axis_index, axis, center, half_height, radius = _axis_span_radial_parameters(points, axes)
    volume = float(pi * radius**2 * (half_height * 2.0))
    contains = bool(_cylinder_contains(points, axis, center, half_height, radius))
    return PrimitiveFit(
        primitive_type="cylinder",
        source_faces=source_faces,
        center=_vector_to_tuple(center),
        axes=_axes_to_tuple(axes),
        dimensions={"radius": radius, "half_height": half_height, "axis_index": axis_index},
        volume=volume,
        weighted_volume=volume,
        contains_assigned_points=contains,
    )


def _fit_cone(
    points: NDArray[np.float64],
    axes: NDArray[np.float64],
    source_faces: tuple[int, ...],
) -> PrimitiveFit:
    local = points @ axes
    spans = local.max(axis=0) - local.min(axis=0)
    axis_index = int(np.argmax(spans))
    candidates = (
        _fit_cone_with_axis_direction(points, axes, source_faces, axis_index, 1.0),
        _fit_cone_with_axis_direction(points, axes, source_faces, axis_index, -1.0),
    )
    return min(candidates, key=lambda fit: fit.weighted_volume)


def _fit_cone_with_axis_direction(
    points: NDArray[np.float64],
    axes: NDArray[np.float64],
    source_faces: tuple[int, ...],
    axis_index: int,
    direction: float,
) -> PrimitiveFit:
    directed_axes = np.array(axes, dtype=np.float64, copy=True)
    if direction < 0.0:
        directed_axes[:, axis_index] *= -1.0
        directed_axes[:, (axis_index + 1) % 3] *= -1.0
    axis = directed_axes[:, axis_index]
    projections = points @ axis
    projection_min = float(projections.min())
    projection_max = float(projections.max())
    projection_span = max(projection_max - projection_min, MIN_DIMENSION * 2.0)
    centroid = points.mean(axis=0)
    perpendicular_center = centroid - axis * float(centroid @ axis)
    radial_vectors = points - perpendicular_center - np.outer(projections, axis)
    radial_distances = np.linalg.norm(radial_vectors, axis=1)
    min_plane_radial = radial_distances[
        np.abs(projections - projection_min) <= CONTAINMENT_TOLERANCE
    ]
    apex_padding = (
        max(projection_span * 0.05, MIN_DIMENSION)
        if min_plane_radial.size and float(min_plane_radial.max(initial=0.0)) > CONTAINMENT_TOLERANCE
        else 0.0
    )
    apex_projection = projection_min - apex_padding
    base_projection = projection_max
    height = max(base_projection - apex_projection, MIN_DIMENSION * 2.0)
    half_height = height * 0.5
    center_projection = (apex_projection + base_projection) * 0.5
    center = perpendicular_center + axis * center_projection
    apex_to_point = np.clip((projections - apex_projection) / height, 0.0, 1.0)
    radius = MIN_DIMENSION
    for radial_distance, t in zip(radial_distances, apex_to_point):
        if t <= CONTAINMENT_TOLERANCE:
            radius = max(radius, float(radial_distance / MIN_DIMENSION))
            continue
        radius = max(radius, float(radial_distance / t))
    volume = float((1.0 / 3.0) * pi * radius**2 * height)
    contains = bool(_cone_contains(points, axis, center, half_height, radius))
    return PrimitiveFit(
        primitive_type="cone",
        source_faces=source_faces,
        center=_vector_to_tuple(center),
        axes=_axes_to_tuple(directed_axes),
        dimensions={
            "radius": radius,
            "half_height": half_height,
            "axis_index": axis_index,
            "fit_model": "right_circular_cone_axis_span_proxy",
        },
        volume=volume,
        weighted_volume=volume,
        contains_assigned_points=contains,
    )


def _fit_ellipsoid(
    points: NDArray[np.float64],
    axes: NDArray[np.float64],
    source_faces: tuple[int, ...],
) -> PrimitiveFit:
    local = points @ axes
    local_min = local.min(axis=0)
    local_max = local.max(axis=0)
    local_center = (local_min + local_max) * 0.5
    radii = np.maximum((local_max - local_min) * 0.5, MIN_DIMENSION)
    normalized_offsets = (local - local_center) / radii
    scale = max(float(np.linalg.norm(normalized_offsets, axis=1).max(initial=0.0)), 1.0)
    radii = radii * scale
    center = axes @ local_center
    volume = float((4.0 / 3.0) * pi * np.prod(radii))
    contains = bool(
        np.all(np.sum(((local - local_center) / radii) ** 2, axis=1) <= 1.0 + CONTAINMENT_TOLERANCE)
    )
    return PrimitiveFit(
        primitive_type="ellipsoid",
        source_faces=source_faces,
        center=_vector_to_tuple(center),
        axes=_axes_to_tuple(axes),
        dimensions={"radii": [float(value) for value in radii]},
        volume=volume,
        weighted_volume=volume,
        contains_assigned_points=contains,
    )


def _fit_capped_cylinder(
    points: NDArray[np.float64],
    axes: NDArray[np.float64],
    source_faces: tuple[int, ...],
) -> PrimitiveFit:
    axis_index, axis, center, half_height, radius = _axis_span_radial_parameters(points, axes)
    cylinder_length = half_height * 2.0
    volume = float(pi * radius**2 * cylinder_length + (4.0 / 3.0) * pi * radius**3)
    contains = bool(_capsule_contains(points, axis, center, half_height, radius))
    return PrimitiveFit(
        primitive_type="capped_cylinder",
        source_faces=source_faces,
        center=_vector_to_tuple(center),
        axes=_axes_to_tuple(axes),
        dimensions={
            "radius": radius,
            "half_height": half_height,
            "axis_index": axis_index,
            "cap_model": "hemisphere_caps",
            "proxy_fit": "axis_span_radial_proxy",
        },
        volume=volume,
        weighted_volume=volume,
        contains_assigned_points=contains,
    )


def _axis_span_radial_parameters(
    points: NDArray[np.float64],
    axes: NDArray[np.float64],
) -> tuple[int, NDArray[np.float64], NDArray[np.float64], float, float]:
    local = points @ axes
    spans = local.max(axis=0) - local.min(axis=0)
    axis_index = int(np.argmax(spans))
    axis = axes[:, axis_index]
    projections = points @ axis
    projection_min = float(projections.min())
    projection_max = float(projections.max())
    center_projection = (projection_min + projection_max) * 0.5
    centroid = points.mean(axis=0)
    perpendicular_center = centroid - axis * float(centroid @ axis)
    center = perpendicular_center + axis * center_projection
    axial_offsets = np.outer(projections - center_projection, axis)
    radial_vectors = points - center - axial_offsets
    radial_distances = np.linalg.norm(radial_vectors, axis=1)
    radius = max(float(radial_distances.max(initial=0.0)), MIN_DIMENSION)
    half_height = max((projection_max - projection_min) * 0.5, MIN_DIMENSION)
    return axis_index, axis, center, half_height, radius


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


def _cylinder_contains(
    points: NDArray[np.float64],
    axis: NDArray[np.float64],
    center: NDArray[np.float64],
    half_height: float,
    radius: float,
) -> bool:
    relative = points - center
    projected = relative @ axis
    radial_vectors = relative - np.outer(projected, axis)
    radial_distances = np.linalg.norm(radial_vectors, axis=1)
    return bool(
        np.all(np.abs(projected) <= half_height + CONTAINMENT_TOLERANCE)
        and np.all(radial_distances <= radius + CONTAINMENT_TOLERANCE)
    )


def _cone_contains(
    points: NDArray[np.float64],
    axis: NDArray[np.float64],
    center: NDArray[np.float64],
    half_height: float,
    radius: float,
) -> bool:
    relative = points - center
    projected = relative @ axis
    radial_vectors = relative - np.outer(projected, axis)
    radial_distances = np.linalg.norm(radial_vectors, axis=1)
    height = max(half_height * 2.0, MIN_DIMENSION)
    apex_to_point = (projected + half_height) / height
    allowed_radius = np.clip(apex_to_point, 0.0, 1.0) * radius
    return bool(
        np.all(projected >= -half_height - CONTAINMENT_TOLERANCE)
        and np.all(projected <= half_height + CONTAINMENT_TOLERANCE)
        and np.all(radial_distances <= allowed_radius + CONTAINMENT_TOLERANCE)
    )


def _vector_to_tuple(vector: NDArray[np.float64]) -> tuple[float, float, float]:
    return tuple(float(value) for value in vector)


def _axes_to_tuple(axes: NDArray[np.float64]) -> tuple[tuple[float, float, float], ...]:
    return tuple(_vector_to_tuple(axes[:, index]) for index in range(axes.shape[1]))
