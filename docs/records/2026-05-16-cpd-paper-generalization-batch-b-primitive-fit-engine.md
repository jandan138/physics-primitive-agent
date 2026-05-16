# 2026-05-16 CPD Paper Generalization Batch B Primitive Fit Engine

## Date

2026-05-16

## Status

Complete

## Changes

- Added `paper_generalization_batch_b_primitive_fit_engine` to the command-only
  `cpd_paper_offline_report`.
- Closed only the primitive-fit engine generalization gate and advanced the current next gate to
  `paper_generalization_batch_c_search_engine`.
- Kept the report `status: partial` with `paper_faithful_offline_supported: false`.
- Added an offline primitive-fit engine matrix over deterministic in-memory probes for all six
  paper primitive names: `oriented_bounding_box`, `sphere`, `capsule`, `capped_cylinder`,
  `frustum`, and `trapezoidal_prism`.
- Recorded candidate generation, target candidate rows, selected candidate rows, containment
  checks, finite numeric fields, and runtime mapping boundaries for each probe.
- Kept package generation, Newton runtime execution, real-USD evidence, and benchmark work out of
  scope.

## Verification

- Baseline worktree verification initially found that ignored paper source intake was absent from
  the new worktree. `python -m pytest -q` failed in
  `tests/test_cpd_paper_importer.py::test_imported_experiment_translation_ids_stay_semantically_aligned`
  because no imported experiment sections were available.
- The ignored local paper source intake was copied from the main worktree into
  `docs/tmp/papers/arXiv-2602.07369v1/` in this isolated worktree. The copied source remains
  ignored and is not a commit artifact.
- Baseline after the ignored-source sync: `python -m pytest -q` passed with 426 tests.
- Baseline after the ignored-source sync: `python scripts/validate_docs.py` passed.
- Baseline after the ignored-source sync: `python scripts/validate_site_claims.py` passed.
- RED:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_primitive_fit_engine_generalization_gate -q`
  failed because Batch B was still reported missing.
- RED:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_search_generalization -q`
  failed because the top-level next gate still pointed to Batch B.
- RED:
  `python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  failed because the CLI JSON still included the Batch B missing label.
- GREEN:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_primitive_fit_engine_generalization_gate -q`
  passed.
- GREEN:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_search_generalization -q`
  passed.
- GREEN:
  `python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  passed.
- `python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q`: 128 passed.
- `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report`
  plus JSON assertions passed and printed
  `primitive fit engine generalization CLI smoke passed`.
- Docs validation before final review fixes:
  `python scripts/validate_docs.py` passed.
- Site claim validation before final review fixes:
  `python scripts/validate_site_claims.py` passed.
- Whitespace validation before final review fixes:
  `git diff --check` passed.
- Focused post-doc update verification:
  `python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q` passed with
  128 tests.
- Post-review final verification is recorded below after review fixes.
- Post-review final verification:
  `python -m pytest -q` passed with 427 tests.
- Post-review final verification:
  `python scripts/validate_docs.py` passed.
- Post-review final verification:
  `python scripts/validate_site_claims.py` passed.
- Post-review final verification:
  `git diff --check` passed.
- Post-review final CLI smoke:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report`
  plus JSON assertions passed and printed
  `primitive fit engine generalization CLI smoke passed`.

## Review Notes

- Planning review agents agreed Batch B should close through a report payload, not a new CLI,
  package path, Newton runtime path, real-USD path, or benchmark path.
- One planning review recommended keeping `_paper_faithful_offline_scope_criteria()` blocking and
  moving only the current report gate from Batch B to Batch C.
- One planning review recommended using deterministic in-memory parametric primitive-fit probes
  outside `_paper_toy_cases()` so this gate summarizes the reusable primitive-fit engine instead of
  adding more named fixture-breadth cases.
- Final implementation/schema review found no issues. It also reran
  `PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q` with
  128 tests passing and ran a CLI JSON smoke that found no package/Newton/USD/benchmark trigger
  flags set true.
- Final docs/claim-boundary review found three status/story consistency issues: the registry entry
  was still planned, this record was still in progress, and some current-next-gate wording could
  read as Batch B still being the current gate. The current-next-gate wording was changed to
  historical source-policy handoff wording, and the record plus registry were updated for this
  completed gate.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `docs/superpowers/specs/2026-05-16-cpd-paper-primitive-fit-engine-generalization-design.md`
- `docs/superpowers/plans/2026-05-16-cpd-paper-primitive-fit-engine-generalization.md`
- `experiments/registry.yaml`

## Claim Impact

Supported:

- The command-only `cpd_paper_offline_report` includes a partial offline primitive-fit engine
  generalization matrix for deterministic in-memory probes.
- `paper_generalization_batch_b_primitive_fit_engine` is closed as an offline report-only gate.
- The next required gate is `paper_generalization_batch_c_search_engine`.

Not supported:

- robust primitive fitting;
- `paper_faithful_offline`;
- full CPD paper reproduction;
- package generation;
- Newton runtime execution;
- real-USD evidence;
- benchmark or collision-quality evidence;
- deployment readiness or safety certification.

## Next Action

Proceed to `paper_generalization_batch_c_search_engine` as the next offline generalization slice.
Keep the lane partial and offline-only until a later dated record documents a stronger boundary.
