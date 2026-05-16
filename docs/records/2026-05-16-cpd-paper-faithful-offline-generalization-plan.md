# 2026-05-16 CPD Paper Faithful Offline Generalization Plan

## Date

2026-05-16

## Status

Complete

## Changes

- Added a command-only offline generalization planning table to `cpd_paper_offline_report`.
- Closed only the planning gate `paper_faithful_offline_generalization_plan`.
- Advanced the top-level next required gate to `paper_generalization_batch_a_source_policy`.
- Split the remaining offline paper-lane generalization work into five explicit batches:
  source policy, primitive-fit engine, search engine, postprocess policy, and package-boundary
  readiness.
- Kept `status: partial`, `paper_faithful_offline_supported: false`, and all package-generation,
  Newton runtime, real-USD, and benchmark triggers false.
- Kept `paper_faithful_offline_generalization_plan` in `implemented_planning_scope`, not in
  `implemented_fixture_scope`.

## Verification

- Baseline full test suite after syncing ignored local paper source intake into the isolated
  worktree:
  `python -m pytest -q` passed: 423 passed.
- RED focused tests:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_generalization_plan_gate tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  failed as expected before implementation because the report still emitted
  `paper_faithful_offline_generalization_missing` and lacked the planning payload.
- RED top-level gate tests:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_failure_labels_point_to_source_policy_gap tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_source_policy_generalization tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_completion_review -q`
  failed as expected before implementation because the report still pointed to
  `paper_faithful_offline_generalization_plan`.
- GREEN focused tests:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_generalization_plan_gate tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  passed: 3 passed.
- GREEN top-level gate tests:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_failure_labels_point_to_source_policy_gap tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_source_policy_generalization tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_completion_review -q`
  passed: 3 passed.
- Final CLI smoke:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report`
  plus JSON assertions passed and printed `generalization plan CLI smoke passed`.
- Pre-finalization full test suite:
  `python -m pytest -q` passed: 424 passed.
- Pre-finalization documentation validators:
  `python scripts/validate_docs.py` passed and `python scripts/validate_site_claims.py` passed.
- Pre-finalization whitespace check:
  `git diff --check` passed with no output.
- Post-review full test suite:
  `python -m pytest -q` passed: 424 passed.
- Post-review documentation validators:
  `python scripts/validate_docs.py` passed and `python scripts/validate_site_claims.py` passed.
- Post-review whitespace check:
  `git diff --check` passed with no output.
- Post-finalization full test suite after marking the record and registry complete:
  `python -m pytest -q` passed: 424 passed.
- Post-finalization documentation validators after marking the record and registry complete:
  `python scripts/validate_docs.py` passed and `python scripts/validate_site_claims.py` passed.
- Post-finalization whitespace check after marking the record and registry complete:
  `git diff --check` passed with no output.

## Review

- RED test compliance review found no issues: the tests match the plan's Task 1 assertions.
- RED claim-boundary review found no issues: the tests keep the report partial, keep
  `paper_faithful_offline_supported` / `paper_faithful_offline_allowed` false, and keep
  package-generation/Newton/real-USD/benchmark triggers false.
- Final implementation/TDD review found no issues. It independently checked the five failure
  labels, `paper_generalization_batch_a_source_policy` as the next gate, exact planned-batch
  payload, planning scope separated from fixture scope, blocking scope-audit actions pointing to
  source policy, partial report status, and false runtime triggers. It also ran focused tests,
  CLI assertions, the full suite, docs validators, site claim validation, and `git diff --check`.
- Final claim-boundary review found stale next-gate wording in current-status docs. The docs were
  corrected so `paper_faithful_offline_generalization_plan` is only historical, nested follow-up,
  or closed-gate wording, while the current next gate is `paper_generalization_batch_a_source_policy`.
- Final documentation/records/process review found the same stale next-gate wording. The docs were
  corrected and revalidated.
- Targeted stale-next-gate re-review found no issues after the corrections. It confirmed the
  current next gate is unambiguously `paper_generalization_batch_a_source_policy` in `README.md`,
  `docs/index.md`, `docs/deepdive/evidence-status.md`, `docs/reference/claim-boundaries.md`,
  `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`, and
  `docs/reference/cpd-paper-story-status.md`.

## Artifacts

- Plan:
  `docs/superpowers/plans/2026-05-16-cpd-paper-faithful-offline-generalization-plan.md`
- Source:
  `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- Tests:
  `tests/test_cpd_paper_offline.py`
  `tests/test_cli.py`
- Registry:
  `experiments/registry.yaml`

## Claim Impact

Supports only this bounded statement:

```text
The command-only synthetic CPD paper offline lane has a planning table for offline generalization
beyond named toy fixtures, and the report remains partial.
```

Does not support `paper_faithful_offline`, full CPD reproduction, package generation, Newton
runtime execution, real-USD evidence, collision-quality evidence, benchmark evidence, deployment
readiness, or safety certification.

## Next Action

Proceed to `paper_generalization_batch_a_source_policy` as the first offline implementation slice
after the planning table.
