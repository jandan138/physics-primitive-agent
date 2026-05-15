# Newton Native Fitting Comparison Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an opt-in synthetic comparison that checks whether simple Newton-native primitive
fitters can emit `cylinder`, `cone`, and `ellipsoid`, and declare bed plus Franka as the next
real-USD scope.

**Architecture:** Extend the existing CPD-like primitive fitter rather than adding a parallel
pipeline. Reuse the existing objective report, collision package conversion, and Newton shape
mapping so the output stays comparable with earlier CPD-like records.

**Tech Stack:** Python, NumPy, pytest, existing `primitive_collision_compiler` package.

---

### Task 1: Synthetic Report Contract

**Files:**
- Modify: `tests/test_cpd_like_synthetic.py`

- [x] **Step 1: Write failing report tests**

Add tests that call `build_newton_native_fitting_comparison_report()` and expect three cases:
`cylindrical_rod`, `tapered_cone`, and `ellipsoid_blob`.

- [x] **Step 2: Verify red**

Run:

```bash
python -m pytest tests/test_cpd_like_synthetic.py::test_newton_native_fitting_comparison_selects_native_primitives -q
```

Expected initial failure: missing report builder and claim-boundary constant.

### Task 2: Native Fitters And Report Builder

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/primitives.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`

- [x] **Step 1: Add opt-in primitive fitters**

Add simple proxy fitters for `cylinder`, `cone`, and `ellipsoid`. Keep them opt-in through the
requested `primitive_subset`.

- [x] **Step 2: Add report builder**

Build the synthetic comparison report with legacy subset `box/sphere/capsule`, native subset
`box/sphere/capsule/cylinder/cone/ellipsoid`, objective metrics, package mapping summaries, and
`real_usd_scope`.

- [x] **Step 3: Verify green**

Run:

```bash
python -m pytest tests/test_cpd_like_synthetic.py::test_newton_native_fitting_comparison_selects_native_primitives tests/test_cpd_like_synthetic.py::test_newton_native_fitting_comparison_report_is_strict_json_serializable -q
```

Expected: pass.

### Task 3: CLI And Config Scope

**Files:**
- Modify: `tests/test_cli.py`
- Modify: `tests/test_cpd_like_config.py`
- Modify: `src/primitive_collision_compiler/cli.py`
- Modify: `src/primitive_collision_compiler/config.py`
- Create: `configs/experiments/newton_native_fitting_comparison.yaml`

- [x] **Step 1: Add failing CLI and config tests**

Add tests for `--run-newton-native-fitting-comparison` and for a config that includes both
`bed_dev_smoke` and `franka_import_smoke`.

- [x] **Step 2: Implement CLI flag and config preservation**

Wire the new report builder into CLI JSON output and preserve `native_fitting_comparison` in
loaded config protocol sections.

- [x] **Step 3: Verify green**

Run:

```bash
python -m pytest tests/test_cli.py::test_cli_run_newton_native_fitting_comparison_emits_json_without_config tests/test_cpd_like_config.py::test_newton_native_fitting_comparison_config_includes_bed_and_franka_scope -q
```

Expected: pass.

### Task 4: Documentation And Records

**Files:**
- Create: `docs/reference/newton-native-fitting-comparison.md`
- Create: `docs/records/2026-05-15-newton-native-fitting-comparison.md`
- Modify: `docs/index.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/newton-native-primitive-bundle-explainer.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/records/README.md`
- Modify: `experiments/registry.yaml`

- [x] **Step 1: Add reference explainer**

Explain that this is an opt-in synthetic native fitting comparison and that real USD bed plus
Franka are only scope-declared at this stage.

- [x] **Step 2: Update canonical claim docs**

Update evidence status and claim boundaries with the narrow supported claim and explicit
unsupported claims.

- [x] **Step 3: Verify docs**

Run:

```bash
python scripts/validate_docs.py
git diff --check
```

Expected: both pass.
