# 2026-05-16 Cylinder Scoring Policy Guardrail

## Date

2026-05-16

## Status

Complete

## Changes

- Extended `build_cpd_like_cylinder_near_miss_scoring_policy_ablation_report()` from one synthetic
  case to two synthetic cases.
- Added `boxy_cuboid_guardrail`, a clearly boxy cuboid negative-control fixture.
- The existing CLI gate now emits both cases:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cylinder-near-miss-scoring-policy-ablation`.
- The fixed `0.88` cylinder multiplier is still applied only inside copied report rows.
- Default primitive fitting, `fit_best_primitive`, support-aware ranking, merge/search, real-USD
  packages, and Newton task execution are unchanged.

## Result

The report returns `smoke_passed` with:

- `cylinder_near_miss_cluster`: default `box`, report-only counterfactual `cylinder`,
  counterfactual selection changed `true`;
- `boxy_cuboid_guardrail`: default `box`, report-only counterfactual `box`,
  counterfactual selection changed `false`;
- report-only cylinder multiplier: `0.88`.

This is a selectivity guardrail for a synthetic report-only multiplier. It does not show the
multiplier is safe, calibrated, or ready for real assets.

## Verification

- RED:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_policy_ablation_reports_counterfactual_flip`
  failed because the existing report only contained `cylinder_near_miss_cluster`.
- GREEN:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_policy_ablation_reports_counterfactual_flip tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_policy_ablation_report_is_strict_json_serializable tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_policy_ablation_derives_default_behavior_gate`
  passed.
- CLI targeted check:
  `PYTHONPATH=src python -m pytest -q tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_policy_ablation_emits_json tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_policy_ablation_returns_nonzero_for_partial`
  passed.
- CLI smoke:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cylinder-near-miss-scoring-policy-ablation`
  returned `smoke_passed` with both expected cases.
- Full verification after review-scope cleanup:
  `python -m pytest -q` passed with 301 tests,
  `python scripts/validate_docs.py` passed,
  `python scripts/validate_site_claims.py` passed, and
  `git diff --check` passed.
- Multi-agent review:
  implementation review found no Critical issues and one Important test-scope leak; the leak was
  fixed by restoring near-miss workbench and fit-ablation tests to single-case expectations. Docs
  review found no Critical or Important issues after the guardrail wording stayed synthetic,
  offline, and report-only.
- Second-pass multi-agent review:
  implementation and docs re-reviews found no Critical or Important issues after the test-scope and
  stale-wording fixes.

## Claim Impact

This record supports only synthetic report-only guardrail accounting for the existing
counterfactual scoring-policy ablation report. It records that the near-miss fixture flips while a
clearly boxy cuboid guardrail remains `box` under the same report-only multiplier.

It does not support objective improvement, scoring calibration, default selection change, cylinder
quality, box failure, real-USD package improvement, Newton task improvement, benchmark evidence,
collision-quality validation, or CPD paper reproduction.

## Next Action

Use this guardrail result to decide whether a broader opt-in scoring experiment should include
more synthetic negative controls or whether the next slice should move to merge/search diagnostics.
Do not rerun bed/Franka Newton tasks until a default package actually changes and still maps fully.
