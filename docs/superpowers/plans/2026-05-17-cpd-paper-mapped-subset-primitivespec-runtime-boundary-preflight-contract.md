# CPD Paper Mapped-Subset PrimitiveSpec Runtime-Boundary Preflight Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a command-only offline gate that defines the report-side boundary before any later
runtime `PrimitiveSpec` construction contract may be proposed.

**Architecture:** Extend the existing CPD paper offline report chain with one preflight payload
after `paper_mapped_subset_primitivespec_native_fixture_serialization_contract`. The new payload
consumes the strict canonical JSON/schema-stable serialization row, records one later-runtime
construction candidate, keeps runtime object/package/Newton counts at zero, and advances the report
to the future `paper_mapped_subset_primitivespec_runtime_construction_contract` gate.

**Tech Stack:** Python, pytest, existing CPD paper offline report schema, Markdown docs.

---

### Task 1: RED Tests For Runtime-Boundary Preflight Gate

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add runtime-construction constant and remaining-gap list**

Add constants near the existing runtime-boundary constant:

```python
EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT = (
    "paper_mapped_subset_primitivespec_runtime_construction_contract"
)

EXPECTED_RUNTIME_BOUNDARY_PREFLIGHT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT,
]
```

Change the top-level current output gap expectation from
`EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT` to
`EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT`.

- [ ] **Step 2: Add exact preflight payload key sets**

Add:

```python
RUNTIME_BOUNDARY_PREFLIGHT_PAYLOAD_REQUIRED_KEYS = {
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
    "runtime_boundary_action",
    "runtime_boundary_requirements",
    "runtime_boundary_preflight_row_count",
    "later_runtime_primitivespec_construction_candidate_count",
    "runtime_construction_allowed_in_current_gate",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "runtime_boundary_preflight_contract",
    "input_contract_summary",
    "runtime_boundary_preflight_rows",
    "coverage_summary",
    "remaining_gaps",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}

RUNTIME_BOUNDARY_PREFLIGHT_ROW_REQUIRED_KEYS = {
    "runtime_boundary_preflight_row_id",
    "source_native_fixture_primitivespec_serialization_row_id",
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
    "serialized_payload_schema_keys",
    "canonical_primitivespec_json",
    "input_json_round_trip_equal",
    "input_canonical_json_stable",
    "input_schema_validation_status",
    "later_runtime_primitivespec_construction_candidate",
    "runtime_construction_allowed_in_current_gate",
    "required_later_gate",
    "preflight_decision",
    "preflight_reason",
    "runtime_instance_generated",
    "generated_primitive_spec",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}
```

- [ ] **Step 3: Add RED gate exposure test**

Add:

```python
def test_cpd_paper_records_mapped_subset_primitivespec_runtime_boundary_preflight_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report[
        "paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract"
    ]

    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT
    )
    assert report["failure_labels"] == [
        "paper_mapped_subset_primitivespec_runtime_construction_contract_missing",
    ]
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_RUNTIME_BOUNDARY_PREFLIGHT_REMAINING_GAPS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_SERIALIZATION_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT
    )
    assert payload["runtime_boundary_preflight_row_count"] == 1
    assert payload["later_runtime_primitivespec_construction_candidate_count"] == 1
    assert payload["runtime_construction_allowed_in_current_gate"] is False
    assert payload["generated_runtime_primitive_spec_count"] == 0
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_RUNTIME_BOUNDARY_PREFLIGHT_REMAINING_GAPS
```

- [ ] **Step 4: Add RED schema and row tests**

Add tests that assert:

```python
assert set(payload) == RUNTIME_BOUNDARY_PREFLIGHT_PAYLOAD_REQUIRED_KEYS
assert payload["paper_faithful_offline_allowed"] is False
assert payload["package_generation_allowed"] is False
assert payload["runtime_boundary_requirements"] == {
    "input_gate_required": (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_SERIALIZATION_CONTRACT
    ),
    "runtime_boundary_preflight_gate_closed": (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
    ),
    "next_runtime_construction_gate_required": (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT
    ),
    "source_fixture_required": "paper_single_box",
    "source_paper_primitive_required": "oriented_bounding_box",
    "source_primitive_spec_kind_required": "box",
    "json_round_trip_required": True,
    "schema_validation_required": True,
    "later_runtime_construction_candidates_required": 1,
    "runtime_construction_allowed_in_current_gate": False,
    "generated_runtime_primitivespecs_required": 0,
    "generated_collision_packages_required": 0,
    "runtime_admissibility_checks_required": 0,
    "newton_runtime_allowed": False,
    "real_usd_allowed": False,
    "benchmark_allowed": False,
    "silent_drop_allowed": False,
}
row = payload["runtime_boundary_preflight_rows"][0]
source_row = build_cpd_paper_offline_report()[
    "paper_mapped_subset_primitivespec_native_fixture_serialization_contract"
]["serialization_rows"][0]
assert set(row) == RUNTIME_BOUNDARY_PREFLIGHT_ROW_REQUIRED_KEYS
assert row["fixture_id"] == "paper_single_box"
assert row["primitive_spec_kind"] == "box"
assert row["source_native_fixture_primitivespec_serialization_row_id"] == (
    source_row["native_fixture_primitivespec_serialization_row_id"]
)
for source_key in (
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
):
    assert row[source_key] == source_row[source_key]
assert row["serialized_payload_schema_keys"] == sorted(
    source_row["serialized_payload"]
)
assert row["input_json_round_trip_equal"] is True
assert row["input_canonical_json_stable"] is True
assert row["input_schema_validation_status"] == "passed"
assert row["later_runtime_primitivespec_construction_candidate"] is True
assert row["runtime_construction_allowed_in_current_gate"] is False
assert row["required_later_gate"] == (
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT
)
assert row["runtime_instance_generated"] is False
assert row["generated_primitive_spec"] is None
for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
    assert payload[flag] is False
    assert row[flag] is False
```

- [ ] **Step 5: Add RED malformed-input tests**

Add `_runtime_boundary_preflight_input()` returning a deep-copied serialization payload from
`build_cpd_paper_offline_report()`.

Call the new private builder directly:

```python
cpd_paper_offline._paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract_payload(
    serialization
)
```

Cover:

- wrong input gate -> `primitivespec_runtime_boundary_preflight_input_gate_id_mismatch`;
- stale input next gate -> `primitivespec_runtime_boundary_preflight_input_next_gate_mismatch`;
- zero or duplicate serialization rows ->
  `primitivespec_runtime_boundary_preflight_serialization_row_count_mismatch`;
- wrong fixture -> `primitivespec_runtime_boundary_preflight_source_fixture_mismatch`;
- wrong kind -> `primitivespec_runtime_boundary_preflight_source_kind_mismatch`;
- missing serialized payload ->
  `primitivespec_runtime_boundary_preflight_serialized_payload_missing`;
- missing serialized schema key ->
  `primitivespec_runtime_boundary_preflight_serialized_payload_schema_mismatch`;
- stale `canonical_primitivespec_json` ->
  `primitivespec_runtime_boundary_preflight_canonical_json_mismatch`;
- `schema_keys` not matching the serialized payload keys ->
  `primitivespec_runtime_boundary_preflight_serialized_payload_schema_mismatch`;
- extra serialized payload key ->
  `primitivespec_runtime_boundary_preflight_serialized_payload_schema_mismatch`;
- false `json_round_trip_equal` ->
  `primitivespec_runtime_boundary_preflight_json_round_trip_missing`;
- canonical JSON round-trip mismatch ->
  `primitivespec_runtime_boundary_preflight_canonical_json_mismatch`;
- non-passed `schema_validation_status` ->
  `primitivespec_runtime_boundary_preflight_schema_validation_missing`;
- row-level `runtime_instance_generated=True` or `generated_primitive_spec={...}` ->
  `primitivespec_runtime_boundary_preflight_runtime_object_leak:<field>`;
- count drift -> `primitivespec_runtime_boundary_preflight_input_count_mismatch:<field>`;
- `paper_faithful_offline_allowed` or `package_generation_allowed` true ->
  `primitivespec_runtime_boundary_preflight_input_trigger_flag_true:<flag>`;
- runtime/package/Newton flag leak ->
  `primitivespec_runtime_boundary_preflight_input_trigger_flag_true:<flag>`.

- [ ] **Step 6: Add CLI RED assertions**

Extend `test_cli_run_cpd_paper_offline_report_emits_json()` to assert the new nested payload exists,
the top-level next gate/failure label have advanced to runtime-construction, and the nested row
keeps `runtime_construction_allowed_in_current_gate is False` with all runtime/package flags false.
Also assert `paper_faithfulness.implemented_output_contract_scope` includes
`paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract` after the serialization
gate.

- [ ] **Step 7: Add RED static runtime/package/Newton guard**

Add a test that inspects the source for the new helper block and proves it does not import or
instantiate runtime/package/Newton objects:

```python
def test_cpd_paper_runtime_boundary_preflight_helper_has_no_runtime_imports_or_calls():
    source = Path(cpd_paper_offline.__file__).read_text(encoding="utf-8")
    block = source[
        source.index("def _paper_validate_primitivespec_runtime_boundary_preflight_false_flags"):
        source.index("def _paper_source_policy_generalization_payload")
    ]

    forbidden_patterns = [
        "PrimitiveSpec(",
        "CollisionPackage(",
        "from primitive_collision_compiler.contracts import PrimitiveSpec",
        "from primitive_collision_compiler.contracts import CollisionPackage",
        "primitive_collision_compiler.newton",
        "import newton",
        "import newton_warp",
        "Newton",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in block
```

Place `RUNTIME_BOUNDARY_PREFLIGHT_PAYLOAD_REQUIRED_KEYS` and
`RUNTIME_BOUNDARY_PREFLIGHT_ROW_REQUIRED_KEYS` after `PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS` so
the starred tuple expansion is defined before the constants are created.

### Task 2: Implement Runtime-Boundary Preflight Payload

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add runtime-construction constant and remaining-gap helper**

Add:

```python
_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT = (
    "paper_mapped_subset_primitivespec_runtime_construction_contract"
)

def _paper_remaining_gaps_after_mapped_subset_primitivespec_runtime_boundary_preflight() -> list[str]:
    return [
        _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT
    ]
```

- [ ] **Step 2: Add input validation helpers**

Implement:

```python
def _paper_validate_primitivespec_runtime_boundary_preflight_false_flags(
    payload: dict[str, object],
) -> None:
    for field_name in ("paper_faithful_offline_allowed", "package_generation_allowed"):
        if bool(payload.get(field_name)):
            raise ValueError(
                "primitivespec_runtime_boundary_preflight_input_trigger_flag_true:"
                f"{field_name}"
            )
    for field_name in _paper_false_primitivespec_generation_flags():
        if bool(payload.get(field_name)):
            raise ValueError(
                "primitivespec_runtime_boundary_preflight_input_trigger_flag_true:"
                f"{field_name}"
            )
```

Implement `_paper_primitivespec_runtime_boundary_preflight_source_row(serialization)` to validate
the input gate, next gate, false flags, counts, one-row shape, fixture/kind fields, JSON/schema
booleans, serialized payload presence, and runtime-zero fields. Use the exact labels listed in the
spec. Validate that `schema_keys == sorted(serialized_payload)`, that
`canonical_primitivespec_json` equals strict canonical JSON for the payload, and that
`json.loads(canonical_primitivespec_json) == serialized_payload`. Reject row-level
`runtime_instance_generated=True` or non-`None` `generated_primitive_spec` using
`primitivespec_runtime_boundary_preflight_runtime_object_leak:<field>`.

- [ ] **Step 3: Add preflight row and coverage builders**

Implement `_paper_primitivespec_runtime_boundary_preflight_row(row)` returning the exact row fields
from Task 1 Step 2, including:

```python
"later_runtime_primitivespec_construction_candidate": True,
"runtime_construction_allowed_in_current_gate": False,
"required_later_gate": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT,
"preflight_decision": "later_runtime_primitivespec_construction_contract_may_be_proposed",
"preflight_reason": (
    "canonical_json_schema_stable_box_payload_but_current_gate_is_boundary_only"
),
"runtime_instance_generated": False,
"generated_primitive_spec": None,
**_paper_false_primitivespec_generation_flags(),
```

Implement `_paper_primitivespec_runtime_boundary_preflight_coverage_summary(rows)` with counts and
distributions for fixture, primitive kind, and preflight decision.

- [ ] **Step 4: Add payload builder**

Implement `_paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract_payload(serialization)`
returning the exact top-level fields from Task 1 Step 2, including:

```python
"gate_id": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT,
"input_gate_id": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_SERIALIZATION_CONTRACT,
"next_required_gate": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT,
"decision_reason": (
    "runtime_boundary_preflight_contract_complete_"
    "runtime_construction_contract_missing"
),
"artifact_kind": (
    "offline_runtime_boundary_preflight_not_runtime_primitivespec_"
    "not_collision_package"
),
"runtime_boundary_action": (
    "record_one_later_runtime_primitivespec_construction_candidate_without_runtime_object"
),
```

- [ ] **Step 5: Wire the payload into `build_cpd_paper_offline_report()`**

After serialization, build:

```python
mapped_subset_primitivespec_runtime_boundary_preflight = (
    _paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract_payload(
        mapped_subset_primitivespec_native_fixture_serialization
    )
)
```

Set `missing_before_paper_faithful` from the new remaining-gap helper, set top-level
`next_required_gate` to runtime-construction, append the runtime-boundary gate to
`implemented_output_contract_scope`, and add the payload under:

`paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`

### Task 3: Documentation, Registry, And Record

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
- Create: `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-runtime-boundary-preflight-contract.md`

- [ ] **Step 1: Update current-status docs**

Replace current-next-gate wording for the serialization gate with runtime-boundary completion
wording and set the new next gate to:

`paper_mapped_subset_primitivespec_runtime_construction_contract`

Use this bounded sentence wherever a short status is needed:

`paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract` is a command-only offline
boundary preflight that records one later runtime `PrimitiveSpec` construction candidate for the
synthetic `paper_single_box` OBB/box row, while creating zero runtime objects, zero
`CollisionPackage`s, zero runtime-admissibility checks, and no Newton, real-USD, benchmark,
collision-quality, deployment, safety, full-CPD, or `paper_faithful_offline` evidence.

- [ ] **Step 2: Update claim boundaries**

Add a `Do not describe` bullet for `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`
that blocks runtime object creation, package readiness, package conversion execution,
CollisionPackage generation, Newton support, runtime admissibility, approximation support, real-USD
evidence, benchmark evidence, collision-quality evidence, deployment readiness, safety
certification, package-generation gate completion, full CPD reproduction, and
`paper_faithful_offline` support.

Add a second bullet for `paper_mapped_subset_primitivespec_runtime_construction_contract` stating
that it is only a future missing gate until a later dated implementation record exists.

- [ ] **Step 3: Add dated record**

Create a record with:

```markdown
# 2026-05-17 CPD Paper Mapped-Subset PrimitiveSpec Runtime-Boundary Preflight Contract

## Summary

Implemented `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract` inside
`cpd_paper_offline_report`.

This is a command-only offline report contract. It records the boundary conditions for proposing a
later runtime `PrimitiveSpec` construction contract for the synthetic `paper_single_box` OBB/box
row.

## Status

Complete.

## Evidence

- Report key: `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`
- Input gate: `paper_mapped_subset_primitivespec_native_fixture_serialization_contract`
- Closed gate: `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`
- Next gate: `paper_mapped_subset_primitivespec_runtime_construction_contract`
- Runtime-boundary preflight rows: 1
- Later runtime construction candidates: 1
- Runtime construction allowed in current gate: false
- Generated runtime PrimitiveSpecs: 0
- Generated CollisionPackages: 0
- Runtime-admissibility checks: 0

## Nonclaims

This record does not claim runtime `PrimitiveSpec` object creation, `CollisionPackage` generation,
Newton support, runtime admissibility, real-USD evidence, benchmark evidence, collision-quality
validation, deployment readiness, safety certification, full CPD paper reproduction, or
`paper_faithful_offline` support.
```

- [ ] **Step 4: Update registry and record index**

Add the record to `docs/records/README.md` and add a complete registry entry in
`experiments/registry.yaml` with the command:

`PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report`

### Task 4: Verification, Review, Commit, Merge

**Files:**
- All modified files

- [ ] **Step 1: Run focused tests**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_boundary_preflight or native_fixture_serialization' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

- [ ] **Step 2: Run docs checks**

Run:

```bash
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

- [ ] **Step 3: Parallel review**

Dispatch three read-only reviewers:

- implementation/test reviewer for `offline.py`, `tests/test_cpd_paper_offline.py`, and
  `tests/test_cli.py`;
- docs/claim reviewer for all changed docs;
- hygiene reviewer for registry, record, ignored assets, caches, staging, and worktree status.

Address all blocking findings before committing.

- [ ] **Step 4: Run full verification**

Run:

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
PYTHONPATH=src python -m py_compile src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cpd_paper_offline.py tests/test_cli.py
```

- [ ] **Step 5: Commit, merge, push, and cleanup**

Commit:

```bash
git add README.md docs experiments src tests
git commit -m "feat: add CPD PrimitiveSpec runtime boundary preflight"
```

Fast-forward merge to `main`, push `origin main`, remove the temporary worktree, delete the branch,
and remove generated caches.
