from __future__ import annotations

import importlib
import sys
from collections import Counter
from pathlib import Path
from types import ModuleType
from typing import Any

import numpy as np

from primitive_collision_compiler.contracts import CollisionPackage
from primitive_collision_compiler.newton.env import (
    _clear_newton_modules,
    _is_relative_to,
    _snapshot_newton_modules,
    inspect_newton_environment,
)
from primitive_collision_compiler.newton.shapes import map_package_shapes
from primitive_collision_compiler.reports.schema import (
    EnvironmentCheck,
    EnvironmentReport,
    NewtonContactCanary,
    NewtonDiagnosticReport,
    NewtonShapeMapping,
)

CONTACT_CLAIM_BOUNDARY = "contact_canary_only_not_collision_quality"


def run_newton_contact_smoke(
    package: CollisionPackage,
    *,
    source_dir: str,
    device: str = "cpu",
    claim_boundary: str = CONTACT_CLAIM_BOUNDARY,
) -> NewtonDiagnosticReport:
    mappings = map_package_shapes(package)
    mapped = tuple(mapping for mapping in mappings if mapping.status == "mapped")
    type_counts = dict(Counter(primitive.kind for primitive in package.primitives))
    if not mapped:
        return _report(
            package,
            status="mapping_gap",
            device=device,
            environment=None,
            type_counts=type_counts,
            mappings=mappings,
            canaries=(),
            claim_boundary=claim_boundary,
            fallback_reason="no_newton_mappable_primitives",
        )

    environment = inspect_newton_environment(source_dir)
    if environment.status != "smoke_passed":
        status = _status_from_environment(environment.status)
        return _report(
            package,
            status=status,
            device=device,
            environment=environment,
            type_counts=type_counts,
            mappings=mappings,
            canaries=(),
            claim_boundary=claim_boundary,
            fallback_reason=environment.status,
        )

    runtime = _import_newton_runtime(source_dir)
    if runtime.status != "smoke_passed":
        return _report(
            package,
            status=runtime.status,
            device=device,
            environment=runtime.environment,
            type_counts=type_counts,
            mappings=mappings,
            canaries=(),
            claim_boundary=claim_boundary,
            fallback_reason=runtime.environment.status,
        )

    try:
        canaries = tuple(
            _run_contact_canary(mapping, runtime.newton, runtime.warp, device)
            for mapping in _representative_mappings(mapped)
        )
    except Exception as exc:
        canaries = (
            NewtonContactCanary(
                primitive_id="runtime",
                kind="runtime",
                status="runtime_failure",
                contact_count=0,
                detail=f"{type(exc).__name__}: {exc}",
            ),
        )
    status = (
        "smoke_passed"
        if canaries and all(c.status == "smoke_passed" for c in canaries)
        else "runtime_failure"
    )
    return _report(
        package,
        status=status,
        device=device,
        environment=environment,
        type_counts=type_counts,
        mappings=mappings,
        canaries=canaries,
        claim_boundary=claim_boundary,
        fallback_reason=None if status == "smoke_passed" else "contact_canary_failed",
    )


class _Runtime:
    def __init__(
        self,
        status: str,
        environment: EnvironmentReport,
        newton: ModuleType | None = None,
        warp: ModuleType | None = None,
    ):
        self.status = status
        self.environment = environment
        self.newton = newton
        self.warp = warp


def _import_newton_runtime(source_dir: str) -> _Runtime:
    source_path = Path(source_dir)
    source_str = str(source_path)
    source_resolved = source_path.resolve()
    inserted = False
    original_modules = _snapshot_newton_modules()
    _clear_newton_modules()
    if not source_path.exists():
        environment = _runtime_environment(
            source_dir,
            "dependency_gap",
            "source_dir does not exist",
        )
        _restore_newton_modules(original_modules)
        return _Runtime("dependency_gap", environment)
    if source_path.exists():
        sys.path.insert(0, source_str)
        inserted = True
    try:
        warp = importlib.import_module("warp")
        newton = importlib.import_module("newton")
        module_file = getattr(newton, "__file__", None)
        if not module_file or not _is_relative_to(Path(module_file), source_resolved):
            _restore_newton_modules(original_modules)
            environment = _runtime_environment(
                source_dir,
                "runtime_failure",
                f"newton runtime resolved outside source_dir: {module_file}",
            )
            return _Runtime("runtime_failure", environment)
    except ModuleNotFoundError as exc:
        _restore_newton_modules(original_modules)
        environment = _runtime_environment(source_dir, "dependency_gap", str(exc))
        return _Runtime("dependency_gap", environment)
    except Exception as exc:
        _restore_newton_modules(original_modules)
        environment = _runtime_environment(
            source_dir,
            "runtime_failure",
            f"{type(exc).__name__}: {exc}",
        )
        return _Runtime("runtime_failure", environment)
    finally:
        if inserted:
            try:
                sys.path.remove(source_str)
            except ValueError:
                pass

    return _Runtime(
        "smoke_passed",
        _runtime_environment(source_dir, "smoke_passed", "newton and warp imported"),
        newton=newton,
        warp=warp,
    )


def _runtime_environment(source_dir: str, status: str, detail: str) -> EnvironmentReport:
    return EnvironmentReport(
        stage="newton_runtime_import",
        status=status,
        source_dir=source_dir,
        source_commit=None,
        checks=(EnvironmentCheck("newton_runtime_import", status, detail),),
    )


def _restore_newton_modules(modules: dict[str, object]) -> None:
    _clear_newton_modules()
    sys.modules.update(modules)


def _status_from_environment(status: str) -> str:
    if status in {"missing_source", "dependency_gap"}:
        return "dependency_gap"
    if status == "import_error":
        return "runtime_failure"
    return status


def _representative_mappings(
    mappings: tuple[NewtonShapeMapping, ...],
) -> tuple[NewtonShapeMapping, ...]:
    representatives: dict[str, NewtonShapeMapping] = {}
    for mapping in mappings:
        representatives.setdefault(mapping.kind, mapping)
    return tuple(representatives[kind] for kind in sorted(representatives))


def _run_contact_canary(
    mapping: NewtonShapeMapping,
    newton: ModuleType | None,
    wp: ModuleType | None,
    device: str,
) -> NewtonContactCanary:
    if newton is None or wp is None:
        return NewtonContactCanary(
            mapping.primitive_id,
            mapping.kind,
            "dependency_gap",
            0,
            "newton runtime missing",
        )

    with wp.ScopedDevice(device):
        builder = newton.ModelBuilder(gravity=0.0)
        _add_static_shape(builder, mapping, wp)
        probe_body = builder.add_body(
            xform=wp.transform(_wp_vec3(wp, mapping.center), wp.quat_identity())
        )
        builder.add_shape_sphere(body=probe_body, radius=_probe_radius(mapping))
        model = builder.finalize(device=device)
        pipeline = newton.CollisionPipeline(model)
        contacts = pipeline.contacts()
        state = model.state()
        pipeline.collide(state, contacts)
        contact_count = int(contacts.rigid_contact_count.numpy()[0])

    status = "smoke_passed" if contact_count > 0 else "runtime_failure"
    detail = (
        "representative contact canary produced; not full package coverage"
        if contact_count > 0
        else "representative contact canary produced no contact"
    )
    return NewtonContactCanary(mapping.primitive_id, mapping.kind, status, contact_count, detail)


def _add_static_shape(builder: Any, mapping: NewtonShapeMapping, wp: ModuleType) -> None:
    xform = wp.transform(_wp_vec3(wp, mapping.center), _shape_quat(mapping, wp))
    dimensions = mapping.dimensions
    if mapping.kind == "box":
        hx, hy, hz = (float(value) for value in dimensions["half_extents"])
        builder.add_shape_box(body=-1, xform=xform, hx=hx, hy=hy, hz=hz)
    elif mapping.kind == "sphere":
        builder.add_shape_sphere(body=-1, xform=xform, radius=float(dimensions["radius"]))
    elif mapping.kind == "capsule":
        builder.add_shape_capsule(
            body=-1,
            xform=xform,
            radius=float(dimensions["radius"]),
            half_height=float(dimensions["half_height"]),
        )
    elif mapping.kind == "cylinder":
        builder.add_shape_cylinder(
            body=-1,
            xform=xform,
            radius=float(dimensions["radius"]),
            half_height=float(dimensions["half_height"]),
        )
    elif mapping.kind == "cone":
        builder.add_shape_cone(
            body=-1,
            xform=xform,
            radius=float(dimensions["radius"]),
            half_height=float(dimensions["half_height"]),
        )
    elif mapping.kind == "ellipsoid":
        rx, ry, rz = (float(value) for value in dimensions["radii"])
        builder.add_shape_ellipsoid(body=-1, xform=xform, rx=rx, ry=ry, rz=rz)
    else:
        raise ValueError(f"unsupported mapped primitive kind: {mapping.kind}")


def _shape_quat(mapping: NewtonShapeMapping, wp: ModuleType):
    axes = mapping.axes
    if mapping.kind in {"capsule", "cylinder", "cone"}:
        axes = _axis_shape_axes(mapping)
    matrix = wp.matrix_from_cols(*(_wp_vec3(wp, axis) for axis in axes))
    return wp.quat_from_matrix(matrix)


def _axis_shape_axes(mapping: NewtonShapeMapping) -> tuple[tuple[float, float, float], ...]:
    axes = np.asarray(mapping.axes, dtype=float)
    axis_index = int(mapping.dimensions.get("axis_index", 2))
    z_axis = _normalize(axes[axis_index])
    seed = axes[(axis_index + 1) % 3]
    y_axis = _normalize(np.cross(z_axis, seed))
    if np.linalg.norm(y_axis) == 0.0:
        y_axis = np.array([0.0, 1.0, 0.0])
    x_axis = _normalize(np.cross(y_axis, z_axis))
    return (_tuple(x_axis), _tuple(y_axis), _tuple(z_axis))


def _probe_radius(mapping: NewtonShapeMapping) -> float:
    dimensions = mapping.dimensions
    if mapping.kind == "sphere":
        return max(float(dimensions["radius"]) * 0.5, 1e-3)
    if mapping.kind in {"capsule", "cylinder", "cone"}:
        return max(float(dimensions["radius"]) * 0.5, 1e-3)
    if mapping.kind == "ellipsoid":
        return max(min(float(value) for value in dimensions["radii"]) * 0.5, 1e-3)
    half_extents = [float(value) for value in dimensions["half_extents"]]
    return max(min(half_extents) * 0.5, 1e-3)


def _report(
    package: CollisionPackage,
    *,
    status: str,
    device: str,
    environment: EnvironmentReport | None,
    type_counts: dict[str, int],
    mappings: tuple[NewtonShapeMapping, ...],
    canaries: tuple[NewtonContactCanary, ...],
    claim_boundary: str,
    fallback_reason: str | None,
) -> NewtonDiagnosticReport:
    return NewtonDiagnosticReport(
        stage="newton_contact_smoke",
        status=status,
        asset_id=package.asset_id,
        package_id=package.package_id,
        probe_type="contact_canary",
        device=device,
        environment=environment,
        primitive_count=len(package.primitives),
        type_counts=type_counts,
        shape_mappings=mappings,
        contact_canaries=canaries,
        claim_boundary=claim_boundary,
        metrics=_contact_smoke_metrics(mappings, canaries),
        fallback_reason=fallback_reason,
    )


def _wp_vec3(wp: ModuleType, values: tuple[float, float, float]):
    return wp.vec3(float(values[0]), float(values[1]), float(values[2]))


def _normalize(vector: np.ndarray) -> np.ndarray:
    norm = float(np.linalg.norm(vector))
    if norm == 0.0:
        return vector
    return vector / norm


def _tuple(vector: np.ndarray) -> tuple[float, float, float]:
    return (float(vector[0]), float(vector[1]), float(vector[2]))


def _contact_smoke_metrics(
    mappings: tuple[NewtonShapeMapping, ...],
    canaries: tuple[NewtonContactCanary, ...],
) -> dict[str, object]:
    mapped = tuple(mapping for mapping in mappings if mapping.status == "mapped")
    return {
        "contact_canary_scope": "one_representative_per_mapped_type",
        "full_package_contact_coverage": False,
        "mapped_primitive_count": len(mapped),
        "mapped_type_count": len({mapping.kind for mapping in mapped}),
        "representative_canary_count": len(canaries),
    }
