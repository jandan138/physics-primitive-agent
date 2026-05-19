# CPD Paper Newton Engine-Builder Entry Contract Design

## Context

Before this slice, the report closed the bounded API-surface contract and reported
`paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract` as the next runtime-lane
gate. The prior consolidation record intentionally retired separate import-boundary-preflight and
import-contract gates because they would repeat the same evidence with diminishing audit value.

This slice implements that consolidated entry gate without crossing into real Newton runtime
execution.

## Goal

Add one bounded, report-only entry contract that consumes the API-surface row, checks the single
synthetic `paper_single_box` lineage, records an explicit no-runtime-entry decision for the
default no-config report, and advances the next gate to a later real engine-builder smoke
contract.

## Non-Goals

- No real `newton` or `warp` import.
- No `newton.ModelBuilder` instantiation.
- No real `add_shape_box` call.
- No model finalization.
- No collision pipeline creation or collision.
- No Newton runtime task execution.
- No bed/Franka or real-USD run.
- No benchmark, collision-quality, deployment, or safety claim.
- No re-introduction of standalone import-boundary-preflight/import-contract gates.

## Design

The implementation adds a new report payload:

```text
paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract
```

It consumes:

```text
paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract
```

The entry payload records one row for the existing synthetic mapped-subset `paper_single_box`
OBB/box lineage. The row carries the upstream API-surface row ID and all relevant source lineage
IDs, then records:

- `entry_decision: defer_real_runtime_entry`;
- `entry_decision_reason: default_no_config_source_dir_no_real_runtime_entry`;
- exact zero counters for real imports, `ModelBuilder`, builder shape calls, finalization,
  collision pipeline calls, and Newton runtime execution;
- `runtime_entry_allowed: false`;
- `runtime_entry_attempted: false`;
- `source_package_copy_forbidden: true`.

The report remains `partial` and `paper_faithful_offline_supported: false`. Closing this entry
contract only means the repository has recorded the conservative boundary decision for the current
single synthetic lineage.

## Next Gate

After the entry contract, the next runtime-lane gap becomes:

```text
paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract
```

That future gate is the first place where real Newton boundary crossing may be designed. This
entry slice must not perform that crossing.

## Tests

Use TDD:

1. Add failing tests that expect the report and CLI JSON to include the entry payload.
2. Add schema tests for the entry payload and row.
3. Add drift tests showing the entry payload rejects stale API-surface input.
4. Add static-boundary tests forbidding real runtime imports and builder/runtime calls inside the
   entry implementation.
5. Implement the smallest report-only payload that passes those tests.

## Claim Boundary

Allowed wording:

- The report records a bounded Newton engine-builder entry decision for one synthetic mapped-subset
  box lineage.
- The default entry decision defers real runtime entry and keeps all Newton runtime counters at
  zero.
- The next gate is a future engine-builder smoke contract.

Forbidden wording:

- Newton support is implemented.
- Runtime compatibility is validated.
- Real builder calls were made or validated.
- A Newton model or shape object was created.
- The package is simulation-checked.
- Collision quality, benchmarks, deployment readiness, or safety certification are shown.
