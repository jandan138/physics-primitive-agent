# 2026-05-16 CPD Paper Priority Queue Trace Audit

## Date

2026-05-16

## Status

Complete

## Changes

- Added `paper_three_face_chain`, a deterministic synthetic fixture for topology-only
  priority-queue trace auditing.
- Recorded initial topology-adjacent queue candidates, paper base cost, weighted priority cost,
  deterministic queue keys, accepted merge events, eager stale-prune events, updated neighbor
  insertion counts, threshold-disabled fields, final active groups, and target-count stop reason.
- Advanced the next paper-lane gate to component-pair edge insertion.
- Kept the command in the offline paper lane: no package generation, no Newton runtime invocation,
  no real USD, no benchmark, and no collision-quality claim.

## Verification

- `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  passed with 2 tests.
- `python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  passed with 5 tests.
- `python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report` emitted JSON with
  `status: partial`, `next_required_gate: paper_component_pair_edge_insertion_audit`,
  `paper_three_face_chain`, `priority_queue_trace_audit_topology_only`,
  `accepted_merge_count: 2`, `stale_entry_skipped_count: 1`, `blocked_merge_count: 0`,
  `stop_reason: target_count_reached`, `package_generation_triggered: false`, and no Newton,
  real-USD, or benchmark trigger.
- `python -m pytest -q` passed with 412 tests.
- `python scripts/validate_docs.py` passed.
- `python scripts/validate_site_claims.py` passed.
- `git diff --check` passed with no output.

## Multi-Agent Review

- Documentation and claim-boundary review found a completion-state mismatch between the registry,
  current docs, and this dated record; it also found missing fixture-table and artifact-list
  traceability. This record was updated to `Complete`, concrete verification evidence was added,
  `paper_three_face_chain` was added to the canonical fixture table, stale target/threshold wording
  was refreshed, changed documentation artifacts were added below, stale spec wording was updated,
  and Task 5 commit/push/clean-status checkboxes remain unchecked until those commands actually run.
- Queue algorithm and schema review found no Critical issues. It required a machine-checkable
  package-generation trigger boundary and tighter stale-prune event ordering tests. The trace now
  records `package_generation_triggered: false`, and tests pin the deterministic accepted/pruned
  event sequence plus `event_kind` and `blocked` fields.
- Final narrow re-reviews reported no remaining Critical, Important, or Minor issues in the
  previously reviewed code/test/schema surface and no remaining Critical, Important, or Minor
  documentation consistency issue.

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
- `docs/superpowers/specs/2026-05-16-cpd-paper-priority-queue-trace-audit-design.md`
- `docs/superpowers/plans/2026-05-16-cpd-paper-priority-queue-trace-audit.md`
- `experiments/registry.yaml`

## Claim Impact

- Supports only a partial, fixture-scoped, command-only topology priority-queue trace audit.
- Does not support `paper_faithful_offline`, full CPD paper reproduction, component-pair edge
  insertion, Newton runtime support, package generation, real-USD evidence, benchmark evidence,
  collision-quality validation, deployment readiness, or safety certification.

## Next Action

- Add disconnected component-pair edge insertion using the same paper cost and trace schema.
