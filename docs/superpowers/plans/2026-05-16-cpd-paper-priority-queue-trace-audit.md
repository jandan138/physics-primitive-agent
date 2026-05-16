# CPD Paper Priority Queue Trace Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a deterministic topology-only paper priority-queue trace audit to
`cpd_paper_offline_report`.

**Architecture:** Keep the lane offline and fixture-scoped. Add one three-face chain fixture,
compute topology-adjacent queue candidates with paper cost payloads, record per-pop queue keys,
accepted merges, stale checks/skips, and updated neighbor insertions, and advance the next gate to
component-pair edge insertion while keeping the report partial.

**Tech Stack:** Python, pytest, Markdown docs, existing CPD paper offline report helpers.

---

### Task 1: RED Tests

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [x] Add assertions that `full_priority_queue_trace_missing` is no longer in `failure_labels`
  while `component_pair_edge_insertion_missing` remains.
- [x] Assert `next_required_gate == "paper_component_pair_edge_insertion_audit"`.
- [x] Assert `paper_three_face_chain` exists in the report cases.
- [x] Assert the `paper_three_face_chain` trace records:
  - `trace_scope == "topology_priority_queue_trace_fixture"`;
  - `priority_queue_policy == "paper_greedy_min_weighted_priority_cost"`;
  - `target_primitive_count == 1`;
  - `excess_volume_threshold == "default_inf"`;
  - `threshold_policy == "disabled"`;
  - `initial_edge_count == 2`;
  - two accepted merge events;
  - stale status fields on every pop event;
  - at least one eager stale-prune skip after the first accepted merge;
  - `stop_reason == "target_count_reached"`;
  - final active group `[0, 1, 2]`;
  - no Newton, real USD, package, or benchmark trigger.
- [x] Assert every pop event carries:
  - `paper_base_cost`;
  - `weighted_priority_cost`;
  - `queue_key`;
  - `source_faces_left`;
  - `source_faces_right`;
  - `edge_source`;
  - `stale_entry`;
  - `accepted`;
  - `resulting_source_faces` when accepted;
  - `active_primitive_count_before`;
  - `active_primitive_count_after`;
  - `updated_neighbor_insertion_count`.
- [x] Update the CLI JSON test expected case set to include `paper_three_face_chain`.
- [x] Run:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice -q`
  and confirm it fails for the missing priority queue trace behavior.

### Task 2: Priority Queue Trace Implementation

**Files:**

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [x] Extend `_PaperToyCase` with an optional `priority_queue_target_count`.
- [x] Add `_three_face_chain_mesh()`.
- [x] Add `paper_three_face_chain` with face groups `{0}`, `{1}`, `{2}` and target count `1`.
- [x] Replace the placeholder trace for queue-enabled cases with a deterministic trace helper.
- [x] Add helper functions for:
  - face adjacency by shared triangle edges;
  - topology-adjacent group candidate generation;
  - a refactored paper cost payload that can emit either legacy single-pop fields or queue
    candidate summaries without carrying the old `greedy_single_pop_fixture` policy into queue
    events;
  - deterministic queue sorting;
  - stale-entry skip records;
  - eager stale pruning immediately after accepted merges;
  - accepted merge records and updated edge insertion.
- [x] Remove `full_priority_queue_trace` from `missing_before_paper_faithful`.
- [x] Set `next_required_gate` to `paper_component_pair_edge_insertion_audit`.
- [x] Add `priority_queue_trace_audit_topology_only` to implemented fixture scope.
- [x] Record `excess_volume_threshold: default_inf`, `threshold_policy: disabled`, and
  `blocked_merge_count: 0` in the trace.
- [x] Run the RED test and confirm it passes.

### Task 3: Docs, Registry, And Record

**Files:**

- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/index.md`
- Modify: `docs/records/README.md`
- Modify: `experiments/registry.yaml`
- Create: `docs/records/2026-05-16-cpd-paper-priority-queue-trace-audit.md`

- [x] Update current paper-lane wording to say topology priority-queue trace exists for toy
  fixtures only.
- [x] Keep `status: partial` and `paper_faithful_offline_supported: false`.
- [x] Make component-pair edge insertion the next gate.
- [x] Update the canonical offline lane gate sequence so component-pair edge insertion is explicit
  between topology search trace and postprocessing.
- [x] Add dated verification and multi-agent review notes.

### Task 4: Verification And Review

- [x] Run focused pytest for CPD paper offline and CLI report tests.
- [x] Run CLI smoke:
  `python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report`.
- [x] Run `python -m pytest -q`.
- [x] Run `python scripts/validate_docs.py`.
- [x] Run `python scripts/validate_site_claims.py`.
- [x] Run `git diff --check`.
- [x] Request multi-agent review for queue algorithm, docs/claim boundaries, and report schema.
- [x] Fix Critical/Important review findings before commit.

### Task 5: Commit

- [ ] Commit with message `feat: audit CPD paper priority queue trace`.
- [ ] Push `main`.
- [ ] Confirm `git status --short` is clean.
