# Cylinder Near-Miss Scoring Policy Ablation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a synthetic/offline, report-only scoring-policy ablation for the cylinder near-miss fixture.

**Architecture:** Reuse the existing fixture and candidate ranking. Add a new report builder that
computes a counterfactual adjusted ranking with a fixed cylinder multiplier, without changing
default primitive selection, merge/search, real-USD packages, or Newton diagnostics.

**Tech Stack:** Python, pytest, strict JSON report dictionaries, existing CPD-like synthetic
workbench helpers.

---

### Task 1: Report Builder

**Files:**
- Modify: `tests/test_cpd_like_synthetic.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`

- [x] **Step 1: Write the failing report test**

Add a test that imports `build_cpd_like_cylinder_near_miss_scoring_policy_ablation_report`, calls
it, and asserts:

```python
report["stage"] == "cpd_like_cylinder_near_miss_scoring_policy_ablation"
report["status"] == "smoke_passed"
case = report["cases"][0]
case["case_id"] == "cylinder_near_miss_cluster"
case["default_selected_primitive_type"] == "box"
case["counterfactual_selected_primitive_type"] == "cylinder"
case["default_selection_changed"] is False
case["counterfactual_selection_changed"] is True
case["counterfactual_ablation"]["report_only_extension_multiplier"] == 0.88
case["decision"]["newton_task_comparison_triggered"] is False
```

- [x] **Step 2: Verify RED**

Run:

```bash
PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_policy_ablation_reports_counterfactual_flip
```

Expected: import error or missing function failure.

- [x] **Step 3: Implement minimal report**

Add constants, a report builder, and a case helper in `synthetic.py`. Compute default ranking rows
from existing candidate ranking and counterfactual rows by multiplying the cylinder weighted volume
by `0.88` inside the report only.

- [x] **Step 4: Verify GREEN**

Run the targeted pytest command from Step 2 and confirm it passes.

### Task 2: CLI Gate

**Files:**
- Modify: `tests/test_cli.py`
- Modify: `src/primitive_collision_compiler/cli.py`

- [x] **Step 1: Write the failing CLI test**

Add a test that runs:

```python
assert cli.main(["--run-cpd-like-cylinder-near-miss-scoring-policy-ablation"]) == 0
```

Then parse stdout and check the stage, `smoke_passed` status, default selected primitive, and
counterfactual selected primitive.

- [x] **Step 2: Verify RED**

Run:

```bash
PYTHONPATH=src python -m pytest -q tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_policy_ablation_emits_json
```

Expected: argparse rejects the missing flag.

- [x] **Step 3: Implement CLI flag**

Import the builder, add the parser flag, emit strict JSON, and return zero only when status is
`smoke_passed`.

- [x] **Step 4: Verify GREEN**

Run the targeted CLI test and confirm it passes.

### Task 3: Documentation And Verification

**Files:**
- Create: `docs/records/2026-05-16-cylinder-near-miss-scoring-policy-ablation.md`
- Modify: `docs/records/README.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-latest-diagnostic-loop-explainer.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/index.md`
- Modify: `experiments/registry.yaml`

- [x] **Step 1: Record the result**

Write a dated record that says the slice is synthetic/offline only, the multiplier is report-only,
and default packages/Newton task gates are unchanged.

- [x] **Step 2: Update claim boundaries and status pages**

Add wording that this is counterfactual scoring-policy ablation, not an objective improvement,
default selector change, or quality result.

- [x] **Step 3: Verify**

Run:

```bash
PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_policy_ablation_emits_json
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.
