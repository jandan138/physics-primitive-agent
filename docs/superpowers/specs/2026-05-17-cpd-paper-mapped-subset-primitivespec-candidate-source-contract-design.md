# CPD Paper Mapped-Subset PrimitiveSpec Candidate Source Contract Design

## Date

2026-05-17

## Status

Proposed for the next offline/report-only CPD paper-lane slice after
`paper_mapped_subset_primitivespec_generation_contract`.

## Context

The current `cpd_paper_offline_report` closes
`paper_mapped_subset_primitivespec_generation_contract`. That gate emits offline template rows for
future Newton-native `box`, `sphere`, and `capsule` PrimitiveSpec shapes, records blocked
approximation-policy rows for `capped_cylinder` and `frustum`, records a no-op row for
`trapezoidal_prism`, and keeps all 16 current rows offline/no-op because the current changed
decomposition rows are still unmapped trapezoidal-prism rows.

The next named blocker is
`paper_mapped_subset_primitivespec_candidate_source_contract`. Its job is not to generate runtime
PrimitiveSpecs. Its job is to audit whether the generation-contract output contains any valid
current candidate source row that a later PrimitiveSpec generation step could instantiate. Today
the answer is deliberately "no".

## Plain-Language Purpose

Think of the previous gate as a form template:

- "If we later have a box-like current row, this is the information a box PrimitiveSpec will need."
- "If we later have a sphere-like current row, this is the information a sphere PrimitiveSpec will
  need."
- "If we later have a capsule-like current row, this is the information a capsule PrimitiveSpec will
  need."

That is not the same as having a real current row. The candidate-source contract makes that
distinction explicit. It says:

- the native-family template rows are future templates, not current candidates;
- the current rows are real traceable rows, but they are unmapped `trapezoidal_prism` rows;
- therefore the report still has zero eligible current PrimitiveSpec candidate sources.

## Design Choice

Implement an offline source-audit contract, not PrimitiveSpec generation.

The payload should consume `paper_mapped_subset_primitivespec_generation_contract` and emit:

- a `source_audit_contract` block that names the upstream generation contract and the next blocker;
- three native-template source audit rows classified as future-only;
- three paper-family blocked/no-op audit rows classified as not current candidates;
- 16 current-row audit rows classified as traceable but ineligible;
- exact source counts and eligibility counts;
- zero runtime PrimitiveSpec candidates;
- zero generated PrimitiveSpecs;
- zero generated CollisionPackages;
- zero runtime-admissibility checks;
- false Newton, real-USD, benchmark, collision-quality, deployment, and certification flags.

The recommended next gate after this slice is:

```text
paper_mapped_subset_native_current_fixture_contract
```

That next gate is intentionally narrow. It says the following step should add or select a
deterministic synthetic current row in the Newton-native mapped subset before real PrimitiveSpec
objects are generated. It does not jump to packages, Newton runtime, real USD, or benchmarks.

## Alternatives Considered

### Option A: Treat Native Templates As Current Candidates

Rejected. The template rows do not come from a current changed decomposition row. Treating them as
current candidates would imply package-readiness evidence that the report does not have.

### Option B: Directly Add Runtime PrimitiveSpecs For Box/Sphere/Capsule

Rejected. There are no eligible current mapped rows to instantiate. Runtime PrimitiveSpec
generation belongs after a current native fixture or another explicit current-candidate source is
recorded.

### Option C: Skip To Package Generation

Rejected. This would hide the biggest remaining boundary: paper-only and unmapped rows still need
either an explicit approximation policy or an explicit mapped current source before package
conversion.

### Option D: Offline Candidate-Source Audit

Selected. It closes the named candidate-source contract while preserving claim boundaries and
making the next blocker precise.

## Payload Contract

Add a payload named:

```text
paper_mapped_subset_primitivespec_candidate_source_contract
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
candidate_source_action
candidate_source_contract
input_contract_summary
native_template_candidate_source_audit_rows
blocked_family_candidate_source_audit_rows
noop_family_candidate_source_audit_rows
current_row_candidate_source_audit_rows
coverage_summary
remaining_gaps
```

The payload must carry the established false/zero runtime boundary fields:

```text
primitive_spec_generation_candidate_count
eligible_current_candidate_source_count
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

## Candidate Source Contract Block

The nested `candidate_source_contract` block must include:

```text
input_gate_required: paper_mapped_subset_primitivespec_generation_contract
current_candidate_source_gate_closed: paper_mapped_subset_primitivespec_candidate_source_contract
next_current_candidate_gate_required: paper_mapped_subset_native_current_fixture_contract
native_template_rows_are_future_only: true
current_rows_must_be_mapped_native_family: true
eligible_current_candidate_source_required_before_runtime_generation: true
zero_runtime_primitivespecs_required: true
zero_collision_packages_required: true
zero_runtime_admissibility_checks_required: true
runtime_primitive_spec_generation_allowed: false
collision_package_generation_allowed: false
newton_runtime_allowed: false
approximation_policy_enabled: false
silent_drop_allowed: false
```

## Input Validation

The candidate-source contract must reject malformed generation-contract payloads.

Required input properties:

- `gate_id == paper_mapped_subset_primitivespec_generation_contract`;
- `next_required_gate == paper_mapped_subset_primitivespec_candidate_source_contract`;
- all runtime, evaluation, package, Newton, real-USD, benchmark, collision-quality, deployment, and
  certification flags are false;
- `primitive_spec_generation_candidate_count == 0`;
- `offline_primitivespec_template_count == 3`;
- `generated_primitive_spec_count == 0`;
- `generated_collision_package_count == 0`;
- `runtime_admissibility_check_count == 0`;
- nested `primitive_spec_generation_contract` keeps:
  - `input_gate_required == paper_mapped_subset_primitivespec_generation_preflight_contract`;
  - `current_candidate_source_gate_required == paper_mapped_subset_primitivespec_candidate_source_contract`;
  - `template_only_native_families == ["box", "sphere", "capsule"]`;
  - zero-runtime and disabled-runtime flags as true/false exactly as emitted by the generation
    contract;
- native template rows are exactly `oriented_bounding_box`, `sphere`, and `capsule`;
- blocked family rows are exactly `capped_cylinder` and `frustum`;
- no-op family rows are exactly `trapezoidal_prism`;
- current rows are 16 traceable `trapezoidal_prism` rows with
  `offline_mapping_label == offline_only_unmapped`;
- all source ids are non-empty;
- emitted candidate-source audit row ids are unique;
- no row carries a generated PrimitiveSpec object, runtime candidate flag, or silent-drop flag.

## Audit Row Types

### Native Template Audit Rows

These rows come from `native_family_primitivespec_template_rows`. They are future-only templates.

Required fields:

```text
candidate_source_audit_row_id
source_primitivespec_generation_row_id
source_primitivespec_generation_preflight_row_id
source_primitivespec_validation_row_id
source_primitivespec_dry_run_row_id
source_adapter_preflight_row_id
source_candidate_matrix_row_id
source_conversion_plan_row_id
paper_primitive
primitive_spec_kind
candidate_mapping_label
source_role
candidate_source_decision
candidate_source_reason
eligible_current_candidate_source
primitive_spec_generation_candidate
generated_primitive_spec
required_later_gate
required_future_policy
```

Required values:

```text
source_role: future_native_template
candidate_source_decision: template_only_not_current_candidate_source
candidate_source_reason: native_family_template_has_no_current_decomposition_row
eligible_current_candidate_source: false
primitive_spec_generation_candidate: false
generated_primitive_spec: null
required_later_gate: paper_mapped_subset_native_current_fixture_contract
required_future_policy: native_current_fixture
```

### Blocked Family Audit Rows

These rows come from blocked `capped_cylinder` and `frustum` generation requirement rows.

Required values:

```text
source_role: blocked_paper_family
candidate_source_decision: blocked_until_approximation_policy
candidate_source_reason: paper_family_requires_explicit_approximation_policy_before_runtime_source
eligible_current_candidate_source: false
required_later_gate: paper_mapped_subset_native_current_fixture_contract
required_future_policy: approximation_policy
```

### No-Op Family Audit Rows

These rows come from the no-op `trapezoidal_prism` generation requirement row.

Required values:

```text
source_role: unmapped_paper_family
candidate_source_decision: no_current_native_candidate_source
candidate_source_reason: paper_family_has_no_newton_native_mapping_in_current_policy
eligible_current_candidate_source: false
required_later_gate: paper_mapped_subset_native_current_fixture_contract
required_future_policy: native_current_fixture_or_explicit_mapping_policy
```

### Current Row Audit Rows

These rows come from `current_row_primitivespec_generation_rows`.

Required values:

```text
source_role: current_unmapped_row
candidate_source_decision: current_row_ineligible_unmapped_paper_primitive
candidate_source_reason: current_row_is_trapezoidal_prism_offline_only_unmapped
eligible_current_candidate_source: false
primitive_spec_generation_candidate: false
generated_primitive_spec: null
required_later_gate: paper_mapped_subset_native_current_fixture_contract
required_future_policy: native_current_fixture
```

Every audit row must also carry the established row-level false flags for PrimitiveSpec,
CollisionPackage, runtime admissibility, Newton, approximation, real USD, benchmark,
collision-quality, deployment/certification, and trigger fields.

## Coverage Summary

The exact coverage summary must include:

```text
candidate_source_requirement_row_count: 6
native_template_candidate_source_audit_row_count: 3
blocked_family_candidate_source_audit_row_count: 2
noop_family_candidate_source_audit_row_count: 1
current_row_candidate_source_audit_row_count: 16
eligible_current_candidate_source_count: 0
ineligible_current_candidate_source_count: 16
future_template_only_source_count: 3
blocked_policy_source_count: 2
noop_unmapped_family_source_count: 1
primitive_spec_generation_candidate_record_count: 0
generated_primitive_spec_record_count: 0
generated_collision_package_record_count: 0
runtime_admissibility_check_record_count: 0
current_paper_primitive_distribution: {"trapezoidal_prism": 16}
current_mapping_label_distribution: {"offline_only_unmapped": 16}
candidate_source_decision_distribution:
  template_only_not_current_candidate_source: 3
  blocked_until_approximation_policy: 2
  no_current_native_candidate_source: 1
  current_row_ineligible_unmapped_paper_primitive: 16
```

## Rejection Labels

The implementation should raise `ValueError` labels that make drift easy to debug:

```text
primitivespec_candidate_source_input_gate_id_mismatch
primitivespec_candidate_source_input_next_gate_mismatch
primitivespec_candidate_source_input_trigger_flag_true:<flag>
primitivespec_candidate_source_input_candidate_count_nonzero
primitivespec_candidate_source_input_template_count_mismatch
primitivespec_candidate_source_input_generated_spec_nonzero
primitivespec_candidate_source_input_generated_collision_package_nonzero
primitivespec_candidate_source_input_runtime_admissibility_nonzero
primitivespec_candidate_source_input_contract_mismatch:<field>
primitivespec_candidate_source_coverage_count_mismatch:<field>
primitivespec_candidate_source_native_template_sequence_mismatch
primitivespec_candidate_source_blocked_family_sequence_mismatch
primitivespec_candidate_source_noop_family_sequence_mismatch
primitivespec_candidate_source_missing_template_source_id:<field>
primitivespec_candidate_source_missing_requirement_source_id:<field>
primitivespec_candidate_source_missing_current_row_source_id:<field>
primitivespec_candidate_source_template_runtime_leak:<field>
primitivespec_candidate_source_requirement_runtime_leak:<field>
primitivespec_candidate_source_current_row_runtime_leak:<field>
primitivespec_candidate_source_current_row_not_unmapped
duplicate_primitivespec_candidate_source_row_id
duplicate_primitivespec_candidate_source_input_row_id
```

## Top-Level Report Integration

After this slice:

```text
report["paper_mapped_subset_primitivespec_candidate_source_contract"]
```

must exist.

Top-level report state should become:

```text
next_required_gate: paper_mapped_subset_native_current_fixture_contract
failure_labels:
  - paper_mapped_subset_native_current_fixture_contract_missing
paper_faithfulness.missing_before_paper_faithful_offline:
  - paper_mapped_subset_native_current_fixture_contract
```

`paper_faithfulness.implemented_output_contract_scope` must append
`paper_mapped_subset_primitivespec_candidate_source_contract`.

## Out Of Scope

This slice must not:

- instantiate `PrimitiveSpec` dataclasses;
- emit runtime PrimitiveSpec dictionaries;
- emit a `CollisionPackage`;
- run Newton;
- load bed, Franka, or any real USD;
- run benchmarks;
- measure collision quality;
- apply capped-cylinder or frustum approximation policy;
- silently drop unsupported paper primitives;
- claim package readiness, Newton readiness, runtime admissibility, deployment readiness, safety
  certification, or full CPD paper reproduction.

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
- `experiments/registry.yaml`;
- add `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-candidate-source-contract.md`.

## Success Criteria

- The new payload exists and closes only
  `paper_mapped_subset_primitivespec_candidate_source_contract`.
- It records zero eligible current candidate sources.
- It distinguishes future native templates from current unmapped rows.
- It advances the next gate to `paper_mapped_subset_native_current_fixture_contract`.
- It preserves all runtime, package, Newton, real-USD, benchmark, collision-quality, deployment,
  and certification boundaries.
- Focused offline tests, CLI tests, full tests, docs validation, site claim validation, and
  whitespace checks pass before merge.
