# 2026-05-16 Cost-Guided Merge Step Trace

## Date

2026-05-16

## Status

Complete

## Changes

- Added `report_merge_trace: steps` as an opt-in CPD-like merge trace mode.
- Added `merge_trace` to `CPDLikeDecompositionReport`.
- Extended the existing cost-guided synthetic comparison so the `cost_guided_pair_choice` fixture
  can expose accepted merge steps for inspection.
- Extended config-driven `--run-cpd-like` so `cpd_like.report_merge_trace: steps` serializes trace
  rows in JSON output.

## Result

Focused RED/GREEN tests show:

- `cost_guided_pairwise` on `cost_guided_pair_choice` records one accepted virtual-component merge
  step;
- threshold-blocked virtual merges record one blocked step with
  `component_merge_threshold_blocked`;
- trace rows record source faces, source component ids, connected component ids, merged primitive
  type, raw excess volume, and AABB-normalized excess volume.

This is synthetic offline merge-step trace diagnostic accounting. It does not change the merge
policy, primitive fitting, generated real-USD packages, or Newton task execution.

## Verification

- RED:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_decompose.py::test_decompose_mesh_steps_trace_records_cost_guided_virtual_merge tests/test_cpd_like_decompose.py::test_decompose_mesh_steps_trace_records_blocked_virtual_merge`
  failed because `report_merge_trace: steps` was invalid.
- RED:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cost_guided_synthetic_comparison_shows_old_new_merge_decision tests/test_cli.py::test_cli_run_cpd_like_accepts_cost_guided_merge_search_policy`
  failed because synthetic summaries and CLI JSON did not expose `merge_trace`.
- GREEN:
  both focused RED commands passed after implementation.
- Full verification:
  `python -m pytest -q` passed with 311 tests,
  `python scripts/validate_docs.py` passed,
  `python scripts/validate_site_claims.py` passed, and
  `git diff --check` passed.
- CLI smoke:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cost-guided-synthetic-comparison`
  returned `smoke_passed` and emitted `merge_trace` rows for the traced policies.
- Multi-agent review:
  implementation review found two Important integration issues: default JSON exposed
  `merge_trace: []`, and synthetic summaries assumed the key was always present. Both were fixed
  with regression tests. Docs review found Important wording drift; it was fixed by standardizing
  "synthetic offline merge-step trace diagnostic accounting" across the record, registry, index,
  claim boundaries, evidence status, and explainers. Re-review found no Critical or Important
  issues.

## Claim Impact

This record supports only synthetic offline merge-step trace diagnostic accounting for a
deterministic cost-guided merge fixture. It makes a merge decision inspectable; it does not show
better decomposition, collision quality, benchmark performance, Newton task improvement,
paper-faithful search behavior, CPD paper optimizer behavior, or CPD reproduction.

## Next Action

Use the trace to design a controlled merge/search change or an opt-in package probe. Do not run
bed/Franka Newton task comparison until a default or explicitly experimental package changes and
maps fully.
