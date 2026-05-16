# 2026-05-16 CPD Paper Fixture Breadth Completion Review

## Date

2026-05-16

## Status

Complete

## Changes

- Added a command-only synthetic fixture-breadth completion review to
  `cpd_paper_offline_report`.
- Closed only the planned `paper_fixture_breadth_expansion` gate after Batch A-E fixture breadth.
- Advanced the next required gate to the planning-only
  `paper_faithful_offline_generalization_plan`.
- Kept `status: partial`, `paper_faithful_offline_supported: false`, and all package-generation,
  Newton runtime, real-USD, and benchmark triggers false.
- Updated the scope-audit `next_action` rows so the live report no longer points to the completed
  fixture-breadth review.
- Updated docs, registry metadata, and tests to keep the claim boundary explicit.

## Verification

- RED focused tests:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_completion_review tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  failed as expected before implementation because the report still emitted
  `paper_fixture_breadth_expansion_missing`.
- RED scope-audit next-action check:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice -q`
  failed as expected after updating the expected scope-audit rows, before updating the source.
- GREEN focused tests:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_completion_review tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  passed: 3 passed.
- GREEN top-level gate tests:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_failure_labels_point_to_generalization_gap tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_generalization_plan -q`
  passed: 2 passed.
- GREEN scope-audit next-action check:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice -q`
  passed: 1 passed.
- Final CLI smoke:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report`
  emitted `failure_labels: ["paper_faithful_offline_generalization_missing"]`,
  `next_required_gate: paper_faithful_offline_generalization_plan`,
  `closed_gate: paper_fixture_breadth_expansion`, Batch A-E completion rows, and false
  package-generation/Newton/real-USD/benchmark triggers.
- Full test suite:
  `python -m pytest -q` passed: 423 passed.
- Focused CPD paper and CLI tests:
  `python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q` passed: 124 passed.
- Documentation validators:
  `python scripts/validate_docs.py` passed and `python scripts/validate_site_claims.py` passed.
- Whitespace check:
  `git diff --check` passed with no output.

## Review

- Documentation consistency review found that the planned CLI smoke bypassed the CLI by importing
  `build_cpd_paper_offline_report()` directly. The plan was fixed to run
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report`.
- Documentation consistency review found stale next-gate surfaces. The plan and docs were expanded
  to update the known stale `README.md`, `docs/index.md`, `docs/deepdive/evidence-status.md`,
  `docs/reference/claim-boundaries.md`, `docs/reference/cpd-paper-reproduction-gap-matrix.md`,
  `docs/reference/cpd-paper-faithful-offline-lane-spec.md`,
  `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`, and
  `docs/reference/cpd-paper-story-status.md` surfaces.
- Claim-boundary review found that the planned canonical-doc wording was too broad. The plan and
  docs now explicitly say the review is command-only, synthetic, fixture-scoped, partial, and not
  `paper_faithful_offline` support.
- Implementation/TDD review found stale focused tests and insufficient exactness in batch metadata
  assertions. The plan and tests were updated to rename the old top-level gate tests, assert exact
  Batch A-E case ids, and assert exact primary criteria mappings.
- Final implementation/TDD review found no issues after the updates.
- Final claim-boundary review found no issues and confirmed the wording stays command-only,
  synthetic, fixture-scoped, partial, and explicitly below `paper_faithful_offline`.
- Final documentation/records consistency review found the record and registry still marked
  in-progress after verification. This record and `experiments/registry.yaml` were updated to
  `Complete` / `complete`.

## Artifacts

- Plan:
  `docs/superpowers/plans/2026-05-16-cpd-paper-fixture-breadth-completion-review.md`
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
The command-only synthetic CPD paper offline lane includes a fixture-breadth completion review for
planned Batches A-E, and the report remains partial.
```

Does not support `paper_faithful_offline`, full CPD reproduction, package generation, Newton
runtime execution, real-USD evidence, collision-quality evidence, benchmark evidence, deployment
readiness, or safety certification.

## Next Action

Proceed to the planning-only `paper_faithful_offline_generalization_plan` gate.
