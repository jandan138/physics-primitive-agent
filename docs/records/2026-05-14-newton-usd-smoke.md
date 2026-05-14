# 2026-05-14 Newton USD Smoke

## Date

2026-05-14

## Status

Complete

## Changes

- Added USD asset-open smoke diagnostics for the CPD-like smoke manifest.
- Added `npc-compile --check-assets`.
- Added `cpd_like.asset_manifest` to keep the bed seed asset path separate from the smoke manifest.
- Kept Newton runtime status separate from USD asset-open status.

## Verification

- `python -m pytest -q`: exit 0, 33 passed.
- `python scripts/validate_docs.py`: exit 0.
- `git diff --check`: exit 0.
- `PYTHONPATH=src python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_baseline.yaml --check-assets`: exit 0, status `smoke_passed`.
- `PYTHONPATH=src python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_baseline.yaml --check-newton`: exit 0, status `dependency_gap`.

The explicit `PYTHONPATH=src` prefix is only needed inside the feature worktree because the active
editable install points at the main checkout. After merge, the command can run from the main
checkout without that prefix.

## Observed Asset Smoke Results

- `bed_dev_smoke`: SHA-256 matched, USD opened, default prim `/Root`, 36 traversed prims, Z-up,
  meters-per-unit `0.01`.
- `franka_import_smoke`: SHA-256 matched, USD opened, default prim `/panda`, 369 traversed prims,
  Z-up, meters-per-unit `1.0`.

## Artifacts

- Config: `configs/experiments/cpd_like_baseline.yaml`
- Manifest: `assets/manifests/cpd_like_smoke_assets.yaml`
- Raw USD assets: not committed.
- Generated report target: `reports/generated/cpd_like_baseline/` (ignored).

## Claim Impact

- Supports only deterministic USD-open smoke diagnostics and environment diagnostics.
- Does not support CPD reproduction, Newton simulation, collision quality, benchmark superiority,
  deployment readiness, or safety certification.

## Next Action

- Resolve Newton `warp` dependency in a reproducible environment.
- After Newton imports cleanly, add the first runtime asset import smoke check.
