# Cylinder Near-Miss Fixture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a deterministic `cylinder_near_miss_cluster` fixture that turns the current real-USD candidate-loss near-miss signal into a reproducible synthetic diagnostic target.

**Architecture:** Keep production primitive selection unchanged relative to the current support-aware baseline. Add one direct synthetic primitive-ranking fixture and one dedicated near-miss workbench report that record `box` selected, `cylinder` close, support-admissible, and suitable for the next fitting or merge/search slice. Do not add it to the native fitting success report.

**Tech Stack:** Python, pytest, existing CPD-like synthetic report code, existing native primitive candidate ranking and candidate-loss terminology.

---

### Task 1: Failing Primitive-Ranking Test

**Files:**
- Modify: `tests/test_cpd_like_synthetic.py`

- [x] **Step 1: Add the failing primitive-ranking test**

Add a test named `test_cylinder_near_miss_cluster_exposes_box_selected_close_cylinder_loss`.
It should call `_cylinder_near_miss_cluster_mesh()` directly and rank `box` versus `cylinder`.

Required assertions:

```python
assert fit.primitive_type == "box"
assert ranked[0].primitive_type == "box"
assert box.selection_admissible is True
assert cylinder.selection_admissible is True
assert cylinder.selection_admissibility_reason == "support_thresholds_met"
assert cylinder.candidate.weighted_volume > box.candidate.weighted_volume
assert 0.0 < relative_gap <= 0.25
assert cylinder.raw_cost_rank == 2
```

- [x] **Step 2: Verify the test fails**

Run:

```bash
python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_cluster_exposes_box_selected_close_cylinder_loss
```

Expected result:

```text
FAILED
AttributeError: module 'primitive_collision_compiler.baselines.cpd_like.synthetic' has no attribute '_cylinder_near_miss_cluster_mesh'
```

### Task 2: Fixture Helper

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`

- [x] **Step 1: Add deterministic mesh**

Create `_cylinder_near_miss_cluster_mesh()` near the other synthetic primitive fixtures. The mesh
must have at least three faces and five unique points so the cylinder candidate is support
admissible.

Use a deterministic six-point cross-section extruded across a short height. The exact assertion
stays relational rather than tied to a fixed floating-point value.

- [x] **Step 2: Verify targeted test passes**

Run:

```bash
python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_cluster_exposes_box_selected_close_cylinder_loss
```

Expected result:

```text
1 passed
```

### Task 3: Keep Report Expectations Unchanged

**Files:**
- Modify: `tests/test_cpd_like_synthetic.py`

- [x] **Step 1: Confirm the native fitting success report still covers only success fixtures**

Do not add `cylinder_near_miss_cluster` to `_native_fitting_cases()` or to
`configs/experiments/newton_native_fitting_comparison.yaml` in this slice. The fixture is an
expected limitation target, not a native-extension success fixture.

- [x] **Step 2: Run the focused file**

Run:

```bash
python -m pytest -q tests/test_cpd_like_synthetic.py
```

Expected result:

```text
all tests in the file pass
```

### Task 3B: Dedicated Near-Miss Workbench Report

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- Modify: `src/primitive_collision_compiler/cli.py`
- Modify: `tests/test_cpd_like_synthetic.py`
- Modify: `tests/test_cli.py`

- [x] **Step 1: Add failing report and CLI tests**

Add tests for `build_cpd_like_near_miss_workbench_report()` and
`--run-cpd-like-near-miss-workbench`.

- [x] **Step 2: Verify the tests fail before implementation**

Run:

```bash
python -m pytest -q tests/test_cpd_like_synthetic.py::test_near_miss_workbench_reports_cylinder_fixture tests/test_cli.py::test_cli_run_cpd_like_near_miss_workbench_emits_json
```

Expected initial result:

```text
ImportError or missing CLI argument
```

- [x] **Step 3: Implement the minimal report and CLI path**

Add a report with stage `cpd_like_near_miss_fixture_workbench`, claim boundary
`synthetic_near_miss_fixture_not_collision_quality_validation`, and a single
`cylinder_near_miss_cluster` case.

- [x] **Step 4: Verify the tests pass**

Run:

```bash
python -m pytest -q tests/test_cpd_like_synthetic.py::test_near_miss_workbench_reports_cylinder_fixture tests/test_cli.py::test_cli_run_cpd_like_near_miss_workbench_emits_json
```

Expected result:

```text
2 passed
```

### Task 4: Documentation And Record

**Files:**
- Modify: `docs/reference/cpd-latest-diagnostic-loop-explainer.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/index.md`
- Modify: `docs/records/README.md`
- Modify: `experiments/registry.yaml`
- Create: `docs/records/2026-05-16-cylinder-near-miss-cluster-fixture.md`

- [x] **Step 1: Add a dated record**

Record:

- what fixture was added;
- that it is support-admissible but still box-selected;
- that it does not change real-USD packages;
- verification commands and exit statuses.

- [x] **Step 2: Update claim-safe docs**

Use only claim-safe wording:

```text
support-admissible cylinder near-miss fixture
synthetic diagnostic target
not collision-quality evidence
not paper-faithful CPD optimization
not a Newton task improvement
```

- [x] **Step 3: Update registry**

Add a registry entry for the CLI-backed near-miss workbench. Do not describe it as a native
fitting comparison case.

### Task 5: Review And Verification

**Files:**
- All files changed by this slice.

- [x] **Step 1: Request two read-only agent reviews**

Ask one reviewer to inspect code/report semantics and one reviewer to inspect claim boundaries.

- [x] **Step 2: Run verification**

Run:

```bash
python -m pytest -q tests/test_cpd_like_synthetic.py
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

- [x] **Step 3: Report smoke**

Run:

```bash
PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-near-miss-workbench
```

Expected result:

```text
status: smoke_passed
```
