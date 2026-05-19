# 2026-05-19 CPD Paper Newton Engine-Builder Gate Consolidation

## Summary

This record documents the anti-overdesign decision for the CPD paper mapped-subset Newton
engine-builder lane.

The recent Newton engine-builder work closed three useful report-only slices:

- `paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract`;
- `paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract`;
- `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract`.

Those records remain useful because they preserve the provenance trail from a synthetic
`CollisionPackage.to_dict()` artifact to a future `newton.ModelBuilder` / `add_shape_box`
boundary. However, continuing with separate
`import-boundary-preflight -> import-contract` gates would split the same boundary facts across
too many small records. The audit value would rise slowly while maintenance and review cost would
rise quickly.

The current next runtime-lane gate is consolidated to:

```text
paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract
```

## Decision

Do not add separate top-level gates for:

- a standalone Newton engine-builder import-boundary preflight;
- a standalone Newton engine-builder import contract.

Use one coarse engine-builder entry contract instead. That future contract should bundle the
remaining meaningful boundary questions:

- whether the explicit Newton source/environment inputs are present and reviewable;
- whether the package, PrimitiveSpec, shape-mapping, builder-plan, boundary-preflight,
  environment-probe, and API-surface rows line up for the same synthetic `paper_single_box`
  OBB/box fixture;
- whether the lane is allowed to cross from offline/static provenance into a real Newton import
  boundary in a later implementation step;
- what the next post-entry gate is if and only if the entry boundary is justified.

Until that contract is implemented and recorded, the report must remain partial.

## What Stays

Keep the already implemented engine-builder evidence:

- boundary-preflight row: future `newton.ModelBuilder` / `add_shape_box` checklist only;
- environment-probe row: JSON-safe configured-source and `find_spec` provenance only;
- API-surface row: source-file / AST inspection only.

These records are not runtime support. They only explain what would need to be true before a
future Newton boundary crossing is attempted.

## What Changes

The report, CLI JSON, tests, and live docs now advance from the API-surface gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract`.

The old planned import-boundary-preflight name is retired from current code and current live
claim docs. Historical implementation records may still explain the API-surface step, but their
current-next wording now points at the consolidated entry contract.

## Claim Boundary

Allowed wording:

- The current next gate is a consolidated Newton engine-builder entry contract.
- The consolidation reduces future gate count by combining import-boundary preconditions and the
  first entry decision into one audit point.
- The already closed engine-builder slices are offline/static or source-inspection evidence only.

Forbidden wording:

- Newton support is implemented.
- Newton runtime compatibility is validated.
- Real Newton builder calls were validated.
- A Newton engine shape object was created.
- The package is simulation-checked.
- The work reproduces the full CPD paper.
- Collision quality, benchmark quality, deployment readiness, or safety certification is shown.

## Review Follow-Up

Multi-agent review found two wording issues before final verification:

- a historical worker plan still told future agents to add an `import-boundary-preflight`
  next-gate constant;
- one story-status bullet used an ambiguous unsupported-import qualifier, which weakened the
  intended no-real-import boundary.

Both were corrected. Current worker-facing and claim-boundary wording now says the next gate is
the consolidated engine-builder entry contract and keeps `no real import` inside this slice.

## Verification

Focused verification after consolidation:

```bash
python -m py_compile \
  src/primitive_collision_compiler/baselines/cpd_paper/offline.py \
  tests/test_cpd_paper_offline.py \
  tests/test_cli.py

python -m pytest \
  tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract_gate \
  tests/test_cpd_paper_offline.py::test_cpd_paper_newton_shape_runtime_engine_builder_api_surface_payload_schema_is_exact \
  -q

python -m pytest \
  tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json \
  -q
```

Result: passed.

Additional pre-merge verification:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "api_surface or engine_builder or cpd_paper_offline_report_next_gate" -q
```

Result: 479 passed, 1254 deselected.

```bash
python -m pytest tests/test_cli.py -k "cpd_paper_offline" -q
```

Result: 3 passed, 109 deselected.

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Result: passed.

```bash
python -m pytest -q
```

Result: 2142 passed, 2 skipped.
