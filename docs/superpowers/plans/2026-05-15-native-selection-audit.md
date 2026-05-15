# Native Selection Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a cost-audit table to the synthetic Newton-native fitting comparison so each
selected native primitive is explained by explicit candidate weighted-volume terms.

**Architecture:** Reuse the existing CPD-like primitive fitting path. Add a candidate-enumeration
helper beside `fit_best_primitive`, then include its summarized results in
`build_newton_native_fitting_comparison_report`.

**Tech Stack:** Python, NumPy, pytest, existing `primitive_collision_compiler` package.

---

### Task 1: Synthetic Report Contract

**Files:**
- Modify: `tests/test_cpd_like_synthetic.py`

- [x] **Step 1: Write failing candidate-audit test**

Add assertions to `test_newton_native_fitting_comparison_selects_native_primitives`:

```python
candidate_audit = case["native"]["candidate_audit"]
assert candidate_audit[0]["primitive_type"] == expected_native[case_id]
assert candidate_audit[0]["selected"] is True
assert candidate_audit[0]["rank"] == 1
assert case["native"]["selected_candidate_rank"] == 1
assert case["native"]["selection_policy"] == "min_weighted_volume_surrogate_v0"
assert case["comparison"]["native_selected_kind_cost_explained"] is True
assert case["comparison"]["native_selection_margin_vs_legacy_best"] <= 0.0
```

- [x] **Step 2: Verify red**

Run:

```bash
python -m pytest tests/test_cpd_like_synthetic.py::test_newton_native_fitting_comparison_selects_native_primitives -q
```

Expected: fail with missing `candidate_audit` or `selection_policy`.

### Task 2: Candidate Enumeration Helper

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/primitives.py`

- [x] **Step 1: Add helper**

Create `fit_primitive_candidates(mesh, face_ids, primitive_subset)` that returns the same
supported candidate fits that `fit_best_primitive` considers, in primitive-subset order.

- [x] **Step 2: Make `fit_best_primitive` reuse the helper**

Keep existing behavior: minimum `weighted_volume`, tie-broken by primitive-subset order.

- [x] **Step 3: Verify targeted tests**

Run:

```bash
python -m pytest tests/test_cpd_like_synthetic.py::test_newton_native_fitting_comparison_selects_native_primitives -q
```

Expected: still fail until Task 3 wires the report fields.

### Task 3: Report Audit Fields

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- Modify: `tests/test_cpd_like_synthetic.py`

- [x] **Step 1: Add lane audit fields**

Add candidate summaries with rank, selected flag, volume, weighted volume, normalized weighted
volume, containment flag, and dimensions.

- [x] **Step 2: Add comparison fields**

Add native-vs-legacy and native-vs-next-candidate margin fields plus claim-boundary text.

- [x] **Step 3: Verify green**

Run:

```bash
python -m pytest tests/test_cpd_like_synthetic.py::test_newton_native_fitting_comparison_selects_native_primitives tests/test_cpd_like_synthetic.py::test_newton_native_fitting_comparison_report_is_strict_json_serializable -q
```

Expected: pass.

### Task 4: CLI And Config Assertions

**Files:**
- Modify: `tests/test_cli.py`
- Modify: `tests/test_cpd_like_config.py`
- Modify: `configs/experiments/newton_native_fitting_comparison.yaml`

- [x] **Step 1: Extend CLI test**

Assert `--run-newton-native-fitting-comparison` emits `selection_policy` and candidate audit
fields in stdout JSON.

- [x] **Step 2: Extend config test**

Assert the config records the selection audit stage in `verify`.

- [x] **Step 3: Verify targeted CLI/config tests**

Run:

```bash
python -m pytest tests/test_cli.py::test_cli_run_newton_native_fitting_comparison_emits_json_without_config tests/test_cpd_like_config.py::test_newton_native_fitting_comparison_config_includes_bed_and_franka_scope -q
```

Expected: pass.

### Task 5: Documentation And Record

**Files:**
- Modify: `docs/reference/newton-native-fitting-comparison.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/real-usd-native-probe-paper-story-explainer.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/index.md`
- Modify: `docs/records/README.md`
- Create: `docs/records/2026-05-15-native-selection-audit.md`

- [x] **Step 1: Update story docs**

Explain that synthetic native fitting now has a candidate weighted-volume audit table.

- [x] **Step 2: Add record**

Record command outputs, artifacts, claim impact, and next action.

- [ ] **Step 3: Verify docs and full suite**

Run:

```bash
python -m pytest -q
python scripts/validate_docs.py
git diff --check
```

Expected: all pass.
