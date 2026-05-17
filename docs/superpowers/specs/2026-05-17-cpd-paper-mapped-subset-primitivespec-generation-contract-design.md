# CPD Paper Mapped-Subset PrimitiveSpec Generation Contract Design

## Date

2026-05-17

## Status

Proposed for the next offline/report-only CPD paper-lane slice.

## Context

The current `cpd_paper_offline_report` has closed
`paper_mapped_subset_primitivespec_generation_preflight_contract`. That preflight gate validates
the previous PrimitiveSpec validation payload, records six paper-family requirements, and keeps the
current 16 unmapped `trapezoidal_prism` rows offline/no-op. It advances the top-level next gate to
`paper_mapped_subset_primitivespec_generation_contract`.

The important constraint is that the report still has zero current PrimitiveSpec generation
candidates. The only mapped native-family information is at the paper-family requirement level:
OBB/box, sphere, and capsule have future native-family requirements, while capped cylinder and
frustum remain blocked behind approximation policy and trapezoidal prism remains no-op/unmapped.

## Design Choice

Use a minimal offline PrimitiveSpec generation contract, not runtime PrimitiveSpec generation.

The new gate should consume the generation-preflight payload and emit:

- three offline native-family PrimitiveSpec template rows for `box`, `sphere`, and `capsule`;
- two blocked approximation-policy rows for `capped_cylinder` and `frustum`;
- one no-op unmapped family row for `trapezoidal_prism`;
- 16 current-row no-generation records that preserve source traceability and keep current rows
  offline;
- zero generated runtime PrimitiveSpec objects;
- zero generated CollisionPackage objects;
- zero runtime-admissibility checks;
- a new next gate for sourcing actual mapped current candidates before package work.

The recommended next gate after this slice is:

```text
paper_mapped_subset_primitivespec_candidate_source_contract
```

That name is intentionally not a package-generation gate. It records the real blocker: the current
offline changed-decomposition rows are still unmapped `trapezoidal_prism` rows, so a later slice
must introduce or select actual mapped current rows before real PrimitiveSpec objects can be
generated.

## Alternatives Considered

### Option A: Generate Runtime PrimitiveSpec Objects Now

This would create real `PrimitiveSpec` dictionaries or classes for the three native families.

Rejected for this slice because the current payload has no mapped current primitive rows to
instantiate. Generating objects only from family requirement rows would look more complete than the
evidence supports.

### Option B: Skip Generation And Jump To CollisionPackage Planning

This would bypass the current next gate and move directly toward package conversion.

Rejected because it would hide the missing PrimitiveSpec candidate-source problem. The paper-lane
needs an explicit record of why no current PrimitiveSpec can be generated.

### Option C: Offline Generation Contract With Template Rows

This is the selected approach. It closes the named generation contract by producing reviewable
template rows and no-generation current rows, while preserving the boundary that no runtime
PrimitiveSpec, CollisionPackage, Newton task, real USD, benchmark, or collision-quality claim is
created.

## Payload Contract

Add a payload named:

```text
paper_mapped_subset_primitivespec_generation_contract
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
primitive_spec_generation_action
primitive_spec_generation_candidate_count
offline_primitivespec_template_count
generated_primitive_spec_count
generated_collision_package_count
runtime_admissibility_check_count
input_contract_summary
primitive_spec_generation_contract
native_family_primitivespec_template_rows
blocked_primitivespec_generation_requirement_rows
noop_primitivespec_generation_requirement_rows
current_row_primitivespec_generation_rows
coverage_summary
remaining_gaps
```

The payload must keep these false or zero:

```text
paper_faithful_offline_allowed
package_generation_allowed
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
package_generation_triggered
newton_runtime_triggered
real_usd_triggered
benchmark_triggered
collision_quality_measured
deployment_or_certification_claimed
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

## Input Validation

The generation contract must reject malformed generation-preflight payloads.

Required input properties:

- `gate_id == paper_mapped_subset_primitivespec_generation_preflight_contract`;
- `next_required_gate == paper_mapped_subset_primitivespec_generation_contract`;
- all report/runtime/claim trigger flags are false;
- generation-preflight candidate count is zero;
- generated PrimitiveSpec count is zero;
- generated CollisionPackage count is zero;
- runtime-admissibility check count is zero;
- nested `primitive_spec_generation_preflight_contract` preserves these exact values:

```text
validation_input_gate_required: paper_mapped_subset_primitivespec_validation_contract
unique_row_ids_required: true
complete_source_evidence_ids_required: true
zero_current_generation_candidates_required: true
zero_generated_primitivespecs_required: true
zero_runtime_admissibility_checks_required: true
allowed_future_mapping_candidate_labels: ["box", "sphere", "capsule"]
required_primitive_spec_fields:
  ["primitive_id", "kind", "center", "axes", "dimensions", "frame", "source_faces",
   "contains_assigned_points", "volume", "weighted_volume", "conversion_status"]
expected_requirement_row_count: 6
expected_current_row_count: 16
primitive_spec_generation_allowed: false
collision_package_generation_allowed: false
newton_runtime_allowed: false
runtime_admissibility_supported: false
approximation_policy_enabled: false
silent_drop_allowed: false
```

- coverage summary has 6 family rows, 3 future native rows, 2 blocked rows, 1 no-op row, 16
  current rows, zero current pass records, 16 current no-op records, zero candidate records, and
  zero generated PrimitiveSpec records;
- family rows preserve this exact order:
  `oriented_bounding_box`, `sphere`, `capsule`, `capped_cylinder`, `frustum`,
  `trapezoidal_prism`;
- all source trace ids are non-empty;
- emitted row ids are unique.

## Native Family Template Rows

The generation contract should emit one template row for each future native family:

| Paper primitive | Template kind |
| --- | --- |
| `oriented_bounding_box` | `box` |
| `sphere` | `sphere` |
| `capsule` | `capsule` |

Each template row records the required PrimitiveSpec field names from the dry-run/validation chain,
but it must not claim to be a runtime PrimitiveSpec instance.

Required fields:

```text
primitive_spec_generation_template_row_id
source_primitivespec_generation_preflight_row_id
source_primitivespec_validation_row_id
source_primitivespec_dry_run_row_id
source_adapter_preflight_row_id
source_candidate_matrix_row_id
source_conversion_plan_row_id
paper_primitive
primitive_spec_kind
candidate_mapping_label
input_primitivespec_generation_preflight_decision
required_primitive_spec_fields
template_only
runtime_instance_generated
primitive_spec_generation_candidate
generated_primitive_spec
silent_drop_detected
primitive_spec_generation_decision
required_current_candidate_source_gate
```

The generation decision for these rows is:

```text
native_family_primitivespec_template_generated_offline_only
```

`input_primitivespec_generation_preflight_decision` must be
`future_native_family_generation_requirement_preflighted`. `template_only` must be true.
`runtime_instance_generated`, `primitive_spec_generation_candidate`, and `silent_drop_detected`
must be false. `generated_primitive_spec` must be null.
`required_current_candidate_source_gate` must be
`paper_mapped_subset_primitivespec_candidate_source_contract`.

Every template row must also carry the established row-level false flags:

```text
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

## Blocked And No-Op Requirement Rows

Capped cylinder and frustum remain blocked:

```text
blocked_approximation_policy_before_primitivespec_generation
```

Trapezoidal prism remains no-op/unmapped:

```text
noop_unmapped_family_before_primitivespec_generation
```

These rows keep their source trace ids and point to
`paper_mapped_subset_primitivespec_candidate_source_contract` as the required later gate.

Blocked and no-op requirement rows must use this exact schema:

```text
primitive_spec_generation_requirement_row_id
source_primitivespec_generation_preflight_row_id
source_primitivespec_validation_row_id
source_primitivespec_dry_run_row_id
source_adapter_preflight_row_id
source_candidate_matrix_row_id
source_conversion_plan_row_id
paper_primitive
candidate_mapping_label
input_primitivespec_generation_preflight_decision
primitive_spec_generation_decision
primitive_spec_generation_action
primitive_spec_generation_candidate
generated_primitive_spec
required_later_gate
required_future_policy
```

Blocked rows must keep:

```text
primitive_spec_generation_action: require_explicit_approximation_policy
primitive_spec_generation_candidate: false
generated_primitive_spec: null
required_future_policy: approximation_policy
```

The no-op trapezoidal-prism row must keep:

```text
primitive_spec_generation_action: keep_unmapped_family_offline
primitive_spec_generation_candidate: false
generated_primitive_spec: null
required_future_policy: mapped_current_candidate_source
```

Every blocked or no-op requirement row must also carry the same row-level false flags as the
native-family template rows.

## Current Row Generation Rows

The 16 current rows remain no-generation rows. Each row records:

```text
primitive_spec_generation_row_id
source_primitivespec_generation_preflight_row_id
source_primitivespec_validation_row_id
source_primitivespec_dry_run_row_id
source_adapter_preflight_row_id
source_candidate_matrix_row_id
source_conversion_plan_row_id
source_policy_decision_id
source_adapter_decision_id
source_output_id
evidence_case_id
offline_primitive_id
paper_primitive
offline_mapping_label
primitive_spec_generation_decision
primitive_spec_generation_action
primitive_spec_generation_candidate
generated_primitive_spec
silent_drop_detected
required_later_gate
required_future_policy
```

The generation decision is:

```text
skip_unmapped_current_row_no_primitivespec_generated
```

The action is:

```text
keep_offline_until_mapped_current_candidate_exists
```

Every current row must keep `primitive_spec_generation_candidate: false`,
`generated_primitive_spec: null`, and `silent_drop_detected: false`.

Every current row must also carry the same row-level false flags as the native-family template
rows.

## Coverage Summary

The generation payload must emit these exact coverage keys and expected values:

| Key | Expected |
| --- | --- |
| `primitive_spec_generation_requirement_row_count` | `6` |
| `native_family_primitivespec_template_row_count` | `3` |
| `blocked_primitivespec_generation_requirement_row_count` | `2` |
| `noop_primitivespec_generation_requirement_row_count` | `1` |
| `current_row_primitivespec_generation_row_count` | `16` |
| `current_primitivespec_generation_pass_record_count` | `0` |
| `primitive_spec_generation_candidate_record_count` | `0` |
| `offline_primitivespec_template_record_count` | `3` |
| `generated_primitive_spec_record_count` | `0` |
| `generated_collision_package_record_count` | `0` |
| `runtime_admissibility_check_record_count` | `0` |
| `current_primitivespec_generation_noop_record_count` | `16` |
| `current_paper_primitive_distribution` | `{"trapezoidal_prism": 16}` |
| `current_mapping_label_distribution` | `{"offline_only_unmapped": 16}` |

The payload-level counts must match the coverage summary:

```text
primitive_spec_generation_candidate_count == 0
offline_primitivespec_template_count == 3
generated_primitive_spec_count == 0
generated_collision_package_count == 0
runtime_admissibility_check_count == 0
```

## Rejection Labels

Tests must lock these `ValueError` labels:

| Rejection | Label |
| --- | --- |
| wrong input gate id | `primitivespec_generation_input_gate_id_mismatch` |
| stale input next gate | `primitivespec_generation_input_next_gate_mismatch` |
| true payload/input trigger flag | `primitivespec_generation_input_trigger_flag_true:<field>` |
| nonzero generation-preflight candidate count | `primitivespec_generation_input_candidate_count_nonzero` |
| nonzero generated PrimitiveSpec count | `primitivespec_generation_input_generated_spec_nonzero` |
| nonzero generated CollisionPackage count | `primitivespec_generation_input_generated_collision_package_nonzero` |
| nonzero runtime-admissibility count | `primitivespec_generation_input_runtime_admissibility_nonzero` |
| nested preflight contract drift | `primitivespec_generation_input_contract_mismatch:<field>` |
| coverage count mismatch | `primitivespec_generation_coverage_count_mismatch:<field>` |
| family order mismatch | `primitivespec_generation_family_primitive_sequence_mismatch` |
| future native family semantic drift | `primitivespec_generation_future_family_contract_mismatch:<paper_primitive>` |
| blocked/no-op family semantic drift | `primitivespec_generation_family_contract_mismatch:<paper_primitive>` |
| missing family source id | `primitivespec_generation_missing_preflight_row_id:<field>` |
| missing current-row source id | `primitivespec_generation_missing_current_row_source_id:<field>` |
| unknown family decision | `unknown_primitivespec_generation_preflight_family_decision:<decision>` |
| unknown current decision | `unknown_primitivespec_generation_preflight_current_decision:<decision>` |
| native template candidate or generated-object leak | `primitivespec_generation_template_runtime_leak:<field>` |
| native template candidate-source gate mismatch | `primitivespec_generation_template_required_current_candidate_source_gate_mismatch` |
| blocked/no-op required-later-gate mismatch | `primitivespec_generation_requirement_required_later_gate_mismatch` |
| current row candidate leak | `primitivespec_generation_current_row_candidate_nonzero` |
| current row generated PrimitiveSpec leak | `primitivespec_generation_current_row_generated_spec_nonzero` |
| current row silent drop leak | `primitivespec_generation_current_row_silent_drop_detected` |
| current row required-later-gate mismatch | `primitivespec_generation_current_row_required_later_gate_mismatch` |
| emitted row id duplicate | `duplicate_primitivespec_generation_row_id` |

## Report Integration

`build_cpd_paper_offline_report()` should:

- build the new generation payload from the generation-preflight payload;
- include it under `paper_mapped_subset_primitivespec_generation_contract`;
- add `_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT` to
  `paper_faithfulness.implemented_output_contract_scope`;
- update `failure_labels`, `next_required_gate`, and
  `paper_faithfulness.missing_before_paper_faithful_offline` to
  `paper_mapped_subset_primitivespec_candidate_source_contract`;
- keep the top-level report `status: partial`;
- keep top-level `paper_faithful_offline_supported: false`;
- keep top-level package/Newton/real-USD/benchmark trigger flags false;
- keep any top-level collision-quality, deployment, certification, or safety evidence flags false
  if such fields are present in the report;
- keep validation and generation-preflight nested payload transitions unchanged.

## Tests

Add TDD coverage in `tests/test_cpd_paper_offline.py` before implementation:

- report records the generation contract and advances the top-level next gate;
- top-level report remains `status: partial` with
  `paper_faithful_offline_supported: false`;
- payload emits 3 native template rows and no runtime PrimitiveSpec instances;
- capped cylinder/frustum blocked rows and trapezoidal-prism no-op row are present;
- 16 current rows remain no-generation/offline;
- `paper_faithful_offline_allowed`, `package_generation_allowed`, and
  `primitive_spec_generation_candidate_count` remain false or zero;
- report-only false flags hold at payload, top-level report, and row levels;
- malformed input gate, stale input next gate, nonzero counts, coverage mismatch, family
  semantics drift, source-id gaps, row-level true trigger flags, current row generation leaks, and
  duplicate emitted row ids raise stable `ValueError` labels.

Add CLI coverage in `tests/test_cli.py`:

- top-level `next_required_gate` is
  `paper_mapped_subset_primitivespec_candidate_source_contract`;
- generation-preflight payload still points to
  `paper_mapped_subset_primitivespec_generation_contract`;
- generation payload exists and records 3 template rows, 16 no-generation current rows, zero real
  generated PrimitiveSpec records, zero package records, zero runtime checks, and false trigger
  flags.

## Documentation

After implementation, update:

- `README.md`;
- `docs/index.md`;
- `docs/deepdive/evidence-status.md`;
- `docs/deepdive/message-map.md` if a new unsafe wording boundary is needed;
- `docs/reference/claim-boundaries.md`;
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`;
- `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`;
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`;
- `docs/reference/cpd-paper-story-status.md`;
- `docs/records/README.md`;
- `experiments/registry.yaml`;
- a new dated record:
  `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-generation-contract.md`.

## Claim Boundary

Allowed wording:

```text
The report now includes an offline PrimitiveSpec generation contract that emits native-family
template rows and records that no current runtime PrimitiveSpec can be generated until mapped
current candidates exist.
```

Forbidden wording:

```text
The system now generates real PrimitiveSpecs.
The system can generate CollisionPackages from the paper lane.
The paper-lane output is Newton-ready.
The mapped subset improves collision quality.
This supports benchmark, real-USD, deployment, or safety claims.
```

## Verification

Required before merge:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k 'primitivespec_generation or primitivespec_generation_preflight or offline_report_covers_first_toy_slice' -q
python -m pytest tests/test_cli.py -k cpd_paper_offline -q
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
python -m pytest -q
```

## Self-Review

- No placeholder text remains.
- The selected design is one slice, not a broad package-generation or Newton-runtime feature.
- The generation contract closes only the named offline gate.
- The new next gate names the real blocker: mapped current candidate sourcing.
- The design preserves claim boundaries and does not assert real PrimitiveSpec, CollisionPackage,
  Newton, benchmark, real-USD, collision-quality, deployment, or safety support.
