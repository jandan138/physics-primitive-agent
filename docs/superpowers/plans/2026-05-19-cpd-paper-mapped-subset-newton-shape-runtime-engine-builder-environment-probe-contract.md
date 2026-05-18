# CPD Paper Mapped-Subset Newton Shape Runtime Engine-Builder Environment Probe Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the report-only `paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract` gate after the existing engine-builder boundary-preflight gate.

**Architecture:** Consume exactly one boundary-preflight row for `paper_single_box`, emit one JSON-safe environment-probe row, and record Newton/Warp provenance status without crossing into `newton.ModelBuilder`, real shape calls, model finalization, collision pipeline, runtime tasks, real USD, benchmarks, or collision-quality measurement.

**Tech Stack:** Python, pytest, Markdown docs, existing `primitive_collision_compiler.baselines.cpd_paper.offline` report builders, and a bounded `importlib.util.find_spec()` provenance helper.

---

## Baseline

Start from commit `ca1dd3c`, which already includes the engine-builder boundary-preflight gate.

Run focused baseline:

```bash
PYTHONPATH=src python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cpd_paper_offline.py -k 'engine_builder_boundary_preflight or cpd_paper_offline_report_next_gate' -q
```

Expected before this plan: selected tests pass and the current next gate is
`paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract`.

## File Structure

- Modify `src/primitive_collision_compiler/newton/env.py`
  - Add a JSON-safe `inspect_newton_warp_provenance()` helper using `importlib.util.find_spec()`.
  - Restore `sys.path` and cached `newton`/`warp` modules after probing.
- Modify `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
  - Add `_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_CONTRACT`.
  - Add remaining-gap helper after the environment-probe gate.
  - Add environment-probe false/true flags.
  - Add input validation for the boundary-preflight payload and row.
  - Add environment-probe row, coverage summary, and payload helpers.
  - Wire the new payload into `build_cpd_paper_offline_report()`.
- Modify `tests/test_cpd_paper_offline.py`
  - Add expected constants, required key sets, row helper, RED tests, static boundary test, and provenance helper tests.
- Modify `tests/test_cli.py`
  - Update the offline report smoke test to expect the new next gate and payload.
- Update docs and records:
  - `README.md`
  - `docs/index.md`
  - `docs/deepdive/evidence-status.md`
  - `docs/deepdive/message-map.md`
  - `docs/reference/claim-boundaries.md`
  - `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
  - `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
  - `docs/reference/cpd-paper-reproduction-gap-matrix.md`
  - `docs/reference/cpd-paper-story-status.md`
  - `docs/records/README.md`
  - `docs/records/2026-05-19-cpd-paper-mapped-subset-newton-shape-runtime-engine-builder-environment-probe-contract.md`

## Task 1: RED Tests For The Environment-Probe Gate

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add expected constants**

```python
EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"
)
EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_CONTRACT,
]
```

- [ ] **Step 2: Add a JSON-copy input helper**

```python
def _newton_shape_runtime_engine_builder_environment_probe_input() -> dict[str, object]:
    report = build_cpd_paper_offline_report()
    return json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract"
            ]
        )
    )
```

- [ ] **Step 3: Add report-level RED test**

Create `test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract_gate`.

Assert:

```python
report["next_required_gate"] == EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_CONTRACT
payload["gate_id"] == EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_CONTRACT
payload["input_gate_id"] == EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT
payload["newton_shape_runtime_engine_builder_environment_probe_row_count"] == 1
payload["newton_model_builder_instantiated_count"] == 0
payload["newton_builder_shape_call_count"] == 0
payload["newton_runtime_execution_count"] == 0
```

- [ ] **Step 4: Add schema and row RED tests**

Add exact key-set tests for the payload and row, including:

```python
"environment_probe_contract"
"input_contract_summary"
"newton_shape_runtime_engine_builder_environment_probe_rows"
"coverage_summary"
"module_probe_rows"
"environment_probe_claim_boundary"
"newton_source_dir_configured"
"newton_source_dir"
"newton_source_dir_resolved"
"newton_module_provenance_status"
"warp_module_provenance_status"
```

- [ ] **Step 5: Add drift and boundary RED tests**

Add tests for stale input `gate_id`, stale input `next_required_gate`, source row drift, row-list
drift, false/true flag drift, and static source inspection forbidding builder/runtime calls.

- [ ] **Step 6: Run RED command**

```bash
PYTHONPATH=src python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cpd_paper_offline.py -k 'environment_probe or cpd_paper_offline_report_next_gate' -q
```

Expected: failure because the new payload helper and report key do not exist yet.

## Task 2: GREEN Environment Provenance Helper

**Files:**
- Modify: `src/primitive_collision_compiler/newton/env.py`
- Modify: `tests/test_cpd_paper_offline.py`

- [ ] **Step 1: Write helper tests**

Use temporary fake package directories for `newton` and `warp` and assert the helper records
availability/origin without importing live modules.

- [ ] **Step 2: Implement helper**

Add `inspect_newton_warp_provenance(source_dir: str | Path | None = None) -> dict[str, object]`.
The helper returns JSON-safe dict fields only and restores `sys.path` / cached modules.

- [ ] **Step 3: Run helper tests**

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_warp_provenance_helper' -q
```

Expected: helper tests pass.

## Task 3: GREEN Report Contract

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add constants and remaining-gap helper**

Add the API-surface next gate constant and:

```python
def _paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_engine_builder_environment_probe() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_CONTRACT]
```

- [ ] **Step 2: Add source-row validation**

Validate one boundary-preflight row, expected source IDs, `future_runtime_module_names == ["newton", "warp"]`,
zero builder/runtime counts, and required true/false flags.

- [ ] **Step 3: Add row and payload helpers**

Emit one environment-probe row and a coverage summary. The default no-config row uses:

```python
"environment_probe_status": "not_run_source_dir_not_configured"
"newton_source_dir_configured": False
"newton_module_provenance_status": "not_run_source_dir_not_configured"
"warp_module_provenance_status": "not_run_source_dir_not_configured"
```

- [ ] **Step 4: Wire the report**

Call the environment-probe payload helper after boundary-preflight, add it to
`implemented_output_contract_scope`, include it in the top-level report dict, and advance
`runtime_lane_remaining_gates` / `next_required_gate` to the API-surface contract.

- [ ] **Step 5: Run focused GREEN tests**

```bash
PYTHONPATH=src python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cpd_paper_offline.py -k 'environment_probe or engine_builder_boundary_preflight or cpd_paper_offline_report_next_gate' -q
```

Expected: selected tests pass.

## Task 4: Documentation And Record

**Files:**
- Modify docs listed in File Structure
- Create: `docs/records/2026-05-19-cpd-paper-mapped-subset-newton-shape-runtime-engine-builder-environment-probe-contract.md`

- [ ] **Step 1: Update claim wording**

Use only these claims:

- implemented a single-fixture bounded environment-provenance contract;
- may record Newton/Warp discoverability/provenance as environment evidence;
- no `newton.ModelBuilder`;
- no real builder shape call;
- no finalize/collide/runtime;
- no real USD, benchmark, collision-quality, deployment, safety, or full-CPD claim.

- [ ] **Step 2: Update status docs and gap matrix**

Advance references from environment-probe being next to API-surface being next, and distinguish
prior no-import gates from this bounded provenance gate.

- [ ] **Step 3: Add dated record**

Record implementation scope, verification commands, multi-agent review findings, artifacts, claim
impact, and next action.

- [ ] **Step 4: Run docs checks**

```bash
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

## Task 5: Review, Fix, Verify, Commit

**Files:**
- All modified files

- [ ] **Step 1: Multi-agent review**

Request independent runtime-boundary, docs/claim-boundary, and test/schema reviews.

- [ ] **Step 2: Fix findings**

Fix every Critical/Important finding, or document why it is invalid with concrete evidence.

- [ ] **Step 3: Run verification**

```bash
PYTHONPATH=src python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cpd_paper_offline.py -k 'environment_probe or engine_builder_boundary_preflight or cpd_paper_offline_report_next_gate' -q
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass before merge.

- [ ] **Step 4: Commit**

```bash
git add src/primitive_collision_compiler/newton/env.py src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cpd_paper_offline.py tests/test_cli.py README.md docs
git commit -m "feat: add CPD Newton engine builder environment probe"
```
