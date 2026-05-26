from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import math
from numbers import Integral
from pathlib import Path

import numpy as np

from primitive_collision_compiler.newton.diagnostics import (
    _import_newton_runtime,
    _status_from_environment,
)
from primitive_collision_compiler.newton.env import inspect_newton_environment
from primitive_collision_compiler.reports.schema import EnvironmentReport
from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec

ARTICULATION_SMOKE_CLAIM_BOUNDARY = (
    "articulation_smoke_diagnostic_not_whole_robot_collision_quality_or_safety_validation"
)
ARTICULATION_SMOKE_EVIDENCE_LEVEL = "newton_articulation_smoke"
ARTICULATION_SMOKE_TASK_SCOPE = "single_articulated_asset_import_hold_kinematic_trajectory"
GENERATED_PACKAGE_ROBOT_TASK_CLAIM_BOUNDARY = (
    "generated_package_robot_task_probe_not_whole_robot_collision_quality_or_safety_validation"
)
GENERATED_PACKAGE_ROBOT_TASK_EVIDENCE_LEVEL = "newton_generated_package_robot_task_smoke"
GENERATED_PACKAGE_ROBOT_TASK_SCOPE = (
    "generated_link_aware_package_import_hold_kinematic_trajectory"
)
GENERATED_PACKAGE_ROBOT_TASK_PROBE_TYPE = "generated_package_robot_task_if_robot"


@dataclass(frozen=True)
class ArticulationSmokeOptions:
    hold_frames: int = 60
    trajectory_delta_rad: float = 0.05
    max_gravity_hold_joint_drift: float = 0.01
    min_end_effector_pose_delta_m: float = 1.0e-6
    substeps: int = 4
    frame_dt_seconds: float = 1.0 / 60.0
    iterations: int = 2
    gravity_mps2: float = -9.81
    mesh_approximation: str = "bounding_box"
    collapse_fixed_joints: bool = True
    enable_self_collisions: bool = False
    load_visual_shapes: bool = False
    hide_collision_shapes: bool = True

    def __post_init__(self) -> None:
        _positive_int(self.hold_frames, "hold_frames")
        _non_negative_float(self.trajectory_delta_rad, "trajectory_delta_rad")
        _non_negative_float(
            self.max_gravity_hold_joint_drift,
            "max_gravity_hold_joint_drift",
        )
        _non_negative_float(
            self.min_end_effector_pose_delta_m,
            "min_end_effector_pose_delta_m",
        )
        _positive_int(self.substeps, "substeps")
        _positive_float(self.frame_dt_seconds, "frame_dt_seconds")
        _positive_int(self.iterations, "iterations")
        _finite_float(self.gravity_mps2, "gravity_mps2")

    @property
    def step_dt_seconds(self) -> float:
        return self.frame_dt_seconds / self.substeps

    def to_initial_conditions(self) -> dict[str, object]:
        return {
            "joint_command": "gravity_hold_then_single_dof_kinematic_delta",
            "trajectory_delta_rad": self.trajectory_delta_rad,
            "max_gravity_hold_joint_drift": self.max_gravity_hold_joint_drift,
            "min_end_effector_pose_delta_m": self.min_end_effector_pose_delta_m,
            "mesh_approximation": self.mesh_approximation,
            "collapse_fixed_joints": self.collapse_fixed_joints,
            "enable_self_collisions": self.enable_self_collisions,
        }

    def to_solver_dict(self) -> dict[str, object]:
        return {
            "solver": "xpbd",
            "hold_frames": self.hold_frames,
            "substeps": self.substeps,
            "frame_dt_seconds": self.frame_dt_seconds,
            "step_dt_seconds": self.step_dt_seconds,
            "iterations": self.iterations,
            "gravity_mps2": self.gravity_mps2,
            "device_default": "cpu",
            "trajectory_mode": "kinematic_fk_smoke",
        }


def run_newton_articulation_smoke(
    *,
    asset_path: str,
    source_dir: str,
    device: str = "cpu",
    options: ArticulationSmokeOptions | None = None,
    claim_boundary: str = ARTICULATION_SMOKE_CLAIM_BOUNDARY,
) -> dict[str, object]:
    options = options or ArticulationSmokeOptions()
    if not source_dir:
        return _blocked_report(
            asset_path=asset_path,
            status="dependency_gap",
            outcome="dependency_gap",
            reason="newton.source_dir or NEWTON_SOURCE_DIR is not configured",
            environment=None,
            device=device,
            options=options,
            claim_boundary=claim_boundary,
        )

    environment = inspect_newton_environment(source_dir)
    if environment.status != "smoke_passed":
        status = _status_from_environment(environment.status)
        return _blocked_report(
            asset_path=asset_path,
            status=status,
            outcome=_outcome_for_status(status),
            reason=environment.status,
            environment=environment,
            device=device,
            options=options,
            claim_boundary=claim_boundary,
        )

    runtime = _import_newton_runtime(source_dir)
    if runtime.status != "smoke_passed":
        return _blocked_report(
            asset_path=asset_path,
            status=runtime.status,
            outcome=_outcome_for_status(runtime.status),
            reason=runtime.environment.status,
            environment=runtime.environment,
            device=device,
            options=options,
            claim_boundary=claim_boundary,
        )

    try:
        import_metrics, gravity_hold_metrics, trajectory_metrics = _run_articulation_runtime(
            asset_path=asset_path,
            newton=runtime.newton,
            wp=runtime.warp,
            device=device,
            options=options,
        )
    except Exception as exc:
        return _runtime_exception_report(
            asset_path=asset_path,
            environment=environment,
            device=device,
            options=options,
            claim_boundary=claim_boundary,
            reason=f"{type(exc).__name__}: {exc}",
        )

    return evaluate_articulation_smoke(
        asset_path=asset_path,
        import_metrics=import_metrics,
        gravity_hold_metrics=gravity_hold_metrics,
        trajectory_metrics=trajectory_metrics,
        options=options,
        environment=environment,
        device=device,
        claim_boundary=claim_boundary,
    )


def run_newton_generated_package_robot_task_probe(
    *,
    asset_path: str,
    collision_package: CollisionPackage | Mapping[str, object] | None,
    source_dir: str,
    device: str = "cpu",
    options: ArticulationSmokeOptions | None = None,
    claim_boundary: str = GENERATED_PACKAGE_ROBOT_TASK_CLAIM_BOUNDARY,
) -> dict[str, object]:
    options = options or ArticulationSmokeOptions(
        collapse_fixed_joints=False,
        mesh_approximation="",
    )
    package_metrics = _package_input_metrics(collision_package)
    if not source_dir:
        return _generated_package_blocked_report(
            asset_path=asset_path,
            status="dependency_gap",
            outcome="dependency_gap",
            reason="newton.source_dir or NEWTON_SOURCE_DIR is not configured",
            environment=None,
            device=device,
            options=options,
            claim_boundary=claim_boundary,
            package_metrics=package_metrics,
        )

    environment = inspect_newton_environment(source_dir)
    if environment.status != "smoke_passed":
        status = _status_from_environment(environment.status)
        return _generated_package_blocked_report(
            asset_path=asset_path,
            status=status,
            outcome=_outcome_for_status(status),
            reason=environment.status,
            environment=environment,
            device=device,
            options=options,
            claim_boundary=claim_boundary,
            package_metrics=package_metrics,
        )

    runtime = _import_newton_runtime(source_dir)
    if runtime.status != "smoke_passed":
        return _generated_package_blocked_report(
            asset_path=asset_path,
            status=runtime.status,
            outcome=_outcome_for_status(runtime.status),
            reason=runtime.environment.status,
            environment=runtime.environment,
            device=device,
            options=options,
            claim_boundary=claim_boundary,
            package_metrics=package_metrics,
        )

    try:
        (
            import_metrics,
            gravity_hold_metrics,
            trajectory_metrics,
            package_metrics,
        ) = _run_generated_package_robot_task_runtime(
            asset_path=asset_path,
            collision_package=collision_package,
            newton=runtime.newton,
            wp=runtime.warp,
            device=device,
            options=options,
        )
    except Exception as exc:
        return _generated_package_runtime_exception_report(
            asset_path=asset_path,
            environment=environment,
            device=device,
            options=options,
            claim_boundary=claim_boundary,
            reason=f"{type(exc).__name__}: {exc}",
            package_metrics=package_metrics,
        )

    return evaluate_generated_package_robot_task_probe(
        asset_path=asset_path,
        package_metrics=package_metrics,
        import_metrics=import_metrics,
        gravity_hold_metrics=gravity_hold_metrics,
        trajectory_metrics=trajectory_metrics,
        options=options,
        environment=environment,
        device=device,
        claim_boundary=claim_boundary,
    )


def evaluate_articulation_smoke(
    *,
    asset_path: str,
    import_metrics: Mapping[str, object],
    gravity_hold_metrics: Mapping[str, object],
    trajectory_metrics: Mapping[str, object],
    options: ArticulationSmokeOptions,
    environment: EnvironmentReport | None,
    device: str,
    claim_boundary: str = ARTICULATION_SMOKE_CLAIM_BOUNDARY,
) -> dict[str, object]:
    labels: list[str] = []
    articulation_count = _int_metric(import_metrics, "articulation_count")
    joint_dof_count = _int_metric(import_metrics, "joint_dof_count")
    max_joint_drift = _float_metric(gravity_hold_metrics, "max_joint_drift")
    end_effector_delta = _float_metric(trajectory_metrics, "end_effector_pose_delta_m")
    commanded_joint_index = trajectory_metrics.get("commanded_joint_index")

    if articulation_count < 1 or joint_dof_count < 1:
        labels.append("joint_tree_import_failed")
    if not bool(gravity_hold_metrics.get("finite_state", False)):
        labels.append("gravity_hold_non_finite_state")
    if max_joint_drift > options.max_gravity_hold_joint_drift:
        labels.append("gravity_hold_drift_exceeded")
    if (
        not bool(trajectory_metrics.get("finite_state", False))
        or commanded_joint_index is None
        or end_effector_delta < options.min_end_effector_pose_delta_m
    ):
        labels.append("trajectory_completion_failed")

    status = "smoke_passed" if not labels else "runtime_failure"
    return _json_safe(
        {
            "stage": "newton_articulation_smoke",
            "status": status,
            "outcome": _outcome_for_status(status),
            "asset_path": asset_path,
            "probe_type": "articulation_smoke_if_robot",
            "device": device,
            "environment": environment.to_dict() if environment else None,
            "task_scope": ARTICULATION_SMOKE_TASK_SCOPE,
            "initial_conditions": options.to_initial_conditions(),
            "solver": {**options.to_solver_dict(), "device": device},
            "metrics": {
                "joint_tree_import": "passed" if articulation_count >= 1 and joint_dof_count >= 1 else "failed",
                "gravity_hold_drift": max_joint_drift,
                "trajectory_completion": "passed"
                if "trajectory_completion_failed" not in labels
                else "failed",
                "self_collision_sanity": (
                    "disabled_for_reproducible_smoke"
                    if not options.enable_self_collisions
                    else "enabled"
                ),
                "end_effector_pose_error": None,
                "import": dict(import_metrics),
                "gravity_hold": dict(gravity_hold_metrics),
                "trajectory": dict(trajectory_metrics),
            },
            "failure_labels": labels,
            "fallback_reason": None if status == "smoke_passed" else "articulation_smoke_failed",
            "claim_boundary": claim_boundary,
            "evidence_level": ARTICULATION_SMOKE_EVIDENCE_LEVEL,
        }
    )


def evaluate_generated_package_robot_task_probe(
    *,
    asset_path: str,
    package_metrics: Mapping[str, object],
    import_metrics: Mapping[str, object],
    gravity_hold_metrics: Mapping[str, object],
    trajectory_metrics: Mapping[str, object],
    options: ArticulationSmokeOptions,
    environment: EnvironmentReport | None,
    device: str,
    claim_boundary: str = GENERATED_PACKAGE_ROBOT_TASK_CLAIM_BOUNDARY,
) -> dict[str, object]:
    base_report = evaluate_articulation_smoke(
        asset_path=asset_path,
        import_metrics=import_metrics,
        gravity_hold_metrics=gravity_hold_metrics,
        trajectory_metrics=trajectory_metrics,
        options=options,
        environment=environment,
        device=device,
        claim_boundary=claim_boundary,
    )
    labels = list(base_report["failure_labels"])
    package_primitive_count = _int_metric(package_metrics, "package_primitive_count")
    generated_shape_count = _int_metric(package_metrics, "generated_collision_shape_count")
    consumed_primitive_count = _int_metric(package_metrics, "consumed_primitive_count")

    if package_primitive_count < 1:
        labels.append("generated_package_empty")
    if generated_shape_count != package_primitive_count:
        labels.append("generated_package_shape_count_mismatch")
    if consumed_primitive_count != package_primitive_count:
        labels.append("generated_package_primitive_consumption_mismatch")
    if _int_metric(package_metrics, "missing_body_link_count") > 0:
        labels.append("generated_package_missing_body_link")
    if _int_metric(package_metrics, "unsupported_primitive_count") > 0:
        labels.append("generated_package_unsupported_primitive")
    if _int_metric(package_metrics, "invalid_box_primitive_count") > 0:
        labels.append("generated_package_invalid_box_primitive")
    if _int_metric(package_metrics, "source_usd_shape_count") > 0:
        labels.append("source_usd_collision_shapes_not_suppressed")

    status = "smoke_passed" if not labels else "runtime_failure"
    generated_package_consumed = status == "smoke_passed"
    metrics = dict(base_report["metrics"])
    metrics.update(
        {
            "generated_package_consumed": generated_package_consumed,
            "package_consumption": dict(package_metrics),
        }
    )
    initial_conditions = {
        **options.to_initial_conditions(),
        "collision_source": "generated_link_aware_package",
        "source_usd_collision_shapes": "ignored_when_separate_from_rigid_body",
    }
    return _json_safe(
        {
            "stage": "newton_generated_package_robot_task_probe",
            "status": status,
            "outcome": _outcome_for_status(status),
            "asset_path": asset_path,
            "probe_type": GENERATED_PACKAGE_ROBOT_TASK_PROBE_TYPE,
            "device": device,
            "environment": environment.to_dict() if environment else None,
            "task_scope": GENERATED_PACKAGE_ROBOT_TASK_SCOPE,
            "initial_conditions": initial_conditions,
            "solver": {**options.to_solver_dict(), "device": device},
            "metrics": metrics,
            "failure_labels": labels,
            "fallback_reason": None if status == "smoke_passed" else "generated_package_robot_task_failed",
            "claim_boundary": claim_boundary,
            "evidence_level": GENERATED_PACKAGE_ROBOT_TASK_EVIDENCE_LEVEL,
        }
    )


def _run_articulation_runtime(
    *,
    asset_path: str,
    newton,
    wp,
    device: str,
    options: ArticulationSmokeOptions,
) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    if not Path(asset_path).exists():
        raise FileNotFoundError(asset_path)
    with wp.ScopedDevice(device):
        builder = newton.ModelBuilder(gravity=options.gravity_mps2, up_axis=newton.Axis.Z)
        builder.add_usd(
            asset_path,
            collapse_fixed_joints=options.collapse_fixed_joints,
            enable_self_collisions=options.enable_self_collisions,
            hide_collision_shapes=options.hide_collision_shapes,
            load_visual_shapes=options.load_visual_shapes,
            skip_mesh_approximation=True,
        )
        if options.mesh_approximation:
            builder.approximate_meshes(options.mesh_approximation)
        return _run_articulation_builder_runtime(
            builder=builder,
            newton=newton,
            device=device,
            options=options,
        )


def _run_generated_package_robot_task_runtime(
    *,
    asset_path: str,
    collision_package: CollisionPackage | Mapping[str, object] | None,
    newton,
    wp,
    device: str,
    options: ArticulationSmokeOptions,
) -> tuple[dict[str, object], dict[str, object], dict[str, object], dict[str, object]]:
    if not Path(asset_path).exists():
        raise FileNotFoundError(asset_path)
    ignore_paths = _source_geometry_ignore_paths(asset_path)
    with wp.ScopedDevice(device):
        builder = newton.ModelBuilder(gravity=options.gravity_mps2, up_axis=newton.Axis.Z)
        import_result = builder.add_usd(
            asset_path,
            collapse_fixed_joints=options.collapse_fixed_joints,
            enable_self_collisions=options.enable_self_collisions,
            hide_collision_shapes=True,
            load_visual_shapes=False,
            skip_mesh_approximation=True,
            ignore_paths=ignore_paths,
        )
        source_shape_count = int(builder.shape_count)
        package_metrics = _attach_generated_package_shapes(
            builder=builder,
            wp=wp,
            newton=newton,
            path_body_map=import_result.get("path_body_map", {}),
            collision_package=collision_package,
            source_shape_count=source_shape_count,
            ignored_source_shape_paths=ignore_paths,
            enable_self_collisions=options.enable_self_collisions,
        )
        import_metrics, gravity_hold_metrics, trajectory_metrics = (
            _run_articulation_builder_runtime(
                builder=builder,
                newton=newton,
                device=device,
                options=options,
            )
        )
    return import_metrics, gravity_hold_metrics, trajectory_metrics, package_metrics


def _run_articulation_builder_runtime(
    *,
    builder,
    newton,
    device: str,
    options: ArticulationSmokeOptions,
) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    model = builder.finalize(device=device)
    state_0 = model.state()
    state_1 = model.state()
    control = model.control()
    contacts = model.contacts()
    solver = newton.solvers.SolverXPBD(model, iterations=options.iterations)

    initial_joint_q = state_0.joint_q.numpy().copy()
    zero_joint_qd = np.zeros_like(state_0.joint_qd.numpy())
    control.joint_target_pos.assign(initial_joint_q)
    control.joint_target_vel.assign(zero_joint_qd)
    max_contact_count = 0
    finite_state = True
    completed_steps = 0
    for _ in range(options.hold_frames):
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
            if not _state_is_finite(state_0):
                finite_state = False
                break
        if not finite_state:
            break
    hold_joint_q = state_0.joint_q.numpy().copy()
    max_joint_drift = (
        0.0
        if len(initial_joint_q) == 0
        else float(np.max(np.abs(hold_joint_q - initial_joint_q)))
    )

    initial_body_q = state_0.body_q.numpy().copy()
    target_joint_q, commanded_index, commanded_delta = _trajectory_target(
        hold_joint_q,
        model,
        options,
    )
    state_0.joint_q.assign(target_joint_q)
    state_0.joint_qd.assign(np.zeros_like(state_0.joint_qd.numpy()))
    newton.eval_fk(model, state_0.joint_q, state_0.joint_qd, state_0)
    trajectory_body_q = state_0.body_q.numpy().copy()
    trajectory_finite = bool(np.all(np.isfinite(trajectory_body_q)))
    end_effector_delta = _end_effector_delta(initial_body_q, trajectory_body_q)

    import_metrics = {
        "articulation_count": int(getattr(model, "articulation_count", 0)),
        "joint_count": int(getattr(model, "joint_count", 0)),
        "joint_dof_count": int(getattr(model, "joint_dof_count", 0)),
        "body_count": int(getattr(model, "body_count", 0)),
        "shape_count": int(getattr(model, "shape_count", 0)),
    }
    gravity_hold_metrics = {
        "finite_state": finite_state,
        "completed_steps": completed_steps,
        "max_joint_drift": max_joint_drift,
        "max_contact_count": max_contact_count,
    }
    trajectory_metrics = {
        "finite_state": trajectory_finite,
        "commanded_joint_index": commanded_index,
        "commanded_joint_delta": commanded_delta,
        "end_effector_pose_delta_m": end_effector_delta,
    }
    return import_metrics, gravity_hold_metrics, trajectory_metrics


def _trajectory_target(
    joint_q: np.ndarray,
    model,
    options: ArticulationSmokeOptions,
) -> tuple[np.ndarray, int | None, float]:
    if len(joint_q) == 0:
        return joint_q.copy(), None, 0.0
    target = joint_q.copy()
    lower = model.joint_limit_lower.numpy() if hasattr(model.joint_limit_lower, "numpy") else None
    upper = model.joint_limit_upper.numpy() if hasattr(model.joint_limit_upper, "numpy") else None
    for index in range(len(target)):
        delta = options.trajectory_delta_rad
        if lower is not None and upper is not None and index < len(lower) and index < len(upper):
            low = float(lower[index])
            high = float(upper[index])
            if math.isfinite(low) and math.isfinite(high) and high > low:
                delta = min(delta, max((high - low) * 0.1, 0.0))
                target[index] = min(max(float(target[index]) + delta, low), high)
                actual_delta = float(target[index] - joint_q[index])
                if abs(actual_delta) > 0.0:
                    return target, index, actual_delta
                continue
        target[index] = float(target[index]) + delta
        return target, index, delta
    return target, None, 0.0


def _end_effector_delta(initial_body_q: np.ndarray, trajectory_body_q: np.ndarray) -> float:
    if len(initial_body_q) == 0 or len(trajectory_body_q) == 0:
        return 0.0
    initial = np.asarray(initial_body_q[-1, :3], dtype=float)
    final = np.asarray(trajectory_body_q[-1, :3], dtype=float)
    return float(np.linalg.norm(final - initial))


def _state_is_finite(state) -> bool:
    return bool(
        np.all(np.isfinite(state.body_q.numpy()))
        and np.all(np.isfinite(state.body_qd.numpy()))
        and np.all(np.isfinite(state.joint_q.numpy()))
        and np.all(np.isfinite(state.joint_qd.numpy()))
    )


def _attach_generated_package_shapes(
    *,
    builder,
    wp,
    newton,
    path_body_map: Mapping[str, object],
    collision_package: CollisionPackage | Mapping[str, object] | None,
    source_shape_count: int,
    ignored_source_shape_paths: list[str],
    enable_self_collisions: bool,
) -> dict[str, object]:
    package_id, primitives = _package_primitives(collision_package)
    shape_cfg = newton.ModelBuilder.ShapeConfig(density=0.0, is_visible=False)
    source_links: set[str] = set()
    consumed_links: set[str] = set()
    missing_body_links: set[str] = set()
    unsupported_primitives: list[str] = []
    invalid_box_primitives: list[str] = []
    generated_shape_labels: list[str] = []
    generated_shape_ids: list[int] = []

    for primitive in primitives:
        primitive_id = str(primitive.get("primitive_id") or f"primitive:{len(generated_shape_labels)}")
        frame = str(primitive.get("frame") or "")
        primitive_source_links = primitive.get("source_links") or ([frame] if frame else [])
        if isinstance(primitive_source_links, list | tuple):
            source_links.update(str(link) for link in primitive_source_links if str(link))
        elif primitive_source_links:
            source_links.add(str(primitive_source_links))
        if str(primitive.get("kind") or "") != "box":
            unsupported_primitives.append(primitive_id)
            continue
        half_extents = _box_half_extents(primitive)
        center = _box_center(primitive)
        if half_extents is None or center is None or not frame:
            invalid_box_primitives.append(primitive_id)
            continue
        body_index = _resolve_body_index(path_body_map, frame)
        if body_index is None:
            missing_body_links.add(frame)
            continue
        label = f"generated:{primitive_id}"
        shape_id = builder.add_shape_box(
            body=body_index,
            xform=wp.transform(wp.vec3(*center), wp.quat_identity()),
            hx=half_extents[0],
            hy=half_extents[1],
            hz=half_extents[2],
            cfg=shape_cfg,
            label=label,
        )
        consumed_links.add(frame)
        generated_shape_ids.append(int(shape_id))
        generated_shape_labels.append(label)

    generated_self_collision_filter_pair_count = 0
    if not enable_self_collisions:
        for left_index, shape_a in enumerate(generated_shape_ids):
            for shape_b in generated_shape_ids[left_index + 1 :]:
                builder.add_shape_collision_filter_pair(shape_a, shape_b)
                generated_self_collision_filter_pair_count += 1

    return _json_safe(
        {
            "package_id": package_id,
            "package_primitive_count": len(primitives),
            "source_link_count": len(source_links),
            "source_links": sorted(source_links),
            "generated_collision_shape_count": len(generated_shape_labels),
            "consumed_primitive_count": len(generated_shape_labels),
            "consumed_links": sorted(consumed_links),
            "missing_body_link_count": len(missing_body_links),
            "missing_body_links": sorted(missing_body_links),
            "unsupported_primitive_count": len(unsupported_primitives),
            "unsupported_primitives": unsupported_primitives,
            "invalid_box_primitive_count": len(invalid_box_primitives),
            "invalid_box_primitives": invalid_box_primitives,
            "source_usd_shape_count": source_shape_count,
            "source_usd_shapes_ignored_count": len(ignored_source_shape_paths),
            "source_usd_shapes_ignored": list(ignored_source_shape_paths),
            "generated_shape_labels": generated_shape_labels,
            "generated_self_collision_filter_pair_count": generated_self_collision_filter_pair_count,
        }
    )


def _package_input_metrics(
    collision_package: CollisionPackage | Mapping[str, object] | None,
) -> dict[str, object]:
    package_id, primitives = _package_primitives(collision_package)
    source_links = _source_links_from_primitives(primitives)
    return {
        "package_id": package_id,
        "package_primitive_count": len(primitives),
        "source_link_count": len(source_links),
        "source_links": sorted(source_links),
        "generated_collision_shape_count": 0,
        "consumed_primitive_count": 0,
        "consumed_links": [],
        "missing_body_link_count": 0,
        "missing_body_links": [],
        "unsupported_primitive_count": 0,
        "unsupported_primitives": [],
        "invalid_box_primitive_count": 0,
        "invalid_box_primitives": [],
        "source_usd_shape_count": 0,
        "source_usd_shapes_ignored_count": 0,
        "source_usd_shapes_ignored": [],
        "generated_shape_labels": [],
        "generated_self_collision_filter_pair_count": 0,
    }


def _package_primitives(
    collision_package: CollisionPackage | Mapping[str, object] | None,
) -> tuple[str, list[dict[str, object]]]:
    if collision_package is None:
        return "", []
    if isinstance(collision_package, CollisionPackage):
        return collision_package.package_id, [
            _primitive_to_mapping(primitive) for primitive in collision_package.primitives
        ]
    if isinstance(collision_package, Mapping):
        raw_primitives = collision_package.get("primitives", [])
        primitives = [
            _primitive_to_mapping(primitive)
            for primitive in raw_primitives
            if isinstance(primitive, Mapping | PrimitiveSpec)
        ]
        return str(collision_package.get("package_id") or ""), primitives
    return "", []


def _primitive_to_mapping(primitive: Mapping[str, object] | PrimitiveSpec) -> dict[str, object]:
    if isinstance(primitive, PrimitiveSpec):
        return primitive.to_dict()
    return dict(primitive)


def _source_links_from_primitives(primitives: list[Mapping[str, object]]) -> set[str]:
    source_links: set[str] = set()
    for primitive in primitives:
        frame = str(primitive.get("frame") or "")
        raw_links = primitive.get("source_links") or ([frame] if frame else [])
        if isinstance(raw_links, list | tuple):
            source_links.update(str(link) for link in raw_links if str(link))
        elif raw_links:
            source_links.add(str(raw_links))
    return source_links


def _box_half_extents(primitive: Mapping[str, object]) -> tuple[float, float, float] | None:
    dimensions = primitive.get("dimensions")
    raw_half_extents: object
    if isinstance(dimensions, Mapping):
        raw_half_extents = dimensions.get("half_extents")
    else:
        raw_half_extents = dimensions
    if not isinstance(raw_half_extents, list | tuple) or len(raw_half_extents) != 3:
        return None
    half_extents = tuple(float(value) for value in raw_half_extents)
    if any((not math.isfinite(value) or value <= 0.0) for value in half_extents):
        return None
    return half_extents


def _box_center(primitive: Mapping[str, object]) -> tuple[float, float, float] | None:
    raw_center = primitive.get("center", (0.0, 0.0, 0.0))
    if not isinstance(raw_center, list | tuple) or len(raw_center) != 3:
        return None
    center = tuple(float(value) for value in raw_center)
    if any(not math.isfinite(value) for value in center):
        return None
    return center


def _resolve_body_index(path_body_map: Mapping[str, object], frame: str) -> int | None:
    candidates = [frame]
    if frame:
        candidates.append(f"/{frame.strip('/')}")
        candidates.append(frame.strip("/"))
    for candidate in candidates:
        if candidate in path_body_map:
            body_index = int(path_body_map[candidate])
            if body_index >= 0:
                return body_index
    return None


def _source_geometry_ignore_paths(asset_path: str) -> list[str]:
    try:
        from pxr import Usd, UsdGeom, UsdPhysics
    except ModuleNotFoundError:
        return []

    stage = Usd.Stage.Open(str(asset_path))
    if stage is None:
        return []
    geometry_types = tuple(
        usd_type
        for type_name in ("Mesh", "Cube", "Sphere", "Capsule", "Cylinder", "Cone", "Plane")
        if (usd_type := getattr(UsdGeom, type_name, None)) is not None
    )
    ignore_paths: list[str] = []
    for prim in stage.Traverse():
        if prim.HasAPI(UsdPhysics.RigidBodyAPI):
            continue
        if any(prim.IsA(usd_type) for usd_type in geometry_types):
            ignore_paths.append(str(prim.GetPath()))
    return ignore_paths


def _blocked_report(
    *,
    asset_path: str,
    status: str,
    outcome: str,
    reason: str,
    environment: EnvironmentReport | None,
    device: str,
    options: ArticulationSmokeOptions,
    claim_boundary: str,
) -> dict[str, object]:
    return _json_safe(
        {
            "stage": "newton_articulation_smoke",
            "status": status,
            "outcome": outcome,
            "asset_path": asset_path,
            "probe_type": "articulation_smoke_if_robot",
            "device": device,
            "environment": environment.to_dict() if environment else None,
            "task_scope": ARTICULATION_SMOKE_TASK_SCOPE,
            "initial_conditions": options.to_initial_conditions(),
            "solver": {**options.to_solver_dict(), "device": device},
            "metrics": {},
            "failure_labels": [],
            "fallback_reason": reason,
            "claim_boundary": claim_boundary,
            "evidence_level": ARTICULATION_SMOKE_EVIDENCE_LEVEL,
        }
    )


def _runtime_exception_report(
    *,
    asset_path: str,
    environment: EnvironmentReport,
    device: str,
    options: ArticulationSmokeOptions,
    claim_boundary: str,
    reason: str,
) -> dict[str, object]:
    return _json_safe(
        {
            "stage": "newton_articulation_smoke",
            "status": "runtime_failure",
            "outcome": "failure",
            "asset_path": asset_path,
            "probe_type": "articulation_smoke_if_robot",
            "device": device,
            "environment": environment.to_dict(),
            "task_scope": ARTICULATION_SMOKE_TASK_SCOPE,
            "initial_conditions": options.to_initial_conditions(),
            "solver": {**options.to_solver_dict(), "device": device},
            "metrics": {},
            "failure_labels": ["runtime_exception"],
            "fallback_reason": reason,
            "claim_boundary": claim_boundary,
            "evidence_level": ARTICULATION_SMOKE_EVIDENCE_LEVEL,
        }
    )


def _generated_package_blocked_report(
    *,
    asset_path: str,
    status: str,
    outcome: str,
    reason: str,
    environment: EnvironmentReport | None,
    device: str,
    options: ArticulationSmokeOptions,
    claim_boundary: str,
    package_metrics: Mapping[str, object],
) -> dict[str, object]:
    return _json_safe(
        {
            "stage": "newton_generated_package_robot_task_probe",
            "status": status,
            "outcome": outcome,
            "asset_path": asset_path,
            "probe_type": GENERATED_PACKAGE_ROBOT_TASK_PROBE_TYPE,
            "device": device,
            "environment": environment.to_dict() if environment else None,
            "task_scope": GENERATED_PACKAGE_ROBOT_TASK_SCOPE,
            "initial_conditions": {
                **options.to_initial_conditions(),
                "collision_source": "generated_link_aware_package",
                "source_usd_collision_shapes": "ignored_when_separate_from_rigid_body",
            },
            "solver": {**options.to_solver_dict(), "device": device},
            "metrics": {
                "generated_package_consumed": False,
                "package_consumption": dict(package_metrics),
            },
            "failure_labels": [],
            "fallback_reason": reason,
            "claim_boundary": claim_boundary,
            "evidence_level": GENERATED_PACKAGE_ROBOT_TASK_EVIDENCE_LEVEL,
        }
    )


def _generated_package_runtime_exception_report(
    *,
    asset_path: str,
    environment: EnvironmentReport,
    device: str,
    options: ArticulationSmokeOptions,
    claim_boundary: str,
    reason: str,
    package_metrics: Mapping[str, object],
) -> dict[str, object]:
    return _json_safe(
        {
            "stage": "newton_generated_package_robot_task_probe",
            "status": "runtime_failure",
            "outcome": "failure",
            "asset_path": asset_path,
            "probe_type": GENERATED_PACKAGE_ROBOT_TASK_PROBE_TYPE,
            "device": device,
            "environment": environment.to_dict(),
            "task_scope": GENERATED_PACKAGE_ROBOT_TASK_SCOPE,
            "initial_conditions": {
                **options.to_initial_conditions(),
                "collision_source": "generated_link_aware_package",
                "source_usd_collision_shapes": "ignored_when_separate_from_rigid_body",
            },
            "solver": {**options.to_solver_dict(), "device": device},
            "metrics": {
                "generated_package_consumed": False,
                "package_consumption": dict(package_metrics),
            },
            "failure_labels": ["runtime_exception"],
            "fallback_reason": reason,
            "claim_boundary": claim_boundary,
            "evidence_level": GENERATED_PACKAGE_ROBOT_TASK_EVIDENCE_LEVEL,
        }
    )


def _outcome_for_status(status: str) -> str:
    if status == "smoke_passed":
        return "accept"
    if status == "dependency_gap":
        return "dependency_gap"
    if status == "not_applicable":
        return "not_applicable"
    return "failure"


def _int_metric(metrics: Mapping[str, object], key: str) -> int:
    return int(metrics.get(key, 0) or 0)


def _float_metric(metrics: Mapping[str, object], key: str) -> float:
    return float(metrics.get(key, 0.0) or 0.0)


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


def _json_safe(value: object) -> object:
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, list | tuple):
        return [_json_safe(item) for item in value]
    return value
