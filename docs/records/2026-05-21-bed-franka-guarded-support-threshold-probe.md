# 2026-05-21 Bed Franka Guarded Support Threshold Probe

## Date

2026-05-21

## Status

Complete.

## Changes

- Added `configs/experiments/bed_franka_native_opt_in_guarded_support_threshold_probe.yaml` as a
  two-role capped bed plus capped Franka `native_opt_in` diagnostic.
- The config composes the existing opt-in large-flat-cylinder selection guard with the existing
  opt-in cylinder extension support-threshold relaxation.
- The config does not use `native_opt_in_primitive_score_multipliers`.
- Default `legacy` and `native` lanes remain support-aware and unchanged. The guard and relaxed
  support thresholds are threaded only into the explicitly configured `native_opt_in` lane.

## Verification

- `python -m pytest tests/test_cpd_like_config.py::test_bed_franka_native_opt_in_guarded_support_threshold_probe_config_is_claim_bounded -q`:
  first exited nonzero before the config existed, then exited `0` with `1 passed` after adding the
  config.
- `PYTHONPATH=src python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_opt_in_guarded_support_threshold_probe.yaml --run-real-usd-native-fitting-comparison`:
  generated `reports/generated/bed_franka_native_opt_in_guarded_support_threshold_probe/fitting_2026-05-21.json`
  with report `status: smoke_passed`.
- Fitting report summary: `bed_dev_smoke` legacy/native/native-opt-in all selected `32` boxes; the
  opt-in candidate audit reported `23` diagnostic guard rejected cylinder candidates. For
  `franka_import_smoke`, legacy/native selected `32` boxes, while `native_opt_in` selected `29`
  boxes plus `3` cylinders; the opt-in candidate audit reported `0` guard rejections and `23`
  support-blocked extension candidates.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_opt_in_guarded_support_threshold_probe.yaml --run-real-usd-native-contact-comparison`:
  exit `0`, generated `reports/generated/bed_franka_native_opt_in_guarded_support_threshold_probe/contact_2026-05-21.json`
  with report `status: smoke_passed`.
- Contact report summary: bed legacy/native/native-opt-in contacts all passed with `32` boxes;
  Franka legacy/native contacts passed with `32` boxes, and Franka native-opt-in contact passed
  with `29` boxes plus `3` cylinders. No contact lane reported a fallback reason.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_opt_in_guarded_support_threshold_probe.yaml --run-real-usd-native-task-comparison`:
  generated `reports/generated/bed_franka_native_opt_in_guarded_support_threshold_probe/task_2026-05-21.json`
  with report `status: smoke_passed`.
- Task report summary: bed and Franka legacy/native/native-opt-in lanes all passed contact,
  drop/settle, and sphere-rain. Franka native-opt-in retained `29` boxes plus `3` cylinders
  through the contact-gated task smokes. The Newton logs include inertia-validation correction
  warnings, while the JSON diagnostic statuses remain `smoke_passed`.

## Artifacts

- Config:
  `configs/experiments/bed_franka_native_opt_in_guarded_support_threshold_probe.yaml`.
- Fitting report:
  `reports/generated/bed_franka_native_opt_in_guarded_support_threshold_probe/fitting_2026-05-21.json`
  (ignored; not committed).
- Contact report:
  `reports/generated/bed_franka_native_opt_in_guarded_support_threshold_probe/contact_2026-05-21.json`
  (ignored; not committed).
- Newton task report:
  `reports/generated/bed_franka_native_opt_in_guarded_support_threshold_probe/task_2026-05-21.json`
  (ignored; not committed).

## Claim Impact

- Supports only that the opt-in guard and opt-in support-threshold relaxation can be composed in a
  single capped bed plus capped Franka diagnostic config without a score multiplier.
- Supports only this recorded package behavior: guarded bed remains `32` boxes and passes the
  recorded Newton smokes; guarded support-threshold Franka changes to `29` boxes plus `3`
  cylinders and also passes the recorded Newton smokes.
- Does not support changing default support-aware lanes, calibrating either threshold, validating
  cylinder collision quality, proving boxes or cylinders are broadly better, whole-robot Franka
  collider quality, benchmark evidence, full CPD reproduction, deployment readiness, safety
  certification, or real-world transfer.

## Next Action

- Treat this combined config as the current story-level opt-in evidence package for the
  bed/Franka Newton-in-the-loop selector narrative. The next useful slice should again change a
  package for a clear selector or fitting reason and rerun the same mapping/contact/task smokes.
