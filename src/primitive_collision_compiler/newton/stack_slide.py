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
    _status_from_environment,
    _wp_vec3,
)
from primitive_collision_compiler.newton.drop_settle import _linear_speed
from primitive_collision_compiler.newton.env import inspect_newton_environment
from primitive_collision_compiler.newton.shapes import map_package_shapes
from primitive_collision_compiler.newton.sphere_rain import (
    _add_static_shape,
    _package_bounds,
    _package_contact_metrics,
)
from primitive_collision_compiler.reports.schema import (
    EnvironmentReport,
    NewtonDiagnosticReport,
    NewtonShapeMapping,
    NewtonStackSlideRun,
)

STACK_SLIDE_CLAIM_BOUNDARY = "stack_slide_task_smoke_not_collision_quality_or_safety"
STACK_SLIDE_EVIDENCE_LEVEL = "newton_stack_slide_task_smoke"
STACK_SLIDE_TASK_SCOPE = "single_asset_static_support_probe_box_lateral_impulse"


@dataclass(frozen=True)
class StackSlideOptions:
    probe_half_extents_m: tuple[float, float, float] = (0.05, 0.05, 0.05)
    lateral_velocity_mps: float = 0.1
    spawn_clearance_m: float = 0.01
    frames: int = 240
    substeps: int = 4
    frame_dt_seconds: float = 1.0 / 60.0
    iterations: int = 4
    gravity_mps2: float = -9.81
    friction: float = 0.7
    max_slide_distance_m: float = 0.25
    max_drop_below_support_m: float = 0.05
    max_settle_linear_speed_mps: float = 0.25
    rigid_contact_max: int = 4096

    def __post_init__(self) -> None:
        _positive_vector3(self.probe_half_extents_m, "probe_half_extents_m")
        _non_negative_float(self.lateral_velocity_mps, "lateral_velocity_mps")
        _non_negative_float(self.spawn_clearance_m, "spawn_clearance_m")
        _positive_int(self.frames, "frames")
        _positive_int(self.substeps, "substeps")
        _positive_float(self.frame_dt_seconds, "frame_dt_seconds")
        _positive_int(self.iterations, "iterations")
        _finite_float(self.gravity_mps2, "gravity_mps2")
        _non_negative_float(self.friction, "friction")
        _non_negative_float(self.max_slide_distance_m, "max_slide_distance_m")
        _non_negative_float(self.max_drop_below_support_m, "max_drop_below_support_m")
        _non_negative_float(self.max_settle_linear_speed_mps, "max_settle_linear_speed_mps")
        _positive_int(self.rigid_contact_max, "rigid_contact_max")

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
            "rigid_contact_max": self.rigid_contact_max,
            "broad_phase": "nxn",
            "deterministic": True,
        }

    def to_initial_conditions(self) -> dict[str, object]:
        return {
            "support": "static_package",
            "probe_shape": "box",
            "probe_half_extents_m": list(self.probe_half_extents_m),
            "lateral_velocity_mps": self.lateral_velocity_mps,
            "spawn_clearance_m": self.spawn_clearance_m,
            "max_slide_distance_m": self.max_slide_distance_m,
            "max_drop_below_support_m": self.max_drop_below_support_m,
            "max_settle_linear_speed_mps": self.max_settle_linear_speed_mps,
        }


def run_newton_stack_slide(
    package: CollisionPackage,
    *,
    source_dir: str,
    device: str = "cpu",
    options: StackSlideOptions | None = None,
    claim_boundary: str = STACK_SLIDE_CLAIM_BOUNDARY,
) -> NewtonDiagnosticReport:
    options = options or StackSlideOptions()
    mappings = map_package_shapes(package)
    mapped = tuple(mapping for mapping in mappings if mapping.status == "mapped")
    type_counts = dict(Counter(primitive.kind for primitive in package.primitives))

    if len(mapped) != len(package.primitives) or not mapped:
        return _stack_slide_report(
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
        return _stack_slide_report(
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
        return _stack_slide_report(
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
        run = _run_stack_slide(mapped, runtime.newton, runtime.warp, device, options)
        runs = (run,)
        status = "smoke_passed" if run.status == "smoke_passed" else "runtime_failure"
        fallback_reason = None if status == "smoke_passed" else "stack_slide_failed"
    except Exception as exc:
        run = NewtonStackSlideRun(
            run_id="seed0",
            status="runtime_failure",
            primitive_ids=tuple(mapping.primitive_id for mapping in mapped),
            completed_steps=0,
            initial_probe_position=(float("nan"), float("nan"), float("nan")),
            final_probe_position=(float("nan"), float("nan"), float("nan")),
            min_probe_height=float("nan"),
            support_top_height=float("nan"),
            final_linear_velocity=(float("nan"), float("nan"), float("nan")),
            max_contact_count=0,
            final_contact_count=0,
            finite_state=False,
            contact_observed=False,
            final_contact_observed=False,
            horizontal_displacement_m=float("nan"),
            final_linear_speed_mps=None,
            failure_labels=(f"runtime_exception_{type(exc).__name__}",),
        )
        runs = (run,)
        status = "runtime_failure"
        fallback_reason = f"{type(exc).__name__}: {exc}"

    return _stack_slide_report(
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


def evaluate_stack_slide_trace(
    *,
    primitive_ids: tuple[str, ...],
    completed_steps: int,
    initial_probe_position: tuple[float, float, float],
    final_probe_position: tuple[float, float, float],
    min_probe_height: float,
    support_top_height: float,
    final_linear_velocity: tuple[float, float, float],
    max_contact_count: int,
    final_contact_count: int,
    finite_state: bool,
    max_slide_distance_m: float = 0.25,
    max_drop_below_support_m: float = 0.05,
    max_settle_linear_speed_mps: float = 0.25,
    run_id: str = "seed0",
) -> NewtonStackSlideRun:
    initial_xy = np.asarray(initial_probe_position[:2], dtype=float)
    final_xy = np.asarray(final_probe_position[:2], dtype=float)
    horizontal_displacement_m = float(np.linalg.norm(final_xy - initial_xy))
    final_linear_speed_mps = _linear_speed(final_linear_velocity)
    contact_observed = bool(max_contact_count > 0)
    final_contact_observed = bool(final_contact_count > 0)

    labels: list[str] = []
    if not finite_state or not np.isfinite(final_linear_speed_mps):
        labels.append("non_finite_state")
    if not contact_observed:
        labels.append("no_contact_observed")
    if contact_observed and not final_contact_observed:
        labels.append("no_final_contact")
    if horizontal_displacement_m > max_slide_distance_m:
        labels.append("excess_horizontal_slide")
    if min_probe_height < support_top_height - max_drop_below_support_m:
        labels.append("probe_below_support")
    if (
        np.isfinite(final_linear_speed_mps)
        and final_linear_speed_mps > max_settle_linear_speed_mps
    ):
        labels.append("not_settled")

    return NewtonStackSlideRun(
        run_id=run_id,
        status="smoke_passed" if not labels else "runtime_failure",
        primitive_ids=primitive_ids,
        completed_steps=int(completed_steps),
        initial_probe_position=tuple(float(value) for value in initial_probe_position),
        final_probe_position=tuple(float(value) for value in final_probe_position),
        min_probe_height=float(min_probe_height),
        support_top_height=float(support_top_height),
        final_linear_velocity=tuple(float(value) for value in final_linear_velocity),
        max_contact_count=int(max_contact_count),
        final_contact_count=int(final_contact_count),
        finite_state=bool(finite_state),
        contact_observed=contact_observed,
        final_contact_observed=final_contact_observed,
        horizontal_displacement_m=horizontal_displacement_m,
        final_linear_speed_mps=(
            None if not np.isfinite(final_linear_speed_mps) else float(final_linear_speed_mps)
        ),
        failure_labels=tuple(labels),
    )


def _run_stack_slide(
    mappings: tuple[NewtonShapeMapping, ...],
    newton: ModuleType | None,
    wp: ModuleType | None,
    device: str,
    options: StackSlideOptions,
) -> NewtonStackSlideRun:
    if newton is None or wp is None:
        return evaluate_stack_slide_trace(
            primitive_ids=tuple(mapping.primitive_id for mapping in mappings),
            completed_steps=0,
            initial_probe_position=(float("nan"), float("nan"), float("nan")),
            final_probe_position=(float("nan"), float("nan"), float("nan")),
            min_probe_height=float("nan"),
            support_top_height=float("nan"),
            final_linear_velocity=(float("nan"), float("nan"), float("nan")),
            max_contact_count=0,
            final_contact_count=0,
            finite_state=False,
        )

    bounds_min, bounds_max = _package_bounds(mappings)
    center = (bounds_min + bounds_max) * 0.5
    support_top_height = float(bounds_max[2])
    hx, hy, hz = options.probe_half_extents_m
    probe_start = (
        float(center[0]),
        float(center[1]),
        float(support_top_height + options.spawn_clearance_m + hz),
    )
    primitive_ids = tuple(mapping.primitive_id for mapping in mappings)

    with wp.ScopedDevice(device):
        builder = newton.ModelBuilder(gravity=options.gravity_mps2, up_axis=newton.Axis.Z)
        builder.default_shape_cfg.mu = options.friction
        package_shape_ids = tuple(
            _add_static_shape(builder, mapping, wp, newton) for mapping in mappings
        )
        probe_body = builder.add_body(
            xform=wp.transform(_wp_vec3(wp, probe_start), wp.quat_identity()),
            label="stack_slide_probe",
        )
        probe_shape = int(
            builder.add_shape_box(
                body=probe_body,
                hx=float(hx),
                hy=float(hy),
                hz=float(hz),
                label="stack_slide_probe",
            )
        )
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

        body_qd = state_0.body_qd.numpy().copy()
        body_qd[probe_body, :3] = (options.lateral_velocity_mps, 0.0, 0.0)
        state_0.body_qd.assign(body_qd)

        initial_probe_position = tuple(float(value) for value in state_0.body_q.numpy()[probe_body, :3])
        final_probe_position = initial_probe_position
        min_probe_height = float(initial_probe_position[2])
        final_linear_velocity = tuple(float(value) for value in body_qd[probe_body, :3])
        max_contact_count = 0
        completed_steps = 0
        finite_state = True
        package_shapes = set(int(shape_id) for shape_id in package_shape_ids)
        probe_shapes = {probe_shape}

        for _ in range(options.frames):
            for _ in range(options.substeps):
                state_0.clear_forces()
                pipeline.collide(state_0, contacts)
                package_contact_count, _ = _package_contact_metrics(
                    contacts,
                    package_shapes,
                    probe_shapes,
                )
                max_contact_count = max(max_contact_count, package_contact_count)
                solver.step(state_0, state_1, control, contacts, options.step_dt_seconds)
                state_0, state_1 = state_1, state_0
                completed_steps += 1
                body_q = state_0.body_q.numpy()
                body_qd = state_0.body_qd.numpy()
                final_probe_position = tuple(float(value) for value in body_q[probe_body, :3])
                min_probe_height = min(min_probe_height, float(final_probe_position[2]))
                final_linear_velocity = tuple(float(value) for value in body_qd[probe_body, :3])
                if not np.all(np.isfinite(body_q)) or not np.all(np.isfinite(body_qd)):
                    finite_state = False
                    break
            if not finite_state:
                break

        pipeline.collide(state_0, contacts)
        final_contact_count, _ = _package_contact_metrics(contacts, package_shapes, probe_shapes)
        max_contact_count = max(max_contact_count, final_contact_count)

    return evaluate_stack_slide_trace(
        primitive_ids=primitive_ids,
        completed_steps=completed_steps,
        initial_probe_position=initial_probe_position,
        final_probe_position=final_probe_position,
        min_probe_height=min_probe_height,
        support_top_height=support_top_height,
        final_linear_velocity=final_linear_velocity,
        max_contact_count=max_contact_count,
        final_contact_count=final_contact_count,
        finite_state=finite_state,
        max_slide_distance_m=options.max_slide_distance_m,
        max_drop_below_support_m=options.max_drop_below_support_m,
        max_settle_linear_speed_mps=options.max_settle_linear_speed_mps,
    )


def _stack_slide_report(
    package: CollisionPackage,
    *,
    status: str,
    device: str,
    environment: EnvironmentReport | None,
    type_counts: dict[str, int],
    mappings: tuple[NewtonShapeMapping, ...],
    runs: tuple[NewtonStackSlideRun, ...],
    options: StackSlideOptions,
    claim_boundary: str,
    fallback_reason: str | None,
) -> NewtonDiagnosticReport:
    return NewtonDiagnosticReport(
        stage="newton_stack_slide",
        status=status,
        asset_id=package.asset_id,
        package_id=package.package_id,
        probe_type="stack_or_slide",
        device=device,
        environment=environment,
        primitive_count=len(package.primitives),
        type_counts=type_counts,
        shape_mappings=mappings,
        contact_canaries=(),
        stack_slide_runs=runs,
        task_scope=STACK_SLIDE_TASK_SCOPE,
        initial_conditions=options.to_initial_conditions(),
        solver={**options.to_solver_dict(), "device": device},
        claim_boundary=claim_boundary,
        metrics=_stack_slide_metrics(mappings, runs),
        fallback_reason=fallback_reason,
        evidence_level=STACK_SLIDE_EVIDENCE_LEVEL,
    )


def _stack_slide_metrics(
    mappings: tuple[NewtonShapeMapping, ...],
    runs: tuple[NewtonStackSlideRun, ...],
) -> dict[str, object]:
    mapped = tuple(mapping for mapping in mappings if mapping.status == "mapped")
    return {
        "task_scope": STACK_SLIDE_TASK_SCOPE,
        "full_package_shape_coverage": len(mapped) == len(mappings) and bool(mapped),
        "mapped_primitive_count": len(mapped),
        "mapping_gap_count": len(mappings) - len(mapped),
        "included_primitive_count": len(mapped),
        "run_count": len(runs),
        "smoke_passed_run_count": sum(1 for run in runs if run.status == "smoke_passed"),
    }


def _positive_vector3(value: tuple[float, float, float], name: str) -> None:
    if not isinstance(value, tuple | list) or len(value) != 3:
        raise ValueError(f"{name} must contain three positive finite values")
    if any(float(component) <= 0.0 or not math.isfinite(float(component)) for component in value):
        raise ValueError(f"{name} must contain three positive finite values")


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
