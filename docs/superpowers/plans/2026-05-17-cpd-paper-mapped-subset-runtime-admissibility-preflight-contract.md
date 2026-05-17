# CPD Paper Mapped-Subset Runtime-Admissibility Preflight Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement `paper_mapped_subset_runtime_admissibility_preflight_contract` as an offline single-fixture preflight row for the existing `paper_single_box` package artifact.

**Architecture:** Extend the CPD paper offline report chain after `paper_mapped_subset_collision_package_generation_contract`. Validate the prior package artifact, record one compact runtime-admissibility preflight row without copying the full package dict, and advance the report to `paper_mapped_subset_runtime_admissibility_contract` while keeping all runtime/Newton/real-USD/benchmark/quality triggers false.

**Tech Stack:** Python report builders in `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`, `CollisionPackage.to_dict()` schema from `src/primitive_collision_compiler/contracts.py`, pytest, Markdown docs.

---

### Task 1: Add RED Tests For The Runtime-Admissibility Preflight Gate

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [x] **Step 1: Add expected next gate constant**

Add near the existing mapped-subset gate constants:

```python
EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT = (
    "paper_mapped_subset_runtime_admissibility_contract"
)
EXPECTED_RUNTIME_ADMISSIBILITY_PREFLIGHT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT,
]
```

- [x] **Step 2: Add helper for the new input payload**

Add near `_collision_package_generation_contract_input()`:

```python
def _runtime_admissibility_preflight_input() -> dict[str, object]:
    report = build_cpd_paper_offline_report()
    return json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_collision_package_generation_contract"
            ]
        )
    )
```

- [x] **Step 3: Add required-key sets**

Add after the existing collision-package key sets:

```python
RUNTIME_ADMISSIBILITY_PREFLIGHT_PAYLOAD_FALSE_FLAGS = (
    "paper_faithful_offline_allowed",
    "paper_faithful_offline_supported",
    *RUNTIME_CONSTRUCTION_FALSE_FLAGS,
)

RUNTIME_ADMISSIBILITY_PREFLIGHT_INPUT_FALSE_FLAGS = (
    *COLLISION_PACKAGE_GENERATION_BOUNDARY_FALSE_FLAGS,
)

RUNTIME_ADMISSIBILITY_PREFLIGHT_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "paper_faithful_offline_allowed",
    "paper_faithful_offline_supported",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "runtime_admissibility_preflight_action",
    "runtime_admissibility_preflight_requirements",
    "runtime_admissibility_preflight_row_count",
    "later_runtime_admissibility_candidate_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "source_collision_package_available",
    "runtime_admissibility_preflight_contract",
    "input_contract_summary",
    "runtime_admissibility_preflight_rows",
    "coverage_summary",
    "remaining_gaps",
    *RUNTIME_ADMISSIBILITY_PREFLIGHT_PAYLOAD_FALSE_FLAGS,
}

RUNTIME_ADMISSIBILITY_PREFLIGHT_ROW_REQUIRED_KEYS = {
    "runtime_admissibility_preflight_row_id",
    "source_collision_package_generation_row_id",
    "source_package_generation_preflight_row_id",
    "source_runtime_construction_row_id",
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
    "candidate_primitivespec_dict",
    "source_package_id",
    "source_asset_id",
    "source_package_stage",
    "source_package_status",
    "source_package_method",
    "source_package_source_path",
    "source_package_source_sha256",
    "source_package_claim_boundary",
    "source_package_primitive_count",
    "source_package_primitive_subset",
    "source_package_unsupported_primitives",
    "source_package_runtime_admissibility_status",
    "source_collision_package_available",
    "later_runtime_admissibility_candidate",
    "runtime_admissibility_preflight_decision",
    "required_later_gate",
    *RUNTIME_ADMISSIBILITY_PREFLIGHT_PAYLOAD_FALSE_FLAGS,
}
```

- [x] **Step 4: Add report and payload RED tests**

Add tests named:

```python
def test_cpd_paper_records_mapped_subset_runtime_admissibility_preflight_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report[
        "paper_mapped_subset_runtime_admissibility_preflight_contract"
    ]
    assert report["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT
    )
    assert report["failure_labels"] == [
        "paper_mapped_subset_runtime_admissibility_contract_missing"
    ]
    assert report["generated_collision_package_count"] == 1
    assert report["runtime_admissibility_check_count"] == 0
    assert (
        EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT
    )
    assert payload["runtime_admissibility_preflight_row_count"] == 1
    assert payload["later_runtime_admissibility_candidate_count"] == 1
    assert payload["generated_runtime_primitive_spec_count"] == 1
    assert payload["generated_primitive_spec_count"] == 1
    assert payload["generated_collision_package_count"] == 1
    assert payload["runtime_admissibility_check_count"] == 0
    assert payload["source_collision_package_available"] is True
    assert payload["runtime_admissibility_preflight_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
        ),
        "preflight_gate_closed": (
            EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT
        ),
        "next_runtime_admissibility_gate_required": (
            EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT
        ),
        "runtime_admissibility_preflight_rows_required": 1,
        "later_runtime_admissibility_candidates_required": 1,
        "generated_collision_packages_required": 1,
        "runtime_admissibility_checks_required": 0,
    }
    assert payload["remaining_gaps"] == (
        EXPECTED_RUNTIME_ADMISSIBILITY_PREFLIGHT_REMAINING_GAPS
    )


def test_cpd_paper_runtime_admissibility_preflight_payload_schema_is_exact():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_runtime_admissibility_preflight_contract"
    ]
    assert set(payload) == RUNTIME_ADMISSIBILITY_PREFLIGHT_PAYLOAD_REQUIRED_KEYS
    assert payload["artifact_kind"] == (
        "runtime_admissibility_preflight_not_runtime_check"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_package_preflight_only_no_runtime_admissibility_"
        "no_newton_no_real_usd_no_benchmark"
    )
    assert payload["source_collision_package_available"] is True
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["paper_faithful_offline_supported"] is False
    assert payload["input_contract_summary"] == {
        "input_gate_id": (
            EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
        ),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT
        ),
        "input_collision_package_generation_row_count": 1,
        "input_generated_collision_package_count": 1,
        "input_runtime_admissibility_check_count": 0,
        "source_row_id": (
            "collision_package_generation__paper_single_box__box"
        ),
        "source_package_id": (
            "paper_single_box:"
            "paper_mapped_subset_collision_package_generation_contract"
        ),
        "source_fixture_id": "paper_single_box",
        "source_primitive_spec_kind": "box",
    }
    assert payload["coverage_summary"] == {
        "runtime_admissibility_preflight_row_count": 1,
        "later_runtime_admissibility_candidate_record_count": 1,
        "generated_collision_package_record_count": 1,
        "runtime_admissibility_check_record_count": 0,
        "fixture_id_distribution": {"paper_single_box": 1},
        "primitive_subset_distribution": {"box": 1},
    }
```

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_admissibility_preflight' -q
```

Expected: fail because the payload is not implemented.

- [x] **Step 5: Add row, package-copy, and boundary RED tests**

Add tests named:

```python
def test_cpd_paper_runtime_admissibility_preflight_records_one_candidate_without_copying_package():
    report = build_cpd_paper_offline_report()
    source_payload = report[
        "paper_mapped_subset_collision_package_generation_contract"
    ]
    source_row = source_payload["collision_package_generation_rows"][0]
    source_package = source_row["generated_collision_package"]
    payload = report["paper_mapped_subset_runtime_admissibility_preflight_contract"]
    rows = payload["runtime_admissibility_preflight_rows"]

    assert len(rows) == 1
    row = rows[0]
    assert set(row) == RUNTIME_ADMISSIBILITY_PREFLIGHT_ROW_REQUIRED_KEYS
    assert row["source_collision_package_generation_row_id"] == (
        source_row["collision_package_generation_row_id"]
    )
    assert row["source_package_id"] == source_package["package_id"]
    assert row["source_asset_id"] == "paper_single_box"
    assert row["source_package_stage"] == (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
    )
    assert row["source_package_status"] == (
        "offline_synthetic_candidate_runtime_admissibility_not_checked"
    )
    assert row["source_package_method"] == "cpd_paper_mapped_subset_offline"
    assert row["source_package_source_path"] == (
        "synthetic://cpd-paper/paper_single_box"
    )
    assert row["source_package_source_sha256"] == source_package["source_sha256"]
    assert row["source_package_primitive_count"] == 1
    assert row["source_package_primitive_subset"] == ["box"]
    assert row["source_package_unsupported_primitives"] == []
    assert row["candidate_primitivespec_dict"] == (
        source_row["candidate_primitivespec_dict"]
    )
    assert row["source_collision_package_available"] is True
    assert row["later_runtime_admissibility_candidate"] is True
    assert row["runtime_admissibility_preflight_decision"] == (
        "eligible_for_later_runtime_admissibility_contract"
    )
    assert row["required_later_gate"] == (
        EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT
    )

    assert list(_recursive_package_dicts(payload)) == []
```

Add parameterized boundary tests that assert every
`RUNTIME_ADMISSIBILITY_PREFLIGHT_PAYLOAD_FALSE_FLAGS` field is false on the payload and row, and a
static source test that checks the new block contains no Newton, USD, runtime checker, benchmark,
or collision-quality tokens.

Add concrete source-drift rejection tests:

```python
@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "gate_id",
            "stale_gate",
            "runtime_admissibility_preflight_input_gate_id_mismatch",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "runtime_admissibility_preflight_input_next_gate_mismatch",
        ),
        (
            "collision_package_generation_row_count",
            2,
            "runtime_admissibility_preflight_input_count_mismatch:collision_package_generation_row_count",
        ),
        (
            "generated_collision_package_count",
            2,
            "runtime_admissibility_preflight_input_count_mismatch:generated_collision_package_count",
        ),
        (
            "runtime_admissibility_check_count",
            1,
            "runtime_admissibility_preflight_input_count_mismatch:runtime_admissibility_check_count",
        ),
    ],
)
def test_cpd_paper_runtime_admissibility_preflight_rejects_input_drift(
    field_name,
    bad_value,
    error_label,
):
    generation = _runtime_admissibility_preflight_input()
    generation[field_name] = bad_value

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_runtime_admissibility_preflight_contract_payload(
            generation
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "asset_id",
            "wrong_asset",
            "runtime_admissibility_preflight_package_mismatch:asset_id",
        ),
        (
            "package_id",
            "wrong_package",
            "runtime_admissibility_preflight_package_mismatch:package_id",
        ),
        (
            "source_path",
            "synthetic://wrong",
            "runtime_admissibility_preflight_package_mismatch:source_path",
        ),
        (
            "method",
            "wrong_method",
            "runtime_admissibility_preflight_package_mismatch:method",
        ),
        (
            "stage",
            "wrong_stage",
            "runtime_admissibility_preflight_package_mismatch:stage",
        ),
        (
            "status",
            "runtime_admissible",
            "runtime_admissibility_preflight_package_mismatch:status",
        ),
        (
            "source_sha256",
            "0" * 64,
            "runtime_admissibility_preflight_package_mismatch:source_sha256",
        ),
        (
            "primitive_subset",
            ["sphere"],
            "runtime_admissibility_preflight_package_mismatch:primitive_subset",
        ),
    ],
)
def test_cpd_paper_runtime_admissibility_preflight_rejects_package_drift(
    field_name,
    bad_value,
    error_label,
):
    generation = _runtime_admissibility_preflight_input()
    rows = [
        json.loads(json.dumps(row))
        for row in generation["collision_package_generation_rows"]
    ]
    rows[0]["generated_collision_package"][field_name] = bad_value
    generation["collision_package_generation_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_runtime_admissibility_preflight_contract_payload(
            generation
        )


@pytest.mark.parametrize(
    ("mutate_rows", "error_label"),
    [
        (
            lambda rows: [],
            "runtime_admissibility_preflight_row_count_mismatch",
        ),
        (
            lambda rows: [rows[0], json.loads(json.dumps(rows[0]))],
            "runtime_admissibility_preflight_row_count_mismatch",
        ),
    ],
)
def test_cpd_paper_runtime_admissibility_preflight_rejects_source_row_count_drift(
    mutate_rows,
    error_label,
):
    generation = _runtime_admissibility_preflight_input()
    generation["collision_package_generation_rows"] = mutate_rows(
        generation["collision_package_generation_rows"]
    )

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_runtime_admissibility_preflight_contract_payload(
            generation
        )


def test_cpd_paper_runtime_admissibility_preflight_rejects_extra_source_package_copy():
    generation = _runtime_admissibility_preflight_input()
    source_package = generation["collision_package_generation_rows"][0][
        "generated_collision_package"
    ]
    generation["unexpected_package_copy"] = json.loads(json.dumps(source_package))

    with pytest.raises(
        ValueError,
        match="runtime_admissibility_preflight_source_package_count_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_runtime_admissibility_preflight_contract_payload(
            generation
        )


def test_cpd_paper_runtime_admissibility_preflight_rejects_primitive_drift():
    generation = _runtime_admissibility_preflight_input()
    rows = [
        json.loads(json.dumps(row))
        for row in generation["collision_package_generation_rows"]
    ]
    rows[0]["generated_collision_package"]["primitives"][0]["kind"] = "sphere"
    generation["collision_package_generation_rows"] = rows

    with pytest.raises(
        ValueError,
        match="runtime_admissibility_preflight_package_mismatch:primitives",
    ):
        cpd_paper_offline._paper_mapped_subset_runtime_admissibility_preflight_contract_payload(
            generation
        )
```

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_admissibility_preflight' -q
```

Expected: fail because production code is still absent.

### Task 2: Implement The Offline Preflight Payload

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [x] **Step 1: Add the next gate constant**

Add near `_PAPER_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT`:

```python
_PAPER_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT = (
    "paper_mapped_subset_runtime_admissibility_contract"
)
```

- [x] **Step 2: Add remaining-gap helper**

Add near the collision-package generation remaining-gap helper:

```python
def _paper_remaining_gaps_after_mapped_subset_runtime_admissibility_preflight() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT]
```

- [x] **Step 3: Add validators and row builder**

Implement helpers after `_paper_mapped_subset_collision_package_generation_contract_payload`:

```python
def _paper_runtime_admissibility_preflight_source_row(
    generation: dict[str, object],
) -> dict[str, object]:
    ...

def _paper_runtime_admissibility_preflight_row(
    row: dict[str, object],
) -> dict[str, object]:
    ...

def _paper_mapped_subset_runtime_admissibility_preflight_contract_payload(
    generation: dict[str, object],
) -> dict[str, object]:
    ...
```

The implementation must validate the previous gate id, next gate, counts, exact generated package
key set, package id, asset id, source path, method, source package stage/status/claim boundary,
recomputed source SHA, primitive equality, exactly one recursive package-shaped dict in the input
gate, and false runtime/Newton boundary flags. It must store package identity, method, source path,
and SHA fields only, not the full package dict.

- [x] **Step 4: Wire the new payload into `build_cpd_paper_offline_report()`**

Construct the new payload after `mapped_subset_collision_package_generation` and use it for:

- top-level `missing_before_paper_faithful`;
- top-level `next_required_gate`;
- top-level `failure_labels`;
- `paper_faithfulness["implemented_output_contract_scope"]`;
- report key `paper_mapped_subset_runtime_admissibility_preflight_contract`.

- [x] **Step 5: Run GREEN tests**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_admissibility_preflight or collision_package_generation_contract' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Expected: pass.

### Task 3: Update Documentation And Records

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
- Create: `docs/records/2026-05-17-cpd-paper-mapped-subset-runtime-admissibility-preflight-contract.md`

- [x] **Step 1: Update current-state wording**

Replace the previous "next gate is runtime-admissibility preflight" wording with:

```markdown
The runtime-admissibility preflight contract is now implemented for the single synthetic
`paper_single_box` report-scoped `CollisionPackage.to_dict()` artifact. It records one later
runtime-admissibility candidate and zero runtime-admissibility checks. This is offline preflight
accounting, not package readiness or runtime admissibility. The next gate is
`paper_mapped_subset_runtime_admissibility_contract`.
```

- [x] **Step 2: Add a dated record**

Create a record with sections:

- Date
- Status
- Context
- What Changed
- Verification
- Artifacts
- Claim Boundary
- Claim Impact
- Next Gate
- Next Action

The record must state that this is not package readiness, not runtime admissibility, not Newton
support, not Newton execution, not real-USD evidence, not benchmark evidence, not
collision-quality evidence, not full CPD reproduction, not paper primitive vocabulary coverage,
not deployment readiness, and not safety certification.

- [x] **Step 3: Run docs validators**

Run:

```bash
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: pass.

### Task 4: Review, Verify, Commit, Merge, Push, And Clean Up

**Files:**
- All changed files

- [x] **Step 1: Request multiagent review**

Dispatch one code-contract reviewer and one docs-claim reviewer. Review scope:

- no runtime/Newton/real-USD/benchmark leakage;
- no duplicated package dict in the new payload;
- exact schema and count consistency;
- docs claim boundaries match implementation.

- [x] **Step 2: Fix review findings and rerun focused tests**

Run:

```bash
python -m py_compile src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cpd_paper_offline.py tests/test_cli.py
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_admissibility_preflight or collision_package_generation_contract' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Expected: pass.

- [x] **Step 3: Final verification**

Run:

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: pass.

- [ ] **Step 4: Commit, merge to main, push, and remove the worktree**

Use a commit message:

```bash
feat: add CPD runtime-admissibility preflight contract
```

After merge and push, verify `git status --short --branch` is clean on main and `git worktree list`
has no leftover feature worktree.
