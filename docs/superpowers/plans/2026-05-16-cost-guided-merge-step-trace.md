# Cost-Guided Merge Step Trace Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an opt-in synthetic/offline merge-step trace so cost-guided merge/search decisions
are inspectable without changing merge behavior.

**Architecture:** Extend `report_merge_trace` with a `steps` mode. `summary` remains the default,
`none` remains compact, and `steps` records accepted/blocked merge candidates in
`CPDLikeDecompositionReport.merge_trace`.

**Tech Stack:** Python dataclasses, pytest, JSON CLI reports, existing CPD-like decompose and
synthetic comparison modules.

---

### Task 1: Decomposition Merge Trace

**Files:**

- Modify: `src/primitive_collision_compiler/baselines/cpd_like/decompose.py`
- Test: `tests/test_cpd_like_decompose.py`

- [x] **Step 1: Write failing accepted-step test**

Add a test:

```python
def test_decompose_mesh_steps_trace_records_cost_guided_virtual_merge():
    report = decompose_mesh(
        _cost_guided_pair_choice_mesh(),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        merge_search_policy="cost_guided_pairwise",
        report_merge_trace="steps",
    )

    assert len(report.merge_trace) == 1
    step = report.merge_trace[0]
    assert step["step_index"] == 1
    assert step["decision"] == "accepted"
    assert step["merge_kind"] == "virtual_component"
    assert step["merged_source_component_ids"] == [0, 2]
    assert step["merged_primitive_type"] == "box"
    assert step["normalized_excess_volume"] == report.merge_cost_summary[
        "accepted_normalized_excess_sum"
    ]
```

- [x] **Step 2: Write failing blocked-step test**

Add:

```python
def test_decompose_mesh_steps_trace_records_blocked_virtual_merge():
    report = decompose_mesh(
        _cost_guided_pair_choice_mesh(),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        merge_search_policy="cost_guided_pairwise",
        excess_volume_threshold_fraction=0.0,
        report_merge_trace="steps",
    )

    assert report.status == "partial"
    assert len(report.merge_trace) == 1
    assert report.merge_trace[0]["decision"] == "blocked"
    assert report.merge_trace[0]["blocked_reason"] == "component_merge_threshold_blocked"
```

- [x] **Step 3: Run RED**

Run:

```bash
PYTHONPATH=src python -m pytest -q tests/test_cpd_like_decompose.py::test_decompose_mesh_steps_trace_records_cost_guided_virtual_merge tests/test_cpd_like_decompose.py::test_decompose_mesh_steps_trace_records_blocked_virtual_merge
```

Expected: fail because `steps` is invalid or `merge_trace` does not exist.

- [x] **Step 4: Implement trace mode**

Add `REPORT_MERGE_TRACE_STEPS = "steps"`, add `merge_trace` to
`CPDLikeDecompositionReport`, and append accepted/blocked candidate rows when
`report_merge_trace == "steps"`.

- [x] **Step 5: Run GREEN**

Run the RED command again.

Expected: both tests pass.

### Task 2: Synthetic Report And CLI Coverage

**Files:**

- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- Modify: `src/primitive_collision_compiler/cli.py`
- Modify: `tests/test_cpd_like_synthetic.py`
- Modify: `tests/test_cli.py`

- [x] **Step 1: Write failing synthetic report assertion**

Extend `test_cost_guided_synthetic_comparison_shows_old_new_merge_decision()`:

```python
trace = case["policies"]["cost_guided_pairwise"]["merge_trace"]
assert trace[0]["merge_kind"] == "virtual_component"
assert trace[0]["decision"] == "accepted"
```

- [x] **Step 2: Write failing CLI/config assertion**

Add or extend a config-driven `--run-cpd-like` test with:

```yaml
cpd_like:
  component_merge: virtual_pairwise
  merge_search_policy: cost_guided_pairwise
  report_merge_trace: steps
```

Assert the JSON payload has `merge_trace[0]["decision"] == "accepted"`.

- [x] **Step 3: Run RED**

Run:

```bash
PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cost_guided_synthetic_comparison_shows_old_new_merge_decision tests/test_cli.py::test_cli_run_cpd_like_accepts_cost_guided_merge_search_policy
```

Expected: fail until synthetic summaries and config validation expose `steps`.

- [x] **Step 4: Implement report propagation**

Set the cost-guided synthetic fixture policies to request `report_merge_trace="steps"` and include
`merge_trace` in `_policy_summary()` only when trace rows are present. Allow `steps` through the
existing config path.

- [x] **Step 5: Run GREEN**

Run the RED command again.

Expected: both tests pass.

### Task 3: Docs And Registry

**Files:**

- Create: `docs/records/2026-05-16-cost-guided-merge-step-trace.md`
- Modify: `docs/records/README.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/cpd-like-face-merge-explainer.md`
- Modify: `docs/index.md`
- Modify: `experiments/registry.yaml`

- [x] **Step 1: Record the slice**

Write that this is a synthetic offline merge-step trace over the existing cost-guided fixture, not
a merge algorithm change.

- [x] **Step 2: Update claim boundaries**

Add allowed wording for "synthetic offline merge-step trace" and reject quality, benchmark,
Newton task, and paper optimizer claims.

- [x] **Step 3: Update story/status pages and registry**

Add the existing synthetic comparison command as the reproducer and link the dated record.

### Task 4: Verification And Review

**Files:**

- Modify: `docs/records/2026-05-16-cost-guided-merge-step-trace.md`
- Modify: this plan file

- [x] **Step 1: Full verification**

Run:

```bash
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cost-guided-synthetic-comparison
```

- [x] **Step 2: Multi-agent review**

Request implementation and docs reviews. Fix Critical/Important findings and re-review.

- [x] **Step 3: Mark verification**

Update this plan and the dated record with final verification and review evidence.
