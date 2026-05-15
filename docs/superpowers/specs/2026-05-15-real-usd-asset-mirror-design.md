# Real USD Asset Mirror Design

## Status

Approved direction, implementation in progress.

## Problem

The bed and Franka smoke assets are currently referenced from absolute CPFS paths in tracked
manifests. That is acceptable for early local smoke tests, but it is weak for DLC and repeatable
agent workflows because a clean checkout cannot tell whether the needed USD dependency closure has
been copied beside the repository.

The repository should keep the raw USD files out of git while still making the runnable asset state
explicit, checkable, and easy to recreate.

## Current Dependency Findings

`bed_dev_smoke` points at one root USD. `UsdUtils.ComputeAllDependencies` reports one USD layer and
seventeen external material dependencies: one `.mdl` file and sixteen `.png` textures. The external
dependencies live under `/cpfs/shared/simulation/.../GRScenes-test0-rebuilt/Material/mdl`. The bed
root USD authors absolute material/texture paths, so simply copying the root USD is not portable.
It needs a localized copy with asset paths rewritten relative to the local mirror.

`franka_import_smoke` points at `franka.usd`. Its minimum USD layer closure is the root USD, eleven
`Props/*.usd` files, and `Materials/Materials.usd`. It also has an unresolved `OmniPBR.mdl`
material shader asset. The USD geometry layer closure can be mirrored, but the material dependency
must remain recorded as unresolved until a reviewed MDL source or search path is added.

## Design

Materialized assets live under ignored repo-local paths:

```text
assets/raw/mirrors/<manifest_id>/<role>/
```

Tracked manifests continue to record the original source path, hash, size, provenance, and license
context. They may also record `local_path`, `local_sha256`, and `materialization` metadata after a
local mirror has been created. Runtime path resolution prefers an existing `local_path`, then falls
back to the source path. This lets the same manifest work both before and after materialization.

The materializer uses USD's dependency tools rather than ad hoc string parsing:

- `UsdUtils.ComputeAllDependencies` records layer, asset, and unresolved dependencies.
- `UsdUtils.LocalizeAsset` writes the local mirror and rewrites resolvable asset paths.
- The report records copied file counts, root-local hash, unresolved dependencies, and whether the
  localized root USD can still open.

## Command Surface

Add one CLI command:

```bash
python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --materialize-assets
```

The command emits JSON. Generated reports may be saved under `reports/generated/asset_materialization/`.
Raw mirrored assets stay under `assets/raw/` and are ignored by git.

## Claim Boundary

This work supports asset intake and reproducibility diagnostics only. It does not add CPD paper
algorithm fidelity, compiler functionality, benchmark evidence, collision-quality validation,
deployment readiness, safety certification, or robot articulation evidence.
