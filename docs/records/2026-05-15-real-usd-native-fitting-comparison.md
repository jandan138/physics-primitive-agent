# 2026-05-15 Real USD Native Fitting Comparison

## Date

2026-05-15

## Status

Complete

## Supersession Note

This record captures the pre-cylinder-axis real-USD baseline. Current status is superseded by
[2026-05-15 Candidate Loss Diagnosis And Cylinder Axis](2026-05-15-candidate-loss-diagnosis-and-cylinder-axis.md),
where capped bed remains `32` boxes and capped Franka native selects `29` boxes plus `3`
cylinders under the current surrogate.

## Changes

- Added a config-driven real-USD old/new native fitting comparison path.
- Added focused config `configs/experiments/bed_franka_native_probe_comparison.yaml`.
- Ran capped `bed_dev_smoke` and capped `franka_import_smoke` through both lanes:
  legacy `box`/`sphere`/`capsule` and native
  `box`/`sphere`/`capsule`/`cylinder`/`cone`/`ellipsoid`.

## Verification

- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --run-real-usd-native-fitting-comparison`
  exited `0`.
- Report status: `smoke_passed`.

## Artifacts

- Config: `configs/experiments/bed_franka_native_probe_comparison.yaml`
- Report: `reports/generated/bed_franka_native_probe_comparison/real_usd_native_fitting_conda.json`
- Manifest: `assets/manifests/cpd_like_smoke_assets.yaml`

## Result Summary

- `bed_dev_smoke`: legacy `32` boxes, native `32` boxes, mapping clean, native normalized volume
  delta `0.0`.
- `franka_import_smoke`: legacy `32` boxes, native `32` boxes, mapping clean, native normalized
  volume delta `0.0`.
- Current native lane selected no `cylinder`, `cone`, or `ellipsoid` on these capped real USD
  meshes.
- The regenerated report now includes `candidate_audit_summary`; both native lanes still have `0`
  clusters where an extension primitive is cheapest under the current surrogate.

## Claim Impact

- Supports a real-USD offline old/new diagnostic smoke for capped bed and capped Franka first-mesh
  scope.
- Does not support collision-quality improvement, benchmark superiority, broad asset coverage,
  whole-robot Franka collider quality, or paper-faithful CPD reproduction.

## Next Action

- Use the real-USD candidate audit summary to choose the next primitive-fitting or merge-search
  improvement before rerunning contact/task probes for native primitive value evidence.
