# 2026-05-16 CPD Paper Frustum Trapezoid Audit

## Date

2026-05-16

## Status

Complete

## Changes

- Extended the command-only partial `cpd_paper_offline_report` with two additional deterministic
  synthetic fixtures: `paper_frustum_like` and `paper_trapezoid_prism_like`.
- Added offline-only `frustum` and `trapezoidal_prism` candidate audit rows with paper weights,
  formula strings, finite dimensions, selected axis or axis-order metadata, containment checks, and
  `newton_runtime_kind: offline_only_unmapped`.
- Kept `frustum` and `trapezoidal_prism` out of CPD-like runtime primitive support and Newton shape
  mapping; both remain paper-lane audit rows only.
- Kept the report payload status `partial` with `paper_faithful_offline_supported: false`.

## Review

- Multi-agent paper/schema review recommended local offline-only fit rows, flat-cylinder axis
  candidates for frustum, six axis-order attempts for trapezoidal prism, and no leak into runtime
  primitive support.
- Multi-agent docs/claim review confirmed no forbidden `paper_faithful_offline`, Newton runtime,
  package-generation, real-USD, benchmark, collision-quality, deployment, or safety-certification
  claims after docs synchronization.
- Multi-agent geometry review found two important implementation issues: frustum containment failed
  on degenerate planar groups, and trapezoidal-prism selection could consider non-containing axis
  attempts. Regression tests now cover both cases, and the fit helpers now adjust extents to
  preserve containment before selection.

## Verification

- Passed:
  `python -m pytest tests/test_cpd_paper_offline.py tests/test_newton_shapes.py::test_map_package_shapes_keeps_paper_only_primitives_as_mapping_gaps tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cli.py::test_cli_run_cpd_paper_offline_report_rejects_nonfinite_json -q`
  (`7 passed in 0.32s`).
- Passed:
  `python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report >/tmp/cpd_paper_offline_report.json`
  (exit `0`; report payload had `status: partial`, `report_generation_status: smoke_passed`, and
  cases `paper_single_box`, `paper_two_face_merge`, `paper_frustum_like`,
  `paper_trapezoid_prism_like`).
- Passed: `python scripts/validate_docs.py` (`docs validation passed`).
- Passed: `python scripts/validate_site_claims.py` (`site claim validation passed`).
- Passed: `git diff --check` (no output).
- Passed: `python -m pytest -q` (`396 passed in 43.55s`).

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

- Supports only partial, fixture-scoped, command-only offline fit-audit rows for `frustum` and
  `trapezoidal_prism`.
- Does not support `paper_faithful_offline`, full CPD paper reproduction, Newton runtime support,
  package generation, real-USD results, benchmark evidence, collision-quality validation,
  deployment readiness, or safety certification.

## Next Action

- Add paper-flat capped-cylinder fitting and then the full paper priority-queue trace before any
  Newton or real-USD work.
