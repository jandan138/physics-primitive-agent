# Cylinder Near-Miss Scoring Policy Ablation Design

## Goal

Add a synthetic, offline, report-only ablation that applies a counterfactual cylinder score
multiplier to the existing `cylinder_near_miss_cluster` fixture and reports whether the fixture
would flip under that hypothetical scoring policy.

## Scope

This slice does not change default primitive fitting, `fit_best_primitive`, support-aware ranking,
merge/search, real-USD packages, or Newton diagnostics. The multiplier is applied only inside the
new report.

## Design

The scoring-sensitivity report measured that the support-admissible cylinder needs a multiplier of
about `0.8869` to tie the selected box. This ablation uses a fixed counterfactual multiplier below
that threshold:

```text
cylinder report-only multiplier = 0.88
```

The report compares:

- default candidate ranking under current weighted-volume scores;
- counterfactual candidate ranking under the report-only cylinder multiplier;
- whether the default selection changed: expected `false`;
- whether the report-only counterfactual selection changed: expected `true`;
- whether Newton task comparison was triggered: expected `false`, because no generated package was
  changed.

## Output

Create `build_cpd_like_cylinder_near_miss_scoring_policy_ablation_report()` with:

- `stage: cpd_like_cylinder_near_miss_scoring_policy_ablation`;
- `claim_boundary: synthetic_cylinder_scoring_policy_ablation_not_default_or_collision_quality_validation`;
- one case, `cylinder_near_miss_cluster`;
- default ranking rows for `box` and `cylinder`;
- counterfactual ranking rows with `report_only_multiplier` and `adjusted_weighted_volume`;
- a `counterfactual_ablation` block with the multiplier, tie threshold, default selected primitive,
  counterfactual selected primitive, and flip status;
- a `decision` block that says no default package changed and no Newton task comparison was
  triggered.

Add a CLI flag:

```bash
python -m primitive_collision_compiler.cli --run-cpd-like-cylinder-near-miss-scoring-policy-ablation
```

## Claim Boundaries

Allowed claims:

- the synthetic fixture flips under a named report-only counterfactual multiplier;
- the default selection and generated packages are unchanged;
- this is a diagnostic input for deciding whether a future scoring-policy experiment is worth
  designing.

Forbidden claims:

- the objective has improved;
- cylinder is better than box;
- a scoring policy has been calibrated;
- real USD packages improved;
- Newton task quality improved;
- benchmark evidence;
- CPD paper reproduction.

## Success Criteria

- The report is strict JSON serializable.
- The CLI emits strict JSON and returns zero only on `smoke_passed`.
- The report shows default selected `box`, counterfactual selected `cylinder`, and no default
  package change.
- Existing near-miss, fit-ablation, and scoring-sensitivity behavior remains unchanged.
