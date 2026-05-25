from __future__ import annotations

from dataclasses import dataclass
import math
from numbers import Integral
from pathlib import Path
from typing import Mapping

import numpy as np

from primitive_collision_compiler.newton.diagnostics import (
    _import_newton_runtime,
    _status_from_environment,
)
from primitive_collision_compiler.newton.env import inspect_newton_environment
from primitive_collision_compiler.reports.schema import EnvironmentReport

ARTICULATION_SMOKE_CLAIM_BOUNDARY = (
    "articulation_smoke_diagnostic_not_whole_robot_collision_quality_or_safety_validation"
)
ARTICULATION_SMOKE_EVIDENCE_LEVEL = "newton_articulation_smoke"
ARTICULATION_SMOKE_TASK_SCOPE = "single_articulated_asset_import_hold_kinematic_trajectory"


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
