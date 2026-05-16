# 2026-05-16 CPD Paper Flat Capped-Cylinder Audit

## Date

2026-05-16

## Status

Complete

## Changes

- Replaced the paper-lane `capped_cylinder` row with an offline-only flat capped-cylinder audit
  row.
- Added three flat-cylinder axis candidates, selected-axis metadata, `cap_model: flat_caps`, radius,
  height, formula, paper weight, containment, and `newton_runtime_kind: offline_only_unmapped`.
- Kept the older CPD-like hemisphere-cap `capped_cylinder` package proxy separate from this
  paper-lane audit row.
- Kept the report payload status `partial` with `paper_faithful_offline_supported: false`.

## Review

- Multi-agent geometry/schema review found no issues after verifying that `capped_cylinder` is kept
  out of the current CPD-like primitive subset and reintroduced only as an offline flat-cap audit
  row with `pi*r^2*h` volume, three axis candidates, containment, and strict JSON coverage.
- Multi-agent docs/claim review found no forbidden runtime, real-USD, benchmark, collision-quality,
  deployment, safety, or full-reproduction claims. It identified one important remaining-gap issue:
  the report needed to keep `paper_capsule_axis_policy_missing` in `failure_labels`. The report and
  tests now cover that boundary.
- Post-fix multi-agent review found no remaining Critical or Important issues and reconfirmed the
  report stays `partial`, `paper_faithful_offline_supported: false`, and
  `next_required_gate: paper_capsule_axis_policy_audit`.

## Verification

- Passed:
  `python -m pytest tests/test_cpd_paper_offline.py tests/test_newton_shapes.py::test_map_package_shapes_keeps_capped_cylinder_as_mapping_gap tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cli.py::test_cli_run_cpd_paper_offline_report_rejects_nonfinite_json -q`
  (`7 passed in 0.68s`).
- Passed:
  `python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report >/tmp/cpd_paper_offline_report.json`
  (exit `0`; report payload had `status: partial`, `report_generation_status: smoke_passed`,
  `next_required_gate: paper_capsule_axis_policy_audit`, and the capped-cylinder row had
  `fit_model: paper_flat_capped_cylinder_min_volume_over_axes`,
  `newton_runtime_kind: offline_only_unmapped`, `cap_model: flat_caps`).
- Passed: `python scripts/validate_docs.py` (`docs validation passed`).
- Passed: `python scripts/validate_site_claims.py` (`site claim validation passed`).
- Passed: `git diff --check` (no output).
- Passed: `python -m pytest -q` (`406 passed in 43.94s`).

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_newton_shapes.py`
- `tests/test_cli.py`
- `docs/reference/claim-boundaries.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `experiments/registry.yaml`

## Claim Impact

- Supports only a partial, fixture-scoped, command-only offline fit-audit row for paper flat capped
  cylinders.
- Does not support `paper_faithful_offline`, full CPD paper reproduction, Newton runtime support,
  package generation, real-USD results, benchmark evidence, collision-quality validation,
  deployment readiness, or safety certification.

## Next Action

- Add paper capsule axis-policy audit and then the full paper priority-queue trace before any Newton
  or real-USD work.
