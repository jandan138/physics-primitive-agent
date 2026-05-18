# 2026-05-18 CPD Paper Mapped-Subset Newton Shape Runtime Builder-Construction Contract

## Date

2026-05-18

## Status

Complete

## Changes

- Added `paper_mapped_subset_newton_shape_runtime_builder_construction_contract` inside
  `cpd_paper_offline_report`.
- Consumed the single `paper_single_box` builder-preflight row and reconstructed its repo-local
  `NewtonShapeMapping.to_dict()` data.
- Called only the repo-local `_add_static_shape` helper with a recording builder and a fake
  Warp-like module.
- Recorded one JSON-safe fake `add_shape_box` call artifact with body `-1`, fake transform data,
  and the actual mapped box half extents.
- Advanced the report-level runtime-lane next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract`.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_builder_construction or cpd_paper_offline_report_next_gate' -q`
  - Result: `103 passed, 1126 deselected in 164.82s`.
- `PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'changed_decomposition_output_contract_gate or package_adapter_contract_gate or newton_shape_mapping_preflight_gate or newton_shape_mapping_contract_gate or newton_shape_runtime_boundary_preflight_contract_gate or newton_shape_runtime_construction_contract_gate or newton_shape_runtime_builder_preflight_contract_gate or newton_shape_runtime_builder_construction_rejects_input_flags or newton_shape_runtime_builder_construction_static_boundary' -q`
  - Result: `58 passed, 1195 deselected in 94.26s`.
- `PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -q`
  - Result: `1253 passed in 2057.08s`.
- `PYTHONPATH=src python -m pytest -q`
  - Result: `1662 passed, 2 skipped in 2075.75s`.
- `PYTHONPATH=src python scripts/validate_docs.py`
  - Result: `docs validation passed`.
- `PYTHONPATH=src python scripts/validate_site_claims.py`
  - Result: `site claim validation passed`.
- `git diff --check`
  - Result: passed with no output.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `docs/superpowers/specs/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-builder-construction-contract-design.md`
- `docs/superpowers/plans/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-builder-construction-contract.md`

## Claim Impact

- This supports only a single-fixture offline/report-only recording-builder construction artifact.
- This is not a real Newton builder call, not Newton `ModelBuilder` instantiation, not a Newton
  engine shape object, not Newton runtime execution, not real-USD evidence, not benchmark
  evidence, not collision-quality evidence, not `paper_faithful_offline`, not full CPD
  reproduction, not deployment readiness, and not safety certification.

## Next Action

Implement `paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract`
before any real Newton engine-builder boundary crossing.
