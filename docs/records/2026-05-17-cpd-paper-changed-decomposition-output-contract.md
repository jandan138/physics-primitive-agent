# 2026-05-17 CPD Paper Changed-Decomposition Output Contract

## Date

2026-05-17

## Status

Complete

## Summary

- Added `paper_offline_changed_decomposition_output_contract` to the command-only partial
  `cpd_paper_offline_report`.
- Closed only the offline output-contract gate and advanced the current next gate to
  `paper_package_adapter_contract`.
- Kept the new artifact explicitly offline: it is an offline changed-decomposition output contract,
  not a `CollisionPackage`.
- Kept package generation, Newton runtime execution, real USD, benchmark, collision-quality,
  deployment, and safety-certification claims blocked.

## What Changed

The new report payload records a stable review contract over existing synthetic toy fixture
evidence:

- decomposition output rows for the nine cases with `collapse_trace.final_active_groups`;
- 16 offline primitive records with stable `offline_primitive_id` values;
- source-face ids, generated triangle face ids, and final active group ids;
- selected paper primitive audit fields reused for contract accounting;
- explicit postprocess state rows for the three postprocess audit fixtures;
- unsupported runtime/package boundaries and false package/Newton/real-USD/benchmark triggers.

The top-level report now emits:

```text
next_required_gate: paper_package_adapter_contract
failure_labels: ["paper_package_adapter_contract_missing"]
paper_faithful_offline_supported: false
```

## Verification So Far

- RED checks were added before implementation for the new output contract gate and CLI JSON
  surface.
- Targeted GREEN checks passed:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_changed_decomposition_output_contract_gate tests/test_cpd_paper_offline.py::test_cpd_paper_changed_decomposition_output_rows_match_search_case_payloads tests/test_cpd_paper_offline.py::test_cpd_paper_changed_decomposition_contract_records_postprocess_state_without_applying_to_search_output tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Result: `4 passed`.

- Focused suite passed:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
```

Result: `137 passed`.

## Claim Boundary

This record supports only this narrow statement:

```text
The partial CPD paper offline report now contains an offline changed-decomposition output contract
for deterministic synthetic fixture evidence.
```

It does not support:

- `paper_faithful_offline`;
- full CPD paper reproduction;
- `CollisionPackage` generation;
- package readiness;
- Newton readiness;
- Newton runtime execution;
- real USD evidence;
- benchmark evidence;
- collision-quality validation;
- deployment readiness;
- safety certification.

## Next Step

Proceed to `paper_package_adapter_contract`. That next slice should define how a future package
adapter may consume the offline output contract, while still avoiding package generation and
Newton runtime execution until a separate dated record justifies those gates.
