# CPD Paper Component-Pair Edge Insertion Audit Design

## Context

The partial `cpd_paper_offline_report` now has a topology-only priority-queue trace for
`paper_three_face_chain`. Tests for that named toy fixture record queue initialization,
minimum weighted-priority-cost pops, accepted merges, eager stale pruning, updated topology-neighbor
insertion, and target-count stop.

The next paper-lane gap is disconnected component handling. When topology edges cannot reduce the
active primitive count to the target, the paper-lane audit needs component-pair candidates that use
the same cost schema and trace event schema as topology candidates. This remains an offline toy
fixture audit, not package generation or Newton runtime work.

## Goal

Add a deterministic fixture-scoped component-pair edge insertion audit to
`cpd_paper_offline_report`.

## Scope

- Add one synthetic `paper_disconnected_components` fixture with two disconnected triangle face
  groups and target primitive count `1`.
- Keep topology candidates first. Insert component-pair candidates only when the topology queue is
  exhausted while active group count is still above target.
- Reuse paper base cost, weighted priority cost, queue key, accepted/blocked/stale fields,
  threshold-disabled fields, and package/Newton/real-USD/benchmark trigger boundaries.
- Keep threshold blocking disabled in this slice. Record the disabled policy explicitly, keep
  `blocked_merge_count: 0`, and keep threshold blocking as a separate next gate.
- Keep the report `status: partial` and `paper_faithful_offline_supported: false`.

## Non-Scope

- No enabled excess-volume threshold or blocked component-pair decision. This means the slice is
  component-pair insertion only, not full component-pair threshold behavior.
- No polygon/quad intake policy.
- No enclosed-primitive postprocessing.
- No package generation.
- No Newton runtime invocation.
- No real USD, bed, Franka, benchmark, speed, or collision-quality claim.

## Design

Extend `_PaperToyCase` with an opt-in component-pair policy for queue traces. The existing
`paper_three_face_chain` keeps component-pair insertion disabled so its trace remains topology-only.
The new `paper_disconnected_components` case enables component-pair insertion and uses two
disconnected triangles:

```text
face 0: triangle near x = 0
face 1: triangle near x = 3
target_primitive_count = 1
```

The trace algorithm should:

1. Initialize active groups from the case's face groups.
2. Build initial topology-adjacent candidates.
3. Process topology candidates exactly as the existing queue trace does.
4. Restructure the current `while len(active_groups) > target_primitive_count and queue` loop into
   a loop that can notice an empty queue before stopping. If the queue is empty and active group
   count is still above target, insert component-pair candidates between disconnected active groups.
5. Mark inserted candidates with `edge_source: component_pair`.
6. Record insertion metadata before processing them:
   - `component_pair_edge_policy: insert_when_topology_queue_exhausted_before_target`;
   - `component_pair_edge_insertion_triggered: true`;
   - `topology_queue_exhausted_before_component_pair_insertion: true`;
   - `component_pair_candidate_count`, defined as the total number of component-pair candidates
     inserted across the whole trace;
   - `component_pair_candidate_cap: all_pairs_for_fixture`.
7. Pop and accept the minimum component-pair candidate with the same event schema as topology
   candidates.
8. Stop when target count is reached.

For this two-component fixture, component-pair insertion is expected to happen once. Future fixtures
with more than two disconnected active groups may repeat the empty-queue insertion phase after a
merge if active group count remains above target; the candidate count remains the cumulative total
inserted across those batches.

For `paper_three_face_chain`, the same fields should show component-pair insertion did not run:

```text
component_pair_edge_policy: disabled
component_pair_edge_insertion_triggered: false
topology_queue_exhausted_before_component_pair_insertion: false
component_pair_candidate_count: 0
component_pair_candidate_cap: disabled
```

## Report And Claim Boundary

After this slice, `component_pair_edge_insertion_missing` should be replaced by the narrower
`component_pair_threshold_blocking_missing` failure label, and `next_required_gate` should advance
to `paper_component_pair_threshold_blocking_audit`.

The report is still partial because component-pair threshold blocking, polygon/quad intake, and
enclosed-primitive postprocessing remain missing. The component-pair audit is only evidence that one
toy disconnected fixture can insert and accept an offline component-pair candidate under
threshold-disabled settings.

## Verification

- RED/GREEN tests for `paper_disconnected_components`.
- Preserve the topology-only trace expectations for `paper_three_face_chain`.
- CLI smoke for `--run-cpd-paper-offline-report`.
- `python -m pytest -q`.
- `python scripts/validate_docs.py`.
- `python scripts/validate_site_claims.py`.
- `git diff --check`.
