# CPD Paper Mapped-Subset Newton Shape Runtime Engine-Builder Boundary Preflight Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the offline/report-only `paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract` gate after the existing builder-construction gate.

**Architecture:** Consume exactly one builder-construction row for `paper_single_box`, validate its fake recording-builder artifact, and emit one JSON-safe boundary-preflight row that lists the checks required before a later real Newton/Warp environment probe. This gate is a checklist and lineage contract only; it does not import real Newton/Warp, instantiate `newton.ModelBuilder`, call real builder shape methods, finalize, collide, run diagnostics, load real USD, benchmark, or measure collision quality.

**Tech Stack:** Python, pytest, Markdown docs, existing `primitive_collision_compiler.baselines.cpd_paper.offline` report builders, and existing CPD paper offline contract patterns.

---

## Baseline

The branch starts from commit `8d99343`; main verification at that commit passed:

```text
PYTHONPATH=src python -m pytest -q
1664 passed in 2106.06s
```

Focused baseline in this worktree also passed:

```text
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_builder_construction or newton_shape_runtime_builder_preflight or newton_shape_runtime_construction_contract_gate' -q
243 passed, 1010 deselected in 377.47s
```

## File Structure

- Modify `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
  - Add `_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_CONTRACT`.
  - Add `_paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight()`.
  - Add engine-builder-boundary preflight false/true flags.
  - Add input validation for the builder-construction payload and row.
  - Add a preflight row helper, coverage summary helper, and payload helper.
  - Wire the new payload into `build_cpd_paper_offline_report()`.
- Modify `tests/test_cpd_paper_offline.py`
  - Add expected gate constants, remaining-gap constants, required key sets, and a JSON-copy input helper.
  - Add RED tests for top-level next gate, exact payload schema, exact row schema, false/true flags, input drift, row drift, recorded-call drift, JSON safety, and static boundary.
- Modify `tests/test_cli.py`
  - Update the offline report smoke test to expect the new next gate and the new preflight payload.
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
  - `docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-engine-builder-boundary-preflight-contract.md`

## Task 1: RED Tests For The New Gate

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add expected constants**

Add the expected environment-probe gate and update current remaining gaps to that gate:

```python
EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract"
)
EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_CONTRACT,
]
```

- [ ] **Step 2: Add a JSON-copy input helper**

```python
def _newton_shape_runtime_engine_builder_boundary_preflight_input() -> dict[str, object]:
    report = build_cpd_paper_offline_report()
    return json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_builder_construction_contract"
            ]
        )
    )
```

- [ ] **Step 3: Add report-level RED test**

Create `test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract_gate`
and assert the new payload exists, closes the preflight gate, advances `next_required_gate` to the
environment-probe gate, has one row, and keeps all real Newton counters at zero.

- [ ] **Step 4: Update CLI smoke RED expectations**

Update `test_cli_run_cpd_paper_offline_report_emits_json` to expect:

```python
payload["next_required_gate"] == (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract"
)
payload["failure_labels"] == [
    "paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract_missing",
]
```

Also assert the new payload has one preflight row and zero real Newton/runtime counters.

- [ ] **Step 5: Run RED command**

```bash
PYTHONPATH=src python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cpd_paper_offline.py -k 'engine_builder_boundary_preflight or cpd_paper_offline_report_next_gate' -q
```

Expected: failure because the new payload helper and report key do not exist yet.

## Task 2: GREEN Implementation

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add the next gate constant**

Add:

```python
_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract"
)
```

- [ ] **Step 2: Add validation helpers**

Add helpers that validate the input `gate_id`, input `next_required_gate`, one source row, source
lineage, recorded fake builder call, JSON-safety, and zero real-runtime counters.

- [ ] **Step 3: Add row and payload helpers**

Create one row with:

```python
"boundary_status": "preflight_recorded_not_crossed"
"boundary_decision": "defer_real_engine_builder_boundary_to_environment_probe_gate"
"future_newton_builder_constructor_name": "newton.ModelBuilder"
"future_newton_builder_method_name": "add_shape_box"
"future_runtime_module_names": ["newton", "warp"]
```

and the ten-item `required_before_engine_builder_boundary` checklist from the design doc.

- [ ] **Step 4: Wire the report**

Call the new payload helper after builder-construction, add it to
`implemented_output_contract_scope`, include it in the top-level report dict, and set
`runtime_lane_remaining_gates` from the new remaining-gap helper.

- [ ] **Step 5: Run GREEN command**

```bash
PYTHONPATH=src python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cpd_paper_offline.py -k 'engine_builder_boundary_preflight or cpd_paper_offline_report_next_gate' -q
```

Expected: all selected tests pass.

## Task 3: Documentation And Record

**Files:**
- Modify: docs listed above
- Create: `docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-engine-builder-boundary-preflight-contract.md`

- [ ] **Step 1: Update claim wording**

Use only these claims:

- implemented a single-fixture offline/report-only engine-builder boundary preflight record;
- no real Newton/Warp import;
- no `newton.ModelBuilder`;
- no real builder shape call;
- no finalize/collide/runtime;
- next gate is environment/provenance probe.

- [ ] **Step 2: Update status docs and gap matrix**

Advance references from builder-construction being next to environment-probe being next.

- [ ] **Step 3: Add dated record**

Record implementation scope, verification commands, artifacts, claim impact, and next action.

- [ ] **Step 4: Run docs checks**

```bash
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

## Task 4: Review, Fix, Verify, Commit

**Files:**
- All modified files

- [ ] **Step 1: Multi-agent review**

Request independent code/runtime-boundary, docs/claim-boundary, and test/schema reviews.

- [ ] **Step 2: Fix findings**

Fix every Critical/Important finding, or document why it is invalid with concrete evidence.

- [ ] **Step 3: Run focused and broad verification**

```bash
PYTHONPATH=src python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cpd_paper_offline.py -k 'engine_builder_boundary_preflight or newton_shape_runtime_builder_construction or cpd_paper_offline_report_next_gate' -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Run the full test suite before merging:

```bash
PYTHONPATH=src python -m pytest -q
```

- [ ] **Step 4: Commit, merge, push, clean up**

Commit this gate, fast-forward main, push `origin main`, and remove the temporary worktree and
feature branch.
