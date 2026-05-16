# 2026-05-17 CPD Paper Package-Adapter Contract

## Date

2026-05-17

## Status

Complete

## Summary

- Added `paper_package_adapter_contract` to the command-only partial
  `cpd_paper_offline_report`.
- Closed only the offline adapter-contract gate and advanced the current next gate to
  `paper_package_adapter_unsupported_primitive_policy`.
- Kept the new artifact explicitly offline: it is a command-only package-adapter contract, not a
  `CollisionPackage`.
- Kept package generation, Newton runtime execution, real USD, benchmark, collision-quality,
  deployment, and safety-certification claims blocked.

## What Changed

The new report payload consumes the existing
`paper_offline_changed_decomposition_output_contract` payload and records adapter-decision
metadata over deterministic synthetic toy fixture evidence:

- input-contract summary for the changed-decomposition output payload;
- adapter-decision contract with the allowed decision labels;
- 16 primitive adapter decision rows, one per offline primitive record;
- current decision partition: 0 `adapter_eligible`, 0 `blocked`, and 16
  `later_policy_required`;
- 16 `offline_only_unmapped` records, all currently `trapezoidal_prism`;
- malformed-record and duplicate-id guardrails that block missing required fields, missing
  source-face mappings, non-finite numeric fields, containment failures, forbidden trigger flags,
  and duplicate `offline_primitive_id` values;
- package/Newton/real-USD/benchmark false triggers at payload and row level.

The top-level report now emits:

```text
next_required_gate: paper_package_adapter_unsupported_primitive_policy
failure_labels: ["paper_package_adapter_unsupported_primitive_policy_missing"]
paper_faithful_offline_supported: false
```

## Verification So Far

- RED checks were added before implementation for the new adapter-contract gate and CLI JSON
  surface.
- Targeted RED checks failed first because the report still pointed to
  `paper_package_adapter_contract_missing`.
- Targeted GREEN checks passed:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_package_adapter_contract_gate tests/test_cpd_paper_offline.py::test_cpd_paper_package_adapter_contract_summarizes_changed_decomposition_contract tests/test_cpd_paper_offline.py::test_cpd_paper_package_adapter_decision_counts_partition_current_records tests/test_cpd_paper_offline.py::test_cpd_paper_package_adapter_contract_stays_report_only tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Result: all selected tests passed.

- Review follow-up guardrail check passed:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_package_adapter_contract_blocks_malformed_or_duplicate_records -q
```

Result: `1 passed`.

- Focused suite passed:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
```

Result: `141 passed`.

## Claim Boundary

This record supports only this narrow statement:

```text
The partial CPD paper offline report now contains a command-only offline package-adapter contract
over deterministic synthetic fixture records.
```

It does not support:

- `paper_faithful_offline`;
- full CPD paper reproduction;
- `CollisionPackage` generation;
- package readiness;
- Newton readiness;
- runtime readiness;
- runtime admissibility;
- Newton runtime execution;
- real USD evidence;
- benchmark evidence;
- collision-quality validation;
- deployment readiness;
- safety certification.

## Next Step

Proceed to `paper_package_adapter_unsupported_primitive_policy`. That next slice should define how
paper-only or unmapped primitive records are handled before any future package-conversion slice,
while still avoiding package generation and Newton runtime execution until a separate dated record
justifies those gates.
