# 2026-05-16 Cylinder Near-Miss Scoring Policy Ablation

## Date

2026-05-16

## Status

Complete

## Changes

- Added `build_cpd_like_cylinder_near_miss_scoring_policy_ablation_report()` for the existing
  `cylinder_near_miss_cluster` synthetic fixture. The report now also includes the
  `boxy_cuboid_guardrail` negative-control fixture.
- Added the CLI gate:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cylinder-near-miss-scoring-policy-ablation`.
- The report applies a fixed counterfactual cylinder multiplier only inside the report and compares
  default ranking with report-only counterfactual ranking.
- Default primitive fitting, `fit_best_primitive`, support-aware ranking, merge/search, real-USD
  packages, and Newton task execution are unchanged.

## Result

The report returns `smoke_passed` with:

- default selected primitive: `box`;
- report-only counterfactual selected primitive: `cylinder`;
- report-only cylinder multiplier: `0.88`;
- cylinder multiplier to tie: `0.8869203986429595`;
- selected box weighted volume: `2.2109628599999995`;
- cylinder weighted volume: `2.4928537706235003`;
- report-only cylinder counterfactual score: `2.1937113181486803`;
- fixed multiplier below tie threshold: `true`;
- default package changed: `false`.
- `boxy_cuboid_guardrail` remains `box` under the same report-only multiplier.

The diagnostic conclusion is
`report_only_counterfactual_multiplier_flips_synthetic_near_miss`.

## Verification

- RED:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_policy_ablation_reports_counterfactual_flip`
  failed because the new report constant/function did not exist.
- GREEN:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_policy_ablation_reports_counterfactual_flip tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_policy_ablation_report_is_strict_json_serializable`
  passed.
- RED:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_policy_ablation_derives_default_behavior_gate`
  failed because `default_selection_changed` was hardcoded on the mismatched path.
- GREEN:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_policy_ablation_reports_counterfactual_flip tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_policy_ablation_report_is_strict_json_serializable tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_policy_ablation_derives_default_behavior_gate`
  passed.
- RED:
  `PYTHONPATH=src python -m pytest -q tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_policy_ablation_emits_json`
  failed because the CLI flag did not exist.
- GREEN:
  `PYTHONPATH=src python -m pytest -q tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_policy_ablation_emits_json tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_policy_ablation_returns_nonzero_for_partial`
  passed.
- Combined focused check:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_policy_ablation_reports_counterfactual_flip tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_policy_ablation_report_is_strict_json_serializable tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_policy_ablation_derives_default_behavior_gate tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_policy_ablation_emits_json tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_policy_ablation_returns_nonzero_for_partial`
  passed with `5 passed`.
- Targeted synthetic/CLI check:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_policy_ablation_emits_json tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_policy_ablation_returns_nonzero_for_partial`
  passed with `29 passed`.
- CLI smoke:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cylinder-near-miss-scoring-policy-ablation`
  returned `smoke_passed`.
- Full test suite:
  `python -m pytest -q` passed with `300 passed`.
- Documentation and hygiene checks passed:
  `python scripts/validate_docs.py`,
  `python scripts/validate_site_claims.py`,
  and `git diff --check`.
- Multi-agent implementation review found one Important issue and several Minor issues. The
  Important issue was fixed by deriving `diagnostic_conclusion` from the mismatched/default-change
  path. Minor fixes clarified counterfactual ranks, verified production `fit_best_primitive()`
  still selects `box`, fixed ambiguous index wording, added safe wording, and checked the plan
  verification step.
- Final multi-agent review reported no Critical or Important findings after those fixes.

## Claim Impact

This record supports only synthetic report-only counterfactual scoring-policy ablation accounting
for the `cylinder_near_miss_cluster` fixture. It shows that a fixed hypothetical cylinder
multiplier can flip the fixture inside the report.

It does not support objective improvement, scoring calibration, default selection change, cylinder
quality, box failure, CPD paper reproduction, paper-faithful optimization, real-USD package
improvement, Newton task improvement, benchmark evidence, collision-quality validation, or
deployment readiness.

## Next Action

Use this ablation to decide whether the next controlled slice should design an actual opt-in
scoring experiment across more synthetic fixtures or move to merge/search diagnostics. Do not
rerun bed/Franka Newton tasks until a default package actually changes and still maps fully.
