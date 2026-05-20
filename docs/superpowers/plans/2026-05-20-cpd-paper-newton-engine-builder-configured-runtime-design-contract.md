# CPD Paper Newton Engine-Builder Configured-Runtime Design Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the report-only Newton engine-builder configured-runtime design contract after the
runtime-lane review contract.

**Architecture:** Extend the existing `cpd_paper_offline_report` gate chain by adding one payload
builder after the runtime-lane review payload. The new payload consumes exactly one
`paper_single_box` runtime-lane review row, verifies the skipped-runtime boundary, records the
configuration inputs a later preflight must validate, and advances the runtime lane to a configured
runtime preflight gate while keeping real runtime work blocked.

**Tech Stack:** Python, pytest, existing dict-contract helpers, Markdown records.

---

### Task 1: Configured-Runtime Design Contract Report Payload

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Write the failing report and CLI tests**

Add constants near the existing configured-runtime design constant:

```python
EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract"
)
EXPECTED_CURRENT_REPORT_NEXT_GATE = (
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_CONTRACT
)
EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_CONTRACT,
]
EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_CONTRACT,
]
```

Add a focused gate test near the runtime-lane review tests:

```python
def test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract"
    ]

    assert report["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract"
    )
    assert report["failure_labels"] == [
        (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_"
            "configured_runtime_preflight_contract_missing"
        ),
    ]
    assert (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract"
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == [
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract"
    ]
    assert payload["gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract"
    )
    assert payload["input_gate_id"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
    )
    assert payload["next_required_gate"] == (
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract"
    )
    assert payload["configured_runtime_design_decision"] == (
        "define_configured_runtime_inputs_keep_real_runtime_blocked"
    )
    assert payload["configured_runtime_design_status"] == "input_design_recorded"
    assert payload["configured_runtime_design_recorded_count"] == 1
    assert payload["configured_runtime_preflight_ready_count"] == 0
    assert payload["runtime_source_configuration_required_count"] == 1
    assert payload["runtime_device_configuration_required_count"] == 1
    assert payload["runtime_entry_decision_required_count"] == 1
    assert payload["runtime_smoke_policy_required_count"] == 1
    assert payload["runtime_execution_policy_required_count"] == 1
    assert payload["required_config_keys"] == ["newton.source_dir", "newton_diagnostic.device"]
    assert payload["required_runtime_input_count"] == 6
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

Update `tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json` to expect:

- failure label `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract_missing`;
- top-level `next_required_gate` and `runtime_lane_remaining_gates` equal to the configured-runtime
  preflight contract;
- implemented-output scope includes the configured-runtime design contract after the runtime-lane
  review contract;
- new configured-runtime design payload key and zero real runtime/build/collision counters.

- [ ] **Step 2: Run RED**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_gate -q
```

Expected: fail because the configured-runtime design payload key does not exist.

- [ ] **Step 3: Write the minimal implementation**

Add the next-gate constant:

```python
_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract"
)
```

Add `_paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design()`
that returns the configured-runtime preflight contract.

Add helpers that consume the runtime-lane review payload, validate one source row, build one
configured-runtime design row, summarize coverage, and return the configured-runtime design payload.
Wire that payload into `build_cpd_paper_offline_report()` immediately after the runtime-lane review
payload and use the configured-runtime design remaining gaps for top-level `failure_labels` and
`next_required_gate`.

The new row should carry these values:

```python
{
    "configured_runtime_design_decision": "define_configured_runtime_inputs_keep_real_runtime_blocked",
    "configured_runtime_design_reason": "runtime_input_design_recorded_preflight_missing",
    "configured_runtime_design_status": "input_design_recorded",
    "configured_runtime_design_recorded": True,
    "configured_runtime_preflight_ready": False,
    "runtime_source_configuration_required": True,
    "runtime_device_configuration_required": True,
    "runtime_entry_decision_required": True,
    "runtime_smoke_policy_required": True,
    "runtime_execution_policy_required": True,
    "required_config_keys": ["newton.source_dir", "newton_diagnostic.device"],
    "required_runtime_inputs": [
        "newton_source_dir",
        "newton_diagnostic_device",
        "runtime_entry_decision",
        "runtime_smoke_policy",
        "runtime_execution_policy",
        "package_lineage_id",
    ],
    "runtime_entry_decision_policy": "require_configured_runtime_preflight_before_entry",
    "runtime_smoke_policy": "skip_until_configured_runtime_preflight_passes",
    "runtime_execution_policy": "skip_until_configured_runtime_preflight_passes",
    "source_package_copy_forbidden": True,
    "real_newton_import_count": 0,
    "real_warp_import_count": 0,
    "newton_model_builder_instantiated_count": 0,
    "newton_engine_shape_object_count": 0,
    "newton_builder_shape_call_count": 0,
    "newton_model_finalized_count": 0,
    "newton_collision_pipeline_created_count": 0,
    "newton_collision_pipeline_collide_count": 0,
    "newton_runtime_execution_count": 0,
}
```

- [ ] **Step 4: Run GREEN**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_gate tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Expected: pass.

- [ ] **Step 5: Request first multi-agent review**

Ask two read-only agents to inspect:

- configured-runtime design gate payload correctness and zero-counter boundary;
- CLI JSON expectations and top-level next-gate/failure-label consistency.

Apply accepted findings before Task 2.

### Task 2: Exact Schema, Drift, And Static Boundary

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Write failing schema and drift tests**

Add exact key-set constants:

```python
NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_FALSE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_FALSE_FLAGS,
    "configured_runtime_preflight_ready",
    "runtime_config_validated",
    "runtime_source_config_resolved",
    "runtime_device_config_resolved",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_TRUE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_TRUE_FLAGS,
    "newton_shape_runtime_engine_builder_configured_runtime_design_recorded",
    "runtime_lane_review_decision_respected",
    "configured_runtime_input_requirements_recorded",
)
```

Add exact payload and row required-key sets that include:

- gate metadata, `configured_runtime_design_action`, `configured_runtime_design_contract`,
  `input_contract_summary`;
- counts for one configured-runtime design row and one source runtime-lane review row;
- required config keys, required runtime inputs, and policy strings;
- row list, coverage summary, remaining gaps, false flags, and true flags.

Add tests:

```python
def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_design_payload_schema_is_exact():
    report = build_cpd_paper_offline_report()
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract"
    ]

    assert set(payload) == NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_PAYLOAD_REQUIRED_KEYS
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_engine_builder_configured_runtime_design_"
        "report_only_partial"
    )
    assert payload["artifact_kind"] == (
        "newton_engine_builder_configured_runtime_design_record_not_runtime_config_validation"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_engine_builder_configured_runtime_design_contract_"
        "no_config_read_no_import_no_model_builder_no_shape_call_no_finalize_no_runtime"
    )
    assert payload["configured_runtime_design_contract"]["runtime_config_validation_allowed"] is False
    assert payload["configured_runtime_design_contract"]["real_runtime_import_allowed"] is False
    assert payload["configured_runtime_design_contract"]["newton_runtime_allowed"] is False
    assert payload["coverage_summary"]["configured_runtime_design_decision_distribution"] == {
        "define_configured_runtime_inputs_keep_real_runtime_blocked": 1
    }
    assert set(payload["newton_shape_runtime_engine_builder_configured_runtime_design_rows"][0]) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_ROW_REQUIRED_KEYS
    )
```

Add drift tests following the existing runtime-lane review pattern:

```python
def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_design_rejects_input_drift():
    report = build_cpd_paper_offline_report()
    source = dict(report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
    ])
    source["runtime_lane_review_decision"] = "runtime_compatibility_validated"

    with pytest.raises(ValueError, match="configured_runtime_design_input_metadata_mismatch"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_payload(source)
```

Cover these cases with parameterized or focused tests:

- stale input `gate_id`, `next_required_gate`, `decision_reason`, and nested
  `runtime_lane_review_contract`;
- `runtime_compatibility_validated` or `real_runtime_execution_evidence` flipped true;
- any real runtime counter made nonzero;
- missing and unexpected input payload keys;
- stale coverage summary;
- missing and unexpected source-row keys;
- stale source-row lineage IDs and decision fields;
- copied source package dict rejected by the helper.

- [ ] **Step 2: Run RED**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_design" -q
```

Expected: fail because schema constants, payload helper, and drift enforcement are not implemented.

- [ ] **Step 3: Implement exact schema, drift, and static-boundary helpers**

Add private constants and helpers mirroring the runtime-lane review slice:

- `_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_PAYLOAD_FALSE_FLAGS`;
- `_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_TRUE_FLAGS`;
- `_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_INPUT_REQUIRED_KEYS`;
- `_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_ROW_INPUT_REQUIRED_KEYS`;
- validation helpers for required keys, unexpected keys, false flags, true flags, coverage summary,
  source row values, and source-package-copy rejection;
- row builder, coverage summary builder, and payload builder.

The configured-runtime design helpers must not import Newton/Warp, inspect USD, call existing
Newton diagnostic task functions, or read config files.

- [ ] **Step 4: Add static-boundary test**

Add a test that parses the new helper ASTs and rejects:

```python
forbidden_import_roots = {"newton", "warp", "pxr"}
forbidden_call_attrs = {
    "__import__",
    "import_module",
    "eval",
    "exec",
    "ModelBuilder",
    "CollisionPipeline",
    "add_shape_box",
    "finalize",
    "collide",
    "run_newton_contact_smoke",
    "run_newton_drop_settle",
    "run_newton_sphere_rain",
    "inspect_real_usd",
    "perf_counter",
    "process_time",
    "collision_quality",
}
```

- [ ] **Step 5: Run GREEN**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_design" -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
git diff --check
```

Expected: pass.

- [ ] **Step 6: Request second multi-agent review**

Ask two read-only agents to inspect:

- exact schema/drift/static-boundary completeness;
- whether any names imply config validation, runtime compatibility, or runtime execution.

Apply accepted findings before Task 3.

### Task 3: Documentation And Dated Record

**Files:**

- Modify: `README.md`
- Modify: `docs/index.md`
- Modify: `docs/deepdive/message-map.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/records/README.md`
- Create: `docs/records/2026-05-20-cpd-paper-newton-engine-builder-configured-runtime-design-contract.md`

- [ ] **Step 1: Update docs for the closed configured-runtime design contract**

Docs must say:

- configured-runtime design contract is closed as report-only input design;
- next gate is `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract`;
- runtime config is not validated by this report path;
- all real runtime counters remain zero;
- no Newton support/runtime compatibility/benchmark/collision-quality/deployment/safety claim.

Also fix review findings:

- `docs/index.md` command summary must mention runtime-lane review between runtime-execution and
  configured-runtime design/preflight.
- README must qualify "No generated collision artifact pipeline" as no production/general generated
  collision artifact pipeline beyond the one synthetic report-scoped box `CollisionPackage.to_dict()`
  artifact.

- [ ] **Step 2: Add the dated record**

The record must include:

- baseline: `python -m pytest -q` observed `2259 passed, 2 skipped`;
- RED and GREEN commands/results;
- multi-agent review findings and accepted fixes;
- final verification commands;
- allowed and forbidden claim wording;
- next action: configured-runtime preflight contract.

- [ ] **Step 3: Run doc checks**

Run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

- [ ] **Step 4: Request third multi-agent review**

Ask two read-only agents to inspect:

- DeepDive wording and claim-boundary consistency;
- dated record evidence and command/result accuracy.

Apply accepted findings before Task 4.

### Task 4: Final Verification, Review, And Integration

**Files:**

- Review all changed files.

- [ ] **Step 1: Run focused verification**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_design" -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

- [ ] **Step 2: Request final multi-agent review**

Ask at least two read-only agents to inspect:

- all code/test changes for schema/runtime-boundary correctness;
- all docs/records for DeepDive and claim-boundary wording.

Apply accepted findings.

- [ ] **Step 3: Run full verification**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_design" -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

- [ ] **Step 4: Finalize records and plan**

Update:

- this plan with completed checkbox status and verification evidence;
- `docs/records/2026-05-20-cpd-paper-newton-engine-builder-configured-runtime-design-contract.md`
  with final verification results and review outcomes.

Re-run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

- [ ] **Step 5: Commit, merge, push, and clean up**

Commit implementation and docs. Use `superpowers:verification-before-completion` before claiming
completion, then use `superpowers:finishing-a-development-branch` to merge to `main`, verify on the
merged result, push, delete the feature branch, and remove the worktree.
