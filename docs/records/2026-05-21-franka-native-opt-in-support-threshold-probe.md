# 2026-05-21 Franka Native Opt-In Support Threshold Probe

## Date

2026-05-21

## Status

Complete.

## Changes

- Added an explicitly opt-in `native_opt_in_extension_support_thresholds` path for CPD-like
  primitive selection.
- The setting is only threaded into configured `native_opt_in` lanes. Default `legacy` and
  `native` lanes still use the existing support-aware thresholds.
- Added `configs/experiments/franka_native_opt_in_support_threshold_probe.yaml` for capped Franka
  first-mesh scope.
- The config lowers the opt-in extension support thresholds for `cylinder` candidates to
  `min_extension_source_faces: 2` and `min_extension_unique_points: 4`.

## Verification

- `python -m pytest tests/test_cpd_like_synthetic.py tests/test_cpd_like_decompose.py tests/test_real_usd_native_comparison.py tests/test_cli.py tests/test_cpd_like_config.py -q`:
  exit `0`, `254 passed`.
- `python -m pytest -q`: exit `0`, `2417 passed, 2 skipped`.
- `PYTHONPATH=src python -m primitive_collision_compiler.cli --config configs/experiments/franka_native_opt_in_support_threshold_probe.yaml --run-real-usd-native-fitting-comparison`:
  exit `0`, report `status: smoke_passed`. The default native lane selected `32` boxes; the
  support-threshold opt-in lane selected `29` boxes plus `3` cylinders and fully mapped.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/franka_native_opt_in_support_threshold_probe.yaml --run-real-usd-native-task-comparison`:
  exit `0`, report `status: smoke_passed`. Legacy, default native, and support-threshold
  opt-in lanes all passed contact, drop/settle, and sphere-rain. The stderr log includes Newton
  inertia-validation correction warnings, while the JSON diagnostic status remains `smoke_passed`.

## Artifacts

- Config:
  `configs/experiments/franka_native_opt_in_support_threshold_probe.yaml`.
- Fitting report:
  `reports/generated/franka_native_opt_in_support_threshold_probe/fitting_2026-05-21.json`
  (ignored; not committed).
- Newton task report:
  `reports/generated/franka_native_opt_in_support_threshold_probe/task_2026-05-21.json`
  (ignored; not committed).

## Claim Impact

- Supports only that the three capped Franka raw-cost support-blocked cylinder candidates can be
  admitted in a separate opt-in support-threshold lane and still pass the recorded mapping,
  contact, drop/settle, and sphere-rain smokes.
- Does not support changing default support thresholds, default selector policy, calibrated
  support thresholds, cylinder-quality improvement, benchmark evidence, whole-robot Franka
  collider quality, full CPD reproduction, deployment readiness, safety certification, or
  real-world transfer.

## Next Action

- Compare this opt-in support-threshold slice against the guarded selector slice when choosing
  the next package-changing fitting/selector target; keep default lanes unchanged unless a later
  record supplies stronger evidence.
