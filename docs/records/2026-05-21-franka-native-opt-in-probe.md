# 2026-05-21 Franka Native Opt-In Probe

## Date

2026-05-21

## Status

Complete

## Changes

- Added explicit real-USD opt-in config:
  `configs/experiments/franka_native_opt_in_probe.yaml`.
- Added optional `native_opt_in` real-USD comparison plumbing. Default `legacy` and `native` lanes
  remain unchanged unless `cpd_like.native_opt_in_primitive_score_multipliers` is configured.
- The opt-in lane keeps the same support-aware primitive-selection guard, then applies the existing
  primitive score multiplier mechanism to the configured native lane only.

## Verification

- `python -m pytest tests/test_real_usd_native_comparison.py tests/test_cli.py -k "real_usd_native" -q`:
  exit `0`, `27 passed, 105 deselected`.
- `python -m pytest tests/test_cpd_like_config.py::test_franka_native_opt_in_probe_config_is_real_usd_and_claim_bounded -q`:
  exit `0`, `1 passed`.
- `python -m pytest tests/test_cpd_like_config.py tests/test_real_usd_native_comparison.py tests/test_cli.py -k "native_opt_in or real_usd_native" -q`:
  exit `0`, `29 passed, 121 deselected`.
- `python scripts/validate_docs.py`: exit `0`, `docs validation passed`.
- `python scripts/validate_site_claims.py`: exit `0`, `site claim validation passed`.
- `git diff --check`: exit `0`.
- `PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --run-real-usd-native-fitting-comparison`:
  exit `0`, report `status: smoke_passed`. The default native lanes stayed box-only. A temporary
  opt-in fitting run with `cylinder: 0.5` selected `25` boxes plus `7` cylinders for capped bed and
  `24` boxes plus `8` cylinders for capped Franka, with both opt-in packages fully mapped.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --run-real-usd-native-task-comparison` with the temporary two-role opt-in setting:
  exit `2`, report `status: runtime_failure`. Capped bed opt-in contact passed for `box` and
  `cylinder`, but drop/settle failed with `not_settled` and `floor_breach`, and sphere-rain failed
  with `no_contact_observed` and `insufficient_contact_density`. Within that top-level
  `runtime_failure` report, the capped Franka opt-in case passed its contact-gated task smokes;
  the top-level run failed because capped bed opt-in failed drop/settle and sphere-rain.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/franka_native_opt_in_probe.yaml --run-real-usd-native-task-comparison`:
  exit `0`, report `status: smoke_passed`.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/franka_native_opt_in_probe.yaml --run-real-usd-native-task-comparison > reports/generated/franka_native_opt_in_probe/task_rerun_after_com_axis_2026-05-21.json`:
  exit `0`, report `status: smoke_passed`. This current-worktree rerun after the bed COM-axis
  diagnostic preserved the capped Franka opt-in passing task-smoke status.

Passing capped Franka result:

- default native lane: `32` boxes, fully mapped;
- opt-in native lane: `24` boxes and `8` cylinders, fully mapped;
- opt-in contact canaries: representative `box` and `cylinder` canaries both `smoke_passed`,
  contact count `1` each;
- opt-in drop/settle: `smoke_passed`, `2880` completed steps, final speed about
  `0.0011827 m/s`, no failure labels;
- opt-in sphere-rain: `smoke_passed`, `960` completed steps, contact-density proxy
  `0.1111111111111111`, no failure labels.

## Artifacts

- Config: `configs/experiments/franka_native_opt_in_probe.yaml`
- Passing report: `reports/generated/franka_native_opt_in_probe/task_2026-05-21.json` (ignored;
  not committed).
- Current-worktree rerun report:
  `reports/generated/franka_native_opt_in_probe/task_rerun_after_com_axis_2026-05-21.json`
  (ignored; not committed). Runtime logs are in the matching `.stderr` file.
- Failed two-role exploratory report:
  `reports/generated/bed_franka_native_probe_comparison/real_usd_native_task_opt_in_2026-05-21.json`
  (ignored; not committed).

## Claim Impact

- Supports that an explicitly opted-in capped Franka first-mesh package containing `24` boxes and
  `8` selected Newton-native `cylinder` primitives can be fully mapped; representative
  `box`/`cylinder` contact canaries and package-level drop/settle and sphere-rain smokes passed.
- Keeps the default capped bed/Franka support-aware config box-only.
- Does not support native primitive quality improvement, collision-quality validation, benchmark
  superiority, whole-robot Franka collider quality, real contact-stress measurement, full CPD
  reproduction, deployment readiness, safety certification, or real-world transfer.
- Records that the analogous capped bed opt-in package did not pass task gates under the same
  settings.

## Next Action

- Diagnose why the capped bed opt-in package passes contact but fails task smokes before expanding
  the opt-in real-USD native-exercising path beyond capped Franka.
