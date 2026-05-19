# CPD Paper Newton Engine-Builder Runtime-Execution Contract Design

## Context

The current `cpd_paper_offline_report` closes the report-only engine-builder smoke contract for
the single synthetic `paper_single_box` OBB/box lineage. That smoke contract records
`skip_real_runtime_smoke`, keeps all real Newton/Warp import, builder, finalization, collision
pipeline, and Newton runtime counters at zero, and reports
`paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract` as the next
runtime-lane gate.

This slice closes that next gate as another report-only decision record. It must not cross the
real Newton runtime boundary.

## Approaches Considered

1. **Recommended: report-only skipped runtime-execution decision.** Consume the smoke row, verify
   the lineage and zero counters, record `skip_real_runtime_execution`, and advance to a later
   claim-boundary review gate. This matches the existing gate-chain style and keeps claim
   boundaries explicit.
2. **Terminal runtime-lane marker.** Close the runtime-execution gate and make remaining runtime
   gaps empty. This is not a good fit because the report builder currently expects a non-empty
   next-gate list.
3. **Configured real runtime attempt.** Import Newton/Warp and try a real runtime call. This is out
   of scope because the previous entry and smoke gates deliberately recorded default no-runtime
   decisions and no configured source/runtime entry exists.

## Goal

Add one bounded, report-only runtime-execution contract that consumes the skipped-smoke row,
verifies the same single synthetic lineage, records that real runtime execution is not run, and
keeps every runtime-affecting counter at zero.

## Non-Goals

- No real `newton` or `warp` import.
- No `newton.ModelBuilder` instantiation.
- No real `add_shape_box` call.
- No Newton engine shape object creation.
- No model finalization.
- No collision pipeline creation or collision.
- No contact, drop/settle, or sphere-rain task execution from this report path.
- No real-USD evaluation.
- No benchmark, collision-quality, deployment, or safety claim.
- No broadening beyond the existing `paper_single_box` lineage.
- No claim that Newton runtime compatibility is validated.

## Design

The implementation adds a new report payload:

```text
paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract
```

It consumes:

```text
paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract
```

The runtime-execution payload records one row for the existing synthetic mapped-subset
`paper_single_box` OBB/box lineage. The row carries the upstream smoke row ID and all relevant
source lineage IDs, then records:

- `runtime_execution_decision: skip_real_runtime_execution`;
- `runtime_execution_decision_reason: default_no_runtime_smoke_decision_preserved`;
- `runtime_execution_allowed: false`;
- `runtime_execution_attempted: false`;
- `runtime_execution_passed: false`;
- `runtime_execution_result_status: not_run_default_no_runtime_smoke`;
- exact zero counters for real imports, `ModelBuilder`, engine shape objects, real builder shape
  calls, model finalization, collision pipeline calls, and Newton runtime execution;
- `source_package_copy_forbidden: true`.

The payload closes only the runtime-execution contract as a report-only decision record. The
report remains `partial` and `paper_faithful_offline_supported: false`.

## Next Gate

After this contract, the next runtime-lane gap becomes:

```text
paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract
```

That future gate is a claim-boundary review point before any stronger runtime work is designed.
It is not a real runtime import, real Newton execution, benchmark, or collision-quality gate.

## Tests

Use TDD:

1. Add failing tests that expect the report and CLI JSON to include the runtime-execution payload
   and advance the top-level next gate to the runtime-lane review contract.
2. Add exact schema tests for the runtime-execution payload and row.
3. Add drift tests showing the runtime-execution payload rejects stale or widened smoke input,
   including more than one smoke row and stale lineage fields.
4. Add static-boundary tests forbidding real runtime imports, dynamic import or execution escape
   hatches, builder calls, finalization, collision calls, existing Newton task smokes, USD
   inspection, benchmark timing APIs, and collision-quality calls inside the new helpers.
5. Implement the smallest report-only payload that passes those tests.

## Claim Boundary

Allowed wording:

- The report records a bounded runtime-execution decision for one synthetic mapped-subset box
  lineage.
- The default no-config report skips real runtime execution because the smoke decision skipped
  real runtime smoke.
- All real Newton/Warp import, builder, shape-object, finalization, collision pipeline, and
  runtime counters remain zero.
- The next gate is a runtime-lane claim-boundary review contract.

Forbidden wording:

- Newton support is implemented.
- Runtime execution ran or passed.
- Runtime compatibility is validated.
- Real builder calls were made or validated.
- A Newton model, engine shape object, or collision pipeline was created.
- The package is simulation-checked by this report path.
- Collision quality, benchmarks, deployment readiness, or safety certification are shown.
