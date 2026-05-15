# CPD Objective Report Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an offline CPD-like objective report that produces paper-aligned surrogate geometry diagnostics for the current baseline.

**Architecture:** Keep the objective report local to `baselines/cpd_like`. Reuse the existing CPD-like decomposition path, then wrap its report with objective/accounting terms. Add a CLI flag and experiment config without touching Newton or changing merge behavior.

**Tech Stack:** Python dataclasses, existing CLI/config loader, pytest, USD tiny fixtures for CLI smoke, Markdown records.

---

### Task 1: Objective Report Core

**Files:**
- Create: `src/primitive_collision_compiler/baselines/cpd_like/objective.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/__init__.py`
- Test: `tests/test_cpd_like_objective.py`

- [ ] **Step 1: Write failing tests**

Add tests for:

- square mesh decomposition emits `stage == "cpd_like_offline_objective"`;
- partial disconnected topology-only decomposition keeps `status == "partial"` and reports
  `unmerged_components`;
- non-finite or negative primitive weights are rejected;
- planar mesh normalizer never emits `NaN` or `Infinity`.

- [ ] **Step 2: Run targeted tests and confirm RED**

Run:

```bash
python -m pytest tests/test_cpd_like_objective.py -q
```

Expected: import failure because the objective module does not exist.

- [ ] **Step 3: Implement core**

Implement `CPDLikeObjectiveOptions`, `CPDLikeObjectiveReport`, and
`build_cpd_like_objective_report(...)`.

- [ ] **Step 4: Run targeted tests and confirm GREEN**

Run:

```bash
python -m pytest tests/test_cpd_like_objective.py -q
```

Expected: all tests pass.

### Task 2: CLI And Config

**Files:**
- Modify: `src/primitive_collision_compiler/cli.py`
- Modify: `src/primitive_collision_compiler/config.py`
- Create: `configs/experiments/cpd_like_objective_report.yaml`
- Modify: `tests/test_cli.py`
- Modify: `tests/test_cpd_like_config.py`

- [ ] **Step 1: Write failing CLI/config tests**

Add tests for:

- `--run-cpd-like-objective-report` emits JSON for a tiny USD;
- malformed `cpd_like_objective.primitive_type_weights` fails cleanly;
- the committed config has safe claim boundary, no `/cpfs/user/`, and
  `report.evidence_level == "offline_cpd_like_objective_surrogate_smoke"`.

- [ ] **Step 2: Run targeted tests and confirm RED**

Run:

```bash
python -m pytest tests/test_cli.py::test_cli_run_cpd_like_objective_report_emits_json_for_tiny_usd tests/test_cpd_like_config.py -q
```

Expected: CLI flag and config are missing.

- [ ] **Step 3: Implement CLI/config**

Add `cpd_like_objective` to `_protocol_sections`, parse objective options, reuse
`_run_cpd_like_report(config)`, and emit the objective report. Do not call Newton.

- [ ] **Step 4: Run targeted tests and confirm GREEN**

Run:

```bash
python -m pytest tests/test_cli.py tests/test_cpd_like_config.py -q
```

Expected: all selected tests pass.

### Task 3: Documentation And Record

**Files:**
- Create: `docs/records/2026-05-15-cpd-like-objective-report.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/cpd-like-face-merge-explainer.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/index.md`
- Modify: `docs/records/README.md`
- Modify: `experiments/registry.yaml`

- [ ] **Step 1: Update docs**

State that the new slice is an offline paper-aligned surrogate objective report. Keep all
non-claims explicit.

- [ ] **Step 2: Add dated record**

Record implementation, verification commands, real smoke command, artifacts, and claim impact.

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

- [ ] **Step 1: Run full test suite**

```bash
python -m pytest -q
```

Expected: all tests pass.

- [ ] **Step 2: Run real clean-env smoke**

```bash
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_objective_report.yaml --run-cpd-like-objective-report
```

Expected: JSON with `stage: cpd_like_offline_objective`.

- [ ] **Step 3: Run final docs and whitespace checks**

```bash
python scripts/validate_docs.py
git diff --check
```

Expected: both pass.

- [ ] **Step 4: Request code review**

Dispatch reviewers for code, tests, and claim boundary. Fix Important/Critical findings before
merge.
