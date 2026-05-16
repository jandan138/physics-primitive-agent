# CPD Paper Search Engine Generalization Design

## Purpose

Close `paper_generalization_batch_c_search_engine` by adding a top-level offline report payload
that summarizes the existing paper-shaped greedy search traces across deterministic synthetic
fixtures. This is a report-only generalization checkpoint. It does not add a new optimizer, build a
`CollisionPackage`, run Newton, load real USD assets, or run benchmarks.

## Current Context

`cpd_paper_offline_report` already contains toy fixture traces for:

- topology priority-queue collapse;
- weighted-priority cost ordering;
- equal-cost deterministic tie handling and stale pruning;
- component-pair insertion after topology exhaustion;
- finite threshold blocking;
- component-pair multi-candidate ordering;
- component-pair candidate-cap skipped-pair accounting.

Those traces live inside individual `cases[*].collapse_trace` payloads. The missing piece is a
stable top-level matrix that says: the search/queue/threshold mechanics are now summarized as one
offline generalization gate, while the whole paper lane remains partial.

## Selected Approach

Use the existing `_priority_queue_trace_payload()` output as evidence and build a lightweight
`paper_generalization_batch_c_search_engine` summary matrix from named cases. The matrix should
reference case ids and copy only bounded summary fields, not duplicate the entire trace.

This is preferred over adding a new search implementation because the goal of Batch C is audit
generalization, not behavior expansion. It is also preferred over jumping to real USD or Newton
because the current paper lane still needs offline postprocess and package-boundary gates.

## Report Contract

The new top-level payload must include:

```text
paper_generalization_batch_c_search_engine
```

Required fields:

- `gate_id: paper_generalization_batch_c_search_engine`
- `gate_status: implemented_offline_report_only_partial`
- `closed_gate: paper_generalization_batch_c_search_engine`
- `next_required_gate: paper_generalization_batch_d_postprocess_policy`
- `decision: remain_partial`
- `decision_reason: search_engine_generalization_complete_postprocess_policy_missing`
- `paper_faithful_offline_allowed: false`
- `source_scope: deterministic_in_memory_search_trace_probes`
- `implementation_boundary: offline_report_only_no_package_or_newton`
- `search_engine_contract`
- `search_trace_matrix`
- `coverage_summary`
- `remaining_gaps`
- false triggers for package generation, Newton runtime, real USD, and benchmarks.

The report itself must remain:

```text
status: partial
paper_faithful_offline_supported: false
next_required_gate: paper_generalization_batch_d_postprocess_policy
```

Top-level failure labels must become only:

```text
paper_generalization_batch_d_postprocess_policy_missing
paper_generalization_batch_e_package_boundary_readiness_missing
```

## Search Engine Contract

`search_engine_contract` pins the current offline search semantics:

- input contract: `TriangleMesh_plus_initial_face_groups_target_count_and_search_policy`;
- primary policy: greedy priority queue, no lookahead;
- cost fields: keep `paper_base_cost` and `weighted_priority_cost` separate;
- queue key field order:
  `[weighted_priority_cost, paper_base_cost, source_faces_left, source_faces_right, insertion_order]`;
- candidate sources: `topology` and optional `component_pair`;
- component-pair insertion policy:
  `insert_when_topology_queue_exhausted_before_target`;
- threshold metric: `paper_base_cost`;
- supported stop reasons:
  `target_count_reached`, `all_remaining_edges_blocked_by_threshold`,
  `queue_exhausted_before_target_count`;
- no package generation, Newton runtime, real USD loading, or benchmark execution.

## Matrix Rows

The Batch C payload should summarize these existing evidence cases:

| Row id | Evidence case | Purpose |
| --- | --- | --- |
| `topology_chain_target_count` | `paper_three_face_chain` | Multi-step topology queue, target-count stop, stale prune. |
| `weighted_priority_over_base_cost` | `paper_branching_cost_order` | Weighted-priority winner can differ from base-cost winner. |
| `equal_cost_queue_tie` | `paper_equal_cost_queue_tie` | Deterministic equal-cost queue ordering plus stale prune. |
| `component_pair_threshold_disabled_accept` | `paper_disconnected_components` | Component-pair insertion accepts when threshold is disabled. |
| `component_pair_zero_threshold_block` | `paper_component_pair_threshold_blocked` | Finite zero threshold blocks component-pair merge. |
| `component_pair_positive_threshold_block` | `paper_nonzero_threshold_block` | Positive finite threshold blocks component-pair merge. |
| `component_pair_multi_candidate_order` | `paper_component_pair_multi_candidate_order` | Multiple component-pair candidates ordered by queue key. |
| `component_pair_candidate_cap_skipped` | `paper_component_pair_cap_skipped` | Candidate cap and skipped-pair accounting. |

Each row should contain:

- `row_id`
- `evidence_case_id`
- `row_status`
- `trace_scope`
- `priority_queue_policy`
- `target_primitive_count`
- `initial_edge_count`
- `initial_candidate_count`
- `component_pair_candidate_count`
- `component_pair_available_pair_count`
- `component_pair_candidate_cap`
- `skipped_component_pair_count`
- `threshold_policy`
- `excess_volume_threshold`
- `threshold_metric`
- `accepted_merge_count`
- `blocked_merge_count`
- `stale_entry_skipped_count`
- `event_kinds`
- `first_accepted_queue_key`
- `stop_reason`
- `final_active_groups`
- false package/Newton/USD/benchmark triggers.

## Invariants

Tests must assert:

- Batch C payload exists and closes only `paper_generalization_batch_c_search_engine`;
- `implemented_generalization_scope` includes Batch A, Batch B, and Batch C;
- top-level `next_required_gate` advances only to Batch D;
- top-level failure labels contain only Batch D and Batch E;
- report status and paper-faithful support remain partial/false;
- all matrix rows point to existing `cases[*].collapse_trace` payloads;
- all summary counts match the referenced trace;
- candidate and event queue keys match the declared queue key field order;
- numeric cost fields are finite where present;
- accepted events include `resulting_source_faces`;
- threshold-blocked events use `threshold_metric: paper_base_cost` and do not change active count;
- component-pair rows insert component pairs only after topology queue exhaustion;
- all new payloads and rows keep package/Newton/USD/benchmark triggers false.

## Claim Boundaries

This slice supports only:

```text
offline report-only search-trace generalization matrix for deterministic synthetic fixtures
```

It does not support claims of:

- full CPD paper reproduction;
- generalized optimizer correctness;
- collision quality improvement;
- real-asset readiness;
- Newton runtime readiness;
- benchmark superiority;
- deployment readiness or safety certification.

## Documentation Updates

Update the durable plan/status docs and records so the public story is consistent:

- `README.md`
- `docs/index.md`
- `docs/deepdive/evidence-status.md`
- `docs/reference/claim-boundaries.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/records/README.md`
- `experiments/registry.yaml`
- `docs/records/2026-05-17-cpd-paper-generalization-batch-c-search-engine.md`

## Self-Review

- No placeholder sections remain.
- The design is offline-only and does not conflict with the Newton-native runtime policy.
- The selected approach follows the existing report pattern from Batches A and B.
- The next gate after this slice is Batch D, not a runtime or benchmark gate.
