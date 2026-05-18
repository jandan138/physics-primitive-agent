# CPD Paper Mapped-Subset Newton Shape Runtime Engine-Builder Boundary Preflight Contract Design

## Summary

Implement the next bounded runtime-lane gate:
`paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract`.

This slice consumes the existing single-fixture
`paper_mapped_subset_newton_shape_runtime_builder_construction_contract` row for `paper_single_box`
and records the checklist required before the project may cross into a real Newton engine-builder
boundary. It is still an offline/report-only preflight record. It must not import the real
`newton` or `warp` runtime packages, must not instantiate `newton.ModelBuilder`, must not call a
real Newton builder shape method, must not finalize a model, must not collide, and must not run
contact, drop-settle, sphere-rain, real-USD, benchmark, or collision-quality workflows.

## Why This Slice Exists

The paper story has reached this point:

```text
paper-selected primitive
-> CollisionPackage-like artifact
-> runtime-admissibility static check
-> NewtonShapeMapping.to_dict() report record
-> data-only add_shape_box call plan
-> repo-local recording-builder call artifact
```

The next useful gate is not real simulation. It is the last explicit checklist before a later
environment probe may import real Newton/Warp modules. In plain language:

- previous slice: "the repo-local dispatch helper can produce a fake `add_shape_box` call";
- this slice: "we know exactly what must be true before we are allowed to touch a real
  `newton.ModelBuilder` boundary";
- later slice: "probe the real Newton/Warp environment and module provenance without claiming
  collision quality."

## Scope

In scope:

- One synthetic fixture only: `paper_single_box`.
- One Newton-native mapped kind only: `box`.
- One source row from the builder-construction contract.
- A JSON-safe engine-builder boundary preflight row.
- A checklist of required future boundary checks: source-dir policy, module provenance, import
  isolation, builder constructor policy, model-finalize policy, collision-pipeline policy, and
  artifact review policy.
- Exact lineage, counters, false/true flags, and remaining-gate accounting.

Out of scope:

- Real Newton or real Warp import.
- `newton.ModelBuilder` instantiation.
- Real `add_shape_box` calls.
- Newton engine shape objects.
- Model finalization.
- `CollisionPipeline`.
- Runtime contact, drop/settle, or sphere-rain execution.
- Real USD assets.
- Benchmarks, collision-quality metrics, deployment readiness, or safety certification.
- Any claim of full CPD reproduction or paper-faithful runtime behavior.

## Proposed Contract

Add the next gate after this preflight:

```python
_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract"
)
```

The new payload should expose:

```python
{
    "gate_id": (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract"
    ),
    "gate_status": (
        "implemented_single_fixture_newton_engine_builder_boundary_preflight_only_partial"
    ),
    "closed_gate": (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract"
    ),
    "input_gate_id": (
        "paper_mapped_subset_newton_shape_runtime_builder_construction_contract"
    ),
    "next_required_gate": (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract"
    ),
    "decision": "remain_partial",
    "decision_reason": (
        "newton_engine_builder_boundary_preflight_complete_"
        "environment_probe_contract_missing"
    ),
    "artifact_kind": (
        "newton_engine_builder_boundary_preflight_record_not_runtime_execution"
    ),
    "schema_version": 1,
    "source_scope": "synthetic_toy_fixtures_only",
    "implementation_boundary": (
        "single_synthetic_box_engine_builder_boundary_preflight_only_"
        "no_real_newton_import_no_model_builder_no_shape_call_no_finalize_no_runtime"
    ),
    "runtime_engine_builder_boundary_preflight_action": (
        "record_real_newton_engine_builder_boundary_requirements_without_importing_newton"
    ),
}
```

The nested contract should explicitly state:

- previous builder-construction gate and one source row are required;
- one repo-local recording-builder call artifact is required as input evidence;
- real Newton import is not allowed in this gate;
- `newton.ModelBuilder` is not allowed in this gate;
- real builder shape calls are not allowed in this gate;
- model finalization, collision pipeline creation, and runtime execution are not allowed;
- the next gate is the real environment/provenance probe, not real simulation.

The single row should preserve source lineage and include a future-boundary checklist:

```python
{
    "newton_shape_runtime_engine_builder_boundary_preflight_row_id": (
        "newton_shape_runtime_engine_builder_boundary_preflight__paper_single_box__box"
    ),
    "source_newton_shape_runtime_builder_construction_row_id": (
        "newton_shape_runtime_builder_construction__paper_single_box__box"
    ),
    "fixture_id": "paper_single_box",
    "target_newton_shape_kind": "box",
    "future_newton_builder_constructor_name": "newton.ModelBuilder",
    "future_newton_builder_method_name": "add_shape_box",
    "future_runtime_module_names": ["newton", "warp"],
    "boundary_status": "preflight_recorded_not_crossed",
    "boundary_decision": "defer_real_engine_builder_boundary_to_environment_probe_gate",
    "blocked_until_gate": (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract"
    ),
    "required_before_engine_builder_boundary": [
        "newton_source_dir_resolved",
        "newton_module_provenance_checked",
        "warp_module_provenance_checked",
        "runtime_module_import_isolation_checked",
        "model_builder_constructor_signature_checked",
        "static_body_binding_policy_reviewed",
        "shape_call_signature_reviewed",
        "model_finalize_policy_deferred_to_later_gate",
        "collision_pipeline_policy_deferred_to_later_gate",
        "generated_collision_package_artifact_reviewed",
    ],
    "real_newton_import_count": 0,
    "newton_model_builder_instantiated_count": 0,
    "newton_builder_shape_call_count": 0,
    "newton_model_finalized_count": 0,
    "newton_runtime_execution_count": 0,
}
```

## Static Boundary Requirements

The new helper block must not contain or call:

- `importlib.import_module("newton")`
- `importlib.import_module("warp")`
- `import newton`
- `import warp`
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

The static test may inspect the new helper functions and the new payload helper source. It should
not forbid the existing string value `"newton.ModelBuilder"` when that value is used as future
checklist data; the forbidden pattern should target call syntax such as `ModelBuilder(`.

## Next Gate

After this slice, the report-level `next_required_gate` should become
`paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract`.

That later gate may inspect the configured Newton source directory and runtime module provenance.
It still should not claim collision quality, drop-settle success, contact correctness, benchmark
superiority, deployment readiness, or safety certification.
