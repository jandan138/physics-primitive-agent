# CPD Paper Component-Pair Edge Insertion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a deterministic offline component-pair edge insertion audit to
`cpd_paper_offline_report`.

**Architecture:** Reuse the existing CPD paper priority-queue trace helper and add an opt-in
component-pair insertion path that activates only when topology candidates cannot reach the target
primitive count. Keep this command-only, fixture-scoped, and claim-bounded.

**Tech Stack:** Python, pytest, Markdown docs, existing CPD paper offline report helpers.

---

### Task 1: RED Tests

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] Add assertions that `component_pair_edge_insertion_missing` is no longer in
  `failure_labels`, while `component_pair_threshold_blocking_missing`,
  `polygon_and_quad_face_policy_missing`, and `postprocess_enclosed_primitive_culling_missing`
  remain.
- [ ] Assert `next_required_gate == "paper_component_pair_threshold_blocking_audit"`.
- [ ] Assert `component_pair_edge_insertion_audit_threshold_disabled` is present in
  `paper_faithfulness.implemented_fixture_scope`.
- [ ] Assert report cases include `paper_disconnected_components`.
- [ ] Assert the existing `paper_three_face_chain` trace remains topology-only:
  - `component_pair_edge_policy == "disabled"`;
  - `component_pair_edge_insertion_triggered is False`;
  - `component_pair_candidate_count == 0`;
  - `component_pair_candidate_cap == "disabled"`;
  - all event `edge_source` values stay `topology`.
- [ ] Assert the new `paper_disconnected_components` trace records:
  - `trace_scope == "component_pair_priority_queue_trace_fixture"`;
  - `priority_queue_policy == "paper_greedy_min_weighted_priority_cost"`;
  - `target_primitive_count == 1`;
  - `initial_active_groups == [[0], [1]]`;
  - `initial_edge_count == 0`;
  - `component_pair_edge_policy == "insert_when_topology_queue_exhausted_before_target"`;
  - `topology_queue_exhausted_before_component_pair_insertion is True`;
  - `component_pair_edge_insertion_triggered is True`;
  - `component_pair_candidate_count == 1`;
  - `component_pair_candidate_cap == "all_pairs_for_fixture"`;
  - `accepted_merge_count == 1`;
  - `blocked_merge_count == 0`;
  - `stop_reason == "target_count_reached"`;
  - `final_active_groups == [[0, 1]]`;
  - no package, Newton, real USD, or benchmark trigger.
- [ ] Assert the component-pair event sequence is exactly one accepted merge with:
  - `event_kind == "accepted_merge"`;
  - `edge_source == "component_pair"`;
  - `source_faces_left == [0]`;
  - `source_faces_right == [1]`;
  - `source_faces_merged == [0, 1]`;
  - `paper_base_cost` and `weighted_priority_cost` are finite numbers;
  - `queue_key == [weighted_priority_cost, paper_base_cost, [0], [1], insertion_order]`;
  - `left_primitive`, `right_primitive`, and `merged_primitive` are present;
  - `accepted is True`;
  - `blocked is False`;
  - `stale_entry is False`;
  - `active_primitive_count_before == 2`;
  - `active_primitive_count_after == 1`;
  - `updated_neighbor_insertion_count == 0`;
  - `resulting_source_faces == [0, 1]`.
- [ ] Update the CLI JSON test expected case list to include `paper_disconnected_components`.
- [ ] Run:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  and confirm it fails for the missing component-pair behavior.

### Task 2: Component-Pair Trace Implementation

**Files:**

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] Extend `_PaperToyCase` with a boolean `component_pair_edge_insertion`.
- [ ] Add `_disconnected_components_mesh()` with two separated triangles.
- [ ] Add `paper_disconnected_components` with face groups `{0}`, `{1}`, target count `1`, and
  component-pair insertion enabled.
- [ ] Extend `_priority_queue_trace_payload()` with an `allow_component_pair_edges` argument.
- [ ] Replace the current `while len(active_groups) > target_primitive_count and queue` loop with a
  loop that can insert component-pair candidates after topology queue exhaustion before returning
  `queue_exhausted_before_target_count`.
- [ ] Add `_component_pair_group_pairs(groups)` that returns deterministic all-pairs over active
  groups using `_ordered_group_pair`.
- [ ] Extend `_queue_candidate_payload()` with an `edge_source` argument defaulting to `topology`.
- [ ] When the queue is empty but active group count is above target and component-pair insertion is
  enabled, insert all deterministic component-pair candidates with `edge_source: component_pair`.
- [ ] Record component-pair metadata fields on every queue trace:
  - `component_pair_edge_policy`;
  - `component_pair_edge_insertion_triggered`;
  - `topology_queue_exhausted_before_component_pair_insertion`;
  - `component_pair_candidate_count`, defined as the cumulative number of component-pair candidates
    inserted across the trace;
  - `component_pair_candidate_cap`.
- [ ] Keep threshold fields disabled and `blocked_merge_count: 0`.
- [ ] Remove `component_pair_edge_insertion` from `missing_before_paper_faithful`.
- [ ] Add `component_pair_threshold_blocking` to `missing_before_paper_faithful`.
- [ ] Set `next_required_gate` to `paper_component_pair_threshold_blocking_audit`.
- [ ] Add `component_pair_edge_insertion_audit_threshold_disabled` to implemented fixture scope.
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
- Create: `docs/records/2026-05-16-cpd-paper-component-pair-edge-insertion.md`

- [ ] Update current paper-lane wording to say component-pair insertion exists for one disconnected
  toy fixture only.
- [ ] Keep `status: partial` and `paper_faithful_offline_supported: false`.
- [ ] Make component-pair threshold blocking the next gate.
- [ ] Update the `paper_disconnected_components` fixture description in the lane spec so it says
  active groups are above target and topology cannot reduce them.
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
- [ ] Request multi-agent review for component-pair algorithm, docs/claim boundaries, and report
  schema.
- [ ] Fix Critical/Important review findings before commit.

### Task 5: Commit

- [ ] Commit with message `feat: audit CPD paper component-pair insertion`.
- [ ] Push `main`.
- [ ] Confirm `git status --short` is clean.
