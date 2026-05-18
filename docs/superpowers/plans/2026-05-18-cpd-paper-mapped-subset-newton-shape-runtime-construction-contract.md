# CPD Paper Mapped-Subset Newton Shape Runtime-Construction Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the bounded offline/report-scoped `paper_mapped_subset_newton_shape_runtime_construction_contract` gate after the existing Newton shape runtime-boundary preflight gate.

**Architecture:** Extend the current `cpd_paper_offline_report` runtime lane by consuming exactly one runtime-boundary preflight row and constructing exactly one repo-local `NewtonShapeMapping.to_dict()` record. This gate must not cross into Newton engine execution: no `primitive_collision_compiler.newton` import, no Newton/warp import, no builder shape call, no runtime diagnostics, no USD, no benchmark, and no collision-quality measurement.

**Tech Stack:** Python, pytest, Markdown docs, existing `primitive_collision_compiler.baselines.cpd_paper.offline` report builders, existing `primitive_collision_compiler.reports.schema.NewtonShapeMapping` dataclass.

---

## File Structure

- Modify `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
  - Add `_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT`.
  - Add `_paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_construction()`.
  - Add construction false/true flag helpers and strict input validation helpers.
  - Add one local `NewtonShapeMapping` construction helper that returns `mapping.to_dict()`.
  - Wire the new payload into `build_cpd_paper_offline_report()`.
- Modify `tests/test_cpd_paper_offline.py`
  - Add constants, required-key sets, focused positive tests, negative drift tests, and static boundary tests for the new gate.
  - Update top-level current output gap and failure label expectations to the builder-preflight gate.
- Modify `tests/test_cli.py`
  - Update the offline report CLI expectations for the new next gate and current failure label.
  - Add assertions for the new runtime-construction payload and one constructed mapping record.
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
  - Create `docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-construction-contract.md`

## Task 1: RED Constants, Schemas, And Helper Input

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`

- [ ] **Step 1: Add the next gate constant and update current failure scope**

Add this next to the existing Newton shape runtime constants:

```python
EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_builder_preflight_contract"
)
EXPECTED_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT,
]
```

Update `EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS` from:

```python
EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT,
]
```

to:

```python
EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT,
]
```

Keep `EXPECTED_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_REMAINING_GAPS` unchanged. The runtime-boundary preflight payload must still point to the construction gate.

Update top-level assertions in earlier Newton shape tests that currently read the report's
`next_required_gate` or `paper_faithfulness.runtime_lane_remaining_gates`. In particular,
`test_cpd_paper_records_mapped_subset_newton_shape_mapping_contract_gate` and
`test_cpd_paper_records_mapped_subset_newton_shape_runtime_boundary_preflight_contract_gate`
must expect:

```python
assert report["next_required_gate"] == (
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT
)
assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
    EXPECTED_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_REMAINING_GAPS
)
```

Do not change those earlier payloads' own `next_required_gate` or `remaining_gaps` assertions:
the shape-mapping payload still points to runtime-boundary preflight, and the runtime-boundary
preflight payload still points to runtime construction.

- [ ] **Step 2: Add construction boundary flag sets**

Add this near `NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_FALSE_FLAGS`:

```python
NEWTON_SHAPE_RUNTIME_CONSTRUCTION_FALSE_FLAGS = (
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
)

NEWTON_SHAPE_RUNTIME_CONSTRUCTION_TRUE_FLAGS = (
    "repo_local_newton_shape_mapping_record_constructed",
    "newton_shape_mapping_record_created",
)
```

- [ ] **Step 3: Add exact payload and row required-key sets**

Add:

```python
NEWTON_SHAPE_RUNTIME_CONSTRUCTION_PAYLOAD_REQUIRED_KEYS = {
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
    "runtime_construction_action",
    "newton_shape_runtime_construction_contract",
    "input_contract_summary",
    "newton_shape_runtime_construction_row_count",
    "source_newton_shape_runtime_boundary_preflight_row_count",
    "constructed_newton_shape_mapping_record_count",
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
    "newton_shape_runtime_construction_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_RUNTIME_CONSTRUCTION_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_CONSTRUCTION_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_CONSTRUCTION_ROW_REQUIRED_KEYS = {
    "newton_shape_runtime_construction_row_id",
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
    "runtime_builder_preflight_candidate",
    "constructed_newton_shape_mapping_record_count",
    "newton_mapping_record_count",
    "newton_mapper_call_count",
    "newton_shape_object_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_runtime_execution_count",
    *NEWTON_SHAPE_RUNTIME_CONSTRUCTION_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_CONSTRUCTION_TRUE_FLAGS,
}
```

- [ ] **Step 4: Add a helper that returns the construction input payload**

Add near `_newton_shape_runtime_boundary_preflight_input()`:

```python
def _newton_shape_runtime_construction_input() -> dict[str, object]:
    report = build_cpd_paper_offline_report()
    return json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"
            ]
        )
    )
```

- [ ] **Step 5: Run the focused test file to confirm constants still parse**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k newton_shape_runtime_boundary_preflight -q
```

Expected: existing runtime-boundary preflight tests still pass before adding new RED assertions.

## Task 2: RED Positive Tests For Runtime Construction

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add the main gate test**

Add after the runtime-boundary preflight tests:

```python
def test_cpd_paper_records_mapped_subset_newton_shape_runtime_construction_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_construction_contract"
    ]

    assert report["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT
    )
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_REMAINING_GAPS
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT
    )
    assert payload["newton_shape_runtime_construction_row_count"] == 1
    assert payload["source_newton_shape_runtime_boundary_preflight_row_count"] == 1
    assert payload["constructed_newton_shape_mapping_record_count"] == 1
    assert payload["newton_mapping_record_count"] == 1
    assert payload["newton_mapper_call_count"] == 0
    assert payload["newton_shape_object_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_REMAINING_GAPS
    )
```

- [ ] **Step 2: Add exact payload schema test**

Add:

```python
def test_cpd_paper_newton_shape_runtime_construction_payload_schema_is_exact():
    report = build_cpd_paper_offline_report()
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_construction_contract"
    ]
    source_row = report[
        "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"
    ]["newton_shape_runtime_boundary_preflight_rows"][0]

    assert set(payload) == NEWTON_SHAPE_RUNTIME_CONSTRUCTION_PAYLOAD_REQUIRED_KEYS
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_shape_mapping_record_"
        "construction_contract_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_shape_mapping_record_construction_complete_"
        "newton_shape_runtime_builder_preflight_missing"
    )
    assert payload["artifact_kind"] == (
        "repo_local_newton_shape_mapping_to_dict_not_newton_engine_shape"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_newton_shape_mapping_record_only_"
        "no_newton_engine_shape_no_runtime_no_real_usd_no_benchmark_no_metrics"
    )
    assert payload["runtime_construction_action"] == (
        "construct_one_repo_local_newton_shape_mapping_from_static_descriptor_"
        "without_newton_import"
    )
    assert payload["newton_shape_runtime_construction_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
        ),
        "closed_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
        ),
        "next_newton_shape_runtime_builder_preflight_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT
        ),
        "source_runtime_boundary_preflight_rows_required": 1,
        "newton_shape_mapping_to_dict_records_required": 1,
        "newton_mapper_call_allowed": False,
        "newton_engine_shape_object_allowed": False,
        "newton_builder_shape_call_allowed": False,
        "newton_runtime_allowed": False,
        "newton_support_claim_allowed": False,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
        ),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
        ),
        "source_newton_shape_runtime_boundary_preflight_row_id": (
            source_row["newton_shape_runtime_boundary_preflight_row_id"]
        ),
        "source_shape_mapping_row_id": source_row["source_shape_mapping_row_id"],
        "source_package_id": source_row["source_package_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": source_row["primitive_id"],
        "source_target_newton_shape_kind": "box",
        "source_descriptor_kind": "newton_shape_descriptor",
        "input_construction_candidate_count": 1,
    }
```

- [ ] **Step 3: Add the row and `NewtonShapeMapping.to_dict()` schema test**

Add:

```python
def test_cpd_paper_newton_shape_runtime_construction_records_one_mapping_row():
    report = build_cpd_paper_offline_report()
    source_row = report[
        "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"
    ]["newton_shape_runtime_boundary_preflight_rows"][0]
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_construction_contract"
    ]
    rows = payload["newton_shape_runtime_construction_rows"]

    assert len(rows) == 1
    row = rows[0]
    assert set(row) == NEWTON_SHAPE_RUNTIME_CONSTRUCTION_ROW_REQUIRED_KEYS
    assert row["newton_shape_runtime_construction_row_id"] == (
        "newton_shape_runtime_construction__paper_single_box__box"
    )
    assert row["source_newton_shape_runtime_boundary_preflight_row_id"] == (
        source_row["newton_shape_runtime_boundary_preflight_row_id"]
    )
    assert row["source_shape_mapping_row_id"] == (
        source_row["source_shape_mapping_row_id"]
    )
    assert row["source_runtime_admissibility_row_id"] == (
        source_row["source_runtime_admissibility_row_id"]
    )
    assert row["source_package_id"] == source_row["source_package_id"]
    assert row["fixture_id"] == "paper_single_box"
    assert row["paper_primitive"] == "oriented_bounding_box"
    assert row["primitive_spec_kind"] == "box"
    assert row["primitive_id"] == (
        "paper_single_box__oriented_bounding_box__box"
    )
    assert row["target_newton_shape_kind"] == "box"
    assert row["descriptor_kind"] == "newton_shape_descriptor"
    assert row["descriptor_center"] == source_row["descriptor_center"]
    assert row["descriptor_axes"] == source_row["descriptor_axes"]
    assert row["descriptor_half_extents"] == source_row["descriptor_half_extents"]
    assert row["constructed_newton_shape_mapping_status"] == "mapped"
    assert row["constructed_newton_shape_mapping_detail"] == "mapped"
    assert row["mapping_constructor"] == "NewtonShapeMapping"
    assert row["mapping_constructor_input_kind"] == "static_descriptor_fields"
    assert row["runtime_builder_preflight_candidate"] is True
    assert row["constructed_newton_shape_mapping_dict"] == {
        "primitive_id": "paper_single_box__oriented_bounding_box__box",
        "kind": "box",
        "status": "mapped",
        "detail": "mapped",
        "center": source_row["descriptor_center"],
        "axes": source_row["descriptor_axes"],
        "dimensions": {
            "half_extents": source_row["descriptor_half_extents"],
        },
    }
    assert list(_recursive_package_dicts(payload)) == []
```

- [ ] **Step 4: Add construction false/true flag test**

Add:

```python
@pytest.mark.parametrize("field_name", NEWTON_SHAPE_RUNTIME_CONSTRUCTION_FALSE_FLAGS)
def test_cpd_paper_newton_shape_runtime_construction_boundary_flags_stay_false(
    field_name,
):
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_newton_shape_runtime_construction_contract"
    ]

    assert payload[field_name] is False
    assert payload["newton_shape_runtime_construction_rows"][0][field_name] is False


@pytest.mark.parametrize("field_name", NEWTON_SHAPE_RUNTIME_CONSTRUCTION_TRUE_FLAGS)
def test_cpd_paper_newton_shape_runtime_construction_record_flags_are_narrowly_true(
    field_name,
):
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_newton_shape_runtime_construction_contract"
    ]

    assert payload[field_name] is True
    assert payload["newton_shape_runtime_construction_rows"][0][field_name] is True
```

- [ ] **Step 5: Update CLI expected current gate and add payload assertions**

In `tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json`, update:

```python
assert payload["failure_labels"] == [
    "paper_mapped_subset_newton_shape_runtime_builder_preflight_contract_missing",
]
assert (
    payload["next_required_gate"]
    == "paper_mapped_subset_newton_shape_runtime_builder_preflight_contract"
)
assert payload["paper_faithfulness"]["runtime_lane_remaining_gates"] == [
    "paper_mapped_subset_newton_shape_runtime_builder_preflight_contract",
]
```

Append the new implemented output contract string after the runtime-boundary preflight string:

```python
"paper_mapped_subset_newton_shape_runtime_construction_contract",
```

Add after the existing `runtime_boundary` assertions:

```python
runtime_construction = payload[
    "paper_mapped_subset_newton_shape_runtime_construction_contract"
]
assert runtime_construction["gate_id"] == (
    "paper_mapped_subset_newton_shape_runtime_construction_contract"
)
assert runtime_construction["input_gate_id"] == (
    "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"
)
assert runtime_construction["next_required_gate"] == (
    "paper_mapped_subset_newton_shape_runtime_builder_preflight_contract"
)
assert runtime_construction["newton_shape_runtime_construction_row_count"] == 1
assert runtime_construction["constructed_newton_shape_mapping_record_count"] == 1
assert runtime_construction["newton_mapping_record_count"] == 1
assert runtime_construction["newton_mapper_call_count"] == 0
assert runtime_construction["newton_shape_object_count"] == 0
assert runtime_construction["newton_engine_shape_object_count"] == 0
assert runtime_construction["newton_builder_shape_call_count"] == 0
assert runtime_construction["newton_runtime_execution_count"] == 0
assert runtime_construction["newton_shape_runtime_construction_rows"][0][
    "constructed_newton_shape_mapping_dict"
]["kind"] == "box"
```

- [ ] **Step 6: Run RED tests and confirm they fail for missing payload/constant wiring**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k newton_shape_runtime_construction -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Expected: failures because `paper_mapped_subset_newton_shape_runtime_construction_contract` is not wired yet.

## Task 3: RED Negative Tests And Static Boundary Tests

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`

- [ ] **Step 1: Add input drift tests**

Add:

```python
@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "gate_id",
            "stale_gate",
            "newton_shape_runtime_construction_input_gate_id_mismatch",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "newton_shape_runtime_construction_input_next_gate_mismatch",
        ),
        (
            "newton_shape_runtime_boundary_preflight_row_count",
            2,
            "newton_shape_runtime_construction_input_count_mismatch:"
            "newton_shape_runtime_boundary_preflight_row_count",
        ),
        (
            "source_shape_mapping_contract_row_count",
            2,
            "newton_shape_runtime_construction_input_count_mismatch:"
            "source_shape_mapping_contract_row_count",
        ),
        (
            "later_newton_shape_runtime_construction_candidate_count",
            2,
            "newton_shape_runtime_construction_input_count_mismatch:"
            "later_newton_shape_runtime_construction_candidate_count",
        ),
        (
            "report_scoped_newton_shape_descriptor_count",
            2,
            "newton_shape_runtime_construction_input_count_mismatch:"
            "report_scoped_newton_shape_descriptor_count",
        ),
        (
            "mapping_attempt_count",
            1,
            "newton_shape_runtime_construction_input_count_mismatch:"
            "mapping_attempt_count",
        ),
        (
            "newton_mapping_record_count",
            1,
            "newton_shape_runtime_construction_input_count_mismatch:"
            "newton_mapping_record_count",
        ),
        (
            "newton_shape_object_count",
            1,
            "newton_shape_runtime_construction_input_count_mismatch:"
            "newton_shape_object_count",
        ),
        (
            "newton_runtime_execution_count",
            1,
            "newton_shape_runtime_construction_input_count_mismatch:"
            "newton_runtime_execution_count",
        ),
        (
            "generated_runtime_primitive_spec_count",
            2,
            "newton_shape_runtime_construction_input_count_mismatch:"
            "generated_runtime_primitive_spec_count",
        ),
        (
            "generated_primitive_spec_count",
            2,
            "newton_shape_runtime_construction_input_count_mismatch:"
            "generated_primitive_spec_count",
        ),
        (
            "generated_collision_package_count",
            2,
            "newton_shape_runtime_construction_input_count_mismatch:"
            "generated_collision_package_count",
        ),
        (
            "runtime_admissibility_check_count",
            2,
            "newton_shape_runtime_construction_input_count_mismatch:"
            "runtime_admissibility_check_count",
        ),
        (
            "offline_static_runtime_admissibility_check_count",
            2,
            "newton_shape_runtime_construction_input_count_mismatch:"
            "offline_static_runtime_admissibility_check_count",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_construction_rejects_input_drift(
    field_name,
    bad_value,
    error_label,
):
    payload = _newton_shape_runtime_construction_input()
    payload[field_name] = bad_value

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_construction_contract_payload(
            payload
        )
```

- [ ] **Step 2: Add forbidden input flag and row count drift tests**

Add:

```python
@pytest.mark.parametrize(
    "field_name",
    NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_FALSE_FLAGS,
)
def test_cpd_paper_newton_shape_runtime_construction_rejects_input_forbidden_flags(
    field_name,
):
    payload = _newton_shape_runtime_construction_input()
    payload[field_name] = True

    with pytest.raises(
        ValueError,
        match=f"newton_shape_runtime_construction_input_flag_true:{field_name}",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_construction_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    ("mutate_rows", "error_label"),
    [
        (
            lambda rows: [],
            "newton_shape_runtime_construction_row_count_mismatch",
        ),
        (
            lambda rows: [rows[0], json.loads(json.dumps(rows[0]))],
            "newton_shape_runtime_construction_row_count_mismatch",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_construction_rejects_row_count_drift(
    mutate_rows,
    error_label,
):
    payload = _newton_shape_runtime_construction_input()
    payload["newton_shape_runtime_boundary_preflight_rows"] = mutate_rows(
        payload["newton_shape_runtime_boundary_preflight_rows"]
    )

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_construction_contract_payload(
            payload
        )
```

- [ ] **Step 3: Add source row drift tests**

Add a parametrized test that mutates the single input row:

```python
@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "newton_shape_runtime_boundary_preflight_row_id",
            "wrong_row",
            "newton_shape_runtime_construction_source_row_mismatch:"
            "newton_shape_runtime_boundary_preflight_row_id",
        ),
        (
            "source_shape_mapping_row_id",
            "wrong_mapping_row",
            "newton_shape_runtime_construction_source_row_mismatch:"
            "source_shape_mapping_row_id",
        ),
        (
            "source_newton_shape_mapping_preflight_row_id",
            "wrong_preflight_row",
            "newton_shape_runtime_construction_source_row_mismatch:"
            "source_newton_shape_mapping_preflight_row_id",
        ),
        (
            "source_runtime_admissibility_row_id",
            "wrong_runtime_admissibility_row",
            "newton_shape_runtime_construction_source_row_mismatch:"
            "source_runtime_admissibility_row_id",
        ),
        (
            "source_package_id",
            "wrong_package",
            "newton_shape_runtime_construction_source_row_mismatch:"
            "source_package_id",
        ),
        (
            "source_asset_id",
            "wrong_asset",
            "newton_shape_runtime_construction_source_row_mismatch:"
            "source_asset_id",
        ),
        (
            "fixture_id",
            "wrong_fixture",
            "newton_shape_runtime_construction_source_row_mismatch:fixture_id",
        ),
        (
            "paper_primitive",
            "sphere",
            "newton_shape_runtime_construction_source_row_mismatch:"
            "paper_primitive",
        ),
        (
            "primitive_spec_kind",
            "sphere",
            "newton_shape_runtime_construction_source_row_mismatch:"
            "primitive_spec_kind",
        ),
        (
            "primitive_id",
            "wrong_primitive",
            "newton_shape_runtime_construction_source_row_mismatch:"
            "primitive_id",
        ),
        (
            "target_newton_shape_kind",
            "sphere",
            "newton_shape_runtime_construction_source_row_mismatch:"
            "target_newton_shape_kind",
        ),
        (
            "descriptor_kind",
            "wrong_descriptor",
            "newton_shape_runtime_construction_source_row_mismatch:"
            "descriptor_kind",
        ),
        (
            "runtime_boundary_preflight_passed",
            False,
            "newton_shape_runtime_construction_source_row_mismatch:"
            "runtime_boundary_preflight_passed",
        ),
        (
            "later_newton_shape_runtime_construction_candidate",
            False,
            "newton_shape_runtime_construction_source_row_mismatch:"
            "later_newton_shape_runtime_construction_candidate",
        ),
        (
            "mapping_attempt_count",
            1,
            "newton_shape_runtime_construction_source_row_mismatch:"
            "mapping_attempt_count",
        ),
        (
            "newton_mapping_record_count",
            1,
            "newton_shape_runtime_construction_source_row_mismatch:"
            "newton_mapping_record_count",
        ),
        (
            "newton_shape_object_count",
            1,
            "newton_shape_runtime_construction_source_row_mismatch:"
            "newton_shape_object_count",
        ),
        (
            "newton_runtime_execution_count",
            1,
            "newton_shape_runtime_construction_source_row_mismatch:"
            "newton_runtime_execution_count",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_construction_rejects_source_row_drift(
    field_name,
    bad_value,
    error_label,
):
    payload = _newton_shape_runtime_construction_input()
    rows = [
        json.loads(json.dumps(row))
        for row in payload["newton_shape_runtime_boundary_preflight_rows"]
    ]
    rows[0][field_name] = bad_value
    payload["newton_shape_runtime_boundary_preflight_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_construction_contract_payload(
            payload
        )
```

- [ ] **Step 4: Add descriptor validation tests**

Add:

```python
@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "descriptor_center",
            None,
            "newton_shape_runtime_construction_descriptor_invalid:center",
        ),
        (
            "descriptor_center",
            [0.0, 1.0],
            "newton_shape_runtime_construction_descriptor_invalid:center",
        ),
        (
            "descriptor_center",
            [0.0, "bad", 1.0],
            "newton_shape_runtime_construction_descriptor_invalid:center",
        ),
        (
            "descriptor_center",
            [0.0, float("inf"), 1.0],
            "newton_shape_runtime_construction_descriptor_invalid:center",
        ),
        (
            "descriptor_axes",
            None,
            "newton_shape_runtime_construction_descriptor_invalid:axes",
        ),
        (
            "descriptor_axes",
            [[1.0, 0.0, 0.0]],
            "newton_shape_runtime_construction_descriptor_invalid:axes",
        ),
        (
            "descriptor_axes",
            [[1.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 1.0]],
            "newton_shape_runtime_construction_descriptor_invalid:axes",
        ),
        (
            "descriptor_axes",
            [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]],
            "newton_shape_runtime_construction_descriptor_invalid:axes",
        ),
        (
            "descriptor_half_extents",
            [1.0, 0.25],
            "newton_shape_runtime_construction_descriptor_invalid:half_extents",
        ),
        (
            "descriptor_half_extents",
            [1.0, "bad", 0.25],
            "newton_shape_runtime_construction_descriptor_invalid:half_extents",
        ),
        (
            "descriptor_half_extents",
            [1.0, 0.0, 0.25],
            "newton_shape_runtime_construction_descriptor_invalid:half_extents",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_construction_rejects_descriptor_drift(
    field_name,
    bad_value,
    error_label,
):
    payload = _newton_shape_runtime_construction_input()
    rows = [
        json.loads(json.dumps(row))
        for row in payload["newton_shape_runtime_boundary_preflight_rows"]
    ]
    rows[0][field_name] = bad_value
    payload["newton_shape_runtime_boundary_preflight_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_construction_contract_payload(
            payload
        )
```

- [ ] **Step 5: Add source package copy and static boundary tests**

Add:

```python
def test_cpd_paper_newton_shape_runtime_construction_rejects_source_package_copy():
    payload = _newton_shape_runtime_construction_input()
    source_package = build_cpd_paper_offline_report()[
        "paper_mapped_subset_collision_package_generation_contract"
    ]["collision_package_generation_rows"][0]["generated_collision_package"]
    payload["source_collision_package_dict"] = json.loads(json.dumps(source_package))

    with pytest.raises(
        ValueError,
        match="newton_shape_runtime_construction_source_package_copy_forbidden",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_construction_contract_payload(
            payload
        )
```

Also narrow the existing `test_cpd_paper_newton_shape_mapping_contract_static_boundaries`
source slice. The new construction helper intentionally contains `NewtonShapeMapping`, so the
older mapping-contract static test must stop before the runtime-boundary/construction helper
section:

```python
contract_block = source[
    source.index("_NEWTON_SHAPE_MAPPING_CONTRACT_PAYLOAD_FALSE_FLAGS"):
    source.index("_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_PAYLOAD_FALSE_FLAGS")
]
```

Then add the new construction-specific static boundary test:

```python


def test_cpd_paper_newton_shape_runtime_construction_static_boundary_is_record_only():
    helpers = (
        cpd_paper_offline._paper_validate_newton_shape_runtime_construction_descriptor,
        cpd_paper_offline._paper_newton_shape_runtime_construction_source_row,
        cpd_paper_offline._paper_constructed_newton_shape_mapping_dict,
        cpd_paper_offline._paper_newton_shape_runtime_construction_row,
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_construction_contract_payload,
        cpd_paper_offline.build_cpd_paper_offline_report,
    )
    source = "\n".join(inspect.getsource(helper) for helper in helpers)

    assert source.count("NewtonShapeMapping(") == 1
    assert (
        "from primitive_collision_compiler.reports.schema import NewtonShapeMapping"
        in source
    )

    forbidden_patterns = (
        "CollisionPackage(",
        "PrimitiveSpec(",
        "FallbackSpec",
        "primitive_collision_compiler.newton",
        "map_package_shapes",
        "import newton",
        "from newton",
        "import newton_warp",
        "builder.add_shape_",
        "CollisionPipeline",
        "collide",
        "finalize",
        "run_newton",
        "newton.",
        "check_runtime_admissibility",
        "run_runtime_admissibility",
        "pxr",
        "Usd.Stage",
        "load_first_mesh",
        "inspect_usd_asset",
        "assets.usd_smoke",
        "real_usd_comparison",
        ".simulate(",
        "timeit",
        "perf_counter",
        "benchmark_metric",
        "surface_distance",
        "timing_result",
        "collision_quality_score",
        "run_benchmark",
        "measure_collision_quality",
        "create_shape(",
        "create_box(",
        "Shape(",
    )
    for pattern in forbidden_patterns:
        assert pattern not in source
```

Do not add the broad forbidden patterns `"Newton"`, `"USD"`, `"benchmark"`, or `"collision_quality"` to this test. The helper intentionally uses `NewtonShapeMapping`, and boundary flag names intentionally include `benchmark_run`, `benchmark_triggered`, and `collision_quality_measured`.

- [ ] **Step 6: Run RED tests and confirm expected failures**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k newton_shape_runtime_construction -q
```

Expected: failures because the new helper functions and payload do not exist yet.

## Task 4: Implement The Offline Runtime-Construction Payload

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add the builder preflight gate constant and remaining-gap helper**

Add after `_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT`:

```python
_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_builder_preflight_contract"
)
```

Add after `_paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_boundary_preflight()`:

```python
def _paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_construction() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT]
```

- [ ] **Step 2: Add construction flag helpers**

Add after the runtime-boundary preflight helpers:

```python
_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_PAYLOAD_FALSE_FLAGS = (
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
)

_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_TRUE_FLAGS = (
    "repo_local_newton_shape_mapping_record_constructed",
    "newton_shape_mapping_record_created",
)


def _paper_newton_shape_runtime_construction_false_flags() -> dict[str, bool]:
    return {
        flag: False
        for flag in _NEWTON_SHAPE_RUNTIME_CONSTRUCTION_PAYLOAD_FALSE_FLAGS
    }


def _paper_newton_shape_runtime_construction_true_flags() -> dict[str, bool]:
    return {
        flag: True
        for flag in _NEWTON_SHAPE_RUNTIME_CONSTRUCTION_TRUE_FLAGS
    }
```

- [ ] **Step 3: Add descriptor validation helpers**

Add:

```python
def _paper_newton_shape_runtime_construction_vector(
    value: object,
    *,
    error_label: str,
) -> list[float]:
    return _paper_newton_shape_mapping_preflight_vector(
        value,
        error_label=error_label,
    )


def _paper_newton_shape_runtime_construction_axes_are_valid(
    axes: list[list[float]],
) -> bool:
    axis_matrix = np.asarray(axes, dtype=np.float64)
    if axis_matrix.shape != (3, 3):
        return False
    if not np.all(np.isfinite(axis_matrix)):
        return False
    if not np.allclose(axis_matrix @ axis_matrix.T, np.eye(3), atol=1e-6):
        return False
    return bool(np.linalg.det(axis_matrix) > 0.0)


def _paper_validate_newton_shape_runtime_construction_descriptor(
    source_row: dict[str, object],
) -> dict[str, list[float] | list[list[float]]]:
    center = _paper_newton_shape_runtime_construction_vector(
        source_row.get("descriptor_center"),
        error_label="newton_shape_runtime_construction_descriptor_invalid:center",
    )
    axes_value = source_row.get("descriptor_axes")
    if not isinstance(axes_value, list | tuple) or len(axes_value) != 3:
        raise ValueError(
            "newton_shape_runtime_construction_descriptor_invalid:axes"
        )
    axes = [
        _paper_newton_shape_runtime_construction_vector(
            axis,
            error_label="newton_shape_runtime_construction_descriptor_invalid:axes",
        )
        for axis in axes_value
    ]
    if not _paper_newton_shape_runtime_construction_axes_are_valid(axes):
        raise ValueError(
            "newton_shape_runtime_construction_descriptor_invalid:axes"
        )
    half_extents = _paper_newton_shape_runtime_construction_vector(
        source_row.get("descriptor_half_extents"),
        error_label=(
            "newton_shape_runtime_construction_descriptor_invalid:half_extents"
        ),
    )
    if any(value <= 0.0 for value in half_extents):
        raise ValueError(
            "newton_shape_runtime_construction_descriptor_invalid:half_extents"
        )
    return {
        "center": center,
        "axes": axes,
        "half_extents": half_extents,
    }
```

- [ ] **Step 4: Add input source row validator**

Add:

```python
def _paper_newton_shape_runtime_construction_source_row(
    preflight: dict[str, object],
) -> dict[str, object]:
    if (
        preflight.get("gate_id")
        != _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
    ):
        raise ValueError(
            "newton_shape_runtime_construction_input_gate_id_mismatch"
        )
    if (
        preflight.get("next_required_gate")
        != _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
    ):
        raise ValueError(
            "newton_shape_runtime_construction_input_next_gate_mismatch"
        )
    _paper_validate_primitivespec_runtime_construction_false_flags(
        preflight,
        error_prefix="newton_shape_runtime_construction_input_flag",
        required_false_flags=_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_PAYLOAD_FALSE_FLAGS,
    )
    expected_counts = {
        "newton_shape_runtime_boundary_preflight_row_count": 1,
        "source_shape_mapping_contract_row_count": 1,
        "later_newton_shape_runtime_construction_candidate_count": 1,
        "report_scoped_newton_shape_descriptor_count": 1,
        "mapping_attempt_count": 0,
        "newton_mapping_record_count": 0,
        "newton_shape_object_count": 0,
        "newton_runtime_execution_count": 0,
        "generated_runtime_primitive_spec_count": 1,
        "generated_primitive_spec_count": 1,
        "generated_collision_package_count": 1,
        "runtime_admissibility_check_count": 1,
        "offline_static_runtime_admissibility_check_count": 1,
    }
    for field_name, expected_value in expected_counts.items():
        if preflight.get(field_name) != expected_value:
            raise ValueError(
                "newton_shape_runtime_construction_input_count_mismatch:"
                f"{field_name}"
            )
    rows = preflight.get("newton_shape_runtime_boundary_preflight_rows")
    if not isinstance(rows, list | tuple) or len(rows) != 1:
        raise ValueError("newton_shape_runtime_construction_row_count_mismatch")
    row = rows[0]
    if not isinstance(row, dict):
        raise ValueError("newton_shape_runtime_construction_row_count_mismatch")
    _paper_validate_primitivespec_runtime_construction_false_flags(
        row,
        error_prefix="newton_shape_runtime_construction_input_flag",
        required_false_flags=_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_PAYLOAD_FALSE_FLAGS,
    )
    expected_row_values = {
        "newton_shape_runtime_boundary_preflight_row_id": (
            "newton_shape_runtime_boundary_preflight__paper_single_box__box"
        ),
        "source_shape_mapping_row_id": "newton_shape_mapping__paper_single_box__box",
        "source_newton_shape_mapping_preflight_row_id": (
            "newton_shape_mapping_preflight__paper_single_box__box"
        ),
        "source_runtime_admissibility_row_id": (
            "runtime_admissibility__paper_single_box__box"
        ),
        "source_package_id": (
            "paper_single_box:"
            f"{_PAPER_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT}"
        ),
        "source_asset_id": "paper_single_box",
        "fixture_id": "paper_single_box",
        "paper_primitive": "oriented_bounding_box",
        "primitive_spec_kind": "box",
        "primitive_id": "paper_single_box__oriented_bounding_box__box",
        "target_newton_shape_kind": "box",
        "descriptor_kind": "newton_shape_descriptor",
        "runtime_boundary_preflight_passed": True,
        "later_newton_shape_runtime_construction_candidate": True,
        "mapping_attempt_count": 0,
        "newton_mapping_record_count": 0,
        "newton_shape_object_count": 0,
        "newton_runtime_execution_count": 0,
    }
    for field_name, expected_value in expected_row_values.items():
        if row.get(field_name) != expected_value:
            raise ValueError(
                "newton_shape_runtime_construction_source_row_mismatch:"
                f"{field_name}"
            )
    _paper_validate_newton_shape_runtime_construction_descriptor(row)
    if list(_paper_runtime_admissibility_preflight_package_dicts(preflight)):
        raise ValueError(
            "newton_shape_runtime_construction_source_package_copy_forbidden"
        )
    return row
```

- [ ] **Step 5: Add the repo-local mapping construction helper**

Add:

```python
def _paper_constructed_newton_shape_mapping_dict(
    source_row: dict[str, object],
) -> dict[str, object]:
    from primitive_collision_compiler.reports.schema import NewtonShapeMapping

    descriptor = _paper_validate_newton_shape_runtime_construction_descriptor(
        source_row
    )
    mapping = NewtonShapeMapping(
        primitive_id=str(source_row["primitive_id"]),
        kind="box",
        status="mapped",
        detail="mapped",
        center=tuple(descriptor["center"]),
        axes=tuple(tuple(axis) for axis in descriptor["axes"]),
        dimensions={
            "half_extents": list(descriptor["half_extents"]),
        },
    )
    return mapping.to_dict()
```

- [ ] **Step 6: Add row, coverage, and payload builders**

Add:

```python
def _paper_newton_shape_runtime_construction_row(
    source_row: dict[str, object],
) -> dict[str, object]:
    descriptor = _paper_validate_newton_shape_runtime_construction_descriptor(
        source_row
    )
    mapping_dict = _paper_constructed_newton_shape_mapping_dict(source_row)
    return {
        "newton_shape_runtime_construction_row_id": (
            "newton_shape_runtime_construction__paper_single_box__box"
        ),
        "source_newton_shape_runtime_boundary_preflight_row_id": source_row[
            "newton_shape_runtime_boundary_preflight_row_id"
        ],
        "source_shape_mapping_row_id": source_row["source_shape_mapping_row_id"],
        "source_newton_shape_mapping_preflight_row_id": source_row[
            "source_newton_shape_mapping_preflight_row_id"
        ],
        "source_runtime_admissibility_row_id": source_row[
            "source_runtime_admissibility_row_id"
        ],
        "source_package_id": source_row["source_package_id"],
        "source_asset_id": source_row["source_asset_id"],
        "fixture_id": source_row["fixture_id"],
        "paper_primitive": source_row["paper_primitive"],
        "primitive_spec_kind": source_row["primitive_spec_kind"],
        "primitive_id": source_row["primitive_id"],
        "target_newton_shape_kind": source_row["target_newton_shape_kind"],
        "descriptor_kind": source_row["descriptor_kind"],
        "descriptor_center": descriptor["center"],
        "descriptor_axes": descriptor["axes"],
        "descriptor_half_extents": descriptor["half_extents"],
        "constructed_newton_shape_mapping_dict": mapping_dict,
        "constructed_newton_shape_mapping_status": "mapped",
        "constructed_newton_shape_mapping_detail": "mapped",
        "mapping_constructor": "NewtonShapeMapping",
        "mapping_constructor_input_kind": "static_descriptor_fields",
        "runtime_builder_preflight_candidate": True,
        "constructed_newton_shape_mapping_record_count": 1,
        "newton_mapping_record_count": 1,
        "newton_mapper_call_count": 0,
        "newton_shape_object_count": 0,
        "newton_engine_shape_object_count": 0,
        "newton_builder_shape_call_count": 0,
        "newton_runtime_execution_count": 0,
        **_paper_newton_shape_runtime_construction_false_flags(),
        **_paper_newton_shape_runtime_construction_true_flags(),
    }


def _paper_newton_shape_runtime_construction_coverage_summary(
    rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "newton_shape_runtime_construction_row_count": len(rows),
        "source_newton_shape_runtime_boundary_preflight_row_count": len(rows),
        "constructed_newton_shape_mapping_record_count": sum(
            int(row["constructed_newton_shape_mapping_record_count"])
            for row in rows
        ),
        "newton_mapping_record_count": sum(
            int(row["newton_mapping_record_count"]) for row in rows
        ),
        "newton_mapper_call_count": 0,
        "newton_shape_object_count": 0,
        "newton_engine_shape_object_count": 0,
        "newton_builder_shape_call_count": 0,
        "newton_runtime_execution_count": 0,
        "runtime_builder_preflight_candidate_count": sum(
            bool(row["runtime_builder_preflight_candidate"]) for row in rows
        ),
        "fixture_id_distribution": _paper_policy_distribution(rows, "fixture_id"),
        "target_newton_shape_kind_distribution": _paper_policy_distribution(
            rows,
            "target_newton_shape_kind",
        ),
    }


def _paper_mapped_subset_newton_shape_runtime_construction_contract_payload(
    preflight: dict[str, object],
) -> dict[str, object]:
    source_row = _paper_newton_shape_runtime_construction_source_row(preflight)
    row = _paper_newton_shape_runtime_construction_row(source_row)
    rows = [row]
    remaining_gaps = (
        _paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_construction()
    )
    return {
        "gate_id": (
            _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
        ),
        "gate_status": (
            "implemented_single_fixture_newton_shape_mapping_record_"
            "construction_contract_only_partial"
        ),
        "closed_gate": (
            _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
        ),
        "input_gate_id": (
            _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
        ),
        "next_required_gate": (
            _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT
        ),
        "decision": "remain_partial",
        "decision_reason": (
            "newton_shape_mapping_record_construction_complete_"
            "newton_shape_runtime_builder_preflight_missing"
        ),
        "artifact_kind": (
            "repo_local_newton_shape_mapping_to_dict_not_newton_engine_shape"
        ),
        "schema_version": 1,
        "source_scope": "synthetic_toy_fixtures_only",
        "implementation_boundary": (
            "single_synthetic_box_newton_shape_mapping_record_only_"
            "no_newton_engine_shape_no_runtime_no_real_usd_no_benchmark_no_metrics"
        ),
        "runtime_construction_action": (
            "construct_one_repo_local_newton_shape_mapping_from_static_descriptor_"
            "without_newton_import"
        ),
        "newton_shape_runtime_construction_contract": {
            "input_gate_required": (
                _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
            ),
            "closed_gate": (
                _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
            ),
            "next_newton_shape_runtime_builder_preflight_gate_required": (
                _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT
            ),
            "source_runtime_boundary_preflight_rows_required": 1,
            "newton_shape_mapping_to_dict_records_required": 1,
            "newton_mapper_call_allowed": False,
            "newton_engine_shape_object_allowed": False,
            "newton_builder_shape_call_allowed": False,
            "newton_runtime_allowed": False,
            "newton_support_claim_allowed": False,
        },
        "input_contract_summary": {
            "input_gate_id": preflight["gate_id"],
            "input_next_required_gate": preflight["next_required_gate"],
            "source_newton_shape_runtime_boundary_preflight_row_id": source_row[
                "newton_shape_runtime_boundary_preflight_row_id"
            ],
            "source_shape_mapping_row_id": source_row["source_shape_mapping_row_id"],
            "source_package_id": source_row["source_package_id"],
            "source_fixture_id": source_row["fixture_id"],
            "source_primitive_id": source_row["primitive_id"],
            "source_target_newton_shape_kind": source_row[
                "target_newton_shape_kind"
            ],
            "source_descriptor_kind": source_row["descriptor_kind"],
            "input_construction_candidate_count": 1,
        },
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
        "newton_shape_runtime_construction_rows": rows,
        "coverage_summary": (
            _paper_newton_shape_runtime_construction_coverage_summary(rows)
        ),
        "remaining_gaps": remaining_gaps,
        **_paper_newton_shape_runtime_construction_false_flags(),
        **_paper_newton_shape_runtime_construction_true_flags(),
    }
```

- [ ] **Step 7: Wire the new payload into `build_cpd_paper_offline_report()`**

After building `mapped_subset_newton_shape_runtime_boundary_preflight`, add:

```python
mapped_subset_newton_shape_runtime_construction = (
    _paper_mapped_subset_newton_shape_runtime_construction_contract_payload(
        mapped_subset_newton_shape_runtime_boundary_preflight
    )
)
```

Change:

```python
runtime_lane_remaining_gates = (
    _paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_boundary_preflight()
)
```

to:

```python
runtime_lane_remaining_gates = (
    _paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_construction()
)
```

Append the new implemented output contract:

```python
_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT,
```

Add the payload to the returned report:

```python
"paper_mapped_subset_newton_shape_runtime_construction_contract": (
    mapped_subset_newton_shape_runtime_construction
),
```

- [ ] **Step 8: Run focused tests**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_construction or newton_shape_runtime_boundary_preflight or newton_shape_mapping_contract' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Expected: pass, or fail only on documentation expectations not yet updated.

## Task 5: Documentation And Record Updates

**Files:**
- Modify: `README.md`
- Modify: `docs/index.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/deepdive/message-map.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- Modify: `docs/records/README.md`
- Create: `docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-construction-contract.md`

- [ ] **Step 1: Update user-facing story wording**

Use these exact claim boundaries wherever the new gate is described:

```markdown
The current runtime lane now constructs one repo-local `NewtonShapeMapping.to_dict()`
report record from the single synthetic `paper_single_box` static descriptor. This is
not a Newton engine shape, does not call a Newton builder, does not import Newton or
warp, does not execute contact/drop/sphere-rain diagnostics, does not load real USD,
does not run a benchmark, and does not measure collision quality.
```

Update the current next gate to:

```markdown
paper_mapped_subset_newton_shape_runtime_builder_preflight_contract
```

Use this short plain-language explanation in `docs/reference/cpd-paper-story-status.md`:

```markdown
In plain terms, the previous step checked that the box descriptor was ready to approach
a runtime boundary. This step turns that descriptor into the repository's JSON-safe
Newton shape mapping record. The next missing step is still the real runtime boundary:
checking whether that record may approach a Newton builder call.
```

- [ ] **Step 2: Add the dated record**

Create `docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-construction-contract.md`:

```markdown
# CPD Paper Mapped-Subset Newton Shape Runtime-Construction Contract

Date: 2026-05-18

## Summary

Closed `paper_mapped_subset_newton_shape_runtime_construction_contract` for the
single synthetic `paper_single_box` mapped subset.

This record means the offline CPD paper report now constructs exactly one repo-local
`NewtonShapeMapping.to_dict()` record from the static descriptor emitted by
`paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`.

## Boundary

- Newton engine shape object count: `0`
- Newton builder shape calls: `0`
- Newton runtime execution count: `0`
- Generic shape mapper calls: `0`
- Real USD loads: `0`
- Benchmark runs: `0`
- Collision-quality measurements: `0`
- Paper-faithful offline support claim: `false`

## Evidence

- New report gate:
  `paper_mapped_subset_newton_shape_runtime_construction_contract`
- Constructed record count:
  `constructed_newton_shape_mapping_record_count: 1`
- Runtime-facing record count:
  `newton_mapping_record_count: 1`
- Next required gate:
  `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`

## Verification

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_construction or newton_shape_runtime_boundary_preflight or newton_shape_mapping_contract' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

## Next Gate

`paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`
```

After final verification, append the actual command results to the `Verification` section.

- [ ] **Step 3: Register the record**

Add the new record to `docs/records/README.md` near the other 2026-05-18 Newton shape records with the same concise wording.

- [ ] **Step 4: Validate docs and claim wording**

Run:

```bash
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: docs validation passed, site claim validation passed, no whitespace errors.

## Task 6: Review, Verification, And Commit

**Files:**
- Review all modified files from previous tasks.

- [ ] **Step 1: Request parallel implementation review**

Dispatch three independent reviewers:

- API reviewer: verify the implementation constructs only `NewtonShapeMapping.to_dict()` and does not cross into `primitive_collision_compiler.newton`, Newton/warp, builder, diagnostics, USD, benchmark, or collision-quality code.
- Claim reviewer: verify docs and report fields do not claim Newton support/readiness, benchmark results, collision-quality evidence, real-USD evidence, deployment readiness, or paper-faithful offline completion.
- Test reviewer: verify tests cover positive payload, exact schema, lineage, input drift, descriptor validation, source package copy rejection, and static boundary behavior.

- [ ] **Step 2: Apply only substantiated review feedback**

For each finding, inspect the cited file and either patch the issue or record why the finding is not valid. Do not broaden scope beyond this single gate.

- [ ] **Step 3: Run focused verification**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_construction or newton_shape_runtime_boundary_preflight or newton_shape_mapping_contract' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

- [ ] **Step 4: Run broader verification**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -q
PYTHONPATH=src python -m pytest -q
```

Expected: all pass. If the full suite is too slow to complete within the working session, keep the focused evidence and explicitly record the incomplete full-suite status in the dated record and final report.

- [ ] **Step 5: Commit the implementation checkpoint**

Run:

```bash
git status --short
git add \
  src/primitive_collision_compiler/baselines/cpd_paper/offline.py \
  tests/test_cpd_paper_offline.py \
  tests/test_cli.py \
  README.md \
  docs/index.md \
  docs/deepdive/evidence-status.md \
  docs/deepdive/message-map.md \
  docs/reference/claim-boundaries.md \
  docs/reference/cpd-paper-faithful-offline-lane-spec.md \
  docs/reference/cpd-paper-reproduction-gap-matrix.md \
  docs/reference/cpd-paper-story-status.md \
  docs/reference/cpd-paper-fixture-breadth-expansion-plan.md \
  docs/records/README.md \
  docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-construction-contract.md
git commit -m "feat: add CPD Newton shape runtime-construction contract"
```

## Self-Review Checklist

- [ ] The new gate constructs one `NewtonShapeMapping.to_dict()` report record.
- [ ] `newton_mapping_record_count` is `1` only after this gate.
- [ ] `newton_mapper_call_count`, `newton_shape_object_count`, `newton_engine_shape_object_count`, `newton_builder_shape_call_count`, and `newton_runtime_execution_count` remain `0`.
- [ ] The next gate is `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`.
- [ ] The previous runtime-boundary preflight payload still points to `paper_mapped_subset_newton_shape_runtime_construction_contract`.
- [ ] Tests reject malformed input, descriptor drift, non-orthonormal or left-handed axes, and source package copies.
- [ ] Static tests allow exactly one local `NewtonShapeMapping(` construction and forbid Newton/warp/runtime/builder/USD/benchmark/collision-quality execution tokens.
- [ ] Docs preserve DeepDive and claim boundaries.
