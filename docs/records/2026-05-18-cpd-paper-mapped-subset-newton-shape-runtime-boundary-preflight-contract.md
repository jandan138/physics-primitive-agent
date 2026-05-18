# CPD Paper Mapped-Subset Newton Shape Runtime-Boundary Preflight Contract

Date: 2026-05-18

## Summary

Implemented the single-fixture offline/static
`paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract` in
`cpd_paper_offline_report`.

This gate consumes the existing
`paper_mapped_subset_newton_shape_mapping_contract` descriptor row for the deterministic synthetic
`paper_single_box` OBB/box artifact and records exactly one later Newton shape runtime-construction
candidate.

## Boundary

This record is report-only evidence. It does not import Newton, call the shape mapper, construct a
Newton shape object, run Newton, load real USD assets, run benchmarks, measure collision quality,
claim Newton support, claim package readiness, claim `paper_faithful_offline`, or claim full CPD
paper reproduction.

The new payload keeps:

- `mapping_attempt_count: 0`
- `newton_mapping_record_count: 0`
- `newton_shape_object_count: 0`
- `newton_runtime_execution_count: 0`
- `paper_faithful_offline_supported: false`
- `newton_support_claimed: false`
- `newton_runtime_triggered: false`
- `real_usd_triggered: false`
- `benchmark_triggered: false`
- `collision_quality_measured: false`

## Evidence

Focused RED before implementation failed on the missing runtime-boundary preflight payload/helper
and stale top-level next gate, as expected.

Focused GREEN after implementation:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_boundary_preflight' -q
```

Result: `71 passed, 819 deselected`.

```bash
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Result: `3 passed, 109 deselected`.

Post-review fixes updated stale top-level remaining-gate/list expectations, expanded negative
coverage for upstream count drift, source-row lineage drift, descriptor lineage and numeric drift,
forbidden package-copy placement, static boundary coverage, and tightened stale documentation
wording.

Focused GREEN after review fixes:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_boundary_preflight or records_mapped_subset_runtime_admissibility_contract_gate or records_mapped_subset_newton_shape_mapping_preflight_gate or records_mapped_subset_newton_shape_mapping_contract_gate' -q
```

Result: `99 passed, 816 deselected`.

```bash
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
```

Result: `3 passed, 109 deselected`.

```bash
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Result: docs validation passed, site claim validation passed, and whitespace check exited 0.

Broader offline report verification:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -q -x
```

Result: `915 passed in 1573.17s`.

Full suite verification:

```bash
PYTHONPATH=src python -m pytest -q
```

Result: `1324 passed, 2 skipped in 1575.10s`.

## Next Gate

The top-level runtime-lane next gate is now
`paper_mapped_subset_newton_shape_runtime_construction_contract`.

That next gate still must preserve the claim boundary unless a separate dated record proves a
narrower executable scope.
