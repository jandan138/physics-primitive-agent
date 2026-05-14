# 2026-05-14 CPD-Like Geometry Smoke Slice

## Date

2026-05-14

## Status

Complete for the first geometry-only CPD-like face-merge smoke slice.

## Decision

Implement a restricted CPD-inspired primitive proposal path before Newton dynamics probes. The
slice keeps the paper-aligned structure of face initialization, enclosing primitive candidates,
adjacent face-group merges, and excess-volume scoring, but it is not a full paper reproduction.

## Implemented Scope

- `TriangleMesh` with validated triangle topology, face area, face operator, and shared-edge
  adjacency.
- Restricted primitive fitting for `box`, `sphere`, and `capsule`.
- Unsupported paper primitives recorded as `capped_cylinder`, `frustum`, and
  `trapezoidal_prism`.
- Deterministic greedy merge of adjacent face groups by weighted excess volume.
- Lazy USD mesh extraction from the first `UsdGeom.Mesh`, with inherited local-to-world transform
  application, polygon fan triangulation, and a `max_source_faces` cap.
- CLI surface:

```bash
npc-compile --config configs/experiments/cpd_like_baseline.yaml --run-cpd-like
```

The committed config points at `assets/manifests/cpd_like_smoke_assets.yaml` and selects
`bed_dev_smoke` by role. Machine-local asset paths stay in the manifest and this dated record, not
in the runnable experiment config. Newton source lookup uses `NEWTON_SOURCE_DIR` when Newton
diagnostics are requested.

## Real Asset Smoke

Command:

```bash
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_baseline.yaml --run-cpd-like
```

Result:

- exit code: 0
- stage: `cpd_like_face_merge`
- status: `smoke_passed`
- asset ID: `grscenes_bed_0a85b986_smoke`
- asset path: resolved from `assets/manifests/cpd_like_smoke_assets.yaml` role `bed_dev_smoke`
- mesh point count in capped extraction: 1898
- mesh face count in capped extraction: 256
- requested max primitives: 32
- primitive count: 32
- primitive subset: `sphere`, `capsule`, `box`
- unsupported primitives recorded: `capped_cylinder`, `frustum`, `trapezoidal_prism`
- fallback reason: none
- total weighted volume: `580.1540625716117`

The command emitted a JSON report to stdout. No generated USD, raw asset, large log, video, or run
directory was committed.

## Verification

- `python -m pytest -q`: 71 passed.
- `python scripts/validate_docs.py`: passed.
- `git diff --check`: passed.
- Clean-env real asset smoke command above: exit 0, status `smoke_passed`.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_baseline.yaml --check-newton`: exit 0, status `smoke_passed`.

## Claim Impact

Supported:

- geometry-only CPD-like face-merge primitive proposal smoke;
- restricted primitive subset report generation;
- deterministic unit tests over synthetic meshes and tiny USD fixtures;
- one capped bed-asset smoke run under the clean Newton Python environment.

Not supported:

- full CPD paper reproduction;
- Sketchfab-scale benchmark reproduction;
- CoACD or V-HACD comparison;
- Newton simulation probe results;
- collision quality or benchmark superiority claims;
- generated collision package deployment.

The correct current wording is "CPD-inspired restricted primitive baseline for Newton diagnostic
probes" or "geometry-only CPD-like face-merge primitive proposal."
