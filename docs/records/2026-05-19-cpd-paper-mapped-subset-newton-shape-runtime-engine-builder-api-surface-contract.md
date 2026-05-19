# 2026-05-19 CPD Paper Mapped-Subset Newton Shape Runtime Engine-Builder API-Surface Contract

## Summary

This record documents the bounded
`paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract` slice inside
`cpd_paper_offline_report`.

The slice consumes the existing single-fixture
`paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract` row for
`paper_single_box` and records one JSON-safe source-AST API-surface row for the future
`newton.ModelBuilder` / `add_shape_box` boundary. It advances the runtime-lane next gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_import_boundary_preflight_contract`.

## Scope

Implemented:

- one synthetic fixture: `paper_single_box`;
- one mapped Newton-native shape kind: `box`;
- one API-surface row linked to the environment-probe row;
- default no-config status: `not_run_source_dir_not_configured`;
- an opt-in source-AST helper for explicit Newton source directories;
- exact zero counters for real Newton/Warp imports, `newton.ModelBuilder`, real builder calls,
  model finalization, collision pipeline calls, Newton runtime execution, real USD, benchmarks,
  and collision-quality evidence.

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

## Implementation Notes

The source-inspection helper lives in `src/primitive_collision_compiler/newton/env.py` as
`inspect_newton_engine_builder_api_surface()`. It reads source files and parses Python AST only
when a source directory is explicitly provided. It does not import `newton` or `warp`, does not
instantiate `ModelBuilder`, and does not return live runtime objects.

The report payload lives in
`src/primitive_collision_compiler/baselines/cpd_paper/offline.py` and preserves the existing
lineage from:

```text
CollisionPackage.to_dict()
-> runtime admissibility static check
-> NewtonShapeMapping.to_dict()
-> future builder-call plan
-> repo-local recording-builder artifact
-> engine-builder boundary preflight
-> environment-probe row
-> API-surface row
```

The next gate is import-boundary preflight, not a real Newton import.

## Review Fixes

Multi-agent review found three issues before final verification:

- the API-surface helper was still recording `source_commit` through `_git_commit()`, which made
  the explicit-source path broader than the claimed source-file/AST-only boundary;
- the API-surface payload `decision_reason` used `complete`, which could be misread as
  compatibility or readiness;
- two exact report-scope tests and several live docs still had stale current-gate wording, and the
  API-surface row did not carry the source module availability booleans that fed the top-level
  module availability counts.

Fixes applied:

- API-surface source inspection now keeps `source_commit: null` and does not call `_git_commit()`;
- static boundary tests now include transitive API-surface helper functions and forbid `_git_commit`,
  `subprocess`, generic import execution helpers, and Newton/Warp runtime entry points;
- the `decision_reason` now uses `newton_engine_builder_source_api_surface_recorded_...`;
- API-surface rows now carry `module_probe_row_count`, `newton_module_available`, and
  `warp_module_available`, and coverage summary now reports the matching counts;
- live current-gate docs now point to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_import_boundary_preflight_contract`.

Second-review follow-up:

- added `_literal_list_contains()` to the API-surface static-boundary helper set so the test covers
  the full current helper chain used by `_module_exports_name()`;
- clarified environment-probe docs as stage-local where they mention API-surface as the next gate.

## Claim Boundary

Allowed wording:

- The report records a bounded source-AST API-surface row for one synthetic mapped-subset `box`
  fixture.
- The default report remains no-config and imports no real Newton or Warp runtime.
- The next runtime-lane gate is an import-boundary preflight.

Forbidden wording:

- Newton support is implemented.
- Newton runtime compatibility is validated.
- The package is simulation-checked.
- Real Newton builder calls were validated.
- A Newton engine shape object was created.
- Collision quality is measured.
- The work reproduces the full CPD paper.
- The artifact is ready for real USD, benchmarks, deployment, or safety certification.

## Verification

Focused helper RED before implementation:

```bash
PYTHONPATH=src python -m pytest \
  tests/test_cpd_paper_offline.py::test_newton_engine_builder_api_surface_helper_records_unconfigured_source_without_import \
  tests/test_cpd_paper_offline.py::test_newton_engine_builder_api_surface_helper_reads_source_ast_without_importing_modules \
  -q
```

Observed result before implementation: failed with missing
`inspect_newton_engine_builder_api_surface`.

Focused helper GREEN after implementation:

```bash
PYTHONPATH=src python -m pytest \
  tests/test_cpd_paper_offline.py::test_newton_engine_builder_api_surface_helper_records_unconfigured_source_without_import \
  tests/test_cpd_paper_offline.py::test_newton_engine_builder_api_surface_helper_reads_source_ast_without_importing_modules \
  -q
```

Observed result: `2 passed in 0.35s`.

Focused report RED before payload implementation:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py \
  -k 'api_surface or cpd_paper_offline_report_next_gate' -q
```

Observed result before implementation: failed because the payload was absent and the top-level next
gate still pointed at the API-surface gate.

Focused report GREEN after payload implementation:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py \
  -k 'api_surface or cpd_paper_offline_report_next_gate' -q
```

Observed result: `181 passed, 1552 deselected in 280.87s`.

Focused post-review GREEN:

```bash
PYTHONPATH=src python -m pytest \
  tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json \
  tests/test_cpd_paper_offline.py \
  -k 'api_surface or environment_probe or implemented_output_contract_scope or cpd_paper_offline_report_next_gate' \
  -q
```

Observed result: `335 passed, 1399 deselected in 524.54s`.

Static/documentation checks after review fixes:

```bash
PYTHONPATH=src python -m py_compile \
  src/primitive_collision_compiler/baselines/cpd_paper/offline.py \
  src/primitive_collision_compiler/newton/env.py \
  tests/test_cpd_paper_offline.py \
  tests/test_cli.py
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Observed result: all commands exited 0; docs validation and site claim validation passed.

Full CPD paper offline suite after review fixes:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -q
```

Observed result: `1733 passed in 2884.31s`.

Full repository suite after review fixes:

```bash
PYTHONPATH=src python -m pytest -q
```

Observed result: `2142 passed, 2 skipped in 2807.21s`.

## Next Action

Implement
`paper_mapped_subset_newton_shape_runtime_engine_builder_import_boundary_preflight_contract` as a
bounded policy/preflight slice. It must still avoid real Newton/Warp imports, `newton.ModelBuilder`
instantiation, real builder shape calls, model finalization, collision pipeline calls, runtime
tasks, real USD, benchmark, and collision-quality claims.
