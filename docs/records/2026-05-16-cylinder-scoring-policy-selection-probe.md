# 2026-05-16 Cylinder Scoring Policy Selection Probe

## Date

2026-05-16

## Status

Complete

## Changes

- Added a strictly opt-in primitive score multiplier path for candidate selection.
- Added `cpd_like_cylinder_scoring_policy_selection_probe`, a synthetic offline report over:
  - `cylinder_near_miss_cluster`;
  - `boxy_cuboid_guardrail`.
- Added CLI smoke:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cylinder-scoring-policy-selection-probe`.

## Result

The focused RED/GREEN tests show:

- default `fit_best_primitive()` still selects `box` for the cylinder near-miss fixture;
- opt-in `primitive_score_multipliers={"cylinder": 0.88}` selects `cylinder` for the near-miss
  fixture;
- default and opt-in selection both remain `box` for the clearly boxy cuboid guardrail;
- the new report records default rank, opt-in rank, raw weighted volume, score multiplier, and
  effective score.

This is a synthetic offline opt-in primitive-choice probe. It does not change default
decomposition, real-USD package generation, or Newton task execution.

## Verification

- RED:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_opt_in_cylinder_multiplier_flips_near_miss_without_default_change tests/test_cpd_like_synthetic.py::test_opt_in_cylinder_multiplier_preserves_boxy_guardrail`
  failed because `primitive_score_multipliers` did not exist.
- RED:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_scoring_policy_selection_probe_reports_opt_in_selection tests/test_cpd_like_synthetic.py::test_cylinder_scoring_policy_selection_probe_report_is_strict_json_serializable tests/test_cli.py::test_cli_run_cpd_like_cylinder_scoring_policy_selection_probe_emits_json tests/test_cli.py::test_cli_run_cpd_like_cylinder_scoring_policy_selection_probe_returns_nonzero_for_partial`
  failed because the report builder and CLI flag did not exist.
- GREEN:
  both focused RED commands passed after implementation.
- Full verification:
  `python -m pytest -q` passed with 307 tests,
  `python scripts/validate_docs.py` passed,
  `python scripts/validate_site_claims.py` passed, and
  `git diff --check` passed.
- CLI smoke:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cylinder-scoring-policy-selection-probe`
  returned `smoke_passed` with the near-miss flip and boxy guardrail no-flip cases.
- Multi-agent review:
  implementation review found no Critical or Important issues. Docs review found Important
  wording/status consistency issues; they were fixed by marking the record and registry complete,
  standardizing "synthetic offline opt-in scoring-policy selection probe" wording, and adding the
  record to the docs index and final claim-boundary summary.

## Claim Impact

This record supports only a synthetic offline opt-in scoring-policy selection probe. It shows that
the already-diagnosed near-miss can flip through an explicit candidate-selection multiplier while
a boxy guardrail remains box under the same multiplier.

It does not support default scoring-policy change, primitive-selection improvement, cylinder
quality, scoring calibration, real-USD package improvement, Newton task improvement, benchmark
evidence, collision-quality validation, or CPD paper reproduction.

## Next Action

Move to a controlled merge/search diagnostic or an explicit opt-in package probe. Do not run a
bed/Franka Newton task comparison until a default or explicitly experimental package changes and
maps fully.
