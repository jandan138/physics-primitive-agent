# CPD Paper Newton Engine-Builder Entry Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [x]`) syntax for tracking.

**Goal:** Add the consolidated report-only Newton engine-builder entry contract after the
API-surface contract.

**Architecture:** Extend the existing `cpd_paper_offline_report` gate chain by adding one payload
builder after the API-surface payload. Keep the slice offline/report-only, validate the upstream
API-surface lineage, and advance the next runtime-lane gap to a future smoke contract.

**Tech Stack:** Python, pytest, existing dict-contract helpers, Markdown records.

---

### Task 1: Entry Contract Report Payload

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [x] **Step 1: Write failing tests**

Add tests near the API-surface tests:

```python
def test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_entry_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"
    ]

    assert report["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"
    )
    assert report["failure_labels"] == [
        "paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract_missing"
    ]
    assert payload["gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"
    )
    assert payload["input_gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"
    )
    assert payload["entry_decision"] == "defer_real_runtime_entry"
    assert payload["runtime_entry_allowed_count"] == 0
    assert payload["runtime_entry_attempted_count"] == 0
    assert payload["real_newton_import_count"] == 0
    assert payload["real_warp_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_collision_pipeline_created_count"] == 0
    assert payload["newton_collision_pipeline_collide_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
```

- [x] **Step 2: Verify RED**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_entry_contract_gate -q
```

Expected: fail because the entry payload key does not exist.

- [x] **Step 3: Implement minimal payload**

Add constants for:

```python
_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"
)
```

Add helper functions that consume the API-surface payload, build one entry row, return a payload,
and wire the payload into `build_cpd_paper_offline_report()`.

- [x] **Step 4: Verify GREEN**

Run the same pytest command and expect pass.

### Task 2: Exact Schema, Drift, And Static Boundary

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [x] **Step 1: Write failing tests**

Add exact-schema and boundary tests:

```python
def test_cpd_paper_newton_shape_runtime_engine_builder_entry_payload_schema_is_exact():
    report = build_cpd_paper_offline_report()
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"
    ]

    assert set(payload) == NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_PAYLOAD_REQUIRED_KEYS
    assert payload["schema_version"] == 1
    assert payload["gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"
    )
    assert payload["closed_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"
    )
    assert payload["input_gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"
    )
    assert payload["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"
    )
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_engine_builder_entry_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_engine_builder_entry_recorded_smoke_contract_missing"
    )
    assert payload["entry_contract"]["real_runtime_import_allowed"] is False
    assert payload["entry_contract"]["newton_model_builder_allowed"] is False
    assert payload["entry_contract"]["newton_builder_shape_call_allowed"] is False
    assert payload["entry_contract"]["newton_model_finalize_allowed"] is False
    assert payload["entry_contract"]["newton_collision_pipeline_allowed"] is False
    assert payload["entry_contract"]["newton_runtime_allowed"] is False
    assert payload["real_newton_import_count"] == 0
    assert payload["real_warp_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_collision_pipeline_created_count"] == 0
    assert payload["newton_collision_pipeline_collide_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["newton_shape_runtime_engine_builder_entry_row_count"] == 1
    assert len(payload["newton_shape_runtime_engine_builder_entry_rows"]) == 1
    assert payload["remaining_gaps"] == [
        "paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"
    ]
    assert set(payload["coverage_summary"]) == {
        "newton_shape_runtime_engine_builder_entry_row_count",
        "source_newton_shape_runtime_engine_builder_api_surface_row_count",
        "runtime_entry_allowed_count",
        "runtime_entry_attempted_count",
        "real_newton_import_count",
        "real_warp_import_count",
        "newton_model_builder_instantiated_count",
        "newton_builder_shape_call_count",
        "newton_model_finalized_count",
        "newton_collision_pipeline_created_count",
        "newton_collision_pipeline_collide_count",
        "newton_runtime_execution_count",
        "entry_decision_distribution",
    }
    row = payload["newton_shape_runtime_engine_builder_entry_rows"][0]
    assert set(row) == NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_ROW_REQUIRED_KEYS
    assert row["runtime_entry_allowed"] is False
    assert row["runtime_entry_attempted"] is False
    assert row["source_package_copy_forbidden"] is True
    assert row["real_newton_import_count"] == 0
    assert row["real_warp_import_count"] == 0
    assert row["newton_model_builder_instantiated_count"] == 0
    assert row["newton_builder_shape_call_count"] == 0
    assert row["newton_model_finalized_count"] == 0
    assert row["newton_collision_pipeline_created_count"] == 0
    assert row["newton_collision_pipeline_collide_count"] == 0
    assert row["newton_runtime_execution_count"] == 0
```

Define exact key-set constants in the test file before using them:

```python
NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_PAYLOAD_REQUIRED_KEYS = {
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
    "entry_action",
    "entry_decision",
    "entry_contract",
    "input_contract_summary",
    "newton_shape_runtime_engine_builder_entry_row_count",
    "source_newton_shape_runtime_engine_builder_api_surface_row_count",
    "runtime_entry_allowed_count",
    "runtime_entry_attempted_count",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
    "newton_shape_runtime_engine_builder_entry_rows",
    "coverage_summary",
    "remaining_gaps",
    "real_runtime_import_allowed",
    "newton_model_builder_allowed",
    "newton_engine_shape_object_allowed",
    "newton_builder_shape_call_allowed",
    "newton_model_finalize_allowed",
    "newton_collision_pipeline_allowed",
    "newton_runtime_allowed",
    "newton_support_claim_allowed",
    "newton_shape_runtime_engine_builder_entry_recorded",
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_ROW_REQUIRED_KEYS = {
    "newton_shape_runtime_engine_builder_entry_row_id",
    "source_newton_shape_runtime_engine_builder_api_surface_row_id",
    "source_newton_shape_runtime_engine_builder_environment_probe_row_id",
    "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id",
    "source_shape_mapping_row_id",
    "source_package_id",
    "source_asset_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "primitive_id",
    "target_newton_shape_kind",
    "entry_decision",
    "entry_decision_reason",
    "future_newton_builder_constructor_name",
    "future_newton_builder_method_name",
    "future_runtime_module_names",
    "api_surface_probe_status",
    "runtime_entry_allowed",
    "runtime_entry_attempted",
    "source_package_copy_forbidden",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
}
```

Add drift tests that mutate the API-surface input and expect `ValueError`:

```python
@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("gate_id", "stale_gate", "entry_input_gate_id_mismatch"),
        ("next_required_gate", "stale_gate", "entry_input_next_gate_mismatch"),
        ("real_newton_import_count", 1, "entry_input_count_mismatch"),
        ("real_warp_import_count", 1, "entry_input_count_mismatch"),
        ("newton_model_builder_instantiated_count", 1, "entry_input_count_mismatch"),
        ("newton_builder_shape_call_count", 1, "entry_input_count_mismatch"),
        ("newton_model_finalized_count", 1, "entry_input_count_mismatch"),
        ("newton_collision_pipeline_created_count", 1, "entry_input_count_mismatch"),
        ("newton_collision_pipeline_collide_count", 1, "entry_input_count_mismatch"),
        ("newton_runtime_execution_count", 1, "entry_input_count_mismatch"),
        ("real_runtime_import_allowed", True, "entry_input_flag_true"),
        ("newton_model_builder_allowed", True, "entry_input_flag_true"),
        ("newton_builder_shape_call_allowed", True, "entry_input_flag_true"),
        ("newton_runtime_allowed", True, "entry_input_flag_true"),
        ("newton_shape_runtime_engine_builder_api_surface_recorded", False, "entry_input_flag_false"),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_entry_rejects_input_drift(field, value, message):
    report = build_cpd_paper_offline_report()
    api_surface = copy.deepcopy(
        report["paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"]
    )
    api_surface[field] = value

    with pytest.raises(ValueError, match=message):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract_payload(api_surface)


def test_cpd_paper_newton_shape_runtime_engine_builder_entry_rejects_source_row_drift_and_copies():
    report = build_cpd_paper_offline_report()
    api_surface = copy.deepcopy(
        report["paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"]
    )

    api_surface["newton_shape_runtime_engine_builder_api_surface_rows"] = []
    with pytest.raises(ValueError, match="entry_row_count_mismatch"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract_payload(api_surface)

    api_surface = copy.deepcopy(
        report["paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"]
    )
    api_surface["newton_shape_runtime_engine_builder_api_surface_rows"][0]["source_package_id"] = "stale_package"
    with pytest.raises(ValueError, match="entry_source_row_mismatch"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract_payload(api_surface)

    api_surface = copy.deepcopy(
        report["paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"]
    )
    api_surface["newton_shape_runtime_engine_builder_api_surface_rows"][0]["source_package"] = {}
    with pytest.raises(ValueError, match="entry_source_package_copy_forbidden"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract_payload(api_surface)
```

Add a static-boundary test that parses this exact helper tuple:

```python
entry_helpers = [
    cpd_paper_offline._paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_engine_builder_entry,
    cpd_paper_offline._paper_newton_shape_runtime_engine_builder_entry_false_flags,
    cpd_paper_offline._paper_newton_shape_runtime_engine_builder_entry_true_flags,
    cpd_paper_offline._paper_newton_shape_runtime_engine_builder_entry_source_row,
    cpd_paper_offline._paper_newton_shape_runtime_engine_builder_entry_row,
    cpd_paper_offline._paper_newton_shape_runtime_engine_builder_entry_coverage_summary,
    cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract_payload,
]
```

It must use AST checks for forbidden import roots `{ "newton", "warp" }`, forbidden
`ImportFrom` roots `{ "newton", "warp" }`, and forbidden call names/attrs:

```text
ModelBuilder
add_shape_box
finalize
CollisionPipeline
collide
import_module
__import__
module_from_spec
exec_module
inspect_newton_environment
run_newton_contact_smoke
run_newton_drop_settle
run_newton_sphere_rain
```

- [x] **Step 2: Verify RED**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "engine_builder_entry" -q
```

Expected: fail until the exact payload, drift validation, and static boundary exist.

- [x] **Step 3: Implement validation and schema**

Add source-row validation that requires:

- API-surface gate ID matches;
- API-surface next gate is the entry contract;
- exactly one API-surface row exists;
- upstream runtime counters remain zero;
- upstream support/runtime flags remain false;
- no source package copy is present.

- [x] **Step 4: Verify GREEN**

Run the same pytest command and expect pass.

### Task 3: CLI And Documentation

**Files:**

- Modify: `tests/test_cli.py`
- Modify: `README.md`
- Modify: `docs/index.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/deepdive/message-map.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/records/README.md`
- Create: `docs/records/2026-05-19-cpd-paper-newton-engine-builder-entry-contract.md`

- [x] **Step 1: Write failing CLI test updates**

Update `test_cli_run_cpd_paper_offline_report_emits_json` to expect:

```python
assert payload["next_required_gate"] == (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"
)
assert payload["failure_labels"] == [
    "paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract_missing"
]
assert "paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract" in payload
assert payload["paper_faithfulness"]["runtime_lane_remaining_gates"] == [
    "paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"
]
assert (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"
    in payload["paper_faithfulness"]["implemented_output_contract_scope"]
)
entry = payload["paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"]
assert entry["entry_decision"] == "defer_real_runtime_entry"
assert entry["runtime_entry_allowed_count"] == 0
assert entry["runtime_entry_attempted_count"] == 0
assert entry["real_newton_import_count"] == 0
assert entry["newton_model_builder_instantiated_count"] == 0
assert entry["newton_builder_shape_call_count"] == 0
assert entry["newton_model_finalized_count"] == 0
assert entry["newton_collision_pipeline_created_count"] == 0
assert entry["newton_collision_pipeline_collide_count"] == 0
assert entry["newton_runtime_execution_count"] == 0
```

- [x] **Step 2: Verify RED**

Run:

```bash
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Expected: fail until CLI JSON includes the entry payload and smoke next gate.

- [x] **Step 3: Update docs and record**

Update live docs to say the entry contract is implemented as a conservative no-runtime-entry
decision and the next gate is the future engine-builder smoke contract. Add a dated record with
verification results and claim boundaries.

Add an explicit doc presence check before calling docs complete:

```bash
rg -n "paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract|engine-builder entry contract|no real import" \
  README.md docs/index.md docs/deepdive/evidence-status.md docs/deepdive/message-map.md \
  docs/reference/claim-boundaries.md docs/reference/cpd-paper-faithful-offline-lane-spec.md \
  docs/reference/cpd-paper-reproduction-gap-matrix.md docs/reference/cpd-paper-story-status.md \
  docs/records/README.md docs/records/2026-05-19-cpd-paper-newton-engine-builder-entry-contract.md
```

- [x] **Step 4: Verify GREEN**

Run:

```bash
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.
