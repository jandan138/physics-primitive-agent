# 2026-05-15 Real USD Native Contact Comparison

## Date

2026-05-15

## Status

Complete

## Changes

- Added a real-USD old/new Newton contact comparison path.
- The comparison enforces full package mapping before contact canary, even though the raw canary
  API can run representative mapped types.
- Ran contact canaries for bed and Franka legacy/native packages generated from the real-USD
  comparison config.

## Verification

- Default shell Python run produced `dependency_gap` because `warp` was unavailable in that
  interpreter. The report was kept as
  `reports/generated/bed_franka_native_probe_comparison/real_usd_native_contact.json`.
- Clean Newton conda command:
  `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --run-real-usd-native-contact-comparison`
  exited `0`.
- Clean-env report status: `smoke_passed`.

## Artifacts

- Config: `configs/experiments/bed_franka_native_probe_comparison.yaml`
- Passing report:
  `reports/generated/bed_franka_native_probe_comparison/real_usd_native_contact_conda.json`
- Dependency-gap report:
  `reports/generated/bed_franka_native_probe_comparison/real_usd_native_contact.json`

## Result Summary

- `bed_dev_smoke` legacy/native: `32` mapped primitives, representative `box` contact canary
  passed with contact count `1`.
- `franka_import_smoke` legacy/native: `32` mapped primitives, representative `box` contact canary
  passed with contact count `1`.

## Claim Impact

- Supports a contact-only Newton consumption smoke for the capped bed and capped Franka old/new
  packages under the clean Newton conda environment.
- Does not support task-level quality, collision-quality validation, whole-robot Franka collider
  quality, benchmark evidence, or safety claims.

## Next Action

- Run drop/settle and sphere-rain only through the gated comparison path after contact canary
  passes for each lane.
