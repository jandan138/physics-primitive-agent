# 2026-05-15 Real USD Native Task Comparison

## Date

2026-05-15

## Status

Complete

## Supersession Note

This record captures the pre-cylinder-axis task comparison. It was superseded by
[2026-05-15 Candidate Loss Diagnosis And Cylinder Axis](2026-05-15-candidate-loss-diagnosis-and-cylinder-axis.md),
then by
[2026-05-15 Low-Support Native Extension Admissibility](2026-05-15-low-support-native-extension-admissibility.md).
The current support-aware status keeps capped Franka native box-only while reporting three cheaper
raw-cost cylinders as support-blocked diagnostic accounting. This supersession does not add
collision-quality evidence.

## Changes

- Added a gated real-USD old/new task comparison path.
- The task comparison runs contact canary first for each lane.
- Drop/settle and sphere-rain run only when contact canary status is `smoke_passed`.
- The final config uses the same robust bed-style task settings already used by prior bed
  Newton smokes.

## Verification

- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --run-real-usd-native-task-comparison`
  exited `0`.
- Report status: `smoke_passed`.

## Artifacts

- Config: `configs/experiments/bed_franka_native_probe_comparison.yaml`
- Report: `reports/generated/bed_franka_native_probe_comparison/real_usd_native_task_conda.json`

## Result Summary

- `bed_dev_smoke` legacy/native:
  - contact canary: `smoke_passed`;
  - drop/settle: `smoke_passed`, final speed about `0.0404565 m/s`;
  - sphere-rain: `smoke_passed`, contact-density proxy `0.1111111111111111`.
- `franka_import_smoke` legacy/native:
  - contact canary: `smoke_passed`;
  - drop/settle: `smoke_passed`, final speed about `0.0005830 m/s`;
  - sphere-rain: `smoke_passed`, contact-density proxy `0.1111111111111111`.

## Claim Impact

- Supports named real-USD task smoke evidence for capped bed and capped Franka first-mesh packages
  under recorded settings and environment.
- Because native and legacy lanes selected the same `box` primitives, this does not support a
  claim that the native lane improved the collision package.
- Does not support benchmark superiority, collision-quality validation, whole-robot Franka
  collider quality, paper-faithful CPD reproduction, or deployment readiness.

## Next Action

- Treat this as a pipeline milestone. The next algorithmic step is to improve primitive fitting or
  merge search so real USD assets can actually exercise native `cylinder`, `cone`, or `ellipsoid`
  choices before claiming native primitive value on assets.
