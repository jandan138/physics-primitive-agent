# 2026-05-20 CPD Paper Newton Engine-Builder Configured Runtime Smoke Contract

## Summary

Closed the next DeepDive report-only Newton runtime-lane gate:
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract`.

The slice records the default skipped configured-runtime smoke decision for the single synthetic
`paper_single_box` lineage. It consumes the configured-runtime entry-decision row, records
`skip_real_runtime_smoke_missing_configured_runtime_entry`, and advances the report-level next
required gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract`.

## Scope

- Adds a bounded smoke payload and top-level report key for the configured-runtime smoke contract.
- Records that real runtime smoke remains disallowed because runtime entry is still false.
- Keeps runtime smoke allowed, attempted, and passed counters at zero.
- Keeps Newton/Warp import, `ModelBuilder` construction, builder shape calls, model finalization,
  collision pipeline calls, Newton execution, runtime compatibility, real-USD evaluation,
  benchmarks, and collision-quality validation at false or zero.
- Updates DeepDive-facing docs, claim-boundary docs, and story/status references so the current
  next runtime-lane gate is configured-runtime execution, not configured-runtime smoke.

## Not Implemented

- No real runtime smoke.
- No config-file or environment-variable reader.
- No runtime source discovery or runtime device selection.
- No filesystem existence check for any Newton source directory.
- No Newton or Warp import.
- No `newton.ModelBuilder` construction or builder shape call.
- No real runtime execution, real-USD evaluation, benchmark, deployment-readiness, or safety claim.

## Verification

RED evidence before implementation:

```text
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_smoke" -q
4 failed, 1905 deselected in 10.19s
```

Focused GREEN evidence after implementation:

```text
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_smoke" -q
4 passed, 1905 deselected in 7.12s
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
1 passed in 2.54s
```

Review follow-up:

- Code and docs review found no claim-boundary issue.
- Test review found the initial drift tests covered required-key/schema changes but not enough direct
  payload values, row counts, or source-row value drift.
- The follow-up adds parameterized drift tests for direct smoke input values, boolean guard flags,
  row counts, source-row values, and source lineage identity.
- The smoke source-row validator now rejects source identity drift before building the skipped smoke
  row.

Focused GREEN evidence after review follow-up:

```text
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_smoke" -q
19 passed, 1905 deselected in 30.25s
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime" -q
74 passed, 1850 deselected in 113.84s (0:01:53)
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
1 passed in 1.89s
python scripts/validate_docs.py
docs validation passed
python scripts/validate_site_claims.py
site claim validation passed
git diff --check
no output
python -m pytest -q
2333 passed, 2 skipped in 3101.70s (0:51:41)
```
