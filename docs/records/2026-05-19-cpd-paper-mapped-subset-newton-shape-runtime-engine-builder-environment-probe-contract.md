# 2026-05-19 CPD Paper Mapped-Subset Newton Shape Runtime Engine-Builder Environment Probe Contract

## Summary

This record documents the bounded
`paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract` slice inside
`cpd_paper_offline_report`.

The slice consumes the existing single-fixture
`paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract` row for
`paper_single_box` and records one JSON-safe Newton/Warp environment-provenance row. It advances
the runtime-lane next gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract`.

## Scope

Implemented:

- one synthetic fixture: `paper_single_box`;
- one mapped Newton-native shape kind: `box`;
- one environment-probe row linked to the engine-builder boundary-preflight row;
- configured-source-dir status for the default no-config report;
- JSON-safe Newton/Warp module provenance shape based on `importlib.util.find_spec()`;
- explicit zero counters for real runtime import, `newton.ModelBuilder`, real builder calls, model
  finalization, collision pipeline calls, Newton runtime execution, real USD, benchmarks, and
  collision-quality evidence.

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

The environment helper lives in `src/primitive_collision_compiler/newton/env.py` as
`inspect_newton_warp_provenance()`. It records JSON-safe provenance rows for `newton` and `warp`.
When no Newton source directory is configured, it does not search or import runtime modules and
records `not_run_source_dir_not_configured`.

When a source directory is passed explicitly, the helper may temporarily add that directory to
`sys.path` for `find_spec()` discovery, then restores `sys.path` and cached `newton` / `warp`
module entries. It returns data only, not live module objects.

The report payload is added to
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
```

The next gate is API-surface inspection, not Newton execution.

## Claim Boundary

Allowed wording:

- The report records a bounded Newton/Warp environment-provenance probe for one synthetic
  mapped-subset `box` fixture.
- The default report remains no-config and imports no real Newton or Warp runtime.
- The next runtime-lane gate is bounded API-surface inspection.

Forbidden wording:

- Newton support is implemented.
- Newton runtime is validated.
- The package is simulation-checked.
- Collision quality is measured.
- The work reproduces the full CPD paper.
- The artifact is ready for real USD, benchmarks, deployment, or safety certification.

## Review Notes

Three parallel review angles were requested before implementation:

- Runtime boundary review recommended a bounded environment/provenance probe rather than using the
  existing real-runtime import helper, and explicitly ruled out `ModelBuilder`, `add_shape_*`,
  finalize, `CollisionPipeline`, task execution, USD, benchmark, and quality claims.
- Docs and claim-boundary review recommended distinguishing this slice from the earlier
  no-import boundary-preflight gate and updating reviewer-facing wording to keep this as
  provenance evidence only.
- Schema and tests review recommended exact payload/row key tests, input drift tests, flag drift
  tests, source-row drift tests, CLI drift checks, and static boundary inspection.

Post-implementation review found two follow-up fixes:

- current evidence and claim-boundary docs still had three non-historical lines that made the
  boundary-preflight gate look like the current next gate was still environment-probe; those lines
  were made stage-specific and the current next gate remains API-surface inspection;
- schema review found three copied lineage fields were not drift-locked for the environment-probe
  source row, and that `closed_gate` was not asserted directly; the tests now cover
  `source_newton_shape_mapping_preflight_row_id`, `source_runtime_admissibility_row_id`,
  `source_asset_id`, and top-level `closed_gate`.

## Verification

Focused RED evidence before implementation:

```bash
PYTHONPATH=src python -m pytest \
  tests/test_cpd_paper_offline.py::test_newton_warp_provenance_helper_records_specs_without_importing_modules \
  tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract_gate \
  -q
```

Expected result before implementation: failing helper/payload lookup.

Focused GREEN evidence after implementation:

```bash
PYTHONPATH=src python -m pytest \
  tests/test_cpd_paper_offline.py::test_newton_warp_provenance_helper_records_specs_without_importing_modules \
  tests/test_cpd_paper_offline.py::test_newton_warp_provenance_helper_records_unconfigured_source_without_lookup \
  tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract_gate \
  -q
```

Observed result: `3 passed in 2.02s`.

Focused environment-probe suite:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'environment_probe' -q
```

Observed result: `151 passed, 1396 deselected in 235.96s`.

Focused CLI and boundary suite:

```bash
PYTHONPATH=src python -m pytest \
  tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json \
  tests/test_cpd_paper_offline.py \
  -k 'environment_probe or engine_builder_boundary_preflight or cpd_paper_offline_report_next_gate' \
  -q
```

Observed result: `293 passed, 1255 deselected in 453.01s`.

Post-review lineage fix:

```bash
PYTHONPATH=src python -m pytest \
  tests/test_cpd_paper_offline.py::test_cpd_paper_newton_shape_runtime_engine_builder_boundary_preflight_rejects_source_row_drift \
  tests/test_cpd_paper_offline.py::test_cpd_paper_newton_shape_runtime_engine_builder_environment_probe_rejects_source_row_drift \
  tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract_gate \
  -q
```

Observed result: `37 passed in 59.26s`.

Post-review focused CLI and boundary suite:

```bash
PYTHONPATH=src python -m pytest \
  tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json \
  tests/test_cpd_paper_offline.py \
  -k 'environment_probe or engine_builder_boundary_preflight or cpd_paper_offline_report_next_gate' \
  -q
```

Observed result: `299 passed, 1255 deselected in 479.00s`.

Full CPD paper offline suite:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -q
```

Observed result: `1553 passed in 2575.65s`.

Full repository test suite:

```bash
PYTHONPATH=src python -m pytest -q
```

Observed result: `1962 passed, 2 skipped in 2551.79s`.

## Next Action

Implement
`paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract` as a bounded
inspection slice. It may inspect API-surface facts such as constructor or method visibility, but
must still avoid `newton.ModelBuilder` instantiation, real builder shape calls, model finalization,
collision pipeline calls, runtime tasks, real USD, benchmark, and collision-quality claims.
