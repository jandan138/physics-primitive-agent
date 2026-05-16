# CPD Paper Capsule Axis Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an offline paper-shaped capsule axis-policy audit row to the partial
`cpd_paper_offline_report`.

**Architecture:** Keep the paper lane command-only and fixture-scoped. Remove the current CPD-like
capsule surrogate from the report's paper candidate set, append an offline capsule row with three
axis candidates, and advance the next gate to priority-queue trace.

**Tech Stack:** Python, pytest, Markdown docs, existing CPD paper offline report helpers.

---

### Task 1: RED Tests

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`

- [x] Add assertions that `paper_capsule_axis_policy_missing` is no longer in `failure_labels`.
- [x] Assert `next_required_gate == "paper_priority_queue_trace_audit"`.
- [x] Assert the capsule row has:
  - `implementation_status == "paper_shaped_offline_fit_audit"`;
  - `fit_model == "paper_capsule_min_volume_over_axes_with_spherical_cap_height"`;
  - `axis_selection_policy == "min_volume_capsule_axis"`;
  - `newton_runtime_kind == "capsule"`;
  - three `paper_capsule_axis_candidates`;
  - selected candidate volume equal to the row volume;
  - containment true.
- [x] Run:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice -q`
  and confirm it fails for the missing capsule audit behavior.

### Task 2: Implementation

**Files:**

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [x] Change `_CURRENT_PRIMITIVE_SUBSET` to `("box", "sphere")`.
- [x] Remove `capsule` from `_PAPER_PRIMITIVE_NAMES` and `_NEWTON_RUNTIME_KIND`.
- [x] Remove `paper_capsule_axis_policy` from `missing_before_paper_faithful`.
- [x] Set `next_required_gate` to `paper_priority_queue_trace_audit`.
- [x] Append `_paper_capsule_candidate_payload(mesh, face_group)` after current box/sphere rows.
- [x] Add helper that computes three capsule axis candidates using the paper spherical-cap height
  equation and selects minimum volume.
- [x] Run the RED test and confirm it passes.

### Task 3: Docs And Record

**Files:**

- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/index.md`
- Modify: `docs/records/README.md`
- Modify: `experiments/registry.yaml`
- Create: `docs/records/2026-05-16-cpd-paper-capsule-axis-audit.md`

- [x] Update current paper-lane wording to say capsule has an offline paper-shaped axis audit row.
- [x] Keep `status: partial` and `paper_faithful_offline_supported: false`.
- [x] Add dated verification and review notes.

### Task 4: Verification And Review

- [x] Run focused pytest for CPD paper offline and CLI report tests.
- [x] Run CLI smoke:
  `python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report`.
- [x] Run `python -m pytest -q`.
- [x] Run `python scripts/validate_docs.py`.
- [x] Run `python scripts/validate_site_claims.py`.
- [x] Run `git diff --check`.
- [x] Request multi-agent review for implementation and docs/claim boundaries.
- [x] Fix Critical/Important review findings before commit.

### Task 5: Commit

- [ ] Commit with message `feat: audit CPD paper capsule axis policy`.
- [ ] Push `main`.
- [ ] Confirm `git status --short` is clean.
