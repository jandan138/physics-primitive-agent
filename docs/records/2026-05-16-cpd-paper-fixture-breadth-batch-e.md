# 2026-05-16 CPD Paper Fixture Breadth Batch E

## Status

Complete.

## Summary

- Added two Batch E postprocess breadth fixtures to the partial offline
  `cpd_paper_offline_report`.
- Added `paper_rotated_nested_primitive` and `paper_cross_type_enclosure_boundary`.
- Added a rotated nested OBB cull audit with non-identity shared axes.
- Added an explicit cross-type unsupported no-cull boundary for sphere-inside-OBB-style
  containment so unsupported cross-type containment cannot silently delete a primitive.
- Advanced `next_required_gate` to `paper_fixture_breadth_completion_review`.
- Kept `status: partial`, `paper_faithful_offline_supported: false`, and
  `failure_labels: ["paper_fixture_breadth_expansion_missing"]`.
- Kept package generation, Newton runtime, real USD, and benchmark triggers false.

## Verification

- RED focused tests failed before implementation because Batch E cases and the completion-review
  next gate were absent:
  `python -m pytest -q tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_batch_e tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_fixture_breadth_completion_review tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json`
  produced 4 expected failures.
- GREEN focused tests passed after implementation:
  `python -m pytest -q tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_batch_e tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_fixture_breadth_completion_review tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json`
  produced 4 passed.
- Focused CPD paper and CLI surface verification passed:
  `python -m pytest -q tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json`
  produced 13 passed.
- CLI smoke confirmed `next_required_gate: paper_fixture_breadth_completion_review`,
  `paper_rotated_nested_primitive` with rotated nested OBB cull from 2 input primitives to 1
  output primitive, `paper_cross_type_enclosure_boundary` with unsupported cross-type no-cull
  accounting from 2 input primitives to 2 output primitives, and false
  package/Newton/real-USD/benchmark triggers.
- A full verification run with the Batch E registry entry marked `in_progress` produced
  422 passed. This kept registry/record completion consistent until final record update.
- Final full verification after marking this record and the registry entry complete produced
  422 passed.
- Documentation and whitespace verification passed:
  `python scripts/validate_docs.py`, `python scripts/validate_site_claims.py`, and
  `git diff --check`.

## Review Notes

- Plan-level subagent review dispatch was attempted for implementation/schema,
  documentation/claim-boundary, and reproducibility/registry perspectives, but review agents were
  interrupted or shut down by the platform usage limit before returning findings.
- Implementation-stage subagent review dispatch was attempted again for implementation/schema,
  documentation/claim-boundary, and reproducibility/registry perspectives after final local
  verification, but all three review agents were interrupted by the platform usage limit before
  returning findings.
- Local implementation/schema review kept the rotated OBB fixture as explicit audit primitives
  rather than generated-search output, preserving the existing postprocess boundary.
- Local claim-boundary review kept cross-type containment as an unsupported no-cull boundary rather
  than claiming a general containment library.
- Reproducibility review kept the registry entry `in_progress` until final verification updated
  this record and the registry entry to complete together.

## Claim Boundary

Supports only partial, fixture-scoped, command-only Batch E postprocess breadth accounting.
Does not support `paper_faithful_offline`, full CPD reproduction, package generation, Newton
runtime support, real-USD evidence, benchmark evidence, collision-quality validation, general
containment-library behavior, deployment readiness, or safety certification.

## Next

- Proceed to `paper_fixture_breadth_completion_review`.
