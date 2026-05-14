# Sphere-Rain, Franka Smoke, And CPD-Like Component Merge Gate Plan

## Date

2026-05-15

## Status

In progress.

## Baseline Evidence

Start branch: `three-step-cpd-newton-20260515` at `e79c492`.

Baseline commands already run on the branch:

- `python -m pytest -q`: 104 passed.
- `python scripts/validate_docs.py`: passed.
- `git diff --check`: passed.

Read-only local probes already run:

- `--check-assets` on `configs/experiments/cpd_like_baseline.yaml`: bed and Franka USD open smoke
  both report `smoke_passed`.
- direct Franka `load_first_mesh(..., max_faces=128)`: `smoke_passed`, 10384 points, 128 faces.
- direct Franka `decompose_mesh(..., max_primitives=16)`: `smoke_passed`, 16 primitives.

## Task 1: Newton Sphere-Rain

Files:

- create `src/primitive_collision_compiler/newton/sphere_rain.py`;
- modify `src/primitive_collision_compiler/reports/schema.py`;
- modify `src/primitive_collision_compiler/cli.py`;
- create `configs/experiments/newton_sphere_rain.yaml`;
- modify `experiments/registry.yaml`;
- add `tests/test_newton_sphere_rain.py`;
- update `tests/test_reports_schema.py`, `tests/test_cli.py`, and `tests/test_cpd_like_config.py`;
- add `docs/records/2026-05-15-newton-sphere-rain.md`;
- update `docs/reference/claim-boundaries.md`, `docs/reference/newton-notes.md`,
  `docs/deepdive/evidence-status.md`, `docs/index.md`, and `docs/records/README.md`.

Implementation:

1. Add `SphereRainOptions` with deterministic defaults and validation.
2. Add `NewtonSphereRainRun` and serialize it through `NewtonDiagnosticReport`.
3. Add `evaluate_sphere_rain_trace()` as a pure testable failure-label function.
4. Build static package shapes with `body=-1`; build a grid of dynamic sphere bodies above the
   package bounds; run XPBD and record contact metrics.
5. Add `--run-newton-sphere-rain` and parse `newton_diagnostic.sphere_rain`.
6. Run unit tests, then run the clean-env smoke command and record exact status.

Focused checks:

```bash
python -m pytest tests/test_newton_sphere_rain.py tests/test_reports_schema.py tests/test_cli.py tests/test_cpd_like_config.py -q
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/newton_sphere_rain.yaml --run-newton-sphere-rain
```

Review checkpoint:

- spec review: report has task-scope, solver, initial conditions, failure labels, and claim
  boundary;
- quality review: no duplicated Newton runtime import logic beyond existing local pattern.

## Task 2: Franka Asset Smoke

Files:

- create `configs/experiments/franka_cpd_like_smoke.yaml`;
- modify `tests/test_cpd_like_config.py`;
- add `docs/records/2026-05-15-franka-cpd-like-smoke.md`;
- update `docs/deepdive/evidence-status.md`, `docs/index.md`, `docs/records/README.md`, and
  `experiments/registry.yaml`.

Implementation:

1. Add a config selecting manifest role `franka_import_smoke`.
2. Keep `/cpfs/user/...` paths in the manifest only.
3. Keep `include_in_cpd_like_aggregate: false`.
4. Run `--check-assets` and `--run-cpd-like` in the clean environment.
5. Record that this is a second asset-class smoke, not aggregate robot evidence.

Focused checks:

```bash
python -m pytest tests/test_cpd_like_config.py tests/test_cli.py::test_cli_run_cpd_like_resolves_manifest_asset_role -q
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/franka_cpd_like_smoke.yaml --run-cpd-like
```

Review checkpoint:

- spec review: no broad robot or benchmark claim;
- quality review: config mirrors the existing baseline style.

## Task 3: CPD-Like Component Merge Gate

Files:

- modify `src/primitive_collision_compiler/baselines/cpd_like/primitives.py`;
- modify `src/primitive_collision_compiler/baselines/cpd_like/decompose.py`;
- modify `src/primitive_collision_compiler/cli.py`;
- create `configs/experiments/cpd_like_component_merge_gate.yaml`;
- update `tests/test_cpd_like_decompose.py`;
- add `docs/records/2026-05-15-cpd-like-component-merge-gate.md`;
- update `docs/reference/cpd-like-face-merge-explainer.md`, `docs/reference/claim-boundaries.md`,
  `docs/deepdive/evidence-status.md`, `docs/index.md`, and `docs/records/README.md`.

Implementation:

1. Add per-primitive `source_face_count`, `source_component_ids`, and `cost_weight` metadata that
   is deterministic and JSON-safe.
2. Keep the default CPD-like path as topology-only face merging.
3. Add opt-in `component_merge: virtual_pairwise` to try disconnected-component pairwise merges
   after topology adjacency merges are exhausted.
4. Normalize optional virtual-merge thresholding by mesh AABB volume and report blocked merges.
5. Add report-level merge policy, component counts, merge counts, normalized total weighted
   volume, and merge-cost summary.
6. Re-run the bed component-merge-gate smoke command and record the new fields.

Focused checks:

```bash
python -m pytest tests/test_cpd_like_decompose.py tests/test_cpd_like_config.py::test_cpd_like_component_merge_gate_config_is_opt_in_and_claim_bounded tests/test_cli.py::test_cli_run_cpd_like_component_merge_gate_emits_merge_metrics -q
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_component_merge_gate.yaml --run-cpd-like
```

Review checkpoint:

- spec review: names stay within `cpd_like_component_merge_gate`;
- quality review: merge fields do not alter existing primitive conversion semantics unless a
  test explicitly covers the intended behavior.

## Final Verification

After all three tasks and review loops:

```bash
python -m pytest -q
python scripts/validate_docs.py
git diff --check
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/newton_sphere_rain.yaml --run-newton-sphere-rain
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/franka_cpd_like_smoke.yaml --run-cpd-like
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_component_merge_gate.yaml --run-cpd-like
```

Then dispatch final review over the full diff and only update the active goal after every prompt
deliverable maps to a tracked artifact or a recorded evidence command.
