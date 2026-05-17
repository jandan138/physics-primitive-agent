# CPD Paper Mapped-Subset Native Current Fixture Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the offline/report-only `paper_mapped_subset_native_current_fixture_contract` gate that records one eligible synthetic Newton-native current fixture source while keeping runtime PrimitiveSpecs, CollisionPackages, Newton, real USD, benchmarks, collision-quality, deployment, and safety claims at zero/false.

**Architecture:** Consume `paper_mapped_subset_primitivespec_candidate_source_contract`, validate its zero-current-source boundary, select the existing `paper_single_box` OBB fit audit as the single synthetic native current fixture source, emit a report-only source row for a future box PrimitiveSpec generation gate, and advance the top-level next gate to `paper_mapped_subset_primitivespec_native_fixture_generation_contract`.

**Tech Stack:** Python, pytest, existing CPD paper offline report builder, Markdown docs, YAML experiment registry.

---

## File Map

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
  - Add `_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT`.
  - Add `_paper_remaining_gaps_after_mapped_subset_native_current_fixture()`.
  - Add candidate-source input validation for the native-current-fixture gate.
  - Add fixture selection and selected-fit validation helpers for `paper_single_box`.
  - Add `_paper_native_current_fixture_source_row()`.
  - Add `_paper_native_current_fixture_coverage_summary()`.
  - Add `_paper_mapped_subset_native_current_fixture_contract_payload()`.
  - Wire the payload into `build_cpd_paper_offline_report()`.
- Modify: `tests/test_cpd_paper_offline.py`
  - Add RED tests for top-level gate movement, exact payload schema, row values, counts, false flags, malformed candidate-source input, malformed fixture input, and no runtime leakage.
- Modify: `tests/test_cli.py`
  - Add CLI JSON assertions for the new payload and top-level next gate.
- Modify docs after GREEN:
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
  - `experiments/registry.yaml`
  - Create: `docs/records/2026-05-17-cpd-paper-mapped-subset-native-current-fixture-contract.md`

## Task 1: Add RED Offline Tests

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`

- [ ] **Step 1: Add constants and helper input builders**

Add after `EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT`:

```python
EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT = (
    "paper_mapped_subset_primitivespec_native_fixture_generation_contract"
)
```

Change:

```python
EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS = [
    EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT,
]
```

to:

```python
EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT,
]
```

Add after `EXPECTED_CANDIDATE_SOURCE_REMAINING_GAPS`:

```python
EXPECTED_NATIVE_CURRENT_FIXTURE_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT,
]
```

Add after `_candidate_source_generation_input()`:

```python
def _native_current_fixture_candidate_source_input() -> dict[str, object]:
    report = build_cpd_paper_offline_report()
    return json.loads(
        json.dumps(
            report["paper_mapped_subset_primitivespec_candidate_source_contract"]
        )
    )


def _native_current_fixture_cases_input() -> list[dict[str, object]]:
    report = build_cpd_paper_offline_report()
    return json.loads(json.dumps(report["cases"]))
```

- [ ] **Step 2: Add required schema key sets**

Add after `PRIMITIVESPEC_CANDIDATE_SOURCE_AUDIT_ROW_REQUIRED_KEYS`:

```python
NATIVE_CURRENT_FIXTURE_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "paper_faithful_offline_allowed",
    "package_generation_allowed",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "native_current_fixture_action",
    "eligible_current_candidate_source_count",
    "primitive_spec_generation_candidate_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "native_current_fixture_contract",
    "input_contract_summary",
    "fixture_source_summary",
    "native_current_fixture_source_rows",
    "coverage_summary",
    "remaining_gaps",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}

NATIVE_CURRENT_FIXTURE_SOURCE_ROW_REQUIRED_KEYS = {
    "native_current_fixture_source_row_id",
    "source_candidate_source_audit_row_id",
    "source_primitivespec_generation_row_id",
    "source_primitivespec_generation_preflight_row_id",
    "source_primitivespec_validation_row_id",
    "source_primitivespec_dry_run_row_id",
    "source_adapter_preflight_row_id",
    "source_candidate_matrix_row_id",
    "source_conversion_plan_row_id",
    "fixture_id",
    "fixture_source_faces",
    "source_fit_selected_paper_primitive",
    "source_fit_candidate_scope",
    "source_fit_selection_rule",
    "paper_primitive",
    "primitive_spec_kind",
    "candidate_mapping_label",
    "newton_runtime_kind",
    "source_role",
    "candidate_source_decision",
    "candidate_source_reason",
    "eligible_current_candidate_source",
    "primitive_spec_generation_candidate",
    "generated_primitive_spec",
    "required_later_gate",
    "required_future_policy",
    "fit_model",
    "axis_selection_policy",
    "center",
    "axes",
    "half_extents",
    "volume",
    "weighted_volume",
    "contains_assigned_points",
    "primitive_parameter_lower_clamp",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}
```

- [ ] **Step 3: Add top-level gate and exact payload test**

Append after candidate-source tests:

```python
def test_cpd_paper_records_mapped_subset_native_current_fixture_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_native_current_fixture_contract"]

    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT
    )
    assert report["failure_labels"] == [
        "paper_mapped_subset_primitivespec_native_fixture_generation_contract_missing",
    ]
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_NATIVE_CURRENT_FIXTURE_REMAINING_GAPS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["status"] == "partial"
    assert report["package_generation_triggered"] is False
    assert report["newton_runtime_triggered"] is False
    assert report["real_usd_triggered"] is False
    assert report["benchmark_triggered"] is False
    assert report["collision_quality_measured"] is False
    assert report["deployment_or_certification_claimed"] is False

    assert payload["gate_id"] == EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT
    assert payload["gate_status"] == (
        "implemented_offline_native_current_fixture_contract_only_partial"
    )
    assert payload["closed_gate"] == EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT
    assert (
        payload["input_gate_id"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert (
        payload["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "native_current_fixture_contract_complete_"
        "primitivespec_native_fixture_generation_contract_missing"
    )
    assert payload["eligible_current_candidate_source_count"] == 1
    assert payload["primitive_spec_generation_candidate_count"] == 1
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_NATIVE_CURRENT_FIXTURE_REMAINING_GAPS
```

- [ ] **Step 4: Add payload schema, contract, and row tests**

Add:

```python
def test_cpd_paper_native_current_fixture_payload_schema_is_exact():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_native_current_fixture_contract"
    ]

    assert set(payload) == NATIVE_CURRENT_FIXTURE_PAYLOAD_REQUIRED_KEYS
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == (
        "offline_native_current_fixture_source_not_primitivespec_"
        "not_collision_package"
    )
    assert payload["implementation_boundary"] == (
        "offline_native_current_fixture_source_only_no_runtime_primitivespec_"
        "no_collision_package_no_newton"
    )
    assert payload["native_current_fixture_action"] == (
        "record_one_synthetic_native_current_fixture_source"
    )
    assert payload["native_current_fixture_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
        ),
        "native_current_fixture_gate_closed": (
            EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT
        ),
        "next_generation_gate_required": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT
        ),
        "source_fixture_required": "paper_single_box",
        "source_fit_selected_paper_primitive_required": "oriented_bounding_box",
        "source_template_row_required": "candidate_source_template__oriented_bounding_box",
        "native_fixture_rows_required": 1,
        "eligible_current_candidate_sources_required": 1,
        "primitive_spec_generation_candidates_required": 1,
        "generated_primitivespecs_required": 0,
        "generated_collision_packages_required": 0,
        "runtime_admissibility_checks_required": 0,
        "runtime_primitive_spec_generation_allowed": False,
        "collision_package_generation_allowed": False,
        "newton_runtime_allowed": False,
        "approximation_policy_enabled": False,
        "real_usd_allowed": False,
        "benchmark_allowed": False,
        "silent_drop_allowed": False,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT,
        "input_next_required_gate": EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT,
        "input_eligible_current_candidate_source_count": 0,
        "input_primitive_spec_generation_candidate_count": 0,
        "input_generated_primitive_spec_count": 0,
        "input_generated_collision_package_count": 0,
        "input_runtime_admissibility_check_count": 0,
        "native_template_candidate_source_audit_row_count": 3,
        "current_row_candidate_source_audit_row_count": 16,
    }
    for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
        assert payload[flag] is False


def test_cpd_paper_native_current_fixture_records_one_box_source_row():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_native_current_fixture_contract"
    ]

    rows = payload["native_current_fixture_source_rows"]
    assert len(rows) == 1
    row = rows[0]
    assert set(row) == NATIVE_CURRENT_FIXTURE_SOURCE_ROW_REQUIRED_KEYS
    assert row["native_current_fixture_source_row_id"] == (
        "native_current_fixture__paper_single_box__oriented_bounding_box"
    )
    assert (
        row["source_candidate_source_audit_row_id"]
        == "candidate_source_template__oriented_bounding_box"
    )
    assert row["fixture_id"] == "paper_single_box"
    assert row["fixture_source_faces"] == list(range(12))
    assert row["source_fit_selected_paper_primitive"] == "oriented_bounding_box"
    assert row["source_fit_candidate_scope"] == "paper_primitive_set_offline_audit_slice"
    assert row["source_fit_selection_rule"] == "min_paper_weighted_volume_for_fixture_audit"
    assert row["paper_primitive"] == "oriented_bounding_box"
    assert row["primitive_spec_kind"] == "box"
    assert row["candidate_mapping_label"] == "box"
    assert row["newton_runtime_kind"] == "box"
    assert row["source_role"] == "synthetic_native_current_fixture"
    assert row["candidate_source_decision"] == (
        "eligible_synthetic_native_current_fixture_source"
    )
    assert row["candidate_source_reason"] == (
        "paper_single_box_selected_obb_fixture_is_newton_native_box_source"
    )
    assert row["eligible_current_candidate_source"] is True
    assert row["primitive_spec_generation_candidate"] is True
    assert row["generated_primitive_spec"] is None
    assert (
        row["required_later_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT
    )
    assert row["required_future_policy"] == (
        "report_only_primitivespec_native_fixture_generation"
    )
    assert row["fit_model"] == "paper_operator_eigenbasis_projected_bounds"
    assert row["axis_selection_policy"] == "paper_q_eigenbasis"
    assert len(row["center"]) == 3
    assert len(row["axes"]) == 3
    assert all(len(axis) == 3 for axis in row["axes"])
    assert len(row["half_extents"]) == 3
    assert all(value > 0.0 for value in row["half_extents"])
    assert row["volume"] > 0.0
    assert row["weighted_volume"] > 0.0
    assert row["contains_assigned_points"] is True
    assert row["primitive_parameter_lower_clamp"] == 0.001
    for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
        assert row[flag] is False
```

- [ ] **Step 5: Add coverage, no-leak, and rejection tests**

Add:

```python
def test_cpd_paper_native_current_fixture_coverage_summary_is_exact():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_native_current_fixture_contract"
    ]

    assert payload["fixture_source_summary"] == {
        "fixture_id": "paper_single_box",
        "fixture_source_faces": list(range(12)),
        "selected_paper_primitive": "oriented_bounding_box",
        "selected_newton_runtime_kind": "box",
        "contains_assigned_points": True,
    }
    assert payload["coverage_summary"] == {
        "native_current_fixture_source_row_count": 1,
        "eligible_current_candidate_source_count": 1,
        "primitive_spec_generation_candidate_record_count": 1,
        "generated_primitive_spec_record_count": 0,
        "generated_collision_package_record_count": 0,
        "runtime_admissibility_check_record_count": 0,
        "fixture_id_distribution": {"paper_single_box": 1},
        "paper_primitive_distribution": {"oriented_bounding_box": 1},
        "candidate_mapping_label_distribution": {"box": 1},
        "native_current_fixture_decision_distribution": {
            "eligible_synthetic_native_current_fixture_source": 1,
        },
    }


def test_cpd_paper_native_current_fixture_stays_report_only():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_native_current_fixture_contract"
    ]

    forbidden_keys = {
        "CollisionPackage",
        "PrimitiveSpec",
        "runtime_result",
        "usd_asset_path",
        "benchmark_metric",
        "timing",
        "surface_distance",
        "collision_quality",
    }
    assert forbidden_keys.isdisjoint(payload)
    assert payload["primitive_spec_generation_candidate_count"] == 1
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
        assert payload[flag] is False
    for row in payload["native_current_fixture_source_rows"]:
        assert forbidden_keys.isdisjoint(row)
        assert row["primitive_spec_generation_candidate"] is True
        assert row["generated_primitive_spec"] is None
        for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
            assert row[flag] is False


def test_cpd_paper_native_current_fixture_rejects_wrong_candidate_source_gate():
    candidate_source = _native_current_fixture_candidate_source_input()
    candidate_source["gate_id"] = "stale_gate"

    with pytest.raises(
        ValueError,
        match="native_current_fixture_input_gate_id_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            candidate_source,
            _native_current_fixture_cases_input(),
        )


def test_cpd_paper_native_current_fixture_rejects_stale_candidate_source_next_gate():
    candidate_source = _native_current_fixture_candidate_source_input()
    candidate_source["next_required_gate"] = "stale_gate"

    with pytest.raises(
        ValueError,
        match="native_current_fixture_input_next_gate_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            candidate_source,
            _native_current_fixture_cases_input(),
        )


def test_cpd_paper_native_current_fixture_rejects_nonzero_input_candidate_counts():
    candidate_source = _native_current_fixture_candidate_source_input()
    candidate_source["eligible_current_candidate_source_count"] = 1

    with pytest.raises(
        ValueError,
        match="native_current_fixture_input_candidate_count_nonzero",
    ):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            candidate_source,
            _native_current_fixture_cases_input(),
        )


def test_cpd_paper_native_current_fixture_rejects_true_input_runtime_flags():
    candidate_source = _native_current_fixture_candidate_source_input()
    candidate_source["newton_runtime_triggered"] = True

    with pytest.raises(
        ValueError,
        match="native_current_fixture_input_trigger_flag_true:newton_runtime_triggered",
    ):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            candidate_source,
            _native_current_fixture_cases_input(),
        )


def test_cpd_paper_native_current_fixture_rejects_template_drift():
    candidate_source = _native_current_fixture_candidate_source_input()
    rows = [
        dict(row)
        for row in candidate_source["native_template_candidate_source_audit_rows"]
    ]
    rows[0]["primitive_spec_kind"] = "capsule"
    candidate_source["native_template_candidate_source_audit_rows"] = rows

    with pytest.raises(
        ValueError,
        match="native_current_fixture_template_row_mismatch:primitive_spec_kind",
    ):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            candidate_source,
            _native_current_fixture_cases_input(),
        )


def test_cpd_paper_native_current_fixture_rejects_missing_single_box_case():
    cases = [
        case
        for case in _native_current_fixture_cases_input()
        if case["case_id"] != "paper_single_box"
    ]

    with pytest.raises(
        ValueError,
        match="native_current_fixture_source_case_missing:paper_single_box",
    ):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            _native_current_fixture_candidate_source_input(),
            cases,
        )


def test_cpd_paper_native_current_fixture_rejects_non_obb_selected_fit():
    cases = _native_current_fixture_cases_input()
    case = next(case for case in cases if case["case_id"] == "paper_single_box")
    selected = dict(case["primitive_fit_audit"]["selected"])
    selected["paper_primitive"] = "sphere"
    case["primitive_fit_audit"]["selected"] = selected

    with pytest.raises(
        ValueError,
        match="native_current_fixture_selected_fit_not_obb",
    ):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            _native_current_fixture_candidate_source_input(),
            cases,
        )


def test_cpd_paper_native_current_fixture_rejects_invalid_fit_geometry():
    cases = _native_current_fixture_cases_input()
    case = next(case for case in cases if case["case_id"] == "paper_single_box")
    selected = dict(case["primitive_fit_audit"]["selected"])
    dimensions = dict(selected["dimensions"])
    dimensions["half_extents"] = [0.0, 0.5, 1.0]
    selected["dimensions"] = dimensions
    case["primitive_fit_audit"]["selected"] = selected

    with pytest.raises(
        ValueError,
        match="native_current_fixture_invalid_half_extents",
    ):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            _native_current_fixture_candidate_source_input(),
            cases,
        )
```

- [ ] **Step 6: Run tests and verify RED**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k 'native_current_fixture' -q
```

Expected before implementation: failures because
`paper_mapped_subset_native_current_fixture_contract` and
`_paper_mapped_subset_native_current_fixture_contract_payload` are missing.

## Task 2: Implement The Offline Native Current Fixture Gate

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add constant and remaining-gap helper**

Add near the existing mapped-subset constants:

```python
_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT = (
    "paper_mapped_subset_primitivespec_native_fixture_generation_contract"
)
```

Add near the candidate-source remaining-gap helper:

```python
def _paper_remaining_gaps_after_mapped_subset_native_current_fixture() -> list[str]:
    return [
        _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT
    ]
```

- [ ] **Step 2: Add candidate-source input validation**

Add validation helpers after `_paper_mapped_subset_primitivespec_candidate_source_contract_payload()`:

```python
def _paper_validate_native_current_fixture_false_flags(
    row: dict[str, object],
) -> None:
    for flag in _PRIMITIVESPEC_VALIDATION_ROW_FALSE_FLAGS:
        if bool(row.get(flag)):
            raise ValueError(
                f"native_current_fixture_input_trigger_flag_true:{flag}"
            )


def _paper_validate_native_current_fixture_candidate_source_input(
    candidate_source: dict[str, object],
) -> None:
    if candidate_source.get("gate_id") != _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT:
        raise ValueError("native_current_fixture_input_gate_id_mismatch")
    if candidate_source.get("next_required_gate") != _PAPER_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT:
        raise ValueError("native_current_fixture_input_next_gate_mismatch")
    for field_name in ("paper_faithful_offline_allowed", "package_generation_allowed"):
        if bool(candidate_source.get(field_name)):
            raise ValueError(f"native_current_fixture_input_boundary_flag_true:{field_name}")
    _paper_validate_native_current_fixture_false_flags(candidate_source)
    if candidate_source["eligible_current_candidate_source_count"] != 0:
        raise ValueError("native_current_fixture_input_candidate_count_nonzero")
    if candidate_source["primitive_spec_generation_candidate_count"] != 0:
        raise ValueError("native_current_fixture_input_generation_candidate_count_nonzero")
    if candidate_source["generated_primitive_spec_count"] != 0:
        raise ValueError("native_current_fixture_input_generated_spec_nonzero")
    if candidate_source["generated_collision_package_count"] != 0:
        raise ValueError("native_current_fixture_input_generated_collision_package_nonzero")
    if candidate_source["runtime_admissibility_check_count"] != 0:
        raise ValueError("native_current_fixture_input_runtime_admissibility_nonzero")
    coverage = candidate_source["coverage_summary"]
    expected_coverage = {
        "native_template_candidate_source_audit_row_count": 3,
        "blocked_family_candidate_source_audit_row_count": 2,
        "noop_family_candidate_source_audit_row_count": 1,
        "current_row_candidate_source_audit_row_count": 16,
        "eligible_current_candidate_source_count": 0,
        "primitive_spec_generation_candidate_record_count": 0,
        "generated_primitive_spec_record_count": 0,
        "generated_collision_package_record_count": 0,
        "runtime_admissibility_check_record_count": 0,
    }
    for field_name, expected_value in expected_coverage.items():
        if coverage[field_name] != expected_value:
            raise ValueError(f"native_current_fixture_coverage_count_mismatch:{field_name}")
    native_rows = candidate_source["native_template_candidate_source_audit_rows"]
    if len(native_rows) != 3:
        raise ValueError("native_current_fixture_native_template_row_count_mismatch")
    obb_rows = [
        row
        for row in native_rows
        if row["candidate_source_audit_row_id"] == "candidate_source_template__oriented_bounding_box"
    ]
    if len(obb_rows) != 1:
        raise ValueError("native_current_fixture_obb_template_row_missing")
    _paper_validate_native_current_fixture_obb_template_row(obb_rows[0])
```

Implement `_paper_validate_native_current_fixture_obb_template_row()` with exact checks for
`paper_primitive == "oriented_bounding_box"`, `primitive_spec_kind == "box"`,
`candidate_mapping_label == "box"`, `source_role == "future_native_template"`,
`eligible_current_candidate_source is False`, `primitive_spec_generation_candidate is False`,
`generated_primitive_spec is None`, and false runtime flags.

Also add negative tests for generation-candidate count, generated-spec count, generated-package
count, runtime-admissibility count, coverage count drift, missing OBB template row, OBB template
`source_role` drift, OBB template eligibility drift, and OBB template runtime-flag drift.

- [ ] **Step 3: Add fixture selection and selected-fit validation**

Add:

```python
def _paper_single_box_case(cases: list[dict[str, object]]) -> dict[str, object]:
    matches = [case for case in cases if case["case_id"] == "paper_single_box"]
    if len(matches) != 1:
        raise ValueError("native_current_fixture_source_case_missing:paper_single_box")
    return matches[0]
```

Add `_paper_validate_native_current_fixture_selected_fit(selected, primitive_fit_audit)` that checks:

```text
paper_primitive == oriented_bounding_box
newton_runtime_kind == box
current_implementation_kind == offline_paper_oriented_bounding_box_fit
fit_model == paper_operator_eigenbasis_projected_bounds
axis_selection_policy == paper_q_eigenbasis
contains_assigned_points == true
center length == 3 and finite
axes is 3x3 and finite
dimensions.half_extents length == 3, finite, and all positive
volume and weighted_volume finite and positive
primitive_parameter_lower_clamp == PAPER_PRIMITIVE_MIN_DIMENSION
source_faces is non-empty
```

Use `np.isfinite()` and raise the labels used by the RED tests:

```text
native_current_fixture_selected_fit_not_obb
native_current_fixture_selected_fit_not_newton_box
native_current_fixture_selected_fit_missing_source_faces
native_current_fixture_invalid_center
native_current_fixture_invalid_axes
native_current_fixture_invalid_half_extents
native_current_fixture_invalid_volume
native_current_fixture_invalid_weighted_volume
native_current_fixture_selected_fit_not_containing_points
native_current_fixture_clamp_mismatch
```

Also add negative tests for duplicate `paper_single_box`, missing `primitive_fit_audit`, empty
`source_faces`, wrong `newton_runtime_kind`, wrong fit model, wrong axis policy, nonfinite center,
nonfinite axes, nonfinite volume, nonfinite weighted volume, false containment, and clamp mismatch.

- [ ] **Step 4: Build the row, coverage, and payload**

Add `_paper_native_current_fixture_source_row(template_row, case)` that returns the row required by
the tests. Copy source ids from the OBB template row. Copy `center`, `axes`, `volume`, and
`weighted_volume` from `case["primitive_fit_audit"]["selected"]`, and derive `half_extents` from
`case["primitive_fit_audit"]["selected"]["dimensions"]["half_extents"]`; there is no top-level
`selected["half_extents"]`.

Add `_paper_native_current_fixture_coverage_summary(rows)`:

```python
return {
    "native_current_fixture_source_row_count": len(rows),
    "eligible_current_candidate_source_count": sum(bool(row["eligible_current_candidate_source"]) for row in rows),
    "primitive_spec_generation_candidate_record_count": sum(bool(row["primitive_spec_generation_candidate"]) for row in rows),
    "generated_primitive_spec_record_count": sum(row["generated_primitive_spec"] is not None for row in rows),
    "generated_collision_package_record_count": 0,
    "runtime_admissibility_check_record_count": 0,
    "fixture_id_distribution": _paper_policy_distribution(rows, "fixture_id"),
    "paper_primitive_distribution": _paper_policy_distribution(rows, "paper_primitive"),
    "candidate_mapping_label_distribution": _paper_policy_distribution(rows, "candidate_mapping_label"),
    "native_current_fixture_decision_distribution": _paper_policy_distribution(rows, "candidate_source_decision"),
}
```

Add `_paper_mapped_subset_native_current_fixture_contract_payload(candidate_source, cases)` with
the exact fields asserted in Task 1.

- [ ] **Step 5: Wire the payload into report builder**

In `build_cpd_paper_offline_report()`:

```python
mapped_subset_native_current_fixture = (
    _paper_mapped_subset_native_current_fixture_contract_payload(
        mapped_subset_primitivespec_candidate_source,
        cases,
    )
)
missing_before_paper_faithful = (
    _paper_remaining_gaps_after_mapped_subset_native_current_fixture()
)
```

Set top-level `next_required_gate` to
`_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT`, append
`_PAPER_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT` to
`implemented_output_contract_scope`, and add:

```python
"paper_mapped_subset_native_current_fixture_contract": (
    mapped_subset_native_current_fixture
),
```

- [ ] **Step 6: Run GREEN tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k 'native_current_fixture' -q
python -m pytest tests/test_cpd_paper_offline.py -k 'candidate_source or native_current_fixture' -q
```

Expected: all selected tests pass.

During this step, update all existing top-level report assertions that check `failure_labels`,
`next_required_gate`, `missing_before_paper_faithful_offline`, or exact
`implemented_output_contract_scope` so they expect
`paper_mapped_subset_primitivespec_native_fixture_generation_contract` as the current top-level
gap and include `paper_mapped_subset_native_current_fixture_contract` as an implemented output
contract. Do not change the candidate-source payload's own `next_required_gate`; that nested
payload still points to `paper_mapped_subset_native_current_fixture_contract`.

## Task 3: Add CLI Coverage

**Files:**
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add CLI assertions**

In the CPD paper offline report CLI test, update the top-level next gate and failure label to:

```python
assert payload["next_required_gate"] == (
    "paper_mapped_subset_primitivespec_native_fixture_generation_contract"
)
assert payload["failure_labels"] == [
    "paper_mapped_subset_primitivespec_native_fixture_generation_contract_missing",
]
```

Append:

```python
native_fixture = payload["paper_mapped_subset_native_current_fixture_contract"]
assert native_fixture["gate_id"] == "paper_mapped_subset_native_current_fixture_contract"
assert native_fixture["input_gate_id"] == (
    "paper_mapped_subset_primitivespec_candidate_source_contract"
)
assert native_fixture["next_required_gate"] == (
    "paper_mapped_subset_primitivespec_native_fixture_generation_contract"
)
assert native_fixture["eligible_current_candidate_source_count"] == 1
assert native_fixture["primitive_spec_generation_candidate_count"] == 1
assert native_fixture["generated_primitive_spec_count"] == 0
assert native_fixture["generated_collision_package_count"] == 0
assert native_fixture["runtime_admissibility_check_count"] == 0
assert len(native_fixture["native_current_fixture_source_rows"]) == 1
row = native_fixture["native_current_fixture_source_rows"][0]
assert row["fixture_id"] == "paper_single_box"
assert row["paper_primitive"] == "oriented_bounding_box"
assert row["primitive_spec_kind"] == "box"
assert row["candidate_mapping_label"] == "box"
assert row["newton_runtime_kind"] == "box"
assert row["eligible_current_candidate_source"] is True
assert row["primitive_spec_generation_candidate"] is True
assert row["generated_primitive_spec"] is None
assert native_fixture["primitive_spec_generated"] is False
assert native_fixture["collision_package_generated"] is False
assert native_fixture["runtime_admissibility_checked"] is False
assert native_fixture["newton_support_claimed"] is False
assert native_fixture["package_generation_triggered"] is False
assert native_fixture["newton_runtime_triggered"] is False
assert native_fixture["real_usd_triggered"] is False
assert native_fixture["benchmark_triggered"] is False
```

- [ ] **Step 2: Run CLI RED/GREEN**

Before implementation this should fail if run with Task 1 RED tests:

```bash
python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

After implementation, expected: selected CLI tests pass.

## Task 4: Update Documentation And Registry

**Files:**
- Modify docs and registry listed in the file map.
- Create: `docs/records/2026-05-17-cpd-paper-mapped-subset-native-current-fixture-contract.md`

- [ ] **Step 1: Update reference docs**

Add plain-language text that the native-current-fixture gate records exactly one synthetic
`paper_single_box` OBB/box source row and advances to
`paper_mapped_subset_primitivespec_native_fixture_generation_contract`. Every updated doc must say
this is not runtime `PrimitiveSpec` generation, not `CollisionPackage` generation, not Newton
runtime, not real-USD evidence, not benchmark evidence, not collision-quality evidence, and not
full CPD reproduction.

- [ ] **Step 2: Add dated record**

Create `docs/records/2026-05-17-cpd-paper-mapped-subset-native-current-fixture-contract.md` with:

```markdown
# CPD Paper Mapped-Subset Native Current Fixture Contract

## Date

2026-05-17

## Status

Complete for a command-only offline/report-only native current fixture source contract. Not
complete for runtime `PrimitiveSpec` generation, `CollisionPackage` generation, runtime
admissibility, Newton runtime, real-USD evidence, benchmarks, collision-quality measurement,
deployment readiness, or safety certification.
```

Include What Changed, Boundary, Verification, Artifacts, Claim Impact, and Next Action sections.

- [ ] **Step 3: Update registry**

Append a new `experiments/registry.yaml` entry with id:

```text
cpd-paper-mapped-subset-native-current-fixture-contract
```

The entry must link to the new record and state only offline/report-only source contract evidence.

- [ ] **Step 4: Run docs checks**

Run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

## Task 5: Final Verification And Review

**Files:**
- No new code files beyond previous tasks.

- [x] **Review fix checkpoint**

External review found two validation gaps after the first implementation pass:

- candidate-source current rows could leak eligible/generation/runtime fields even while top-level
  counts stayed zero;
- selected `paper_single_box` OBB geometry was finite but not checked against the OBB candidate row
  in the same primitive-fit audit.

The fix adds RED/GREEN tests for both cases and tightens input validation before the source row is
emitted. This still remains report-only/offline and still generates zero runtime PrimitiveSpecs,
zero CollisionPackages, and zero Newton checks.

- [ ] **Step 1: Run targeted verification**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k 'candidate_source or native_current_fixture' -q
python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Expected: pass.

- [ ] **Step 2: Run full verification**

Run:

```bash
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: pass.

- [ ] **Step 3: Request multi-agent review**

Ask one reviewer to check code/test behavior and one reviewer to check docs/claim boundaries. Fix
Critical and Important findings, rerun the affected tests, and request re-review.

- [ ] **Step 4: Merge and push after clean review**

Fast-forward merge to `main`, rerun full verification on `main`, push `origin main`, and remove the
feature worktree only after `main` is clean.
