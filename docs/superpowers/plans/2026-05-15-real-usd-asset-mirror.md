# Real USD Asset Mirror Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Materialize the bed and Franka USD dependency closures into ignored repo-local asset mirrors, while keeping tracked manifests and runtime resolution reproducible.

**Architecture:** Add a small asset materialization module and a resolver path in the existing asset smoke module. CLI, CPD-like source resolution, and real-USD comparison share that resolver so a materialized `local_path` is used consistently when present.

**Tech Stack:** Python, PyYAML, USD `pxr.UsdUtils`, pytest, existing CLI/config/report patterns.

---

### Task 1: Asset Path Resolver

**Files:**
- Modify: `src/primitive_collision_compiler/assets/usd_smoke.py`
- Modify: `src/primitive_collision_compiler/assets/__init__.py`
- Test: `tests/test_usd_smoke.py`

- [ ] Add tests showing `inspect_usd_asset()` prefers an existing `local_path` and reports source/configured path metadata.
- [ ] Add a small `ResolvedAssetPath` dataclass and `resolve_asset_path()` helper.
- [ ] Make `inspect_usd_asset()` use the resolved path and the matching hash field: `local_sha256` for local paths, `sha256`/`source_sha256` for source paths.
- [ ] Run `python -m pytest tests/test_usd_smoke.py -q`.

### Task 2: Materialization Report

**Files:**
- Create: `src/primitive_collision_compiler/assets/materialization.py`
- Modify: `src/primitive_collision_compiler/assets/__init__.py`
- Test: `tests/test_asset_materialization.py`

- [ ] Add a failing pytest that creates a tiny USD root plus sublayer and expects materialization into a destination directory.
- [ ] Implement dependency discovery with `UsdUtils.ComputeAllDependencies`.
- [ ] Implement `build_asset_materialization_report()` using `UsdUtils.LocalizeAsset`, root hash computation, file counts, unresolved dependency recording, and local USD-open smoke.
- [ ] Run `python -m pytest tests/test_asset_materialization.py -q`.

### Task 3: CLI And Runtime Resolution Integration

**Files:**
- Modify: `src/primitive_collision_compiler/cli.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/real_usd_comparison.py`
- Test: `tests/test_cli.py`
- Test: `tests/test_real_usd_native_comparison.py`

- [ ] Add tests for `--materialize-assets` and for role resolution using a materialized path.
- [ ] Add the CLI flag and wire it to `build_asset_materialization_report()`.
- [ ] Update CPD-like and real-USD role resolution to use `resolve_asset_path()`.
- [ ] Run the targeted CLI and real-USD tests.

### Task 4: Manifest And Docs

**Files:**
- Modify: `assets/manifests/cpd_like_smoke_assets.yaml`
- Modify: `assets/manifests/franka_usd_smoke_assets.yaml`
- Modify: `assets/README.md`
- Create: `docs/reference/asset-mirror-materialization.md`
- Create: `docs/records/2026-05-15-real-usd-asset-mirror-materialization.md`
- Modify: `docs/records/README.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/index.md`
- Modify: `experiments/registry.yaml`

- [ ] Materialize the bed/Franka assets into `assets/raw/mirrors/...`.
- [ ] Update tracked manifests with `source_path`, `local_path`, `local_sha256`, and materialization metadata.
- [ ] Save the generated materialization report under `reports/generated/asset_materialization/`.
- [ ] Document the mirror layout, unresolved Franka material boundary, and no-git raw asset policy.

### Task 5: Review And Verification

**Files:**
- Review all changed code/docs.

- [ ] Dispatch code and documentation review agents.
- [ ] Address important review findings.
- [ ] Run `python -m pytest -q`.
- [ ] Run `python scripts/validate_docs.py`.
- [ ] Run `git diff --check`.
