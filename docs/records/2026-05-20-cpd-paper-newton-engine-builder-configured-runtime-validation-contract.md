# 2026-05-20 CPD Paper Newton Engine-Builder Configured-Runtime Validation Contract

## Date

2026-05-20

## Status

Implementation, focused RED/GREEN verification, split regression verification, docs/claim
validation, and multi-agent review are complete. Merge, push, and worktree cleanup remain pending.

## Summary

This record documents the
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_validation_contract`
slice inside `cpd_paper_offline_report`.

The slice consumes the report-only configured-runtime preflight row for the synthetic
`paper_single_box` OBB/box lineage and records a report-only configured-runtime validation result:
`configured_runtime_validation_status:
runtime_config_validation_failed_missing_required_config`. It advances the current next gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract`.

This is not runtime source resolution, runtime device resolution, runtime compatibility, or Newton
runtime execution. It records that the default report has no configured runtime source or
diagnostic device while keeping config-file reads, environment reads, source/device resolution,
real Newton/Warp imports, `newton.ModelBuilder`, real builder calls, model finalization, collision
pipeline calls, Newton runtime execution, real USD, benchmarks, and collision-quality evidence at
zero or false.

## Scope

Implemented:

- one synthetic fixture: `paper_single_box`;
- one mapped Newton-native shape kind: `box`;
- one configured-runtime validation row linked to the configured-runtime preflight row;
- required runtime config-key and runtime-input lists carried forward from the preflight row;
- explicit default missing-config statuses for `newton.source_dir` and
  `newton_diagnostic.device`;
- explicit next gate:
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract`;
- report-only validation counts:
  `configured_runtime_validation_recorded_count: 1`,
  `configured_runtime_validation_passed_count: 0`, and
  `configured_runtime_validation_failed_count: 1`;
- zero real runtime counters and false runtime config/source/device validation flags.

Not implemented:

- config file loading;
- environment-variable config loading;
- runtime source resolution;
- runtime device resolution;
- real Newton runtime import;
- `newton.ModelBuilder` instantiation;
- real `add_shape_box` calls;
- Newton engine shape objects;
- model finalization;
- collision pipeline creation or collision;
- contact, drop/settle, or sphere-rain task execution from this report path;
- runtime compatibility validation;
- real-USD evaluation;
- benchmark or collision-quality measurement;
- full CPD paper reproduction or `paper_faithful_offline` support.

## Verification

Focused RED before implementation:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_validation" -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Observed results before implementation: the Python report failed because the configured-runtime
validation payload was missing, and the CLI test still reported the old validation-missing gate.

Focused GREEN after implementation:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_validation" -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Observed results: `4 passed, 1889 deselected in 7.06s`; `1 passed in 2.02s`.

Focused configured-runtime regression after incorporating review feedback:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime" -q
```

Observed result: `43 passed, 1850 deselected in 66.11s`.

Full CPD paper offline report regression after updating legacy implemented-scope assertions:

```bash
python -m pytest tests/test_cpd_paper_offline.py -q
```

Observed result: `1893 passed in 3041.67s (0:50:41)`.

Remaining repository test coverage, excluding the CPD paper offline file already verified above:

```bash
python -m pytest -q --ignore=tests/test_cpd_paper_offline.py
```

Observed result: `409 passed, 2 skipped in 47.90s`.

Docs and workspace validation:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Observed results after the final record update: docs validation passed, site claim validation
passed, and `git diff --check` exited with code 0.

## Review

Code/test review reported no findings. It also checked the validation payload source for forbidden
config/env/source/runtime/import patterns and found none.

Docs/claims review reported two low-severity wording gaps:

- README no-claim caveat omitted the configured-runtime-validation slice;
- the story-status next-slice checklist mentioned keeping the configured-runtime design row
  report-scoped but omitted the preflight and validation rows.

Both wording gaps were fixed before final verification.
