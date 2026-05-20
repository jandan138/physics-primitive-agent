# 2026-05-20 CPD Paper Newton Engine-Builder Configured Runtime Device-Resolution Contract

## Summary

Closed the next DeepDive report-only Newton runtime-lane gate:
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract`.

The slice records the default missing-device decision for the single synthetic `paper_single_box`
lineage. It consumes the configured-runtime source-resolution row, records that
`newton_diagnostic.device` is not configured, and at that stage advanced the report-level next
required gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract`.

## Scope

- Adds a bounded device-resolution payload and top-level report key for the configured-runtime
  device-resolution contract.
- Records the missing `newton_diagnostic.device` result without reading a config file or
  environment.
- Records that no runtime device object was created.
- Keeps runtime source resolution, runtime device resolution, Newton/Warp import, `ModelBuilder`
  construction, builder shape calls, model finalization, collision pipeline calls, Newton execution,
  runtime compatibility, real-USD evaluation, benchmarks, and collision-quality validation at false
  or zero.
- Updates DeepDive-facing docs, claim-boundary docs, and story/status references so the
  stage-local next runtime-lane gate is entry decision, not device resolution.

## Not Implemented

- No runtime device selection.
- No runtime device object creation.
- No config-file or environment-variable reader.
- No real runtime source discovery.
- No filesystem existence check for any Newton source directory.
- No Newton or Warp import.
- No `newton.ModelBuilder` construction or builder shape call.
- No real runtime execution, real-USD evaluation, benchmark, deployment-readiness, or safety claim.

## Verification

RED evidence before implementation:

```text
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_device_resolution" -q
4 failed, 1897 deselected in 10.06s
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
1 failed in 2.97s
```

GREEN evidence after implementation:

```text
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_device_resolution" -q
4 passed, 1897 deselected in 8.47s
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
1 passed in 2.15s
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
51 passed, 1850 deselected in 81.70s
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
1 passed in 2.01s
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_changed_decomposition_output_contract_gate tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_package_adapter_contract_gate -q
2 passed in 3.56s
python -m pytest -q --ignore=tests/test_cpd_paper_offline.py
409 passed, 2 skipped in 50.41s
```

Review before merge:

- Documentation review found no stale current-gate wording or overclaims at the time of the slice.
  It confirmed the stage-local next runtime-lane gate was the configured-runtime entry-decision
  contract, while device resolution was documented only as a closed report-only missing-device
  slice.
- Code/test review found no high-severity issues in the narrowed slice. It confirmed the
  device-resolution gate consumes source resolution, advances to entry decision, keeps config/env,
  filesystem, import, and runtime work disallowed, and updates exact implemented-output scope
  expectations to include the device-resolution contract.
