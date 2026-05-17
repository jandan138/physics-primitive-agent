# CPD Paper Mapped-Subset PrimitiveSpec Candidate Source Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the offline/report-only `paper_mapped_subset_primitivespec_candidate_source_contract` gate that audits candidate-source eligibility after the PrimitiveSpec generation contract while keeping runtime PrimitiveSpecs, CollisionPackages, Newton, real USD, benchmarks, collision-quality, deployment, and safety claims at zero/false.

**Architecture:** Consume `paper_mapped_subset_primitivespec_generation_contract`, validate it strictly, classify native templates as future-only, classify blocked/no-op paper-family rows as ineligible, classify all 16 current rows as traceable but unmapped, and advance the top-level next gate to `paper_mapped_subset_native_current_fixture_contract`.

**Tech Stack:** Python, pytest, existing CPD paper offline report builder, Markdown docs, YAML experiment registry.

---

## File Map

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
  - Add `_PAPER_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT`.
  - Add `_paper_remaining_gaps_after_mapped_subset_primitivespec_candidate_source()`.
  - Add candidate-source input validation helpers.
  - Add audit row builders for native templates, blocked/no-op family rows, and current rows.
  - Add `_paper_require_unique_candidate_source_row_ids()`.
  - Add `_paper_mapped_subset_primitivespec_candidate_source_contract_payload()`.
  - Wire the payload into `build_cpd_paper_offline_report()`.
- Modify: `tests/test_cpd_paper_offline.py`
  - Add RED tests for top-level gate movement, exact payload schema, audit row content, false flags, coverage counts, rejection labels, and duplicate row ids.
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
  - Create: `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-candidate-source-contract.md`

## Task 1: Add RED Offline Tests

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`

- [ ] **Step 1: Add import and constants**

Add a module alias for new helper access during RED, while keeping existing direct imports for
already-implemented helpers:

```python
import primitive_collision_compiler.baselines.cpd_paper.offline as cpd_paper_offline
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

Call new helpers through `cpd_paper_offline.<helper_name>` in RED tests. This keeps pytest
collection runnable before the new functions exist, so the first RED failure points at missing
behavior rather than an import-time collection error.

Add:

```python
EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT = (
    "paper_mapped_subset_native_current_fixture_contract"
)
EXPECTED_CANDIDATE_SOURCE_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT,
]
```

Change:

```python
EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT,
]
```

to:

```python
EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS = [
    EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT,
]
```

- [ ] **Step 2: Add helper and required key sets**

Add after `_generation_contract_preflight_input()`:

```python
def _candidate_source_generation_input() -> dict[str, object]:
    report = build_cpd_paper_offline_report()
    return json.loads(
        json.dumps(report["paper_mapped_subset_primitivespec_generation_contract"])
    )
```

Add:

```python
PRIMITIVESPEC_CANDIDATE_SOURCE_PAYLOAD_REQUIRED_KEYS = {
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
    "candidate_source_action",
    "primitive_spec_generation_candidate_count",
    "eligible_current_candidate_source_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "candidate_source_contract",
    "input_contract_summary",
    "native_template_candidate_source_audit_rows",
    "blocked_family_candidate_source_audit_rows",
    "noop_family_candidate_source_audit_rows",
    "current_row_candidate_source_audit_rows",
    "coverage_summary",
    "remaining_gaps",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}

PRIMITIVESPEC_CANDIDATE_SOURCE_AUDIT_ROW_REQUIRED_KEYS = {
    "candidate_source_audit_row_id",
    "source_primitivespec_generation_row_id",
    "source_primitivespec_generation_preflight_row_id",
    "source_primitivespec_validation_row_id",
    "source_primitivespec_dry_run_row_id",
    "source_adapter_preflight_row_id",
    "source_candidate_matrix_row_id",
    "source_conversion_plan_row_id",
    "paper_primitive",
    "primitive_spec_kind",
    "candidate_mapping_label",
    "source_role",
    "candidate_source_decision",
    "candidate_source_reason",
    "eligible_current_candidate_source",
    "primitive_spec_generation_candidate",
    "generated_primitive_spec",
    "required_later_gate",
    "required_future_policy",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}
```

- [ ] **Step 3: Add top-level and payload tests**

Append tests after the generation contract tests:

```python
def test_cpd_paper_records_mapped_subset_primitivespec_candidate_source_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_primitivespec_candidate_source_contract"]

    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT
    )
    assert report["failure_labels"] == [
        "paper_mapped_subset_native_current_fixture_contract_missing",
    ]
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_CANDIDATE_SOURCE_REMAINING_GAPS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert (
        report["paper_mapped_subset_primitivespec_generation_contract"][
            "next_required_gate"
        ]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )

    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
    )
    assert (
        payload["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT
    )
    assert payload["decision_reason"] == (
        "primitivespec_candidate_source_contract_complete_"
        "native_current_fixture_contract_missing"
    )
    assert payload["primitive_spec_generation_candidate_count"] == 0
    assert payload["eligible_current_candidate_source_count"] == 0
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_CANDIDATE_SOURCE_REMAINING_GAPS
```

Add the exact schema test:

```python
def test_cpd_paper_primitivespec_candidate_source_payload_schema_is_exact():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_primitivespec_candidate_source_contract"
    ]

    assert set(payload) == PRIMITIVESPEC_CANDIDATE_SOURCE_PAYLOAD_REQUIRED_KEYS
    assert payload["gate_status"] == (
        "implemented_offline_primitivespec_candidate_source_contract_only_partial"
    )
    assert payload["artifact_kind"] == (
        "offline_primitivespec_candidate_source_audit_not_primitivespec_"
        "not_collision_package"
    )
    assert payload["candidate_source_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
        ),
        "current_candidate_source_gate_closed": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
        ),
        "next_current_candidate_gate_required": (
            EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT
        ),
        "native_template_rows_are_future_only": True,
        "current_rows_must_be_mapped_native_family": True,
        "eligible_current_candidate_source_required_before_runtime_generation": True,
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

- [ ] **Step 4: Add row and coverage tests**

Add tests that assert:

```python
payload = build_cpd_paper_offline_report()[
    "paper_mapped_subset_primitivespec_candidate_source_contract"
]
assert [row["paper_primitive"] for row in payload["native_template_candidate_source_audit_rows"]] == [
    "oriented_bounding_box",
    "sphere",
    "capsule",
]
assert [row["source_role"] for row in payload["native_template_candidate_source_audit_rows"]] == [
    "future_native_template",
    "future_native_template",
    "future_native_template",
]
assert [row["paper_primitive"] for row in payload["blocked_family_candidate_source_audit_rows"]] == [
    "capped_cylinder",
    "frustum",
]
assert [row["paper_primitive"] for row in payload["noop_family_candidate_source_audit_rows"]] == [
    "trapezoidal_prism",
]
assert len(payload["current_row_candidate_source_audit_rows"]) == 16
assert payload["coverage_summary"] == {
    "candidate_source_requirement_row_count": 6,
    "native_template_candidate_source_audit_row_count": 3,
    "blocked_family_candidate_source_audit_row_count": 2,
    "noop_family_candidate_source_audit_row_count": 1,
    "current_row_candidate_source_audit_row_count": 16,
    "eligible_current_candidate_source_count": 0,
    "ineligible_current_candidate_source_count": 16,
    "future_template_only_source_count": 3,
    "blocked_policy_source_count": 2,
    "noop_unmapped_family_source_count": 1,
    "primitive_spec_generation_candidate_record_count": 0,
    "generated_primitive_spec_record_count": 0,
    "generated_collision_package_record_count": 0,
    "runtime_admissibility_check_record_count": 0,
    "current_paper_primitive_distribution": {"trapezoidal_prism": 16},
    "current_mapping_label_distribution": {"offline_only_unmapped": 16},
    "candidate_source_decision_distribution": {
        "template_only_not_current_candidate_source": 3,
        "blocked_until_approximation_policy": 2,
        "no_current_native_candidate_source": 1,
        "current_row_ineligible_unmapped_paper_primitive": 16,
    },
}
```

Loop through every row and assert:

```python
for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
    assert row[flag] is False
assert row["eligible_current_candidate_source"] is False
assert row["primitive_spec_generation_candidate"] is False
assert row["generated_primitive_spec"] is None
assert (
    row["required_later_gate"]
    == EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT
)
```

- [ ] **Step 5: Add rejection tests**

Add targeted rejection tests:

```python
def test_cpd_paper_primitivespec_candidate_source_rejects_wrong_input_gate():
    generation = _candidate_source_generation_input()
    generation["gate_id"] = "stale_gate"

    with pytest.raises(
        ValueError,
        match="primitivespec_candidate_source_input_gate_id_mismatch",
    ):
        _paper_mapped_subset_primitivespec_candidate_source_contract_payload(
            generation
        )


def test_cpd_paper_primitivespec_candidate_source_rejects_runtime_leak():
    generation = _candidate_source_generation_input()
    generation["generated_primitive_spec_count"] = 1

    with pytest.raises(
        ValueError,
        match="primitivespec_candidate_source_input_generated_spec_nonzero",
    ):
        _paper_mapped_subset_primitivespec_candidate_source_contract_payload(
            generation
        )


def test_cpd_paper_primitivespec_candidate_source_rejects_current_row_candidate_leak():
    generation = _candidate_source_generation_input()
    rows = [
        dict(row)
        for row in generation["current_row_primitivespec_generation_rows"]
    ]
    rows[0]["primitive_spec_generation_candidate"] = True
    generation["current_row_primitivespec_generation_rows"] = rows

    with pytest.raises(
        ValueError,
        match="primitivespec_candidate_source_current_row_runtime_leak:"
        "primitive_spec_generation_candidate",
    ):
        _paper_mapped_subset_primitivespec_candidate_source_contract_payload(
            generation
        )


def test_cpd_paper_primitivespec_candidate_source_rejects_duplicate_row_ids():
    rows = [
        {"candidate_source_audit_row_id": "duplicate"},
        {"candidate_source_audit_row_id": "duplicate"},
    ]

    with pytest.raises(
        ValueError,
        match="duplicate_primitivespec_candidate_source_row_id",
    ):
        _paper_require_unique_candidate_source_row_ids(rows)
```

- [ ] **Step 6: Run RED tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k 'candidate_source or primitivespec_generation_contract_gate' -q
```

Expected: tests that reference `_paper_mapped_subset_primitivespec_candidate_source_contract_payload`,
`_paper_require_unique_candidate_source_row_ids`, and the new top-level gate fail because
implementation is missing.

- [ ] **Step 7: Commit RED tests**

```bash
git add tests/test_cpd_paper_offline.py
git commit -m "test: add CPD PrimitiveSpec candidate source contract coverage"
```

## Task 2: Implement Candidate-Source Contract

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add constants and remaining-gaps helper**

Add near the existing PrimitiveSpec contract constants:

```python
_PAPER_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT = (
    "paper_mapped_subset_native_current_fixture_contract"
)
```

Add near the remaining-gap helpers:

```python
def _paper_remaining_gaps_after_mapped_subset_primitivespec_candidate_source() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT]
```

- [ ] **Step 2: Add validators and row-id helper**

Add helpers below the generation-contract payload:

```python
def _paper_require_unique_candidate_source_row_ids(
    rows: list[dict[str, object]],
) -> None:
    row_ids = [str(row["candidate_source_audit_row_id"]) for row in rows]
    if len(row_ids) != len(set(row_ids)):
        raise ValueError("duplicate_primitivespec_candidate_source_row_id")
```

Add validation functions that check:

```python
generation.get("gate_id") == _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
generation.get("next_required_gate") == _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
generation.get("primitive_spec_generation_candidate_count") == 0
generation.get("offline_primitivespec_template_count") == 3
generation.get("generated_primitive_spec_count") == 0
generation.get("generated_collision_package_count") == 0
generation.get("runtime_admissibility_check_count") == 0
```

Also validate the upstream structure exactly:

```python
generation["primitive_spec_generation_contract"]["input_gate_required"] == _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
generation["primitive_spec_generation_contract"]["current_candidate_source_gate_required"] == _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
generation["primitive_spec_generation_contract"]["template_only_native_families"] == ["box", "sphere", "capsule"]
[row["paper_primitive"] for row in generation["native_family_primitivespec_template_rows"]] == ["oriented_bounding_box", "sphere", "capsule"]
[row["paper_primitive"] for row in generation["blocked_primitivespec_generation_requirement_rows"]] == ["capped_cylinder", "frustum"]
[row["paper_primitive"] for row in generation["noop_primitivespec_generation_requirement_rows"]] == ["trapezoidal_prism"]
len(generation["current_row_primitivespec_generation_rows"]) == 16
all(row["paper_primitive"] == "trapezoidal_prism" for row in generation["current_row_primitivespec_generation_rows"])
all(row["offline_mapping_label"] == "offline_only_unmapped" for row in generation["current_row_primitivespec_generation_rows"])
```

Reject all true row-level runtime/package/Newton/USD/benchmark/collision-quality/deployment flags
in every upstream row collection. Reject non-empty generated specs, candidate flags, silent-drop
flags, empty source ids, sequence drift, coverage count drift, duplicate upstream row ids, and
duplicate emitted audit row ids with the rejection labels from the design spec.

Use the rejection labels from the design spec. Reuse `_paper_false_primitivespec_generation_flags()`
and the existing distribution helpers where possible.

- [ ] **Step 3: Add audit row builders**

Implement native-template row builder:

```python
def _paper_candidate_source_native_template_row(
    row: dict[str, object],
) -> dict[str, object]:
    return {
        "candidate_source_audit_row_id": (
            f"candidate_source_template__{row['paper_primitive']}"
        ),
        "source_primitivespec_generation_row_id": (
            row["primitive_spec_generation_template_row_id"]
        ),
        "source_primitivespec_generation_preflight_row_id": (
            row["source_primitivespec_generation_preflight_row_id"]
        ),
        "source_primitivespec_validation_row_id": (
            row["source_primitivespec_validation_row_id"]
        ),
        "source_primitivespec_dry_run_row_id": row["source_primitivespec_dry_run_row_id"],
        "source_adapter_preflight_row_id": row["source_adapter_preflight_row_id"],
        "source_candidate_matrix_row_id": row["source_candidate_matrix_row_id"],
        "source_conversion_plan_row_id": row["source_conversion_plan_row_id"],
        "paper_primitive": row["paper_primitive"],
        "primitive_spec_kind": row["primitive_spec_kind"],
        "candidate_mapping_label": row["candidate_mapping_label"],
        "source_role": "future_native_template",
        "candidate_source_decision": "template_only_not_current_candidate_source",
        "candidate_source_reason": (
            "native_family_template_has_no_current_decomposition_row"
        ),
        "eligible_current_candidate_source": False,
        "primitive_spec_generation_candidate": False,
        "generated_primitive_spec": None,
        "required_later_gate": _PAPER_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT,
        "required_future_policy": "native_current_fixture",
        **_paper_false_primitivespec_generation_flags(),
    }
```

Implement blocked, no-op, and current-row builders using the same key set, changing only
`source_role`, `candidate_source_decision`, `candidate_source_reason`, `required_future_policy`,
and the source row id field.

- [ ] **Step 4: Add payload function and wire report**

Implement:

```python
def _paper_mapped_subset_primitivespec_candidate_source_contract_payload(
    generation: dict[str, object],
) -> dict[str, object]:
    _paper_validate_primitivespec_candidate_source_input(generation)
    native_rows = [
        _paper_candidate_source_native_template_row(row)
        for row in generation["native_family_primitivespec_template_rows"]
    ]
    blocked_rows = [
        _paper_candidate_source_blocked_family_row(row)
        for row in generation["blocked_primitivespec_generation_requirement_rows"]
    ]
    noop_rows = [
        _paper_candidate_source_noop_family_row(row)
        for row in generation["noop_primitivespec_generation_requirement_rows"]
    ]
    current_rows = [
        _paper_candidate_source_current_row(row)
        for row in generation["current_row_primitivespec_generation_rows"]
    ]
    all_rows = native_rows + blocked_rows + noop_rows + current_rows
    _paper_require_unique_candidate_source_row_ids(all_rows)
    remaining_gaps = (
        _paper_remaining_gaps_after_mapped_subset_primitivespec_candidate_source()
    )
    return {
        "gate_id": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT,
        "gate_status": (
            "implemented_offline_primitivespec_candidate_source_contract_only_partial"
        ),
        "closed_gate": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT,
        "input_gate_id": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT,
        "next_required_gate": _PAPER_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT,
        "decision": "remain_partial",
        "decision_reason": (
            "primitivespec_candidate_source_contract_complete_"
            "native_current_fixture_contract_missing"
        ),
        "paper_faithful_offline_allowed": False,
        "package_generation_allowed": False,
        "artifact_kind": (
            "offline_primitivespec_candidate_source_audit_not_primitivespec_"
            "not_collision_package"
        ),
        "schema_version": 1,
        "source_scope": "synthetic_toy_fixtures_only",
        "implementation_boundary": (
            "offline_primitivespec_candidate_source_audit_only_no_runtime_"
            "primitivespec_no_collision_package_no_newton"
        ),
        "candidate_source_action": (
            "audit_sources_and_keep_current_candidate_count_zero"
        ),
        "primitive_spec_generation_candidate_count": 0,
        "eligible_current_candidate_source_count": 0,
        "generated_primitive_spec_count": 0,
        "generated_collision_package_count": 0,
        "runtime_admissibility_check_count": 0,
        "input_contract_summary": {
            "input_gate_id": generation["gate_id"],
            "input_artifact_kind": generation["artifact_kind"],
            "native_family_primitivespec_template_row_count": (
                generation["coverage_summary"][
                    "native_family_primitivespec_template_row_count"
                ]
            ),
            "blocked_primitivespec_generation_requirement_row_count": (
                generation["coverage_summary"][
                    "blocked_primitivespec_generation_requirement_row_count"
                ]
            ),
            "noop_primitivespec_generation_requirement_row_count": (
                generation["coverage_summary"][
                    "noop_primitivespec_generation_requirement_row_count"
                ]
            ),
            "current_row_primitivespec_generation_row_count": (
                generation["coverage_summary"][
                    "current_row_primitivespec_generation_row_count"
                ]
            ),
            "primitive_spec_generation_candidate_record_count": (
                generation["coverage_summary"][
                    "primitive_spec_generation_candidate_record_count"
                ]
            ),
            "generated_primitive_spec_record_count": (
                generation["coverage_summary"][
                    "generated_primitive_spec_record_count"
                ]
            ),
        },
        "candidate_source_contract": {
            "input_gate_required": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT,
            "current_candidate_source_gate_closed": (
                _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
            ),
            "next_current_candidate_gate_required": (
                _PAPER_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT
            ),
            "native_template_rows_are_future_only": True,
            "current_rows_must_be_mapped_native_family": True,
            "eligible_current_candidate_source_required_before_runtime_generation": True,
            "zero_runtime_primitivespecs_required": True,
            "zero_collision_packages_required": True,
            "zero_runtime_admissibility_checks_required": True,
            "runtime_primitive_spec_generation_allowed": False,
            "collision_package_generation_allowed": False,
            "newton_runtime_allowed": False,
            "approximation_policy_enabled": False,
            "silent_drop_allowed": False,
        },
        "native_template_candidate_source_audit_rows": native_rows,
        "blocked_family_candidate_source_audit_rows": blocked_rows,
        "noop_family_candidate_source_audit_rows": noop_rows,
        "current_row_candidate_source_audit_rows": current_rows,
        "coverage_summary": _paper_candidate_source_coverage_summary(
            native_rows, blocked_rows, noop_rows, current_rows
        ),
        "remaining_gaps": remaining_gaps,
        **_paper_false_primitivespec_generation_flags(),
    }
```

In `build_cpd_paper_offline_report()`, create `mapped_subset_primitivespec_candidate_source` after
`mapped_subset_primitivespec_generation`, set `missing_before_paper_faithful` using the new helper,
set top-level `next_required_gate` to `_PAPER_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT`, append
the candidate-source contract to `implemented_output_contract_scope`, and add the payload to the
returned dictionary.

- [ ] **Step 5: Run GREEN tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k 'candidate_source or primitivespec_generation_contract_gate' -q
```

Expected: passing.

- [ ] **Step 6: Commit implementation**

```bash
git add src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cpd_paper_offline.py
git commit -m "feat: implement CPD PrimitiveSpec candidate source contract"
```

## Task 3: Add CLI Coverage

**Files:**
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write CLI RED assertions**

In `test_cli_run_cpd_paper_offline_report_emits_json`, update the top-level gate:

```python
assert payload["failure_labels"] == [
    "paper_mapped_subset_native_current_fixture_contract_missing",
]
assert payload["next_required_gate"] == (
    "paper_mapped_subset_native_current_fixture_contract"
)
assert payload["paper_faithfulness"]["missing_before_paper_faithful_offline"] == [
    "paper_mapped_subset_native_current_fixture_contract",
]
```

Append the candidate-source scope string to `implemented_output_contract_scope` and add:

```python
candidate_source = payload[
    "paper_mapped_subset_primitivespec_candidate_source_contract"
]
assert (
    candidate_source["gate_id"]
    == "paper_mapped_subset_primitivespec_candidate_source_contract"
)
assert (
    candidate_source["input_gate_id"]
    == "paper_mapped_subset_primitivespec_generation_contract"
)
assert (
    candidate_source["next_required_gate"]
    == "paper_mapped_subset_native_current_fixture_contract"
)
assert candidate_source["eligible_current_candidate_source_count"] == 0
assert candidate_source["generated_primitive_spec_count"] == 0
assert candidate_source["generated_collision_package_count"] == 0
assert candidate_source["runtime_admissibility_check_count"] == 0
assert len(candidate_source["native_template_candidate_source_audit_rows"]) == 3
assert len(candidate_source["blocked_family_candidate_source_audit_rows"]) == 2
assert len(candidate_source["noop_family_candidate_source_audit_rows"]) == 1
assert len(candidate_source["current_row_candidate_source_audit_rows"]) == 16
assert candidate_source["primitive_spec_generated"] is False
assert candidate_source["collision_package_generated"] is False
assert candidate_source["runtime_admissibility_checked"] is False
assert candidate_source["newton_support_claimed"] is False
assert candidate_source["package_generation_triggered"] is False
assert candidate_source["newton_runtime_triggered"] is False
assert candidate_source["real_usd_triggered"] is False
assert candidate_source["benchmark_triggered"] is False
```

- [ ] **Step 2: Run CLI tests**

Run:

```bash
python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Expected: passing after Task 2; if run before Task 2, fail on missing payload/gate.

- [ ] **Step 3: Commit CLI coverage**

```bash
git add tests/test_cli.py
git commit -m "test: cover CPD candidate source contract in CLI"
```

## Task 4: Update Documentation And Registry

**Files:**
- Modify docs and registry listed in the file map.
- Create dated record.

- [ ] **Step 1: Add dated record**

Create `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-candidate-source-contract.md`
with:

```markdown
# CPD Paper Mapped-Subset PrimitiveSpec Candidate Source Contract

Date: 2026-05-17

Status: implemented as an offline/report-only contract.

This record closes `paper_mapped_subset_primitivespec_candidate_source_contract`.
It audits the output of `paper_mapped_subset_primitivespec_generation_contract`, classifies
native box/sphere/capsule rows as future templates only, records blocked/no-op paper-family rows,
keeps all 16 current rows ineligible because they remain `trapezoidal_prism` /
`offline_only_unmapped`, and advances the next gate to
`paper_mapped_subset_native_current_fixture_contract`.

No runtime `PrimitiveSpec`, `CollisionPackage`, Newton runtime, real USD, benchmark,
collision-quality, deployment, or safety-certification claim is created.

Verification:

- focused offline candidate-source tests
- CLI CPD paper offline JSON test
- full pytest
- docs validation
- site-claim validation
- git diff whitespace check
```

- [ ] **Step 2: Update reader-facing references**

Update each reader-facing CPD paper reference listed in the file map so it says the
candidate-source contract is implemented and the current next gate is
`paper_mapped_subset_native_current_fixture_contract`. Keep older historical record links intact;
only revise present-tense status, current-next-action, gap-matrix, story-status, evidence, and
message-map wording.

- [ ] **Step 3: Update claim boundaries**

Add boundary language:

```markdown
- The current code can close `paper_mapped_subset_primitivespec_candidate_source_contract` as
  offline source-audit accounting only. It records zero eligible current PrimitiveSpec candidate
  sources and advances the next gate to `paper_mapped_subset_native_current_fixture_contract`.
  It is not PrimitiveSpec readiness, package readiness, runtime admissibility, Newton support,
  approximation support, real-USD evidence, benchmark evidence, collision-quality validation,
  deployment readiness, safety certification, or full CPD paper reproduction.
```

- [ ] **Step 4: Update registry**

Add a new `experiments/registry.yaml` entry with scope:

```yaml
- id: cpd_paper_mapped_subset_primitivespec_candidate_source_contract
  status: implemented
  scope:
    - partial command-only offline PrimitiveSpec candidate-source audit for deterministic synthetic fixture records only
    - records zero eligible current candidate sources
    - closes only paper_mapped_subset_primitivespec_candidate_source_contract and advances the next gate to paper_mapped_subset_native_current_fixture_contract
    - no runtime PrimitiveSpec generation, CollisionPackage generation, Newton runtime, real-USD loading, benchmark, collision-quality, deployment, or safety-certification claim
```

- [ ] **Step 5: Run docs checks**

Run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
```

Expected: both pass.

- [ ] **Step 6: Commit docs**

```bash
git add README.md docs/index.md docs/deepdive/evidence-status.md docs/deepdive/message-map.md docs/reference/claim-boundaries.md docs/reference/cpd-paper-faithful-offline-lane-spec.md docs/reference/cpd-paper-fixture-breadth-expansion-plan.md docs/reference/cpd-paper-reproduction-gap-matrix.md docs/reference/cpd-paper-story-status.md docs/records/README.md docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-candidate-source-contract.md experiments/registry.yaml
git commit -m "docs: record CPD PrimitiveSpec candidate source contract"
```

## Task 5: Final Review And Verification

**Files:**
- No planned edits unless review finds issues.

- [ ] **Step 1: Run relevant tests**

```bash
python -m pytest -q tests/test_cpd_paper_offline.py tests/test_cli.py
```

Expected: all pass.

- [ ] **Step 2: Run full verification**

```bash
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

- [ ] **Step 3: Request multi-agent code review**

Dispatch reviewers with:

```text
Review the candidate-source contract slice from HEAD~N..HEAD.
Check spec compliance, claim boundaries, tests, docs, and whether native templates are kept
future-only rather than current candidates.
```

- [ ] **Step 4: Fix review findings with RED/GREEN if needed**

If a reviewer finds a behavior gap, add or update a failing test first, run it RED, implement the
minimal fix, run GREEN, then re-request review.

- [ ] **Step 5: Commit verification record**

Add verification output to the dated record and commit:

```bash
git add docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-candidate-source-contract.md
git commit -m "docs: record CPD candidate source verification"
```

- [ ] **Step 6: Merge and push**

From the main worktree:

```bash
git merge --ff-only cpd-paper-primitivespec-candidate-source-contract
git push origin main
```

Then remove the feature worktree and delete the branch after the push succeeds.
