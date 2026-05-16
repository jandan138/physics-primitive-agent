# CPD Paper Primitive Fit Engine Generalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an offline report-only Batch B primitive-fit engine generalization payload and move
the current CPD paper offline gate to Batch C.

**Architecture:** Reuse the existing `_primitive_fit_audit_payload()` as the primitive-fit engine.
Add a small generated-probe matrix outside `_paper_toy_cases()` and summarize it in a new top-level
report payload. Keep all runtime, package, real-USD, and benchmark triggers false.

**Tech Stack:** Python, pytest, Markdown records, YAML experiment registry, existing
`primitive_collision_compiler.baselines.cpd_paper.offline` helpers.

---

## Files

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`
- Modify: `README.md`
- Modify: `docs/index.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/records/README.md`
- Modify: `experiments/registry.yaml`
- Create: `docs/records/2026-05-16-cpd-paper-generalization-batch-b-primitive-fit-engine.md`

## Task 1: RED Tests For Batch B Gate Closure

- [ ] Update `tests/test_cpd_paper_offline.py` constants:

```python
EXPECTED_CLOSED_GENERALIZATION_GATES = [
    "paper_generalization_batch_a_source_policy",
    "paper_generalization_batch_b_primitive_fit_engine",
]
EXPECTED_GENERALIZATION_GATES = [
    "paper_generalization_batch_c_search_engine",
    "paper_generalization_batch_d_postprocess_policy",
    "paper_generalization_batch_e_package_boundary_readiness",
]
```

- [ ] Update tests that currently expect Batch B as the next gate so they expect:

```python
assert report["next_required_gate"] == "paper_generalization_batch_c_search_engine"
assert report["failure_labels"] == [
    "paper_generalization_batch_c_search_engine_missing",
    "paper_generalization_batch_d_postprocess_policy_missing",
    "paper_generalization_batch_e_package_boundary_readiness_missing",
]
```

- [ ] Add `test_cpd_paper_offline_report_records_primitive_fit_engine_generalization_gate`.
It must assert:

```python
payload = report["paper_generalization_batch_b_primitive_fit_engine"]
assert payload["gate_status"] == "implemented_offline_report_only_partial"
assert payload["closed_gate"] == "paper_generalization_batch_b_primitive_fit_engine"
assert payload["next_required_gate"] == "paper_generalization_batch_c_search_engine"
assert payload["paper_faithful_offline_allowed"] is False
assert payload["package_generation_triggered"] is False
assert payload["newton_runtime_triggered"] is False
assert payload["real_usd_triggered"] is False
assert payload["benchmark_triggered"] is False
```

- [ ] Add assertions that the new `primitive_family_matrix`:

```python
assert len(payload["primitive_family_matrix"]) == 6
for row in payload["primitive_family_matrix"]:
    assert row["candidate_row_count"] == 6
    assert row["candidate_order"] == [
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
    assert row["missing_paper_primitives"] == []
    assert row["contains_assigned_points"] is True
    assert row["finite_numeric_fields"] is True
```

- [ ] Add CLI assertions in `tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json`
that Batch B payload exists, Batch B missing label is absent, and Batch C is the next gate.

- [ ] Run RED commands:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_primitive_fit_engine_generalization_gate -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Expected: both fail because the Batch B payload does not exist and the report still points to
Batch B.

## Task 2: Implement Batch B Payload

- [ ] Add constants near the existing generalization constants:

```python
_PAPER_GENERALIZATION_BATCH_C_SEARCH = "paper_generalization_batch_c_search_engine"
_PAPER_GENERALIZATION_C_NEXT_ACTION = (
    "Proceed to paper_generalization_batch_c_search_engine after the "
    "primitive-fit engine generalization matrix; keep stronger wording blocked."
)
```

- [ ] Replace the source-policy-specific remaining-gates helper with a closed-gates helper:

```python
def _paper_remaining_generalization_gates_after(
    closed_gates: set[str],
) -> list[str]:
    return [
        str(batch["batch_id"])
        for batch in _paper_faithful_offline_generalization_batches()
        if str(batch["batch_id"]) not in closed_gates
    ]
```

- [ ] Keep source-policy payload using `{_PAPER_GENERALIZATION_BATCH_A_SOURCE_POLICY}` as its
closed set; use Batch A and Batch B as the closed set for top-level report state.

- [ ] Extract candidate row construction:

```python
def _paper_primitive_fit_candidate_rows(
    mesh: TriangleMesh,
    face_group: frozenset[int],
) -> list[dict[str, object]]:
    obb_row = _paper_obb_candidate_payload(mesh, face_group)
    return [
        obb_row,
        _paper_sphere_candidate_payload(mesh, face_group, obb_row),
        _paper_capsule_candidate_payload(mesh, face_group),
        _flat_capped_cylinder_candidate_payload(mesh, face_group),
        _frustum_candidate_payload(mesh, face_group),
        _trapezoidal_prism_candidate_payload(mesh, face_group),
    ]
```

- [ ] Modify `_primitive_fit_audit_payload()` to call `_paper_primitive_fit_candidate_rows()`.

- [ ] Add `_paper_primitive_fit_engine_probe_specs()` returning six probe definitions:

```python
[
    (
        "paper_fit_engine_rotated_obb_probe",
        "oriented_bounding_box",
        _paper_rotated_box_fit_mesh(),
        {"shape_family": "rotated_nonuniform_cuboid"},
    ),
    (
        "paper_fit_engine_offset_sphere_probe",
        "sphere",
        _paper_offset_sphere_fit_mesh(),
        {"shape_family": "offset_cuboid_with_asymmetric_point"},
    ),
    (
        "paper_fit_engine_off_axis_capsule_probe",
        "capsule",
        _paper_off_axis_capsule_fit_mesh(),
        {"shape_family": "elongated_off_axis_cuboid"},
    ),
    (
        "paper_fit_engine_flat_capped_cylinder_probe",
        "capped_cylinder",
        _paper_flat_capped_cylinder_axis_fit_mesh(),
        {"shape_family": "off_axis_flat_capped_cylinder_like_cuboid"},
    ),
    (
        "paper_fit_engine_tapered_frustum_probe",
        "frustum",
        _paper_tapered_frustum_fit_mesh(),
        {"shape_family": "tapered_unequal_radius_frustum_like_mesh"},
    ),
    (
        "paper_fit_engine_asymmetric_trapezoid_probe",
        "trapezoidal_prism",
        _paper_asymmetric_trapezoid_fit_mesh(),
        {"shape_family": "asymmetric_trapezoidal_prism_like_wedge"},
    ),
]
```

- [ ] Add `_paper_primitive_fit_engine_generalization_payload()` that builds one row per probe by
calling `_primitive_fit_audit_payload(mesh, frozenset(range(len(mesh.faces))))`.

- [ ] Add top-level report fields:

```python
"paper_generalization_batch_b_primitive_fit_engine": (
    _paper_primitive_fit_engine_generalization_payload()
)
```

- [ ] Update top-level `missing_before_paper_faithful`, `failure_labels`, and
`next_required_gate` to use C-E after Batch B closure.

## Task 3: GREEN Tests And CLI Smoke

- [ ] Run focused tests:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_primitive_fit_engine_generalization_gate -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Expected: both pass.

- [ ] Run CPD paper and CLI tests:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
```

Expected: all pass.

- [ ] Run CLI smoke:

```bash
PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report \
  | python -c 'import json,sys; p=json.load(sys.stdin); assert p["next_required_gate"] == "paper_generalization_batch_c_search_engine"; assert "paper_generalization_batch_b_primitive_fit_engine_missing" not in p["failure_labels"]; assert p["paper_generalization_batch_b_primitive_fit_engine"]["closed_gate"] == "paper_generalization_batch_b_primitive_fit_engine"; assert p["paper_faithful_offline_supported"] is False; print("primitive fit engine generalization CLI smoke passed")'
```

Expected: prints `primitive fit engine generalization CLI smoke passed`.

## Task 4: Documentation, Registry, And Record

- [ ] Update current-status docs so the current next gate is Batch C:
  `README.md`, `docs/index.md`, `docs/deepdive/evidence-status.md`,
  `docs/reference/claim-boundaries.md`, `docs/reference/cpd-paper-faithful-offline-lane-spec.md`,
  `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`,
  `docs/reference/cpd-paper-reproduction-gap-matrix.md`, and
  `docs/reference/cpd-paper-story-status.md`.

- [ ] Add record `docs/records/2026-05-16-cpd-paper-generalization-batch-b-primitive-fit-engine.md`
with:
  - status complete only after verification;
  - RED/GREEN test evidence;
  - ignored paper source worktree baseline note;
  - multi-agent review summary;
  - supported and unsupported claims.

- [ ] Add the record to `docs/records/README.md`, `docs/index.md`, and
`experiments/registry.yaml`.

- [ ] Run docs and claim validation:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

## Task 5: Review, Full Verification, Merge

- [ ] Request read-only implementation/schema and docs/claim-boundary reviews before commit.

- [ ] Fix valid findings one at a time.

- [ ] Run final verification:

```bash
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

- [ ] Commit:

```bash
git add src/primitive_collision_compiler/baselines/cpd_paper/offline.py \
  tests/test_cpd_paper_offline.py tests/test_cli.py README.md docs/index.md \
  docs/deepdive/evidence-status.md docs/reference/claim-boundaries.md \
  docs/reference/cpd-paper-faithful-offline-lane-spec.md \
  docs/reference/cpd-paper-fixture-breadth-expansion-plan.md \
  docs/reference/cpd-paper-reproduction-gap-matrix.md \
  docs/reference/cpd-paper-story-status.md docs/records/README.md \
  docs/records/2026-05-16-cpd-paper-generalization-batch-b-primitive-fit-engine.md \
  docs/superpowers/specs/2026-05-16-cpd-paper-primitive-fit-engine-generalization-design.md \
  docs/superpowers/plans/2026-05-16-cpd-paper-primitive-fit-engine-generalization.md \
  experiments/registry.yaml
git commit -m "feat: add CPD paper primitive fit engine generalization"
```

- [ ] Fast-forward merge into `main`, rerun verification on main, push `origin main`, and remove
only `.worktrees/cpd-paper-primitive-fit-engine-generalization`.
