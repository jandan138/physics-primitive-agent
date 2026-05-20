# CPD Paper Newton Engine-Builder Configured-Runtime Design Contract Design

## Context

The current `cpd_paper_offline_report` closes the report-only Newton engine-builder runtime-lane
review contract for the single synthetic `paper_single_box` OBB/box lineage. That contract records
`runtime_lane_review_decision: keep_real_runtime_execution_blocked`, keeps runtime compatibility
unvalidated, keeps every real runtime/import/builder/finalization/collision counter at zero, and
reports `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract`
as the next required gate.

This slice closes that configured-runtime design gate as a report-only input-design record. It
defines the configuration and lineage fields that a later preflight must check before any real
runtime import can even be considered. It must not read a user runtime config, import Newton/Warp,
instantiate `newton.ModelBuilder`, run a smoke, or reinterpret the review record as compatibility.

## Approaches Considered

1. **Recommended: report-only configured-runtime input design.** Consume the runtime-lane review
   payload, verify the same single lineage and zero real runtime counters, record the required
   Newton source, diagnostic-device, runtime-decision, smoke-policy, execution-policy, and package
   lineage inputs for a later configured-runtime preflight, and advance to that preflight gate.
   This keeps the lane moving while preserving claim boundaries.
2. **Configured-runtime preflight now.** Read actual runtime config values and resolve source/device
   inputs in this slice. This is too broad because the current gate is explicitly a design gate, not
   a config validation gate, and would conflate design with preflight evidence.
3. **Real runtime entry.** Attempt a Newton/Warp import or `newton.ModelBuilder` construction once
   the design is recorded. This violates the existing runtime-lane review boundary and would create
   unsupported Newton readiness or compatibility claims.

## Goal

Add one bounded report-only configured-runtime design contract that consumes the runtime-lane review
payload, records the exact runtime inputs a later preflight must validate, keeps all real runtime
work blocked, and advances to a future configured-runtime preflight contract.

## Non-Goals

- No real `newton` or `warp` import.
- No runtime config file read or environment-variable expansion from this report path.
- No `newton.ModelBuilder` instantiation.
- No real `add_shape_box` call.
- No Newton engine shape object creation.
- No model finalization.
- No collision pipeline creation or collision.
- No Newton contact, drop/settle, sphere-rain, or runtime-execution task.
- No real-USD evaluation.
- No benchmark or collision-quality measurement.
- No claim that Newton support, runtime compatibility, deployment readiness, or safety certification
  is validated.
- No broadening beyond the existing `paper_single_box` lineage.

## Design

The implementation adds a new report payload:

```text
paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract
```

It consumes:

```text
paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract
```

The payload records one row for the existing synthetic mapped-subset `paper_single_box` OBB/box
lineage. The row carries the upstream runtime-lane review row ID and all source lineage IDs, then
records:

- `configured_runtime_design_decision: define_configured_runtime_inputs_keep_real_runtime_blocked`;
- `configured_runtime_design_reason: runtime_input_design_recorded_preflight_missing`;
- `configured_runtime_design_status: input_design_recorded`;
- `configured_runtime_design_recorded: true`;
- `configured_runtime_preflight_ready: false`;
- `runtime_source_configuration_required: true`;
- `runtime_device_configuration_required: true`;
- `runtime_entry_decision_required: true`;
- `runtime_smoke_policy_required: true`;
- `runtime_execution_policy_required: true`;
- `required_config_keys: ["newton.source_dir", "newton_diagnostic.device"]`;
- `required_runtime_inputs: ["newton_source_dir", "newton_diagnostic_device",
  "runtime_entry_decision", "runtime_smoke_policy", "runtime_execution_policy",
  "package_lineage_id"]`;
- `runtime_entry_decision_policy: require_configured_runtime_preflight_before_entry`;
- `runtime_smoke_policy: skip_until_configured_runtime_preflight_passes`;
- `runtime_execution_policy: skip_until_configured_runtime_preflight_passes`;
- exact zero counters for real imports, `ModelBuilder`, engine shape objects, real builder shape
  calls, model finalization, collision pipeline calls, runtime-execution attempts, and Newton
  runtime execution;
- `source_package_copy_forbidden: true`.

The payload closes only the configured-runtime design gate as a report-only record. The report
remains `partial` and `paper_faithful_offline_supported: false`.

## Next Gate

After this contract, the next runtime-lane gap becomes:

```text
paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract
```

That future preflight gate may validate explicit config values and lineage readiness, but it still
must not imply Newton support, runtime compatibility, benchmark evidence, or collision quality unless
a later standard and record explicitly support those claims.

## Tests

Use TDD:

1. Add a failing report/CLI test that expects the configured-runtime design payload and advances the
   top-level next gate to the configured-runtime preflight contract.
2. Add exact schema tests for the configured-runtime design payload and row.
3. Add drift tests showing the design payload rejects stale or widened runtime-lane review input,
   including stale metadata, stale nested contract, nonzero real runtime counters, copied source
   packages, compatibility wording, and stale source lineage fields.
4. Add static-boundary tests forbidding real runtime imports, dynamic import or execution escape
   hatches, builder calls, finalization, collision calls, existing Newton task smokes, USD
   inspection, benchmark timing APIs, and collision-quality calls inside the new helpers.
5. Implement the smallest report-only payload that passes those tests.

## Documentation

Update the DeepDive and reference docs so the current next gate becomes the configured-runtime
preflight contract. Add a dated record under `docs/records/` that captures baseline evidence, RED and
GREEN test evidence, multi-agent review findings, final verification, and claim boundaries.

Also fix two stale documentation boundaries identified during design review:

- `docs/index.md` command-summary text must include the already-closed runtime-lane review contract
  between the skipped-runtime-execution contract and the configured-runtime design/preflight gate.
- README wording must qualify "No generated collision artifact pipeline" as no production or general
  generated collision artifact pipeline beyond the one synthetic report-scoped box
  `CollisionPackage.to_dict()` artifact.

## Claim Boundary

Allowed wording:

- The report records a bounded configured-runtime input-design contract for one synthetic
  mapped-subset box lineage.
- The design lists the inputs a later configured-runtime preflight must validate before real runtime
  entry can be considered.
- All real Newton/Warp import, builder, shape-object, finalization, collision pipeline, and runtime
  counters remain zero.
- The next gate is a configured-runtime preflight contract.

Forbidden wording:

- Newton support is implemented.
- Runtime execution ran or passed.
- Runtime compatibility is validated.
- A runtime config was validated by this report path.
- Real builder calls were made or validated.
- A Newton model, engine shape object, or collision pipeline was created.
- The package is simulation-checked by this report path.
- Collision quality, benchmarks, deployment readiness, or safety certification are shown.
