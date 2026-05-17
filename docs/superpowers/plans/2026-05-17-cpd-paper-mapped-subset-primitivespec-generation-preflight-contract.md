# CPD Paper Mapped-Subset PrimitiveSpec Generation Preflight Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the command-only offline `paper_mapped_subset_primitivespec_generation_preflight_contract` gate without generating real `PrimitiveSpec` objects, `CollisionPackage`s, Newton runtime work, real-USD runs, benchmark evidence, or collision-quality claims.

**Architecture:** Extend the existing CPD paper offline report builder with one validated payload after `paper_mapped_subset_primitivespec_validation_contract`. The new payload validates the validation payload as input, emits family/current-row generation-preflight records with zero current candidates and zero generated specs, and advances the top-level next gate to the new mapped-subset `paper_mapped_subset_primitivespec_generation_contract`.

**Tech Stack:** Python, pytest, existing CPD paper offline report, Markdown docs, YAML experiment registry.

---

## File Map

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
  - Add `_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT`.
  - Add remaining-gap helper after generation preflight.
  - Add validation-input checks for `paper_mapped_subset_primitivespec_validation_contract`.
  - Add generation-preflight requirement/current row builders.
  - Wire generation-preflight payload into `build_cpd_paper_offline_report`.
- Modify: `tests/test_cpd_paper_offline.py`
  - Add RED tests for payload shape, six-family decisions, 16 current no-op rows, claim-boundary flags, duplicate/blank ids, wrong gates, nonzero counts, and malformed validation rows.
- Modify: `tests/test_cli.py`
  - Update CLI JSON assertions for the new top-level next gate and the new payload.
- Modify docs:
  - `README.md`
  - `docs/index.md`
  - `docs/deepdive/evidence-status.md`
  - `docs/reference/claim-boundaries.md`
  - `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
  - `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
  - `docs/reference/cpd-paper-reproduction-gap-matrix.md`
  - `docs/reference/cpd-paper-story-status.md`
  - `docs/records/README.md`
  - `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-generation-preflight-contract.md`
  - `experiments/registry.yaml`

## Task 1: Add RED Tests For Generation Preflight

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add import and expected constant**

In `tests/test_cpd_paper_offline.py`, add `_paper_mapped_subset_primitivespec_generation_preflight_contract_payload` to the import block. Add:

```python
EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT = (
    "paper_mapped_subset_primitivespec_generation_contract"
)
EXPECTED_GENERATION_PREFLIGHT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT,
]
```

- [ ] **Step 2: Update current top-level expected labels**

Change current top-level expected output so `build_cpd_paper_offline_report()` expects:

```python
EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT,
]
EXPECTED_GENERALIZATION_FAILURE_LABELS = [
    "paper_mapped_subset_primitivespec_generation_contract_missing",
]
```

Keep the validation payload's own `next_required_gate` and `remaining_gaps` as
`paper_mapped_subset_primitivespec_generation_preflight_contract`.

- [ ] **Step 3: Add generation-preflight gate shape test**

Add this test near the existing PrimitiveSpec validation tests:

```python
def test_cpd_paper_records_mapped_subset_primitivespec_generation_preflight_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report[
        "paper_mapped_subset_primitivespec_generation_preflight_contract"
    ]

    assert report["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
    )
    assert report["failure_labels"] == [
        "paper_mapped_subset_primitivespec_generation_contract_missing",
    ]
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_GENERATION_PREFLIGHT_REMAINING_GAPS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert (
        report["paper_mapped_subset_primitivespec_validation_contract"][
            "next_required_gate"
        ]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
    )
    assert (
        payload["gate_id"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
    )
    assert payload["gate_status"] == (
        "implemented_offline_primitivespec_generation_preflight_contract_only_partial"
    )
    assert payload["closed_gate"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
    )
    assert (
        payload["input_gate_id"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT
    )
    assert (
        payload["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "primitivespec_generation_preflight_contract_complete_"
        "primitivespec_generation_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "offline_primitivespec_generation_preflight_contract_not_primitivespec_"
        "not_collision_package"
    )
    assert payload["generation_preflight_candidate_count"] == 0
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_GENERATION_PREFLIGHT_REMAINING_GAPS
```

- [ ] **Step 4: Add six-family generation-preflight row test**

Add:

```python
def test_cpd_paper_primitivespec_generation_preflight_records_family_requirements():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_primitivespec_generation_preflight_contract"
    ]
    rows = {
        row["paper_primitive"]: row
        for row in payload[
            "primitive_spec_generation_preflight_requirement_rows"
        ]
    }

    assert list(rows) == [
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
    for primitive_name, kind in (
        ("oriented_bounding_box", "box"),
        ("sphere", "sphere"),
        ("capsule", "capsule"),
    ):
        row = rows[primitive_name]
        assert row["primitive_spec_generation_preflight_decision"] == (
            "future_native_family_generation_requirement_preflighted"
        )
        assert row["candidate_mapping_label"] == kind
        assert row["validated_future_primitive_spec_kind"] == kind
        assert row["generation_preflight_candidate"] is False
        assert (
            row["required_later_gate"]
            == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
        )
    assert rows["capped_cylinder"]["primitive_spec_generation_preflight_decision"] == (
        "blocked_approximation_policy_generation_preflight_recorded"
    )
    assert rows["frustum"]["primitive_spec_generation_preflight_decision"] == (
        "blocked_approximation_policy_generation_preflight_recorded"
    )
    assert rows["trapezoidal_prism"][
        "primitive_spec_generation_preflight_decision"
    ] == "noop_unmapped_family_generation_preflight_recorded"
```

- [ ] **Step 5: Add 16 current-row no-op generation-preflight test**

Add:

```python
def test_cpd_paper_primitivespec_generation_preflight_noops_current_unmapped_rows():
    report = build_cpd_paper_offline_report()
    validation = report["paper_mapped_subset_primitivespec_validation_contract"]
    payload = report[
        "paper_mapped_subset_primitivespec_generation_preflight_contract"
    ]
    summary = payload["coverage_summary"]
    rows = payload["current_row_primitivespec_generation_preflight_rows"]

    assert summary["primitive_spec_generation_preflight_requirement_row_count"] == 6
    assert summary["future_native_primitivespec_generation_preflight_count"] == 3
    assert summary["blocked_primitivespec_generation_preflight_requirement_count"] == 2
    assert summary["noop_primitivespec_generation_preflight_requirement_count"] == 1
    assert summary["current_row_primitivespec_generation_preflight_row_count"] == 16
    assert summary["current_primitivespec_generation_preflight_pass_record_count"] == 0
    assert summary["current_primitivespec_generation_preflight_noop_record_count"] == 16
    assert summary["generation_preflight_candidate_record_count"] == 0
    assert summary["generated_primitive_spec_record_count"] == 0

    validation_rows = validation["current_row_primitivespec_validation_rows"]
    assert len(rows) == len(validation_rows) == 16
    for row, upstream_row in zip(rows, validation_rows):
        assert row["source_primitivespec_validation_row_id"] == (
            upstream_row["primitive_spec_validation_row_id"]
        )
        assert row["source_primitivespec_dry_run_row_id"] == (
            upstream_row["source_primitivespec_dry_run_row_id"]
        )
        assert row["primitive_spec_generation_preflight_decision"] == (
            "skip_unmapped_current_row_preflighted"
        )
        assert row["primitive_spec_generation_preflight_action"] == "keep_offline"
        assert row["primitive_spec_generation_preflight_passed"] is False
        assert row["primitive_spec_generation_candidate"] is False
        assert row["generated_primitive_spec"] is None
        assert row["silent_drop_detected"] is False
        assert (
            row["required_later_gate"]
            == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
        )
```

- [ ] **Step 6: Add report-only boundary test**

Add a test asserting the payload and every emitted row do not contain keys named
`"PrimitiveSpec"`, `"CollisionPackage"`, `"runtime_result"`, `"usd_asset_path"`,
`"benchmark_metric"`, `"timing"`, `"surface_distance"`, or `"collision_quality"`. It must also
assert these top-level booleans are false:

```python
for flag in (
    "primitive_spec_generated",
    "collision_package_generated",
    "runtime_admissibility_checked",
    "newton_support_claimed",
    "approximation_policy_applied",
    "real_usd_loaded",
    "benchmark_run",
    "collision_quality_measured",
    "deployment_or_certification_claimed",
    "package_generation_triggered",
    "newton_runtime_triggered",
    "real_usd_triggered",
    "benchmark_triggered",
    "primitive_spec_generation_allowed",
    "collision_package_generation_allowed",
    "newton_runtime_allowed",
    "runtime_admissibility_supported",
    "approximation_policy_enabled",
    "silent_drop_allowed",
):
    assert payload[flag] is False
```

The same test must also assert every row in
`primitive_spec_generation_preflight_requirement_rows` and
`current_row_primitivespec_generation_preflight_rows` carries explicit false row-level trigger
flags:

```python
for row in (
    payload["primitive_spec_generation_preflight_requirement_rows"]
    + payload["current_row_primitivespec_generation_preflight_rows"]
):
    for flag in (
        "primitive_spec_generation_triggered",
        "collision_package_generation_triggered",
        "runtime_admissibility_triggered",
        "newton_runtime_triggered",
        "real_usd_loaded",
        "benchmark_run",
        "collision_quality_measured",
        "deployment_or_certification_claimed",
        "package_generation_triggered",
        "newton_runtime_triggered",
        "real_usd_triggered",
        "benchmark_triggered",
    ):
        assert row[flag] is False
```

- [ ] **Step 7: Add validation-failure tests**

Add tests that call `_paper_mapped_subset_primitivespec_generation_preflight_contract_payload(validation)` and expect `ValueError` for:

- wrong input `gate_id`: `primitivespec_generation_preflight_input_gate_id_mismatch`;
- top-level true trigger flag: `generation_preflight_input_trigger_flag_true:<flag>`;
- nonzero validated candidate count: `generation_preflight_input_candidate_count_nonzero`;
- nonzero generated spec count: `generation_preflight_input_generated_spec_nonzero`;
- nonzero generated collision package count: `generation_preflight_input_generated_collision_package_nonzero`;
- nonzero runtime check count: `generation_preflight_input_trigger_flag_true:runtime_admissibility_check_count`;
- bad coverage count: `generation_preflight_coverage_count_mismatch:<field>`;
- wrong six-family order: `generation_preflight_family_primitive_sequence_mismatch`;
- mutated future mapping label: `generation_preflight_future_mapping_label_mismatch:<paper_primitive>`;
- mutated family semantics: `generation_preflight_family_contract_mismatch:<paper_primitive>`;
- unknown requirement-row validation decision:
  `unknown_primitivespec_validation_family_decision:<decision>`;
- unknown current-row validation decision:
  `unknown_primitivespec_validation_current_decision:<decision>`;
- blank validation row id: `generation_preflight_missing_validation_row_id:<field>`;
- duplicate validation row id: `duplicate_primitivespec_validation_row_id`;
- row-level true trigger flag: `generation_preflight_input_trigger_flag_true:<flag>`;
- current-row generated spec: `generation_preflight_input_generated_spec_nonzero`;
- current-row pass or candidate: `generation_preflight_input_candidate_count_nonzero`;
- wrong current-row `required_later_gate`: `generation_preflight_current_row_required_later_gate_mismatch`;
- duplicate emitted id via direct `_paper_require_unique_generation_preflight_row_ids(rows)` helper
  test: `duplicate_primitivespec_generation_preflight_row_id`.

- [ ] **Step 8: Update CLI RED expectations**

In `tests/test_cli.py`, change the top-level expected failure label and next gate to
`paper_mapped_subset_primitivespec_generation_contract`. Add assertions for:

```python
generation_preflight = payload[
    "paper_mapped_subset_primitivespec_generation_preflight_contract"
]
assert generation_preflight["gate_id"] == (
    "paper_mapped_subset_primitivespec_generation_preflight_contract"
)
assert generation_preflight["input_gate_id"] == (
    "paper_mapped_subset_primitivespec_validation_contract"
)
assert generation_preflight["next_required_gate"] == (
    "paper_mapped_subset_primitivespec_generation_contract"
)
assert generation_preflight["generation_preflight_candidate_count"] == 0
assert generation_preflight["generated_primitive_spec_count"] == 0
assert (
    generation_preflight["coverage_summary"][
        "primitive_spec_generation_preflight_requirement_row_count"
    ]
    == 6
)
assert (
    generation_preflight["coverage_summary"][
        "future_native_primitivespec_generation_preflight_count"
    ]
    == 3
)
assert (
    generation_preflight["coverage_summary"][
        "current_row_primitivespec_generation_preflight_row_count"
    ]
    == 16
)
assert (
    generation_preflight["coverage_summary"][
        "generation_preflight_candidate_record_count"
    ]
    == 0
)
```

- [ ] **Step 9: Run RED focused tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k 'primitivespec_generation_preflight or offline_report_covers_first_toy_slice' -q
python -m pytest tests/test_cli.py -k cpd_paper_offline -q
```

Expected: fail because the generation-preflight builder and report payload do not exist yet.

## Task 2: Implement The Offline Generation-Preflight Payload

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add constant and remaining-gap helper**

Add beside the PrimitiveSpec gate constants:

```python
_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT = (
    "paper_mapped_subset_primitivespec_generation_contract"
)
```

Add beside the remaining-gap helpers:

```python
def _paper_remaining_gaps_after_mapped_subset_primitivespec_generation_preflight() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT]
```

Do not use `_PAPER_PACKAGE_GENERATION_CONTRACT` for this slice.

- [ ] **Step 2: Add expected validation-input semantics**

Add constants near the existing PrimitiveSpec validation helpers:

```python
_PRIMITIVESPEC_GENERATION_PREFLIGHT_EXPECTED_FAMILY_REQUIREMENTS = {
    "oriented_bounding_box": {
        "primitive_spec_validation_decision": (
            "future_native_family_primitivespec_shape_requirement_validated"
        ),
        "candidate_mapping_label": "box",
        "validated_future_primitive_spec_kind": "box",
    },
    "sphere": {
        "primitive_spec_validation_decision": (
            "future_native_family_primitivespec_shape_requirement_validated"
        ),
        "candidate_mapping_label": "sphere",
        "validated_future_primitive_spec_kind": "sphere",
    },
    "capsule": {
        "primitive_spec_validation_decision": (
            "future_native_family_primitivespec_shape_requirement_validated"
        ),
        "candidate_mapping_label": "capsule",
        "validated_future_primitive_spec_kind": "capsule",
    },
    "capped_cylinder": {
        "primitive_spec_validation_decision": (
            "blocked_approximation_policy_validation_recorded"
        ),
        "candidate_mapping_label": "offline_only_unmapped",
        "validated_future_primitive_spec_kind": None,
    },
    "frustum": {
        "primitive_spec_validation_decision": (
            "blocked_approximation_policy_validation_recorded"
        ),
        "candidate_mapping_label": "offline_only_unmapped",
        "validated_future_primitive_spec_kind": None,
    },
    "trapezoidal_prism": {
        "primitive_spec_validation_decision": "noop_unmapped_family_validation_recorded",
        "candidate_mapping_label": "offline_only_unmapped",
        "validated_future_primitive_spec_kind": None,
    },
}
```

- [ ] **Step 3: Add validation-input checker**

Add `_paper_validate_primitivespec_generation_preflight_validation(validation)` after
`_paper_mapped_subset_primitivespec_validation_contract_payload`. It must:

- require `validation["gate_id"] == _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT`;
- require every false trigger flag to be false;
- require top-level generated/candidate/runtime counts to be zero;
- require exact coverage counts from the validation payload;
- require exactly six requirement rows and sixteen current rows;
- require family row order equal to `_PRIMITIVESPEC_VALIDATION_EXPECTED_FAMILY_ORDER`;
- require each validation row id and source id to be non-empty;
- require requirement-row semantics to match `_PRIMITIVESPEC_GENERATION_PREFLIGHT_EXPECTED_FAMILY_REQUIREMENTS`;
- require current-row decision `skip_unmapped_current_row_validated`;
- require current-row `required_later_gate == _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT`;
- require row ids to be unique.

- [ ] **Step 4: Add row builders**

Add `_paper_primitivespec_generation_preflight_requirement_row(row)`,
`_paper_primitivespec_generation_preflight_current_row(row)`, and
`_paper_require_unique_generation_preflight_row_ids(rows)`.

The requirement builder must emit `primitive_spec_generation_preflight_row_id` as
`f"{row['primitive_spec_validation_row_id']}:generation_preflight"`, copy all source ids, set
`required_later_gate` to `_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT`, and set
`generation_preflight_candidate` to `False`. It must also emit explicit false flags for
`primitive_spec_generation_triggered`, `collision_package_generation_triggered`,
`runtime_admissibility_triggered`, `newton_runtime_triggered`, `real_usd_loaded`,
`benchmark_run`, `collision_quality_measured`, `deployment_or_certification_claimed`,
`package_generation_triggered`, `real_usd_triggered`, and `benchmark_triggered`.

The current-row builder must emit `primitive_spec_generation_preflight_row_id` the same way, copy
all source ids, set `primitive_spec_generation_preflight_decision` to
`skip_unmapped_current_row_preflighted`, set `primitive_spec_generation_preflight_action` to
`keep_offline`, keep `primitive_spec_generation_candidate` false, keep
`generated_primitive_spec` as `None`, keep `silent_drop_detected` false, and set
`required_later_gate` to `_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT`. It must emit the
same explicit false row-level trigger flags as the requirement-row builder.

`_paper_require_unique_generation_preflight_row_ids(rows)` must scan emitted
`primitive_spec_generation_preflight_row_id` values after row building and raise
`ValueError("duplicate_primitivespec_generation_preflight_row_id")` on duplicates. This helper is
tested directly because valid input validation row ids already make duplicate emitted ids
unreachable through the full payload builder.

- [ ] **Step 5: Add payload builder**

Add `_paper_mapped_subset_primitivespec_generation_preflight_contract_payload(validation)`. It must
call the input checker, build requirement/current rows, compute coverage summary fields named in
the design, verify emitted row ids are unique, and return a payload with:

```python
"gate_id": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
"input_gate_id": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT
"next_required_gate": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
"decision_reason": (
    "primitivespec_generation_preflight_contract_complete_"
    "primitivespec_generation_contract_missing"
)
"remaining_gaps": [
    _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT,
]
```

All generation/runtime/real-USD/benchmark/collision-quality/deployment booleans must remain false.

- [ ] **Step 6: Wire report builder**

In `build_cpd_paper_offline_report()`, after validation:

```python
mapped_subset_primitivespec_generation_preflight = (
    _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(
        mapped_subset_primitivespec_validation
    )
)
missing_before_paper_faithful = (
    _paper_remaining_gaps_after_mapped_subset_primitivespec_generation_preflight()
)
```

Update top-level `next_required_gate`, `implemented_output_contract_scope`, and the returned report
dictionary to include `paper_mapped_subset_primitivespec_generation_preflight_contract`.

- [ ] **Step 7: Run GREEN focused tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k 'primitivespec_generation_preflight or primitivespec_validation or offline_report_covers_first_toy_slice' -q
python -m pytest tests/test_cli.py -k cpd_paper_offline -q
```

Expected: pass.

## Task 3: Update Documentation And Registry

**Files:**
- Modify: `README.md`
- Modify: `docs/index.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/records/README.md`
- Create: `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-generation-preflight-contract.md`
- Modify: `experiments/registry.yaml`

- [ ] **Step 1: Update canonical status wording**

Update the docs listed above to say:

- generation preflight is now implemented as an offline/report-only gate;
- it consumes the validation contract and emits zero current PrimitiveSpec candidates;
- it keeps OBB/box, sphere, and capsule as future native family requirements;
- it keeps capped cylinder and frustum blocked behind approximation policy;
- it keeps trapezoidal prism no-op/unmapped;
- it does not generate real PrimitiveSpecs, CollisionPackages, package readiness, Newton runtime,
  real-USD evidence, benchmark evidence, collision-quality evidence, deployment readiness, or safety
  certification;
- the next gate is `paper_mapped_subset_primitivespec_generation_contract`.

- [ ] **Step 2: Add dated record**

Create `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-generation-preflight-contract.md` with:

```markdown
# CPD Paper Mapped-Subset PrimitiveSpec Generation Preflight Contract

## Date

2026-05-17

## Decision

Implemented `paper_mapped_subset_primitivespec_generation_preflight_contract` as an offline,
command-only report gate after `paper_mapped_subset_primitivespec_validation_contract`.

## Evidence

- The report now includes `paper_mapped_subset_primitivespec_generation_preflight_contract`.
- The top-level next gate is `paper_mapped_subset_primitivespec_generation_contract`.
- Six family generation-preflight rows are recorded.
- Sixteen current rows remain no-op/offline.
- Generation-preflight candidate count is zero.
- Generated PrimitiveSpec count is zero.
- Generated CollisionPackage count is zero.
- Runtime admissibility check count is zero.

## Claim Boundary

This is not real PrimitiveSpec generation, not CollisionPackage generation, not package readiness,
not Newton runtime support, not real-USD evidence, not benchmark evidence, not collision-quality
evidence, not deployment readiness, and not safety certification.

## Next Gate

`paper_mapped_subset_primitivespec_generation_contract`
```

- [ ] **Step 3: Update registry**

Add a registry entry with the new gate id and record path. Keep artifact paths to Markdown/config
only; do not add raw USD or generated 3D assets.

- [ ] **Step 4: Run docs checks**

Run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all exit `0`.

## Task 4: Review, Verify, Commit, Merge, Push, Clean

**Files:**
- All modified files from Tasks 1-3.

- [ ] **Step 1: Request multi-agent review**

Send two independent review prompts:

- Reviewer A: code/contract correctness against tests and design.
- Reviewer B: docs/claim-boundary correctness against `AGENTS.md` and `docs/reference/claim-boundaries.md`.

Fix Critical and Important findings before proceeding.

- [ ] **Step 2: Run focused verification**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all exit `0`.

- [ ] **Step 3: Run full verification**

Run:

```bash
python -m pytest -q
```

Expected: all tests pass.

- [ ] **Step 4: Commit implementation**

Run:

```bash
git status --short
git add README.md docs experiments src tests
git commit -m "feat: add CPD PrimitiveSpec generation preflight contract"
```

- [ ] **Step 5: Merge and push**

From the main worktree:

```bash
git checkout main
git pull --ff-only
git merge --no-ff cpd-paper-primitivespec-generation-preflight-contract -m "merge CPD PrimitiveSpec generation preflight contract"
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
python -m pytest -q
git push origin main
```

- [ ] **Step 6: Clean worktree**

After the merge and push have fresh verification evidence:

```bash
git worktree remove .worktrees/cpd-paper-primitivespec-generation-preflight-contract
git branch -d cpd-paper-primitivespec-generation-preflight-contract
git status --short --branch
```

Expected: main is clean and matches `origin/main`.

## Self-Review

- The plan creates one offline report gate, not a broad package-generation project.
- It uses a new mapped-subset generation contract gate and does not reuse `paper_package_generation_contract`.
- It keeps validation payload semantics intact: validation still points to generation preflight.
- It keeps all current generation counts at zero.
- It requires exact six-family and sixteen-current-row coverage.
- It preserves claim boundaries for Newton, real USD, benchmarks, collision quality, deployment, and safety.
