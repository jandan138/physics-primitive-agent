# CPD Paper Mapped-Subset PrimitiveSpec Validation Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the command-only offline `paper_mapped_subset_primitivespec_validation_contract` gate without generating real `PrimitiveSpec` objects, `CollisionPackage`s, Newton runtime work, real-USD runs, benchmark evidence, or collision-quality claims.

**Architecture:** Extend the existing CPD paper offline report builder with one validated payload after `paper_mapped_subset_primitivespec_dry_run_contract`. The new payload validates the dry-run contract shape, records requirement/current-row validation accounting, keeps all current candidate and generation counts at zero, and advances the next gate to `paper_mapped_subset_primitivespec_generation_preflight_contract`.

**Tech Stack:** Python, pytest, existing CPD paper offline report, Markdown docs, YAML experiment registry.

---

## File Map

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
  - Add the generation-preflight next-gate constant.
  - Add remaining-gap helper after PrimitiveSpec validation.
  - Add dry-run validation helpers and validation row builders.
  - Wire validation payload into `build_cpd_paper_offline_report`.
- Modify: `tests/test_cpd_paper_offline.py`
  - Add RED tests for payload shape, family validation rows, current no-op validation rows, report-only boundary, and validation failures.
- Modify: `tests/test_cli.py`
  - Add CLI JSON assertions for the new payload and updated top-level next gate.
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
  - `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-validation-contract.md`
  - `experiments/registry.yaml`

## Task 1: Add RED Tests For The Validation Payload

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add import and expected constants**

In `tests/test_cpd_paper_offline.py`, add `_paper_mapped_subset_primitivespec_validation_contract_payload`
to the import block. Add constants:

```python
EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_primitivespec_generation_preflight_contract"
)
EXPECTED_VALIDATION_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT,
]
```

- [ ] **Step 2: Update current top-level expected labels**

Change the current top-level expected output so `build_cpd_paper_offline_report()` expects:

```python
EXPECTED_GENERALIZATION_FAILURE_LABELS = [
    "paper_mapped_subset_primitivespec_generation_preflight_contract_missing",
]
EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT,
]
```

Keep the dry-run payload's own `remaining_gaps` as
`["paper_mapped_subset_primitivespec_validation_contract"]`.

- [ ] **Step 3: Add validation gate shape test**

Add a test near the existing PrimitiveSpec dry-run tests:

```python
def test_cpd_paper_records_mapped_subset_primitivespec_validation_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_primitivespec_validation_contract"]

    assert report["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
    )
    assert report["failure_labels"] == [
        "paper_mapped_subset_primitivespec_generation_preflight_contract_missing",
    ]
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_VALIDATION_REMAINING_GAPS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert payload["gate_id"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT
    assert payload["gate_status"] == (
        "implemented_offline_primitivespec_validation_contract_only_partial"
    )
    assert payload["closed_gate"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT
    assert payload["input_gate_id"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT
    assert (
        payload["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "primitivespec_validation_contract_complete_"
        "primitivespec_generation_preflight_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "offline_primitivespec_validation_contract_not_primitivespec_"
        "not_collision_package"
    )
    assert payload["validated_primitive_spec_candidate_count"] == 0
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_VALIDATION_REMAINING_GAPS
```

- [ ] **Step 4: Add family validation row test**

Add a test asserting the six requirement rows map to the expected validation decisions:

```python
payload = build_cpd_paper_offline_report()[
    "paper_mapped_subset_primitivespec_validation_contract"
]
rows = {
    row["paper_primitive"]: row
    for row in payload["primitive_spec_validation_requirement_rows"]
}
assert list(rows) == [
    "oriented_bounding_box",
    "sphere",
    "capsule",
    "capped_cylinder",
    "frustum",
    "trapezoidal_prism",
]
assert rows["oriented_bounding_box"]["primitive_spec_validation_decision"] == (
    "future_native_family_primitivespec_shape_validated"
)
assert rows["oriented_bounding_box"]["validated_future_primitive_spec_kind"] == "box"
assert rows["sphere"]["validated_future_primitive_spec_kind"] == "sphere"
assert rows["capsule"]["validated_future_primitive_spec_kind"] == "capsule"
assert rows["capped_cylinder"]["primitive_spec_validation_decision"] == (
    "blocked_approximation_policy_validation_recorded"
)
assert rows["frustum"]["primitive_spec_validation_decision"] == (
    "blocked_approximation_policy_validation_recorded"
)
assert rows["trapezoidal_prism"]["primitive_spec_validation_decision"] == (
    "noop_unmapped_family_validation_recorded"
)
```

- [ ] **Step 5: Add current-row validation test**

Add a test asserting the 16 current rows remain no-op and traceable:

```python
payload = build_cpd_paper_offline_report()[
    "paper_mapped_subset_primitivespec_validation_contract"
]
summary = payload["coverage_summary"]
rows = payload["current_row_primitivespec_validation_rows"]
assert summary["primitive_spec_validation_requirement_row_count"] == 6
assert summary["future_native_primitivespec_shape_validation_count"] == 3
assert summary["blocked_primitivespec_validation_requirement_count"] == 3
assert summary["current_row_primitivespec_validation_row_count"] == 16
assert summary["current_primitivespec_validation_pass_record_count"] == 0
assert summary["current_primitivespec_validation_noop_record_count"] == 16
assert summary["validated_primitive_spec_candidate_record_count"] == 0
assert summary["generated_primitive_spec_record_count"] == 0
for row in rows:
    assert row["primitive_spec_validation_decision"] == (
        "skip_unmapped_current_row_validated"
    )
    assert row["primitive_spec_validation_action"] == "keep_offline"
    assert row["primitive_spec_validation_passed"] is False
    assert row["primitive_spec_candidate"] is False
    assert row["generated_primitive_spec"] is None
    assert row["silent_drop_detected"] is False
```

- [ ] **Step 6: Add report-only boundary test**

Add a test mirroring the dry-run report-only test. It must assert the validation payload and rows do
not contain keys named `"PrimitiveSpec"`, `"CollisionPackage"`, `"runtime_result"`,
`"usd_asset_path"`, `"benchmark_metric"`, `"timing"`, `"surface_distance"`, or
`"collision_quality"`, and that every generation/runtime/real-USD/benchmark/collision-quality/
deployment flag remains false.

- [ ] **Step 7: Add validation-failure tests**

Add tests that call `_paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)` and
expect `ValueError` for:

- wrong `gate_id`: `primitivespec_validation_input_gate_id_mismatch`;
- top-level true trigger flag: `validation_input_trigger_flag_true`;
- nonzero `candidate_count_at_dry_run`: `validation_input_candidate_count_nonzero`;
- missing required field in `primitive_spec_dry_run_contract`: `validation_required_fields_mismatch`;
- extra allowed runtime kind: `validation_allowed_runtime_kinds_mismatch`;
- duplicate `primitive_spec_dry_run_row_id`: `duplicate_primitivespec_dry_run_row_id`;
- unknown family decision: `unknown_primitivespec_dry_run_family_decision`;
- future-native family missing kind: `future_native_primitivespec_kind_missing`;
- row-level `primitive_spec_dry_run_passed=True`: `validation_input_pass_count_nonzero`;
- row-level `primitive_spec_candidate=True`: `validation_input_candidate_count_nonzero`;
- row-level generated spec not `None`: `validation_input_generated_spec_nonzero`;
- missing current source id: `validation_missing_current_row_source_id`;
- wrong `required_later_gate`: `validation_current_row_required_later_gate_mismatch`.

- [ ] **Step 8: Update CLI RED expectations**

In `tests/test_cli.py`, update the top-level next gate and failure label expectations to the
generation-preflight gate. Add assertions for
`payload["paper_mapped_subset_primitivespec_validation_contract"]` matching the shape and zero-count
constraints from Step 3 and Step 5.

- [ ] **Step 9: Run RED focused tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k 'primitivespec_validation or offline_report_covers_first_toy_slice' -q
python -m pytest tests/test_cli.py -k cpd_paper_offline -q
```

Expected: fail because `_paper_mapped_subset_primitivespec_validation_contract_payload` and the new
report payload do not exist yet.

## Task 2: Implement The Offline Validation Payload

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add constants and remaining-gap helper**

Add:

```python
_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_primitivespec_generation_preflight_contract"
)


def _paper_remaining_gaps_after_mapped_subset_primitivespec_validation() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT]
```

- [ ] **Step 2: Add validation row helpers**

Add `_paper_primitivespec_validation_requirement_row(row)` and
`_paper_primitivespec_validation_current_row(row)` after the dry-run payload. The requirement helper
must translate known dry-run decisions into the three validation decisions described above. The
current helper must accept only `skip_unmapped_current_row`, preserve all source ids, and emit
`silent_drop_detected: False`.

- [ ] **Step 3: Add input validator**

Add `_paper_validate_primitivespec_validation_dry_run(dry_run)`. It must validate the input gate,
top-level false trigger flags, zero candidate/generated/runtime counts, exact required field set,
exact allowed runtime kind set, unique dry-run row ids, known family/current decisions, source-id
preservation, no row-level pass, no row-level candidate, no generated spec, and required later gate
equal to `paper_mapped_subset_primitivespec_validation_contract`.

- [ ] **Step 4: Add payload builder**

Add `_paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)`. It must call the
validator, build requirement/current rows, compute coverage counts, keep all generation/runtime
flags false, and return the payload fields from the design doc.

- [ ] **Step 5: Wire top-level report**

In `build_cpd_paper_offline_report()`:

1. Build `mapped_subset_primitivespec_validation` after `mapped_subset_primitivespec_dry_run`.
2. Set `missing_before_paper_faithful` from
   `_paper_remaining_gaps_after_mapped_subset_primitivespec_validation()`.
3. Set top-level `next_required_gate` to
   `_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT`.
4. Add `_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT` to
   `implemented_output_contract_scope`.
5. Add `"paper_mapped_subset_primitivespec_validation_contract"` to the returned report.

- [ ] **Step 6: Run GREEN focused tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k 'primitivespec_validation or offline_report_covers_first_toy_slice' -q
python -m pytest tests/test_cli.py -k cpd_paper_offline -q
```

Expected: all selected tests pass.

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
- Create: `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-validation-contract.md`
- Modify: `experiments/registry.yaml`

- [ ] **Step 1: Update reference docs**

Update the CPD paper story, lane spec, gap matrix, fixture breadth plan, claim boundaries, and
DeepDive evidence status to say:

```text
paper_mapped_subset_primitivespec_validation_contract is implemented as a command-only offline
validation contract. It validates the dry-run contract shape and zero-candidate/no-op behavior. It
does not generate PrimitiveSpec objects, CollisionPackages, Newton runtime evidence, real-USD
evidence, benchmark evidence, or collision-quality evidence. The next gate is
paper_mapped_subset_primitivespec_generation_preflight_contract.
```

- [ ] **Step 2: Add dated record**

Create `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-validation-contract.md` with:

```markdown
# CPD Paper Mapped-Subset PrimitiveSpec Validation Contract

## Date

2026-05-17

## Decision

Implement `paper_mapped_subset_primitivespec_validation_contract` as a command-only offline
validation contract after the PrimitiveSpec dry-run contract.

## What Changed

- The CPD paper offline report now records PrimitiveSpec validation requirement rows for six paper
  primitive families.
- The report now records 16 current no-op validation rows for unmapped trapezoidal-prism rows.
- The report keeps current candidates, generated PrimitiveSpecs, generated CollisionPackages,
  runtime admissibility checks, Newton runtime, real-USD loading, benchmark runs, collision-quality
  measurement, and deployment/certification claims at zero or false.

## Boundary

This is not PrimitiveSpec generation, CollisionPackage generation, package readiness, runtime
admissibility, Newton support, real-USD evidence, benchmark evidence, collision-quality evidence, or
deployment readiness.

## Next Gate

`paper_mapped_subset_primitivespec_generation_preflight_contract`
```

- [ ] **Step 3: Update registry**

Add an `experiments/registry.yaml` entry for the validation contract with explicit notes that the
artifact is report-only and keeps all generation/runtime/evaluation flags false.

- [ ] **Step 4: Validate docs**

Run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all commands exit 0.

## Task 4: Review, Full Verification, And Merge Prep

**Files:**
- Review all modified files.

- [ ] **Step 1: Run focused tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
```

Expected: `180+` tests pass, with the exact count read from pytest output.

- [ ] **Step 2: Run full tests**

Run:

```bash
python -m pytest -q
```

Expected: full suite passes. If the ignored paper source is missing in the worktree, copy it from
the main workspace first:

```bash
mkdir -p docs/tmp/papers
cp -a /cpfs/user/zhuzihou/dev/physics-primitive-agent/docs/tmp/papers/arXiv-2602.07369v1 docs/tmp/papers/
```

- [ ] **Step 3: Run smoke check**

Run:

```bash
python - <<'PY'
from primitive_collision_compiler.baselines.cpd_paper.offline import build_cpd_paper_offline_report

report = build_cpd_paper_offline_report()
payload = report["paper_mapped_subset_primitivespec_validation_contract"]
print(report["next_required_gate"])
print(report["failure_labels"])
print(payload["coverage_summary"]["primitive_spec_validation_requirement_row_count"])
print(payload["coverage_summary"]["current_row_primitivespec_validation_row_count"])
print(payload["validated_primitive_spec_candidate_count"])
print(payload["generated_primitive_spec_count"])
print(payload["primitive_spec_generated"], payload["collision_package_generated"], payload["newton_support_claimed"])
PY
```

Expected output:

```text
paper_mapped_subset_primitivespec_generation_preflight_contract
['paper_mapped_subset_primitivespec_generation_preflight_contract_missing']
6
16
0
0
False False False
```

- [ ] **Step 4: Multi-agent review**

Dispatch at least two review agents:

- implementation reviewer: compare tests/code against this plan and the design doc;
- docs/claim reviewer: check reference docs, dated record, registry, and claim boundaries.

Fix Critical and Important findings. Re-run the relevant verification after fixes.

- [ ] **Step 5: Commit, merge, push, and clean**

Commit implementation/docs. Merge the feature branch to `main` after verification and review. Push
`main`. Remove the validation worktree and delete the local feature branch if it has been merged.
