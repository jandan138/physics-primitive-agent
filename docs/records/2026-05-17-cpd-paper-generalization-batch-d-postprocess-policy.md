# 2026-05-17 CPD Paper Generalization Batch D Postprocess Policy

## Date

2026-05-17

## Status

Complete

## Changes

- Added `paper_generalization_batch_d_postprocess_policy` to the command-only
  `cpd_paper_offline_report`.
- Closed only the postprocess-policy generalization gate and advanced the current next gate to
  `paper_generalization_batch_e_package_boundary_readiness`.
- Kept the report `status: partial` with `paper_faithful_offline_supported: false`.
- Added an offline postprocess-policy matrix that summarizes existing deterministic
  `postprocess_audit` evidence for identity-axis OBB culling, rotated OBB culling, and conservative
  unsupported cross-type no-silent-cull accounting.
- Recorded the postprocess contract: explicit audit primitive rows only, OBB-corner containment as
  the supported same-family test, unsupported cross-type boundary accounting, before/after counts,
  kept and culled ids, cull or unsupported records, and no package generation or Newton runtime.
- Kept package generation, Newton runtime execution, real-USD evidence, and benchmark work out of
  scope.

## Verification

- RED:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_postprocess_policy_generalization_gate tests/test_cpd_paper_offline.py::test_cpd_paper_postprocess_policy_generalization_rows_match_case_payloads tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  failed because Batch D was still reported missing and
  `paper_generalization_batch_d_postprocess_policy` did not exist.
- GREEN:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_postprocess_policy_generalization_gate tests/test_cpd_paper_offline.py::test_cpd_paper_postprocess_policy_generalization_rows_match_case_payloads tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  passed.
- Focused suite:
  `python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q` passed with 132 tests.
- First full-suite attempt:
  `python -m pytest -q` passed all behavior tests but failed docs validation because this dated
  record did not yet exist.
- Docs validation after adding the dated record:
  `python scripts/validate_docs.py` passed.
- Site claim validation:
  `python scripts/validate_site_claims.py` passed.
- Whitespace validation:
  `git diff --check` passed.
- Final full suite:
  `python -m pytest -q` passed with 431 tests.

## Review Notes

- Planning reviewers recommended closing Batch D with a top-level offline report payload that
  summarizes existing `postprocess_audit` outputs rather than adding a new containment library.
- Planning reviewers recommended explicitly distinguishing this generalization Batch D
  postprocess-policy gate from the older fixture-breadth Batch D component-pair slice.
- Planning reviewers recommended keeping historical Batch C payload next-gate wording intact while
  advancing only the current top-level gate to Batch E.
- Final implementation and docs review agents were dispatched after implementation, but both were
  unavailable because the agent usage limit was reached. Their review was not counted as approval.
- Local follow-up review searched for stale current-gate wording, found one remaining
  `claim-boundaries.md` sentence that still named Batch D as the current unresolved gate, and
  corrected it to Batch E.
- Post-fix validation reran `python scripts/validate_docs.py`, `python scripts/validate_site_claims.py`,
  `git diff --check`, the focused CPD paper/CLI test suite, the full test suite, a source-local
  JSON smoke, and a stale-current-gate text search.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `docs/superpowers/specs/2026-05-17-cpd-paper-postprocess-policy-generalization-design.md`
- `docs/superpowers/plans/2026-05-17-cpd-paper-postprocess-policy-generalization.md`
- `experiments/registry.yaml`

## Claim Impact

Supported:

- The command-only `cpd_paper_offline_report` includes a partial offline postprocess-policy
  generalization matrix for deterministic synthetic fixtures.
- `paper_generalization_batch_d_postprocess_policy` is closed as an offline report-only gate.
- The next required gate is `paper_generalization_batch_e_package_boundary_readiness`.

Not supported:

- a general primitive containment library;
- `paper_faithful_offline`;
- full CPD paper reproduction;
- package generation;
- Newton runtime execution;
- real-USD evidence;
- benchmark or collision-quality evidence;
- deployment readiness or safety certification.
