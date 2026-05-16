# 2026-05-16 Cylinder Near-Miss Fit Ablation

## Date

2026-05-16

## Status

Complete

## Changes

- Added `build_cpd_like_cylinder_near_miss_fit_ablation_report()` for the existing
  `cylinder_near_miss_cluster` synthetic fixture.
- Added the CLI gate:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cylinder-near-miss-fit-ablation`.
- The report records current `box` and `cylinder` candidate costs plus a pairwise radial lower
  bound for any containment-preserving circular-cylinder fit on the current cylinder axis.
- Default primitive selection, merge/search, real-USD packages, and Newton task execution are
  unchanged.

## Result

The report returns `smoke_passed` with:

- selected primitive: `box`;
- extension primitive: `cylinder`;
- current cylinder radius: `1.15`;
- pairwise radius lower bound: `1.15`;
- selected box weighted volume: `2.2109628599999995`;
- current and lower-bound cylinder weighted volume: `2.4928537706235003`;
- lower-bound relative gap after ablation: `0.12749689998116967`;
- lower-bound cylinder volume beats selected box: `false`.

The diagnostic conclusion is
`radial_center_refinement_cannot_flip_selection_under_containment`.

## Verification

- RED:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_fit_ablation_reports_radial_refinement_gate`
  failed because the new report constant/function did not exist.
- GREEN:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_fit_ablation_reports_radial_refinement_gate`
  passed.
- RED:
  `PYTHONPATH=src python -m pytest -q tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_fit_ablation_emits_json`
  failed because the CLI flag did not exist.
- GREEN:
  `PYTHONPATH=src python -m pytest -q tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_fit_ablation_emits_json`
  passed.
- Combined targeted check:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_fit_ablation_reports_radial_refinement_gate tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_fit_ablation_emits_json`
  passed.
- Code review found that `default_behavior_changed` and then `newton_task_comparison_gate` should
  be derived from observed selection instead of hardcoded. Both were fixed, with regression tests
  for the normal and mismatched paths.
- Review-fix focused check:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_fit_ablation_reports_radial_refinement_gate tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_fit_ablation_derives_default_behavior_flag tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_fit_ablation_report_is_strict_json_serializable tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_fit_ablation_emits_json tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_fit_ablation_returns_nonzero_for_partial`
  passed with `5 passed`.
- Targeted synthetic/CLI check:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_fit_ablation_emits_json tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_fit_ablation_returns_nonzero_for_partial`
  passed with `23 passed`.
- CLI smoke:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cylinder-near-miss-fit-ablation`
  returned `smoke_passed`.
- Full test suite:
  `python -m pytest -q` passed with `289 passed`.
- Documentation and hygiene checks passed:
  `python scripts/validate_docs.py`,
  `python scripts/validate_site_claims.py`,
  and `git diff --check`.
- Final code review reported no Critical or Important findings after the derived-gate fixes.

## Claim Impact

This record supports only synthetic fit-ablation accounting for the
`cylinder_near_miss_cluster` fixture. It shows that the current fixture is a containment
lower-bound cylinder loss under the current surrogate, not a missed radial-center fit.

It does not support CPD paper reproduction, paper-faithful optimization, native primitive quality,
bed/Franka improvement, real-USD package improvement, Newton task improvement, benchmark evidence,
collision-quality validation, or deployment readiness.

## Next Action

Use this result to avoid forcing a radial cylinder fitting change on this fixture. The next
controlled slice should either test a different legal primitive-fitting fixture or move to
scoring/merge-search diagnostics before any bed/Franka Newton rerun.
