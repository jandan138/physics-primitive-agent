# CPD Paper Package Adapter Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an offline/report-only package-adapter contract and move the current CPD paper
offline gate to `paper_package_adapter_unsupported_primitive_policy`.

**Architecture:** Keep the implementation in
`primitive_collision_compiler.baselines.cpd_paper.offline`. Consume the existing
`paper_offline_changed_decomposition_output_contract` payload and emit adapter decision rows
without generating packages, importing package runtime types, mapping Newton shapes, loading real
USD, or running benchmarks.

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
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/records/README.md`
- Modify: `experiments/registry.yaml`
- Create: `docs/records/2026-05-17-cpd-paper-package-adapter-contract.md`

## Task 1: RED Tests For Adapter Contract

- [ ] Add constants in `tests/test_cpd_paper_offline.py`:

```python
EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY = (
    "paper_package_adapter_unsupported_primitive_policy"
)
EXPECTED_POST_PACKAGE_ADAPTER_FAILURE_LABELS = [
    "paper_package_adapter_unsupported_primitive_policy_missing",
]
```

- [ ] Add `test_cpd_paper_offline_report_records_package_adapter_contract_gate`.
It must assert:

```python
report = build_cpd_paper_offline_report()
payload = report["paper_package_adapter_contract"]
assert report["next_required_gate"] == EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY
assert report["failure_labels"] == EXPECTED_POST_PACKAGE_ADAPTER_FAILURE_LABELS
assert report["paper_faithful_offline_supported"] is False
assert payload["gate_id"] == EXPECTED_PACKAGE_ADAPTER_CONTRACT
assert payload["gate_status"] == "implemented_offline_adapter_contract_only_partial"
assert payload["closed_gate"] == EXPECTED_PACKAGE_ADAPTER_CONTRACT
assert payload["input_gate_id"] == EXPECTED_CLOSED_CHANGED_DECOMPOSITION_CONTRACT
assert payload["next_required_gate"] == EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY
assert payload["package_generation_allowed"] is False
assert payload["artifact_kind"] == "offline_package_adapter_contract_not_collision_package"
```

- [ ] Add `test_cpd_paper_package_adapter_contract_summarizes_changed_decomposition_contract`.
It must assert:

```python
changed = report["paper_offline_changed_decomposition_output_contract"]
adapter = report["paper_package_adapter_contract"]
assert adapter["input_contract_summary"]["input_gate_id"] == changed["gate_id"]
assert adapter["input_contract_summary"]["decomposition_output_row_count"] == 9
assert adapter["input_contract_summary"]["primitive_record_count"] == 16
assert adapter["coverage_summary"]["primitive_decision_row_count"] == 16
```

- [ ] Add `test_cpd_paper_package_adapter_decision_counts_partition_current_records`.
It must assert:

```python
summary = adapter["coverage_summary"]
assert summary["adapter_eligible_record_count"] == 0
assert summary["blocked_record_count"] == 0
assert summary["later_policy_required_record_count"] == 16
assert summary["offline_only_unmapped_record_count"] == 16
assert (
    summary["adapter_eligible_record_count"]
    + summary["blocked_record_count"]
    + summary["later_policy_required_record_count"]
    == summary["primitive_decision_row_count"]
)
for row in adapter["primitive_adapter_decision_rows"]:
    assert row["paper_primitive"] == "trapezoidal_prism"
    assert row["offline_runtime_kind_label"] == "offline_only_unmapped"
    assert row["adapter_decision"] == "later_policy_required"
    assert row["required_later_gate"] == EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY
```

- [ ] Add `test_cpd_paper_package_adapter_contract_stays_report_only`.
It must assert every adapter row has all four false triggers and the payload lacks
`CollisionPackage`, `PrimitiveSpec`, `runtime_result`, `usd_asset_path`, `benchmark_metric`,
`timing`, `surface_distance`, and `collision_quality` keys.

- [ ] Update `tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json` to assert the
new top-level gate, failure label, implemented output-contract scope, and adapter coverage
summary.

- [ ] Run RED commands:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_package_adapter_contract_gate -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Expected: both fail because `paper_package_adapter_contract` does not exist yet and the report
still points to `paper_package_adapter_contract`.

## Task 2: Implement Adapter Decision Payload

- [ ] Add `_PAPER_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY` in `offline.py`:

```python
_PAPER_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY = (
    "paper_package_adapter_unsupported_primitive_policy"
)
```

- [ ] Add:

```python
def _paper_remaining_gaps_after_package_adapter_contract() -> list[str]:
    return [_PAPER_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY]
```

- [ ] Add `_paper_adapter_required_fields_present(primitive_record)` returning `True` only when
`offline_primitive_id`, `paper_primitive`, `center`, `axes`, `dimensions`, `volume`,
`paper_weight`, `weighted_volume`, `contains_assigned_points`, `newton_runtime_kind`,
`source_face_ids`, and `generated_triangle_face_ids` are present.

- [ ] Add `_paper_adapter_primitive_decision_row(output_row, primitive_record)` that returns
`adapter_eligible`, `blocked`, or `later_policy_required` according to the design spec.

- [ ] Add `_paper_package_adapter_contract_payload(changed_payload)` returning the schema in the
design spec.

- [ ] Update `build_cpd_paper_offline_report()` to build the changed-decomposition payload once,
pass it into `_paper_package_adapter_contract_payload(changed_payload)`, and set:

```python
missing_before_paper_faithful = _paper_remaining_gaps_after_package_adapter_contract()
next_required_gate = _PAPER_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY
"implemented_output_contract_scope": [
    _PAPER_CHANGED_DECOMPOSITION_OUTPUT_CONTRACT,
    _PAPER_PACKAGE_ADAPTER_CONTRACT,
]
"paper_package_adapter_contract": _paper_package_adapter_contract_payload(changed_payload)
```

Keep `implemented_generalization_scope` as the Batch A-E list.

## Task 3: GREEN Tests And CLI Smoke

- [ ] Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_package_adapter_contract_gate -q
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_package_adapter_contract_summarizes_changed_decomposition_contract -q
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_package_adapter_decision_counts_partition_current_records -q
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_package_adapter_contract_stays_report_only -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Expected: all pass.

- [ ] Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
```

Expected: all pass.

## Task 4: Documentation And Record Updates

- [ ] Update current status docs so the adapter contract is implemented and the next gate is
`paper_package_adapter_unsupported_primitive_policy`.
- [ ] Add `docs/records/2026-05-17-cpd-paper-package-adapter-contract.md`.
- [ ] Update `docs/records/README.md`.
- [ ] Add a registry entry in `experiments/registry.yaml`.

Documentation wording must say:

```text
command-only offline package-adapter contract, not a CollisionPackage
```

and must not claim:

```text
package ready
Newton-ready
runtime-ready
runtime admissible
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
assert report["next_required_gate"] == "paper_package_adapter_unsupported_primitive_policy"
assert report["failure_labels"] == [
    "paper_package_adapter_unsupported_primitive_policy_missing"
]
payload = report["paper_package_adapter_contract"]
assert payload["artifact_kind"] == "offline_package_adapter_contract_not_collision_package"
assert payload["package_generation_allowed"] is False
assert payload["coverage_summary"]["primitive_decision_row_count"] == 16
assert payload["coverage_summary"]["later_policy_required_record_count"] == 16
assert report["paper_faithful_offline_supported"] is False
print("package adapter contract smoke passed")
PY
```

Expected: all pass.
