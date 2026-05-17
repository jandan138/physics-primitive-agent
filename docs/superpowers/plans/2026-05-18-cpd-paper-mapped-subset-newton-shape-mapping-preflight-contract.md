# CPD Paper Mapped-Subset Newton Shape-Mapping Preflight Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement `paper_mapped_subset_newton_shape_mapping_preflight_contract` as a bounded offline/static request for one later Newton shape-mapping attempt.

**Architecture:** Extend the CPD paper offline report chain after `paper_mapped_subset_runtime_admissibility_contract`. Validate the one runtime-admissibility row, record one compact shape-mapping preflight row for the `paper_single_box` box PrimitiveSpec-like dict, advance the next gate to `paper_mapped_subset_newton_shape_mapping_contract`, and keep Newton mapping/runtime/USD/benchmark/collision-quality triggers false.

**Tech Stack:** Python report builders in `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`, pytest, CLI JSON tests, Markdown docs. This plan must not import or call `primitive_collision_compiler.newton`.

---

### Task 1: Add RED Tests For The Preflight Gate

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add constants**

Add near the existing mapped-subset constants:

```python
EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT = (
    "paper_mapped_subset_newton_shape_mapping_contract"
)
EXPECTED_NEWTON_SHAPE_MAPPING_PREFLIGHT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT,
]
```

Update `EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS` to use
`EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT` only after the implementation task closes
the preflight gate.

- [ ] **Step 2: Add an input helper**

Add near `_runtime_admissibility_contract_input()`:

```python
def _newton_shape_mapping_preflight_input() -> dict[str, object]:
    report = build_cpd_paper_offline_report()
    return json.loads(
        json.dumps(report["paper_mapped_subset_runtime_admissibility_contract"])
    )
```

- [ ] **Step 3: Add schema key sets**

Add `NEWTON_SHAPE_MAPPING_PREFLIGHT_PAYLOAD_REQUIRED_KEYS`,
`NEWTON_SHAPE_MAPPING_PREFLIGHT_ROW_REQUIRED_KEYS`, and
`NEWTON_SHAPE_MAPPING_PREFLIGHT_FALSE_FLAGS`. The false flags must include paper-faithful,
package-generation, Newton runtime, real-USD, benchmark, collision-quality, deployment,
certification, approximation, silent-drop, and mapping-attempt booleans.

The implementation in `offline.py` must also define the private marker constant
`_NEWTON_SHAPE_MAPPING_PREFLIGHT_PAYLOAD_FALSE_FLAGS` so the source-boundary test can slice the
new contract block reliably.

- [ ] **Step 4: Add report-level failing tests**

Add tests asserting:

```python
def test_cpd_paper_records_mapped_subset_newton_shape_mapping_preflight_gate():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_newton_shape_mapping_preflight_contract"]

    assert report["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT
    )
    assert report["failure_labels"] == [
        "paper_mapped_subset_newton_shape_mapping_contract_missing"
    ]
    assert report["newton_runtime_triggered"] is False
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_NEWTON_SHAPE_MAPPING_PREFLIGHT_REMAINING_GAPS
    )
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT
    )
    assert payload["newton_shape_mapping_preflight_row_count"] == 1
    assert payload["newton_mapping_record_count"] == 0
    assert payload["mapping_attempt_count"] == 0
```

- [ ] **Step 5: Add payload and row tests**

Add tests asserting exact payload keys, exact one row, source row lineage, target kind `box`,
transfer fields `center`, `axes`, and `dimensions.half_extents`, and false mapping/runtime flags.

- [ ] **Step 6: Add drift rejection tests**

Add parametrized tests that mutate the copied input and expect `ValueError` labels for:

- wrong input `gate_id`;
- wrong input `next_required_gate`;
- wrong count fields;
- true forbidden flags;
- zero or two runtime-admissibility rows;
- wrong source row id;
- wrong `fixture_id`;
- wrong `primitive_spec_kind`;
- copied full generated package dict;
- missing or malformed `candidate_primitivespec_dict`;
- `candidate_primitivespec_dict["kind"] != "box"`;
- missing `dimensions["half_extents"]`.
- `offline_static_runtime_admissibility_check_passed` set to `False`;
- `offline_static_runtime_admissibility_checked` set to `False`.

- [ ] **Step 7: Update existing top-level gate tests**

Search and update existing top-level report assertions that currently expect
`EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT`, including tests around:

```bash
rg -n "next_required_gate|failure_labels|runtime_lane_remaining_gates|implemented_output_contract_scope" tests/test_cpd_paper_offline.py tests/test_cli.py
```

Rules:

- top-level `report["next_required_gate"]` should become
  `EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT`;
- top-level `report["failure_labels"]` should become
  `["paper_mapped_subset_newton_shape_mapping_contract_missing"]`;
- top-level `paper_faithfulness["runtime_lane_remaining_gates"]` should become
  `EXPECTED_NEWTON_SHAPE_MAPPING_PREFLIGHT_REMAINING_GAPS`;
- top-level `paper_faithfulness["implemented_output_contract_scope"]` should include
  `EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT`;
- `paper_mapped_subset_runtime_admissibility_contract["next_required_gate"]` must remain
  `EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT`;
- `paper_mapped_subset_runtime_admissibility_contract["remaining_gaps"]` must remain
  `EXPECTED_RUNTIME_ADMISSIBILITY_CONTRACT_REMAINING_GAPS`.

- [ ] **Step 8: Add source-boundary test**

Add a source block test that slices from
`_NEWTON_SHAPE_MAPPING_PREFLIGHT_PAYLOAD_FALSE_FLAGS` to the next payload helper and asserts the
block does not contain:

```python
forbidden_patterns = [
    "primitive_collision_compiler.newton",
    "NewtonShapeMapping",
    "map_package_shapes",
    "PrimitiveSpec(",
    "CollisionPackage(",
    "import newton",
    "import newton_warp",
    "pxr",
    "Usd",
    "USD",
    "run_newton",
    "timeit",
    "perf_counter",
    "benchmark_metric",
    "collision_quality_score",
]
```

- [ ] **Step 9: Add CLI expectations**

Update `test_cli_run_cpd_paper_offline_report_emits_json` to expect the new top-level next gate,
the new failure label, the new implemented output-contract scope entry, and the new preflight
payload with one row and zero mapping/runtime counts.

- [ ] **Step 10: Run RED tests**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_mapping_preflight' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Expected before implementation: failures caused by the missing
`paper_mapped_subset_newton_shape_mapping_preflight_contract` payload and stale next-gate
expectations.

### Task 2: Implement The Offline/Static Preflight Payload

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add the later gate constant**

Add:

```python
_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT = (
    "paper_mapped_subset_newton_shape_mapping_contract"
)
```

- [ ] **Step 2: Add remaining-gap helper**

Add:

```python
def _paper_remaining_gaps_after_mapped_subset_newton_shape_mapping_preflight() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT]
```

- [ ] **Step 3: Add preflight validation helpers**

Add helpers that:

- reject wrong input gate and next gate;
- reject forbidden true flags;
- reject copied full package dicts;
- require exactly one runtime-admissibility row;
- require source row id `runtime_admissibility__paper_single_box__box`;
- require `offline_static_runtime_admissibility_check_passed is True`;
- require `offline_static_runtime_admissibility_checked is True`;
- require `primitive_spec_kind == "box"`;
- require `candidate_primitivespec_dict["kind"] == "box"`;
- require `candidate_primitivespec_dict["dimensions"]["half_extents"]` to be a length-3 list.

- [ ] **Step 4: Add one preflight row builder**

Build a row with id:

```python
"newton_shape_mapping_preflight__paper_single_box__box"
```

The row must set:

```python
"target_newton_shape_kind": "box"
"target_newton_shape_kind_declared": True
"newton_shape_support_evidence_status": (
    "pending_later_mapping_contract_no_support_claim"
)
"target_newton_shape_kind_handoff_source": (
    "static_current_report_lane_declares_box_target_schema_for_later_mapper"
)
"center_transfer_field": "candidate_primitivespec_dict.center"
"axes_transfer_field": "candidate_primitivespec_dict.axes"
"dimensions_transfer_field": "candidate_primitivespec_dict.dimensions"
"box_half_extents_transfer_field": (
    "candidate_primitivespec_dict.dimensions.half_extents"
)
"mapping_attempted": False
"newton_shape_mapping_record_created": False
```

- [ ] **Step 5: Add payload builder**

Add `_paper_mapped_subset_newton_shape_mapping_preflight_contract_payload(runtime_admissibility)`.
It should return the exact schema tested in Task 1, with:

```python
"gate_id": _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT
"input_gate_id": _PAPER_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT
"next_required_gate": _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT
"newton_shape_mapping_preflight_row_count": 1
"mapping_attempt_count": 0
"newton_mapping_record_count": 0
"newton_runtime_execution_count": 0
```

- [ ] **Step 6: Wire the report chain**

In `build_cpd_paper_offline_report()`, call the new payload builder after
`mapped_subset_runtime_admissibility`, append the preflight gate to
`implemented_output_contract_scope`, set `runtime_lane_remaining_gates` from the new remaining-gap
helper, expose the payload under `paper_mapped_subset_newton_shape_mapping_preflight_contract`,
and advance the top-level failure label and next gate to the later mapping contract.

- [ ] **Step 7: Run GREEN tests**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_mapping_preflight' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Expected after implementation: both commands pass.

### Task 3: Update Durable Docs And Dated Record

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
- Create: `docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-mapping-preflight-contract.md`

- [ ] **Step 1: Update claim-boundary wording**

Add allowed wording that this gate records one offline/static preflight row for a later mapping
attempt, and forbidden wording that it is not package readiness, Newton mapping, Newton readiness,
Newton support, Newton execution, real-USD evidence, benchmark evidence, collision-quality
evidence, full CPD reproduction, deployment readiness, or safety certification.

- [ ] **Step 2: Update story/status docs**

Move the current runtime-lane next gate from
`paper_mapped_subset_newton_shape_mapping_preflight_contract` to
`paper_mapped_subset_newton_shape_mapping_contract`.

- [ ] **Step 3: Add dated record**

Record context, what changed, verification commands, claim boundary, artifacts, and next gate.
The record must explicitly say the gate does not invoke Newton and does not create a
`NewtonShapeMapping`.

- [ ] **Step 4: Run docs validators**

Run:

```bash
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

### Task 4: Review, Final Verification, Commit, Merge, Push

**Files:**
- All files changed by Tasks 1-3.

- [ ] **Step 1: Request independent reviews**

Dispatch one code/test reviewer and one docs/claim-boundary reviewer. Fix critical and important
findings before proceeding.

- [ ] **Step 2: Run final verification**

Run:

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

- [ ] **Step 3: Commit**

Commit with:

```bash
git add README.md docs src tests
git commit -m "feat: add CPD Newton shape-mapping preflight contract"
```

- [ ] **Step 4: Merge and push**

Fast-forward merge into `main`, rerun focused post-merge checks, push `main`, remove the worktree,
and delete the feature branch.
