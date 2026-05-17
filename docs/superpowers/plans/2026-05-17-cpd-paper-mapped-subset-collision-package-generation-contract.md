# CPD Paper Mapped-Subset CollisionPackage Generation Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement `paper_mapped_subset_collision_package_generation_contract` as a single-fixture offline package artifact gate.

**Architecture:** Extend the existing command-only `cpd_paper_offline_report` chain after the package-generation preflight gate. Construct one `PrimitiveSpec` and one `CollisionPackage`, store exactly one `CollisionPackage.to_dict()` artifact at `collision_package_generation_rows[0]["generated_collision_package"]`, and advance the next gate to `paper_mapped_subset_runtime_admissibility_preflight_contract` while keeping runtime/Newton/real-USD/benchmark/quality triggers false.

**Tech Stack:** Python dataclasses in `src/primitive_collision_compiler/contracts.py`, report builders in `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`, pytest, Markdown docs.

---

### Task 1: Add RED Tests For The New Gate

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add expected gate and flag constants**

Add gate constants near the existing CPD paper gate constants:

```python
EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT = (
    "paper_mapped_subset_collision_package_generation_contract"
)
EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_runtime_admissibility_preflight_contract"
)
EXPECTED_COLLISION_PACKAGE_GENERATION_CONTRACT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT,
]
```

Add flag constants after `RUNTIME_CONSTRUCTION_FALSE_FLAGS` is defined:

```python
EXPECTED_COLLISION_PACKAGE_GENERATION_ALLOWED_TRUE_FLAGS = (
    "collision_package_generated",
    "package_generation_allowed",
    "collision_package_generation_allowed",
    "package_generation_triggered",
    "collision_package_generation_triggered",
)
EXPECTED_COLLISION_PACKAGE_GENERATION_BOUNDARY_FALSE_FLAGS = tuple(
    flag
    for flag in RUNTIME_CONSTRUCTION_FALSE_FLAGS
    if flag not in EXPECTED_COLLISION_PACKAGE_GENERATION_ALLOWED_TRUE_FLAGS
)
```

- [ ] **Step 2: Add report-level RED assertions**

Update the existing report-level tests so they expect:

```python
assert report["next_required_gate"] == (
    EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT
)
assert report["failure_labels"] == [
    f"{EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT}_missing"
]
assert report["generated_collision_package_count"] == 1
assert report["runtime_admissibility_check_count"] == 0
```

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'next_gate or collision_package_generation_contract' -q
```

Expected: fail because the new gate does not exist and the report still points to
`paper_mapped_subset_collision_package_generation_contract`.

- [ ] **Step 3: Add payload schema/count RED test**

Add a test named:

```python
def test_cpd_paper_collision_package_generation_contract_schema_and_counts():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_collision_package_generation_contract"]
    assert payload["gate_id"] == EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
    assert payload["input_gate_id"] == EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT
    assert payload["next_required_gate"] == EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT
    assert payload["generated_collision_package_count"] == 1
    assert payload["runtime_admissibility_check_count"] == 0
    assert payload["collision_package_generated"] is True
    assert payload["package_generation_allowed"] is True
    assert payload["collision_package_generation_allowed"] is True
    assert payload["package_generation_triggered"] is True
    assert payload["collision_package_generation_triggered"] is True
    assert payload["runtime_admissibility_checked"] is False
    assert payload["runtime_admissibility_triggered"] is False
    assert payload["runtime_admissibility_supported"] is False
    assert payload["newton_support_claimed"] is False
    assert payload["newton_runtime_allowed"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_loaded"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_run"] is False
    assert payload["benchmark_triggered"] is False
    assert payload["collision_quality_measured"] is False
    assert payload["deployment_or_certification_claimed"] is False
    assert payload["approximation_policy_applied"] is False
    assert payload["approximation_policy_enabled"] is False
    assert payload["silent_drop_allowed"] is False
```

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_collision_package_generation_contract_schema_and_counts -q
```

Expected: fail with missing key.

- [ ] **Step 4: Add package artifact RED test**

Add a test named:

```python
def test_cpd_paper_collision_package_generation_contract_records_one_package_dict():
    report = build_cpd_paper_offline_report()
    preflight_row = report[
        "paper_mapped_subset_collision_package_generation_preflight_contract"
    ]["package_generation_preflight_rows"][0]
    payload = report["paper_mapped_subset_collision_package_generation_contract"]
    rows = payload["collision_package_generation_rows"]
    assert len(rows) == 1
    row = rows[0]
    package = row["generated_collision_package"]
    assert package["package_id"] == (
        "paper_single_box:paper_mapped_subset_collision_package_generation_contract"
    )
    assert package["asset_id"] == "paper_single_box"
    assert package["source_path"] == "synthetic://cpd-paper/paper_single_box"
    assert package["method"] == "cpd_paper_mapped_subset_offline"
    assert package["stage"] == EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
    assert package["status"] == "offline_synthetic_candidate_runtime_admissibility_not_checked"
    assert package["claim_boundary"] == (
        "single_fixture_box_only_offline_collision_package_artifact_"
        "not_paper_vocabulary_runtime_admissibility_or_newton"
    )
    assert package["mesh_point_count"] == 8
    assert package["mesh_face_count"] == 12
    assert package["max_source_faces"] == 12
    assert package["primitive_subset"] == ["box"]
    assert package["unsupported_primitives"] == []
    assert package["fallback"] is None
    assert "not_paper_vocabulary" in package["claim_boundary"]
    assert package["primitives"] == [preflight_row["candidate_primitivespec_dict"]]
    assert row["unsupported_primitives_in_this_single_fixture"] == []
    assert row["primitive_families_not_evaluated_by_this_gate"] == [
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
```

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_collision_package_generation_contract_records_one_package_dict -q
```

Expected: fail with missing key.

- [ ] **Step 5: Add single-storage, manifest, and boundary RED tests**

Add helpers and tests:

```python
def _recursive_package_dicts(value):
    if isinstance(value, dict):
        if {
            "package_id",
            "asset_id",
            "source_path",
            "source_sha256",
            "primitives",
            "fallback",
        }.issubset(value):
            yield value
        for nested in value.values():
            yield from _recursive_package_dicts(nested)
    elif isinstance(value, list | tuple):
        for nested in value:
            yield from _recursive_package_dicts(nested)


def test_cpd_paper_collision_package_generation_contract_stores_package_dict_once():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_collision_package_generation_contract"
    ]
    packages = list(_recursive_package_dicts(payload))
    assert len(packages) == 1
    assert packages[0] is payload["collision_package_generation_rows"][0][
        "generated_collision_package"
    ]


def test_cpd_paper_collision_package_generation_contract_source_manifest_sha_is_exact():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_collision_package_generation_contract"
    ]
    row = payload["collision_package_generation_rows"][0]
    package = row["generated_collision_package"]
    expected_manifest = {
        "contract_gate": "paper_mapped_subset_collision_package_generation_contract",
        "fixture_id": "paper_single_box",
        "fixture_scope": "synthetic_toy_mesh",
        "mesh_face_count": 12,
        "mesh_point_count": 8,
        "primitive_id": "paper_single_box__oriented_bounding_box__box",
        "primitive_kind": "box",
        "source_faces": list(range(12)),
    }
    expected_json = json.dumps(
        expected_manifest,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    assert row["synthetic_source_manifest"] == expected_manifest
    assert row["synthetic_source_manifest_canonical_json"] == expected_json
    assert package["source_sha256"] == hashlib.sha256(
        expected_json.encode("utf-8")
    ).hexdigest()


@pytest.mark.parametrize(
    "field_name", EXPECTED_COLLISION_PACKAGE_GENERATION_ALLOWED_TRUE_FLAGS
)
def test_cpd_paper_collision_package_generation_contract_allowed_package_flags_are_true(
    field_name,
):
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_collision_package_generation_contract"
    ]
    assert payload[field_name] is True
    assert payload["collision_package_generation_rows"][0][field_name] is True


@pytest.mark.parametrize("field_name", EXPECTED_COLLISION_PACKAGE_GENERATION_BOUNDARY_FALSE_FLAGS)
def test_cpd_paper_collision_package_generation_contract_boundary_flags_stay_false(
    field_name,
):
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_collision_package_generation_contract"
    ]
    assert payload[field_name] is False
    assert payload["collision_package_generation_rows"][0][field_name] is False
```

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'collision_package_generation_contract and (stores_package_dict_once or source_manifest_sha_is_exact or boundary_flags or allowed_package_flags)' -q
```

Expected: fail with missing key.

- [ ] **Step 6: Add malformed input RED tests**

Add tests that call
`_paper_mapped_subset_collision_package_generation_contract_payload()` directly and assert
`ValueError` for:

```python
preflight["gate_id"] = "wrong_gate"
preflight["next_required_gate"] = "wrong_next_gate"
preflight["later_collision_package_generation_candidate_count"] = 0
preflight["generated_collision_package_count"] = 1
preflight["runtime_admissibility_check_count"] = 1
preflight["package_generation_preflight_rows"] = []
preflight["package_generation_preflight_rows"][0]["later_collision_package_generation_candidate"] = False
preflight["package_generation_preflight_rows"][0]["package_generation_allowed_in_current_gate"] = True
preflight["package_generation_preflight_rows"][0]["source_candidate_matrix_row_id"] = "wrong"
preflight["package_generation_preflight_rows"][0]["constructed_primitivespec_dict"]["kind"] = "sphere"
preflight["package_generation_preflight_rows"][0]["generated_primitive_spec"]["kind"] = "sphere"
preflight["package_generation_preflight_rows"][0]["candidate_primitivespec_dict"]["kind"] = "sphere"
preflight["package_generation_preflight_rows"][0]["candidate_primitivespec_dict"]["dimensions"] = {"half_extents": [0.5, 0.5]}
preflight["package_generation_preflight_rows"][0]["newton_runtime_triggered"] = True
preflight["package_generation_preflight_rows"][0]["runtime_admissibility_triggered"] = True
```

Also add parametrized rejection tests over every `RUNTIME_CONSTRUCTION_FALSE_FLAGS` member for the
input payload and for the single preflight row:

```python
@pytest.mark.parametrize("field_name", RUNTIME_CONSTRUCTION_FALSE_FLAGS)
def test_cpd_paper_collision_package_generation_contract_rejects_input_forbidden_flags(
    field_name,
):
    preflight = _collision_package_generation_contract_input()
    preflight[field_name] = True
    with pytest.raises(ValueError, match=f"collision_package_generation_contract_input_trigger_flag_true:{field_name}"):
        cpd_paper_offline._paper_mapped_subset_collision_package_generation_contract_payload(
            preflight
        )


@pytest.mark.parametrize("field_name", RUNTIME_CONSTRUCTION_FALSE_FLAGS)
def test_cpd_paper_collision_package_generation_contract_rejects_row_forbidden_flags(
    field_name,
):
    preflight = _collision_package_generation_contract_input()
    rows = [dict(row) for row in preflight["package_generation_preflight_rows"]]
    rows[0][field_name] = True
    preflight["package_generation_preflight_rows"] = rows
    with pytest.raises(ValueError, match=f"collision_package_generation_contract_input_trigger_flag_true:{field_name}"):
        cpd_paper_offline._paper_mapped_subset_collision_package_generation_contract_payload(
            preflight
        )
```

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'collision_package_generation_contract and rejects' -q
```

Expected: fail because the implementation function does not exist.

- [ ] **Step 7: Update static-boundary RED tests for the new executable package gate**

Update `test_cpd_paper_primitivespec_runtime_construction_static_boundaries` so its source slice
ends at `_COLLISION_PACKAGE_GENERATION_PREFLIGHT_PAYLOAD_FALSE_FLAGS`, not at
`def _paper_source_policy_generalization_payload`. Update
`test_cpd_paper_collision_package_generation_preflight_static_boundaries` so its source slice ends
at `_COLLISION_PACKAGE_GENERATION_CONTRACT_PAYLOAD_TRUE_FLAGS`.

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'static_boundaries and (runtime_construction or collision_package_generation_preflight)' -q
```

Expected: fail until the new `_COLLISION_PACKAGE_GENERATION_CONTRACT_PAYLOAD_TRUE_FLAGS` sentinel
exists.

### Task 2: Implement The Package Generation Gate

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add constants**

Add:

```python
_PAPER_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_runtime_admissibility_preflight_contract"
)
_RUNTIME_ADMISSIBILITY_PREFLIGHT_MISSING_GAPS = [
    _PAPER_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT
]
_PAPER_COLLISION_PACKAGE_GENERATION_CLAIM_BOUNDARY = (
    "single_fixture_box_only_offline_collision_package_artifact_"
    "not_paper_vocabulary_runtime_admissibility_or_newton"
)
_PAPER_COLLISION_PACKAGE_GENERATION_NOT_EVALUATED_PRIMITIVE_FAMILIES = (
    "sphere",
    "capsule",
    "capped_cylinder",
    "frustum",
    "trapezoidal_prism",
)
_COLLISION_PACKAGE_GENERATION_CONTRACT_PAYLOAD_TRUE_FLAGS = (
    "collision_package_generated",
    "package_generation_allowed",
    "collision_package_generation_allowed",
    "package_generation_triggered",
    "collision_package_generation_triggered",
)
```

Place `_COLLISION_PACKAGE_GENERATION_CONTRACT_PAYLOAD_TRUE_FLAGS` immediately before the new
package-generation contract block so the existing preflight static-boundary test can use it as a
stable end sentinel.

- [ ] **Step 2: Add source-row validator**

Add `_paper_collision_package_generation_source_row(preflight)` as the single validator for this
gate. It must validate the input gate, next gate, all preflight false boundary flags, counts, one
row, candidate flag, package-generation disallowed flag, runtime-admissibility false flag, anchored
lineage fields, generated primitive dict, constructed primitive dict, and candidate
`PrimitiveSpec.to_dict()` equality with the preflight row. It must recompute the deterministic
preflight anchor with `_paper_collision_package_generation_preflight_expected_source_row()` and
`_paper_collision_package_generation_preflight_row(expected_source_row)`, then compare every
persisted preflight row field against that expected preflight row. Canonical JSON and loaded-payload
drift remain enforced by the previous preflight/runtime-construction gates because the preflight
row does not persist those source fields.

- [ ] **Step 3: Add package builders**

Add helpers:

```python
def _paper_collision_package_generation_source_manifest(row: dict[str, object]) -> dict[str, object]:
    return {
        "contract_gate": "paper_mapped_subset_collision_package_generation_contract",
        "fixture_id": "paper_single_box",
        "fixture_scope": "synthetic_toy_mesh",
        "mesh_face_count": 12,
        "mesh_point_count": 8,
        "primitive_id": row["primitive_id"],
        "primitive_kind": "box",
        "source_faces": row["candidate_primitivespec_dict"]["source_faces"],
    }

```

Add `_paper_runtime_primitivespec_from_dict(payload)` so it calls
`_paper_validate_primitivespec_runtime_construction_payload_shape(payload)`, constructs the
`PrimitiveSpec` dataclass, and asserts `primitive.to_dict() == payload` before returning. Add
`_paper_collision_package_from_preflight_row(row)` so it builds one `CollisionPackage` using the
manifest SHA and `_PAPER_COLLISION_PACKAGE_GENERATION_CLAIM_BOUNDARY`. Use
`CollisionPackage.to_dict()` for the report artifact.

- [ ] **Step 4: Add row, coverage, payload functions**

Add `_paper_collision_package_generation_row(row)`,
`_paper_collision_package_generation_coverage_summary(rows)`, and
`_paper_mapped_subset_collision_package_generation_contract_payload(preflight)`.
The payload must include `generated_collision_package_count: 1`,
`runtime_admissibility_check_count: 0`, no payload-level copy of the package dict, and
`remaining_gaps: ["paper_mapped_subset_runtime_admissibility_preflight_contract"]`.
The only package-shaped dict in the payload must be
`collision_package_generation_rows[0]["generated_collision_package"]`.

- [ ] **Step 5: Wire into `build_cpd_paper_offline_report()`**

After `mapped_subset_collision_package_generation_preflight`, call the new payload and set:

```python
missing_before_paper_faithful = [
    _PAPER_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT
]
```

Add the new payload to the returned report dict, update report-level counts, and append
`_PAPER_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT` to
`paper_faithfulness["implemented_output_contract_scope"]`.

- [ ] **Step 6: Run GREEN tests**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'collision_package_generation_contract or collision_package_generation_preflight or runtime_construction' -q
```

Expected: pass.

### Task 3: Update CLI Assertions

**Files:**
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Update CLI report expectations**

Update `test_cli_run_cpd_paper_offline_report_emits_json` to expect:

```python
payload["next_required_gate"] == "paper_mapped_subset_runtime_admissibility_preflight_contract"
payload["failure_labels"] == [
    "paper_mapped_subset_runtime_admissibility_preflight_contract_missing"
]
payload["generated_collision_package_count"] == 1
payload["runtime_admissibility_check_count"] == 0
```

Assert the new nested key exists and the package dict mirrors the offline test.
Also assert `paper_mapped_subset_collision_package_generation_contract` appears in
`payload["paper_faithfulness"]["implemented_output_contract_scope"]`.

- [ ] **Step 2: Run CLI focused test**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Expected: pass.

### Task 4: Update Documentation And Record

**Files:**
- Modify: `README.md`
- Modify: `docs/index.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/deepdive/message-map.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/records/README.md`
- Create: `docs/records/2026-05-17-cpd-paper-mapped-subset-collision-package-generation-contract.md`

- [ ] **Step 1: Update current next gate wording**

Replace current-gate references from
`paper_mapped_subset_collision_package_generation_contract` to
`paper_mapped_subset_runtime_admissibility_preflight_contract` where they refer to current state.

- [ ] **Step 2: Add bounded package-artifact wording**

Use the phrase:

```text
single-fixture offline CollisionPackage.to_dict() artifact
```

and explicitly pair it with:

```text
not runtime admissibility, not Newton execution, not real-USD evidence, not benchmark evidence,
not collision-quality evidence, not package readiness, not full CPD reproduction, not deployment
readiness, not safety certification, not paper primitive vocabulary coverage
```

- [ ] **Step 3: Add dated record**

The record must include:

- gate id and date;
- one generated `CollisionPackage.to_dict()` artifact;
- generated package count one;
- runtime-admissibility check count zero;
- Newton/real-USD/benchmark/collision-quality/deployment/safety and paper primitive vocabulary
  coverage unsupported;
- commands run and review notes;
- next gate `paper_mapped_subset_runtime_admissibility_preflight_contract`.

- [ ] **Step 4: Run doc validators**

Run:

```bash
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

### Task 5: Review, Full Verification, Commit, Merge

**Files:**
- All modified files.

- [ ] **Step 1: Request code and docs reviews**

Dispatch at least two agents:

- code/test reviewer for `offline.py`, `tests/test_cpd_paper_offline.py`, `tests/test_cli.py`;
- docs/claim-boundary reviewer for all docs and record changes.

- [ ] **Step 2: Address review feedback using TDD**

For every valid bug:

1. write a failing test;
2. run it and see it fail;
3. implement the minimal fix;
4. rerun focused tests.

- [ ] **Step 3: Run full verification**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
PYTHONPATH=src python -m pytest tests/test_cpd_paper_importer.py::test_imported_experiment_translation_ids_stay_semantically_aligned -q
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass. If the importer test fails because ignored paper source is absent, sync
`docs/tmp/papers/arXiv-2602.07369v1/` from the main workspace and rerun.

- [ ] **Step 4: Commit**

Run:

```bash
git add README.md docs src tests
git commit -m "feat: add CPD CollisionPackage generation contract"
```

- [ ] **Step 5: Merge and push**

Fast-forward merge to `main`, rerun focused and full verification on `main`, push `origin main`,
then remove the feature worktree and branch.
