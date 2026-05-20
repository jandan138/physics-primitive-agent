# 2026-05-20 CPD Paper Newton Engine-Builder Configured Runtime Entry-Decision Contract

## Summary

Closed the next DeepDive report-only Newton runtime-lane gate:
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract`.

The slice records the default no-runtime-entry decision for the single synthetic
`paper_single_box` lineage. It consumes the configured-runtime device-resolution row, records
`defer_real_runtime_entry_missing_configured_runtime_source_or_device`, and advances the
report-level next required gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract`.

## Scope

- Adds a bounded entry-decision payload and top-level report key for the configured-runtime
  entry-decision contract.
- Records that real runtime entry remains disallowed because configured runtime source and device
  resolution are still false.
- Keeps runtime entry allowed, attempted, and passed counters at zero.
- Keeps Newton/Warp import, `ModelBuilder` construction, builder shape calls, model finalization,
  collision pipeline calls, Newton execution, runtime compatibility, real-USD evaluation,
  benchmarks, and collision-quality validation at false or zero.
- Updates DeepDive-facing docs, claim-boundary docs, and story/status references so the stage-local
  next runtime-lane gate after entry decision is configured-runtime smoke, not entry decision.

## Not Implemented

- No real runtime entry.
- No config-file or environment-variable reader.
- No runtime source discovery or runtime device selection.
- No filesystem existence check for any Newton source directory.
- No Newton or Warp import.
- No `newton.ModelBuilder` construction or builder shape call.
- No real runtime smoke, real runtime execution, real-USD evaluation, benchmark,
  deployment-readiness, or safety claim.

## Verification

RED evidence before implementation:

```text
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_entry_decision" -q
4 failed, 1901 deselected in 9.68s
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
1 failed in 2.62s
```

Focused GREEN evidence after implementation:

```text
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_entry_decision" -q
4 passed, 1901 deselected in 8.85s
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
1 passed in 2.19s
```

Broader verification before merge:

```text
python scripts/validate_docs.py
docs validation passed
python scripts/validate_site_claims.py
site claim validation passed
git diff --check
passed
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime" -q
55 passed, 1850 deselected in 84.93s
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
1 passed in 2.12s
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_changed_decomposition_output_contract_gate tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_package_adapter_contract_gate -q
2 passed in 3.68s
python -m pytest -q --ignore=tests/test_cpd_paper_offline.py
409 passed, 2 skipped in 47.38s
```

Review fixes before merge:

- Documentation review found stale current-state wording in the prior device-resolution record.
  That record now describes entry decision as the device slice's stage-local next gate, not the
  current report next gate.
- Code/test review found that the entry-decision input validator accepted drift in nested
  `coverage_summary`, `input_contract_summary`, and
  `configured_runtime_device_resolution_contract` values. The validator now rejects those nested
  mismatches, and the entry-decision drift test mutates each nested object.
- Final documentation review found stale current-state wording in `docs/index.md` that still pointed
  the then-current next gate at configured-runtime preflight. The index then distinguished
  historical stage-local design/preflight wording from the report next gate at that time,
  configured-runtime smoke.

Post-review verification:

```text
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_entry_decision" -q
4 passed, 1901 deselected in 9.51s
python scripts/validate_docs.py
docs validation passed
python scripts/validate_site_claims.py
site claim validation passed
git diff --check
passed
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
1 passed in 2.03s
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_changed_decomposition_output_contract_gate tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_package_adapter_contract_gate -q
2 passed in 3.74s
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime" -q
55 passed, 1850 deselected in 90.86s
```

Final index cleanup verification before merge:

```text
python scripts/validate_docs.py
docs validation passed
python scripts/validate_site_claims.py
site claim validation passed
git diff --check
passed
rg -n 'current next gate|next step is a future configured-runtime|configured_runtime_preflight_contract|configured-runtime preflight' docs/index.md docs/records/2026-05-20-cpd-paper-newton-engine-builder-configured-runtime-entry-decision-contract.md docs/records/2026-05-20-cpd-paper-newton-engine-builder-configured-runtime-device-resolution-contract.md
only then-current configured-runtime smoke references and historical stage-local preflight references remain
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_entry_decision" -q
4 passed, 1901 deselected in 7.09s
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
1 passed in 2.05s
```
