# CPD Paper Frustum And Trapezoid Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add offline-only frustum and trapezoidal-prism candidate audit rows to
`cpd_paper_offline_report`.

**Architecture:** Keep the implementation in
`src/primitive_collision_compiler/baselines/cpd_paper/offline.py`. Reuse the current report schema
and append paper-shaped offline rows after the existing current surrogate rows.

**Tech Stack:** Python, NumPy, pytest, Markdown records.

---

### Task 1: RED Tests

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`

- [x] **Step 1: Add failing tests**

Tests assert that frustum and trapezoidal-prism rows exist, are offline-only, contain assigned
points, and move the next required gate to `paper_flat_capped_cylinder_fit_audit`.

- [x] **Step 2: Verify RED**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_audits_frustum_and_trapezoidal_prism_candidates -q
```

Expected and observed before implementation: fails because `frustum_fit_missing` and
`trapezoidal_prism_fit_missing` are still present and `paper_frustum_like` does not exist.

### Task 2: Offline Fit Rows

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add two paper toy meshes**

Add `_frustum_like_mesh()` and `_trapezoid_prism_like_mesh()` and include them in
`_paper_toy_cases()`.

- [ ] **Step 2: Add offline paper candidate rows**

Change `_primitive_fit_audit_payload()` so it combines existing current rows with local
`frustum` and `trapezoidal_prism` rows. Do not add these rows to Newton mapping or the CPD-like
runtime primitive set.

- [ ] **Step 3: Add containment helpers**

Implement deterministic helpers for linear top/bottom radius fitting, frustum containment, and
trapezoidal-prism containment.

- [ ] **Step 4: Verify GREEN**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_audits_frustum_and_trapezoidal_prism_candidates -q
```

Expected: both tests pass.

### Task 3: Docs And Record

**Files:**
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/index.md`
- Modify: `docs/records/README.md`
- Create: `docs/records/2026-05-16-cpd-paper-frustum-trapezoid-audit.md`
- Modify: `experiments/registry.yaml`

- [ ] **Step 1: Update claim-safe docs**

Document the new offline-only frustum/trapezoidal-prism audit rows and keep the remaining gaps
explicit.

- [ ] **Step 2: Add dated record and registry entry**

Record commands, review results, verification output, and claim impact.

- [ ] **Step 3: Verify docs**

Run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

### Task 4: Review, Full Verification, Commit

**Files:**
- All files changed by Tasks 1-3.

- [ ] **Step 1: Request multi-agent review**

Ask one reviewer to check the fit rows and one reviewer to check docs/claims.

- [ ] **Step 2: Apply valid review fixes**

Fix Critical and Important findings before committing.

- [ ] **Step 3: Run final verification**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cli.py::test_cli_run_cpd_paper_offline_report_rejects_nonfinite_json -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
python -m pytest -q
```

Expected: all pass.

- [ ] **Step 4: Commit and push**

Commit with:

```bash
git commit -m "feat: audit CPD paper frustum and trapezoid fits"
```

Push to `origin/main`.

