# CPD Paper Mapped-Subset Conversion Candidate Matrix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the offline-only `paper_mapped_subset_conversion_candidate_matrix` gate to `cpd_paper_offline_report`.

**Architecture:** Extend `src/primitive_collision_compiler/baselines/cpd_paper/offline.py` with a candidate-matrix payload that consumes `paper_package_conversion_mapped_subset_plan`. The payload emits family review rows and current row review rows, records zero current package-conversion candidates, and advances to `paper_mapped_subset_adapter_preflight_contract` without creating packages or runtime artifacts.

**Tech Stack:** Python, pytest, Markdown docs, YAML registry, existing CLI JSON report command.

---

### Task 1: Add RED Tests

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add test constants**

In `tests/test_cpd_paper_offline.py`, add:

```python
EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_adapter_preflight_contract"
)
EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS = [
    EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT
]
EXPECTED_CANDIDATE_MATRIX_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT
]
```

Update existing current-output expected constants so earlier payload-specific tests still preserve
their historical `remaining_gaps` expectations where required.

- [ ] **Step 2: Write failing offline-report gate test**

Add:

```python
def test_cpd_paper_records_mapped_subset_conversion_candidate_matrix_gate():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_conversion_candidate_matrix"]

    assert report["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT
    )
    assert report["failure_labels"] == [
        "paper_mapped_subset_adapter_preflight_contract_missing",
    ]
    assert payload["gate_id"] == EXPECTED_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX
    assert payload["input_gate_id"] == EXPECTED_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT
    )
    assert payload["gate_status"] == "implemented_offline_candidate_matrix_only_partial"
    assert payload["decision"] == "remain_partial"
    assert payload["package_generation_allowed"] is False
    assert payload["remaining_gaps"] == EXPECTED_CANDIDATE_MATRIX_REMAINING_GAPS
    assert payload["primitive_spec_generated"] is False
    assert payload["collision_package_generated"] is False
    assert payload["runtime_admissibility_checked"] is False
    assert payload["newton_support_claimed"] is False
```

- [ ] **Step 3: Write failing family matrix test**

Add:

```python
def test_cpd_paper_candidate_matrix_records_future_family_review_rows():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_conversion_candidate_matrix"]
    rows = {
        row["paper_primitive"]: row
        for row in payload["future_family_candidate_matrix_rows"]
    }

    assert list(rows) == [
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
    expected_native = {
        "oriented_bounding_box": "box",
        "sphere": "sphere",
        "capsule": "capsule",
    }
    for primitive_name, runtime_kind in expected_native.items():
        row = rows[primitive_name]
        assert row["candidate_runtime_kind"] == runtime_kind
        assert row["candidate_matrix_decision"] == "native_family_review_only"
        assert row["future_family_review_candidate"] is True
        assert row["current_row_evidence_count"] == 0
        assert row["current_package_conversion_candidate_count"] == 0
        assert row["package_conversion_enabled_by_this_gate"] is False

    for primitive_name in ("capped_cylinder", "frustum"):
        row = rows[primitive_name]
        assert row["candidate_runtime_kind"] == "offline_only_unmapped"
        assert row["candidate_matrix_decision"] == "blocked_approximation_policy_missing"
        assert row["future_family_review_candidate"] is False
        assert row["package_conversion_enabled_by_this_gate"] is False

    trapezoid = rows["trapezoidal_prism"]
    assert trapezoid["candidate_matrix_decision"] == "blocked_unmapped_current_rows"
    assert trapezoid["current_row_evidence_count"] == 16
```

- [ ] **Step 4: Write failing current-row matrix test**

Add:

```python
def test_cpd_paper_candidate_matrix_blocks_current_unmapped_rows():
    report = build_cpd_paper_offline_report()
    plan = report["paper_package_conversion_mapped_subset_plan"]
    payload = report["paper_mapped_subset_conversion_candidate_matrix"]
    summary = payload["coverage_summary"]
    rows = payload["current_row_candidate_matrix_rows"]

    assert summary["future_family_candidate_matrix_row_count"] == 6
    assert summary["future_family_review_candidate_count"] == 3
    assert summary["excluded_family_review_row_count"] == 3
    assert summary["current_row_candidate_matrix_row_count"] == 16
    assert summary["current_package_conversion_candidate_count"] == 0
    assert summary["current_blocked_requires_policy_count"] == 16
    assert summary["package_candidate_record_count"] == 0
    assert summary["current_paper_primitive_distribution"] == {
        "trapezoidal_prism": 16,
    }
    assert summary["current_runtime_kind_distribution"] == {
        "offline_only_unmapped": 16,
    }

    plan_rows = plan["current_row_conversion_plan_rows"]
    assert len(rows) == len(plan_rows) == 16
    for row, upstream_row in zip(rows, plan_rows):
        assert row["source_conversion_plan_row_id"] == upstream_row[
            "conversion_plan_row_id"
        ]
        assert row["paper_primitive"] == "trapezoidal_prism"
        assert row["offline_runtime_kind_label"] == "offline_only_unmapped"
        assert row["input_conversion_plan_decision"] == (
            "exclude_requires_explicit_mapping_or_approximation_policy"
        )
        assert row["candidate_matrix_decision"] == "blocked_unmapped_current_rows"
        assert row["candidate_matrix_action"] == "keep_offline"
        assert row["current_package_conversion_candidate"] is False
        assert row["package_candidate_status"] == (
            "not_current_candidate_unsupported_policy_block"
        )
        assert row["required_future_policy"] == (
            "explicit_mapping_or_approximation_policy_before_package_generation"
        )
        assert row["primitive_spec_generation_triggered"] is False
        assert row["collision_package_generation_triggered"] is False
        assert row["runtime_admissibility_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False
```

- [ ] **Step 5: Write failing report-only boundary test**

Add:

```python
def test_cpd_paper_candidate_matrix_stays_report_only():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_conversion_candidate_matrix"]

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
    assert payload["candidate_matrix_contract"][
        "primitive_spec_generation_allowed"
    ] is False
    assert payload["candidate_matrix_contract"][
        "collision_package_generation_allowed"
    ] is False
    assert payload["candidate_matrix_contract"]["newton_runtime_allowed"] is False
    assert payload["candidate_matrix_contract"][
        "runtime_admissibility_supported"
    ] is False
    for row in payload["future_family_candidate_matrix_rows"]:
        assert forbidden_keys.isdisjoint(row)
    for row in payload["current_row_candidate_matrix_rows"]:
        assert forbidden_keys.isdisjoint(row)
```

- [ ] **Step 6: Extend CLI test**

In `test_cli_run_cpd_paper_offline_report_emits_json`, update top-level expectations to:

```python
assert payload["failure_labels"] == [
    "paper_mapped_subset_adapter_preflight_contract_missing",
]
assert payload["next_required_gate"] == "paper_mapped_subset_adapter_preflight_contract"
```

Add assertions for:

```python
candidate_matrix = payload["paper_mapped_subset_conversion_candidate_matrix"]
assert candidate_matrix["gate_id"] == "paper_mapped_subset_conversion_candidate_matrix"
assert candidate_matrix["input_gate_id"] == "paper_package_conversion_mapped_subset_plan"
assert (
    candidate_matrix["next_required_gate"]
    == "paper_mapped_subset_adapter_preflight_contract"
)
assert candidate_matrix["coverage_summary"]["future_family_candidate_matrix_row_count"] == 6
assert candidate_matrix["coverage_summary"]["future_family_review_candidate_count"] == 3
assert candidate_matrix["coverage_summary"]["current_row_candidate_matrix_row_count"] == 16
assert candidate_matrix["coverage_summary"]["current_package_conversion_candidate_count"] == 0
assert candidate_matrix["package_generation_triggered"] is False
assert candidate_matrix["newton_runtime_triggered"] is False
```

- [ ] **Step 7: Run RED tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
```

Expected: fail because `paper_mapped_subset_conversion_candidate_matrix` and
`paper_mapped_subset_adapter_preflight_contract` are not wired yet.

### Task 2: Implement Offline Candidate Matrix Payload

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add next-gate constant**

Add near the existing paper gate constants:

```python
_PAPER_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_adapter_preflight_contract"
)
```

- [ ] **Step 2: Add remaining-gap helper**

Add:

```python
def _paper_remaining_gaps_after_mapped_subset_candidate_matrix() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT]
```

- [ ] **Step 3: Add family candidate row builder**

Create `_paper_future_family_candidate_matrix_row(family_row)`:

```python
def _paper_future_family_candidate_matrix_row(
    family_row: dict[str, object],
) -> dict[str, object]:
    paper_primitive = str(family_row["paper_primitive"])
    input_decision = str(family_row["conversion_plan_decision"])
    runtime_kind = str(family_row["planned_runtime_kind"])
    current_count = int(family_row["current_row_evidence_count"])
    if input_decision == "plan_direct_native_mapping_later":
        decision = "native_family_review_only"
        future_candidate = True
        status = "future_family_review_candidate_no_current_rows"
    elif paper_primitive == "trapezoidal_prism" and current_count:
        decision = "blocked_unmapped_current_rows"
        future_candidate = False
        status = "not_current_candidate_unsupported_policy_block"
    else:
        decision = "blocked_approximation_policy_missing"
        future_candidate = False
        status = "not_current_candidate_mapping_or_approximation_missing"
    return {
        "candidate_matrix_row_id": (
            f"{family_row['family_conversion_plan_row_id']}:candidate_matrix"
        ),
        "source_conversion_plan_row_id": family_row["family_conversion_plan_row_id"],
        "paper_primitive": paper_primitive,
        "input_conversion_plan_decision": input_decision,
        "candidate_matrix_decision": decision,
        "candidate_runtime_kind": runtime_kind,
        "future_family_review_candidate": future_candidate,
        "current_row_evidence_count": current_count,
        "current_package_conversion_candidate_count": 0,
        "package_candidate_status": status,
        "package_conversion_enabled_by_this_gate": False,
        "claim_boundary": "review_row_not_package_ready",
        "primitive_spec_generation_triggered": False,
        "collision_package_generation_triggered": False,
        "runtime_admissibility_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }
```

- [ ] **Step 4: Add current row candidate builder**

Create `_paper_current_row_candidate_matrix_row(current_row)`:

```python
def _paper_current_row_candidate_matrix_row(
    current_row: dict[str, object],
) -> dict[str, object]:
    return {
        "candidate_matrix_row_id": (
            f"{current_row['conversion_plan_row_id']}:candidate_matrix"
        ),
        "source_conversion_plan_row_id": current_row["conversion_plan_row_id"],
        "source_policy_decision_id": current_row["source_policy_decision_id"],
        "source_adapter_decision_id": current_row["source_adapter_decision_id"],
        "source_output_id": current_row["source_output_id"],
        "evidence_case_id": current_row["evidence_case_id"],
        "offline_primitive_id": current_row["offline_primitive_id"],
        "paper_primitive": current_row["paper_primitive"],
        "offline_runtime_kind_label": current_row["offline_runtime_kind_label"],
        "input_conversion_plan_decision": current_row["conversion_plan_decision"],
        "candidate_matrix_decision": "blocked_unmapped_current_rows",
        "candidate_matrix_action": "keep_offline",
        "current_package_conversion_candidate": False,
        "package_candidate_status": "not_current_candidate_unsupported_policy_block",
        "required_later_gate": _PAPER_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT,
        "required_future_policy": (
            "explicit_mapping_or_approximation_policy_before_package_generation"
        ),
        "primitive_spec_generation_triggered": False,
        "collision_package_generation_triggered": False,
        "runtime_admissibility_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }
```

- [ ] **Step 5: Add payload builder**

Create `_paper_mapped_subset_conversion_candidate_matrix_payload(mapped_subset_plan)` with:

```python
future_rows = [
    _paper_future_family_candidate_matrix_row(row)
    for row in mapped_subset_plan["paper_primitive_family_conversion_plan_rows"]
]
current_rows = [
    _paper_current_row_candidate_matrix_row(row)
    for row in mapped_subset_plan["current_row_conversion_plan_rows"]
]
remaining_gaps = _paper_remaining_gaps_after_mapped_subset_candidate_matrix()
```

Return the payload with `candidate_matrix_contract`, `input_contract_summary`,
`future_family_candidate_matrix_rows`, `current_row_candidate_matrix_rows`, coverage summary,
explicit false trigger booleans, and the generated/admissibility false fields required by the
tests.

- [ ] **Step 6: Wire payload into `build_cpd_paper_offline_report()`**

Build the candidate matrix from the mapped-subset plan, update top-level:

```python
missing_before_paper_faithful = (
    _paper_remaining_gaps_after_mapped_subset_candidate_matrix()
)
failure_labels = ["paper_mapped_subset_adapter_preflight_contract_missing"]
next_required_gate = _PAPER_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT
```

Append `_PAPER_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX` to
`implemented_output_contract_scope` and add the payload to the report under
`"paper_mapped_subset_conversion_candidate_matrix"`.

- [ ] **Step 7: Run GREEN tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
```

Expected: pass.

### Task 3: Update Documentation And Registry

**Files:**
- Modify: `README.md`
- Modify: `docs/index.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/records/README.md`
- Modify: `experiments/registry.yaml`
- Add: `docs/records/2026-05-17-cpd-paper-mapped-subset-conversion-candidate-matrix.md`

- [ ] **Step 1: Update current-status prose**

Replace current-status wording that says the current next gate is
`paper_mapped_subset_conversion_candidate_matrix` with wording that says this gate is now closed
as an offline candidate matrix and the next gate is
`paper_mapped_subset_adapter_preflight_contract`.

- [ ] **Step 2: Tighten candidate wording**

Prefer "native-family review rows" and "future-family review candidates" over package-readiness
language. State explicitly that current package-conversion candidate count remains zero.

- [ ] **Step 3: Add dated record and registry entry**

Add a dated record and a matching complete registry entry after
`cpd-paper-package-conversion-mapped-subset-plan`.

- [ ] **Step 4: Run docs checks**

Run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

### Task 4: Review, Verify, Commit, Merge

**Files:**
- All changed files

- [ ] **Step 1: Request multi-agent review**

Request one implementation/schema review and one docs/claim-boundary review.

- [ ] **Step 2: Fix Critical and Important review findings**

Evaluate every finding against the codebase and fix valid issues. Fix low-risk naming or test
coverage findings when cheap.

- [ ] **Step 3: Run final verification**

Run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
python -m pytest -q
PYTHONPATH=src python - <<'PY'
from primitive_collision_compiler.baselines.cpd_paper.offline import build_cpd_paper_offline_report
report = build_cpd_paper_offline_report()
payload = report["paper_mapped_subset_conversion_candidate_matrix"]
summary = payload["coverage_summary"]
assert report["next_required_gate"] == "paper_mapped_subset_adapter_preflight_contract"
assert report["failure_labels"] == ["paper_mapped_subset_adapter_preflight_contract_missing"]
assert summary["future_family_review_candidate_count"] == 3
assert summary["current_package_conversion_candidate_count"] == 0
assert summary["current_blocked_requires_policy_count"] == 16
assert payload["primitive_spec_generated"] is False
assert payload["collision_package_generated"] is False
assert payload["runtime_admissibility_checked"] is False
assert payload["newton_runtime_triggered"] is False
print("candidate matrix smoke passed")
PY
```

Expected: all pass.

- [ ] **Step 4: Commit and integrate**

Commit the slice, fast-forward merge to `main`, push `main`, remove the worktree, close agents,
and verify main with docs checks plus focused pytest.
