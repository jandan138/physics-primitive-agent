# 2026-05-18 CPD Paper Mapped-Subset Newton Shape Runtime Builder-Preflight Contract

## Summary

Closed `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract` as a
single-fixture offline/static report contract inside `cpd_paper_offline_report`.

The new contract consumes the existing synthetic `paper_single_box`
`NewtonShapeMapping.to_dict()` report record and records exactly one JSON-safe future box builder
call plan. The plan names the future builder method and signature fields (`body`, `xform`, `hx`,
`hy`, `hz`) plus body-binding and deferred transform policy text.

## Evidence Added

- Top-level `next_required_gate` now advances to
  `paper_mapped_subset_newton_shape_runtime_builder_construction_contract`.
- `implemented_output_contract_scope` now includes
  `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`.
- The builder-preflight payload records:
  - `newton_shape_runtime_builder_preflight_row_count: 1`
  - `runtime_builder_preflight_passed_count: 1`
  - `builder_call_plan_count: 1`
  - `builder_call_allowed_count: 0`
  - `newton_engine_shape_object_count: 0`
  - `newton_builder_shape_call_count: 0`
  - `newton_runtime_execution_count: 0`
- Tests cover exact payload schema, row schema, lineage, mapping drift, input drift, false/true
  flags, source-package-copy rejection, JSON serializability, and static no-Newton/no-builder-call
  source boundaries.

## Claim Boundary

This is not a Newton builder call, not Newton engine shape object construction, not Newton
execution, not Newton support, not real-USD evidence, not benchmark evidence, not
collision-quality evidence, not `paper_faithful_offline`, not deployment readiness, and not safety
certification.

The contract is a report-only preflight that makes the future Newton builder-construction gate
reviewable before any actual builder invocation is introduced.

The builder-preflight helper block adds no Newton/Warp import and invokes no Newton/Warp API.
The broader `cpd_paper.offline` module import path still preloads existing repo-local Newton
diagnostic modules through the older CPD-like package import chain, so this record does not claim
module-level no-Newton import.

## Verification

Focused TDD verification:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_builder_preflight or cpd_paper_offline_report_next_gate' -q
```

Result:

```text
116 passed, 1010 deselected
```

Stale report-scope and CLI expectation regression verification:

```bash
PYTHONPATH=src python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_changed_decomposition_output_contract_gate tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_package_adapter_contract_gate -q
```

Result:

```text
3 passed
```

Full branch verification:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -q
PYTHONPATH=src python -m pytest -q
```

Results:

```text
1126 passed
1535 passed, 2 skipped
```

## Next Gate

`paper_mapped_subset_newton_shape_runtime_builder_construction_contract`
