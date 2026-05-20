# CPD Paper Newton Engine-Builder Runtime-Lane Review Contract Design

## Context

The current `cpd_paper_offline_report` closes the report-only Newton engine-builder
runtime-execution contract for the single synthetic `paper_single_box` OBB/box lineage. That
contract records `skip_real_runtime_execution`, keeps real Newton/Warp import, builder,
finalization, collision pipeline, and runtime counters at zero, and reports
`paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract` as the next
required gate.

This slice closes that review gate as a claim-boundary review record. It must not cross the real
runtime boundary and must not reinterpret skipped execution as runtime compatibility.

## Approaches Considered

1. **Recommended: report-only runtime-lane review decision.** Consume the runtime-execution
   payload, verify it is still a skipped-runtime-execution record with zero real runtime counters,
   record that the review preserves claim boundaries, and advance to a later real-runtime source
   and configuration preflight gate. This keeps the chain moving without broadening evidence.
2. **Terminal runtime lane.** Close the review gate and make remaining runtime gaps empty. This is
   too strong because no real runtime source, runtime configuration, Newton import, builder call,
   or execution path exists.
3. **Runtime smoke redesign.** Reopen the lane by attempting a real Newton runtime smoke. This is
   out of scope because the current records deliberately preserve default no-runtime decisions and
   no configured Newton source directory is required by the report path.

## Goal

Add one bounded report-only runtime-lane review contract that consumes the skipped runtime-execution
payload, records that the runtime lane remains blocked by claim boundaries, and advances to a
future configured-runtime design contract before any real Newton runtime work can be designed.

## Non-Goals

- No real `newton` or `warp` import.
- No `newton.ModelBuilder` instantiation.
- No `add_shape_box` call.
- No Newton engine shape object creation.
- No model finalization.
- No collision pipeline creation or collision.
- No Newton contact, drop/settle, or sphere-rain task execution from this report path.
- No real-USD evaluation.
- No benchmark or collision-quality measurement.
- No claim that Newton support, runtime compatibility, deployment readiness, or safety
  certification is validated.
- No broadening beyond the existing `paper_single_box` lineage.

## Design

The implementation adds a new report payload:

```text
paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract
```

It consumes:

```text
paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract
```

The review payload records one row for the existing synthetic mapped-subset `paper_single_box`
OBB/box lineage. The row carries the upstream runtime-execution row ID and source lineage IDs, then
records:

- `runtime_lane_review_decision: keep_real_runtime_execution_blocked`;
- `runtime_lane_review_reason: skipped_runtime_execution_is_not_runtime_compatibility`;
- `runtime_lane_review_status: claim_boundary_preserved`;
- `runtime_lane_review_recorded: true` for the report-only review record;
- `runtime_lane_claim_boundary_preserved: true` for the documentation/claim-boundary review only;
- `real_runtime_execution_evidence: false`;
- `runtime_compatibility_validated: false`;
- exact zero counters for real imports, `ModelBuilder`, engine shape objects, real builder shape
  calls, model finalization, collision pipeline calls, and Newton runtime execution;
- `source_package_copy_forbidden: true`.

The payload closes only the review gate as a report-only decision record. The report remains
`partial` and `paper_faithful_offline_supported: false`.

## Next Gate

After this contract, the next runtime-lane gap should become:

```text
paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract
```

That future gate may only define the explicit Newton/Warp source and runtime inputs, package
lineage checks, and exit criteria required before any later real runtime import attempt. It is not
a real runtime import, real Newton execution, benchmark, or collision-quality gate.

## Tests

Use TDD:

1. Add a failing report/CLI test that expects the runtime-lane review payload and advances the
   top-level next gate to the configured-runtime design contract.
2. Add exact schema tests for the review payload and row.
3. Add drift tests showing the review payload rejects stale or widened runtime-execution input,
   including stale metadata, stale nested contract, nonzero real runtime counters, copied source
   packages, and stale source lineage fields.
4. Add static-boundary tests forbidding real runtime imports, dynamic import or execution escape
   hatches, builder calls, finalization, collision calls, existing Newton task smokes, USD
   inspection, benchmark timing APIs, and collision-quality calls inside the new helpers.
5. Implement the smallest report-only payload that passes those tests.

## Claim Boundary

Allowed wording:

- The report records a bounded runtime-lane claim-boundary review for one synthetic mapped-subset
  box lineage.
- The review preserves the skipped-runtime-execution boundary and keeps real runtime work blocked.
- All real Newton/Warp import, builder, shape-object, finalization, collision pipeline, and runtime
  counters remain zero.
- The next gate is a configured-runtime design contract before any real runtime work.

Forbidden wording:

- Newton support is implemented.
- Runtime execution ran or passed.
- Runtime compatibility is validated.
- Real builder calls were made or validated.
- A Newton model, engine shape object, or collision pipeline was created.
- The package is simulation-checked by this report path.
- Collision quality, benchmarks, deployment readiness, or safety certification are shown.
