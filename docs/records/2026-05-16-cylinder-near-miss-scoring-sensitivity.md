# 2026-05-16 Cylinder Near-Miss Scoring Sensitivity

## Date

2026-05-16

## Status

Complete

## Changes

- Added `build_cpd_like_cylinder_near_miss_scoring_sensitivity_report()` for the existing
  `cylinder_near_miss_cluster` synthetic fixture.
- Added the CLI gate:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cylinder-near-miss-scoring-sensitivity`.
- The report records the counterfactual cylinder score multiplier and cost reduction required for
  the support-admissible cylinder candidate to tie the selected box under the current
  weighted-volume surrogate.
- Default primitive fitting, primitive selection, merge/search, real-USD packages, and Newton task
  execution are unchanged.

## Result

The report returns `smoke_passed` with:

- selected primitive: `box`;
- extension primitive: `cylinder`;
- extension raw-cost rank: `2`;
- selected box weighted volume: `2.2109628599999995`;
- cylinder weighted volume: `2.4928537706235003`;
- absolute cost gap: `0.2818909106235008`;
- selected-denominator relative gap: `0.12749689998116967`;
- selected-denominator cylinder-over-box ratio: `1.1274968999811696`;
- cylinder score multiplier to tie: `0.8869203986429595`;
- cylinder cost-reduction fraction to tie: `0.11307960135704054`.

The diagnostic conclusion is `scoring_change_required_to_flip_current_surrogate`.

## Verification

- RED:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_sensitivity_reports_required_multiplier`
  failed because the new report constant/function did not exist.
- GREEN:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_sensitivity_reports_required_multiplier tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_sensitivity_report_is_strict_json_serializable`
  passed.
- RED:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_sensitivity_derives_default_behavior_gate`
  failed because the Newton gate was still hardcoded on the mismatched path.
- GREEN:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_sensitivity_reports_required_multiplier tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_sensitivity_report_is_strict_json_serializable tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_sensitivity_derives_default_behavior_gate`
  passed.
- RED:
  `PYTHONPATH=src python -m pytest -q tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_sensitivity_emits_json`
  failed because the CLI flag did not exist.
- GREEN:
  `PYTHONPATH=src python -m pytest -q tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_sensitivity_emits_json tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_sensitivity_returns_nonzero_for_partial`
  passed.
- Combined focused check:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_sensitivity_reports_required_multiplier tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_sensitivity_report_is_strict_json_serializable tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_sensitivity_derives_default_behavior_gate tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_sensitivity_emits_json tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_sensitivity_returns_nonzero_for_partial`
  passed with `5 passed`.
- Targeted synthetic/CLI check:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_sensitivity_emits_json tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_sensitivity_returns_nonzero_for_partial`
  passed with `26 passed`.
- CLI smoke:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cylinder-near-miss-scoring-sensitivity`
  returned `smoke_passed`.
- Full test suite:
  `python -m pytest -q` passed with `295 passed`.
- Documentation and hygiene checks passed:
  `python scripts/validate_docs.py`,
  `python scripts/validate_site_claims.py`,
  and `git diff --check`.
- Multi-agent implementation review reported no Critical or Important findings after the field-name
  and documentation cleanup.

## Claim Impact

This record supports only synthetic scoring-sensitivity accounting for the
`cylinder_near_miss_cluster` fixture. It quantifies a hypothetical scoring change; it does not
apply that change.

It does not support primitive-selection improvement, cylinder quality, box failure, CPD paper
reproduction, paper-faithful optimization, real-USD package improvement, Newton task improvement,
benchmark evidence, collision-quality validation, or deployment readiness.

## Next Action

Use this sensitivity result to decide whether the next controlled slice should be an opt-in
scoring-policy ablation on synthetic fixtures or a merge/search diagnostic. Do not rerun bed/Franka
Newton tasks until a default package actually changes and still maps fully.
