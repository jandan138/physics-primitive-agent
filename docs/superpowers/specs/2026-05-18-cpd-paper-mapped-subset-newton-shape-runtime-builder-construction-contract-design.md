# CPD Paper Mapped-Subset Newton Shape Runtime Builder-Construction Contract Design

## Summary

Implement the next bounded runtime-lane gate:
`paper_mapped_subset_newton_shape_runtime_builder_construction_contract`.

This slice consumes the existing single-fixture
`paper_mapped_subset_newton_shape_runtime_builder_preflight_contract` row for `paper_single_box`
and exercises the repo-local static shape builder dispatch path with a recording builder and a
fake Warp-like module. The output is a JSON-safe recorded builder-call artifact.

This is not a real Newton engine call. The helper block may import the repo-local
`primitive_collision_compiler.newton.diagnostics` helper, but it must not import the real `newton`
or `warp` runtime packages, must not instantiate `newton.ModelBuilder`, must not finalize a model,
must not create a `CollisionPipeline`, must not run contact/drop/sphere-rain diagnostics, must not
load real USD, must not run a benchmark, and must not measure collision quality.

The broader `cpd_paper.offline` import path already preloads repo-local Newton diagnostic modules
through existing package imports, so this slice must not claim module-level no-Newton import. The
claim is narrower: no real Newton/Warp runtime import or engine object is created by the new
builder-construction helper block.

## Why This Slice Exists

The current paper story has reached this point:

```text
paper-selected primitive
-> CollisionPackage-like artifact
-> runtime-admissibility static check
-> NewtonShapeMapping.to_dict() report record
-> data-only add_shape_box call plan
```

The next useful gate is to prove that the planned box call can flow through the existing repo-local
Newton diagnostic shape-dispatch helper without crossing into the real Newton runtime. In plain
language:

- previous slice: "we know which future builder method and scalar fields would be used";
- this slice: "we can feed the mapping into the repo-local dispatch function and record the exact
  fake-builder call it would make";
- later slice: "separately decide whether to cross the real Newton/Warp import and engine-builder
  boundary."

## Scope

In scope:

- One synthetic fixture only: `paper_single_box`.
- One mapped Newton-native kind only: `box`.
- One repo-local helper path only: `primitive_collision_compiler.newton.diagnostics._add_static_shape`.
- One recording builder method call: `add_shape_box`.
- One fake Warp-like module that returns JSON-safe vector, matrix, quaternion, and transform records.
- Exact input validation against the builder-preflight payload.
- Exact output schema, row schema, counters, lineage, and false/true boundary flags.

Out of scope:

- Real Newton or real Warp import.
- `newton.ModelBuilder`.
- Newton engine shape objects.
- Model finalization.
- `CollisionPipeline`.
- Runtime contact, drop/settle, or sphere-rain execution.
- Real USD assets.
- Benchmarks, collision-quality metrics, deployment readiness, or safety certification.
- Paper-only primitives outside the Newton-native mapped subset.

## Proposed Report Contract

Add the next gate constant:

```python
_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract"
)
```

The builder-construction payload should have:

```python
{
    "gate_id": "paper_mapped_subset_newton_shape_runtime_builder_construction_contract",
    "gate_status": "implemented_single_fixture_repo_local_recording_builder_construction_only_partial",
    "closed_gate": "paper_mapped_subset_newton_shape_runtime_builder_construction_contract",
    "input_gate_id": "paper_mapped_subset_newton_shape_runtime_builder_preflight_contract",
    "next_required_gate": (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract"
    ),
    "decision": "remain_partial",
    "decision_reason": (
        "repo_local_recording_builder_construction_complete_"
        "engine_builder_boundary_preflight_contract_missing"
    ),
    "artifact_kind": "repo_local_recording_builder_call_not_newton_engine_shape",
    "schema_version": 1,
    "source_scope": "synthetic_toy_fixtures_only",
    "implementation_boundary": (
        "single_synthetic_box_repo_local_recording_builder_only_"
        "no_real_newton_import_no_engine_shape_no_model_finalize_no_runtime"
    ),
    "runtime_builder_construction_action": (
        "call_repo_local_static_shape_helper_with_recording_builder_and_fake_wp"
    ),
    "newton_shape_runtime_builder_construction_contract": {
        "input_gate_required": (
            "paper_mapped_subset_newton_shape_runtime_builder_preflight_contract"
        ),
        "closed_gate": (
            "paper_mapped_subset_newton_shape_runtime_builder_construction_contract"
        ),
        "next_engine_builder_boundary_preflight_gate_required": (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract"
        ),
        "source_builder_preflight_rows_required": 1,
        "repo_local_recording_builder_calls_required": 1,
        "real_newton_import_allowed": False,
        "newton_model_builder_allowed": False,
        "newton_engine_shape_object_allowed": False,
        "newton_runtime_allowed": False,
        "newton_support_claim_allowed": False,
    },
}
```

The single construction row should include:

```python
{
    "newton_shape_runtime_builder_construction_row_id": (
        "newton_shape_runtime_builder_construction__paper_single_box__box"
    ),
    "source_newton_shape_runtime_builder_preflight_row_id": (
        "newton_shape_runtime_builder_preflight__paper_single_box__box"
    ),
    "source_newton_shape_runtime_construction_row_id": (
        "newton_shape_runtime_construction__paper_single_box__box"
    ),
    "source_shape_mapping_row_id": "newton_shape_mapping__paper_single_box__box",
    "source_package_id": (
        "paper_single_box:paper_mapped_subset_collision_package_generation_contract"
    ),
    "fixture_id": "paper_single_box",
    "paper_primitive": "oriented_bounding_box",
    "primitive_spec_kind": "box",
    "primitive_id": "paper_single_box__oriented_bounding_box__box",
    "target_newton_shape_kind": "box",
    "constructed_newton_shape_mapping_dict": {
        "primitive_id": "paper_single_box__oriented_bounding_box__box",
        "kind": "box",
        "status": "mapped",
        "detail": "mapped",
        "center": [1.0, 0.5, 0.25],
        "axes": [
            [0.0, 0.0, 1.0],
            [8.000013929428336e-07, 0.99999999999968, 0.0],
            [-0.99999999999968, 8.000013929428336e-07, 0.0],
        ],
        "dimensions": {"half_extents": [0.25, 0.5000008000012329, 1.0000004000003766]},
    },
    "repo_local_static_shape_helper": "_add_static_shape",
    "repo_local_static_shape_helper_called": True,
    "recording_builder_kind": "repo_local_recording_builder_not_newton_model_builder",
    "recording_builder_shape_call_count": 1,
    "recorded_builder_method_name": "add_shape_box",
    "recorded_builder_call": {
        "method": "add_shape_box",
        "body": -1,
        "hx": 0.25,
        "hy": 0.5000008000012329,
        "hz": 1.0000004000003766,
        "xform": {
            "kind": "fake_wp_transform",
            "translation": [1.0, 0.5, 0.25],
            "rotation": {
                "kind": "fake_wp_quat_from_matrix",
                "matrix": {
                    "kind": "fake_wp_matrix_from_cols",
                    "cols": [
                        [0.0, 0.0, 1.0],
                        [8.000013929428336e-07, 0.99999999999968, 0.0],
                        [-0.99999999999968, 8.000013929428336e-07, 0.0],
                    ],
                },
            },
        },
    },
    "newton_builder_shape_call_count": 0,
    "newton_engine_shape_object_count": 0,
    "newton_model_finalized_count": 0,
    "newton_runtime_execution_count": 0,
}
```

## Validation Requirements

The implementation must reject:

- Wrong input `gate_id`.
- Wrong input `next_required_gate`.
- Missing or false previous builder-preflight record flags.
- Any previous builder-preflight false flag set to true.
- Any input count drift for package, mapping, builder-plan, builder-call, engine-shape, runtime,
  real-USD, benchmark, and collision-quality counters.
- Zero or multiple source rows.
- Source-row lineage drift.
- Source mapping drift.
- Builder call plan drift, including wrong method, wrong dimensions, unexpected callable, non-JSON
  value, or forbidden real-runtime transform object.
- Source package copies appearing in the payload.

## Static Boundary Requirements

The new helper block may reference the repo-local diagnostic helper
`primitive_collision_compiler.newton.diagnostics._add_static_shape`.

The new helper block must not contain:

- `importlib.import_module("newton")`
- `importlib.import_module("warp")`
- `newton.ModelBuilder`
- `CollisionPipeline`
- `.finalize(`
- `pipeline.collide`
- `run_newton_contact_smoke`
- `run_newton_drop_settle`
- `run_newton_sphere_rain`
- `load_first_mesh`
- `inspect_usd_asset`
- benchmark or timing calls

`add_shape_box` is allowed only as the method implemented by the recording builder and the recorded
method name. It is not evidence of a real Newton engine shape object.

## Documentation Requirements

Update:

- `README.md`
- `docs/index.md`
- `docs/deepdive/evidence-status.md`
- `docs/deepdive/message-map.md`
- `docs/reference/claim-boundaries.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/records/README.md`
- a new dated record:
  `docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-builder-construction-contract.md`

All docs must say this is repo-local recording-builder evidence only. It is not real Newton runtime
evidence, not Newton support, not collision quality, not benchmark evidence, not real-USD evidence,
not deployment readiness, and not safety certification.

## Verification Commands

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_builder_construction or cpd_paper_offline_report_next_gate or cli_run_cpd_paper_offline_report' -q
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -q
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```
