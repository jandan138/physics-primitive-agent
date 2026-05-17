# CPD Paper Mapped-Subset Adapter Preflight Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the offline-only `paper_mapped_subset_adapter_preflight_contract` gate to `cpd_paper_offline_report`.

**Architecture:** Extend `src/primitive_collision_compiler/baselines/cpd_paper/offline.py` with a preflight payload that consumes `paper_mapped_subset_conversion_candidate_matrix`. The payload records family preflight requirements and current-row no-op behavior, advances to `paper_mapped_subset_primitivespec_dry_run_contract`, and keeps all package/runtime/real-USD/benchmark triggers false.

**Tech Stack:** Python, pytest, Markdown docs, YAML registry, existing CLI JSON report command.

---

### Task 1: Add RED Tests

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add test constants**

In `tests/test_cpd_paper_offline.py`, add:

```python
EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT = (
    "paper_mapped_subset_primitivespec_dry_run_contract"
)
EXPECTED_PREFLIGHT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT,
]
```

Update `EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS` and
`EXPECTED_GENERALIZATION_FAILURE_LABELS` to point at
`EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT` after the preflight payload is wired.

- [ ] **Step 2: Write failing offline-report preflight gate test**

Add:

```python
def test_cpd_paper_records_mapped_subset_adapter_preflight_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_adapter_preflight_contract"]

    assert report["next_required_gate"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT
    assert report["failure_labels"] == [
        "paper_mapped_subset_primitivespec_dry_run_contract_missing",
    ]
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_PREFLIGHT_REMAINING_GAPS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert payload["gate_id"] == EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT
    assert payload["gate_status"] == (
        "implemented_offline_adapter_preflight_contract_only_partial"
    )
    assert payload["closed_gate"] == EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT
    assert payload["input_gate_id"] == EXPECTED_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX
    assert payload["next_required_gate"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT
    assert payload["decision"] == "remain_partial"
    assert (
        payload["decision_reason"]
        == "adapter_preflight_contract_complete_primitivespec_dry_run_contract_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == (
        "offline_adapter_preflight_contract_not_primitivespec_not_collision_package"
    )
    assert payload["candidate_count_at_preflight"] == 0
    assert payload["preflight_action"] == "no_op_keep_offline"
    assert payload["remaining_gaps"] == EXPECTED_PREFLIGHT_REMAINING_GAPS
```

- [ ] **Step 3: Write failing family preflight test**

Add:

```python
def test_cpd_paper_adapter_preflight_records_family_requirements():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_adapter_preflight_contract"]
    rows = {
        row["paper_primitive"]: row
        for row in payload["adapter_preflight_requirement_rows"]
    }

    assert list(rows) == [
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
    for primitive_name, runtime_kind in {
        "oriented_bounding_box": "box",
        "sphere": "sphere",
        "capsule": "capsule",
    }.items():
        row = rows[primitive_name]
        assert row["candidate_runtime_kind"] == runtime_kind
        assert (
            row["adapter_preflight_decision"]
            == "future_native_family_preflight_recorded_only"
        )
        assert row["future_native_family_preflight_recorded"] is True
        assert row["current_package_conversion_candidate_count"] == 0
        assert row["package_generation_enabled_by_this_gate"] is False

    for primitive_name in ("capped_cylinder", "frustum"):
        row = rows[primitive_name]
        assert row["candidate_runtime_kind"] == "offline_only_unmapped"
        assert (
            row["adapter_preflight_decision"]
            == "blocked_approximation_policy_missing"
        )
        assert row["future_native_family_preflight_recorded"] is False

    trapezoid = rows["trapezoidal_prism"]
    assert (
        trapezoid["adapter_preflight_decision"]
        == "noop_current_unmapped_rows_keep_offline"
    )
    assert trapezoid["current_row_evidence_count"] == 16
```

- [ ] **Step 4: Write failing current-row preflight test**

Add:

```python
def test_cpd_paper_adapter_preflight_noops_current_unmapped_rows():
    report = build_cpd_paper_offline_report()
    matrix = report["paper_mapped_subset_conversion_candidate_matrix"]
    payload = report["paper_mapped_subset_adapter_preflight_contract"]
    summary = payload["coverage_summary"]
    rows = payload["current_row_adapter_preflight_rows"]

    assert summary["family_preflight_requirement_row_count"] == 6
    assert summary["future_native_family_preflight_record_count"] == 3
    assert summary["blocked_family_preflight_record_count"] == 3
    assert summary["current_row_adapter_preflight_row_count"] == 16
    assert summary["current_preflight_pass_record_count"] == 0
    assert summary["current_preflight_noop_record_count"] == 16
    assert summary["current_package_conversion_candidate_count"] == 0
    assert summary["package_candidate_record_count"] == 0
    assert summary["current_paper_primitive_distribution"] == {
        "trapezoidal_prism": 16,
    }
    assert summary["current_runtime_kind_distribution"] == {
        "offline_only_unmapped": 16,
    }

    matrix_rows = matrix["current_row_candidate_matrix_rows"]
    assert len(rows) == len(matrix_rows) == 16
    for row, upstream_row in zip(rows, matrix_rows):
        assert row["source_candidate_matrix_row_id"] == upstream_row[
            "candidate_matrix_row_id"
        ]
        assert row["paper_primitive"] == "trapezoidal_prism"
        assert row["offline_runtime_kind_label"] == "offline_only_unmapped"
        assert row["input_candidate_matrix_decision"] == "blocked_unmapped_current_rows"
        assert (
            row["adapter_preflight_decision"]
            == "noop_keep_offline_unmapped_current_row"
        )
        assert row["current_package_conversion_candidate"] is False
        assert row["adapter_preflight_passed"] is False
        assert row["package_generation_enabled_by_this_gate"] is False
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
def test_cpd_paper_adapter_preflight_stays_report_only():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_adapter_preflight_contract"]

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
    assert payload["adapter_preflight_contract"][
        "primitive_spec_generation_allowed"
    ] is False
    assert payload["adapter_preflight_contract"][
        "collision_package_generation_allowed"
    ] is False
    assert payload["adapter_preflight_contract"]["newton_runtime_allowed"] is False
    assert payload["adapter_preflight_contract"][
        "runtime_admissibility_supported"
    ] is False
    assert payload["adapter_preflight_contract"]["silent_drop_allowed"] is False
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    for row in payload["adapter_preflight_requirement_rows"]:
        assert forbidden_keys.isdisjoint(row)
    for row in payload["current_row_adapter_preflight_rows"]:
        assert forbidden_keys.isdisjoint(row)
```

- [ ] **Step 6: Extend CLI test**

In `test_cli_run_cpd_paper_offline_report_emits_json`, update top-level expectations to:

```python
assert payload["failure_labels"] == [
    "paper_mapped_subset_primitivespec_dry_run_contract_missing",
]
assert payload["next_required_gate"] == "paper_mapped_subset_primitivespec_dry_run_contract"
```

Add assertions for:

```python
preflight = payload["paper_mapped_subset_adapter_preflight_contract"]
assert preflight["gate_id"] == "paper_mapped_subset_adapter_preflight_contract"
assert preflight["input_gate_id"] == "paper_mapped_subset_conversion_candidate_matrix"
assert preflight["next_required_gate"] == "paper_mapped_subset_primitivespec_dry_run_contract"
assert preflight["coverage_summary"]["family_preflight_requirement_row_count"] == 6
assert preflight["coverage_summary"]["future_native_family_preflight_record_count"] == 3
assert preflight["coverage_summary"]["current_row_adapter_preflight_row_count"] == 16
assert preflight["coverage_summary"]["current_preflight_pass_record_count"] == 0
assert preflight["coverage_summary"]["current_package_conversion_candidate_count"] == 0
assert preflight["package_generation_triggered"] is False
assert preflight["newton_runtime_triggered"] is False
```

- [ ] **Step 7: Run RED tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
```

Expected: fail because `paper_mapped_subset_adapter_preflight_contract` and
`paper_mapped_subset_primitivespec_dry_run_contract` are not wired yet.

### Task 2: Implement Offline Adapter Preflight Payload

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add next-gate constant**

Add near the existing paper gate constants:

```python
_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT = (
    "paper_mapped_subset_primitivespec_dry_run_contract"
)
```

- [ ] **Step 2: Add remaining-gap helper**

Add:

```python
def _paper_remaining_gaps_after_mapped_subset_adapter_preflight() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT]
```

- [ ] **Step 3: Add family preflight row helper**

Implement a helper that consumes each `future_family_candidate_matrix_rows` row and emits:

```python
{
    "adapter_preflight_row_id": f"{row['candidate_matrix_row_id']}:adapter_preflight",
    "source_candidate_matrix_row_id": row["candidate_matrix_row_id"],
    "paper_primitive": row["paper_primitive"],
    "candidate_runtime_kind": row["candidate_runtime_kind"],
    "input_candidate_matrix_decision": row["candidate_matrix_decision"],
    "adapter_preflight_decision": decision,
    "future_native_family_preflight_recorded": decision
        == "future_native_family_preflight_recorded_only",
    "current_row_evidence_count": row["current_row_evidence_count"],
    "current_package_conversion_candidate_count": row[
        "current_package_conversion_candidate_count"
    ],
    "package_generation_enabled_by_this_gate": False,
    "primitive_spec_generation_triggered": False,
    "collision_package_generation_triggered": False,
    "runtime_admissibility_triggered": False,
    "newton_runtime_triggered": False,
    "real_usd_triggered": False,
    "benchmark_triggered": False,
}
```

Decision mapping:

```python
native_family_review_only -> future_native_family_preflight_recorded_only
blocked_approximation_policy_missing -> blocked_approximation_policy_missing
blocked_unmapped_current_rows -> noop_current_unmapped_rows_keep_offline
```

- [ ] **Step 4: Add current-row preflight helper**

Implement a helper that consumes each `current_row_candidate_matrix_rows` row and emits:

```python
{
    "adapter_preflight_row_id": f"{row['candidate_matrix_row_id']}:adapter_preflight",
    "source_candidate_matrix_row_id": row["candidate_matrix_row_id"],
    "source_conversion_plan_row_id": row["source_conversion_plan_row_id"],
    "source_policy_decision_id": row["source_policy_decision_id"],
    "source_adapter_decision_id": row["source_adapter_decision_id"],
    "source_output_id": row["source_output_id"],
    "evidence_case_id": row["evidence_case_id"],
    "offline_primitive_id": row["offline_primitive_id"],
    "paper_primitive": row["paper_primitive"],
    "offline_runtime_kind_label": row["offline_runtime_kind_label"],
    "input_candidate_matrix_decision": row["candidate_matrix_decision"],
    "adapter_preflight_decision": "noop_keep_offline_unmapped_current_row",
    "adapter_preflight_action": "keep_offline",
    "current_package_conversion_candidate": False,
    "adapter_preflight_passed": False,
    "package_generation_enabled_by_this_gate": False,
    "required_later_gate": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT,
    "required_future_policy": row["required_future_policy"],
    "primitive_spec_generation_triggered": False,
    "collision_package_generation_triggered": False,
    "runtime_admissibility_triggered": False,
    "newton_runtime_triggered": False,
    "real_usd_triggered": False,
    "benchmark_triggered": False,
}
```

- [ ] **Step 5: Add preflight payload helper**

Add `_paper_mapped_subset_adapter_preflight_contract_payload(candidate_matrix)` returning the
payload shape from the design spec, including:

```python
"adapter_preflight_contract": {
    "candidate_matrix_required": True,
    "candidate_matrix_input_gate_required": (
        _PAPER_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX
    ),
    "unique_row_ids_required": True,
    "complete_source_evidence_ids_required": True,
    "zero_current_package_candidates_required": True,
    "no_silent_drop_required": True,
    "primitive_spec_generation_allowed": False,
    "collision_package_generation_allowed": False,
    "package_generation_allowed": False,
    "newton_runtime_allowed": False,
    "runtime_admissibility_supported": False,
    "approximation_policy_enabled": False,
    "silent_drop_allowed": False,
}
```

- [ ] **Step 6: Wire payload into top-level report**

In `build_cpd_paper_offline_report()`:

- build `mapped_subset_adapter_preflight` after `mapped_subset_candidate_matrix`;
- set `missing_before_paper_faithful` to
  `_paper_remaining_gaps_after_mapped_subset_adapter_preflight()`;
- set top-level `next_required_gate` to `_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT`;
- add `_PAPER_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT` to
  `paper_faithfulness["implemented_output_contract_scope"]`;
- add `"paper_mapped_subset_adapter_preflight_contract": mapped_subset_adapter_preflight` to the
  returned report.

- [ ] **Step 7: Run GREEN tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
```

Expected: all focused tests pass.

### Task 3: Update Durable Documentation

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
- Create: `docs/records/2026-05-17-cpd-paper-mapped-subset-adapter-preflight-contract.md`

- [ ] **Step 1: Add dated record**

Create a record that states:

```text
The partial CPD paper offline report now contains a command-only offline mapped-subset adapter
preflight contract over deterministic synthetic fixture records. It consumes the mapped-subset
candidate matrix, records preflight requirements, records no-op behavior for the current zero
package-conversion-candidate state, keeps all current unmapped trapezoidal-prism rows offline, and
advances the next gate to `paper_mapped_subset_primitivespec_dry_run_contract`.
```

Also state explicitly that it does not generate `PrimitiveSpec`, does not generate
`CollisionPackage`, does not run runtime admissibility, Newton, real USD, or benchmark diagnostics,
and does not claim collision quality or safety.

- [ ] **Step 2: Update index and story docs**

Update `README.md`, `docs/index.md`, `docs/reference/cpd-paper-story-status.md`,
`docs/reference/cpd-paper-reproduction-gap-matrix.md`,
`docs/reference/cpd-paper-faithful-offline-lane-spec.md`, and
`docs/reference/cpd-paper-fixture-breadth-expansion-plan.md` so they say the preflight contract is
implemented and the next gate is `paper_mapped_subset_primitivespec_dry_run_contract`.

- [ ] **Step 3: Update claim/evidence docs**

Update `docs/reference/claim-boundaries.md` and `docs/deepdive/evidence-status.md` to include the
preflight contract as offline command-only evidence, with the same false-trigger boundary.

- [ ] **Step 4: Update records index and registry**

Add the new record to `docs/records/README.md`. Add an `experiments/registry.yaml` entry near the
candidate matrix entry with the existing command-only report command and conservative claims.

- [ ] **Step 5: Validate docs**

Run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

### Task 4: Review, Verify, Commit, Merge

**Files:**
- All changed files.

- [ ] **Step 1: Run full verification**

Run:

```bash
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

- [ ] **Step 2: Run report smoke**

Run:

```bash
python -m primitive_collision_compiler.cli cpd-paper-offline-report --pretty
```

Expected: JSON includes `paper_mapped_subset_adapter_preflight_contract`, top-level
`next_required_gate: paper_mapped_subset_primitivespec_dry_run_contract`, and zero current package
conversion/preflight pass counts.

- [ ] **Step 3: Request multi-agent review**

Dispatch at least two reviewers:

- implementation/schema reviewer for tests and `offline.py`;
- docs/claim-boundary reviewer for docs, record, registry, and stale wording.

Fix Critical and Important findings, and fix cheap Low findings where practical. Re-run focused
verification after fixes.

- [ ] **Step 4: Commit and merge**

Commit with:

```bash
git add src/primitive_collision_compiler/baselines/cpd_paper/offline.py \
  tests/test_cpd_paper_offline.py tests/test_cli.py README.md docs experiments
git commit -m "feat: add CPD mapped subset adapter preflight contract"
```

Then merge fast-forward to `main`, push to `origin/main`, and remove the feature worktree and
branch after final verification on main.
