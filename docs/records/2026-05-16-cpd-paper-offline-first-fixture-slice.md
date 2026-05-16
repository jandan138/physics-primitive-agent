# 2026-05-16 CPD Paper Offline First Fixture Slice

## Date

2026-05-16

## Status

Complete

## Changes

- Added a new command-only `cpd_paper_offline_report` lane for two synthetic toy fixtures:
  `paper_single_box` and `paper_two_face_merge`.
- Added fixture-scoped paper-side audit fields for triangle-only mesh intake, per-face and
  merged-group `Q` operators, a four-primitive fit-audit subset, and separate
  `paper_base_cost` versus `weighted_priority_cost` fields.
- Added `npc-compile --run-cpd-paper-offline-report` as a command-only CLI entry point.
- Kept the report payload status `partial`, while the CLI exits successfully when strict JSON report
  generation succeeds.
- Expanded the merge-cost audit to expose left, right, and merged fit-audit payloads, so the
  cost inputs are reviewable from the report.
- Marked audited primitive rows as current surrogate/proxy fit rows, recorded the current parameter
  clamp and axis-selection policy, and explicitly disabled Newton runtime, real-USD, package,
  benchmark, and collision-quality claims.

## Review

- Multi-agent CLI/registry review identified that successful JSON generation should not return a
  process failure just because the paper-lane payload status is `partial`; the CLI now exits `0`
  when `report_generation_status` is `smoke_passed`.
- Multi-agent algorithm review identified that collapse-cost inputs needed to be reviewable and
  that current primitive rows needed stronger surrogate/proxy labeling; the report and tests now
  cover both.
- Multi-agent docs/claim review identified stale planned-artifact wording and the record/registry
  mismatch; the offline-lane spec and this dated record now reflect the implemented partial slice.

## Verification

- Passed:
  `python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cli.py::test_cli_run_cpd_paper_offline_report_rejects_nonfinite_json -q`
  (`4 passed in 0.33s`).
- Passed:
  `python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report >/tmp/cpd_paper_offline_report.json`
  (exit `0`; report payload had `status: partial`, `report_generation_status: smoke_passed`, and
  cases `paper_single_box`, `paper_two_face_merge`).
- Passed: `python scripts/validate_docs.py` (`docs validation passed`).
- Passed: `python scripts/validate_site_claims.py` (`site claim validation passed`).
- Passed: `git diff --check` (no output).
- Passed: `python -m pytest -q` (`393 passed in 42.91s`).

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `src/primitive_collision_compiler/baselines/cpd_paper/__init__.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/claim-boundaries.md`
- `experiments/registry.yaml`

## Claim Impact

- Supports only a partial, fixture-scoped, command-only offline paper-lane audit over
  `paper_single_box` and `paper_two_face_merge`.
- Does not support `paper_faithful_offline`, full CPD paper reproduction, Newton runtime support,
  real-USD results, package generation, benchmark evidence, collision-quality validation,
  deployment readiness, or safety certification.

## Next Action

- Add the next offline paper-lane gate: frustum and trapezoidal-prism fit audit on synthetic toy
  fixtures before any Newton or real-USD work.
