# 2026-05-15 Real USD Asset Mirror Materialization

## Date

2026-05-15

## Status

Complete

## Changes

- Added repo-local asset path resolution that prefers existing manifest `local_path` values and
  falls back to recorded source paths.
- Added `--materialize-assets` to create ignored USD mirrors under `assets/raw/mirrors/`.
- Materialized the combined bed/Franka smoke manifest and the standalone Franka smoke manifest.
- Updated tracked manifests with `source_path`, `local_path`, `local_sha256`, and materialization
  metadata.
- Added source-hash validation, safe asset-role validation, missing-path failure reports, and CLI
  stdout isolation so materialization reports remain parseable JSON.

## Review Outcome

- Multi-agent review found that source hash mismatches must fail before materialization, builder
  stdout must not pollute JSON stdout, environment-expanded paths must be used at runtime, unsafe
  roles must not escape the mirror root, and the default mirror root must be repo-local.
- Follow-up fixes covered all five points, and a final read-only review reported no remaining
  critical, important, or minor issues for those points.

## Verification

- `python -m pytest -q` exited 0 with 259 passed.
- `python scripts/validate_docs.py` exited 0; docs validation passed.
- `python scripts/validate_site_claims.py` exited 0; site claim validation passed.
- `git diff --check` exited 0.
- Focused asset mirror review verification ran
  `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider tests/test_usd_smoke.py tests/test_asset_materialization.py tests/test_cli.py`
  and passed with 72 tests.
- `PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --materialize-assets` exited 0.
- `PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/franka_cpd_like_smoke.yaml --materialize-assets` exited 0.
- `PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --check-assets` exited 0 and selected `local_path` for both roles.
- `PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/franka_cpd_like_smoke.yaml --check-assets` exited 0 and selected `local_path`.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --run-real-usd-native-fitting-comparison` exited 0 with `smoke_passed`; the report selected local mirror paths for both bed and Franka.

## Artifacts

- `assets/raw/mirrors/cpd_like_smoke_assets_2026_05_14/bed_dev_smoke/`: ignored local bed USD
  closure, 18 files, 81,263,551 bytes.
- `assets/raw/mirrors/cpd_like_smoke_assets_2026_05_14/franka_import_smoke/`: ignored local
  Franka USD layer closure, 13 files, 10,115,746 bytes, unresolved `OmniPBR.mdl`.
- `assets/raw/mirrors/franka_usd_smoke_assets_2026_05_15/franka_import_smoke/`: ignored local
  standalone Franka USD layer closure, 13 files, 10,115,746 bytes, unresolved `OmniPBR.mdl`.
- `reports/generated/asset_materialization/cpd_like_smoke_assets_2026_05_14.json`
- `reports/generated/asset_materialization/franka_usd_smoke_assets_2026_05_15.json`
- `reports/generated/asset_materialization/cpd_like_smoke_assets_check_after_mirror.json`
- `reports/generated/asset_materialization/franka_usd_smoke_assets_check_after_mirror.json`
- `reports/generated/asset_materialization/real_usd_native_fitting_after_mirror.json`

## Claim Impact

This supports asset intake and reproducibility diagnostics for the current smoke assets. It does
not support benchmark, CPD reproduction, collision-quality, whole-robot collider-quality,
deployment-readiness, or safety-certification claims.

## Next Action

Continue CPD-like algorithm work using the local mirror paths, and resolve `OmniPBR.mdl` only if a
visual/material-complete Franka package becomes necessary.
