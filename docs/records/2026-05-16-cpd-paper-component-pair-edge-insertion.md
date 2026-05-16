# 2026-05-16 CPD Paper Component-Pair Edge Insertion

## Date

2026-05-16

## Status

Complete

## Changes

- Added `paper_disconnected_components`, a deterministic disconnected two-triangle fixture for
  threshold-disabled component-pair edge insertion auditing.
- Extended the offline paper-lane priority queue so an empty topology queue can trigger
  component-pair candidate insertion before declaring queue exhaustion.
- Recorded component-pair policy, topology-exhaustion trigger, cumulative component-pair candidate
  count, candidate cap, accepted `component_pair` event fields, target-count stop reason, and
  package/Newton/real-USD/benchmark trigger boundaries.
- Advanced the next paper-lane gate to component-pair threshold blocking.
- Kept the command in the offline paper lane: no package generation, no Newton runtime invocation,
  no real USD, no benchmark, and no collision-quality claim.

## Verification

- `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  failed in the RED step for the old `component_pair_edge_insertion_missing` label and the missing
  `paper_disconnected_components` case.
- `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  passed with 2 tests after implementation.
- `python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cli.py::test_cli_run_cpd_paper_offline_report_rejects_nonfinite_json -q`
  passed with 6 tests.
- `python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report` emitted JSON with
  `status: partial`, `next_required_gate: paper_component_pair_threshold_blocking_audit`,
  `component_pair_threshold_blocking_missing`, `paper_disconnected_components`,
  `component_pair_edge_insertion_audit_threshold_disabled`,
  `component_pair_edge_policy: insert_when_topology_queue_exhausted_before_target`,
  `component_pair_candidate_count: 1`, `accepted_merge_count: 1`, `blocked_merge_count: 0`, and no
  package, Newton, real-USD, or benchmark trigger.
- `python -m pytest -q` passed with 412 tests.
- `python scripts/validate_docs.py` passed.
- `python scripts/validate_site_claims.py` passed.
- `git diff --check` passed with no output.

## Multi-Agent Review

- Design review found no Critical issues. Important fixes were applied before implementation:
  empty-queue insertion control flow was made explicit, component-pair event schema assertions were
  strengthened, cumulative candidate-count semantics were defined, disabled component-pair cap
  metadata was specified, and threshold blocking was kept as a separate next gate.
- Implementation review found no Critical or Important issues. It noted stale documentation wording
  in the lane spec and paper-story summary; those were updated before commit.
- Documentation and claim-boundary review found two Important stale-doc issues: the docs index CLI
  command entry omitted `paper_disconnected_components`, and the lane spec gate sequence did not
  separate component-pair insertion from component-pair threshold blocking. Both were fixed, and
  final narrow re-reviews reported no remaining Critical, Important, or Minor issues.

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
- `docs/superpowers/specs/2026-05-16-cpd-paper-component-pair-edge-insertion-design.md`
- `docs/superpowers/plans/2026-05-16-cpd-paper-component-pair-edge-insertion.md`
- `experiments/registry.yaml`

## Claim Impact

- Supports only a partial, fixture-scoped, command-only threshold-disabled component-pair insertion
  audit.
- Does not support `paper_faithful_offline`, full CPD paper reproduction, enabled component-pair
  threshold blocking, Newton runtime support, package generation, real-USD evidence, benchmark
  evidence, collision-quality validation, deployment readiness, or safety certification.

## Next Action

- Add enabled component-pair threshold blocking and skipped/blocked pair accounting using the same
  paper cost and trace schema.
