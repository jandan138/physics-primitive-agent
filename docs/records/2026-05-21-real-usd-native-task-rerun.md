# 2026-05-21 Real USD Native Task Rerun

## Date

2026-05-21

## Status

Complete

## Changes

- Reused the documented clean Newton conda environment:
  `/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python`.
- Reused the documented Newton checkout:
  `/cpfs/user/zhuzihou/dev/newton`.
- Re-ran the existing real-USD native task comparison over capped `bed_dev_smoke` and capped
  `franka_import_smoke` old/new packages.

## Verification

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src \
/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m primitive_collision_compiler.cli \
  --config configs/experiments/bed_franka_native_probe_comparison.yaml \
  --run-real-usd-native-task-comparison \
  > reports/generated/bed_franka_native_probe_comparison/real_usd_native_task_2026-05-21.json
```

Observed result: exit `0`, report `status: smoke_passed`, stage
`newton_real_usd_native_task_comparison`, claim boundary
`real_usd_native_task_smoke_not_collision_quality_or_safety`.

Result summary:

- `bed_dev_smoke` legacy and native lanes both selected `box` only, mapped `32` primitives, passed
  contact canary with contact count `1`, passed drop/settle with `2880` completed steps and final
  speed about `0.0404565 m/s`, and passed sphere-rain with `960` completed steps, `9` probes, and
  contact-density proxy `0.1111111111111111`.
- `franka_import_smoke` legacy and native lanes both selected `box` only, mapped `32` primitives,
  passed contact canary with contact count `1`, passed drop/settle with `2880` completed steps and
  final speed about `0.0005830 m/s`, and passed sphere-rain with `960` completed steps, `9`
  probes, and contact-density proxy `0.1111111111111111`.

## Artifacts

- Config: `configs/experiments/bed_franka_native_probe_comparison.yaml`
- Generated report:
  `reports/generated/bed_franka_native_probe_comparison/real_usd_native_task_2026-05-21.json`
  (ignored; not committed).

## Claim Impact

- Supports that the documented clean Newton environment still runs the existing real-USD capped
  bed/Franka contact-gated task smoke path.
- Because legacy and native lanes both selected `box` only in this rerun, it does not support a
  native primitive improvement claim.
- Does not support collision-quality validation, benchmark superiority, whole-robot Franka
  collider quality, real contact-stress measurement, full CPD reproduction, deployment readiness,
  safety certification, or real-world transfer.

## Next Action

- Use this rerun as the current runtime evidence floor, then focus the next implementation step on
  changing the fitting or merge-search behavior enough for real-USD assets to exercise native
  primitives under the same Newton gates.
