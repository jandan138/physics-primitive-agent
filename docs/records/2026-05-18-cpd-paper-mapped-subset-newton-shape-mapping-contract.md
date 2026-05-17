# 2026-05-18 CPD Paper Mapped-Subset Newton Shape-Mapping Contract

## Date

2026-05-18

## Status

Complete in the feature branch.

## Context

The previous gate, `paper_mapped_subset_newton_shape_mapping_preflight_contract`, consumed the
single synthetic `paper_single_box` runtime-admissibility row and recorded one offline/static
mapper-handoff preflight row. It deliberately kept mapping attempts, Newton mapping records,
Newton runtime execution, real-USD evaluation, benchmark work, and collision-quality measurement
at zero or false.

That previous gate pointed next to:

`paper_mapped_subset_newton_shape_mapping_contract`

This record covers only that next single-fixture offline/static descriptor contract. It does not
cover actual Newton shape object construction, Newton runtime execution, real-USD evaluation,
benchmark work, or collision-quality measurement.

## What Changed

The partial `cpd_paper_offline_report` now includes
`paper_mapped_subset_newton_shape_mapping_contract`.

The new payload:

- consumes `paper_mapped_subset_newton_shape_mapping_preflight_contract`;
- validates the input gate id, expected next gate, row counts, false boundary flags, and one
  shape-mapping preflight row;
- validates the source identity fields for the deterministic `paper_single_box` OBB/box row;
- rejects copied source package dicts so the descriptor contract stays a row-level handoff instead
  of a duplicate package store;
- validates that the candidate PrimitiveSpec-like dict has target kind `box`;
- validates finite center, axes, dimensions, and positive box half extents before creating the
  report-scoped descriptor dict;
- records exactly one `shape_mapping_rows` entry for
  `newton_shape_mapping__paper_single_box__box`;
- records exactly one `newton_shape_descriptor_dict` with target kind `box`, source fixture and
  primitive ids, center, axes, half extents, and
  `mapping_contract: report_scoped_static_descriptor_no_newton_call`;
- records `mapping_attempt_count: 0`;
- records `newton_mapping_record_count: 0`;
- records `newton_shape_object_count: 0`;
- records `newton_runtime_execution_count: 0`;
- keeps Newton support claims, approximation policy, package generation triggers, Newton runtime
  triggers, real-USD triggers, benchmark triggers, collision-quality measurement, deployment, and
  certification claims zero or false;
- keeps `paper_faithful_offline` blockers separate from runtime-lane gates;
- advances the next gate to
  `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`.

The row is intentionally a narrow static report descriptor for one synthetic box artifact. It says
the report has enough JSON-safe descriptor fields for a later Newton runtime-boundary check; it
does not say Newton has mapped, supported, constructed, or executed the shape.

## Verification

Commands run during this branch after implementation:

```bash
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
# exit 0; 3 passed, 109 deselected in 5.51s

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_mapping_contract' -q
# exit 0; 60 passed, 760 deselected in 94.52s

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_mapping_contract or newton_shape_runtime_boundary' -q
# exit 0; 61 passed, 759 deselected in 102.20s

PYTHONPATH=src python scripts/validate_docs.py
# exit 0; docs validation passed

PYTHONPATH=src python scripts/validate_site_claims.py
# exit 0; site claim validation passed

git diff --check
# exit 0

PYTHONPATH=src python -m pytest -q
# exit 0; 1229 passed, 2 skipped in 1491.57s (0:24:51)
```

Multi-agent review found one stale story sentence and two stale test names. The story sentence was
updated to point the next step at the runtime-boundary preflight instead of the just-closed
descriptor row, and the stale test names were updated to match their assertions.

## Artifacts

- Report key: `paper_mapped_subset_newton_shape_mapping_contract`
- Row id: `newton_shape_mapping__paper_single_box__box`
- Closed gate: `paper_mapped_subset_newton_shape_mapping_contract`
- Input gate: `paper_mapped_subset_newton_shape_mapping_preflight_contract`
- Next gate: `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`
- Source fixture: `paper_single_box`
- Source primitive family: `oriented_bounding_box`
- Target descriptor kind: `box`

## Claim Boundary

This record supports only the statement that the CPD paper offline report has one static,
single-fixture Newton shape descriptor contract row for the synthetic `paper_single_box` box
artifact.

Do not cite this record as evidence for Newton readiness, Newton support, actual Newton shape
object construction, Newton runtime execution, real-USD evaluation, benchmark evidence,
collision-quality evidence, paper primitive vocabulary coverage, approximation-policy support,
`paper_faithful_offline`, full CPD reproduction, deployment readiness, safety certification, or
general package readiness.
