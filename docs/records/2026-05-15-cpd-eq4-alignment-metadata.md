# 2026-05-15 CPD Eq.4 Alignment Metadata

## Date

2026-05-15

## Status

Complete.

## Changes

- Added raw Eq.4-like merge delta summary fields to CPD-like merge-cost reports:
  `accepted_eq4_cost_*` and `blocked_eq4_cost_*`.
- Kept AABB-normalized diagnostic costs as separate `accepted_normalized_excess_*` and
  `blocked_normalized_excess_*` fields.
- Added a `normalization` block that records the source mesh AABB normalizer, floor, and fields
  affected by normalization.
- Added `metrics.paper_alignment` to the CPD-like objective report. It records the paper id,
  arXiv version, local intake PDF hash, paper section, Eq.4 reference, current JSON term path,
  weight/threshold scope, and non-faithful gaps.
- Added `cost_unit_terms` so raw Eq.4-like volume deltas and AABB-normalized diagnostic deltas are
  explicitly separated in the metadata.
- Passed `paper_alignment` through synthetic policy summaries so old/new toy comparisons carry the
  same boundary metadata.
- Updated CPD story, objective-alignment, claim-boundary, evidence, index, README, and record
  documentation.

## Verification

- `python -m pytest tests/test_cpd_like_decompose.py tests/test_cpd_like_objective.py tests/test_cpd_like_synthetic.py tests/test_cli.py -q -k "eq4 or paper_alignment or cost_guided_synthetic_comparison_shows_old_new_merge_decision or objective_report_emits_json"`:
  5 passed, 70 deselected.
- `python -m pytest tests/test_cpd_like_decompose.py tests/test_cpd_like_objective.py tests/test_cpd_like_synthetic.py tests/test_cli.py -q`:
  75 passed.
- Review-fix TDD check, `python -m pytest tests/test_cpd_like_objective.py -q -k "stable_schema or maps_merge_excess"`:
  first failed on missing `cost_unit_terms` and normalized-only `current_cost_units`, then passed
  with 2 passed, 11 deselected after the unit metadata fix.
- Review-fix focused check, `python -m pytest tests/test_cpd_like_objective.py -q -k "blocked_component_merge or stable_schema or maps_merge_excess"`:
  3 passed, 10 deselected.
- `python -m pytest tests/test_cpd_like_objective.py -q`: 13 passed.
- `python scripts/validate_docs.py`: passed.
- `git diff --check`: passed.
- `python -m pytest -q`: 167 passed in 3.06s.

## Review Notes

- Code/schema review found one Important issue: `current_cost_units` was normalized-only while the
  report now also carries raw Eq.4-like fields. Fixed by using a mixed-unit label and explicit
  `cost_unit_terms`.
- The same review noted a Minor test gap for blocked raw Eq.4-like terms. Fixed by pinning blocked
  raw fields in the objective test.
- Claim-boundary review found no overclaiming. Its Minor wording suggestion was applied by changing
  "pipeline validation" to "pipeline diagnostic plumbing".
- Focused re-review found no remaining Important issue. Its Minor accepted-value and stale-spec
  notes were addressed by checking accepted raw objective values against the decomposition summary
  and updating the design note to describe mixed raw/normalized units.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_like/decompose.py`
- `src/primitive_collision_compiler/baselines/cpd_like/objective.py`
- `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- `tests/test_cpd_like_decompose.py`
- `tests/test_cpd_like_objective.py`
- `tests/test_cpd_like_synthetic.py`
- `tests/test_cli.py`
- `docs/superpowers/specs/2026-05-15-cpd-eq4-alignment-design.md`
- `docs/superpowers/plans/2026-05-15-cpd-eq4-alignment.md`

The source-intake paper PDF remains uncommitted under `docs/tmp/` per artifact policy. The local
hash used for provenance was:
`847c069dafec31e3873a6bdf9b65fa01e1058f4b34036982eaefcefe0e696f95`.

## Claim Impact

This supports only structured Eq.4 alignment metadata for current CPD-like surrogate accounting.
It does not support Eq.4 implementation, a paper-faithful objective, CPD optimizer claims,
collision-quality validation, benchmark evidence, or full CPD paper reproduction.

## Next Action

Use this metadata as the audit baseline for the next workbench slice: add expected-failure
synthetic fixtures or a focused primitive-fitting improvement, then compare old/new outputs through
the same objective report.
