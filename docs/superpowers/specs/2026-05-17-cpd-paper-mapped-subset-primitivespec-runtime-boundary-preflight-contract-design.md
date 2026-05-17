# CPD Paper Mapped-Subset PrimitiveSpec Runtime-Boundary Preflight Contract Design

## Purpose

Close `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract` as the next
command-only offline CPD paper-lane gate.

This slice consumes `paper_mapped_subset_primitivespec_native_fixture_serialization_contract` and
defines the report-side boundary for whether a later runtime `PrimitiveSpec` construction contract
may be proposed for the deterministic synthetic `paper_single_box` OBB/box row.

## Boundary

This gate is a preflight boundary only. It must not:

- instantiate a runtime `PrimitiveSpec`;
- create or modify a `CollisionPackage`;
- perform runtime-admissibility checks;
- call Newton;
- load real USD assets;
- run benchmarks;
- report collision quality, deployment readiness, safety certification, full CPD reproduction, or
  `paper_faithful_offline` support.

The existing false flag `primitive_spec_generated` remains false because it means runtime
PrimitiveSpec generation in this report family. This gate can mark one report row as a candidate
for a later runtime-construction contract, but the current gate still creates zero runtime objects.

## Input Contract

The input payload must satisfy:

- `gate_id == paper_mapped_subset_primitivespec_native_fixture_serialization_contract`;
- `next_required_gate == paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`;
- exactly one `serialization_rows` entry;
- `serialized_primitivespec_like_dict_count == 1`;
- `json_serialization_check_count == 1`;
- `json_round_trip_match_count == 1`;
- `schema_stability_check_count == 1`;
- `generated_runtime_primitive_spec_count == 0`;
- `generated_primitive_spec_count == 0`;
- `generated_collision_package_count == 0`;
- `runtime_admissibility_check_count == 0`;
- all package/Newton/real-USD/benchmark/collision/deployment flags remain false.

The one serialization row must be for:

- `fixture_id == paper_single_box`;
- `paper_primitive == oriented_bounding_box`;
- `primitive_spec_kind == box`;
- `candidate_mapping_label == box`;
- `newton_runtime_kind == box`;
- `kind == box`;
- `schema_validation_status == passed`;
- `json_round_trip_equal is True`;
- `canonical_json_stable is True`;
- `serialized_payload` is a dict;
- `schema_keys` equals the sorted serialized payload keys;
- `generated_primitive_spec is None`;
- `runtime_instance_generated is False`.

Any input runtime/package/Newton/real-USD/benchmark/collision/deployment trigger must raise a
runtime-boundary-specific error.

The implementation must also avoid runtime/package/Newton code paths directly. This gate may not
import or instantiate `PrimitiveSpec`, import or create `CollisionPackage`, or import/call Newton
modules inside the new runtime-boundary helper path. Tests should include a static guard for this
helper block, in addition to report-output false flags.

## Boundary Decision

The gate records one preflight row. The row says that a later runtime-construction contract may be
proposed only because all of the following report-only inputs are true:

- the source row is the deterministic synthetic `paper_single_box` fixture;
- the mapped subset is `oriented_bounding_box -> box`;
- the serialized payload has the expected PrimitiveSpec-like schema;
- canonical JSON is strict and round-trips to the same dict;
- the serialization row still has zero runtime object, package, Newton, USD, benchmark, and
  collision-quality evidence.

The gate does not decide that runtime construction is already supported. It sets:

- `later_runtime_primitivespec_construction_candidate_count: 1`;
- `runtime_construction_allowed_in_current_gate: False`;
- `generated_runtime_primitive_spec_count: 0`;
- `generated_primitive_spec_count: 0`;
- `generated_collision_package_count: 0`;
- `runtime_admissibility_check_count: 0`.

## Output Payload

The new payload key is:

`paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`

Top-level required fields:

- `gate_id`, `closed_gate`, `input_gate_id`, `next_required_gate`;
- `gate_status`, `decision`, `decision_reason`;
- `artifact_kind`, `implementation_boundary`, `source_scope`, `schema_version`;
- `runtime_boundary_action`;
- `runtime_boundary_requirements`;
- `runtime_boundary_preflight_row_count`;
- `later_runtime_primitivespec_construction_candidate_count`;
- `runtime_construction_allowed_in_current_gate`;
- `generated_runtime_primitive_spec_count`;
- `generated_primitive_spec_count`;
- `generated_collision_package_count`;
- `runtime_admissibility_check_count`;
- `runtime_boundary_preflight_contract`;
- `input_contract_summary`;
- `runtime_boundary_preflight_rows`;
- `coverage_summary`;
- `remaining_gaps`;
- false runtime/package/evaluation flags.

The next gate after this slice is:

`paper_mapped_subset_primitivespec_runtime_construction_contract`

That next gate is where any real runtime object proposal must be handled. This preflight gate only
defines the handoff conditions and keeps the report partial.

## Output Row

The single row must carry source lineage and boundary evidence:

- `runtime_boundary_preflight_row_id`;
- `source_native_fixture_primitivespec_serialization_row_id`;
- `source_native_fixture_primitivespec_generation_row_id`;
- source ids inherited from the serialization row;
- `fixture_id`, `paper_primitive`, `primitive_spec_kind`, `candidate_mapping_label`,
  `newton_runtime_kind`;
- `primitive_id`, `kind`, `serialized_payload_schema_keys`;
- `canonical_primitivespec_json`;
- `input_json_round_trip_equal`, `input_canonical_json_stable`,
  `input_schema_validation_status`;
- `later_runtime_primitivespec_construction_candidate`;
- `runtime_construction_allowed_in_current_gate`;
- `required_later_gate`;
- `preflight_decision`;
- `preflight_reason`;
- `runtime_instance_generated is False`;
- `generated_primitive_spec is None`;
- package/runtime trigger flags false.

## Failure Labels

Use these labels for malformed inputs:

- `primitivespec_runtime_boundary_preflight_input_gate_id_mismatch`;
- `primitivespec_runtime_boundary_preflight_input_next_gate_mismatch`;
- `primitivespec_runtime_boundary_preflight_serialization_row_count_mismatch`;
- `primitivespec_runtime_boundary_preflight_source_fixture_mismatch`;
- `primitivespec_runtime_boundary_preflight_source_kind_mismatch`;
- `primitivespec_runtime_boundary_preflight_serialized_payload_missing`;
- `primitivespec_runtime_boundary_preflight_serialized_payload_schema_mismatch`;
- `primitivespec_runtime_boundary_preflight_canonical_json_mismatch`;
- `primitivespec_runtime_boundary_preflight_json_round_trip_missing`;
- `primitivespec_runtime_boundary_preflight_schema_validation_missing`;
- `primitivespec_runtime_boundary_preflight_runtime_object_leak:<field>`;
- `primitivespec_runtime_boundary_preflight_input_count_mismatch:<field>`;
- `primitivespec_runtime_boundary_preflight_input_trigger_flag_true:<flag>`.

After this gate, the top-level missing label is:

`paper_mapped_subset_primitivespec_runtime_construction_contract_missing`

## Tests

Use TDD. Add RED tests before production code:

- gate/top-level status and next gate;
- exact payload schema;
- exact row schema;
- input lineage from serialization to runtime-boundary row;
- static guard that the new helper block does not instantiate/import `PrimitiveSpec`, create/import
  `CollisionPackage`, or import/call Newton modules;
- report-only boundary flags and forbidden runtime/package/Newton/evaluation keys;
- malformed input gate, next gate, row count, fixture/kind drift, missing serialized payload,
  missing JSON/schema checks, canonical JSON drift, row-level runtime object leaks, count drift, and
  trigger-flag leaks;
- CLI report assertions for the new nested payload.

## Documentation

Update durable CPD paper story docs and registry with safe wording:

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
- a dated record under `docs/records/`.

Use only preflight-boundary wording. Do not describe this gate as PrimitiveSpec readiness,
package readiness, package conversion, runtime admissibility, Newton support, real-USD evidence,
benchmark evidence, collision-quality evidence, deployment readiness, safety certification, full
CPD reproduction, or `paper_faithful_offline` support.
