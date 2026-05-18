# CPD Paper Mapped-Subset Newton Shape Runtime-Builder Preflight Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the bounded offline/report-only `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract` gate after the existing Newton shape runtime-construction gate.

**Architecture:** Extend `build_cpd_paper_offline_report()` by consuming exactly one runtime-construction row and emitting exactly one data-only Newton builder-call plan for the existing `paper_single_box` box mapping record. The gate must remain offline/static: no Newton or warp import, no `ModelBuilder`, no `add_shape_*` call, no runtime pose construction, no model finalization, no USD, no benchmark, and no collision-quality measurement.

**Tech Stack:** Python, pytest, Markdown docs, existing `primitive_collision_compiler.baselines.cpd_paper.offline` report builders, existing `NewtonShapeMapping.to_dict()` report records.

---

## File Structure

- Modify `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
  - Add `_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT`.
  - Add `_paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_builder_preflight()`.
  - Add builder-preflight false/true flags, input validation helpers, builder-call-plan helper, row helper, coverage helper, and payload helper.
  - Wire the payload into `build_cpd_paper_offline_report()`.
- Modify `tests/test_cpd_paper_offline.py`
  - Add expected next-gate constants, required key sets, positive payload tests, drift tests, and static boundary tests.
  - Update the current top-level next gate from builder preflight to builder construction.
- Modify `tests/test_cli.py`
  - Update offline report CLI expectations and add assertions for the builder-preflight payload.
- Modify docs:
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
  - Create `docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-builder-preflight-contract.md`

## Task 1: RED Top-Level Gate And Schema Tests

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`

- [ ] **Step 1: Add the next gate constant**

Add this next to the existing runtime-builder-preflight constant:

```python
EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_builder_construction_contract"
)
EXPECTED_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT,
]
```

Change:

```python
EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT,
]
```

to:

```python
EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT,
]
```

- [ ] **Step 2: Add builder-preflight key sets**

Add the false and true flag sets:

```python
NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_FALSE_FLAGS = (
    "paper_faithful_offline_allowed",
    "paper_faithful_offline_supported",
    "newton_support_claimed",
    "approximation_policy_applied",
    "real_usd_loaded",
    "benchmark_run",
    "collision_quality_measured",
    "deployment_or_certification_claimed",
    "package_generation_triggered",
    "newton_runtime_triggered",
    "real_usd_triggered",
    "benchmark_triggered",
    "newton_runtime_allowed",
    "approximation_policy_enabled",
    "silent_drop_allowed",
    "mapping_attempted",
    "newton_shape_mapping_triggered",
    "newton_shape_object_created",
    "newton_shape_runtime_construction_triggered",
    "newton_shape_runtime_boundary_crossed",
    "newton_engine_shape_object_created",
    "newton_builder_shape_called",
    "newton_runtime_builder_invoked",
    "newton_model_builder_instantiated",
    "newton_model_finalized",
)

NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_TRUE_FLAGS = (
    "newton_shape_runtime_builder_preflight_recorded",
    "repo_local_newton_builder_call_plan_record_created",
)
```

Add exact payload and row key sets with the fields from the design spec:

```python
NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "runtime_builder_preflight_action",
    "newton_shape_runtime_builder_preflight_contract",
    "input_contract_summary",
    "newton_shape_runtime_builder_preflight_row_count",
    "source_newton_shape_runtime_construction_row_count",
    "source_newton_shape_mapping_record_count",
    "runtime_builder_preflight_passed",
    "runtime_builder_preflight_passed_count",
    "builder_call_plan_count",
    "builder_call_allowed_count",
    "later_newton_shape_runtime_builder_candidate_count",
    "newton_mapping_record_count",
    "newton_mapper_call_count",
    "newton_shape_object_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_runtime_execution_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "offline_static_runtime_admissibility_check_count",
    "report_scoped_newton_shape_descriptor_count",
    "later_newton_shape_runtime_construction_candidate_count",
    "constructed_newton_shape_mapping_record_count",
    "newton_shape_runtime_builder_preflight_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_TRUE_FLAGS,
}
```

Add the exact row key set. Do not use "same as previous row" shorthand:

```python
NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_ROW_REQUIRED_KEYS = {
    "newton_shape_runtime_builder_preflight_row_id",
    "source_newton_shape_runtime_construction_row_id",
    "source_newton_shape_runtime_boundary_preflight_row_id",
    "source_shape_mapping_row_id",
    "source_newton_shape_mapping_preflight_row_id",
    "source_runtime_admissibility_row_id",
    "source_package_id",
    "source_asset_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "primitive_id",
    "target_newton_shape_kind",
    "descriptor_kind",
    "descriptor_center",
    "descriptor_axes",
    "descriptor_half_extents",
    "constructed_newton_shape_mapping_dict",
    "constructed_newton_shape_mapping_status",
    "constructed_newton_shape_mapping_detail",
    "mapping_constructor",
    "mapping_constructor_input_kind",
    "runtime_builder_preflight_passed",
    "builder_call_allowed",
    "builder_candidate_kind",
    "builder_shape_kind",
    "builder_method_name",
    "call_signature_fields",
    "body_binding_policy",
    "deferred_xform_policy",
    "deferred_translation_inputs",
    "deferred_rotation_inputs",
    "dimension_source",
    "builder_center",
    "builder_axes",
    "builder_half_extents",
    "builder_dimension_argument_schema",
    "builder_call_plan",
    "builder_call_plan_count",
    "later_newton_shape_runtime_builder_candidate",
    "runtime_builder_construction_contract_candidate",
    "constructed_newton_shape_mapping_record_count",
    "newton_mapping_record_count",
    "newton_mapper_call_count",
    "newton_shape_object_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_runtime_execution_count",
    *NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_TRUE_FLAGS,
}
```

- [ ] **Step 3: Add the input helper**

Add near `_newton_shape_runtime_construction_input()`:

```python
def _newton_shape_runtime_builder_preflight_input() -> dict[str, object]:
    report = build_cpd_paper_offline_report()
    return json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_construction_contract"
            ]
        )
    )
```

- [ ] **Step 4: Add positive tests that initially fail**

Add tests that assert:

```python
report["next_required_gate"] == (
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT
)
report["failure_labels"] == [
    "paper_mapped_subset_newton_shape_runtime_builder_construction_contract_missing",
]
report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
    EXPECTED_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_REMAINING_GAPS
)
```

Add a payload schema test that asserts:

```python
payload = report[
    "paper_mapped_subset_newton_shape_runtime_builder_preflight_contract"
]
assert set(payload) == NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_PAYLOAD_REQUIRED_KEYS
assert payload["gate_id"] == (
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT
)
assert payload["input_gate_id"] == (
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
)
assert payload["next_required_gate"] == (
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT
)
assert payload["runtime_builder_preflight_passed"] is True
assert payload["runtime_builder_preflight_passed_count"] == 1
assert payload["builder_call_plan_count"] == 1
assert payload["builder_call_allowed_count"] == 0
assert payload["newton_builder_shape_call_count"] == 0
assert payload["newton_engine_shape_object_count"] == 0
assert payload["newton_runtime_execution_count"] == 0
```

Also assert the nested contract dict exactly:

```python
assert payload["newton_shape_runtime_builder_preflight_contract"] == {
    "input_gate_required": (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
    ),
    "closed_gate": (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT
    ),
    "next_newton_shape_runtime_builder_construction_gate_required": (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT
    ),
    "source_runtime_construction_rows_required": 1,
    "builder_call_plans_required": 1,
    "newton_engine_shape_object_allowed": False,
    "newton_builder_shape_call_allowed": False,
    "newton_runtime_allowed": False,
    "newton_support_claim_allowed": False,
}
```

Assert the exact input summary:

```python
source_row = report[
    "paper_mapped_subset_newton_shape_runtime_construction_contract"
]["newton_shape_runtime_construction_rows"][0]
assert payload["input_contract_summary"] == {
    "input_gate_id": (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
    ),
    "input_next_required_gate": (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT
    ),
    "source_newton_shape_runtime_construction_row_id": (
        source_row["newton_shape_runtime_construction_row_id"]
    ),
    "source_newton_shape_runtime_boundary_preflight_row_id": source_row[
        "source_newton_shape_runtime_boundary_preflight_row_id"
    ],
    "source_shape_mapping_row_id": source_row["source_shape_mapping_row_id"],
    "source_package_id": source_row["source_package_id"],
    "source_fixture_id": "paper_single_box",
    "source_primitive_id": source_row["primitive_id"],
    "source_target_newton_shape_kind": "box",
    "source_mapping_constructor": "NewtonShapeMapping",
    "input_runtime_builder_preflight_candidate_count": 1,
}
```

- [ ] **Step 5: Run focused tests and confirm RED**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_builder_preflight or cpd_paper_offline_report_next_gate' -q
```

Expected: failing tests because the payload and new next gate are not implemented yet.

## Task 2: RED Builder Plan, Drift, And Static Boundary Tests

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`

- [ ] **Step 1: Add row content assertions**

Add a row test with this expected builder plan:

```python
expected_plan = {
    "method": "add_shape_box",
    "call_signature_fields": ["body", "xform", "hx", "hy", "hz"],
    "body_binding_policy": (
        "static_package_or_probe_uses_body_minus_one_"
        "drop_settle_uses_created_body_id"
    ),
    "deferred_xform_policy": (
        "future_runtime_may_derive_xform_from_center_and_axes"
    ),
    "deferred_translation_inputs": (
        "mapping_center_only_no_runtime_transform_constructed"
    ),
    "deferred_rotation_inputs": (
        "mapping_axes_only_no_quat_or_runtime_rotation_constructed"
    ),
    "dimension_arguments": {"hx": 1.0, "hy": 0.5, "hz": 0.25},
}
assert row["builder_method_name"] == "add_shape_box"
assert row["call_signature_fields"] == ["body", "xform", "hx", "hy", "hz"]
assert row["builder_call_plan"] == expected_plan
assert row["builder_call_allowed"] is False
assert row["runtime_builder_construction_contract_candidate"] is True
```

Use the actual source row's half-extents rather than hardcoding if the current fixture values differ.

- [ ] **Step 2: Add coverage summary assertions**

Assert exactly:

```python
assert payload["coverage_summary"] == {
    "newton_shape_runtime_builder_preflight_row_count": 1,
    "source_newton_shape_runtime_construction_row_count": 1,
    "source_newton_shape_mapping_record_count": 1,
    "runtime_builder_preflight_passed_count": 1,
    "builder_call_plan_count": 1,
    "builder_call_allowed_count": 0,
    "later_newton_shape_runtime_builder_candidate_count": 1,
    "constructed_newton_shape_mapping_record_count": 1,
    "newton_mapping_record_count": 1,
    "newton_mapper_call_count": 0,
    "newton_shape_object_count": 0,
    "newton_engine_shape_object_count": 0,
    "newton_builder_shape_call_count": 0,
    "newton_runtime_execution_count": 0,
    "fixture_id_distribution": {"paper_single_box": 1},
    "target_newton_shape_kind_distribution": {"box": 1},
    "builder_method_distribution": {"add_shape_box": 1},
}
```

- [ ] **Step 3: Add drift tests**

Add parametrized tests for:

```python
("gate_id", "stale_gate", "newton_shape_runtime_builder_preflight_input_gate_id_mismatch")
("next_required_gate", "stale_gate", "newton_shape_runtime_builder_preflight_input_next_gate_mismatch")
("newton_shape_runtime_construction_row_count", 2, "newton_shape_runtime_builder_preflight_input_count_mismatch:newton_shape_runtime_construction_row_count")
("source_newton_shape_runtime_boundary_preflight_row_count", 2, "newton_shape_runtime_builder_preflight_input_count_mismatch:source_newton_shape_runtime_boundary_preflight_row_count")
("newton_mapping_record_count", 2, "newton_shape_runtime_builder_preflight_input_count_mismatch:newton_mapping_record_count")
("newton_mapper_call_count", 1, "newton_shape_runtime_builder_preflight_input_count_mismatch:newton_mapper_call_count")
("newton_shape_object_count", 1, "newton_shape_runtime_builder_preflight_input_count_mismatch:newton_shape_object_count")
("constructed_newton_shape_mapping_record_count", 2, "newton_shape_runtime_builder_preflight_input_count_mismatch:constructed_newton_shape_mapping_record_count")
("generated_runtime_primitive_spec_count", 2, "newton_shape_runtime_builder_preflight_input_count_mismatch:generated_runtime_primitive_spec_count")
("generated_primitive_spec_count", 2, "newton_shape_runtime_builder_preflight_input_count_mismatch:generated_primitive_spec_count")
("generated_collision_package_count", 2, "newton_shape_runtime_builder_preflight_input_count_mismatch:generated_collision_package_count")
("runtime_admissibility_check_count", 2, "newton_shape_runtime_builder_preflight_input_count_mismatch:runtime_admissibility_check_count")
("offline_static_runtime_admissibility_check_count", 2, "newton_shape_runtime_builder_preflight_input_count_mismatch:offline_static_runtime_admissibility_check_count")
("report_scoped_newton_shape_descriptor_count", 2, "newton_shape_runtime_builder_preflight_input_count_mismatch:report_scoped_newton_shape_descriptor_count")
("later_newton_shape_runtime_construction_candidate_count", 2, "newton_shape_runtime_builder_preflight_input_count_mismatch:later_newton_shape_runtime_construction_candidate_count")
("newton_builder_shape_call_count", 1, "newton_shape_runtime_builder_preflight_input_count_mismatch:newton_builder_shape_call_count")
("newton_engine_shape_object_count", 1, "newton_shape_runtime_builder_preflight_input_count_mismatch:newton_engine_shape_object_count")
("newton_runtime_execution_count", 1, "newton_shape_runtime_builder_preflight_input_count_mismatch:newton_runtime_execution_count")
```

Add row drift tests for:

```python
"newton_shape_runtime_construction_row_id"
"source_newton_shape_runtime_boundary_preflight_row_id"
"source_shape_mapping_row_id"
"source_newton_shape_mapping_preflight_row_id"
"source_runtime_admissibility_row_id"
"source_package_id"
"source_asset_id"
"fixture_id"
"paper_primitive"
"primitive_spec_kind"
"primitive_id"
"target_newton_shape_kind"
"descriptor_kind"
"mapping_constructor"
"mapping_constructor_input_kind"
"runtime_builder_preflight_candidate"
"newton_builder_shape_call_count"
"newton_engine_shape_object_count"
"newton_runtime_execution_count"
```

For each row drift case, mutate the single row in
`payload["newton_shape_runtime_construction_rows"]`, call
`cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_builder_preflight_contract_payload(payload)`,
and expect `newton_shape_runtime_builder_preflight_source_row_mismatch:<field>`.

Add mapping dict drift tests for:

- exact mapping key set:
  `newton_shape_runtime_builder_preflight_mapping_key_mismatch`;
- exact `dimensions` key set:
  `newton_shape_runtime_builder_preflight_mapping_dimensions_key_mismatch`;
- valid-looking but wrong `primitive_id`, `kind`, `status`, `detail`, `center`, `axes`, and
  `half_extents` values:
  `newton_shape_runtime_builder_preflight_mapping_mismatch:<field>`;
- invalid center:
  `newton_shape_runtime_builder_preflight_mapping_invalid:center`;
- invalid axes:
  `newton_shape_runtime_builder_preflight_mapping_invalid:axes`;
- invalid half-extents:
  `newton_shape_runtime_builder_preflight_mapping_invalid:half_extents`.

- [ ] **Step 4: Add static boundary test**

Add a static test over the new helpers:

```python
helpers = (
    cpd_paper_offline._paper_newton_shape_runtime_builder_preflight_source_row,
    cpd_paper_offline._paper_validate_newton_shape_runtime_builder_preflight_mapping,
    cpd_paper_offline._paper_newton_shape_runtime_builder_call_plan,
    cpd_paper_offline._paper_newton_shape_runtime_builder_preflight_row,
    cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_builder_preflight_contract_payload,
)
source = "\n".join(inspect.getsource(helper) for helper in helpers)
```

This static source check must inspect only the new builder-preflight helpers. Separately assert the
generated report output counters remain zero; do not treat `inspect.getsource(build_cpd_paper_offline_report)`
as proof of no transitive runtime work.

Forbid:

```python
(
    "primitive_collision_compiler.newton",
    "import newton",
    "from newton",
    "import warp",
    "from warp",
    "import newton_warp",
    "newton_warp",
    "importlib",
    "__import__",
    "getattr(",
    "callable(",
    "eval(",
    "exec(",
    "newton.ModelBuilder",
    "ModelBuilder",
    "CollisionPipeline",
    "add_shape_",
    "add_shape_box(",
    "add_shape_sphere(",
    "add_shape_capsule(",
    "add_shape_cylinder(",
    "add_shape_cone(",
    "add_shape_ellipsoid(",
    ".add_shape_",
    "builder.",
    "model_builder.",
    "builder.finalize",
    "model_builder.finalize",
    ".finalize(",
    "pipeline.collide",
    "wp.transform",
    "wp.quat",
    "warp.transform",
    "warp.quat",
    "transformf",
    "quat_from",
    "CollisionPackage(",
    "PrimitiveSpec(",
    "load_first_mesh",
    "inspect_usd_asset",
    "real_usd_comparison",
    "timeit",
    "perf_counter",
    "benchmark_metric",
    "collision_quality_score",
    "run_benchmark",
    "measure_collision_quality",
)
```

Add an output-data assertion that the builder plan is JSON-like data:

```python
json.dumps(row["builder_call_plan"])

def _contains_callable(value: object) -> bool:
    if callable(value):
        return True
    if isinstance(value, dict):
        return any(_contains_callable(item) for item in value.values())
    if isinstance(value, list | tuple):
        return any(_contains_callable(item) for item in value)
    return False

assert _contains_callable(row["builder_call_plan"]) is False
```

Add another assertion that no constructed runtime pose data appears. Allow `"xform"` only in
`call_signature_fields`; forbid these keys recursively in the row and nested plan:

```python
forbidden_runtime_pose_keys = {
    "builder_xform",
    "runtime_xform",
    "xform_value",
    "transform",
    "runtime_transform",
    "quat",
    "quaternion",
    "rotation_quat",
    "orientation_quaternion",
}
```

Also assert:

```python
payload = build_cpd_paper_offline_report()[
    "paper_mapped_subset_newton_shape_runtime_builder_preflight_contract"
]
assert payload["newton_builder_shape_call_count"] == 0
assert payload["newton_engine_shape_object_count"] == 0
assert payload["newton_runtime_execution_count"] == 0
```

- [ ] **Step 5: Run focused tests and confirm RED**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_builder_preflight' -q
```

Expected: failing tests because no implementation exists.

## Task 3: GREEN Offline Payload Implementation

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add constants and remaining-gap helper**

Add:

```python
_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_builder_construction_contract"
)
```

Add:

```python
def _paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_builder_preflight() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT]
```

Update `build_cpd_paper_offline_report()` so `runtime_lane_remaining_gates` uses that helper after
the new builder-preflight payload is created.

- [ ] **Step 2: Add flags and input validation helpers**

Add `_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_PAYLOAD_FALSE_FLAGS` and
`_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_TRUE_FLAGS` matching the tests.

Implement:

```python
def _paper_newton_shape_runtime_builder_preflight_false_flags() -> dict[str, bool]:
    return {
        flag: False
        for flag in _NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_PAYLOAD_FALSE_FLAGS
    }


def _paper_newton_shape_runtime_builder_preflight_true_flags() -> dict[str, bool]:
    return {
        flag: True
        for flag in _NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_TRUE_FLAGS
    }
```

Implement `_paper_newton_shape_runtime_builder_preflight_source_row(construction)` by mirroring
the prior source-row validators:

```python
if construction.get("gate_id") != _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT:
    raise ValueError("newton_shape_runtime_builder_preflight_input_gate_id_mismatch")
if construction.get("next_required_gate") != _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT:
    raise ValueError("newton_shape_runtime_builder_preflight_input_next_gate_mismatch")
```

Use `_paper_validate_primitivespec_runtime_construction_false_flags()` with
`_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_PAYLOAD_FALSE_FLAGS` for required input flags. For new
builder-preflight-only flags, reject only if present and true.

Validate this exact payload count contract:

```python
expected_counts = {
    "newton_shape_runtime_construction_row_count": 1,
    "source_newton_shape_runtime_boundary_preflight_row_count": 1,
    "constructed_newton_shape_mapping_record_count": 1,
    "newton_mapping_record_count": 1,
    "newton_mapper_call_count": 0,
    "newton_shape_object_count": 0,
    "newton_engine_shape_object_count": 0,
    "newton_builder_shape_call_count": 0,
    "newton_runtime_execution_count": 0,
    "generated_runtime_primitive_spec_count": 1,
    "generated_primitive_spec_count": 1,
    "generated_collision_package_count": 1,
    "runtime_admissibility_check_count": 1,
    "offline_static_runtime_admissibility_check_count": 1,
    "report_scoped_newton_shape_descriptor_count": 1,
    "later_newton_shape_runtime_construction_candidate_count": 1,
}
for field_name, expected_value in expected_counts.items():
    if construction.get(field_name) != expected_value:
        raise ValueError(
            "newton_shape_runtime_builder_preflight_input_count_mismatch:"
            f"{field_name}"
        )
```

After selecting the single source row, validate row-level inherited false flags and zero counters:

```python
_paper_validate_primitivespec_runtime_construction_false_flags(
    row,
    error_prefix="newton_shape_runtime_builder_preflight_input_flag",
    required_false_flags=_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_PAYLOAD_FALSE_FLAGS,
)
for field_name in (
    "newton_mapper_call_count",
    "newton_shape_object_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_runtime_execution_count",
):
    if row.get(field_name) != 0:
        raise ValueError(
            "newton_shape_runtime_builder_preflight_source_row_mismatch:"
            f"{field_name}"
        )
```

- [ ] **Step 3: Add mapping and builder-plan helpers**

Implement `_paper_validate_newton_shape_runtime_builder_preflight_mapping(row)`:

```python
mapping = row.get("constructed_newton_shape_mapping_dict")
if not isinstance(mapping, dict):
    raise ValueError("newton_shape_runtime_builder_preflight_mapping_invalid:mapping")
if set(mapping) != {"primitive_id", "kind", "status", "detail", "center", "axes", "dimensions"}:
    raise ValueError("newton_shape_runtime_builder_preflight_mapping_key_mismatch")
dimensions = mapping.get("dimensions")
if not isinstance(dimensions, dict) or set(dimensions) != {"half_extents"}:
    raise ValueError("newton_shape_runtime_builder_preflight_mapping_dimensions_key_mismatch")
```

Validate primitive id, kind `box`, status/detail `mapped`, center, axes, and half-extents using the
existing runtime-construction vector/axes validation helpers. Each valid-looking but wrong value
must raise:

```python
raise ValueError("newton_shape_runtime_builder_preflight_mapping_mismatch:<field>")
```

Return normalized center, axes, and half-extents lists.

Implement:

```python
def _paper_newton_shape_runtime_builder_call_plan(
    half_extents: list[float],
) -> dict[str, object]:
    return {
        "method": "add_shape_box",
        "call_signature_fields": ["body", "xform", "hx", "hy", "hz"],
        "body_binding_policy": (
            "static_package_or_probe_uses_body_minus_one_"
            "drop_settle_uses_created_body_id"
        ),
        "deferred_xform_policy": (
            "future_runtime_may_derive_xform_from_center_and_axes"
        ),
        "deferred_translation_inputs": (
            "mapping_center_only_no_runtime_transform_constructed"
        ),
        "deferred_rotation_inputs": (
            "mapping_axes_only_no_quat_or_runtime_rotation_constructed"
        ),
        "dimension_arguments": {
            "hx": half_extents[0],
            "hy": half_extents[1],
            "hz": half_extents[2],
        },
    }
```

- [ ] **Step 4: Add row, coverage, and payload helpers**

Implement `_paper_newton_shape_runtime_builder_preflight_row(source_row)` with the exact row fields
from Task 1. The row must copy lineage from the runtime-construction row, include
`builder_call_allowed: False`, `later_newton_shape_runtime_builder_candidate: True`,
`runtime_builder_construction_contract_candidate: True`, all per-row zero counters, all false flags,
and both true flags. It must include only JSON-like data fields.

Implement `_paper_newton_shape_runtime_builder_preflight_coverage_summary(rows)` returning the exact
coverage dict from Task 2.

Implement `_paper_mapped_subset_newton_shape_runtime_builder_preflight_contract_payload(construction)`
with this exact payload skeleton:

```python
return {
    "gate_id": _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT,
    "gate_status": (
        "implemented_single_fixture_newton_shape_runtime_builder_"
        "preflight_only_partial"
    ),
    "closed_gate": _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT,
    "input_gate_id": _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT,
    "next_required_gate": (
        _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT
    ),
    "decision": "remain_partial",
    "decision_reason": (
        "newton_shape_runtime_builder_preflight_complete_"
        "newton_shape_runtime_builder_construction_contract_missing"
    ),
    "artifact_kind": "offline_static_newton_builder_call_plan_not_builder_call",
    "schema_version": 1,
    "source_scope": "synthetic_toy_fixtures_only",
    "implementation_boundary": (
        "single_synthetic_box_newton_builder_preflight_only_no_builder_call_"
        "no_engine_shape_no_runtime_no_real_usd_no_benchmark_no_metrics"
    ),
    "runtime_builder_preflight_action": (
        "record_one_newton_builder_call_plan_from_repo_local_mapping_dict_"
        "without_newton_import_or_builder_call"
    ),
    "newton_shape_runtime_builder_preflight_contract": {
        "input_gate_required": (
            _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
        ),
        "closed_gate": (
            _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT
        ),
        "next_newton_shape_runtime_builder_construction_gate_required": (
            _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT
        ),
        "source_runtime_construction_rows_required": 1,
        "builder_call_plans_required": 1,
        "newton_engine_shape_object_allowed": False,
        "newton_builder_shape_call_allowed": False,
        "newton_runtime_allowed": False,
        "newton_support_claim_allowed": False,
    },
    "input_contract_summary": {
        "input_gate_id": construction["gate_id"],
        "input_next_required_gate": construction["next_required_gate"],
        "source_newton_shape_runtime_construction_row_id": source_row[
            "newton_shape_runtime_construction_row_id"
        ],
        "source_newton_shape_runtime_boundary_preflight_row_id": source_row[
            "source_newton_shape_runtime_boundary_preflight_row_id"
        ],
        "source_shape_mapping_row_id": source_row["source_shape_mapping_row_id"],
        "source_package_id": source_row["source_package_id"],
        "source_fixture_id": source_row["fixture_id"],
        "source_primitive_id": source_row["primitive_id"],
        "source_target_newton_shape_kind": source_row["target_newton_shape_kind"],
        "source_mapping_constructor": source_row["mapping_constructor"],
        "input_runtime_builder_preflight_candidate_count": 1,
    },
    "newton_shape_runtime_builder_preflight_row_count": 1,
    "source_newton_shape_runtime_construction_row_count": 1,
    "source_newton_shape_mapping_record_count": 1,
    "runtime_builder_preflight_passed": True,
    "runtime_builder_preflight_passed_count": 1,
    "builder_call_plan_count": 1,
    "builder_call_allowed_count": 0,
    "later_newton_shape_runtime_builder_candidate_count": 1,
    "constructed_newton_shape_mapping_record_count": 1,
    "newton_mapping_record_count": 1,
    "newton_mapper_call_count": 0,
    "newton_shape_object_count": 0,
    "newton_engine_shape_object_count": 0,
    "newton_builder_shape_call_count": 0,
    "newton_runtime_execution_count": 0,
    "generated_runtime_primitive_spec_count": 1,
    "generated_primitive_spec_count": 1,
    "generated_collision_package_count": 1,
    "runtime_admissibility_check_count": 1,
    "offline_static_runtime_admissibility_check_count": 1,
    "report_scoped_newton_shape_descriptor_count": 1,
    "later_newton_shape_runtime_construction_candidate_count": 1,
    "newton_shape_runtime_builder_preflight_rows": rows,
    "coverage_summary": (
        _paper_newton_shape_runtime_builder_preflight_coverage_summary(rows)
    ),
    "remaining_gaps": (
        _paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_builder_preflight()
    ),
    **_paper_newton_shape_runtime_builder_preflight_false_flags(),
    **_paper_newton_shape_runtime_builder_preflight_true_flags(),
}
```

- [ ] **Step 5: Wire into `build_cpd_paper_offline_report()`**

After runtime construction:

```python
mapped_subset_newton_shape_runtime_builder_preflight = (
    _paper_mapped_subset_newton_shape_runtime_builder_preflight_contract_payload(
        mapped_subset_newton_shape_runtime_construction
    )
)
```

Use:

```python
runtime_lane_remaining_gates = (
    _paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_builder_preflight()
)
```

Add the new contract to `implemented_output_contract_scope` and to the top-level returned report.

- [ ] **Step 6: Run focused tests and confirm GREEN**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_builder_preflight' -q
```

Expected: all selected builder-preflight tests pass.

## Task 4: CLI Contract Coverage

**Files:**
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Update offline CLI top-level expectations**

In `test_cli_run_cpd_paper_offline_report_emits_json`, change failure labels and runtime-lane
remaining gates to:

```python
[
    "paper_mapped_subset_newton_shape_runtime_builder_construction_contract_missing",
]
```

and:

```python
[
    "paper_mapped_subset_newton_shape_runtime_builder_construction_contract",
]
```

Append `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract` to
`implemented_output_contract_scope`.

- [ ] **Step 2: Add CLI payload assertions**

Add:

```python
builder_preflight = payload[
    "paper_mapped_subset_newton_shape_runtime_builder_preflight_contract"
]
assert builder_preflight["gate_id"] == (
    "paper_mapped_subset_newton_shape_runtime_builder_preflight_contract"
)
assert builder_preflight["next_required_gate"] == (
    "paper_mapped_subset_newton_shape_runtime_builder_construction_contract"
)
assert builder_preflight["runtime_builder_preflight_passed"] is True
assert builder_preflight["builder_call_plan_count"] == 1
assert builder_preflight["builder_call_allowed_count"] == 0
assert builder_preflight["newton_builder_shape_call_count"] == 0
assert builder_preflight["newton_engine_shape_object_count"] == 0
assert builder_preflight["newton_runtime_execution_count"] == 0
assert builder_preflight["newton_shape_runtime_builder_preflight_rows"][0][
    "builder_method_name"
] == "add_shape_box"
```

- [ ] **Step 3: Run CLI tests**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Expected: all selected CLI tests pass.

## Task 5: Documentation And Record

**Files:**
- Modify: listed docs
- Create: `docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-builder-preflight-contract.md`

- [ ] **Step 1: Update canonical status wording**

First locate stale references and table rows:

```bash
rg -n "paper_mapped_subset_newton_shape_runtime_builder_preflight_contract|runtime-construction|builder preflight|builder-preflight" README.md docs/index.md docs/deepdive docs/reference docs/records/README.md
```

Per-file edit targets:

- `README.md`: append the builder-preflight paragraph after the runtime-construction paragraph and
  advance the current next gate.
- `docs/index.md`: update the current evidence/gate summary.
- `docs/deepdive/evidence-status.md`: add the executable-surface bullet and update the first
  unresolved runtime-lane gate.
- `docs/deepdive/message-map.md`: update the canonical unsafe-claims paragraph.
- `docs/reference/claim-boundaries.md`: add the positive boundary bullet and the matching
  "Do not describe..." bullet.
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`: append the new lane chronology entry.
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`: update repeated gap-table cells rather
  than pasting a duplicate paragraph where table wording is expected.
- `docs/reference/cpd-paper-story-status.md`: mark builder preflight closed and advance the
  recommended next slice.
- `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`: update the current next-gate
  sentence and supported-statement block.
- `docs/records/README.md`: add the new dated record entry after the runtime-construction record.

In each listed doc, replace stale builder-preflight-as-next wording with:

```text
`paper_mapped_subset_newton_shape_runtime_builder_preflight_contract` is now a
single-fixture offline/static builder-boundary preflight. It consumes one repo-local
`NewtonShapeMapping.to_dict()` mapping record for the synthetic `paper_single_box` box descriptor
and records one repo-local data-only sketch of a possible future `add_shape_box` call signature,
not a Newton builder call. It keeps Newton engine shape object construction, Newton builder shape
calls, Newton runtime execution, real-USD loading, benchmark runs, collision-quality measurement,
deployment readiness, and safety certification at zero or false. The current next gate is
`paper_mapped_subset_newton_shape_runtime_builder_construction_contract`.
```

- [ ] **Step 2: Add the dated record**

Create the record with:

```markdown
# 2026-05-18 CPD Paper Mapped-Subset Newton Shape Runtime-Builder Preflight Contract

## Summary

Closed `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract` as a
single-fixture offline/static builder-boundary preflight.

## Boundary

This is not Newton support, not Newton readiness, not a Newton builder call, not a Newton engine
shape object, not Newton runtime execution, not real-USD evidence, not benchmark evidence, not
collision-quality validation, not `paper_faithful_offline`, not deployment readiness, and not
safety certification.

## Evidence

- One source `NewtonShapeMapping.to_dict()` record from `paper_single_box`.
- One repo-local data-only sketch of a possible future `add_shape_box` call signature.
- `newton_builder_shape_call_count: 0`
- `newton_engine_shape_object_count: 0`
- `newton_runtime_execution_count: 0`

## Next Gate

`paper_mapped_subset_newton_shape_runtime_builder_construction_contract`
```

- [ ] **Step 3: Run docs checks**

Run:

```bash
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

## Task 6: Review, Verification, Commit, Merge

**Files:**
- Review all changed files

- [ ] **Step 1: Run focused verification**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_builder_preflight or newton_shape_runtime_construction or newton_shape_runtime_boundary_preflight' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Expected: all selected tests pass.

- [ ] **Step 2: Request multi-agent review**

Dispatch reviewers for:

- schema/test coverage;
- Newton/runtime boundary;
- docs/claim boundary.

Fix every finding, then rerun the affected tests.

- [ ] **Step 3: Run final verification**

Run:

```bash
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Run the full suite if practical:

```bash
PYTHONPATH=src python -m pytest -q
```

If the full suite is not run, record the reason and the narrower verification coverage in the
dated record and final summary.

- [ ] **Step 4: Update the dated record with final verification**

After final verification, update
`docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-builder-preflight-contract.md`
with:

```markdown
## Verification

- `PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_builder_preflight or newton_shape_runtime_construction or newton_shape_runtime_boundary_preflight' -q`
- `PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q`
- `PYTHONPATH=src python scripts/validate_docs.py`
- `PYTHONPATH=src python scripts/validate_site_claims.py`
- `git diff --check`
- Full suite: <run result, or explicit reason skipped>
```

- [ ] **Step 5: Commit implementation and docs**

Use focused commits:

```bash
git add src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cpd_paper_offline.py tests/test_cli.py
git commit -m "feat: add CPD Newton shape builder preflight"
git add README.md docs/index.md docs/deepdive/evidence-status.md docs/deepdive/message-map.md docs/reference/claim-boundaries.md docs/reference/cpd-paper-faithful-offline-lane-spec.md docs/reference/cpd-paper-reproduction-gap-matrix.md docs/reference/cpd-paper-story-status.md docs/reference/cpd-paper-fixture-breadth-expansion-plan.md docs/records/README.md docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-builder-preflight-contract.md docs/superpowers/plans/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-builder-preflight-contract.md
git commit -m "docs: record CPD Newton shape builder preflight"
```

- [ ] **Step 6: Merge and clean worktree**

After verification and review:

```bash
git -C /cpfs/user/zhuzihou/dev/physics-primitive-agent switch main
git -C /cpfs/user/zhuzihou/dev/physics-primitive-agent pull --ff-only
git -C /cpfs/user/zhuzihou/dev/physics-primitive-agent merge --ff-only cpd-paper-newton-shape-builder-preflight-contract
git -C /cpfs/user/zhuzihou/dev/physics-primitive-agent push
git -C /cpfs/user/zhuzihou/dev/physics-primitive-agent worktree remove .worktrees/cpd-paper-newton-shape-builder-preflight-contract
git -C /cpfs/user/zhuzihou/dev/physics-primitive-agent branch -d cpd-paper-newton-shape-builder-preflight-contract
git -C /cpfs/user/zhuzihou/dev/physics-primitive-agent status --short --branch
```

Expected final main status: clean and synced to origin.

## Self-Review

- Spec coverage: every design requirement maps to a task above.
- Placeholder scan: no placeholder-driven implementation steps remain.
- Type consistency: gate names, payload fields, row fields, and counter names match the design spec.
- Boundary check: every implementation task preserves report-only behavior and keeps Newton builder/runtime counters at zero.
