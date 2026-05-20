# 2026-05-20 CPD Paper Newton Engine-Builder Configured Runtime Execution Contract

## Date

2026-05-20

## Status

Complete

## Changes

- Added `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract`
  to `cpd_paper_offline_report`.
- The payload consumes the configured-runtime smoke row, records
  `skip_real_runtime_execution_configured_runtime_smoke_not_allowed`, and advances the current
  report next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review_contract`.
- The slice keeps configured-runtime execution allowed, attempted, and passed false.
- The slice keeps Newton/Warp imports, `newton.ModelBuilder` construction, builder shape calls,
  model finalization, collision pipeline calls, Newton execution, runtime compatibility, real-USD
  evaluation, benchmarks, and collision-quality validation at false or zero.
- Source-row validators now reject drift in inherited source/device resolution flags before the
  execution row is built.

## Verification

Focused implementation evidence:

```text
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_execution" -q
25 passed, 1924 deselected in 40.64s

python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
1 passed in 2.66s
```

Broader branch evidence after documentation sync and stale top-level gate assertion cleanup:

```text
python scripts/validate_docs.py
docs validation passed

python scripts/validate_site_claims.py
site claim validation passed

git diff --check
no output

python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime" -q
99 passed, 1850 deselected in 158.88s (0:02:38)
```

Final regression evidence after the stale overview scope assertions were updated to include the
new execution contract:

```text
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_changed_decomposition_output_contract_gate tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_package_adapter_contract_gate -q
2 passed in 5.66s

python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime" -q
99 passed, 1850 deselected in 156.53s (0:02:36)

python -m pytest -q
2358 passed, 2 skipped in 3138.70s (0:52:18)
```

## Review Follow-Up

- Code review found the first execution-decision wording implied the smoke payload was missing even
  though the execution contract consumes the smoke payload. The decision/status strings now say the
  smoke row exists but smoke was not allowed.
- Code review found the source-row validator did not guard inherited source/device resolution
  booleans. The validator now rejects those mismatches before coverage counts are summarized.
- Test review found missing row-level runtime counter assertions, missing duplicate-row drift
  coverage, and no static report-only boundary audit for the new execution helpers. The focused
  tests now cover those cases.
- Documentation review found stale current-status wording in `docs/index.md` and
  `docs/deepdive/evidence-status.md` that still pointed at configured-runtime execution as the
  current next gate. Those sections now identify configured-runtime lane review as the current next
  gate, and the execution record status is complete.
- A second narrow code/test review found no issues in the configured-runtime execution helpers or
  focused tests.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `docs/deepdive/evidence-status.md`
- `docs/deepdive/message-map.md`
- `docs/reference/claim-boundaries.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-story-status.md`

## Claim Impact

- Supports only a report-only configured-runtime execution decision for one synthetic
  `paper_single_box` lineage.
- Does not support real Newton runtime execution, runtime compatibility, package readiness,
  real-USD evidence, benchmark evidence, collision-quality validation, deployment readiness,
  safety certification, full CPD reproduction, or `paper_faithful_offline`.

## Next Action

- Add the configured-runtime lane-review contract while preserving the same single-fixture,
  report-only claim boundary.
