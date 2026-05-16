# 2026-05-16 Cylinder Scoring Policy Newton Probe

## Date

2026-05-16

## Status

Complete

## Changes

- Added `cpd_like_cylinder_scoring_policy_newton_probe`, an explicitly opt-in synthetic Newton
  diagnostic over the changed `cylinder_near_miss_cluster` package pair.
- Added contact-gated task execution:
  - run `newton_contact_smoke`;
  - run `newton_drop_settle` and `newton_sphere_rain` only if contact passes;
  - record `blocked_by_contact_canary` task payloads otherwise.
- Added CLI:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --config configs/experiments/cylinder_scoring_policy_newton_probe.yaml --run-cpd-like-cylinder-scoring-policy-newton-probe`.
- Added config:
  `configs/experiments/cylinder_scoring_policy_newton_probe.yaml`.
- Hardened the report and CLI after review:
  - the report now derives `package_pair_changed` and `opt_in_package_changed` from the actual
    generated package collision payloads, including primitive dimensions, centers, axes, volumes,
    source faces, fallback, and status while ignoring package metadata such as ids and source paths;
  - the CLI now rejects configs that are not scoped to
    `synthetic://cylinder_near_miss_cluster` and
    `synthetic_cylinder_scoring_policy_newton_probe`.

## Result

The clean local Newton run reported `smoke_passed` for the synthetic package pair:

- default package: `box`;
- opt-in package: `cylinder`;
- both packages passed contact canary;
- both packages passed drop/settle;
- both packages passed sphere-rain.

This is named synthetic task-smoke execution evidence for one explicitly opt-in changed package. It
is not collision-quality validation, scoring calibration, real-USD evidence, bed/Franka evidence,
benchmark evidence, or CPD paper reproduction.

## Verification

- RED:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_scoring_policy_newton_probe_runs_contact_gated_tasks tests/test_cpd_like_synthetic.py::test_cylinder_scoring_policy_newton_probe_blocks_tasks_when_contact_fails tests/test_cpd_like_synthetic.py::test_cylinder_scoring_policy_newton_probe_report_is_strict_json_serializable tests/test_cli.py::test_cli_run_cpd_like_cylinder_scoring_policy_newton_probe_requires_config tests/test_cli.py::test_cli_run_cpd_like_cylinder_scoring_policy_newton_probe_emits_json tests/test_cli.py::test_cli_run_cpd_like_cylinder_scoring_policy_newton_probe_returns_nonzero_for_partial`
  failed because the new claim constant and report builder did not exist.
- GREEN:
  the same focused command passed after implementation.
- Focused regression:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_scoring_policy_package_probe_outputs_mapped_opt_in_package tests/test_cpd_like_synthetic.py::test_cylinder_scoring_policy_newton_probe_runs_contact_gated_tasks tests/test_cpd_like_synthetic.py::test_cylinder_scoring_policy_newton_probe_blocks_tasks_when_contact_fails tests/test_cpd_like_synthetic.py::test_cylinder_scoring_policy_newton_probe_report_is_strict_json_serializable tests/test_cli.py::test_cli_run_cpd_like_cylinder_scoring_policy_newton_probe_requires_config tests/test_cli.py::test_cli_run_cpd_like_cylinder_scoring_policy_newton_probe_emits_json tests/test_cli.py::test_cli_run_cpd_like_cylinder_scoring_policy_newton_probe_returns_nonzero_for_partial tests/test_cpd_like_config.py::test_cylinder_scoring_policy_newton_probe_config_is_synthetic_and_claim_bounded`
  passed with 8 tests.
- Clean-env CLI smoke:
  `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/cylinder_scoring_policy_newton_probe.yaml --run-cpd-like-cylinder-scoring-policy-newton-probe`
  returned exit code 0 and `smoke_passed`.
- Full regression:
  `python -m pytest -q` passed with 330 tests.
- Documentation and claim checks:
  `python scripts/validate_docs.py`, `python scripts/validate_site_claims.py`, and
  `git diff --check` passed.

Multi-agent review found no Critical issues. The Important findings were fixed: changed-package
state is now derived from actual package contents, the CLI now rejects non-target configs, and the
status docs/index/plan were synchronized.

## Claim Impact

This record supports only an explicitly opt-in synthetic Newton diagnostic over the changed
near-miss package pair. It records named contact, drop/settle, and sphere-rain task-smoke status
under recorded settings.

It does not support default scoring-policy change, default package-generation change, scoring
calibration, collision-quality validation, real-USD package improvement, bed/Franka improvement,
benchmark evidence, real contact-stress measurement, safety certification, or CPD paper
reproduction.

## Next Action

The next legal slice is a separate controlled merge/search behavior change, followed by a synthetic
workbench rerun. Bed/Franka reruns should wait until the behavior-change gate is explicit and full
mapping/contact/task gates remain intact.
