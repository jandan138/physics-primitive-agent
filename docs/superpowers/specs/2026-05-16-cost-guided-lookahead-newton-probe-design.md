# Cost-Guided Lookahead Newton Probe Design

## Goal

Add the next legal gate after the completed synthetic lookahead package probe: an explicitly opt-in
synthetic Newton task-smoke probe over the `lookahead_merge_trap` package pair.

The previous package probe records that greedy `cost_guided_pairwise` and opt-in
`two_step_lookahead` produce different `CollisionPackage` source-face groupings and that both
packages map to Newton shapes. This slice runs named Newton diagnostics over that changed synthetic
package pair under recorded settings.

## Scope

In scope:

- one synthetic fixture: `lookahead_merge_trap`;
- greedy lane: `cost_guided_pairwise`;
- lookahead lane: `two_step_lookahead`;
- `newton_contact_smoke` first for each lane;
- `newton_drop_settle` and `newton_sphere_rain` only when contact passes for that lane;
- explicit config-scoped CLI execution;
- dated record, registry entry, claim-boundary, evidence, CPD story, and index updates.

Out of scope:

- real assets, bed, Franka, whole-robot, or benchmark runs;
- default merge-policy or package behavior changes;
- new merge/search algorithm work;
- collision geometry quality measurement;
- merge-policy ranking;
- paper-level reproduction.

## Report Shape

The report stage is:

```text
cpd_like_cost_guided_lookahead_newton_probe
```

Top-level fields:

- `status`;
- `status_semantics`;
- `claim_boundary`;
- `contact_claim_boundary`;
- `task_claim_boundary`;
- `evidence_level`;
- `source_dir`;
- `device`;
- `real_usd_scope: not_run_synthetic_only`;
- `default_pipeline_changed: false`;
- `newton_task_comparison_triggered: true`;
- `real_usd_rerun_triggered: false`;
- `cases`.

`newton_task_comparison_triggered` is kept for consistency with existing probe schemas. In this
slice it means task-smoke payloads were run for both package lanes; it is not a policy ranking or
superiority field.

Case fields:

- `case_id: lookahead_merge_trap`;
- `greedy_merge_search_policy: cost_guided_pairwise`;
- `lookahead_merge_search_policy: two_step_lookahead`;
- `greedy_package`;
- `lookahead_package`;
- `greedy_contact`;
- `lookahead_contact`;
- `greedy_tasks`;
- `lookahead_tasks`;
- `decision`.

The top-level `status` is `smoke_passed` only when:

- the greedy and lookahead package payloads differ;
- greedy package source faces are `[[0, 2, 3], [1]]`;
- lookahead package source faces are `[[0, 1], [2, 3]]`;
- both contact canaries pass;
- both `drop_settle` tasks pass;
- both `sphere_rain` tasks pass.

If a lane contact canary does not pass, that lane's task payloads are blocked payloads and the
top-level status is the aggregate diagnostic status, not `smoke_passed`.

## CLI And Config

CLI:

```text
--run-cpd-like-cost-guided-lookahead-newton-probe
```

Config file:

```text
configs/experiments/cost_guided_lookahead_newton_probe.yaml
```

Config requirements:

- `asset.path: synthetic://lookahead_merge_trap`;
- `task.primary: synthetic_cost_guided_lookahead_newton_probe`;
- `compile.verify` includes `cpd_like_cost_guided_lookahead_newton_probe`;
- `newton.source_dir` is present.

The CLI expands environment variables in `newton.source_dir`, emits strict JSON, and returns 0 only
when the report status is `smoke_passed`.

## Claim Boundary

Allowed wording:

- "synthetic lookahead Newton task-smoke probe";
- "contact-gated Newton smoke over one changed synthetic package pair";
- "named Newton task status under recorded settings."

Forbidden wording:

- "real asset result";
- "bed or Franka result";
- "merge-search improvement";
- "collision geometry quality result";
- "benchmark result";
- "paper reproduction complete";
- "failure modes found or ruled out."

## Verification Strategy

Use TDD:

1. RED report-builder test for contact-gated task execution over the greedy and lookahead lanes.
2. RED contact-failure test that blocks drop/settle and sphere-rain execution.
3. RED unchanged package pair test that prevents top-level `smoke_passed`.
4. RED strict JSON serialization test.
5. RED config ownership test for `configs/experiments/cost_guided_lookahead_newton_probe.yaml`.
6. RED CLI config-scope tests and JSON output tests.
7. GREEN implementation using the existing lookahead package pair and shared synthetic Newton task
   payload helper.
8. Dated record, registry, evidence, claim-boundary, index, CPD story, and explainer updates.
9. Multi-agent implementation and documentation review.
10. Focused tests, clean Newton CLI smoke, full tests, docs validation, site claim validation, and
    `git diff --check`.

## Self-Review

No placeholders remain. The design is one focused task-smoke gate after a completed package/mapping
gate. It keeps real assets and bed/Franka reruns out of scope and does not claim quality,
benchmark, ranking, or paper-level reproduction.
