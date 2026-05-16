# 2026-05-16 CPD Paper Fixture Breadth Batch C

## Status

Complete.

## Summary

- Added three Batch C cost/search/stop breadth fixtures to the partial offline
  `cpd_paper_offline_report`.
- Added `paper_branching_cost_order`, `paper_equal_cost_queue_tie`, and
  `paper_nonzero_threshold_block`.
- Advanced `next_required_gate` to `paper_fixture_breadth_batch_d`.
- Kept `status: partial`, `paper_faithful_offline_supported: false`, and
  `failure_labels: ["paper_fixture_breadth_expansion_missing"]`.
- Kept package generation, Newton runtime, real USD, and benchmark triggers false.

## Verification

- RED focused tests failed before implementation because Batch C cases and the Batch D next gate
  were absent:
  `python -m pytest -q tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_batch_c tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_fixture_breadth_batch_d tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json`
  produced 4 expected failures.
- GREEN focused tests passed after implementation:
  `python -m pytest -q tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_batch_c tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_fixture_breadth_batch_d tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json`
  produced 4 passed.
- Focused CPD paper and CLI surface verification passed:
  `python -m pytest -q tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json`
  produced 11 passed.
- CLI smoke:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report`
  emitted strict JSON with `next_required_gate: paper_fixture_breadth_batch_d`, the Batch C
  implemented fixture-scope marker, all three Batch C case ids, a positive finite threshold
  `1e-06`, and false package/Newton/real-USD/benchmark triggers. The branching fixture showed
  different base-cost and weighted-priority winners, and the accepted event used the
  weighted-priority winner.
- Full verification passed:
  `python -m pytest -q` produced 420 passed.
- Documentation and whitespace verification passed:
  `python scripts/validate_docs.py`, `python scripts/validate_site_claims.py`, and
  `git diff --check`.

## Review Notes

- Initial implementation review found that the branching fixture did not isolate weighted-priority
  ordering from base-cost ordering and that the docs could overstate stale-pop coverage. The
  branching fixture was replaced with a deterministic mesh where base-cost and weighted-priority
  winners differ, tests now assert that distinction, and wording was narrowed to
  eager-stale-prune behavior.
- Docs/claim review found stale current-gate wording and a mismatch between implemented-facing docs
  and the pending record. The claim-boundary, index, evidence, story, gap-matrix, and this record
  were updated.
- Reproducibility/registry review found the same weighted-priority wording risk and confirmed the
  registry/record should be marked complete together only after verification. The registry is now
  complete and points to this complete record.

## Claim Boundary

Supports only partial, fixture-scoped, command-only Batch C cost/search/stop breadth accounting.
Does not support `paper_faithful_offline`, full CPD reproduction, package generation, Newton
runtime support, real-USD evidence, benchmark evidence, collision-quality validation, deployment
readiness, or safety certification.

## Next

- Proceed to `paper_fixture_breadth_batch_d`.
