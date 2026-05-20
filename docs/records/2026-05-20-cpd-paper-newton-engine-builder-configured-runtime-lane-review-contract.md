# 2026-05-20 CPD Paper Newton Engine-Builder Configured Runtime Lane Review Contract

## Date

2026-05-20

## Status

Complete

## Changes

- Added `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review_contract`
  to `cpd_paper_offline_report`.
- The payload consumes the configured-runtime execution row, records
  `keep_real_runtime_execution_blocked_after_configured_runtime_execution_review`, and advances the
  current report next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_run_contract`.
- The slice keeps real runtime evidence, runtime compatibility, and configured-runtime run
  allowed/attempted/passed false.
- The slice keeps Newton/Warp imports, `newton.ModelBuilder` construction, builder shape calls,
  model finalization, collision pipeline calls, Newton execution, real-USD evaluation, benchmarks,
  and collision-quality validation at false or zero.
- Source-row validators now reject drift in the skipped configured-runtime execution row before the
  lane-review row is built.

## Verification

Focused implementation evidence:

```text
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_lane_review" -q
22 passed, 1949 deselected in 33.67s

python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
1 passed in 2.17s
```

Broader targeted branch evidence:

```text
python -m pytest -q
2380 passed, 2 skipped in 3223.10s (0:53:43)

python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime" -q
121 passed, 1850 deselected in 189.78s (0:03:09)

python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
1 passed in 1.94s

python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_changed_decomposition_output_contract_gate tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_package_adapter_contract_gate -q
2 passed in 5.45s

python scripts/validate_docs.py
docs validation passed

python scripts/validate_site_claims.py
site claim validation passed

git diff --check
exit 0
```

## Claim Boundary

- This record is not Newton runtime support, runtime compatibility evidence, real-USD evidence,
  benchmark evidence, collision-quality validation, deployment readiness, or safety certification.
- The configured-runtime lane-review row is a report-only claim-boundary review for one synthetic
  `paper_single_box` lineage.
- The next gate name is a run contract, but this record does not claim that a real Newton run has
  occurred.
