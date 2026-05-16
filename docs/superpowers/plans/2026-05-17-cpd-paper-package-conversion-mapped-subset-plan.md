# CPD Paper Package Conversion Mapped-Subset Plan Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the offline-only `paper_package_conversion_mapped_subset_plan` gate to `cpd_paper_offline_report`.

**Architecture:** Extend `src/primitive_collision_compiler/baselines/cpd_paper/offline.py` with a planning payload that consumes `paper_package_adapter_unsupported_primitive_policy`. The payload emits family conversion-plan rows and current row conversion-plan rows. It does not create packages, primitive specs, runtime-admissibility results, Newton diagnostics, real-USD reports, or benchmark metrics.

**Tech Stack:** Python, pytest, Markdown docs, YAML registry, existing CLI JSON report command.

---

### Task 1: Add RED Tests

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write failing offline-report tests**

Add tests that assert:

```python
def test_cpd_paper_records_package_conversion_mapped_subset_plan_gate():
    report = build_cpd_paper_offline_report()
    payload = report["paper_package_conversion_mapped_subset_plan"]

    assert report["next_required_gate"] == "paper_mapped_subset_conversion_candidate_matrix"
    assert report["failure_labels"] == ["paper_mapped_subset_conversion_candidate_matrix_missing"]
    assert payload["gate_id"] == "paper_package_conversion_mapped_subset_plan"
    assert payload["input_gate_id"] == "paper_package_adapter_unsupported_primitive_policy"
    assert payload["next_required_gate"] == "paper_mapped_subset_conversion_candidate_matrix"
    assert payload["package_generation_allowed"] is False
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
```

Also add tests for six family rows, 16 current row-plan rows, zero candidates, and no forbidden
runtime/package keys.

- [ ] **Step 2: Write failing CLI test**

Extend `test_cli_run_cpd_paper_offline_report_emits_json` to assert the new top-level gate,
failure label, and mapped-subset payload summary.

- [ ] **Step 3: Run RED tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
```

Expected: fail because `paper_package_conversion_mapped_subset_plan` and
`paper_mapped_subset_conversion_candidate_matrix` do not exist yet.

### Task 2: Implement Offline Mapped-Subset Planning Payload

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add next-gate constant**

Add:

```python
_PAPER_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX = (
    "paper_mapped_subset_conversion_candidate_matrix"
)
```

- [ ] **Step 2: Add remaining-gap helper**

Add:

```python
def _paper_remaining_gaps_after_conversion_mapped_subset_plan() -> list[str]:
    return [_PAPER_PACKAGE_CONVERSION_CONTRACT]
```

- [ ] **Step 3: Add family conversion-plan row builder**

Create six rows from the unsupported-policy family rows. Native candidate families should be
marked `planned_for_future_mapped_subset`; unsupported families should be
`excluded_until_explicit_mapping_or_approximation_policy`.

- [ ] **Step 4: Add current conversion-plan row builder**

Convert every current unsupported-policy row into a conversion-plan row. Current
`trapezoidal_prism` / `offline_only_unmapped` rows must be excluded and kept offline.

- [ ] **Step 5: Add payload builder**

Add `_paper_package_conversion_mapped_subset_plan_payload(unsupported_payload)` with gate
metadata, planning tables, coverage counts, remaining gaps, and false trigger booleans.

- [ ] **Step 6: Wire payload into `build_cpd_paper_offline_report()`**

Build the mapped-subset plan payload from the unsupported-policy payload, update top-level
`missing_before_paper_faithful`, `failure_labels`, `next_required_gate`, and
`implemented_output_contract_scope`, then add the new payload to the report.

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
- Add: `docs/records/2026-05-17-cpd-paper-package-conversion-mapped-subset-plan.md`

- [ ] **Step 1: Update current-status prose**

Replace statements that say the current next gate is
`paper_package_conversion_mapped_subset_plan` with wording that says this gate is now closed as
offline mapped-subset planning and the next gate is `paper_mapped_subset_conversion_candidate_matrix`.

- [ ] **Step 2: Tighten claim boundaries**

Add explicit language that this gate is not package readiness, package generation, Newton support,
runtime admissibility, approximation support, or package-conversion execution.

- [ ] **Step 3: Add dated record and registry entry**

Add a dated record and matching complete registry entry after
`cpd-paper-package-adapter-unsupported-primitive-policy`.

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

Evaluate every finding against the codebase and fix valid issues.

- [ ] **Step 3: Run final verification**

Run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
python -m pytest -q
```

Expected: all pass.

- [ ] **Step 4: Commit and integrate**

Commit the slice, fast-forward merge to `main`, push `main`, remove the worktree, and verify main
with docs checks plus focused pytest.
