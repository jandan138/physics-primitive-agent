# Cost-Guided Lookahead Merge Design

## Goal

Add one narrow, opt-in merge/search algorithmic slice after the controlled merge-search Newton
probe: a synthetic-only two-step lookahead policy that can choose a first merge by projected
two-step cost instead of immediate merge-excess only.

This is a direct merge/search change for the Newton CPD workbench. It is not a CPD paper optimizer,
not a default pipeline change, not real-USD evidence, and not collision-quality evidence.

## Context

The current `cost_guided_pairwise` policy is already a greedy best-first policy. At each merge
loop it compares the best topology merge and the best virtual component merge by normalized
merge-excess, then accepts the lower-cost candidate.

That is useful, but it remains locally greedy. A locally cheapest first merge can leave a much
more expensive second merge. The next algorithmic slice should therefore test a tiny search idea:
when more than one merge remains before the primitive budget is reached, choose the first merge by
the cost of that merge plus the best immediate follow-up merge.

## Rejected Alternatives

### Rename Current Best-First Frontier

Rejected because the current `cost_guided_pairwise` implementation already compares the best
topology and best virtual candidates. A new `frontier` name without a different decision rule
would add ceremony rather than algorithmic progress.

### Beam Search

Rejected for this slice because a beam-search policy introduces beam width, configurable depth,
and broader optimizer language before the workbench has a controlled failure fixture. A fixed
two-step lookahead is smaller, easier to audit, and enough to expose the next search question.

### Diagnostics-Only Trace Expansion

Rejected as the next slice because the trace and package/Newton probes already show the current
merge/search path. The next gap is an actual opt-in decision change, not more accounting around
the same decision.

## Proposed Policy

Add a new merge-search policy constant:

```python
MERGE_SEARCH_TWO_STEP_LOOKAHEAD = "two_step_lookahead"
```

The policy is valid only with:

```python
component_merge="virtual_pairwise"
```

The policy is also mechanically bounded to tiny meshes:

```text
mesh.face_count <= 6
```

That guard keeps this slice a synthetic diagnostic smoke and prevents accidental real-USD or
large-mesh use before a separate design exists.

At each loop step:

1. Enumerate legal topology and virtual pair candidates under the existing rules.
2. For each first-step candidate, simulate accepting it on copied merge state.
3. If another merge is still needed to reach `max_primitives`, find the best legal follow-up
   candidate from the copied state.
4. Score the first-step candidate by:

```text
candidate.normalized_excess_volume + follow_up.normalized_excess_volume
```

5. If no follow-up is needed, score only the first-step candidate.
6. Choose the candidate with the lowest projected cost.

Tie-breaks stay deterministic:

```text
projected cost
immediate normalized merge-excess
topology before virtual
left cluster id
right cluster id
```

The virtual threshold gate remains conservative. If the chosen first-step candidate is virtual and
exceeds `excess_volume_threshold_fraction`, record `component_merge_threshold_blocked` and stop.
Do not silently fall back to a different candidate in the same step.

## Synthetic Fixture

Add a deterministic `lookahead_merge_trap` fixture with four disconnected triangle components and
`max_primitives=2`.

Expected behavior:

```text
cost_guided_pairwise:
  first merge: [0, 2]
  final grouping: [[0, 2, 3], [1]]
  projected two-step normalized excess: higher

two_step_lookahead:
  first merge: [0, 1] or [2, 3] by deterministic tie-break
  final grouping: [[0, 1], [2, 3]]
  projected two-step normalized excess: lower
```

The fixture exists to record that lookahead can change a merge/search decision on one inspectable
toy case. It does not show better collider quality.

## Report

Add a command-only synthetic report:

```text
cpd_like_cost_guided_lookahead_merge_report
```

It should compare:

- greedy lane: `cost_guided_pairwise`;
- lookahead lane: `two_step_lookahead`.

The report should include:

- source-face grouping for both lanes;
- accepted normalized excess sums;
- first-step trace rows for both lanes;
- projected two-step normalized excess for the chosen first merge;
- `lookahead_decision_changed`;
- `projected_cost_improved`;
- `tiny_mesh_guard_applied`;
- `default_pipeline_changed: false`;
- `newton_task_comparison_triggered: false`;
- `real_usd_rerun_triggered: false`;
- `collision_quality_claim_supported: false`;
- `merge_policy_superiority_claim_supported: false`.

This report is offline merge/search accounting only. A later package probe and Newton task probe
may be added only after this report is complete and reviewed.

## CLI

Add a no-config command:

```text
--run-cpd-like-cost-guided-lookahead-merge-report
```

It should emit strict JSON and return exit code 0 only when the synthetic report status is
`smoke_passed`.

## Claim Boundary

Allowed wording:

- "synthetic cost-guided lookahead merge/search smoke";
- "synthetic two-step merge-search lookahead smoke";
- "bounded diagnostic merge/search heuristic";
- "two-step lookahead over deterministic toy merge states";
- "offline merge/search decision accounting";
- "opt-in synthetic merge/search policy."

Forbidden wording:

- "CPD optimizer implemented";
- "paper-faithful search";
- "merge-policy superiority";
- "better collision geometry";
- "collision-quality validation";
- "benchmark result";
- "real-USD improvement";
- "bed/Franka evidence";
- "Newton task evidence";
- "CPD paper reproduction."

## Verification Strategy

Use TDD:

1. RED decomposition test that `two_step_lookahead` is accepted only with
   `virtual_pairwise`.
2. RED decomposition test that the `lookahead_merge_trap` fixture produces a different first merge
   and lower projected two-step cost than greedy `cost_guided_pairwise`.
3. RED test that the virtual threshold gate can still block a chosen virtual first-step candidate.
4. RED synthetic-report test for strict JSON fields and claim boundaries.
5. RED CLI test for strict JSON emission and non-finite JSON rejection.
6. Minimal implementation in `decompose.py`, `synthetic.py`, and `cli.py`.
7. Dated record, registry, index, CPD story, loop explainer, face-merge explainer, evidence, and
   claim-boundary updates.
8. Multi-agent implementation and docs review.
9. Focused tests, CLI smoke, full `python -m pytest -q`, docs validation, site claims, and
   `git diff --check`.

## Self-Review

No placeholders remain. The design is one focused merge/search algorithmic slice. It preserves
default behavior, keeps real USD out of scope, and does not add package, Newton task,
collision-quality, benchmark, or CPD reproduction claims.
