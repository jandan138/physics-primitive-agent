# 2026-05-22 Cylinder Package Body-State Guard Candidate

## Date

2026-05-22

## Status

Complete for an opt-in diagnostic guard-candidate report. Not complete as root-cause proof,
validated repair, or default selector policy.

## Changes

- Extended `cylinder_package_body_state_risk_probe` with `package_body_state_guard` decisions.
- The guard decision uses the existing package COM/inertia proxy risk class:
  - flagged packages recommend `fallback_to_native_package`;
  - unflagged packages recommend `keep_native_opt_in_package`.
- The diagnostic script now carries both native and native-opt-in task evidence into the report,
  so the recommended lane records its existing Newton task status.

## Recorded Real-Report Probe

Command:

```bash
PYTHONPATH=src python scripts/diagnostics/cylinder_package_risk_probe.py \
  --bed-task-report /cpfs/user/zhuzihou/dev/physics-primitive-agent/reports/generated/cylinder_stability_mechanism/bed_task.json \
  --franka-task-report /cpfs/user/zhuzihou/dev/physics-primitive-agent/reports/generated/cylinder_stability_mechanism/franka_cost_guided_task.json \
  --output reports/generated/cylinder_package_risk/bed_franka_package_guard_worktree.json
```

Result:

- `status: diagnostic_recorded`
- bed `package_risk_class: large_flat_cylinder_body_state_delta_risk`
- bed `package_body_state_guard.decision: fallback_to_native_package`
- bed recommended lane recorded task status: `smoke_passed`
- Franka `package_risk_class: not_flagged`
- Franka `package_body_state_guard.decision: keep_native_opt_in_package`
- Franka recommended lane recorded task status: `smoke_passed`

The generated report is ignored by git under
`reports/generated/cylinder_package_risk/bed_franka_package_guard_worktree.json`.

## Real Newton Rerun

Command:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src \
timeout 600s /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m primitive_collision_compiler.cli \
  --config configs/experiments/bed_franka_native_opt_in_guarded_support_threshold_probe.yaml \
  --run-real-usd-native-task-comparison \
  > reports/generated/bed_franka_native_opt_in_guarded_support_threshold_probe/task_2026-05-22_package_guard_worktree.json
```

Result:

- command exit `0`
- report `status: smoke_passed`
- capped bed guarded native-opt-in lane: `32` boxes, drop/settle `smoke_passed`, sphere-rain
  `smoke_passed`
- capped Franka guarded support-threshold native-opt-in lane: `29` boxes plus `3` cylinders,
  drop/settle `smoke_passed`, sphere-rain `smoke_passed`

The generated task report is ignored by git under
`reports/generated/bed_franka_native_opt_in_guarded_support_threshold_probe/task_2026-05-22_package_guard_worktree.json`.

## Claim Impact

This advances the prior report-only package-risk probe into an opt-in diagnostic guard-candidate
decision: the package-level proxy recommends rejecting the recorded capped bed risky opt-in
cylinder package and retaining the recorded capped Franka cost-guided cylinder package.

This still does not prove the physical root cause, validate a general COM/inertia repair, close
contact/floor effects, calibrate thresholds, or establish a default selector policy. The real
Newton rerun validates the existing configured guard/support-threshold package under the recorded
task smokes; it is one configured diagnostic slice, not broad asset evidence.

## Verification

- `python -m pytest tests/test_cylinder_package_risk.py -q`
- `python -m pytest tests/test_bootstrap_command_surface.py::test_cylinder_package_risk_probe_builds_bed_franka_report tests/test_cylinder_package_risk.py -q`
- Real-report probe command above, exit `0`
- Real Newton rerun command above, exit `0`

## Next Action

Either wire this package-level guard candidate into a named opt-in package-selection path, or run a
narrow contact/floor closure audit for the bed-vs-Franka contrast before considering the long
cylinder mechanism goal complete.
