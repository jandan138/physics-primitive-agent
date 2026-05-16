# CPD Paper OBB/Sphere Fit Faithfulness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the CPD paper offline report's shared CPD-like OBB/sphere candidate rows with
paper-lane OBB/sphere fit-audit rows and advance the next gate to duplicate-vertex preprocessing.

**Architecture:** Keep `cpd_like.primitives` unchanged. Add paper-only OBB/sphere helper functions
inside `cpd_paper.offline`, using the paper's `1e-3` primitive lower clamp, operator eigenbasis
axes, projected point bounds, and OBB-center sphere radius. Preserve offline-only boundaries: no
package generation, no Newton runtime, no real USD, and no benchmark claim.

**Tech Stack:** Python, NumPy, pytest, Markdown docs, YAML registry.

---

### Task 1: RED Tests For Gate Advancement And Paper Rows

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [x] Update `test_cpd_paper_offline_report_failure_labels_point_to_obb_sphere_fit_gap` to expect:

```python
assert report["failure_labels"] == ["paper_duplicate_vertex_preprocessing_missing"]
```

- [x] Update `test_cpd_paper_offline_report_next_gate_is_obb_sphere_fit_audit` to expect:

```python
assert report["next_required_gate"] == "paper_duplicate_vertex_preprocessing_audit"
```

- [x] In `test_cpd_paper_offline_report_covers_first_toy_slice`, update the top-level assertions:

```python
assert report["failure_labels"] == ["paper_duplicate_vertex_preprocessing_missing"]
assert report["next_required_gate"] == "paper_duplicate_vertex_preprocessing_audit"
assert "paper_obb_sphere_fit_faithfulness_audit" in report["paper_faithfulness"][
    "implemented_fixture_scope"
]
```

- [x] Assert the report case set includes `paper_tiny_sphere_clamp`.

- [x] Replace the current single-box OBB surrogate assertions with paper-row assertions:

```python
box = [
    row
    for row in single_box["primitive_fit_audit"]["candidates"]
    if row["paper_primitive"] == "oriented_bounding_box"
][0]
assert box["implementation_status"] == "paper_shaped_offline_fit_audit"
assert box["current_implementation_kind"] == "offline_paper_oriented_bounding_box_fit"
assert box["fit_model"] == "paper_operator_eigenbasis_projected_bounds"
assert box["axis_selection_policy"] == "paper_q_eigenbasis"
assert box["axis_matrix_layout"] == "rows_are_axes"
assert box["primitive_parameter_lower_clamp"] == 1e-3
assert box["newton_runtime_kind"] == "box"
assert box["contains_assigned_points"] is True
assert box["fit_failure_reason"] is None
box_dims = box["dimensions"]
assert box_dims["volume_formula"] == "8*hx*hy*hz"
assert box_dims["lower_bounds"]
assert box_dims["upper_bounds"]
assert box_dims["paper_center_local"]
assert box_dims["paper_center_world"] == box["center"]
assert box_dims["axis_order_policy"] == "descending_abs_q_eigenvalue"
assert box_dims["half_extents"] == box["dimensions"]["half_extents"]
```

- [x] Add explicit OBB formula checks for `paper_single_box`:

```python
axes = box["axes"]
points = single_box_points
local = [
    [sum(point[index] * axis[index] for index in range(3)) for axis in axes]
    for point in points
]
lower = [min(row[index] for row in local) for index in range(3)]
upper = [max(row[index] for row in local) for index in range(3)]
center_local = [(lower[index] + upper[index]) * 0.5 for index in range(3)]
half_extents = [max((upper[index] - lower[index]) * 0.5, 1e-3) for index in range(3)]
center = [
    sum(axes[axis_index][coord] * center_local[axis_index] for axis_index in range(3))
    for coord in range(3)
]
assert all(abs(box_dims["lower_bounds"][index] - lower[index]) < 1e-9 for index in range(3))
assert all(abs(box_dims["upper_bounds"][index] - upper[index]) < 1e-9 for index in range(3))
assert all(abs(box_dims["paper_center_local"][index] - center_local[index]) < 1e-9 for index in range(3))
assert all(abs(box_dims["paper_center_world"][index] - center[index]) < 1e-9 for index in range(3))
assert all(abs(box_dims["half_extents"][index] - half_extents[index]) < 1e-9 for index in range(3))
assert all(abs(box["center"][index] - center[index]) < 1e-9 for index in range(3))
expected_box_volume = 8.0 * half_extents[0] * half_extents[1] * half_extents[2]
assert abs(box["volume"] - expected_box_volume) < 1e-9
```

- [x] Add a helper `_assert_paper_obb_sphere_rows(case, points)` and call it for both
  `paper_single_box` and the non-axis-aligned `paper_quad_face_intake`. The helper must recompute
  projected bounds from the emitted row axes, compare `paper_center_world`, compare half-extents,
  compare OBB volume, compare sphere center to OBB center, and compare sphere radius to
  `max(max_distance, 1e-3)`. Use these quad points:

```python
quad_face_points = [
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [1.0, 1.0, 0.0],
    [0.0, 1.0, 0.0],
]
```

- [x] Add sphere paper-row assertions immediately after the OBB assertions:

```python
sphere = [
    row
    for row in single_box["primitive_fit_audit"]["candidates"]
    if row["paper_primitive"] == "sphere"
][0]
assert sphere["implementation_status"] == "paper_shaped_offline_fit_audit"
assert sphere["current_implementation_kind"] == "offline_paper_sphere_fit"
assert sphere["fit_model"] == "paper_obb_center_max_distance_radius"
assert sphere["axis_selection_policy"] == "paper_obb_center"
assert sphere["primitive_parameter_lower_clamp"] == 1e-3
assert sphere["newton_runtime_kind"] == "sphere"
assert sphere["contains_assigned_points"] is True
assert sphere["fit_failure_reason"] is None
sphere_dims = sphere["dimensions"]
assert sphere_dims["center_source"] == "paper_obb_center"
assert sphere_dims["radius_source"] == "max_distance_from_obb_center_clamped"
assert sphere_dims["volume_formula"] == "4/3*pi*r^3"
assert sphere["center"] == box["center"]
expected_radius = max(
    sqrt(sum((point[index] - box["center"][index]) ** 2 for index in range(3)))
    for point in single_box_points
)
expected_radius = max(expected_radius, 1e-3)
assert abs(sphere_dims["unclamped_radius"] - max(
    sqrt(sum((point[index] - box["center"][index]) ** 2 for index in range(3)))
    for point in single_box_points
)) < 1e-9
assert abs(sphere_dims["radius"] - expected_radius) < 1e-9
assert abs(sphere["volume"] - (4.0 / 3.0) * pi * expected_radius**3) < 1e-9
```

- [x] Add a clamp-path assertion for `paper_tiny_sphere_clamp`:

```python
tiny_sphere = _candidate_by_paper_primitive(
    cases["paper_tiny_sphere_clamp"]["primitive_fit_audit"],
    "sphere",
)
assert tiny_sphere["dimensions"]["unclamped_radius"] < 1e-3
assert tiny_sphere["dimensions"]["radius"] == 1e-3
```

- [x] Assert `operator_audit.merged_group.eigenvector_matrix_layout == "columns_are_eigenvectors"`
  and primitive candidate `axis_matrix_layout == "rows_are_axes"`.

- [x] Add a uniqueness assertion for every primitive fit audit in every case:

```python
for case in cases.values():
    for audit in case["primitive_fit_audits"]:
        paper_primitives = [row["paper_primitive"] for row in audit["candidates"]]
        assert len(paper_primitives) == len(set(paper_primitives))
```

- [x] Strengthen merge-cost and queue-trace regression assertions:

```python
assert cost["left_primitive"] == cost["left_fit_audit"]["selected"]["paper_primitive"]
assert cost["right_primitive"] == cost["right_fit_audit"]["selected"]["paper_primitive"]
assert cost["merged_primitive"] == cost["merged_fit_audit"]["selected"]["paper_primitive"]
for event in events:
    assert event["left_primitive"]
    assert event["right_primitive"]
    assert event["merged_primitive"]
    assert isfinite(event["paper_base_cost"])
    assert isfinite(event["weighted_priority_cost"])
    assert event["queue_key"] == [
        event["weighted_priority_cost"],
        event["paper_base_cost"],
        event["source_faces_left"],
        event["source_faces_right"],
        event["insertion_order"],
    ]
```

- [x] Update `tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json` so it expects
  the new top-level failure label and next gate while preserving the same case list. Also assert the
  emitted JSON for `paper_single_box` contains paper-shaped OBB and sphere rows with clamps `1e-3`.

- [x] Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_failure_labels_point_to_obb_sphere_fit_gap tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_obb_sphere_fit_audit tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Expected: failures for old failure label, old next gate, missing implemented scope entry, and old
OBB/sphere surrogate metadata.

### Task 2: Paper OBB/Sphere Offline Fit Helpers

**Files:**

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [x] Add a paper-lane clamp constant near the existing paper constants:

```python
PAPER_PRIMITIVE_MIN_DIMENSION = 1e-3
```

- [x] Add `_paper_obb_fit(mesh, face_group)` below `_primitive_fit_audit_payload`:

```python
def _paper_obb_fit(
    mesh: TriangleMesh,
    face_group: frozenset[int],
) -> dict[str, object]:
    points = _assigned_points(mesh, face_group)
    axes = _candidate_axes(mesh, face_group)
    local = points @ axes
    lower = local.min(axis=0)
    upper = local.max(axis=0)
    center_local = (lower + upper) * 0.5
    half_extents = np.maximum((upper - lower) * 0.5, PAPER_PRIMITIVE_MIN_DIMENSION)
    center = axes @ center_local
    volume = float(8.0 * np.prod(half_extents))
    contains = bool(np.all(np.abs(local - center_local) <= half_extents + 1e-8))
    return _offline_paper_candidate_payload(
        paper_primitive="oriented_bounding_box",
        current_implementation_kind="offline_paper_oriented_bounding_box_fit",
        fit_model="paper_operator_eigenbasis_projected_bounds",
        axis_selection_policy="paper_q_eigenbasis",
        center=center,
        axes=axes,
        dimensions={
            "lower_bounds": _vector(lower),
            "upper_bounds": _vector(upper),
            "paper_center_local": _vector(center_local),
            "paper_center_world": _vector(center),
            "half_extents": _vector(half_extents),
            "axis_order_policy": "descending_abs_q_eigenvalue",
            "volume_formula": "8*hx*hy*hz",
        },
        volume=volume,
        contains_assigned_points=contains,
        newton_runtime_kind="box",
        primitive_parameter_lower_clamp=PAPER_PRIMITIVE_MIN_DIMENSION,
    )
```

- [x] Extend `_offline_paper_candidate_payload(...)` with an optional
  `primitive_parameter_lower_clamp: float = MIN_DIMENSION` parameter and use that value in the
  emitted row:

```python
"primitive_parameter_lower_clamp": primitive_parameter_lower_clamp,
```

- [x] Add `_paper_sphere_fit(mesh, face_group, obb_row)` below `_paper_obb_fit`:

```python
def _paper_sphere_fit(
    mesh: TriangleMesh,
    face_group: frozenset[int],
    obb_row: dict[str, object],
) -> dict[str, object]:
    points = _assigned_points(mesh, face_group)
    center = np.asarray(obb_row["center"], dtype=np.float64)
    axes = np.asarray(obb_row["axes"], dtype=np.float64).T
    distances = np.linalg.norm(points - center, axis=1)
    unclamped_radius = float(distances.max(initial=0.0))
    radius = max(unclamped_radius, PAPER_PRIMITIVE_MIN_DIMENSION)
    volume = float((4.0 / 3.0) * pi * radius**3)
    contains = bool(np.all(distances <= radius + 1e-8))
    return _offline_paper_candidate_payload(
        paper_primitive="sphere",
        current_implementation_kind="offline_paper_sphere_fit",
        fit_model="paper_obb_center_max_distance_radius",
        axis_selection_policy="paper_obb_center",
        center=center,
        axes=axes,
        dimensions={
            "radius": radius,
            "center_source": "paper_obb_center",
            "radius_source": "max_distance_from_obb_center_clamped",
            "unclamped_radius": unclamped_radius,
            "volume_formula": "4/3*pi*r^3",
        },
        volume=volume,
        contains_assigned_points=contains,
        newton_runtime_kind="sphere",
        primitive_parameter_lower_clamp=PAPER_PRIMITIVE_MIN_DIMENSION,
    )
```

- [x] Replace the first two candidate rows in `_primitive_fit_audit_payload`:

```python
obb_row = _paper_obb_fit(mesh, face_group)
rows = [
    obb_row,
    _paper_sphere_fit(mesh, face_group, obb_row),
]
```

Then keep appending capsule, capped cylinder, frustum, and trapezoidal prism rows in the existing
order. Do not append the new OBB/sphere rows after the shared CPD-like rows; the report must contain
only one candidate row per `paper_primitive`.

- [x] Advance report labels in `build_cpd_paper_offline_report()`:

```python
missing_before_paper_faithful = [
    "paper_duplicate_vertex_preprocessing",
]
...
"next_required_gate": "paper_duplicate_vertex_preprocessing_audit",
...
"paper_obb_sphere_fit_faithfulness_audit",
```

- [x] Run the RED command from Task 1 again.

Expected: all selected tests pass.

### Task 3: Docs, Registry, And Record

**Files:**

- Modify: `docs/index.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/records/README.md`
- Modify: `experiments/registry.yaml`
- Create: `docs/records/2026-05-16-cpd-paper-obb-sphere-fit-faithfulness.md`

- [x] Update current-status wording to say OBB/sphere are now paper-shaped offline fit-audit rows
  for named toy fixtures.
- [x] Keep `status: partial` and `paper_faithful_offline_supported: false`.
- [x] Add `paper_duplicate_vertex_preprocessing_missing` as the current failure label.
- [x] Make `paper_duplicate_vertex_preprocessing_audit` the next gate.
- [x] Add a registry entry:

```yaml
- id: cpd-paper-obb-sphere-fit-faithfulness
  status: complete
  command: PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report
  record: docs/records/2026-05-16-cpd-paper-obb-sphere-fit-faithfulness.md
```

Include claims limited to fixture-scoped offline OBB/sphere fit audit only, with explicit no
`paper_faithful_offline`, full CPD reproduction, Newton runtime, package generation, real-USD,
collision-quality, benchmark, deployment, or safety-certification claim.

- [x] Create the dated record with:
  - status `Complete`;
  - implementation summary;
  - RED/GREEN focused pytest command;
  - CLI smoke summary;
  - full verification commands;
  - multi-agent review notes;
  - claim impact;
  - next action `paper_duplicate_vertex_preprocessing_audit`.

### Task 4: Verification And Multi-Agent Review

- [x] Run focused pytest:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cli.py::test_cli_run_cpd_paper_offline_report_rejects_nonfinite_json -q
```

- [x] Run CLI smoke:

```bash
python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report
```

- [x] Run full verification:

```bash
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

- [x] Request multi-agent review for:
  - paper alignment of OBB and sphere formulas;
  - test coverage and report schema clarity;
  - docs and claim-boundary consistency.

- [x] Fix all Critical and Important review findings, then rerun the relevant focused tests and
  final verification commands.

### Task 5: Commit And Push

- [x] Commit the spec and plan checkpoint:

```bash
git add docs/superpowers/specs/2026-05-16-cpd-paper-obb-sphere-fit-faithfulness-design.md docs/superpowers/plans/2026-05-16-cpd-paper-obb-sphere-fit-faithfulness.md
git commit -m "docs: plan CPD paper OBB sphere fit audit"
```

- [x] Commit implementation after review and verification:

```bash
git add src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cpd_paper_offline.py tests/test_cli.py docs/index.md docs/reference/claim-boundaries.md docs/reference/cpd-paper-reproduction-gap-matrix.md docs/reference/cpd-paper-faithful-offline-lane-spec.md docs/reference/cpd-paper-story-status.md docs/records/README.md docs/records/2026-05-16-cpd-paper-obb-sphere-fit-faithfulness.md experiments/registry.yaml docs/superpowers/plans/2026-05-16-cpd-paper-obb-sphere-fit-faithfulness.md
git commit -m "feat: audit CPD paper OBB sphere fitting"
```

- [x] Push `main`:

```bash
git push
```

- [x] Confirm worktree is clean:

```bash
git status --short
```
