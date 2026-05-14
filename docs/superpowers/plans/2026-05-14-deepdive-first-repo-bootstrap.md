# DeepDive-First Repo Bootstrap Implementation Plan

Status: Historical implementation plan. Current evidence is recorded in `docs/records/`.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete DeepDive-first repository skeleton for the Newton Primitive Collision Compiler proposal while keeping research implementation explicitly out of scope.

**Architecture:** The bootstrap creates a reviewer-facing documentation system, a minimal installable Python package, a small config/test harness, and claim-boundary validation. DeepDive materials are the primary user surface; code exists only to prove future engineering discipline and stable contracts.

**Tech Stack:** Python 3.10+, standard library dataclasses/argparse/json, PyYAML for config loading, pytest for tests, ruff for lint configuration.

---

## File Structure

- Create `README.md`, `CONTRIBUTING.md`, `.python-version`, `Makefile`, `pyproject.toml`, and `requirements.txt` for repo identity and canonical commands.
- Create `docs/index.md`, `docs/deepdive/*`, `docs/design/*`, `docs/reference/*`, `docs/records/*`, `docs/tmp/README.md`, and `docs/superpowers/README.md` for a Genesis-like but DeepDive-first documentation system.
- Create `src/primitive_collision_compiler/{__init__.py,contracts.py,config.py,cli.py}` for a minimal package with explicit contracts and dry-run CLI.
- Create `configs/deepdive/mvp.yaml`, `configs/experiments/phase0_baseline.yaml`, and `tests/fixtures/dry_run_mvp.yaml` as config examples.
- Create `tests/test_contracts.py`, `tests/test_cli.py`, and `scripts/validate_docs.py` for TDD and claim-boundary validation.
- Create `experiments/README.md`, `experiments/registry.yaml`, `assets/README.md`, `reports/README.md`, and `archive/README.md` for artifact boundaries.

## Task 1: Repository Metadata And Command Surface

**Files:**
- Create/modify: `.gitignore`, `.python-version`, `README.md`, `CONTRIBUTING.md`, `Makefile`, `pyproject.toml`, `requirements.txt`

- [ ] **Step 1: Add metadata files**

Create `.python-version`:

```text
3.10
```

Create `requirements.txt`:

```text
-e .[dev]
```

Create `pyproject.toml` with project metadata, package discovery from `src`, console script `npc-compile = "primitive_collision_compiler.cli:main"`, pytest config, and ruff target `py310`.

Create `Makefile` with targets:

```make
.PHONY: install test validate docs-check
install:
	python -m pip install -e ".[dev]"

test:
	python -m pytest

validate:
	python scripts/validate_docs.py
	python -m pytest

docs-check:
	python scripts/validate_docs.py
```

- [ ] **Step 2: Add human-facing repo docs**

Create `README.md` with these sections: overview, current status, strategic framing, safe claim, unsafe claim, repository layout, quick start, DeepDive navigation, and current non-goals.

Create `CONTRIBUTING.md` with canonical commands, claim-boundary rules, and artifact policy.

- [ ] **Step 3: Verify metadata**

Run:

```bash
python -m pip install -e ".[dev]"
python -m pytest --collect-only
```

Expected: package install succeeds; pytest collection may find zero or existing tests at this stage, but should not fail from package metadata.

- [ ] **Step 4: Commit**

```bash
git add .gitignore .python-version README.md CONTRIBUTING.md Makefile pyproject.toml requirements.txt
git commit -m "chore: add repository metadata"
```

## Task 2: Minimal Package Contracts And CLI

**Files:**
- Create: `src/primitive_collision_compiler/__init__.py`
- Create: `src/primitive_collision_compiler/contracts.py`
- Create: `src/primitive_collision_compiler/config.py`
- Create: `src/primitive_collision_compiler/cli.py`
- Create: `tests/fixtures/dry_run_mvp.yaml`
- Create: `tests/test_contracts.py`
- Create: `tests/test_cli.py`

- [ ] **Step 1: Write failing contract tests**

`tests/test_contracts.py` should assert:

```python
from primitive_collision_compiler.contracts import CompileConfig, CompileReport

def test_compile_config_defaults_are_conservative():
    config = CompileConfig(asset_path="assets/example.usda", task="grasping")
    assert config.method == "primitive_first"
    assert config.max_primitives == 16
    assert config.allowed_fallback == ("coacd", "sdf")

def test_compile_report_marks_dry_run_not_compiled():
    report = CompileReport(asset_id="example", task="grasping", dry_run=True)
    payload = report.to_dict()
    assert payload["status"] == "dry_run"
    assert payload["compiled"] is False
```

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
python -m pytest tests/test_contracts.py -q
```

Expected: FAIL because `primitive_collision_compiler` is not implemented yet.

- [ ] **Step 3: Implement contracts**

Implement dataclasses for `CompileConfig`, `PrimitiveSpec`, `FallbackSpec`, `CollisionPackage`, and `CompileReport`. Use tuples for default fallbacks and checks. Provide `to_dict()` on `CompileReport`.

- [ ] **Step 4: Write failing CLI/config tests**

`tests/test_cli.py` should assert:

```python
import json
import subprocess
import sys
from pathlib import Path

def test_cli_help_mentions_newton_primitive_collision_compiler():
    result = subprocess.run(
        [sys.executable, "-m", "primitive_collision_compiler.cli", "--help"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Newton Primitive Collision Compiler" in result.stdout

def test_cli_dry_run_outputs_json_report():
    fixture = Path(__file__).parent / "fixtures" / "dry_run_mvp.yaml"
    result = subprocess.run(
        [sys.executable, "-m", "primitive_collision_compiler.cli", "--config", str(fixture), "--dry-run"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    assert payload["status"] == "dry_run"
    assert payload["compiled"] is False
    assert payload["task"] == "grasping"
```

- [ ] **Step 5: Run CLI tests and verify RED**

Run:

```bash
python -m pytest tests/test_cli.py -q
```

Expected: FAIL because config loading and CLI are not implemented yet.

- [ ] **Step 6: Implement config loader and CLI**

Create YAML fixture:

```yaml
asset:
  path: assets/example.usda
task:
  primary: grasping
compile:
  method: primitive_first
  max_primitives: 16
  allowed_fallback: [coacd, sdf]
```

Implement `config.py` with `load_compile_config(path: str | Path) -> CompileConfig` using `yaml.safe_load`.

Implement `cli.py` with argparse options `--config` and `--dry-run`; dry-run prints JSON report and exits 0. Non-dry-run exits with a clear message that real compilation is not implemented.

- [ ] **Step 7: Verify package tests**

Run:

```bash
python -m pytest tests/test_contracts.py tests/test_cli.py -q
```

Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add src tests
git commit -m "feat: add primitive collision compiler skeleton"
```

## Task 3: DeepDive And Design Documentation System

**Files:**
- Create: `docs/index.md`
- Create: `docs/deepdive/README.md`
- Create: `docs/deepdive/message-map.md`
- Create: `docs/deepdive/application.md`
- Create: `docs/deepdive/evidence-status.md`
- Create: `docs/deepdive/pitch-outline.md`
- Create: `docs/deepdive/review-qa.md`
- Create: `docs/deepdive/one-page-summary.md`
- Create: `docs/design/project-scope.md`
- Create: `docs/design/system-architecture.md`
- Create: `docs/design/research-roadmap.md`
- Create: `docs/design/evaluation-plan.md`
- Create: `docs/design/benchmark-protocol.md`

- [ ] **Step 1: Create DeepDive docs**

Each DeepDive file must include the strategic story, the narrow first milestone, and clear non-goals. `review-qa.md` must include sections named `Taste`, `Benchmark`, `User Experience`, and `Value Delivering`.

- [ ] **Step 2: Create design docs**

`evaluation-plan.md` must include baseline, task, metric, reporting, phase gate, and no-go criteria sections matching the approved spec.

`research-roadmap.md` must include Phase 0, Phase 1, Phase 2, Phase 3, and Phase 4.

- [ ] **Step 3: Commit**

```bash
git add docs/index.md docs/deepdive docs/design
git commit -m "docs: add deepdive documentation system"
```

## Task 4: Reference, Records, Artifacts, And Claim Validation

**Files:**
- Create: `docs/reference/claim-boundaries.md`
- Create: `docs/reference/literature-map.md`
- Create: `docs/reference/newton-notes.md`
- Create: `docs/reference/related-work-notes.md`
- Create: `docs/records/README.md`
- Create: `docs/records/2026-05-14-project-bootstrap.md`
- Create: `docs/tmp/README.md`
- Create: `docs/superpowers/README.md`
- Create: `experiments/README.md`
- Create: `experiments/registry.yaml`
- Create: `assets/README.md`
- Create: `reports/README.md`
- Create: `archive/README.md`
- Create: `scripts/validate_docs.py`
- Create: `tests/test_docs_validation.py`

- [ ] **Step 1: Write failing docs validation test**

`tests/test_docs_validation.py` should assert that claim lint catches unscoped dangerous terms:

```python
from scripts.validate_docs import find_claim_boundary_issues

def test_claim_boundary_lint_flags_unscoped_guarantee():
    issues = find_claim_boundary_issues("This system guarantees real-world safety.")
    assert issues
    assert "guarantees" in issues[0].term
```

- [ ] **Step 2: Run docs validation test and verify RED**

Run:

```bash
python -m pytest tests/test_docs_validation.py -q
```

Expected: FAIL because `scripts.validate_docs` does not exist.

- [ ] **Step 3: Implement reference and artifact docs**

`claim-boundaries.md` must include allowed current claims, claims requiring Phase 0, claims requiring Phase 1/2, and forbidden claims.

`docs/records/README.md` must include the record template: Date, Status, Changes, Verification, Artifacts, Claim Impact, Next Action.

Artifact README files must explain that large/generated assets are not committed.

- [ ] **Step 4: Implement `scripts/validate_docs.py`**

The script must expose `find_claim_boundary_issues(text: str) -> list[ClaimIssue]` and a CLI that scans `README.md`, `docs/deepdive`, `docs/design`, and `docs/reference`. It should flag unscoped terms including `guarantee`, `guarantees`, `deployment-ready`, `certified safe`, `proven safe`, and `fully replaces`.

- [ ] **Step 5: Verify docs validation**

Run:

```bash
python -m pytest tests/test_docs_validation.py -q
python scripts/validate_docs.py
```

Expected: PASS and no claim-boundary violations in repository docs.

- [ ] **Step 6: Commit**

```bash
git add docs/reference docs/records docs/tmp/README.md docs/superpowers/README.md experiments assets reports archive scripts tests/test_docs_validation.py
git commit -m "docs: add claim and artifact governance"
```

## Task 5: Configs, Final Verification, And Bootstrap Commit Hygiene

**Files:**
- Create: `configs/deepdive/mvp.yaml`
- Create: `configs/experiments/phase0_baseline.yaml`
- Modify if needed: `README.md`, `docs/index.md`, `AGENTS.md`
- Add existing source materials if accepted: `docs/tmp/DeepDive_usage_guide.md`, `docs/tmp/newton_llm_primitive_first_research_review.md`

- [ ] **Step 1: Add configs and agent rules**

Create config files matching the approved spec. Create `AGENTS.md` with DeepDive priority, claim-boundary rules, source directory, artifact policy, and config policy.

- [ ] **Step 2: Track source materials**

Add the two existing source documents under `docs/tmp/` so the repo keeps its original research context. They remain marked as temporary source intake, not durable reviewer-facing docs.

- [ ] **Step 3: Run full verification**

Run:

```bash
python -m pip install -e ".[dev]"
python scripts/validate_docs.py
python -m pytest
git diff --check
```

Expected: all commands exit 0.

- [ ] **Step 4: Commit final bootstrap files**

```bash
git add AGENTS.md configs docs/tmp/DeepDive_usage_guide.md docs/tmp/newton_llm_primitive_first_research_review.md
git commit -m "chore: complete deepdive bootstrap skeleton"
```

## Plan Self-Review

- Spec coverage: the plan covers repository metadata, docs hierarchy, package skeleton, configs, validation, records, artifacts, and source material tracking.
- Placeholder scan: this plan avoids unresolved placeholder language and gives concrete file paths and command expectations.
- Type consistency: package name is consistently `primitive_collision_compiler`; CLI command remains `npc-compile` with expanded help text.
