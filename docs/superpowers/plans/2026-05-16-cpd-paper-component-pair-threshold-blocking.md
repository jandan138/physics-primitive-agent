# CPD Paper Component-Pair Threshold Blocking Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a deterministic offline component-pair threshold-blocking audit to
`cpd_paper_offline_report`.

**Architecture:** Extend the existing CPD paper priority-queue trace helper with an opt-in finite
component-pair threshold. The threshold only applies to component-pair candidates in the new toy
fixture and records a blocked event without changing packages or calling Newton.

**Tech Stack:** Python, pytest, Markdown docs, existing CPD paper offline report helpers.

---

### Task 1: RED Tests

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] Add assertions that `component_pair_threshold_blocking_missing` is no longer in
  `failure_labels`, while `polygon_and_quad_face_policy_missing` and
  `postprocess_enclosed_primitive_culling_missing` remain.
- [ ] Assert `next_required_gate == "paper_cpd_postprocess_audit"`.
- [ ] Assert `component_pair_threshold_blocking_audit` is present in
  `paper_faithfulness.implemented_fixture_scope`.
- [ ] Assert report cases include `paper_component_pair_threshold_blocked`.
- [ ] Preserve the existing `paper_disconnected_components` assertions:
  - `threshold_policy == "disabled"`;
  - `blocked_merge_count == 0`;
  - one accepted `component_pair` event.
- [ ] Assert the new `paper_component_pair_threshold_blocked` trace records:
  - `trace_scope == "component_pair_priority_queue_trace_fixture"`;
  - `target_primitive_count == 1`;
  - `excess_volume_threshold == 0.0`;
  - `threshold_policy == "component_pair_paper_base_cost_lte_threshold"`;
  - `initial_active_groups == [[0], [1]]`;
  - `initial_edge_count == 0`;
  - `component_pair_edge_insertion_triggered is True`;
  - `component_pair_candidate_count == 1`;
  - `accepted_merge_count == 0`;
  - `blocked_merge_count == 1`;
  - `skipped_component_pair_count == 0`;
  - `component_pair_attempted_pair_count == 1`;
  - `stale_entry_skipped_count == 0`;
  - `stop_reason == "all_remaining_edges_blocked_by_threshold"`;
  - `final_active_groups == [[0], [1]]`;
  - no package, Newton, real USD, or benchmark trigger.
- [ ] Assert the blocked component-pair event has:
  - `event_kind == "blocked_by_threshold"`;
  - `edge_source == "component_pair"`;
  - `source_faces_left == [0]`;
  - `source_faces_right == [1]`;
  - `source_faces_merged == [0, 1]`;
  - `paper_base_cost > 0.0`;
  - `paper_base_cost` is finite;
  - `weighted_priority_cost` is finite;
  - `queue_key == [weighted_priority_cost, paper_base_cost, [0], [1], insertion_order]`;
  - `accepted is False`;
  - `blocked is True`;
  - `blocked_reason == "component_pair_threshold_exceeded"`;
  - `threshold_value == 0.0`;
  - `threshold_metric == "paper_base_cost"`;
  - `stale_entry is False`;
  - `active_primitive_count_before == 2`;
  - `active_primitive_count_after == 2`;
  - `updated_neighbor_insertion_count == 0`;
  - no `resulting_source_faces`.
- [ ] Update the CLI JSON test expected case list to include
  `paper_component_pair_threshold_blocked`.
- [ ] Run:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  and confirm it fails for the missing threshold-blocking behavior.

### Task 2: Threshold Blocking Implementation

**Files:**

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] Extend `_PaperToyCase` with `component_pair_excess_volume_threshold: float | None`.
- [ ] Reuse `_disconnected_components_mesh()` for `paper_component_pair_threshold_blocked`.
- [ ] Add `paper_component_pair_threshold_blocked` with face groups `{0}`, `{1}`, target count `1`,
  component-pair insertion enabled, and threshold `0.0`.
- [ ] Extend `_priority_queue_trace_payload()` with `component_pair_excess_volume_threshold`.
- [ ] Track attempted component-pair pairs by sorted source-face tuples so blocked pairs are not
  reinserted.
- [ ] Insert only unattempted component-pair candidates when the queue is empty.
- [ ] Emit threshold fields:
  - disabled cases keep `excess_volume_threshold: "default_inf"` and `threshold_policy:
    "disabled"`;
  - threshold case records `excess_volume_threshold: 0.0` and `threshold_policy:
    "component_pair_paper_base_cost_lte_threshold"`.
- [ ] Before accepting a live component-pair candidate, compare `paper_base_cost` against the finite
  threshold.
- [ ] If `paper_base_cost` exceeds threshold, append a `_queue_event_payload()` event with
  `accepted=False`, `blocked=True`, `event_kind="blocked_by_threshold"`, and threshold metadata.
- [ ] Do not mutate `active_groups` for the blocked event.
- [ ] Increment `blocked_merge_count`.
- [ ] Increment `component_pair_attempted_pair_count` when a live component-pair candidate is
  attempted.
- [ ] Emit `skipped_component_pair_count: 0` for this all-pairs fixture and preserve the field on
  disabled/accepted traces.
- [ ] Stop with `all_remaining_edges_blocked_by_threshold` when the queue is exhausted after one or
  more threshold blocks, no unattempted component-pair pairs remain, and the target is not reached.
- [ ] Remove `component_pair_threshold_blocking` from `missing_before_paper_faithful`.
- [ ] Set `next_required_gate` to `paper_cpd_postprocess_audit`.
- [ ] Add `component_pair_threshold_blocking_audit` to implemented fixture scope.
- [ ] Run the RED test and confirm it passes.

### Task 3: Docs, Registry, And Record

**Files:**

- Modify: `docs/index.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/records/README.md`
- Modify: `experiments/registry.yaml`
- Create: `docs/records/2026-05-16-cpd-paper-component-pair-threshold-blocking.md`

- [ ] Update current paper-lane wording to say one toy component-pair threshold block is recorded.
- [ ] Keep `status: partial` and `paper_faithful_offline_supported: false`.
- [ ] Make `paper_cpd_postprocess_audit` the next gate.
- [ ] Keep package generation, Newton, real USD, benchmark, and collision-quality claims out of
  scope.
- [ ] Add dated verification and multi-agent review notes.

### Task 4: Verification And Review

- [ ] Run focused pytest for CPD paper offline and CLI report tests.
- [ ] Run CLI smoke:
  `python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report`.
- [ ] Run `python -m pytest -q`.
- [ ] Run `python scripts/validate_docs.py`.
- [ ] Run `python scripts/validate_site_claims.py`.
- [ ] Run `git diff --check`.
- [ ] Request multi-agent review for threshold-blocking algorithm, docs/claim boundaries, and report
  schema.
- [ ] Fix Critical/Important review findings before commit.

### Task 5: Commit

- [ ] Commit with message `feat: audit CPD paper component-pair threshold blocking`.
- [ ] Push `main`.
- [ ] Confirm `git status --short` is clean.
