# CPD Paper Mapped-Subset Newton Shape Runtime-Construction Contract Design

## Summary

Implement the next bounded CPD paper runtime-lane gate:
`paper_mapped_subset_newton_shape_runtime_construction_contract`.

The existing chain already names this gate as "runtime construction", but the implementation must
define that phrase narrowly: this slice constructs exactly one repo-local, JSON-safe
`NewtonShapeMapping.to_dict()` record from the static descriptor for the deterministic synthetic
`paper_single_box` OBB/box artifact.

It does not construct a Newton engine shape, does not import Newton or warp, does not call a
Newton builder, does not run contact/drop/sphere-rain diagnostics, does not load real USD, does
not run a benchmark, and does not measure collision quality.

## Why This Slice Exists

The previous gate checked that one static descriptor is ready to approach a runtime boundary:

```text
shape-mapping descriptor
-> runtime-boundary preflight row
-> later runtime-construction candidate
```

That row still kept every construction counter at zero. The next useful step is to prove the
descriptor can be turned into the repository's runtime-facing shape mapping record type without
jumping into Newton engine execution.

In plain terms:

- previous slice: "the static descriptor passed a boundary preflight";
- this slice: "the descriptor can become one `NewtonShapeMapping.to_dict()` report record";
- later slice: "decide whether that mapping record may approach a Newton import/builder boundary."

## Design Choice

Use repo-local `NewtonShapeMapping` construction, not a Newton builder call.

Rejected alternatives:

- Construct a real Newton/warp builder shape now. That would introduce environment-dependent
  Newton imports into `cpd_paper_offline_report` and would mix shape record construction with
  engine runtime entry.
- Rename the existing gate to a schema-only gate. That wording would be cleaner, but the previous
  committed report chain already points to
  `paper_mapped_subset_newton_shape_runtime_construction_contract`. This spec instead makes the
  gate's limited meaning explicit.
- Keep this gate as another static preflight. The previous slice already did that, so it would not
  reduce the current gap.
- Generalize beyond `paper_single_box`. The current mapped subset has one eligible construction
  candidate, and broadening would create unearned support claims.

Recommended approach:

- Add one payload under `cpd_paper_offline_report`:
  `paper_mapped_subset_newton_shape_runtime_construction_contract`.
- Validate that the input preflight payload is exactly the one-row `paper_single_box` box gate.
- Locally import `NewtonShapeMapping` inside the construction helper.
- Construct exactly one `NewtonShapeMapping(...)` object from descriptor center, axes, half
  extents, primitive id, and target kind.
- Store only `constructed_newton_shape_mapping_dict = mapping.to_dict()` in the report.
- Record `constructed_newton_shape_mapping_record_count: 1` and
  `newton_mapping_record_count: 1`.
- Keep generic mapper-call, Newton engine shape, builder, and runtime counters at zero.
- Advance the top-level next gate to
  `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`.

## Terminology

This design uses strict terms:

- `NewtonShapeMapping`: repo-local Python dataclass in
  `primitive_collision_compiler.reports.schema`. It is JSON-serializable report data used by
  runtime diagnostics.
- `Newton engine shape`: an object/index created by Newton/warp builder calls such as
  `builder.add_shape_box`. This slice must not create one.
- `Newton runtime execution`: contact, collide, model finalize, drop/settle, sphere-rain, timing,
  or benchmark execution. This slice must not do any of these.

The existing `newton_shape_object_count` field remains reserved for real Newton engine/builder
shape evidence. `newton_mapping_record_count` counts JSON-safe `NewtonShapeMapping.to_dict()`
records. Generic mapper execution remains separate:

- `constructed_newton_shape_mapping_record_count: 1`
- `newton_mapping_record_count: 1`
- `newton_mapper_call_count: 0`
- `newton_shape_object_count: 0`
- `newton_engine_shape_object_count: 0`
- `newton_builder_shape_call_count: 0`
- `newton_runtime_execution_count: 0`

## Payload Contract

The new payload must include:

- `gate_id: paper_mapped_subset_newton_shape_runtime_construction_contract`
- `gate_status: implemented_single_fixture_newton_shape_mapping_record_construction_contract_only_partial`
- `closed_gate: paper_mapped_subset_newton_shape_runtime_construction_contract`
- `input_gate_id: paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`
- `next_required_gate: paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`
- `decision: remain_partial`
- `decision_reason:
  newton_shape_mapping_record_construction_complete_newton_shape_runtime_builder_preflight_missing`
- `artifact_kind:
  repo_local_newton_shape_mapping_to_dict_not_newton_engine_shape`
- `schema_version: 1`
- `source_scope: synthetic_toy_fixtures_only`
- `implementation_boundary:
  single_synthetic_box_newton_shape_mapping_record_only_no_newton_engine_shape_no_runtime_no_real_usd_no_benchmark_no_metrics`
- `runtime_construction_action:
  construct_one_repo_local_newton_shape_mapping_from_static_descriptor_without_newton_import`
- `newton_shape_runtime_construction_contract`, a nested contract summary with input gate,
  closed gate, next runtime-builder preflight gate, required row count, required
  `NewtonShapeMapping.to_dict()` record count, and false engine/runtime permissions
- `input_contract_summary`, with input gate id, input next gate, source preflight row id, source
  shape-mapping row id, source package id, fixture id, primitive id, target kind, descriptor kind,
  and input construction candidate count
- `newton_shape_runtime_construction_row_count: 1`
- `source_newton_shape_runtime_boundary_preflight_row_count: 1`
- `constructed_newton_shape_mapping_record_count: 1`
- `newton_mapping_record_count: 1`
- `newton_mapper_call_count: 0`
- `newton_shape_object_count: 0`
- `newton_engine_shape_object_count: 0`
- `newton_builder_shape_call_count: 0`
- `newton_runtime_execution_count: 0`
- carried-forward completed-gate counters:
  `generated_runtime_primitive_spec_count: 1`, `generated_primitive_spec_count: 1`,
  `generated_collision_package_count: 1`, `runtime_admissibility_check_count: 1`,
  `offline_static_runtime_admissibility_check_count: 1`,
  `report_scoped_newton_shape_descriptor_count: 1`, and
  `later_newton_shape_runtime_construction_candidate_count: 1`
- `newton_shape_runtime_construction_rows: [...]`
- `coverage_summary`
- `remaining_gaps: [paper_mapped_subset_newton_shape_runtime_builder_preflight_contract]`

The payload and each row must keep these claim/runtime boundary flags false:

- `paper_faithful_offline_allowed`
- `paper_faithful_offline_supported`
- `newton_support_claimed`
- `approximation_policy_applied`
- `real_usd_loaded`
- `benchmark_run`
- `collision_quality_measured`
- `deployment_or_certification_claimed`
- `package_generation_triggered`
- `newton_runtime_triggered`
- `real_usd_triggered`
- `benchmark_triggered`
- `newton_runtime_allowed`
- `approximation_policy_enabled`
- `silent_drop_allowed`
- `mapping_attempted`
- `newton_shape_mapping_triggered`
- `newton_shape_object_created`
- `newton_shape_runtime_construction_triggered`
- `newton_shape_runtime_boundary_crossed`
- `newton_engine_shape_object_created`
- `newton_builder_shape_called`

The payload and row may set these narrow report-record fields to true/count one:

- `repo_local_newton_shape_mapping_record_constructed: true`
- `newton_shape_mapping_record_created: true`
- `constructed_newton_shape_mapping_record_count: 1`
- `newton_mapping_record_count: 1`

The row must include:

- `newton_shape_runtime_construction_row_id:
  newton_shape_runtime_construction__paper_single_box__box`
- `source_newton_shape_runtime_boundary_preflight_row_id:
  newton_shape_runtime_boundary_preflight__paper_single_box__box`
- `source_shape_mapping_row_id: newton_shape_mapping__paper_single_box__box`
- source runtime-admissibility row id, package id, asset id, fixture id, paper primitive, primitive
  id, and PrimitiveSpec kind
- `target_newton_shape_kind: box`
- descriptor fields copied from the preflight row: center, axes, half extents
- `constructed_newton_shape_mapping_dict`
- `constructed_newton_shape_mapping_status: mapped`
- `constructed_newton_shape_mapping_detail: mapped`
- `mapping_constructor: NewtonShapeMapping`
- `mapping_constructor_input_kind: static_descriptor_fields`
- `runtime_builder_preflight_candidate: true`
- `constructed_newton_shape_mapping_record_count: 1`
- `newton_mapping_record_count: 1`
- `newton_mapper_call_count: 0`
- `newton_shape_object_count: 0`
- `newton_engine_shape_object_count: 0`
- `newton_builder_shape_call_count: 0`
- `newton_runtime_execution_count: 0`

The exact `constructed_newton_shape_mapping_dict` must match `NewtonShapeMapping.to_dict()`:

```json
{
  "primitive_id": "paper_single_box__oriented_bounding_box__box",
  "kind": "box",
  "status": "mapped",
  "detail": "mapped",
  "center": "<descriptor_center>",
  "axes": "<descriptor_axes>",
  "dimensions": {"half_extents": "<descriptor_half_extents>"}
}
```

The string placeholders above mean the values must exactly equal the runtime-boundary preflight
row's descriptor fields, serialized as JSON-safe lists.

## Input Validation

The new payload builder must reject input drift from the runtime-boundary preflight payload:

- wrong `gate_id`;
- wrong `next_required_gate`;
- count drift for boundary preflight rows, later construction candidates, descriptor count,
  mapping attempts, Newton mapping records, Newton shape objects, Newton runtime execution,
  generated PrimitiveSpecs, generated CollisionPackages, and runtime-admissibility checks already
  exposed by the preflight payload;
- true values for any preflight false boundary flag;
- missing or extra runtime-boundary preflight rows;
- wrong fixture/source identifiers;
- non-box target kind;
- missing or malformed descriptor fields;
- descriptor center, axes, or half extents drifting between source row and constructed mapping;
- non-finite center, axes, or half extents;
- axes that are not orthonormal or not right-handed, matching the `mapped` semantics used by
  `primitive_collision_compiler.newton.shapes`;
- non-positive half extents;
- copied source `CollisionPackage.to_dict()` artifacts inside the input payload.

The row-level construction should reuse existing finite vector checks where practical. The
runtime-boundary preflight row remains the single source of truth for descriptor fields. This
slice must not re-consume earlier source package dicts or real USD assets.

## Report Integration

`build_cpd_paper_offline_report()` should:

- build the current shape-mapping contract payload;
- build the current runtime-boundary preflight payload;
- build the new runtime-construction payload from that preflight payload;
- add `paper_mapped_subset_newton_shape_runtime_construction_contract` to the report;
- append `paper_mapped_subset_newton_shape_runtime_construction_contract` to
  `implemented_output_contract_scope`;
- change top-level `paper_faithfulness.runtime_lane_remaining_gates` and `next_required_gate` to
  `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`;
- keep `paper_faithful_offline_supported: false` and report `status: partial`.

The runtime-boundary preflight payload's own `next_required_gate` remains
`paper_mapped_subset_newton_shape_runtime_construction_contract`. Only the top-level report
advances after the new construction payload exists.

## Documentation

Update the usual CPD story docs:

- `README.md`
- `docs/index.md`
- `docs/deepdive/evidence-status.md`
- `docs/deepdive/message-map.md`
- `docs/reference/claim-boundaries.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- `docs/records/README.md`
- a new dated record under `docs/records/`

The docs must say this slice constructs one repo-local `NewtonShapeMapping.to_dict()` report
record from one static descriptor. They must not claim Newton engine shape construction, Newton
support, Newton readiness, Newton task execution, contact evidence, real-USD evidence, benchmark
evidence, collision-quality evidence, paper-faithful offline support, full CPD reproduction,
deployment readiness, safety certification, or general package readiness.

## Tests

Add focused tests in `tests/test_cpd_paper_offline.py` for:

- payload presence and exact schema;
- row schema and `constructed_newton_shape_mapping_dict` schema;
- top-level next gate advancing to
  `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`;
- runtime-boundary preflight payload next gate remaining
  `paper_mapped_subset_newton_shape_runtime_construction_contract`;
- narrow report-record construction fields and engine/runtime false fields;
- lineage from constructed mapping back to runtime-boundary preflight, shape-mapping contract,
  runtime-admissibility row, and package id;
- descriptor center/axes/half-extents equality between source row and constructed mapping;
- input drift rejection;
- descriptor numeric validation and source-descriptor divergence rejection;
- source package copy rejection;
- static source boundary check proving the new implementation allows exactly one local
  `NewtonShapeMapping` construction while forbidding Newton/warp imports, builder calls, contact
  canaries, drop/settle, sphere-rain, USD loading, benchmark/timing, and collision-quality code.
  The static guard should count exactly one `NewtonShapeMapping(` call and allow a local
  `from primitive_collision_compiler.reports.schema import NewtonShapeMapping` import. It should
  not forbid the broad substring `Newton`, because that would reject the intended report-schema
  constructor. It must still forbid `primitive_collision_compiler.newton`, `import newton`,
  `from newton`, `builder.add_shape_`, `CollisionPipeline`, `collide`, `finalize`, diagnostics
  task calls, USD loading, and executable benchmark/collision-quality tokens such as
  `run_benchmark`, `benchmark_metric`, `timeit`, `perf_counter`, `measure_collision_quality`, and
  `collision_quality_score`. It must allow false boundary flag names such as `benchmark_run`,
  `benchmark_triggered`, and `collision_quality_measured`.

Update CLI tests in `tests/test_cli.py` so the offline report command expects the new current
failure label and next gate:

- `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract_missing`
- `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`

## Verification

Required verification:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_construction or newton_shape_runtime_boundary_preflight or newton_shape_mapping_contract' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -q
PYTHONPATH=src python -m pytest -q
```

## Non-Goals

- No Newton or warp import.
- No `newton.ModelBuilder`, `builder.add_shape_*`, `CollisionPipeline`, `collide`, `finalize`, or
  contact count.
- No contact canary, drop/settle, sphere-rain, timing, benchmark, or surface-distance metric.
- No USD loading and no bed/Franka rerun.
- No general primitive mapping beyond the one synthetic `paper_single_box` box descriptor.
- No claim that the constructed mapping improves collision quality or supports the full CPD paper
  primitive vocabulary.
