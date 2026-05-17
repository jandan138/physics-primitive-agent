# CPD Paper Mapped-Subset Native Current Fixture Contract Design

## Date

2026-05-17

## Status

Proposed for the next offline/report-only CPD paper-lane slice after
`paper_mapped_subset_primitivespec_candidate_source_contract`.

## Context

The current `cpd_paper_offline_report` closes
`paper_mapped_subset_primitivespec_candidate_source_contract`. That gate proves a negative fact:
the report has future native templates for `box`, `sphere`, and `capsule`, but it has zero eligible
current candidate sources because the 16 current changed-decomposition rows are still
`trapezoidal_prism` / `offline_only_unmapped`.

The next blocker is `paper_mapped_subset_native_current_fixture_contract`. Its purpose is to add one
deterministic, synthetic, Newton-native current fixture source that a later report-only
PrimitiveSpec generation gate can consume. This slice still must not generate runtime
`PrimitiveSpec` objects, `CollisionPackage` artifacts, runtime-admissibility records, Newton task
results, real-USD evidence, benchmarks, collision-quality evidence, deployment readiness, or safety
certification claims.

## Plain-Language Purpose

The previous gate said:

```text
We know what a future box/sphere/capsule PrimitiveSpec template would need, but no current row is
eligible yet.
```

This gate should say:

```text
For one tiny synthetic fixture, we now have one traceable current source row in the mapped
Newton-native subset: the paper_single_box OBB audit can be used later as a box PrimitiveSpec
candidate source.
```

It does not say:

```text
We generated a PrimitiveSpec.
We generated a CollisionPackage.
Newton ran it.
The collider is better.
The paper has been reproduced.
```

## Design Choice

Implement a narrow offline native-current-fixture source contract.

The payload should consume:

- `paper_mapped_subset_primitivespec_candidate_source_contract`;
- the existing `paper_single_box` toy fixture from `cases`;
- the selected `oriented_bounding_box` primitive-fit audit row from that fixture.

The payload should emit exactly one native current fixture source row:

```text
fixture_id: paper_single_box
paper_primitive: oriented_bounding_box
primitive_spec_kind: box
candidate_mapping_label: box
source_role: synthetic_native_current_fixture
eligible_current_candidate_source: true
primitive_spec_generation_candidate: true
generated_primitive_spec: null
```

The top-level report should remain `partial` and advance the next gate to:

```text
paper_mapped_subset_primitivespec_native_fixture_generation_contract
```

That next gate can later turn the fixture source into a report-only generated PrimitiveSpec record.
This slice stops before that step.

## Alternatives Considered

### Option A: Reclassify The Existing 16 Current Rows As Native

Rejected. Those rows are traceable but still `trapezoidal_prism` / `offline_only_unmapped`.
Reclassifying them as `box`, `sphere`, or `capsule` would erase the paper-vocabulary gap and would
make the report look package-ready without evidence.

### Option B: Use The Future Native Template Rows As Current Sources

Rejected. Template rows describe the shape of future records. They are not produced by a concrete
fixture source and therefore cannot be counted as current candidate sources.

### Option C: Generate A Runtime PrimitiveSpec Immediately

Rejected. This gate should establish one eligible source row only. Generation, validation,
packaging, and runtime admissibility remain separate gates so the evidence chain stays reviewable.

### Option D: Add One Synthetic OBB/Box Current Fixture Source

Selected. The existing `paper_single_box` fixture already has a paper-shaped OBB fit audit with
`newton_runtime_kind: box`, containment status, finite center/axes/half-extents, and source-face
traceability. Using it gives the next gate a real source row without inventing runtime behavior.

## Payload Contract

Add a payload named:

```text
paper_mapped_subset_native_current_fixture_contract
```

The payload must include:

```text
gate_id
gate_status
closed_gate
input_gate_id
next_required_gate
decision
decision_reason
paper_faithful_offline_allowed
package_generation_allowed
artifact_kind
schema_version
source_scope
implementation_boundary
native_current_fixture_action
native_current_fixture_contract
input_contract_summary
fixture_source_summary
native_current_fixture_source_rows
coverage_summary
remaining_gaps
```

The payload must also carry the established runtime boundary and count fields:

```text
eligible_current_candidate_source_count
primitive_spec_generation_candidate_count
generated_primitive_spec_count
generated_collision_package_count
runtime_admissibility_check_count
primitive_spec_generated
collision_package_generated
runtime_admissibility_checked
newton_support_claimed
approximation_policy_applied
real_usd_loaded
benchmark_run
collision_quality_measured
deployment_or_certification_claimed
package_generation_triggered
newton_runtime_triggered
real_usd_triggered
benchmark_triggered
primitive_spec_generation_allowed
collision_package_generation_allowed
runtime_admissibility_supported
newton_runtime_allowed
approximation_policy_enabled
silent_drop_allowed
primitive_spec_generation_triggered
collision_package_generation_triggered
runtime_admissibility_triggered
```

Counts must be:

```text
eligible_current_candidate_source_count: 1
primitive_spec_generation_candidate_count: 1
generated_primitive_spec_count: 0
generated_collision_package_count: 0
runtime_admissibility_check_count: 0
```

## Native Current Fixture Contract Block

The nested `native_current_fixture_contract` block must include:

```text
input_gate_required: paper_mapped_subset_primitivespec_candidate_source_contract
native_current_fixture_gate_closed: paper_mapped_subset_native_current_fixture_contract
next_generation_gate_required: paper_mapped_subset_primitivespec_native_fixture_generation_contract
source_fixture_required: paper_single_box
source_fit_selected_paper_primitive_required: oriented_bounding_box
source_template_row_required: candidate_source_template__oriented_bounding_box
native_fixture_rows_required: 1
eligible_current_candidate_sources_required: 1
primitive_spec_generation_candidates_required: 1
generated_primitivespecs_required: 0
generated_collision_packages_required: 0
runtime_admissibility_checks_required: 0
runtime_primitive_spec_generation_allowed: false
collision_package_generation_allowed: false
newton_runtime_allowed: false
approximation_policy_enabled: false
real_usd_allowed: false
benchmark_allowed: false
silent_drop_allowed: false
```

## Native Current Fixture Source Row

Each row in `native_current_fixture_source_rows` must include:

```text
native_current_fixture_source_row_id
source_candidate_source_audit_row_id
source_primitivespec_generation_row_id
source_primitivespec_generation_preflight_row_id
source_primitivespec_validation_row_id
source_primitivespec_dry_run_row_id
source_adapter_preflight_row_id
source_candidate_matrix_row_id
source_conversion_plan_row_id
fixture_id
fixture_source_faces
source_fit_selected_paper_primitive
source_fit_candidate_scope
source_fit_selection_rule
paper_primitive
primitive_spec_kind
candidate_mapping_label
newton_runtime_kind
source_role
candidate_source_decision
candidate_source_reason
eligible_current_candidate_source
primitive_spec_generation_candidate
generated_primitive_spec
required_later_gate
required_future_policy
fit_model
axis_selection_policy
center
axes
half_extents
volume
weighted_volume
contains_assigned_points
primitive_parameter_lower_clamp
```

The single row must use:

```text
native_current_fixture_source_row_id: native_current_fixture__paper_single_box__oriented_bounding_box
source_candidate_source_audit_row_id: candidate_source_template__oriented_bounding_box
fixture_id: paper_single_box
paper_primitive: oriented_bounding_box
primitive_spec_kind: box
candidate_mapping_label: box
newton_runtime_kind: box
source_role: synthetic_native_current_fixture
candidate_source_decision: eligible_synthetic_native_current_fixture_source
candidate_source_reason: paper_single_box_selected_obb_fixture_is_newton_native_box_source
eligible_current_candidate_source: true
primitive_spec_generation_candidate: true
generated_primitive_spec: null
required_later_gate: paper_mapped_subset_primitivespec_native_fixture_generation_contract
required_future_policy: report_only_primitivespec_native_fixture_generation
```

The row must keep every runtime/evaluation/package flag false. `primitive_spec_generation_candidate`
is true because this is now an eligible source for a future report-only generation gate, but
`primitive_spec_generation_triggered` remains false because no generation is executed in this slice.

## Input Validation

The native-current-fixture contract must reject malformed inputs.

Candidate-source payload requirements:

- `gate_id == paper_mapped_subset_primitivespec_candidate_source_contract`;
- `next_required_gate == paper_mapped_subset_native_current_fixture_contract`;
- `eligible_current_candidate_source_count == 0`;
- `primitive_spec_generation_candidate_count == 0`;
- `generated_primitive_spec_count == 0`;
- `generated_collision_package_count == 0`;
- `runtime_admissibility_check_count == 0`;
- all runtime, package, Newton, real-USD, benchmark, collision-quality, deployment, certification,
  approximation, and silent-drop flags are false;
- `native_template_candidate_source_audit_rows` contains exactly one
  `candidate_source_template__oriented_bounding_box` row with `primitive_spec_kind == box`,
  `candidate_mapping_label == box`, `source_role == future_native_template`, and
  `eligible_current_candidate_source == false`;
- every `current_row_candidate_source_audit_rows` row still has
  `eligible_current_candidate_source == false`, `primitive_spec_generation_candidate == false`,
  `generated_primitive_spec == null`, and false runtime/package/Newton/evaluation flags;
- blocked/no-op/current-row counts still match the candidate-source contract.

Fixture requirements:

- the cases list contains exactly one `paper_single_box` case;
- that case has `primitive_fit_audit.selected.paper_primitive == oriented_bounding_box`;
- selected fit fields are finite and complete: center, axes, half-extents, volume, weighted volume,
  containment status, and `newton_runtime_kind == box`;
- selected OBB geometry must match the OBB candidate row in the same primitive-fit audit for
  center, axes, half-extents, volume, and weighted volume;
- the fixture has non-empty source faces;
- the selected fit contains assigned points.

## Top-Level Report Changes

After this gate:

```text
next_required_gate: paper_mapped_subset_primitivespec_native_fixture_generation_contract
failure_labels:
  - paper_mapped_subset_primitivespec_native_fixture_generation_contract_missing
missing_before_paper_faithful_offline:
  - paper_mapped_subset_primitivespec_native_fixture_generation_contract
implemented_output_contract_scope:
  - ... existing gates ...
  - paper_mapped_subset_native_current_fixture_contract
```

The report must remain:

```text
status: partial
paper_faithful_offline_supported: false
package_generation_triggered: false
newton_runtime_triggered: false
real_usd_triggered: false
benchmark_triggered: false
collision_quality_measured: false
deployment_or_certification_claimed: false
```

## Documentation Updates

Update:

- `README.md`;
- `docs/index.md`;
- `docs/deepdive/evidence-status.md`;
- `docs/deepdive/message-map.md`;
- `docs/reference/claim-boundaries.md`;
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`;
- `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`;
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`;
- `docs/reference/cpd-paper-story-status.md`;
- `docs/records/README.md`;
- `experiments/registry.yaml`.

Create:

- `docs/records/2026-05-17-cpd-paper-mapped-subset-native-current-fixture-contract.md`.

## Acceptance Criteria

- The report includes `paper_mapped_subset_native_current_fixture_contract`.
- The payload records exactly one eligible synthetic native current fixture source row.
- The row is traced to `paper_single_box`, selected OBB fit fields, and the OBB native template row.
- The payload advances only to the report-only native-fixture PrimitiveSpec generation gate.
- Runtime `PrimitiveSpec`, `CollisionPackage`, Newton, real USD, benchmarks, collision-quality,
  deployment, and safety claims remain false/zero.
- Tests cover payload schema, exact counts, row values, top-level next gate movement, CLI JSON
  exposure, malformed candidate-source input, malformed fixture input, and no runtime leakage.
- Docs and records explain the gate in plain language and preserve claim boundaries.
