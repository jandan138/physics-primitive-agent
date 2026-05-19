# 2026-05-19 CPD Paper Newton Engine-Builder Smoke Contract

## Date

2026-05-19

## Status

Complete

## Summary

This record documents the
`paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract` slice inside
`cpd_paper_offline_report`.

The slice consumes the report-only engine-builder entry row for the synthetic `paper_single_box`
OBB/box lineage and records a report-only skipped-smoke decision:
`skip_real_runtime_smoke`. It advances the runtime-lane next gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract`.

This is not a real Newton runtime smoke. It records the default no-config consequence of the
previous `defer_real_runtime_entry` decision.

## Scope

Implemented:

- one synthetic fixture: `paper_single_box`;
- one mapped Newton-native shape kind: `box`;
- one smoke row linked to the engine-builder entry row;
- default smoke decision: `skip_real_runtime_smoke`;
- zero runtime-smoke attempts;
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

- The report records a bounded engine-builder smoke decision for one synthetic mapped-subset `box`
  fixture.
- The default report skips real runtime smoke because the entry decision deferred real runtime
  entry.
- The next runtime-lane gate is the future runtime-execution contract.

Forbidden wording:

- Newton support is implemented.
- Newton runtime compatibility is validated.
- Real Newton builder calls were validated.
- A Newton engine shape object was created.
- The package is simulation-checked by this report path.
- Collision quality is measured.
- The work reproduces the full CPD paper.
- The artifact is ready for real USD, benchmarks, deployment, or safety certification.

## Verification

Focused RED before implementation:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract_gate -q
```

Observed result before implementation: failed with missing smoke payload.

Focused GREEN after implementation:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "engine_builder_smoke" -q
```

Observed result before review hardening: `20 passed, 1752 deselected`.

Focused GREEN after multi-agent review hardening:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "engine_builder_smoke" -q
```

Observed result: `24 passed, 1752 deselected`.

Focused post-schema regression:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "engine_builder_entry or engine_builder_smoke or api_surface or cpd_paper_offline_report_next_gate" -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Observed results:

- `224 passed, 1552 deselected`;
- `1 passed`.

Full regression after review hardening:

```bash
python -m pytest -q
```

Observed result: `2185 passed, 2 skipped`.

Documentation and whitespace checks after review fixes:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Observed results:

- `docs validation passed`;
- `site claim validation passed`;
- no whitespace errors.

Multi-agent review completed with three read-only reviewers. Accepted fixes:

- removed stale story-status wording that still pointed the next code slice at the smoke contract;
- made the entry record index wording stage-local instead of current-state wording;
- added entry/smoke-specific claim-boundary rules;
- added `newton_engine_shape_object_count: 0` to entry and smoke payload/row/coverage surfaces;
- hardened smoke input validation for `entry_decision`, `remaining_gaps`, and `coverage_summary`
  drift.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `docs/superpowers/specs/2026-05-19-cpd-paper-newton-engine-builder-smoke-contract-design.md`
- `docs/superpowers/plans/2026-05-19-cpd-paper-newton-engine-builder-smoke-contract.md`

## Next Action

Keep the next implementation slice focused on
`paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract`. Do not use
the skipped-smoke row as Newton support, simulation-checked evidence, benchmark evidence, or
collision-quality evidence.
