# 2026-05-25 Phase 0 GRScenes Asset Intake

## Date

2026-05-25

## Status

Complete for Phase 0 asset selection, repo-local mirror materialization, and manifest recording.
Not complete for Phase 0 benchmark execution, primitive package generation, Newton task probes, or
paper metric claims.

## Changes

- Replaced the placeholder Phase 0 asset manifest with five selected GRScenes USD assets:
  `box`, `bowl`, `cup`, `tray`, and `keyboard`.
- Covered the Phase 0 manifest roles `rigid_prop`, `container`, `contact_affordance`,
  `stackable`, and `precision_negative_control`.
- Kept the original GRScenes locations only as `source_path` fields and pointed runtime
  `path`/`local_path` fields at the ignored repo-local mirror under
  `assets/raw/mirrors/phase0_grscenes_assets_2026_05_25/`.
- Recorded source hashes, local hashes, materialization method, local file counts, local extension
  counts, concrete localized MDL/texture dependency filenames, dependency counts, and unresolved
  dependency counts in `assets/manifests/phase0_assets.yaml`.
- Kept `pxr.UsdUtils.ComputeAllDependencies` plus `pxr.UsdUtils.LocalizeAsset` as the primary
  materialization path because it produced the USD, MDL, and texture dependency closure for these
  binary GRScenes USD files.

## Artifacts

- Tracked manifest: `assets/manifests/phase0_assets.yaml`.
- Ignored local mirror: `assets/raw/mirrors/phase0_grscenes_assets_2026_05_25/`.
- Ignored materialization report:
  `reports/generated/asset_materialization/phase0_grscenes_assets_2026_05_25.json`.

## Materialization Result

- command exit: `0`
- report status: `materialized`
- asset count: `5`
- per-asset status: all five entries `materialized`
- unresolved dependency count: `0` for each selected asset

USD localization printed resolver warnings while chasing material and texture references. The
generated report still records resolved dependency summaries and zero unresolved dependencies for
the selected entries.

## Cross-Check

`/cpfs/shared/simulation/zhuzihou/dev/usd-scene-physics-prep/scripts/build_uid_subset_package.py`
was used as a reference for GRScenes UID packaging semantics. It is useful to confirm that selected
UIDs live under the expected `GRScenes_assets/<category>/<uid>/` folders and to package whole UID
directories. For this Phase 0 intake, it was not used as the primary dependency-closure mechanism
because its USD attribute scanner did not collect the MDL/texture references that
`UsdUtils.ComputeAllDependencies` reported for the selected binary USD files.

## Verification

- `python -m pytest tests/test_configs.py::test_phase0_manifest_uses_repo_local_grscenes_mirrors -q`:
  `1 passed`.

## Claim Impact

This supports only the claim that the Phase 0 benchmark now has a concrete, repo-local,
manifested GRScenes asset intake. It does not support benchmark results, simulation-checked
acceptance rates, speedup claims, collision-quality validation, deployment readiness, or safety
certification.

## Next Action

Run the Phase 0 multi-asset benchmark suite and add dated records for accept/fallback outcomes
before using Phase 0 tables in the paper.
