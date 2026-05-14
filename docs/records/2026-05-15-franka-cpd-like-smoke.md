# 2026-05-15 Franka CPD-Like Smoke

## Date

2026-05-15

## Status

Complete for the narrow Franka USD and capped geometry smoke slice.

## Changes

- Added `assets/manifests/franka_usd_smoke_assets.yaml` for the local Franka USD path and hash.
- Added `configs/experiments/franka_cpd_like_smoke.yaml`, selecting manifest role
  `franka_import_smoke`.
- Kept `include_in_cpd_like_aggregate: false` for the Franka asset.
- Added config/manifest tests for the Franka smoke path.

## Verification

- `python -m pytest tests/test_cpd_like_config.py::test_franka_smoke_asset_manifest_records_robot_path_without_committing_asset tests/test_cpd_like_config.py::test_franka_cpd_like_smoke_config_selects_robot_manifest_role -q`: 2 passed.
- `PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/franka_cpd_like_smoke.yaml --check-assets`: exit 0, `smoke_passed`.
- `PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/franka_cpd_like_smoke.yaml --run-cpd-like`: exit 0, `smoke_passed`.

Franka USD-open summary:

- role: `franka_import_smoke`
- path: `/cpfs/user/zhuzihou/assets/zzh-grscenes/robots/franka/franka.usd`
- SHA-256: `2bfd004928d4157ca2fdca3e79bcfb913b4008eef3ec16f839ad89314141976b`
- default prim: `/panda`
- prim count: 369
- meters per unit: 1.0
- up axis: `Z`

Franka capped CPD-like geometry summary:

- `stage`: `cpd_like_face_merge`
- `status`: `smoke_passed`
- `mesh_point_count`: 10384
- `mesh_face_count`: 128
- `primitive_count`: 16
- `max_primitives`: 16
- `total_weighted_volume`: `3.8345518193648747e-07`
- claim boundary: `robot_asset_import_smoke_not_collision_quality`

## Artifacts

- Manifest: `assets/manifests/franka_usd_smoke_assets.yaml`
- Config: `configs/experiments/franka_cpd_like_smoke.yaml`
- Generated console JSON was not committed; large/generated run outputs remain outside git.

## Claim Impact

This supports only that the local Franka USD can be opened and that the current geometry-only
CPD-like smoke path can extract a capped first mesh and emit restricted primitive proposals.

It does not support whole-robot collider quality, articulated dynamics, robot task simulation,
aggregate robot evidence, benchmark superiority, or full CPD paper reproduction.

## Next Action

Implement the opt-in CPD-like component-merge gate as a narrow CPD-inspired algorithm slice.
