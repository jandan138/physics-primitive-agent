# 2026-05-16 CPD Paper Fixture Breadth Batch D

## Status

Complete.

## Summary

- Added two Batch D component-pair breadth fixtures to the partial offline
  `cpd_paper_offline_report`.
- Added `paper_component_pair_multi_candidate_order` and
  `paper_component_pair_cap_skipped`.
- Added component-pair candidate tables, available-pair counts, cap values, skipped-pair keys,
  and deterministic skipped-pair counts.
- Advanced `next_required_gate` to `paper_fixture_breadth_batch_e`.
- Kept `status: partial`, `paper_faithful_offline_supported: false`, and
  `failure_labels: ["paper_fixture_breadth_expansion_missing"]`.
- Kept package generation, Newton runtime, real USD, and benchmark triggers false.

## Verification

- RED focused tests failed before implementation because Batch D cases and the Batch E next gate
  were absent:
  `python -m pytest -q tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_batch_d tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_fixture_breadth_batch_e tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json`
  produced 4 expected failures.
- GREEN focused tests passed after implementation:
  `python -m pytest -q tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_batch_d tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_fixture_breadth_batch_e tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json`
  produced 4 passed.
- Focused CPD paper and CLI surface verification passed:
  `python -m pytest -q tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json`
  produced 12 passed.
- CLI smoke confirmed `next_required_gate: paper_fixture_breadth_batch_e`,
  `paper_component_pair_multi_candidate_order` with 3 available and 3 admitted component-pair
  candidates, `paper_component_pair_cap_skipped` with 6 available pairs, cap `2`, and 4 skipped
  pairs, one accepted merge per Batch D case, target-count stop reasons, and false
  package/Newton/real-USD/benchmark triggers.
- A full verification run with the Batch D registry entry temporarily marked `in_progress`
  produced 421 passed. This isolated the previous documentation-consistency issue before the
  record and registry were marked complete together.
- Final full verification after marking this record and the registry entry complete produced
  421 passed.
- Documentation and whitespace verification passed:
  `python scripts/validate_docs.py`, `python scripts/validate_site_claims.py`, and
  `git diff --check`.

## Review Notes

- Plan-level subagent review dispatch was attempted for implementation/schema,
  documentation/claim-boundary, and reproducibility/registry perspectives, but all three review
  agents were interrupted by the platform usage limit before returning findings.
- Implementation-stage subagent review dispatch was attempted again for the same three
  perspectives after final local verification, but those review agents were also interrupted by
  the platform usage limit before returning findings.
- Local implementation/schema review checked that the three-component fixture creates three
  component-pair candidates, the four-component cap fixture creates six available pairs with two
  admitted and four skipped, and both fixtures stop after one accepted merge at target count.
- Local claim-boundary review kept the slice offline-only and did not add Newton, package, real
  USD, benchmark, collision-quality, deployment, or safety claims.
- Reproducibility review found that a complete registry entry must point to a complete record. The
  registry was temporarily marked `in_progress` during verification, then this complete record and
  the complete registry entry were updated together.

## Claim Boundary

Supports only partial, fixture-scoped, command-only Batch D component-pair breadth accounting.
Does not support `paper_faithful_offline`, full CPD reproduction, package generation, Newton
runtime support, real-USD evidence, benchmark evidence, collision-quality validation, deployment
readiness, or safety certification.

## Next

- Proceed to `paper_fixture_breadth_batch_e`.
