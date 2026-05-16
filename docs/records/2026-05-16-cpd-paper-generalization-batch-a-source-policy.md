# 2026-05-16 CPD Paper Generalization Batch A Source Policy

## Date

2026-05-16

## Status

Complete

## Changes

- Added `paper_generalization_batch_a_source_policy` to the command-only
  `cpd_paper_offline_report`.
- Closed only the source-policy generalization gate and advanced the current next gate to
  `paper_generalization_batch_b_primitive_fit_engine`.
- Kept the report `status: partial` with `paper_faithful_offline_supported: false`.
- Added an offline source-policy matrix for deterministic synthetic meshes. It records
  exact-coordinate dedup policy, source-face intake/remap policy, concave-polygon rejection, and
  source-face `Q` aggregation accounting.
- Kept package generation, Newton runtime execution, real-USD evidence, and benchmark work out of
  scope.

## Verification

- RED:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_source_policy_generalization_gate -q`
  failed because `paper_generalization_batch_a_source_policy_missing` was still present.
- RED:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_source_policy_generalization_rows_match_case_payloads -q`
  failed because `paper_generalization_batch_a_source_policy` did not exist.
- RED:
  `python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  failed because the CLI JSON still reported Batch A as missing.
- GREEN:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_source_policy_generalization_gate -q`
  passed.
- GREEN:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_source_policy_generalization_rows_match_case_payloads -q`
  passed.
- GREEN:
  `python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  passed.
- `python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q`: 127 passed.
- `python scripts/validate_site_claims.py`: passed.
- `git diff --check`: no whitespace errors.
- `python -m pytest -q`: 426 passed.
- `python scripts/validate_docs.py`: passed after registry/record status was synchronized.
- `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report`
  plus JSON assertions passed and printed `source policy generalization CLI smoke passed`.
- Post-review final verification:
  `python scripts/validate_docs.py` passed.
- Post-review final verification:
  `python scripts/validate_site_claims.py` passed.
- Post-review final verification:
  `git diff --check` passed.
- Post-review final verification:
  `python -m pytest -q` passed with 426 tests.

## Review Notes

- Initial implementation-design, claim-boundary, and docs/process agents agreed this gate should
  be an offline source-policy matrix derived from existing source/preprocess/intake/operator
  fixture cases, not a new USD, package, Newton, or benchmark path.
- A later review noted that the tests needed to pin policy-section payloads, coverage summary,
  stale next-action wording, and source-face `Q` aggregation. The tests and payload were tightened
  before the focused GREEN run.
- Two early plan-review agents looked at the main worktree rather than this feature worktree and
  reported the new spec/plan as missing. That finding was not applicable to this branch, but their
  broader stale-gate and claim-boundary concerns were covered by this record and the docs update.
- One CLI smoke attempt without `PYTHONPATH=src` read outside the feature worktree and failed its
  JSON assertion. The smoke was rerun with `PYTHONPATH=src`, matching the registry command pattern.
- Final implementation/schema review found no source or schema blockers after the earlier test
  tightening. It reported one stale current-doc wording issue, which was fixed in
  `docs/deepdive/evidence-status.md` and `docs/reference/claim-boundaries.md`.
- Final claim-boundary review found no overclaim issues.
- Final docs/process review found one low-severity stale future-tense sentence in
  `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`; it was rewritten to state that the
  first implementation gate is now implemented.
- A final pre-commit docs review found stale current-status wording that could still read as
  Batch A being the active next gate, plus two conservative-wording issues. `docs/index.md` and
  `docs/reference/cpd-paper-story-status.md` now describe Batch A as the planning-stage follow-up
  that has since closed. `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`,
  `docs/reference/cpd-paper-reproduction-gap-matrix.md`, and this record now use weaker
  audit/document wording.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `docs/superpowers/specs/2026-05-16-cpd-paper-source-policy-generalization-design.md`
- `docs/superpowers/plans/2026-05-16-cpd-paper-source-policy-generalization.md`
- `experiments/registry.yaml`

## Claim Impact

Supported:

- The command-only `cpd_paper_offline_report` includes a partial offline source-policy
  generalization matrix for deterministic synthetic meshes.
- `paper_generalization_batch_a_source_policy` is closed as an offline report-only gate.
- The next required gate is `paper_generalization_batch_b_primitive_fit_engine`.

Not supported:

- robust mesh cleanup;
- general polygon intake;
- `paper_faithful_offline`;
- full CPD paper reproduction;
- package generation;
- Newton runtime execution;
- real-USD evidence;
- benchmark or collision-quality evidence;
- deployment readiness or safety certification.

## Next Action

Proceed to `paper_generalization_batch_b_primitive_fit_engine` as the next offline
generalization slice. Keep the lane partial and offline-only until a later dated record documents
a stronger boundary.
