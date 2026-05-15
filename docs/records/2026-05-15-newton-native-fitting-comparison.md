# 2026-05-15 Newton Native Fitting Comparison

## Date

2026-05-15

## Status

Complete

## Changes

- Added opt-in CPD-like fitting proxies for Newton-native `cylinder`, `cone`, and `ellipsoid`.
- Added `build_newton_native_fitting_comparison_report()`.
- Added `npc-compile --run-newton-native-fitting-comparison`.
- Added `configs/experiments/newton_native_fitting_comparison.yaml`.
- Added a plain-language reference note for the native fitting comparison.
- Declared bed and Franka USD roles as the next real-asset scope for this comparison.

## Verification

- `python -m pytest tests/test_cpd_like_synthetic.py::test_newton_native_fitting_comparison_selects_native_primitives tests/test_cpd_like_synthetic.py::test_newton_native_fitting_comparison_report_is_strict_json_serializable -q`
- `python -m pytest tests/test_cpd_like_synthetic.py::test_cone_proxy_stays_finite_when_forced_on_non_cone_fixture -q`
- `python -m pytest tests/test_cpd_like_synthetic.py::test_newton_native_fitting_comparison_respects_custom_legacy_subset tests/test_cpd_like_synthetic.py::test_cylinder_proxy_floors_zero_span_volume tests/test_cpd_like_synthetic.py::test_newton_native_fitting_comparison_selects_native_primitives -q`
- `python -m pytest tests/test_cli.py::test_cli_run_newton_native_fitting_comparison_emits_json_without_config tests/test_cli.py::test_cli_run_newton_native_fitting_comparison_rejects_non_finite_json -q`
- `python -m pytest tests/test_cli.py::test_cli_run_newton_native_fitting_comparison_reads_config_subsets tests/test_cli.py::test_cli_run_newton_native_fitting_comparison_emits_json_without_config tests/test_cli.py::test_cli_run_cpd_like_reports_clean_error_for_bad_subset -q`
- `python -m pytest tests/test_cpd_like_config.py::test_newton_native_fitting_comparison_config_includes_bed_and_franka_scope -q`
- `python -m pytest tests/test_cpd_like_synthetic.py tests/test_cpd_like_package.py tests/test_cpd_like_objective.py tests/test_newton_shapes.py -q`
- `python -m pytest tests/test_cli.py tests/test_cpd_like_config.py -q`
- `python -m primitive_collision_compiler.cli --config configs/experiments/newton_native_fitting_comparison.yaml --run-newton-native-fitting-comparison`
- `python -m pytest -q`
- `python scripts/validate_docs.py`
- `git diff --check`

## Result Summary

The config-driven command reported:

- `stage`: `cpd_like_newton_native_fitting_comparison`
- `status`: `smoke_passed`
- `legacy_primitive_subset`: `box`, `sphere`, `capsule`
- `native_primitive_subset`: `box`, `sphere`, `capsule`, `cylinder`, `cone`, `ellipsoid`

Synthetic case outcomes:

- `cylindrical_rod`: legacy selected `capsule`; native selected `cylinder`; mapping status
  `mapped`.
- `tapered_cone`: legacy selected `capsule`; native selected `cone`; mapping status `mapped`.
- `ellipsoid_blob`: legacy selected `box`; native selected `ellipsoid`; mapping status `mapped`.

The report status is synthetic-only. It also includes `real_usd_scope.status:
scope_declared_not_run` for `bed_dev_smoke` and `franka_import_smoke`.

## Config/Command Note

The registry command uses `configs/experiments/newton_native_fitting_comparison.yaml`. The config
owns the legacy/native primitive subsets, claim boundary, evidence level, and bed/Franka next-scope
roles. The command still uses in-memory synthetic fixtures for the completed `smoke_passed`
comparison; real USD execution remains the next action.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_like/primitives.py`
- `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- `src/primitive_collision_compiler/cli.py`
- `configs/experiments/newton_native_fitting_comparison.yaml`
- `docs/reference/newton-native-fitting-comparison.md`
- `assets/manifests/cpd_like_smoke_assets.yaml`

## Claim Impact

Supported narrow claim:

```text
On three deterministic synthetic meshes, the opt-in six-kind native subset can select cylinder,
cone, and ellipsoid proposals and map the resulting one-primitive packages through Newton shape
mapping.
```

Unsupported claims remain unsupported:

- collision-quality improvement;
- benchmark superiority;
- paper-faithful CPD reproduction;
- broad asset evidence;
- whole-robot collider quality;
- completed bed/Franka old/new native-fitting comparison.

The `real_usd_scope` section is scope declaration only. It records that `bed_dev_smoke` and
`franka_import_smoke` are next in scope, not that they have passed this comparison.

## Next Action

Run old/new native-fitting objective reports on capped bed and capped Franka USD meshes, then use
Newton contact canary before broader drop/settle or sphere-rain task smokes.
