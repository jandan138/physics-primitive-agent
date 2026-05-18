# CPD Paper Mapped-Subset Newton Shape Runtime-Boundary Preflight Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the bounded offline/report-only `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract` gate after the existing Newton shape-mapping contract gate.

**Architecture:** Extend the existing `cpd_paper_offline_report` runtime-lane chain by consuming the shape-mapping contract payload and emitting exactly one static preflight row for a later Newton shape runtime-construction gate. The slice must stay report-only: no Newton imports, no mapper calls, no Newton shape objects, no runtime execution, no USD, no benchmark, no collision-quality measurement.

**Tech Stack:** Python, pytest, Markdown docs, existing `primitive_collision_compiler.baselines.cpd_paper.offline` report builders.

---

## File Structure

- Modify `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
  - Add `_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT`.
  - Add a helper that advances remaining gaps after
    `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`.
  - Add runtime-boundary preflight validation/build helpers after the existing shape-mapping
    contract helpers.
  - Wire the new payload into `build_cpd_paper_offline_report()`.
- Modify `tests/test_cpd_paper_offline.py`
  - Add `inspect` import.
  - Add constants, false-flag sets, required-key sets, positive tests, negative input-drift tests,
    and static boundary tests.
  - Update all top-level `build_cpd_paper_offline_report()["next_required_gate"]` assertions that
    currently point at `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract` to
    point at `paper_mapped_subset_newton_shape_runtime_construction_contract`.
- Modify `tests/test_cli.py`
  - Update the offline report expected failure label and next gate.
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
  - Create `docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-boundary-preflight-contract.md`

## Task 1: RED Tests For The Runtime-Boundary Preflight Contract

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add constants and key sets**

Add `inspect` to the imports:

```python
import inspect
```

Add near the existing Newton shape-mapping contract constants:

```python
EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_construction_contract"
)
EXPECTED_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT,
]
```

Update `EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS` to point at
`EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT`.

Update every top-level offline-report next-gate assertion that currently checks:

```python
report["next_required_gate"] == (
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
)
```

to check:

```python
report["next_required_gate"] == (
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
)
```

Do not change payload-local assertions for earlier gates. In particular,
`paper_mapped_subset_newton_shape_mapping_contract["next_required_gate"]` must remain
`EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT`.

Add runtime-boundary preflight false flags:

```python
NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_FALSE_FLAGS = (
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
    "newton_shape_mapping_record_created",
    "newton_shape_object_created",
    "newton_shape_runtime_construction_triggered",
    "newton_shape_runtime_boundary_crossed",
)
```

Add exact payload and row required-key sets:

```python
NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_ROW_REQUIRED_KEYS = frozenset(
    {
        "newton_shape_runtime_boundary_preflight_row_id",
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
        "runtime_boundary_preflight_passed",
        "descriptor_kind_check_passed",
        "target_kind_check_passed",
        "descriptor_lineage_check_passed",
        "center_descriptor_check_passed",
        "axes_descriptor_check_passed",
        "half_extents_descriptor_check_passed",
        "later_newton_shape_runtime_construction_candidate",
        "mapping_attempt_count",
        "newton_mapping_record_count",
        "newton_shape_object_count",
        "newton_runtime_execution_count",
        *NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_FALSE_FLAGS,
    }
)

NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_PAYLOAD_REQUIRED_KEYS = frozenset(
    {
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
        "runtime_boundary_preflight_action",
        "newton_shape_runtime_boundary_preflight_contract",
        "input_contract_summary",
        "newton_shape_runtime_boundary_preflight_row_count",
        "source_shape_mapping_contract_row_count",
        "later_newton_shape_runtime_construction_candidate_count",
        "report_scoped_newton_shape_descriptor_count",
        "runtime_boundary_preflight_passed",
        "mapping_attempt_count",
        "newton_mapping_record_count",
        "newton_shape_object_count",
        "newton_runtime_execution_count",
        "generated_runtime_primitive_spec_count",
        "generated_primitive_spec_count",
        "generated_collision_package_count",
        "runtime_admissibility_check_count",
        "offline_static_runtime_admissibility_check_count",
        "newton_shape_runtime_boundary_preflight_rows",
        "coverage_summary",
        "remaining_gaps",
        *NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_FALSE_FLAGS,
    }
)
```

- [ ] **Step 2: Add helper to fetch the input shape-mapping contract payload**

Add near `_newton_shape_mapping_contract_input()`:

```python
def _newton_shape_runtime_boundary_preflight_input() -> dict[str, object]:
    report = build_cpd_paper_offline_report()
    return json.loads(
        json.dumps(
            report["paper_mapped_subset_newton_shape_mapping_contract"]
        )
    )
```

- [ ] **Step 3: Add positive tests**

Add tests after the shape-mapping contract tests:

```python
def test_cpd_paper_records_newton_shape_runtime_boundary_preflight_gate():
    report = build_cpd_paper_offline_report()
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"
    ]

    assert report["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
    )
    assert report["failure_labels"] == [
        "paper_mapped_subset_newton_shape_runtime_construction_contract_missing"
    ]
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_REMAINING_GAPS
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
    )
    assert payload["newton_shape_runtime_boundary_preflight_row_count"] == 1
    assert payload["source_shape_mapping_contract_row_count"] == 1
    assert payload["later_newton_shape_runtime_construction_candidate_count"] == 1
    assert payload["report_scoped_newton_shape_descriptor_count"] == 1
    assert payload["runtime_boundary_preflight_passed"] is True
    assert payload["mapping_attempt_count"] == 0
    assert payload["newton_mapping_record_count"] == 0
    assert payload["newton_shape_object_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0


def test_cpd_paper_newton_shape_runtime_boundary_preflight_payload_schema_is_exact():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"
    ]

    assert set(payload) == NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_PAYLOAD_REQUIRED_KEYS
    assert payload["gate_status"] == (
        "implemented_offline_newton_shape_runtime_boundary_preflight_only"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_shape_runtime_boundary_preflight_complete_"
        "newton_shape_runtime_construction_missing"
    )
    assert payload["artifact_kind"] == (
        "offline_static_newton_shape_runtime_boundary_preflight_not_shape_object"
    )
    assert payload["newton_shape_runtime_boundary_preflight_contract"] == {
        "input_gate_required": EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT,
        "closed_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
        ),
        "next_newton_shape_runtime_construction_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
        ),
        "runtime_boundary_preflight_rows_required": 1,
        "later_newton_shape_runtime_construction_candidates_required": 1,
        "newton_shape_object_allowed": False,
        "newton_runtime_allowed": False,
        "newton_support_claim_allowed": False,
    }


def test_cpd_paper_newton_shape_runtime_boundary_preflight_records_row():
    report = build_cpd_paper_offline_report()
    source_row = report["paper_mapped_subset_newton_shape_mapping_contract"][
        "shape_mapping_rows"
    ][0]
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"
    ]
    rows = payload["newton_shape_runtime_boundary_preflight_rows"]

    assert len(rows) == 1
    row = rows[0]
    assert set(row) == NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_ROW_REQUIRED_KEYS
    assert row["newton_shape_runtime_boundary_preflight_row_id"] == (
        "newton_shape_runtime_boundary_preflight__paper_single_box__box"
    )
    assert row["source_shape_mapping_row_id"] == source_row["shape_mapping_row_id"]
    assert row["target_newton_shape_kind"] == "box"
    assert row["descriptor_kind"] == "newton_shape_descriptor"
    assert row["descriptor_center"] == source_row["newton_shape_descriptor_dict"]["center"]
    assert row["descriptor_axes"] == source_row["newton_shape_descriptor_dict"]["axes"]
    assert row["descriptor_half_extents"] == (
        source_row["newton_shape_descriptor_dict"]["half_extents"]
    )
    assert row["runtime_boundary_preflight_passed"] is True
    assert row["later_newton_shape_runtime_construction_candidate"] is True
    assert row["newton_shape_object_count"] == 0
    assert row["newton_runtime_execution_count"] == 0


@pytest.mark.parametrize("flag", NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_FALSE_FLAGS)
def test_cpd_paper_newton_shape_runtime_boundary_preflight_boundary_flags_are_false(flag):
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"
    ]
    row = payload["newton_shape_runtime_boundary_preflight_rows"][0]

    assert payload[flag] is False
    assert row[flag] is False
```

- [ ] **Step 4: Add boundary and negative tests**

Add tests that mutate `_newton_shape_runtime_boundary_preflight_input()` and expect these errors:

```python
def test_cpd_paper_newton_shape_runtime_boundary_preflight_rejects_input_gate_drift():
    payload = _newton_shape_runtime_boundary_preflight_input()
    payload["gate_id"] = "wrong"

    with pytest.raises(ValueError, match="newton_shape_runtime_boundary_preflight_input_gate_id_mismatch"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_payload(payload)


def test_cpd_paper_newton_shape_runtime_boundary_preflight_rejects_input_next_gate_drift():
    payload = _newton_shape_runtime_boundary_preflight_input()
    payload["next_required_gate"] = "wrong"

    with pytest.raises(ValueError, match="newton_shape_runtime_boundary_preflight_input_next_gate_mismatch"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_payload(payload)


def test_cpd_paper_newton_shape_runtime_boundary_preflight_rejects_forbidden_input_flags():
    for flag in NEWTON_SHAPE_MAPPING_CONTRACT_FALSE_FLAGS:
        payload = _newton_shape_runtime_boundary_preflight_input()
        payload[flag] = True

        with pytest.raises(ValueError, match="newton_shape_runtime_boundary_preflight_input_flag"):
            cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_payload(payload)


@pytest.mark.parametrize(
    ("field_name", "bad_value"),
    (
        ("shape_mapping_contract_row_count", 2),
        ("source_newton_shape_mapping_preflight_row_count", 2),
        ("report_scoped_newton_shape_descriptor_count", 2),
        ("mapping_attempt_count", 1),
        ("newton_mapping_record_count", 1),
        ("newton_shape_object_count", 1),
        ("newton_runtime_execution_count", 1),
        ("generated_runtime_primitive_spec_count", 0),
        ("generated_primitive_spec_count", 0),
        ("generated_collision_package_count", 0),
        ("runtime_admissibility_check_count", 0),
        ("offline_static_runtime_admissibility_check_count", 0),
    ),
)
def test_cpd_paper_newton_shape_runtime_boundary_preflight_rejects_count_drift(field_name, bad_value):
    payload = _newton_shape_runtime_boundary_preflight_input()
    payload[field_name] = bad_value

    with pytest.raises(ValueError, match=f"newton_shape_runtime_boundary_preflight_input_count_mismatch:{field_name}"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_payload(payload)


def test_cpd_paper_newton_shape_runtime_boundary_preflight_rejects_row_count_drift():
    payload = _newton_shape_runtime_boundary_preflight_input()
    payload["shape_mapping_rows"] = []

    with pytest.raises(ValueError, match="newton_shape_runtime_boundary_preflight_row_count_mismatch"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_payload(payload)


@pytest.mark.parametrize(
    "field_name",
    (
        "mapping_attempt_count",
        "newton_mapping_record_count",
        "newton_shape_object_count",
        "newton_runtime_execution_count",
    ),
)
def test_cpd_paper_newton_shape_runtime_boundary_preflight_rejects_source_row_count_drift(field_name):
    payload = _newton_shape_runtime_boundary_preflight_input()
    row = dict(payload["shape_mapping_rows"][0])
    row[field_name] = 1
    payload["shape_mapping_rows"] = [row]

    with pytest.raises(ValueError, match=f"newton_shape_runtime_boundary_preflight_source_row_mismatch:{field_name}"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_payload(payload)


def test_cpd_paper_newton_shape_runtime_boundary_preflight_rejects_descriptor_kind_drift():
    payload = _newton_shape_runtime_boundary_preflight_input()
    row = dict(payload["shape_mapping_rows"][0])
    descriptor = dict(row["newton_shape_descriptor_dict"])
    descriptor["descriptor_kind"] = "wrong"
    row["newton_shape_descriptor_dict"] = descriptor
    payload["shape_mapping_rows"] = [row]

    with pytest.raises(ValueError, match="newton_shape_runtime_boundary_preflight_descriptor_mismatch:descriptor_kind"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_payload(payload)


@pytest.mark.parametrize(
    ("field_name", "bad_value", "expected_label"),
    (
        ("shape_mapping_row_id", "wrong", "source_row_mismatch:shape_mapping_row_id"),
        ("target_newton_shape_kind", "sphere", "source_row_mismatch:target_newton_shape_kind"),
        ("fixture_id", "wrong", "source_row_mismatch:fixture_id"),
        ("primitive_id", "wrong", "source_row_mismatch:primitive_id"),
    ),
)
def test_cpd_paper_newton_shape_runtime_boundary_preflight_rejects_source_row_drift(
    field_name,
    bad_value,
    expected_label,
):
    payload = _newton_shape_runtime_boundary_preflight_input()
    row = dict(payload["shape_mapping_rows"][0])
    row[field_name] = bad_value
    payload["shape_mapping_rows"] = [row]

    with pytest.raises(ValueError, match=f"newton_shape_runtime_boundary_preflight_{expected_label}"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_payload(payload)


@pytest.mark.parametrize(
    ("field_name", "bad_value"),
    (
        ("target_newton_shape_kind", "sphere"),
        ("source_fixture_id", "wrong"),
        ("source_primitive_id", "wrong"),
        ("mapping_contract", "wrong"),
    ),
)
def test_cpd_paper_newton_shape_runtime_boundary_preflight_rejects_descriptor_lineage_drift(
    field_name,
    bad_value,
):
    payload = _newton_shape_runtime_boundary_preflight_input()
    row = dict(payload["shape_mapping_rows"][0])
    descriptor = dict(row["newton_shape_descriptor_dict"])
    descriptor[field_name] = bad_value
    row["newton_shape_descriptor_dict"] = descriptor
    payload["shape_mapping_rows"] = [row]

    with pytest.raises(ValueError, match=f"newton_shape_runtime_boundary_preflight_descriptor_mismatch:{field_name}"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_payload(payload)


@pytest.mark.parametrize(
    ("descriptor_value", "expected_label"),
    (
        (None, "descriptor_invalid:descriptor"),
        ([], "descriptor_invalid:descriptor"),
        ({"descriptor_kind": "newton_shape_descriptor"}, "descriptor_mismatch:target_newton_shape_kind"),
    ),
)
def test_cpd_paper_newton_shape_runtime_boundary_preflight_rejects_malformed_descriptor(
    descriptor_value,
    expected_label,
):
    payload = _newton_shape_runtime_boundary_preflight_input()
    row = dict(payload["shape_mapping_rows"][0])
    row["newton_shape_descriptor_dict"] = descriptor_value
    payload["shape_mapping_rows"] = [row]

    with pytest.raises(ValueError, match=f"newton_shape_runtime_boundary_preflight_{expected_label}"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_payload(payload)


def test_cpd_paper_newton_shape_runtime_boundary_preflight_rejects_descriptor_numeric_drift():
    payload = _newton_shape_runtime_boundary_preflight_input()
    row = dict(payload["shape_mapping_rows"][0])
    descriptor = dict(row["newton_shape_descriptor_dict"])
    descriptor["half_extents"] = [1.0, 0.0, 0.25]
    row["newton_shape_descriptor_dict"] = descriptor
    payload["shape_mapping_rows"] = [row]

    with pytest.raises(ValueError, match="newton_shape_runtime_boundary_preflight_descriptor_invalid:half_extents"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_payload(payload)


def test_cpd_paper_newton_shape_runtime_boundary_preflight_rejects_source_package_copy():
    payload = _newton_shape_runtime_boundary_preflight_input()
    package_payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_collision_package_generation_contract"
    ]
    payload["source_collision_package_dict"] = package_payload[
        "collision_package_generation_rows"
    ][0]["generated_collision_package"]

    with pytest.raises(ValueError, match="newton_shape_runtime_boundary_preflight_source_package_copy_forbidden"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_payload(payload)
```

Add a static source boundary test:

```python
def test_cpd_paper_newton_shape_runtime_boundary_preflight_static_boundary_has_no_runtime_calls():
    helpers = (
        cpd_paper_offline._paper_validate_newton_shape_runtime_boundary_descriptor,
        cpd_paper_offline._paper_newton_shape_runtime_boundary_preflight_source_row,
        cpd_paper_offline._paper_newton_shape_runtime_boundary_preflight_row,
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_payload,
    )
    source = "\n".join(inspect.getsource(helper) for helper in helpers)

    forbidden_patterns = (
        "import newton",
        "from newton",
        "import pxr",
        "from pxr",
        "Usd.Stage",
        ".simulate(",
        "run_benchmark",
        "collision_quality",
        "create_shape(",
        "create_box(",
        "Shape(",
        "map_package_shapes",
        "NewtonShapeMapping",
        "primitive_collision_compiler.newton",
    )
    for pattern in forbidden_patterns:
        assert pattern not in source
```

- [ ] **Step 5: Update CLI expectations**

In `tests/test_cli.py`, update `test_cli_run_cpd_paper_offline_report_emits_json`:

```python
assert payload["failure_labels"] == [
    "paper_mapped_subset_newton_shape_runtime_construction_contract_missing",
]
assert (
    payload["next_required_gate"]
    == "paper_mapped_subset_newton_shape_runtime_construction_contract"
)
assert payload["paper_faithfulness"]["runtime_lane_remaining_gates"] == [
    "paper_mapped_subset_newton_shape_runtime_construction_contract",
]
assert "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract" in (
    payload["paper_faithfulness"]["implemented_output_contract_scope"]
)
```

- [ ] **Step 6: Run RED tests**

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_boundary_preflight' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Expected before implementation: failures due to missing report key/helper and stale CLI next gate.

## Task 2: Implement The Runtime-Boundary Preflight Payload

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add the next gate constant and remaining-gaps helper**

Add near the existing Newton shape runtime-boundary preflight constant:

```python
_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_construction_contract"
)
```

Add after `_paper_remaining_gaps_after_mapped_subset_newton_shape_mapping_contract()`:

```python
def _paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_boundary_preflight() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT]
```

- [ ] **Step 2: Add false flags and descriptor validation helpers**

Add after the shape-mapping contract helpers:

```python
_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_FALSE_FLAGS = (
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
    "newton_shape_mapping_record_created",
    "newton_shape_object_created",
    "newton_shape_runtime_construction_triggered",
    "newton_shape_runtime_boundary_crossed",
)


def _paper_newton_shape_runtime_boundary_preflight_false_flags() -> dict[str, bool]:
    return {
        flag: False
        for flag in _NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_FALSE_FLAGS
    }
```

Add descriptor validation:

```python
def _paper_validate_newton_shape_runtime_boundary_descriptor(
    row: dict[str, object],
) -> dict[str, object]:
    descriptor = row.get("newton_shape_descriptor_dict")
    if not isinstance(descriptor, dict):
        raise ValueError(
            "newton_shape_runtime_boundary_preflight_descriptor_invalid:descriptor"
        )
    expected_pairs = {
        "descriptor_kind": "newton_shape_descriptor",
        "target_newton_shape_kind": row.get("target_newton_shape_kind"),
        "source_fixture_id": row.get("fixture_id"),
        "source_primitive_id": row.get("primitive_id"),
        "mapping_contract": "report_scoped_static_descriptor_no_newton_call",
    }
    for field_name, expected_value in expected_pairs.items():
        if descriptor.get(field_name) != expected_value:
            raise ValueError(
                "newton_shape_runtime_boundary_preflight_descriptor_mismatch:"
                f"{field_name}"
            )
    _paper_newton_shape_mapping_preflight_vector(
        descriptor.get("center"),
        error_label="newton_shape_runtime_boundary_preflight_descriptor_invalid:center",
    )
    axes = descriptor.get("axes")
    if not isinstance(axes, list | tuple) or len(axes) != 3:
        raise ValueError(
            "newton_shape_runtime_boundary_preflight_descriptor_invalid:axes"
        )
    for axis in axes:
        _paper_newton_shape_mapping_preflight_vector(
            axis,
            error_label=(
                "newton_shape_runtime_boundary_preflight_descriptor_invalid:axes"
            ),
        )
    half_extents = _paper_newton_shape_mapping_preflight_vector(
        descriptor.get("half_extents"),
        error_label=(
            "newton_shape_runtime_boundary_preflight_descriptor_invalid:half_extents"
        ),
    )
    if any(value <= 0.0 for value in half_extents):
        raise ValueError(
            "newton_shape_runtime_boundary_preflight_descriptor_invalid:half_extents"
        )
    return descriptor
```

- [ ] **Step 3: Add input source-row validation**

```python
def _paper_newton_shape_runtime_boundary_preflight_source_row(
    contract: dict[str, object],
) -> dict[str, object]:
    if contract.get("gate_id") != _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT:
        raise ValueError(
            "newton_shape_runtime_boundary_preflight_input_gate_id_mismatch"
        )
    if (
        contract.get("next_required_gate")
        != _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
    ):
        raise ValueError(
            "newton_shape_runtime_boundary_preflight_input_next_gate_mismatch"
        )
    _paper_validate_primitivespec_runtime_construction_false_flags(
        contract,
        error_prefix="newton_shape_runtime_boundary_preflight_input_flag",
        required_false_flags=_NEWTON_SHAPE_MAPPING_CONTRACT_PAYLOAD_FALSE_FLAGS,
    )
    expected_counts = {
        "shape_mapping_contract_row_count": 1,
        "source_newton_shape_mapping_preflight_row_count": 1,
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
        if contract.get(field_name) != expected_value:
            raise ValueError(
                "newton_shape_runtime_boundary_preflight_input_count_mismatch:"
                f"{field_name}"
            )
    rows = contract.get("shape_mapping_rows")
    if not isinstance(rows, list | tuple) or len(rows) != 1:
        raise ValueError(
            "newton_shape_runtime_boundary_preflight_row_count_mismatch"
        )
    row = rows[0]
    if not isinstance(row, dict):
        raise ValueError(
            "newton_shape_runtime_boundary_preflight_row_count_mismatch"
        )
    _paper_validate_primitivespec_runtime_construction_false_flags(
        row,
        error_prefix="newton_shape_runtime_boundary_preflight_input_flag",
        required_false_flags=_NEWTON_SHAPE_MAPPING_CONTRACT_PAYLOAD_FALSE_FLAGS,
    )
    expected_row_values = {
        "shape_mapping_row_id": "newton_shape_mapping__paper_single_box__box",
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
        "descriptor_contract_passed": True,
        "mapping_attempt_count": 0,
        "newton_mapping_record_count": 0,
        "newton_shape_object_count": 0,
        "newton_runtime_execution_count": 0,
    }
    for field_name, expected_value in expected_row_values.items():
        if row.get(field_name) != expected_value:
            raise ValueError(
                "newton_shape_runtime_boundary_preflight_source_row_mismatch:"
                f"{field_name}"
            )
    _paper_validate_newton_shape_runtime_boundary_descriptor(row)
    if list(_paper_runtime_admissibility_preflight_package_dicts(contract)):
        raise ValueError(
            "newton_shape_runtime_boundary_preflight_source_package_copy_forbidden"
        )
    return row
```

- [ ] **Step 4: Add row, coverage, and payload builders**

```python
def _paper_newton_shape_runtime_boundary_preflight_row(
    source_row: dict[str, object],
) -> dict[str, object]:
    descriptor = _paper_validate_newton_shape_runtime_boundary_descriptor(source_row)
    return {
        "newton_shape_runtime_boundary_preflight_row_id": (
            "newton_shape_runtime_boundary_preflight__paper_single_box__box"
        ),
        "source_shape_mapping_row_id": source_row["shape_mapping_row_id"],
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
        "descriptor_kind": descriptor["descriptor_kind"],
        "descriptor_center": descriptor["center"],
        "descriptor_axes": descriptor["axes"],
        "descriptor_half_extents": descriptor["half_extents"],
        "runtime_boundary_preflight_passed": True,
        "descriptor_kind_check_passed": True,
        "target_kind_check_passed": True,
        "descriptor_lineage_check_passed": True,
        "center_descriptor_check_passed": True,
        "axes_descriptor_check_passed": True,
        "half_extents_descriptor_check_passed": True,
        "later_newton_shape_runtime_construction_candidate": True,
        "mapping_attempt_count": 0,
        "newton_mapping_record_count": 0,
        "newton_shape_object_count": 0,
        "newton_runtime_execution_count": 0,
        **_paper_newton_shape_runtime_boundary_preflight_false_flags(),
    }


def _paper_newton_shape_runtime_boundary_preflight_coverage_summary(
    rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "newton_shape_runtime_boundary_preflight_row_count": len(rows),
        "source_shape_mapping_contract_row_count": len(rows),
        "later_newton_shape_runtime_construction_candidate_count": sum(
            bool(row["later_newton_shape_runtime_construction_candidate"])
            for row in rows
        ),
        "report_scoped_newton_shape_descriptor_count": len(rows),
        "runtime_boundary_preflight_passed_count": sum(
            bool(row["runtime_boundary_preflight_passed"]) for row in rows
        ),
        "mapping_attempt_count": 0,
        "newton_mapping_record_count": 0,
        "newton_shape_object_count": 0,
        "newton_runtime_execution_count": 0,
        "fixture_id_distribution": _paper_policy_distribution(rows, "fixture_id"),
        "target_newton_shape_kind_distribution": _paper_policy_distribution(
            rows,
            "target_newton_shape_kind",
        ),
    }
```

Add payload builder:

```python
def _paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_payload(
    contract: dict[str, object],
) -> dict[str, object]:
    source_row = _paper_newton_shape_runtime_boundary_preflight_source_row(
        contract
    )
    row = _paper_newton_shape_runtime_boundary_preflight_row(source_row)
    rows = [row]
    remaining_gaps = (
        _paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_boundary_preflight()
    )
    return {
        "gate_id": (
            _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
        ),
        "gate_status": (
            "implemented_offline_newton_shape_runtime_boundary_preflight_only"
        ),
        "closed_gate": (
            _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
        ),
        "input_gate_id": _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT,
        "next_required_gate": (
            _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
        ),
        "decision": "remain_partial",
        "decision_reason": (
            "newton_shape_runtime_boundary_preflight_complete_"
            "newton_shape_runtime_construction_missing"
        ),
        "artifact_kind": (
            "offline_static_newton_shape_runtime_boundary_preflight_not_shape_object"
        ),
        "schema_version": 1,
        "source_scope": "synthetic_toy_fixtures_only",
        "implementation_boundary": (
            "single_synthetic_box_newton_shape_runtime_boundary_preflight_only_"
            "no_newton_object_no_runtime_no_real_usd_no_benchmark_no_metrics"
        ),
        "runtime_boundary_preflight_action": (
            "record_one_later_newton_shape_runtime_construction_candidate_"
            "without_newton_call"
        ),
        "newton_shape_runtime_boundary_preflight_contract": {
            "input_gate_required": (
                _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT
            ),
            "closed_gate": (
                _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
            ),
            "next_newton_shape_runtime_construction_gate_required": (
                _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
            ),
            "runtime_boundary_preflight_rows_required": 1,
            "later_newton_shape_runtime_construction_candidates_required": 1,
            "newton_shape_object_allowed": False,
            "newton_runtime_allowed": False,
            "newton_support_claim_allowed": False,
        },
        "input_contract_summary": {
            "input_gate_id": contract["gate_id"],
            "input_next_required_gate": contract["next_required_gate"],
            "source_shape_mapping_row_id": source_row["shape_mapping_row_id"],
            "source_newton_shape_mapping_preflight_row_id": source_row[
                "source_newton_shape_mapping_preflight_row_id"
            ],
            "source_runtime_admissibility_row_id": source_row[
                "source_runtime_admissibility_row_id"
            ],
            "source_package_id": source_row["source_package_id"],
            "source_fixture_id": source_row["fixture_id"],
            "source_primitive_id": source_row["primitive_id"],
            "source_target_newton_shape_kind": source_row[
                "target_newton_shape_kind"
            ],
            "source_descriptor_kind": source_row[
                "newton_shape_descriptor_dict"
            ]["descriptor_kind"],
        },
        "newton_shape_runtime_boundary_preflight_row_count": 1,
        "source_shape_mapping_contract_row_count": 1,
        "later_newton_shape_runtime_construction_candidate_count": 1,
        "report_scoped_newton_shape_descriptor_count": 1,
        "runtime_boundary_preflight_passed": True,
        "mapping_attempt_count": 0,
        "newton_mapping_record_count": 0,
        "newton_shape_object_count": 0,
        "newton_runtime_execution_count": 0,
        "generated_runtime_primitive_spec_count": 1,
        "generated_primitive_spec_count": 1,
        "generated_collision_package_count": 1,
        "runtime_admissibility_check_count": 1,
        "offline_static_runtime_admissibility_check_count": 1,
        "newton_shape_runtime_boundary_preflight_rows": rows,
        "coverage_summary": (
            _paper_newton_shape_runtime_boundary_preflight_coverage_summary(rows)
        ),
        "remaining_gaps": remaining_gaps,
        **_paper_newton_shape_runtime_boundary_preflight_false_flags(),
    }
```

- [ ] **Step 5: Wire into report builder**

Inside `build_cpd_paper_offline_report()`:

1. Build `mapped_subset_newton_shape_runtime_boundary_preflight` after
   `mapped_subset_newton_shape_mapping`.
2. Set `runtime_lane_remaining_gates` from
   `_paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_boundary_preflight()`.
3. Add `_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT` to
   `implemented_output_contract_scope`.
4. Add report key
   `"paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"`.
5. Update top-level next gate and failure label through existing `runtime_lane_remaining_gates`.

- [ ] **Step 6: Run GREEN focused tests**

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_boundary_preflight' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Expected: all selected tests pass.

## Task 3: Update Documentation And Dated Record

**Files:**
- Modify docs listed in File Structure.
- Create `docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-boundary-preflight-contract.md`.

- [ ] **Step 1: Update CPD story docs**

Update each doc to say:

- the previous descriptor contract is closed;
- the new runtime-boundary preflight is closed;
- it records one later Newton shape runtime-construction candidate for the synthetic
  `paper_single_box` box descriptor;
- it keeps mapping attempts, Newton mapping records, Newton shape objects, Newton runtime,
  real-USD, benchmark, and collision-quality evidence at zero or false;
- the current next gate is
  `paper_mapped_subset_newton_shape_runtime_construction_contract`;
- the slice is not Newton readiness, not Newton support, not Newton execution, not real-USD
  evidence, not benchmark evidence, not collision-quality evidence, not `paper_faithful_offline`,
  not full CPD reproduction, not deployment readiness, and not safety certification.

- [ ] **Step 2: Add the dated record**

Create the record with sections:

- Date
- Status
- Context
- What Changed
- Verification
- Artifacts
- Claim Boundary

Before final verification, set status to "Implemented in the feature branch. Final branch-wide
verification is still required before merge." After final verification, update to "Complete in the
feature branch" and append exact command results.

- [ ] **Step 3: Run docs checks**

```bash
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

## Task 4: Review And Final Verification

**Files:**
- All modified files.

- [ ] **Step 1: Request multi-agent review**

Dispatch at least two review agents:

1. Code/tests review: check gate chain, payload exactness, input validation, false flags, no
   Newton/USD/runtime/benchmark/collision-quality calls.
2. Docs/claim review: check no overclaims and current next gate consistency.

- [ ] **Step 2: Fix review findings**

Use `superpowers:receiving-code-review` discipline:

- verify each finding;
- fix valid blocker/important findings;
- rerun affected focused checks;
- request re-review when necessary.

- [ ] **Step 3: Run final verification**

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_boundary_preflight' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
PYTHONPATH=src python -m pytest -q
```

- [ ] **Step 4: Update dated record with final verification**

Add the exact results from Step 3 to the new record.

- [ ] **Step 5: Commit implementation**

```bash
git add README.md docs src tests
git commit -m "feat: add CPD Newton shape runtime-boundary preflight"
```

- [ ] **Step 6: Merge, verify on main, push, and cleanup**

```bash
cd /cpfs/user/zhuzihou/dev/physics-primitive-agent
git pull --ff-only
git merge --no-ff cpd-paper-newton-shape-runtime-boundary-preflight-contract -m "merge CPD Newton shape runtime-boundary preflight"
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
PYTHONPATH=src python -m pytest -q
git push origin main
git worktree remove /cpfs/user/zhuzihou/dev/physics-primitive-agent/.worktrees/cpd-paper-newton-shape-runtime-boundary-preflight-contract
git branch -d cpd-paper-newton-shape-runtime-boundary-preflight-contract
```
