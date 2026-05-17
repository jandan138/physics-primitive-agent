# 2026-05-17 CPD Paper Mapped-Subset PrimitiveSpec Native-Fixture Serialization Contract

## Summary

Implemented `paper_mapped_subset_primitivespec_native_fixture_serialization_contract` inside
`cpd_paper_offline_report`.

This is a command-only offline report contract. It validates deterministic JSON serialization and
schema stability for exactly one report-only PrimitiveSpec-like dict from the synthetic
`paper_single_box` OBB/box native-fixture row.

## Status

Complete.

## Evidence

- Report key: `paper_mapped_subset_primitivespec_native_fixture_serialization_contract`
- Input gate: `paper_mapped_subset_primitivespec_native_fixture_generation_contract`
- Closed gate: `paper_mapped_subset_primitivespec_native_fixture_serialization_contract`
- Next gate: `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`
- Serialized report-only dict count: 1
- JSON serialization check count: 1
- JSON round-trip match count: 1
- Schema stability check count: 1
- Generated runtime PrimitiveSpecs: 0
- Generated CollisionPackages: 0
- Runtime-admissibility checks: 0

## Serialization Policy

The serialized PrimitiveSpec-like dict is checked with:

```python
json.dumps(payload, allow_nan=False, sort_keys=True, separators=(",", ":"))
```

The report records the canonical JSON string and verifies that
`json.loads(canonical_json) == serialized_payload`.

## Nonclaims

This record does not claim:

- runtime `PrimitiveSpec` object creation;
- `CollisionPackage` generation;
- Newton runtime support;
- runtime admissibility;
- real-USD evidence;
- benchmark evidence;
- collision-quality validation;
- deployment readiness;
- safety certification;
- full CPD paper reproduction;
- `paper_faithful_offline` support.

## Follow-Up

The next gate is `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`.
That gate should remain a preflight boundary unless a later dated record actually creates and
verifies a runtime object.
