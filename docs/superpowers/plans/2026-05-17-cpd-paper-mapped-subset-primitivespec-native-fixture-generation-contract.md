# CPD Paper Mapped-Subset PrimitiveSpec Native Fixture Generation Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a command-only offline gate that emits exactly one serialized PrimitiveSpec-like dict
for the synthetic `paper_single_box` OBB/box current fixture source row.

**Architecture:** Extend `cpd_paper/offline.py` with one new payload builder after
`_paper_mapped_subset_native_current_fixture_contract_payload()`. The builder validates the prior
native-current fixture contract, constructs one report-only dict shaped like `PrimitiveSpec.to_dict()`
without instantiating `PrimitiveSpec`, and updates the top-level CPD paper report chain.

**Tech Stack:** Python, pytest, existing CPD paper offline report schema, Markdown docs.

---

### Task 1: RED Tests For New Gate

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add constants and required key sets**

Add:

```python
EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_SERIALIZATION_CONTRACT = (
    "paper_mapped_subset_primitivespec_native_fixture_serialization_contract"
)
EXPECTED_NATIVE_FIXTURE_GENERATION_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_SERIALIZATION_CONTRACT,
]
```

Add exact key sets:

```python
SERIALIZED_PRIMITIVESPEC_LIKE_DICT_REQUIRED_KEYS = {
    "primitive_id",
    "kind",
    "pose",
    "center",
    "axes",
    "dimensions",
    "frame",
    "source_faces",
    "contains_assigned_points",
    "volume",
    "weighted_volume",
    "conversion_status",
}
```

- [ ] **Step 2: Add RED report tests**

Add tests that currently fail because the payload key is missing:

```python
payload = build_cpd_paper_offline_report()[
    "paper_mapped_subset_primitivespec_native_fixture_generation_contract"
]
```

Assert gate id, exact schema, one source row, one offline serialized dict, zero runtime
PrimitiveSpecs, zero packages, zero runtime checks, and false runtime/package/evaluation flags.

- [ ] **Step 3: Add RED malformed-input tests**

Call the new private builder directly:

```python
cpd_paper_offline._paper_mapped_subset_primitivespec_native_fixture_generation_contract_payload(
    native_current_fixture
)
```

Cover wrong gate, stale next gate, row-count mismatch, ineligible source, non-candidate source,
preexisting generated spec, kind/runtime drift, invalid geometry, empty source faces, and trigger
flag leaks.

- [ ] **Step 4: Add CLI RED assertions**

Extend the CPD paper CLI report test to assert the new payload exists, top-level failure label
advances to the serialization gate, and the one offline serialized dict has the expected box fields.

- [ ] **Step 5: Run RED tests**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'native_fixture_generation or native_current_fixture' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Expected: new native-fixture-generation tests fail with missing payload/helper errors while existing
native-current-fixture tests still pass.

### Task 2: Production Implementation

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add constants and remaining-gap helper**

Add:

```python
_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_SERIALIZATION_CONTRACT = (
    "paper_mapped_subset_primitivespec_native_fixture_serialization_contract"
)
```

Return that gate from a new `_paper_remaining_gaps_after_mapped_subset_primitivespec_native_fixture_generation()`.

- [ ] **Step 2: Add input validators**

Validate the prior native-current fixture payload and the single source row with
generation-specific error labels. Reject any runtime/package/Newton/real-USD/benchmark/collision
flag leak.

- [ ] **Step 3: Add serialized dict builder**

Build this dict from the source row without importing or instantiating `PrimitiveSpec`:

```python
{
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

- [ ] **Step 4: Add payload builder and wire report chain**

Add `paper_mapped_subset_primitivespec_native_fixture_generation_contract` to
`build_cpd_paper_offline_report()`, update `next_required_gate`, `failure_labels`,
`missing_before_paper_faithful_offline`, and `implemented_output_contract_scope`.

- [ ] **Step 5: Run GREEN tests**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'native_fixture_generation or native_current_fixture' -q
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
- Create: `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-native-fixture-generation-contract.md`

- [ ] **Step 1: Update current story wording**

Say the slice emits one report-only serialized PrimitiveSpec-like dict row, not runtime
PrimitiveSpec object creation.

- [ ] **Step 2: Update next gate wording**

Set the current next gate to
`paper_mapped_subset_primitivespec_native_fixture_serialization_contract`.

- [ ] **Step 3: Add record and registry entry**

Record command, scope, evidence, and explicit non-claims.

- [ ] **Step 4: Run docs validation**

Run:

```bash
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

### Task 4: Review, Full Verification, Commit

**Files:**
- All changed files

- [ ] **Step 1: Request multi-agent review**

Ask implementation and docs reviewers to inspect the diff before merge.

- [ ] **Step 2: Fix review findings with RED/GREEN tests**

For any blocker, add or adjust focused tests before production changes.

- [ ] **Step 3: Run full verification**

Run:

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

- [ ] **Step 4: Commit**

Commit with:

```bash
git add README.md docs experiments src tests
git commit -m "feat: add CPD native fixture PrimitiveSpec dict contract"
```

