# CPD Paper Newton Engine-Builder Runtime-Execution Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the report-only Newton engine-builder runtime-execution contract after the skipped
smoke contract.

**Architecture:** Extend the existing `cpd_paper_offline_report` gate chain by adding one payload
builder after the smoke payload. Keep the slice offline/report-only, validate the upstream smoke
lineage, record the default skipped-runtime-execution decision, and advance the next runtime-lane
gap to a claim-boundary review contract.

**Tech Stack:** Python, pytest, existing dict-contract helpers, Markdown records.

---

### Task 1: Runtime-Execution Contract Report Payload

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Write the failing tests**

Add a test near the smoke-contract tests:

```python
def test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
    ]

    assert report["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
    )
    assert report["failure_labels"] == [
        (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_"
            "runtime_lane_review_contract_missing"
        )
    ]
    assert (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == [
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
    ]
    assert payload["gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
    )
    assert payload["input_gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"
    )
    assert payload["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
    )
    assert payload["runtime_execution_decision"] == "skip_real_runtime_execution"
    assert payload["runtime_execution_allowed_count"] == 0
    assert payload["runtime_execution_attempted_count"] == 0
    assert payload["runtime_execution_passed_count"] == 0
    assert payload["real_newton_import_count"] == 0
    assert payload["real_warp_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_collision_pipeline_created_count"] == 0
    assert payload["newton_collision_pipeline_collide_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
```

Update the CLI JSON test to expect the new top-level next gate and runtime-execution payload.

- [ ] **Step 2: Run RED**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_gate -q
```

Expected: fail because the runtime-execution payload key does not exist.

- [ ] **Step 3: Write the minimal implementation**

Add the next-gate constant:

```python
_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
)
```

Add `_paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution()`
that returns the runtime-lane review contract.

Add helpers that consume the smoke payload, validate one smoke row, build one runtime-execution
row, summarize coverage, and return the runtime-execution payload. Wire the payload into
`build_cpd_paper_offline_report()` after the smoke payload and use the runtime-execution remaining
gaps for top-level `failure_labels` and `next_required_gate`.

- [ ] **Step 4: Run GREEN**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_gate -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Expected: pass.

### Task 2: Exact Schema, Drift, And Static Boundary

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Write failing tests**

Add exact key-set constants:

```python
NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_FALSE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_FALSE_FLAGS,
    "runtime_execution_allowed",
    "runtime_execution_attempted",
    "runtime_execution_passed",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_TRUE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_TRUE_FLAGS,
    "newton_shape_runtime_engine_builder_runtime_execution_recorded",
    "smoke_decision_respected",
    "runtime_execution_source_lineage_checked",
)
```

Add a schema test that asserts the runtime-execution payload and row exactly contain the fields
for gate IDs, lineage IDs, skipped-runtime decision/status, zero counters, coverage summary,
remaining gaps, false flags, and true flags.

Add drift tests that mutate the smoke payload and expect `ValueError` messages:

```python
@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("gate_id", "stale_gate", "runtime_execution_input_gate_id_mismatch"),
        ("next_required_gate", "stale_gate", "runtime_execution_input_next_gate_mismatch"),
        ("remaining_gaps", ["stale_gate"], "runtime_execution_input_remaining_gaps_mismatch"),
        ("smoke_decision", "allow_real_runtime_smoke", "runtime_execution_input_smoke_decision_mismatch"),
        ("runtime_smoke_attempted_count", 1, "runtime_execution_input_count_mismatch"),
        ("real_newton_import_count", 1, "runtime_execution_input_count_mismatch"),
        ("real_warp_import_count", 1, "runtime_execution_input_count_mismatch"),
        ("newton_model_builder_instantiated_count", 1, "runtime_execution_input_count_mismatch"),
        ("newton_engine_shape_object_count", 1, "runtime_execution_input_count_mismatch"),
        ("newton_builder_shape_call_count", 1, "runtime_execution_input_count_mismatch"),
        ("newton_model_finalized_count", 1, "runtime_execution_input_count_mismatch"),
        ("newton_collision_pipeline_created_count", 1, "runtime_execution_input_count_mismatch"),
        ("newton_collision_pipeline_collide_count", 1, "runtime_execution_input_count_mismatch"),
        ("newton_runtime_execution_count", 1, "runtime_execution_input_count_mismatch"),
        ("runtime_smoke_attempted", True, "runtime_execution_input_flag_true"),
        ("newton_runtime_allowed", True, "runtime_execution_input_flag_true"),
        (
            "newton_shape_runtime_engine_builder_smoke_recorded",
            False,
            "runtime_execution_input_flag_false",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_runtime_execution_rejects_input_drift(field, value, message):
    report = build_cpd_paper_offline_report()
    smoke = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"
            ]
        )
    )
    smoke[field] = value

    with pytest.raises(ValueError, match=message):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_payload(
            smoke
        )
```

Add source-row drift/copy tests for empty rows, more than one smoke row, stale
`source_package_id`, stale lineage fields such as
`source_newton_shape_runtime_engine_builder_entry_row_id`, nonzero
`newton_runtime_execution_count`, and injected `source_package`.

Add a static-boundary test that inspects the runtime-execution helpers and forbids imports,
dynamic import or execution escape hatches, `ModelBuilder`, real builder calls, finalization,
collision calls, existing Newton task smokes, USD inspection, benchmark timing APIs, and
collision-quality calls. The forbidden text and AST call names must include at least:

```python
(
    "importlib.import_module",
    "module_from_spec",
    "exec_module",
    "__import__",
    "getattr(",
    "eval(",
    "exec(",
    "compile(",
)
```

- [ ] **Step 2: Run RED**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "engine_builder_runtime_execution" -q
```

Expected: fail because the schema helpers and runtime-execution behavior do not exist.

- [ ] **Step 3: Implement schema and validation**

Add runtime-execution false/true flag helpers, optional-false-field validation, source-row
validation, row serialization validation, coverage summary, and the final runtime-execution
payload function.

- [ ] **Step 4: Run GREEN**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "engine_builder_runtime_execution" -q
python -m pytest tests/test_cpd_paper_offline.py -k "engine_builder_smoke or engine_builder_runtime_execution or cpd_paper_offline_report_next_gate" -q
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
- Create: `docs/records/2026-05-20-cpd-paper-newton-engine-builder-runtime-execution-contract.md`

- [ ] **Step 1: Update claim-boundary docs**

Replace wording that says the current next gate is the runtime-execution contract with wording
that says the runtime-execution contract is implemented as a report-only skipped-runtime-execution
decision and the current next gate is the runtime-lane claim-boundary review contract.

- [ ] **Step 2: Add dated record**

Add a record documenting scope, non-goals, current verification, and artifacts for the
runtime-execution contract. Mark multi-agent review as pending until Task 4 completes.

- [ ] **Step 3: Run docs checks**

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

- [ ] **Step 1: Request multi-agent review**

Ask at least two read-only review agents to inspect:

- code schema/runtime-boundary correctness;
- DeepDive and claim-boundary wording.

- [ ] **Step 2: Fix accepted findings**

Apply only findings that improve contract correctness or claim boundaries.

- [ ] **Step 3: Finalize the dated record after review**

Update `docs/records/2026-05-20-cpd-paper-newton-engine-builder-runtime-execution-contract.md` with
the completed multi-agent review outcome, accepted fixes, and final verification commands.

- [ ] **Step 4: Final verification**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "engine_builder_runtime_execution" -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

- [ ] **Step 5: Commit and merge**

Commit the implementation and documentation, then use `superpowers:finishing-a-development-branch`
to merge, push, and clean up the worktree.
