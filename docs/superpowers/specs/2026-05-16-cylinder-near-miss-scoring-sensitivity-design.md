# Cylinder Near-Miss Scoring Sensitivity Design

## Goal

Add a diagnostic-only report for `cylinder_near_miss_cluster` that measures how much the current
weighted-volume score would need to change for the support-admissible cylinder candidate to tie the
selected box candidate.

## Scope

This is synthetic and offline only. It does not change primitive fitting, primitive selection,
merge/search, real-USD packages, or Newton task execution.

## Design

The previous fit-ablation report showed that radial-center refinement cannot legally flip this
fixture while preserving containment. The next question is therefore scoring sensitivity:

- current selected box weighted volume;
- current support-admissible cylinder weighted volume;
- cylinder-over-box cost ratio;
- cylinder score multiplier required to tie the selected box;
- cylinder cost-reduction fraction required to tie the selected box.

The report must not apply the multiplier. It only records the size of a hypothetical scoring
change so the next slice can decide whether an opt-in scoring-policy ablation is justified.

## Output

Create `build_cpd_like_cylinder_near_miss_scoring_sensitivity_report()` with:

- `stage: cpd_like_cylinder_near_miss_scoring_sensitivity`;
- `claim_boundary: synthetic_cylinder_scoring_sensitivity_not_collision_quality_validation`;
- one case, `cylinder_near_miss_cluster`;
- current ranking rows for `box` and `cylinder`;
- a `scoring_sensitivity` block with the current costs, absolute and relative cost gap, required
  cylinder score multiplier to tie, and required cost reduction fraction to tie;
- a `decision` block that says no default selection changed and no Newton task comparison was
  triggered.

Add a CLI flag:

```bash
python -m primitive_collision_compiler.cli --run-cpd-like-cylinder-near-miss-scoring-sensitivity
```

## Claim Boundaries

Allowed claims:

- the synthetic near-miss fixture now has a scoring-sensitivity diagnostic;
- the current surrogate would need a quantified cylinder score reduction to tie box on this
  fixture;
- this is a planning diagnostic for a future opt-in scoring-policy ablation.

Forbidden claims:

- cylinder is better than box;
- the objective has been improved;
- primitive selection behavior changed;
- real USD packages changed;
- Newton task quality changed;
- CPD paper reproduction or benchmark evidence.

## Success Criteria

- The report is strict JSON serializable.
- The CLI emits strict JSON and returns zero only on `smoke_passed`.
- The report shows box still selected, cylinder support-admissible, cylinder raw rank 2, and the
  required multiplier is between `0.0` and `1.0`.
- Existing near-miss and fit-ablation behavior remains unchanged.
