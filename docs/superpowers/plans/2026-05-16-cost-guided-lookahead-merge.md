# Cost-Guided Lookahead Merge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an explicitly opt-in synthetic two-step merge/search lookahead smoke that changes one deterministic toy grouping without changing default behavior, real-USD behavior, package probes, or Newton task probes.

**Architecture:** Extend the existing CPD-like merge/search policy layer with a bounded `two_step_lookahead` policy. The policy reuses the existing legal candidate generation, normalized merge-excess scoring, trace rows, virtual threshold gate, and deterministic tie-breaks, but scores each first merge by immediate plus best follow-up cost on copied tiny-mesh state.

**Tech Stack:** Python, pytest, existing CPD-like decomposition/report code, strict JSON CLI output, Markdown records and claim-boundary docs.

---

## File Structure

- `src/primitive_collision_compiler/baselines/cpd_like/decompose.py`
  Owns the new policy constant, validation, tiny-mesh guard, candidate enumeration, two-step scoring, and trace metadata.
- `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
  Owns the `lookahead_merge_trap` synthetic fixture and command-only report builder.
- `src/primitive_collision_compiler/cli.py`
  Owns the no-config CLI flag and strict JSON handling.
- `tests/test_cpd_like_decompose.py`
  Owns decomposition-level RED/GREEN tests for policy validation, changed grouping, threshold behavior, and guard behavior.
- `tests/test_cpd_like_synthetic.py`
  Owns synthetic report tests and strict JSON serialization tests.
- `tests/test_cli.py`
  Owns CLI smoke, non-finite JSON rejection, and partial exit-code tests.
- `docs/records/2026-05-16-cost-guided-lookahead-merge.md`
  Owns dated evidence and verification notes.
- `experiments/registry.yaml`, `docs/records/README.md`, `docs/reference/claim-boundaries.md`,
  `docs/deepdive/evidence-status.md`, `docs/index.md`,
  `docs/reference/cpd-paper-story-status.md`,
  `docs/reference/cpd-latest-diagnostic-loop-explainer.md`,
  `docs/reference/cpd-like-face-merge-explainer.md`
  Own discoverability and claim-boundary updates.

## Task 1: Add RED Decomposition Tests

**Files:**
- Modify: `tests/test_cpd_like_decompose.py`

- [x] Add `_lookahead_merge_trap_mesh()` helper beside `_cost_guided_pair_choice_mesh()`.
- [x] Add `test_decompose_mesh_two_step_lookahead_changes_first_merge_on_trap`.
- [x] Assert greedy `cost_guided_pairwise` keeps the known trap grouping `((0, 2, 3), (1,))`.
- [x] Assert opt-in `two_step_lookahead` produces paired grouping `((0, 1), (2, 3))`.
- [x] Assert the lookahead accepted normalized-excess sum is lower than the greedy accepted
  normalized-excess sum on this fixture.
- [x] Assert lookahead trace exposes `projected_followup_normalized_excess_volume` and
  `projected_total_normalized_excess_volume` on the first accepted step.
- [x] Add `test_decompose_mesh_two_step_lookahead_requires_virtual_pairwise`.
- [x] Add `test_decompose_mesh_two_step_lookahead_rejects_non_tiny_mesh`.
- [x] Add `test_decompose_mesh_two_step_lookahead_preserves_virtual_threshold_block`.

Expected RED:

```bash
PYTHONPATH=src python -m pytest -q \
  tests/test_cpd_like_decompose.py::test_decompose_mesh_two_step_lookahead_changes_first_merge_on_trap \
  tests/test_cpd_like_decompose.py::test_decompose_mesh_two_step_lookahead_requires_virtual_pairwise \
  tests/test_cpd_like_decompose.py::test_decompose_mesh_two_step_lookahead_rejects_non_tiny_mesh \
  tests/test_cpd_like_decompose.py::test_decompose_mesh_two_step_lookahead_preserves_virtual_threshold_block
```

Failure should mention unknown `two_step_lookahead` or missing trace metadata.

## Task 2: Implement Bounded Two-Step Lookahead Policy

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/decompose.py`

- [x] Add `MERGE_SEARCH_TWO_STEP_LOOKAHEAD = "two_step_lookahead"`.
- [x] Add `TWO_STEP_LOOKAHEAD_MAX_FACE_COUNT = 6`.
- [x] Extend `_validate_component_merge_options(...)` so `two_step_lookahead` is known and
  requires `component_merge == COMPONENT_MERGE_VIRTUAL_PAIRWISE`.
- [x] Add a runtime guard in `decompose_mesh(...)` that raises `ValueError` if
  `merge_search_policy == MERGE_SEARCH_TWO_STEP_LOOKAHEAD` and `mesh.face_count > 6`.
- [x] Add `_all_merge_candidates(...)` to enumerate legal topology and virtual candidates using
  the same adjacency and connected-component rules as `_best_merge(...)`.
- [x] Refactor `_best_merge(...)` to use `_all_merge_candidates(...)` or keep it behaviorally
  identical while sharing candidate construction.
- [x] Add `_best_two_step_lookahead_merge(...)`:
  - enumerate all legal first-step candidates;
  - copy `clusters`, `fits`, `component_ids`, and `connected_component_ids`;
  - simulate `_accept_merge(...)` on the copy;
  - if another merge is still needed, choose the best legal follow-up by existing one-step
    normalized-excess ordering;
  - score by immediate plus follow-up normalized excess;
  - tie-break by projected total, immediate cost, topology before virtual, left id, right id.
- [x] Add projected follow-up and projected total metadata to `_MergeCandidate` with defaults, or
  add an explicit trace metadata path that does not affect existing candidates.
- [x] Route `MERGE_SEARCH_TWO_STEP_LOOKAHEAD` through the main merge loop.
- [x] Preserve virtual threshold blocking exactly as current cost-guided policy does.
- [x] Preserve existing `cost_guided_pairwise`, `topology_then_virtual`, and trace behavior.

Run:

```bash
PYTHONPATH=src python -m pytest -q tests/test_cpd_like_decompose.py -k "lookahead or cost_guided or merge_search"
```

Expected GREEN for the new decomposition tests and no regressions in existing cost-guided tests.

## Task 3: Add Synthetic Report And CLI RED Tests

**Files:**
- Modify: `tests/test_cpd_like_synthetic.py`
- Modify: `tests/test_cli.py`

- [x] Import the new report builder and claim-boundary constant.
- [x] Add `test_cost_guided_lookahead_merge_report_compares_greedy_and_lookahead`.
- [x] Assert report stage `cpd_like_cost_guided_lookahead_merge_report`.
- [x] Assert greedy policy `cost_guided_pairwise` and lookahead policy `two_step_lookahead`.
- [x] Assert `lookahead_decision_changed is True`.
- [x] Assert `projected_cost_improved is True`.
- [x] Assert `default_pipeline_changed is False`.
- [x] Assert `newton_task_comparison_triggered is False`.
- [x] Assert `real_usd_rerun_triggered is False`.
- [x] Assert both `collision_quality_claim_supported` and
  `merge_policy_superiority_claim_supported` are false.
- [x] Add strict JSON serialization test with `json.dumps(..., allow_nan=False)`.
- [x] Add CLI test for
  `--run-cpd-like-cost-guided-lookahead-merge-report`.
- [x] Add CLI non-finite JSON rejection test.

Expected RED:

```bash
PYTHONPATH=src python -m pytest -q \
  tests/test_cpd_like_synthetic.py::test_cost_guided_lookahead_merge_report_compares_greedy_and_lookahead \
  tests/test_cpd_like_synthetic.py::test_cost_guided_lookahead_merge_report_is_strict_json_serializable \
  tests/test_cli.py::test_cli_run_cpd_like_cost_guided_lookahead_merge_report_emits_json \
  tests/test_cli.py::test_cli_run_cpd_like_cost_guided_lookahead_merge_report_rejects_nonfinite_json
```

Failure should mention missing report builder, missing claim constant, or missing CLI flag.

## Task 4: Implement Synthetic Report And CLI

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- Modify: `src/primitive_collision_compiler/cli.py`

- [x] Add claim/evidence/status constants:
  `COST_GUIDED_LOOKAHEAD_MERGE_CLAIM_BOUNDARY`,
  `COST_GUIDED_LOOKAHEAD_MERGE_EVIDENCE_LEVEL`,
  `COST_GUIDED_LOOKAHEAD_MERGE_STATUS_SEMANTICS`.
- [x] Add `_lookahead_merge_trap_mesh()` using the deterministic four-triangle coordinates from
  the decomposition test.
- [x] Add `build_cpd_like_cost_guided_lookahead_merge_report()`.
- [x] Run greedy and lookahead lanes with:
  `component_merge="virtual_pairwise"`, `max_primitives=2`, `primitive_subset=("box",)`,
  `report_merge_trace="steps"`.
- [x] Include lane summaries, source-face groupings, merge traces, accepted normalized-excess
  sums, first-step projected costs, and decision flags.
- [x] Add CLI flag `--run-cpd-like-cost-guided-lookahead-merge-report`.
- [x] Emit strict JSON with `allow_nan=False`.
- [x] Return exit code 0 only for `smoke_passed`.

Run:

```bash
PYTHONPATH=src python -m pytest -q \
  tests/test_cpd_like_synthetic.py::test_cost_guided_lookahead_merge_report_compares_greedy_and_lookahead \
  tests/test_cpd_like_synthetic.py::test_cost_guided_lookahead_merge_report_is_strict_json_serializable \
  tests/test_cli.py::test_cli_run_cpd_like_cost_guided_lookahead_merge_report_emits_json \
  tests/test_cli.py::test_cli_run_cpd_like_cost_guided_lookahead_merge_report_rejects_nonfinite_json
```

Expected GREEN.

## Task 5: Update Docs, Registry, And Records

**Files:**
- Create: `docs/records/2026-05-16-cost-guided-lookahead-merge.md`
- Modify: `docs/records/README.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/index.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/cpd-latest-diagnostic-loop-explainer.md`
- Modify: `docs/reference/cpd-like-face-merge-explainer.md`
- Modify: `experiments/registry.yaml`

- [x] Add dated record with RED/GREEN, CLI smoke, review, verification, and claim boundary.
- [x] Add registry entry after the controlled merge-search Newton probe.
- [x] Update CPD story docs to say the next merge/search algorithmic slice is synthetic
  two-step lookahead accounting, not package, Newton, real-USD, or quality evidence.
- [x] Update claim boundaries to allow only synthetic two-step merge-search lookahead smoke.
- [x] Update unsupported claims to keep real-USD, package, Newton task, collision quality,
  benchmark, and CPD reproduction out of scope.

Run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

## Task 6: Review And Verify

- [x] Request implementation review from a fresh read-only agent.
- [x] Request documentation/claim-boundary review from a fresh read-only agent.
- [x] Fix all Critical and Important findings.
- [x] Re-run focused tests:

```bash
PYTHONPATH=src python -m pytest -q \
  tests/test_cpd_like_decompose.py -k "lookahead or cost_guided or merge_search" \
  tests/test_cpd_like_synthetic.py -k "lookahead" \
  tests/test_cli.py -k "lookahead"
```

- [x] Run CLI smoke:

```bash
PYTHONPATH=src python -m primitive_collision_compiler.cli \
  --run-cpd-like-cost-guided-lookahead-merge-report
```

- [x] Run full verification:

```bash
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

- [x] Mark the plan and dated record complete only after review and verification pass.

## Self-Review

Spec coverage: every requirement in
`docs/superpowers/specs/2026-05-16-cost-guided-lookahead-merge-design.md` maps to a task above.
No placeholders remain. Function names, report names, and policy names consistently use
`two_step_lookahead` for the merge-search policy and
`cpd_like_cost_guided_lookahead_merge_report` for the report stage.
