# 2026-05-16 CPD Paper Faithful Offline Scope Audit

## Date

2026-05-16

## Status

Complete

## Changes

- Added a top-level `paper_faithful_offline_scope_audit` object to the partial
  `cpd_paper_offline_report`.
- The audit records `decision: remain_partial`, `paper_faithful_offline_allowed: false`, and
  `decision_reason: fixture_scope_still_partial`.
- The criteria table has fourteen rows covering source mesh/preprocessing, source-face intake,
  operator `Q`, primitive vocabulary and fitting, collapse cost and weighting, priority-queue
  trace, target/threshold stops, component-pair handling, enclosed-primitive postprocess,
  report/record reproducibility, package-generation boundary, Newton runtime boundary, real-USD
  boundary, and benchmark boundary.
- The nine paper-mechanics rows are blocking for stronger offline wording; package generation,
  Newton runtime, real USD, and benchmark rows are explicit non-blocking boundaries for this
  offline decision.
- The top-level report remains `status: partial` and
  `paper_faithful_offline_supported: false`.
- The next gate advances from `paper_faithful_offline_scope_audit` to
  `paper_fixture_breadth_expansion_plan`.

## Verification

- RED command:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_failure_labels_point_to_fixture_breadth_gap tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_fixture_breadth_plan tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  - Result before implementation: failed on the old `paper_faithful_offline_scope_missing`
    failure label and old `paper_faithful_offline_scope_audit` gate.
- GREEN command:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_failure_labels_point_to_fixture_breadth_gap tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_fixture_breadth_plan tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  - Result after implementation: `4 passed`.
- Review-fix focused verification:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  - Result after replacing the over-strong report-schema evidence sentence: `2 passed`.
- Focused verification:
  `python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cli.py::test_cli_run_cpd_paper_offline_report_rejects_nonfinite_json -q`
  - Result: `9 passed`.
- CLI smoke:
  `python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report`
  - Result: exited `0` and emitted strict JSON with
    `failure_labels: ["paper_fixture_breadth_expansion_missing"]`,
    `next_required_gate: "paper_fixture_breadth_expansion_plan"`,
    `decision: "remain_partial"`, `paper_faithful_offline_allowed: false`, fourteen criteria
    rows, and nine blocking criteria ids.
- Full tests:
  `python -m pytest -q`
  - Result: `417 passed`.
- Docs validation:
  `python scripts/validate_docs.py`
  - Result: `docs validation passed`.
- Site-claim validation:
  `python scripts/validate_site_claims.py`
  - Result: `site claim validation passed`.
- Whitespace check:
  `git diff --check`
  - Result: passed with no output.

## Multi-Agent Review

- Implementation/test reviewer: no Critical, Important, or Minor findings. Confirmed the new
  top-level gate labels, `partial` status, false support/runtime trigger flags, fourteen ordered
  criteria rows, expected blocker list, allowed status/alignment labels, and absence of
  `paper_faithful_offline` in row status or alignment fields.
- Docs/claim reviewer: no Critical, Important, or Minor findings. Confirmed the docs and registry
  keep the lane partial, preserve `paper_faithful_offline_supported: false`, use
  `decision: remain_partial`, advance the next gate to `paper_fixture_breadth_expansion_plan`,
  and avoid full CPD, Newton runtime, real-USD, benchmark, collision-quality, deployment, or
  safety-certification claims.
- Reproducibility/schema reviewer: found one Important issue. The
  `report_schema_tests_and_records.current_evidence` row originally said the slice adds final
  verification while the record was still in progress. The row now says it adds RED/GREEN tests,
  registry metadata, and a dated record path. Re-review found no Critical, Important, or Minor
  findings.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `docs/index.md`
- `docs/deepdive/evidence-status.md`
- `docs/records/README.md`
- `docs/records/2026-05-16-cpd-paper-faithful-offline-scope-audit.md`
- `docs/reference/claim-boundaries.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/superpowers/specs/2026-05-16-cpd-paper-faithful-offline-scope-audit-design.md`
- `docs/superpowers/plans/2026-05-16-cpd-paper-faithful-offline-scope-audit.md`
- `experiments/registry.yaml`

## Claim Impact

- Supports only a partial, fixture-scoped, command-only offline scope audit that keeps the CPD
  paper lane partial.
- Does not support `paper_faithful_offline`, full CPD paper reproduction, package generation,
  Newton runtime support, real-USD evidence, benchmark evidence, collision-quality validation,
  deployment readiness, or safety certification.

## Next Action

- Proceed to `paper_fixture_breadth_expansion_plan`.
