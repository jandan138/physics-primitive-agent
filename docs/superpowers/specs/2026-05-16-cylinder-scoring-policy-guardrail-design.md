# Cylinder Scoring Policy Guardrail Design

## Goal

Extend the synthetic, offline, report-only scoring-policy ablation report with a boxy guardrail
case for the fixed counterfactual cylinder multiplier.

## Scope

This slice does not change default primitive fitting, `fit_best_primitive`, support-aware ranking,
merge/search, real-USD packages, or Newton diagnostics. The multiplier is applied only inside the
existing scoring-policy ablation report.

## Design

The previous report-only ablation showed that a `0.88` cylinder multiplier flips the
`cylinder_near_miss_cluster` fixture. This guardrail asks whether the same report-only multiplier
also incorrectly flips a clearly boxy fixture.

The existing report will include two synthetic cases:

- `cylinder_near_miss_cluster`: expected default `box`, expected counterfactual `cylinder`;
- `boxy_cuboid_guardrail`: expected default `box`, expected counterfactual `box`.

Both cases use the same `0.88` report-only cylinder multiplier. The counterfactual score is
computed from copied report rows; production candidate fits and ranks are not mutated.

## Output

Extend `build_cpd_like_cylinder_near_miss_scoring_policy_ablation_report()` so it still emits:

- `stage: cpd_like_cylinder_near_miss_scoring_policy_ablation`;
- `claim_boundary: synthetic_cylinder_scoring_policy_ablation_not_default_or_collision_quality_validation`;
- one expected-flip near-miss case and one no-flip boxy guardrail case;
- default candidate ranking rows;
- counterfactual ranking rows with `default_rank`, `counterfactual_rank`,
  `report_only_multiplier`, and `counterfactual_score`;
- per-case decision fields saying default selection and Newton tasks are unchanged.

Use the existing CLI flag:

```bash
python -m primitive_collision_compiler.cli --run-cpd-like-cylinder-near-miss-scoring-policy-ablation
```

## Claim Boundaries

Allowed claims:

- one synthetic near-miss fixture flips under the report-only multiplier;
- one clearly boxy synthetic guardrail fixture does not flip under the same multiplier;
- default selection and generated packages are unchanged.

Forbidden claims:

- the multiplier is safe or calibrated;
- the objective has improved;
- cylinder is better than box;
- real USD packages improved;
- Newton task quality improved;
- benchmark evidence;
- CPD paper reproduction.

## Success Criteria

- The report is strict JSON serializable.
- The CLI emits strict JSON and returns zero only on `smoke_passed`.
- The report shows the near-miss case flips only in the report-only counterfactual ranking.
- The report shows the boxy guardrail case remains `box`.
- Existing near-miss, fit-ablation, scoring-sensitivity, and report-only ablation behavior remains
  unchanged.
