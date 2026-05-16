# Cylinder Scoring Policy Guardrail Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the synthetic/offline scoring-policy ablation report with a boxy guardrail case.

**Architecture:** Reuse the existing report-only counterfactual scoring helper and CLI command.
Add a boxy cuboid synthetic guardrail fixture and extend the current report so it compares expected
flip and expected no-flip cases without changing production primitive selection or Newton
diagnostics.

**Tech Stack:** Python, pytest, strict JSON report dictionaries, existing CPD-like synthetic
workbench helpers.

---

### Task 1: Report Builder

**Files:**
- Modify: `tests/test_cpd_like_synthetic.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`

- [x] **Step 1: Write the failing report test**

Update the existing ablation report test for
`build_cpd_like_cylinder_near_miss_scoring_policy_ablation_report()` and
asserts:

```python
report["stage"] == "cpd_like_cylinder_near_miss_scoring_policy_ablation"
report["status"] == "smoke_passed"
cases = {case["case_id"]: case for case in report["cases"]}
cases["cylinder_near_miss_cluster"]["counterfactual_selected_primitive_type"] == "cylinder"
cases["boxy_cuboid_guardrail"]["counterfactual_selected_primitive_type"] == "box"
cases["boxy_cuboid_guardrail"]["counterfactual_selection_changed"] is False
```

- [x] **Step 2: Verify RED**

Run:

```bash
PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_near_miss_scoring_policy_ablation_reports_counterfactual_flip
```

Expected: assertion failure because the existing report initially lacks the boxy guardrail case.

- [x] **Step 3: Implement minimal report**

Add a `boxy_cuboid_guardrail` mesh helper and generalize the existing scoring-policy ablation case
helper in `synthetic.py`. Compute default rows through existing candidate ranking and
counterfactual rows through copied report rows only.

- [x] **Step 4: Verify GREEN**

Run the targeted pytest command from Step 2 and confirm it passes.

### Task 2: Existing CLI Coverage

**Files:**
- Modify: `tests/test_cli.py`

- [x] **Step 1: Extend the CLI test**

Update the existing CLI test that runs:

```python
assert cli.main(["--run-cpd-like-cylinder-near-miss-scoring-policy-ablation"]) == 0
```

Then parse stdout and check the stage, `smoke_passed` status, and both case ids.

- [x] **Step 2: Verify RED**

Run:

```bash
PYTHONPATH=src python -m pytest -q tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_policy_ablation_emits_json
```

Expected: assertion failure before the report includes the boxy guardrail case.

- [x] **Step 3: Keep the existing CLI flag**

No parser change is needed. The existing command emits the expanded report and still returns zero
only when status is `smoke_passed`.

- [x] **Step 4: Verify GREEN**

Run the targeted CLI test and confirm it passes.

### Task 3: Documentation And Verification

**Files:**
- Create: `docs/records/2026-05-16-cylinder-scoring-policy-guardrail.md`
- Modify: `docs/records/README.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-latest-diagnostic-loop-explainer.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/index.md`
- Modify: `experiments/registry.yaml`

- [x] **Step 1: Record the result**

Write a dated record that says the slice is synthetic/offline only, the multiplier is report-only,
near-miss flips, boxy guardrail does not flip, and default packages/Newton task gates are
unchanged.

- [x] **Step 2: Update claim boundaries and status pages**

Add wording that this is a guardrail diagnostic, not evidence the multiplier is safe, calibrated,
or quality-improving.

- [x] **Step 3: Verify**

Run:

```bash
PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py tests/test_cli.py::test_cli_run_cpd_like_cylinder_near_miss_scoring_policy_ablation_emits_json
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.
