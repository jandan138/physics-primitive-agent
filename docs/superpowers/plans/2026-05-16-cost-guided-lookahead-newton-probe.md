# Cost-Guided Lookahead Newton Probe Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an explicitly opt-in synthetic Newton task-smoke probe for the `lookahead_merge_trap` greedy versus `two_step_lookahead` package pair.

**Architecture:** Reuse the completed lookahead decomposition/package pair, run contact canaries first, and run drop/settle plus sphere-rain only for lanes whose contact canary passes. Keep execution config-scoped and synthetic-only.

**Tech Stack:** Python, pytest, existing CPD-like synthetic report helpers, Newton diagnostic helpers, strict JSON CLI output, YAML experiment config, Markdown records and claim-boundary docs.

---

## File Structure

- `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
  Owns report constants, the report builder, the lookahead Newton case payload, and status
  aggregation for greedy/lookahead lane keys.
- `src/primitive_collision_compiler/cli.py`
  Owns the CLI flag, config validation, strict JSON handling, and error status.
- `configs/experiments/cost_guided_lookahead_newton_probe.yaml`
  Owns recorded synthetic task-smoke runtime settings.
- `tests/test_cpd_like_synthetic.py`
  Owns report-builder, contact-gating, unchanged-package, and JSON serialization tests.
- `tests/test_cli.py`
  Owns CLI config-scope, JSON output, non-finite JSON, and partial-status tests.
- `tests/test_cpd_like_config.py`
  Owns config ownership and claim-boundary checks.
- `docs/records/2026-05-16-cost-guided-lookahead-newton-probe.md`
  Owns dated evidence and verification notes.
- `experiments/registry.yaml`, `docs/records/README.md`, `docs/reference/claim-boundaries.md`,
  `docs/deepdive/evidence-status.md`, `docs/index.md`,
  `docs/reference/cpd-paper-story-status.md`,
  `docs/reference/cpd-latest-diagnostic-loop-explainer.md`,
  `docs/reference/cpd-like-face-merge-explainer.md`
  Own discoverability and claim-boundary updates.

## Task 1: Add RED Report-Builder Tests

**Files:**
- Modify: `tests/test_cpd_like_synthetic.py`

- [x] Import `COST_GUIDED_LOOKAHEAD_NEWTON_PROBE_CLAIM_BOUNDARY`.
- [x] Import `COST_GUIDED_LOOKAHEAD_NEWTON_TASK_CLAIM_BOUNDARY`.
- [x] Import `build_cpd_like_cost_guided_lookahead_newton_probe_report`.
- [x] Add `test_cost_guided_lookahead_newton_probe_runs_contact_gated_tasks`.
- [x] Monkeypatch `cpd_synthetic.run_newton_contact_smoke`, `run_newton_drop_settle`, and
  `run_newton_sphere_rain` to return `_newton_report(..., status="smoke_passed")`.
- [x] Assert calls are exactly:
  `contact/drop/sphere` for `lookahead_merge_trap_cost_guided_pairwise`, then
  `contact/drop/sphere` for `lookahead_merge_trap_two_step_lookahead`.
- [x] Assert stage `cpd_like_cost_guided_lookahead_newton_probe`.
- [x] Assert top-level status `smoke_passed`.
- [x] Assert top-level claim boundary is `COST_GUIDED_LOOKAHEAD_NEWTON_PROBE_CLAIM_BOUNDARY`.
- [x] Assert `real_usd_scope == "not_run_synthetic_only"`.
- [x] Assert `newton_task_comparison_triggered is True`.
- [x] Assert case id `lookahead_merge_trap`.
- [x] Assert greedy package source faces `[[0, 2, 3], [1]]`.
- [x] Assert lookahead package source faces `[[0, 1], [2, 3]]`.
- [x] Assert contact and task statuses are `smoke_passed`.
- [x] Assert decision `claim_boundary == COST_GUIDED_LOOKAHEAD_NEWTON_TASK_CLAIM_BOUNDARY`.
- [x] Assert decision `collision_quality_claim_supported is False`.
- [x] Add `test_cost_guided_lookahead_newton_probe_blocks_tasks_when_contact_fails`.
- [x] Monkeypatch contact to return status `dependency_gap`.
- [x] Monkeypatch tasks to raise `AssertionError("tasks must be blocked when contact fails")`.
- [x] Assert report status is `dependency_gap`.
- [x] Assert decision `status_gate == "newton_tasks_blocked_or_failed"`.
- [x] Assert blocked `drop_settle` and `sphere_rain` payloads contain status
  `blocked_by_contact_canary`.
- [x] Add `test_cost_guided_lookahead_newton_probe_does_not_pass_when_pair_unchanged`.
- [x] Monkeypatch `_lookahead_merge_package_pair` to return the same one-box package twice.
- [x] Assert report status is `partial` and decision `package_pair_changed is False`.
- [x] Add `test_cost_guided_lookahead_newton_probe_does_not_pass_with_wrong_faces`.
- [x] Monkeypatch `_lookahead_merge_package_pair` to return two different packages whose
  `primitive_source_faces` do not match the expected lookahead package-probe faces.
- [x] Assert report status is `partial`, decision `expected_package_faces is False`, and
  `status_gate == "lookahead_package_faces_unexpected"`.
- [x] Add a mixed contact-gating test where greedy contact fails but lookahead contact passes.
- [x] Assert greedy tasks are blocked while lookahead tasks run.
- [x] Add `test_cost_guided_lookahead_newton_probe_report_is_strict_json_serializable`.

Expected RED:

```bash
PYTHONPATH=src python -m pytest -q \
  tests/test_cpd_like_synthetic.py::test_cost_guided_lookahead_newton_probe_runs_contact_gated_tasks \
  tests/test_cpd_like_synthetic.py::test_cost_guided_lookahead_newton_probe_blocks_tasks_when_contact_fails \
  tests/test_cpd_like_synthetic.py::test_cost_guided_lookahead_newton_probe_does_not_pass_when_pair_unchanged \
  tests/test_cpd_like_synthetic.py::test_cost_guided_lookahead_newton_probe_report_is_strict_json_serializable
```

Failure should mention the missing constants or report builder.

## Task 2: Add RED Config And CLI Tests

**Files:**
- Modify: `tests/test_cpd_like_config.py`
- Modify: `tests/test_cli.py`

- [x] Add `test_cost_guided_lookahead_newton_probe_config_is_synthetic_and_claim_bounded`.
- [x] Assert config path `configs/experiments/cost_guided_lookahead_newton_probe.yaml`.
- [x] Assert `asset_id == "cost_guided_lookahead_newton_probe"`.
- [x] Assert `asset_path == "synthetic://lookahead_merge_trap"`.
- [x] Assert `task == "synthetic_cost_guided_lookahead_newton_probe"`.
- [x] Assert `verify == ("cpd_like_cost_guided_lookahead_newton_probe",)`.
- [x] Assert `newton.source_dir == "$NEWTON_SOURCE_DIR"`.
- [x] Add CLI tests:
  - requires `--config`;
  - rejects missing `newton.source_dir`;
  - rejects wrong fixture;
  - rejects wrong task;
  - rejects missing verify;
  - emits JSON and passes config-derived options to the builder;
  - rejects non-finite JSON;
  - returns nonzero for partial status.

Expected RED:

```bash
PYTHONPATH=src python -m pytest -q \
  tests/test_cpd_like_config.py::test_cost_guided_lookahead_newton_probe_config_is_synthetic_and_claim_bounded \
  tests/test_cli.py -k "cost_guided_lookahead_newton_probe"
```

Failure should mention missing config, CLI flag, validation, or builder import.

## Task 3: Implement Report Builder, Config, And CLI

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- Modify: `src/primitive_collision_compiler/cli.py`
- Create: `configs/experiments/cost_guided_lookahead_newton_probe.yaml`

- [x] Add constants:
  `COST_GUIDED_LOOKAHEAD_NEWTON_PROBE_CLAIM_BOUNDARY`,
  `COST_GUIDED_LOOKAHEAD_NEWTON_CONTACT_CLAIM_BOUNDARY`,
  `COST_GUIDED_LOOKAHEAD_NEWTON_TASK_CLAIM_BOUNDARY`,
  `COST_GUIDED_LOOKAHEAD_NEWTON_PROBE_EVIDENCE_LEVEL`,
  `COST_GUIDED_LOOKAHEAD_NEWTON_PROBE_STATUS_SEMANTICS`.
- [x] Add `build_cpd_like_cost_guided_lookahead_newton_probe_report(...)`.
- [x] Add `_lookahead_newton_probe_case_payload(...)`.
- [x] Add `_lookahead_newton_probe_statuses(case_payload)`.
- [x] Use `_lookahead_newton_probe_statuses(case_payload)` for both top-level status aggregation
  and decision `status_gate`; do not reuse `_newton_probe_statuses`, which is keyed for
  `default_*` and `opt_in_*` lanes.
- [x] Reuse `_lookahead_merge_decomposition_pair()`, `_lookahead_merge_package_pair(...)`, and
  `_synthetic_task_probe_payloads(...)`.
- [x] Use lane keys `greedy_contact`, `lookahead_contact`, `greedy_tasks`, and `lookahead_tasks`.
- [x] Set decision fields:
  `package_pair_changed`, `lookahead_package_changed`, `merge_search_behavior_changed`,
  `status_gate`, `newton_task_comparison_triggered`, `real_usd_rerun_triggered`,
  `collision_quality_claim_supported`, `merge_policy_superiority_claim_supported`, and
  `claim_boundary`.
- [x] Treat `newton_task_comparison_triggered` as the existing schema-compatible smoke-trigger
  flag only. Do not use it as a policy ranking or superiority signal.
- [x] Gate `smoke_passed` on the exact expected package faces:
  greedy `[[0, 2, 3], [1]]` and lookahead `[[0, 1], [2, 3]]`.
- [x] Add CLI flag `--run-cpd-like-cost-guided-lookahead-newton-probe`.
- [x] Add `_validate_cost_guided_lookahead_newton_probe_config(config)`.
- [x] Add `_cost_guided_lookahead_newton_probe_error_status(message)`.
- [x] Emit strict JSON with `allow_nan=False`.
- [x] Return exit code 0 only when report status is `smoke_passed`.
- [x] Create `configs/experiments/cost_guided_lookahead_newton_probe.yaml` using the same Newton
  task settings as `controlled_merge_search_newton_probe.yaml`, but with the lookahead ids and
  claim boundaries.

Run:

```bash
PYTHONPATH=src python -m pytest -q \
  tests/test_cpd_like_synthetic.py -k "lookahead_newton_probe" \
  tests/test_cpd_like_config.py::test_cost_guided_lookahead_newton_probe_config_is_synthetic_and_claim_bounded \
  tests/test_cli.py -k "cost_guided_lookahead_newton_probe"
```

Expected GREEN.

## Task 4: Update Docs, Registry, And Records

**Files:**
- Create: `docs/records/2026-05-16-cost-guided-lookahead-newton-probe.md`
- Modify: `docs/records/README.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/index.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/cpd-latest-diagnostic-loop-explainer.md`
- Modify: `docs/reference/cpd-like-face-merge-explainer.md`
- Modify: `experiments/registry.yaml`

- [x] Add dated record with RED/GREEN, CLI smoke, review, verification, and claim boundary.
- [x] Add registry entry after `cost-guided-lookahead-package-probe`.
- [x] Update claim boundaries to allow only synthetic lookahead Newton task-smoke status under
  recorded settings.
- [x] Update status docs to keep real assets, bed/Franka, collision geometry quality, benchmark,
  policy ranking, and paper-level reproduction out of scope.
- [x] Update next action to real-asset rerun only after a separate real package change plus full
  mapping, contact-canary, task-gate, and dated-record gates, or to the next paper-aligned
  objective/fitting slice if no real package changes.

Run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

## Task 5: Review And Verify

- [x] Request implementation review from a fresh read-only agent.
- [x] Request documentation/claim-boundary review from a fresh read-only agent.
- [x] Fix all Critical and Important findings.
- [x] Run focused tests:

```bash
PYTHONPATH=src python -m pytest -q \
  tests/test_cpd_like_synthetic.py -k "lookahead_newton_probe" \
  tests/test_cpd_like_config.py::test_cost_guided_lookahead_newton_probe_config_is_synthetic_and_claim_bounded \
  tests/test_cli.py -k "cost_guided_lookahead_newton_probe"
```

- [x] Run clean Newton CLI smoke:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src \
/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m primitive_collision_compiler.cli \
  --config configs/experiments/cost_guided_lookahead_newton_probe.yaml \
  --run-cpd-like-cost-guided-lookahead-newton-probe
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
`docs/superpowers/specs/2026-05-16-cost-guided-lookahead-newton-probe-design.md` maps to a task
above. No placeholders remain. The plan intentionally does not include real assets, bed/Franka,
benchmark, collision-geometry-quality measurement, policy ranking, or paper-level reproduction.
