# CPD Paper Mapped-Subset Newton Shape Runtime-Boundary Preflight Contract Design

## Summary

Implement the next bounded CPD paper runtime-lane gate:
`paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`.

This is still an offline/report-only contract. It consumes the existing
`paper_mapped_subset_newton_shape_mapping_contract` row for the deterministic synthetic
`paper_single_box` OBB/box artifact and emits exactly one static preflight row for a later Newton
shape runtime-construction gate. The row records that the report-scoped descriptor has the lineage
and JSON-safe fields a later gate would need before any real Newton shape object may be considered.
It does not import Newton, construct a Newton shape object, call a mapper, run a Newton task, load
USD, run benchmarks, or measure collision quality.

## Why This Slice Exists

The previous gate recorded one static `newton_shape_descriptor_dict`:

- target kind `box`;
- source fixture and primitive ids;
- center, axes, and half extents copied from the single synthetic package artifact;
- a report-only marker:
  `mapping_contract: report_scoped_static_descriptor_no_newton_call`.

That proves the report can describe the intended Newton shape input, but it does not prove the
descriptor is allowed to cross a runtime boundary. This slice closes only the next small gap:
record one static runtime-boundary preflight row saying the descriptor is eligible for a later
Newton shape construction contract to inspect.

In plain terms:

- previous slice: "the report has a static Newton box descriptor";
- this slice: "the report has a preflight row that checks the descriptor before a runtime boundary";
- later slice: "decide whether to construct a real Newton shape object from the descriptor."

## Design Choice

Use a static runtime-boundary preflight, not real Newton construction.

Rejected alternatives:

- Construct a Newton shape now. That would cross the current evidence boundary because this gate is
  only the preflight before runtime construction.
- Collapse preflight and construction into one gate. That would hide whether descriptor validation,
  runtime-boundary admission, and object construction each passed.
- Generalize to all descriptor kinds. The mapped subset has exactly one eligible descriptor:
  `paper_single_box` as `box`; broadening now would create unearned support claims.

Recommended approach:

- Add one payload under `cpd_paper_offline_report`:
  `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`.
- Add one row:
  `newton_shape_runtime_boundary_preflight__paper_single_box__box`.
- Copy only row-level lineage and descriptor field checks, not full package artifacts.
- Keep all mapping/object/runtime counters zero.
- Advance the top-level next gate to
  `paper_mapped_subset_newton_shape_runtime_construction_contract`.

## Payload Contract

The new payload must include:

- `gate_id: paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`
- `gate_status: implemented_offline_newton_shape_runtime_boundary_preflight_only`
- `closed_gate: paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`
- `input_gate_id: paper_mapped_subset_newton_shape_mapping_contract`
- `next_required_gate: paper_mapped_subset_newton_shape_runtime_construction_contract`
- `decision: remain_partial`
- `decision_reason:
  newton_shape_runtime_boundary_preflight_complete_newton_shape_runtime_construction_missing`
- `artifact_kind: offline_static_newton_shape_runtime_boundary_preflight_not_shape_object`
- `schema_version: 1`
- `source_scope: synthetic_toy_fixtures_only`
- `implementation_boundary:
  single_synthetic_box_newton_shape_runtime_boundary_preflight_only_no_newton_object_no_runtime_no_real_usd_no_benchmark_no_metrics`
- `runtime_boundary_preflight_action:
  record_one_later_newton_shape_runtime_construction_candidate_without_newton_call`
- `newton_shape_runtime_boundary_preflight_contract`, a nested contract summary with input gate,
  closed gate, next construction gate, required row count, required later construction candidate
  count, and `newton_shape_object_allowed: false`
- `input_contract_summary`, with input gate id, input next gate, source shape-mapping row id,
  source package id, fixture id, primitive id, target kind, and descriptor kind
- `newton_shape_runtime_boundary_preflight_row_count: 1`
- `source_shape_mapping_contract_row_count: 1`
- `later_newton_shape_runtime_construction_candidate_count: 1`
- `report_scoped_newton_shape_descriptor_count: 1`
- `runtime_boundary_preflight_passed: true`
- `mapping_attempt_count: 0`
- `newton_mapping_record_count: 0`
- `newton_shape_object_count: 0`
- `newton_runtime_execution_count: 0`
- carried-forward completed-gate counters:
  `generated_runtime_primitive_spec_count: 1`, `generated_primitive_spec_count: 1`,
  `generated_collision_package_count: 1`, `runtime_admissibility_check_count: 1`, and
  `offline_static_runtime_admissibility_check_count: 1`
- `newton_shape_runtime_boundary_preflight_rows: [...]`
- `coverage_summary`
- `remaining_gaps: [paper_mapped_subset_newton_shape_runtime_construction_contract]`

The payload and each row must carry these false boundary flags:

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
- `newton_shape_mapping_record_created`
- `newton_shape_object_created`
- `newton_shape_runtime_construction_triggered`
- `newton_shape_runtime_boundary_crossed`

The row must include:

- `newton_shape_runtime_boundary_preflight_row_id:
  newton_shape_runtime_boundary_preflight__paper_single_box__box`
- `source_shape_mapping_row_id: newton_shape_mapping__paper_single_box__box`
- source runtime-admissibility row id, package id, asset id, fixture id, paper primitive, primitive
  id, and PrimitiveSpec kind
- `target_newton_shape_kind: box`
- descriptor checks for `descriptor_kind`, target kind, center, axes, and half extents
- lineage checks back to the shape-mapping contract row
- `later_newton_shape_runtime_construction_candidate: true`
- `newton_shape_object_count: 0`
- `newton_runtime_execution_count: 0`
- all runtime, USD, benchmark, collision-quality, deployment, and certification triggers false

The preflight row may summarize descriptor fields, but it must not copy a full source
`CollisionPackage.to_dict()` artifact and must not create a real Newton shape object.

## Input Validation

The new payload builder must reject input drift from the shape-mapping contract payload:

- wrong `gate_id`;
- wrong `next_required_gate`;
- count drift for shape-mapping rows, descriptor count, mapping attempts, Newton mapping records,
  Newton shape objects, Newton runtime execution, generated PrimitiveSpecs, generated
  CollisionPackages, and runtime-admissibility checks;
- true values for any shape-mapping contract false boundary flag;
- missing or extra shape-mapping rows;
- wrong fixture/source identifiers;
- non-box target kind;
- missing or malformed `newton_shape_descriptor_dict`;
- descriptor drift within the shape-mapping contract row itself: descriptor kind must be
  `newton_shape_descriptor`, descriptor target kind must match the row target kind, descriptor
  source fixture and primitive ids must match the row, and descriptor center, axes, and half
  extents must be finite with positive half extents;
- copied source package dicts inside the input payload.

The row-level validation should reuse the existing finite vector checks where practical. The
shape-mapping contract row remains the single source of truth for the descriptor fields. This slice
must not re-consume the earlier shape-mapping preflight payload or require original
`candidate_primitivespec_dict` values that are no longer present in the input payload.

## Report Integration

`build_cpd_paper_offline_report()` should:

- build the current shape-mapping preflight payload;
- build the current shape-mapping contract payload;
- build the new runtime-boundary preflight payload from that contract payload;
- add `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract` to the report;
- append `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract` to
  `implemented_output_contract_scope`;
- change top-level `paper_faithfulness.runtime_lane_remaining_gates` and `next_required_gate` to
  `paper_mapped_subset_newton_shape_runtime_construction_contract`;
- keep `paper_faithful_offline_supported: false` and report `status: partial`.

The shape-mapping contract payload's own `next_required_gate` remains
`paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`. Only the top-level report
advances after the new preflight exists.

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

The docs must say this slice records one report-only runtime-boundary preflight row. They must not
claim Newton readiness, Newton support, actual Newton shape object construction, Newton execution,
real-USD evidence, benchmark evidence, collision-quality evidence, paper-faithful offline support,
full CPD reproduction, deployment readiness, safety certification, or general package readiness.

## Tests

Add focused tests in `tests/test_cpd_paper_offline.py` for:

- payload presence and exact schema;
- row schema and descriptor field checks;
- top-level next gate advancing to
  `paper_mapped_subset_newton_shape_runtime_construction_contract`;
- shape-mapping contract payload next gate remaining
  `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`;
- false boundary flags staying false at payload and row levels;
- input drift rejection;
- descriptor numeric validation and source-descriptor divergence rejection;
- source package copy rejection;
- static source boundary check proving the new implementation does not import/call Newton, USD,
  runtime execution, benchmarks, or collision-quality code.

Update CLI tests in `tests/test_cli.py` so the offline report command expects the new current
failure label and next gate:

- `paper_mapped_subset_newton_shape_runtime_construction_contract_missing`
- `paper_mapped_subset_newton_shape_runtime_construction_contract`

## Verification

Required verification:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_boundary_preflight' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
PYTHONPATH=src python -m pytest -q
```

## Non-Goals

- No Newton import.
- No Newton mapper call.
- No Newton shape object creation.
- No Newton runtime execution.
- No USD asset loading.
- No benchmark or collision-quality metrics.
- No bed/Franka rerun.
- No general primitive mapping beyond the one synthetic `paper_single_box` box descriptor.
- No claim that Newton supports this descriptor until a later runtime construction or execution
  gate records evidence.
