from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import math
from numbers import Integral
from types import ModuleType
from typing import Any

import numpy as np

from primitive_collision_compiler.contracts import CollisionPackage
from primitive_collision_compiler.newton.diagnostics import (
    _import_newton_runtime,
    _shape_quat,
    _status_from_environment,
    _wp_vec3,
)
from primitive_collision_compiler.newton.drop_settle import _world_half_extents
from primitive_collision_compiler.newton.env import inspect_newton_environment
from primitive_collision_compiler.newton.shapes import map_package_shapes
from primitive_collision_compiler.reports.schema import (
    EnvironmentReport,
    NewtonDiagnosticReport,
    NewtonShapeMapping,
    NewtonSphereRainRun,
)

SPHERE_RAIN_CLAIM_BOUNDARY = "sphere_rain_task_smoke_not_collision_quality_or_safety"
SPHERE_RAIN_EVIDENCE_LEVEL = "newton_sphere_rain_task_smoke"
SPHERE_RAIN_TASK_SCOPE = "single_asset_sphere_rain_static_package"


@dataclass(frozen=True)
class SphereRainOptions:
    sphere_count_x: int = 3
    sphere_count_y: int = 3
    sphere_radius_m: float = 0.5
    spawn_height_m: float = 2.0
    grid_spacing_m: float | None = None
    frames: int = 240
    substeps: int = 4
    frame_dt_seconds: float = 1.0 / 60.0
    iterations: int = 4
    gravity_mps2: float = -9.81
    friction: float = 0.5
    min_contact_density: float = 0.05
    require_final_contact: bool = False
    rigid_contact_max: int = 4096

    def __post_init__(self) -> None:
        _positive_int(self.sphere_count_x, "sphere_count_x")
        _positive_int(self.sphere_count_y, "sphere_count_y")
        _positive_float(self.sphere_radius_m, "sphere_radius_m")
        _non_negative_float(self.spawn_height_m, "spawn_height_m")
        if self.grid_spacing_m is not None:
            _positive_float(self.grid_spacing_m, "grid_spacing_m")
        _positive_int(self.frames, "frames")
        _positive_int(self.substeps, "substeps")
        _positive_float(self.frame_dt_seconds, "frame_dt_seconds")
        _positive_int(self.iterations, "iterations")
        _finite_float(self.gravity_mps2, "gravity_mps2")
        _non_negative_float(self.friction, "friction")
        _non_negative_float(self.min_contact_density, "min_contact_density")
        _positive_int(self.rigid_contact_max, "rigid_contact_max")

    @property
    def sphere_count(self) -> int:
        return self.sphere_count_x * self.sphere_count_y

    @property
    def step_dt_seconds(self) -> float:
        return self.frame_dt_seconds / self.substeps

    @property
    def total_steps(self) -> int:
        return self.frames * self.substeps

    @property
    def grid_spacing(self) -> float:
        return self.grid_spacing_m if self.grid_spacing_m is not None else self.sphere_radius_m * 2.5

    def to_solver_dict(self) -> dict[str, object]:
        return {
            "solver": "xpbd",
            "frames": self.frames,
            "substeps": self.substeps,
            "frame_dt_seconds": self.frame_dt_seconds,
            "step_dt_seconds": self.step_dt_seconds,
            "iterations": self.iterations,
            "gravity_mps2": self.gravity_mps2,
            "device_default": "cpu",
            "rigid_contact_max": self.rigid_contact_max,
            "broad_phase": "nxn",
            "deterministic": True,
        }

    def to_initial_conditions(self) -> dict[str, object]:
        return {
            "sphere_count_x": self.sphere_count_x,
            "sphere_count_y": self.sphere_count_y,
            "sphere_count": self.sphere_count,
            "sphere_radius_m": self.sphere_radius_m,
            "spawn_height_m": self.spawn_height_m,
            "grid_spacing_m": self.grid_spacing,
            "initial_velocity_mps": [0.0, 0.0, 0.0],
            "min_contact_density": self.min_contact_density,
            "require_final_contact": self.require_final_contact,
        }


def run_newton_sphere_rain(
    package: CollisionPackage,
    *,
    source_dir: str,
    device: str = "cpu",
    options: SphereRainOptions | None = None,
    claim_boundary: str = SPHERE_RAIN_CLAIM_BOUNDARY,
) -> NewtonDiagnosticReport:
    options = options or SphereRainOptions()
    mappings = map_package_shapes(package)
    mapped = tuple(mapping for mapping in mappings if mapping.status == "mapped")
    type_counts = dict(Counter(primitive.kind for primitive in package.primitives))

    if len(mapped) != len(package.primitives) or not mapped:
        return _sphere_rain_report(
            package,
            status="mapping_gap",
            device=device,
            environment=None,
            type_counts=type_counts,
            mappings=mappings,
            runs=(),
            options=options,
            claim_boundary=claim_boundary,
            fallback_reason="full_package_shape_coverage_required",
        )

    environment = inspect_newton_environment(source_dir)
    if environment.status != "smoke_passed":
        return _sphere_rain_report(
            package,
            status=_status_from_environment(environment.status),
            device=device,
            environment=environment,
            type_counts=type_counts,
            mappings=mappings,
            runs=(),
            options=options,
            claim_boundary=claim_boundary,
            fallback_reason=environment.status,
        )

    runtime = _import_newton_runtime(source_dir)
    if runtime.status != "smoke_passed":
        return _sphere_rain_report(
            package,
            status=runtime.status,
            device=device,
            environment=runtime.environment,
            type_counts=type_counts,
            mappings=mappings,
            runs=(),
            options=options,
            claim_boundary=claim_boundary,
            fallback_reason=runtime.environment.status,
        )

    try:
        run = _run_sphere_rain(mapped, runtime.newton, runtime.warp, device, options)
        runs = (run,)
        status = "smoke_passed" if run.status == "smoke_passed" else "runtime_failure"
        fallback_reason = None if status == "smoke_passed" else "sphere_rain_failed"
    except Exception as exc:
        run = NewtonSphereRainRun(
            run_id="seed0",
            status="runtime_failure",
            primitive_ids=tuple(mapping.primitive_id for mapping in mapped),
            sphere_count=options.sphere_count,
            completed_steps=0,
            initial_min_height=float("nan"),
            final_min_height=float("nan"),
            min_height=float("nan"),
            max_contact_count=0,
            final_contact_count=0,
            max_contacted_probe_count=0,
            final_contacted_probe_count=0,
            contact_density=0.0,
            finite_state=False,
            contact_observed=False,
            final_contact_observed=False,
            failure_labels=(f"runtime_exception_{type(exc).__name__}",),
            sphere_radius_m=options.sphere_radius_m,
            total_steps=options.total_steps,
        )
        runs = (run,)
        status = "runtime_failure"
        fallback_reason = f"{type(exc).__name__}: {exc}"

    return _sphere_rain_report(
        package,
        status=status,
        device=device,
        environment=environment,
        type_counts=type_counts,
        mappings=mappings,
        runs=runs,
        options=options,
        claim_boundary=claim_boundary,
        fallback_reason=fallback_reason,
    )


def evaluate_sphere_rain_trace(
    *,
    primitive_ids: tuple[str, ...],
    sphere_count: int,
    completed_steps: int,
    initial_min_height: float,
    final_min_height: float,
    min_height: float,
    max_contact_count: int,
    final_contact_count: int,
    finite_state: bool,
    max_contacted_probe_count: int | None = None,
    final_contacted_probe_count: int | None = None,
    min_contact_density: float = 0.05,
    require_final_contact: bool = False,
    run_id: str = "seed0",
    sphere_radius_m: float | None = None,
    total_steps: int | None = None,
    contact_count_trace: tuple[int, ...] = (),
) -> NewtonSphereRainRun:
    contacted_probe_count = 0 if max_contacted_probe_count is None else int(max_contacted_probe_count)
    final_contacted_probe_count = (
        0 if final_contacted_probe_count is None else int(final_contacted_probe_count)
    )
    contact_observed = bool(max_contact_count > 0 or contacted_probe_count > 0)
    final_contact_observed = bool(final_contact_count > 0 or final_contacted_probe_count > 0)
    contact_density = float(contacted_probe_count / sphere_count) if sphere_count > 0 else 0.0
    labels: list[str] = []
    if sphere_count < 1:
        labels.append("no_probe_spheres")
    if not finite_state:
        labels.append("non_finite_state")
    if not contact_observed:
        labels.append("no_contact_observed")
    if require_final_contact and not final_contact_observed:
        labels.append("no_final_contact")
    if contact_density < min_contact_density:
        labels.append("insufficient_contact_density")
    status = "smoke_passed" if not labels else "runtime_failure"
    return NewtonSphereRainRun(
        run_id=run_id,
        status=status,
        primitive_ids=primitive_ids,
        sphere_count=int(sphere_count),
        completed_steps=int(completed_steps),
        initial_min_height=float(initial_min_height),
        final_min_height=float(final_min_height),
        min_height=float(min_height),
        max_contact_count=int(max_contact_count),
        final_contact_count=int(final_contact_count),
        max_contacted_probe_count=contacted_probe_count,
        final_contacted_probe_count=final_contacted_probe_count,
        contact_density=contact_density,
        finite_state=bool(finite_state),
        contact_observed=contact_observed,
        final_contact_observed=final_contact_observed,
        failure_labels=tuple(labels),
        sphere_radius_m=None if sphere_radius_m is None else float(sphere_radius_m),
        total_steps=total_steps,
        package_contact_count_p95=_p95(contact_count_trace) if contact_count_trace else None,
    )


def _run_sphere_rain(
    mappings: tuple[NewtonShapeMapping, ...],
    newton: ModuleType | None,
    wp: ModuleType | None,
    device: str,
    options: SphereRainOptions,
) -> NewtonSphereRainRun:
    if newton is None or wp is None:
        return evaluate_sphere_rain_trace(
            primitive_ids=tuple(mapping.primitive_id for mapping in mappings),
            sphere_count=options.sphere_count,
            completed_steps=0,
            initial_min_height=float("nan"),
            final_min_height=float("nan"),
            min_height=float("nan"),
            max_contact_count=0,
            final_contact_count=0,
            finite_state=False,
            sphere_radius_m=options.sphere_radius_m,
            total_steps=options.total_steps,
        )

    bounds_min, bounds_max = _package_bounds(mappings)
    spawn_points = _spawn_points(bounds_min, bounds_max, options)
    primitive_ids = tuple(mapping.primitive_id for mapping in mappings)

    with wp.ScopedDevice(device):
        builder = newton.ModelBuilder(gravity=options.gravity_mps2, up_axis=newton.Axis.Z)
        builder.default_shape_cfg.mu = options.friction
        package_shape_ids = tuple(_add_static_shape(builder, mapping, wp) for mapping in mappings)
        sphere_shape_ids: list[int] = []
        sphere_bodies: list[int] = []
        for index, point in enumerate(spawn_points):
            body = builder.add_body(
                xform=wp.transform(_wp_vec3(wp, point), wp.quat_identity()),
                label=f"sphere_rain_{index}",
            )
            shape = builder.add_shape_sphere(
                body=body,
                radius=options.sphere_radius_m,
                label=f"sphere_rain_{index}",
            )
            sphere_bodies.append(body)
            sphere_shape_ids.append(shape)
        for left_index, left_shape in enumerate(sphere_shape_ids):
            for right_shape in sphere_shape_ids[left_index + 1 :]:
                builder.add_shape_collision_filter_pair(left_shape, right_shape)

        model = builder.finalize(device=device)
        pipeline = newton.CollisionPipeline(
            model,
            broad_phase="nxn",
            deterministic=True,
            rigid_contact_max=options.rigid_contact_max,
        )
        solver = newton.solvers.SolverXPBD(model, iterations=options.iterations)
        state_0 = model.state()
        state_1 = model.state()
        control = model.control()
        contacts = pipeline.contacts()

        initial_heights = state_0.body_q.numpy()[sphere_bodies, 2]
        initial_min_height = float(np.min(initial_heights))
        final_min_height = initial_min_height
        min_height = initial_min_height
        max_contact_count = 0
        final_contact_count = 0
        max_contacted_probe_count = 0
        final_contacted_probe_count = 0
        completed_steps = 0
        finite_state = True
        contact_count_trace: list[int] = []
        package_shapes = set(int(shape_id) for shape_id in package_shape_ids)
        probe_shapes = set(int(shape_id) for shape_id in sphere_shape_ids)

        for _ in range(options.frames):
            for _ in range(options.substeps):
                state_0.clear_forces()
                pipeline.collide(state_0, contacts)
                package_contact_count, contacted_probe_count = _package_contact_metrics(
                    contacts,
                    package_shapes,
                    probe_shapes,
                )
                contact_count_trace.append(package_contact_count)
                max_contact_count = max(max_contact_count, package_contact_count)
                max_contacted_probe_count = max(max_contacted_probe_count, contacted_probe_count)
                solver.step(state_0, state_1, control, contacts, options.step_dt_seconds)
                state_0, state_1 = state_1, state_0
                completed_steps += 1
                body_q = state_0.body_q.numpy()
                body_qd = state_0.body_qd.numpy()
                sphere_heights = body_q[sphere_bodies, 2]
                final_min_height = float(np.min(sphere_heights))
                min_height = min(min_height, final_min_height)
                if not np.all(np.isfinite(body_q)) or not np.all(np.isfinite(body_qd)):
                    finite_state = False
                    break
            if not finite_state:
                break

        pipeline.collide(state_0, contacts)
        final_contact_count, final_contacted_probe_count = _package_contact_metrics(
            contacts,
            package_shapes,
            probe_shapes,
        )
        max_contact_count = max(max_contact_count, final_contact_count)
        max_contacted_probe_count = max(max_contacted_probe_count, final_contacted_probe_count)
        contact_count_trace.append(final_contact_count)

    return evaluate_sphere_rain_trace(
        primitive_ids=primitive_ids,
        sphere_count=options.sphere_count,
        completed_steps=completed_steps,
        initial_min_height=initial_min_height,
        final_min_height=final_min_height,
        min_height=min_height,
        max_contact_count=max_contact_count,
        final_contact_count=final_contact_count,
        finite_state=finite_state,
        max_contacted_probe_count=max_contacted_probe_count,
        final_contacted_probe_count=final_contacted_probe_count,
        min_contact_density=options.min_contact_density,
        require_final_contact=options.require_final_contact,
        sphere_radius_m=options.sphere_radius_m,
        total_steps=options.total_steps,
        contact_count_trace=tuple(contact_count_trace),
    )


def _add_static_shape(builder: Any, mapping: NewtonShapeMapping, wp: ModuleType) -> int:
    xform = wp.transform(_wp_vec3(wp, mapping.center), _shape_quat(mapping, wp))
    dimensions = mapping.dimensions
    if mapping.kind == "box":
        hx, hy, hz = (float(value) for value in dimensions["half_extents"])
        return int(builder.add_shape_box(body=-1, xform=xform, hx=hx, hy=hy, hz=hz))
    if mapping.kind == "sphere":
        return int(builder.add_shape_sphere(body=-1, xform=xform, radius=float(dimensions["radius"])))
    if mapping.kind == "capsule":
        return int(
            builder.add_shape_capsule(
                body=-1,
                xform=xform,
                radius=float(dimensions["radius"]),
                half_height=float(dimensions["half_height"]),
            )
        )
    if mapping.kind == "cylinder":
        return int(
            builder.add_shape_cylinder(
                body=-1,
                xform=xform,
                radius=float(dimensions["radius"]),
                half_height=float(dimensions["half_height"]),
            )
        )
    if mapping.kind == "cone":
        return int(
            builder.add_shape_cone(
                body=-1,
                xform=xform,
                radius=float(dimensions["radius"]),
                half_height=float(dimensions["half_height"]),
            )
        )
    if mapping.kind == "ellipsoid":
        rx, ry, rz = (float(value) for value in dimensions["radii"])
        return int(builder.add_shape_ellipsoid(body=-1, xform=xform, rx=rx, ry=ry, rz=rz))
    raise ValueError(f"unsupported mapped primitive kind: {mapping.kind}")


def _package_contact_metrics(
    contacts: Any,
    package_shapes: set[int],
    probe_shapes: set[int],
) -> tuple[int, int]:
    raw_count = int(contacts.rigid_contact_count.numpy()[0])
    count = min(raw_count, int(contacts.rigid_contact_max))
    if count <= 0:
        return 0, 0
    shape0 = contacts.rigid_contact_shape0.numpy()[:count]
    shape1 = contacts.rigid_contact_shape1.numpy()[:count]
    package_contacts = 0
    contacted_probes: set[int] = set()
    for left, right in zip(shape0, shape1):
        left_id = int(left)
        right_id = int(right)
        if left_id in package_shapes and right_id in probe_shapes:
            package_contacts += 1
            contacted_probes.add(right_id)
        elif right_id in package_shapes and left_id in probe_shapes:
            package_contacts += 1
            contacted_probes.add(left_id)
    return package_contacts, len(contacted_probes)


def _spawn_points(
    bounds_min: np.ndarray,
    bounds_max: np.ndarray,
    options: SphereRainOptions,
) -> tuple[tuple[float, float, float], ...]:
    center = (bounds_min + bounds_max) * 0.5
    spacing = options.grid_spacing
    x_values = _axis_positions(center[0], bounds_min[0], bounds_max[0], options.sphere_count_x, spacing)
    y_values = _axis_positions(center[1], bounds_min[1], bounds_max[1], options.sphere_count_y, spacing)
    z_value = float(bounds_max[2] + options.spawn_height_m + options.sphere_radius_m)
    return tuple((float(x), float(y), z_value) for x in x_values for y in y_values)


def _axis_positions(
    center: float,
    axis_min: float,
    axis_max: float,
    count: int,
    spacing: float,
) -> np.ndarray:
    if count == 1:
        return np.asarray([center], dtype=float)
    span = max(float(axis_max - axis_min), spacing * float(count - 1))
    return np.linspace(center - span * 0.5, center + span * 0.5, count)


def _package_bounds(mappings: tuple[NewtonShapeMapping, ...]) -> tuple[np.ndarray, np.ndarray]:
    mins = []
    maxs = []
    for mapping in mappings:
        center = np.asarray(mapping.center, dtype=float)
        half_extents = _world_half_extents(mapping)
        mins.append(center - half_extents)
        maxs.append(center + half_extents)
    return np.min(np.vstack(mins), axis=0), np.max(np.vstack(maxs), axis=0)


def _sphere_rain_report(
    package: CollisionPackage,
    *,
    status: str,
    device: str,
    environment: EnvironmentReport | None,
    type_counts: dict[str, int],
    mappings: tuple[NewtonShapeMapping, ...],
    runs: tuple[NewtonSphereRainRun, ...],
    options: SphereRainOptions,
    claim_boundary: str,
    fallback_reason: str | None,
) -> NewtonDiagnosticReport:
    return NewtonDiagnosticReport(
        stage="newton_sphere_rain",
        status=status,
        asset_id=package.asset_id,
        package_id=package.package_id,
        probe_type="sphere_rain",
        device=device,
        environment=environment,
        primitive_count=len(package.primitives),
        type_counts=type_counts,
        shape_mappings=mappings,
        contact_canaries=(),
        sphere_rain_runs=runs,
        task_scope=SPHERE_RAIN_TASK_SCOPE,
        initial_conditions=options.to_initial_conditions(),
        solver={**options.to_solver_dict(), "device": device},
        claim_boundary=claim_boundary,
        metrics=_sphere_rain_metrics(mappings, runs),
        fallback_reason=fallback_reason,
        evidence_level=SPHERE_RAIN_EVIDENCE_LEVEL,
    )


def _sphere_rain_metrics(
    mappings: tuple[NewtonShapeMapping, ...],
    runs: tuple[NewtonSphereRainRun, ...],
) -> dict[str, object]:
    mapped = tuple(mapping for mapping in mappings if mapping.status == "mapped")
    return {
        "task_scope": SPHERE_RAIN_TASK_SCOPE,
        "contact_metric": "unique_probe_contact_density_proxy",
        "full_package_shape_coverage": len(mapped) == len(mappings) and bool(mapped),
        "mapped_primitive_count": len(mapped),
        "mapping_gap_count": len(mappings) - len(mapped),
        "included_primitive_count": len(mapped),
        "run_count": len(runs),
        "smoke_passed_run_count": sum(1 for run in runs if run.status == "smoke_passed"),
    }


def _p95(values: tuple[int, ...]) -> float:
    if not values:
        return 0.0
    return float(np.percentile(np.asarray(values, dtype=float), 95.0))


def _positive_int(value: int, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, Integral) or int(value) < 1:
        raise ValueError(f"{name} must be at least 1")


def _positive_float(value: float, name: str) -> None:
    result = float(value)
    if not math.isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be greater than 0")


def _non_negative_float(value: float, name: str) -> None:
    result = float(value)
    if not math.isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be non-negative")


def _finite_float(value: float, name: str) -> None:
    if not math.isfinite(float(value)):
        raise ValueError(f"{name} must be finite")
