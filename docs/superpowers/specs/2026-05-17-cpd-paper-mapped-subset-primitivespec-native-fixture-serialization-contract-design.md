# CPD Paper Mapped-Subset PrimitiveSpec Native-Fixture Serialization Contract Design

## Purpose

Close `paper_mapped_subset_primitivespec_native_fixture_serialization_contract` as the next
command-only offline CPD paper-lane gate.

This slice consumes `paper_mapped_subset_primitivespec_native_fixture_generation_contract` and
verifies serialization/schema stability for exactly one report-only PrimitiveSpec-like dictionary
for the deterministic synthetic `paper_single_box` OBB/box source row.

## Boundary

This gate is a verifier/echo contract only. It must not:

- instantiate a runtime `PrimitiveSpec`;
- create or modify a `CollisionPackage`;
- perform runtime-admissibility checks;
- call Newton;
- load real USD assets;
- run benchmarks;
- report collision quality, deployment readiness, safety certification, or full CPD reproduction.

The existing false flag `primitive_spec_generated` remains false because it means runtime
PrimitiveSpec generation in this report family. This gate validates a serialized report artifact
only.

## Input Contract

The input payload must satisfy:

- `gate_id == paper_mapped_subset_primitivespec_native_fixture_generation_contract`;
- `next_required_gate == paper_mapped_subset_primitivespec_native_fixture_serialization_contract`;
- exactly one `native_fixture_primitivespec_generation_rows` entry;
- `offline_serialized_primitivespec_like_dict_count == 1`;
- `generated_runtime_primitive_spec_count == 0`;
- `generated_primitive_spec_count == 0`;
- `generated_collision_package_count == 0`;
- `runtime_admissibility_check_count == 0`;
- all package/Newton/real-USD/benchmark/collision/deployment flags remain false.

The one generation row must be for:

- `fixture_id == paper_single_box`;
- `paper_primitive == oriented_bounding_box`;
- `primitive_spec_kind == box`;
- `candidate_mapping_label == box`;
- `newton_runtime_kind == box`;
- `offline_serialized_primitivespec_like_dict` is a dict;
- `generated_primitive_spec is None`;
- `runtime_instance_generated is False`.

Any input runtime/package/Newton/real-USD/benchmark/collision/deployment trigger must raise a
serialization-specific error.

## Serialized Dict Contract

The report-only dict must have exactly these keys:

- `primitive_id`;
- `kind`;
- `pose`;
- `center`;
- `axes`;
- `dimensions`;
- `frame`;
- `source_faces`;
- `contains_assigned_points`;
- `volume`;
- `weighted_volume`;
- `conversion_status`.

It must also satisfy:

- `primitive_id == paper_single_box__oriented_bounding_box__box`;
- `kind == box`;
- `pose == []`;
- `dimensions == {"half_extents": [...]}`;
- `frame == asset`;
- `conversion_status == report_only_offline_serialized_primitivespec_like_dict_not_runtime_object`;
- numeric fields are strict JSON values with no NaN or Infinity.

## Canonical JSON Policy

The canonical JSON string is:

```python
json.dumps(spec, allow_nan=False, sort_keys=True, separators=(",", ":"))
```

The contract must record:

- `json_allow_nan: False`;
- `json_sort_keys: True`;
- `json_separators: [",", ":"]`;
- `json_round_trip_equal: True`;
- `canonical_json_stable: True`.

The round-trip check is:

```python
json.loads(canonical_json) == spec
```

The same report built twice must produce the same canonical JSON string for this row.

## Output Payload

The new payload key is:

`paper_mapped_subset_primitivespec_native_fixture_serialization_contract`

Top-level required fields:

- `gate_id`, `closed_gate`, `input_gate_id`, `next_required_gate`;
- `gate_status`, `decision`, `decision_reason`;
- `artifact_kind`, `implementation_boundary`, `source_scope`, `schema_version`;
- `serialization_action`;
- `canonical_json_policy`;
- `serialized_primitivespec_like_dict_count`;
- `json_serialization_check_count`;
- `json_round_trip_match_count`;
- `schema_stability_check_count`;
- `generated_runtime_primitive_spec_count`;
- `generated_primitive_spec_count`;
- `generated_collision_package_count`;
- `runtime_admissibility_check_count`;
- `native_fixture_primitivespec_serialization_contract`;
- `input_contract_summary`;
- `serialization_rows`;
- `coverage_summary`;
- `remaining_gaps`;
- false runtime/package/evaluation flags.

The next gate after this slice is:

`paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`

That next gate is still a command-only preflight. It should define the boundary for whether any
later runtime PrimitiveSpec construction may be proposed, without creating a runtime object yet.

## Output Row

The single row must carry source lineage and serialization evidence:

- `native_fixture_primitivespec_serialization_row_id`;
- `source_native_fixture_primitivespec_generation_row_id`;
- source ids inherited from the generation row;
- `fixture_id`, `paper_primitive`, `primitive_spec_kind`, `candidate_mapping_label`,
  `newton_runtime_kind`;
- `primitive_id`, `kind`, `schema_keys`;
- `serialized_payload`;
- `canonical_primitivespec_json`;
- `json_allow_nan`, `json_sort_keys`, `json_separators`;
- `json_round_trip_equal`, `canonical_json_stable`;
- `schema_validation_status`;
- `serialization_decision`;
- `runtime_instance_generated is False`;
- `generated_primitive_spec is None`;
- package/runtime trigger flags false.

## Failure Labels

Use these labels for malformed inputs:

- `primitivespec_native_fixture_serialization_input_gate_id_mismatch`;
- `primitivespec_native_fixture_serialization_input_next_gate_mismatch`;
- `primitivespec_native_fixture_serialization_generation_row_count_mismatch`;
- `primitivespec_native_fixture_serialization_source_fixture_mismatch`;
- `primitivespec_native_fixture_serialization_source_kind_mismatch`;
- `primitivespec_native_fixture_serialization_missing_payload`;
- `primitivespec_native_fixture_serialization_payload_schema_mismatch`;
- `primitivespec_native_fixture_serialization_payload_field_drift`;
- `primitivespec_native_fixture_serialization_non_strict_json`;
- `primitivespec_native_fixture_serialization_round_trip_mismatch`;
- `primitivespec_native_fixture_serialization_input_trigger_flag_true:<flag>`.

After this gate, the top-level missing label is:

`paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract_missing`

## Tests

Use TDD. Add RED tests before production code:

- gate/top-level status and next gate;
- exact payload schema;
- exact row schema;
- deterministic canonical JSON;
- JSON round-trip equality;
- preservation of the exact report-only dict payload;
- malformed input gate, next gate, row count, fixture/kind drift, malformed dict payload, and
  trigger-flag leaks;
- report-only boundary flags and forbidden runtime/package/Newton/evaluation keys;
- CLI report assertions for the new nested payload and canonical JSON stability.

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

Use only report-only serialization/schema-stability wording. Do not describe this gate as
PrimitiveSpec readiness, package readiness, package conversion, runtime admissibility, Newton
support, real-USD evidence, benchmark evidence, collision-quality evidence, deployment readiness,
safety certification, or full CPD reproduction.
