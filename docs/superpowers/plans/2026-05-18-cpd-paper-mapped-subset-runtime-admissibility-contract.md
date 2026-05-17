# CPD Paper Mapped-Subset Runtime-Admissibility Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement `paper_mapped_subset_runtime_admissibility_contract` as a bounded offline/static runtime-admissibility check for the existing synthetic `paper_single_box` package artifact.

**Architecture:** Extend the CPD paper offline report chain after `paper_mapped_subset_runtime_admissibility_preflight_contract`. Validate the preflight row and source package identity, run one report-only static PrimitiveSpec/package admissibility check, record one compact row, and advance the next gate to `paper_mapped_subset_newton_shape_mapping_preflight_contract` while keeping Newton/USD/benchmark/runtime execution triggers false.

**Tech Stack:** Python report builders in `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`, `PrimitiveSpec.to_dict()` and `CollisionPackage.to_dict()` schema from `src/primitive_collision_compiler/contracts.py`, pytest, CLI JSON tests, Markdown docs.

---

### Task 1: Add RED Tests For The Runtime-Admissibility Contract Gate

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add the next gate constant and remaining gap expectation**

Add near the existing mapped-subset runtime-admissibility constants:

```python
EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_newton_shape_mapping_preflight_contract"
)
EXPECTED_RUNTIME_ADMISSIBILITY_CONTRACT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT,
]
```

Do not reuse `EXPECTED_RUNTIME_ADMISSIBILITY_CONTRACT_REMAINING_GAPS` for
`paper_faithfulness["missing_before_paper_faithful_offline"]`. That field must remain tied to the
paper-faithful offline scope blockers, not the Newton/runtime lane.

- [ ] **Step 2: Add helper for the new input payload**

Add near `_runtime_admissibility_preflight_input()`:

```python
def _runtime_admissibility_contract_input() -> dict[str, object]:
    report = build_cpd_paper_offline_report()
    return json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_runtime_admissibility_preflight_contract"
            ]
        )
    )
```

- [ ] **Step 3: Add required-key sets**

Add after `RUNTIME_ADMISSIBILITY_PREFLIGHT_ROW_REQUIRED_KEYS`:

```python
RUNTIME_ADMISSIBILITY_CONTRACT_PAYLOAD_FALSE_FLAGS = (
    "paper_faithful_offline_allowed",
    "paper_faithful_offline_supported",
    *(
        flag
        for flag in RUNTIME_CONSTRUCTION_FALSE_FLAGS
        if flag != "runtime_admissibility_checked"
    ),
)

RUNTIME_ADMISSIBILITY_CONTRACT_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "paper_faithful_offline_allowed",
    "paper_faithful_offline_supported",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "runtime_admissibility_action",
    "runtime_admissibility_requirements",
    "runtime_admissibility_row_count",
    "offline_static_runtime_admissibility_check_count",
    "offline_static_runtime_admissibility_checked",
    "runtime_admissibility_check_count",
    "runtime_execution_count",
    "newton_mapping_record_count",
    "newton_runtime_execution_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "source_collision_package_available",
    "runtime_admissibility_contract",
    "input_contract_summary",
    "runtime_admissibility_rows",
    "coverage_summary",
    "remaining_gaps",
    *RUNTIME_ADMISSIBILITY_CONTRACT_PAYLOAD_FALSE_FLAGS,
}

RUNTIME_ADMISSIBILITY_CONTRACT_ROW_REQUIRED_KEYS = {
    "runtime_admissibility_row_id",
    "source_runtime_admissibility_preflight_row_id",
    "source_collision_package_generation_row_id",
    "source_package_generation_preflight_row_id",
    "source_runtime_construction_row_id",
    "source_runtime_boundary_preflight_row_id",
    "source_native_fixture_primitivespec_serialization_row_id",
    "source_native_fixture_primitivespec_generation_row_id",
    "source_native_current_fixture_source_row_id",
    "source_candidate_source_audit_row_id",
    "source_primitivespec_generation_row_id",
    "source_primitivespec_generation_preflight_row_id",
    "source_primitivespec_validation_row_id",
    "source_primitivespec_dry_run_row_id",
    "source_adapter_preflight_row_id",
    "source_candidate_matrix_row_id",
    "source_conversion_plan_row_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "candidate_mapping_label",
    "newton_runtime_kind",
    "primitive_id",
    "kind",
    "candidate_primitivespec_dict",
    "source_package_id",
    "source_asset_id",
    "source_package_stage",
    "source_package_status",
    "source_package_method",
    "source_package_source_path",
    "source_package_source_sha256",
    "source_package_claim_boundary",
    "source_package_primitive_count",
    "source_package_primitive_subset",
    "source_package_unsupported_primitives",
    "source_collision_package_available",
    "runtime_admissibility_static_check_kind",
    "runtime_admissibility_decision",
    "runtime_admissibility_status",
    "required_later_gate",
    "finite_center_check_passed",
    "finite_axes_check_passed",
    "orthonormal_axes_check_passed",
    "right_handed_axes_check_passed",
    "positive_dimensions_check_passed",
    "target_shape_schema_check_passed",
    "source_faces_check_passed",
    "contains_assigned_points_check_passed",
    "volume_check_passed",
    "weighted_volume_check_passed",
    "offline_static_runtime_admissibility_check_passed",
    "offline_static_runtime_admissibility_checked",
    *RUNTIME_ADMISSIBILITY_CONTRACT_PAYLOAD_FALSE_FLAGS,
}
```

- [ ] **Step 4: Add report-level RED test**

Add:

```python
def test_cpd_paper_records_mapped_subset_runtime_admissibility_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_runtime_admissibility_contract"]

    assert report["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT
    )
    assert report["failure_labels"] == [
        "paper_mapped_subset_newton_shape_mapping_preflight_contract_missing"
    ]
    assert report["generated_collision_package_count"] == 1
    assert report["runtime_admissibility_check_count"] == 1
    assert (
        EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_RUNTIME_ADMISSIBILITY_CONTRACT_REMAINING_GAPS
    )
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT
    )
    assert payload["runtime_admissibility_row_count"] == 1
    assert payload["offline_static_runtime_admissibility_check_count"] == 1
    assert payload["offline_static_runtime_admissibility_checked"] is True
    assert payload["runtime_admissibility_check_count"] == 1
    assert payload["runtime_execution_count"] == 0
    assert payload["newton_mapping_record_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["generated_collision_package_count"] == 1
    assert payload["source_collision_package_available"] is True
    assert payload["remaining_gaps"] == (
        EXPECTED_RUNTIME_ADMISSIBILITY_CONTRACT_REMAINING_GAPS
    )
```

- [ ] **Step 5: Add payload schema and row RED tests**

Add:

```python
def test_cpd_paper_runtime_admissibility_contract_payload_schema_is_exact():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_runtime_admissibility_contract"
    ]

    assert set(payload) == RUNTIME_ADMISSIBILITY_CONTRACT_PAYLOAD_REQUIRED_KEYS
    assert payload["gate_status"] == (
        "implemented_single_fixture_runtime_admissibility_contract_"
        "static_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "runtime_admissibility_contract_complete_"
        "newton_shape_mapping_preflight_missing"
    )
    assert payload["artifact_kind"] == (
        "offline_static_runtime_admissibility_contract_not_newton_mapping"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_package_static_admissibility_only_"
        "no_newton_no_real_usd_no_benchmark_no_metrics"
    )
    assert payload["runtime_admissibility_action"] == (
        "run_one_offline_static_runtime_admissibility_check_for_"
        "paper_single_box_box_package"
    )
    assert payload["runtime_admissibility_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT
        ),
        "closed_gate": (
            EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT
        ),
        "next_newton_shape_mapping_preflight_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT
        ),
        "runtime_admissibility_rows_required": 1,
        "offline_static_runtime_admissibility_checks_required": 1,
        "runtime_execution_allowed": False,
        "newton_mapping_allowed": False,
    }
    assert payload["coverage_summary"] == {
        "runtime_admissibility_row_count": 1,
        "offline_static_runtime_admissibility_check_count": 1,
        "passed_static_runtime_admissibility_check_count": 1,
        "runtime_execution_count": 0,
        "newton_mapping_record_count": 0,
        "fixture_id_distribution": {"paper_single_box": 1},
        "primitive_subset_distribution": {"box": 1},
    }


def test_cpd_paper_runtime_admissibility_contract_records_static_check_row():
    report = build_cpd_paper_offline_report()
    source_payload = report[
        "paper_mapped_subset_runtime_admissibility_preflight_contract"
    ]
    source_row = source_payload["runtime_admissibility_preflight_rows"][0]
    payload = report["paper_mapped_subset_runtime_admissibility_contract"]
    rows = payload["runtime_admissibility_rows"]

    assert len(rows) == 1
    row = rows[0]
    assert set(row) == RUNTIME_ADMISSIBILITY_CONTRACT_ROW_REQUIRED_KEYS
    assert row["runtime_admissibility_row_id"] == (
        "runtime_admissibility__paper_single_box__box"
    )
    assert row["source_runtime_admissibility_preflight_row_id"] == (
        source_row["runtime_admissibility_preflight_row_id"]
    )
    assert row["candidate_primitivespec_dict"] == (
        source_row["candidate_primitivespec_dict"]
    )
    assert row["source_package_id"] == source_row["source_package_id"]
    assert row["source_package_stage"] == (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
    )
    assert row["source_package_primitive_subset"] == ["box"]
    assert row["source_package_unsupported_primitives"] == []
    assert row["runtime_admissibility_static_check_kind"] == (
        "offline_static_primitivespec_box_schema_check"
    )
    assert row["runtime_admissibility_decision"] == (
        "admissible_for_later_newton_shape_mapping_preflight"
    )
    assert row["runtime_admissibility_status"] == (
        "offline_static_admissible_for_later_newton_shape_mapping_preflight"
    )
    assert row["required_later_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT
    )
    assert row["finite_center_check_passed"] is True
    assert row["finite_axes_check_passed"] is True
    assert row["orthonormal_axes_check_passed"] is True
    assert row["right_handed_axes_check_passed"] is True
    assert row["positive_dimensions_check_passed"] is True
    assert row["target_shape_schema_check_passed"] is True
    assert row["source_faces_check_passed"] is True
    assert row["contains_assigned_points_check_passed"] is True
    assert row["volume_check_passed"] is True
    assert row["weighted_volume_check_passed"] is True
    assert row["offline_static_runtime_admissibility_check_passed"] is True
    assert row["offline_static_runtime_admissibility_checked"] is True
    assert list(_recursive_package_dicts(payload)) == []
```

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_admissibility_contract' -q
```

Expected: fail because the new payload does not exist.

### Task 2: Implement The Offline/Static Runtime-Admissibility Contract

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add next-gate constant and remaining-gap helper**

Add after `_PAPER_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT`:

```python
_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_newton_shape_mapping_preflight_contract"
)
```

Add:

```python
def _paper_remaining_gaps_after_mapped_subset_runtime_admissibility_contract() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT]
```

- [ ] **Step 2: Add validation helpers**

Add after `_paper_mapped_subset_runtime_admissibility_preflight_contract_payload`:

```python
_RUNTIME_ADMISSIBILITY_CONTRACT_PAYLOAD_FALSE_FLAGS = tuple(
    flag
    for flag in _RUNTIME_ADMISSIBILITY_PREFLIGHT_PAYLOAD_FALSE_FLAGS
    if flag != "runtime_admissibility_checked"
)


def _paper_runtime_admissibility_false_flags() -> dict[str, bool]:
    return {
        flag: False
        for flag in _RUNTIME_ADMISSIBILITY_CONTRACT_PAYLOAD_FALSE_FLAGS
    }


def _paper_runtime_admissibility_vector(
    value: object,
    *,
    error_label: str,
    length: int = 3,
) -> list[float]:
    if not isinstance(value, list | tuple) or len(value) != length:
        raise ValueError(error_label)
    result = [float(item) for item in value]
    if not all(np.isfinite(result)):
        raise ValueError(error_label)
    return result


def _paper_validate_runtime_admissibility_axes(axes: object) -> list[list[float]]:
    if not isinstance(axes, list | tuple) or len(axes) != 3:
        raise ValueError("runtime_admissibility_primitivespec_invalid_axes")
    rows = [
        _paper_runtime_admissibility_vector(
            axis,
            error_label="runtime_admissibility_primitivespec_invalid_axes",
        )
        for axis in axes
    ]
    matrix = np.asarray(rows, dtype=np.float64)
    if not np.all(np.isfinite(matrix)):
        raise ValueError("runtime_admissibility_primitivespec_invalid_axes")
    norms = np.linalg.norm(matrix, axis=1)
    if not np.allclose(norms, np.ones(3), atol=1e-9):
        raise ValueError("runtime_admissibility_primitivespec_axes_not_orthonormal")
    gram = matrix @ matrix.T
    if not np.allclose(gram, np.eye(3), atol=1e-9):
        raise ValueError("runtime_admissibility_primitivespec_axes_not_orthonormal")
    if float(np.dot(np.cross(matrix[0], matrix[1]), matrix[2])) <= 1.0 - 1e-9:
        raise ValueError("runtime_admissibility_primitivespec_axes_not_right_handed")
    return rows


def _paper_validate_runtime_admissibility_candidate(candidate: dict[str, object]) -> dict[str, bool]:
    expected_keys = set(_paper_primitivespec_like_required_schema_keys())
    if set(candidate) != expected_keys:
        raise ValueError("runtime_admissibility_primitivespec_schema_mismatch")
    if candidate.get("kind") != "box":
        raise ValueError("runtime_admissibility_primitivespec_mismatch:kind")
    if candidate.get("primitive_id") != "paper_single_box__oriented_bounding_box__box":
        raise ValueError("runtime_admissibility_primitivespec_mismatch:primitive_id")
    if candidate.get("frame") != "asset":
        raise ValueError("runtime_admissibility_primitivespec_mismatch:frame")
    if candidate.get("conversion_status") != _RUNTIME_CONSTRUCTION_OUTPUT_STATUS:
        raise ValueError("runtime_admissibility_primitivespec_mismatch:conversion_status")
    _paper_runtime_admissibility_vector(
        candidate.get("center"),
        error_label="runtime_admissibility_primitivespec_invalid_center",
    )
    _paper_validate_runtime_admissibility_axes(candidate.get("axes"))
    dimensions = candidate.get("dimensions")
    if not isinstance(dimensions, dict) or set(dimensions) != {"half_extents"}:
        raise ValueError("runtime_admissibility_primitivespec_invalid_dimensions")
    half_extents = _paper_runtime_admissibility_vector(
        dimensions.get("half_extents"),
        error_label="runtime_admissibility_primitivespec_invalid_dimensions",
    )
    if any(value <= 0.0 for value in half_extents):
        raise ValueError("runtime_admissibility_primitivespec_invalid_dimensions")
    if candidate.get("source_faces") != list(range(12)):
        raise ValueError("runtime_admissibility_primitivespec_mismatch:source_faces")
    if candidate.get("contains_assigned_points") is not True:
        raise ValueError("runtime_admissibility_primitivespec_mismatch:contains_assigned_points")
    try:
        volume = float(candidate.get("volume"))
    except (TypeError, ValueError) as exc:
        raise ValueError("runtime_admissibility_primitivespec_mismatch:volume") from exc
    try:
        weighted_volume = float(candidate.get("weighted_volume"))
    except (TypeError, ValueError) as exc:
        raise ValueError("runtime_admissibility_primitivespec_mismatch:weighted_volume") from exc
    expected_volume = float(8.0 * np.prod(np.asarray(half_extents, dtype=np.float64)))
    if (
        not np.isfinite(volume)
        or volume <= 0.0
        or not np.isclose(volume, expected_volume, rtol=0.0, atol=1e-9)
    ):
        raise ValueError("runtime_admissibility_primitivespec_mismatch:volume")
    if (
        not np.isfinite(weighted_volume)
        or weighted_volume <= 0.0
        or not np.isclose(weighted_volume, volume, rtol=0.0, atol=1e-9)
    ):
        raise ValueError("runtime_admissibility_primitivespec_mismatch:weighted_volume")
    return {
        "finite_center_check_passed": True,
        "finite_axes_check_passed": True,
        "orthonormal_axes_check_passed": True,
        "right_handed_axes_check_passed": True,
        "positive_dimensions_check_passed": True,
        "target_shape_schema_check_passed": True,
        "source_faces_check_passed": True,
        "contains_assigned_points_check_passed": True,
        "volume_check_passed": True,
        "weighted_volume_check_passed": True,
        "offline_static_runtime_admissibility_check_passed": True,
        "offline_static_runtime_admissibility_checked": True,
    }
```

- [ ] **Step 3: Add source-row and payload builders**

Add:

```python
def _paper_runtime_admissibility_source_row(
    preflight: dict[str, object],
) -> dict[str, object]:
    if preflight.get("gate_id") != _PAPER_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT:
        raise ValueError("runtime_admissibility_input_gate_id_mismatch")
    if preflight.get("next_required_gate") != _PAPER_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT:
        raise ValueError("runtime_admissibility_input_next_gate_mismatch")
    _paper_validate_primitivespec_runtime_construction_false_flags(
        preflight,
        error_prefix="runtime_admissibility_input_trigger_flag",
        required_false_flags=_RUNTIME_ADMISSIBILITY_PREFLIGHT_PAYLOAD_FALSE_FLAGS,
    )
    expected_counts = {
        "runtime_admissibility_preflight_row_count": 1,
        "later_runtime_admissibility_candidate_count": 1,
        "generated_collision_package_count": 1,
        "runtime_admissibility_check_count": 0,
    }
    for field_name, expected_value in expected_counts.items():
        if preflight.get(field_name) != expected_value:
            raise ValueError(f"runtime_admissibility_input_count_mismatch:{field_name}")
    rows = preflight.get("runtime_admissibility_preflight_rows")
    if not isinstance(rows, list | tuple) or len(rows) != 1 or not isinstance(rows[0], dict):
        raise ValueError("runtime_admissibility_preflight_row_count_mismatch")
    row = rows[0]
    _paper_validate_primitivespec_runtime_construction_false_flags(
        row,
        error_prefix="runtime_admissibility_input_trigger_flag",
        required_false_flags=_RUNTIME_ADMISSIBILITY_PREFLIGHT_PAYLOAD_FALSE_FLAGS,
    )
    if row.get("runtime_admissibility_preflight_decision") != "eligible_for_later_runtime_admissibility_contract":
        raise ValueError("runtime_admissibility_preflight_decision_mismatch")
    if row.get("required_later_gate") != _PAPER_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT:
        raise ValueError("runtime_admissibility_preflight_required_gate_mismatch")
    expected_source = _paper_runtime_admissibility_preflight_row(
        _paper_runtime_admissibility_preflight_expected_source_row()
    )
    for field_name, expected_value in expected_source.items():
        if field_name == "candidate_primitivespec_dict":
            continue
        if row.get(field_name) != expected_value:
            raise ValueError(f"runtime_admissibility_preflight_row_mismatch:{field_name}")
    if list(_paper_runtime_admissibility_preflight_package_dicts(preflight)):
        raise ValueError("runtime_admissibility_source_package_copy_forbidden")
    return row
```

Add:

```python
def _paper_runtime_admissibility_row(
    source_row: dict[str, object],
) -> dict[str, object]:
    candidate = source_row["candidate_primitivespec_dict"]
    if not isinstance(candidate, dict):
        raise ValueError("runtime_admissibility_primitivespec_schema_mismatch")
    checks = _paper_validate_runtime_admissibility_candidate(candidate)
    return {
        "runtime_admissibility_row_id": (
            "runtime_admissibility__paper_single_box__box"
        ),
        "source_runtime_admissibility_preflight_row_id": source_row[
            "runtime_admissibility_preflight_row_id"
        ],
        "source_collision_package_generation_row_id": source_row[
            "source_collision_package_generation_row_id"
        ],
        "source_package_generation_preflight_row_id": source_row[
            "source_package_generation_preflight_row_id"
        ],
        "source_runtime_construction_row_id": source_row[
            "source_runtime_construction_row_id"
        ],
        "source_runtime_boundary_preflight_row_id": source_row[
            "source_runtime_boundary_preflight_row_id"
        ],
        "source_native_fixture_primitivespec_serialization_row_id": source_row[
            "source_native_fixture_primitivespec_serialization_row_id"
        ],
        "source_native_fixture_primitivespec_generation_row_id": source_row[
            "source_native_fixture_primitivespec_generation_row_id"
        ],
        "source_native_current_fixture_source_row_id": source_row[
            "source_native_current_fixture_source_row_id"
        ],
        "source_candidate_source_audit_row_id": source_row[
            "source_candidate_source_audit_row_id"
        ],
        "source_primitivespec_generation_row_id": source_row[
            "source_primitivespec_generation_row_id"
        ],
        "source_primitivespec_generation_preflight_row_id": source_row[
            "source_primitivespec_generation_preflight_row_id"
        ],
        "source_primitivespec_validation_row_id": source_row[
            "source_primitivespec_validation_row_id"
        ],
        "source_primitivespec_dry_run_row_id": source_row[
            "source_primitivespec_dry_run_row_id"
        ],
        "source_adapter_preflight_row_id": source_row[
            "source_adapter_preflight_row_id"
        ],
        "source_candidate_matrix_row_id": source_row[
            "source_candidate_matrix_row_id"
        ],
        "source_conversion_plan_row_id": source_row["source_conversion_plan_row_id"],
        "fixture_id": source_row["fixture_id"],
        "paper_primitive": source_row["paper_primitive"],
        "primitive_spec_kind": source_row["primitive_spec_kind"],
        "candidate_mapping_label": source_row["candidate_mapping_label"],
        "newton_runtime_kind": source_row["newton_runtime_kind"],
        "primitive_id": source_row["primitive_id"],
        "kind": source_row["kind"],
        "candidate_primitivespec_dict": candidate,
        "source_package_id": source_row["source_package_id"],
        "source_asset_id": source_row["source_asset_id"],
        "source_package_stage": source_row["source_package_stage"],
        "source_package_status": source_row["source_package_status"],
        "source_package_method": source_row["source_package_method"],
        "source_package_source_path": source_row["source_package_source_path"],
        "source_package_source_sha256": source_row["source_package_source_sha256"],
        "source_package_claim_boundary": source_row["source_package_claim_boundary"],
        "source_package_primitive_count": source_row[
            "source_package_primitive_count"
        ],
        "source_package_primitive_subset": source_row[
            "source_package_primitive_subset"
        ],
        "source_package_unsupported_primitives": source_row[
            "source_package_unsupported_primitives"
        ],
        "source_collision_package_available": True,
        "runtime_admissibility_static_check_kind": (
            "offline_static_primitivespec_box_schema_check"
        ),
        "runtime_admissibility_decision": (
            "admissible_for_later_newton_shape_mapping_preflight"
        ),
        "runtime_admissibility_status": (
            "offline_static_admissible_for_later_newton_shape_mapping_preflight"
        ),
        "required_later_gate": (
            _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT
        ),
        **checks,
        **_paper_runtime_admissibility_false_flags(),
    }


def _paper_runtime_admissibility_coverage_summary(
    rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "runtime_admissibility_row_count": len(rows),
        "offline_static_runtime_admissibility_check_count": len(rows),
        "passed_static_runtime_admissibility_check_count": sum(
            bool(row["offline_static_runtime_admissibility_check_passed"])
            for row in rows
        ),
        "runtime_execution_count": 0,
        "newton_mapping_record_count": 0,
        "fixture_id_distribution": _paper_policy_distribution(rows, "fixture_id"),
        "primitive_subset_distribution": {"box": len(rows)},
    }


def _paper_mapped_subset_runtime_admissibility_contract_payload(
    preflight: dict[str, object],
) -> dict[str, object]:
    source_row = _paper_runtime_admissibility_source_row(preflight)
    row = _paper_runtime_admissibility_row(source_row)
    rows = [row]
    remaining_gaps = (
        _paper_remaining_gaps_after_mapped_subset_runtime_admissibility_contract()
    )
    return {
        "gate_id": _PAPER_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT,
        "gate_status": (
            "implemented_single_fixture_runtime_admissibility_contract_"
            "static_only_partial"
        ),
        "closed_gate": _PAPER_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT,
        "input_gate_id": (
            _PAPER_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT
        ),
        "next_required_gate": (
            _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT
        ),
        "decision": "remain_partial",
        "decision_reason": (
            "runtime_admissibility_contract_complete_"
            "newton_shape_mapping_preflight_missing"
        ),
        "paper_faithful_offline_allowed": False,
        "paper_faithful_offline_supported": False,
        "artifact_kind": (
            "offline_static_runtime_admissibility_contract_not_newton_mapping"
        ),
        "schema_version": 1,
        "source_scope": "synthetic_toy_fixtures_only",
        "implementation_boundary": (
            "single_synthetic_box_package_static_admissibility_only_"
            "no_newton_no_real_usd_no_benchmark_no_metrics"
        ),
        "runtime_admissibility_action": (
            "run_one_offline_static_runtime_admissibility_check_for_"
            "paper_single_box_box_package"
        ),
        "runtime_admissibility_requirements": {
            "input_gate_required": (
                _PAPER_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT
            ),
            "closed_gate": _PAPER_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT,
            "next_newton_shape_mapping_preflight_gate_required": (
                _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT
            ),
            "source_fixture_required": "paper_single_box",
            "source_primitive_spec_kind_required": "box",
            "offline_static_runtime_admissibility_checks_required": 1,
            "runtime_execution_allowed": False,
            "newton_mapping_allowed": False,
            "newton_runtime_allowed": False,
            "real_usd_allowed": False,
            "benchmark_allowed": False,
            "silent_drop_allowed": False,
        },
        "runtime_admissibility_row_count": 1,
        "offline_static_runtime_admissibility_check_count": 1,
        "offline_static_runtime_admissibility_checked": True,
        "runtime_admissibility_check_count": 1,
        "runtime_execution_count": 0,
        "newton_mapping_record_count": 0,
        "newton_runtime_execution_count": 0,
        "generated_runtime_primitive_spec_count": 1,
        "generated_primitive_spec_count": 1,
        "generated_collision_package_count": 1,
        "source_collision_package_available": True,
        "runtime_admissibility_contract": {
            "input_gate_required": (
                _PAPER_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT
            ),
            "closed_gate": _PAPER_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT,
            "next_newton_shape_mapping_preflight_gate_required": (
                _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT
            ),
            "runtime_admissibility_rows_required": 1,
            "offline_static_runtime_admissibility_checks_required": 1,
            "runtime_execution_allowed": False,
            "newton_mapping_allowed": False,
        },
        "input_contract_summary": {
            "input_gate_id": preflight["gate_id"],
            "input_next_required_gate": preflight["next_required_gate"],
            "input_runtime_admissibility_preflight_row_count": preflight[
                "runtime_admissibility_preflight_row_count"
            ],
            "input_generated_collision_package_count": preflight[
                "generated_collision_package_count"
            ],
            "input_runtime_admissibility_check_count": preflight[
                "runtime_admissibility_check_count"
            ],
            "source_row_id": source_row[
                "runtime_admissibility_preflight_row_id"
            ],
            "source_package_id": source_row["source_package_id"],
            "source_fixture_id": source_row["fixture_id"],
            "source_primitive_spec_kind": source_row["primitive_spec_kind"],
        },
        "runtime_admissibility_rows": rows,
        "coverage_summary": _paper_runtime_admissibility_coverage_summary(rows),
        "remaining_gaps": remaining_gaps,
        **_paper_runtime_admissibility_false_flags(),
    }
```

- [ ] **Step 4: Wire the report chain**

In `build_cpd_paper_offline_report()`, after
`mapped_subset_runtime_admissibility_preflight`, create
`mapped_subset_runtime_admissibility` from the new payload, change
top-level `runtime_admissibility_check_count` to `1`, set top-level `next_required_gate` to
`_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT`, keep
`paper_faithfulness["missing_before_paper_faithful_offline"]` tied to
`_paper_faithful_offline_scope_audit_payload()["blocking_criteria_ids"]`, add
`paper_faithfulness["runtime_lane_remaining_gates"]` with
`_paper_remaining_gaps_after_mapped_subset_runtime_admissibility_contract()`, append
`_PAPER_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT` to `implemented_output_contract_scope`, and
add report key `paper_mapped_subset_runtime_admissibility_contract`.

- [ ] **Step 5: Run focused GREEN test**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_admissibility_contract' -q
```

Expected: the new runtime-admissibility contract tests pass.

### Task 3: Add Negative Drift Tests And Static Boundary Tests

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`

- [ ] **Step 1: Add drift rejection tests**

Add tests that mutate `_runtime_admissibility_contract_input()` and assert `ValueError` labels:

- `gate_id` -> `runtime_admissibility_input_gate_id_mismatch`
- `next_required_gate` -> `runtime_admissibility_input_next_gate_mismatch`
- `runtime_admissibility_preflight_row_count` -> `runtime_admissibility_input_count_mismatch:runtime_admissibility_preflight_row_count`
- duplicate preflight rows -> `runtime_admissibility_preflight_row_count_mismatch`
- `fixture_id` -> `runtime_admissibility_preflight_row_mismatch:fixture_id`
- `source_package_claim_boundary` -> `runtime_admissibility_preflight_row_mismatch:source_package_claim_boundary`
- add copied package dict -> `runtime_admissibility_source_package_copy_forbidden`

- [ ] **Step 2: Add PrimitiveSpec drift tests**

Mutate `candidate_primitivespec_dict` in both the preflight row and any carried copy needed to
exercise the validator. Assert exact labels:

- bad `kind` -> `runtime_admissibility_primitivespec_mismatch:kind`
- bad `center` -> `runtime_admissibility_primitivespec_invalid_center`
- malformed `axes` -> `runtime_admissibility_primitivespec_invalid_axes`
- non-unit axis -> `runtime_admissibility_primitivespec_axes_not_orthonormal`
- left-handed axis frame -> `runtime_admissibility_primitivespec_axes_not_right_handed`
- missing `half_extents` -> `runtime_admissibility_primitivespec_invalid_dimensions`
- negative half extent -> `runtime_admissibility_primitivespec_invalid_dimensions`
- bad `source_faces` -> `runtime_admissibility_primitivespec_mismatch:source_faces`
- `contains_assigned_points: false` -> `runtime_admissibility_primitivespec_mismatch:contains_assigned_points`
- bad `volume` -> `runtime_admissibility_primitivespec_mismatch:volume`
- bad `weighted_volume` -> `runtime_admissibility_primitivespec_mismatch:weighted_volume`
- bad `conversion_status` -> `runtime_admissibility_primitivespec_mismatch:conversion_status`

- [ ] **Step 3: Add static source boundary test**

Slice the source from `_RUNTIME_ADMISSIBILITY_PREFLIGHT_PAYLOAD_FALSE_FLAGS` to
`def _paper_source_policy_generalization_payload` and assert these forbidden tokens are absent
inside the new runtime-admissibility contract block:

```python
forbidden_patterns = [
    "FallbackSpec",
    "primitive_collision_compiler.newton",
    "import newton",
    "import newton_warp",
    "Newton",
    "run_newton",
    "map_package_shapes",
    "check_runtime_admissibility",
    "run_runtime_admissibility",
    "newton.",
    "pxr",
    "Usd",
    "USD",
    "load_first_mesh",
    "inspect_usd_asset",
    "assets.usd_smoke",
    "real_usd_comparison",
    "timeit",
    "perf_counter",
    "benchmark_metric",
    "surface_distance",
    "timing_result",
    "collision_quality_score",
    "run_benchmark",
    "measure_collision_quality",
]
```

- [ ] **Step 4: Run focused tests**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_admissibility_contract or runtime_admissibility_preflight' -q
```

Expected: all focused contract/preflight tests pass.

### Task 4: Update CLI Tests And Documentation

**Files:**
- Modify: `tests/test_cli.py`
- Modify: `README.md`
- Modify: `docs/index.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/deepdive/message-map.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/records/README.md`
- Create: `docs/records/2026-05-18-cpd-paper-mapped-subset-runtime-admissibility-contract.md`

- [ ] **Step 1: Update CLI expectations**

Update `tests/test_cli.py` so the `cpd-paper-offline-report` JSON assertions expect:

- `next_required_gate == "paper_mapped_subset_newton_shape_mapping_preflight_contract"`
- failure label `paper_mapped_subset_newton_shape_mapping_preflight_contract_missing`
- report key `paper_mapped_subset_runtime_admissibility_contract`
- `runtime_admissibility_check_count == 1`
- `newton_runtime_triggered is False`

- [ ] **Step 2: Update reference docs**

Use the claim-boundary wording from the spec. Every edited reference/doc page must state that this
is one offline/static single-fixture check, not Newton readiness, not Newton execution, not
real-USD evidence, not benchmark evidence, and not collision-quality validation.

- [ ] **Step 3: Add dated record**

Create `docs/records/2026-05-18-cpd-paper-mapped-subset-runtime-admissibility-contract.md` with:

- status `Complete` only after implementation and verification pass;
- context from the preflight gate;
- what changed;
- verification commands;
- artifact names;
- claim boundary;
- next gate `paper_mapped_subset_newton_shape_mapping_preflight_contract`.

- [ ] **Step 4: Run docs and CLI checks**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
```

Expected: CLI tests and docs validators pass.

### Task 5: Final Verification, Review, Commit, Merge, Push, Cleanup

**Files:**
- Verify all files touched by Tasks 1-4.

- [ ] **Step 1: Run final verification**

Run:

```bash
python -m py_compile src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cpd_paper_offline.py tests/test_cli.py
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_admissibility_contract or runtime_admissibility_preflight or collision_package_generation_contract' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
PYTHONPATH=src python -m pytest -q
```

Expected: all commands pass.

- [ ] **Step 2: Multi-agent review**

Dispatch one code reviewer and one docs/claim-boundary reviewer. Fix every valid finding with a
new RED/GREEN cycle when behavior changes.

- [ ] **Step 3: Commit, merge, push, cleanup**

Commit with:

```bash
git add src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cpd_paper_offline.py tests/test_cli.py README.md docs
git commit -m "feat: add CPD runtime-admissibility contract"
```

Merge to `main`, push `origin main`, remove the worktree, delete the branch, and confirm:

```bash
git status --short --branch
git worktree list
```

Expected: main is clean and tracks `origin/main`; no temporary worktree remains.
