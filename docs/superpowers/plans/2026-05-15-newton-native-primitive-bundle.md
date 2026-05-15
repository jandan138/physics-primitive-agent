# Newton Native Primitive Bundle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add verified runtime-path support for Newton-native `cylinder`, `cone`, and `ellipsoid` package primitives, on top of existing `box`, `sphere`, and `capsule` support.

**Architecture:** Keep the runtime lane Newton-native first. `src/primitive_collision_compiler/newton/shapes.py` validates package dimensions and produces `NewtonShapeMapping`; each Newton diagnostic module owns its own builder call and conservative AABB/support estimates. Keep `capped_cylinder`, `frustum`, and `trapezoidal_prism` outside runtime mapping.

**Tech Stack:** Python dataclasses, pytest, existing Newton diagnostic modules, Markdown dated records.

---

## File Structure

- Modify `src/primitive_collision_compiler/newton/shapes.py`: expand `SUPPORTED_NEWTON_SHAPES`, validate schemas for `cylinder`, `cone`, and `ellipsoid`.
- Modify `src/primitive_collision_compiler/newton/diagnostics.py`: add static-shape builder calls and probe-radius logic for the three new native kinds.
- Modify `src/primitive_collision_compiler/newton/drop_settle.py`: add dynamic-shape builder calls plus conservative world extent and support-height estimates.
- Modify `src/primitive_collision_compiler/newton/sphere_rain.py`: add static-shape builder calls; package bounds reuse `drop_settle._world_half_extents`.
- Modify `tests/test_newton_shapes.py`: add mapping and validation tests for the complete native bundle and preserve `capped_cylinder` mapping gap.
- Modify `tests/test_newton_diagnostics.py`: add direct builder/probe tests for native static contact canary construction.
- Modify `tests/test_newton_drop_settle.py`: add direct builder and extent/support tests for native dynamic drop-settle construction.
- Modify `tests/test_newton_sphere_rain.py`: add direct builder and package-bounds tests for native static sphere-rain construction.
- Add `docs/records/2026-05-15-newton-native-primitive-bundle.md`: dated implementation and verification record.
- Update `docs/index.md`, `docs/reference/cpd-objective-report-alignment.md`, `docs/reference/cpd-paper-story-status.md`, `docs/deepdive/evidence-status.md`, and `docs/records/README.md`: move the native bundle from roadmap to implemented diagnostic evidence, with clear claim boundaries.

## Dimension Schemas

- `cylinder`: `{"radius": float > 0, "half_height": float >= 0, "axis_index": 0|1|2 optional}`.
- `cone`: `{"radius": float > 0, "half_height": float >= 0, "axis_index": 0|1|2 optional}`.
- `ellipsoid`: `{"radii": [rx, ry, rz]}` with all three radii positive finite.

`axis_index` follows the existing capsule convention: the selected package axis becomes Newton local Z for Z-axis analytic shapes. Ellipsoid uses the package axes directly.

### Task 1: Mapping Contract

**Files:**
- Modify: `tests/test_newton_shapes.py`
- Modify: `src/primitive_collision_compiler/newton/shapes.py`

- [ ] **Step 1: Write failing tests for complete native mapping**

Add a test that builds one package with `box`, `sphere`, `capsule`, `cylinder`, `cone`, and `ellipsoid`, then asserts all map and serialize with finite JSON.

```python
def test_map_package_shapes_accepts_complete_newton_native_bundle_without_importing_newton():
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(
            PrimitiveSpec(primitive_id="box0", kind="box", dimensions={"half_extents": [1.0, 2.0, 3.0]}),
            PrimitiveSpec(primitive_id="sphere0", kind="sphere", dimensions={"radius": 0.5}),
            PrimitiveSpec(primitive_id="capsule0", kind="capsule", dimensions={"radius": 0.25, "half_height": 1.0, "axis_index": 2}),
            PrimitiveSpec(primitive_id="cylinder0", kind="cylinder", dimensions={"radius": 0.3, "half_height": 0.8, "axis_index": 1}),
            PrimitiveSpec(primitive_id="cone0", kind="cone", dimensions={"radius": 0.4, "half_height": 0.9, "axis_index": 0}),
            PrimitiveSpec(primitive_id="ellipsoid0", kind="ellipsoid", dimensions={"radii": [0.2, 0.4, 0.6]}),
        ),
    )

    mappings = map_package_shapes(package)

    assert [mapping.status for mapping in mappings] == ["mapped"] * 6
    assert [mapping.kind for mapping in mappings] == [
        "box",
        "sphere",
        "capsule",
        "cylinder",
        "cone",
        "ellipsoid",
    ]
    json.dumps([mapping.to_dict() for mapping in mappings], allow_nan=False)
```

- [ ] **Step 2: Write failing tests for native validation errors**

Add one test that verifies invalid `radius`, `half_height`, `axis_index`, and `radii` values are mapping gaps with readable details.

```python
def test_map_package_shapes_rejects_bad_native_bundle_dimensions():
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(
            PrimitiveSpec(primitive_id="bad-cylinder-radius", kind="cylinder", dimensions={"radius": 0.0, "half_height": 1.0}),
            PrimitiveSpec(primitive_id="bad-cylinder-axis", kind="cylinder", dimensions={"radius": 0.3, "half_height": 1.0, "axis_index": 4}),
            PrimitiveSpec(primitive_id="bad-cone-height", kind="cone", dimensions={"radius": 0.3, "half_height": -1.0}),
            PrimitiveSpec(primitive_id="bad-capsule-axis-bool", kind="capsule", dimensions={"radius": 0.3, "half_height": 1.0, "axis_index": True}),
            PrimitiveSpec(primitive_id="bad-cylinder-axis-float", kind="cylinder", dimensions={"radius": 0.3, "half_height": 1.0, "axis_index": 1.0}),
            PrimitiveSpec(primitive_id="bad-ellipsoid-radii", kind="ellipsoid", dimensions={"radii": [0.2, math.inf, 0.6]}),
        ),
    )

    mappings = map_package_shapes(package)

    assert [mapping.status for mapping in mappings] == ["mapping_gap"] * 6
    assert "cylinder radius" in mappings[0].detail
    assert "cylinder axis_index" in mappings[1].detail
    assert "cone half_height" in mappings[2].detail
    assert "capsule axis_index" in mappings[3].detail
    assert "cylinder axis_index" in mappings[4].detail
    assert "ellipsoid radii" in mappings[5].detail
```

- [ ] **Step 3: Run RED mapping tests**

Run:

```bash
python -m pytest tests/test_newton_shapes.py -q -k "complete_newton_native_bundle or bad_native_bundle_dimensions"
```

Expected: fail because `cylinder`, `cone`, and `ellipsoid` are unsupported.

- [ ] **Step 4: Implement minimal mapping validators**

Update `SUPPORTED_NEWTON_SHAPES` and dispatch validation by kind:

```python
SUPPORTED_NEWTON_SHAPES = ("box", "sphere", "capsule", "cylinder", "cone", "ellipsoid")
```

Import `Integral` from `numbers`, then add helpers:

```python
def _validate_axis_shape(dimensions: dict[str, Any], kind: str) -> str:
    if _as_positive_float(dimensions.get("radius")) is None:
        return f"{kind} radius is required and must be positive finite"
    if _as_non_negative_float(dimensions.get("half_height")) is None:
        return f"{kind} half_height is required and must be non-negative finite"
    axis_index = dimensions.get("axis_index", 2)
    if isinstance(axis_index, bool) or not isinstance(axis_index, Integral) or axis_index not in (0, 1, 2):
        return f"{kind} axis_index must be 0, 1, or 2"
    return ""


def _validate_ellipsoid(dimensions: dict[str, Any]) -> str:
    radii = dimensions.get("radii")
    if not isinstance(radii, list | tuple) or len(radii) != 3:
        return "ellipsoid radii must contain three positive finite values"
    if any(_as_positive_float(value) is None for value in radii):
        return "ellipsoid radii must contain three positive finite values"
    return ""
```

- [ ] **Step 5: Run GREEN mapping tests**

Run:

```bash
python -m pytest tests/test_newton_shapes.py -q -k "native_bundle or capped_cylinder"
```

Expected: pass, including the preserved `capped_cylinder` mapping-gap test.

- [ ] **Step 6: Commit mapping contract**

```bash
git add tests/test_newton_shapes.py src/primitive_collision_compiler/newton/shapes.py
git commit -m "feat: map newton native primitive bundle"
```

### Task 2: Contact Canary Builder

**Files:**
- Modify: `tests/test_newton_diagnostics.py`
- Modify: `src/primitive_collision_compiler/newton/diagnostics.py`

- [ ] **Step 1: Write failing direct builder test**

Add small fake `wp` and builder classes, then assert `_add_static_shape` dispatches each new kind to the matching Newton builder method.

```python
from primitive_collision_compiler.newton.diagnostics import _add_static_shape, _probe_radius
from primitive_collision_compiler.reports.schema import NewtonShapeMapping


def test_contact_canary_builds_newton_native_static_shapes():
    builder = _RecordingBuilder()
    wp = _FakeWarp()
    mappings = (
        _mapping("cylinder0", "cylinder", {"radius": 0.3, "half_height": 0.8, "axis_index": 1}),
        _mapping("cone0", "cone", {"radius": 0.4, "half_height": 0.9, "axis_index": 0}),
        _mapping("ellipsoid0", "ellipsoid", {"radii": [0.2, 0.4, 0.6]}),
    )

    for mapping in mappings:
        _add_static_shape(builder, mapping, wp)

    assert [call[0] for call in builder.calls] == ["cylinder", "cone", "ellipsoid"]
    assert builder.calls[0][1]["radius"] == 0.3
    assert builder.calls[1][1]["half_height"] == 0.9
    assert builder.calls[2][1]["rx"] == 0.2
    assert builder.calls[2][1]["ry"] == 0.4
    assert builder.calls[2][1]["rz"] == 0.6
```

Also add:

```python
def test_contact_canary_probe_radius_uses_native_bundle_dimensions():
    assert _probe_radius(_mapping("cylinder0", "cylinder", {"radius": 0.3, "half_height": 0.8})) == 0.15
    assert _probe_radius(_mapping("cone0", "cone", {"radius": 0.4, "half_height": 0.9})) == 0.2
    assert _probe_radius(_mapping("ellipsoid0", "ellipsoid", {"radii": [0.2, 0.4, 0.6]})) == 0.1
```

- [ ] **Step 2: Run RED contact tests**

Run:

```bash
python -m pytest tests/test_newton_diagnostics.py -q -k "native_static_shapes or probe_radius"
```

Expected: fail because the new kinds are not builder-supported.

- [ ] **Step 3: Implement contact builder support**

In `_add_static_shape`, add:

```python
elif mapping.kind == "cylinder":
    builder.add_shape_cylinder(body=-1, xform=xform, radius=float(dimensions["radius"]), half_height=float(dimensions["half_height"]))
elif mapping.kind == "cone":
    builder.add_shape_cone(body=-1, xform=xform, radius=float(dimensions["radius"]), half_height=float(dimensions["half_height"]))
elif mapping.kind == "ellipsoid":
    rx, ry, rz = (float(value) for value in dimensions["radii"])
    builder.add_shape_ellipsoid(body=-1, xform=xform, rx=rx, ry=ry, rz=rz)
```

Use the same axis-orientation helper for `cylinder` and `cone` that `capsule` uses.

- [ ] **Step 4: Run GREEN contact tests**

Run:

```bash
python -m pytest tests/test_newton_diagnostics.py tests/test_newton_shapes.py -q -k "native or representative_canary_scope or capped_cylinder"
```

Expected: pass.

- [ ] **Step 5: Commit contact support**

```bash
git add tests/test_newton_diagnostics.py src/primitive_collision_compiler/newton/diagnostics.py
git commit -m "feat: add native primitive contact canary builders"
```

### Task 3: Drop-Settle Builder And Extents

**Files:**
- Modify: `tests/test_newton_drop_settle.py`
- Modify: `src/primitive_collision_compiler/newton/drop_settle.py`

- [ ] **Step 1: Write failing builder and extent tests**

Add tests that assert dynamic shape dispatch, world half-extents, and support-height estimates for native shapes.

```python
from primitive_collision_compiler.newton.drop_settle import _add_dynamic_shape, _support_extent_z, _world_half_extents
from primitive_collision_compiler.reports.schema import NewtonShapeMapping


def test_drop_settle_builds_newton_native_dynamic_shapes():
    builder = _RecordingBuilder()
    wp = _FakeWarp()
    anchor = (1.0, 2.0, 3.0)
    mappings = (
        _mapping("cylinder0", "cylinder", {"radius": 0.3, "half_height": 0.8, "axis_index": 1}, center=(1.0, 2.0, 4.0)),
        _mapping("cone0", "cone", {"radius": 0.4, "half_height": 0.9, "axis_index": 0}, center=(2.0, 2.0, 3.0)),
        _mapping("ellipsoid0", "ellipsoid", {"radii": [0.2, 0.4, 0.6]}, center=(1.0, 3.0, 3.0)),
    )

    for mapping in mappings:
        _add_dynamic_shape(builder, mapping, wp, body=7, anchor=anchor)

    assert [call[0] for call in builder.calls] == ["cylinder", "cone", "ellipsoid"]
    assert builder.calls[0][1]["body"] == 7
    assert builder.calls[0][1]["half_height"] == 0.8
    assert builder.calls[2][1]["rz"] == 0.6
```

```python
def test_drop_settle_native_world_extents_and_support_height_are_conservative():
    cylinder = _mapping("cylinder0", "cylinder", {"radius": 0.3, "half_height": 0.8, "axis_index": 2})
    cone = _mapping("cone0", "cone", {"radius": 0.4, "half_height": 0.9, "axis_index": 2})
    ellipsoid = _mapping("ellipsoid0", "ellipsoid", {"radii": [0.2, 0.4, 0.6]})
    world_axes = np.eye(3, dtype=float)

    np.testing.assert_allclose(_world_half_extents(cylinder), [0.3, 0.3, 0.8])
    np.testing.assert_allclose(_world_half_extents(cone), [0.4, 0.4, 0.9])
    np.testing.assert_allclose(_world_half_extents(ellipsoid), [0.2, 0.4, 0.6])
    assert _support_extent_z(cylinder, world_axes) == 0.8
    assert _support_extent_z(cone, world_axes) == 0.9
    assert _support_extent_z(ellipsoid, world_axes) == 0.6
```

- [ ] **Step 2: Run RED drop-settle tests**

Run:

```bash
python -m pytest tests/test_newton_drop_settle.py -q -k "native_dynamic_shapes or native_world_extents"
```

Expected: fail because builders/extents do not yet support the new kinds.

- [ ] **Step 3: Implement drop-settle support**

Add builder dispatch for `cylinder`, `cone`, and `ellipsoid`. Add local half-extent helper semantics:

```python
if mapping.kind in {"cylinder", "cone"}:
    radius = float(dimensions["radius"])
    half_height = float(dimensions["half_height"])
    axis_index = int(dimensions.get("axis_index", 2))
    local_extents = np.full(3, radius, dtype=float)
    local_extents[axis_index] = half_height
    return np.abs(axes) @ local_extents
if mapping.kind == "ellipsoid":
    radii = np.asarray(dimensions["radii"], dtype=float)
    return np.abs(axes) @ radii
```

Use the same logic in `_support_extent_z` through `np.abs(world_axes[2, :]) @ local_extents`.

- [ ] **Step 4: Run GREEN drop-settle tests**

Run:

```bash
python -m pytest tests/test_newton_drop_settle.py tests/test_newton_shapes.py -q -k "native or full_mapping"
```

Expected: pass.

- [ ] **Step 5: Commit drop-settle support**

```bash
git add tests/test_newton_drop_settle.py src/primitive_collision_compiler/newton/drop_settle.py
git commit -m "feat: add native primitive drop settle support"
```

### Task 4: Sphere-Rain Builder And Bounds

**Files:**
- Modify: `tests/test_newton_sphere_rain.py`
- Modify: `src/primitive_collision_compiler/newton/sphere_rain.py`

- [ ] **Step 1: Write failing static builder and bounds tests**

Add tests that assert static shape dispatch and package bounds for native shapes.

```python
from primitive_collision_compiler.newton.sphere_rain import _add_static_shape, _package_bounds
from primitive_collision_compiler.reports.schema import NewtonShapeMapping


def test_sphere_rain_builds_newton_native_static_shapes():
    builder = _RecordingBuilder()
    wp = _FakeWarp()

    for mapping in (
        _mapping("cylinder0", "cylinder", {"radius": 0.3, "half_height": 0.8}),
        _mapping("cone0", "cone", {"radius": 0.4, "half_height": 0.9}),
        _mapping("ellipsoid0", "ellipsoid", {"radii": [0.2, 0.4, 0.6]}),
    ):
        _add_static_shape(builder, mapping, wp)

    assert [call[0] for call in builder.calls] == ["cylinder", "cone", "ellipsoid"]
```

```python
def test_sphere_rain_package_bounds_include_native_primitives():
    bounds_min, bounds_max = _package_bounds(
        (
            _mapping("cylinder0", "cylinder", {"radius": 0.3, "half_height": 0.8}, center=(0.0, 0.0, 0.0)),
            _mapping("ellipsoid0", "ellipsoid", {"radii": [0.2, 0.4, 0.6]}, center=(1.0, 0.0, 0.0)),
        )
    )

    np.testing.assert_allclose(bounds_min, [-0.3, -0.4, -0.8])
    np.testing.assert_allclose(bounds_max, [1.2, 0.4, 0.8])
```

- [ ] **Step 2: Run RED sphere-rain tests**

Run:

```bash
python -m pytest tests/test_newton_sphere_rain.py -q -k "native_static_shapes or package_bounds_include_native"
```

Expected: fail because `sphere_rain._add_static_shape` does not support new kinds.

- [ ] **Step 3: Implement sphere-rain support**

Add static builder dispatch matching contact canary:

```python
if mapping.kind == "cylinder":
    return int(builder.add_shape_cylinder(body=-1, xform=xform, radius=float(dimensions["radius"]), half_height=float(dimensions["half_height"])))
if mapping.kind == "cone":
    return int(builder.add_shape_cone(body=-1, xform=xform, radius=float(dimensions["radius"]), half_height=float(dimensions["half_height"])))
if mapping.kind == "ellipsoid":
    rx, ry, rz = (float(value) for value in dimensions["radii"])
    return int(builder.add_shape_ellipsoid(body=-1, xform=xform, rx=rx, ry=ry, rz=rz))
```

- [ ] **Step 4: Run GREEN sphere-rain tests**

Run:

```bash
python -m pytest tests/test_newton_sphere_rain.py tests/test_newton_drop_settle.py -q -k "native or package_bounds or contact_metrics"
```

Expected: pass.

- [ ] **Step 5: Commit sphere-rain support**

```bash
git add tests/test_newton_sphere_rain.py src/primitive_collision_compiler/newton/sphere_rain.py
git commit -m "feat: add native primitive sphere rain support"
```

### Task 5: Documentation And Records

**Files:**
- Add: `docs/records/2026-05-15-newton-native-primitive-bundle.md`
- Modify: `docs/index.md`
- Modify: `docs/reference/cpd-objective-report-alignment.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/records/README.md`

- [ ] **Step 1: Add dated record**

Create `docs/records/2026-05-15-newton-native-primitive-bundle.md` with:

```markdown
# 2026-05-15 Newton Native Primitive Bundle

## Decision

Runtime primitive support follows the Newton-native lane. This slice adds package mapping and
Newton diagnostic construction for `cylinder`, `cone`, and `ellipsoid`, on top of existing
`box`, `sphere`, and `capsule` support.

## Evidence

- Mapping contract covers all six native kinds.
- Contact canary, drop/settle, and sphere-rain builders dispatch the three new native kinds.
- Conservative bounds/support estimates are used for drop/settle and sphere-rain setup.

## Boundaries

This is runtime diagnostic support for Newton-native analytic shapes. It is not full CPD paper
reproduction, benchmark superiority, deployment readiness, or support for `capped_cylinder`,
`frustum`, or `trapezoidal_prism` in Newton runtime.
```

- [ ] **Step 2: Update status docs**

Update roadmap/status wording so it says the native bundle is implemented as diagnostic-path support only. Keep unsupported paper primitives explicit.

- [ ] **Step 3: Run docs validation**

Run:

```bash
python scripts/validate_docs.py
```

Expected: `docs validation passed`.

- [ ] **Step 4: Commit docs**

```bash
git add docs/index.md docs/reference/cpd-objective-report-alignment.md docs/reference/cpd-paper-story-status.md docs/deepdive/evidence-status.md docs/records/README.md docs/records/2026-05-15-newton-native-primitive-bundle.md docs/superpowers/plans/2026-05-15-newton-native-primitive-bundle.md
git commit -m "docs: record newton native primitive bundle"
```

### Task 6: Verification, Runtime Smoke, And Review

**Files:**
- Modify records if the real Newton runtime smoke produces additional confirmed evidence.

- [ ] **Step 1: Run targeted tests**

Run:

```bash
python -m pytest tests/test_newton_shapes.py tests/test_newton_diagnostics.py tests/test_newton_drop_settle.py tests/test_newton_sphere_rain.py -q -k "native or capped_cylinder or mapping_gap or dependency_gap"
```

Expected: pass.

- [ ] **Step 2: Run full tests and static checks**

Run:

```bash
python -m pytest -q
python scripts/validate_docs.py
git diff --check
```

Expected: all pass.

- [ ] **Step 3: Run clean-env Newton smoke if local Newton env is available**

Use the project-standard external conda environment and local Newton source when present:

```bash
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python - <<'PY'
from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.newton.diagnostics import run_newton_contact_smoke
from primitive_collision_compiler.newton.drop_settle import DropSettleOptions, run_newton_drop_settle
from primitive_collision_compiler.newton.sphere_rain import SphereRainOptions, run_newton_sphere_rain

package = CollisionPackage(
    package_id="native_bundle_smoke",
    asset_id="synthetic_native_bundle",
    primitives=(
        PrimitiveSpec(primitive_id="box0", kind="box", dimensions={"half_extents": [0.2, 0.2, 0.2]}),
        PrimitiveSpec(primitive_id="sphere0", kind="sphere", center=(0.7, 0.0, 0.0), dimensions={"radius": 0.2}),
        PrimitiveSpec(primitive_id="capsule0", kind="capsule", center=(1.4, 0.0, 0.0), dimensions={"radius": 0.15, "half_height": 0.3}),
        PrimitiveSpec(primitive_id="cylinder0", kind="cylinder", center=(2.1, 0.0, 0.0), dimensions={"radius": 0.15, "half_height": 0.3}),
        PrimitiveSpec(primitive_id="cone0", kind="cone", center=(2.8, 0.0, 0.0), dimensions={"radius": 0.18, "half_height": 0.3}),
        PrimitiveSpec(primitive_id="ellipsoid0", kind="ellipsoid", center=(3.5, 0.0, 0.0), dimensions={"radii": [0.16, 0.2, 0.24]}),
    ),
)
source_dir = "/cpfs/user/zhuzihou/dev/newton"
print("contact", run_newton_contact_smoke(package, source_dir=source_dir, device="cpu").status)
print("drop", run_newton_drop_settle(package, source_dir=source_dir, device="cpu", options=DropSettleOptions(frames=120, substeps=4)).status)
print("sphere_rain", run_newton_sphere_rain(package, source_dir=source_dir, device="cpu", options=SphereRainOptions(sphere_count_x=2, sphere_count_y=2, frames=120, substeps=4)).status)
PY
```

Expected: use output as evidence. If runtime has a dependency gap, document the actual gap and keep claims at unit/diagnostic-construction level.

- [ ] **Step 4: Multi-agent review**

Dispatch at least two reviewers:

- Spec reviewer: compare implementation against this plan and the native-primitive policy design.
- Code-quality reviewer: inspect validation, builder dispatch, extent math, claim boundaries, and tests.

Fix Critical and Important findings before merging.

- [ ] **Step 5: Merge back to master after verification**

From the main worktree:

```bash
git merge --ff-only newton-native-primitive-bundle-20260515
```

Then re-run:

```bash
python -m pytest -q
python scripts/validate_docs.py
git diff --check
```

Expected: all pass on `master`.
