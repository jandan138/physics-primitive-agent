# CPD-Like Geometry Smoke Slice Implementation Plan

Status: Historical implementation plan. Current evidence is recorded in
`docs/records/2026-05-14-cpd-like-geometry-smoke-slice.md`.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first executable geometry-only CPD-like face-merge primitive proposal path.

**Architecture:** Add a narrow baseline package under `src/primitive_collision_compiler/baselines/cpd_like/` plus a small reusable geometry package. The implementation stays independent from Newton runtime probes and emits JSON reports through the existing CLI.

**Tech Stack:** Python 3.10+, NumPy for eigendecomposition and vector math, PyYAML config loading, pytest, optional `pxr.Usd`/`pxr.UsdGeom` for USD mesh extraction.

---

## File Structure

- Create `src/primitive_collision_compiler/geometry/mesh.py`: immutable triangle mesh, face areas, face operators, and adjacency by shared edges.
- Create `src/primitive_collision_compiler/baselines/__init__.py`: namespace marker.
- Create `src/primitive_collision_compiler/baselines/cpd_like/__init__.py`: exported CPD-like baseline API.
- Create `src/primitive_collision_compiler/baselines/cpd_like/primitives.py`: restricted enclosing primitive fitting for `box`, `sphere`, and `capsule`.
- Create `src/primitive_collision_compiler/baselines/cpd_like/decompose.py`: greedy adjacent-face merge loop and report dataclasses.
- Create `src/primitive_collision_compiler/baselines/cpd_like/usd.py`: lazy USD mesh extraction, inherited transform application, and face cap handling.
- Modify `src/primitive_collision_compiler/cli.py`: add `--run-cpd-like`.
- Modify `configs/experiments/cpd_like_baseline.yaml`: move `decomposition_stage` to `cpd_like_face_merge_smoke`, add `max_source_faces`, and record unsupported primitives.
- Modify `pyproject.toml`: add NumPy as a runtime dependency.
- Add tests in `tests/test_cpd_like_geometry.py`, `tests/test_cpd_like_decompose.py`, `tests/test_cpd_like_usd.py`, and `tests/test_cli.py`.
- Add `docs/records/2026-05-14-cpd-like-geometry-smoke-slice.md`: durable record after
  implementation and verification.

## Task 1: Geometry Mesh And Adjacency

**Files:**
- Create: `src/primitive_collision_compiler/geometry/mesh.py`
- Create: `src/primitive_collision_compiler/geometry/__init__.py`
- Test: `tests/test_cpd_like_geometry.py`

- [ ] **Step 1: Write failing tests**

```python
import numpy as np

from primitive_collision_compiler.geometry.mesh import TriangleMesh


def test_triangle_mesh_builds_shared_edge_adjacency():
    mesh = TriangleMesh(
        points=np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [1.0, 1.0, 0.0],
                [0.0, 1.0, 0.0],
                [3.0, 0.0, 0.0],
                [4.0, 0.0, 0.0],
                [3.0, 1.0, 0.0],
            ]
        ),
        faces=np.array([[0, 1, 2], [0, 2, 3], [4, 5, 6]]),
    )

    assert mesh.face_count == 3
    assert mesh.adjacent_faces() == {0: {1}, 1: {0}, 2: set()}


def test_triangle_mesh_face_operator_is_area_weighted():
    mesh = TriangleMesh(
        points=np.array([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0], [0.0, 1.0, 0.0]]),
        faces=np.array([[0, 1, 2]]),
    )

    assert mesh.face_area(0) == 1.0
    operator = mesh.face_operator(0)
    assert operator.shape == (3, 3)
    assert operator[2, 2] > 0.99
```

- [ ] **Step 2: Run red test**

Run: `python -m pytest tests/test_cpd_like_geometry.py -q`

Expected: fail with `ModuleNotFoundError` for `primitive_collision_compiler.geometry`.

- [ ] **Step 3: Implement minimal mesh support**

Implement `TriangleMesh` with validated `(N, 3)` float points, `(M, 3)` integer faces, `face_count`,
`face_points(index)`, `face_area(index)`, `face_operator(index, epsilon=1e-6)`, and
`adjacent_faces()`.

- [ ] **Step 4: Run green test**

Run: `python -m pytest tests/test_cpd_like_geometry.py -q`

Expected: pass.

## Task 2: Restricted Primitive Fitting

**Files:**
- Create: `src/primitive_collision_compiler/baselines/__init__.py`
- Create: `src/primitive_collision_compiler/baselines/cpd_like/__init__.py`
- Create: `src/primitive_collision_compiler/baselines/cpd_like/primitives.py`
- Test: `tests/test_cpd_like_decompose.py`

- [ ] **Step 1: Write failing tests**

```python
import numpy as np

from primitive_collision_compiler.baselines.cpd_like.primitives import fit_best_primitive
from primitive_collision_compiler.geometry.mesh import TriangleMesh


def test_fit_best_primitive_records_supported_and_unsupported_types():
    mesh = TriangleMesh(
        points=np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]]),
        faces=np.array([[0, 1, 2], [0, 2, 3]]),
    )

    fit = fit_best_primitive(mesh, frozenset({0, 1}), ("box", "sphere", "capsule"))

    assert fit.primitive_type in {"box", "sphere", "capsule"}
    assert fit.source_faces == (0, 1)
    assert fit.contains_assigned_points is True
    assert fit.volume > 0
    assert fit.weighted_volume > 0
    assert "frustum" in fit.unsupported_primitives
    assert "trapezoidal_prism" in fit.unsupported_primitives
```

- [ ] **Step 2: Run red test**

Run: `python -m pytest tests/test_cpd_like_decompose.py::test_fit_best_primitive_records_supported_and_unsupported_types -q`

Expected: fail with `ModuleNotFoundError` for `primitive_collision_compiler.baselines`.

- [ ] **Step 3: Implement primitive fitting**

Implement `PrimitiveFit` plus `fit_best_primitive(mesh, face_ids, primitive_subset)`. Fit OBB,
sphere, and capsule from eigen axes derived from summed face operators. Clamp dimensions with
`1e-6`, compute finite positive volume for flat meshes, and keep unsupported paper primitives in
the report.

- [ ] **Step 4: Run green test**

Run: `python -m pytest tests/test_cpd_like_decompose.py::test_fit_best_primitive_records_supported_and_unsupported_types -q`

Expected: pass.

## Task 3: Greedy Face-Merge Decomposition

**Files:**
- Create: `src/primitive_collision_compiler/baselines/cpd_like/decompose.py`
- Test: `tests/test_cpd_like_decompose.py`

- [ ] **Step 1: Write failing tests**

```python
import numpy as np

from primitive_collision_compiler.baselines.cpd_like.decompose import decompose_mesh
from primitive_collision_compiler.geometry.mesh import TriangleMesh


def test_decompose_mesh_merges_adjacent_square_to_requested_count():
    mesh = TriangleMesh(
        points=np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]]),
        faces=np.array([[0, 1, 2], [0, 2, 3]]),
    )

    report = decompose_mesh(mesh, max_primitives=1, primitive_subset=("box", "sphere", "capsule"))

    assert report.stage == "cpd_like_face_merge"
    assert report.status == "smoke_passed"
    assert report.primitive_count == 1
    assert report.primitives[0].source_faces == (0, 1)
    assert report.primitives[0].contains_assigned_points is True
    assert report.to_dict()["primitive_count"] == 1
```

- [ ] **Step 2: Run red test**

Run: `python -m pytest tests/test_cpd_like_decompose.py::test_decompose_mesh_merges_adjacent_square_to_requested_count -q`

Expected: fail because `decompose_mesh` is not implemented.

- [ ] **Step 3: Implement greedy merge**

Implement a deterministic loop: initialize one cluster per face, compute adjacency between live
clusters, score each adjacent merge by excess weighted volume, merge the lowest-cost pair, and
repeat until the requested primitive count is reached or no merge exists.

- [ ] **Step 4: Run green tests**

Run: `python -m pytest tests/test_cpd_like_decompose.py -q`

Expected: pass.

## Task 4: USD Mesh Extraction And CLI

**Files:**
- Create: `src/primitive_collision_compiler/baselines/cpd_like/usd.py`
- Modify: `src/primitive_collision_compiler/cli.py`
- Modify: `configs/experiments/cpd_like_baseline.yaml`
- Test: `tests/test_cpd_like_usd.py`
- Test: `tests/test_cli.py`

- [ ] **Step 1: Write failing USD and CLI tests**

```python
import json
from pathlib import Path

import pytest

from primitive_collision_compiler import cli
from primitive_collision_compiler.baselines.cpd_like.usd import load_first_mesh


def test_load_first_mesh_triangulates_usd_mesh(tmp_path):
    Usd = pytest.importorskip("pxr.Usd")
    UsdGeom = pytest.importorskip("pxr.UsdGeom")
    asset_path = tmp_path / "quad.usda"
    stage = Usd.Stage.CreateNew(str(asset_path))
    mesh = UsdGeom.Mesh.Define(stage, "/Quad")
    mesh.CreatePointsAttr([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
    mesh.CreateFaceVertexCountsAttr([4])
    mesh.CreateFaceVertexIndicesAttr([0, 1, 2, 3])
    stage.GetRootLayer().Save()

    loaded = load_first_mesh(asset_path, max_faces=8)

    assert loaded.face_count == 2


def test_cli_run_cpd_like_emits_report_for_tiny_usd(tmp_path, capsys):
    Usd = pytest.importorskip("pxr.Usd")
    UsdGeom = pytest.importorskip("pxr.UsdGeom")
    asset_path = tmp_path / "quad.usda"
    stage = Usd.Stage.CreateNew(str(asset_path))
    mesh = UsdGeom.Mesh.Define(stage, "/Quad")
    mesh.CreatePointsAttr([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
    mesh.CreateFaceVertexCountsAttr([4])
    mesh.CreateFaceVertexIndicesAttr([0, 1, 2, 3])
    stage.GetRootLayer().Save()
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: tiny_quad",
                f"  path: {asset_path}",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "compile:",
                "  method: cpd_like_baseline",
                "  max_primitives: 1",
                "  allowed_fallback:",
                "    - convex_hull",
                "  verify:",
                "    - geometry_only",
                "cpd_like:",
                "  primitive_subset:",
                "    - box",
                "    - sphere",
                "    - capsule",
                "  max_source_faces: 8",
            ]
        ),
        encoding="utf-8",
    )

    assert cli.main(["--config", str(config_path), "--run-cpd-like"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "cpd_like_face_merge"
    assert payload["status"] == "smoke_passed"
    assert payload["asset_id"] == "tiny_quad"
    assert payload["primitive_count"] == 1
```

- [ ] **Step 2: Run red tests**

Run: `python -m pytest tests/test_cpd_like_usd.py tests/test_cli.py::test_cli_run_cpd_like_emits_report_for_tiny_usd -q`

Expected: fail because USD extraction and `--run-cpd-like` are not implemented.

- [ ] **Step 3: Implement USD extraction and CLI**

Implement lazy USD imports, first-mesh traversal, inherited local-to-world transform application,
fan triangulation, face cap, JSON report emission, and clean exit code `2` for dependency gaps or
invalid mesh.

- [ ] **Step 4: Run green tests**

Run: `python -m pytest tests/test_cpd_like_usd.py tests/test_cli.py::test_cli_run_cpd_like_emits_report_for_tiny_usd -q`

Expected: pass.

## Task 5: Dependency, Docs, And Verification

**Files:**
- Modify: `pyproject.toml`
- Modify: `docs/deepdive/evidence-status.md`
- Create: `docs/records/2026-05-14-cpd-like-geometry-smoke-slice.md`

- [ ] **Step 1: Add NumPy dependency and config ownership**

Add `numpy>=1.26` to `pyproject.toml`. Update `configs/experiments/cpd_like_baseline.yaml` with
`cpd_like.decomposition_stage: cpd_like_face_merge_smoke`, `cpd_like.max_source_faces: 256`, and
`cpd_like.unsupported_primitives`.

- [ ] **Step 2: Run full verification**

Run:

```bash
python -m pytest -q
python scripts/validate_docs.py
git diff --check
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_baseline.yaml --run-cpd-like
```

Expected: tests, docs validation, and whitespace pass. The real-asset smoke command should either
emit `smoke_passed` or a clean JSON dependency/asset status that is recorded.

- [ ] **Step 3: Record result**

Create a dated record with the verification commands, exact result status, source asset path, and
claim boundary. The record must state that this is a geometry-only CPD-like primitive proposal
slice and does not run Newton simulation probes.

- [ ] **Step 4: Commit**

Run:

```bash
git add pyproject.toml configs/experiments/cpd_like_baseline.yaml docs/deepdive/evidence-status.md docs/records/2026-05-14-cpd-like-geometry-smoke-slice.md
git commit -m "docs: record cpd reproduction slice"
```
