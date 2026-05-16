# Controlled Merge-Search Package Probe Plan

## Task 1: Add RED Tests

**Files:**
- Modify: `tests/test_cpd_like_synthetic.py`
- Modify: `tests/test_cli.py`

- [x] Add report-builder test for `build_cpd_like_controlled_merge_search_package_probe_report`.
- [x] Assert default source faces `[[0, 1], [2]]` and opt-in source faces `[[0, 2], [1]]`.
- [x] Assert both package lanes fully map through Newton shape mapping.
- [x] Add strict-JSON test.
- [x] Add CLI smoke and nonzero partial tests.

Expected RED: import/CLI collection fails because the constant, report builder, and flag do not
exist.

## Task 2: Implement Synthetic Package Probe

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- Modify: `src/primitive_collision_compiler/cli.py`

- [x] Add claim/evidence/status-semantics constants.
- [x] Add `build_cpd_like_controlled_merge_search_package_probe_report`.
- [x] Build default `topology_then_virtual` and opt-in `cost_guided_pairwise` packages for the
  existing `cost_guided_pair_choice` fixture.
- [x] Record primitive source-face groupings, merge traces, surrogate merge-excess delta, and Newton
  shape-mapping summaries.
- [x] Add `--run-cpd-like-controlled-merge-search-package-probe`.
- [x] Keep this command synthetic-only, command-only, mapping-only, and task-free.

## Task 3: Update Docs And Registry

**Files:**
- Create: `docs/records/2026-05-16-controlled-merge-search-package-probe.md`
- Modify: `docs/records/README.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/index.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/cpd-latest-diagnostic-loop-explainer.md`
- Modify: `docs/reference/cpd-like-face-merge-explainer.md`
- Modify: `experiments/registry.yaml`

- [x] Add dated record.
- [x] Add safe and forbidden claim wording.
- [x] Update status explainers and record indexes.
- [x] Add registry entry after the cost-guided merge-step trace entry.

## Task 4: Review And Verify

- [x] Request implementation review.
- [x] Request docs/claim-boundary review.
- [x] Fix Critical and Important findings.
- [x] Run focused tests.
- [x] Run CLI smoke.
- [x] Run full tests, docs validation, site claims, and `git diff --check`.
