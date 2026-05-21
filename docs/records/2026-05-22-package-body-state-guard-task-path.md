# 2026-05-22 Package Body-State Guard Task Path

## Date

2026-05-22

## Status

Complete for an explicitly opt-in package body-state guard task path. Not complete as physical
root-cause proof, a validated repair, calibrated thresholds, a default selector policy,
collision-quality validation, or safety evidence.

## Changes

- Added `cpd_like.native_opt_in_package_body_state_guard` as an explicit config/CLI option.
- Wired the package body-state guard into the real-USD native contact/task comparison path:
  flagged `native_opt_in` packages run task probes against the native package, while unflagged
  packages keep the `native_opt_in` package.
- Added `configs/experiments/bed_franka_native_opt_in_package_body_state_guard_probe.yaml` as a
  two-role capped bed/Franka probe. It combines the bed cylinder score multiplier with the
  support-threshold opt-in needed for Franka cylinders, then applies the package body-state guard.
- A score-multiplier-only local fitting check was not used as goal evidence because capped Franka
  stayed box-only. The committed config adds the already claim-bounded support-threshold opt-in so
  both bed and Franka exercise selected cylinders before the package guard decision.

## Recorded Fitting Probe

Command:

```bash
PYTHONPATH=src \
timeout 180s python -m primitive_collision_compiler.cli \
  --config configs/experiments/bed_franka_native_opt_in_package_body_state_guard_probe.yaml \
  --run-real-usd-native-fitting-comparison \
  > reports/generated/bed_franka_native_opt_in_package_body_state_guard_probe/fitting_2026-05-22.json
```

Result:

- command exit `0`
- report `status: smoke_passed`
- capped bed native: `32` boxes
- capped bed native-opt-in candidate: `31` boxes plus `1` cylinder
- capped Franka native: `32` boxes
- capped Franka native-opt-in candidate: `23` boxes plus `9` cylinders

## Real Newton Task Probe

Command:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src \
timeout 600s /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m primitive_collision_compiler.cli \
  --config configs/experiments/bed_franka_native_opt_in_package_body_state_guard_probe.yaml \
  --run-real-usd-native-task-comparison \
  > reports/generated/bed_franka_native_opt_in_package_body_state_guard_probe/task_2026-05-22.json
```

Result:

- command exit `0`
- report `status: smoke_passed`
- Newton source commit recorded in the generated task report:
  `96713fa965463b69c229a4d30582c733ff3526bb`
- capped bed guard decision:
  - candidate lane: `native_opt_in`, `31` boxes plus `1` cylinder
  - `package_risk_class: large_flat_cylinder_body_state_delta_risk`
  - `decision: fallback_to_native_package`
  - effective task package: `bed_dev_smoke_native:cpd_like_component_merge_gate`
  - effective task type counts: `32` boxes
  - drop/settle and sphere-rain both `smoke_passed`
- capped Franka guard decision:
  - candidate lane: `native_opt_in`, `23` boxes plus `9` cylinders
  - `package_risk_class: not_flagged`
  - `decision: keep_native_opt_in_package`
  - effective task package: `franka_import_smoke_native_opt_in:cpd_like_component_merge_gate`
  - effective task type counts: `23` boxes plus `9` cylinders
  - drop/settle and sphere-rain both `smoke_passed`

The generated fitting and task reports are ignored by git under
`reports/generated/bed_franka_native_opt_in_package_body_state_guard_probe/`.

## Claim Impact

This advances the previous package body-state guard from report-candidate evidence into a real
task-path diagnostic: in one explicitly configured bed/Franka probe, the system first creates
cylinder-bearing native-opt-in candidates for both roles, then uses the package-level COM/inertia
proxy to fall back only the flagged bed package while preserving the unflagged Franka cylinder
package.

This still does not prove the physical root cause of the bed `not_settled` behavior. It does not
validate COM/inertia repair, calibrate guard thresholds, close contact/floor effects, prove
cylinders are broadly stable or unstable, or justify changing default selector behavior.

## Verification

- `python -m pytest tests/test_cpd_like_config.py::test_bed_franka_package_body_state_guard_probe_config_is_claim_bounded -q`:
  passed.
- Real fitting command above: exit `0`.
- Real Newton task command above: exit `0`.

## Next Action

Keep the long bed-vs-Franka cylinder mechanism goal active. The next useful step is a narrow
contact/floor closure or a same-report audit that explains why the flagged bed package needs
fallback beyond the proxy decision, without promoting this guard to a default policy.
