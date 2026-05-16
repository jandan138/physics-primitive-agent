# Controlled Merge-Search Package Probe Design

## Goal

Add a synthetic package-path bridge for the existing cost-guided merge-search smoke.

The current `cost_guided_pair_choice` fixture already shows that opt-in
`merge_search_policy: cost_guided_pairwise` chooses a virtual component merge while the default
`topology_then_virtual` path chooses a topology merge. This slice carries that existing synthetic
merge/search difference into `CollisionPackage` generation and Newton shape-mapping accounting.

## Scope

In scope:

- command-only synthetic report;
- one fixture: `cost_guided_pair_choice`;
- default lane: `topology_then_virtual`;
- opt-in lane: `cost_guided_pairwise`;
- package summaries, primitive source-face groupings, merge traces, surrogate merge-excess delta,
  and Newton shape-mapping coverage.

Out of scope:

- new merge algorithm;
- default pipeline change;
- Newton contact, drop/settle, or sphere-rain task execution;
- real USD, bed, Franka, whole-robot, or benchmark runs.

## Report Shape

The report stage is:

```text
cpd_like_controlled_merge_search_package_probe
```

It records:

- `synthetic_only: true`;
- `command_only: true`;
- `real_usd_scope: not_run_synthetic_only`;
- default and opt-in merge-search policies;
- default and opt-in package primitive source faces;
- `package_pair_changed`;
- `merge_search_behavior_changed`;
- default and opt-in Newton shape-mapping status counts;
- `newton_task_comparison_triggered: false`.

## Claim Boundaries

Allowed wording:

- "single-fixture controlled merge-search package-path probe";
- "synthetic package-path and Newton shape-mapping accounting";
- "existing cost-guided merge-search smoke carried into CollisionPackage generation";
- "surrogate merge-excess delta on one deterministic fixture."

Forbidden wording:

- "new CPD optimizer";
- "default merge policy changed";
- "Newton diagnostic/task evidence";
- "simulation-checked package";
- "real-USD package improvement";
- "collision-quality improvement";
- "benchmark result";
- "CPD paper reproduced."

## Verification

Required checks:

1. RED report-builder test for the changed package source-face grouping and mapping summary.
2. RED strict-JSON test.
3. RED CLI smoke and nonzero partial tests.
4. GREEN implementation with no new merge algorithm.
5. Documentation, record, registry, claim-boundary, and explainer updates.
6. Focused tests, full tests, docs validation, site claim validation, and `git diff --check`.
7. Multi-agent implementation and claim-boundary review.
