from __future__ import annotations

from typing import Any

from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.reports.schema import NewtonShapeMapping

SUPPORTED_NEWTON_SHAPES = ("box", "sphere", "capsule")
IDENTITY_AXES = (
    (1.0, 0.0, 0.0),
    (0.0, 1.0, 0.0),
    (0.0, 0.0, 1.0),
)


def map_package_shapes(package: CollisionPackage) -> tuple[NewtonShapeMapping, ...]:
    return tuple(_map_primitive(primitive) for primitive in package.primitives)


def _map_primitive(primitive: PrimitiveSpec) -> NewtonShapeMapping:
    dimensions = _dimension_mapping(primitive.dimensions)
    if primitive.kind not in SUPPORTED_NEWTON_SHAPES:
        return _gap(primitive, dimensions, f"unsupported primitive kind: {primitive.kind}")
    if primitive.kind == "box":
        detail = _validate_box(dimensions)
    elif primitive.kind == "sphere":
        detail = _validate_sphere(dimensions)
    else:
        detail = _validate_capsule(dimensions)
    if detail:
        return _gap(primitive, dimensions, detail)
    return NewtonShapeMapping(
        primitive_id=primitive.primitive_id,
        kind=primitive.kind,
        status="mapped",
        detail="mapped",
        center=primitive.center,
        axes=primitive.axes or IDENTITY_AXES,
        dimensions=dimensions,
    )


def _dimension_mapping(value: tuple[float, ...] | dict[str, Any]) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    return {"values": list(value)}


def _validate_box(dimensions: dict[str, Any]) -> str:
    half_extents = dimensions.get("half_extents")
    if not isinstance(half_extents, list | tuple) or len(half_extents) != 3:
        return "box half_extents must contain three positive values"
    if any(_as_positive_float(value) is None for value in half_extents):
        return "box half_extents must contain three positive values"
    return ""


def _validate_sphere(dimensions: dict[str, Any]) -> str:
    if _as_positive_float(dimensions.get("radius")) is None:
        return "sphere radius is required and must be positive"
    return ""


def _validate_capsule(dimensions: dict[str, Any]) -> str:
    if _as_positive_float(dimensions.get("radius")) is None:
        return "capsule radius is required and must be positive"
    if _as_non_negative_float(dimensions.get("half_height")) is None:
        return "capsule half_height is required and must be non-negative"
    axis_index = dimensions.get("axis_index", 2)
    if axis_index not in (0, 1, 2):
        return "capsule axis_index must be 0, 1, or 2"
    return ""


def _as_positive_float(value: object) -> float | None:
    try:
        result = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    if result <= 0.0:
        return None
    return result


def _as_non_negative_float(value: object) -> float | None:
    try:
        result = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    if result < 0.0:
        return None
    return result


def _gap(
    primitive: PrimitiveSpec,
    dimensions: dict[str, Any],
    detail: str,
) -> NewtonShapeMapping:
    return NewtonShapeMapping(
        primitive_id=primitive.primitive_id,
        kind=primitive.kind,
        status="mapping_gap",
        detail=detail,
        center=primitive.center,
        axes=primitive.axes or IDENTITY_AXES,
        dimensions=dimensions,
    )
