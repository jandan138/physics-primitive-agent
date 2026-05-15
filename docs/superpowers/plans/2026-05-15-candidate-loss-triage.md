# Candidate Loss Triage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a claim-bounded triage layer to the real-USD candidate-loss diagnosis so the next
primitive-fitting or merge-search target can be selected from ranked diagnostic rows.

**Architecture:** Keep the triage inside the existing candidate-loss report builder. It will read
the already generated per-cluster candidate rows, compute relative near-miss gaps for box-selected
clusters, group the likely next targets by extension kind and bottleneck, and emit deterministic
JSON metadata. No new optimizer or collision-quality metric is introduced.

**Tech Stack:** Python, pytest, existing CPD-like baseline report builders, existing docs and
records.

---

### Task 1: Candidate-Loss Triage Metadata

**Files:**
- Modify: `tests/test_real_usd_native_comparison.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/real_usd_comparison.py`

- [x] **Step 1: Write failing test**

Add a test that monkeypatches candidate costs to make `cylinder` a near miss behind selected
`box`, then assert the candidate-loss diagnosis contains a `triage` section with a ranked
near-miss row and a recommended next slice.

- [x] **Step 2: Verify RED**

Run:

```bash
python -m pytest -q tests/test_real_usd_native_comparison.py::test_real_usd_candidate_loss_diagnosis_triages_near_miss_extension_targets
```

Expected: fail because the report does not yet contain `triage`.

- [x] **Step 3: Implement triage metadata**

Add helpers in `real_usd_comparison.py` that:

- compute `relative_extension_gap = (best_extension_cost - selected_cost) / selected_cost`;
- classify near misses under a fixed diagnostic threshold;
- rank near misses by relative gap, then asset cluster index;
- count near misses by extension primitive kind;
- emit a first recommended next slice when a near miss exists.

- [x] **Step 4: Verify GREEN**

Run the targeted test and then the full real-USD comparison test file.

### Task 2: Documentation And Local-State Hygiene

**Files:**
- Modify: `.gitignore`
- Modify: `docs/reference/cpd-latest-diagnostic-loop-explainer.md`
- Create: `docs/records/2026-05-15-candidate-loss-triage.md`
- Modify: `docs/records/README.md`
- Modify: `docs/index.md`

- [x] **Step 1: Ignore local agent settings**

Add `.claude/` to the local machine-specific ignore block so local tool state does not keep the
worktree dirty.

- [x] **Step 2: Document triage output**

Update the latest diagnostic-loop explainer with a short section explaining how the new triage
metadata turns candidate-loss rows into the next synthetic target recommendation.

- [x] **Step 3: Add dated record**

Record the triage report change, verification commands, and claim boundary.

### Task 3: Verification And Review

**Files:**
- No production files beyond Tasks 1 and 2.

- [x] **Step 1: Run targeted tests**

```bash
python -m pytest -q tests/test_real_usd_native_comparison.py tests/test_cli.py
```

- [x] **Step 2: Run full tests and docs checks**

```bash
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

- [x] **Step 3: Request review**

Ask code/docs review agents to inspect the triage metadata, claim boundaries, and tests before
committing.
