# 2026-05-15 Newton Sphere-Rain

## Date

2026-05-15

## Status

Complete for the narrow smoke slice.

## Changes

- Added `newton_sphere_rain`, a second named Newton task-level smoke diagnostic over the existing
  CPD-like `CollisionPackage`.
- Added `configs/experiments/newton_sphere_rain.yaml` with solver, sphere grid, contact-density
  threshold, and claim-boundary settings owned by config.
- Extended the Newton diagnostic JSON schema with `NewtonSphereRainRun` and `sphere_rain_runs`.
- Kept raw package-probe contact-row counts, but define contact density from unique contacted
  probe spheres so repeated contact rows from one sphere do not overstate coverage.
- Added CLI support for `--run-newton-sphere-rain`.

## Verification

- `python -m pytest tests/test_newton_sphere_rain.py tests/test_reports_schema.py::test_newton_diagnostic_report_serializes_sphere_rain_run tests/test_cpd_like_config.py::test_newton_sphere_rain_config_owns_probe_parameters tests/test_cli.py::test_cli_run_newton_sphere_rain_emits_report_for_tiny_usd tests/test_cli.py::test_cli_run_newton_sphere_rain_keeps_stdout_json_only tests/test_cli.py::test_cli_run_newton_sphere_rain_rejects_unsupported_probe_type -q`: 12 passed.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/newton_sphere_rain.yaml --run-newton-sphere-rain`: exit 0.

Reproducibility environment:

- Code root: `/cpfs/user/zhuzihou/dev/physics-primitive-agent/.worktrees/three-step-cpd-newton-20260515`
- Branch: `three-step-cpd-newton-20260515`
- Base git commit at the recorded run: `e79c492dfb009fc12ec929aab4c53bc5eb498550`
- Tree state at the recorded run: dirty feature worktree containing the sphere-rain code, config,
  tests, and this record; generated console JSON was not committed.
- `NEWTON_SOURCE_DIR`: `/cpfs/user/zhuzihou/dev/newton`
- Newton source commit: `96713fa965463b69c229a4d30582c733ff3526bb`
- `PYTHONPATH`: `src`
- `NPC_ENV_ROOT`: not exported for this CLI smoke; equivalent environment root:
  `/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310`
- `NPC_PYTHON`: not exported for this CLI smoke; Python executable:
  `/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python`
- Python prefix: `/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310`
- `NPC_CODE_ROOT`: not exported for this CLI smoke; code root is the worktree above.
- `NPC_OUTPUT_DIR`: not exported; this smoke emitted console JSON only.
- Platform: `Linux-5.10.134-17.3.al8.x86_64-x86_64-with-glibc2.35`
- Warp runtime observed in the smoke output: `1.13.0`
- Device setting: `cpu`; local runtime also reported an RTX 4090 CUDA device as visible.

Clean-env smoke result summary:

- `stage`: `newton_sphere_rain`
- `status`: `smoke_passed`
- `evidence_level`: `newton_sphere_rain_task_smoke`
- Newton source commit: `96713fa965463b69c229a4d30582c733ff3526bb`
- primitive mappings: 32 mapped, 0 mapping gaps
- sphere grid: 3 x 3, 9 total spheres
- sphere radius: `0.5`
- completed steps: 960
- max package-probe contact count: 1
- final package-probe contact count: 0
- max contacted probe spheres: 1
- final contacted probe spheres: 0
- contact density proxy: `0.1111111111111111` (`1 / 9` unique probe spheres)
- failure labels: none

## Artifacts

- Config: `configs/experiments/newton_sphere_rain.yaml`
- Code: `src/primitive_collision_compiler/newton/sphere_rain.py`
- Schema: `src/primitive_collision_compiler/reports/schema.py`
- CLI: `src/primitive_collision_compiler/cli.py`
- Generated console JSON was not committed; large/generated run outputs remain outside git.

## Claim Impact

This supports only a named `newton_sphere_rain` contact-density proxy smoke diagnostic for the
capped bed CPD-like package in the recorded clean local Newton environment.

It does not support collision quality validation, real contact-stress measurement, benchmark
superiority, broad asset/task coverage, safety certification, or full CPD paper reproduction.

## Next Action

See the Franka and component-merge-gate records for the next completed slices. Continue with
full verification and final review before merging the feature branch.
