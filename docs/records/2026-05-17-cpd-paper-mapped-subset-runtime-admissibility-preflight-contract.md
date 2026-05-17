# 2026-05-17 CPD Paper Mapped-Subset Runtime-Admissibility Preflight Contract

## Date

2026-05-17

## Status

Complete.

## Context

The previous gate, `paper_mapped_subset_collision_package_generation_contract`, constructed exactly
one synthetic, report-scoped `CollisionPackage.to_dict()` artifact for the deterministic
`paper_single_box` OBB/box row. That package artifact deliberately kept
`runtime_admissibility_check_count: 0`, marked its status as
`offline_synthetic_candidate_runtime_admissibility_not_checked`, and did not run Newton.

That previous gate pointed next to:

`paper_mapped_subset_runtime_admissibility_preflight_contract`

This record covers only that next single-fixture offline preflight contract. It does not cover the
later runtime-admissibility check itself.

## What Changed

The partial `cpd_paper_offline_report` now includes
`paper_mapped_subset_runtime_admissibility_preflight_contract`.

The new payload:

- consumes `paper_mapped_subset_collision_package_generation_contract`;
- validates the input gate id, expected next gate, one source row, and expected source counts;
- validates the source row identity and lineage fields for the one deterministic
  `paper_single_box` OBB/box source row before copying any source-row fields into the new
  preflight row;
- anchors the expected source row and expected package primitive payload to the canonical
  `paper_single_box` generation row, so coupled source-row and package primitive drift cannot
  redefine the candidate shape by changing both input copies together;
- validates that the source package artifact has the exact expected package schema, package id,
  asset id, source path, source SHA-256, method, stage, status, claim boundary, primitive subset,
  unsupported primitive list, and primitive payload;
- rejects extra copied package dicts in the input so the preflight payload does not silently depend
  on duplicated package artifacts;
- records exactly one `runtime_admissibility_preflight_rows` entry for
  `paper_single_box`;
- records package lineage fields such as `source_package_id`, `source_package_source_path`,
  `source_package_source_sha256`, `source_package_primitive_count`, and
  `source_package_primitive_subset`;
- deliberately does not copy the full `generated_collision_package` dict into the new preflight
  payload;
- records `later_runtime_admissibility_candidate_count: 1`;
- keeps `runtime_admissibility_check_count: 0`;
- keeps `paper_faithful_offline_allowed: false` and `paper_faithful_offline_supported: false`;
- keeps package, Newton, real-USD, benchmark, collision-quality, deployment, and certification
  triggers false;
- advances the next gate to `paper_mapped_subset_runtime_admissibility_contract`.

The preflight row is intentionally just a narrow handoff record. It says there is one bounded
package artifact eligible for the later runtime-admissibility gate; it does not say that the
package is runtime-admissible.

## Verification

Commands run during this branch after the implementation:

```bash
python -m py_compile src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cpd_paper_offline.py tests/test_cli.py tests/test_cpd_paper_importer.py
# exit 0

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'changed_decomposition_output_contract_gate or package_adapter_contract_gate or collision_package_generation_preflight_contract_gate' -q
# exit 0; 3 passed, 611 deselected

PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
# exit 0; 3 passed, 109 deselected

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_admissibility_preflight or collision_package_generation_contract' -q
# exit 0; 165 passed, 450 deselected

PYTHONPATH=src python scripts/validate_docs.py
# exit 0; docs validation passed

PYTHONPATH=src python scripts/validate_site_claims.py
# exit 0; site claim validation passed

git diff --check
# exit 0

PYTHONPATH=src python -m pytest -q
# exit 0; 1024 passed, 2 skipped
```

The focused RED run before implementation failed as expected because the report lacked the new
preflight payload, runtime-admissibility next gate, preflight row, input package validation, and
static boundary coverage.

## Artifacts

- Report key: `paper_mapped_subset_runtime_admissibility_preflight_contract`
- Previous report gate: `paper_mapped_subset_collision_package_generation_contract`
- Next report gate: `paper_mapped_subset_runtime_admissibility_contract`
- Preflight row id: `runtime_admissibility_preflight__paper_single_box__box`
- Source package id:
  `paper_single_box:paper_mapped_subset_collision_package_generation_contract`
- Implementation plan:
  `docs/superpowers/plans/2026-05-17-cpd-paper-mapped-subset-runtime-admissibility-preflight-contract.md`
- Design spec:
  `docs/superpowers/specs/2026-05-17-cpd-paper-mapped-subset-runtime-admissibility-preflight-contract-design.md`

## Claim Boundary

Supported:

- partial single-fixture offline runtime-admissibility preflight accounting for one deterministic
  synthetic fixture;
- validation that the source `paper_single_box` package artifact matches the expected report
  identity, schema, source metadata, primitive subset, and claim boundary;
- validation that source row identity fields still describe the same `paper_single_box` OBB/box
  row before the preflight row copies them forward;
- exactly one later runtime-admissibility candidate row;
- explicit accounting that runtime-admissibility checks, Newton runtime, real-USD loading,
  benchmark runs, collision-quality measurement, deployment, and certification triggers remain
  zero or false;
- explicit accounting that the preflight payload stores lineage fields and does not copy the full
  generated package dict.

Not supported:

- package readiness;
- runtime admissibility;
- Newton support or Newton execution;
- real-USD evidence;
- benchmark evidence;
- collision-quality evidence;
- paper primitive vocabulary coverage;
- `paper_faithful_offline` support;
- full CPD reproduction;
- deployment readiness or safety certification.

## Claim Impact

This record supports only a partial, single-fixture offline preflight claim for one deterministic
synthetic `paper_single_box` OBB/box fixture. It moves the CPD paper lane from "one bounded package
dict exists for review" to "one bounded package dict has a recorded handoff row for a later
runtime-admissibility gate".

It does not make that package runtime-admissible and does not add Newton evidence.

## Next Gate

`paper_mapped_subset_runtime_admissibility_contract`

That next gate must decide what the one report-scoped package artifact must check before any
runtime admissibility or Newton-related support is claimed.

## Next Action

- Implement `paper_mapped_subset_runtime_admissibility_contract` under a separate dated record
  before claiming runtime admissibility, Newton runtime support, or broader package readiness.
