# Asset Mirror Materialization

This page explains how real USD smoke assets are kept near the repository without committing raw
assets to git.

## Plain Summary

The tracked repository keeps only small contracts:

- YAML manifests that name the source USDs;
- hash and provenance metadata;
- commands and records that can regenerate local mirrors.

The heavy files live in ignored paths:

```text
assets/raw/mirrors/<manifest_id>/<asset_role>/
```

This is the intended compromise for the current work:

```text
stable enough for local Newton/CPD smoke runs
without committing USD, MDL, or texture payloads to git
```

## Why This Layout Is The Project Norm

The bed and Franka manifests can now point at ignored repo-local mirrors under `assets/raw/mirrors/`.
The original CPFS source paths are still recorded, but runtime resolution prefers `local_path` when
that file exists.

That gives three useful properties:

- **Reproducibility:** the manifest keeps the source path, source hash, local path, local hash, and
  materialization report path.
- **Local stability:** downstream commands can use a repo-local path instead of repeatedly reaching
  through the original CPFS dataset layout.
- **Git hygiene:** raw USD closures, MDL files, textures, and generated JSON reports stay out of
  git; only lightweight manifests and records are tracked.

The materializer command is:

```bash
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --materialize-assets
```

Generated JSON reports are kept under `reports/generated/asset_materialization/`, which is also
ignored by git.

## Runtime Resolution Rule

Every manifest asset can carry both a source path and a local mirror path:

```yaml
path: /original/cpfs/source/root.usd
source_path: /original/cpfs/source/root.usd
local_path: assets/raw/mirrors/<manifest_id>/<role>/root.usd
sha256: <source-root-hash>
local_sha256: <localized-root-hash>
```

Runtime inspection and real-USD CPD-like comparison use this rule:

```text
if local_path exists:
    use local_path and validate local_sha256 when present
else:
    use path/source_path and validate sha256/source_sha256 when present
```

The local root hash can differ from the source root hash because USD localization rewrites asset
references from absolute or external paths into local relative paths. That is expected when the
localized USD opens and the source hash was checked before materialization.

## Bed

The bed root USD has one USD layer and seventeen external material assets: one `.mdl` file and
sixteen `.png` textures. The source USD authored absolute material paths, so the materializer uses
USD localization to create a local copy with relative asset paths.

Current local root:

```text
assets/raw/mirrors/cpd_like_smoke_assets_2026_05_14/bed_dev_smoke/0a85b986de35ccfdec7c686d791fd747.usd
```

The local root hash differs from the source root hash because localization rewrites asset paths.

Current recorded closure:

```text
18 files
81,263,551 bytes
1 USD layer
17 external material assets
0 unresolved dependencies
```

For the current CPD/Newton smoke story, the bed mirror is the cleaner of the two real assets: its
known material and texture dependencies are present in the local mirror. That still does not make
it a benchmark asset or a collision-quality reference asset.

## Franka

The Franka root USD has a local USD layer closure: `franka.usd`, eleven `Props/*.usd` files, and
`Materials/Materials.usd`. The material shader references `OmniPBR.mdl`, which is unresolved in
the current mirror.

Current local root for the combined bed/Franka manifest:

```text
assets/raw/mirrors/cpd_like_smoke_assets_2026_05_14/franka_import_smoke/franka.usd
```

Current local root for the standalone Franka smoke manifest:

```text
assets/raw/mirrors/franka_usd_smoke_assets_2026_05_15/franka_import_smoke/franka.usd
```

Both local Franka roots open for the current USD smoke path, but the unresolved MDL means this is
not a complete visual/material packaging claim.

Current recorded closure per Franka mirror:

```text
13 files
10,115,746 bytes
13 USD layers
0 copied external texture assets
1 known unresolved dependency: OmniPBR.mdl
```

That unresolved dependency is acceptable for the current geometry-first smoke path because the USD
opens and mesh extraction works. It becomes a blocker only if the project wants to claim a
complete visual/material package, inspect rendered visual fidelity, or depend on the material
graph for a future task.

## What Goes Into Git

Commit-safe:

- `assets/manifests/*.yaml`;
- `configs/experiments/*.yaml`;
- `docs/reference/*.md`;
- `docs/records/*.md`;
- small test fixtures created specifically for unit tests.

Not commit-safe by default:

- `assets/raw/mirrors/`;
- `assets/generated/`;
- `reports/generated/`;
- large logs, videos, run directories, copied USD payloads, MDL files, and textures.

The tracked manifest is the contract. The ignored mirror is the local payload.

## How To Check A Mirror

After materialization, run asset checks through the same config:

```bash
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --check-assets
```

For the current smoke assets, a healthy check means:

- both roles select `local_path`;
- both root USD files open;
- source or local hash fields match the file actually used;
- unresolved dependencies remain recorded instead of being hidden.

For Franka, `OmniPBR.mdl` remains an explicit visual/material boundary rather than an unknown
failure.

## Where This Fits In The CPD Story

Asset mirrors are not an algorithmic result. They are the stable input shelf for algorithmic work:

```text
source USD
-> ignored local mirror
-> USD-open and mesh-extraction smoke
-> CPD-like primitive proposals
-> CollisionPackage
-> Newton diagnostics
```

The current mirror work makes the first arrow reproducible enough for local and future DLC-style
runs. It does not change the fact that the current real-USD native lanes still selected only
`box` primitives.

## Claim Boundary

Asset materialization is an intake and reproducibility diagnostic. It does not claim CPD
reproduction, compiler completeness, benchmark evidence, collision-quality validation,
whole-robot Franka collider quality, deployment readiness, or safety certification.
