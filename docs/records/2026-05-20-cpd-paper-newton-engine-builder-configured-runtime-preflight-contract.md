# 2026-05-20 CPD Paper Newton Engine-Builder Configured-Runtime Preflight Contract

## Date

2026-05-20

## Status

Implementation, focused configured-runtime regression, full-regression verification, and scoped
multi-agent review are complete. Merge, push, and worktree cleanup remain pending.

## Summary

This record documents the
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract`
slice inside `cpd_paper_offline_report`.

The slice consumes the report-only configured-runtime design row for the synthetic
`paper_single_box` OBB/box lineage and records a report-only configured-runtime preflight:
`configured_runtime_preflight_decision:
record_configured_runtime_preflight_keep_real_runtime_blocked`. It advances the current next gate
to
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_validation_contract`.

This is not runtime config validation. It records that the bounded preflight row exists while
keeping runtime config validation, runtime source/device resolution, real Newton/Warp imports,
`newton.ModelBuilder`, real builder calls, model finalization, collision pipeline calls, Newton
runtime execution, real USD, benchmarks, and collision-quality evidence at zero or false.

## Scope

Implemented:

- one synthetic fixture: `paper_single_box`;
- one mapped Newton-native shape kind: `box`;
- one configured-runtime preflight row linked to the configured-runtime design row;
- required runtime config-key and runtime-input lists carried forward from the design row;
- explicit next gate:
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_validation_contract`;
- report-only preflight counts:
  `configured_runtime_preflight_recorded_count: 1`,
  `configured_runtime_preflight_passed_count: 1`, and
  `configured_runtime_validation_ready_count: 0`;
- zero real runtime counters and false runtime config/source/device validation flags.

Not implemented:

- runtime config file or environment validation;
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
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_preflight" -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Observed results before implementation: the Python report failed with the configured-runtime
preflight payload missing, and the CLI test still reported the old preflight-missing gate.

Focused GREEN after implementation:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_preflight" -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Observed results: `2 passed, 1885 deselected in 3.96s`; `1 passed in 2.05s`.

Reviewer-requested exact-schema RED after initial GREEN:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_preflight_rejects" -q
```

Observed result before the exact-schema fix: both drift tests failed with `DID NOT RAISE`,
confirming that unexpected top-level preflight input keys and unexpected configured-runtime design
source-row keys were still accepted.

Focused GREEN after exact-schema fix:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_preflight_rejects" -q
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_preflight" -q
```

Observed results: `2 passed, 1887 deselected in 4.02s`; `4 passed, 1885 deselected in 7.28s`.

Configured-runtime regression:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime" -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Observed results after the exact-schema fix: `39 passed, 1850 deselected in 60.13s`; `1 passed in
1.92s`.

Documentation and claim-boundary checks:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Observed results: docs validation passed, site claim validation passed, and whitespace check
passed.

Full regression:

```bash
python -m pytest -q
```

Observed result: `2298 passed, 2 skipped in 3075.66s (0:51:15)`.

Scoped multi-agent review:

- docs/claim review found stale current-gate wording in `README.md` and
  `docs/reference/cpd-paper-faithful-offline-lane-spec.md`; both were corrected to point at the
  configured-runtime validation gate;
- code/test review found the exact-schema acceptance gap above; focused RED tests were added and
  the validator was tightened;
- final scoped code/test re-review reported no findings for the configured-runtime preflight fix
  and report-only boundary.
