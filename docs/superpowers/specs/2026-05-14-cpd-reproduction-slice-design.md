# CPD Reproduction Slice Design

Date: 2026-05-14

## Goal

Build the first executable geometry-only slice inspired by *Convex Primitive Decomposition for
Collision Detection* while preserving the repository's claim boundary.

This slice turns the current CPD-like baseline from configuration and USD smoke checks into a
deterministic primitive proposal path:

- read a USD mesh or an in-memory triangle mesh;
- compute face adjacency;
- initialize one group per face;
- fit enclosing primitives from a restricted Newton-friendly subset;
- greedily merge adjacent face groups by weighted excess volume;
- emit a JSON report with containment, cost, unsupported primitive, and fallback metadata.

This is not a full paper reproduction. It is a restricted, executable baseline for later Newton
diagnostic probes.

## Paper-Aligned Core

The paper's method is face-based. A primitive owns a set of faces and must enclose the vertices
assigned to those faces. The implementation should preserve that basic shape even in the first
slice:

1. Build a triangle mesh from points and triangular faces.
2. Build face adjacency from shared mesh edges.
3. For each face, compute an area-weighted face operator:
   `Q_i = area(F_i) * (n_i n_i^T + epsilon * t_i t_i^T)`.
4. For a face group, sum `Q_i`, eigendecompose the result, and use the eigenvectors as candidate
   axes.
5. Fit supported enclosing primitive candidates.
6. Score adjacent group merges by excess weighted volume:
   `weighted_volume(merged) - weighted_volume(left) - weighted_volume(right)`.
7. Merge greedily until `max_primitives` is reached or no adjacent merge remains.

## Restricted Primitive Set

The first executable set is:

- `box`;
- `sphere`;
- `capsule`.

The report must explicitly record unsupported paper primitives:

- `capped_cylinder`;
- `frustum`;
- `trapezoidal_prism`.

The first slice may choose the best primitive by weighted volume among the supported set. It does
not need intersection-volume correction, dense sampling, or postprocess primitive pruning.

## Inputs

Supported inputs:

- in-memory `TriangleMesh` for deterministic tests;
- `UsdGeom.Mesh` extraction for smoke usage.

The USD extractor must:

- import `pxr` lazily so non-USD environments can still import the package;
- triangulate polygon faces by fan triangulation;
- limit extracted faces with a config-controlled cap for smoke runs;
- report clean dependency gaps or mesh absence instead of tracebacks.

## Outputs

The CLI report should be JSON and include:

- stage and status;
- asset ID and source path;
- primitive count and requested maximum;
- primitive subset and unsupported primitive list;
- mesh point and face counts;
- per-primitive type, dimensions, source face IDs, weighted volume, raw volume, and containment;
- total weighted volume;
- fallback reason, if generation cannot run.

The output is a diagnostic report, not a generated collision asset package.

## CLI Surface

Add:

```bash
npc-compile --config configs/experiments/cpd_like_baseline.yaml --run-cpd-like
```

The command should return:

- exit code `0` when the geometry-only CPD-like slice runs and emits a `smoke_passed` report;
- exit code `2` for missing config, missing asset, USD dependency gap, no mesh, or invalid mesh.

## Claim Boundaries

Allowed wording:

- "CPD-inspired restricted primitive baseline for Newton diagnostic probes."
- "Geometry-only CPD-like face-merge primitive proposal."
- "First executable subset covering face adjacency, enclosing primitive candidates, greedy
  excess-volume merges, and fallback records."

Avoid:

- "we reproduced CPD";
- "our CPD method";
- "state-of-the-art primitive decomposition";
- "benchmark superiority";
- "validated collision correctness";
- Do not use "deployment-ready compiler";
- Do not use "safety guarantee";
- "simulation-checked" until a named Newton probe record exists.

## Non-Goals

This slice does not include:

- full CPD paper parity;
- Sketchfab-scale benchmark reproduction;
- CoACD or V-HACD comparisons;
- Newton simulation probes;
- frustum, trapezoidal prism, or capped-cylinder fitting;
- generated USD collision assets;
- large committed run artifacts.

## Verification

Required before merge:

```bash
python -m pytest -q
python scripts/validate_docs.py
git diff --check
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_baseline.yaml --run-cpd-like
```

If the real-asset smoke command fails because the dataset path or USD dependency is unavailable,
record the exact JSON status in a dated record and keep unit tests as the executable evidence.
