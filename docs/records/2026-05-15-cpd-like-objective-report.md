# 2026-05-15 CPD-Like Objective Report

## Date

2026-05-15

## Status

Complete.

## Changes

- Added `cpd_like_offline_objective`, an offline paper-aligned surrogate objective report over the
  current CPD-like decomposition report.
- Added a dedicated CLI flag: `--run-cpd-like-objective-report`.
- Added `configs/experiments/cpd_like_objective_report.yaml` for the capped bed objective-report
  smoke.
- Added objective terms for primitive budget, AABB-normalized volume proxy, merge-excess
  accounting, assigned-point containment proxy, unsupported paper primitive gaps, and
  component/fallback labels.
- Added focused synthetic tests for objective math, partial decompositions, finite normalization,
  invalid weights, CLI JSON output, and config claim boundaries.
- Added review hardening for strict finite JSON output, partial objective CLI behavior,
  malformed objective config coverage, blocked-merge labels, uncontained primitive labels, and
  stable report schema keys.

## Verification

- `python -m pytest tests/test_cpd_like_objective.py tests/test_cli.py -q -k 'objective_report or objective'`: 20 passed, 28 deselected.
- `python -m pytest tests/test_cpd_like_objective.py tests/test_cli.py tests/test_cpd_like_config.py -q`: 58 passed.
- `PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_objective_report.yaml --run-cpd-like-objective-report`: exit 0.
- `python -m pytest -q`: 149 passed.
- `python scripts/validate_docs.py`: passed.
- `git diff --check`: passed.

## Smoke Summary

- Stage: `cpd_like_offline_objective`
- Status: `smoke_passed`
- Source decomposition stage: `cpd_like_component_merge_gate`
- Mesh cap: 256 faces, 1898 points
- Primitive budget: 32/32, over budget count 0
- Containment proxy: 32/32 assigned-point-containing primitives
- Merge accounting: 224 accepted topology merges, 0 virtual component merges, 0 blocked merges
- Accepted normalized merge-excess sum: `0.000996148870132146`
- Normalized weighted primitive volume: `0.0009961811821648128`
- Unsupported paper primitive gap: `capped_cylinder`, `frustum`, `trapezoidal_prism`
- Failure labels: none

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_like/objective.py`
- `configs/experiments/cpd_like_objective_report.yaml`
- `tests/test_cpd_like_objective.py`
- `docs/superpowers/specs/2026-05-15-cpd-objective-report-design.md`
- `docs/superpowers/plans/2026-05-15-cpd-objective-report.md`

Generated console JSON and runtime logs were not committed.

## Claim Impact

This record supports only an offline CPD-like objective diagnostic smoke over the capped bed
baseline. It does not support full CPD paper reproduction, paper-faithful primitive optimization,
collision-quality validation, benchmark superiority, broad asset/task evidence, whole-robot
collider quality, or safety/deployment claims.

## Next Action

Add small inspectable synthetic cases and compare topology-only versus component-merge outputs
using the same objective report before changing primitive fitting, merge search, or Newton task
probes.
