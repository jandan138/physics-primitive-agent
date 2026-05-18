# CPD Paper Mapped-Subset Newton Shape Runtime Engine-Builder Environment Probe Contract Design

## Summary

Implement the next bounded runtime-lane gate:
`paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract`.

This slice consumes the existing single-fixture
`paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract` row for
`paper_single_box` and records a Newton/Warp environment provenance probe contract. It is still a
report-only environment boundary, not a Newton engine-builder boundary crossing. It must not
instantiate `newton.ModelBuilder`, must not call real `add_shape_box`, must not create Newton
engine shape objects, must not finalize a model, must not create or collide a `CollisionPipeline`,
must not run contact/drop-settle/sphere-rain tasks, must not load real USD assets, must not
benchmark, and must not measure collision quality.

## Why This Slice Exists

The paper story has reached this point:

```text
paper-selected primitive
-> CollisionPackage-like artifact
-> runtime-admissibility static check
-> NewtonShapeMapping.to_dict() report record
-> data-only add_shape_box call plan
-> repo-local recording-builder call artifact
-> future-boundary checklist before real Newton ModelBuilder
```

The next useful gate is not simulation. It is a narrow environment/provenance gate that answers:

- where should the Newton source directory come from;
- can the report record Newton/Warp module provenance in a JSON-safe way;
- can the probe keep import/discovery state isolated from the rest of the report;
- can the report keep all builder/runtime/collision counters at zero.

In plain language: this gate may inspect whether Newton/Warp are discoverable from a configured
environment, but it still does not build a Newton model.

## Scope

In scope:

- One synthetic fixture only: `paper_single_box`.
- One Newton-native mapped kind only: `box`.
- One source row from the engine-builder boundary-preflight contract.
- A JSON-safe environment-probe row.
- A bounded module discoverability/provenance helper for `newton` and `warp`.
- Deterministic no-config behavior for the default offline report.
- Optional configured-source behavior for later CLI/config use.
- Exact lineage, counters, false/true flags, and remaining-gate accounting.

Out of scope:

- Returning live `newton` or `warp` module objects.
- Real Newton builder construction.
- Real builder shape calls.
- Newton engine shape objects.
- Model finalization.
- Collision pipeline creation or collision.
- Contact, drop-settle, or sphere-rain tasks.
- Real USD assets.
- Benchmarks, collision-quality metrics, deployment readiness, or safety certification.
- Any claim of full CPD reproduction or paper-faithful runtime behavior.

## Probe Boundary

The helper should prefer low-side-effect `importlib.util.find_spec()` provenance checks over
`importlib.import_module()`. It may insert a configured `source_dir` into `sys.path` only for the
duration of the probe, then restore `sys.path` and the cached `newton`/`warp` modules.

The default `build_cpd_paper_offline_report()` path should remain reproducible when no Newton
source directory is configured. In that default mode, the environment-probe row records
`source_dir_configured: False` and module rows with a `not_run_source_dir_not_configured` status.
That is still useful because the contract, lineage, forbidden runtime boundary, and next gate are
explicitly recorded without depending on the machine running the report.

## Proposed Next Gate

After this slice, the runtime-lane next gate should become:

```python
_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"
)
```

That later gate may check API-surface facts such as `newton.ModelBuilder` constructor visibility
and `add_shape_box` signature, but it still must not create a model, finalize, collide, run tasks,
load real USD assets, benchmark, or claim collision quality.

## Proposed Payload

The new payload should expose:

```python
{
    "gate_id": (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract"
    ),
    "gate_status": (
        "implemented_single_fixture_newton_engine_builder_environment_probe_only_partial"
    ),
    "closed_gate": (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract"
    ),
    "input_gate_id": (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract"
    ),
    "next_required_gate": (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"
    ),
    "decision": "remain_partial",
    "decision_reason": (
        "newton_engine_builder_environment_probe_complete_"
        "api_surface_contract_missing"
    ),
    "artifact_kind": (
        "newton_engine_builder_environment_probe_record_not_runtime_execution"
    ),
    "schema_version": 1,
    "source_scope": "synthetic_toy_fixtures_only",
    "implementation_boundary": (
        "single_synthetic_box_engine_builder_environment_probe_only_"
        "no_model_builder_no_shape_call_no_finalize_no_collision_pipeline_no_runtime"
    ),
}
```

The nested contract should explicitly state:

- one boundary-preflight row is required as input;
- Newton/Warp module provenance may be recorded as environment evidence;
- no Newton runtime support claim is allowed;
- no `newton.ModelBuilder` instantiation is allowed;
- no real builder shape call is allowed;
- no model finalization, collision pipeline creation, or runtime execution is allowed.

The row should include:

```python
{
    "newton_shape_runtime_engine_builder_environment_probe_row_id": (
        "newton_shape_runtime_engine_builder_environment_probe__paper_single_box__box"
    ),
    "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id": (
        "newton_shape_runtime_engine_builder_boundary_preflight__paper_single_box__box"
    ),
    "fixture_id": "paper_single_box",
    "target_newton_shape_kind": "box",
    "future_runtime_module_names": ["newton", "warp"],
    "environment_probe_status": "not_run_source_dir_not_configured",
    "environment_probe_claim_boundary": (
        "bounded_environment_provenance_probe_only_not_newton_runtime_execution"
    ),
    "newton_model_builder_instantiated_count": 0,
    "newton_builder_shape_call_count": 0,
    "newton_model_finalized_count": 0,
    "newton_collision_pipeline_created_count": 0,
    "newton_collision_pipeline_collide_count": 0,
    "newton_runtime_execution_count": 0,
}
```

## Static Boundary Requirements

The new gate helper block must not contain or call:

- `newton.ModelBuilder`
- `ModelBuilder(`
- `.add_shape_box(` on a real builder object
- `.finalize(`
- `CollisionPipeline`
- `.collide`
- `run_newton_contact_smoke`
- `run_newton_drop_settle`
- `run_newton_sphere_rain`
- real USD loaders
- benchmark or collision-quality measurement helpers

The provenance helper may use `importlib.util.find_spec()` and may mention the strings
`"newton"` and `"warp"`. It must not call `importlib.import_module()` for this gate.

## Claim Boundary

Allowed claim:

> The report now records a bounded Newton/Warp environment provenance probe contract for the
> single synthetic `paper_single_box` mapped subset.

Forbidden claims:

- Newton support is implemented.
- Newton runtime is validated.
- The package is simulation-checked.
- Collision quality is measured.
- The work reproduces the full CPD paper.
- Benchmarks or deployment readiness exist.
