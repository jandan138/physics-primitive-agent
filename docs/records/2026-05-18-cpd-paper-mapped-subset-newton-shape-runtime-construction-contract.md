# 2026-05-18 CPD Paper Mapped-Subset Newton Shape Runtime-Construction Contract

Date: 2026-05-18

## Summary

Implemented the single-fixture offline/report-scoped
`paper_mapped_subset_newton_shape_runtime_construction_contract` in
`cpd_paper_offline_report`.

This gate consumes the one synthetic `paper_single_box` Newton shape runtime-boundary preflight
row and constructs exactly one repo-local `NewtonShapeMapping.to_dict()` report record for the
static box descriptor. In plain terms, the previous gate only checked that the descriptor was ready
to approach the runtime boundary; this gate turns that descriptor into the repository's JSON-safe
Newton shape mapping record.

The next missing runtime-lane gate is
`paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`.

## Boundary

This is report-only evidence. It does not import Newton or warp, call `map_package_shapes`, call a
Newton builder, construct a Newton engine shape object, run Newton, load real USD, run benchmarks,
measure collision quality, claim Newton support/readiness, claim package readiness, claim
`paper_faithful_offline`, or claim full CPD reproduction.

Recorded counts:

- `constructed_newton_shape_mapping_record_count: 1`
- `newton_mapping_record_count: 1`
- `newton_mapper_call_count: 0`
- `newton_shape_object_count: 0`
- `newton_engine_shape_object_count: 0`
- `newton_builder_shape_call_count: 0`
- `newton_runtime_execution_count: 0`

The row stays tied to the synthetic `paper_single_box` fixture and target Newton shape kind `box`.
It is not real-USD evidence, benchmark evidence, collision-quality evidence, deployment readiness,
or safety certification.

## Evidence

Focused RED checks were run before implementation and failed because the construction payload and
builder-preflight next gate were not wired yet.

Focused GREEN checks after implementation:

- `PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q`
  - `3 passed, 109 deselected in 5.17s`
- `PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_construction or newton_shape_runtime_boundary_preflight or newton_shape_mapping_contract' -q`
  - `251 passed, 760 deselected in 395.69s (0:06:35)`
- `PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_construction_static_boundary or records_one_mapping_row' -q`
  - `2 passed, 1009 deselected in 3.26s`
- `PYTHONPATH=src python scripts/validate_docs.py`
  - docs validation passed
- `PYTHONPATH=src python scripts/validate_site_claims.py`
  - site claim validation passed
- `git diff --check`
  - exit code 0
- `PYTHONPATH=src python -m pytest -q`
  - `1420 passed, 2 skipped in 1781.30s (0:29:41)`

Before the full-suite pass, one full run exposed stale test expectations in older gate tests:
two exact implemented-scope assertions omitted this new construction gate, and four static
source-slice tests ended too late and incorrectly scanned the later construction helper. The tests
were narrowed to their intended gate boundaries, the exact scope assertions were updated, and the
six failing tests passed before the full suite was rerun.

## Review Notes

Multi-agent implementation review found no runtime-boundary issues in `offline.py`: the only added
executable construction is the repo-local `NewtonShapeMapping(...).to_dict()` record.

Multi-agent test review found that the static test should explicitly pin `mapping.to_dict()`, widen
the forbidden runtime/builder/USD/warp patterns, and assert the positive row lineage for
`source_newton_shape_mapping_preflight_row_id` and `source_asset_id`. Those test gaps were fixed
before this record was added.

## Next Gate

Implement `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract` as a bounded
preflight before any Newton builder shape call or Newton engine shape object construction.
