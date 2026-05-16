# Cost-Guided Lookahead Package Probe Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a command-only synthetic package-path and Newton shape-mapping probe for the `lookahead_merge_trap` greedy versus `two_step_lookahead` package pair.

**Architecture:** Reuse the completed lookahead decomposition pair, convert each lane to `CollisionPackage`, compare package payloads, and summarize Newton shape mappings. This plan does not run Newton contact, drop/settle, sphere-rain, real USD, bed/Franka, benchmark, or collision-quality checks.

**Tech Stack:** Python, pytest, existing CPD-like package conversion helpers, Newton shape mapping, strict JSON CLI output, Markdown records and claim-boundary docs.

---

## File Structure

- `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
  Owns the report constants, decomposition pair helper, package pair helper, report builder, and
  package/mapping case payload.
- `src/primitive_collision_compiler/cli.py`
  Owns the no-config CLI flag and strict JSON handling.
- `tests/test_cpd_like_synthetic.py`
  Owns report behavior and strict JSON serialization tests.
- `tests/test_cli.py`
  Owns CLI JSON, partial exit, and non-finite JSON tests.
- `docs/records/2026-05-16-cost-guided-lookahead-package-probe.md`
  Owns dated evidence and verification notes.
- `experiments/registry.yaml`, `docs/records/README.md`, `docs/reference/claim-boundaries.md`,
  `docs/deepdive/evidence-status.md`, `docs/index.md`,
  `docs/reference/cpd-paper-story-status.md`,
  `docs/reference/cpd-latest-diagnostic-loop-explainer.md`,
  `docs/reference/cpd-like-face-merge-explainer.md`
  Own discoverability and claim-boundary updates.

## Task 1: Add RED Report And CLI Tests

**Files:**
- Modify: `tests/test_cpd_like_synthetic.py`
- Modify: `tests/test_cli.py`

- [x] Import `COST_GUIDED_LOOKAHEAD_PACKAGE_PROBE_CLAIM_BOUNDARY`.
- [x] Import `build_cpd_like_cost_guided_lookahead_package_probe_report`.
- [x] Add `test_cost_guided_lookahead_package_probe_outputs_mapped_changed_package`.
- [x] Assert stage `cpd_like_cost_guided_lookahead_package_probe`.
- [x] Assert `status == "smoke_passed"`.
- [x] Assert top-level `default_pipeline_changed is False`.
- [x] Assert top-level `newton_task_comparison_triggered is False`.
- [x] Assert top-level `real_usd_rerun_triggered is False`.
- [x] Assert case id `lookahead_merge_trap`.
- [x] Assert greedy package source faces `[[0, 2, 3], [1]]`.
- [x] Assert lookahead package source faces `[[0, 1], [2, 3]]`.
- [x] Assert `package_pair_changed is True`.
- [x] Assert `lookahead_package_mapping["fully_mapped"] is True`.
- [x] Assert `lookahead_package_mapping["status_counts"] == {"mapped": 2}`.
- [x] Assert decision gate `not_triggered_synthetic_package_probe_only`.
- [x] Add strict JSON serialization test with `json.dumps(..., allow_nan=False)`.
- [x] Add CLI smoke test for `--run-cpd-like-cost-guided-lookahead-package-probe`.
- [x] Add CLI partial-status nonzero test.
- [x] Add CLI non-finite JSON rejection test.

Expected RED:

```bash
PYTHONPATH=src python -m pytest -q \
  tests/test_cpd_like_synthetic.py::test_cost_guided_lookahead_package_probe_outputs_mapped_changed_package \
  tests/test_cpd_like_synthetic.py::test_cost_guided_lookahead_package_probe_report_is_strict_json_serializable \
  tests/test_cli.py::test_cli_run_cpd_like_cost_guided_lookahead_package_probe_emits_json \
  tests/test_cli.py::test_cli_run_cpd_like_cost_guided_lookahead_package_probe_returns_nonzero_for_partial \
  tests/test_cli.py::test_cli_run_cpd_like_cost_guided_lookahead_package_probe_rejects_nonfinite_json
```

Failure should mention the missing claim constant, report builder, or CLI flag.

## Task 2: Implement Package Probe Report And CLI

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- Modify: `src/primitive_collision_compiler/cli.py`

- [x] Add constants:
  `COST_GUIDED_LOOKAHEAD_PACKAGE_PROBE_CLAIM_BOUNDARY`,
  `COST_GUIDED_LOOKAHEAD_PACKAGE_PROBE_EVIDENCE_LEVEL`,
  `COST_GUIDED_LOOKAHEAD_PACKAGE_PROBE_STATUS_SEMANTICS`.
- [x] Add `_lookahead_merge_decomposition_pair()` that returns greedy `cost_guided_pairwise` and
  lookahead `two_step_lookahead` decompositions on `_lookahead_merge_trap_mesh()`.
- [x] Add `_lookahead_merge_package_pair()` that converts both decompositions with
  `package_from_cpd_like_report`.
- [x] Add `_lookahead_package_probe_case_payload()` that records package summaries, mapping
  summaries, package payload comparison, accepted/projected cost deltas, and decision fields.
- [x] Add `build_cpd_like_cost_guided_lookahead_package_probe_report()`.
- [x] Add CLI flag `--run-cpd-like-cost-guided-lookahead-package-probe`.
- [x] Emit strict JSON with `allow_nan=False`.
- [x] Return exit code 0 only when report status is `smoke_passed`.

Run:

```bash
PYTHONPATH=src python -m pytest -q \
  tests/test_cpd_like_synthetic.py::test_cost_guided_lookahead_package_probe_outputs_mapped_changed_package \
  tests/test_cpd_like_synthetic.py::test_cost_guided_lookahead_package_probe_report_is_strict_json_serializable \
  tests/test_cli.py::test_cli_run_cpd_like_cost_guided_lookahead_package_probe_emits_json \
  tests/test_cli.py::test_cli_run_cpd_like_cost_guided_lookahead_package_probe_returns_nonzero_for_partial \
  tests/test_cli.py::test_cli_run_cpd_like_cost_guided_lookahead_package_probe_rejects_nonfinite_json
```

Expected GREEN.

## Task 3: Update Docs, Registry, And Records

**Files:**
- Create: `docs/records/2026-05-16-cost-guided-lookahead-package-probe.md`
- Modify: `docs/records/README.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/index.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/cpd-latest-diagnostic-loop-explainer.md`
- Modify: `docs/reference/cpd-like-face-merge-explainer.md`
- Modify: `experiments/registry.yaml`

- [x] Add dated record with RED/GREEN, CLI smoke, review, verification, and claim boundary.
- [x] Add registry entry after `cost-guided-lookahead-merge`.
- [x] Update claim boundaries to allow only synthetic lookahead package-path and shape-mapping
  accounting.
- [x] Update status docs to keep Newton contact/task, real USD, collision quality, benchmark, and
  CPD reproduction out of scope.
- [x] Update next action to an explicitly opt-in synthetic Newton task probe only after this
  package/mapping gate completes.

Run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

## Task 4: Review And Verify

- [x] Request implementation review from a fresh read-only agent.
- [x] Request documentation/claim-boundary review from a fresh read-only agent.
- [x] Fix all Critical and Important findings.
- [x] Run focused tests:

```bash
PYTHONPATH=src python -m pytest -q \
  tests/test_cpd_like_synthetic.py -k "lookahead_package" \
  tests/test_cli.py -k "lookahead_package"
```

- [x] Run CLI smoke:

```bash
PYTHONPATH=src python -m primitive_collision_compiler.cli \
  --run-cpd-like-cost-guided-lookahead-package-probe
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
`docs/superpowers/specs/2026-05-16-cost-guided-lookahead-package-probe-design.md` maps to a task
above. No placeholders remain. This plan intentionally does not include Newton contact/task,
real-USD, bed/Franka, benchmark, or collision-quality execution.
