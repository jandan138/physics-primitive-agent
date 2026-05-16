# CPD Paper Priority Queue Trace Audit Design

## Context

Before this slice, the partial `cpd_paper_offline_report` recorded paper-side operator fields, all
six paper primitive names as current surrogate or offline audit rows, paper base collapse cost, and
weighted priority cost. The next planned gate for this design was the paper greedy priority-queue
trace.

Before this slice, the report still had only a small `collapse_trace` placeholder for one two-face
merge. It did not yet show queue initialization, deterministic pop order, stale-entry pruning after
a merge, neighbor candidate insertion, or a final stop reason. The implemented record for this
design is `docs/records/2026-05-16-cpd-paper-priority-queue-trace-audit.md`.

## Goal

Add a topology-only, fixture-scoped offline priority-queue trace audit that demonstrates the paper
search control flow on tiny synthetic meshes without generating packages or calling Newton. This is
not the full paper search lane because disconnected component-pair insertion remains a separate
gate.

## Scope

- Synthetic toy fixtures only.
- Command-only `cpd_paper_offline_report` only.
- Topology-adjacent face groups only.
- No disconnected component-pair edge insertion.
- No package generation.
- No Newton runtime invocation.
- No real USD, bed, Franka, benchmark, speed, or collision-quality claim.

## Design

Add a new `paper_three_face_chain` fixture with three triangle face groups arranged in a topology
chain. The trace target count is `1`.

The trace should use eager stale pruning immediately after an accepted merge: remove queue entries
whose source groups are no longer active, record them as stale skip events, then push updated
topology-adjacent candidates for the merged group. This keeps priority-queue acceptance
deterministic while making stale-pruning coverage independent of cost ordering.

The trace algorithm should:

1. Initialize active groups from the case's face groups.
2. Build topology-adjacent candidate edges between active groups.
3. Compute each candidate's paper base cost and weighted priority cost using the existing
   primitive-fit audit payloads.
4. Sort queue entries deterministically by weighted priority cost, paper base cost, source faces,
   and insertion order.
5. Pop the minimum entry.
6. If either source group is no longer active when popped, record a stale-entry skip.
7. Otherwise accept the merge, remove the two old groups, and insert the merged group.
8. Eagerly prune and record stale entries that refer to removed groups.
9. Push updated topology-adjacent candidates from the merged group to remaining active groups.
10. Stop when the target primitive count is reached or the queue is exhausted.

The report should record:

- `trace_scope`;
- queue policy;
- target primitive count;
- `excess_volume_threshold: default_inf`;
- `threshold_policy: disabled`;
- initial active groups;
- initial edge count and initial candidate summaries;
- step-by-step pop events;
- for every pop: `paper_base_cost`, `weighted_priority_cost`, queue key fields, source groups,
  edge source, stale status, accepted/blocked decision, active primitive count before and after,
  resulting group when accepted, and updated neighbor insertion count;
- for every eager stale-prune event: queue key fields, source groups, edge source, stale status,
  accepted `false`, active primitive count before and after, and updated neighbor insertion count
  `0`;
- accepted merge count;
- stale-entry skipped count;
- blocked merge count, fixed at `0` for this no-threshold slice;
- final active groups;
- stop reason;
- `package_generation_triggered: false`;
- `newton_runtime_triggered: false`.

## Claim Boundary

This closes only the topology priority-queue trace audit gate for deterministic toy fixtures. The
report must remain `status: partial` with `paper_faithful_offline_supported: false`. It does not
implement disconnected component-pair insertion, polygon/quad intake, enclosed primitive culling,
real asset decomposition, package generation, Newton runtime diagnostics, benchmark evaluation, or
full CPD reproduction.

## Next Gate

After this slice, the next paper-lane gate should be component-pair edge insertion. That next gate
will add disconnected component candidate edges using the same cost and trace schema, still offline
and fixture-scoped.

## Verification

- RED/GREEN tests for `paper_three_face_chain`.
- Existing two-face trace stays compatible.
- CLI smoke for `--run-cpd-paper-offline-report`.
- `python -m pytest -q`.
- `python scripts/validate_docs.py`.
- `python scripts/validate_site_claims.py`.
- `git diff --check`.
