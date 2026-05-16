# 2026-05-16 Cylinder Scoring Policy Package Probe

## Date

2026-05-16

## Status

Complete

## Changes

- Threaded explicit `primitive_score_multipliers` through CPD-like decomposition.
- Added `cpd_like_cylinder_scoring_policy_package_probe`, a synthetic offline package-path report
  over:
  - `cylinder_near_miss_cluster`;
  - `boxy_cuboid_guardrail`.
- Added CLI smoke:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cylinder-scoring-policy-package-probe`.

## Result

The focused tests show:

- default decomposition still selects `box` for the cylinder near-miss fixture;
- opt-in decomposition with `primitive_score_multipliers={"cylinder": 0.88}` selects `cylinder`;
- default and opt-in package generation both remain `box` for the clearly boxy cuboid guardrail;
- the changed synthetic package reports complete Newton shape-mapping coverage.

This is an explicitly opt-in synthetic package probe. It does not change default package
generation, real-USD package generation, or Newton task execution. It records a Newton
shape-mapping summary only; it does not run Newton contact canaries, drop/settle, or sphere-rain
task diagnostics.

## Verification

- RED:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_decompose.py::test_decompose_mesh_applies_opt_in_primitive_score_multipliers tests/test_cpd_like_decompose.py::test_decompose_mesh_rejects_bad_primitive_score_multipliers tests/test_cpd_like_synthetic.py::test_cylinder_scoring_policy_package_probe_outputs_mapped_opt_in_package tests/test_cpd_like_synthetic.py::test_cylinder_scoring_policy_package_probe_report_is_strict_json_serializable tests/test_cli.py::test_cli_run_cpd_like_cylinder_scoring_policy_package_probe_emits_json tests/test_cli.py::test_cli_run_cpd_like_cylinder_scoring_policy_package_probe_returns_nonzero_for_partial`
  failed because the new report builder and claim constant did not exist.
- GREEN:
  the same focused command passed after implementation with 6 tests.
- CLI smoke:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cylinder-scoring-policy-package-probe`
  returned `smoke_passed` and recorded one opt-in `cylinder` package for the near-miss fixture
  plus an unchanged `box` package for the guardrail.
- Focused integration verification:
  `python -m pytest -q tests/test_cpd_like_decompose.py tests/test_cpd_like_synthetic.py tests/test_cli.py`
  passed with 131 tests.
- Full verification:
  `python -m pytest -q` passed with 317 tests,
  `python scripts/validate_docs.py` passed,
  `python scripts/validate_site_claims.py` passed, and
  `git diff --check` passed.
- Multi-agent review:
  implementation review found no Critical or Important issues. Documentation review found two
  Important wording issues: standalone summaries did not always repeat the full package-probe
  boundary, and the design doc used over-strong "proves" wording. Both were fixed, and re-review
  found no Critical or Important issues.

## Claim Impact

This record supports only an explicitly opt-in synthetic package probe with Newton shape-mapping
summary. It does not support default scoring-policy change, scoring calibration, primitive-quality
improvement, real-USD package improvement, Newton contact/task evidence, benchmark evidence,
collision-quality validation, or CPD paper reproduction.

## Next Action

Finish docs/review/full verification. After that, the next legal slice is either an explicitly
opt-in Newton diagnostic over the synthetic changed package, or a separate controlled merge/search
behavior change. Capped bed/Franka reruns should wait until a default or explicitly experimental
real-USD package changes and still maps fully.
