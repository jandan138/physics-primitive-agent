# 2026-05-15 Synthetic Native Selection Audit Explainer Docs

## Date

2026-05-15

## Status

Complete

## Changes

- Added a field-by-field plain-language explainer for the synthetic native selection audit table.
- Linked the explainer from the Newton-native fitting comparison page and documentation indexes.
- Clarified that the audit is scoped to one-primitive whole-fixture synthetic cases.
- Documented the scope guard fields now emitted by the report.

## Verification

- `python -m pytest tests/test_cpd_like_synthetic.py::test_newton_native_fitting_comparison_selects_native_primitives tests/test_cpd_like_synthetic.py::test_fit_primitive_candidates_preserves_subset_order_and_paper_gap_metadata tests/test_cpd_like_synthetic.py::test_fit_best_primitive_breaks_equal_cost_ties_by_subset_order -q`
  exited `0` with `3 passed`.
- `python -m pytest -q` exited `0` with `239 passed`.
- `python scripts/validate_docs.py` exited `0`.
- `git diff --check` exited `0`.

## Artifacts

- `docs/reference/synthetic-native-selection-audit-explainer.md`
- `docs/reference/newton-native-fitting-comparison.md`
- `docs/index.md`
- `docs/records/README.md`

## Claim Impact

- Clarifies how to read candidate weighted-volume audit fields.
- Does not add paper-faithful objective, collision-quality, benchmark, real-USD improvement, or
  native primitive value claims.

## Next Action

- Use the now-documented and directly tested audit table to choose the next primitive-fitting or
  merge-search improvement.
