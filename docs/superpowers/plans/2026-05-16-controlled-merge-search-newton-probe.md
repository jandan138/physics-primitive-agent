# Controlled Merge-Search Newton Probe Plan

## Task 1: Add RED Tests

**Files:**
- Modify: `tests/test_cpd_like_synthetic.py`
- Modify: `tests/test_cli.py`
- Modify: `tests/test_cpd_like_config.py`

- [x] Add report-builder test for contact-gated task execution on default and opt-in packages.
- [x] Add contact-failure blocked-task test.
- [x] Add unchanged-package guard test.
- [x] Add strict JSON serialization test.
- [x] Add CLI config-required, config-scope, JSON output, partial, and non-finite JSON tests.
- [x] Add config ownership test for `configs/experiments/controlled_merge_search_newton_probe.yaml`.

Expected RED: imports fail because the claim constant/report builder and CLI flag do not exist.

## Task 2: Implement Synthetic Newton Probe

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- Modify: `src/primitive_collision_compiler/cli.py`
- Create: `configs/experiments/controlled_merge_search_newton_probe.yaml`

- [x] Add claim/evidence/status-semantics constants.
- [x] Add `build_cpd_like_controlled_merge_search_newton_probe_report`.
- [x] Reuse the controlled merge-search package pair.
- [x] Run `run_newton_contact_smoke` first for each lane.
- [x] Run drop/settle and sphere-rain only when contact passes.
- [x] Add CLI flag and config validation.
- [x] Emit strict JSON and return 0 only for `smoke_passed`.

## Task 3: Update Docs And Registry

**Files:**
- Create: `docs/records/2026-05-16-controlled-merge-search-newton-probe.md`
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
- [x] Add registry entry after the controlled package-probe entry.

## Task 4: Review And Verify

- [x] Request implementation review.
- [x] Request docs/claim-boundary review.
- [x] Fix Critical and Important findings.
- [x] Run focused tests.
- [x] Run clean Newton CLI smoke.
- [x] Run full tests, docs validation, site claims, and `git diff --check`.
