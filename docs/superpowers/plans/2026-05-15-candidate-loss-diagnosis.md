# Candidate Loss Diagnosis Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a candidate-loss diagnosis report, make one controlled cylinder-fitting improvement, and rerun synthetic plus real-USD bed/Franka diagnostics under the existing claim boundaries.

**Architecture:** Reuse the existing real-USD native artifact builder so fitting, package mapping, and Newton task gates stay centralized. Add diagnosis helpers in `real_usd_comparison.py`, expose a CLI flag, improve only cylinder axis selection in `primitives.py`, and document the generated reports in dated records.

**Tech Stack:** Python, pytest, USD via pxr for real-USD smoke inputs, existing Newton diagnostic CLI, Markdown records.

---

### Task 1: Candidate-Loss Diagnosis Report

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/real_usd_comparison.py`
- Modify: `src/primitive_collision_compiler/cli.py`
- Test: `tests/test_real_usd_native_comparison.py`
- Test: `tests/test_cli.py`

- [ ] Write failing tests for `build_real_usd_candidate_loss_diagnosis_report()`.
- [ ] Write failing CLI test for `--run-real-usd-candidate-loss-diagnosis`.
- [ ] Implement the report by reusing `build_real_usd_native_artifacts()`.
- [ ] Include baseline-lock summaries and per-cluster diagnosis rows for native lanes.
- [ ] Run targeted tests for real-USD comparison and CLI.

### Task 2: Controlled Cylinder Axis Improvement

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/primitives.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- Test: `tests/test_cpd_like_synthetic.py`
- Test: `tests/test_cpd_like_decompose.py`

- [ ] Write a failing primitive test showing a squat-cylinder mesh should select `cylinder`.
- [ ] Add a failing synthetic native fitting expectation for `squat_cylinder`.
- [ ] Change cylinder fitting to evaluate all candidate axes and choose the lowest-volume
  containing cylinder.
- [ ] Keep capsule, capped-cylinder, cone, and ellipsoid behavior unchanged.
- [ ] Run targeted primitive and synthetic tests.

### Task 3: Reports, Records, And Registry

**Files:**
- Modify: `experiments/registry.yaml`
- Modify: `docs/reference/cpd-next-steps-after-real-usd-mirrors.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/index.md`
- Modify: `docs/records/README.md`
- Create: `docs/records/2026-05-15-candidate-loss-diagnosis-and-cylinder-axis.md`

- [ ] Add registry entries for the candidate-loss diagnosis and regenerated synthetic fitting
  comparison.
- [ ] Run the synthetic fitting report and save it under `reports/generated/`.
- [ ] Run the real-USD candidate-loss diagnosis report and save it under `reports/generated/`.
- [ ] Re-run bed/Franka fitting, contact, and task comparison reports.
- [ ] Update docs and records with exact statuses and claim boundaries.

### Task 4: Review And Final Verification

**Files:**
- Review all changed code, tests, configs, and docs.

- [ ] Request focused code review for report semantics and cylinder fitting.
- [ ] Request focused docs/claim-boundary review.
- [ ] Address Important/Critical findings.
- [ ] Run `python -m pytest -q`.
- [ ] Run `python scripts/validate_docs.py`.
- [ ] Run `python scripts/validate_site_claims.py`.
- [ ] Run `git diff --check`.
