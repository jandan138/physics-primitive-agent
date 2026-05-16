# 2026-05-16 CPD Paper Component-Pair Threshold Blocking

## Date

2026-05-16

## Status

Complete

## Changes

- Added `paper_component_pair_threshold_blocked`, a deterministic disconnected two-triangle fixture
  for finite-threshold component-pair blocking.
- Extended the offline paper-lane priority queue with opt-in component-pair threshold metadata using
  `threshold_metric: paper_base_cost` and a zero threshold.
- Tracked attempted component-pair source-face pairs so blocked pairs are not reinserted forever.
- Recorded one blocked `component_pair` event, attempted pair count `1`, skipped pair count `0`,
  active primitive count unchanged, and `all_remaining_edges_blocked_by_threshold` stop reason.
- Advanced the next paper-lane gate to `paper_cpd_postprocess_audit`.
- Kept the command in the offline paper lane: no package generation, no Newton runtime invocation,
  no real USD, no benchmark, and no collision-quality claim.

## Verification

- `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  failed in the RED step for the old `component_pair_threshold_blocking_missing` label and the
  missing `paper_component_pair_threshold_blocked` case.
- `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  passed with 2 tests after implementation.
- `python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cli.py::test_cli_run_cpd_paper_offline_report_rejects_nonfinite_json -q`
  passed with 6 tests.
- `python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report` emitted JSON with
  `status: partial`, `next_required_gate: paper_cpd_postprocess_audit`,
  `paper_component_pair_threshold_blocked`, `component_pair_threshold_blocking_audit`,
  `threshold_policy: component_pair_paper_base_cost_lte_threshold`,
  `accepted_merge_count: 0`, `blocked_merge_count: 1`, `skipped_component_pair_count: 0`,
  `component_pair_attempted_pair_count: 1`, `stop_reason:
  all_remaining_edges_blocked_by_threshold`, and no package, Newton, real-USD, or benchmark trigger.
- `python -m pytest -q` passed with 412 tests.
- `python scripts/validate_docs.py` passed.
- `python scripts/validate_site_claims.py` passed.
- `git diff --check` passed with no output.

## Multi-Agent Review

- Design review found no Critical issues. Important fixes were applied before implementation:
  attempted component-pair tracking was added to prevent reinsertion loops, finite-cost assertions
  were added, skipped component-pair count was recorded as `0`, and cap-skipped fixtures were kept
  explicitly out of scope.
- Final implementation review found no Critical or Important issues. A finite-threshold guard was
  added after review so future non-finite threshold values fail before report serialization.
- Final documentation and claim-boundary review found one Important status mismatch between the
  registry, dated record, and plan. This record was updated to `Complete`, concrete verification was
  added, plan checkboxes were updated, and the cap-skipped fixture boundary was repeated in this
  record and the registry entry.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `docs/index.md`
- `docs/records/README.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/reference/claim-boundaries.md`
- `docs/superpowers/specs/2026-05-16-cpd-paper-component-pair-threshold-blocking-design.md`
- `docs/superpowers/plans/2026-05-16-cpd-paper-component-pair-threshold-blocking.md`
- `experiments/registry.yaml`

## Claim Impact

- Supports only a partial, fixture-scoped, command-only finite-threshold component-pair blocked
  event audit.
- Does not support `paper_faithful_offline`, full CPD paper reproduction, broad threshold-policy
  handling, Newton runtime support, package generation, real-USD evidence, benchmark evidence,
  collision-quality validation, deployment readiness, or safety certification.
- Does not support capped skipped-pair fixtures; this all-pairs toy fixture records
  `skipped_component_pair_count: 0`.

## Next Action

- Add `paper_cpd_postprocess_audit` for enclosed-primitive culling using a named toy fixture.
