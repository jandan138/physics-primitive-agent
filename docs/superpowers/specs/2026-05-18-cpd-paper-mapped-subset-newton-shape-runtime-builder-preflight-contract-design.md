# CPD Paper Mapped-Subset Newton Shape Runtime-Builder Preflight Contract Design

## Summary

Implement the next bounded CPD paper runtime-lane gate:
`paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`.

This slice consumes the existing single-fixture
`paper_mapped_subset_newton_shape_runtime_construction_contract` row and records exactly one
offline/static Newton builder-call candidate for the deterministic `paper_single_box` OBB/box
artifact.

The builder-preflight helper block adds no new Newton/Warp import and invokes no Newton/Warp API;
this is not a module-level no-Newton-import claim. It does not instantiate `ModelBuilder`, does
not call `builder.add_shape_box`, does not create a Newton engine shape object, does not finalize a
model, does not run contact/drop/sphere-rain diagnostics, does not load real USD, does not run a
benchmark, and does not measure collision quality.

## Why This Slice Exists

The current paper story has reached this point:

```text
paper-selected primitive
-> CollisionPackage-like artifact
-> runtime-admissibility static check
-> NewtonShapeMapping.to_dict() report record
```

The previous gate proved that one static descriptor can become a repo-local
`NewtonShapeMapping.to_dict()` record. The next useful gate is not a real Newton call yet. It is
a report-only checklist item for a possible future runtime gate: "if a later runtime gate is
separately allowed to consider this record, which builder method and scalar inputs would it
inspect first?"

In plain terms:

- previous slice: "we have one JSON-safe Newton shape mapping record";
- this slice: "we record the intended repo-local Newton builder method name and scalar fields for
  later runtime review";
- later slice: "separately evaluate whether crossing the Newton import/builder boundary is in
  scope."

## Design Choice

Use a builder preflight row, not a Newton builder call.

Recommended approach:

- Add one payload under `cpd_paper_offline_report`:
  `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`.
- Add the next runtime-lane gate constant:
  `paper_mapped_subset_newton_shape_runtime_builder_construction_contract`.
- Validate that the input construction payload is exactly the one-row `paper_single_box` box gate.
- Read the constructed `NewtonShapeMapping.to_dict()` record from the input row.
- Validate identity and lineage across the input row and mapping dict.
- Validate box-specific builder inputs:
  center is finite vector3, axes are finite right-handed orthonormal rows, half extents are three
  positive finite values, and mapping status is `mapped`.
- Record a data-only builder-call plan:
  `builder_method_name: add_shape_box`, `call_signature_fields: [body, xform, hx, hy, hz]`,
  `builder_dimension_argument_schema`, `builder_call_plan`, center, axes, and half-extents. The
  plan records the observed body-binding options without choosing a task runtime: static
  package/probe helpers bind `body=-1`, while drop/settle binds the created body id.
- Record `runtime_builder_preflight_passed: true` and
  `later_newton_shape_runtime_builder_candidate_count: 1`.
- Keep mapper-call, Newton engine shape, Newton builder call, runtime, USD, benchmark, and
  collision-quality counters at zero.
- Advance the top-level next gate to
  `paper_mapped_subset_newton_shape_runtime_builder_construction_contract`.
  Top-level `paper_faithfulness.runtime_lane_remaining_gates` must be exactly
  `[paper_mapped_subset_newton_shape_runtime_builder_construction_contract]`.

Rejected alternatives:

- Call `newton.ModelBuilder` in the offline paper report. That would make a report-only CPD paper
  audit depend on environment-specific Newton/warp imports and would cross the runtime boundary.
- Reuse `primitive_collision_compiler.newton.diagnostics._add_static_shape` inside the offline
  report. That helper performs real builder calls; this gate must only record a candidate.
- Generalize to sphere/capsule/cylinder in this slice. The current mapped-subset paper lane has
  one eligible `paper_single_box` row, so broadening now would imply unearned support evidence.
- Claim Newton readiness because a builder candidate exists. The candidate is a checklist item,
  not runtime execution evidence.

## Terminology

- `NewtonShapeMapping.to_dict()` record: repo-local JSON-safe report data created by the previous
  gate.
- `Builder preflight candidate`: an offline/static dictionary that names the future Newton builder
  method and scalar arguments, without creating any Newton object.
- `Newton builder call`: a real runtime call such as
  `builder.add_shape_box(body=-1, xform=xform, hx=hx, hy=hy, hz=hz)`. This slice must not perform
  such a call.
- `Newton engine shape object`: the shape/index stored in a Newton model after a real builder
  call. This slice must not create one.

The report fields must keep these meanings:

- `newton_mapping_record_count: 1`: there is one repo-local mapping record from the previous gate.
- `later_newton_shape_runtime_builder_candidate_count: 1`: there is one offline candidate for a
  future builder call.
- `newton_mapper_call_count: 0`: no generic package-to-Newton mapper was run.
- `newton_builder_shape_call_count: 0`: no real builder shape method was called.
- `newton_shape_object_count: 0` and `newton_engine_shape_object_count: 0`: no Newton engine shape
  exists.
- `newton_runtime_execution_count: 0`: no runtime task was executed.

## Payload Contract

The new payload must include:

- `gate_id: paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`
- `gate_status: implemented_single_fixture_newton_shape_runtime_builder_preflight_only_partial`
- `closed_gate: paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`
- `input_gate_id: paper_mapped_subset_newton_shape_runtime_construction_contract`
- `next_required_gate: paper_mapped_subset_newton_shape_runtime_builder_construction_contract`
- `decision: remain_partial`
- `decision_reason:
  newton_shape_runtime_builder_preflight_complete_newton_shape_runtime_builder_construction_contract_missing`
- `artifact_kind:
  offline_static_newton_builder_call_plan_not_builder_call`
- `schema_version: 1`
- `source_scope: synthetic_toy_fixtures_only`
- `implementation_boundary:
  single_synthetic_box_newton_builder_preflight_only_no_builder_call_no_engine_shape_no_runtime_no_real_usd_no_benchmark_no_metrics`
- `runtime_builder_preflight_action:
  record_one_newton_builder_call_plan_from_repo_local_mapping_dict_without_builder_call_or_newton_runtime_execution`
- `newton_shape_runtime_builder_preflight_contract`, a nested contract summary with the input
  gate, closed gate, next builder gate, required row count, required builder-call candidate count,
  and false builder/runtime permissions
- `input_contract_summary`, with input gate id, input next gate, source construction row id,
  source runtime-boundary preflight row id, source shape-mapping row id, source package id,
  fixture id, primitive id, target kind, and constructor name
- `newton_shape_runtime_builder_preflight_row_count: 1`
- `source_newton_shape_runtime_construction_row_count: 1`
- `source_newton_shape_mapping_record_count: 1`
- `runtime_builder_preflight_passed: true`
- `runtime_builder_preflight_passed_count: 1`
- `builder_call_plan_count: 1`
- `builder_call_allowed_count: 0`
- `later_newton_shape_runtime_builder_candidate_count: 1`
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
  `report_scoped_newton_shape_descriptor_count: 1`,
  `later_newton_shape_runtime_construction_candidate_count: 1`, and
  `constructed_newton_shape_mapping_record_count: 1`
- `newton_shape_runtime_builder_preflight_rows: [...]`
- `coverage_summary`
- `remaining_gaps: [paper_mapped_subset_newton_shape_runtime_builder_construction_contract]`

The row must include:

- `newton_shape_runtime_builder_preflight_row_id:
  newton_shape_runtime_builder_preflight__paper_single_box__box`
- `source_newton_shape_runtime_construction_row_id:
  newton_shape_runtime_construction__paper_single_box__box`
- source runtime-boundary preflight row id, shape-mapping row id, mapping-preflight row id,
  runtime-admissibility row id, package id, asset id, fixture id, paper primitive, PrimitiveSpec
  kind, primitive id, target kind, and descriptor kind
- `constructed_newton_shape_mapping_dict`, copied from the previous gate
- `runtime_builder_preflight_passed: true`
- `builder_call_allowed: false`
- `builder_candidate_kind: static_shape_builder_call`
- `builder_shape_kind: box`
- `builder_method_name: add_shape_box`
- `call_signature_fields: [body, xform, hx, hy, hz]`
- `body_binding_policy:
  static_package_or_probe_uses_body_minus_one_drop_settle_uses_created_body_id`
- `deferred_xform_policy: future_runtime_may_derive_xform_from_center_and_axes`
- `deferred_translation_inputs: mapping_center_only_no_runtime_transform_constructed`
- `deferred_rotation_inputs: mapping_axes_only_no_quat_or_runtime_rotation_constructed`
- `dimension_source: constructed_newton_shape_mapping_dict.dimensions.half_extents`
- `builder_center`, copied from mapping `center`
- `builder_axes`, copied from mapping `axes`
- `builder_half_extents`, copied from mapping `dimensions.half_extents`
- `builder_dimension_argument_schema:
  {"hx": "half_extents[0]", "hy": "half_extents[1]", "hz": "half_extents[2]"}`
- `builder_call_plan`, a pure dict with:
  `method: add_shape_box`, `call_signature_fields: [body, xform, hx, hy, hz]`,
  `body_binding_policy`, deferred xform policy fields, and `dimension_arguments`
- `builder_call_plan_count: 1`
- `later_newton_shape_runtime_builder_candidate: true`
- `runtime_builder_construction_contract_candidate: true`
- `newton_mapping_record_count: 1`
- `newton_mapper_call_count: 0`
- `newton_shape_object_count: 0`
- `newton_engine_shape_object_count: 0`
- `newton_builder_shape_call_count: 0`
- `newton_runtime_execution_count: 0`

These body/xform policies are descriptive repo-local conventions for later review. This gate does
not choose, validate, or execute any task runtime.

The exact `coverage_summary` must include:

- `newton_shape_runtime_builder_preflight_row_count: 1`
- `source_newton_shape_runtime_construction_row_count: 1`
- `source_newton_shape_mapping_record_count: 1`
- `runtime_builder_preflight_passed_count: 1`
- `builder_call_plan_count: 1`
- `builder_call_allowed_count: 0`
- `later_newton_shape_runtime_builder_candidate_count: 1`
- `constructed_newton_shape_mapping_record_count: 1`
- `newton_mapping_record_count: 1`
- `newton_mapper_call_count: 0`
- `newton_shape_object_count: 0`
- `newton_engine_shape_object_count: 0`
- `newton_builder_shape_call_count: 0`
- `newton_runtime_execution_count: 0`
- `fixture_id_distribution: {"paper_single_box": 1}`
- `target_newton_shape_kind_distribution: {"box": 1}`
- `builder_method_distribution: {"add_shape_box": 1}`

## Boundary Flags

The payload and each row must keep these false:

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
- `newton_runtime_builder_invoked`
- `newton_model_builder_instantiated`
- `newton_model_finalized`

The payload and row may set these narrow preflight booleans to true:

- `newton_shape_runtime_builder_preflight_recorded: true`
- `repo_local_newton_builder_call_plan_record_created: true`

These are not runtime evidence.

## Input Validation

The new payload builder must reject input drift from the runtime-construction payload:

- wrong `gate_id`;
- wrong `next_required_gate`;
- required false input flags from the source runtime-construction schema set to true;
- any new builder-preflight output-only false flag present on the input and set to true;
- count drift for construction rows, source boundary-preflight rows, mapping records, mapper calls,
  shape object counts, builder call count, runtime count, package counters, admissibility counters,
  descriptor count, and construction candidate count;
- missing, non-dict, or multiple `newton_shape_runtime_construction_rows`;
- source row identity drift for construction row id, source boundary-preflight row id,
  shape-mapping row id, mapping-preflight row id, runtime-admissibility row id, package id, asset
  id, fixture id, paper primitive, PrimitiveSpec kind, primitive id, target kind, descriptor kind,
  constructor name, constructor input kind, and runtime-builder candidate flag;
- constructed mapping dict drift for primitive id, kind, status, detail, center, axes, and
  half-extents;
- constructed mapping dict key drift. The mapping dict must have exactly
  `{primitive_id, kind, status, detail, center, axes, dimensions}`, and `dimensions` must have
  exactly `{half_extents}` for this box gate;
- non-finite center values;
- axes that are not finite, orthonormal, and right-handed;
- half-extents that are missing, non-finite, or non-positive;
- accidental `generated_collision_package` copies in the input or output.

This gate must not construct any xform, transform object, quaternion, rotation object, or runtime
pose. It only copies center and axes as scalar/list report data and records deferred policy labels.

## Static Boundary Tests

Tests must prove the builder-preflight helper block does not contain:

- `primitive_collision_compiler.newton`
- `import newton`
- `from newton`
- `import warp`
- `from warp`
- `import newton_warp`
- `newton.ModelBuilder`
- `ModelBuilder`
- `CollisionPipeline`
- `add_shape_box(`
- `add_shape_sphere(`
- `add_shape_capsule(`
- `add_shape_cylinder(`
- `add_shape_cone(`
- `add_shape_ellipsoid(`
- `.add_shape_`
- `builder.finalize`
- `model_builder.finalize`
- `.finalize(`
- `pipeline.collide`
- `wp.transform`
- `wp.quat`
- `warp.transform`
- `warp.quat`
- `transformf`
- `quat_from`
- `CollisionPackage(`
- `PrimitiveSpec(`
- USD loading, real-USD comparison, benchmark, timing, or collision-quality patterns

The method name `add_shape_box` is allowed only as inert report data inside the candidate row.
The static test should forbid executable-call patterns such as `add_shape_box(` over helper source
while positive payload tests assert the inert method name and builder-call-plan dict in the
generated report.

## Documentation Updates

Update the canonical docs after implementation:

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
- Create
  `docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-builder-preflight-contract.md`

The docs must say this gate is a builder-call preflight only. They must not describe it as Newton
support, Newton execution, Newton readiness, collision quality, benchmark evidence, real-USD
evidence, or paper-faithful CPD reproduction.

Each listed document must replace stale "current next gate is builder preflight" wording with:
builder preflight is closed, and the current next gate is
`paper_mapped_subset_newton_shape_runtime_builder_construction_contract`, while preserving the no
Newton execution/support/readiness boundary.

## Test Strategy

Run focused tests first:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_builder_preflight' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Then run doc and whitespace checks:

```bash
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Before merge, run either the full test suite or the smallest defensible broader suite that covers
the touched report chain. If the full suite is skipped because of runtime cost, record that
explicitly in the completion record and final summary.

## Success Criteria

- The top-level report's `next_required_gate` becomes
  `paper_mapped_subset_newton_shape_runtime_builder_construction_contract`.
- The top-level failure label becomes
  `paper_mapped_subset_newton_shape_runtime_builder_construction_contract_missing`.
- The report includes
  `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`.
- That payload consumes exactly one runtime-construction row and records exactly one builder
  preflight candidate for `paper_single_box`/`box`.
- All Newton builder/runtime counters remain zero.
- The inert builder candidate records `add_shape_box`, call fields, body-binding policy,
  dimension-argument mapping for `hx`, `hy`, and `hz`, center, axes, and a deferred runtime-xform
  policy.
- No Newton/warp/runtime/USD/benchmark/collision-quality code path is introduced.
- Docs and dated records preserve the claim boundary.
