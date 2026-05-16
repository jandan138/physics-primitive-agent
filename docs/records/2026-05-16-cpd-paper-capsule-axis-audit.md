# 2026-05-16 CPD Paper Capsule Axis Audit

## Date

2026-05-16

## Status

Complete

## Changes

- Replaced the partial `cpd_paper_offline_report` capsule row with an offline paper-shaped
  axis-policy fit-audit row.
- Recorded one capsule candidate per operator axis, selected the minimum-volume candidate, and
  emitted radius, height, half-height, segment endpoints, spherical-cap-adjusted height inputs,
  volume formula, containment status, paper weight, and `newton_runtime_kind: capsule`.
- Kept the command in the offline paper lane: no package generation, no Newton runtime invocation,
  no real USD, no benchmark, and no collision-quality claim.
- Advanced the next paper-lane gate from capsule axis-policy audit to deterministic
  priority-queue trace audit.

## Verification

- `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice -q`
  exited 0; 1 test passed.
- `python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  exited 0; 5 tests passed.
- `python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report` exited 0; the report
  remained `status: partial`, `paper_faithful_offline_supported: false`,
  `newton_runtime_triggered: false`, `real_usd_triggered: false`, `benchmark_triggered: false`,
  and `next_required_gate: paper_priority_queue_trace_audit`.
- `python -m pytest -q` exited 0; 412 tests passed.
- `python scripts/validate_docs.py` exited 0; docs validation passed.
- `python scripts/validate_site_claims.py` exited 0; site claim validation passed.
- `git diff --check` exited 0.
- `npm --prefix site run build` exited 0; Astro built 8 static paper pages.
- Multi-agent review found no Critical or Important issues after fixes to the capsule equation
  regression coverage and design wording.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/claim-boundaries.md`
- `docs/superpowers/specs/2026-05-16-cpd-paper-capsule-axis-audit-design.md`
- `docs/superpowers/plans/2026-05-16-cpd-paper-capsule-axis-audit.md`
- `experiments/registry.yaml`

## Claim Impact

- Supports only a partial, fixture-scoped, command-only offline primitive-fit audit row for the
  paper capsule axis policy.
- Does not support `paper_faithful_offline`, full CPD paper reproduction, Newton runtime support,
  package generation, real-USD evidence, benchmark evidence, collision-quality validation,
  deployment readiness, or safety certification.

## Next Action

- Add the deterministic offline paper priority-queue trace audit with stale-entry pruning,
  accepted/blocked merge records, updated adjacency candidates, and stop reasons.
