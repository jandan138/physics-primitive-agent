# CPD Paper Changed Decomposition Output Contract Design

## Purpose

Close `paper_offline_changed_decomposition_output_contract` by adding an offline/report-only
contract payload to `cpd_paper_offline_report`.

This contract turns the existing paper-lane audit rows into a durable, reviewable offline
decomposition-output shape for a future package adapter. It is not a `CollisionPackage`, does not
import or instantiate package/runtime types, does not map primitives to Newton, does not load real
USD assets, and does not run benchmarks.

## Current Context

The current report closes:

- source-policy generalization;
- primitive-fit engine generalization;
- search-engine generalization;
- postprocess-policy generalization;
- package-boundary readiness.

Batch E now says the next missing item is a durable changed-decomposition output contract. Without
that contract, a future adapter cannot know which offline primitive rows, face groups, source
faces, postprocess decisions, and unsupported boundaries are reviewable inputs.

## Selected Approach

Add a top-level payload:

```text
paper_offline_changed_decomposition_output_contract
```

The payload should summarize existing search and postprocess fixture evidence into contract rows:

- `decomposition_output_rows` for cases with `collapse_trace.final_active_groups`;
- `primitive_records` inside each output row, using `offline_primitive_id` identifiers;
- `postprocess_state_rows` for explicit postprocess audit fixtures;
- source, primitive, search, postprocess, and package-boundary summary references;
- false package/Newton/real-USD/benchmark triggers.

The next gate after this contract should be `paper_package_adapter_contract`, not package
generation. That name keeps the next step focused on adapter contract design rather than implying
that packages are ready.

## Report Contract

The new top-level payload must include:

- `gate_id: paper_offline_changed_decomposition_output_contract`
- `gate_status: implemented_offline_contract_only_partial`
- `closed_gate: paper_offline_changed_decomposition_output_contract`
- `next_required_gate: paper_package_adapter_contract`
- `decision: remain_partial`
- `decision_reason: changed_decomposition_output_contract_complete_package_adapter_contract_missing`
- `paper_faithful_offline_allowed: false`
- `package_generation_allowed: false`
- `artifact_kind: offline_changed_decomposition_output_not_collision_package`
- `schema_version: 1`
- `source_scope: synthetic_toy_fixtures_only`
- `implementation_boundary: offline_report_contract_no_collision_package_no_newton`
- `output_contract`
- `decomposition_output_rows`
- `postprocess_state_rows`
- `coverage_summary`
- `remaining_gaps`
- false triggers for package generation, Newton runtime, real USD, and benchmarks.

After this slice, the report itself must remain:

```text
status: partial
paper_faithful_offline_supported: false
next_required_gate: paper_package_adapter_contract
```

Top-level failure labels must become only:

```text
paper_package_adapter_contract_missing
```

## Decomposition Output Rows

Rows should be created from cases that already have `collapse_trace.final_active_groups`.

Each row should contain:

- `output_id`
- `evidence_case_id`
- `row_status`
- `source_mesh_summary`
- `search_summary`
- `primitive_records`
- `postprocess_state`
- `unsupported_boundaries`
- `claim_boundary`
- false package/Newton/real-USD/benchmark triggers.

Each primitive record should contain:

- `offline_primitive_id`
- `source_faces`
- `source_face_ids`
- `generated_triangle_face_ids`
- `paper_primitive`
- `center`
- `axes`
- `dimensions`
- `volume`
- `paper_weight`
- `weighted_volume`
- `contains_assigned_points`
- `newton_runtime_kind`
- `conversion_status: offline_contract_only_not_package_candidate`

The first version may reuse the case-level selected primitive audit row for each final active group
and must label that reuse as contract accounting, not group-specific refitting.

## Postprocess State Rows

Rows should be created from the three explicit postprocess audit fixtures:

- `paper_nested_primitive`
- `paper_rotated_nested_primitive`
- `paper_cross_type_enclosure_boundary`

Each row should contain:

- `state_id`
- `evidence_case_id`
- `postprocess_input_source`
- `postprocess_policy`
- `kept_primitive_ids`
- `culled_primitive_ids`
- `cull_record_count`
- `unsupported_record_count`
- `unsupported_containment_label`
- `state_scope: explicit_postprocess_audit_fixture_not_search_output`
- false package/Newton/real-USD/benchmark triggers.

## Invariants

Tests must assert:

- the new payload exists and closes only `paper_offline_changed_decomposition_output_contract`;
- top-level `next_required_gate` moves to `paper_package_adapter_contract`;
- top-level failure labels remove `paper_offline_changed_decomposition_output_contract_missing`;
- `paper_faithfulness.implemented_output_contract_scope` contains only
  `paper_offline_changed_decomposition_output_contract`;
- `paper_faithfulness.implemented_generalization_scope` remains the Batch A-E list;
- report status remains partial and `paper_faithful_offline_supported` remains false;
- no package, Newton, real-USD, benchmark, timing, surface-distance, or collision-quality output is
  introduced;
- decomposition rows match the referenced search case payloads;
- postprocess state rows are explicitly marked as audit fixtures, not search output.

## Claim Boundaries

This slice supports only:

```text
offline changed-decomposition output contract for deterministic synthetic fixture evidence
```

It does not support claims of:

- `CollisionPackage` generation;
- package readiness;
- Newton readiness;
- runtime readiness;
- `paper_faithful_offline` support;
- full CPD paper reproduction;
- general mesh cleanup;
- general containment-library correctness;
- real-USD evidence;
- benchmark or collision-quality evidence;
- deployment readiness or safety certification.

## Documentation Updates

Update current status and boundary docs:

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
- `docs/records/2026-05-17-cpd-paper-changed-decomposition-output-contract.md`

## Self-Review

- No placeholder sections remain.
- The design keeps package generation and Newton runtime out of scope.
- The next gate is `paper_package_adapter_contract`, not a package-generation claim.
- The report remains partial and keeps `paper_faithful_offline_supported: false`.
