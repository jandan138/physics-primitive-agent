# CPD Paper Newton Engine-Builder Runtime-Lane Review Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the report-only Newton engine-builder runtime-lane review contract after the skipped
runtime-execution contract.

**Architecture:** Extend the existing `cpd_paper_offline_report` gate chain by adding one payload
builder after the runtime-execution payload. The new payload consumes the skipped-runtime-execution
record, verifies the same single synthetic lineage and zero real runtime counters, records a
claim-boundary review decision, and advances the runtime lane to a configured-runtime design gate.

**Tech Stack:** Python, pytest, existing dict-contract helpers, Markdown records.

---

### Task 1: Runtime-Lane Review Contract Report Payload

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [x] **Step 1: Write the failing report/CLI tests**

Add constants near the existing runtime-execution constants:

```python
EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract"
)
EXPECTED_CURRENT_REPORT_NEXT_GATE = (
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT
)
EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT,
]
EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT,
]
```

Add a report gate test near the runtime-execution tests:

```python
def test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
    ]

    assert report["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract"
    )
    assert report["failure_labels"] == [
        (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_"
            "configured_runtime_design_contract_missing"
        )
    ]
    assert (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == [
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract"
    ]
    assert payload["gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
    )
    assert payload["input_gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
    )
    assert payload["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract"
    )
    assert payload["runtime_lane_review_decision"] == "keep_real_runtime_execution_blocked"
    assert payload["runtime_lane_review_status"] == "claim_boundary_preserved"
    assert payload["real_runtime_execution_evidence"] is False
    assert payload["runtime_compatibility_validated"] is False
    assert payload["runtime_lane_review_recorded_count"] == 1
    assert payload["runtime_lane_claim_boundary_preserved_count"] == 1
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

Update `tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json` to expect the new
top-level next gate, the new failure label, the new payload key, the new implemented-output scope
entry, and zero real runtime/build/collision counters.

- [x] **Step 2: Run RED**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_gate -q
```

Expected: fail because the runtime-lane review payload key does not exist.

- [x] **Step 3: Write the minimal implementation**

Add the next-gate constant:

```python
_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract"
)
```

Add `_paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review()`
that returns the configured-runtime design contract.

Add helpers that consume the runtime-execution payload, validate one runtime-execution row, build
one runtime-lane review row, summarize coverage, and return the runtime-lane review payload. Wire
the payload into `build_cpd_paper_offline_report()` after the runtime-execution payload and use the
runtime-lane review remaining gaps for top-level `failure_labels` and `next_required_gate`.

- [x] **Step 4: Run GREEN**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_gate tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Expected: pass.

Task 1 execution evidence:

- RED: `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_gate -q`
  failed before implementation with the runtime-lane review payload key missing.
- GREEN: `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_gate tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  passed with `2 passed`.

### Task 2: Exact Schema, Drift, And Static Boundary

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [x] **Step 1: Write failing schema and drift tests**

Add exact key-set constants:

```python
NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_FALSE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_FALSE_FLAGS,
    "real_runtime_execution_evidence",
    "runtime_compatibility_validated",
    "configured_runtime_design_ready",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_TRUE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_TRUE_FLAGS,
    "newton_shape_runtime_engine_builder_runtime_lane_review_recorded",
    "runtime_execution_decision_reviewed",
    "runtime_lane_claim_boundary_preserved",
)
```

Add `test_cpd_paper_newton_shape_runtime_engine_builder_runtime_lane_review_payload_schema_is_exact`
that asserts the payload and one row exactly contain:

- gate IDs and `next_required_gate`;
- `runtime_lane_review_decision: keep_real_runtime_execution_blocked`;
- `runtime_lane_review_reason: skipped_runtime_execution_is_not_runtime_compatibility`;
- `runtime_lane_review_status: claim_boundary_preserved`;
- `runtime_lane_review_recorded_count: 1`;
- `runtime_lane_claim_boundary_preserved_count: 1`;
- `real_runtime_execution_evidence: False`;
- `runtime_compatibility_validated: False`;
- exact zero real runtime/import/build/finalize/collision counters;
- source runtime-execution lineage IDs;
- coverage summary and remaining gaps;
- false/true boundary flags.

Add input drift tests:

```python
@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("gate_id", "stale_gate", "runtime_lane_review_input_gate_id_mismatch"),
        ("closed_gate", "stale_gate", "runtime_lane_review_input_metadata_mismatch:closed_gate"),
        ("input_gate_id", "stale_gate", "runtime_lane_review_input_metadata_mismatch:input_gate_id"),
        ("next_required_gate", "stale_gate", "runtime_lane_review_input_next_gate_mismatch"),
        ("schema_version", 2, "runtime_lane_review_input_metadata_mismatch:schema_version"),
        ("source_scope", "real_usd_assets", "runtime_lane_review_input_metadata_mismatch:source_scope"),
        ("implementation_boundary", "real_runtime_execution", "runtime_lane_review_input_metadata_mismatch:implementation_boundary"),
        ("runtime_execution_decision", "run_real_runtime_execution", "runtime_lane_review_input_decision_mismatch"),
        ("runtime_execution_allowed_count", 1, "runtime_lane_review_input_count_mismatch"),
        ("runtime_execution_attempted_count", 1, "runtime_lane_review_input_count_mismatch"),
        ("real_newton_import_count", 1, "runtime_lane_review_input_count_mismatch"),
        ("real_warp_import_count", 1, "runtime_lane_review_input_count_mismatch"),
        ("newton_model_builder_instantiated_count", 1, "runtime_lane_review_input_count_mismatch"),
        ("newton_engine_shape_object_count", 1, "runtime_lane_review_input_count_mismatch"),
        ("newton_builder_shape_call_count", 1, "runtime_lane_review_input_count_mismatch"),
        ("newton_model_finalized_count", 1, "runtime_lane_review_input_count_mismatch"),
        ("newton_collision_pipeline_created_count", 1, "runtime_lane_review_input_count_mismatch"),
        ("newton_collision_pipeline_collide_count", 1, "runtime_lane_review_input_count_mismatch"),
        ("newton_runtime_execution_count", 1, "runtime_lane_review_input_count_mismatch"),
        ("runtime_execution_attempted", True, "runtime_lane_review_input_flag_true"),
        ("newton_runtime_allowed", True, "runtime_lane_review_input_flag_true"),
        (
            "newton_shape_runtime_engine_builder_runtime_execution_decision_recorded",
            False,
            "runtime_lane_review_input_flag_false",
        ),
        (
            "unexpected_runtime_lane_review_input_key",
            True,
            "runtime_lane_review_input_unexpected_keys",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_runtime_lane_review_rejects_input_drift(field, value, message):
    report = build_cpd_paper_offline_report()
    runtime_execution = json.loads(json.dumps(report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
    ]))
    runtime_execution[field] = value

    with pytest.raises(ValueError, match=message):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_payload(
            runtime_execution
        )
```

Add source-row drift/copy tests for empty rows, more than one runtime-execution row, stale
`source_package_id`, stale `source_newton_shape_runtime_engine_builder_smoke_row_id`, nonzero
`newton_runtime_execution_count`, injected `source_package`, and nested copied collision package.

Add a static-boundary test that inspects the runtime-lane review helpers and forbids:

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
    "import newton",
    "from newton",
    "import warp",
    "from warp",
    "ModelBuilder(",
    "CollisionPipeline(",
    ".add_shape_box(",
    ".finalize(",
    ".collide(",
    "run_newton_contact_smoke",
    "run_newton_drop_settle",
    "run_newton_sphere_rain",
    "inspect_newton_environment",
    "_import_newton_runtime",
    "inspect_newton_warp_provenance",
    "load_first_mesh",
    "inspect_usd_asset",
    "timeit",
    "perf_counter",
    "benchmark_metric",
    "measure_collision_quality",
)
```

- [x] **Step 2: Run RED**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "runtime_lane_review" -q
```

Expected: fail because the runtime-lane review schema helpers and exact payload fields do not
exist.

- [x] **Step 3: Implement schema and validation**

Add runtime-lane review false/true flag helpers, exact input key validation, required-key-first
validation, source-row validation, source-package copy rejection, row serialization validation,
coverage summary, and the final runtime-lane review payload function.

- [x] **Step 4: Run GREEN**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "runtime_lane_review" -q
python -m pytest tests/test_cpd_paper_offline.py -k "engine_builder_runtime_execution or runtime_lane_review or cpd_paper_offline_report_next_gate" -q
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
- Create: `docs/records/2026-05-20-cpd-paper-newton-engine-builder-runtime-lane-review-contract.md`

- [x] **Step 1: Update claim-boundary docs**

Replace wording that says the current next gate is the runtime-lane review contract with wording
that says the runtime-lane review contract is implemented as a report-only claim-boundary review
and the current next gate is:

```text
paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract
```

Keep the forbidden wording list explicit: no Newton readiness, Newton support, Newton execution,
runtime compatibility, real Newton/Warp imports, `newton.ModelBuilder`, engine shape objects, real
builder calls, model finalization, collision pipeline creation/collision, runtime-smoke or
runtime-execution attempts, simulation-checked wording, real USD, benchmark, collision-quality,
deployment, or safety evidence.

- [x] **Step 2: Add dated record**

Add a record documenting scope, non-goals, current verification, artifacts, and multi-agent review
for the runtime-lane review contract. Mark final full-regression verification as pending until Task
4 completes.

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

Ask at least two read-only review agents to inspect:

- code schema/runtime-boundary correctness;
- DeepDive and claim-boundary wording.

- [x] **Step 2: Fix accepted findings**

Apply only findings that improve contract correctness or claim boundaries.

- [x] **Step 3: Finalize the dated record after review**

Update `docs/records/2026-05-20-cpd-paper-newton-engine-builder-runtime-lane-review-contract.md`
with the completed multi-agent review outcome, accepted fixes, and final verification commands.

- [x] **Step 4: Final verification**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "runtime_lane_review" -q
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
