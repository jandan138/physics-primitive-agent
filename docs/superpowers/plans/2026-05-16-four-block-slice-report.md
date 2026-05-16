# Four-Block Slice Report Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Add a command-only report that maps one already recorded synthetic slice across the four Newton CPD workbench blocks.

**Architecture:** Implement a small report builder in `synthetic.py` that reads only repository record paths and returns a fixed evidence map for `cost_guided_lookahead`. Add a config-free CLI flag that emits strict JSON and does not invoke USD loading or Newton runtime helpers.

**Tech Stack:** Python, pytest, existing CLI strict JSON pattern, pathlib record checks, Markdown records and claim-boundary docs.

---

## File Structure

- `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
  Owns report constants, required record path metadata, block payload construction, and report
  status.
- `src/primitive_collision_compiler/cli.py`
  Owns the config-free CLI flag and strict JSON handling.
- `tests/test_cpd_like_synthetic.py`
  Owns report behavior, missing-record, and strict JSON tests.
- `tests/test_cli.py`
  Owns CLI JSON, partial-status, and non-finite JSON tests.
- `docs/records/2026-05-16-four-block-slice-report.md`
  Owns dated evidence and verification notes.
- `experiments/registry.yaml`, `docs/records/README.md`, `docs/reference/claim-boundaries.md`,
  `docs/deepdive/evidence-status.md`, `docs/index.md`,
  `docs/reference/cpd-paper-story-status.md`,
  `docs/reference/cpd-latest-diagnostic-loop-explainer.md`
  Own discoverability and claim-boundary updates.

## Task 1: Add RED Report Tests

**Files:**
- Modify: `tests/test_cpd_like_synthetic.py`

- [x] Import `FOUR_BLOCK_SLICE_REPORT_CLAIM_BOUNDARY`.
- [x] Import `build_cpd_like_four_block_slice_report`.
- [x] Add `test_four_block_slice_report_summarizes_cost_guided_lookahead`.
- [x] Assert stage `cpd_like_four_block_slice_report`.
- [x] Assert status `smoke_passed`.
- [x] Assert `slice_id == "cost_guided_lookahead"`.
- [x] Assert `command_only is True`.
- [x] Assert `synthetic_only is True`.
- [x] Assert `real_usd_rerun_triggered is False`.
- [x] Assert `newton_task_comparison_triggered is False` because the report itself does not run
  tasks.
- [x] Assert `report_newton_task_comparison_triggered is False`.
- [x] Assert block ids:
  `primitive_fitting_selection`, `merge_search`, `offline_diagnostic_reports`,
  `newton_task_comparison`.
- [x] Assert primitive fitting block status is `not_changed_for_this_slice`.
- [x] Assert merge/search, offline diagnostics, and Newton task blocks are `complete`.
- [x] Assert every block has at least one existing evidence record path.
- [x] Assert summary `four_block_record_map_complete is True`.
- [x] Assert next action machine fields:
  `blocked_real_asset_rerun is True`,
  `requires_separate_real_package_change is True`, and
  `required_real_asset_gates == ["full_mapping", "contact_canary", "task_gate", "dated_record"]`.
- [x] Assert forbidden payload keys are absent from the whole serialized report:
  `cases`, `greedy_package`, `lookahead_package`, `greedy_contact`, `lookahead_contact`,
  `greedy_tasks`, `lookahead_tasks`, `source_dir`, and `device`.
- [x] Add `test_four_block_slice_report_does_not_rerun_source_reports`.
- [x] Monkeypatch `cpd_synthetic.decompose_mesh`,
  `build_cpd_like_cost_guided_lookahead_merge_report`,
  `build_cpd_like_cost_guided_lookahead_package_probe_report`,
  `build_cpd_like_cost_guided_lookahead_newton_probe_report`,
  `run_newton_contact_smoke`, `run_newton_drop_settle`, and `run_newton_sphere_rain` to raise.
- [x] Assert `build_cpd_like_four_block_slice_report()` still returns `smoke_passed`.
- [x] Add `test_four_block_slice_report_record_paths_are_cwd_independent`.
- [x] Temporarily `chdir` to a temp directory and assert the default report still returns
  `smoke_passed`.
- [x] Add `test_four_block_slice_report_rejects_unsupported_slice`.
- [x] Assert `build_cpd_like_four_block_slice_report(slice_id="unknown")` returns status `partial`
  and `fallback_reason == "unsupported_slice"`.
- [x] Add `test_four_block_slice_report_returns_partial_when_record_missing`.
- [x] Monkeypatch the required record path map so one path is missing.
- [x] Assert status `partial` and missing path is listed.
- [x] Add `test_four_block_slice_report_is_strict_json_serializable`.

Expected RED:

```bash
PYTHONPATH=src python -m pytest -q \
  tests/test_cpd_like_synthetic.py::test_four_block_slice_report_summarizes_cost_guided_lookahead \
  tests/test_cpd_like_synthetic.py::test_four_block_slice_report_returns_partial_when_record_missing \
  tests/test_cpd_like_synthetic.py::test_four_block_slice_report_is_strict_json_serializable
```

Failure should mention missing constants or report builder.

## Task 2: Add RED CLI Tests

**Files:**
- Modify: `tests/test_cli.py`

- [x] Add `test_cli_run_cpd_like_four_block_slice_report_emits_json`.
- [x] Assert `cli.main(["--run-cpd-like-four-block-slice-report"]) == 0`.
- [x] Assert payload stage and status.
- [x] Assert no `greedy_contact` or Newton runtime payloads are present.
- [x] Add `test_cli_run_cpd_like_four_block_slice_report_returns_nonzero_for_partial`.
- [x] Monkeypatch builder to return status `partial`.
- [x] Assert CLI returns 2 and prints JSON.
- [x] Add `test_cli_run_cpd_like_four_block_slice_report_rejects_nonfinite_json`.
- [x] Monkeypatch builder to return `float("nan")`.
- [x] Assert CLI returns 2 and writes a non-finite JSON error.

Expected RED:

```bash
PYTHONPATH=src python -m pytest -q tests/test_cli.py -k "four_block_slice_report"
```

Failure should mention missing CLI flag or builder import.

## Task 3: Implement Report Builder And CLI

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- Modify: `src/primitive_collision_compiler/cli.py`

- [x] Add constants:
  `FOUR_BLOCK_SLICE_REPORT_CLAIM_BOUNDARY`,
  `FOUR_BLOCK_SLICE_REPORT_EVIDENCE_LEVEL`,
  `FOUR_BLOCK_SLICE_REPORT_STATUS_SEMANTICS`.
- [x] Add `_FOUR_BLOCK_COST_GUIDED_LOOKAHEAD_RECORDS` mapping block ids to required record paths.
- [x] Add `_repo_root()` helper based on `Path(__file__).resolve().parents[...]`, not `Path.cwd()`.
- [x] Add `_four_block_record_status(record_paths)`.
- [x] Add `_four_block_payload(block_id, status, summary, record_paths, command_surface, claim_supported, claim_not_supported)`.
- [x] Add `build_cpd_like_four_block_slice_report(slice_id: str = "cost_guided_lookahead")`.
- [x] Return `unsupported_slice` partial report for unsupported slice ids.
- [x] Ensure the builder does not call Newton helpers, USD loaders, or decomposition functions.
- [x] Ensure the report contains no raw source report payloads: no `cases`, package payloads,
  contact payloads, task payloads, `source_dir`, or `device`.
- [x] Add CLI import for `build_cpd_like_four_block_slice_report`.
- [x] Add parser flag `--run-cpd-like-four-block-slice-report`.
- [x] Emit strict JSON with `allow_nan=False`.
- [x] Return exit code 0 only when report status is `smoke_passed`.

Run:

```bash
PYTHONPATH=src python -m pytest -q \
  tests/test_cpd_like_synthetic.py -k "four_block_slice_report" \
  tests/test_cli.py -k "four_block_slice_report"
```

Expected GREEN.

## Task 4: Update Docs, Registry, And Records

**Files:**
- Create: `docs/records/2026-05-16-four-block-slice-report.md`
- Modify: `docs/records/README.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/index.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/cpd-latest-diagnostic-loop-explainer.md`
- Modify: `experiments/registry.yaml`

- [x] Add dated record with RED/GREEN, CLI smoke, review, verification, and claim boundary.
- [x] Add registry entry after `cost-guided-lookahead-newton-probe`.
- [x] Update claim boundaries to allow only command-only four-block evidence mapping.
- [x] Update status docs to say this report integrates existing evidence and does not run Newton
  tasks, real assets, benchmarks, or quality measurements.
- [x] Update next action to choose the next paper-aligned objective/fitting/merge-search slice, or
  real-asset rerun only after a separate real package change plus full gates.

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
  tests/test_cpd_like_synthetic.py -k "four_block_slice_report" \
  tests/test_cli.py -k "four_block_slice_report"
```

- [x] Run CLI smoke:

```bash
PYTHONPATH=src python -m primitive_collision_compiler.cli \
  --run-cpd-like-four-block-slice-report
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
`docs/superpowers/specs/2026-05-16-four-block-slice-report-design.md` maps to a task above. No
placeholders remain. The plan intentionally avoids new algorithmic, Newton runtime, real-asset,
benchmark, quality, deployment, certification, or paper-reproduction claims.
