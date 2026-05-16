# CPD Paper Package Boundary Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the offline report-only Batch E package-boundary readiness matrix and move the
current CPD paper offline gate to the next changed-decomposition output contract.

**Architecture:** Keep the implementation inside
`primitive_collision_compiler.baselines.cpd_paper.offline`. Add a small constant and payload
builder for Batch E, then update tests and docs so the current status remains partial and
package/Newton/runtime work remains blocked.

**Tech Stack:** Python, pytest, Markdown records, YAML experiment registry, existing
`cpd_paper_offline_report` CLI surface.

---

## Files

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`
- Modify: `README.md`
- Modify: `docs/index.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/records/README.md`
- Modify: `experiments/registry.yaml`
- Create: `docs/records/2026-05-17-cpd-paper-generalization-batch-e-package-boundary-readiness.md`

## Task 1: RED Tests For Batch E Gate Closure

- [ ] Update `tests/test_cpd_paper_offline.py` constants so the current gate is:

```python
EXPECTED_NEXT_AFTER_PACKAGE_BOUNDARY = "paper_offline_changed_decomposition_output_contract"
EXPECTED_POST_PACKAGE_BOUNDARY_FAILURE_LABELS = [
    "paper_offline_changed_decomposition_output_contract_missing",
    "paper_package_generation_contract_missing",
]
EXPECTED_CLOSED_PACKAGE_BOUNDARY_GATE = (
    "paper_generalization_batch_e_package_boundary_readiness"
)
```

- [ ] Add `test_cpd_paper_offline_report_records_package_boundary_readiness_gate`.
It must assert:

```python
report = build_cpd_paper_offline_report()
payload = report["paper_generalization_batch_e_package_boundary_readiness"]
assert report["next_required_gate"] == EXPECTED_NEXT_AFTER_PACKAGE_BOUNDARY
assert report["failure_labels"] == EXPECTED_POST_PACKAGE_BOUNDARY_FAILURE_LABELS
assert report["paper_faithful_offline_supported"] is False
assert payload["gate_status"] == "implemented_planning_only_partial"
assert payload["closed_gate"] == EXPECTED_CLOSED_PACKAGE_BOUNDARY_GATE
assert payload["next_required_gate"] == EXPECTED_NEXT_AFTER_PACKAGE_BOUNDARY
assert payload["paper_faithful_offline_allowed"] is False
assert payload["package_generation_allowed"] is False
```

- [ ] Add matrix assertions:

```python
assert [row["row_id"] for row in payload["boundary_review_matrix"]] == [
    "changed_decomposition_output_contract",
    "package_generation_boundary",
    "newton_runtime_boundary",
    "real_usd_boundary",
    "benchmark_evaluation_boundary",
]
for row in payload["boundary_review_matrix"]:
    assert row["package_generation_triggered"] is False
    assert row["newton_runtime_triggered"] is False
    assert row["real_usd_triggered"] is False
    assert row["benchmark_triggered"] is False
```

- [ ] Add `test_cpd_paper_package_boundary_readiness_keeps_runtime_work_blocked` to assert the
coverage summary counts and that no row status is package-ready or runtime-ready.

- [ ] Update `tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json` to assert
Batch E exists, Batch E missing label is absent, and the next gate is the changed-decomposition
contract.

- [ ] Run RED commands:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_package_boundary_readiness_gate -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Expected: both fail because Batch E payload does not exist and the report still points to Batch E.

## Task 2: Implement Batch E Payload

- [ ] Add constants in `offline.py`:

```python
_PAPER_CHANGED_DECOMPOSITION_OUTPUT_CONTRACT = (
    "paper_offline_changed_decomposition_output_contract"
)
_PAPER_PACKAGE_GENERATION_CONTRACT = "paper_package_generation_contract"
```

- [ ] Add:

```python
def _paper_remaining_generalization_gates_after_package_boundary() -> list[str]:
    return _paper_remaining_generalization_gates_after(
        {
            _PAPER_GENERALIZATION_BATCH_A_SOURCE_POLICY,
            _PAPER_GENERALIZATION_BATCH_B_PRIMITIVE_FIT,
            _PAPER_GENERALIZATION_BATCH_C_SEARCH,
            _PAPER_GENERALIZATION_BATCH_D_POSTPROCESS,
            _PAPER_GENERALIZATION_BATCH_E_PACKAGE_BOUNDARY,
        }
    )
```

- [ ] Add `_paper_package_boundary_readiness_rows()` returning five static rows with explicit
blocked reasons and false trigger fields for package, Newton, real USD, and benchmark execution.

- [ ] Add `_paper_package_boundary_readiness_payload()` that returns the Batch E payload with:

```python
"gate_status": "implemented_planning_only_partial"
"closed_gate": _PAPER_GENERALIZATION_BATCH_E_PACKAGE_BOUNDARY
"next_required_gate": _PAPER_CHANGED_DECOMPOSITION_OUTPUT_CONTRACT
"decision_reason": "package_boundary_readiness_review_complete_changed_decomposition_output_contract_missing"
"paper_faithful_offline_allowed": False
"package_generation_allowed": False
"implementation_boundary": "planning_only_no_package_or_newton"
```

- [ ] Update `build_cpd_paper_offline_report()` to:

```python
missing_before_paper_faithful = [
    _PAPER_CHANGED_DECOMPOSITION_OUTPUT_CONTRACT,
    _PAPER_PACKAGE_GENERATION_CONTRACT,
]
```

and to add Batch E to `implemented_generalization_scope` plus a top-level
`paper_generalization_batch_e_package_boundary_readiness` payload.

- [ ] Keep historical Batch A-D nested payloads unchanged unless their current-gate summaries
must reflect that Batch E is now closed.

## Task 3: GREEN Tests And CLI Smoke

- [ ] Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_package_boundary_readiness_gate -q
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_package_boundary_readiness_keeps_runtime_work_blocked -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Expected: all pass.

- [ ] Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
```

Expected: all pass.

## Task 4: Documentation And Record Updates

- [ ] Update status docs so Batch E is implemented as an offline package-boundary readiness
matrix and the next gate is `paper_offline_changed_decomposition_output_contract`.
- [ ] Add
`docs/records/2026-05-17-cpd-paper-generalization-batch-e-package-boundary-readiness.md`.
- [ ] Update `docs/records/README.md`.
- [ ] Add a registry entry in `experiments/registry.yaml`.
- [ ] Correct README Franka native-lane wording so it matches the current claim boundary.

Documentation wording must say:

```text
offline package-boundary readiness matrix before package conversion
```

and must not claim:

```text
package ready
Newton-ready
runtime-ready
paper_faithful_offline
CollisionPackage generation
Newton runtime execution
real USD evidence
benchmark or collision-quality improvement
```

## Task 5: Review And Verification

- [ ] Request implementation/schema review from a fresh agent.
- [ ] Request documentation/claim-boundary review from a fresh agent.
- [ ] Address all critical or important findings.
- [ ] Run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
python -m pytest -q
PYTHONPATH=src python - <<'PY'
from primitive_collision_compiler.baselines.cpd_paper.offline import build_cpd_paper_offline_report

report = build_cpd_paper_offline_report()
assert report["next_required_gate"] == "paper_offline_changed_decomposition_output_contract"
assert report["failure_labels"] == [
    "paper_offline_changed_decomposition_output_contract_missing",
    "paper_package_generation_contract_missing",
]
payload = report["paper_generalization_batch_e_package_boundary_readiness"]
assert payload["package_generation_allowed"] is False
assert payload["coverage_summary"]["boundary_review_row_count"] == 5
assert report["paper_faithful_offline_supported"] is False
print("package boundary readiness smoke passed")
PY
```

Expected: all pass.

## Execution Status

- [x] RED tests failed first on the old
  `paper_generalization_batch_e_package_boundary_readiness_missing` label.
- [x] Batch E implementation added an offline package-boundary readiness matrix and moved the next
  gate to `paper_offline_changed_decomposition_output_contract`.
- [x] Focused CPD paper/CLI tests passed.
- [x] Docs, claim-boundary, registry, README, and dated record updates landed.
- [x] Implementation/schema and documentation/claim-boundary review agents reported no blocking
  issues.
- [x] Full validation passed before merge.
