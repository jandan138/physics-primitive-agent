# Cost-Guided Merge Step Trace Design

## Goal

Add an opt-in merge/search step trace for the existing cost-guided synthetic fixture.

The current cost-guided merge-search smoke records summary counts and accepted merge-excess
totals, but it does not expose the actual merge step. This slice makes the merge decision
inspectable without changing the merge algorithm.

## Scope

The trace covers deterministic CPD-like synthetic merge/search diagnostics only. It should work
for the existing `cost_guided_pair_choice` fixture and for config-driven CPD-like runs that set:

```yaml
cpd_like:
  report_merge_trace: steps
```

The default remains `summary`, so existing reports keep their compact behavior unless the trace is
explicitly requested.

## Architecture

Add a third merge-trace mode:

```text
none    -> no merge-cost summary and no merge trace
summary -> existing merge-cost summary only
steps   -> existing summary plus per-accepted-or-blocked merge steps
```

Each trace step should record:

- step index;
- decision: `accepted` or `blocked`;
- merge kind: `topology` or `virtual_component`;
- left/right/merged source faces;
- left/right/merged source component ids;
- merged primitive type;
- left/right/merged weighted volume;
- raw excess volume;
- normalized excess volume;
- blocked reason when a threshold blocks the candidate.

## Claim Boundaries

Allowed wording:

- "synthetic offline merge-step trace";
- "merge/search decision trace";
- "diagnostic accounting for one deterministic fixture";
- "no merge policy change."

Forbidden wording:

- "better decomposition";
- "collision-quality improvement";
- "paper-faithful search trace";
- "CPD optimizer implemented";
- "Newton task improvement."

## Verification

Required checks:

1. RED test that `report_merge_trace="steps"` exposes one accepted cost-guided virtual merge step
   on `cost_guided_pair_choice`.
2. RED test that threshold-blocked virtual merges produce a blocked trace step.
3. RED synthetic comparison test that the cost-guided report includes merge traces for the
   fixture.
4. RED CLI/config test that `report_merge_trace: steps` is accepted and serializes trace rows.
5. Green implementation with default `summary` behavior unchanged.
6. Docs, record, registry, claim-boundary updates.
7. Multi-agent review and full verification.
