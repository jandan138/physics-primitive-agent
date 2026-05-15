# Real USD Candidate Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a claim-bounded candidate audit summary to real-USD bed/Franka native fitting reports
so the repository can inspect why the native lane still selects boxes.

**Architecture:** Reuse `fit_primitive_candidates()` against each final selected cluster from the
existing decomposition report. Summarize the per-cluster candidate ranks instead of emitting large
raw per-candidate tables.

**Tech Stack:** Python, NumPy, pytest, existing `primitive_collision_compiler` package.

---

### Task 1: Report Contract Test

**Files:**
- Modify: `tests/test_real_usd_native_comparison.py`

- [ ] **Step 1: Write failing assertions**

In `test_real_usd_native_fitting_report_runs_roles_from_manifest`, assert:

```python
native_audit = report["cases"][0]["native"]["candidate_audit_summary"]
assert native_audit["scope"] == "per_selected_cluster"
assert native_audit["cluster_count"] == report["cases"][0]["native"]["primitive_count"]
assert native_audit["extension_candidate_kinds"] == ["cylinder", "cone", "ellipsoid"]
assert "box_selected_cluster_count" in native_audit
assert "clusters_with_extension_best" in native_audit
```

- [ ] **Step 2: Verify red**

Run:

```bash
python -m pytest tests/test_real_usd_native_comparison.py::test_real_usd_native_fitting_report_runs_roles_from_manifest -q
```

Expected: fail with missing `candidate_audit_summary`.

### Task 2: Implement Summary

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/real_usd_comparison.py`

- [ ] **Step 1: Store source mesh in lane artifact**

Add `mesh: TriangleMesh` to `NativeLaneArtifact` so the summary can refit candidates for selected
clusters without reopening the USD.

- [ ] **Step 2: Build candidate audit summary**

For each final primitive's `source_faces`, call `fit_primitive_candidates(mesh, faces,
primitive_subset)`, sort by `(weighted_volume, candidate_order)`, and collect selected rank,
extension-best counts, box counts, and mean margins.

- [ ] **Step 3: Verify green**

Run:

```bash
python -m pytest tests/test_real_usd_native_comparison.py::test_real_usd_native_fitting_report_runs_roles_from_manifest tests/test_real_usd_native_comparison.py::test_real_usd_native_fitting_report_is_strict_json_serializable -q
```

Expected: pass.

### Task 3: Documentation And Record

**Files:**
- Modify: `docs/reference/bed-franka-native-probe-comparison.md`
- Modify: `docs/reference/real-usd-native-probe-paper-story-explainer.md`
- Modify: `docs/reference/synthetic-native-selection-audit-explainer.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/index.md`
- Modify: `docs/records/README.md`
- Create: `docs/records/2026-05-15-real-usd-candidate-audit.md`

- [ ] **Step 1: Update docs**

Explain that the real-USD report now includes summary candidate accounting per selected cluster.

- [ ] **Step 2: Add record**

Record command paths, claim impact, and next action.

- [ ] **Step 3: Verify**

Run:

```bash
python -m pytest -q
python scripts/validate_docs.py
git diff --check
```

Expected: all pass.
