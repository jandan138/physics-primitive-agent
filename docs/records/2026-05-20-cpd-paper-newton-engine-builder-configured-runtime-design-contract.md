# 2026-05-20 CPD Paper Newton Engine-Builder Configured-Runtime Design Contract

## Date

2026-05-20

## Status

Implementation, focused schema hardening, documentation sync, final multi-agent review, and
full-regression verification are complete. Merge, push, and worktree cleanup remain pending.

## Summary

This record documents the
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract` slice
inside `cpd_paper_offline_report`.

The slice consumes the report-only engine-builder runtime-lane review row for the synthetic
`paper_single_box` OBB/box lineage and records a report-only configured-runtime input design:
`configured_runtime_design_decision: define_configured_runtime_inputs_keep_real_runtime_blocked`.
It advances the current next gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract`.

This is not runtime config validation. It records required inputs for a later preflight gate while
keeping real Newton/Warp imports, `newton.ModelBuilder`, real builder calls, model finalization,
collision pipeline calls, Newton runtime execution, real USD, benchmarks, and collision-quality
evidence at zero or false.

## Scope

Implemented:

- one synthetic fixture: `paper_single_box`;
- one mapped Newton-native shape kind: `box`;
- one configured-runtime design row linked to the runtime-lane review row;
- required runtime inputs for runtime source, runtime device, entry decision, smoke policy,
  execution policy, and runtime-lane review decision;
- exact input runtime-lane review payload and source-row key validation, including missing-key and
  unexpected-key drift checks;
- source-package copy rejection at payload and row scope;
- static boundary checks for no real runtime import, no config/env read, no model builder, no
  shape call, no finalization, no runtime execution, no benchmark, and no collision-quality path;
- zero runtime config validation count and zero preflight-ready count;
- exact zero counters for real Newton/Warp imports, `newton.ModelBuilder`, Newton engine shape
  objects, real builder calls, model finalization, collision pipeline creation/collide calls,
  Newton runtime execution, real USD, benchmarks, and collision-quality evidence.

Not implemented:

- runtime config file or environment validation;
- runtime source resolution;
- runtime device resolution;
- real Newton runtime import;
- `newton.ModelBuilder` instantiation;
- real `add_shape_box` calls;
- Newton engine shape objects;
- model finalization;
- collision pipeline creation or collision;
- contact, drop/settle, or sphere-rain task execution from this report path;
- runtime compatibility validation;
- real-USD evaluation;
- benchmark or collision-quality measurement;
- full CPD paper reproduction or `paper_faithful_offline` support.

## Claim Boundary

Allowed wording:

- The report records a bounded configured-runtime input design for one synthetic mapped-subset
  `box` fixture.
- The design contract defines required runtime inputs for a later configured-runtime preflight gate.
- Runtime config validation remains false and real runtime work remains blocked.
- The next runtime-lane gate is the configured-runtime preflight contract.

Forbidden wording:

- Newton support is implemented.
- A runtime config was validated.
- Newton runtime compatibility is validated.
- Real Newton builder calls were validated.
- A Newton engine shape object was created.
- Newton runtime execution ran or passed.
- The package is simulation-checked by this report path.
- Collision quality is measured.
- The work reproduces the full CPD paper.
- The artifact is ready for real USD, benchmarks, deployment, or safety certification.

## Verification

Baseline before this slice:

```bash
python -m pytest -q
```

Observed result: `2259 passed, 2 skipped in 2961.53s (0:49:21)`.

Focused RED before Task 1 implementation:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_gate -q
```

Observed result before implementation: failed with a missing configured-runtime design payload.

Focused GREEN after Task 1 implementation:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_gate tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_gate tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Observed result: `3 passed in 7.17s`.

Review follow-up after Task 1:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_changed_decomposition_output_contract_gate tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_package_adapter_contract_gate -p no:cacheprovider
```

Observed result after syncing two legacy full-list expectations: `2 passed`.

Focused RED before Task 2 hardening:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_design" -q
```

Observed result before hardening: `28 failed, 7 passed, 1850 deselected in 60.98s (0:01:00)`.

Focused GREEN after schema, drift, source-copy, and static-boundary hardening:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_design" -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
git diff --check
```

Observed results: `35 passed, 1850 deselected in 54.91s`; `1 passed in 1.99s`; whitespace check
passed.

Targeted schema/static verification after review follow-up:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_design_payload_schema_is_exact tests/test_cpd_paper_offline.py::test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_design_static_boundary_is_report_only -q
```

Observed result: `2 passed in 1.92s`.

Task 3 documentation checks:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Observed results: docs validation passed; site claim validation passed; whitespace check passed.

Focused Task 3 recheck after documentation sync:

```bash
python -m pytest tests/test_cpd_paper_offline.py -k "configured_runtime_design" -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Observed results: `35 passed, 1850 deselected in 54.19s`; `1 passed in 1.91s`.

Task 3 review follow-up after claim-boundary findings:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Observed results after replacing stale current-gate wording, narrowing Newton primitive wording,
and extending the report-scoped preservation list: docs validation passed; site claim validation
passed; whitespace check passed.

Final verification after final multi-agent review:

```bash
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Observed results: `2294 passed, 2 skipped in 3099.97s (0:51:39)`; docs validation passed; site
claim validation passed; whitespace check passed.

## Multi-Agent Review

Task 1 implementation review:

- one reviewer approved the implementation and zero-counter boundary;
- one reviewer found two stale `implemented_output_contract_scope` expectations that still ended
  at the runtime-lane review gate; both expectations were updated to include the configured-runtime
  design contract.

Task 2 hardening review:

- one reviewer approved the claim-boundary wording and zero-runtime evidence boundary;
- one reviewer found that the static-boundary test claimed `no_config_read` but did not block
  config or environment reads. The finding was accepted, and the static-boundary test now rejects
  file/config/env read paths such as `open`, `Path.read_text`, YAML/TOML/config parser reads, and
  `os.environ`.

Task 3 documentation review:

- one reviewer approved the record/index/link consistency with no findings, while noting that the
  new dated record must be included in the eventual docs commit;
- one reviewer found stale README current-gate wording that described the runtime-lane review as
  advancing the current gate to configured-runtime design. The wording now describes that as the
  stage-local gate at that earlier stage;
- the same reviewer found over-strong primitive "support" wording in the gap matrix and story
  status. The wording now uses diagnostic mapping/construction coverage instead of Newton support;
- the same reviewer found that the preservation list omitted the runtime-lane review row and
  configured-runtime design row. The list now includes both and keeps them report-scoped until a
  configured-runtime preflight and later reviewed Newton runtime gate allow broader runtime work.
- the claim-boundary reviewer re-reviewed those fixes and approved them, including the interim
  dated record update that kept final full-regression verification pending at that stage.

Final review:

- one code/schema reviewer approved the configured-runtime design implementation with no findings
  after inspecting the code/test diff and running targeted schema, CLI, next-gate, real-runtime
  counter, docs, and whitespace probes;
- one docs/claim reviewer approved the final documentation and claim-boundary diff with no
  findings, noting that historical Newton diagnostic-smoke and mapping wording remains bounded as
  dated diagnostic evidence and is not used as configured-runtime support.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `README.md`
- `docs/index.md`
- `docs/deepdive/message-map.md`
- `docs/deepdive/evidence-status.md`
- `docs/reference/claim-boundaries.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/superpowers/specs/2026-05-20-cpd-paper-newton-engine-builder-configured-runtime-design-contract-design.md`
- `docs/superpowers/plans/2026-05-20-cpd-paper-newton-engine-builder-configured-runtime-design-contract.md`

## Next Action

Keep the next implementation slice focused on
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract`. Do
not use the configured-runtime design row as Newton support, simulation-checked evidence,
benchmark evidence, runtime compatibility evidence, runtime config validation evidence, or
collision-quality evidence.
