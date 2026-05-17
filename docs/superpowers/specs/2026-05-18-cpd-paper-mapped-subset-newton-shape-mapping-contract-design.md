# CPD Paper Mapped-Subset Newton Shape-Mapping Contract Design

## Summary

Implement the next bounded CPD paper runtime-lane gate:
`paper_mapped_subset_newton_shape_mapping_contract`.

This is still an offline/report-only contract. It consumes the existing
`paper_mapped_subset_newton_shape_mapping_preflight_contract` row for the deterministic synthetic
`paper_single_box` OBB/box artifact and emits exactly one report-scoped Newton shape descriptor
contract row. The row records how the candidate box fields would be handed to a later Newton shape
construction gate, but it does not import Newton, construct a Newton shape object, run a Newton
task, load USD, run benchmarks, or measure collision quality.

## Why This Slice Exists

The previous gate proved only that one report row has the fields a later mapper would need:
target kind `box`, center, axes, dimensions, and half extents. The current next gate should close
the next tiny gap: record the actual report-side descriptor contract for that one mapped-subset
artifact.

In plain terms:

- previous slice: "the row has fields a mapper would need";
- this slice: "the report now contains a descriptor row saying how those fields map to a Newton
  box descriptor";
- later slice: "decide whether and how that descriptor may be handed to real Newton runtime code."

## Design Choice

Use a static descriptor contract, not a Newton runtime mapper.

Rejected alternatives:

- Real Newton mapping now. This would cross the current evidence boundary because no runtime
  boundary gate exists for shape construction.
- A broad multi-primitive mapper. The current mapped subset has one eligible artifact:
  `paper_single_box` as `box`; generalizing now would create unearned support claims.
- Skipping directly to a drop/settle or contact task. That would mix descriptor correctness,
  Newton object construction, and runtime execution in one step.

Recommended approach:

- Add one payload under `cpd_paper_offline_report`:
  `paper_mapped_subset_newton_shape_mapping_contract`.
- Add one row:
  `newton_shape_mapping__paper_single_box__box`.
- Add one report-scoped descriptor dict with only JSON-safe scalar/list fields:
  `newton_shape_descriptor_dict`.
- Keep all Newton runtime/object counters zero.
- Advance the top-level next gate to
  `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`.
  This slice must add that new gate id as the next unresolved report-lane gate and the report's
  next failure label must become
  `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_missing`.

## Payload Contract

The new payload must include:

- `gate_id: paper_mapped_subset_newton_shape_mapping_contract`
- `gate_status: implemented_offline_static_shape_descriptor_contract_only`
- `input_gate_id: paper_mapped_subset_newton_shape_mapping_preflight_contract`
- `next_required_gate: paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`
- `shape_mapping_contract_row_count: 1`
- `report_scoped_newton_shape_descriptor_count: 1`
- `newton_shape_object_count: 0`
- `newton_runtime_execution_count: 0`
- `mapping_attempt_count: 0`
- `newton_mapping_record_count: 0`
- `shape_mapping_rows: [...]`
- false boundary flags for unsupported claims and runtime triggers

The row must include:

- `shape_mapping_row_id: newton_shape_mapping__paper_single_box__box`
- `source_newton_shape_mapping_preflight_row_id`, copied from the preflight row's
  `newton_shape_mapping_preflight_row_id`
- source package id, source asset id, fixture id, primitive id, paper primitive, and
  PrimitiveSpec kind
- `target_newton_shape_kind: box`
- `newton_shape_descriptor_dict`
- `descriptor_contract_passed: true`
- checks for center, axes, half extents, source preflight status, and lineage
- `mapping_attempt_count: 0`
- `newton_mapping_record_count: 0`
- `newton_shape_object_count: 0`
- `newton_runtime_execution_count: 0`
- all runtime, USD, benchmark, collision-quality, deployment, and certification triggers false

The descriptor dict must be report-scoped:

```json
{
  "descriptor_kind": "newton_shape_descriptor",
  "target_newton_shape_kind": "box",
  "source_fixture_id": "paper_single_box",
  "source_primitive_id": "paper_single_box__oriented_bounding_box__box",
  "center": [0.0, 0.0, 0.0],
  "axes": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
  "half_extents": [1.0, 0.5, 0.25],
  "mapping_contract": "report_scoped_static_descriptor_no_newton_call"
}
```

The exact numeric values should come from the current preflight row, not from hardcoded test-only
fixtures outside the report chain.

## Input Validation

The new payload builder must reject input drift from the preflight payload:

- wrong `gate_id`;
- wrong `next_required_gate`;
- count drift for preflight rows, mapping attempts, Newton mapping records, Newton runtime
  execution, and source runtime-admissibility rows;
- true values for any preflight false boundary flag;
- missing or extra preflight rows;
- wrong fixture/source identifiers;
- non-box target kind;
- missing or malformed `candidate_primitivespec_dict`;
- copied source package dicts inside the new payload input.

The row-level validation should reuse the existing finite vector checks where practical and should
keep the source preflight row as the single source of truth for center, axes, and half extents.

## Report Integration

`build_cpd_paper_offline_report()` should:

- build the current preflight payload;
- build the new shape-mapping contract payload from that preflight payload;
- add `paper_mapped_subset_newton_shape_mapping_contract` to the report;
- append `paper_mapped_subset_newton_shape_mapping_contract` to
  `implemented_output_contract_scope`;
- change top-level `paper_faithfulness.runtime_lane_remaining_gates` and
  `next_required_gate` to
  `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`;
- keep `paper_faithful_offline_supported: false` and report `status: partial`.

The preflight payload's own `next_required_gate` remains
`paper_mapped_subset_newton_shape_mapping_contract`. Only the top-level report advances after the
new contract exists.

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

The docs must say this slice records one report-scoped descriptor contract row only. They must not
claim Newton readiness, Newton support, actual Newton shape object construction, Newton execution,
real-USD evidence, benchmark evidence, collision-quality evidence, paper-faithful offline support,
full CPD reproduction, deployment readiness, safety certification, or general package readiness.

## Tests

Add focused tests in `tests/test_cpd_paper_offline.py` for:

- payload presence and schema;
- row schema and descriptor dict schema;
- top-level next gate advancing to
  `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`;
- preflight payload next gate remaining
  `paper_mapped_subset_newton_shape_mapping_contract`;
- false boundary flags staying false at payload and row levels;
- input drift rejection;
- candidate/descriptor numeric validation;
- source package copy rejection;
- static source boundary check proving the new implementation does not import/call Newton, USD,
  runtime execution, benchmarks, or collision-quality code.

Update CLI tests in `tests/test_cli.py` so the offline report command expects the new current
failure label and next gate:

- `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_missing`
- `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`

## Verification

Required verification:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_mapping_contract' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
PYTHONPATH=src python -m pytest -q
```

## Non-Goals

- No Newton import or Newton shape object creation.
- No Newton runtime execution.
- No USD asset loading.
- No benchmark or collision-quality metrics.
- No bed/Franka rerun.
- No general primitive mapping beyond the one synthetic `paper_single_box` box descriptor.
- No claim that Newton supports this descriptor until a later runtime-boundary/runtime gate records
  evidence.
