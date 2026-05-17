# CPD Paper Mapped-Subset Newton Shape-Mapping Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the bounded offline/report-only `paper_mapped_subset_newton_shape_mapping_contract` gate after the existing Newton shape-mapping preflight gate.

**Architecture:** Extend the existing `cpd_paper_offline_report` runtime-lane chain by consuming the preflight payload and emitting exactly one report-scoped Newton box descriptor contract row for `paper_single_box`. The slice must stay static and report-only: no Newton imports, no Newton shape objects, no runtime execution, no USD, no benchmark, no collision-quality measurement.

**Tech Stack:** Python, pytest, Markdown docs, existing `primitive_collision_compiler.baselines.cpd_paper.offline` report builders.

---

## File Structure

- Modify `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
  - Add `_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT`.
  - Add a helper that advances remaining gaps after `paper_mapped_subset_newton_shape_mapping_contract`.
  - Add shape-mapping contract validation/build helpers after the existing preflight helpers.
  - Wire the new payload into `build_cpd_paper_offline_report()`.
- Modify `tests/test_cpd_paper_offline.py`
  - Add constants, required-key sets, positive schema tests, negative drift tests, and static boundary tests.
- Modify `tests/test_cli.py`
  - Update the offline report expected failure label and next gate.
- Modify docs:
  - `README.md`
  - `docs/index.md`
  - `docs/deepdive/evidence-status.md`
  - `docs/deepdive/message-map.md`
  - `docs/reference/claim-boundaries.md`
  - `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
  - `docs/reference/cpd-paper-reproduction-gap-matrix.md`
  - `docs/reference/cpd-paper-story-status.md`
  - `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
  - `docs/records/README.md`
  - Create `docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-mapping-contract.md`

## Task 1: RED Tests For The Shape-Mapping Contract

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add constants and key sets**

Add near the existing Newton shape-mapping preflight constants:

```python
EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"
)
EXPECTED_NEWTON_SHAPE_MAPPING_CONTRACT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT,
]
```

Add shape-mapping contract key sets after the preflight key sets:

```python
NEWTON_SHAPE_MAPPING_CONTRACT_FALSE_FLAGS = (
    "paper_faithful_offline_allowed",
    "paper_faithful_offline_supported",
    "newton_support_claimed",
    "approximation_policy_applied",
    "real_usd_loaded",
    "benchmark_run",
    "collision_quality_measured",
    "deployment_or_certification_claimed",
    "package_generation_triggered",
    "newton_runtime_triggered",
    "real_usd_triggered",
    "benchmark_triggered",
    "newton_runtime_allowed",
    "approximation_policy_enabled",
    "silent_drop_allowed",
    "mapping_attempted",
    "newton_shape_mapping_triggered",
    "newton_shape_mapping_record_created",
    "newton_shape_object_created",
)

NEWTON_SHAPE_MAPPING_CONTRACT_ROW_REQUIRED_KEYS = frozenset(
    {
        "shape_mapping_row_id",
        "source_newton_shape_mapping_preflight_row_id",
        "source_runtime_admissibility_row_id",
        "source_package_id",
        "source_asset_id",
        "fixture_id",
        "paper_primitive",
        "primitive_spec_kind",
        "primitive_id",
        "target_newton_shape_kind",
        "newton_shape_descriptor_dict",
        "descriptor_contract_passed",
        "descriptor_kind_check_passed",
        "target_kind_check_passed",
        "center_descriptor_check_passed",
        "axes_descriptor_check_passed",
        "half_extents_descriptor_check_passed",
        "source_preflight_check_passed",
        "source_lineage_check_passed",
        "mapping_attempt_count",
        "newton_mapping_record_count",
        "newton_shape_object_count",
        "newton_runtime_execution_count",
        *NEWTON_SHAPE_MAPPING_CONTRACT_FALSE_FLAGS,
    }
)

NEWTON_SHAPE_MAPPING_CONTRACT_PAYLOAD_REQUIRED_KEYS = frozenset(
    {
        "gate_id",
        "gate_status",
        "closed_gate",
        "input_gate_id",
        "next_required_gate",
        "decision",
        "decision_reason",
        "artifact_kind",
        "schema_version",
        "source_scope",
        "implementation_boundary",
        "shape_mapping_contract_action",
        "newton_shape_mapping_contract",
        "input_contract_summary",
        "shape_mapping_contract_row_count",
        "source_newton_shape_mapping_preflight_row_count",
        "report_scoped_newton_shape_descriptor_count",
        "source_preflight_check_passed",
        "mapping_attempt_count",
        "newton_mapping_record_count",
        "newton_shape_object_count",
        "newton_runtime_execution_count",
        "generated_runtime_primitive_spec_count",
        "generated_primitive_spec_count",
        "generated_collision_package_count",
        "runtime_admissibility_check_count",
        "offline_static_runtime_admissibility_check_count",
        "shape_mapping_rows",
        "coverage_summary",
        "remaining_gaps",
        *NEWTON_SHAPE_MAPPING_CONTRACT_FALSE_FLAGS,
    }
)
```

- [ ] **Step 2: Add helper to fetch the input preflight payload**

Add near `_newton_shape_mapping_preflight_input()`:

```python
def _newton_shape_mapping_contract_input():
    return json.loads(
        json.dumps(
            build_cpd_paper_offline_report()[
                "paper_mapped_subset_newton_shape_mapping_preflight_contract"
            ]
        )
    )
```

- [ ] **Step 3: Add positive tests**

Add tests after the preflight tests:

```python
def test_cpd_paper_records_mapped_subset_newton_shape_mapping_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_newton_shape_mapping_contract"]

    assert report["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
    )
    assert report["failure_labels"] == [
        "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_missing"
    ]
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_NEWTON_SHAPE_MAPPING_CONTRACT_REMAINING_GAPS
    )
    assert payload["gate_id"] == EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
    )
    assert payload["shape_mapping_contract_row_count"] == 1
    assert payload["report_scoped_newton_shape_descriptor_count"] == 1
    assert payload["mapping_attempt_count"] == 0
    assert payload["newton_mapping_record_count"] == 0
    assert payload["newton_shape_object_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0


def test_cpd_paper_newton_shape_mapping_contract_payload_schema_is_exact():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_newton_shape_mapping_contract"
    ]

    assert set(payload) == NEWTON_SHAPE_MAPPING_CONTRACT_PAYLOAD_REQUIRED_KEYS
    assert payload["gate_status"] == (
        "implemented_offline_static_shape_descriptor_contract_only"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_shape_mapping_contract_complete_"
        "newton_shape_runtime_boundary_preflight_missing"
    )
    assert payload["artifact_kind"] == (
        "offline_static_newton_shape_descriptor_contract_not_runtime_mapping"
    )
    assert payload["newton_shape_mapping_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT
        ),
        "closed_gate": EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT,
        "next_newton_shape_runtime_boundary_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
        ),
        "shape_mapping_contract_rows_required": 1,
        "report_scoped_newton_shape_descriptors_required": 1,
        "newton_shape_object_allowed": False,
        "newton_runtime_allowed": False,
        "newton_support_claim_allowed": False,
    }


def test_cpd_paper_newton_shape_mapping_contract_records_descriptor_row():
    report = build_cpd_paper_offline_report()
    preflight_row = report[
        "paper_mapped_subset_newton_shape_mapping_preflight_contract"
    ]["newton_shape_mapping_preflight_rows"][0]
    payload = report["paper_mapped_subset_newton_shape_mapping_contract"]
    rows = payload["shape_mapping_rows"]

    assert len(rows) == 1
    row = rows[0]
    assert set(row) == NEWTON_SHAPE_MAPPING_CONTRACT_ROW_REQUIRED_KEYS
    assert row["shape_mapping_row_id"] == "newton_shape_mapping__paper_single_box__box"
    assert row["source_newton_shape_mapping_preflight_row_id"] == (
        preflight_row["newton_shape_mapping_preflight_row_id"]
    )
    assert row["target_newton_shape_kind"] == "box"
    assert row["descriptor_contract_passed"] is True
    descriptor = row["newton_shape_descriptor_dict"]
    candidate = preflight_row["candidate_primitivespec_dict"]
    assert descriptor == {
        "descriptor_kind": "newton_shape_descriptor",
        "target_newton_shape_kind": "box",
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": "paper_single_box__oriented_bounding_box__box",
        "center": candidate["center"],
        "axes": candidate["axes"],
        "half_extents": candidate["dimensions"]["half_extents"],
        "mapping_contract": "report_scoped_static_descriptor_no_newton_call",
    }
    assert row["newton_shape_object_count"] == 0
    assert row["newton_runtime_execution_count"] == 0
    assert list(_recursive_package_dicts(payload)) == []
```

- [ ] **Step 4: Add boundary flag and negative tests**

Add:

```python
@pytest.mark.parametrize("field_name", NEWTON_SHAPE_MAPPING_CONTRACT_FALSE_FLAGS)
def test_cpd_paper_newton_shape_mapping_contract_boundary_flags_stay_false(field_name):
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_newton_shape_mapping_contract"
    ]

    assert payload[field_name] is False
    assert payload["shape_mapping_rows"][0][field_name] is False


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        ("gate_id", "stale_gate", "newton_shape_mapping_contract_input_gate_id_mismatch"),
        (
            "next_required_gate",
            "stale_gate",
            "newton_shape_mapping_contract_input_next_gate_mismatch",
        ),
        (
            "newton_shape_mapping_preflight_row_count",
            2,
            "newton_shape_mapping_contract_input_count_mismatch:"
            "newton_shape_mapping_preflight_row_count",
        ),
        (
            "mapping_attempt_count",
            1,
            "newton_shape_mapping_contract_input_count_mismatch:mapping_attempt_count",
        ),
        (
            "newton_mapping_record_count",
            1,
            "newton_shape_mapping_contract_input_count_mismatch:"
            "newton_mapping_record_count",
        ),
        (
            "newton_runtime_execution_count",
            1,
            "newton_shape_mapping_contract_input_count_mismatch:"
            "newton_runtime_execution_count",
        ),
    ],
)
def test_cpd_paper_newton_shape_mapping_contract_rejects_input_drift(
    field_name,
    bad_value,
    error_label,
):
    preflight = _newton_shape_mapping_contract_input()
    preflight[field_name] = bad_value

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_mapping_contract_payload(
            preflight
        )
```

Also add row drift, descriptor source-package copy, candidate non-dict/malformed half-extent, and
static boundary tests mirroring the preflight block. The static boundary test must slice from
`_NEWTON_SHAPE_MAPPING_CONTRACT_PAYLOAD_FALSE_FLAGS` to
`def _paper_source_policy_generalization_payload` and reject:

```python
[
    "CollisionPackage(",
    "PrimitiveSpec(",
    "FallbackSpec",
    "primitive_collision_compiler.newton",
    "NewtonShapeMapping",
    "map_package_shapes",
    "import newton",
    "import newton_warp",
    "Newton",
    "run_newton",
    "newton.",
    "check_runtime_admissibility",
    "run_runtime_admissibility",
    "pxr",
    "Usd",
    "USD",
    "load_first_mesh",
    "inspect_usd_asset",
    "assets.usd_smoke",
    "real_usd_comparison",
    "timeit",
    "perf_counter",
    "benchmark_metric",
    "surface_distance",
    "collision_quality_score",
    "run_benchmark",
    "measure_collision_quality",
]
```

- [ ] **Step 5: Update CLI expected current gate**

In `tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json`, update:

```python
assert payload["failure_labels"] == [
    "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_missing",
]
assert (
    payload["next_required_gate"]
    == "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"
)
assert payload["paper_faithfulness"]["runtime_lane_remaining_gates"] == [
    "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract",
]
```

Also append `"paper_mapped_subset_newton_shape_mapping_contract"` to the expected
`implemented_output_contract_scope` list.

- [ ] **Step 6: Run RED tests**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_mapping_contract' -q
```

Expected: fails because `paper_mapped_subset_newton_shape_mapping_contract` and helper do not
exist yet.

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Expected: fails because the current report still points at
`paper_mapped_subset_newton_shape_mapping_contract`.

## Task 2: Implement The Report-Only Shape-Mapping Contract

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add the next gate constant and remaining-gap helper**

Near the current Newton shape-mapping constants, add:

```python
_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"
)
```

After `_paper_remaining_gaps_after_mapped_subset_newton_shape_mapping_preflight()` add:

```python
def _paper_remaining_gaps_after_mapped_subset_newton_shape_mapping_contract() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT]
```

- [ ] **Step 2: Add contract false flags and descriptor helpers**

After `_paper_mapped_subset_newton_shape_mapping_preflight_contract_payload()`, add helpers named:

```python
_NEWTON_SHAPE_MAPPING_CONTRACT_PAYLOAD_FALSE_FLAGS
_paper_newton_shape_mapping_contract_false_flags
_paper_newton_shape_mapping_contract_source_row
_paper_newton_shape_mapping_descriptor
_paper_newton_shape_mapping_contract_row
_paper_newton_shape_mapping_contract_coverage_summary
_paper_mapped_subset_newton_shape_mapping_contract_payload
```

Use `_paper_newton_shape_mapping_preflight_vector()` and
`_paper_validate_newton_shape_mapping_preflight_candidate()` for numeric/candidate validation.

`_paper_newton_shape_mapping_contract_source_row(preflight)` must validate:

```python
preflight["gate_id"] == _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT
preflight["next_required_gate"] == _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT
preflight["newton_shape_mapping_preflight_row_count"] == 1
preflight["source_runtime_admissibility_row_count"] == 1
preflight["mapping_attempt_count"] == 0
preflight["newton_mapping_record_count"] == 0
preflight["newton_runtime_execution_count"] == 0
```

It must require all preflight false flags to remain false and exactly one
`newton_shape_mapping_preflight_rows` item.

The source row must match:

```python
{
    "newton_shape_mapping_preflight_row_id":
        "newton_shape_mapping_preflight__paper_single_box__box",
    "source_runtime_admissibility_row_id":
        "runtime_admissibility__paper_single_box__box",
    "fixture_id": "paper_single_box",
    "paper_primitive": "oriented_bounding_box",
    "primitive_spec_kind": "box",
    "primitive_id": "paper_single_box__oriented_bounding_box__box",
    "target_newton_shape_kind": "box",
    "newton_shape_mapping_preflight_passed": True,
}
```

It must reject copied package dicts using `_paper_runtime_admissibility_preflight_package_dicts`.

- [ ] **Step 3: Build the descriptor row**

The descriptor helper must return:

```python
{
    "descriptor_kind": "newton_shape_descriptor",
    "target_newton_shape_kind": "box",
    "source_fixture_id": source_row["fixture_id"],
    "source_primitive_id": source_row["primitive_id"],
    "center": candidate["center"],
    "axes": candidate["axes"],
    "half_extents": candidate["dimensions"]["half_extents"],
    "mapping_contract": "report_scoped_static_descriptor_no_newton_call",
}
```

The row helper must return the fields required by
`NEWTON_SHAPE_MAPPING_CONTRACT_ROW_REQUIRED_KEYS`, with `mapping_attempt_count`,
`newton_mapping_record_count`, `newton_shape_object_count`, and `newton_runtime_execution_count`
set to zero.

- [ ] **Step 4: Build the payload**

The payload helper must return the fields required by
`NEWTON_SHAPE_MAPPING_CONTRACT_PAYLOAD_REQUIRED_KEYS`. Set:

```python
"gate_id": _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT
"input_gate_id": _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT
"next_required_gate": _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
"remaining_gaps": _paper_remaining_gaps_after_mapped_subset_newton_shape_mapping_contract()
```

No Newton runtime objects, imports, or calls are allowed.

- [ ] **Step 5: Wire into `build_cpd_paper_offline_report()`**

After `mapped_subset_newton_shape_mapping_preflight`, add:

```python
mapped_subset_newton_shape_mapping = (
    _paper_mapped_subset_newton_shape_mapping_contract_payload(
        mapped_subset_newton_shape_mapping_preflight
    )
)
```

Update:

- top-level `runtime_lane_remaining_gates` to
  `_paper_remaining_gaps_after_mapped_subset_newton_shape_mapping_contract()`;
- top-level `next_required_gate` derived from that list;
- `implemented_output_contract_scope` to include
  `_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT`;
- report dict to include
  `"paper_mapped_subset_newton_shape_mapping_contract": mapped_subset_newton_shape_mapping`.

- [ ] **Step 6: Run GREEN tests**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_mapping_contract' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Expected: both pass.

## Task 3: Update Documentation And Record

**Files:**
- Modify: `README.md`
- Modify: `docs/index.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/deepdive/message-map.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- Modify: `docs/records/README.md`
- Create: `docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-mapping-contract.md`

- [ ] **Step 1: Update current-gate wording**

Replace current top-level mentions that say the next gate is
`paper_mapped_subset_newton_shape_mapping_contract` with
`paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`.

Keep historical/payload-specific mentions intact:

- the preflight payload still points to `paper_mapped_subset_newton_shape_mapping_contract`;
- dated records for prior gates should not be rewritten as if they happened later.

- [ ] **Step 2: Add bounded claim text**

Add wording:

```markdown
The partial `cpd_paper_offline_report` now includes
`paper_mapped_subset_newton_shape_mapping_contract`, a single-fixture offline/static shape
descriptor contract. It consumes the Newton shape-mapping preflight row for synthetic
`paper_single_box`, emits one report-scoped `newton_shape_descriptor_dict` for target kind `box`,
and keeps mapping attempts, Newton mapping records, Newton shape objects, Newton runtime
execution, real-USD asset evidence, benchmark evidence, collision-quality evidence, deployment,
and certification triggers at zero or false.
```

- [ ] **Step 3: Add dated record**

Create:

`docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-mapping-contract.md`

Include:

- date;
- status as implemented pending final verification until final verification is done;
- what changed;
- artifacts;
- claim boundary;
- verification commands with placeholders that are replaced after final verification.

- [ ] **Step 4: Run docs validation**

Run:

```bash
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

## Task 4: Review, Fix, And Final Verification

**Files:**
- Review all touched files.

- [ ] **Step 1: Request multi-agent review**

Dispatch at least two reviewers:

- code/tests reviewer focused on `offline.py`, `tests/test_cpd_paper_offline.py`, and
  `tests/test_cli.py`;
- docs/claim-boundary reviewer focused on the docs and new record.

Reviewers must check:

- no Newton/USD/runtime/benchmark/collision-quality imports or calls;
- no unsupported claim wording;
- correct distinction between preflight payload next gate and top-level current next gate;
- descriptor rows do not copy full package dicts;
- negative tests cover input drift and candidate/descriptor drift.

- [ ] **Step 2: Fix findings**

For each valid finding:

1. verify it against code/docs;
2. patch the smallest affected surface;
3. rerun the narrow relevant test or validator;
4. request re-review if the finding was important.

- [ ] **Step 3: Run final verification**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_mapping_contract' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
PYTHONPATH=src python -m pytest -q
```

Expected: all pass.

- [ ] **Step 4: Update the dated record with final verification**

After final verification, change the new record status to complete in the feature branch and add
the exact final command results.

- [ ] **Step 5: Commit, merge, push, clean**

Commit implementation:

```bash
git add README.md docs/index.md docs/deepdive/evidence-status.md docs/deepdive/message-map.md docs/reference/claim-boundaries.md docs/reference/cpd-paper-faithful-offline-lane-spec.md docs/reference/cpd-paper-reproduction-gap-matrix.md docs/reference/cpd-paper-story-status.md docs/reference/cpd-paper-fixture-breadth-expansion-plan.md docs/records/README.md docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-mapping-contract.md src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cli.py tests/test_cpd_paper_offline.py
git commit -m "feat: add CPD Newton shape-mapping contract"
```

Merge to main from `/cpfs/user/zhuzihou/dev/physics-primitive-agent`:

```bash
git merge --ff-only cpd-paper-newton-shape-mapping-contract
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
git push origin main
git worktree remove /cpfs/user/zhuzihou/dev/physics-primitive-agent/.worktrees/cpd-paper-newton-shape-mapping-contract
git branch -d cpd-paper-newton-shape-mapping-contract
```

Expected: main pushed, worktree removed, local feature branch deleted.
