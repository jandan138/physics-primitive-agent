# CPD Capped-Cylinder Proxy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an opt-in offline `capped_cylinder` geometry proposal proxy and record the reduced
unsupported paper primitive gap for a named objective-report smoke.

**Architecture:** Keep the change inside the CPD-like geometry/report lane. Add the primitive
proxy to `primitives.py`, keep Newton mapping unchanged, add a new offline config, and update docs
to state that this is primitive-vocabulary accounting rather than paper-faithful fitting.

**Tech Stack:** Python dataclasses, NumPy, pytest, YAML config, Markdown records.

---

### Task 1: Primitive Fitting Tests

**Files:**
- Modify: `tests/test_cpd_like_decompose.py`

- [ ] **Step 1: Write failing capped-cylinder proxy test**

Add this helper near the other mesh helpers:

```python
def _long_bar_mesh() -> TriangleMesh:
    return TriangleMesh(
        points=np.array(
            [
                [0.0, -0.1, -0.1],
                [4.0, -0.1, -0.1],
                [4.0, 0.1, -0.1],
                [0.0, 0.1, -0.1],
                [0.0, -0.1, 0.1],
                [4.0, -0.1, 0.1],
                [4.0, 0.1, 0.1],
                [0.0, 0.1, 0.1],
            ]
        ),
        faces=np.array(
            [
                [0, 1, 2],
                [0, 2, 3],
                [4, 5, 6],
                [4, 6, 7],
            ]
        ),
    )
```

Add:

```python
def test_fit_best_primitive_supports_capped_cylinder_proxy():
    fit = fit_best_primitive(_long_bar_mesh(), frozenset({0, 1, 2, 3}), ("capped_cylinder",))

    assert fit.primitive_type == "capped_cylinder"
    assert fit.contains_assigned_points is True
    assert fit.dimensions["radius"] > 0.0
    assert fit.dimensions["half_height"] > 0.0
    assert fit.dimensions["axis_index"] in (0, 1, 2)
    assert fit.dimensions["cap_model"] == "hemisphere_caps"
    assert fit.dimensions["proxy_fit"] == "axis_span_radial_proxy"
    assert fit.volume > 0.0
    assert fit.weighted_volume == fit.volume
    assert fit.unsupported_primitives == ("frustum", "trapezoidal_prism")
```

- [ ] **Step 2: Write failing unsupported-gap accounting test**

Add:

```python
def test_fit_best_primitive_tracks_requested_capped_cylinder_support():
    box_only = fit_best_primitive(_square_mesh(), frozenset({0, 1}), ("box",))
    mixed = fit_best_primitive(_square_mesh(), frozenset({0, 1}), ("box", "capped_cylinder"))

    assert box_only.unsupported_primitives == (
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    )
    assert mixed.unsupported_primitives == ("frustum", "trapezoidal_prism")
```

- [ ] **Step 3: Write failing tie-break test**

Add:

```python
def test_fit_best_primitive_uses_subset_order_to_break_equal_proxy_ties():
    mesh = _long_bar_mesh()

    capped_first = fit_best_primitive(
        mesh,
        frozenset({0, 1, 2, 3}),
        ("capped_cylinder", "capsule"),
    )
    capsule_first = fit_best_primitive(
        mesh,
        frozenset({0, 1, 2, 3}),
        ("capsule", "capped_cylinder"),
    )

    assert capped_first.primitive_type == "capped_cylinder"
    assert capsule_first.primitive_type == "capsule"
```

- [ ] **Step 4: Run primitive tests and confirm RED**

```bash
python -m pytest tests/test_cpd_like_decompose.py -q -k "capped_cylinder or unsupported_gap or equal_proxy"
```

Expected: failures because `capped_cylinder` is not supported and unsupported accounting still
treats it as unsupported.

### Task 2: Primitive Fitting Implementation

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/primitives.py`
- Test: `tests/test_cpd_like_decompose.py`

- [ ] **Step 1: Add vocabulary constants and requested-gap helper**

Update imports:

```python
from dataclasses import dataclass, replace
```

Change constants to:

```python
SUPPORTED_PRIMITIVES = ("box", "sphere", "capsule", "capped_cylinder")
PAPER_SCOPE_PRIMITIVES = ("capped_cylinder", "frustum", "trapezoidal_prism")
UNSUPPORTED_PAPER_PRIMITIVES = PAPER_SCOPE_PRIMITIVES
```

Add:

```python
def _unsupported_paper_primitives_for_subset(requested: tuple[str, ...]) -> tuple[str, ...]:
    requested_set = set(requested)
    supported_set = set(SUPPORTED_PRIMITIVES)
    return tuple(
        primitive
        for primitive in PAPER_SCOPE_PRIMITIVES
        if primitive not in requested_set or primitive not in supported_set
    )
```

- [ ] **Step 2: Preserve primitive subset order for ties**

Replace candidate selection in `fit_best_primitive(...)` with:

```python
    candidates = [
        (
            order,
            _fit_primitive(primitive, points, axes, tuple(sorted(face_ids))),
        )
        for order, primitive in enumerate(supported_requested)
    ]
    best = min(candidates, key=lambda item: (item[1].weighted_volume, item[0]))[1]
    return replace(
        best,
        unsupported_primitives=_unsupported_paper_primitives_for_subset(requested),
    )
```

Remove the old `unsupported_requested` merge-return block. Keep the existing validation that at
least one supported primitive is requested.

- [ ] **Step 3: Add capped-cylinder dispatch and fitter**

Add to `_fit_primitive(...)`:

```python
    if primitive_type == "capped_cylinder":
        return _fit_capped_cylinder(points, axes, source_faces)
```

Add:

```python
def _fit_capped_cylinder(
    points: NDArray[np.float64],
    axes: NDArray[np.float64],
    source_faces: tuple[int, ...],
) -> PrimitiveFit:
    local = points @ axes
    spans = local.max(axis=0) - local.min(axis=0)
    axis_index = int(np.argmax(spans))
    axis = axes[:, axis_index]
    projections = points @ axis
    projection_min = float(projections.min())
    projection_max = float(projections.max())
    segment_center_projection = (projection_min + projection_max) * 0.5
    centroid = points.mean(axis=0)
    perpendicular_center = centroid - axis * float(centroid @ axis)
    center = perpendicular_center + axis * segment_center_projection
    axial_offsets = np.outer(projections - segment_center_projection, axis)
    radial_vectors = points - center - axial_offsets
    radial_distances = np.linalg.norm(radial_vectors, axis=1)
    radius = max(float(radial_distances.max(initial=0.0)), MIN_DIMENSION)
    half_height = max((projection_max - projection_min) * 0.5, 0.0)
    cylinder_length = half_height * 2.0
    volume = float(pi * radius**2 * cylinder_length + (4.0 / 3.0) * pi * radius**3)
    contains = bool(_capsule_contains(points, axis, center, half_height, radius))
    return PrimitiveFit(
        primitive_type="capped_cylinder",
        source_faces=source_faces,
        center=_vector_to_tuple(center),
        axes=_axes_to_tuple(axes),
        dimensions={
            "radius": radius,
            "half_height": half_height,
            "axis_index": axis_index,
            "cap_model": "hemisphere_caps",
            "proxy_fit": "axis_span_radial_proxy",
        },
        volume=volume,
        weighted_volume=volume,
        contains_assigned_points=contains,
    )
```

- [ ] **Step 4: Run primitive tests and confirm GREEN**

```bash
python -m pytest tests/test_cpd_like_decompose.py -q -k "capped_cylinder or unsupported_gap or equal_proxy"
```

Expected: selected tests pass.

### Task 3: Objective, Newton Boundary, And CLI Tests

**Files:**
- Modify: `tests/test_cpd_like_objective.py`
- Modify: `tests/test_newton_shapes.py`
- Modify: `tests/test_cli.py`
- Modify: `tests/test_cpd_like_config.py`
- Create: `configs/experiments/cpd_like_capped_cylinder_proxy.yaml`

- [ ] **Step 1: Write objective gap test**

Add to `tests/test_cpd_like_objective.py`:

```python
def test_objective_report_counts_capped_cylinder_as_opt_in_supported_proxy():
    decomposition = decompose_mesh(
        _square_mesh(),
        max_primitives=1,
        primitive_subset=("capped_cylinder",),
    )

    payload = build_cpd_like_objective_report(
        decomposition,
        asset_id="square_capped_cylinder",
        source_path="tests/generated/square.usda",
        max_source_faces=8,
    ).to_dict()

    assert payload["metrics"]["paper_primitive_gap"]["current_primitive_subset"] == [
        "capped_cylinder"
    ]
    assert payload["metrics"]["paper_primitive_gap"]["unsupported_paper_primitives"] == [
        "frustum",
        "trapezoidal_prism",
    ]
    assert payload["metrics"]["paper_primitive_gap"]["unsupported_paper_primitive_count"] == 2
    assert payload["decomposition"]["primitive_count"] == 1
```

- [ ] **Step 2: Write Newton mapping boundary test**

Add to `tests/test_newton_shapes.py`:

```python
def test_map_package_shapes_keeps_capped_cylinder_as_mapping_gap():
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(
            PrimitiveSpec(
                primitive_id="capped-cylinder0",
                kind="capped_cylinder",
                dimensions={
                    "radius": 0.25,
                    "half_height": 1.0,
                    "axis_index": 0,
                    "cap_model": "hemisphere_caps",
                    "proxy_fit": "axis_span_radial_proxy",
                },
            ),
        ),
    )

    mappings = map_package_shapes(package)

    assert mappings[0].status == "mapping_gap"
    assert "unsupported primitive kind: capped_cylinder" in mappings[0].detail
```

- [ ] **Step 3: Add new offline config**

Create `configs/experiments/cpd_like_capped_cylinder_proxy.yaml`:

```yaml
asset:
  id: grscenes_bed_0a85b986_capped_cylinder_proxy
  path: assets/manifests/cpd_like_smoke_assets.yaml
task:
  primary: collision_proxy_diagnostic
compile:
  method: cpd_like_baseline
  max_primitives: 32
  allowed_fallback:
    - convex_hull
  verify:
    - cpd_like_objective_report
  keep_visual: false
cpd_like:
  paper: Convex Primitive Decomposition for Collision Detection
  asset_manifest: assets/manifests/cpd_like_smoke_assets.yaml
  asset_role: bed_dev_smoke
  primitive_subset:
    - capped_cylinder
  unsupported_primitives:
    - frustum
    - trapezoidal_prism
  max_source_faces: 256
  decomposition_stage: cpd_like_capped_cylinder_proxy
  component_merge: virtual_pairwise
  excess_volume_threshold_fraction: 1.0
  report_merge_trace: summary
  claim_boundary: capped_cylinder_proxy_not_paper_faithful_or_newton_supported
cpd_like_objective:
  objective_version: cpd_paper_aligned_surrogate_v0
  claim_boundary: capped_cylinder_proxy_objective_not_collision_quality_validation
  evidence_level: offline_cpd_like_capped_cylinder_proxy_smoke
  primitive_type_weights:
    capped_cylinder: 1.0
report:
  output_dir: reports/generated/cpd_like_capped_cylinder_proxy
  evidence_level: offline_cpd_like_capped_cylinder_proxy_smoke
```

- [ ] **Step 4: Write config test**

Add to `tests/test_cpd_like_config.py`:

```python
def test_cpd_like_capped_cylinder_proxy_config_is_offline_only():
    config = load_compile_config("configs/experiments/cpd_like_capped_cylinder_proxy.yaml")

    assert config.asset_id == "grscenes_bed_0a85b986_capped_cylinder_proxy"
    assert config.verify == ("cpd_like_objective_report",)
    assert "newton" not in config.protocol
    assert "newton_diagnostic" not in config.protocol
    assert config.protocol["cpd_like"]["primitive_subset"] == ["capped_cylinder"]
    assert config.protocol["cpd_like"]["unsupported_primitives"] == [
        "frustum",
        "trapezoidal_prism",
    ]
    assert config.protocol["cpd_like_objective"]["primitive_type_weights"] == {
        "capped_cylinder": 1.0
    }
```

- [ ] **Step 5: Write CLI objective test**

Add to `tests/test_cli.py` after the objective-report CLI tests:

```python
def test_cli_run_cpd_like_objective_report_accepts_capped_cylinder_proxy(tmp_path, capsys):
    asset_path = tmp_path / "quad.usda"
    _write_mesh_usd(
        asset_path,
        [(0, 0, 0), (2, 0, 0), (2, 0.2, 0), (0, 0.2, 0)],
        [4],
        [0, 1, 2, 3],
    )
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: tiny_capped_cylinder_proxy",
                f"  path: {asset_path}",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "compile:",
                "  method: cpd_like_baseline",
                "  max_primitives: 1",
                "  verify:",
                "    - cpd_like_objective_report",
                "cpd_like:",
                "  primitive_subset:",
                "    - capped_cylinder",
                "  max_source_faces: 8",
                "cpd_like_objective:",
                "  objective_version: cpd_paper_aligned_surrogate_v0",
                "  claim_boundary: capped_cylinder_proxy_objective_not_collision_quality_validation",
                "  evidence_level: offline_cpd_like_capped_cylinder_proxy_smoke",
                "  primitive_type_weights:",
                "    capped_cylinder: 1.0",
            ]
        ),
        encoding="utf-8",
    )

    assert cli.main(["--config", str(config_path), "--run-cpd-like-objective-report"]) == 0

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["stage"] == "cpd_like_offline_objective"
    assert payload["metrics"]["paper_primitive_gap"]["unsupported_paper_primitive_count"] == 2
    assert payload["metrics"]["paper_primitive_gap"]["unsupported_paper_primitives"] == [
        "frustum",
        "trapezoidal_prism",
    ]
    assert payload["decomposition"]["primitive_count"] == 1
    assert captured.err == ""
```

- [ ] **Step 6: Run selected tests and confirm RED**

```bash
python -m pytest tests/test_cpd_like_objective.py tests/test_newton_shapes.py tests/test_cli.py tests/test_cpd_like_config.py -q -k "capped_cylinder"
```

Expected: failures because config and primitive support are not implemented yet.

### Task 4: Objective/Config/Boundary Implementation

**Files:**
- Create: `configs/experiments/cpd_like_capped_cylinder_proxy.yaml`
- Implementation already covered by Task 2.
- Test: `tests/test_cpd_like_objective.py`, `tests/test_newton_shapes.py`, `tests/test_cli.py`,
  `tests/test_cpd_like_config.py`

- [ ] **Step 1: Add offline config**

Create `configs/experiments/cpd_like_capped_cylinder_proxy.yaml` exactly as specified in Task 3.

- [ ] **Step 2: Run selected tests and confirm GREEN**

```bash
python -m pytest tests/test_cpd_like_decompose.py tests/test_cpd_like_objective.py tests/test_newton_shapes.py tests/test_cli.py tests/test_cpd_like_config.py -q -k "capped_cylinder or unsupported_gap or equal_proxy"
```

Expected: selected tests pass.

- [ ] **Step 3: Run the real offline config smoke**

```bash
PYTHONPATH=src python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_capped_cylinder_proxy.yaml --run-cpd-like-objective-report
```

Expected: exit 0, strict JSON, stage `cpd_like_offline_objective`, evidence level
`offline_cpd_like_capped_cylinder_proxy_smoke`, and unsupported paper primitive count `2`.

### Task 5: Documentation And Records

**Files:**
- Create: `docs/records/2026-05-15-cpd-capped-cylinder-proxy.md`
- Modify: `README.md`
- Modify: `docs/index.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/cpd-like-face-merge-explainer.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/cpd-objective-report-alignment.md`
- Modify: `docs/records/README.md`
- Modify: `experiments/registry.yaml`

- [ ] **Step 1: Update canonical claim docs**

Add safe wording:

- "opt-in offline `capped_cylinder` geometry proposal proxy";
- "unsupported paper primitive gap decreases from 3 to 2 in the named opt-in report";
- "primitive-vocabulary accounting for a restricted proposal baseline";
- "no Newton mapping or task-level improvement is claimed for `capped_cylinder`."

Add forbidden wording:

- no "CPD primitive fitting implemented";
- no "paper-faithful capped cylinder support";
- no "Newton supports capped cylinders";
- no "collision quality improved";
- no "benchmark result".

- [ ] **Step 2: Add record**

Create `docs/records/2026-05-15-cpd-capped-cylinder-proxy.md` with:

- config path;
- CLI command;
- result status and unsupported primitive count;
- note that `frustum` and `trapezoidal_prism` remain unsupported;
- note that Newton mapping still reports `mapping_gap` for `capped_cylinder`;
- verification commands;
- claim impact and next action.

- [ ] **Step 3: Update registry**

Add `experiments/registry.yaml` entry:

```yaml
  - id: cpd-like-capped-cylinder-proxy
    status: complete
    config: configs/experiments/cpd_like_capped_cylinder_proxy.yaml
    record: docs/records/2026-05-15-cpd-capped-cylinder-proxy.md
    purpose: >
      Run an opt-in offline capped-cylinder geometry proposal proxy and record the reduced
      unsupported paper primitive vocabulary gap in the CPD-like objective report.
    claims_supported:
      - offline geometry-only capped-cylinder proposal proxy smoke only
      - no Newton support, collision-quality, benchmark, broad asset/task, paper-faithful optimization, or full CPD reproduction claim
```

- [ ] **Step 4: Run doc checks**

```bash
python scripts/validate_docs.py
git diff --check
```

Expected: both pass.

### Task 6: Review, Verification, Commit, Merge

**Files:**
- All changed files.

- [ ] **Step 1: Run targeted tests**

```bash
python -m pytest tests/test_cpd_like_decompose.py tests/test_cpd_like_objective.py tests/test_newton_shapes.py tests/test_cli.py tests/test_cpd_like_config.py -q -k "capped_cylinder or unsupported_gap or equal_proxy"
```

Expected: selected tests pass.

- [ ] **Step 2: Run full tests**

```bash
python -m pytest -q
```

Expected: all tests pass.

- [ ] **Step 3: Request focused agent review**

Ask one reviewer to inspect primitive fitting/schema/CLI behavior and one reviewer to inspect docs
and claim boundaries.

- [ ] **Step 4: Fix Critical/Important/Medium findings**

If review finds issues, fix them, re-run the relevant targeted tests, and request re-review.

- [ ] **Step 5: Commit implementation**

```bash
git add configs/experiments/cpd_like_capped_cylinder_proxy.yaml \
  src/primitive_collision_compiler/baselines/cpd_like/primitives.py \
  tests/test_cpd_like_decompose.py \
  tests/test_cpd_like_objective.py \
  tests/test_newton_shapes.py \
  tests/test_cli.py \
  tests/test_cpd_like_config.py \
  README.md \
  docs/index.md \
  docs/reference/claim-boundaries.md \
  docs/deepdive/evidence-status.md \
  docs/reference/cpd-like-face-merge-explainer.md \
  docs/reference/cpd-paper-story-status.md \
  docs/reference/cpd-objective-report-alignment.md \
  docs/records/README.md \
  docs/records/2026-05-15-cpd-capped-cylinder-proxy.md \
  experiments/registry.yaml \
  docs/superpowers/specs/2026-05-15-cpd-capped-cylinder-proxy-design.md \
  docs/superpowers/plans/2026-05-15-cpd-capped-cylinder-proxy.md
git commit -m "feat: add cpd capped cylinder proxy"
```

## Self-Review

This plan keeps the slice opt-in and offline. It does not add Newton mapping, change completed
configs, claim paper-faithful primitive fitting, or claim collision-quality improvement. It includes
negative Newton mapping coverage and documentation updates for stale current-status wording.
