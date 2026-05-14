# Newton USD Smoke Design

## Purpose

The next proof slice should turn the current Newton dependency diagnostic into a broader smoke
surface: Newton source import status plus USD asset-open status for the bed and Franka seed assets.
This is still pre-algorithm work. It does not decompose geometry, run Newton simulation, compare
collision quality, or claim CPD reproduction.

## Current State

- Newton source is present at `/cpfs/user/zhuzihou/dev/newton`.
- `import newton` still reports `dependency_gap` because `warp` is missing.
- `pxr.Usd` is available in the active Python environment.
- Manual preflight showed the bed USD opens with 36 traversed prims, Z-up, and meters-per-unit
  `0.01`.
- Manual preflight showed the Franka USD opens with 369 traversed prims, Z-up, and meters-per-unit
  `1.0`.

These observations are useful smoke evidence only. They do not establish asset correctness,
physical scale correctness, collision readiness, or licensing/provenance clearance.

## Recommended Approach

Use a small USD smoke module and CLI flag rather than trying to install or repair Newton runtime
dependencies inside the repository code.

The approach has three advantages:

- It produces immediate reproducible evidence from already available dependencies.
- It keeps generated outputs and raw assets outside git.
- It keeps the Newton `warp` gap explicit while unblocking asset intake checks.

## Interfaces

Add `primitive_collision_compiler.assets.usd_smoke` with two public functions:

- `load_asset_manifest(path)`: parse the existing smoke asset manifest and return asset entries.
- `inspect_usd_asset(asset)`: check path existence, optional SHA-256, `pxr.Usd` availability, USD
  stage open, default prim, prim count, up axis, and meters-per-unit.

Add a report dataclass:

- `AssetSmokeReport`: serializes `stage`, `status`, `role`, `path`, `checks`, and `metadata`.

Add CLI support:

```bash
npc-compile --config configs/experiments/cpd_like_baseline.yaml --check-assets
```

The command reads the `asset.path` manifest from the config and prints JSON with one report per
manifest asset. It returns exit `0` only when every report status is `smoke_passed`.

## Status Contract

- `smoke_passed`: the asset path exists, hash matches when provided, `pxr.Usd` is available, and
  `Usd.Stage.Open` returns a stage.
- `missing_asset`: the manifest path points to a missing file.
- `hash_mismatch`: a provided SHA-256 does not match the file.
- `dependency_gap`: `pxr.Usd` is unavailable.
- `usd_open_failed`: USD cannot open the file or raises an exception.

Only `smoke_passed` counts as a passing asset smoke check. Other statuses are diagnostic, not CPD
or Newton runtime results.

## Testing

Use TDD with hermetic tests:

- Create tiny USD fixtures in `tmp_path` with `pxr.Usd` for success tests.
- Use temporary manifest files instead of the CPFS asset paths for unit and CLI tests.
- Keep one integration CLI command against `configs/experiments/cpd_like_baseline.yaml` for local
  verification and records, but do not make ordinary tests depend on CPFS paths.

## Claim Boundary

This slice supports the claim that the repository can run deterministic environment and USD-open
smoke diagnostics. It does not support:

- CPD reproduction.
- Newton simulation execution.
- Collision proxy quality.
- Benchmark superiority.
- Deployment readiness.
- Safety certification.

## Next Step After This Slice

If the USD smoke check passes for bed and Franka while Newton still reports `dependency_gap`, the
next concrete step is a reproducible Newton dependency environment attempt, recorded separately.
