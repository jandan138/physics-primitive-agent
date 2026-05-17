# 2026-05-18 CPD Paper Mapped-Subset Newton Shape-Mapping Preflight Contract

## Date

2026-05-18

## Status

Complete in the feature branch.

## Context

The previous gate, `paper_mapped_subset_runtime_admissibility_contract`, consumed the single
synthetic `paper_single_box` runtime-admissibility preflight row and recorded one offline/static
finite-geometry and box-schema check. It deliberately kept Newton shape mapping, Newton runtime
execution, real-USD evaluation, benchmark work, and collision-quality measurement at zero or
false.

That previous gate pointed next to:

`paper_mapped_subset_newton_shape_mapping_preflight_contract`

This record covers only that next single-fixture offline/static preflight. It does not cover
actual Newton shape mapping, Newton runtime execution, real-USD evaluation, benchmark work, or
collision-quality measurement.

## What Changed

The partial `cpd_paper_offline_report` now includes
`paper_mapped_subset_newton_shape_mapping_preflight_contract`.

The new payload:

- consumes `paper_mapped_subset_runtime_admissibility_contract`;
- validates the input gate id, expected next gate, row counts, false boundary flags, and one
  runtime-admissibility row;
- validates the source identity fields for the deterministic `paper_single_box` OBB/box row;
- rejects copied source package dicts so the preflight stays a row-level handoff instead of a
  duplicate package store;
- validates that the candidate PrimitiveSpec-like dict has target kind `box`;
- validates finite center, axes, dimensions, and positive box half extents for later mapper
  handoff;
- records exactly one `newton_shape_mapping_preflight_rows` entry for
  `newton_shape_mapping_preflight__paper_single_box__box`;
- records `target_newton_shape_kind: box` and
  `newton_shape_support_evidence_status: pending_later_mapping_contract_no_support_claim`;
- records `mapping_attempt_count: 0`;
- records `newton_mapping_record_count: 0`;
- records `newton_runtime_execution_count: 0`;
- keeps Newton support claims, approximation policy, package generation triggers, Newton runtime
  triggers, real-USD triggers, benchmark triggers, collision-quality measurement, deployment, and
  certification claims zero or false;
- keeps `paper_faithful_offline` blockers separate from runtime-lane gates;
- advances the next gate to `paper_mapped_subset_newton_shape_mapping_contract`.

The row is intentionally a narrow static report handoff for one synthetic box artifact. It says the
row has enough report-side fields for a later shape-mapping contract; it does not say Newton has
mapped, supported, or executed it.

## Verification

Commands run during this branch after implementation:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_mapping_preflight' -q
# first focused RED before implementation: exit 1; missing payload/helper and stale next gate

PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
# first focused RED before implementation: exit 1; stale preflight missing failure label

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_mapping_preflight' -q
# exit 0; 61 passed, 689 deselected

PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
# exit 0; 3 passed, 109 deselected
```

Independent review found two stale exact-scope tests that still omitted
`paper_mapped_subset_newton_shape_mapping_preflight_contract`, plus missing negative coverage for
some preflight input-count and candidate-dict rejection paths. The stale tests and coverage gaps
were fixed before final verification.

Final verification before merge:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -q -k 'implemented_output_contract_scope or records_changed_decomposition_output_contract_gate or records_package_adapter_contract_gate or newton_shape_mapping_preflight'
# exit 0; 73 passed, 688 deselected

PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
# exit 0; 3 passed, 109 deselected

PYTHONPATH=src python scripts/validate_docs.py
# exit 0; docs validation passed

PYTHONPATH=src python scripts/validate_site_claims.py
# exit 0; site claim validation passed

git diff --check
# exit 0

PYTHONPATH=src python -m pytest -q
# exit 0; 1170 passed, 2 skipped
```

Final documentation review found no claim-boundary violation, stale current-stage name, or
contradiction between the top-level next gate and payload-specific next gate.

## Artifacts

- Report key: `paper_mapped_subset_newton_shape_mapping_preflight_contract`
- Row id: `newton_shape_mapping_preflight__paper_single_box__box`
- Closed gate: `paper_mapped_subset_newton_shape_mapping_preflight_contract`
- Next gate: `paper_mapped_subset_newton_shape_mapping_contract`
- Source fixture: `paper_single_box`
- Source primitive family: `oriented_bounding_box`
- Target mapped kind for later contract: `box`

## Claim Boundary

This record supports only the statement that the CPD paper offline report has one static,
single-fixture Newton shape-mapping preflight row for the synthetic `paper_single_box` box
artifact.

Do not cite this record as evidence for Newton readiness, Newton support, actual Newton shape
mapping, Newton runtime execution, real-USD evaluation, benchmark evidence, collision-quality
evidence, paper primitive vocabulary coverage, approximation-policy support,
`paper_faithful_offline`, full CPD reproduction, deployment readiness, safety certification, or
general package readiness.
