# 2026-05-16 Cylinder Near-Miss Cluster Fixture

## Date

2026-05-16

## Status

Complete

## Changes

- Added a deterministic `_cylinder_near_miss_cluster_mesh()` helper for a synthetic
  support-admissible cylinder near-miss target.
- Did not change primitive selection logic relative to the current support-aware baseline.
- Added a focused primitive-ranking test where:
  - `box` remains selected;
  - `cylinder` is support-admissible;
  - `cylinder` is more expensive than `box` but within a `0.25` relative gap;
  - the result points to a future fitting or merge/search change.
- Added a dedicated `cpd_like_near_miss_fixture_workbench` report and
  `--run-cpd-like-near-miss-workbench` CLI entry for this diagnostic target.
- Kept the fixture out of `_native_fitting_cases()` because it is a diagnostic limitation target,
  not a native-extension success case.

## Verification

- `python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_cluster_exposes_box_selected_close_cylinder_loss`
  first failed with missing `_cylinder_near_miss_cluster_mesh`.
- `python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_cluster_exposes_box_selected_close_cylinder_loss`
  exited `0` with `1 passed` after adding the fixture helper.
- `python -m pytest -q tests/test_cpd_like_synthetic.py::test_near_miss_workbench_reports_cylinder_fixture tests/test_cli.py::test_cli_run_cpd_like_near_miss_workbench_emits_json`
  first failed before the near-miss workbench builder and CLI existed.
- `python -m pytest -q tests/test_cpd_like_synthetic.py::test_near_miss_workbench_reports_cylinder_fixture tests/test_cli.py::test_cli_run_cpd_like_near_miss_workbench_emits_json`
  exited `0` with `2 passed` after adding the report and CLI entry.
- `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-near-miss-workbench`
  exited `0` and reported `smoke_passed` for `cylinder_near_miss_cluster`.
- `python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_cluster_exposes_box_selected_close_cylinder_loss tests/test_cpd_like_synthetic.py::test_newton_native_fitting_comparison_selects_native_primitives`
  exited `0` with `2 passed`.
- `python -m pytest -q tests/test_cpd_like_synthetic.py tests/test_cli.py::test_cli_run_cpd_like_near_miss_workbench_emits_json`
  exited `0` with `19 passed`.
- `python -m pytest -q tests/test_cpd_like_synthetic.py` exited `0` with `17 passed`.
- `python -m pytest -q` exited `0` with `284 passed`.
- `python scripts/validate_docs.py` exited `0` with docs validation passed.
- `python scripts/validate_site_claims.py` exited `0` with site claim validation passed.
- `git diff --check` exited `0`.
- Read-only code review reported no Critical, Important, or Minor findings after scoping the
  fixture against the current support-aware baseline.
- Read-only docs/claims review first flagged one Important wording issue in the four-block spec;
  "CPD reproduction workbench" was replaced with claim-bounded diagnostic-workbench wording.
  Follow-up validation passed.

## Claim Impact

This supports only a synthetic candidate-loss fixture for a support-admissible cylinder near miss.
It does not support:

- CPD paper reproduction;
- paper-faithful primitive fitting;
- cylinder quality improvement;
- bed or Franka improvement;
- collision-quality validation;
- benchmark superiority;
- Newton task improvement.

## Next Action

Use this fixture and near-miss workbench report to decide whether the next controlled change should
improve cylinder fitting or cluster grouping.
