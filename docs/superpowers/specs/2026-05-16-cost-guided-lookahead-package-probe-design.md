# Cost-Guided Lookahead Package Probe Design

## Goal

Add the next legal gate after the synthetic two-step lookahead merge report: a command-only
synthetic package-path and Newton shape-mapping probe for the `lookahead_merge_trap` package pair.

This slice carries the already recorded offline grouping change into `CollisionPackage` generation
and Newton shape mapping. It does not run Newton contact, drop/settle, sphere-rain, real USD,
bed/Franka, benchmark, or collision-quality checks.

## Context

The completed `cpd_like_cost_guided_lookahead_merge_report` records:

```text
greedy cost_guided_pairwise grouping: [[0, 2, 3], [1]]
lookahead two_step_lookahead grouping: [[0, 1], [2, 3]]
```

That report is offline merge/search accounting only. Before any Newton task probe, the workbench
needs the same intermediate gate used by prior scoring-policy and controlled merge/search slices:

```text
decomposition pair
-> CollisionPackage pair
-> package payload comparison
-> Newton shape-mapping summary
```

## Scope

Add a new report:

```text
cpd_like_cost_guided_lookahead_package_probe
```

The report is command-only and uses the in-memory `lookahead_merge_trap` fixture. It should not
require a config because there are no external paths, no real USD assets, and no Newton runtime
task settings.

The report compares:

- greedy lane: `cost_guided_pairwise`;
- lookahead lane: `two_step_lookahead`.

## Report Fields

Top-level fields:

- `stage: cpd_like_cost_guided_lookahead_package_probe`;
- `status`;
- `claim_boundary`;
- `evidence_level`;
- `status_semantics`;
- `default_pipeline_changed: false`;
- `newton_task_comparison_triggered: false`;
- `real_usd_rerun_triggered: false`;
- `collision_quality_claim_supported: false`;
- `merge_policy_superiority_claim_supported: false`;
- `cases`.

Case fields:

- `case_id: lookahead_merge_trap`;
- `greedy_merge_search_policy: cost_guided_pairwise`;
- `lookahead_merge_search_policy: two_step_lookahead`;
- `greedy_package`;
- `lookahead_package`;
- `greedy_package_mapping`;
- `lookahead_package_mapping`;
- `package_pair_changed`;
- `lookahead_package_changed`;
- `merge_search_behavior_changed`;
- `comparison.accepted_normalized_excess_delta`;
- `comparison.projected_total_normalized_excess_delta`;
- `decision.newton_mapping_summary_recorded: true`;
- `decision.newton_task_comparison_triggered: false`;
- `decision.newton_task_comparison_gate: not_triggered_synthetic_package_probe_only`;
- `decision.recommended_next_component: lookahead_merge_search_newton_task_probe_or_real_usd_gate`;
- `decision.claim_boundary`.

`status` should be `smoke_passed` only when:

- package payloads differ;
- greedy package source faces are `[[0, 2, 3], [1]]`;
- lookahead package source faces are `[[0, 1], [2, 3]]`;
- both packages fully map to Newton shapes;
- lookahead projected two-step cost remains lower than greedy projected two-step cost.

## CLI

Add:

```text
--run-cpd-like-cost-guided-lookahead-package-probe
```

It should emit strict JSON and return 0 only for `smoke_passed`.

## Claim Boundary

Allowed wording:

- "synthetic lookahead package-path probe";
- "Newton shape-mapping accounting";
- "changed synthetic package pair";
- "package-path and mapping gate before Newton tasks."

Forbidden wording:

- "Newton task checked";
- "simulation-checked";
- "merge-policy superiority";
- "better collision quality";
- "real-USD evidence";
- "bed/Franka evidence";
- "benchmark result";
- "CPD reproduced";
- "safety validation."

## Verification Strategy

Use TDD:

1. RED synthetic report test for changed package source faces and mapping summaries.
2. RED strict JSON serialization test.
3. RED CLI JSON smoke test.
4. RED CLI non-finite JSON rejection test.
5. Minimal implementation by reusing the lookahead decomposition pair and existing
   `package_from_cpd_like_report`, `_package_collision_payload`, `_package_probe_package_summary`,
   and `_package_mapping_summary` helpers.
6. Dated record, registry, index, CPD story, loop explainer, face-merge explainer, evidence, and
   claim-boundary updates.
7. Multi-agent implementation and docs review.
8. Focused tests, CLI smoke, full `python -m pytest -q`, docs validation, site claims, and
   `git diff --check`.

## Self-Review

No placeholders remain. The design is one focused package/mapping gate. It preserves the previous
offline lookahead report boundary, keeps real USD and Newton task execution out of scope, and
prepares a later explicitly opt-in Newton task probe only if this package pair remains useful after
review.
