# 2026-05-20 CPD Paper Newton Engine-Builder Runtime-Execution Contract

## Date

2026-05-20

## Status

Implementation, review hardening, and full-regression verification complete.

## Summary

This record documents the
`paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract` slice inside
`cpd_paper_offline_report`.

The slice consumes the report-only engine-builder skipped-smoke row for the synthetic
`paper_single_box` OBB/box lineage and records a report-only skipped-runtime-execution decision:
`skip_real_runtime_execution`. It advances the runtime-lane next gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract`.

This is not real Newton runtime execution. It records the default no-config consequence of the
previous `skip_real_runtime_smoke` decision.

## Scope

Implemented:

- one synthetic fixture: `paper_single_box`;
- one mapped Newton-native shape kind: `box`;
- one runtime-execution row linked to the engine-builder smoke row;
- default runtime-execution decision: `skip_real_runtime_execution`;
- exact input smoke-payload and smoke-row key validation, including missing-key and unexpected-key
  drift checks;
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
- real-USD evaluation;
- benchmark or collision-quality measurement;
- full CPD paper reproduction or `paper_faithful_offline` support.

## Claim Boundary

Allowed wording:

- The report records a bounded engine-builder runtime-execution decision for one synthetic
  mapped-subset `box` fixture.
- The default report skips real runtime execution because the smoke decision skipped real runtime
  smoke.
- The next runtime-lane gate is the runtime-lane review contract.

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

Focused RED before implementation:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_gate -q
```

Observed result before implementation: failed with missing runtime-execution payload.

Focused GREEN after implementation:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_gate tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Observed result: `2 passed`.

Focused schema/static-boundary verification after review hardening:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_newton_shape_runtime_engine_builder_runtime_execution_rejects_input_drift tests/test_cpd_paper_offline.py::test_cpd_paper_newton_shape_runtime_engine_builder_runtime_execution_rejects_input_key_drift_and_copies tests/test_cpd_paper_offline.py::test_cpd_paper_newton_shape_runtime_engine_builder_runtime_execution_rejects_source_row_drift_and_copies tests/test_cpd_paper_offline.py::test_cpd_paper_newton_shape_runtime_engine_builder_runtime_execution_static_boundary_is_report_only -q
```

Observed result: `21 passed`.

Final-review RED for upstream smoke metadata drift:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_newton_shape_runtime_engine_builder_runtime_execution_rejects_input_drift -q
```

Observed result before metadata hardening: `12 failed, 18 passed`.

Focused GREEN after upstream smoke metadata hardening:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_newton_shape_runtime_engine_builder_runtime_execution_rejects_input_drift -q
python -m pytest tests/test_cpd_paper_offline.py -k "engine_builder_runtime_execution" -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
python -m pytest tests/test_cpd_paper_offline.py -k "engine_builder_smoke or engine_builder_runtime_execution or cpd_paper_offline_report_next_gate" -q
```

Observed results: `30 passed`; `36 passed, 1776 deselected`; `1 passed`; `61 passed, 1751
deselected`.

Full-regression verification after metadata hardening:

```bash
python -m pytest -q
```

Observed result: `2221 passed, 2 skipped`.

Final documentation and whitespace checks:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Observed result: docs validation passed, site claim validation passed, and whitespace check passed.

## Multi-Agent Review

Read-only review completed during implementation and final review. Accepted fixes:

- renamed runtime-execution record flags to `decision_recorded` wording so the payload does not
  imply real execution evidence;
- added static-boundary checks for runtime-execution helper code;
- added exact input key validation for smoke payloads and source rows;
- added missing-key tests for required input payload and source-row keys;
- preserved `runtime_execution_source_package_copy_forbidden` as the dedicated payload/row
  package-copy error label;
- preserved semantic drift labels ahead of generic unexpected-key labels;
- updated DeepDive and claim-boundary wording to show that the current next gate is the
  runtime-lane review contract.
- narrowed gap-matrix wording from runtime compatibility to runtime-admissibility/schema preflight;
- added upstream smoke metadata and nested `smoke_contract` drift rejection before consuming the
  smoke payload as runtime-execution lineage;
- added `input_contract_summary` drift rejection so `runtime_execution_source_lineage_checked`
  cannot survive stale summary lineage;
- preserved missing-key error priority ahead of metadata mismatch while keeping semantic drift
  labels ahead of generic unexpected-key labels.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `docs/superpowers/specs/2026-05-20-cpd-paper-newton-engine-builder-runtime-execution-contract-design.md`
- `docs/superpowers/plans/2026-05-20-cpd-paper-newton-engine-builder-runtime-execution-contract.md`

## Next Action

Keep the next implementation slice focused on
`paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract`. Do not use
the skipped-runtime-execution row as Newton support, simulation-checked evidence, benchmark
evidence, or collision-quality evidence.
