from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
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
from primitive_collision_compiler.newton.env import inspect_newton_environment
from primitive_collision_compiler.newton.shapes import map_package_shapes
from primitive_collision_compiler.reports.schema import (
    EnvironmentReport,
    NewtonDiagnosticReport,
    NewtonDropSettleRun,
    NewtonShapeMapping,
)

DROP_SETTLE_CLAIM_BOUNDARY = "drop_settle_task_smoke_not_collision_quality_or_safety"
DROP_SETTLE_EVIDENCE_LEVEL = "newton_drop_settle_task_smoke"
DROP_SETTLE_TASK_SCOPE = "single_asset_drop_settle_static_plane"


@dataclass(frozen=True)
class DropSettleOptions:
    height_m: float = 0.25
    frames: int = 360
    substeps: int = 8
    frame_dt_seconds: float = 1.0 / 60.0
    iterations: int = 2
    gravity_mps2: float = -9.81
    ground_height_m: float = 0.0
    friction: float = 0.5
    min_descent_m: float = 1.0e-5
    max_floor_breach_m: float = 0.05
    max_settle_linear_speed_mps: float = 0.05

    def __post_init__(self) -> None:
        _positive_int(self.frames, "frames")
        _positive_int(self.substeps, "substeps")
        _positive_int(self.iterations, "iterations")
        _positive_float(self.frame_dt_seconds, "frame_dt_seconds")
        _non_negative_float(self.height_m, "height_m")
        _non_negative_float(self.friction, "friction")
        _non_negative_float(self.min_descent_m, "min_descent_m")
        _non_negative_float(self.max_floor_breach_m, "max_floor_breach_m")
        _non_negative_float(self.max_settle_linear_speed_mps, "max_settle_linear_speed_mps")

    @property
    def step_dt_seconds(self) -> float:
        return self.frame_dt_seconds / self.substeps

    @property
    def total_steps(self) -> int:
        return self.frames * self.substeps

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
        }

    def to_initial_conditions(self) -> dict[str, object]:
        return {
            "height_m": self.height_m,
            "ground_height_m": self.ground_height_m,
            "initial_velocity_mps": [0.0, 0.0, 0.0],
            "body_orientation": "identity",
            "max_floor_breach_m": self.max_floor_breach_m,
            "max_settle_linear_speed_mps": self.max_settle_linear_speed_mps,
        }


def run_newton_drop_settle(
    package: CollisionPackage,
    *,
    source_dir: str,
    device: str = "cpu",
    options: DropSettleOptions | None = None,
    claim_boundary: str = DROP_SETTLE_CLAIM_BOUNDARY,
) -> NewtonDiagnosticReport:
    options = options or DropSettleOptions()
    mappings = map_package_shapes(package)
    mapped = tuple(mapping for mapping in mappings if mapping.status == "mapped")
    type_counts = dict(Counter(primitive.kind for primitive in package.primitives))

    if len(mapped) != len(package.primitives) or not mapped:
        return _drop_report(
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
        return _drop_report(
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
        return _drop_report(
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
        run = _run_drop_settle(mapped, runtime.newton, runtime.warp, device, options)
        runs = (run,)
        status = "smoke_passed" if run.status == "smoke_passed" else "runtime_failure"
        fallback_reason = None if status == "smoke_passed" else "drop_settle_failed"
    except Exception as exc:
        run = NewtonDropSettleRun(
            run_id="seed0",
            status="runtime_failure",
            primitive_ids=tuple(mapping.primitive_id for mapping in mapped),
            completed_steps=0,
            initial_height=options.height_m,
            final_height=float("nan"),
            min_height=float("nan"),
            final_linear_velocity=(float("nan"), float("nan"), float("nan")),
            max_contact_count=0,
            final_contact_count=0,
            finite_state=False,
            descended=False,
            contact_observed=False,
            failure_labels=(f"runtime_exception_{type(exc).__name__}",),
        )
        runs = (run,)
        status = "runtime_failure"
        fallback_reason = f"{type(exc).__name__}: {exc}"

    return _drop_report(
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


def evaluate_drop_settle_trace(
    *,
    primitive_ids: tuple[str, ...],
    completed_steps: int,
    initial_height: float,
    final_height: float,
    min_height: float,
    final_linear_velocity: tuple[float, float, float],
    max_contact_count: int,
    final_contact_count: int,
    finite_state: bool,
    min_descent_m: float = 1.0e-5,
    final_support_height: float | None = None,
    min_support_height: float | None = None,
    min_allowed_support_height: float | None = None,
    max_settle_linear_speed_mps: float = 0.05,
    run_id: str = "seed0",
) -> NewtonDropSettleRun:
    descended = bool(final_height < initial_height - min_descent_m)
    contact_observed = bool(max_contact_count > 0)
    final_contact_observed = bool(final_contact_count > 0)
    final_linear_speed_mps = _linear_speed(final_linear_velocity)
    labels: list[str] = []
    if not finite_state or not np.isfinite(final_linear_speed_mps):
        labels.append("non_finite_state")
    if not descended:
        labels.append("no_descent")
    if not contact_observed:
        labels.append("no_contact_observed")
    if contact_observed and not final_contact_observed:
        labels.append("no_final_contact")
    if np.isfinite(final_linear_speed_mps) and final_linear_speed_mps > max_settle_linear_speed_mps:
        labels.append("not_settled")
    if (
        min_support_height is not None
        and min_allowed_support_height is not None
        and min_support_height < min_allowed_support_height
    ):
        labels.append("floor_breach")
    status = "smoke_passed" if not labels else "runtime_failure"
    return NewtonDropSettleRun(
        run_id=run_id,
        status=status,
        primitive_ids=primitive_ids,
        completed_steps=completed_steps,
        initial_height=float(initial_height),
        final_height=float(final_height),
        min_height=float(min_height),
        final_linear_velocity=tuple(float(value) for value in final_linear_velocity),
        max_contact_count=int(max_contact_count),
        final_contact_count=int(final_contact_count),
        finite_state=bool(finite_state),
        descended=descended,
        contact_observed=contact_observed,
        failure_labels=tuple(labels),
        final_support_height=None if final_support_height is None else float(final_support_height),
        min_support_height=None if min_support_height is None else float(min_support_height),
        final_linear_speed_mps=None if not np.isfinite(final_linear_speed_mps) else float(final_linear_speed_mps),
    )


def _run_drop_settle(
    mappings: tuple[NewtonShapeMapping, ...],
    newton: ModuleType | None,
    wp: ModuleType | None,
    device: str,
    options: DropSettleOptions,
) -> NewtonDropSettleRun:
    if newton is None or wp is None:
        return evaluate_drop_settle_trace(
            primitive_ids=tuple(mapping.primitive_id for mapping in mappings),
            completed_steps=0,
            initial_height=options.height_m,
            final_height=float("nan"),
            min_height=float("nan"),
            final_linear_velocity=(float("nan"), float("nan"), float("nan")),
            max_contact_count=0,
            final_contact_count=0,
            finite_state=False,
        )

    anchor, _ = _package_anchor(mappings)
    primitive_ids = tuple(mapping.primitive_id for mapping in mappings)
    with wp.ScopedDevice(device):
        builder = newton.ModelBuilder(gravity=options.gravity_mps2, up_axis=newton.Axis.Z)
        builder.default_shape_cfg.mu = options.friction
        builder.add_ground_plane(height=options.ground_height_m)
        body = builder.add_body(
            xform=wp.transform(
                wp.vec3(0.0, 0.0, options.ground_height_m + options.height_m),
                wp.quat_identity(),
            )
        )
        for mapping in mappings:
            _add_dynamic_shape(builder, mapping, wp, body, anchor)
        model = builder.finalize(device=device)
        solver = newton.solvers.SolverXPBD(model, iterations=options.iterations)
        state_0 = model.state()
        state_1 = model.state()
        control = model.control()
        contacts = model.contacts()

        initial_height = float(state_0.body_q.numpy()[body, 2])
        initial_support_height = _estimated_support_height(mappings, anchor, state_0.body_q.numpy()[body])
        final_height = initial_height
        min_height = initial_height
        final_support_height = initial_support_height
        min_support_height = initial_support_height
        final_linear_velocity = (0.0, 0.0, 0.0)
        max_contact_count = 0
        completed_steps = 0
        finite_state = True

        for _ in range(options.frames):
            for _ in range(options.substeps):
                state_0.clear_forces()
                model.collide(state_0, contacts)
                max_contact_count = max(
                    max_contact_count,
                    int(contacts.rigid_contact_count.numpy()[0]),
                )
                solver.step(state_0, state_1, control, contacts, options.step_dt_seconds)
                state_0, state_1 = state_1, state_0
                completed_steps += 1
                body_q = state_0.body_q.numpy()
                body_qd = state_0.body_qd.numpy()
                final_height = float(body_q[body, 2])
                min_height = min(min_height, final_height)
                final_support_height = _estimated_support_height(mappings, anchor, body_q[body])
                min_support_height = min(min_support_height, final_support_height)
                final_linear_velocity = tuple(float(value) for value in body_qd[body, :3])
                if not np.all(np.isfinite(body_q)) or not np.all(np.isfinite(body_qd)):
                    finite_state = False
                    break
            if not finite_state:
                break

        model.collide(state_0, contacts)
        final_contact_count = int(contacts.rigid_contact_count.numpy()[0])
        max_contact_count = max(max_contact_count, final_contact_count)

    return evaluate_drop_settle_trace(
        primitive_ids=primitive_ids,
        completed_steps=completed_steps,
        initial_height=initial_height,
        final_height=final_height,
        min_height=min_height,
        final_linear_velocity=final_linear_velocity,
        max_contact_count=max_contact_count,
        final_contact_count=final_contact_count,
        finite_state=finite_state,
        min_descent_m=options.min_descent_m,
        final_support_height=final_support_height,
        min_support_height=min_support_height,
        min_allowed_support_height=options.ground_height_m - options.max_floor_breach_m,
        max_settle_linear_speed_mps=options.max_settle_linear_speed_mps,
    )


def _add_dynamic_shape(
    builder: Any,
    mapping: NewtonShapeMapping,
    wp: ModuleType,
    body: int,
    anchor: tuple[float, float, float],
) -> None:
    local_center = tuple(float(mapping.center[index] - anchor[index]) for index in range(3))
    xform = wp.transform(_wp_vec3(wp, local_center), _shape_quat(mapping, wp))
    dimensions = mapping.dimensions
    if mapping.kind == "box":
        hx, hy, hz = (float(value) for value in dimensions["half_extents"])
        builder.add_shape_box(body=body, xform=xform, hx=hx, hy=hy, hz=hz)
    elif mapping.kind == "sphere":
        builder.add_shape_sphere(body=body, xform=xform, radius=float(dimensions["radius"]))
    elif mapping.kind == "capsule":
        builder.add_shape_capsule(
            body=body,
            xform=xform,
            radius=float(dimensions["radius"]),
            half_height=float(dimensions["half_height"]),
        )
    elif mapping.kind == "cylinder":
        builder.add_shape_cylinder(
            body=body,
            xform=xform,
            radius=float(dimensions["radius"]),
            half_height=float(dimensions["half_height"]),
        )
    elif mapping.kind == "cone":
        builder.add_shape_cone(
            body=body,
            xform=xform,
            radius=float(dimensions["radius"]),
            half_height=float(dimensions["half_height"]),
        )
    elif mapping.kind == "ellipsoid":
        rx, ry, rz = (float(value) for value in dimensions["radii"])
        builder.add_shape_ellipsoid(body=body, xform=xform, rx=rx, ry=ry, rz=rz)
    else:
        raise ValueError(f"unsupported mapped primitive kind: {mapping.kind}")


def _package_anchor(
    mappings: tuple[NewtonShapeMapping, ...],
) -> tuple[tuple[float, float, float], tuple[tuple[float, float, float], tuple[float, float, float]]]:
    mins = []
    maxs = []
    for mapping in mappings:
        center = np.asarray(mapping.center, dtype=float)
        half_extents = _world_half_extents(mapping)
        mins.append(center - half_extents)
        maxs.append(center + half_extents)
    bounds_min = np.min(np.vstack(mins), axis=0)
    bounds_max = np.max(np.vstack(maxs), axis=0)
    anchor = np.array(
        [
            (bounds_min[0] + bounds_max[0]) * 0.5,
            (bounds_min[1] + bounds_max[1]) * 0.5,
            bounds_min[2],
        ],
        dtype=float,
    )
    return (
        _tuple3(anchor),
        (_tuple3(bounds_min), _tuple3(bounds_max)),
    )


def _world_half_extents(mapping: NewtonShapeMapping) -> np.ndarray:
    axes = _axes_matrix(mapping)
    dimensions = mapping.dimensions
    if mapping.kind == "sphere":
        return np.full(3, float(dimensions["radius"]), dtype=float)
    if mapping.kind == "capsule":
        radius = float(dimensions["radius"])
        half_height = float(dimensions["half_height"])
        axis_index = int(dimensions.get("axis_index", 2))
        axis = axes[:, axis_index]
        return np.abs(axis) * half_height + radius
    if mapping.kind == "box":
        half_extents = np.asarray(dimensions["half_extents"], dtype=float)
        return np.abs(axes) @ half_extents
    if mapping.kind in {"cylinder", "cone", "ellipsoid"}:
        return np.abs(axes) @ _local_half_extents(mapping)
    raise ValueError(f"unsupported mapped primitive kind: {mapping.kind}")


def _estimated_support_height(
    mappings: tuple[NewtonShapeMapping, ...],
    anchor: tuple[float, float, float],
    body_q: np.ndarray,
) -> float:
    body_position = np.asarray(body_q[:3], dtype=float)
    body_rotation = _quat_to_matrix(np.asarray(body_q[3:7], dtype=float))
    min_height = float("inf")
    for mapping in mappings:
        local_center = np.asarray(
            [mapping.center[index] - anchor[index] for index in range(3)],
            dtype=float,
        )
        world_center = body_position + body_rotation @ local_center
        world_axes = body_rotation @ _axes_matrix(mapping)
        support_height = float(world_center[2] - _support_extent_z(mapping, world_axes))
        min_height = min(min_height, support_height)
    return min_height


def _support_extent_z(mapping: NewtonShapeMapping, world_axes: np.ndarray) -> float:
    dimensions = mapping.dimensions
    if mapping.kind == "sphere":
        return float(dimensions["radius"])
    if mapping.kind == "capsule":
        radius = float(dimensions["radius"])
        half_height = float(dimensions["half_height"])
        axis_index = int(dimensions.get("axis_index", 2))
        return abs(float(world_axes[2, axis_index])) * half_height + radius
    if mapping.kind == "box":
        half_extents = np.asarray(dimensions["half_extents"], dtype=float)
        return float(np.abs(world_axes[2, :]) @ half_extents)
    if mapping.kind in {"cylinder", "cone", "ellipsoid"}:
        return float(np.abs(world_axes[2, :]) @ _local_half_extents(mapping))
    raise ValueError(f"unsupported mapped primitive kind: {mapping.kind}")


def _local_half_extents(mapping: NewtonShapeMapping) -> np.ndarray:
    dimensions = mapping.dimensions
    if mapping.kind in {"cylinder", "cone"}:
        radius = float(dimensions["radius"])
        half_height = float(dimensions["half_height"])
        axis_index = int(dimensions.get("axis_index", 2))
        half_extents = np.full(3, radius, dtype=float)
        half_extents[axis_index] = half_height
        return half_extents
    if mapping.kind == "ellipsoid":
        return np.asarray(dimensions["radii"], dtype=float)
    raise ValueError(f"unsupported mapped primitive kind: {mapping.kind}")


def _quat_to_matrix(quat: np.ndarray) -> np.ndarray:
    qx, qy, qz, qw = (float(value) for value in quat)
    norm = (qx * qx + qy * qy + qz * qz + qw * qw) ** 0.5
    if norm == 0.0:
        return np.eye(3, dtype=float)
    qx, qy, qz, qw = (qx / norm, qy / norm, qz / norm, qw / norm)
    return np.array(
        [
            [1.0 - 2.0 * (qy * qy + qz * qz), 2.0 * (qx * qy - qz * qw), 2.0 * (qx * qz + qy * qw)],
            [2.0 * (qx * qy + qz * qw), 1.0 - 2.0 * (qx * qx + qz * qz), 2.0 * (qy * qz - qx * qw)],
            [2.0 * (qx * qz - qy * qw), 2.0 * (qy * qz + qx * qw), 1.0 - 2.0 * (qx * qx + qy * qy)],
        ],
        dtype=float,
    )


def _axes_matrix(mapping: NewtonShapeMapping) -> np.ndarray:
    if mapping.axes:
        return np.asarray(mapping.axes, dtype=float).T
    return np.eye(3, dtype=float)


def _linear_speed(velocity: tuple[float, float, float]) -> float:
    vector = np.asarray(velocity, dtype=float)
    return float(np.linalg.norm(vector))


def _drop_report(
    package: CollisionPackage,
    *,
    status: str,
    device: str,
    environment: EnvironmentReport | None,
    type_counts: dict[str, int],
    mappings: tuple[NewtonShapeMapping, ...],
    runs: tuple[NewtonDropSettleRun, ...],
    options: DropSettleOptions,
    claim_boundary: str,
    fallback_reason: str | None,
) -> NewtonDiagnosticReport:
    return NewtonDiagnosticReport(
        stage="newton_drop_settle",
        status=status,
        asset_id=package.asset_id,
        package_id=package.package_id,
        probe_type="drop_settle",
        device=device,
        environment=environment,
        primitive_count=len(package.primitives),
        type_counts=type_counts,
        shape_mappings=mappings,
        contact_canaries=(),
        drop_settle_runs=runs,
        task_scope=DROP_SETTLE_TASK_SCOPE,
        initial_conditions=options.to_initial_conditions(),
        solver={**options.to_solver_dict(), "device": device},
        claim_boundary=claim_boundary,
        metrics=_drop_metrics(mappings, runs),
        fallback_reason=fallback_reason,
        evidence_level=DROP_SETTLE_EVIDENCE_LEVEL,
    )


def _drop_metrics(
    mappings: tuple[NewtonShapeMapping, ...],
    runs: tuple[NewtonDropSettleRun, ...],
) -> dict[str, object]:
    mapped = tuple(mapping for mapping in mappings if mapping.status == "mapped")
    return {
        "task_scope": DROP_SETTLE_TASK_SCOPE,
        "full_package_shape_coverage": len(mapped) == len(mappings) and bool(mapped),
        "mapped_primitive_count": len(mapped),
        "mapping_gap_count": len(mappings) - len(mapped),
        "included_primitive_count": len(mapped),
        "run_count": len(runs),
        "smoke_passed_run_count": sum(1 for run in runs if run.status == "smoke_passed"),
    }


def _positive_int(value: int, name: str) -> None:
    if int(value) < 1:
        raise ValueError(f"{name} must be at least 1")


def _positive_float(value: float, name: str) -> None:
    if float(value) <= 0.0:
        raise ValueError(f"{name} must be greater than 0")


def _non_negative_float(value: float, name: str) -> None:
    if float(value) < 0.0:
        raise ValueError(f"{name} must be non-negative")


def _tuple3(vector: np.ndarray) -> tuple[float, float, float]:
    return (float(vector[0]), float(vector[1]), float(vector[2]))
