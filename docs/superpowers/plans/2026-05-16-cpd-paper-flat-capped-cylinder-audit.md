# CPD Paper Flat Capped Cylinder Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the capped-cylinder proxy row in `cpd_paper_offline_report` with an offline-only
paper-shaped flat-capped cylinder audit row.

**Architecture:** Keep the fit helper local to `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`.
Reuse the frustum flat-cylinder axis-candidate helper data shape where possible.

**Tech Stack:** Python, NumPy, pytest, Markdown records.

---

### Task 1: RED Test

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`

- [x] **Step 1: Write failing assertions**

Assert that `paper_flat_capped_cylinder_fit_missing` is removed, the next gate moves to
`paper_capsule_axis_policy_audit`, and the capped-cylinder row is a flat-cap offline audit row.

- [x] **Step 2: Verify RED**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice -q
```

Expected and observed before implementation: fails because
`paper_flat_capped_cylinder_fit_missing` is still present.

### Task 2: Minimal Implementation

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Remove current capped-cylinder proxy from paper audit candidates**

Use CPD-like fitters only for `box`, `sphere`, and `capsule`.

- [ ] **Step 2: Add paper-flat capped-cylinder candidate row**

Compute three flat-cylinder axis candidates, select the minimum-volume candidate, and emit the
offline-only audit row.

- [ ] **Step 3: Verify GREEN**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice -q
```

Expected: pass.

### Task 3: Docs, Review, Verification

**Files:**
- Modify docs under `docs/reference/`, `docs/index.md`, `docs/records/README.md`,
  `experiments/registry.yaml`.
- Create dated record under `docs/records/`.

- [ ] **Step 1: Update claim-safe docs**

Document flat capped-cylinder offline audit support without claiming Newton support or full paper
reproduction.

- [ ] **Step 2: Request multi-agent review**

Use separate reviewers for geometry/schema and docs/claims.

- [ ] **Step 3: Run verification**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_newton_shapes.py::test_map_package_shapes_keeps_capped_cylinder_as_mapping_gap tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cli.py::test_cli_run_cpd_paper_offline_report_rejects_nonfinite_json -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
python -m pytest -q
```

Expected: all pass.

