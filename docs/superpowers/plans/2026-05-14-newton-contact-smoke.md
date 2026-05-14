# Newton Contact Smoke Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first Newton-facing contact-only diagnostic for CPD-like primitive proposals.

**Architecture:** Add a common collision package adapter, a Newton-independent shape mapping layer, a lazily imported Newton diagnostic runner, and a CLI flag that orchestrates the existing CPD-like geometry path into `newton_contact_smoke` JSON.

**Tech Stack:** Python 3.10, NumPy, PyYAML, pytest, optional Newton/Warp runtime in the clean external conda environment.

---

## File Structure

- Modify `src/primitive_collision_compiler/contracts.py`: enrich `PrimitiveSpec` and `CollisionPackage` with conservative metadata and `to_dict()` methods while preserving old default construction.
- Create `src/primitive_collision_compiler/baselines/cpd_like/package.py`: adapt `CPDLikeDecompositionReport` to `CollisionPackage`.
- Create `src/primitive_collision_compiler/newton/shapes.py`: map common package primitives to Newton-facing descriptors and structured mapping gaps.
- Create `src/primitive_collision_compiler/newton/diagnostics.py`: lazily import Newton/Warp and run contact canaries.
- Modify `src/primitive_collision_compiler/reports/schema.py`: add `NewtonShapeMapping`, `NewtonContactCanary`, and `NewtonDiagnosticReport`.
- Modify `src/primitive_collision_compiler/cli.py`: add `--run-newton-contact-smoke` and keep existing `--run-cpd-like` behavior unchanged.
- Modify `configs/experiments/cpd_like_baseline.yaml`: add `newton_diagnostic` settings.
- Test with `tests/test_cpd_like_package.py`, `tests/test_newton_shapes.py`, `tests/test_reports_schema.py`, `tests/test_cpd_like_config.py`, and `tests/test_cli.py`.
- Add `docs/records/2026-05-14-newton-contact-smoke.md`: durable evidence record after verification.

## Task 1: Common Package Contract And CPD Adapter

**Files:**
- Modify: `src/primitive_collision_compiler/contracts.py`
- Create: `src/primitive_collision_compiler/baselines/cpd_like/package.py`
- Test: `tests/test_cpd_like_package.py`

- [ ] **Step 1: Write failing adapter tests**

```python
import numpy as np

from primitive_collision_compiler.baselines.cpd_like.decompose import decompose_mesh
from primitive_collision_compiler.baselines.cpd_like.package import package_from_cpd_like_report
from primitive_collision_compiler.geometry.mesh import TriangleMesh


def test_package_from_cpd_like_report_preserves_primitive_metadata():
    mesh = TriangleMesh(
        points=np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]),
        faces=np.array([[0, 1, 2]]),
    )
    report = decompose_mesh(mesh, max_primitives=1, primitive_subset=("box", "sphere", "capsule"))

    package = package_from_cpd_like_report(
        report,
        asset_id="tiny_tri",
        source_path="/tmp/tiny.usda",
        claim_boundary="internal_baseline_not_reproduction_claim",
        max_source_faces=8,
    )

    assert package.package_id == "tiny_tri:cpd_like_face_merge"
    assert package.asset_id == "tiny_tri"
    assert package.source_path == "/tmp/tiny.usda"
    assert package.method == "cpd_like_baseline"
    assert package.status == "smoke_passed"
    assert package.mesh_face_count == 1
    assert package.max_source_faces == 8
    assert package.primitives[0].primitive_id == "tiny_tri:primitive:0"
    assert package.primitives[0].kind in {"box", "sphere", "capsule"}
    assert package.primitives[0].source_faces == (0,)
    assert package.primitives[0].contains_assigned_points is True
    assert package.to_dict()["primitives"][0]["source_faces"] == [0]


def test_package_from_partial_report_marks_runtime_probe_blocked():
    mesh = TriangleMesh(
        points=np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [4.0, 0.0, 0.0],
                [5.0, 0.0, 0.0],
                [4.0, 1.0, 0.0],
            ]
        ),
        faces=np.array([[0, 1, 2], [3, 4, 5]]),
    )
    report = decompose_mesh(mesh, max_primitives=1, primitive_subset=("box",))

    package = package_from_cpd_like_report(
        report,
        asset_id="two_tri",
        source_path="/tmp/two.usda",
        claim_boundary="internal_baseline_not_reproduction_claim",
    )

    assert package.status == "partial"
    assert package.fallback.reason == "no_adjacent_clusters_remaining"
```

- [ ] **Step 2: Run red tests**

Run: `python -m pytest tests/test_cpd_like_package.py -q`

Expected: fail because `baselines.cpd_like.package` does not exist.

- [ ] **Step 3: Implement contract and adapter**

Add metadata fields with defaults to `PrimitiveSpec` and `CollisionPackage`, plus `to_dict()` methods. Create `package_from_cpd_like_report()` that copies CPD-like report fields into those contracts.

- [ ] **Step 4: Run green tests**

Run: `python -m pytest tests/test_cpd_like_package.py -q`

Expected: pass.

- [ ] **Step 5: Commit**

Run:

```bash
git add src/primitive_collision_compiler/contracts.py src/primitive_collision_compiler/baselines/cpd_like/package.py tests/test_cpd_like_package.py
git commit -m "feat: adapt cpd-like report to collision package"
```

## Task 2: Newton Shape Mapping

**Files:**
- Create: `src/primitive_collision_compiler/newton/shapes.py`
- Modify: `src/primitive_collision_compiler/reports/schema.py`
- Test: `tests/test_newton_shapes.py`, `tests/test_reports_schema.py`

- [ ] **Step 1: Write failing shape mapping tests**

```python
from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.newton.shapes import map_package_shapes


def test_map_package_shapes_accepts_box_sphere_capsule_without_importing_newton():
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(
            PrimitiveSpec(primitive_id="box0", kind="box", dimensions={"half_extents": [1.0, 2.0, 3.0]}),
            PrimitiveSpec(primitive_id="sphere0", kind="sphere", dimensions={"radius": 0.5}),
            PrimitiveSpec(
                primitive_id="capsule0",
                kind="capsule",
                dimensions={"radius": 0.25, "half_height": 1.0, "axis_index": 2},
            ),
        ),
    )

    mappings = map_package_shapes(package)

    assert [mapping.status for mapping in mappings] == ["mapped", "mapped", "mapped"]
    assert [mapping.kind for mapping in mappings] == ["box", "sphere", "capsule"]


def test_map_package_shapes_reports_mapping_gap_for_bad_dimensions():
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(PrimitiveSpec(primitive_id="bad", kind="sphere", dimensions={}),),
    )

    mappings = map_package_shapes(package)

    assert mappings[0].status == "mapping_gap"
    assert "radius" in mappings[0].detail
```

- [ ] **Step 2: Run red tests**

Run: `python -m pytest tests/test_newton_shapes.py -q`

Expected: fail because `primitive_collision_compiler.newton.shapes` does not exist.

- [ ] **Step 3: Implement shape mapping and schema serialization**

Create `NewtonShapeMapping` in `reports/schema.py` and `map_package_shapes()` in `newton/shapes.py`. Validate only dimensions and primitive kinds here. Do not import Newton.

- [ ] **Step 4: Run green tests**

Run: `python -m pytest tests/test_newton_shapes.py tests/test_reports_schema.py -q`

Expected: pass.

- [ ] **Step 5: Commit**

Run:

```bash
git add src/primitive_collision_compiler/newton/shapes.py src/primitive_collision_compiler/reports/schema.py tests/test_newton_shapes.py tests/test_reports_schema.py
git commit -m "feat: map collision packages to newton shape descriptors"
```

## Task 3: Newton Contact Smoke Runner

**Files:**
- Create: `src/primitive_collision_compiler/newton/diagnostics.py`
- Modify: `src/primitive_collision_compiler/reports/schema.py`
- Test: `tests/test_newton_diagnostics.py`

- [ ] **Step 1: Write failing diagnostic tests**

```python
from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.newton.diagnostics import run_newton_contact_smoke


def test_newton_contact_smoke_reports_mapping_gap_without_supported_shapes():
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(PrimitiveSpec(primitive_id="bad", kind="mesh", dimensions={}),),
    )

    report = run_newton_contact_smoke(package, source_dir="/missing/newton", device="cpu")

    assert report.stage == "newton_contact_smoke"
    assert report.status == "mapping_gap"
    assert report.asset_id == "asset"
    assert report.shape_status_counts["mapping_gap"] == 1


def test_newton_contact_smoke_reports_dependency_gap_after_mapping_passes(tmp_path):
    source_dir = tmp_path / "newton-source"
    source_dir.mkdir()
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(PrimitiveSpec(primitive_id="sphere", kind="sphere", dimensions={"radius": 0.5}),),
    )

    report = run_newton_contact_smoke(package, source_dir=str(source_dir), device="cpu")

    assert report.status in {"dependency_gap", "runtime_failure", "smoke_passed"}
    assert report.shape_status_counts["mapped"] == 1
```

- [ ] **Step 2: Run red tests**

Run: `python -m pytest tests/test_newton_diagnostics.py -q`

Expected: fail because `primitive_collision_compiler.newton.diagnostics` does not exist.

- [ ] **Step 3: Implement lazy Newton runner**

Create `NewtonDiagnosticReport` and `NewtonContactCanary` serialization, then implement:

- mapping first;
- dependency report via `inspect_newton_environment()`;
- lazy imports of `newton`, `warp`, and `numpy`;
- one representative mapped primitive per kind;
- CPU default device;
- contact count extraction from `contacts.rigid_contact_count.numpy()[0]`;
- fail-closed status classification.

- [ ] **Step 4: Run green tests**

Run: `python -m pytest tests/test_newton_diagnostics.py tests/test_reports_schema.py -q`

Expected: pass in the ambient environment without requiring Newton.

- [ ] **Step 5: Commit**

Run:

```bash
git add src/primitive_collision_compiler/newton/diagnostics.py src/primitive_collision_compiler/reports/schema.py tests/test_newton_diagnostics.py tests/test_reports_schema.py
git commit -m "feat: add newton contact smoke runner"
```

## Task 4: CLI And Config Wiring

**Files:**
- Modify: `src/primitive_collision_compiler/cli.py`
- Modify: `configs/experiments/cpd_like_baseline.yaml`
- Test: `tests/test_cli.py`, `tests/test_cpd_like_config.py`

- [ ] **Step 1: Write failing CLI and config tests**

Add a CLI test that creates a tiny USD quad, runs `--run-newton-contact-smoke`, and asserts JSON
contains `stage: newton_contact_smoke`, package metadata, and a status from
`{"smoke_passed", "dependency_gap", "mapping_gap", "runtime_failure"}`.

Add a config test that asserts `newton_diagnostic.probe_type == contact_canary` and `device == cpu`.

- [ ] **Step 2: Run red tests**

Run:

```bash
python -m pytest tests/test_cli.py::test_cli_run_newton_contact_smoke_emits_report_for_tiny_usd tests/test_cpd_like_config.py -q
```

Expected: fail because the CLI flag and config section do not exist.

- [ ] **Step 3: Implement CLI orchestration**

Add `--run-newton-contact-smoke`, reuse the existing CPD-like source resolution helpers, build the
package with `package_from_cpd_like_report()`, call `run_newton_contact_smoke()`, print JSON, and
return `0` only for `smoke_passed`.

- [ ] **Step 4: Run green tests**

Run:

```bash
python -m pytest tests/test_cli.py::test_cli_run_newton_contact_smoke_emits_report_for_tiny_usd tests/test_cpd_like_config.py -q
```

Expected: pass.

- [ ] **Step 5: Commit**

Run:

```bash
git add src/primitive_collision_compiler/cli.py configs/experiments/cpd_like_baseline.yaml tests/test_cli.py tests/test_cpd_like_config.py
git commit -m "feat: expose newton contact smoke cli"
```

## Task 5: Record, Verification, And Cleanup

**Files:**
- Create: `docs/records/2026-05-14-newton-contact-smoke.md`
- Modify: `docs/records/README.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/index.md`

- [ ] **Step 1: Add record and current status docs**

Record the repository verification commands and the clean-env `--run-newton-contact-smoke` command.
State the claim boundary: contact-only canary evidence, not collision quality or benchmark
evidence.

- [ ] **Step 2: Run full verification**

Run:

```bash
python -m pytest -q
python scripts/validate_docs.py
git diff --check
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_baseline.yaml --run-newton-contact-smoke
```

Expected: pytest/docs/whitespace pass. The clean-env command should emit `stage:
newton_contact_smoke`; if it returns `smoke_passed`, record the canary contact counts.

- [ ] **Step 3: Commit**

Run:

```bash
git add docs/records/2026-05-14-newton-contact-smoke.md docs/records/README.md docs/deepdive/evidence-status.md docs/reference/claim-boundaries.md docs/index.md
git commit -m "docs: record newton contact smoke"
```

## Self-Review

- Spec coverage: covers package adaptation, shape mapping, lazy Newton diagnostic, CLI wiring, config, records, and verification.
- Claim boundary: avoids full CPD, collision quality, benchmark, deployment, and safety claims.
- Type consistency: `CollisionPackage`, `PrimitiveSpec`, `NewtonShapeMapping`, `NewtonContactCanary`, and `NewtonDiagnosticReport` are named consistently across tasks.
