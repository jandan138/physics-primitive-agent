# 2026-05-17 CPD Paper Generalization Batch E Package Boundary Readiness

## Date

2026-05-17

## Status

Complete

## Changes

- Added `paper_generalization_batch_e_package_boundary_readiness` to the command-only
  `cpd_paper_offline_report`.
- Closed only the package-boundary readiness gate with an offline package-boundary readiness
  matrix before package conversion.
- Advanced the current next gate to `paper_offline_changed_decomposition_output_contract`.
- Replaced the top-level Batch E missing label with
  `paper_offline_changed_decomposition_output_contract_missing` and
  `paper_package_generation_contract_missing`.
- Kept the report `status: partial` with `paper_faithful_offline_supported: false`.
- Kept package generation, Newton runtime execution, real-USD evidence, benchmark work, and
  collision-quality claims out of scope.
- Corrected README wording so the capped Franka support-aware native lane is described as selecting
  boxes while reporting three cheaper raw-cost cylinder candidates as support-blocked.

## Verification

- RED:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_package_boundary_readiness_gate -q`
  failed because the report still emitted
  `paper_generalization_batch_e_package_boundary_readiness_missing`.
- RED:
  `python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  failed because the CLI JSON still emitted
  `paper_generalization_batch_e_package_boundary_readiness_missing`.
- GREEN:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_package_boundary_readiness_gate -q`
  passed.
- GREEN:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_package_boundary_readiness_keeps_runtime_work_blocked -q`
  passed.
- GREEN:
  `python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  passed.
- Focused suite:
  `python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q` passed with 134 tests.
- Full suite:
  `python -m pytest -q` passed with 433 tests.
- Docs validation:
  `python scripts/validate_docs.py` passed.
- Site claim validation:
  `python scripts/validate_site_claims.py` passed.
- Whitespace validation:
  `git diff --check` passed.
- Source-local smoke:
  a direct `build_cpd_paper_offline_report()` check confirmed
  `next_required_gate: paper_offline_changed_decomposition_output_contract`, failure labels
  `paper_offline_changed_decomposition_output_contract_missing` and
  `paper_package_generation_contract_missing`, five boundary-review rows, and
  `paper_faithful_offline_supported: false`.

## Review Notes

- Planning reviewers recommended treating Batch E as a readiness checklist before package
  conversion, not as package generation or Newton runtime execution.
- Planning reviewers recommended keeping the next blocker explicit as a changed-decomposition
  output contract before any package adapter work.
- Documentation review identified stale current-gate wording and a README Franka native-lane
  wording mismatch; both were included in this slice.
- Final implementation/schema review found no blocking issues and confirmed the Batch E schema,
  top-level gate/failure labels, A-D historical payload boundaries, and trigger-false tests.
- Final documentation/claim-boundary review found no blocking issues and confirmed current docs
  treat Batch E as implemented/closed, point next to
  `paper_offline_changed_decomposition_output_contract`, and do not claim package readiness,
  Newton readiness, package generation, real-USD evidence, benchmark evidence, collision quality,
  or `paper_faithful_offline`.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `docs/superpowers/specs/2026-05-17-cpd-paper-package-boundary-readiness-design.md`
- `docs/superpowers/plans/2026-05-17-cpd-paper-package-boundary-readiness.md`
- `experiments/registry.yaml`

## Claim Impact

Supported:

- The command-only `cpd_paper_offline_report` includes an offline package-boundary readiness
  matrix before package conversion.
- `paper_generalization_batch_e_package_boundary_readiness` is closed as a planning/report-only
  gate.
- The next required gate is `paper_offline_changed_decomposition_output_contract`.

Not supported:

- package readiness;
- Newton readiness;
- `paper_faithful_offline`;
- full CPD paper reproduction;
- package generation;
- Newton runtime execution;
- real-USD evidence;
- benchmark or collision-quality evidence;
- deployment readiness or safety certification.
