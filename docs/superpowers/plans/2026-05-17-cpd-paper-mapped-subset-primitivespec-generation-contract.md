# CPD Paper Mapped-Subset PrimitiveSpec Generation Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the offline/report-only `paper_mapped_subset_primitivespec_generation_contract` gate that closes the named generation contract without producing runtime `PrimitiveSpec`, `CollisionPackage`, Newton, real-USD, benchmark, collision-quality, deployment, or safety evidence.

**Architecture:** Consume the existing `paper_mapped_subset_primitivespec_generation_preflight_contract` payload, validate it strictly, emit three native-family template rows for box/sphere/capsule, emit blocked/no-op rows for unsupported or unmapped paper families, and emit 16 current-row no-generation records. The top-level report remains partial and advances to `paper_mapped_subset_primitivespec_candidate_source_contract`, which names the real blocker before runtime PrimitiveSpec/package work.

**Tech Stack:** Python, pytest, existing CPD paper offline report builder, Markdown docs, YAML experiment registry.

---

## File Map

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
  - Add `_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT`.
  - Add `_paper_remaining_gaps_after_mapped_subset_primitivespec_generation()`.
  - Add generation-contract validators for the generation-preflight payload.
  - Add row builders for native-family template rows, blocked/no-op requirement rows, and current no-generation rows.
  - Add `_paper_require_unique_generation_row_ids()`.
  - Add `_paper_mapped_subset_primitivespec_generation_contract_payload()`.
  - Wire the new payload into `build_cpd_paper_offline_report()`.
- Modify: `tests/test_cpd_paper_offline.py`
  - Add RED tests for payload shape, row content, false flags, coverage counts, rejection labels, top-level report integration, and unique emitted ids.
- Modify: `tests/test_cli.py`
  - Add CLI JSON assertions for the new generation payload and the new top-level next gate.
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
  - `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-generation-contract.md`
  - `experiments/registry.yaml`

## Task 1: Add RED Offline Tests

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`

- [ ] **Step 1: Add imports and constants**

Add `_paper_mapped_subset_primitivespec_generation_contract_payload` and
`_paper_require_unique_generation_row_ids` to the existing import block:

```python
from primitive_collision_compiler.baselines.cpd_paper.offline import (
    CPD_PAPER_OFFLINE_CLAIM_BOUNDARY,
    _paper_mapped_subset_adapter_preflight_contract_payload,
    _paper_mapped_subset_primitivespec_dry_run_contract_payload,
    _paper_mapped_subset_primitivespec_generation_contract_payload,
    _paper_mapped_subset_primitivespec_generation_preflight_contract_payload,
    _paper_mapped_subset_primitivespec_validation_contract_payload,
    _paper_package_adapter_contract_payload,
    _paper_require_unique_generation_preflight_row_ids,
    _paper_require_unique_generation_row_ids,
    build_cpd_paper_offline_report,
)
```

Add the next-gate constant below
`EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT`:

```python
EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT = (
    "paper_mapped_subset_primitivespec_candidate_source_contract"
)
EXPECTED_GENERATION_CONTRACT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT,
]
```

Change:

```python
EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT,
]
```

to:

```python
EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT,
]
```

- [ ] **Step 2: Add helper and row false flags**

Add this helper after `_generation_preflight_validation_input()`:

```python
def _generation_contract_preflight_input() -> dict[str, object]:
    report = build_cpd_paper_offline_report()
    return json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_primitivespec_generation_preflight_contract"
            ]
        )
    )
```

Add a generation-contract false-flag tuple. It must match the row-level validation flags:

```python
PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS = (
    "primitive_spec_generated",
    "collision_package_generated",
    "runtime_admissibility_checked",
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
    "primitive_spec_generation_allowed",
    "collision_package_generation_allowed",
    "runtime_admissibility_supported",
    "newton_runtime_allowed",
    "approximation_policy_enabled",
    "silent_drop_allowed",
    "primitive_spec_generation_triggered",
    "collision_package_generation_triggered",
    "runtime_admissibility_triggered",
)
```

- [ ] **Step 3: Add exact payload and row schema constants**

Add these constants below `PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS`:

```python
PRIMITIVESPEC_GENERATION_PAYLOAD_REQUIRED_KEYS = {
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
    "primitive_spec_generation_action",
    "primitive_spec_generation_candidate_count",
    "offline_primitivespec_template_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "input_contract_summary",
    "primitive_spec_generation_contract",
    "native_family_primitivespec_template_rows",
    "blocked_primitivespec_generation_requirement_rows",
    "noop_primitivespec_generation_requirement_rows",
    "current_row_primitivespec_generation_rows",
    "coverage_summary",
    "remaining_gaps",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}

PRIMITIVESPEC_GENERATION_NATIVE_TEMPLATE_ROW_REQUIRED_KEYS = {
    "primitive_spec_generation_template_row_id",
    "source_primitivespec_generation_preflight_row_id",
    "source_primitivespec_validation_row_id",
    "source_primitivespec_dry_run_row_id",
    "source_adapter_preflight_row_id",
    "source_candidate_matrix_row_id",
    "source_conversion_plan_row_id",
    "paper_primitive",
    "primitive_spec_kind",
    "candidate_mapping_label",
    "input_primitivespec_generation_preflight_decision",
    "required_primitive_spec_fields",
    "template_only",
    "runtime_instance_generated",
    "primitive_spec_generation_candidate",
    "generated_primitive_spec",
    "silent_drop_detected",
    "primitive_spec_generation_decision",
    "required_current_candidate_source_gate",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}

PRIMITIVESPEC_GENERATION_REQUIREMENT_ROW_REQUIRED_KEYS = {
    "primitive_spec_generation_requirement_row_id",
    "source_primitivespec_generation_preflight_row_id",
    "source_primitivespec_validation_row_id",
    "source_primitivespec_dry_run_row_id",
    "source_adapter_preflight_row_id",
    "source_candidate_matrix_row_id",
    "source_conversion_plan_row_id",
    "paper_primitive",
    "candidate_mapping_label",
    "input_primitivespec_generation_preflight_decision",
    "primitive_spec_generation_decision",
    "primitive_spec_generation_action",
    "primitive_spec_generation_candidate",
    "generated_primitive_spec",
    "required_later_gate",
    "required_future_policy",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}

PRIMITIVESPEC_GENERATION_CURRENT_ROW_REQUIRED_KEYS = {
    "primitive_spec_generation_row_id",
    "source_primitivespec_generation_preflight_row_id",
    "source_primitivespec_validation_row_id",
    "source_primitivespec_dry_run_row_id",
    "source_adapter_preflight_row_id",
    "source_candidate_matrix_row_id",
    "source_conversion_plan_row_id",
    "source_policy_decision_id",
    "source_adapter_decision_id",
    "source_output_id",
    "evidence_case_id",
    "offline_primitive_id",
    "paper_primitive",
    "offline_mapping_label",
    "primitive_spec_generation_decision",
    "primitive_spec_generation_action",
    "primitive_spec_generation_candidate",
    "generated_primitive_spec",
    "silent_drop_detected",
    "required_later_gate",
    "required_future_policy",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}
```

- [ ] **Step 4: Update existing top-level gate expectations**

Search the existing offline tests for hard-coded top-level references to
`EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT` and replace only the top-level
`report["next_required_gate"]`, `report["failure_labels"]`, and
`report["paper_faithfulness"]["missing_before_paper_faithful_offline"]` expectations with
`EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT` or
`EXPECTED_GENERATION_CONTRACT_REMAINING_GAPS`.

The generation-preflight nested payload must keep:

```python
assert (
    report["paper_mapped_subset_primitivespec_generation_preflight_contract"][
        "next_required_gate"
    ]
    == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
)
```

Run this check while editing:

```bash
rg -n "next_required_gate|failure_labels|missing_before_paper_faithful_offline|EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT" tests/test_cpd_paper_offline.py
```

The exact migrated top-level assertions should use:

```python
assert (
    report["next_required_gate"]
    == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
)
assert report["failure_labels"] == [
    "paper_mapped_subset_primitivespec_candidate_source_contract_missing",
]
assert (
    report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
    == EXPECTED_GENERATION_CONTRACT_REMAINING_GAPS
)
```

- [ ] **Step 5: Add report integration RED test**

Add this test after the existing generation-preflight tests:

```python
def test_cpd_paper_records_mapped_subset_primitivespec_generation_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_primitivespec_generation_contract"]

    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert report["failure_labels"] == [
        "paper_mapped_subset_primitivespec_candidate_source_contract_missing",
    ]
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_GENERATION_CONTRACT_REMAINING_GAPS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["status"] == "partial"
    assert report["paper_faithful_offline_supported"] is False
    assert report["package_generation_triggered"] is False
    assert report["newton_runtime_triggered"] is False
    assert report["real_usd_triggered"] is False
    assert report["benchmark_triggered"] is False
    assert report["collision_quality_measured"] is False
    assert report["deployment_or_certification_claimed"] is False

    preflight = report[
        "paper_mapped_subset_primitivespec_generation_preflight_contract"
    ]
    assert (
        preflight["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
    )

    assert (
        payload["gate_id"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
    )
    assert payload["gate_status"] == (
        "implemented_offline_primitivespec_generation_contract_only_partial"
    )
    assert (
        payload["closed_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
    )
    assert (
        payload["input_gate_id"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
    )
    assert (
        payload["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "primitivespec_generation_contract_complete_"
        "mapped_current_candidate_source_contract_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == (
        "offline_primitivespec_generation_contract_template_rows_"
        "not_runtime_primitivespec_not_collision_package"
    )
    assert payload["primitive_spec_generation_action"] == (
        "emit_offline_templates_and_keep_current_rows_offline"
    )
    assert payload["primitive_spec_generation_candidate_count"] == 0
    assert payload["offline_primitivespec_template_count"] == 3
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_GENERATION_CONTRACT_REMAINING_GAPS
```

- [ ] **Step 6: Add payload-shape RED test**

Add:

```python
def test_cpd_paper_primitivespec_generation_payload_schema_is_exact():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_primitivespec_generation_contract"
    ]

    assert set(payload) == PRIMITIVESPEC_GENERATION_PAYLOAD_REQUIRED_KEYS
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["implementation_boundary"] == (
        "offline_primitivespec_generation_templates_only_no_runtime_"
        "primitivespec_no_collision_package_no_newton"
    )
    assert payload["input_contract_summary"] == {
        "input_gate_id": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
        ),
        "input_artifact_kind": (
            "offline_primitivespec_generation_preflight_contract_not_"
            "primitivespec_not_collision_package"
        ),
        "primitive_spec_generation_preflight_requirement_row_count": 6,
        "current_row_primitivespec_generation_preflight_row_count": 16,
        "generation_preflight_candidate_record_count": 0,
        "generated_primitive_spec_record_count": 0,
    }
    assert payload["primitive_spec_generation_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
        ),
        "current_candidate_source_gate_required": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
        ),
        "template_only_native_families": ["box", "sphere", "capsule"],
        "zero_runtime_primitivespecs_required": True,
        "zero_collision_packages_required": True,
        "zero_runtime_admissibility_checks_required": True,
        "runtime_primitive_spec_generation_allowed": False,
        "collision_package_generation_allowed": False,
        "newton_runtime_allowed": False,
        "approximation_policy_enabled": False,
        "silent_drop_allowed": False,
    }
```

- [ ] **Step 7: Add native template RED test**

Add:

```python
def test_cpd_paper_primitivespec_generation_emits_native_family_templates_only():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_primitivespec_generation_contract"
    ]
    rows = {
        row["paper_primitive"]: row
        for row in payload["native_family_primitivespec_template_rows"]
    }

    assert list(rows) == ["oriented_bounding_box", "sphere", "capsule"]
    for primitive_name, kind in (
        ("oriented_bounding_box", "box"),
        ("sphere", "sphere"),
        ("capsule", "capsule"),
    ):
        row = rows[primitive_name]
        assert set(row) == PRIMITIVESPEC_GENERATION_NATIVE_TEMPLATE_ROW_REQUIRED_KEYS
        assert row["primitive_spec_kind"] == kind
        assert row["candidate_mapping_label"] == kind
        assert row["input_primitivespec_generation_preflight_decision"] == (
            "future_native_family_generation_requirement_preflighted"
        )
        assert row["required_primitive_spec_fields"] == [
            "primitive_id",
            "kind",
            "center",
            "axes",
            "dimensions",
            "frame",
            "source_faces",
            "contains_assigned_points",
            "volume",
            "weighted_volume",
            "conversion_status",
        ]
        assert row["template_only"] is True
        assert row["runtime_instance_generated"] is False
        assert row["primitive_spec_generation_candidate"] is False
        assert row["generated_primitive_spec"] is None
        assert row["silent_drop_detected"] is False
        assert row["primitive_spec_generation_decision"] == (
            "native_family_primitivespec_template_generated_offline_only"
        )
        assert (
            row["required_current_candidate_source_gate"]
            == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
        )
        for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
            assert row[flag] is False
```

- [ ] **Step 8: Add blocked/no-op requirement RED test**

Add:

```python
def test_cpd_paper_primitivespec_generation_records_blocked_and_noop_family_rows():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_primitivespec_generation_contract"
    ]
    blocked = {
        row["paper_primitive"]: row
        for row in payload["blocked_primitivespec_generation_requirement_rows"]
    }
    noop = {
        row["paper_primitive"]: row
        for row in payload["noop_primitivespec_generation_requirement_rows"]
    }

    assert list(blocked) == ["capped_cylinder", "frustum"]
    for row in blocked.values():
        assert set(row) == PRIMITIVESPEC_GENERATION_REQUIREMENT_ROW_REQUIRED_KEYS
        assert row["candidate_mapping_label"] == "offline_only_unmapped"
        assert row["input_primitivespec_generation_preflight_decision"] == (
            "blocked_approximation_policy_generation_preflight_recorded"
        )
        assert row["primitive_spec_generation_decision"] == (
            "blocked_approximation_policy_before_primitivespec_generation"
        )
        assert row["primitive_spec_generation_action"] == (
            "require_explicit_approximation_policy"
        )
        assert row["primitive_spec_generation_candidate"] is False
        assert row["generated_primitive_spec"] is None
        assert (
            row["required_later_gate"]
            == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
        )
        assert row["required_future_policy"] == "approximation_policy"
        for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
            assert row[flag] is False

    assert list(noop) == ["trapezoidal_prism"]
    row = noop["trapezoidal_prism"]
    assert set(row) == PRIMITIVESPEC_GENERATION_REQUIREMENT_ROW_REQUIRED_KEYS
    assert row["candidate_mapping_label"] == "offline_only_unmapped"
    assert row["input_primitivespec_generation_preflight_decision"] == (
        "noop_unmapped_family_generation_preflight_recorded"
    )
    assert row["primitive_spec_generation_decision"] == (
        "noop_unmapped_family_before_primitivespec_generation"
    )
    assert row["primitive_spec_generation_action"] == "keep_unmapped_family_offline"
    assert row["primitive_spec_generation_candidate"] is False
    assert row["generated_primitive_spec"] is None
    assert (
        row["required_later_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert row["required_future_policy"] == "mapped_current_candidate_source"
```

- [ ] **Step 9: Add current-row no-generation RED test**

Add:

```python
def test_cpd_paper_primitivespec_generation_keeps_current_rows_no_generation():
    report = build_cpd_paper_offline_report()
    preflight = report[
        "paper_mapped_subset_primitivespec_generation_preflight_contract"
    ]
    payload = report["paper_mapped_subset_primitivespec_generation_contract"]
    rows = payload["current_row_primitivespec_generation_rows"]
    upstream_rows = preflight["current_row_primitivespec_generation_preflight_rows"]

    assert len(rows) == len(upstream_rows) == 16
    for row, upstream_row in zip(rows, upstream_rows):
        assert set(row) == PRIMITIVESPEC_GENERATION_CURRENT_ROW_REQUIRED_KEYS
        assert row["source_primitivespec_generation_preflight_row_id"] == (
            upstream_row["primitive_spec_generation_preflight_row_id"]
        )
        assert row["source_primitivespec_validation_row_id"] == (
            upstream_row["source_primitivespec_validation_row_id"]
        )
        assert row["source_primitivespec_dry_run_row_id"] == (
            upstream_row["source_primitivespec_dry_run_row_id"]
        )
        assert row["source_adapter_preflight_row_id"] == (
            upstream_row["source_adapter_preflight_row_id"]
        )
        assert row["source_candidate_matrix_row_id"] == (
            upstream_row["source_candidate_matrix_row_id"]
        )
        assert row["source_conversion_plan_row_id"] == (
            upstream_row["source_conversion_plan_row_id"]
        )
        assert row["source_policy_decision_id"] == (
            upstream_row["source_policy_decision_id"]
        )
        assert row["source_adapter_decision_id"] == (
            upstream_row["source_adapter_decision_id"]
        )
        assert row["source_output_id"] == upstream_row["source_output_id"]
        assert row["evidence_case_id"] == upstream_row["evidence_case_id"]
        assert row["offline_primitive_id"] == upstream_row["offline_primitive_id"]
        assert row["paper_primitive"] == "trapezoidal_prism"
        assert row["offline_mapping_label"] == "offline_only_unmapped"
        assert row["primitive_spec_generation_decision"] == (
            "skip_unmapped_current_row_no_primitivespec_generated"
        )
        assert row["primitive_spec_generation_action"] == (
            "keep_offline_until_mapped_current_candidate_exists"
        )
        assert row["primitive_spec_generation_candidate"] is False
        assert row["generated_primitive_spec"] is None
        assert row["silent_drop_detected"] is False
        assert (
            row["required_later_gate"]
            == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
        )
        assert row["required_future_policy"] == "mapped_current_candidate_source"
        for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
            assert row[flag] is False
```

- [ ] **Step 10: Add coverage-summary RED test**

Add:

```python
def test_cpd_paper_primitivespec_generation_coverage_summary_is_exact():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_primitivespec_generation_contract"
    ]
    assert payload["coverage_summary"] == {
        "primitive_spec_generation_requirement_row_count": 6,
        "native_family_primitivespec_template_row_count": 3,
        "blocked_primitivespec_generation_requirement_row_count": 2,
        "noop_primitivespec_generation_requirement_row_count": 1,
        "current_row_primitivespec_generation_row_count": 16,
        "current_primitivespec_generation_pass_record_count": 0,
        "primitive_spec_generation_candidate_record_count": 0,
        "offline_primitivespec_template_record_count": 3,
        "generated_primitive_spec_record_count": 0,
        "generated_collision_package_record_count": 0,
        "runtime_admissibility_check_record_count": 0,
        "current_primitivespec_generation_noop_record_count": 16,
        "current_paper_primitive_distribution": {"trapezoidal_prism": 16},
        "current_mapping_label_distribution": {"offline_only_unmapped": 16},
    }
```

- [ ] **Step 11: Add report-only false-flag RED test**

Add:

```python
def test_cpd_paper_primitivespec_generation_stays_report_only():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_primitivespec_generation_contract"
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
    for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
        assert payload[flag] is False
    rows = (
        payload["native_family_primitivespec_template_rows"]
        + payload["blocked_primitivespec_generation_requirement_rows"]
        + payload["noop_primitivespec_generation_requirement_rows"]
        + payload["current_row_primitivespec_generation_rows"]
    )
    for row in rows:
        assert forbidden_keys.isdisjoint(row)
        for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
            assert row[flag] is False
```

- [ ] **Step 12: Add malformed-input rejection RED tests**

Add:

```python
def test_cpd_paper_primitivespec_generation_rejects_wrong_input_gate():
    preflight = _generation_contract_preflight_input()
    preflight["gate_id"] = "stale_gate"

    with pytest.raises(
        ValueError,
        match="primitivespec_generation_input_gate_id_mismatch",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_stale_input_next_gate():
    preflight = _generation_contract_preflight_input()
    preflight["next_required_gate"] = "stale_gate"

    with pytest.raises(
        ValueError,
        match="primitivespec_generation_input_next_gate_mismatch",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_true_input_trigger_flags():
    preflight = _generation_contract_preflight_input()
    preflight["real_usd_loaded"] = True

    with pytest.raises(
        ValueError,
        match="primitivespec_generation_input_trigger_flag_true:real_usd_loaded",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


@pytest.mark.parametrize(
    ("field_name", "error_label"),
    [
        (
            "generation_preflight_candidate_count",
            "primitivespec_generation_input_candidate_count_nonzero",
        ),
        (
            "generated_primitive_spec_count",
            "primitivespec_generation_input_generated_spec_nonzero",
        ),
        (
            "generated_collision_package_count",
            "primitivespec_generation_input_generated_collision_package_nonzero",
        ),
        (
            "runtime_admissibility_check_count",
            "primitivespec_generation_input_runtime_admissibility_nonzero",
        ),
    ],
)
def test_cpd_paper_primitivespec_generation_rejects_nonzero_counts(
    field_name,
    error_label,
):
    preflight = _generation_contract_preflight_input()
    preflight[field_name] = 1

    with pytest.raises(ValueError, match=error_label):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_input_contract_drift():
    preflight = _generation_contract_preflight_input()
    contract = dict(preflight["primitive_spec_generation_preflight_contract"])
    contract["expected_current_row_count"] = 15
    preflight["primitive_spec_generation_preflight_contract"] = contract

    with pytest.raises(
        ValueError,
        match=(
            "primitivespec_generation_input_contract_mismatch:"
            "expected_current_row_count"
        ),
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_coverage_mismatch():
    preflight = _generation_contract_preflight_input()
    coverage = dict(preflight["coverage_summary"])
    coverage["current_row_primitivespec_generation_preflight_row_count"] = 15
    preflight["coverage_summary"] = coverage

    with pytest.raises(
        ValueError,
        match=(
            "primitivespec_generation_coverage_count_mismatch:"
            "current_row_primitivespec_generation_preflight_row_count"
        ),
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_family_order_mismatch():
    preflight = _generation_contract_preflight_input()
    rows = [
        dict(row)
        for row in preflight[
            "primitive_spec_generation_preflight_requirement_rows"
        ]
    ]
    rows[0]["paper_primitive"] = "sphere"
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match="primitivespec_generation_family_primitive_sequence_mismatch",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)
```

- [ ] **Step 13: Add row semantic rejection RED tests**

Add:

```python
def test_cpd_paper_primitivespec_generation_rejects_future_family_contract_drift():
    preflight = _generation_contract_preflight_input()
    rows = [
        dict(row)
        for row in preflight[
            "primitive_spec_generation_preflight_requirement_rows"
        ]
    ]
    rows[0]["candidate_mapping_label"] = "sphere"
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(
            "primitivespec_generation_future_family_contract_mismatch:"
            "oriented_bounding_box"
        ),
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_blocked_family_contract_drift():
    preflight = _generation_contract_preflight_input()
    rows = [
        dict(row)
        for row in preflight[
            "primitive_spec_generation_preflight_requirement_rows"
        ]
    ]
    capped_cylinder = next(
        row for row in rows if row["paper_primitive"] == "capped_cylinder"
    )
    capped_cylinder["primitive_spec_generation_preflight_decision"] = (
        "future_native_family_generation_requirement_preflighted"
    )
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match="primitivespec_generation_family_contract_mismatch:capped_cylinder",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_missing_family_source_id():
    preflight = _generation_contract_preflight_input()
    rows = [
        dict(row)
        for row in preflight[
            "primitive_spec_generation_preflight_requirement_rows"
        ]
    ]
    rows[0]["source_conversion_plan_row_id"] = ""
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(
            "primitivespec_generation_missing_preflight_row_id:"
            "source_conversion_plan_row_id"
        ),
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_unknown_family_decision():
    preflight = _generation_contract_preflight_input()
    rows = [
        dict(row)
        for row in preflight[
            "primitive_spec_generation_preflight_requirement_rows"
        ]
    ]
    rows[0]["primitive_spec_generation_preflight_decision"] = "misspelled"
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match="unknown_primitivespec_generation_preflight_family_decision:misspelled",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_unknown_current_decision():
    preflight = _generation_contract_preflight_input()
    rows = [
        dict(row)
        for row in preflight["current_row_primitivespec_generation_preflight_rows"]
    ]
    rows[0]["primitive_spec_generation_preflight_decision"] = "misspelled"
    preflight["current_row_primitivespec_generation_preflight_rows"] = rows

    with pytest.raises(
        ValueError,
        match="unknown_primitivespec_generation_preflight_current_decision:misspelled",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)
```

- [ ] **Step 14: Add leak and duplicate rejection RED tests**

Add:

```python
@pytest.mark.parametrize(
    ("field_name", "field_value", "error_label"),
    [
        (
            "generation_preflight_candidate",
            True,
            "primitivespec_generation_template_runtime_leak:"
            "generation_preflight_candidate",
        ),
        (
            "generated_primitive_spec",
            {"kind": "box"},
            "primitivespec_generation_template_runtime_leak:"
            "generated_primitive_spec",
        ),
    ],
)
def test_cpd_paper_primitivespec_generation_rejects_native_template_runtime_leaks(
    field_name,
    field_value,
    error_label,
):
    preflight = _generation_contract_preflight_input()
    rows = [
        dict(row)
        for row in preflight[
            "primitive_spec_generation_preflight_requirement_rows"
        ]
    ]
    rows[0][field_name] = field_value
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_current_source_id_gap():
    preflight = _generation_contract_preflight_input()
    rows = [
        dict(row)
        for row in preflight["current_row_primitivespec_generation_preflight_rows"]
    ]
    rows[0]["source_output_id"] = ""
    preflight["current_row_primitivespec_generation_preflight_rows"] = rows

    with pytest.raises(
        ValueError,
        match="primitivespec_generation_missing_current_row_source_id:source_output_id",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_template_candidate_source_gate_mismatch():
    preflight = _generation_contract_preflight_input()
    rows = [
        dict(row)
        for row in preflight[
            "primitive_spec_generation_preflight_requirement_rows"
        ]
    ]
    rows[0]["required_later_gate"] = "stale_gate"
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(
            "primitivespec_generation_template_required_current_candidate_"
            "source_gate_mismatch"
        ),
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_requirement_required_later_gate_mismatch():
    preflight = _generation_contract_preflight_input()
    rows = [
        dict(row)
        for row in preflight[
            "primitive_spec_generation_preflight_requirement_rows"
        ]
    ]
    capped_cylinder = next(
        row for row in rows if row["paper_primitive"] == "capped_cylinder"
    )
    capped_cylinder["required_later_gate"] = "stale_gate"
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match="primitivespec_generation_requirement_required_later_gate_mismatch",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


@pytest.mark.parametrize(
    ("field_name", "field_value", "error_label"),
    [
        (
            "primitive_spec_generation_candidate",
            True,
            "primitivespec_generation_current_row_candidate_nonzero",
        ),
        (
            "generated_primitive_spec",
            {"kind": "box"},
            "primitivespec_generation_current_row_generated_spec_nonzero",
        ),
        (
            "silent_drop_detected",
            True,
            "primitivespec_generation_current_row_silent_drop_detected",
        ),
    ],
)
def test_cpd_paper_primitivespec_generation_rejects_current_row_generation_leaks(
    field_name,
    field_value,
    error_label,
):
    preflight = _generation_contract_preflight_input()
    rows = [
        dict(row)
        for row in preflight["current_row_primitivespec_generation_preflight_rows"]
    ]
    rows[0][field_name] = field_value
    preflight["current_row_primitivespec_generation_preflight_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_current_row_gate_mismatch():
    preflight = _generation_contract_preflight_input()
    rows = [
        dict(row)
        for row in preflight["current_row_primitivespec_generation_preflight_rows"]
    ]
    rows[0]["required_later_gate"] = "stale_gate"
    preflight["current_row_primitivespec_generation_preflight_rows"] = rows

    with pytest.raises(
        ValueError,
        match="primitivespec_generation_current_row_required_later_gate_mismatch",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_duplicate_emitted_row_ids():
    rows = [
        {"primitive_spec_generation_row_id": "duplicate"},
        {"primitive_spec_generation_row_id": "duplicate"},
    ]

    with pytest.raises(
        ValueError,
        match="duplicate_primitivespec_generation_row_id",
    ):
        _paper_require_unique_generation_row_ids(rows)
```

- [ ] **Step 15: Run RED offline tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k 'primitivespec_generation and not primitivespec_generation_preflight' -q
```

Expected before implementation: FAIL with import errors for
`_paper_mapped_subset_primitivespec_generation_contract_payload` and
`_paper_require_unique_generation_row_ids`, or with missing
`paper_mapped_subset_primitivespec_generation_contract` if imports are stubbed first.

- [ ] **Step 16: Commit RED tests**

Run:

```bash
git add tests/test_cpd_paper_offline.py
git commit -m "test: add CPD PrimitiveSpec generation contract coverage"
```

## Task 2: Add RED CLI Tests

**Files:**
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Update top-level CLI assertions**

In the CPD paper offline CLI test, update every existing top-level exact assertion that currently
expects `paper_mapped_subset_primitivespec_generation_contract` as the report-level missing gate.
This includes the top-level `missing_before_paper_faithful_offline`, `failure_labels`,
`next_required_gate`, and `implemented_output_contract_scope` assertions.

Use:

```python
assert (
    payload["next_required_gate"]
    == "paper_mapped_subset_primitivespec_candidate_source_contract"
)
assert payload["failure_labels"] == [
    "paper_mapped_subset_primitivespec_candidate_source_contract_missing",
]
assert (
    "paper_mapped_subset_primitivespec_generation_contract"
    in payload["paper_faithfulness"]["implemented_output_contract_scope"]
)
assert (
    payload["paper_faithfulness"]["missing_before_paper_faithful_offline"]
    == ["paper_mapped_subset_primitivespec_candidate_source_contract"]
)
```

The nested generation-preflight payload must keep this assertion:

```python
assert (
    payload["paper_mapped_subset_primitivespec_generation_preflight_contract"][
        "next_required_gate"
    ]
    == "paper_mapped_subset_primitivespec_generation_contract"
)
```

- [ ] **Step 2: Add generation payload CLI assertions**

Add this block after the existing generation-preflight CLI assertions:

```python
generation = payload["paper_mapped_subset_primitivespec_generation_contract"]
assert (
    generation["gate_id"]
    == "paper_mapped_subset_primitivespec_generation_contract"
)
assert (
    generation["input_gate_id"]
    == "paper_mapped_subset_primitivespec_generation_preflight_contract"
)
assert (
    generation["next_required_gate"]
    == "paper_mapped_subset_primitivespec_candidate_source_contract"
)
assert generation["primitive_spec_generation_candidate_count"] == 0
assert generation["offline_primitivespec_template_count"] == 3
assert generation["generated_primitive_spec_count"] == 0
assert generation["generated_collision_package_count"] == 0
assert generation["runtime_admissibility_check_count"] == 0
assert len(generation["native_family_primitivespec_template_rows"]) == 3
assert len(generation["blocked_primitivespec_generation_requirement_rows"]) == 2
assert len(generation["noop_primitivespec_generation_requirement_rows"]) == 1
assert len(generation["current_row_primitivespec_generation_rows"]) == 16
assert generation["coverage_summary"][
    "primitive_spec_generation_requirement_row_count"
] == 6
assert generation["coverage_summary"][
    "current_row_primitivespec_generation_row_count"
] == 16
assert generation["coverage_summary"][
    "primitive_spec_generation_candidate_record_count"
] == 0
assert generation["coverage_summary"][
    "offline_primitivespec_template_record_count"
] == 3
assert generation["primitive_spec_generated"] is False
assert generation["collision_package_generated"] is False
assert generation["runtime_admissibility_checked"] is False
assert generation["newton_support_claimed"] is False
assert generation["package_generation_triggered"] is False
assert generation["newton_runtime_triggered"] is False
assert generation["real_usd_triggered"] is False
assert generation["benchmark_triggered"] is False
assert payload["collision_quality_measured"] is False
assert payload["deployment_or_certification_claimed"] is False
```

- [ ] **Step 3: Run RED CLI tests**

Run:

```bash
python -m pytest tests/test_cli.py -k cpd_paper_offline -q
```

Expected before implementation: FAIL because the CLI JSON lacks
`paper_mapped_subset_primitivespec_generation_contract` and still points the top-level next gate to
`paper_mapped_subset_primitivespec_generation_contract`.

- [ ] **Step 4: Commit RED CLI tests**

Run:

```bash
git add tests/test_cli.py
git commit -m "test: add CPD PrimitiveSpec generation CLI assertions"
```

## Task 3: Implement Generation Contract Payload

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add candidate-source gate constant and remaining-gap helper**

Add after `_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT`:

```python
_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT = (
    "paper_mapped_subset_primitivespec_candidate_source_contract"
)
```

Add after `_paper_remaining_gaps_after_mapped_subset_primitivespec_generation_preflight()`:

```python
def _paper_remaining_gaps_after_mapped_subset_primitivespec_generation() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT]
```

- [ ] **Step 2: Add generation-contract false flags and expected input contract**

Add after `_paper_mapped_subset_primitivespec_generation_preflight_contract_payload()`:

```python
def _paper_false_primitivespec_generation_flags() -> dict[str, bool]:
    return {
        flag: False
        for flag in _PRIMITIVESPEC_VALIDATION_ROW_FALSE_FLAGS
    }


def _paper_expected_primitivespec_generation_preflight_contract() -> dict[str, object]:
    return {
        "validation_input_gate_required": (
            _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT
        ),
        "unique_row_ids_required": True,
        "complete_source_evidence_ids_required": True,
        "zero_current_generation_candidates_required": True,
        "zero_generated_primitivespecs_required": True,
        "zero_runtime_admissibility_checks_required": True,
        "allowed_future_mapping_candidate_labels": list(
            _PRIMITIVESPEC_VALIDATION_ALLOWED_FUTURE_KINDS
        ),
        "required_primitive_spec_fields": list(
            _PRIMITIVESPEC_DRY_RUN_REQUIRED_FIELDS
        ),
        "expected_requirement_row_count": 6,
        "expected_current_row_count": 16,
        "primitive_spec_generation_allowed": False,
        "collision_package_generation_allowed": False,
        "newton_runtime_allowed": False,
        "runtime_admissibility_supported": False,
        "approximation_policy_enabled": False,
        "silent_drop_allowed": False,
    }
```

- [ ] **Step 3: Add input validators**

Add:

```python
def _paper_validate_primitivespec_generation_false_flags(
    row: dict[str, object],
) -> None:
    for flag in _PRIMITIVESPEC_VALIDATION_ROW_FALSE_FLAGS:
        if bool(row.get(flag)):
            raise ValueError(
                f"primitivespec_generation_input_trigger_flag_true:{flag}"
            )


def _paper_validate_primitivespec_generation_preflight_contract(
    preflight: dict[str, object],
) -> None:
    contract = preflight["primitive_spec_generation_preflight_contract"]
    expected_contract = _paper_expected_primitivespec_generation_preflight_contract()
    for field_name, expected_value in expected_contract.items():
        if contract[field_name] != expected_value:
            raise ValueError(
                f"primitivespec_generation_input_contract_mismatch:{field_name}"
            )


def _paper_validate_primitivespec_generation_input(
    preflight: dict[str, object],
) -> None:
    if (
        preflight.get("gate_id")
        != _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
    ):
        raise ValueError("primitivespec_generation_input_gate_id_mismatch")
    if (
        preflight.get("next_required_gate")
        != _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
    ):
        raise ValueError("primitivespec_generation_input_next_gate_mismatch")

    _paper_validate_primitivespec_generation_false_flags(preflight)
    if preflight["generation_preflight_candidate_count"] != 0:
        raise ValueError("primitivespec_generation_input_candidate_count_nonzero")
    if preflight["generated_primitive_spec_count"] != 0:
        raise ValueError("primitivespec_generation_input_generated_spec_nonzero")
    if preflight["generated_collision_package_count"] != 0:
        raise ValueError(
            "primitivespec_generation_input_generated_collision_package_nonzero"
        )
    if preflight["runtime_admissibility_check_count"] != 0:
        raise ValueError("primitivespec_generation_input_runtime_admissibility_nonzero")

    _paper_validate_primitivespec_generation_preflight_contract(preflight)
```

- [ ] **Step 4: Add coverage and family/current validation**

Add to the validator from Step 3, after contract validation:

```python
    requirement_rows = preflight[
        "primitive_spec_generation_preflight_requirement_rows"
    ]
    current_rows = preflight["current_row_primitivespec_generation_preflight_rows"]
    coverage = preflight["coverage_summary"]
    expected_coverage = {
        "primitive_spec_generation_preflight_requirement_row_count": 6,
        "future_native_primitivespec_generation_preflight_count": 3,
        "blocked_primitivespec_generation_preflight_requirement_count": 2,
        "noop_primitivespec_generation_preflight_requirement_count": 1,
        "current_row_primitivespec_generation_preflight_row_count": 16,
        "current_primitivespec_generation_preflight_pass_record_count": 0,
        "current_primitivespec_generation_preflight_noop_record_count": 16,
        "generation_preflight_candidate_record_count": 0,
        "generated_primitive_spec_record_count": 0,
    }
    for field_name, expected_value in expected_coverage.items():
        if coverage[field_name] != expected_value:
            raise ValueError(
                f"primitivespec_generation_coverage_count_mismatch:{field_name}"
            )
    if len(requirement_rows) != 6 or len(current_rows) != 16:
        raise ValueError("primitivespec_generation_coverage_count_mismatch:row_count")
    if [
        row["paper_primitive"] for row in requirement_rows
    ] != _PRIMITIVESPEC_VALIDATION_EXPECTED_FAMILY_ORDER:
        raise ValueError("primitivespec_generation_family_primitive_sequence_mismatch")

    for requirement_row in requirement_rows:
        _paper_validate_primitivespec_generation_requirement_input(requirement_row)
    for current_row in current_rows:
        _paper_validate_primitivespec_generation_current_input(current_row)
```

Add the called helpers:

```python
def _paper_validate_primitivespec_generation_requirement_input(
    requirement_row: dict[str, object],
) -> None:
    for field_name in (
        "primitive_spec_generation_preflight_row_id",
        "source_primitivespec_validation_row_id",
        "source_primitivespec_dry_run_row_id",
        "source_adapter_preflight_row_id",
        "source_candidate_matrix_row_id",
        "source_conversion_plan_row_id",
    ):
        _paper_require_nonempty_source_id(
            requirement_row,
            field_name,
            "primitivespec_generation_missing_preflight_row_id",
        )
    _paper_validate_primitivespec_generation_false_flags(requirement_row)
    decision = str(requirement_row["primitive_spec_generation_preflight_decision"])
    known_decisions = {
        "future_native_family_generation_requirement_preflighted",
        "blocked_approximation_policy_generation_preflight_recorded",
        "noop_unmapped_family_generation_preflight_recorded",
    }
    if decision not in known_decisions:
        raise ValueError(
            f"unknown_primitivespec_generation_preflight_family_decision:"
            f"{decision}"
        )
    if bool(requirement_row["generation_preflight_candidate"]):
        raise ValueError(
            "primitivespec_generation_template_runtime_leak:"
            "generation_preflight_candidate"
        )
    if requirement_row.get("generated_primitive_spec") is not None:
        raise ValueError(
            "primitivespec_generation_template_runtime_leak:"
            "generated_primitive_spec"
        )

    paper_primitive = str(requirement_row["paper_primitive"])
    if paper_primitive in {"oriented_bounding_box", "sphere", "capsule"}:
        expected_mapping = {
            "oriented_bounding_box": "box",
            "sphere": "sphere",
            "capsule": "capsule",
        }[paper_primitive]
        if (
            requirement_row["required_later_gate"]
            != _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
        ):
            raise ValueError(
                "primitivespec_generation_template_required_current_candidate_"
                "source_gate_mismatch"
            )
        if decision != "future_native_family_generation_requirement_preflighted":
            raise ValueError(
                f"primitivespec_generation_future_family_contract_mismatch:"
                f"{paper_primitive}"
            )
        if requirement_row["candidate_mapping_label"] != expected_mapping:
            raise ValueError(
                f"primitivespec_generation_future_family_contract_mismatch:"
                f"{paper_primitive}"
            )
        return
    if paper_primitive in {"capped_cylinder", "frustum"}:
        if (
            requirement_row["required_later_gate"]
            != _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
        ):
            raise ValueError(
                "primitivespec_generation_requirement_required_later_gate_mismatch"
            )
        if (
            decision
            != "blocked_approximation_policy_generation_preflight_recorded"
        ):
            raise ValueError(
                f"primitivespec_generation_family_contract_mismatch:{paper_primitive}"
            )
        if requirement_row["candidate_mapping_label"] != "offline_only_unmapped":
            raise ValueError(
                f"primitivespec_generation_family_contract_mismatch:{paper_primitive}"
            )
        return
    if paper_primitive == "trapezoidal_prism":
        if (
            requirement_row["required_later_gate"]
            != _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
        ):
            raise ValueError(
                "primitivespec_generation_requirement_required_later_gate_mismatch"
            )
        if decision != "noop_unmapped_family_generation_preflight_recorded":
            raise ValueError(
                f"primitivespec_generation_family_contract_mismatch:{paper_primitive}"
            )
        if requirement_row["candidate_mapping_label"] != "offline_only_unmapped":
            raise ValueError(
                f"primitivespec_generation_family_contract_mismatch:{paper_primitive}"
            )
        return
    raise ValueError(
        f"unknown_primitivespec_generation_preflight_family_decision:{decision}"
    )


def _paper_validate_primitivespec_generation_current_input(
    current_row: dict[str, object],
) -> None:
    for field_name in (
        "primitive_spec_generation_preflight_row_id",
        "source_primitivespec_validation_row_id",
        "source_primitivespec_dry_run_row_id",
        "source_adapter_preflight_row_id",
        "source_candidate_matrix_row_id",
        "source_conversion_plan_row_id",
        "source_policy_decision_id",
        "source_adapter_decision_id",
        "source_output_id",
        "evidence_case_id",
        "offline_primitive_id",
    ):
        _paper_require_nonempty_source_id(
            current_row,
            field_name,
            "primitivespec_generation_missing_current_row_source_id",
        )
    _paper_validate_primitivespec_generation_false_flags(current_row)
    decision = str(current_row["primitive_spec_generation_preflight_decision"])
    if decision != "skip_unmapped_current_row_preflighted":
        raise ValueError(
            f"unknown_primitivespec_generation_preflight_current_decision:"
            f"{decision}"
        )
    if bool(current_row["primitive_spec_generation_candidate"]):
        raise ValueError("primitivespec_generation_current_row_candidate_nonzero")
    if current_row["generated_primitive_spec"] is not None:
        raise ValueError("primitivespec_generation_current_row_generated_spec_nonzero")
    if bool(current_row["silent_drop_detected"]):
        raise ValueError("primitivespec_generation_current_row_silent_drop_detected")
    if (
        current_row["required_later_gate"]
        != _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
    ):
        raise ValueError(
            "primitivespec_generation_current_row_required_later_gate_mismatch"
        )
```

- [ ] **Step 5: Add row builders**

Add:

```python
def _paper_primitivespec_generation_native_template_row(
    requirement_row: dict[str, object],
) -> dict[str, object]:
    return {
        "primitive_spec_generation_template_row_id": (
            f"{requirement_row['primitive_spec_generation_preflight_row_id']}:"
            "primitivespec_generation_template"
        ),
        "source_primitivespec_generation_preflight_row_id": requirement_row[
            "primitive_spec_generation_preflight_row_id"
        ],
        "source_primitivespec_validation_row_id": requirement_row[
            "source_primitivespec_validation_row_id"
        ],
        "source_primitivespec_dry_run_row_id": requirement_row[
            "source_primitivespec_dry_run_row_id"
        ],
        "source_adapter_preflight_row_id": requirement_row[
            "source_adapter_preflight_row_id"
        ],
        "source_candidate_matrix_row_id": requirement_row[
            "source_candidate_matrix_row_id"
        ],
        "source_conversion_plan_row_id": requirement_row[
            "source_conversion_plan_row_id"
        ],
        "paper_primitive": requirement_row["paper_primitive"],
        "primitive_spec_kind": requirement_row["candidate_mapping_label"],
        "candidate_mapping_label": requirement_row["candidate_mapping_label"],
        "input_primitivespec_generation_preflight_decision": requirement_row[
            "primitive_spec_generation_preflight_decision"
        ],
        "required_primitive_spec_fields": list(
            requirement_row["required_primitive_spec_fields"]
        ),
        "template_only": True,
        "runtime_instance_generated": False,
        "primitive_spec_generation_candidate": False,
        "generated_primitive_spec": None,
        "silent_drop_detected": False,
        "primitive_spec_generation_decision": (
            "native_family_primitivespec_template_generated_offline_only"
        ),
        "required_current_candidate_source_gate": (
            _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
        ),
        **_paper_false_primitivespec_generation_flags(),
    }


def _paper_primitivespec_generation_requirement_row(
    requirement_row: dict[str, object],
) -> dict[str, object]:
    paper_primitive = str(requirement_row["paper_primitive"])
    if paper_primitive in {"capped_cylinder", "frustum"}:
        decision = "blocked_approximation_policy_before_primitivespec_generation"
        action = "require_explicit_approximation_policy"
        future_policy = "approximation_policy"
    elif paper_primitive == "trapezoidal_prism":
        decision = "noop_unmapped_family_before_primitivespec_generation"
        action = "keep_unmapped_family_offline"
        future_policy = "mapped_current_candidate_source"
    else:
        raise ValueError(
            "unknown_primitivespec_generation_preflight_family_decision:"
            f"{requirement_row['primitive_spec_generation_preflight_decision']}"
        )
    return {
        "primitive_spec_generation_requirement_row_id": (
            f"{requirement_row['primitive_spec_generation_preflight_row_id']}:"
            "primitivespec_generation_requirement"
        ),
        "source_primitivespec_generation_preflight_row_id": requirement_row[
            "primitive_spec_generation_preflight_row_id"
        ],
        "source_primitivespec_validation_row_id": requirement_row[
            "source_primitivespec_validation_row_id"
        ],
        "source_primitivespec_dry_run_row_id": requirement_row[
            "source_primitivespec_dry_run_row_id"
        ],
        "source_adapter_preflight_row_id": requirement_row[
            "source_adapter_preflight_row_id"
        ],
        "source_candidate_matrix_row_id": requirement_row[
            "source_candidate_matrix_row_id"
        ],
        "source_conversion_plan_row_id": requirement_row[
            "source_conversion_plan_row_id"
        ],
        "paper_primitive": requirement_row["paper_primitive"],
        "candidate_mapping_label": requirement_row["candidate_mapping_label"],
        "input_primitivespec_generation_preflight_decision": requirement_row[
            "primitive_spec_generation_preflight_decision"
        ],
        "primitive_spec_generation_decision": decision,
        "primitive_spec_generation_action": action,
        "primitive_spec_generation_candidate": False,
        "generated_primitive_spec": None,
        "required_later_gate": (
            _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
        ),
        "required_future_policy": future_policy,
        **_paper_false_primitivespec_generation_flags(),
    }


def _paper_primitivespec_generation_current_row(
    current_row: dict[str, object],
) -> dict[str, object]:
    return {
        "primitive_spec_generation_row_id": (
            f"{current_row['primitive_spec_generation_preflight_row_id']}:"
            "primitivespec_generation"
        ),
        "source_primitivespec_generation_preflight_row_id": current_row[
            "primitive_spec_generation_preflight_row_id"
        ],
        "source_primitivespec_validation_row_id": current_row[
            "source_primitivespec_validation_row_id"
        ],
        "source_primitivespec_dry_run_row_id": current_row[
            "source_primitivespec_dry_run_row_id"
        ],
        "source_adapter_preflight_row_id": current_row[
            "source_adapter_preflight_row_id"
        ],
        "source_candidate_matrix_row_id": current_row[
            "source_candidate_matrix_row_id"
        ],
        "source_conversion_plan_row_id": current_row[
            "source_conversion_plan_row_id"
        ],
        "source_policy_decision_id": current_row["source_policy_decision_id"],
        "source_adapter_decision_id": current_row["source_adapter_decision_id"],
        "source_output_id": current_row["source_output_id"],
        "evidence_case_id": current_row["evidence_case_id"],
        "offline_primitive_id": current_row["offline_primitive_id"],
        "paper_primitive": current_row["paper_primitive"],
        "offline_mapping_label": current_row["offline_mapping_label"],
        "primitive_spec_generation_decision": (
            "skip_unmapped_current_row_no_primitivespec_generated"
        ),
        "primitive_spec_generation_action": (
            "keep_offline_until_mapped_current_candidate_exists"
        ),
        "primitive_spec_generation_candidate": False,
        "generated_primitive_spec": None,
        "silent_drop_detected": False,
        "required_later_gate": (
            _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
        ),
        "required_future_policy": "mapped_current_candidate_source",
        **_paper_false_primitivespec_generation_flags(),
    }
```

- [ ] **Step 6: Add unique-id helper and payload builder**

Add:

```python
def _paper_require_unique_generation_row_ids(
    rows: list[dict[str, object]],
) -> None:
    row_ids: list[str] = []
    for row in rows:
        for field_name in (
            "primitive_spec_generation_template_row_id",
            "primitive_spec_generation_requirement_row_id",
            "primitive_spec_generation_row_id",
        ):
            if field_name in row:
                row_ids.append(str(row[field_name]))
                break
    if len(row_ids) != len(set(row_ids)):
        raise ValueError("duplicate_primitivespec_generation_row_id")
```

Add the payload builder:

```python
def _paper_mapped_subset_primitivespec_generation_contract_payload(
    preflight: dict[str, object],
) -> dict[str, object]:
    _paper_validate_primitivespec_generation_input(preflight)
    requirement_rows = preflight[
        "primitive_spec_generation_preflight_requirement_rows"
    ]
    current_input_rows = preflight[
        "current_row_primitivespec_generation_preflight_rows"
    ]
    native_template_rows = [
        _paper_primitivespec_generation_native_template_row(row)
        for row in requirement_rows
        if row["primitive_spec_generation_preflight_decision"]
        == "future_native_family_generation_requirement_preflighted"
    ]
    blocked_rows = [
        _paper_primitivespec_generation_requirement_row(row)
        for row in requirement_rows
        if row["primitive_spec_generation_preflight_decision"]
        == "blocked_approximation_policy_generation_preflight_recorded"
    ]
    noop_rows = [
        _paper_primitivespec_generation_requirement_row(row)
        for row in requirement_rows
        if row["primitive_spec_generation_preflight_decision"]
        == "noop_unmapped_family_generation_preflight_recorded"
    ]
    current_rows = [
        _paper_primitivespec_generation_current_row(row)
        for row in current_input_rows
    ]
    _paper_require_unique_generation_row_ids(
        native_template_rows + blocked_rows + noop_rows + current_rows
    )

    candidate_count = sum(
        bool(row["primitive_spec_generation_candidate"])
        for row in current_rows
    )
    current_noop_count = sum(
        row["primitive_spec_generation_decision"]
        == "skip_unmapped_current_row_no_primitivespec_generated"
        for row in current_rows
    )
    remaining_gaps = _paper_remaining_gaps_after_mapped_subset_primitivespec_generation()
    return {
        "gate_id": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT,
        "gate_status": (
            "implemented_offline_primitivespec_generation_contract_only_partial"
        ),
        "closed_gate": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT,
        "input_gate_id": (
            _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
        ),
        "next_required_gate": (
            _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
        ),
        "decision": "remain_partial",
        "decision_reason": (
            "primitivespec_generation_contract_complete_"
            "mapped_current_candidate_source_contract_missing"
        ),
        "paper_faithful_offline_allowed": False,
        "package_generation_allowed": False,
        "artifact_kind": (
            "offline_primitivespec_generation_contract_template_rows_"
            "not_runtime_primitivespec_not_collision_package"
        ),
        "schema_version": 1,
        "source_scope": "synthetic_toy_fixtures_only",
        "implementation_boundary": (
            "offline_primitivespec_generation_templates_only_no_runtime_"
            "primitivespec_no_collision_package_no_newton"
        ),
        "primitive_spec_generation_action": (
            "emit_offline_templates_and_keep_current_rows_offline"
        ),
        "primitive_spec_generation_candidate_count": candidate_count,
        "offline_primitivespec_template_count": len(native_template_rows),
        "generated_primitive_spec_count": 0,
        "generated_collision_package_count": 0,
        "runtime_admissibility_check_count": 0,
        "input_contract_summary": {
            "input_gate_id": preflight["gate_id"],
            "input_artifact_kind": preflight["artifact_kind"],
            "primitive_spec_generation_preflight_requirement_row_count": (
                preflight["coverage_summary"][
                    "primitive_spec_generation_preflight_requirement_row_count"
                ]
            ),
            "current_row_primitivespec_generation_preflight_row_count": (
                preflight["coverage_summary"][
                    "current_row_primitivespec_generation_preflight_row_count"
                ]
            ),
            "generation_preflight_candidate_record_count": (
                preflight["coverage_summary"][
                    "generation_preflight_candidate_record_count"
                ]
            ),
            "generated_primitive_spec_record_count": (
                preflight["coverage_summary"][
                    "generated_primitive_spec_record_count"
                ]
            ),
        },
        "primitive_spec_generation_contract": {
            "input_gate_required": (
                _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
            ),
            "current_candidate_source_gate_required": (
                _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
            ),
            "template_only_native_families": ["box", "sphere", "capsule"],
            "zero_runtime_primitivespecs_required": True,
            "zero_collision_packages_required": True,
            "zero_runtime_admissibility_checks_required": True,
            "runtime_primitive_spec_generation_allowed": False,
            "collision_package_generation_allowed": False,
            "newton_runtime_allowed": False,
            "approximation_policy_enabled": False,
            "silent_drop_allowed": False,
        },
        "native_family_primitivespec_template_rows": native_template_rows,
        "blocked_primitivespec_generation_requirement_rows": blocked_rows,
        "noop_primitivespec_generation_requirement_rows": noop_rows,
        "current_row_primitivespec_generation_rows": current_rows,
        "coverage_summary": {
            "primitive_spec_generation_requirement_row_count": len(requirement_rows),
            "native_family_primitivespec_template_row_count": len(
                native_template_rows
            ),
            "blocked_primitivespec_generation_requirement_row_count": len(
                blocked_rows
            ),
            "noop_primitivespec_generation_requirement_row_count": len(noop_rows),
            "current_row_primitivespec_generation_row_count": len(current_rows),
            "current_primitivespec_generation_pass_record_count": 0,
            "primitive_spec_generation_candidate_record_count": candidate_count,
            "offline_primitivespec_template_record_count": len(
                native_template_rows
            ),
            "generated_primitive_spec_record_count": 0,
            "generated_collision_package_record_count": 0,
            "runtime_admissibility_check_record_count": 0,
            "current_primitivespec_generation_noop_record_count": (
                current_noop_count
            ),
            "current_paper_primitive_distribution": _paper_policy_distribution(
                current_rows,
                "paper_primitive",
            ),
            "current_mapping_label_distribution": _paper_policy_distribution(
                current_rows,
                "offline_mapping_label",
            ),
        },
        "remaining_gaps": remaining_gaps,
        **_paper_false_primitivespec_generation_flags(),
    }
```

- [ ] **Step 7: Wire into report builder**

In `build_cpd_paper_offline_report()`, add after the preflight payload:

```python
    mapped_subset_primitivespec_generation = (
        _paper_mapped_subset_primitivespec_generation_contract_payload(
            mapped_subset_primitivespec_generation_preflight
        )
    )
```

Change:

```python
    missing_before_paper_faithful = (
        _paper_remaining_gaps_after_mapped_subset_primitivespec_generation_preflight()
    )
```

to:

```python
    missing_before_paper_faithful = (
        _paper_remaining_gaps_after_mapped_subset_primitivespec_generation()
    )
```

Change top-level `next_required_gate` to:

```python
        "next_required_gate": (
            _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
        ),
```

Add these top-level false evidence fields next to the existing package/Newton/real-USD/benchmark
trigger flags:

```python
        "collision_quality_measured": False,
        "deployment_or_certification_claimed": False,
```

Add `_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT` to
`implemented_output_contract_scope` after
`_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT`.

Add the payload to the returned dictionary:

```python
        "paper_mapped_subset_primitivespec_generation_contract": (
            mapped_subset_primitivespec_generation
        ),
```

- [ ] **Step 8: Run GREEN focused tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k 'primitivespec_generation or primitivespec_generation_preflight or offline_report_covers_first_toy_slice' -q
python -m pytest tests/test_cli.py -k cpd_paper_offline -q
```

Expected after implementation: PASS.

- [ ] **Step 9: Commit implementation**

Run:

```bash
git add src/primitive_collision_compiler/baselines/cpd_paper/offline.py
git commit -m "feat: add CPD PrimitiveSpec generation contract"
```

## Task 4: Update Documentation And Registry

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
- Create: `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-generation-contract.md`
- Modify: `experiments/registry.yaml`

- [ ] **Step 1: Update user-facing status wording**

Use this canonical wording in status documents:

```text
The CPD paper lane now has an offline PrimitiveSpec generation contract. It emits
reviewable native-family template rows for box, sphere, and capsule, and records
that all current rows remain no-generation rows until a mapped current candidate
source contract exists.
```

Use this boundary wording wherever a limitation is needed:

```text
This is not runtime PrimitiveSpec generation, not CollisionPackage generation,
not Newton admissibility, not real-USD evidence, not benchmark evidence, and not
a collision-quality result.
```

- [ ] **Step 2: Update `docs/reference/cpd-paper-story-status.md`**

Add a section under the mapped-subset package/PrimitiveSpec story:

```markdown
### PrimitiveSpec Generation Contract

Current status: offline/report-only contract implemented.

What changed:

- the paper lane now closes `paper_mapped_subset_primitivespec_generation_contract`;
- it emits mapped native-family template labels for box, sphere, and capsule;
- capped cylinder and frustum remain blocked behind an explicit approximation-policy gate;
- trapezoidal prism remains unmapped;
- all 16 current rows remain no-generation rows;
- the next required gate is
  `paper_mapped_subset_primitivespec_candidate_source_contract`.

Boundary: this does not create runtime PrimitiveSpec objects, CollisionPackages, Newton runtime
checks, Newton runtime/admissibility evidence, real-USD evidence, benchmark evidence, or
collision-quality evidence.
```

- [ ] **Step 3: Update gap matrix and offline-lane spec**

In `docs/reference/cpd-paper-reproduction-gap-matrix.md`, change the PrimitiveSpec generation row
from missing/preflight-only to implemented offline/report-only, with the next blocker as
`paper_mapped_subset_primitivespec_candidate_source_contract`.

In `docs/reference/cpd-paper-faithful-offline-lane-spec.md`, add the ordered lane step:

```markdown
1. `paper_mapped_subset_primitivespec_generation_contract`
   - status: implemented offline/report-only;
   - output: native-family template rows and current-row no-generation records;
   - next blocker: `paper_mapped_subset_primitivespec_candidate_source_contract`;
   - not allowed: runtime PrimitiveSpec, CollisionPackage, Newton runtime, real USD, benchmark,
     collision-quality, deployment, or safety claims.
```

Also replace stale current-gate wording in `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
so the document no longer says the current report is waiting on
`paper_mapped_subset_primitivespec_generation_contract`. The replacement sentence must be:

```markdown
Current gate status: `paper_mapped_subset_primitivespec_generation_contract` is closed as an
offline/report-only contract; the current next required gate is
`paper_mapped_subset_primitivespec_candidate_source_contract`.
```

- [ ] **Step 4: Update DeepDive evidence and claim boundaries**

In `docs/deepdive/evidence-status.md`, replace stale statements that say the current next gate is
`paper_mapped_subset_primitivespec_generation_contract` with:

```markdown
- Current next gate:
  `paper_mapped_subset_primitivespec_candidate_source_contract`.
```

Also add the new evidence line under CPD paper-lane evidence:

```markdown
- `paper_mapped_subset_primitivespec_generation_contract`: implemented as an offline/report-only
  contract with three native-family template rows and 16 current no-generation rows.
```

In `docs/reference/claim-boundaries.md`, replace stale statements that say the current next gate is
`paper_mapped_subset_primitivespec_generation_contract` with:

```markdown
The current paper-lane next gate is
`paper_mapped_subset_primitivespec_candidate_source_contract`, after the offline/report-only
PrimitiveSpec generation contract.
```

Add or keep these boundaries:

```markdown
- A PrimitiveSpec generation contract may be described as offline/report-only unless a record
  shows runtime PrimitiveSpec objects were emitted and reviewed.
- Do not describe the offline/report-only PrimitiveSpec generation contract as runtime
  PrimitiveSpec generation, CollisionPackage generation, Newton runtime support, Newton
  admissibility, real-USD evidence, benchmark evidence, collision-quality evidence, deployment
  evidence, or safety certification.
```

In `docs/deepdive/message-map.md`, keep any outward-facing wording aligned to:

```text
diagnostic checker
simulation-checked
offline/report-only PrimitiveSpec generation contract
```

- [ ] **Step 5: Create dated record**

Create `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-generation-contract.md`
with:

```markdown
# CPD Paper Mapped-Subset PrimitiveSpec Generation Contract

## Date

2026-05-17

## Status

Complete for an offline/report-only PrimitiveSpec generation contract. Not complete for runtime
PrimitiveSpec generation, CollisionPackage generation, Newton runtime support, real-USD evidence,
benchmark evidence, collision-quality evidence, deployment evidence, or safety certification.

## Summary

The CPD paper lane now closes
`paper_mapped_subset_primitivespec_generation_contract`. The report emits native-family template
rows for box, sphere, and capsule, blocked/no-op family rows for unsupported or unmapped paper
families, and 16 current-row no-generation records.

## Evidence

- Payload: `paper_mapped_subset_primitivespec_generation_contract`
- Native template rows: 3
- Blocked requirement rows: 2
- No-op requirement rows: 1
- Current no-generation rows: 16
- Runtime PrimitiveSpec records: 0
- CollisionPackage records: 0
- Runtime admissibility checks: 0
- Next required gate: `paper_mapped_subset_primitivespec_candidate_source_contract`

## Artifact Policy

No raw or generated 3D assets, large logs, videos, or run directories were committed. If ignored
raw paper intake had to be copied into the feature worktree for full-suite verification, it
remained ignored and uncommitted.

## Boundary

This record does not claim runtime PrimitiveSpec generation, CollisionPackage generation, Newton
runtime support, real-USD evidence, benchmark evidence, collision-quality evidence, deployment
evidence, or safety certification.

## Verification

```bash
python -m pytest tests/test_cpd_paper_offline.py -k 'primitivespec_generation or primitivespec_generation_preflight or offline_report_covers_first_toy_slice' -q
python -m pytest tests/test_cli.py -k cpd_paper_offline -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Record the actual result line after each command, for example:

```text
Result: 238 passed
Result: docs validation passed
Result: site claim validation passed
Result: no whitespace errors
```
```

- [ ] **Step 6: Update registry and record index**

Add the record path to `docs/records/README.md` in date order.

Add or update an experiment registry entry in `experiments/registry.yaml` with:

```yaml
- id: cpd-paper-mapped-subset-primitivespec-generation-contract
  status: complete
  command: PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report
  record: docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-generation-contract.md
  purpose: >
    Add a command-only offline mapped-subset PrimitiveSpec generation contract that emits
    template rows and no-generation current rows before any runtime PrimitiveSpec,
    CollisionPackage, runtime admissibility, package generation, or Newton runtime work.
  claims_supported:
    - partial command-only offline PrimitiveSpec generation contract for deterministic synthetic fixture records only
    - emits three mapped native-family template rows for box, sphere, and capsule
    - records two blocked approximation-policy rows and one no-op unmapped family row
    - records 16 current rows as no-generation rows until mapped current candidate sourcing exists
    - keeps generated PrimitiveSpecs, generated CollisionPackages, runtime-admissibility checks, Newton runtime, real-USD loading, benchmark runs, collision-quality measurement, and deployment/certification claims at zero or false
    - closes only paper_mapped_subset_primitivespec_generation_contract and advances the next gate to paper_mapped_subset_primitivespec_candidate_source_contract
    - no package-readiness claim, runtime PrimitiveSpec-generation claim, CollisionPackage-generation claim, Newton-support claim, runtime-admissibility claim, approximation-support claim, paper_faithful_offline claim, full CPD reproduction claim, package-generation claim, Newton runtime claim, real-USD claim, collision-quality claim, benchmark-suite claim, deployment claim, or safety-certification claim
```

- [ ] **Step 7: Run docs verification**

Run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all commands pass.

- [ ] **Step 8: Commit docs**

Run:

```bash
git add README.md docs/index.md docs/deepdive/evidence-status.md docs/deepdive/message-map.md docs/reference/claim-boundaries.md docs/reference/cpd-paper-faithful-offline-lane-spec.md docs/reference/cpd-paper-fixture-breadth-expansion-plan.md docs/reference/cpd-paper-reproduction-gap-matrix.md docs/reference/cpd-paper-story-status.md docs/records/README.md docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-generation-contract.md experiments/registry.yaml
git commit -m "docs: record CPD PrimitiveSpec generation contract"
```

## Task 5: Review, Verify, Merge, Push, And Clean Up

**Files:**
- Review all changed files from this branch.

- [ ] **Step 1: Dispatch multi-agent reviews**

Dispatch at least two independent reviewers:

```text
Reviewer A: Verify implementation and tests against
docs/superpowers/specs/2026-05-17-cpd-paper-mapped-subset-primitivespec-generation-contract-design.md.
Focus on payload fields, row schemas, input validation, rejection labels, coverage counts, and
top-level next-gate integration.

Reviewer B: Verify docs, records, registry, and claim boundaries. Focus on avoiding runtime
PrimitiveSpec, CollisionPackage, Newton runtime support, real-USD, benchmark, collision-quality,
deployment, or safety claims.
```

Fix Critical and Important issues before continuing.

- [ ] **Step 2: Run focused and full verification**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k 'primitivespec_generation or primitivespec_generation_preflight or offline_report_covers_first_toy_slice' -q
python -m pytest tests/test_cli.py -k cpd_paper_offline -q
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
python -m pytest -q
```

Expected: all commands pass. If full pytest fails only because ignored raw paper intake is missing
from this worktree, copy the ignored local intake from the main worktree and rerun the exact failing
test plus the full suite. Do not commit ignored raw paper artifacts.

- [ ] **Step 3: Commit review fixes**

If review or verification required fixes, run:

```bash
git add src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cpd_paper_offline.py tests/test_cli.py README.md docs/index.md docs/deepdive/evidence-status.md docs/deepdive/message-map.md docs/reference/claim-boundaries.md docs/reference/cpd-paper-faithful-offline-lane-spec.md docs/reference/cpd-paper-fixture-breadth-expansion-plan.md docs/reference/cpd-paper-reproduction-gap-matrix.md docs/reference/cpd-paper-story-status.md docs/records/README.md docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-generation-contract.md experiments/registry.yaml
git commit -m "fix: tighten CPD PrimitiveSpec generation contract"
```

- [ ] **Step 4: Merge to main and push**

Run:

```bash
cd /cpfs/user/zhuzihou/dev/physics-primitive-agent
git status --short --branch
git merge --no-ff cpd-paper-primitivespec-generation-contract -m "merge CPD PrimitiveSpec generation contract"
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
python -m pytest -q
git push origin main
```

Expected: merge succeeds, verification passes on `main`, and push succeeds.

- [ ] **Step 5: Clean feature worktree**

Run:

```bash
git worktree remove /cpfs/user/zhuzihou/dev/physics-primitive-agent/.worktrees/cpd-paper-primitivespec-generation-contract
git branch -d cpd-paper-primitivespec-generation-contract
git status --short --branch
```

Expected: the branch is deleted, the worktree is removed, and `main` is clean against
`origin/main`.

## Required Claim Boundary

Allowed wording:

```text
The report includes an offline PrimitiveSpec generation contract with native-family template rows
and no-generation current rows.
```

Forbidden wording:

```text
The system generates runtime PrimitiveSpecs.
The output is CollisionPackage-ready.
The output has Newton runtime support.
The paper-lane output improves collision quality.
The report provides benchmark, real-USD, deployment, or safety evidence.
```

## Verification Checklist

- `paper_mapped_subset_primitivespec_generation_contract` exists in the report.
- Top-level `next_required_gate` is `paper_mapped_subset_primitivespec_candidate_source_contract`.
- The generation-preflight nested payload still points to `paper_mapped_subset_primitivespec_generation_contract`.
- Native-family template rows: 3.
- Blocked requirement rows: 2.
- No-op requirement rows: 1.
- Current no-generation rows: 16.
- Runtime PrimitiveSpec count: 0.
- CollisionPackage count: 0.
- Runtime admissibility count: 0.
- Package/Newton/real-USD/benchmark/collision-quality/deployment/safety flags remain false.
- Docs and records describe the slice as offline/report-only.
- Focused tests, docs validators, `git diff --check`, and full pytest pass before merge.

## Self-Review

- This plan implements one gate, not a broad package-generation or Newton-runtime feature.
- The new next gate names the real blocker: mapped current candidate sourcing.
- The plan keeps all runtime and safety-affecting claims blocked.
- The plan includes concrete RED tests, implementation steps, docs steps, verification commands, review, merge, push, and cleanup.
