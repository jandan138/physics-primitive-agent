# CPD Paper Mapped-Subset PrimitiveSpec Native-Fixture Serialization Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a command-only offline gate that validates deterministic JSON serialization and schema
stability for exactly one report-only PrimitiveSpec-like dict.

**Architecture:** Extend the existing CPD paper offline report chain with one verifier/echo payload
after `paper_mapped_subset_primitivespec_native_fixture_generation_contract`. The new payload consumes
the generated report-only dict, validates exact schema and canonical JSON round-trip, and advances
the report to a later runtime-boundary preflight gate without creating runtime objects.

**Tech Stack:** Python, `json`, pytest, existing CPD paper offline report schema, Markdown docs.

---

### Task 1: RED Tests For Serialization Gate

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add serialization constants**

Add constants near the existing native-fixture constants:

```python
EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract"
)

EXPECTED_NATIVE_FIXTURE_SERIALIZATION_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT,
]
```

Change the top-level current output gap expectation from
`EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_SERIALIZATION_CONTRACT` to
`EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT`.

- [ ] **Step 2: Add exact serialization payload key sets**

Add:

```python
NATIVE_FIXTURE_PRIMITIVESPEC_SERIALIZATION_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "paper_faithful_offline_allowed",
    "package_generation_allowed",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "serialization_action",
    "canonical_json_policy",
    "serialized_primitivespec_like_dict_count",
    "json_serialization_check_count",
    "json_round_trip_match_count",
    "schema_stability_check_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "native_fixture_primitivespec_serialization_contract",
    "input_contract_summary",
    "serialization_rows",
    "coverage_summary",
    "remaining_gaps",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}

NATIVE_FIXTURE_PRIMITIVESPEC_SERIALIZATION_ROW_REQUIRED_KEYS = {
    "native_fixture_primitivespec_serialization_row_id",
    "source_native_fixture_primitivespec_generation_row_id",
    "source_native_current_fixture_source_row_id",
    "source_candidate_source_audit_row_id",
    "source_primitivespec_generation_row_id",
    "source_primitivespec_generation_preflight_row_id",
    "source_primitivespec_validation_row_id",
    "source_primitivespec_dry_run_row_id",
    "source_adapter_preflight_row_id",
    "source_candidate_matrix_row_id",
    "source_conversion_plan_row_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "candidate_mapping_label",
    "newton_runtime_kind",
    "primitive_id",
    "kind",
    "schema_keys",
    "serialized_payload",
    "canonical_primitivespec_json",
    "json_allow_nan",
    "json_sort_keys",
    "json_separators",
    "json_round_trip_equal",
    "canonical_json_stable",
    "schema_validation_status",
    "serialization_decision",
    "runtime_instance_generated",
    "generated_primitive_spec",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}
```

- [ ] **Step 3: Add RED gate exposure test**

Add:

```python
def test_cpd_paper_records_mapped_subset_primitivespec_native_fixture_serialization_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report[
        "paper_mapped_subset_primitivespec_native_fixture_serialization_contract"
    ]

    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
    )
    assert report["failure_labels"] == [
        "paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract_missing",
    ]
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_NATIVE_FIXTURE_SERIALIZATION_REMAINING_GAPS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_SERIALIZATION_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_SERIALIZATION_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT
    )
    assert payload["serialized_primitivespec_like_dict_count"] == 1
    assert payload["json_serialization_check_count"] == 1
    assert payload["json_round_trip_match_count"] == 1
    assert payload["schema_stability_check_count"] == 1
    assert payload["generated_runtime_primitive_spec_count"] == 0
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
```

- [ ] **Step 4: Add RED schema and canonical JSON tests**

Add tests that assert:

```python
assert set(payload) == NATIVE_FIXTURE_PRIMITIVESPEC_SERIALIZATION_PAYLOAD_REQUIRED_KEYS
assert payload["canonical_json_policy"] == {
    "json_allow_nan": False,
    "json_sort_keys": True,
    "json_separators": [",", ":"],
}
row = payload["serialization_rows"][0]
assert set(row) == NATIVE_FIXTURE_PRIMITIVESPEC_SERIALIZATION_ROW_REQUIRED_KEYS
spec = row["serialized_payload"]
expected_json = json.dumps(
    spec,
    allow_nan=False,
    sort_keys=True,
    separators=(",", ":"),
)
assert row["canonical_primitivespec_json"] == expected_json
assert json.loads(row["canonical_primitivespec_json"]) == spec
assert row["json_round_trip_equal"] is True
assert row["canonical_json_stable"] is True
for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
    assert payload[flag] is False
    assert row[flag] is False
```

Build the report twice and assert the canonical JSON string is byte-identical across both reports.

- [ ] **Step 5: Add RED malformed-input tests**

Call the new private builder directly:

```python
cpd_paper_offline._paper_mapped_subset_primitivespec_native_fixture_serialization_contract_payload(
    native_fixture_generation
)
```

Cover:

- wrong input gate -> `primitivespec_native_fixture_serialization_input_gate_id_mismatch`;
- stale input next gate -> `primitivespec_native_fixture_serialization_input_next_gate_mismatch`;
- zero or duplicate generation rows -> `primitivespec_native_fixture_serialization_generation_row_count_mismatch`;
- wrong fixture -> `primitivespec_native_fixture_serialization_source_fixture_mismatch`;
- wrong kind -> `primitivespec_native_fixture_serialization_source_kind_mismatch`;
- missing dict -> `primitivespec_native_fixture_serialization_missing_payload`;
- missing/extra dict key -> `primitivespec_native_fixture_serialization_payload_schema_mismatch`;
- drifted dict value -> `primitivespec_native_fixture_serialization_payload_field_drift`;
- NaN/Infinity -> `primitivespec_native_fixture_serialization_non_strict_json`;
- runtime/package/Newton flag leak -> `primitivespec_native_fixture_serialization_input_trigger_flag_true:<flag>`.

- [ ] **Step 6: Add CLI RED assertions**

Extend `test_cli_run_cpd_paper_offline_report_emits_json()` to assert the new nested payload exists,
the canonical JSON string round-trips to `serialized_payload`, and the top-level next gate/failure
label have advanced to runtime-boundary preflight.

Add a separate CLI determinism test that runs `cli.main(["--run-cpd-paper-offline-report"])` twice
and asserts the nested `canonical_primitivespec_json` string is byte-identical across both CLI
outputs.

- [ ] **Step 7: Run RED commands**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'native_fixture_serialization or native_fixture_generation' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Expected: new serialization tests fail with missing payload/helper errors; existing
native-fixture-generation tests still pass.

### Task 2: Production Serialization Builder

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add constants and remaining-gap helper**

Add:

```python
_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract"
)
```

Add:

```python
def _paper_remaining_gaps_after_mapped_subset_primitivespec_native_fixture_serialization() -> list[str]:
    return [
        _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
    ]
```

- [ ] **Step 2: Add canonical JSON helper**

Add:

```python
def _paper_primitivespec_native_fixture_canonical_json(
    payload: dict[str, object],
) -> str:
    try:
        return json.dumps(
            payload,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "primitivespec_native_fixture_serialization_non_strict_json"
        ) from exc
```

`json` is already available in the test layer; import it in `offline.py` if not already imported.

- [ ] **Step 3: Add input and row validators**

Validate the input generation payload:

- `gate_id`;
- `next_required_gate`;
- false runtime/package/evaluation flags;
- counts of one serialized dict and zero runtime/package/admissibility artifacts;
- exactly one `native_fixture_primitivespec_generation_rows` row.

Validate the row:

- `fixture_id == paper_single_box`;
- `paper_primitive == oriented_bounding_box`;
- `primitive_spec_kind == box`;
- `candidate_mapping_label == box`;
- `newton_runtime_kind == box`;
- `generated_primitive_spec is None`;
- `runtime_instance_generated is False`;
- `offline_serialized_primitivespec_like_dict` is a dict.

- [ ] **Step 4: Add serialized dict validator**

Validate exact keys and expected field values:

```python
expected_payload = {
    "primitive_id": "paper_single_box__oriented_bounding_box__box",
    "kind": "box",
    "pose": [],
    "center": row["center"],
    "axes": row["axes"],
    "dimensions": {"half_extents": row["half_extents"]},
    "frame": "asset",
    "source_faces": row["fixture_source_faces"],
    "contains_assigned_points": row["contains_assigned_points"],
    "volume": row["volume"],
    "weighted_volume": row["weighted_volume"],
    "conversion_status": (
        "report_only_offline_serialized_primitivespec_like_dict_not_runtime_object"
    ),
}
```

Raise schema mismatch for key drift and field drift for value drift.

- [ ] **Step 5: Add serialization row builder**

Build one row with:

```python
{
    "native_fixture_primitivespec_serialization_row_id": (
        "native_fixture_primitivespec_serialization__paper_single_box__"
        "oriented_bounding_box__box"
    ),
    "source_native_fixture_primitivespec_generation_row_id": row[
        "native_fixture_primitivespec_generation_row_id"
    ],
    "primitive_id": spec["primitive_id"],
    "kind": spec["kind"],
    "schema_keys": sorted(spec),
    "serialized_payload": spec,
    "canonical_primitivespec_json": canonical_json,
    "json_allow_nan": False,
    "json_sort_keys": True,
    "json_separators": [",", ":"],
    "json_round_trip_equal": json.loads(canonical_json) == spec,
    "canonical_json_stable": True,
    "schema_validation_status": "passed",
    "serialization_decision": (
        "report_only_primitivespec_like_dict_canonical_json_round_trip_passed"
    ),
    "runtime_instance_generated": False,
    "generated_primitive_spec": None,
    **_paper_false_primitivespec_generation_flags(),
}
```

Include the source ids already present on the generation row.

- [ ] **Step 6: Add payload builder and wire report chain**

Add `_paper_mapped_subset_primitivespec_native_fixture_serialization_contract_payload()` and insert it
after the native-fixture generation payload inside `build_cpd_paper_offline_report()`.

Update:

- top-level `next_required_gate`;
- top-level `failure_labels`;
- `paper_faithfulness["missing_before_paper_faithful_offline"]`;
- `paper_faithfulness["implemented_output_contract_scope"]`;
- top-level payload key.

- [ ] **Step 7: Run GREEN commands**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'native_fixture_serialization or native_fixture_generation' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Expected: all selected tests pass.

### Task 3: Documentation And Registry

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
- Modify: `experiments/registry.yaml`
- Create: `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-native-fixture-serialization-contract.md`

- [ ] **Step 1: Update current story wording**

Say this slice validates deterministic serialization/schema stability for one report-only
PrimitiveSpec-like dict. It does not create a runtime PrimitiveSpec object.

- [ ] **Step 2: Update next gate wording**

Set the current next gate to
`paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`, with explicit wording
that this next gate is still preflight and not runtime construction.

- [ ] **Step 3: Add dated record and registry entry**

Record command, scope, evidence fields, exact nonclaims, and next gate.

- [ ] **Step 4: Run docs validation**

Run:

```bash
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

### Task 4: Multi-Agent Review, Verification, Commit

**Files:**
- All changed files

- [ ] **Step 1: Request implementation review**

Ask a read-only reviewer to inspect the serialization builder, validators, tests, and CLI assertions.

- [ ] **Step 2: Request docs/claim review**

Ask a read-only reviewer to inspect docs and claim boundaries for runtime/package/Newton overclaiming.

- [ ] **Step 3: Request hygiene review**

Ask a read-only reviewer to inspect registry/records, staged files, ignored artifacts, and worktree
hygiene.

- [ ] **Step 4: Fix review findings with TDD**

For any implementation finding, add or adjust a failing test first, run it RED, then implement the
fix and run it GREEN.

- [ ] **Step 5: Run full verification**

Run:

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
PYTHONPATH=src python -m py_compile src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cpd_paper_offline.py tests/test_cli.py
```

Expected: all pass.

- [ ] **Step 6: Commit**

Commit with:

```bash
git add README.md docs experiments src tests
git commit -m "feat: add CPD native fixture PrimitiveSpec serialization contract"
```
