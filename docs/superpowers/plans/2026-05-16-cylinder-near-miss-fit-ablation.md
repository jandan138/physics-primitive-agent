# Cylinder Near-Miss Fit Ablation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a diagnostic-only cylinder near-miss fit-ablation report and CLI gate.

**Architecture:** Keep default fitting and selection unchanged. Compute a lower-bound radial
diagnostic inside the synthetic workbench code and expose it through tests, CLI, records, and
claim-boundary docs.

**Tech Stack:** Python, pytest, strict JSON report dictionaries, existing CPD-like synthetic
workbench helpers.

---

### Task 1: Report Builder

**Files:**
- Modify: `tests/test_cpd_like_synthetic.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`

- [x] **Step 1: Write failing report test**

Add a test that imports `build_cpd_like_cylinder_near_miss_fit_ablation_report`, calls it, and
asserts:

```python
report["stage"] == "cpd_like_cylinder_near_miss_fit_ablation"
report["status"] == "smoke_passed"
case = report["cases"][0]
case["case_id"] == "cylinder_near_miss_cluster"
case["ablation"]["lower_bound_volume_beats_selected"] is False
case["decision"]["recommended_next_component"] == "scoring_or_merge_search_not_radial_center_refinement"
```

- [x] **Step 2: Verify RED**

Run:

```bash
PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_fit_ablation_reports_radial_refinement_gate
```

Expected: import error or missing function failure.

- [x] **Step 3: Implement minimal report**

Add constants, a report builder, and small helpers in `synthetic.py`:

- compute ranked `box`/`cylinder` rows using existing candidate ranking;
- compute pairwise radial lower bound from points projected away from the selected cylinder axis;
- compute lower-bound cylinder volume using current half height;
- mark smoke passed when the lower bound cannot beat box and current behavior remains the known
  near-miss.

- [x] **Step 4: Verify GREEN**

Run the targeted pytest command from Step 2 and confirm it passes.

### Task 2: CLI Gate

**Files:**
- Modify: `tests/test_cli.py`
- Modify: `src/primitive_collision_compiler/cli.py`

- [x] **Step 1: Write failing CLI test**

Add a test that runs:

```python
assert cli.main(["--run-cpd-like-cylinder-near-miss-fit-ablation"]) == 0
```

Then parses stdout and checks the stage and decision field.

- [x] **Step 2: Verify RED**

Run:

```bash
PYTHONPATH=src python -m pytest -q tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_fit_ablation_emits_json
```

Expected: argparse rejects the missing flag.

- [x] **Step 3: Implement CLI flag**

Import the builder, add the parser flag, emit strict JSON, and return zero only when status is
`smoke_passed`.

- [x] **Step 4: Verify GREEN**

Run the targeted CLI test and confirm it passes.

### Task 3: Documentation And Verification

**Files:**
- Create: `docs/records/2026-05-16-cylinder-near-miss-fit-ablation.md`
- Modify: `docs/records/README.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-latest-diagnostic-loop-explainer.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/index.md`
- Modify: `experiments/registry.yaml`

- [x] **Step 1: Record the result**

Write a dated record that says the slice is synthetic/offline only, default packages are unchanged,
and Newton task comparison is not triggered.

- [x] **Step 2: Update claim boundaries and status pages**

Add wording that this is diagnostic triage, not CPD reproduction or collision validation.

- [x] **Step 3: Verify**

Run:

```bash
PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_fit_ablation_emits_json
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.
