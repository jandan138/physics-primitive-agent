# Controlled Merge-Search Newton Probe Design

## Goal

Add a synthetic Newton task-smoke bridge for the existing controlled merge-search package-path
probe.

The previous slice showed that the existing `cost_guided_pair_choice` fixture can produce different
`CollisionPackage` groupings under default `topology_then_virtual` and opt-in
`cost_guided_pairwise` merge-search lanes, and that both packages map to Newton shapes. This slice
runs named Newton task smokes over that changed synthetic package pair.

## Scope

In scope:

- one synthetic fixture: `cost_guided_pair_choice`;
- default lane: `topology_then_virtual`;
- opt-in lane: `cost_guided_pairwise`;
- `newton_contact_smoke` first;
- `newton_drop_settle` and `newton_sphere_rain` only when contact passes;
- explicit config-scoped CLI execution.

Out of scope:

- real USD, bed, Franka, whole-robot, or benchmark runs;
- new merge algorithm;
- default merge-policy/package behavior change;
- collision-quality validation;
- merge-policy superiority claims;
- CPD paper reproduction.

## Report Shape

The report stage is:

```text
cpd_like_controlled_merge_search_newton_probe
```

It records:

- `real_usd_scope: not_run_synthetic_only`;
- default and opt-in package summaries;
- package-pair changed status;
- contact status for each package lane;
- task status for each package lane;
- blocked task payloads when contact does not pass;
- top-level status `smoke_passed` only when package pair changed and all contact/task reports pass.

## CLI And Config

CLI:

```text
--run-cpd-like-controlled-merge-search-newton-probe
```

Config requirements:

- `asset.path: synthetic://cost_guided_pair_choice`;
- `task.primary: synthetic_controlled_merge_search_newton_probe`;
- `compile.verify` includes `cpd_like_controlled_merge_search_newton_probe`;
- `newton.source_dir` is present.

## Claim Boundaries

Allowed wording:

- "synthetic controlled merge-search Newton task-smoke probe";
- "contact-gated Newton smoke over one changed synthetic package pair";
- "named Newton task status under recorded settings."

Forbidden wording:

- "real-USD result";
- "bed/Franka result";
- "merge-search improvement";
- "collision-quality validation";
- "benchmark result";
- "CPD reproduced";
- "failure modes found or ruled out."

## Verification

Required checks:

1. RED report-builder test for contact-gated task execution.
2. RED contact-failure blocks task execution.
3. RED unchanged package pair cannot report top-level `smoke_passed`.
4. RED CLI config-scope tests and JSON output tests.
5. GREEN implementation with no real-USD execution.
6. Focused tests, clean Newton CLI smoke, full tests, docs validation, site claim validation, and
   `git diff --check`.
7. Multi-agent implementation and claim-boundary review.
