# 2026-05-19 CPD Paper Newton Engine-Builder Entry Contract

## Date

2026-05-19

## Status

Complete

## Summary

This record documents the consolidated
`paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract` slice inside
`cpd_paper_offline_report`.

The slice consumes the bounded source-AST API-surface row for the synthetic `paper_single_box`
OBB/box lineage and records a report-only default entry decision:
`defer_real_runtime_entry`. It advances the runtime-lane next gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract`.

This is the anti-overdesign follow-through from the engine-builder gate consolidation record: it
keeps the useful boundary-preflight, environment-probe, and API-surface evidence, but does not add
separate import-boundary-preflight/import-contract gates.

## Scope

Implemented:

- one synthetic fixture: `paper_single_box`;
- one mapped Newton-native shape kind: `box`;
- one entry row linked to the API-surface row;
- default entry decision: `defer_real_runtime_entry`;
- zero runtime-entry attempts;
- exact zero counters for real Newton/Warp imports, `newton.ModelBuilder`, real builder calls,
  model finalization, collision pipeline creation/collide calls, Newton runtime execution, real
  USD, benchmarks, and collision-quality evidence.

Not implemented:

- real Newton runtime import;
- `newton.ModelBuilder` instantiation;
- real `add_shape_box` calls;
- Newton engine shape objects;
- model finalization;
- collision pipeline creation or collision;
- contact, drop/settle, or sphere-rain task execution;
- real-USD evaluation;
- benchmark or collision-quality measurement;
- full CPD paper reproduction or `paper_faithful_offline` support.

## Claim Boundary

Allowed wording:

- The report records a bounded engine-builder entry decision for one synthetic mapped-subset `box`
  fixture.
- The default report remains no-config and records no real runtime entry.
- The next runtime-lane gate is the future engine-builder smoke contract.

Forbidden wording:

- Newton support is implemented.
- Newton runtime compatibility is validated.
- Real Newton builder calls were validated.
- A Newton engine shape object was created.
- The package is simulation-checked.
- Collision quality is measured.
- The work reproduces the full CPD paper.
- The artifact is ready for real USD, benchmarks, deployment, or safety certification.

## Verification

Focused RED before implementation:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "engine_builder_entry" -q
```

Observed result before implementation: failed with missing entry payload/helper functions.

Focused GREEN after implementation:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "engine_builder_entry" -q
```

Observed result: `19 passed, 1733 deselected`.

CLI report GREEN after synchronization:

```bash
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Observed result: `1 passed`.

Multi-agent review found and the implementation fixed:

- an entry-row lineage bug where `paper_primitive` was incorrectly copied from
  `primitive_spec_kind`;
- stale tests and docs that still described entry as the current next gate after the entry contract
  had closed.

Focused post-review regression checks:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "engine_builder_entry" -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
python -m pytest tests/test_cpd_paper_offline.py -k "engine_builder_entry or api_surface or cpd_paper_offline_report_next_gate" -q
```

Observed results:

- `19 passed, 1733 deselected`;
- `1 passed`;
- `200 passed, 1552 deselected`.

Broad verification before merge:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
python -m pytest -q
```

Observed results:

- `docs validation passed`;
- `site claim validation passed`;
- `git diff --check` exited 0;
- `2161 passed, 2 skipped`.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `docs/superpowers/specs/2026-05-19-cpd-paper-newton-engine-builder-entry-contract-design.md`
- `docs/superpowers/plans/2026-05-19-cpd-paper-newton-engine-builder-entry-contract.md`

## Next Action

Merge the report-only entry contract, then keep the next implementation slice focused on
`paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract`.
