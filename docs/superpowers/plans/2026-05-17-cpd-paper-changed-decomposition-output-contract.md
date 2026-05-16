# CPD Paper Changed Decomposition Output Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an offline/report-only changed-decomposition output contract and move the current
CPD paper offline gate to `paper_package_adapter_contract`.

**Architecture:** Keep the implementation in
`primitive_collision_compiler.baselines.cpd_paper.offline`. Summarize existing `cases[*]`,
Batch A-E payloads, and postprocess audits into a stable contract payload without importing or
using `CollisionPackage` or Newton runtime types.

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
- Create: `docs/records/2026-05-17-cpd-paper-changed-decomposition-output-contract.md`

## Task 1: RED Tests For Changed-Decomposition Contract

- [ ] Add constants in `tests/test_cpd_paper_offline.py`:

```python
EXPECTED_CLOSED_CHANGED_DECOMPOSITION_CONTRACT = (
    "paper_offline_changed_decomposition_output_contract"
)
EXPECTED_NEXT_AFTER_CHANGED_DECOMPOSITION_CONTRACT = "paper_package_adapter_contract"
EXPECTED_POST_CHANGED_DECOMPOSITION_FAILURE_LABELS = [
    "paper_package_adapter_contract_missing",
]
```

- [ ] Add `test_cpd_paper_offline_report_records_changed_decomposition_output_contract_gate`.
It must assert:

```python
report = build_cpd_paper_offline_report()
payload = report["paper_offline_changed_decomposition_output_contract"]
assert report["next_required_gate"] == EXPECTED_NEXT_AFTER_CHANGED_DECOMPOSITION_CONTRACT
assert report["failure_labels"] == EXPECTED_POST_CHANGED_DECOMPOSITION_FAILURE_LABELS
assert report["paper_faithful_offline_supported"] is False
assert payload["gate_status"] == "implemented_offline_contract_only_partial"
assert payload["closed_gate"] == EXPECTED_CLOSED_CHANGED_DECOMPOSITION_CONTRACT
assert payload["next_required_gate"] == EXPECTED_NEXT_AFTER_CHANGED_DECOMPOSITION_CONTRACT
assert payload["package_generation_allowed"] is False
```

- [ ] Add matrix shape assertions:

```python
assert payload["artifact_kind"] == "offline_changed_decomposition_output_not_collision_package"
assert payload["schema_version"] == 1
assert payload["coverage_summary"]["decomposition_output_row_count"] == 9
assert payload["coverage_summary"]["primitive_record_count"] == 16
assert payload["coverage_summary"]["postprocess_state_row_count"] == 3
assert len(payload["decomposition_output_rows"]) == 9
assert len(payload["postprocess_state_rows"]) == 3
```

- [ ] Add `test_cpd_paper_changed_decomposition_output_rows_match_search_case_payloads` to compare
each output row against the referenced case's `source_mesh`, `collapse_trace.final_active_groups`,
and `primitive_fit_audit.selected`.

- [ ] Add
`test_cpd_paper_changed_decomposition_contract_records_postprocess_state_without_applying_to_search_output`
to assert each postprocess state row uses
`state_scope: explicit_postprocess_audit_fixture_not_search_output`.

- [ ] Update `tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json`.

- [ ] Run RED commands:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_changed_decomposition_output_contract_gate -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Expected: both fail because the new payload does not exist and the report still points to
`paper_offline_changed_decomposition_output_contract`.

## Task 2: Implement Contract Payload

- [ ] Add `_PAPER_PACKAGE_ADAPTER_CONTRACT = "paper_package_adapter_contract"` in `offline.py`.

- [ ] Add:

```python
def _paper_remaining_gaps_after_changed_decomposition_contract() -> list[str]:
    return [_PAPER_PACKAGE_ADAPTER_CONTRACT]
```

- [ ] Add `_paper_changed_decomposition_output_contract_payload(cases)` returning the schema in the
design spec.

- [ ] Add `_offline_changed_decomposition_output_rows(cases)` that filters cases with
`collapse_trace.final_active_groups`.

- [ ] Add `_offline_decomposition_primitive_records(case_payload)` that emits one primitive record
per final active group using `offline_primitive_id`, face ids, source face ids, generated triangle
face ids, and bounded fields from `primitive_fit_audit.selected`.

- [ ] Add `_paper_postprocess_state_contract_rows(cases)` over the three explicit postprocess
audit fixtures.

- [ ] Update `build_cpd_paper_offline_report()` to:

```python
missing_before_paper_faithful = _paper_remaining_gaps_after_changed_decomposition_contract()
next_required_gate = _PAPER_PACKAGE_ADAPTER_CONTRACT
```

and add:

```python
"implemented_output_contract_scope": [
    _PAPER_CHANGED_DECOMPOSITION_OUTPUT_CONTRACT,
],
"paper_offline_changed_decomposition_output_contract": (
    _paper_changed_decomposition_output_contract_payload(cases)
),
```

Keep `implemented_generalization_scope` as the Batch A-E list.

## Task 3: GREEN Tests And CLI Smoke

- [ ] Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_changed_decomposition_output_contract_gate -q
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_changed_decomposition_output_rows_match_search_case_payloads -q
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_changed_decomposition_contract_records_postprocess_state_without_applying_to_search_output -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Expected: all pass.

- [ ] Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
```

Expected: all pass.

## Task 4: Documentation And Record Updates

- [ ] Update current status docs so the changed-decomposition output contract is implemented and
the next gate is `paper_package_adapter_contract`.
- [ ] Add `docs/records/2026-05-17-cpd-paper-changed-decomposition-output-contract.md`.
- [ ] Update `docs/records/README.md`.
- [ ] Add a registry entry in `experiments/registry.yaml`.

Documentation wording must say:

```text
offline changed-decomposition output contract, not a CollisionPackage
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
assert report["next_required_gate"] == "paper_package_adapter_contract"
assert report["failure_labels"] == ["paper_package_adapter_contract_missing"]
payload = report["paper_offline_changed_decomposition_output_contract"]
assert payload["artifact_kind"] == "offline_changed_decomposition_output_not_collision_package"
assert payload["package_generation_allowed"] is False
assert payload["coverage_summary"]["decomposition_output_row_count"] == 9
assert payload["coverage_summary"]["postprocess_state_row_count"] == 3
assert report["paper_faithful_offline_supported"] is False
print("changed decomposition output contract smoke passed")
PY
```

Expected: all pass.
