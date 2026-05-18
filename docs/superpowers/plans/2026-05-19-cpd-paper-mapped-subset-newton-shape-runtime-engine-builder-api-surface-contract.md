# CPD Paper Newton Engine-Builder API-Surface Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a bounded offline/source-AST API-surface contract after the existing Newton/Warp environment-probe contract.

**Architecture:** The new helper lives in `primitive_collision_compiler.newton.env` and returns JSON-safe source-inspection data without importing Newton or Warp. The CPD paper offline report consumes the existing environment-probe row, records one API-surface row, advances the next gate to an import-boundary preflight, and keeps every runtime counter at zero.

**Tech Stack:** Python, `ast`, pytest, existing `cpd_paper_offline_report` dict contracts, Markdown records.

---

### Task 1: Helper Contract Tests

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `src/primitive_collision_compiler/newton/env.py`

- [ ] **Step 1: Write failing tests**

Add tests that call `newton_env.inspect_newton_engine_builder_api_surface(None)`, a missing
source directory, and a fake Newton source tree containing `newton/__init__.py` and
`newton/_src/sim/builder.py`. Assert no import attempts, JSON-safe output, source-file status, and
signature fields.

- [ ] **Step 2: Run RED**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py::test_newton_engine_builder_api_surface_helper_records_unconfigured_source_without_import tests/test_cpd_paper_offline.py::test_newton_engine_builder_api_surface_helper_reads_source_ast_without_importing_modules -q
```

Expected: fail because the helper does not exist.

- [ ] **Step 3: Implement helper**

Implement `inspect_newton_engine_builder_api_surface()` with `pathlib`, `ast`, and existing git
commit helper reuse. Do not use `importlib.import_module()`, `ModelBuilder()`, or any Newton/Warp
imports.

- [ ] **Step 4: Run GREEN**

Run the same pytest command and expect pass.

### Task 2: Offline Report Payload

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Write failing report tests**

Add exact payload/row schema tests for
`paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract`, plus gate,
remaining-gap, false-flag, true-flag, source-row drift, and static-boundary tests.

- [ ] **Step 2: Run RED**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'api_surface or cpd_paper_offline_report_next_gate' -q
```

Expected: fail because the report payload is absent and current next gate still points at the new
gate.

- [ ] **Step 3: Implement payload**

Add the import-boundary-preflight next-gate constant, remaining-gap helper, API-surface false/true
flags, source-row validator, row builder, coverage summary, payload builder, and wire it into
`build_cpd_paper_offline_report()`.

- [ ] **Step 4: Run GREEN**

Run the same pytest command and expect pass.

### Task 3: CLI And Documentation

**Files:**
- Modify: `tests/test_cli.py`
- Modify: `README.md`
- Modify: `docs/index.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/deepdive/message-map.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/records/README.md`
- Add: `docs/records/2026-05-19-cpd-paper-mapped-subset-newton-shape-runtime-engine-builder-api-surface-contract.md`

- [ ] **Step 1: Write failing CLI expectation**

Update `test_cli_run_cpd_paper_offline_report_emits_json` to expect the new payload, the new
implemented-output scope entry, and the next gate
`paper_mapped_subset_newton_shape_runtime_engine_builder_import_boundary_preflight_contract`.

- [ ] **Step 2: Update docs**

Update current-status wording and add a dated record. Use only source-level API-surface wording and
explicitly forbid Newton readiness/runtime wording.

- [ ] **Step 3: Verify**

Run:

```bash
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
PYTHONPATH=src python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cpd_paper_offline.py -k 'api_surface or environment_probe or cpd_paper_offline_report_next_gate' -q
PYTHONPATH=src python -m pytest -q
```

Expected: all pass before merge.
