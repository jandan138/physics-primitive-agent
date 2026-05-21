# 2026-05-21 Real Newton Smoke Rerun

## Date

2026-05-21

## Status

Complete

## Changes

- Stopped the report-only configured-runtime run-contract path for this turn.
- Reused the documented clean Newton conda environment:
  `/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python`.
- Reused the documented Newton checkout:
  `/cpfs/user/zhuzihou/dev/newton`.
- Re-ran the existing real Newton CLI diagnostics for the capped bed CPD-like smoke package.

## Verification

- Ambient `/usr/bin/python` did not have the runtime dependencies: `newton` and `warp` were not
  importable, and the default config failed before runtime because `$NEWTON_SOURCE_DIR` was unset.
- The clean conda environment resolved both modules:
  - `warp`: `/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/lib/python3.10/site-packages/warp/__init__.py`
  - `newton`: `/cpfs/user/zhuzihou/dev/newton/newton/__init__.py`
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_baseline.yaml --run-newton-contact-smoke`:
  exit `0`, status `smoke_passed`, Newton source commit
  `96713fa965463b69c229a4d30582c733ff3526bb`, `32` mapped box primitives, one representative
  box canary, contact count `1`.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/newton_drop_settle.yaml --run-newton-drop-settle`:
  exit `0`, status `smoke_passed`, `32` mapped primitives, one run, `2880` completed steps,
  final contact count `4`, final linear speed about `0.0404565 m/s`.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/newton_sphere_rain.yaml --run-newton-sphere-rain`:
  exit `0`, status `smoke_passed`, `32` mapped primitives, one run, `960` completed steps,
  `9` probe spheres, contact-density proxy `0.1111111111111111`.

## Artifacts

- Configs:
  - `configs/experiments/cpd_like_baseline.yaml`
  - `configs/experiments/newton_drop_settle.yaml`
  - `configs/experiments/newton_sphere_rain.yaml`
- No raw run logs, videos, assets, or generated reports were committed.

## Claim Impact

- Supports that the existing clean conda environment can still execute the named Newton contact,
  drop/settle, and sphere-rain smoke diagnostics for the capped bed CPD-like package.
- Does not add benchmark, collision-quality, full CPD reproduction, deployment-readiness,
  real-world transfer, or safety-certification evidence.

## Next Action

- Use this real Newton environment for the next runtime-facing step instead of adding another
  report-only run contract.
