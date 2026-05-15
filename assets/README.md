# Assets

This directory is for small manifests and hand-authored examples. Raw or generated 3D assets are
not committed by default.

## Policy

- Keep raw assets under `assets/raw/` and generated assets under `assets/generated/`.
- Commit only lightweight manifests, licenses, and tiny examples needed for tests.
- Record source, license, normalization, and task suitability before an asset enters a benchmark.
- Treat generated collision packages as safety-affecting artifacts that require review.

## Repo-Local Mirrors

Real USD smoke assets may be materialized into:

```text
assets/raw/mirrors/<manifest_id>/<role>/
```

This directory is intentionally ignored by git. The tracked contract is the manifest, not the raw
USD files. A manifest entry may keep the original `path`/`source_path` while adding:

- `local_path`: ignored repo-local root USD produced by asset materialization.
- `local_sha256`: hash of the local root USD. This may differ from `sha256` when USD localization
  rewrites asset paths.
- `materialization`: method, report path, local file count, dependency counts, and unresolved
  dependency names.

Runtime asset resolution prefers an existing `local_path` and falls back to the original source
path. This keeps local DLC/checker runs stable without committing raw USD, MDL, or texture files.

The current materializer records unresolved dependencies instead of hiding them. For example,
Franka mirrors currently record unresolved `OmniPBR.mdl`; this is acceptable for current geometry
smokes because the local USD still opens, but it is not a complete visual/material package.
