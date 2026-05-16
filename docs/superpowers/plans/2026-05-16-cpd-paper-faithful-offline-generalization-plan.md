# CPD Paper Faithful Offline Generalization Plan Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a command-only planning payload that closes the `paper_faithful_offline_generalization_plan` gate and splits the remaining offline paper-lane generalization work into explicit next slices.

**Architecture:** The report remains in `src/primitive_collision_compiler/baselines/cpd_paper/offline.py` and stays `partial`. The new payload is a planning table only: it names the future offline generalization slices, advances the top-level next gate to the first source-policy slice, and keeps package generation, Newton runtime, real USD, and benchmark work blocked.

**Tech Stack:** Python 3.10+, NumPy, pytest, existing `npc-compile` CLI surface.

---

## File Structure

- Modify `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`:
  add `_paper_faithful_offline_generalization_plan_payload()` and wire it into
  `build_cpd_paper_offline_report()`.
- Modify `tests/test_cpd_paper_offline.py`:
  add RED tests for the new planning payload and update existing top-level gate expectations.
- Modify `tests/test_cli.py`:
  assert the CLI JSON exposes the new planning payload and first implementation gate.
- Modify documentation:
  `README.md`, `docs/index.md`, `docs/deepdive/evidence-status.md`,
  `docs/reference/claim-boundaries.md`,
  `docs/reference/cpd-paper-reproduction-gap-matrix.md`,
  `docs/reference/cpd-paper-faithful-offline-lane-spec.md`,
  `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`,
  `docs/reference/cpd-paper-story-status.md`, and `docs/records/README.md`.
- Modify `experiments/registry.yaml`:
  add a complete registry entry for the generalization-plan gate.
- Create `docs/records/2026-05-16-cpd-paper-faithful-offline-generalization-plan.md`:
  record RED/GREEN verification, CLI smoke, full verification, review notes, and claim impact.

## Claim Boundary

This slice may support only:

```text
The command-only synthetic CPD paper offline lane has a planning table for offline generalization
beyond named toy fixtures, and the report remains partial.
```

It must not support:

- `paper_faithful_offline`;
- full CPD paper reproduction;
- package generation;
- Newton runtime execution;
- real-USD evidence;
- benchmark or collision-quality evidence;
- deployment readiness or safety certification.

## Task 1: RED Tests For The Generalization Plan

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add the focused offline report test**

Append this test near
`test_cpd_paper_offline_report_records_fixture_breadth_completion_review` in
`tests/test_cpd_paper_offline.py`:

```python
def test_cpd_paper_offline_report_records_generalization_plan_gate():
    report = build_cpd_paper_offline_report()
    expected_missing = [
        "paper_generalization_batch_a_source_policy",
        "paper_generalization_batch_b_primitive_fit_engine",
        "paper_generalization_batch_c_search_engine",
        "paper_generalization_batch_d_postprocess_policy",
        "paper_generalization_batch_e_package_boundary_readiness",
    ]

    assert report["failure_labels"] == [
        f"{gate}_missing" for gate in expected_missing
    ]
    assert report["next_required_gate"] == "paper_generalization_batch_a_source_policy"
    assert report["paper_faithfulness"]["missing_before_paper_faithful_offline"] == expected_missing
    assert "paper_faithful_offline_generalization_plan" not in report[
        "paper_faithfulness"
    ]["implemented_fixture_scope"]
    assert "paper_faithful_offline_generalization_plan" in report[
        "paper_faithfulness"
    ]["implemented_planning_scope"]

    plan = report["paper_faithful_offline_generalization_plan"]
    assert plan["plan_scope"] == "offline_algorithm_generalization_beyond_named_toy_fixtures"
    assert plan["closed_gate"] == "paper_faithful_offline_generalization_plan"
    assert plan["decision"] == "remain_partial"
    assert plan["decision_reason"] == "generalization_plan_complete_first_source_policy_slice_missing"
    assert plan["generalization_plan_complete"] is True
    assert plan["paper_faithful_offline_allowed"] is False
    assert plan["next_required_gate"] == "paper_generalization_batch_a_source_policy"
    assert plan["package_generation_triggered"] is False
    assert plan["newton_runtime_triggered"] is False
    assert plan["real_usd_triggered"] is False
    assert plan["benchmark_triggered"] is False

    expected_batches = [
        {
            "batch_id": "paper_generalization_batch_a_source_policy",
            "purpose": "generalize_source_mesh_preprocess_intake_operator_policy",
            "primary_criteria": [
                "source_mesh_and_preprocessing_policy",
                "source_face_intake_policy",
                "operator_q_audit",
            ],
            "implementation_boundary": "offline_report_only_no_package_or_newton",
            "required_output": "source_policy_generalization_report",
        },
        {
            "batch_id": "paper_generalization_batch_b_primitive_fit_engine",
            "purpose": "generalize_paper_primitive_fit_engine_beyond_named_cases",
            "primary_criteria": [
                "primitive_vocabulary_and_fit",
            ],
            "implementation_boundary": "offline_report_only_no_package_or_newton",
            "required_output": "primitive_fit_engine_generalization_report",
        },
        {
            "batch_id": "paper_generalization_batch_c_search_engine",
            "purpose": "generalize_cost_queue_threshold_and_component_pair_search",
            "primary_criteria": [
                "paper_collapse_cost_and_weighting",
                "greedy_priority_queue_trace",
                "target_count_and_threshold_stop",
                "component_pair_edge_handling",
            ],
            "implementation_boundary": "offline_report_only_no_package_or_newton",
            "required_output": "search_engine_generalization_report",
        },
        {
            "batch_id": "paper_generalization_batch_d_postprocess_policy",
            "purpose": "generalize_enclosed_primitive_postprocess_policy",
            "primary_criteria": [
                "enclosed_primitive_postprocess",
            ],
            "implementation_boundary": "offline_report_only_no_package_or_newton",
            "required_output": "postprocess_policy_generalization_report",
        },
        {
            "batch_id": "paper_generalization_batch_e_package_boundary_readiness",
            "purpose": "review_offline_package_boundary_readiness_after_changed_decomposition",
            "primary_criteria": [
                "package_generation_boundary",
                "newton_runtime_boundary",
                "real_usd_boundary",
                "benchmark_evaluation_boundary",
            ],
            "implementation_boundary": "planning_only_no_package_or_newton",
            "required_output": "package_boundary_readiness_review",
        },
    ]
    assert plan["planned_batches"] == expected_batches
    assert plan["first_unresolved_gate"] == "paper_generalization_batch_a_source_policy"
    assert plan["remaining_generalization_gates"] == expected_missing
    assert plan["blocked_runtime_gates"] == [
        "package_generation_boundary",
        "newton_runtime_boundary",
        "real_usd_boundary",
        "benchmark_evaluation_boundary",
    ]
```

- [ ] **Step 2: Update existing top-level gate tests**

Rename and change
`test_cpd_paper_offline_report_failure_labels_point_to_generalization_gap`:

```python
def test_cpd_paper_offline_report_failure_labels_point_to_source_policy_gap():
    report = build_cpd_paper_offline_report()

    assert report["failure_labels"] == [
        "paper_generalization_batch_a_source_policy_missing",
        "paper_generalization_batch_b_primitive_fit_engine_missing",
        "paper_generalization_batch_c_search_engine_missing",
        "paper_generalization_batch_d_postprocess_policy_missing",
        "paper_generalization_batch_e_package_boundary_readiness_missing",
    ]
```

Rename and change `test_cpd_paper_offline_report_next_gate_is_generalization_plan`:

```python
def test_cpd_paper_offline_report_next_gate_is_source_policy_generalization():
    report = build_cpd_paper_offline_report()

    assert report["next_required_gate"] == "paper_generalization_batch_a_source_policy"
```

In `test_cpd_paper_offline_report_covers_first_toy_slice`, change the top-level assertions:

```python
assert report["failure_labels"] == [
    "paper_generalization_batch_a_source_policy_missing",
    "paper_generalization_batch_b_primitive_fit_engine_missing",
    "paper_generalization_batch_c_search_engine_missing",
    "paper_generalization_batch_d_postprocess_policy_missing",
    "paper_generalization_batch_e_package_boundary_readiness_missing",
]
assert report["next_required_gate"] == "paper_generalization_batch_a_source_policy"
assert report["paper_faithfulness"]["missing_before_paper_faithful_offline"] == [
    "paper_generalization_batch_a_source_policy",
    "paper_generalization_batch_b_primitive_fit_engine",
    "paper_generalization_batch_c_search_engine",
    "paper_generalization_batch_d_postprocess_policy",
    "paper_generalization_batch_e_package_boundary_readiness",
]
assert "paper_faithful_offline_generalization_plan" not in report["paper_faithfulness"][
    "implemented_fixture_scope"
]
assert "paper_faithful_offline_generalization_plan" in report["paper_faithfulness"][
    "implemented_planning_scope"
]
```

Also update
`test_cpd_paper_offline_report_records_fixture_breadth_completion_review` so its top-level
assertions match the same five `failure_labels`, the same
`missing_before_paper_faithful_offline` list, and the same top-level
`next_required_gate: "paper_generalization_batch_a_source_policy"`. Keep the nested
`paper_fixture_breadth_completion_review["next_required_gate"]` assertion unchanged at
`"paper_faithful_offline_generalization_plan"` because that payload describes the previous closed
gate.

Add this constant near `EXPECTED_SCOPE_AUDIT_ROWS` and use it for every blocking scope-audit row's
`next_action` in `tests/test_cpd_paper_offline.py`:

```python
EXPECTED_GENERALIZATION_SOURCE_POLICY_NEXT_ACTION = (
    "Proceed to paper_generalization_batch_a_source_policy as the first offline "
    "generalization slice before stronger wording."
)
```

For each blocking scope-audit row in `EXPECTED_SCOPE_AUDIT_ROWS`, set:

```python
"next_action": EXPECTED_GENERALIZATION_SOURCE_POLICY_NEXT_ACTION,
```

- [ ] **Step 3: Update the CLI test**

In `tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json`, change the top-level
gate assertions and add plan assertions:

```python
assert payload["failure_labels"] == [
    "paper_generalization_batch_a_source_policy_missing",
    "paper_generalization_batch_b_primitive_fit_engine_missing",
    "paper_generalization_batch_c_search_engine_missing",
    "paper_generalization_batch_d_postprocess_policy_missing",
    "paper_generalization_batch_e_package_boundary_readiness_missing",
]
assert payload["next_required_gate"] == "paper_generalization_batch_a_source_policy"
plan = payload["paper_faithful_offline_generalization_plan"]
assert plan["closed_gate"] == "paper_faithful_offline_generalization_plan"
assert plan["generalization_plan_complete"] is True
assert plan["paper_faithful_offline_allowed"] is False
assert plan["next_required_gate"] == "paper_generalization_batch_a_source_policy"
assert [batch["batch_id"] for batch in plan["planned_batches"]] == [
    "paper_generalization_batch_a_source_policy",
    "paper_generalization_batch_b_primitive_fit_engine",
    "paper_generalization_batch_c_search_engine",
    "paper_generalization_batch_d_postprocess_policy",
    "paper_generalization_batch_e_package_boundary_readiness",
]
assert plan["package_generation_triggered"] is False
assert plan["newton_runtime_triggered"] is False
assert plan["real_usd_triggered"] is False
assert plan["benchmark_triggered"] is False
```

- [ ] **Step 4: Run RED tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_generalization_plan_gate tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_failure_labels_point_to_source_policy_gap tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_source_policy_generalization tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_completion_review -q
```

Expected: FAIL because the report still emits
`paper_faithful_offline_generalization_missing`, still points to
`paper_faithful_offline_generalization_plan`, and lacks the
`paper_faithful_offline_generalization_plan` payload.

## Task 2: Implement The Generalization-Plan Payload

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add the planned batch helper**

Add this helper near `_paper_fixture_breadth_completion_review_payload()`:

```python
def _paper_faithful_offline_generalization_batches() -> list[dict[str, object]]:
    return [
        {
            "batch_id": "paper_generalization_batch_a_source_policy",
            "purpose": "generalize_source_mesh_preprocess_intake_operator_policy",
            "primary_criteria": [
                "source_mesh_and_preprocessing_policy",
                "source_face_intake_policy",
                "operator_q_audit",
            ],
            "implementation_boundary": "offline_report_only_no_package_or_newton",
            "required_output": "source_policy_generalization_report",
        },
        {
            "batch_id": "paper_generalization_batch_b_primitive_fit_engine",
            "purpose": "generalize_paper_primitive_fit_engine_beyond_named_cases",
            "primary_criteria": [
                "primitive_vocabulary_and_fit",
            ],
            "implementation_boundary": "offline_report_only_no_package_or_newton",
            "required_output": "primitive_fit_engine_generalization_report",
        },
        {
            "batch_id": "paper_generalization_batch_c_search_engine",
            "purpose": "generalize_cost_queue_threshold_and_component_pair_search",
            "primary_criteria": [
                "paper_collapse_cost_and_weighting",
                "greedy_priority_queue_trace",
                "target_count_and_threshold_stop",
                "component_pair_edge_handling",
            ],
            "implementation_boundary": "offline_report_only_no_package_or_newton",
            "required_output": "search_engine_generalization_report",
        },
        {
            "batch_id": "paper_generalization_batch_d_postprocess_policy",
            "purpose": "generalize_enclosed_primitive_postprocess_policy",
            "primary_criteria": [
                "enclosed_primitive_postprocess",
            ],
            "implementation_boundary": "offline_report_only_no_package_or_newton",
            "required_output": "postprocess_policy_generalization_report",
        },
        {
            "batch_id": "paper_generalization_batch_e_package_boundary_readiness",
            "purpose": "review_offline_package_boundary_readiness_after_changed_decomposition",
            "primary_criteria": [
                "package_generation_boundary",
                "newton_runtime_boundary",
                "real_usd_boundary",
                "benchmark_evaluation_boundary",
            ],
            "implementation_boundary": "planning_only_no_package_or_newton",
            "required_output": "package_boundary_readiness_review",
        },
    ]
```

- [ ] **Step 2: Add the payload helper**

Add this helper after the batch helper:

```python
def _paper_faithful_offline_generalization_plan_payload() -> dict[str, object]:
    planned_batches = _paper_faithful_offline_generalization_batches()
    return {
        "plan_scope": "offline_algorithm_generalization_beyond_named_toy_fixtures",
        "closed_gate": "paper_faithful_offline_generalization_plan",
        "decision": "remain_partial",
        "decision_reason": "generalization_plan_complete_first_source_policy_slice_missing",
        "generalization_plan_complete": True,
        "paper_faithful_offline_allowed": False,
        "next_required_gate": "paper_generalization_batch_a_source_policy",
        "first_unresolved_gate": "paper_generalization_batch_a_source_policy",
        "planned_batches": planned_batches,
        "remaining_generalization_gates": [
            str(batch["batch_id"]) for batch in planned_batches
        ],
        "blocked_runtime_gates": [
            "package_generation_boundary",
            "newton_runtime_boundary",
            "real_usd_boundary",
            "benchmark_evaluation_boundary",
        ],
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }
```

- [ ] **Step 3: Wire the helper into `build_cpd_paper_offline_report()`**

Change `missing_before_paper_faithful`:

```python
missing_before_paper_faithful = [
    "paper_generalization_batch_a_source_policy",
    "paper_generalization_batch_b_primitive_fit_engine",
    "paper_generalization_batch_c_search_engine",
    "paper_generalization_batch_d_postprocess_policy",
    "paper_generalization_batch_e_package_boundary_readiness",
]
```

Change `next_required_gate`:

```python
"next_required_gate": "paper_generalization_batch_a_source_policy",
```

Add the planning scope field inside `paper_faithfulness`, separate from
`implemented_fixture_scope`:

```python
"implemented_planning_scope": [
    "paper_faithful_offline_generalization_plan",
],
```

Do not add `paper_faithful_offline_generalization_plan` to `implemented_fixture_scope`.

Add the top-level report payload:

```python
"paper_faithful_offline_generalization_plan": (
    _paper_faithful_offline_generalization_plan_payload()
),
```

- [ ] **Step 4: Update scope-audit next-action source strings**

Add this constant near the top of
`src/primitive_collision_compiler/baselines/cpd_paper/offline.py`:

```python
_PAPER_GENERALIZATION_SOURCE_POLICY_NEXT_ACTION = (
    "Proceed to paper_generalization_batch_a_source_policy as the first offline "
    "generalization slice before stronger wording."
)
```

Use `_PAPER_GENERALIZATION_SOURCE_POLICY_NEXT_ACTION` as the `next_action` value for every
blocking row in `_paper_faithful_offline_scope_criteria()`.

- [ ] **Step 5: Run GREEN focused tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_generalization_plan_gate tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_failure_labels_point_to_source_policy_gap tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_source_policy_generalization tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_completion_review -q
```

Expected: PASS.

## Task 3: Documentation, Record, And Registry

**Files:**
- Modify: `README.md`
- Modify: `docs/index.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/records/README.md`
- Modify: `experiments/registry.yaml`
- Create: `docs/records/2026-05-16-cpd-paper-faithful-offline-generalization-plan.md`

- [ ] **Step 1: Update canonical docs**

Replace stale "generalization plan is next" wording with:

```text
The command-only synthetic CPD paper offline lane now includes a planning table for offline
generalization beyond named toy fixtures. The report remains partial,
`paper_faithful_offline_supported` remains false, and the next gate is
`paper_generalization_batch_a_source_policy`.
```

Define the first source-policy gate:

```text
`paper_generalization_batch_a_source_policy` is the first offline implementation gate after the
planning table. It should broaden source mesh, preprocessing, source-face intake, and operator
policy beyond named toy fixtures. It is not package generation, Newton runtime execution, real USD,
benchmark evidence, paper_faithful_offline support, full CPD reproduction, collision-quality
evidence, deployment readiness, or safety certification.
```

Keep these explicit negatives in reviewer-facing docs:

```text
This planning table does not support paper_faithful_offline, full CPD reproduction, package
generation, Newton runtime execution, real-USD evidence, collision-quality evidence, benchmark
evidence, deployment readiness, or safety certification.
```

- [ ] **Step 2: Add registry entry**

Add this entry after `cpd-paper-fixture-breadth-completion-review`:

```yaml
  - id: cpd-paper-faithful-offline-generalization-plan
    status: in_progress
    command: PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report
    record: docs/records/2026-05-16-cpd-paper-faithful-offline-generalization-plan.md
    purpose: >
      Add a command-only planning table for offline CPD paper-lane generalization beyond
      named toy fixtures.
    claims_supported:
      - partial planning-only offline generalization roadmap for the synthetic CPD paper lane
      - records a planning-only closed paper_faithful_offline_generalization_plan gate while keeping paper_generalization_batch_a_source_policy and later offline generalization batches missing
      - no paper_faithful_offline claim, full CPD reproduction claim, package-generation claim, Newton runtime claim, real-USD claim, collision-quality claim, benchmark-suite claim, deployment claim, or safety-certification claim
```

- [ ] **Step 3: Add pending record**

Create `docs/records/2026-05-16-cpd-paper-faithful-offline-generalization-plan.md` with status
`In progress`, planned changes, evidence fields for command output, review notes, claim impact,
and next action.

- [ ] **Step 4: Add the record to both indexes**

Add the new record to `docs/records/README.md` and to the CPD paper record list in
`docs/index.md`:

```md
- 2026-05-16 CPD Paper Faithful Offline Generalization Plan
  (`2026-05-16-cpd-paper-faithful-offline-generalization-plan.md`):
  command-only planning table for offline CPD paper-lane generalization beyond named toy fixtures.
```

```md
- CPD paper faithful offline generalization plan record
  (`records/2026-05-16-cpd-paper-faithful-offline-generalization-plan.md`):
  dated implementation record for the command-only planning table beyond named toy fixtures.
```

- [ ] **Step 5: Run docs validators**

Run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

## Task 4: Review, Final Verification, And Commit

**Files:**
- All files changed by Tasks 1-3.

- [ ] **Step 1: Run focused CLI smoke**

Run:

```bash
PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report > /tmp/cpd_paper_offline_generalization_plan.json
python - <<'PY'
import json
from pathlib import Path

report = json.loads(Path("/tmp/cpd_paper_offline_generalization_plan.json").read_text())
plan = report["paper_faithful_offline_generalization_plan"]
expected_missing = [
    "paper_generalization_batch_a_source_policy_missing",
    "paper_generalization_batch_b_primitive_fit_engine_missing",
    "paper_generalization_batch_c_search_engine_missing",
    "paper_generalization_batch_d_postprocess_policy_missing",
    "paper_generalization_batch_e_package_boundary_readiness_missing",
]
expected_batch_ids = [
    "paper_generalization_batch_a_source_policy",
    "paper_generalization_batch_b_primitive_fit_engine",
    "paper_generalization_batch_c_search_engine",
    "paper_generalization_batch_d_postprocess_policy",
    "paper_generalization_batch_e_package_boundary_readiness",
]
assert report["failure_labels"] == expected_missing
assert report["next_required_gate"] == "paper_generalization_batch_a_source_policy"
assert plan["closed_gate"] == "paper_faithful_offline_generalization_plan"
assert plan["generalization_plan_complete"] is True
assert [batch["batch_id"] for batch in plan["planned_batches"]] == expected_batch_ids
assert plan["remaining_generalization_gates"] == expected_batch_ids
assert plan["blocked_runtime_gates"] == [
    "package_generation_boundary",
    "newton_runtime_boundary",
    "real_usd_boundary",
    "benchmark_evaluation_boundary",
]
assert plan["package_generation_triggered"] is False
assert plan["newton_runtime_triggered"] is False
assert plan["real_usd_triggered"] is False
assert plan["benchmark_triggered"] is False
print("generalization plan CLI smoke passed")
PY
```

Expected:

```text
generalization plan CLI smoke passed
```

- [ ] **Step 2: Run pre-finalization full verification**

Run:

```bash
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: pytest reports all tests passed; docs validators pass; `git diff --check` emits no
output.

- [ ] **Step 3: Attempt multi-agent review and record result**

Request independent review from implementation, paper-claim-boundary, and documentation angles. If
the platform quota blocks subagents, record the failed attempt exactly and perform a local fallback
review from the same three angles.

- [ ] **Step 4: Finalize record and registry**

Replace `In progress` with `Complete`, add exact command output summaries, and change the registry
entry to `complete`.

- [ ] **Step 5: Run post-finalization full verification**

Run the same verification after the record and registry status flip:

```bash
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: pytest reports all tests passed; docs validators pass; `git diff --check` emits no
output.

- [ ] **Step 6: Record post-finalization verification evidence**

Append the post-finalization command results to
`docs/records/2026-05-16-cpd-paper-faithful-offline-generalization-plan.md`, including the final
pytest pass count, docs validator status, site claim validator status, and `git diff --check`
status. Keep the registry entry `complete`.

- [ ] **Step 7: Run docs validators after the record update**

Run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

- [ ] **Step 8: Commit and push**

Run:

```bash
git add src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cpd_paper_offline.py tests/test_cli.py README.md docs/index.md docs/deepdive/evidence-status.md docs/reference/claim-boundaries.md docs/reference/cpd-paper-reproduction-gap-matrix.md docs/reference/cpd-paper-faithful-offline-lane-spec.md docs/reference/cpd-paper-fixture-breadth-expansion-plan.md docs/reference/cpd-paper-story-status.md docs/records/README.md docs/records/2026-05-16-cpd-paper-faithful-offline-generalization-plan.md experiments/registry.yaml
git commit -m "feat: add CPD paper offline generalization plan"
git push
```

Expected: commit succeeds and push updates `origin/main`.

## Self-Review

- Spec coverage: this plan covers the report payload, tests, CLI, docs, registry, record,
  verification, and review requirement for the generalization-plan gate.
- Unresolved-marker scan: no incomplete or unspecified behavior remains in implementation steps.
- Scope boundary: the plan closes only the planning gate and advances to the first offline
  source-policy implementation gate; it does not enter package generation, Newton runtime, real
  USD, or benchmarks.
- Type consistency: all new field names use JSON-compatible dict/list/string/bool values and
  match the test snippets.
