# CPD Paper Component-Pair Threshold Blocking Audit Design

## Context

The partial `cpd_paper_offline_report` now has:

- topology-only queue search over `paper_three_face_chain`;
- threshold-disabled component-pair insertion over `paper_disconnected_components`.

The next gap is enabled threshold behavior for disconnected component pairs. The report needs to
show that a finite threshold can block a component-pair candidate, record why the target count was
not reached, and preserve the same cost/event schema without generating packages or running Newton.

## Goal

Add a deterministic fixture-scoped component-pair threshold-blocking audit to
`cpd_paper_offline_report`.

## Scope

- Add one synthetic `paper_component_pair_threshold_blocked` fixture with two disconnected triangle
  face groups and target primitive count `1`.
- Enable component-pair insertion for this fixture.
- Set a deterministic finite `excess_volume_threshold` lower than the inserted component-pair
  candidate's `paper_base_cost`.
- Record a blocked component-pair event rather than accepting the merge.
- Keep package generation, Newton, real USD, benchmark, speed, and collision-quality work out of
  scope.

## Non-Scope

- No adaptive threshold search.
- No mixed accepted-and-blocked multi-component fixture.
- No polygon/quad intake policy.
- No enclosed-primitive postprocessing.
- No package generation or Newton runtime invocation.

## Design

Extend `_PaperToyCase` with an optional `component_pair_excess_volume_threshold`.

For queue traces:

1. Existing topology-only and threshold-disabled component-pair fixtures keep
   `excess_volume_threshold: default_inf` and `threshold_policy: disabled`.
2. The threshold-blocked fixture uses:

```text
component_pair_excess_volume_threshold = 0.0
threshold_policy = component_pair_paper_base_cost_lte_threshold
threshold_metric = paper_base_cost
```

The threshold is intentionally zero and uses raw `paper_base_cost`, so raw-versus-normalized units
cannot change this fixture's decision: any positive excess is blocked.

3. Track attempted component-pair source-face pairs for the trace. Component-pair insertion may only
   enqueue unattempted pairs, so a blocked pair cannot be reinserted forever.
4. When a live component-pair candidate is popped and its `paper_base_cost` is greater than the
   threshold, the trace records a blocked event:
   - `event_kind: blocked_by_threshold`;
   - `edge_source: component_pair`;
   - `accepted: false`;
   - `blocked: true`;
   - `blocked_reason: component_pair_threshold_exceeded`;
   - `threshold_value`;
   - `threshold_metric: paper_base_cost`;
   - active primitive count before and after unchanged.
5. The blocked candidate is not reinserted. With no remaining queue entries or unattempted
   component pairs, the trace stops with:
   - `blocked_merge_count: 1`;
   - `accepted_merge_count: 0`;
   - `skipped_component_pair_count: 0`;
   - `component_pair_attempted_pair_count: 1`;
   - `final_active_groups == [[0], [1]]`;
   - `stop_reason: all_remaining_edges_blocked_by_threshold`.

The component-pair candidate count remains cumulative inserted candidates. The component-pair
candidate cap remains `all_pairs_for_fixture`.

## Report And Claim Boundary

After this slice, `component_pair_threshold_blocking_missing` should be removed from
`failure_labels`, and `next_required_gate` should advance to `paper_cpd_postprocess_audit`.

The report is still partial because polygon/quad intake and enclosed-primitive postprocessing remain
missing. The threshold-blocking audit is only evidence that one toy disconnected fixture can record
one blocked component-pair candidate under a fixed finite threshold. It also records
`skipped_component_pair_count: 0` for this all-pairs fixture; skipped pair caps remain out of scope
until a fixture with an explicit component-pair cap is added.

## Verification

- RED/GREEN tests for `paper_component_pair_threshold_blocked`.
- Preserve threshold-disabled component-pair fixture behavior.
- CLI smoke for `--run-cpd-paper-offline-report`.
- `python -m pytest -q`.
- `python scripts/validate_docs.py`.
- `python scripts/validate_site_claims.py`.
- `git diff --check`.
