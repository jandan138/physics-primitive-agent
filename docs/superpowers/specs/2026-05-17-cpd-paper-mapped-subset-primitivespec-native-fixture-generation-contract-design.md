# CPD Paper Mapped-Subset PrimitiveSpec Native Fixture Generation Contract Design

## Purpose

Close `paper_mapped_subset_primitivespec_native_fixture_generation_contract` as the next
command-only offline CPD paper-lane gate.

The slice consumes `paper_mapped_subset_native_current_fixture_contract` and emits exactly one
serialized, report-only PrimitiveSpec-like dictionary for the deterministic synthetic
`paper_single_box` selected OBB/box source row.

## Boundary

This is not runtime `PrimitiveSpec` object creation, not `CollisionPackage` generation, not runtime
admissibility, not Newton execution, not real-USD evidence, not benchmark evidence, not collision
quality evidence, not deployment readiness, not safety certification, and not full CPD
reproduction.

The artifact must use explicit offline wording:

- `offline_serialized_primitivespec_like_dict_count: 1`
- `generated_runtime_primitive_spec_count: 0`
- `generated_collision_package_count: 0`
- `runtime_admissibility_check_count: 0`
- all package/Newton/real-USD/benchmark/collision/deployment flags remain false

The existing false flag `primitive_spec_generated` remains false because it means runtime
PrimitiveSpec generation in this report family. The new artifact is counted separately as an
offline serialized PrimitiveSpec-like dictionary.

## Input Contract

The input payload must satisfy:

- `gate_id == paper_mapped_subset_native_current_fixture_contract`
- `next_required_gate == paper_mapped_subset_primitivespec_native_fixture_generation_contract`
- exactly one `native_current_fixture_source_rows` entry
- top-level counts:
  - eligible current candidate sources: 1
  - PrimitiveSpec generation candidates: 1
  - generated runtime PrimitiveSpecs: 0
  - generated CollisionPackages: 0
  - runtime-admissibility checks: 0
- the one source row must be:
  - `fixture_id == paper_single_box`
  - `paper_primitive == oriented_bounding_box`
  - `primitive_spec_kind == box`
  - `candidate_mapping_label == box`
  - `newton_runtime_kind == box`
  - `eligible_current_candidate_source is True`
  - `primitive_spec_generation_candidate is True`
  - `generated_primitive_spec is None`

Any input runtime/package/Newton/real-USD/benchmark/collision/deployment trigger must raise a
native-fixture-generation-specific error.

## Output Payload

The new payload key is:

`paper_mapped_subset_primitivespec_native_fixture_generation_contract`

Top-level required fields follow the existing gate style:

- `gate_id`, `closed_gate`, `input_gate_id`, `next_required_gate`
- `gate_status`, `decision`, `decision_reason`
- `artifact_kind`, `implementation_boundary`, `source_scope`, `schema_version`
- `native_fixture_primitivespec_generation_action`
- `primitive_spec_generation_candidate_count`
- `offline_serialized_primitivespec_like_dict_count`
- `generated_runtime_primitive_spec_count`
- `generated_primitive_spec_count`
- `generated_collision_package_count`
- `runtime_admissibility_check_count`
- `native_fixture_primitivespec_generation_contract`
- `input_contract_summary`
- `native_fixture_primitivespec_generation_rows`
- `coverage_summary`
- `remaining_gaps`
- false runtime/package/evaluation flags

`generated_primitive_spec_count` remains zero to preserve the existing runtime-generation
semantics. `offline_serialized_primitivespec_like_dict_count` is the count that becomes one.

## Output Row

The single row must carry source lineage and the generated offline dict:

- `native_fixture_primitivespec_generation_row_id`
- `source_native_current_fixture_source_row_id`
- source ids inherited from the source row
- `fixture_id`, `fixture_source_faces`
- `paper_primitive`, `primitive_spec_kind`, `candidate_mapping_label`, `newton_runtime_kind`
- `generation_decision == report_only_serialized_primitivespec_like_dict_generated`
- `generation_action == emit_offline_serialized_dict_only`
- `primitive_spec_generation_candidate is True`
- `offline_serialized_primitivespec_like_dict`
- `runtime_instance_generated is False`
- `generated_primitive_spec is None`
- package/runtime trigger flags false
- geometry copied from the source row
- `required_later_gate == paper_mapped_subset_primitivespec_native_fixture_serialization_contract`
- `required_future_policy == report_only_primitivespec_payload_serialization_contract`

The generated dictionary mirrors `PrimitiveSpec.to_dict()` shape without instantiating
`PrimitiveSpec`:

- `primitive_id`
- `kind`
- `pose`
- `center`
- `axes`
- `dimensions`
- `frame`
- `source_faces`
- `contains_assigned_points`
- `volume`
- `weighted_volume`
- `conversion_status`

The deterministic primitive id is `paper_single_box__oriented_bounding_box__box`. `pose` is an
empty list, `frame` is `asset`, and `dimensions == {"half_extents": source_half_extents}`.

## Next Gate

After this slice, the next missing gate is:

`paper_mapped_subset_primitivespec_native_fixture_serialization_contract`

That later gate should validate report serialization and schema stability before package adapter
or runtime-admissibility wording enters the path.

## Tests

Use TDD. Add RED tests before production code:

- gate/top-level status and next gate
- exact payload schema
- one generated offline box dict matching the source row
- exact coverage summary
- report-only boundary flags
- malformed input gate, next gate, row count, source eligibility/candidate, stale generated spec,
  kind/runtime drift, invalid geometry, empty source faces, and trigger-flag leaks
- CLI report assertions for the new payload

## Documentation

Update the durable CPD paper story docs and registry with safe wording:

- `README.md`
- `docs/index.md`
- `docs/deepdive/evidence-status.md`
- `docs/deepdive/message-map.md`
- `docs/reference/claim-boundaries.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/records/README.md`
- `experiments/registry.yaml`
- a dated record under `docs/records/`

