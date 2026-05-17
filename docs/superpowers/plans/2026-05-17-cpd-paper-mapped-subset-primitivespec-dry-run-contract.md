# CPD Paper Mapped-Subset PrimitiveSpec Dry-Run Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the command-only offline `paper_mapped_subset_primitivespec_dry_run_contract` gate without generating real `PrimitiveSpec` objects, `CollisionPackage`s, Newton runtime work, real-USD runs, benchmark evidence, or collision-quality claims.

**Architecture:** Extend the existing CPD paper offline report builder with one more validated payload after `paper_mapped_subset_adapter_preflight_contract`. The new payload copies family/current preflight rows into PrimitiveSpec dry-run requirement/no-op rows, keeps all counts at zero for current candidates, and advances the next gate to `paper_mapped_subset_primitivespec_validation_contract`.

**Tech Stack:** Python, pytest, existing CPD paper offline report, Markdown docs, YAML experiment registry.

---

## File Map

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
  - Add the validation-contract gate constant.
  - Add remaining-gap helper after PrimitiveSpec dry-run.
  - Add PrimitiveSpec dry-run row builders and input validator.
  - Wire payload into `build_cpd_paper_offline_report`.
- Modify: `tests/test_cpd_paper_offline.py`
  - Add RED tests for payload shape, rows, false trigger flags, and validation failures.
- Modify: `tests/test_cli.py`
  - Add CLI JSON assertions for the new payload and updated top-level next gate.
- Modify docs:
  - `README.md`
  - `docs/index.md`
  - `docs/deepdive/evidence-status.md`
  - `docs/reference/claim-boundaries.md`
  - `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
  - `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
  - `docs/reference/cpd-paper-reproduction-gap-matrix.md`
  - `docs/reference/cpd-paper-story-status.md`
  - `docs/records/README.md`
  - `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-dry-run-contract.md`
  - `experiments/registry.yaml`

## Task 1: Add RED Tests For The New Payload

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`

- [ ] **Step 1: Add imports and constants**

Add `_paper_mapped_subset_primitivespec_dry_run_contract_payload` to the import block. Add:

```python
EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT = (
    "paper_mapped_subset_primitivespec_dry_run_contract"
)
EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT = (
    "paper_mapped_subset_primitivespec_validation_contract"
)
EXPECTED_PRIMITIVESPEC_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT,
]
```

- [ ] **Step 2: Update existing expected top-level labels**

Change the current top-level `EXPECTED_GENERALIZATION_FAILURE_LABELS` and
`EXPECTED_PREFLIGHT_REMAINING_GAPS` usage so the top-level report after this slice expects:

```python
[
    "paper_mapped_subset_primitivespec_validation_contract_missing",
]
```

Keep the adapter-preflight payload's own `remaining_gaps` as
`["paper_mapped_subset_primitivespec_dry_run_contract"]`.

- [ ] **Step 3: Add payload shape test**

Append this test near the existing adapter-preflight tests:

```python
def test_cpd_paper_records_mapped_subset_primitivespec_dry_run_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_primitivespec_dry_run_contract"]

    assert report["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT
    )
    assert report["failure_labels"] == [
        "paper_mapped_subset_primitivespec_validation_contract_missing",
    ]
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_PRIMITIVESPEC_REMAINING_GAPS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )

    assert payload["gate_id"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT
    assert payload["gate_status"] == (
        "implemented_offline_primitivespec_dry_run_contract_only_partial"
    )
    assert payload["closed_gate"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT
    assert payload["input_gate_id"] == EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT
    assert (
        payload["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "primitivespec_dry_run_contract_complete_"
        "primitivespec_validation_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "offline_primitivespec_dry_run_contract_not_primitivespec_"
        "not_collision_package"
    )
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_PRIMITIVESPEC_REMAINING_GAPS
```

- [ ] **Step 4: Add family requirement row test**

Add a test asserting:

```python
rows = {
    row["paper_primitive"]: row
    for row in payload["primitive_spec_dry_run_requirement_rows"]
}
assert list(rows) == [
    "oriented_bounding_box",
    "sphere",
    "capsule",
    "capped_cylinder",
    "frustum",
    "trapezoidal_prism",
]
assert rows["oriented_bounding_box"]["future_primitive_spec_kind"] == "box"
assert rows["sphere"]["future_primitive_spec_kind"] == "sphere"
assert rows["capsule"]["future_primitive_spec_kind"] == "capsule"
assert rows["capped_cylinder"]["primitive_spec_dry_run_decision"] == (
    "blocked_approximation_policy_missing"
)
assert rows["frustum"]["primitive_spec_dry_run_decision"] == (
    "blocked_approximation_policy_missing"
)
assert rows["trapezoidal_prism"]["primitive_spec_dry_run_decision"] == (
    "noop_current_unmapped_rows_keep_offline"
)
```

- [ ] **Step 5: Add current-row no-op test**

Add a test asserting:

```python
summary = payload["coverage_summary"]
rows = payload["current_row_primitivespec_dry_run_rows"]
assert summary["primitive_spec_requirement_row_count"] == 6
assert summary["future_native_primitivespec_shape_record_count"] == 3
assert summary["blocked_primitivespec_requirement_row_count"] == 2
assert summary["noop_primitivespec_requirement_row_count"] == 1
assert summary["current_row_primitivespec_dry_run_row_count"] == 16
assert summary["current_primitivespec_dry_run_pass_record_count"] == 0
assert summary["current_primitivespec_noop_record_count"] == 16
assert summary["primitive_spec_candidate_record_count"] == 0
assert summary["generated_primitive_spec_record_count"] == 0
assert summary["current_paper_primitive_distribution"] == {
    "trapezoidal_prism": 16,
}
assert summary["current_runtime_kind_distribution"] == {
    "offline_only_unmapped": 16,
}
for row in rows:
    assert row["primitive_spec_dry_run_decision"] == "skip_unmapped_current_row"
    assert row["primitive_spec_dry_run_action"] == "keep_offline"
    assert row["primitive_spec_dry_run_passed"] is False
    assert row["primitive_spec_candidate"] is False
    assert row["generated_primitive_spec"] is None
```

- [ ] **Step 6: Add report-only boundary test**

Add a test that mirrors `test_cpd_paper_adapter_preflight_stays_report_only`, asserting the new
payload and all rows do not contain `"PrimitiveSpec"`, `"CollisionPackage"`, `"runtime_result"`,
`"usd_asset_path"`, `"benchmark_metric"`, `"surface_distance"`, or `"collision_quality"` keys, and
that all trigger flags stay false.

- [ ] **Step 7: Add validation-failure tests**

Add tests that call `_paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)` and
expect `ValueError` for:

- wrong `gate_id`: `primitivespec_dry_run_input_gate_id_mismatch`;
- top-level true trigger flag: `input_trigger_flag_true`;
- nonzero `candidate_count_at_preflight`: `input_primitivespec_candidate_count_nonzero`;
- nonzero coverage `current_preflight_pass_record_count`: `input_preflight_pass_count_nonzero`;
- row-level `adapter_preflight_passed=True`: `input_preflight_pass_count_nonzero`;
- row-level `current_package_conversion_candidate=True`: `input_primitivespec_candidate_count_nonzero`;
- duplicate `adapter_preflight_row_id`: `duplicate_adapter_preflight_row_id`;
- unknown family decision: `unknown_adapter_preflight_family_decision`;
- missing current source id: `missing_current_row_source_id`;
- wrong `required_later_gate`: `current_row_required_later_gate_mismatch`.

- [ ] **Step 8: Run RED focused tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k 'primitivespec_dry_run or offline_report_next_gate or cli' -q
```

Expected: fail because `_paper_mapped_subset_primitivespec_dry_run_contract_payload` and the new
payload do not exist yet.

## Task 2: Implement The Offline Payload

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add constants and remaining-gap helper**

Add:

```python
_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT = (
    "paper_mapped_subset_primitivespec_validation_contract"
)


def _paper_remaining_gaps_after_mapped_subset_primitivespec_dry_run() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT]
```

- [ ] **Step 2: Add family row builder**

Implement `_paper_primitivespec_dry_run_requirement_row(row)`:

- input `future_native_family_preflight_recorded_only` maps to
  `future_native_family_primitivespec_shape_recorded_only`;
- `blocked_approximation_policy_missing` stays blocked;
- `noop_current_unmapped_rows_keep_offline` stays no-op;
- unknown decision raises `ValueError("unknown_adapter_preflight_family_decision:<decision>")`.

The returned row must include:

```python
"primitive_spec_dry_run_row_id": f"{row['adapter_preflight_row_id']}:primitivespec_dry_run"
"source_adapter_preflight_row_id": row["adapter_preflight_row_id"]
"paper_primitive": row["paper_primitive"]
"candidate_runtime_kind": row["candidate_runtime_kind"]
"future_primitive_spec_kind": row["candidate_runtime_kind"] if recorded else None
"required_primitive_spec_fields": [
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
"primitive_spec_generation_triggered": False
"collision_package_generation_triggered": False
```

- [ ] **Step 3: Add current-row builder**

Implement `_paper_primitivespec_dry_run_current_row(row)` preserving source ids and emitting the
no-op row fields from Task 1.

- [ ] **Step 4: Add validator**

Implement `_paper_validate_primitivespec_dry_run_preflight(preflight)` with the validation labels
from Task 1 Step 7.

- [ ] **Step 5: Add payload builder**

Implement `_paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)` returning the
payload fields, rows, coverage summary, `remaining_gaps`, and all false trigger flags described in
the design doc.

- [ ] **Step 6: Wire into report builder**

In `build_cpd_paper_offline_report()`:

- build `mapped_subset_primitivespec_dry_run` after adapter preflight;
- set `missing_before_paper_faithful` from
  `_paper_remaining_gaps_after_mapped_subset_primitivespec_dry_run()`;
- set top-level `next_required_gate` to
  `_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT`;
- set top-level `failure_labels` to
  `["paper_mapped_subset_primitivespec_validation_contract_missing"]`;
- append `_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT` to
  `implemented_output_contract_scope`;
- add `"paper_mapped_subset_primitivespec_dry_run_contract": mapped_subset_primitivespec_dry_run`
  to the returned report.

- [ ] **Step 7: Run focused tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k 'primitivespec_dry_run or offline_report_next_gate' -q
```

Expected: pass for the new focused tests.

## Task 3: Update CLI Assertions

**Files:**
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Update top-level CLI expectations**

In `test_cli_run_cpd_paper_offline_report_emits_json`, change:

```python
payload["failure_labels"]
payload["next_required_gate"]
payload["paper_faithfulness"]["missing_before_paper_faithful_offline"]
payload["paper_faithfulness"]["implemented_output_contract_scope"]
```

to expect the validation contract as the next gate and include
`paper_mapped_subset_primitivespec_dry_run_contract` in the implemented output scope.

- [ ] **Step 2: Add CLI payload assertions**

After the adapter-preflight CLI assertions, add:

```python
dry_run = payload["paper_mapped_subset_primitivespec_dry_run_contract"]
assert dry_run["gate_id"] == "paper_mapped_subset_primitivespec_dry_run_contract"
assert dry_run["input_gate_id"] == "paper_mapped_subset_adapter_preflight_contract"
assert dry_run["next_required_gate"] == (
    "paper_mapped_subset_primitivespec_validation_contract"
)
assert dry_run["generated_primitive_spec_count"] == 0
assert dry_run["coverage_summary"]["primitive_spec_requirement_row_count"] == 6
assert dry_run["coverage_summary"]["future_native_primitivespec_shape_record_count"] == 3
assert dry_run["coverage_summary"]["current_row_primitivespec_dry_run_row_count"] == 16
assert dry_run["coverage_summary"]["primitive_spec_candidate_record_count"] == 0
assert dry_run["primitive_spec_generated"] is False
assert dry_run["collision_package_generated"] is False
assert dry_run["runtime_admissibility_checked"] is False
assert dry_run["newton_support_claimed"] is False
assert dry_run["package_generation_triggered"] is False
assert dry_run["newton_runtime_triggered"] is False
assert dry_run["real_usd_triggered"] is False
assert dry_run["benchmark_triggered"] is False
```

- [ ] **Step 3: Run CLI test**

Run:

```bash
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Expected: pass.

## Task 4: Update Docs And Registry

**Files:**
- Modify docs listed in File Map.
- Create: `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-dry-run-contract.md`

- [ ] **Step 1: Add dated record**

Create a short record with:

- status complete;
- changes: command-only PrimitiveSpec dry-run contract, six requirement rows, 16 no-op rows, zero
  current candidates, zero generated specs;
- verification commands;
- claim impact: no PrimitiveSpec generation, no CollisionPackage, no Newton, no real-USD, no
  benchmark, no collision-quality claim;
- next action: `paper_mapped_subset_primitivespec_validation_contract`.

- [ ] **Step 2: Update canonical docs**

In every active doc, move "current next gate" from
`paper_mapped_subset_primitivespec_dry_run_contract` to
`paper_mapped_subset_primitivespec_validation_contract`, while preserving historical wording for
previous records as "at that stage".

- [ ] **Step 3: Update claim-boundary forbidden wording**

Add a forbidden wording bullet:

```md
- Do not describe `paper_mapped_subset_primitivespec_dry_run_contract` as PrimitiveSpec
  readiness, PrimitiveSpec generation, package readiness, package conversion execution,
  CollisionPackage generation, runtime admissibility, Newton support, or Newton execution.
```

- [ ] **Step 4: Update registry**

Add a `cpd-paper-mapped-subset-primitivespec-dry-run-contract` entry after the adapter-preflight
entry in `experiments/registry.yaml`, with explicit no-claim bullets.

- [ ] **Step 5: Validate docs**

Run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

## Task 5: Review, Verify, Commit, Merge, Push

**Files:** all changed files.

- [ ] **Step 1: Run focused verification**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
```

Expected: all pass.

- [ ] **Step 2: Run full verification**

Run:

```bash
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

- [ ] **Step 3: Request review**

Ask one implementation reviewer to inspect code/tests and one docs reviewer to inspect claim
boundaries. Fix any blocking feedback and rerun focused checks.

- [ ] **Step 4: Commit implementation**

Run:

```bash
git add README.md docs experiments src tests
git commit -m "feat: add CPD PrimitiveSpec dry-run contract"
```

- [ ] **Step 5: Merge and push**

In the main worktree:

```bash
git merge --ff-only cpd-paper-primitivespec-dry-run-contract
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
git push origin main
```

- [ ] **Step 6: Clean worktree**

Run:

```bash
git worktree remove /cpfs/user/zhuzihou/dev/physics-primitive-agent/.worktrees/cpd-paper-primitivespec-dry-run-contract
git branch -d cpd-paper-primitivespec-dry-run-contract
```

Leave unrelated older worktrees alone unless a separate cleanup decision is made.

## Self-Review

- Spec coverage: the plan implements the dry-run payload, validation, CLI assertions, docs, record,
  registry, review, verification, merge, push, and cleanup.
- Placeholder scan: no incomplete placeholder markers remain.
- Type consistency: all gate names match the design doc and use existing report dictionary style.
