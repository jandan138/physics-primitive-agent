# 2026-05-26 Generated-Package Robot Task Probe

## Date

2026-05-26

## Status

Complete for the first generated-package robot task smoke over the Phase 0 Franka USD asset.

## Changes

- Added `generated_package_robot_task_if_robot` as a Phase 0 articulated-robot probe.
- Kept the existing `articulation_smoke_if_robot` source-USD import smoke as a separate check.
- Added a generated-package Newton path that:
  - imports the Franka body and joint tree from the source USD mirror;
  - ignores source USD geometry/collision shapes when they are separate from rigid-body prims;
  - attaches generated link-aware box primitives to Newton bodies by primitive `frame`;
  - runs with `collapse_fixed_joints: false` so all 12 detected Franka links remain addressable;
  - disables generated self-collision pairs when `enable_self_collisions: false`, matching the
    source articulation smoke's reproducible self-collision setting;
  - records package-consumption metrics next to gravity-hold and trajectory smoke metrics.

## Results

Generated report:

- `reports/generated/phase0_baseline/phase0_grscenes_rigid_plus_franka_newton_2026-05-26.json`

Overall recorded outcomes after adding the generated-package robot task probe:

- accept: 99
- dependency gap: 0
- failure: 11
- fallback: 30
- not applicable: 70

Report scope:

- rigid assets: 5 from `assets/manifests/phase0_assets.yaml`
- articulated assets: 1 from `assets/manifests/franka_usd_smoke_assets.yaml`
- `link_aware_robot_package_generation`: true
- `generated_package_robot_task_checks`: true
- `whole_robot_collision_quality`: false

Franka generated-package task summary:

| Metric | Value |
|---|---:|
| package primitives | 12 |
| package source links | 12 |
| generated Newton collision shapes | 12 |
| consumed package primitives | 12 |
| missing body links | 0 |
| source USD shapes remaining in generated-package run | 0 |
| source USD shapes ignored | 11 |
| generated self-collision filter pairs | 66 |
| Newton body count in generated-package run | 12 |
| Newton shape count in generated-package run | 12 |
| gravity-hold completed steps | 30 |
| gravity-hold max joint drift | 0.0 |
| trajectory end-effector pose delta (m) | 0.31682334509622223 |

The generated-package probe status is `smoke_passed`, outcome `accept`, and
`generated_package_consumed: true`.

## Verification

- `python -m pytest tests/test_newton_articulation_smoke.py tests/test_phase0_benchmark.py tests/test_configs.py -q`:
  19 passed.
- Direct Franka generated-package probe:
  `smoke_passed`, `generated_package_consumed: true`, 12 generated collision shapes over 12
  package primitives, zero source USD shapes remaining, and 66 generated self-collision filter
  pairs.
- `time -p timeout 1200 env NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/phase0_baseline.yaml --run-phase0-benchmark`:
  exit 0, `real 987.38`, report status `completed_with_recorded_failures`.
- Parsed the generated JSON successfully. The report records
  `generated_package_robot_task_checks: true` and the Franka generated-package task probe as
  `smoke_passed`.

## Artifacts

- Design: `docs/superpowers/specs/2026-05-26-generated-package-robot-task-probes-design.md`.
- Plan: `docs/superpowers/plans/2026-05-26-generated-package-robot-task-probes.md`.
- Config: `configs/experiments/phase0_baseline.yaml`.
- Generated report, ignored by git:
  `reports/generated/phase0_baseline/phase0_grscenes_rigid_plus_franka_newton_2026-05-26.json`.

## Claim Impact

- Supports the claim that one recorded Franka link-aware generated package is consumed by a named
  Newton robot task smoke under recorded settings.
- Supports only generated-package consumption, joint-tree import, gravity hold, and scripted
  kinematic trajectory for the recorded Franka USD smoke asset.
- Does not support whole-robot collider quality, manipulation performance, broad robot-operation
  validation, deployment readiness, real-world transfer, or safety certification.

## Next Action

Keep V-HACD probe-failure triage as a secondary baseline-stability task. The next robot-facing
step should broaden link-aware/generated-package checks to more robot assets or add a contact
operation smoke before any stronger robot-operation wording.
