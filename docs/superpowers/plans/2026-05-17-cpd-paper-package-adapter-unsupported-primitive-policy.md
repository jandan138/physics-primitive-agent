# CPD Paper Package-Adapter Unsupported Primitive Policy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the offline-only `paper_package_adapter_unsupported_primitive_policy` gate to `cpd_paper_offline_report`.

**Architecture:** The implementation extends the existing CPD paper offline report builder in
`src/primitive_collision_compiler/baselines/cpd_paper/offline.py`. It consumes the existing
`paper_package_adapter_contract` payload and emits a policy payload with family-level primitive
policy rows plus current adapter decision policy rows. The report remains partial and advances to
`paper_package_conversion_mapped_subset_plan`.

**Tech Stack:** Python, pytest, Markdown docs, YAML registry, existing CLI JSON report command.

---

### Task 1: Add RED Tests For Unsupported Primitive Policy

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write the failing offline-report tests**

Add tests that assert:

```python
def test_cpd_paper_offline_report_records_unsupported_primitive_policy_gate():
    report = build_cpd_paper_offline_report()

    assert report["next_required_gate"] == "paper_package_conversion_mapped_subset_plan"
    assert report["failure_labels"] == [
        "paper_package_conversion_mapped_subset_plan_missing"
    ]
    assert (
        "paper_package_adapter_unsupported_primitive_policy"
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )

    payload = report["paper_package_adapter_unsupported_primitive_policy"]
    assert payload["gate_id"] == "paper_package_adapter_unsupported_primitive_policy"
    assert payload["input_gate_id"] == "paper_package_adapter_contract"
    assert payload["next_required_gate"] == "paper_package_conversion_mapped_subset_plan"
    assert payload["package_generation_allowed"] is False
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
```

Also add tests for six primitive-family rows, 16 current decision policy rows, and no forbidden
runtime/package keys.

- [ ] **Step 2: Write the failing CLI test**

Extend the existing CPD paper offline CLI JSON test so it asserts the new top-level gate, failure
label, and unsupported-policy payload.

- [ ] **Step 3: Run RED tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
```

Expected: fail because `paper_package_adapter_unsupported_primitive_policy` and
`paper_package_conversion_mapped_subset_plan` do not exist yet.

### Task 2: Implement Offline Policy Payload

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add the next-gate constant**

Add:

```python
_PAPER_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN = (
    "paper_package_conversion_mapped_subset_plan"
)
```

- [ ] **Step 2: Add remaining-gap helper**

Add:

```python
def _paper_remaining_gaps_after_unsupported_primitive_policy() -> list[str]:
    return [_PAPER_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN]
```

- [ ] **Step 3: Add family policy row builder**

Add a helper that returns six rows for `_AUDITED_PAPER_PRIMITIVES`. Native candidates may be
identified as `oriented_bounding_box`, `sphere`, and `capsule`, but each row must say package
conversion is not enabled by this gate.

- [ ] **Step 4: Add current decision policy row builder**

Convert every row in `adapter_payload["primitive_adapter_decision_rows"]` into a policy row.
Current unsupported rows must be classified as:

```python
{
    "unsupported_policy_decision": "block_package_conversion",
    "adapter_action": "keep_offline",
    "package_candidate_status": "not_package_candidate_unsupported_policy_block",
}
```

- [ ] **Step 5: Add payload builder**

Add `_paper_package_adapter_unsupported_primitive_policy_payload(adapter_payload)` with gate
metadata, policy tables, coverage counts, remaining gaps, and false trigger booleans.

- [ ] **Step 6: Wire payload into `build_cpd_paper_offline_report()`**

Build the adapter payload once, build the unsupported-policy payload from it, update top-level
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
- Add: `docs/records/2026-05-17-cpd-paper-package-adapter-unsupported-primitive-policy.md`

- [ ] **Step 1: Update current-status prose**

Replace statements that say the current next gate is
`paper_package_adapter_unsupported_primitive_policy` with wording that says this gate is now closed
as offline policy accounting and the next gate is `paper_package_conversion_mapped_subset_plan`.

- [ ] **Step 2: Tighten claim boundaries**

Add explicit language that this gate is not package readiness, Newton support, runtime
admissibility, approximation support, or package-generation completion.

- [ ] **Step 3: Add dated record and registry entry**

Add a dated record that states the exact command, scope, evidence, and unsupported claims. Add a
matching complete registry entry after `cpd-paper-package-adapter-contract`.

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
