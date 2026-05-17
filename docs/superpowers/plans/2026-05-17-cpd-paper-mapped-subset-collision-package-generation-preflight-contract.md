# CPD Paper Mapped-Subset CollisionPackage Generation Preflight Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `paper_mapped_subset_collision_package_generation_preflight_contract` gate that records exactly one later CollisionPackage-generation candidate from the validated synthetic `paper_single_box` runtime `PrimitiveSpec.to_dict()` row, while generating zero CollisionPackages.

**Architecture:** Extend the existing `cpd_paper_offline_report` gate chain in `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`. The new helper consumes `paper_mapped_subset_primitivespec_runtime_construction_contract`, validates its single runtime `PrimitiveSpec.to_dict()` row, records a package-generation preflight row, and advances the next gate to `paper_mapped_subset_collision_package_generation_contract` without importing or constructing `CollisionPackage`.

**Tech Stack:** Python dict contracts, pytest, existing CPD paper offline report helpers, existing docs validators.

---

### Task 1: Add RED Tests For CollisionPackage Generation Preflight

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add expected gate constants**

In `tests/test_cpd_paper_offline.py`, add the next gate constant near the existing collision-package preflight constant:

```python
EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT = (
    "paper_mapped_subset_collision_package_generation_contract"
)
```

Add the new remaining gap list:

```python
EXPECTED_COLLISION_PACKAGE_GENERATION_PREFLIGHT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT,
]
```

Update the current output gap list and failure labels so the current missing contract becomes:

```python
EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
```

Expected report-level values after implementation:

```python
assert report["next_required_gate"] == (
    EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
)
assert report["failure_labels"] == [
    "paper_mapped_subset_collision_package_generation_contract_missing"
]
assert report["paper_faithfulness"]["missing_before_paper_faithful_offline"] == (
    EXPECTED_COLLISION_PACKAGE_GENERATION_PREFLIGHT_REMAINING_GAPS
)
```

Update every existing report-level `report["next_required_gate"]` assertion that currently expects
`EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT` so it now expects
`EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT`. This includes the top-level
`test_cpd_paper_offline_report_next_gate_is_collision_package_generation_preflight_contract` test
and the report-level assertions inside older gate tests such as the runtime-construction test.
Keep payload-level assertions on older gates unchanged; for example the runtime-construction
payload must still have:

```python
assert payload["next_required_gate"] == (
    EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT
)
```

- [ ] **Step 2: Add helper input**

Add near `_runtime_construction_input()`:

```python
def _collision_package_generation_preflight_input() -> dict[str, object]:
    report = build_cpd_paper_offline_report()
    return json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_primitivespec_runtime_construction_contract"
            ]
        )
    )
```

- [ ] **Step 3: Add required key sets**

Add these key sets near `RUNTIME_CONSTRUCTION_ROW_REQUIRED_KEYS`:

```python
COLLISION_PACKAGE_GENERATION_PREFLIGHT_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "paper_faithful_offline_allowed",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "package_generation_preflight_action",
    "package_generation_preflight_requirements",
    "package_generation_preflight_row_count",
    "later_collision_package_generation_candidate_count",
    "package_generation_allowed_in_current_gate",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "package_generation_preflight_contract",
    "input_contract_summary",
    "package_generation_preflight_rows",
    "coverage_summary",
    "remaining_gaps",
    *RUNTIME_CONSTRUCTION_FALSE_FLAGS,
}

COLLISION_PACKAGE_GENERATION_PREFLIGHT_ROW_REQUIRED_KEYS = {
    "package_generation_preflight_row_id",
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
    "generated_primitive_spec",
    "constructed_primitivespec_dict",
    "candidate_primitivespec_dict",
    "candidate_package_primitive_kind",
    "candidate_package_scope",
    "later_collision_package_generation_candidate",
    "package_generation_allowed_in_current_gate",
    "required_later_gate",
    "preflight_decision",
    "preflight_reason",
    "collision_package_generated",
    "generated_collision_package",
    "runtime_admissibility_checked",
    *RUNTIME_CONSTRUCTION_FALSE_FLAGS,
}
```

- [ ] **Step 4: Add report-level RED test**

Add:

```python
def test_cpd_paper_records_mapped_subset_collision_package_generation_preflight_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report[
        "paper_mapped_subset_collision_package_generation_preflight_contract"
    ]

    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
    )
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_COLLISION_PACKAGE_GENERATION_PREFLIGHT_REMAINING_GAPS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
    )
    assert payload["package_generation_preflight_row_count"] == 1
    assert payload["later_collision_package_generation_candidate_count"] == 1
    assert payload["package_generation_allowed_in_current_gate"] is False
    assert payload["generated_runtime_primitive_spec_count"] == 1
    assert payload["generated_primitive_spec_count"] == 1
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    assert (
        payload["remaining_gaps"]
        == EXPECTED_COLLISION_PACKAGE_GENERATION_PREFLIGHT_REMAINING_GAPS
    )
```

- [ ] **Step 5: Add row, boundary, and malformed-input tests**

Add tests that assert:

- `set(payload) == COLLISION_PACKAGE_GENERATION_PREFLIGHT_PAYLOAD_REQUIRED_KEYS`;
- `set(row) == COLLISION_PACKAGE_GENERATION_PREFLIGHT_ROW_REQUIRED_KEYS`;
- `row["source_runtime_construction_row_id"]` equals the runtime-construction source row id;
- every inherited `source_*` lineage id equals the runtime-construction row value;
- `row["candidate_primitivespec_dict"] == source_row["generated_primitive_spec"]`;
- `row["candidate_primitivespec_dict"] == source_row["constructed_primitivespec_dict"]`;
- `row["candidate_package_primitive_kind"] == "box"`;
- `row["candidate_package_scope"] == "single_primitivespec_dict_candidate_only"`;
- `row["later_collision_package_generation_candidate"] is True`;
- `row["package_generation_allowed_in_current_gate"] is False`;
- `row["required_later_gate"] == EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT`;
- `row["collision_package_generated"] is False`;
- `row["generated_collision_package"] is None`;
- `row["runtime_admissibility_checked"] is False`;
- `payload["generated_collision_package_count"] == 0`;
- `payload["generated_runtime_primitive_spec_count"] == 1` and
  `payload["generated_primitive_spec_count"] == 1` are carried-forward counts from the input
  runtime-construction gate, not new generation by this preflight gate;
- `payload["package_generation_preflight_requirements"]` exactly matches:

```python
{
    "input_gate_required": (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT
    ),
    "package_generation_preflight_gate_closed": (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT
    ),
    "next_collision_package_generation_gate_required": (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
    ),
    "source_fixture_required": "paper_single_box",
    "source_primitive_spec_kind_required": "box",
    "later_collision_package_generation_candidates_required": 1,
    "generated_collision_packages_required": 0,
    "runtime_admissibility_checks_required": 0,
    "newton_runtime_allowed": False,
    "real_usd_allowed": False,
    "benchmark_allowed": False,
    "silent_drop_allowed": False,
}
```

- `payload["package_generation_preflight_contract"]` exactly matches:

```python
{
    "input_gate_required": (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT
    ),
    "package_generation_preflight_gate_closed": (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT
    ),
    "next_collision_package_generation_gate_required": (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
    ),
    "package_generation_preflight_rows_required": 1,
    "later_collision_package_generation_candidates_required": 1,
    "generated_collision_packages_required": 0,
    "runtime_admissibility_checks_required": 0,
}
```

- `payload["input_contract_summary"]` exactly matches:

```python
{
    "input_gate_id": (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT
    ),
    "input_next_required_gate": (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT
    ),
    "input_runtime_construction_row_count": 1,
    "input_constructed_runtime_primitivespec_count": 1,
    "input_generated_runtime_primitive_spec_count": 1,
    "input_generated_collision_package_count": 0,
    "source_row_id": source_row["runtime_construction_row_id"],
    "source_fixture_id": "paper_single_box",
    "source_primitive_spec_kind": "box",
}
```

- `payload["coverage_summary"]` exactly matches:

```python
{
    "package_generation_preflight_row_count": 1,
    "later_collision_package_generation_candidate_record_count": 1,
    "package_generation_allowed_record_count": 0,
    "generated_collision_package_record_count": 0,
    "runtime_admissibility_check_record_count": 0,
    "fixture_id_distribution": {"paper_single_box": 1},
    "candidate_package_primitive_kind_distribution": {"box": 1},
}
```
- `json.dumps(payload, allow_nan=False, sort_keys=True)` succeeds;
- no row stores a live `CollisionPackage`, live `PrimitiveSpec`, or non-JSON object;
- the preflight helper source block does not contain `CollisionPackage`, `FallbackSpec`,
  `PrimitiveSpec(`, Newton imports/calls, USD loading tokens, executable runtime-admissibility
  helper calls such as `check_runtime_admissibility` or `run_runtime_admissibility`, `timeit`,
  `perf_counter`, `benchmark_metric`, `surface_distance`, `timing_result`,
  `collision_quality_score`, `run_benchmark`, or `measure_collision_quality`;
- stale input gate, stale input next gate, row-count drift, nonzero generated package count,
  true package/Newton flags, missing runtime PrimitiveSpec dict, generated/constructed dict
  mismatch, unsupported kind, and runtime-admissibility leakage raise explicit `ValueError` labels.

- [ ] **Step 6: Add CLI RED assertions**

In `tests/test_cli.py`, update the CPD paper offline report test so it expects:

```python
payload["next_required_gate"] == "paper_mapped_subset_collision_package_generation_contract"
payload["failure_labels"] == [
    "paper_mapped_subset_collision_package_generation_contract_missing"
]
```

Add assertions for:

```python
preflight = payload[
    "paper_mapped_subset_collision_package_generation_preflight_contract"
]
assert preflight["gate_id"] == (
    "paper_mapped_subset_collision_package_generation_preflight_contract"
)
assert preflight["input_gate_id"] == (
    "paper_mapped_subset_primitivespec_runtime_construction_contract"
)
assert preflight["next_required_gate"] == (
    "paper_mapped_subset_collision_package_generation_contract"
)
assert preflight["package_generation_preflight_row_count"] == 1
assert preflight["later_collision_package_generation_candidate_count"] == 1
assert preflight["generated_collision_package_count"] == 0
assert preflight["runtime_admissibility_check_count"] == 0
```

Also update the exact CLI list assertions:

```python
assert payload["paper_faithfulness"]["missing_before_paper_faithful_offline"] == [
    "paper_mapped_subset_collision_package_generation_contract",
]
assert payload["paper_faithfulness"]["implemented_output_contract_scope"] == [
    "paper_offline_changed_decomposition_output_contract",
    "paper_package_adapter_contract",
    "paper_package_adapter_unsupported_primitive_policy",
    "paper_package_conversion_mapped_subset_plan",
    "paper_mapped_subset_conversion_candidate_matrix",
    "paper_mapped_subset_adapter_preflight_contract",
    "paper_mapped_subset_primitivespec_dry_run_contract",
    "paper_mapped_subset_primitivespec_validation_contract",
    "paper_mapped_subset_primitivespec_generation_preflight_contract",
    "paper_mapped_subset_primitivespec_generation_contract",
    "paper_mapped_subset_primitivespec_candidate_source_contract",
    "paper_mapped_subset_native_current_fixture_contract",
    "paper_mapped_subset_primitivespec_native_fixture_generation_contract",
    "paper_mapped_subset_primitivespec_native_fixture_serialization_contract",
    "paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract",
    "paper_mapped_subset_primitivespec_runtime_construction_contract",
    "paper_mapped_subset_collision_package_generation_preflight_contract",
]
```

- [ ] **Step 7: Run RED tests**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'collision_package_generation_preflight or runtime_construction' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Expected: fail because the package-generation preflight payload and helpers do not exist yet.

### Task 2: Implement CollisionPackage Generation Preflight Helper

**Files:**

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add next-gate constant and remaining-gap helper**

Add:

```python
_PAPER_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT = (
    "paper_mapped_subset_collision_package_generation_contract"
)


def _paper_remaining_gaps_after_mapped_subset_collision_package_generation_preflight() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT]
```

- [ ] **Step 2: Add false-flag constants**

Add near `_RUNTIME_CONSTRUCTION_BOUNDARY_FALSE_FLAGS`:

```python
_COLLISION_PACKAGE_GENERATION_PREFLIGHT_PAYLOAD_FALSE_FLAGS = (
    "paper_faithful_offline_allowed",
    *_RUNTIME_CONSTRUCTION_BOUNDARY_FALSE_FLAGS,
)

_COLLISION_PACKAGE_GENERATION_PREFLIGHT_ROW_FALSE_FLAGS = (
    *_RUNTIME_CONSTRUCTION_BOUNDARY_FALSE_FLAGS,
)
```

The source row for this gate is a runtime-construction row, and runtime-construction rows include
`package_generation_allowed`. Do not exclude that field from the source-row false-flag checks.

- [ ] **Step 3: Add input source-row validator**

Add `_paper_collision_package_generation_preflight_source_row(runtime_construction)` that:

- requires `gate_id == _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT`;
- requires `next_required_gate == _PAPER_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT`;
- requires payload false flags from `_COLLISION_PACKAGE_GENERATION_PREFLIGHT_PAYLOAD_FALSE_FLAGS`;
- requires `runtime_construction_row_count == 1`;
- requires `constructed_runtime_primitivespec_count == 1`;
- requires `generated_runtime_primitive_spec_count == 1`;
- requires `generated_primitive_spec_count == 1`;
- requires `generated_collision_package_count == 0`;
- requires `runtime_admissibility_check_count == 0`;
- requires exactly one `runtime_construction_rows` dict;
- requires row false flags from `_COLLISION_PACKAGE_GENERATION_PREFLIGHT_ROW_FALSE_FLAGS`;
- requires `fixture_id == "paper_single_box"`;
- requires `paper_primitive == "oriented_bounding_box"`;
- requires `primitive_spec_kind == "box"`;
- requires `candidate_mapping_label == "box"`;
- requires `newton_runtime_kind == "box"`;
- requires `kind == "box"`;
- requires `runtime_instance_generated is True`;
- requires `runtime_primitivespec_construction_triggered is True`;
- requires `generated_primitive_spec == constructed_primitivespec_dict`;
- requires `generated_primitive_spec` is a JSON-serializable dict;
- rejects any existing generated collision package or runtime-admissibility evidence.

Use labels shaped like:

```python
"collision_package_generation_preflight_input_gate_id_mismatch"
"collision_package_generation_preflight_input_next_gate_mismatch"
"collision_package_generation_preflight_input_trigger_flag_true:<field>"
"collision_package_generation_preflight_input_count_mismatch:<field>"
"collision_package_generation_preflight_row_count_mismatch"
"collision_package_generation_preflight_source_kind_mismatch"
"collision_package_generation_preflight_runtime_primitivespec_missing"
"collision_package_generation_preflight_primitivespec_dict_mismatch"
"collision_package_generation_preflight_prior_package_leak:<field>"
"collision_package_generation_preflight_prior_runtime_admissibility_leak:<field>"
```

- [ ] **Step 4: Add row and coverage helpers**

Add `_paper_collision_package_generation_preflight_row(row)` returning one row with:

```python
{
    "package_generation_preflight_row_id": (
        "collision_package_generation_preflight__paper_single_box__box"
    ),
    "source_runtime_construction_row_id": row["runtime_construction_row_id"],
    "source_runtime_boundary_preflight_row_id": row[
        "source_runtime_boundary_preflight_row_id"
    ],
    "source_native_fixture_primitivespec_serialization_row_id": row[
        "source_native_fixture_primitivespec_serialization_row_id"
    ],
    "source_native_fixture_primitivespec_generation_row_id": row[
        "source_native_fixture_primitivespec_generation_row_id"
    ],
    "source_native_current_fixture_source_row_id": row[
        "source_native_current_fixture_source_row_id"
    ],
    "source_candidate_source_audit_row_id": row[
        "source_candidate_source_audit_row_id"
    ],
    "source_primitivespec_generation_row_id": row[
        "source_primitivespec_generation_row_id"
    ],
    "source_primitivespec_generation_preflight_row_id": row[
        "source_primitivespec_generation_preflight_row_id"
    ],
    "source_primitivespec_validation_row_id": row[
        "source_primitivespec_validation_row_id"
    ],
    "source_primitivespec_dry_run_row_id": row[
        "source_primitivespec_dry_run_row_id"
    ],
    "source_adapter_preflight_row_id": row["source_adapter_preflight_row_id"],
    "source_candidate_matrix_row_id": row["source_candidate_matrix_row_id"],
    "source_conversion_plan_row_id": row["source_conversion_plan_row_id"],
    "fixture_id": row["fixture_id"],
    "paper_primitive": row["paper_primitive"],
    "primitive_spec_kind": row["primitive_spec_kind"],
    "candidate_mapping_label": row["candidate_mapping_label"],
    "newton_runtime_kind": row["newton_runtime_kind"],
    "primitive_id": row["primitive_id"],
    "kind": row["kind"],
    "generated_primitive_spec": row["generated_primitive_spec"],
    "constructed_primitivespec_dict": row["constructed_primitivespec_dict"],
    "candidate_primitivespec_dict": row["generated_primitive_spec"],
    "candidate_package_primitive_kind": "box",
    "candidate_package_scope": "single_primitivespec_dict_candidate_only",
    "later_collision_package_generation_candidate": True,
    "package_generation_allowed_in_current_gate": False,
    "required_later_gate": (
        _PAPER_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
    ),
    "preflight_decision": (
        "later_collision_package_generation_contract_may_be_proposed"
    ),
    "preflight_reason": (
        "runtime_primitivespec_dict_available_but_current_gate_is_preflight_only"
    ),
    "collision_package_generated": False,
    "generated_collision_package": None,
    "runtime_admissibility_checked": False,
    **_paper_false_runtime_construction_boundary_flags(),
}
```

Add `_paper_collision_package_generation_preflight_coverage_summary(rows)` returning:

```python
{
    "package_generation_preflight_row_count": len(rows),
    "later_collision_package_generation_candidate_record_count": sum(
        bool(row["later_collision_package_generation_candidate"]) for row in rows
    ),
    "package_generation_allowed_record_count": sum(
        bool(row["package_generation_allowed_in_current_gate"]) for row in rows
    ),
    "generated_collision_package_record_count": 0,
    "runtime_admissibility_check_record_count": 0,
    "fixture_id_distribution": _paper_policy_distribution(rows, "fixture_id"),
    "candidate_package_primitive_kind_distribution": _paper_policy_distribution(
        rows,
        "candidate_package_primitive_kind",
    ),
}
```

- [ ] **Step 5: Add payload helper**

Add `_paper_mapped_subset_collision_package_generation_preflight_contract_payload(runtime_construction)`.
Start the helper with this setup before returning the payload dictionary:

```python
def _paper_mapped_subset_collision_package_generation_preflight_contract_payload(
    runtime_construction: dict[str, object],
) -> dict[str, object]:
    source_row = _paper_collision_package_generation_preflight_source_row(
        runtime_construction
    )
    preflight_row = _paper_collision_package_generation_preflight_row(source_row)
    rows = [preflight_row]
    remaining_gaps = (
        _paper_remaining_gaps_after_mapped_subset_collision_package_generation_preflight()
    )
```

Then return this dictionary:

```python
{
    "gate_id": _PAPER_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT,
    "gate_status": (
        "implemented_single_fixture_collision_package_generation_preflight_"
        "contract_only_partial"
    ),
    "closed_gate": _PAPER_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT,
    "input_gate_id": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT,
    "next_required_gate": _PAPER_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT,
    "decision": "remain_partial",
    "decision_reason": (
        "collision_package_generation_preflight_complete_"
        "collision_package_generation_contract_missing"
    ),
    "paper_faithful_offline_allowed": False,
    "artifact_kind": "collision_package_generation_preflight_not_package",
    "schema_version": 1,
    "source_scope": "synthetic_toy_fixtures_only",
    "implementation_boundary": (
        "single_synthetic_primitivespec_dict_package_candidate_only_"
        "no_collision_package_no_newton_no_real_usd_no_benchmark"
    ),
    "package_generation_preflight_action": (
        "record_one_later_collision_package_generation_candidate"
    ),
    "package_generation_preflight_requirements": {
        "input_gate_required": (
            _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT
        ),
        "package_generation_preflight_gate_closed": (
            _PAPER_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT
        ),
        "next_collision_package_generation_gate_required": (
            _PAPER_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
        ),
        "source_fixture_required": "paper_single_box",
        "source_primitive_spec_kind_required": "box",
        "later_collision_package_generation_candidates_required": 1,
        "generated_collision_packages_required": 0,
        "runtime_admissibility_checks_required": 0,
        "newton_runtime_allowed": False,
        "real_usd_allowed": False,
        "benchmark_allowed": False,
        "silent_drop_allowed": False,
    },
    "package_generation_preflight_row_count": 1,
    "later_collision_package_generation_candidate_count": 1,
    "package_generation_allowed_in_current_gate": False,
    "generated_runtime_primitive_spec_count": 1,
    "generated_primitive_spec_count": 1,
    "generated_collision_package_count": 0,
    "runtime_admissibility_check_count": 0,
    "package_generation_preflight_contract": {
        "input_gate_required": (
            _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT
        ),
        "package_generation_preflight_gate_closed": (
            _PAPER_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT
        ),
        "next_collision_package_generation_gate_required": (
            _PAPER_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
        ),
        "package_generation_preflight_rows_required": 1,
        "later_collision_package_generation_candidates_required": 1,
        "generated_collision_packages_required": 0,
        "runtime_admissibility_checks_required": 0,
    },
    "input_contract_summary": {
        "input_gate_id": runtime_construction["gate_id"],
        "input_next_required_gate": runtime_construction["next_required_gate"],
        "input_runtime_construction_row_count": runtime_construction[
            "runtime_construction_row_count"
        ],
        "input_constructed_runtime_primitivespec_count": runtime_construction[
            "constructed_runtime_primitivespec_count"
        ],
        "input_generated_runtime_primitive_spec_count": runtime_construction[
            "generated_runtime_primitive_spec_count"
        ],
        "input_generated_collision_package_count": runtime_construction[
            "generated_collision_package_count"
        ],
        "source_row_id": source_row["runtime_construction_row_id"],
        "source_fixture_id": source_row["fixture_id"],
        "source_primitive_spec_kind": source_row["primitive_spec_kind"],
    },
    "package_generation_preflight_rows": rows,
    "coverage_summary": (
        _paper_collision_package_generation_preflight_coverage_summary(rows)
    ),
    "remaining_gaps": remaining_gaps,
    **_paper_false_runtime_construction_boundary_flags(),
}
```

- [ ] **Step 6: Wire `build_cpd_paper_offline_report()`**

After `mapped_subset_primitivespec_runtime_construction`, add:

```python
mapped_subset_collision_package_generation_preflight = (
    _paper_mapped_subset_collision_package_generation_preflight_contract_payload(
        mapped_subset_primitivespec_runtime_construction
    )
)
remaining_gaps = (
    _paper_remaining_gaps_after_mapped_subset_collision_package_generation_preflight()
)
```

Update:

- top-level `next_required_gate`;
- `failure_labels`;
- `paper_faithfulness["missing_before_paper_faithful_offline"]`;
- `paper_faithfulness["implemented_output_contract_scope"]`;
- the report dict with key
  `"paper_mapped_subset_collision_package_generation_preflight_contract"`.

- [ ] **Step 7: Run GREEN tests**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'collision_package_generation_preflight or runtime_construction' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Expected: pass.

### Task 3: Update Documentation And Record

**Files:**

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
- Create: `docs/records/2026-05-17-cpd-paper-mapped-subset-collision-package-generation-preflight-contract.md`

- [ ] **Step 1: Update current-next-gate wording**

Use this exact boundary sentence where a short summary is needed:

```text
The collision-package generation preflight contract records one later package-generation candidate
from the single synthetic `paper_single_box` runtime `PrimitiveSpec.to_dict()` row, keeps generated
CollisionPackages and runtime-admissibility checks at zero, and advances the current next gate to
`paper_mapped_subset_collision_package_generation_contract`.
```

- [ ] **Step 2: Add dated record**

Create `docs/records/2026-05-17-cpd-paper-mapped-subset-collision-package-generation-preflight-contract.md` with:

```markdown
# 2026-05-17 CPD Paper Mapped-Subset CollisionPackage Generation Preflight Contract

## Date

2026-05-17

## Status

Complete.

## Context

The previous gate, `paper_mapped_subset_primitivespec_runtime_construction_contract`, constructs
exactly one report-scoped runtime `PrimitiveSpec` and stores only `PrimitiveSpec.to_dict()` in the
offline report. This record covers only the next preflight gate for later CollisionPackage
generation.

## What Changed

The partial `cpd_paper_offline_report` now includes
`paper_mapped_subset_collision_package_generation_preflight_contract`.

The new payload validates the single synthetic `paper_single_box` runtime PrimitiveSpec dict,
records one later package-generation candidate, keeps package generation disallowed in the current
gate, records zero generated CollisionPackages, records zero runtime-admissibility checks, and
advances the next gate to `paper_mapped_subset_collision_package_generation_contract`.

## Claim Boundary

Supported:

- one synthetic preflight candidate for later package generation;
- report-only reuse of the existing `PrimitiveSpec.to_dict()` payload;
- explicit accounting that no `CollisionPackage`, Newton execution, runtime-admissibility check,
  real-USD load, benchmark, collision-quality measurement, deployment, or certification work ran.

Not supported:

- `CollisionPackage` generation;
- package readiness;
- runtime admissibility;
- Newton support or Newton execution;
- real-USD evidence;
- benchmark evidence;
- collision-quality evidence;
- `paper_faithful_offline` support;
- full CPD reproduction;
- deployment readiness or safety certification.

## Next Gate

`paper_mapped_subset_collision_package_generation_contract`
```

- [ ] **Step 3: Run doc checks**

Run:

```bash
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

### Task 4: Final Verification And Commit

**Files:**

- All files touched in Tasks 1-3

- [ ] **Step 1: Run focused tests**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'collision_package_generation_preflight or runtime_construction' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Expected: pass.

- [ ] **Step 2: Run report command**

Run:

```bash
PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report >/tmp/cpd_paper_collision_package_preflight_report.json
```

Expected: exit 0.

- [ ] **Step 3: Run full checks**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -q
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

- [ ] **Step 4: Request multi-agent review**

Dispatch one implementation reviewer and one docs/claim-boundary reviewer. Fix all critical or
important findings before committing.

- [ ] **Step 5: Commit**

Run:

```bash
git add README.md docs src tests
git commit -m "feat: add CPD CollisionPackage generation preflight contract"
```
