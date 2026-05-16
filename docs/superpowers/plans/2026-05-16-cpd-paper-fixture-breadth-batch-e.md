# CPD Paper Fixture Breadth Batch E Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Batch E postprocess breadth fixtures to the partial offline
`cpd_paper_offline_report`.

**Architecture:** Keep the slice fixture-only, command-only, and offline-only. Extend the explicit
postprocess audit payloads so the existing identity-axis OBB cull can coexist with a rotated OBB
cull fixture and a conservative cross-type boundary fixture that records unsupported cross-type
culling without silently deleting primitives. Do not add package generation, Newton, real USD,
benchmark, generated-search postprocess, or a general containment library.

**Tech Stack:** Python, NumPy, pytest, Markdown docs, YAML registry.

---

### Task 1: RED Tests For Batch E Report Surface

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] Add a failing offline-report test named
  `test_cpd_paper_offline_report_records_fixture_breadth_batch_e`.

```python
def test_cpd_paper_offline_report_records_fixture_breadth_batch_e():
    report = build_cpd_paper_offline_report()
    cases = {case["case_id"]: case for case in report["cases"]}

    expected_case_ids = {
        "paper_rotated_nested_primitive",
        "paper_cross_type_enclosure_boundary",
    }
    assert expected_case_ids.issubset(cases)
    for case_id in expected_case_ids:
        case = cases[case_id]
        assert case["fixture_breadth_batch"] == "paper_fixture_breadth_batch_e"
        assert case["package_generation_triggered"] is False
        assert case["newton_runtime_triggered"] is False
        assert case["real_usd_triggered"] is False
        assert case["benchmark_triggered"] is False
        postprocess = case["postprocess_audit"]
        assert postprocess["package_generation_triggered"] is False
        assert postprocess["newton_runtime_triggered"] is False
        assert postprocess["real_usd_triggered"] is False
        assert postprocess["benchmark_triggered"] is False

    rotated = cases["paper_rotated_nested_primitive"]["postprocess_audit"]
    assert rotated["audit_scope"] == "enclosed_primitive_culling_fixture"
    assert rotated["fixture_variant"] == "rotated_nested_obb"
    assert rotated["containment_test_type"] == "obb_corners_inside_obb"
    assert rotated["axis_policy"] == "shared_rotated_axes"
    assert rotated["input_primitive_count"] == 2
    assert rotated["output_primitive_count"] == 1
    assert rotated["culled_primitive_ids"] == [1]
    assert rotated["kept_primitive_ids"] == [0]
    assert rotated["rotation_degrees_about_z"] == 30.0
    assert rotated["rotated_axes_non_identity"] is True
    assert rotated["input_primitives"][0]["axes"] == rotated["input_primitives"][1]["axes"]
    assert rotated["input_primitives"][0]["axes"] != [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ]
    assert rotated["cull_records"] == [
        {
            "culled_primitive_id": 1,
            "enclosing_primitive_id": 0,
            "cull_reason": "primitive_enclosed_by_larger_primitive",
            "containment_passed": True,
            "tested_corner_count": 8,
        }
    ]

    cross_type = cases["paper_cross_type_enclosure_boundary"]["postprocess_audit"]
    assert cross_type["audit_scope"] == "enclosed_primitive_cross_type_boundary_fixture"
    assert cross_type["fixture_variant"] == "cross_type_unsupported_boundary"
    assert cross_type["containment_test_type"] == "cross_type_containment_unsupported"
    assert cross_type["cross_type_culling_supported"] is False
    assert cross_type["unsupported_containment_label"] == (
        "cross_type_enclosure_boundary_not_supported"
    )
    assert cross_type["top_level_failure_label"] is False
    assert cross_type["input_primitive_count"] == 2
    assert cross_type["output_primitive_count"] == 2
    assert cross_type["culled_primitive_ids"] == []
    assert cross_type["kept_primitive_ids"] == [0, 1]
    assert cross_type["cull_records"] == []
    assert cross_type["unsupported_records"] == [
        {
            "candidate_primitive_id": 1,
            "enclosing_primitive_id": 0,
            "candidate_kind": "sphere",
            "enclosing_kind": "oriented_bounding_box",
            "unsupported_reason": "cross_type_containment_not_implemented_for_fixture",
        }
    ]
```

- [ ] Update the next-gate test so Batch E advances the current report to a post-fixture scope
  review while the top report stays partial.

```python
def test_cpd_paper_offline_report_next_gate_is_fixture_breadth_completion_review():
    report = build_cpd_paper_offline_report()

    assert report["next_required_gate"] == "paper_fixture_breadth_completion_review"
```

- [ ] Update `test_cpd_paper_offline_report_covers_first_toy_slice` so it expects:

```python
assert report["next_required_gate"] == "paper_fixture_breadth_completion_review"
assert "paper_fixture_breadth_batch_e_postprocess" in report[
    "paper_faithfulness"
]["implemented_fixture_scope"]
```

- [ ] Add the two Batch E case ids to the exact `set(cases)` assertion in
  `test_cpd_paper_offline_report_covers_first_toy_slice`:

```python
"paper_rotated_nested_primitive",
"paper_cross_type_enclosure_boundary",
```

- [ ] Update `EXPECTED_SCOPE_AUDIT_ROWS` in `tests/test_cpd_paper_offline.py` for the
  `enclosed_primitive_postprocess` row only. Keep `status` as `partial_fixture_scope`, keep
  `blocking_for_paper_faithful_offline` as `True`, and keep the report decision as
  `remain_partial`.

```python
{
    "criterion_id": "enclosed_primitive_postprocess",
    "current_evidence": (
        "Identity-axis and rotated nested OBB cull fixtures exist, and Batch E records "
        "a conservative cross-type unsupported boundary with no silent cull."
    ),
    "next_action": "Run fixture-breadth completion review before stronger wording.",
}
```

- [ ] Update `tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json` so it expects
  `paper_fixture_breadth_completion_review`, includes the two Batch E ids in the case-id subset,
  and adds this lightweight JSON surface block.

```python
batch_e_cases = {
    case["case_id"]: case
    for case in payload["cases"]
    if case["case_id"]
    in {
        "paper_rotated_nested_primitive",
        "paper_cross_type_enclosure_boundary",
    }
}
assert set(batch_e_cases) == {
    "paper_rotated_nested_primitive",
    "paper_cross_type_enclosure_boundary",
}
assert batch_e_cases["paper_rotated_nested_primitive"]["postprocess_audit"][
    "output_primitive_count"
] == 1
assert batch_e_cases["paper_cross_type_enclosure_boundary"]["postprocess_audit"][
    "cross_type_culling_supported"
] is False
for case in batch_e_cases.values():
    assert case["fixture_breadth_batch"] == "paper_fixture_breadth_batch_e"
    assert case["package_generation_triggered"] is False
    assert case["newton_runtime_triggered"] is False
    assert case["real_usd_triggered"] is False
    assert case["benchmark_triggered"] is False
```

- [ ] Run the focused RED tests and verify they fail because the Batch E fields and gate do not
  exist yet.

```bash
python -m pytest -q \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_batch_e \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_fixture_breadth_completion_review \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice \
  tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json
```

Expected: FAIL, with missing Batch E case ids and `paper_fixture_breadth_batch_e` still reported
as the next gate.

### Task 2: Minimal Batch E Implementation

**Files:**

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] Add an optional postprocess audit variant to `_PaperToyCase`.

```python
postprocess_audit_variant: str | None = None
```

- [ ] Change `_case_payload` to pass the requested variant while preserving the existing
  `paper_nested_primitive` behavior.

```python
if case.postprocess_fixture:
    payload["postprocess_audit"] = _postprocess_audit_payload(
        case.postprocess_audit_variant or "identity_nested_obb"
    )
```

- [ ] Replace `_postprocess_audit_payload()` with a variant dispatcher.

```python
def _postprocess_audit_payload(variant: str = "identity_nested_obb") -> dict[str, object]:
    if variant == "identity_nested_obb":
        return _nested_obb_postprocess_audit_payload(
            axes=np.eye(3, dtype=np.float64),
            axis_policy="shared_identity_axes",
            fixture_variant="identity_nested_obb",
            rotation_degrees_about_z=0.0,
        )
    if variant == "rotated_nested_obb":
        angle = np.deg2rad(30.0)
        axes = np.array(
            [
                [np.cos(angle), -np.sin(angle), 0.0],
                [np.sin(angle), np.cos(angle), 0.0],
                [0.0, 0.0, 1.0],
            ],
            dtype=np.float64,
        )
        return _nested_obb_postprocess_audit_payload(
            axes=axes,
            axis_policy="shared_rotated_axes",
            fixture_variant="rotated_nested_obb",
            rotation_degrees_about_z=30.0,
        )
    if variant == "cross_type_unsupported_boundary":
        return _cross_type_unsupported_postprocess_audit_payload()
    raise ValueError(f"unsupported postprocess audit variant: {variant}")
```

- [ ] Move the existing identity OBB logic into `_nested_obb_postprocess_audit_payload(...)` and
  add the variant metadata fields used by the tests:

```python
"fixture_variant": fixture_variant,
"rotation_degrees_about_z": float(rotation_degrees_about_z),
"rotated_axes_non_identity": bool(not np.allclose(axes, np.eye(3))),
```

- [ ] Add `_postprocess_sphere_row(...)`.

```python
def _postprocess_sphere_row(
    *,
    primitive_id: int,
    center: NDArray[np.float64],
    radius: float,
) -> dict[str, object]:
    return {
        "primitive_id": primitive_id,
        "kind": "sphere",
        "center": _vector(center),
        "radius": float(radius),
    }
```

- [ ] Add `_cross_type_unsupported_postprocess_audit_payload()` with explicit no-cull accounting.

```python
def _cross_type_unsupported_postprocess_audit_payload() -> dict[str, object]:
    outer = _postprocess_obb_row(
        primitive_id=0,
        center=np.array([0.0, 0.0, 0.0], dtype=np.float64),
        half_extents=np.array([1.0, 1.0, 1.0], dtype=np.float64),
        axes=np.eye(3, dtype=np.float64),
    )
    inner = _postprocess_sphere_row(
        primitive_id=1,
        center=np.array([0.0, 0.0, 0.0], dtype=np.float64),
        radius=0.25,
    )
    return {
        "audit_scope": "enclosed_primitive_cross_type_boundary_fixture",
        "fixture_variant": "cross_type_unsupported_boundary",
        "postprocess_input_source": "explicit_audit_primitives_not_search_trace",
        "input_primitive_count": 2,
        "output_primitive_count": 2,
        "postprocess_policy": "do_not_silently_cull_unsupported_cross_type_boundary",
        "containment_test_type": "cross_type_containment_unsupported",
        "cross_type_culling_supported": False,
        "unsupported_containment_label": "cross_type_enclosure_boundary_not_supported",
        "top_level_failure_label": False,
        "input_primitives": [outer, inner],
        "cull_records": [],
        "unsupported_records": [
            {
                "candidate_primitive_id": 1,
                "enclosing_primitive_id": 0,
                "candidate_kind": "sphere",
                "enclosing_kind": "oriented_bounding_box",
                "unsupported_reason": "cross_type_containment_not_implemented_for_fixture",
            }
        ],
        "enclosed_primitive_ids": [],
        "enclosing_primitive_ids": [],
        "kept_primitive_ids": [0, 1],
        "culled_primitive_ids": [],
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }
```

- [ ] Add two Batch E cases to `_paper_toy_cases()` after Batch D.

```python
_PaperToyCase(
    case_id="paper_rotated_nested_primitive",
    description="Batch E rotated nested OBB fixture for enclosed-primitive postprocess breadth",
    mesh=_nested_primitive_mesh(),
    face_groups=(frozenset(range(12)),),
    postprocess_fixture=True,
    postprocess_audit_variant="rotated_nested_obb",
    fixture_breadth_batch="paper_fixture_breadth_batch_e",
),
_PaperToyCase(
    case_id="paper_cross_type_enclosure_boundary",
    description="Batch E cross-type postprocess boundary fixture with explicit unsupported no-cull accounting",
    mesh=_nested_primitive_mesh(),
    face_groups=(frozenset(range(12)),),
    postprocess_fixture=True,
    postprocess_audit_variant="cross_type_unsupported_boundary",
    fixture_breadth_batch="paper_fixture_breadth_batch_e",
),
```

- [ ] Advance the report gate and implemented fixture scope.

```python
"next_required_gate": "paper_fixture_breadth_completion_review",
```

```python
"paper_fixture_breadth_batch_e_postprocess",
```

- [ ] Update the postprocess scope audit row in `offline.py` to match the test string from Task 1.

- [ ] Run the focused GREEN tests.

```bash
python -m pytest -q \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_batch_e \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_fixture_breadth_completion_review \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice \
  tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json
```

Expected: PASS.

### Task 3: Documentation And Record Updates

**Files:**

- Modify: `README.md`
- Modify: `docs/index.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/records/README.md`
- Modify: `experiments/registry.yaml`
- Create: `docs/records/2026-05-16-cpd-paper-fixture-breadth-batch-e.md`

- [ ] Update top-level and DeepDive evidence wording so it says Batch E is implemented and the
  next gate is `paper_fixture_breadth_completion_review`, while keeping the report partial.

- [ ] Update the paper gap matrix postprocess row so it says Batch E records:
  rotated nested OBB containment, conservative cross-type unsupported boundary accounting, and
  offline-only/no-runtime boundaries.

- [ ] Update the offline-lane spec and story-status docs so the story reads:

```text
Batch A: source/preprocess/intake/operator breadth
Batch B: primitive-fit breadth
Batch C: cost/search/stop breadth
Batch D: component-pair breadth
Batch E: postprocess breadth
Next: fixture-breadth completion review
```

- [ ] Fix the Batch A status block in
  `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md` if it is still missing its
  explicit code block.

- [ ] Add a dated record mirroring the Batch D record style, including RED, GREEN, focused, CLI
  smoke, full pytest, docs/site/diff verification, subagent usage-limit notes if applicable, and
  local three-angle review notes.

- [ ] Add an `experiments/registry.yaml` entry named
  `cpd-paper-fixture-breadth-batch-e` with status `complete`, command
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report`, and
  the new record path.

### Task 4: Verification, Review, Commit, Push

**Files:**

- Inspect all files touched in Tasks 1-3.

- [ ] Run a CLI smoke to inspect the Batch E fields.

```bash
python - <<'PY'
from primitive_collision_compiler.baselines.cpd_paper.offline import build_cpd_paper_offline_report

report = build_cpd_paper_offline_report()
cases = {case["case_id"]: case for case in report["cases"]}
print(report["next_required_gate"])
for case_id in (
    "paper_rotated_nested_primitive",
    "paper_cross_type_enclosure_boundary",
):
    audit = cases[case_id]["postprocess_audit"]
    print(case_id)
    print("scope", audit["audit_scope"])
    print("variant", audit["fixture_variant"])
    print("input", audit["input_primitive_count"])
    print("output", audit["output_primitive_count"])
    print("culled", audit["culled_primitive_ids"])
    print("kept", audit["kept_primitive_ids"])
print(report["package_generation_triggered"], report["newton_runtime_triggered"], report["real_usd_triggered"], report["benchmark_triggered"])
PY
```

Expected:

```text
paper_fixture_breadth_completion_review
paper_rotated_nested_primitive
scope enclosed_primitive_culling_fixture
variant rotated_nested_obb
input 2
output 1
culled [1]
kept [0]
paper_cross_type_enclosure_boundary
scope enclosed_primitive_cross_type_boundary_fixture
variant cross_type_unsupported_boundary
input 2
output 2
culled []
kept [0, 1]
False False False False
```

- [ ] Run focused tests.

```bash
python -m pytest -q tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json
```

Expected: PASS.

- [ ] Run full verification.

```bash
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all commands exit 0.

- [ ] Attempt three independent review agents: implementation/schema review,
  documentation/claim-boundary review, and reproducibility/registry review. If platform usage
  limits prevent review agents from returning findings, record that limitation explicitly in the
  dated record and perform local three-angle review before committing.

- [ ] Commit and push the plan checkpoint before implementation if this task is still only the
  plan. Commit and push the final implementation after all verification and reviews pass or after
  usage-limit fallback review is recorded.

```bash
git add docs/superpowers/plans/2026-05-16-cpd-paper-fixture-breadth-batch-e.md
git commit -m "docs: plan CPD paper fixture breadth batch E"
git push
```

```bash
git add README.md docs/index.md docs/deepdive/evidence-status.md docs/reference/claim-boundaries.md docs/reference/cpd-paper-reproduction-gap-matrix.md docs/reference/cpd-paper-faithful-offline-lane-spec.md docs/reference/cpd-paper-fixture-breadth-expansion-plan.md docs/reference/cpd-paper-story-status.md docs/records/README.md docs/records/2026-05-16-cpd-paper-fixture-breadth-batch-e.md experiments/registry.yaml src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cpd_paper_offline.py tests/test_cli.py
git commit -m "feat: add CPD paper fixture breadth batch E"
git push
```

Expected: branch remains clean and synced with `origin/main`.

## Self-Review

- Spec coverage: the plan maps Batch E fixture ids, rotated OBB containment, cross-type no-cull
  unsupported accounting, RED/GREEN tests, docs, records, registry, verification, review fallback,
  commit, and push to explicit tasks.
- Placeholder scan: no unfilled task placeholders are present.
- Claim boundary: every task keeps package generation, Newton runtime, real USD, benchmark,
  generated-search postprocess, general containment library, deployment, and safety claims out of
  scope.
