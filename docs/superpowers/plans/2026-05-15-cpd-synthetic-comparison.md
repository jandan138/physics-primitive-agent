# CPD Synthetic Comparison Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an offline synthetic comparison report for topology-only versus component-merge CPD-like objective outputs.

**Architecture:** Keep synthetic meshes and comparison logic local to `baselines/cpd_like/synthetic.py`. Reuse `decompose_mesh(...)` and `build_cpd_like_objective_report(...)`; do not change primitive fitting, merge search, USD loading, or Newton diagnostics. Expose a no-config CLI smoke path that emits strict JSON.

**Tech Stack:** Python dataclasses/helpers, existing CPD-like decomposition/objective modules, argparse CLI, pytest, Markdown records.

---

### Task 1: Synthetic Comparison Core

**Files:**
- Create: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/__init__.py`
- Test: `tests/test_cpd_like_synthetic.py`

- [ ] **Step 1: Write the failing test**

Add `tests/test_cpd_like_synthetic.py`:

```python
import json

from primitive_collision_compiler.baselines.cpd_like.synthetic import (
    SYNTHETIC_COMPARISON_CLAIM_BOUNDARY,
    build_cpd_like_synthetic_comparison_report,
)


def test_synthetic_comparison_report_covers_inspectable_cases():
    report = build_cpd_like_synthetic_comparison_report()

    assert report["stage"] == "cpd_like_synthetic_objective_comparison"
    assert report["status"] == "smoke_passed"
    assert report["claim_boundary"] == SYNTHETIC_COMPARISON_CLAIM_BOUNDARY
    assert [case["case_id"] for case in report["cases"]] == [
        "adjacent_square",
        "disconnected_pair",
        "blocked_disconnected_pair",
    ]

    cases = {case["case_id"]: case for case in report["cases"]}
    assert cases["adjacent_square"]["policies"]["topology_only"]["status"] == "smoke_passed"
    assert cases["adjacent_square"]["policies"]["virtual_pairwise"]["status"] == "smoke_passed"
    assert cases["adjacent_square"]["comparison"]["primitive_count_delta_virtual_minus_topology"] == 0

    disconnected = cases["disconnected_pair"]
    assert disconnected["policies"]["topology_only"]["status"] == "partial"
    assert disconnected["policies"]["virtual_pairwise"]["status"] == "smoke_passed"
    assert disconnected["comparison"][
        "virtual_pairwise_omits_topology_unmerged_component_label"
    ] is True
    assert disconnected["comparison"]["primitive_count_delta_virtual_minus_topology"] == -1

    blocked = cases["blocked_disconnected_pair"]
    assert blocked["policies"]["topology_only"]["status"] == "partial"
    assert blocked["policies"]["virtual_pairwise"]["status"] == "partial"
    assert "component_merge_blocked" in blocked["policies"]["virtual_pairwise"]["failure_labels"]


def test_synthetic_comparison_report_is_strict_json_serializable():
    report = build_cpd_like_synthetic_comparison_report()

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_like_synthetic_objective_comparison" in encoded
```

- [ ] **Step 2: Run the test and confirm RED**

Run:

```bash
python -m pytest tests/test_cpd_like_synthetic.py -q
```

Expected: import error because `synthetic.py` does not exist.

- [ ] **Step 3: Implement the synthetic module**

Create `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py` with:

```python
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from primitive_collision_compiler.baselines.cpd_like.decompose import decompose_mesh
from primitive_collision_compiler.baselines.cpd_like.objective import (
    CPDLikeObjectiveOptions,
    build_cpd_like_objective_report,
)
from primitive_collision_compiler.geometry.mesh import TriangleMesh

SYNTHETIC_COMPARISON_CLAIM_BOUNDARY = (
    "synthetic_objective_comparison_not_collision_quality_validation"
)
SYNTHETIC_COMPARISON_EVIDENCE_LEVEL = "offline_cpd_like_synthetic_comparison_smoke"


@dataclass(frozen=True)
class _PolicySpec:
    label: str
    component_merge: str
    excess_volume_threshold_fraction: float | None = None


@dataclass(frozen=True)
class _SyntheticCase:
    case_id: str
    description: str
    expectation: str
    mesh: TriangleMesh
    policies: tuple[_PolicySpec, ...]


def build_cpd_like_synthetic_comparison_report(
    *,
    primitive_subset: tuple[str, ...] = ("box",),
    objective_options: CPDLikeObjectiveOptions | None = None,
) -> dict[str, object]:
    options = objective_options or CPDLikeObjectiveOptions(
        claim_boundary=SYNTHETIC_COMPARISON_CLAIM_BOUNDARY,
        evidence_level=SYNTHETIC_COMPARISON_EVIDENCE_LEVEL,
    )
    case_payloads = [
        _case_payload(case, primitive_subset=primitive_subset, options=options)
        for case in _synthetic_cases()
    ]
    status = (
        "smoke_passed"
        if all(case["expectation_status"] == "matched" for case in case_payloads)
        else "partial"
    )
    return {
        "stage": "cpd_like_synthetic_objective_comparison",
        "status": status,
        "claim_boundary": options.claim_boundary,
        "evidence_level": options.evidence_level,
        "objective_version": options.objective_version,
        "cases": case_payloads,
    }
```

Then add helpers for `_synthetic_cases()`, `_adjacent_square_mesh()`, `_disconnected_triangles_mesh()`,
`_case_payload(...)`, `_policy_summary(...)`, `_comparison(...)`, and `_expectation_status(...)`.
The helper should summarize only compact objective fields: `status`, `decomposition_stage`,
`primitive_count`, `failure_labels`, `primitive_budget`, `merge_excess_terms`, and
`component_accounting`.

Modify `src/primitive_collision_compiler/baselines/cpd_like/__init__.py` to export
`SYNTHETIC_COMPARISON_CLAIM_BOUNDARY` and `build_cpd_like_synthetic_comparison_report`.

- [ ] **Step 4: Run targeted tests and confirm GREEN**

Run:

```bash
python -m pytest tests/test_cpd_like_synthetic.py -q
```

Expected: 2 passed.

### Task 2: CLI Entry

**Files:**
- Modify: `src/primitive_collision_compiler/cli.py`
- Test: `tests/test_cli.py`

- [ ] **Step 1: Write failing CLI tests**

Add tests:

```python
def test_cli_run_cpd_like_synthetic_comparison_emits_json_without_config(capsys):
    assert cli.main(["--run-cpd-like-synthetic-comparison"]) == 0

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["stage"] == "cpd_like_synthetic_objective_comparison"
    assert payload["status"] == "smoke_passed"
    assert [case["case_id"] for case in payload["cases"]] == [
        "adjacent_square",
        "disconnected_pair",
        "blocked_disconnected_pair",
    ]
    assert captured.err == ""


def test_cli_run_cpd_like_synthetic_comparison_rejects_non_finite_json(capsys, monkeypatch):
    monkeypatch.setattr(
        cli,
        "build_cpd_like_synthetic_comparison_report",
        lambda: {
            "stage": "cpd_like_synthetic_objective_comparison",
            "status": "smoke_passed",
            "bad": float("nan"),
        },
    )

    assert cli.main(["--run-cpd-like-synthetic-comparison"]) == 2

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "cpd_like_synthetic_comparison report contains non-finite JSON values" in captured.err
    assert "Traceback" not in captured.err
```

- [ ] **Step 2: Run tests and confirm RED**

Run:

```bash
python -m pytest tests/test_cli.py -q -k synthetic_comparison
```

Expected: parser rejects the missing flag.

- [ ] **Step 3: Implement CLI**

Modify `src/primitive_collision_compiler/cli.py`:

- import `build_cpd_like_synthetic_comparison_report`;
- add `--run-cpd-like-synthetic-comparison` to the parser;
- add a no-config branch that prints `json.dumps(report, sort_keys=True, allow_nan=False)`;
- return `2` with a clean stderr message if strict JSON serialization fails;
- return `0` only when `report["status"] == "smoke_passed"`.

- [ ] **Step 4: Run targeted tests and confirm GREEN**

Run:

```bash
python -m pytest tests/test_cpd_like_synthetic.py tests/test_cli.py -q -k "synthetic_comparison or cpd_like_synthetic"
```

Expected: all selected tests pass.

### Task 3: Docs And Record

**Files:**
- Create: `docs/records/2026-05-15-cpd-like-synthetic-comparison.md`
- Modify: `docs/records/README.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/cpd-like-face-merge-explainer.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/index.md`
- Modify: `experiments/registry.yaml`

- [ ] **Step 1: Update docs**

Use the phrase `synthetic objective comparison`. State that this is an offline diagnostic comparison
over deterministic toy meshes. Do not call it validation, benchmark evidence, or proof of
decomposition quality.

- [ ] **Step 2: Add dated record**

Record:

- the three synthetic cases;
- expected topology-only versus virtual-pairwise behavior;
- targeted and full verification commands;
- claim impact and next action.

- [ ] **Step 3: Run docs checks**

Run:

```bash
python scripts/validate_docs.py
git diff --check
```

Expected: both pass.

### Task 4: Final Verification And Review

**Files:**
- All changed files.

- [ ] **Step 1: Run full verification**

Run:

```bash
python -m pytest -q
python scripts/validate_docs.py
git diff --check
PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-synthetic-comparison
```

Expected:

- pytest passes;
- docs validation passes;
- whitespace check passes;
- CLI emits JSON with `stage == "cpd_like_synthetic_objective_comparison"` and
  `status == "smoke_passed"`.

- [ ] **Step 2: Request review**

Dispatch one code/test reviewer and one claim/docs reviewer. Fix Critical or Important findings
before merge.

- [ ] **Step 3: Commit and merge**

Commit implementation and docs, verify on `master` after fast-forward merge, and remove the feature
worktree.

## Self-Review

The plan covers the spec requirements, contains no placeholders, and keeps the slice offline,
synthetic, and claim-bounded.
