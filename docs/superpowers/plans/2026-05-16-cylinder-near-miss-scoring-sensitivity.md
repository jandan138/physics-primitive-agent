# Cylinder Near-Miss Scoring Sensitivity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a diagnostic-only scoring-sensitivity report and CLI gate for the synthetic cylinder near-miss fixture.

**Architecture:** Reuse the existing near-miss fixture and candidate ranking. Add a new report
builder that computes sensitivity metrics without changing fitting, selection, merge/search,
real-USD packages, or Newton diagnostics.

**Tech Stack:** Python, pytest, strict JSON report dictionaries, existing CPD-like synthetic
workbench helpers.

---

### Task 1: Report Builder

**Files:**
- Modify: `tests/test_cpd_like_synthetic.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`

- [x] **Step 1: Write the failing report test**

Add a test that imports `build_cpd_like_cylinder_near_miss_scoring_sensitivity_report`, calls it,
and asserts:

```python
report["stage"] == "cpd_like_cylinder_near_miss_scoring_sensitivity"
report["status"] == "smoke_passed"
case = report["cases"][0]
case["case_id"] == "cylinder_near_miss_cluster"
case["selected_primitive_type"] == "box"
case["extension_primitive_type"] == "cylinder"
case["selection_policy_changed"] is False
0.0 < case["scoring_sensitivity"]["extension_score_multiplier_to_tie"] < 1.0
case["decision"]["newton_task_comparison_triggered"] is False
```

- [x] **Step 2: Verify RED**

Run:

```bash
PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_sensitivity_reports_required_multiplier
```

Expected: import error or missing function failure.

- [x] **Step 3: Implement minimal report**

Add constants, a report builder, and a case helper in `synthetic.py`. Compute:

- selected box cost;
- support-admissible cylinder cost;
- absolute cost gap;
- relative gap versus selected cost;
- cylinder-over-selected cost ratio;
- required cylinder score multiplier to tie;
- required cylinder cost reduction fraction to tie.

- [x] **Step 4: Verify GREEN**

Run the targeted pytest command from Step 2 and confirm it passes.

### Task 2: CLI Gate

**Files:**
- Modify: `tests/test_cli.py`
- Modify: `src/primitive_collision_compiler/cli.py`

- [x] **Step 1: Write the failing CLI test**

Add a test that runs:

```python
assert cli.main(["--run-cpd-like-cylinder-near-miss-scoring-sensitivity"]) == 0
```

Then parse stdout and check the stage, `smoke_passed` status, and required multiplier.

- [x] **Step 2: Verify RED**

Run:

```bash
PYTHONPATH=src python -m pytest -q tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_sensitivity_emits_json
```

Expected: argparse rejects the missing flag.

- [x] **Step 3: Implement CLI flag**

Import the builder, add the parser flag, emit strict JSON, and return zero only when status is
`smoke_passed`.

- [x] **Step 4: Verify GREEN**

Run the targeted CLI test and confirm it passes.

### Task 3: Documentation And Verification

**Files:**
- Create: `docs/records/2026-05-16-cylinder-near-miss-scoring-sensitivity.md`
- Modify: `docs/records/README.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-latest-diagnostic-loop-explainer.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/index.md`
- Modify: `experiments/registry.yaml`

- [x] **Step 1: Record the result**

Write a dated record that says the slice is synthetic/offline only, default selection and Newton
packages are unchanged, and the report only quantifies a hypothetical scoring change.

- [x] **Step 2: Update claim boundaries and status pages**

Add wording that this is scoring-sensitivity planning, not an objective improvement or quality
result.

- [x] **Step 3: Verify**

Run:

```bash
PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_sensitivity_emits_json
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.
