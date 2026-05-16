# CPD Paper Postprocess Policy Generalization Design

## Purpose

Close `paper_generalization_batch_d_postprocess_policy` by adding a top-level offline report
payload that summarizes the existing enclosed-primitive postprocess audit fixtures. This is a
report-only generalization checkpoint. It does not add a broad containment library, build a
`CollisionPackage`, run Newton, load real USD assets, or run benchmarks.

## Current Context

`cpd_paper_offline_report` already contains three postprocess evidence cases:

- `paper_nested_primitive`: identity-axis OBB inside a larger OBB, with the inner primitive
  culled;
- `paper_rotated_nested_primitive`: rotated OBB inside a larger rotated OBB, with the inner
  primitive culled after transformed-corner containment passes;
- `paper_cross_type_enclosure_boundary`: sphere inside an OBB, explicitly recorded as unsupported
  cross-type containment with no silent cull.

Those fixtures currently live only under individual `cases[*].postprocess_audit` payloads. Batch D
needs a stable top-level matrix that says: the postprocess policy evidence is now summarized as one
offline generalization gate, while the whole paper lane remains partial.

## Selected Approach

Reuse existing `postprocess_audit` payloads and build a lightweight
`paper_generalization_batch_d_postprocess_policy` summary matrix from named cases. The matrix
should reference case ids and copy bounded summary fields, not duplicate full primitive geometry
rows.

This is preferred over adding generic cross-type containment because the current Newton-facing
strategy remains native-primitive-first, and unsupported paper/runtime gaps must stay explicit.
It is also preferred over jumping to package generation because the package boundary is the next
separate gate.

## Report Contract

The new top-level payload must include:

```text
paper_generalization_batch_d_postprocess_policy
```

Required fields:

- `gate_id: paper_generalization_batch_d_postprocess_policy`
- `gate_status: implemented_offline_report_only_partial`
- `closed_gate: paper_generalization_batch_d_postprocess_policy`
- `next_required_gate: paper_generalization_batch_e_package_boundary_readiness`
- `decision: remain_partial`
- `decision_reason: postprocess_policy_generalization_complete_package_boundary_readiness_missing`
- `paper_faithful_offline_allowed: false`
- `source_scope: deterministic_in_memory_postprocess_audit_fixtures`
- `implementation_boundary: offline_report_only_no_package_or_newton`
- `postprocess_policy_contract`
- `postprocess_policy_matrix`
- `coverage_summary`
- `remaining_gaps`
- false triggers for package generation, Newton runtime, real USD, and benchmarks.

The report itself must remain:

```text
status: partial
paper_faithful_offline_supported: false
next_required_gate: paper_generalization_batch_e_package_boundary_readiness
```

Top-level failure labels must become only:

```text
paper_generalization_batch_e_package_boundary_readiness_missing
```

## Postprocess Policy Contract

`postprocess_policy_contract` pins the current offline postprocess semantics:

- input contract: explicit audit primitive rows, not generated search output;
- supported cull policy: same-family OBB containment by testing all candidate OBB corners inside
  the enclosing OBB;
- supported axis cases: shared identity axes and shared rotated axes;
- unsupported cross-type policy: do not silently cull; record an unsupported boundary row;
- output accounting: input count, output count, kept ids, culled ids, cull records, unsupported
  records where applicable;
- no package generation, Newton runtime, real USD loading, or benchmark execution.

## Matrix Rows

The Batch D payload should summarize these existing evidence cases:

| Row id | Evidence case | Purpose |
| --- | --- | --- |
| `identity_nested_obb_cull` | `paper_nested_primitive` | Identity-axis OBB containment culls one enclosed primitive. |
| `rotated_nested_obb_cull` | `paper_rotated_nested_primitive` | Shared rotated OBB containment culls one enclosed primitive. |
| `cross_type_enclosure_no_silent_cull_boundary` | `paper_cross_type_enclosure_boundary` | Unsupported cross-type boundary records no silent cull. |

Each row should contain:

- `row_id`
- `evidence_case_id`
- `row_status`
- `audit_scope`
- `fixture_variant`
- `postprocess_input_source`
- `postprocess_policy`
- `containment_test_type`
- `axis_policy`
- `rotation_degrees_about_z`
- `rotated_axes_non_identity`
- `cross_type_culling_supported`
- `unsupported_containment_label`
- `input_primitive_count`
- `output_primitive_count`
- `culled_primitive_ids`
- `kept_primitive_ids`
- `enclosed_primitive_ids`
- `enclosing_primitive_ids`
- `cull_record_count`
- `unsupported_record_count`
- `top_level_failure_label`
- `claim_boundary`
- false package/Newton/USD/benchmark triggers.

## Invariants

Tests must assert:

- Batch D payload exists and closes only `paper_generalization_batch_d_postprocess_policy`;
- `implemented_generalization_scope` includes Batch A, Batch B, Batch C, and Batch D;
- top-level `next_required_gate` advances only to Batch E;
- top-level failure labels contain only Batch E;
- report status and paper-faithful support remain partial/false;
- all matrix rows point to existing `cases[*].postprocess_audit` payloads;
- all summary counts and ids match the referenced audit payloads;
- OBB cull rows have one cull record, one culled primitive, and output count one less than input
  count;
- the cross-type boundary has `cross_type_culling_supported: false`, zero cull records, one
  unsupported record, and no top-level failure label;
- all new payloads and rows keep package/Newton/USD/benchmark triggers false;
- no timing, surface distance, collision-quality, benchmark, package, or runtime-readiness fields
  are introduced.
- references to older fixture-breadth Batch D remain explicitly qualified as component-pair
  fixture breadth, not this generalization Batch D postprocess policy gate.

## Claim Boundaries

This slice supports only:

```text
offline report-only postprocess policy generalization matrix for deterministic synthetic fixtures
```

It does not support claims of:

- full CPD paper reproduction;
- generalized containment-library correctness;
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
- `docs/records/2026-05-17-cpd-paper-generalization-batch-d-postprocess-policy.md`

## Self-Review

- No placeholder sections remain.
- The design is offline-only and does not conflict with the Newton-native runtime policy.
- The selected approach follows the existing report pattern from Batches A, B, and C.
- The next gate after this slice is Batch E package-boundary readiness, not runtime or benchmark
  execution.
