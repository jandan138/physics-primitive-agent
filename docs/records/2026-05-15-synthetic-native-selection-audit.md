# 2026-05-15 Synthetic Native Selection Audit

## Date

2026-05-15

## Status

Complete

## Changes

- Added candidate weighted-volume audit tables to the synthetic Newton-native fitting comparison.
- Kept the existing selection rule unchanged: choose the lowest weighted primitive volume and
  break ties by primitive subset order.
- Added report fields for selected candidate rank, selection policy, native-vs-legacy surrogate
  margin, native-vs-next-candidate surrogate margin, and selection claim boundary.
- Added scope guard fields so the report states that the candidate audit applies to
  one-primitive full-mesh synthetic fixtures.
- Updated the experiment config to declare `synthetic_native_selection_audit` as part of the
  opt-in synthetic native fitting comparison slice.

## Verification

- `PYTHONPATH=src python -m primitive_collision_compiler.cli --config configs/experiments/newton_native_fitting_comparison.yaml --run-newton-native-fitting-comparison > reports/generated/newton_native_fitting_comparison/native_selection_audit.json`
  exited `0` and emitted report status `smoke_passed`.
- `python -m pytest tests/test_cpd_like_synthetic.py::test_newton_native_fitting_comparison_selects_native_primitives tests/test_cpd_like_synthetic.py::test_fit_primitive_candidates_preserves_subset_order_and_paper_gap_metadata tests/test_cpd_like_synthetic.py::test_fit_best_primitive_breaks_equal_cost_ties_by_subset_order -q`
  exited `0` with `3 passed`.
- `python -m pytest -q` exited `0` with `239 passed`.
- `python scripts/validate_docs.py` exited `0`.
- `git diff --check` exited `0`.

## Artifacts

- Config: `configs/experiments/newton_native_fitting_comparison.yaml`
- Report: `reports/generated/newton_native_fitting_comparison/native_selection_audit.json`
- Code: `src/primitive_collision_compiler/baselines/cpd_like/primitives.py`
- Code: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- Tests: `tests/test_cpd_like_synthetic.py`
- Tests: `tests/test_cli.py`
- Tests: `tests/test_cpd_like_config.py`

## Result Summary

- `cylindrical_rod`: native lane selected `cylinder`, ranked first by normalized weighted volume.
- `tapered_cone`: native lane selected `cone`, ranked first by normalized weighted volume.
- `ellipsoid_blob`: native lane selected `ellipsoid`, ranked first by normalized weighted volume.
- All three native lanes report `candidate_audit_scope` as `single_primitive_full_mesh_fixture`
  and `candidate_audit_matches_selection_scope` as `true`.
- All three selected native candidates mapped through Newton shape mapping in the existing
  synthetic comparison report.

## Claim Impact

- Supports deterministic synthetic native-selection audit on toy meshes.
- Supports candidate-cost explanation for why `cylinder`, `cone`, and `ellipsoid` are selected on
  the named synthetic fixtures.
- Does not support full CPD paper reproduction, paper-faithful primitive fitting/search/objective,
  real-USD asset improvement, bed/Franka native improvement, collision-quality validation,
  benchmark superiority, deployment readiness, or safety certification.
- Lower candidate cost is an internal surrogate audit score for toy selection only, not a
  collision-quality metric.

## Next Action

- Use the audit table to design the next primitive fitting or merge-search improvement, then
  re-run bed/Franka only after the synthetic fixture shows a meaningful selection improvement.
