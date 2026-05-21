# 2026-05-21 Franka Cost-Guided Merge Opt-In Probe

## Date

2026-05-21

## Status

Complete.

## Changes

- Added `cpd_like.native_opt_in_merge_search_policy` as an explicit real-USD opt-in config key.
- The default `legacy` and `native` lanes keep `cpd_like.merge_search_policy`.
- Only the configured `native_opt_in` lane receives the opt-in merge-search policy override.
- Added `configs/experiments/franka_native_opt_in_cost_guided_merge_probe.yaml` as a capped
  Franka first-mesh diagnostic. It composes:
  - default `merge_search_policy: topology_then_virtual` for legacy/native lanes;
  - `native_opt_in_merge_search_policy: cost_guided_pairwise`;
  - the existing native opt-in cylinder selection guard;
  - the existing native opt-in cylinder support-threshold relaxation;
  - no `native_opt_in_primitive_score_multipliers`.

## Verification

- `python -m pytest tests/test_real_usd_native_comparison.py::test_real_usd_native_fitting_report_applies_opt_in_merge_search_policy_only_to_opt_in_lane tests/test_cli.py::test_cli_run_real_usd_native_fitting_comparison_reads_opt_in_merge_search_policy -q`:
  first exited nonzero before implementation, then exited `0` with `2 passed`.
- `python -m pytest tests/test_cpd_like_config.py::test_franka_native_opt_in_cost_guided_merge_probe_config_is_claim_bounded -q`:
  first exited nonzero before the config existed, then exited `0` with `1 passed`.
- `PYTHONPATH=/cpfs/user/zhuzihou/dev/physics-primitive-agent/.worktrees/opt-in-merge-search-slice/src:$PYTHONPATH timeout 180s python -m primitive_collision_compiler.cli --config configs/experiments/franka_native_opt_in_cost_guided_merge_probe.yaml --run-real-usd-native-fitting-comparison`:
  exit `0`, generated
  `reports/generated/franka_native_opt_in_cost_guided_merge_probe/fitting.json` with report
  `status: smoke_passed`.
- Fitting report summary: capped Franka legacy/native lanes selected `32` boxes with
  `topology_then_virtual`; the `native_opt_in` lane selected `25` boxes plus `7` cylinders with
  `cost_guided_pairwise`. The native and native-opt-in collision packages differ, and the opt-in
  comparison records `native_uses_extended_primitive: true`.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=/cpfs/user/zhuzihou/dev/physics-primitive-agent/.worktrees/opt-in-merge-search-slice/src:$PYTHONPATH timeout 300s /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/franka_native_opt_in_cost_guided_merge_probe.yaml --run-real-usd-native-contact-comparison`:
  exit `0`, generated
  `reports/generated/franka_native_opt_in_cost_guided_merge_probe/contact.json` with report
  `status: smoke_passed`.
- Contact report summary: capped Franka legacy/native/native-opt-in lanes all passed the contact
  canary with no fallback reason; native-opt-in retained `25` boxes plus `7` cylinders.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=/cpfs/user/zhuzihou/dev/physics-primitive-agent/.worktrees/opt-in-merge-search-slice/src:$PYTHONPATH timeout 600s /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/franka_native_opt_in_cost_guided_merge_probe.yaml --run-real-usd-native-task-comparison`:
  exit `0`, generated
  `reports/generated/franka_native_opt_in_cost_guided_merge_probe/task.json` with report
  `status: smoke_passed`.
- Task report summary: capped Franka legacy/native/native-opt-in lanes all passed contact,
  drop/settle, and sphere-rain. The `native_opt_in` lane retained `25` boxes plus `7` cylinders
  through the contact-gated Newton task smokes. The Newton logs include inertia-validation
  correction warnings, while the JSON diagnostic statuses remain `smoke_passed`.

## Triage Notes

- A two-role bed plus Franka cost-guided version was not adopted as the passing evidence package.
- With `bed_dev_smoke: 64` and `franka_import_smoke: 64`, fitting passed, but the capped bed
  legacy/native/native-opt-in lanes failed the drop/settle and sphere-rain task probes. This
  showed the 64-face capped bed package was too coarse for the current task-smoke settings.
- With `bed_dev_smoke: 128` and `franka_import_smoke: 64`, fitting exceeded the `180s` smoke
  timeout before producing a report. This kept the cost-guided real-USD slice scoped to capped
  Franka for this record.

## Artifacts

- Config:
  `configs/experiments/franka_native_opt_in_cost_guided_merge_probe.yaml`.
- Fitting report:
  `reports/generated/franka_native_opt_in_cost_guided_merge_probe/fitting.json` (ignored; not
  committed).
- Contact report:
  `reports/generated/franka_native_opt_in_cost_guided_merge_probe/contact.json` (ignored; not
  committed).
- Newton task report:
  `reports/generated/franka_native_opt_in_cost_guided_merge_probe/task.json` (ignored; not
  committed).

## Claim Impact

- Supports only that the capped Franka first-mesh `native_opt_in` lane can use
  `cost_guided_pairwise` merge search, change the package from `32` boxes to `25` boxes plus `7`
  cylinders under the recorded guard/support-threshold controls, fully map to Newton shapes, and
  pass the recorded contact/drop/sphere smokes.
- Supports that `cpd_like.native_opt_in_merge_search_policy` is an opt-in lane control and does
  not change the default legacy/native merge-search policy in the recorded tests.
- Does not support merge-policy superiority, collision-quality improvement, whole-robot Franka
  collider quality, benchmark evidence, default selector behavior, broad real-USD coverage, full
  CPD reproduction, deployment readiness, safety certification, or real-world transfer.

## Next Action

- Treat this as the first real-USD cost-guided package-changing Newton-smoke slice. The next useful
  slice should either make the cost-guided search cheaper for broader two-role smoke configs or
  target another clearly scoped package-changing real-USD lane with the same claim boundaries.
