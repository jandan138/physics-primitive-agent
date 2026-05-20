# 2026-05-20 CPD Paper Newton Engine-Builder Runtime-Lane Review Contract

## Date

2026-05-20

## Status

Implementation, focused schema hardening, final review, and full-regression verification are
complete. Commit, merge, push, and worktree cleanup remain pending.

## Summary

This record documents the
`paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract` slice inside
`cpd_paper_offline_report`.

The slice consumes the report-only engine-builder skipped-runtime-execution row for the synthetic
`paper_single_box` OBB/box lineage and records a report-only runtime-lane claim-boundary review:
`runtime_lane_review_decision: keep_real_runtime_execution_blocked`. It advances the runtime-lane
next gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract`.

This is not real Newton runtime execution and not runtime compatibility evidence. It records that
the previous `skip_real_runtime_execution` decision remains a boundary, not a compatibility pass.

## Scope

Implemented:

- one synthetic fixture: `paper_single_box`;
- one mapped Newton-native shape kind: `box`;
- one runtime-lane review row linked to the engine-builder runtime-execution row;
- default runtime-lane review decision: `keep_real_runtime_execution_blocked`;
- exact input runtime-execution payload and runtime-execution row key validation, including
  missing-key and unexpected-key drift checks;
- source-package copy rejection at payload and row scope;
- zero runtime-execution attempts;
- exact zero counters for real Newton/Warp imports, `newton.ModelBuilder`, Newton engine shape
  objects, real builder calls, model finalization, collision pipeline creation/collide calls,
  Newton runtime execution, real USD, benchmarks, and collision-quality evidence.

Not implemented:

- real Newton runtime import;
- `newton.ModelBuilder` instantiation;
- real `add_shape_box` calls;
- Newton engine shape objects;
- model finalization;
- collision pipeline creation or collision;
- contact, drop/settle, or sphere-rain task execution from this report path;
- runtime compatibility validation;
- configured Newton/Warp source or runtime input design;
- real-USD evaluation;
- benchmark or collision-quality measurement;
- full CPD paper reproduction or `paper_faithful_offline` support.

## Claim Boundary

Allowed wording:

- The report records a bounded runtime-lane claim-boundary review for one synthetic mapped-subset
  `box` fixture.
- The review preserves the skipped-runtime-execution boundary and keeps real runtime work blocked.
- The next runtime-lane gate is the configured-runtime design contract.

Forbidden wording:

- Newton support is implemented.
- Newton runtime compatibility is validated.
- Real Newton builder calls were validated.
- A Newton engine shape object was created.
- Newton runtime execution ran or passed.
- The package is simulation-checked by this report path.
- Collision quality is measured.
- The work reproduces the full CPD paper.
- The artifact is ready for real USD, benchmarks, deployment, or safety certification.

## Verification

Focused RED before Task 1 implementation:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_gate -q
```

Observed result before implementation: failed with missing runtime-lane review payload.

Focused GREEN after Task 1 implementation:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_gate tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Observed result: `2 passed`.

Focused RED after review hardening tests:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_newton_shape_runtime_engine_builder_runtime_lane_review_payload_schema_is_exact tests/test_cpd_paper_offline.py::test_cpd_paper_newton_shape_runtime_engine_builder_runtime_lane_review_rejects_input_drift tests/test_cpd_paper_offline.py::test_cpd_paper_newton_shape_runtime_engine_builder_runtime_lane_review_rejects_input_key_drift_and_copies tests/test_cpd_paper_offline.py::test_cpd_paper_newton_shape_runtime_engine_builder_runtime_lane_review_rejects_input_coverage_summary_drift tests/test_cpd_paper_offline.py::test_cpd_paper_newton_shape_runtime_engine_builder_runtime_lane_review_rejects_source_row_drift_and_copies tests/test_cpd_paper_offline.py::test_cpd_paper_newton_shape_runtime_engine_builder_runtime_lane_review_static_boundary_is_report_only -q
```

Observed result before hardening: `22 failed, 15 passed`.

Focused GREEN after schema, drift, and static-boundary hardening:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "runtime_lane_review" -q
python -m pytest tests/test_cpd_paper_offline.py -k "engine_builder_runtime_execution or runtime_lane_review or cpd_paper_offline_report_next_gate" -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
git diff --check
```

Observed results: `38 passed, 1812 deselected`; `75 passed, 1775 deselected`; `1 passed`;
whitespace check passed.

Documentation checks after Task 3:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Observed result: docs validation passed; site claim validation passed; whitespace check passed.

First full-regression attempt after final review:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "runtime_lane_review" -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
python -m pytest -q
```

Observed results before the final test expectation sync: `38 passed, 1812 deselected`; `1 passed`;
then full `python -m pytest -q` failed with two stale legacy
`implemented_output_contract_scope` full-list assertions that still ended at the skipped-runtime
execution contract. The root cause was test expectation drift, not report output drift: the report
correctly included the runtime-lane review contract and kept the current next gate at the
configured-runtime design contract.

Targeted repro and fix verification:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_changed_decomposition_output_contract_gate tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_package_adapter_contract_gate -q
```

Observed results: failed before sync; `2 passed` after adding the runtime-lane review contract to
the two legacy full-list expectations.

Final verification after the legacy expectation sync:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "runtime_lane_review" -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Observed results: `38 passed, 1812 deselected`; `1 passed`; `2259 passed, 2 skipped`; docs
validation passed; site claim validation passed; whitespace check passed.

## Multi-Agent Review

Read-only review completed during implementation and final Task 1/2 review. Accepted fixes:

- replaced `runtime_lane_review_passed_count` with `runtime_lane_review_recorded_count` and
  `runtime_lane_claim_boundary_preserved_count`;
- added exact payload and row schema tests for the runtime-lane review gate;
- added input metadata, count, flag, coverage-summary, source-row, and source-package-copy drift
  rejection;
- added static-boundary checks for runtime-lane review helpers;
- updated design and plan wording so the next gate is the configured-runtime design contract.

Second-round code/schema review reported no findings for `offline.py`, `tests/test_cpd_paper_offline.py`,
or `tests/test_cli.py`. Second-round claim-boundary review identified stale docs, which this Task 3
record and companion docs updates address.

Final Task 4 review found three record or wording issues, all accepted:

- revised README wording so the runtime-lane review contract is described as a stage-local
  follow-up from the skipped-runtime-execution slice, not the current next gate;
- revised this record status so final review completion is not overstated before final verification;
- added the observed Task 3 documentation and site-claim validation evidence to this record.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `README.md`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `docs/superpowers/specs/2026-05-20-cpd-paper-newton-engine-builder-runtime-lane-review-contract-design.md`
- `docs/superpowers/plans/2026-05-20-cpd-paper-newton-engine-builder-runtime-lane-review-contract.md`

## Next Action

Keep the next implementation slice focused on
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract`. Do not
use the skipped-runtime-execution row or runtime-lane review row as Newton support,
simulation-checked evidence, benchmark evidence, runtime compatibility evidence, or
collision-quality evidence.
