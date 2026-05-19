# CPD Paper Newton Engine-Builder Smoke Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the report-only Newton engine-builder smoke contract after the entry contract.

**Architecture:** Extend the existing `cpd_paper_offline_report` gate chain by adding one payload
builder after the entry payload. Keep the slice offline/report-only, validate the upstream entry
lineage, record the default skipped-smoke decision, and advance the next runtime-lane gap to a
future runtime-execution contract.

**Tech Stack:** Python, pytest, existing dict-contract helpers, Markdown records.

---

### Task 1: Smoke Contract Report Payload

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [x] **Step 1: Write the failing tests**

Add a test near the entry-contract tests:

```python
def test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"
    ]

    assert report["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
    )
    assert report["failure_labels"] == [
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_missing"
    ]
    assert (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == [
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
    ]
    assert payload["gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"
    )
    assert payload["input_gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"
    )
    assert payload["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
    )
    assert payload["smoke_decision"] == "skip_real_runtime_smoke"
    assert payload["runtime_smoke_allowed_count"] == 0
    assert payload["runtime_smoke_attempted_count"] == 0
    assert payload["runtime_smoke_passed_count"] == 0
    assert payload["real_newton_import_count"] == 0
    assert payload["real_warp_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_collision_pipeline_created_count"] == 0
    assert payload["newton_collision_pipeline_collide_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
```

Update the CLI JSON test to expect the new top-level next gate and the smoke payload.

- [x] **Step 2: Run RED**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract_gate -q
```

Expected: fail because the smoke payload key does not exist.

- [x] **Step 3: Write the minimal implementation**

Add the next-gate constant:

```python
_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
)
```

Add `_paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_engine_builder_smoke()` that
returns the runtime-execution contract.

Add helpers that consume the entry payload, validate one entry row, build one smoke row, summarize
coverage, and return the smoke payload. Wire the payload into `build_cpd_paper_offline_report()`
after the entry payload and use the smoke remaining gaps for top-level `failure_labels` and
`next_required_gate`.

- [x] **Step 4: Run GREEN**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract_gate -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Expected: pass.

### Task 2: Exact Schema, Drift, And Static Boundary

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [x] **Step 1: Write failing tests**

Add exact key-set constants:

```python
NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_FALSE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_FALSE_FLAGS,
    "runtime_smoke_allowed",
    "runtime_smoke_attempted",
    "runtime_smoke_passed",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_TRUE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_TRUE_FLAGS,
    "newton_shape_runtime_engine_builder_smoke_recorded",
    "entry_decision_respected",
    "smoke_source_lineage_checked",
)
```

Add a schema test that asserts the smoke payload and row exactly contain the fields for gate IDs,
lineage IDs, smoke decision/status, zero counters, coverage summary, remaining gaps, false flags,
and true flags.

Add drift tests that mutate the entry payload and expect `ValueError` messages:

```python
@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("gate_id", "stale_gate", "smoke_input_gate_id_mismatch"),
        ("next_required_gate", "stale_gate", "smoke_input_next_gate_mismatch"),
        ("runtime_entry_attempted_count", 1, "smoke_input_count_mismatch"),
        ("real_newton_import_count", 1, "smoke_input_count_mismatch"),
        ("newton_model_builder_instantiated_count", 1, "smoke_input_count_mismatch"),
        ("newton_builder_shape_call_count", 1, "smoke_input_count_mismatch"),
        ("newton_model_finalized_count", 1, "smoke_input_count_mismatch"),
        ("newton_runtime_execution_count", 1, "smoke_input_count_mismatch"),
        ("runtime_entry_allowed", True, "smoke_input_flag_true"),
        ("newton_runtime_allowed", True, "smoke_input_flag_true"),
        ("newton_shape_runtime_engine_builder_entry_recorded", False, "smoke_input_flag_false"),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_smoke_rejects_input_drift(field, value, message):
    report = build_cpd_paper_offline_report()
    entry = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"
            ]
        )
    )
    entry[field] = value

    with pytest.raises(ValueError, match=message):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract_payload(
            entry
        )
```

Add a static-boundary test that inspects the smoke helpers and forbids imports, `ModelBuilder`,
real builder calls, finalization, collision calls, existing Newton task smokes, USD inspection, and
benchmark timing APIs.

- [x] **Step 2: Run RED**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "engine_builder_smoke" -q
```

Expected: fail because the schema helpers and drift behavior do not exist.

- [x] **Step 3: Implement schema and validation**

Add smoke false/true flag helpers, optional-false-field validation, source-row validation, row
serialization validation, coverage summary, and the final smoke payload function.

- [x] **Step 4: Run GREEN**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "engine_builder_smoke" -q
python -m pytest tests/test_cpd_paper_offline.py -k "engine_builder_entry or engine_builder_smoke or api_surface or cpd_paper_offline_report_next_gate" -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Expected: all selected tests pass.

### Task 3: Documentation And Record Synchronization

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
- Create: `docs/records/2026-05-19-cpd-paper-newton-engine-builder-smoke-contract.md`

- [x] **Step 1: Update claim-boundary docs**

Replace wording that says the current next gate is the smoke contract with wording that says the
smoke contract is implemented as a report-only skipped-smoke decision and the current next gate is
the future runtime-execution contract.

- [x] **Step 2: Add dated record**

Add a record documenting scope, non-goals, verification, multi-agent review, and artifacts for the
smoke contract.

- [x] **Step 3: Run docs checks**

Run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

### Task 4: Review, Verification, And Merge Prep

**Files:**

- Review all changed files.

- [x] **Step 1: Request multi-agent review**

Ask three review agents to inspect:

- claim-boundary discipline;
- report schema and drift validation;
- docs synchronization and stale next-gate wording.

- [x] **Step 2: Apply accepted review fixes**

Use the receiving-code-review skill before changing code for review comments.

- [x] **Step 3: Run final verification**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "engine_builder_entry or engine_builder_smoke or api_surface or cpd_paper_offline_report_next_gate" -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

If time permits before merge, also run:

```bash
python -m pytest -q
```

Expected: all pass.
