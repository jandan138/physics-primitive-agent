# CPD Synthetic Expected-Failure Workbench Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a deterministic command-only synthetic workbench that classifies current CPD-like baseline limitations as expected diagnostic flags.

**Architecture:** Extend `synthetic.py` with a separate expected-failure report builder that reuses the existing objective report and policy summaries. Add a CLI flag that emits strict JSON, tests that pin report shape and flags, and documentation that frames the workbench as diagnostic accounting rather than quality evidence.

**Tech Stack:** Python dictionaries/dataclasses, existing CPD-like mesh helpers, pytest, argparse CLI, Markdown records.

---

### Task 1: Expected-Failure Report Tests

**Files:**
- Modify: `tests/test_cpd_like_synthetic.py`

- [ ] **Step 1: Write failing report schema test**

Add import:

```python
from primitive_collision_compiler.baselines.cpd_like.synthetic import (
    EXPECTED_FAILURE_WORKBENCH_CLAIM_BOUNDARY,
    build_cpd_like_cost_guided_synthetic_comparison_report,
    build_cpd_like_expected_failure_synthetic_workbench_report,
    build_cpd_like_synthetic_comparison_report,
)
```

Add:

```python
def test_expected_failure_workbench_reports_known_cpd_gaps():
    report = build_cpd_like_expected_failure_synthetic_workbench_report()

    assert report["stage"] == "cpd_like_expected_failure_synthetic_workbench"
    assert report["status"] == "smoke_passed"
    assert report["status_semantics"] == (
        "expected_limitations_reported_not_decomposition_success"
    )
    assert report["claim_boundary"] == EXPECTED_FAILURE_WORKBENCH_CLAIM_BOUNDARY
    assert report["evidence_level"] == (
        "offline_cpd_like_expected_failure_workbench_smoke"
    )
    assert [case["case_id"] for case in report["cases"]] == [
        "restricted_primitive_vocabulary_gap",
        "single_proxy_wraps_disconnected_components",
        "threshold_blocks_component_merge",
    ]

    cases = {case["case_id"]: case for case in report["cases"]}
    restricted = cases["restricted_primitive_vocabulary_gap"]
    assert restricted["expectation_status"] == "matched"
    assert restricted["limitation_class"] == "expected_primitive_fit_gap"
    assert restricted["next_capability_needed"] == "primitive_fit_extension"
    assert restricted["paper_gap_tags"] == [
        "restricted_primitive_vocabulary",
        "paper_scope_primitive_fitting",
    ]
    assert restricted["fixture_geometry_summary"] == {
        "point_count": 4,
        "face_count": 2,
        "connected_component_count": 1,
        "mesh_aabb_volume": 0.0,
        "normalizer_floor_applied": True,
    }
    assert restricted["expected_diagnostic_flags"] == {
        "expected": [
            "unsupported_paper_primitives_present",
            "paper_alignment_surrogate_not_paper_faithful",
        ],
        "observed": [
            "unsupported_paper_primitives_present",
            "paper_alignment_surrogate_not_paper_faithful",
        ],
        "missing": [],
        "unexpected": [],
        "match_status": "matched",
    }
    assert restricted["metrics"]["paper_primitive_gap"][
        "unsupported_paper_primitive_count"
    ] == 3

    wrapped = cases["single_proxy_wraps_disconnected_components"]
    assert wrapped["expectation_status"] == "matched"
    assert wrapped["limitation_class"] == "expected_empty_wrapper_proxy"
    assert wrapped["next_capability_needed"] == "primitive_fit_extension"
    assert wrapped["fixture_geometry_summary"]["connected_component_count"] == 2
    assert wrapped["expected_diagnostic_flags"]["missing"] == []
    assert wrapped["expected_diagnostic_flags"]["unexpected"] == []
    assert "virtual_component_merge_used" in wrapped["expected_diagnostic_flags"]["observed"]
    assert "empty_space_wrap_proxy_present" in wrapped["expected_diagnostic_flags"]["observed"]
    assert wrapped["policy"]["status"] == "smoke_passed"
    assert wrapped["metrics"]["component_accounting"]["virtual_component_merge_count"] == 1
    assert wrapped["metrics"]["merge_excess_terms"]["accepted_eq4_cost_sum"] > 0.0

    blocked = cases["threshold_blocks_component_merge"]
    assert blocked["expectation_status"] == "matched"
    assert blocked["limitation_class"] == "expected_threshold_block"
    assert blocked["next_capability_needed"] == "merge_search_extension"
    assert blocked["policy"]["status"] == "partial"
    assert blocked["expected_diagnostic_flags"] == {
        "expected": [
            "unsupported_paper_primitives_present",
            "paper_alignment_surrogate_not_paper_faithful",
            "component_merge_blocked",
            "unmerged_components",
            "primitive_budget_not_met",
        ],
        "observed": [
            "unsupported_paper_primitives_present",
            "paper_alignment_surrogate_not_paper_faithful",
            "component_merge_blocked",
            "unmerged_components",
            "primitive_budget_not_met",
        ],
        "missing": [],
        "unexpected": [],
        "match_status": "matched",
    }
```

- [ ] **Step 2: Write failing strict JSON test**

Add:

```python
def test_expected_failure_workbench_report_is_strict_json_serializable():
    report = build_cpd_like_expected_failure_synthetic_workbench_report()

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_like_expected_failure_synthetic_workbench" in encoded
```

- [ ] **Step 3: Run tests and confirm RED**

Run:

```bash
python -m pytest tests/test_cpd_like_synthetic.py -q -k expected_failure
```

Expected: import failure because the expected-failure builder and constant do not exist.

### Task 2: Expected-Failure Report Builder

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/__init__.py`
- Test: `tests/test_cpd_like_synthetic.py`

- [ ] **Step 1: Add constants and public builder**

In `synthetic.py`, import the normalizer floor:

```python
from primitive_collision_compiler.baselines.cpd_like.decompose import (
    MIN_NORMALIZATION_VOLUME,
    decompose_mesh,
)
```

Add:

```python
EXPECTED_FAILURE_WORKBENCH_CLAIM_BOUNDARY = (
    "synthetic_expected_failure_workbench_not_collision_quality_validation"
)
EXPECTED_FAILURE_WORKBENCH_EVIDENCE_LEVEL = (
    "offline_cpd_like_expected_failure_workbench_smoke"
)
EXPECTED_FAILURE_WORKBENCH_STATUS_SEMANTICS = (
    "expected_limitations_reported_not_decomposition_success"
)
```

Add:

```python
def build_cpd_like_expected_failure_synthetic_workbench_report(
    *,
    primitive_subset: tuple[str, ...] = ("box",),
    objective_options: CPDLikeObjectiveOptions | None = None,
) -> dict[str, object]:
    options = objective_options or CPDLikeObjectiveOptions(
        claim_boundary=EXPECTED_FAILURE_WORKBENCH_CLAIM_BOUNDARY,
        evidence_level=EXPECTED_FAILURE_WORKBENCH_EVIDENCE_LEVEL,
    )
    case_payloads = [
        _expected_failure_case_payload(case, primitive_subset=primitive_subset, options=options)
        for case in _expected_failure_cases()
    ]
    status = (
        "smoke_passed"
        if all(case["expectation_status"] == "matched" for case in case_payloads)
        else "partial"
    )
    return {
        "stage": "cpd_like_expected_failure_synthetic_workbench",
        "status": status,
        "status_semantics": EXPECTED_FAILURE_WORKBENCH_STATUS_SEMANTICS,
        "claim_boundary": options.claim_boundary,
        "evidence_level": options.evidence_level,
        "objective_version": options.objective_version,
        "cases": case_payloads,
    }
```

- [ ] **Step 2: Add expected-failure case specs**

Add:

```python
@dataclass(frozen=True)
class _ExpectedFailureCase:
    case_id: str
    description: str
    paper_story_gap: str
    paper_gap_tags: tuple[str, ...]
    limitation_class: str
    next_capability_needed: str
    expected_diagnostic_flags: tuple[str, ...]
    mesh: TriangleMesh
    policy: _PolicySpec
    target_primitive_count: int = 1
```

Add `_expected_failure_cases()` with the three cases from the design. Use these exact tuples:

```python
("restricted_primitive_vocabulary", "paper_scope_primitive_fitting")
("assigned_vertex_containment_proxy_only", "no_surface_distance_or_collision_benchmark")
("threshold_applies_only_to_virtual_component_merges", "candidate_graph_restricted")
```

- [ ] **Step 3: Extend policy summary**

In `_policy_summary(...)`, read:

```python
geometric_excess_proxy = objective["metrics"]["geometric_excess_proxy"]
paper_primitive_gap = objective["metrics"]["paper_primitive_gap"]
```

and include:

```python
"geometric_excess_proxy": geometric_excess_proxy,
"paper_primitive_gap": paper_primitive_gap,
```

- [ ] **Step 4: Add payload and flag helpers**

Implement:

```python
def _expected_failure_case_payload(
    case: _ExpectedFailureCase,
    *,
    primitive_subset: tuple[str, ...],
    options: CPDLikeObjectiveOptions,
) -> dict[str, object]:
    policy = _policy_summary(
        _SyntheticCase(
            case_id=case.case_id,
            description=case.description,
            expectation="Expected diagnostic flags should be observed.",
            mesh=case.mesh,
            policies=(case.policy,),
            target_primitive_count=case.target_primitive_count,
        ),
        case.policy,
        primitive_subset=primitive_subset,
        options=options,
    )
    expected = list(case.expected_diagnostic_flags)
    observed = _diagnostic_flags(policy)
    missing = [flag for flag in expected if flag not in observed]
    unexpected = [flag for flag in observed if flag not in expected]
    match_status = "matched" if not missing and not unexpected else "mismatched"
    return {
        "case_id": case.case_id,
        "description": case.description,
        "paper_story_gap": case.paper_story_gap,
        "paper_gap_tags": list(case.paper_gap_tags),
        "limitation_class": case.limitation_class,
        "next_capability_needed": case.next_capability_needed,
        "fixture_geometry_summary": _fixture_geometry_summary(case.mesh, policy),
        "expected_diagnostic_flags": {
            "expected": expected,
            "observed": observed,
            "missing": missing,
            "unexpected": unexpected,
            "match_status": match_status,
        },
        "expectation_status": match_status,
        "policy": policy,
        "metrics": {
            "primitive_budget": policy["primitive_budget"],
            "merge_excess_terms": policy["merge_excess_terms"],
            "component_accounting": policy["component_accounting"],
            "paper_primitive_gap": policy["paper_primitive_gap"],
            "paper_alignment": policy["paper_alignment"],
        },
    }
```

Implement `_diagnostic_flags(policy)` with deterministic ordering:

```python
def _diagnostic_flags(policy: dict[str, object]) -> list[str]:
    flags: list[str] = []
    paper_alignment = policy["paper_alignment"]
    paper_primitive_gap = policy["paper_primitive_gap"]
    merge_excess_terms = policy["merge_excess_terms"]
    component_accounting = policy["component_accounting"]
    failure_labels = set(policy["failure_labels"])

    if paper_primitive_gap["unsupported_paper_primitive_count"] > 0:
        flags.append("unsupported_paper_primitives_present")
    if paper_alignment["paper_faithfulness"] == "surrogate_not_paper_faithful":
        flags.append("paper_alignment_surrogate_not_paper_faithful")
    if component_accounting["virtual_component_merge_count"] > 0:
        flags.append("virtual_component_merge_used")
    if (
        component_accounting["virtual_component_merge_count"] > 0
        and float(merge_excess_terms["accepted_eq4_cost_sum"] or 0.0) > 0.0
    ):
        flags.append("empty_space_wrap_proxy_present")
    if "component_merge_blocked" in failure_labels:
        flags.append("component_merge_blocked")
    if "unmerged_components" in failure_labels:
        flags.append("unmerged_components")
    if "primitive_budget_not_met" in failure_labels:
        flags.append("primitive_budget_not_met")
    return flags
```

Implement geometry helpers:

```python
def _fixture_geometry_summary(
    mesh: TriangleMesh,
    policy: dict[str, object],
) -> dict[str, object]:
    mesh_aabb_volume = float(policy["geometric_excess_proxy"]["mesh_aabb_volume"])
    return {
        "point_count": int(mesh.points.shape[0]),
        "face_count": mesh.face_count,
        "connected_component_count": _connected_component_count(mesh),
        "mesh_aabb_volume": mesh_aabb_volume,
        "normalizer_floor_applied": bool(mesh_aabb_volume < MIN_NORMALIZATION_VOLUME),
    }


def _connected_component_count(mesh: TriangleMesh) -> int:
    adjacency = mesh.adjacent_faces()
    unseen = set(adjacency)
    count = 0
    while unseen:
        count += 1
        stack = [unseen.pop()]
        while stack:
            face_id = stack.pop()
            for neighbor in adjacency[face_id]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    stack.append(neighbor)
    return count
```

- [ ] **Step 5: Export from package init**

In `src/primitive_collision_compiler/baselines/cpd_like/__init__.py`, import and add to
`__all__`:

```python
build_cpd_like_expected_failure_synthetic_workbench_report
```

- [ ] **Step 6: Run tests and confirm GREEN**

Run:

```bash
python -m pytest tests/test_cpd_like_synthetic.py -q -k expected_failure
```

Expected: selected tests pass.

### Task 3: CLI Flag

**Files:**
- Modify: `src/primitive_collision_compiler/cli.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write failing CLI tests**

Add:

```python
def test_cli_run_cpd_like_expected_failure_workbench_emits_json_without_config(capsys):
    assert cli.main(["--run-cpd-like-expected-failure-workbench"]) == 0

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert payload["stage"] == "cpd_like_expected_failure_synthetic_workbench"
    assert payload["status"] == "smoke_passed"
    assert payload["status_semantics"] == (
        "expected_limitations_reported_not_decomposition_success"
    )
    assert payload["cases"][0]["case_id"] == "restricted_primitive_vocabulary_gap"
```

Add:

```python
def test_cli_run_cpd_like_expected_failure_workbench_rejects_non_finite_json(
    monkeypatch, capsys
):
    monkeypatch.setattr(
        cli,
        "build_cpd_like_expected_failure_synthetic_workbench_report",
        lambda: {
            "stage": "cpd_like_expected_failure_synthetic_workbench",
            "status": "smoke_passed",
            "bad": float("nan"),
        },
    )

    assert cli.main(["--run-cpd-like-expected-failure-workbench"]) == 2

    captured = capsys.readouterr()
    assert (
        "cpd_like_expected_failure_workbench report contains non-finite JSON values"
        in captured.err
    )
```

- [ ] **Step 2: Run tests and confirm RED**

Run:

```bash
python -m pytest tests/test_cli.py -q -k expected_failure_workbench
```

Expected: parser rejects the new flag or imported builder is missing.

- [ ] **Step 3: Implement CLI flag**

In `cli.py`, import the builder, add:

```python
parser.add_argument(
    "--run-cpd-like-expected-failure-workbench",
    action="store_true",
    help="run offline synthetic expected-failure workbench for known CPD-like gaps",
)
```

Add handling after the other synthetic no-config commands:

```python
if args.run_cpd_like_expected_failure_workbench:
    report = build_cpd_like_expected_failure_synthetic_workbench_report()
    try:
        print(json.dumps(report, sort_keys=True, allow_nan=False))
    except ValueError as exc:
        print(
            "npc-compile: cpd_like_expected_failure_workbench report contains "
            f"non-finite JSON values: {exc}",
            file=sys.stderr,
        )
        return 2
    return 0 if report["status"] == "smoke_passed" else 2
```

- [ ] **Step 4: Run CLI tests and confirm GREEN**

Run:

```bash
python -m pytest tests/test_cli.py -q -k expected_failure_workbench
```

Expected: selected CLI tests pass.

### Task 4: Documentation And Record

**Files:**
- Create: `docs/records/2026-05-15-cpd-synthetic-expected-failure-workbench.md`
- Modify: `docs/reference/cpd-objective-report-alignment.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/index.md`
- Modify: `docs/records/README.md`
- Modify: `README.md`

- [ ] **Step 1: Update reference docs**

Document that the expected-failure workbench converts known CPD-paper gaps into deterministic
diagnostic flags. Use:

- `deterministic expected-failure synthetic workbench`;
- `expected limitation fixtures`;
- `diagnostic flags`;
- `known CPD-paper gaps`;
- `not benchmark evidence`;
- `not collision-quality validation`;
- `not paper-faithful CPD reproduction`;
- `smoke_passed means expected limitations were reported, not decomposition success`.

- [ ] **Step 2: Add dated record**

Record:

- new report stage and CLI flag;
- fixture ids;
- expected/observed/missing/unexpected flag semantics;
- verification commands;
- claim impact;
- next action.

- [ ] **Step 3: Run documentation checks**

Run:

```bash
python scripts/validate_docs.py
git diff --check
```

Expected: both pass.

### Task 5: Review, Final Verification, Commit

**Files:**
- All changed files.

- [ ] **Step 1: Run targeted tests**

```bash
python -m pytest tests/test_cpd_like_synthetic.py tests/test_cli.py -q -k "expected_failure or synthetic_comparison"
```

Expected: selected tests pass.

- [ ] **Step 2: Run full tests**

```bash
python -m pytest -q
```

Expected: all tests pass.

- [ ] **Step 3: Request focused agent review**

Ask one reviewer to check report/schema/test correctness and one reviewer to check claim-boundary
wording.

- [ ] **Step 4: Fix Important/Critical findings**

If review finds Important or Critical issues, fix them with tests and rerun verification.

- [ ] **Step 5: Commit**

```bash
git add src/primitive_collision_compiler/baselines/cpd_like/synthetic.py \
  src/primitive_collision_compiler/baselines/cpd_like/__init__.py \
  src/primitive_collision_compiler/cli.py \
  tests/test_cpd_like_synthetic.py \
  tests/test_cli.py \
  docs/records/2026-05-15-cpd-synthetic-expected-failure-workbench.md \
  docs/reference/cpd-objective-report-alignment.md \
  docs/reference/cpd-paper-story-status.md \
  docs/reference/claim-boundaries.md \
  docs/deepdive/evidence-status.md \
  docs/index.md \
  docs/records/README.md \
  README.md \
  docs/superpowers/specs/2026-05-15-cpd-synthetic-expected-failure-design.md \
  docs/superpowers/plans/2026-05-15-cpd-synthetic-expected-failure.md
git commit -m "feat: add cpd synthetic expected failure workbench"
```

## Self-Review

No placeholders remain. The plan keeps this slice diagnostic and does not add new primitive fitting,
Newton execution, benchmark evaluation, general failure detection, or collision-quality claims.

