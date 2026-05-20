# 2026-05-20 CPD Paper Newton Engine-Builder Configured Runtime Source-Resolution Contract

## Summary

Closed the next DeepDive report-only Newton runtime-lane gate:
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract`.

The slice records the default missing-source decision for the single synthetic `paper_single_box`
lineage. It consumes the configured-runtime validation row, records that `newton.source_dir` is not
configured, and advances the report-level next required gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract`.

## Scope

- Adds a bounded source-resolution payload and top-level report key for the configured-runtime
  source-resolution contract.
- Records the missing `newton.source_dir` result without reading a config file or environment.
- Records that no filesystem probe was attempted.
- Keeps runtime source resolution, runtime device resolution, Newton/Warp import, `ModelBuilder`
  construction, builder shape calls, model finalization, collision pipeline calls, Newton execution,
  runtime compatibility, real-USD evaluation, benchmarks, and collision-quality validation at false
  or zero.
- Updates DeepDive-facing docs, claim-boundary docs, and story/status references so the current
  next runtime-lane gate is device resolution, not source resolution.

## Not Implemented

- No real runtime source discovery.
- No filesystem existence check for any Newton source directory.
- No config-file or environment-variable reader.
- No runtime device selection.
- No Newton or Warp import.
- No `newton.ModelBuilder` construction or builder shape call.
- No real runtime execution, real-USD evaluation, benchmark, deployment-readiness, or safety claim.

## Verification

RED evidence before implementation:

```text
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_source_resolution" -q
4 failed, 1893 deselected in 9.86s
```

GREEN evidence after implementation:

```text
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_source_resolution" -q
4 passed, 1893 deselected in 6.85s
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
1 passed in 2.62s
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
47 passed, 1850 deselected in 78.11s
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
1 passed in 1.95s
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_changed_decomposition_output_contract_gate tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_package_adapter_contract_gate -q
2 passed in 5.35s
python -m pytest tests/test_cpd_paper_offline.py -k "newton_shape_runtime_engine_builder" -q
640 passed, 1257 deselected in 1023.17s
python -m pytest -q --ignore=tests/test_cpd_paper_offline.py
409 passed, 2 skipped in 50.69s
```

Review before merge:

- Documentation review found no stale current-gate wording or overclaims. It flagged this record's
  previous placeholder sentence as unsupported evidence; this section replaces that placeholder
  with concrete verification and review notes.
- Code/test review found no runtime-broadening issue in the source-resolution payload. It found two
  stale exact `implemented_output_contract_scope` expectations that still stopped at the
  configured-runtime validation contract; those expectations now include the configured-runtime
  source-resolution contract and passed the targeted two-test rerun listed above.
