# CPD Paper Fixture Breadth Batch B Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Batch B primitive-fit breadth fixtures to the partial offline
`cpd_paper_offline_report`.

**Architecture:** Keep the lane command-only and offline-only. Add six synthetic toy cases under
`cpd_paper.offline` that exercise all six paper primitive names in primitive-fit audit rows:
oriented bounding box, sphere, capsule, capped cylinder, frustum, and trapezoidal prism. Reuse the
existing candidate payload helpers, add fixture-level metadata only where it makes the report easier
to audit, and keep Newton, package generation, real USD, and benchmark work out of scope.

**Tech Stack:** Python, NumPy, pytest, Markdown docs, YAML registry.

---

### Task 1: RED Tests For Batch B Report Surface

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] Add a failing offline-report test named
  `test_cpd_paper_offline_report_records_fixture_breadth_batch_b`.

```python
def test_cpd_paper_offline_report_records_fixture_breadth_batch_b():
    report = build_cpd_paper_offline_report()
    cases = {case["case_id"]: case for case in report["cases"]}

    expected_case_ids = {
        "paper_rotated_box_fit",
        "paper_offset_sphere_fit",
        "paper_off_axis_capsule_fit",
        "paper_flat_capped_cylinder_axis_fit",
        "paper_tapered_frustum_fit",
        "paper_asymmetric_trapezoid_fit",
    }
    assert expected_case_ids.issubset(cases)
    for case_id in expected_case_ids:
        case = cases[case_id]
        assert case["fixture_breadth_batch"] == "paper_fixture_breadth_batch_b"
        assert case["package_generation_triggered"] is False
        assert case["newton_runtime_triggered"] is False
        assert case["real_usd_triggered"] is False
        assert case["benchmark_triggered"] is False

    rotated_box = cases["paper_rotated_box_fit"]
    obb = _candidate_by_paper_primitive(
        rotated_box["primitive_fit_audit"],
        "oriented_bounding_box",
    )
    assert obb["contains_assigned_points"] is True
    assert _candidate_has_common_fit_fields(obb)
    assert obb["dimensions"]["volume_formula"] == "8*hx*hy*hz"
    assert obb["dimensions"]["axis_order_policy"] == "descending_abs_q_eigenvalue"
    assert obb["dimensions"]["lower_bounds"]
    assert obb["dimensions"]["upper_bounds"]
    assert obb["dimensions"]["paper_center_local"]
    assert obb["dimensions"]["paper_center_world"] == obb["center"]
    assert obb["dimensions"]["half_extents"]
    assert obb["newton_runtime_kind"] == "box"
    assert _axes_are_orthonormal(obb["axes"])
    assert not _axes_are_world_aligned(obb["axes"])

    offset_sphere = cases["paper_offset_sphere_fit"]
    sphere = _candidate_by_paper_primitive(
        offset_sphere["primitive_fit_audit"],
        "sphere",
    )
    assert sphere["contains_assigned_points"] is True
    assert _candidate_has_common_fit_fields(sphere)
    assert sphere["dimensions"]["center_source"] == "paper_obb_center"
    assert sphere["dimensions"]["radius"] >= 1e-3
    assert sphere["dimensions"]["unclamped_radius"] > 0.0
    assert sphere["dimensions"]["volume_formula"] == "4/3*pi*r^3"
    assert sphere["dimensions"]["fixture_center_relation"] == "differs_from_point_centroid"
    assert sphere["dimensions"]["center_differs_from_point_centroid"] is True
    assert sphere["dimensions"]["center_centroid_distance"] > 1e-3
    assert sphere["newton_runtime_kind"] == "sphere"

    off_axis_capsule = cases["paper_off_axis_capsule_fit"]
    capsule = _candidate_by_paper_primitive(
        off_axis_capsule["primitive_fit_audit"],
        "capsule",
    )
    assert capsule["contains_assigned_points"] is True
    assert _candidate_has_common_fit_fields(capsule)
    assert capsule["dimensions"]["axis_selection_policy"] == "min_volume_capsule_axis"
    assert len(capsule["dimensions"]["paper_capsule_axis_candidates"]) == 3
    assert capsule["dimensions"]["height"] > 0.0
    assert capsule["dimensions"]["radius"] > 0.0
    assert not _axis_is_world_basis(capsule["axes"][capsule["dimensions"]["selected_axis_index"]])

    flat_cylinder = cases["paper_flat_capped_cylinder_axis_fit"]
    capped = _candidate_by_paper_primitive(
        flat_cylinder["primitive_fit_audit"],
        "capped_cylinder",
    )
    assert capped["contains_assigned_points"] is True
    assert _candidate_has_common_fit_fields(capped)
    assert capped["newton_runtime_kind"] == "offline_only_unmapped"
    assert capped["dimensions"]["cap_model"] == "flat_caps"
    assert capped["dimensions"]["volume_formula"] == "pi*r^2*h"
    assert len(capped["dimensions"]["flat_cylinder_axis_candidates"]) == 3
    assert capped["dimensions"]["radius"] > 0.0
    assert capped["dimensions"]["height"] > 0.0
    assert not _axis_is_world_basis(capped["axes"][capped["dimensions"]["selected_axis_index"]])

    tapered = cases["paper_tapered_frustum_fit"]
    frustum = _candidate_by_paper_primitive(
        tapered["primitive_fit_audit"],
        "frustum",
    )
    assert frustum["contains_assigned_points"] is True
    assert _candidate_has_common_fit_fields(frustum)
    assert frustum["newton_runtime_kind"] == "offline_only_unmapped"
    assert abs(frustum["dimensions"]["top_radius"] - frustum["dimensions"]["bottom_radius"]) > 0.05
    assert frustum["dimensions"]["height"] > 0.0
    assert frustum["dimensions"]["top_center"]
    assert frustum["dimensions"]["bottom_center"]
    assert frustum["dimensions"]["volume_formula"] == "pi*h/3*(rt^2 + rt*rb + rb^2)"

    trapezoid = cases["paper_asymmetric_trapezoid_fit"]
    prism = _candidate_by_paper_primitive(
        trapezoid["primitive_fit_audit"],
        "trapezoidal_prism",
    )
    assert prism["contains_assigned_points"] is True
    assert _candidate_has_common_fit_fields(prism)
    assert prism["newton_runtime_kind"] == "offline_only_unmapped"
    assert prism["dimensions"]["axis_order_attempt_count"] == 6
    assert len(prism["dimensions"]["axis_order_attempts"]) == 6
    assert prism["dimensions"]["axis_order"]
    assert prism["dimensions"]["h_x"] > 0.0
    assert prism["dimensions"]["h_y"] > 0.0
    assert prism["dimensions"]["h_zt"] > 0.0
    assert prism["dimensions"]["h_zb"] > 0.0
    assert prism["dimensions"]["volume_formula"] == "4*h_x*h_y*(h_zt + h_zb)"
```

- [ ] Add small numeric helpers in the test file:

```python
def _axes_are_orthonormal(axes):
    for axis in axes:
        length = sum(value * value for value in axis) ** 0.5
        assert abs(length - 1.0) < 1e-9
    for left_index in range(3):
        for right_index in range(left_index + 1, 3):
            dot = sum(
                axes[left_index][coord] * axes[right_index][coord]
                for coord in range(3)
            )
            assert abs(dot) < 1e-9
    return True


def _axes_are_world_aligned(axes):
    return all(_axis_is_world_basis(axis) for axis in axes)


def _axis_is_world_basis(axis):
    abs_values = [abs(value) for value in axis]
    max_index = max(range(3), key=lambda index: abs_values[index])
    return (
        abs(abs_values[max_index] - 1.0) < 1e-9
        and all(abs_values[index] < 1e-9 for index in range(3) if index != max_index)
    )


def _candidate_has_common_fit_fields(row):
    assert row["paper_primitive"]
    assert row["current_implementation_kind"]
    assert row["implementation_status"] == "paper_shaped_offline_fit_audit"
    assert row["fit_model"]
    assert row["axis_selection_policy"]
    assert row["center"]
    assert row["axes"]
    assert row["dimensions"]
    assert row["volume"] > 0.0
    assert row["paper_weight"] > 0.0
    assert row["weighted_volume"] > 0.0
    assert "contains_assigned_points" in row
    assert "fit_failure_reason" in row
    return True
```

- [ ] Update `test_cpd_paper_offline_report_next_gate_is_fixture_breadth_batch_b` to expect the
  next gate after Batch B:

```python
assert report["next_required_gate"] == "paper_fixture_breadth_batch_c"
```

- [ ] Update `test_cpd_paper_offline_report_covers_first_toy_slice` so it expects
  `paper_fixture_breadth_batch_c`, includes the six Batch B case ids, updates
  `EXPECTED_SCOPE_AUDIT_ROWS` for the revised `primitive_vocabulary_and_fit` evidence text, and
  asserts the implemented fixture scope contains:

```python
"paper_fixture_breadth_batch_b_primitive_fit"
```

- [ ] Run the RED command and confirm it fails because the Batch B cases and next gate are absent:

```bash
python -m pytest \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_batch_b \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_fixture_breadth_batch_b \
  tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json \
  -q
```

Expected: fail with missing Batch B case ids and current gate
`paper_fixture_breadth_batch_b`.

### Task 2: Implement Batch B Fixtures

**Files:**

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] Update `tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json` so it expects
  `paper_fixture_breadth_batch_c`, checks all six Batch B ids are present, and avoids depending on
  their exact insertion order unless the implementation deliberately appends them in one fixed
  place.

- [ ] Add small mesh helpers after the existing toy mesh helpers. The helpers below are
  deterministic, finite, non-degenerate, and synthetic. The offset sphere fixture deliberately
  includes an interior audit vertex referenced by a triangle so the OBB bounds remain corner-driven
  while the point centroid shifts away from the OBB center.

```python
def _rotate_z_then_x(
    point: tuple[float, float, float],
    *,
    z_radians: float,
    x_radians: float,
) -> tuple[float, float, float]:
    x, y, z = point
    cos_z = float(np.cos(z_radians))
    sin_z = float(np.sin(z_radians))
    z_rotated = (cos_z * x - sin_z * y, sin_z * x + cos_z * y, z)
    cos_x = float(np.cos(x_radians))
    sin_x = float(np.sin(x_radians))
    return (
        z_rotated[0],
        cos_x * z_rotated[1] - sin_x * z_rotated[2],
        sin_x * z_rotated[1] + cos_x * z_rotated[2],
    )


def _cuboid_points(
    *,
    center: tuple[float, float, float],
    half_extents: tuple[float, float, float],
) -> tuple[tuple[float, float, float], ...]:
    cx, cy, cz = center
    hx, hy, hz = half_extents
    return (
        (cx - hx, cy - hy, cz - hz),
        (cx + hx, cy - hy, cz - hz),
        (cx + hx, cy + hy, cz - hz),
        (cx - hx, cy + hy, cz - hz),
        (cx - hx, cy - hy, cz + hz),
        (cx + hx, cy - hy, cz + hz),
        (cx + hx, cy + hy, cz + hz),
        (cx - hx, cy + hy, cz + hz),
    )


def _box_surface_mesh_from_points(
    points: tuple[tuple[float, float, float], ...],
) -> TriangleMesh:
    return TriangleMesh(
        points=np.asarray(points, dtype=np.float64),
        faces=np.asarray(
            [
                (0, 1, 2),
                (0, 2, 3),
                (4, 6, 5),
                (4, 7, 6),
                (0, 4, 5),
                (0, 5, 1),
                (1, 5, 6),
                (1, 6, 2),
                (2, 6, 7),
                (2, 7, 3),
                (3, 7, 4),
                (3, 4, 0),
            ],
            dtype=np.int64,
        ),
    )


def _paper_rotated_box_fit_mesh() -> TriangleMesh:
    base = _cuboid_points(center=(0.2, -0.3, 0.4), half_extents=(0.9, 0.35, 0.2))
    rotated = [_rotate_z_then_x(point, z_radians=0.6, x_radians=0.35) for point in base]
    return _box_surface_mesh_from_points(tuple(rotated))


def _paper_offset_sphere_fit_mesh() -> TriangleMesh:
    base = _cuboid_points(center=(1.1, -0.4, 0.3), half_extents=(0.75, 0.25, 0.18))
    rotated = [_rotate_z_then_x(point, z_radians=0.35, x_radians=-0.25) for point in base]
    interior = _rotate_z_then_x((1.45, -0.28, 0.34), z_radians=0.35, x_radians=-0.25)
    return TriangleMesh(
        points=np.asarray(tuple(rotated) + (interior,), dtype=np.float64),
        faces=np.asarray(
            [
                (0, 1, 2),
                (0, 2, 3),
                (4, 6, 5),
                (4, 7, 6),
                (0, 4, 5),
                (0, 5, 1),
                (1, 5, 6),
                (1, 6, 2),
                (2, 6, 7),
                (2, 7, 3),
                (3, 7, 4),
                (3, 4, 0),
                (0, 1, 8),
            ],
            dtype=np.int64,
        ),
    )


def _paper_off_axis_capsule_fit_mesh() -> TriangleMesh:
    base = _cuboid_points(center=(0.0, 0.0, 0.0), half_extents=(1.6, 0.18, 0.18))
    rotated = [_rotate_z_then_x(point, z_radians=0.7, x_radians=0.45) for point in base]
    return _box_surface_mesh_from_points(tuple(rotated))


def _paper_flat_capped_cylinder_axis_fit_mesh() -> TriangleMesh:
    base = _cuboid_points(center=(-0.2, 0.1, 0.0), half_extents=(0.28, 0.28, 1.1))
    rotated = [_rotate_z_then_x(point, z_radians=-0.55, x_radians=0.4) for point in base]
    return _box_surface_mesh_from_points(tuple(rotated))


def _paper_tapered_frustum_fit_mesh() -> TriangleMesh:
    bottom = [(-1.0, -0.65, -1.8), (1.0, -0.65, -1.8), (1.0, 0.65, -1.8), (-1.0, 0.65, -1.8)]
    top = [(-0.22, -0.14, 1.8), (0.22, -0.14, 1.8), (0.22, 0.14, 1.8), (-0.22, 0.14, 1.8)]
    rotated = [_rotate_z_then_x(point, z_radians=0.45, x_radians=0.25) for point in bottom + top]
    return _box_surface_mesh_from_points(tuple(rotated))


def _paper_asymmetric_trapezoid_fit_mesh() -> TriangleMesh:
    points = (
        (-0.9, -0.5, -0.35),
        (0.9, -0.5, -0.25),
        (0.65, 0.5, -0.12),
        (-0.55, 0.5, -0.28),
        (-0.45, -0.5, 0.62),
        (0.5, -0.5, 0.48),
        (0.35, 0.5, 0.22),
        (-0.25, 0.5, 0.52),
    )
    rotated = [_rotate_z_then_x(point, z_radians=-0.25, x_radians=0.3) for point in points]
    return _box_surface_mesh_from_points(tuple(rotated))
```

- [ ] Add the six `_PaperToyCase` rows after Batch A cases or directly before them if that keeps
  the fixture story easier to scan:

```python
_PaperToyCase(
    case_id="paper_rotated_box_fit",
    description="Batch B rotated cuboid fixture for non-identity paper OBB axes",
    mesh=_paper_rotated_box_fit_mesh(),
    face_groups=(frozenset(range(12)),),
    fixture_breadth_batch="paper_fixture_breadth_batch_b",
),
_PaperToyCase(
    case_id="paper_offset_sphere_fit",
    description="Batch B offset cuboid fixture for OBB-centered sphere audit",
    mesh=_paper_offset_sphere_fit_mesh(),
    face_groups=(frozenset(range(13)),),
    fixture_breadth_batch="paper_fixture_breadth_batch_b",
),
_PaperToyCase(
    case_id="paper_off_axis_capsule_fit",
    description="Batch B elongated off-axis fixture for capsule axis audit",
    mesh=_paper_off_axis_capsule_fit_mesh(),
    face_groups=(frozenset(range(12)),),
    fixture_breadth_batch="paper_fixture_breadth_batch_b",
),
_PaperToyCase(
    case_id="paper_flat_capped_cylinder_axis_fit",
    description="Batch B off-axis flat-capped-cylinder primitive-fit audit",
    mesh=_paper_flat_capped_cylinder_axis_fit_mesh(),
    face_groups=(frozenset(range(12)),),
    fixture_breadth_batch="paper_fixture_breadth_batch_b",
),
_PaperToyCase(
    case_id="paper_tapered_frustum_fit",
    description="Batch B tapered fixture for unequal frustum radii audit",
    mesh=_paper_tapered_frustum_fit_mesh(),
    face_groups=(frozenset(range(12)),),
    fixture_breadth_batch="paper_fixture_breadth_batch_b",
),
_PaperToyCase(
    case_id="paper_asymmetric_trapezoid_fit",
    description="Batch B asymmetric wedge fixture for trapezoidal-prism axis-order audit",
    mesh=_paper_asymmetric_trapezoid_fit_mesh(),
    face_groups=(frozenset(range(12)),),
    fixture_breadth_batch="paper_fixture_breadth_batch_b",
),
```

- [ ] Add fixture-specific metadata inside existing candidate payload helpers only where tests need
  it. The expected metadata additions are:

```python
sphere["dimensions"]["center_differs_from_point_centroid"]
sphere["dimensions"]["fixture_center_relation"]
sphere["dimensions"]["center_centroid_distance"]
```

These fields should be computed generically from assigned points and OBB center. Do not add
case-id branching unless there is no cleaner way. Compute
`center_differs_from_point_centroid` from `center_centroid_distance > 1e-3`, not from direct float
inequality.

- [ ] Update `build_cpd_paper_offline_report()`:

```python
"next_required_gate": "paper_fixture_breadth_batch_c"
```

and append to `implemented_fixture_scope`:

```python
"paper_fixture_breadth_batch_b_primitive_fit"
```

- [ ] Update `_paper_faithful_offline_scope_criteria()` so the
  `primitive_vocabulary_and_fit` row mentions the six Batch B fixtures in `current_evidence`.
  Keep the row partial/fixture-scoped rather than flipping the whole report to
  `paper_faithful_offline`.

- [ ] Run the GREEN command:

```bash
python -m pytest \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_batch_b \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_fixture_breadth_batch_b \
  tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json \
  -q
```

Expected: pass.

### Task 3: Update Durable Docs And Registry

**Files:**

- Modify: `docs/index.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- Modify: `docs/records/README.md`
- Create: `docs/records/2026-05-16-cpd-paper-fixture-breadth-batch-b.md`
- Modify: `experiments/registry.yaml`

- [ ] Update canonical docs to say Batch B is implemented and the next gate is
  `paper_fixture_breadth_batch_c`.

- [ ] Keep all claims narrow:

```text
synthetic offline primitive-fit fixture breadth only
not paper_faithful_offline
not full CPD reproduction
not package generation
not Newton runtime support
not real-USD evidence
not benchmark evidence
not collision-quality validation
not deployment readiness or safety certification
```

- [ ] Add a dated record with:

```markdown
# 2026-05-16 CPD Paper Fixture Breadth Batch B

## Date

2026-05-16

## Status

In progress

## Changes

- Added six Batch B primitive-fit breadth fixtures to the partial offline
  `cpd_paper_offline_report`.
- Advanced `next_required_gate` to `paper_fixture_breadth_batch_c`.
- Kept package generation, Newton runtime, real USD, and benchmark work out of scope.

## Verification

- RED command: pending.
- GREEN command: pending.
- Focused verification: pending.
- CLI smoke and inspected JSON facts: pending.
- Full tests: pending.
- Docs validation: pending.
- Site-claim validation: pending.
- Whitespace check: pending.

## Multi-Agent Review

- Pending.

## Fixture Scope

- Synthetic toy fixtures only.
- Primitive-fit audit rows only.
- No package generation, Newton runtime, real USD, benchmark, deployment, or safety-certification
  evidence.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `docs/index.md`
- `docs/deepdive/evidence-status.md`
- `docs/reference/claim-boundaries.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- `docs/records/README.md`
- `docs/records/2026-05-16-cpd-paper-fixture-breadth-batch-b.md`
- `experiments/registry.yaml`

## Claim Impact

- Supports only partial, fixture-scoped, command-only Batch B primitive-fit breadth accounting.
- Does not support `paper_faithful_offline`, full CPD reproduction, package generation, Newton
  runtime support, real-USD evidence, benchmark evidence, collision-quality validation, deployment
  readiness, or safety certification.

## Next Action

- Proceed to `paper_fixture_breadth_batch_c`.
```

- [ ] Add `docs/records/2026-05-16-cpd-paper-fixture-breadth-batch-b.md` to the current record
  index in `docs/records/README.md`.

- [ ] Keep the record `Status` as `In progress` while verification or multi-agent review entries
  are pending. Do not add the final `complete` registry entry while the record is still
  `In progress`.

### Task 4: Multi-Agent Review And Final Verification

**Files:**

- Review the full diff.

- [ ] Dispatch at least three reviewers:

```text
1. implementation reviewer: code/report semantics and source-face/runtime boundaries
2. docs/claim reviewer: canonical docs, DeepDive wording, claim-boundary consistency
3. reproducibility reviewer: registry, records, commands, validators, final git state
```

- [ ] Fix Critical and Important findings. If a reviewer is wrong, document the technical reason
  and keep evidence.

- [ ] Run focused tests:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cli.py::test_cli_run_cpd_paper_offline_report_rejects_nonfinite_json -q
```

- [ ] Run the CLI smoke:

```bash
python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report
```

Expected facts to inspect in JSON:

```text
next_required_gate == paper_fixture_breadth_batch_c
implemented_fixture_scope contains paper_fixture_breadth_batch_b_primitive_fit
cases contain all six Batch B ids
package_generation_triggered/newton_runtime_triggered/real_usd_triggered/benchmark_triggered are false
```

- [ ] Run full verification:

```bash
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

- [ ] Update `docs/records/2026-05-16-cpd-paper-fixture-breadth-batch-b.md` with exact command
  results, inspected CLI JSON facts, review outcomes, and the final `Complete` status.

- [ ] After the record is `Complete`, add the final registry entry:

```yaml
- id: cpd-paper-fixture-breadth-batch-b
  status: complete
  record: docs/records/2026-05-16-cpd-paper-fixture-breadth-batch-b.md
  command: PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report
  purpose: >
    Extend the command-only partial offline CPD paper-lane audit with Batch B primitive-fit
    fixture breadth for all six paper primitive names.
  claims_supported:
    - records synthetic offline primitive-fit fixture breadth for OBB, sphere, capsule, capped
      cylinder, frustum, and trapezoidal prism rows
    - records next_required_gate paper_fixture_breadth_batch_c
    - no package generation, Newton runtime support, real-USD evidence, benchmark evidence,
      collision-quality validation, paper-faithful optimization, or full CPD reproduction claim
```

- [ ] Commit and push:

```bash
git add src/primitive_collision_compiler/baselines/cpd_paper/offline.py \
  tests/test_cpd_paper_offline.py tests/test_cli.py docs/index.md \
  docs/deepdive/evidence-status.md docs/reference/claim-boundaries.md \
  docs/reference/cpd-paper-reproduction-gap-matrix.md \
  docs/reference/cpd-paper-faithful-offline-lane-spec.md \
  docs/reference/cpd-paper-story-status.md \
  docs/reference/cpd-paper-fixture-breadth-expansion-plan.md \
  docs/records/README.md docs/records/2026-05-16-cpd-paper-fixture-breadth-batch-b.md \
  experiments/registry.yaml docs/superpowers/plans/2026-05-16-cpd-paper-fixture-breadth-batch-b.md
git commit -m "feat: add CPD paper fixture breadth batch B"
git push
```

## Self-Review Checklist

- [ ] The plan covers exactly the six Batch B fixture ids from
  `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`.
- [ ] The plan keeps the lane partial and offline-only.
- [ ] The plan does not add Newton runtime support, package generation, real USD, benchmark work, or
  collision-quality claims.
- [ ] The plan includes RED, GREEN, docs, registry, multi-agent review, full verification, and push
  steps.
