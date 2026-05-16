# 2026-05-16 Four-Block Slice Report

## Date

2026-05-16

## Status

Complete

## Changes

- Added `cpd_like_four_block_slice_report`, a command-only report for the recorded
  `cost_guided_lookahead` synthetic slice.
- Added `--run-cpd-like-four-block-slice-report`, a config-free CLI entry point that emits strict
  JSON and returns success only when the record map is complete.
- The report summarizes four workbench blocks:
  primitive fitting/selection, merge/search, offline diagnostic reports, and Newton task
  comparison.
- The report reads repository record-path metadata only. It does not invoke decomposition helpers,
  source lookahead report builders, USD loaders, Newton contact smokes, drop/settle, or
  sphere-rain.

## Verification

- `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py -k "four_block_slice_report" tests/test_cli.py -k "four_block_slice_report"`:
  `10 passed, 159 deselected`.
- `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-four-block-slice-report`:
  exit `0`, top-level `status` was `smoke_passed`, and `newton_task_comparison_triggered` was
  `false`.
- `python -m pytest -q`: `389 passed in 43.01s`.
- `python scripts/validate_docs.py`: `docs validation passed`.
- `python scripts/validate_site_claims.py`: `site claim validation passed`.
- `git diff --check`: passed with no output.

## Review

- Implementation review reported no Critical or Important findings. Minor hardening was applied:
  missing-record blocks now become `partial`, summary wording was narrowed to
  `four_block_record_map_complete`, and CLI-level no-runtime-call coverage was added.
- Documentation/claim-boundary review reported two Important freshness issues. The index/status
  wording, latest-loop next-step wording, registry status, and evidence status were updated so the
  four-block report is consistently represented as complete after verification.
- Final implementation review reported one Important missing-record overclaim. Missing-record
  blocks now clear `claim_supported` and add an explicit claim-withheld note until evidence
  records exist.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- `src/primitive_collision_compiler/cli.py`
- `tests/test_cpd_like_synthetic.py`
- `tests/test_cli.py`
- `docs/superpowers/specs/2026-05-16-four-block-slice-report-design.md`
- `docs/superpowers/plans/2026-05-16-four-block-slice-report.md`

## Claim Impact

- Supports only a command-only four-block evidence map for an already recorded synthetic slice.
- Does not support a new Newton task result, real-USD result, bed/Franka result, collision-quality
  result, policy ranking, benchmark claim, deployment/certification claim, or completed CPD paper
  reproduction.

## Next Action

- Use the four-block report as the review checklist for the next bounded paper-aligned objective,
  primitive-fitting, or merge/search slice.
- Keep bed/Franka reruns blocked until a separate real package change passes full mapping,
  contact-canary, task-gate, and dated-record gates.
