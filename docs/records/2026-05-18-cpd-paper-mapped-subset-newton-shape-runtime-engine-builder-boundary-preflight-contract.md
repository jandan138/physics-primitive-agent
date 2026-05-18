# 2026-05-18 CPD Paper Mapped-Subset Newton Shape Runtime Engine-Builder Boundary Preflight Contract

## Date

2026-05-18

## Status

Complete

## Changes

- Added `paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract`
  to `cpd_paper_offline_report`.
- Consumed the single `paper_single_box` builder-construction row and recorded one offline/static
  future-boundary checklist row for the later real `newton.ModelBuilder` / `add_shape_box`
  environment boundary.
- Kept all real Newton boundary crossings out of scope: no real Newton import, no Warp import, no
  `newton.ModelBuilder` instantiation, no real builder shape call, no model finalization, no
  collision pipeline call, and no Newton runtime execution.
- Advanced the runtime-lane next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract`.
- Updated current-status, claim-boundary, DeepDive, index, gap-matrix, offline-lane, and story
  documentation so the current gate is the environment probe, not boundary preflight.

## Verification

- RED check, expected failure before implementation:
  `PYTHONPATH=src python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cpd_paper_offline.py -k 'engine_builder_boundary_preflight or cpd_paper_offline_report_next_gate' -q`
  failed on the missing payload/helper and old next-gate assertions.
- Focused green check after implementation:
  `PYTHONPATH=src python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cpd_paper_offline.py -k 'engine_builder_boundary_preflight or cpd_paper_offline_report_next_gate' -q`
  passed with `126 passed, 1253 deselected`.
- Adjacent Newton runtime-lane green check:
  `PYTHONPATH=src python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_builder_construction or newton_shape_runtime_builder_preflight or newton_shape_runtime_construction_contract_gate or engine_builder_boundary_preflight or cpd_paper_offline_report_next_gate' -q`
  passed with `369 passed, 1010 deselected`.
- Post-review targeted regression check:
  `PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'engine_builder_boundary_preflight_rejects_input_true_flag_drift or engine_builder_boundary_preflight_rejects_row_list_drift or engine_builder_boundary_preflight_rejects_malformed_builder_dimensions' -q`
  passed with `17 passed, 1378 deselected`.
- Post-review focused gate check:
  `PYTHONPATH=src python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cpd_paper_offline.py -k 'engine_builder_boundary_preflight or newton_shape_runtime_builder_construction or cpd_paper_offline_report_next_gate' -q`
  passed with `270 passed, 1126 deselected`.
- Post-review documentation and whitespace checks:
  `PYTHONPATH=src python scripts/validate_docs.py`,
  `PYTHONPATH=src python scripts/validate_site_claims.py`, and `git diff --check` passed.
- Final full CPD paper offline check after fixing two stale `implemented_output_contract_scope`
  expectations:
  `PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -q` passed with
  `1395 passed`.
- Final full repository check:
  `PYTHONPATH=src python -m pytest -q` passed with `1804 passed, 2 skipped`.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `README.md`
- `docs/index.md`
- `docs/deepdive/evidence-status.md`
- `docs/deepdive/message-map.md`
- `docs/reference/claim-boundaries.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/records/README.md`
- `docs/superpowers/specs/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-engine-builder-boundary-preflight-contract-design.md`
- `docs/superpowers/plans/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-engine-builder-boundary-preflight-contract.md`

## Claim Impact

- Supports only the claim that one synthetic `paper_single_box` row now has an offline/static
  Newton engine-builder boundary-preflight checklist in the partial CPD paper offline report.
- Does not support Newton readiness, Newton support, real Newton execution, real-USD evidence,
  benchmark evidence, collision-quality validation, paper primitive vocabulary coverage,
  approximation support, `paper_faithful_offline`, full CPD reproduction, deployment readiness,
  safety certification, or general package readiness.

## Next Action

- Implement
  `paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract` as the next
  bounded runtime-lane gate before any real Newton builder boundary crossing.
