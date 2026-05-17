# CPD Paper Mapped-Subset PrimitiveSpec Runtime Construction Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `paper_mapped_subset_primitivespec_runtime_construction_contract` gate that constructs exactly one runtime `PrimitiveSpec` from the validated synthetic `paper_single_box` OBB/box preflight row.

**Architecture:** Extend the existing `cpd_paper_offline_report` gate chain in `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`. The new helper consumes the runtime-boundary preflight payload, validates the contract, constructs one `PrimitiveSpec`, stores only `PrimitiveSpec.to_dict()` in the JSON report, and advances the next gate to `paper_mapped_subset_collision_package_generation_preflight_contract`.

**Tech Stack:** Python dataclasses, pytest, existing CPD paper offline report helpers, existing docs validators.

---

### Task 1: Add RED Tests For Runtime Construction Contract

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`

- [ ] **Step 1: Add constants and expected gaps**

Add `EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT` next to the existing runtime-construction constant:

```python
EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_collision_package_generation_preflight_contract"
)
```

Change `EXPECTED_RUNTIME_BOUNDARY_PREFLIGHT_REMAINING_GAPS` to expect the runtime-construction
gate as before, and add:

```python
EXPECTED_RUNTIME_CONSTRUCTION_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT,
]
```

Update the shared current gap list used by `EXPECTED_GENERALIZATION_FAILURE_LABELS` so the current
missing output contract becomes
`EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT`, not the runtime
construction contract.

Also update direct top-level next-gate assertions that currently expect
`EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT`. The report-level next gate
must move to `EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT`; only the
runtime-boundary preflight payload should keep
`payload["next_required_gate"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT`.

- [ ] **Step 2: Add helper input**

Add near `_runtime_boundary_preflight_input()`:

```python
def _runtime_construction_input() -> dict[str, object]:
    report = build_cpd_paper_offline_report()
    return json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract"
            ]
        )
    )
```

- [ ] **Step 3: Add required key sets**

Add `RUNTIME_CONSTRUCTION_PAYLOAD_REQUIRED_KEYS` and `RUNTIME_CONSTRUCTION_ROW_REQUIRED_KEYS`
near the runtime-boundary required key sets.

Use this row key set:

```python
RUNTIME_CONSTRUCTION_ROW_REQUIRED_KEYS = {
    "runtime_construction_row_id",
    "source_runtime_boundary_preflight_row_id",
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
    "canonical_primitivespec_json",
    "loaded_primitivespec_payload",
    "constructed_primitivespec_dict",
    "conversion_status_transition",
    "runtime_instance_generated",
    "generated_primitive_spec",
    "runtime_primitivespec_construction_triggered",
    "collision_package_generated",
    "runtime_admissibility_checked",
    "newton_support_claimed",
    "approximation_policy_applied",
    "real_usd_loaded",
    "benchmark_run",
    "package_generation_allowed",
    "collision_package_generation_allowed",
    "runtime_admissibility_supported",
    "newton_runtime_allowed",
    "approximation_policy_enabled",
    "silent_drop_allowed",
    "collision_package_generation_triggered",
    "runtime_admissibility_triggered",
    "newton_runtime_triggered",
    "real_usd_triggered",
    "benchmark_triggered",
    "collision_quality_measured",
    "deployment_or_certification_claimed",
}
```

- [ ] **Step 4: Add report-level RED test**

Add:

```python
def test_cpd_paper_records_mapped_subset_primitivespec_runtime_construction_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report[
        "paper_mapped_subset_primitivespec_runtime_construction_contract"
    ]

    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT
    )
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_RUNTIME_CONSTRUCTION_REMAINING_GAPS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT
    )
    assert payload["runtime_construction_row_count"] == 1
    assert payload["constructed_runtime_primitivespec_count"] == 1
    assert payload["generated_runtime_primitive_spec_count"] == 1
    assert payload["generated_primitive_spec_count"] == 1
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_RUNTIME_CONSTRUCTION_REMAINING_GAPS
```

- [ ] **Step 5: Add row, boundary, and malformed-input tests**

Add tests that assert:

- `set(payload) == RUNTIME_CONSTRUCTION_PAYLOAD_REQUIRED_KEYS`;
- `set(row) == RUNTIME_CONSTRUCTION_ROW_REQUIRED_KEYS`;
- `row["loaded_primitivespec_payload"]` equals the dict loaded from the row's canonical JSON;
- `row["constructed_primitivespec_dict"]` matches the source geometry, dimensions, ids, and
  lineage fields;
- `row["loaded_primitivespec_payload"]` comes from `json.loads(row["canonical_primitivespec_json"])`
  because the preflight row does not carry `serialized_payload`;
- `row["constructed_primitivespec_dict"]["conversion_status"] == "runtime_primitivespec_constructed_from_canonical_preflight_payload"`;
- `row["conversion_status_transition"] == {
  "from": "report_only_offline_serialized_primitivespec_like_dict_not_runtime_object",
  "to": "runtime_primitivespec_constructed_from_canonical_preflight_payload",
}`;
- `row["runtime_instance_generated"] is True`;
- `row["generated_primitive_spec"] == row["constructed_primitivespec_dict"]`;
- `payload["generated_collision_package_count"] == 0`;
- the full runtime-construction block contains exactly one `PrimitiveSpec(` and the one allowed
  local import, and does not contain `CollisionPackage`, `FallbackSpec`, Newton calls/imports, USD
  loading tokens, `timeit`, `perf_counter`, `benchmark_metric`, `surface_distance`,
  `timing_result`, `collision_quality_score`, `run_benchmark`, or
  `measure_collision_quality`;
- top-level package/Newton/real-USD/benchmark/collision-quality/deployment flags remain false;
- `json.dumps(payload, allow_nan=False, sort_keys=True)` succeeds;
- no row stores a live `PrimitiveSpec` object;
- stale input gate, stale input next gate, row-count drift, missing candidate flag, true package or
  Newton flags, canonical JSON drift, and canonical payload value drift raise explicit
  `ValueError` labels.

- [ ] **Step 6: Run RED tests**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_construction or runtime_boundary_preflight' -q
```

Expected: fail because the runtime-construction payload and helper do not exist yet.

### Task 2: Implement Runtime Construction Helper

**Files:**

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add next-gate constant**

Add:

```python
_PAPER_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_collision_package_generation_preflight_contract"
)
```

- [ ] **Step 2: Add remaining-gap helper**

Add:

```python
def _paper_remaining_gaps_after_mapped_subset_primitivespec_runtime_construction() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT]
```

- [ ] **Step 3: Add input validator**

Add `_paper_primitivespec_runtime_construction_source_row(preflight)` that validates:

- input `gate_id` equals `_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT`;
- input `next_required_gate` equals `_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT`;
- input row count equals one;
- preflight row candidate is true;
- previous `runtime_construction_allowed_in_current_gate` is false;
- previous `runtime_instance_generated` is false and `generated_primitive_spec` is `None`;
- source fixture is `paper_single_box`;
- kind fields are all `box`;
- canonical JSON loads back to the expected serialized payload;
- package, runtime-admissibility, Newton, real-USD, benchmark, collision-quality, deployment, and
  certification flags remain false.

- [ ] **Step 4: Add constructor helper**

Add `_paper_construct_primitivespec_from_runtime_preflight_row(row)` with a local import:

```python
from primitive_collision_compiler.contracts import PrimitiveSpec
```

Load `payload = json.loads(row["canonical_primitivespec_json"])`, then instantiate:

```python
primitive = PrimitiveSpec(
    primitive_id=str(payload["primitive_id"]),
    kind=str(payload["kind"]),
    pose=tuple(float(value) for value in payload["pose"]),
    center=tuple(float(value) for value in payload["center"]),
    axes=tuple(
        tuple(float(value) for value in axis)
        for axis in payload["axes"]
    ),
    dimensions={
        "half_extents": [
            float(value)
            for value in payload["dimensions"]["half_extents"]
        ]
    },
    frame=str(payload["frame"]),
    source_faces=tuple(int(value) for value in payload["source_faces"]),
    contains_assigned_points=bool(payload["contains_assigned_points"]),
    volume=float(payload["volume"]),
    weighted_volume=float(payload["weighted_volume"]),
    conversion_status=(
        "runtime_primitivespec_constructed_from_canonical_preflight_payload"
    ),
)
```

Return `primitive.to_dict()`.

Do not read `row["serialized_payload"]` here; the preflight row intentionally carries only
canonical JSON and schema keys.

- [ ] **Step 5: Add row, coverage, and payload builders**

Add:

- `_paper_primitivespec_runtime_construction_row(source_row)`;
- `_paper_primitivespec_runtime_construction_coverage_summary(rows)`;
- `_paper_mapped_subset_primitivespec_runtime_construction_contract_payload(preflight)`.

The payload must store only dicts/lists/scalars and must set package/Newton/real-USD/benchmark
triggers false.

Do not spread `_paper_false_primitivespec_generation_flags()` into this new payload or row. Use a
runtime-construction-specific flag set: construction indicators true/count one, package/runtime
admissibility/Newton/real-USD/benchmark/collision-quality/deployment indicators false/count zero.
The false set must include generated, checked, claimed, allowed, supported, enabled, triggered,
loaded, run, measured, deployment/certification, approximation-policy, and silent-drop flags for
all forbidden package/runtime/Newton/real-USD/benchmark/collision-quality boundaries.

- [ ] **Step 6: Wire into report builder**

In `build_cpd_paper_offline_report()`:

- build `mapped_subset_primitivespec_runtime_construction` after preflight;
- compute `missing_before_paper_faithful` from
  `_paper_remaining_gaps_after_mapped_subset_primitivespec_runtime_construction()`;
- set top-level `next_required_gate` to
  `_PAPER_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT`;
- add the runtime-construction gate to `implemented_output_contract_scope`;
- add the payload under
  `"paper_mapped_subset_primitivespec_runtime_construction_contract"`.

- [ ] **Step 7: Run GREEN tests**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_construction or runtime_boundary_preflight' -q
```

Expected: all selected tests pass.

### Task 3: Update Documentation And Records

**Files:**

- Modify: `README.md`
- Modify: `docs/index.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/records/README.md`
- Create: `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-runtime-construction-contract.md`

- [ ] **Step 1: Update status wording**

Update each reference page so it says the runtime-construction contract creates exactly one runtime
`PrimitiveSpec` for `paper_single_box` and still creates zero `CollisionPackage` objects, zero
runtime-admissibility checks, zero Newton runtime records, zero real-USD evidence, zero benchmark
evidence, and zero collision-quality evidence.
Also state that this is not PrimitiveSpec readiness or a general PrimitiveSpec generation path; it
is one deterministic runtime-construction smoke only.

- [ ] **Step 2: Add dated record**

Add a record with sections:

- `## Date`
- `## Status`
- `## Context`
- `## What Changed`
- `## Verification`
- `## Artifacts`
- `## Claim Boundary`
- `## Claim Impact`
- `## Next Gate`
- `## Next Action`

- [ ] **Step 3: Run docs validation**

Run:

```bash
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: all commands exit 0.

### Task 4: Full Verification, Review, Commit, Merge

**Files:**

- Inspect all modified files.

- [ ] **Step 1: Run focused and full verification**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_construction or runtime_boundary_preflight' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report >/tmp/cpd_paper_runtime_construction_report.json
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: all commands exit 0.

- [ ] **Step 2: Request multi-agent review**

Dispatch reviewers for:

- implementation and TDD coverage;
- docs and claim boundaries;
- report schema and static boundary guards.

Fix Critical and Important findings before proceeding.

- [ ] **Step 3: Commit**

Run:

```bash
git add README.md docs src tests
git commit -m "feat: add CPD PrimitiveSpec runtime construction contract"
```

- [ ] **Step 4: Merge and push**

From main:

```bash
git merge --ff-only cpd-paper-runtime-construction-contract
git push origin main
```

- [ ] **Step 5: Clean worktree**

Remove the feature worktree after merge and delete the branch.
