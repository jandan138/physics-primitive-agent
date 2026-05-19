# CPD Paper Newton Engine-Builder Smoke Contract Design

## Context

The current `cpd_paper_offline_report` closes the bounded engine-builder entry contract and
reports `paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract` as the next
runtime-lane gate. The entry row records the default `defer_real_runtime_entry` decision for the
single synthetic `paper_single_box` OBB/box lineage.

This slice implements the smoke contract without crossing the real Newton runtime boundary.

## Goal

Add one bounded, report-only engine-builder smoke contract that consumes the entry row, verifies
the same synthetic lineage, records that the default no-config report skips real runtime smoke, and
advances the next gate to a later runtime-execution contract.

## Non-Goals

- No real `newton` or `warp` import.
- No `newton.ModelBuilder` instantiation.
- No real `add_shape_box` call.
- No Newton shape object creation.
- No model finalization.
- No collision pipeline creation or collision.
- No contact, drop/settle, or sphere-rain task execution from this report path.
- No real-USD evaluation.
- No benchmark, collision-quality, deployment, or safety claim.
- No broadening beyond the existing `paper_single_box` lineage.

## Design

The implementation adds a new report payload:

```text
paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract
```

It consumes:

```text
paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract
```

The smoke payload records one row for the existing synthetic mapped-subset `paper_single_box`
OBB/box lineage. The row carries the upstream entry row ID and all relevant source lineage IDs,
then records:

- `smoke_decision: skip_real_runtime_smoke`;
- `smoke_decision_reason: default_no_runtime_entry_decision_preserved`;
- `runtime_smoke_allowed: false`;
- `runtime_smoke_attempted: false`;
- `runtime_smoke_passed: false`;
- `runtime_smoke_result_status: not_run_default_no_runtime_entry`;
- exact zero counters for real imports, `ModelBuilder`, real builder shape calls, model
  finalization, collision pipeline calls, and Newton runtime execution;
- `source_package_copy_forbidden: true`.

The payload closes only the smoke contract as a report-only decision record. The report remains
`partial` and `paper_faithful_offline_supported: false`.

## Next Gate

After the smoke contract, the next runtime-lane gap becomes:

```text
paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract
```

That future gate is where a configured runtime attempt may be designed. This smoke slice must not
perform that attempt.

## Tests

Use TDD:

1. Add failing tests that expect the report and CLI JSON to include the smoke payload and advance
   the top-level next gate.
2. Add exact schema tests for the smoke payload and row.
3. Add drift tests showing the smoke payload rejects stale entry input.
4. Add static-boundary tests forbidding real runtime imports and builder/runtime calls inside the
   smoke implementation.
5. Implement the smallest report-only payload that passes those tests.

## Claim Boundary

Allowed wording:

- The report records a bounded engine-builder smoke decision for one synthetic mapped-subset box
  lineage.
- The default no-config report skips real runtime smoke because the entry decision deferred real
  runtime entry.
- All real Newton/Warp import, builder, finalization, collision pipeline, and runtime counters
  remain zero.
- The next gate is a future runtime-execution contract.

Forbidden wording:

- Newton support is implemented.
- Runtime compatibility is validated.
- Real builder calls were made or validated.
- A Newton model, engine shape object, or collision pipeline was created.
- The package is simulation-checked by this report path.
- Collision quality, benchmarks, deployment readiness, or safety certification are shown.
