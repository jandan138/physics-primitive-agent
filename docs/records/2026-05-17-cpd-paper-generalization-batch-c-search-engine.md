# 2026-05-17 CPD Paper Generalization Batch C Search Engine

## Date

2026-05-17

## Status

Complete

## Changes

- Added `paper_generalization_batch_c_search_engine` to the command-only
  `cpd_paper_offline_report`.
- Closed only the search-engine generalization gate and advanced the current next gate to
  `paper_generalization_batch_d_postprocess_policy`.
- Kept the report `status: partial` with `paper_faithful_offline_supported: false`.
- Added an offline search-trace matrix that summarizes existing deterministic `collapse_trace`
  evidence for topology queue target-count stops, weighted-priority ordering, equal-cost queue
  ties, threshold-disabled component-pair acceptance, zero and positive finite threshold blocking,
  multi-candidate component-pair ordering, and capped skipped-pair accounting.
- Recorded the search contract: separate `paper_base_cost` and `weighted_priority_cost`, queue key
  field order, component-pair insertion after topology exhaustion, threshold metric
  `paper_base_cost`, stop reasons, and no lookahead.
- Kept package generation, Newton runtime execution, real-USD evidence, and benchmark work out of
  scope.

## Verification

- RED:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_search_engine_generalization_gate tests/test_cpd_paper_offline.py::test_cpd_paper_search_engine_generalization_rows_match_case_payloads tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  failed because Batch C was still reported missing and `paper_generalization_batch_c_search_engine`
  did not exist.
- GREEN:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_search_engine_generalization_gate tests/test_cpd_paper_offline.py::test_cpd_paper_search_engine_generalization_rows_match_case_payloads tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  passed.
- Focused suite:
  `python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q` passed with 130 tests.
- Final full suite:
  `python -m pytest -q` passed with 429 tests.
- Final docs validation:
  `python scripts/validate_docs.py` passed.
- Final site claim validation:
  `python scripts/validate_site_claims.py` passed.
- Final whitespace validation:
  `git diff --check` passed.
- Final source-local smoke:
  `PYTHONPATH=src python - <<'PY' ... PY` passed and printed
  `search engine generalization CLI smoke passed`.

## Review Notes

- Planning reviewers recommended closing Batch C with a top-level offline report payload that
  summarizes existing `collapse_trace` outputs rather than adding a new search algorithm.
- Planning reviewers recommended keeping historical Batch A and Batch B payload next-gate wording
  intact while advancing only the current top-level gate to Batch D.
- Final implementation/schema review found no issues. It reran the CPD paper offline and CLI test
  subset, docs validation, whitespace validation, and a CLI JSON smoke that confirmed Batch C
  payload shape, D/E failure labels, Batch D next gate, eight search rows, and false
  package/Newton/USD/benchmark triggers.
- Final docs/claim-boundary review found no issues and confirmed the Batch C slice is consistently
  bounded as offline/report-only, D is the current next gate, D/E remain missing, and unsupported
  claims remain blocked.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `docs/superpowers/specs/2026-05-17-cpd-paper-search-engine-generalization-design.md`
- `docs/superpowers/plans/2026-05-17-cpd-paper-search-engine-generalization.md`
- `experiments/registry.yaml`

## Claim Impact

Supported:

- The command-only `cpd_paper_offline_report` includes a partial offline search-engine
  generalization matrix for deterministic synthetic traces.
- `paper_generalization_batch_c_search_engine` is closed as an offline report-only gate.
- The next required gate is `paper_generalization_batch_d_postprocess_policy`.

Not supported:

- generalized optimizer correctness;
- `paper_faithful_offline`;
- full CPD paper reproduction;
- package generation;
- Newton runtime execution;
- real-USD evidence;
- benchmark or collision-quality evidence;
- deployment readiness or safety certification.
