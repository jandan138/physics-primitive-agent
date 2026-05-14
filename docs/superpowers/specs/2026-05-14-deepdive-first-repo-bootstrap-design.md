# DeepDive-First Repo Bootstrap Design

Date: 2026-05-14

## Goal

Turn `physics-primitive-agent` from a two-document research note directory into a clean, durable project repository that supports the immediate DeepDive application while leaving a disciplined path for later research and engineering.

The first deliverable is not a working primitive collision compiler. The first deliverable is a credible DeepDive-ready repository: clear project framing, reviewer-facing materials, evidence boundaries, and a minimal Python package skeleton that can grow into implementation after approval.

## Current State

The repository currently contains:

- `docs/tmp/newton_llm_primitive_first_research_review.md`: the main technical review for a Newton primitive-first collision compiler.
- `docs/tmp/DeepDive_usage_guide.md`: company DeepDive guidance and examples.

It does not currently contain a git repository, README, package metadata, source tree, tests, configs, scripts, experiment registry, or organized documentation index.

## Design Direction

Use a DeepDive-first full skeleton:

- Make the repository look intentional and maintainable from day one.
- Keep DeepDive application materials as the primary surface.
- Add a minimal engineering skeleton to show feasibility and future execution discipline.
- Avoid pretending that research implementation already exists.
- Preserve the existing long-form review documents under `docs/tmp/` until they are later cleaned or archived.

## Strategic Narrative For Leadership

The DeepDive materials should include a leadership-facing story that connects the project to the Physical Intelligence Center's broader strategy.

The strategic framing is:

- Physical intelligence systems need AI models that respect physical safety constraints, not only models that generate plausible actions, assets, or plans.
- A physics engine is the executable substrate for those constraints: it can expose penetrations, unstable contacts, unsafe force transfer, false negative collision gaps, and task-level physical failures before deployment.
- Collision geometry is one of the lowest-level safety interfaces between AI-generated worlds, robot policies, and simulation. If the collision proxy is wrong, downstream policy training, evaluation, and safety claims become untrustworthy.
- A primitive-first, simulation-verified, fallback-aware collision compiler is therefore not just an asset conversion tool. It is a small but concrete step toward an AI safety infrastructure for physical intelligence.

This story should be used in `docs/deepdive/application.md`, `docs/deepdive/one-page-summary.md`, and `docs/deepdive/pitch-outline.md` so leaders can understand why the project matters strategically.

This narrative does not change the technical substance of the bootstrap. The first engineering milestone remains a non-LLM primitive baseline plus Newton verifier, not a broad physical-safety platform.

## Proposed Top-Level Structure

```text
physics-primitive-agent/
  AGENTS.md
  README.md
  pyproject.toml
  requirements.txt
  .gitignore
  docs/
    index.md
    deepdive/
      application.md
      pitch-outline.md
      review-qa.md
      one-page-summary.md
    design/
      project-scope.md
      system-architecture.md
      milestone-plan.md
      evaluation-plan.md
    reference/
      literature-map.md
      newton-notes.md
      related-work-notes.md
    records/
      2026-05-14-project-bootstrap.md
    tmp/
      DeepDive_usage_guide.md
      newton_llm_primitive_first_research_review.md
    superpowers/
      specs/
      plans/
  src/
    npc_compiler/
      __init__.py
      contracts.py
      config.py
      cli.py
  tests/
    test_contracts.py
    test_cli.py
  configs/
    deepdive/
      mvp.yaml
    experiments/
      phase0_baseline.yaml
  scripts/
    validate_docs.py
  experiments/
    README.md
    registry.yaml
  assets/
    README.md
  reports/
    README.md
  archive/
    README.md
```

## Documentation System

The documentation system follows the spirit of `genesis-llm` but adapts it to a pre-DeepDive project.

### `docs/index.md`

The project documentation hub. It should provide quick navigation, project status, and the current recommended next action.

### `docs/deepdive/`

The primary folder for the current objective.

- `application.md`: direct DeepDive application draft, written around problem, strategic relevance to physical safety constraints, technical route, current evidence, next plan, and requested support.
- `pitch-outline.md`: 20-30 minute presentation outline matching the DeepDive reporting flow: core problem, strategic story, technical route, current preparation, next milestones, support request.
- `review-qa.md`: reviewer question preparation organized around Taste, Benchmark, User Experience, and Value Delivering.
- `one-page-summary.md`: concise reviewer-facing summary for technical reviewers and leaders.

### `docs/design/`

Design documents for later execution.

- `project-scope.md`: what this project is and is not.
- `system-architecture.md`: future NPC Compiler architecture.
- `milestone-plan.md`: 0-4, 4-8, 8-12, and 12-24 week route.
- `evaluation-plan.md`: baselines, metrics, benchmark assets, and go/no-go criteria.

### `docs/reference/`

Reference notes distilled from the current long review:

- `literature-map.md`: CPD, V-HACD, CoACD, VisACD, PrimitiveAnything, MeshLLM, ResFit, simulator-in-the-loop LLM work.
- `newton-notes.md`: Newton API assumptions and integration notes.
- `related-work-notes.md`: claim boundaries and differentiation.

### `docs/records/`

Append-only progress records similar to `genesis-llm/docs/records/`.

The first record documents the bootstrap: what was created, what remains deliberately non-implemented, and the current DeepDive-first status.

## Engineering Skeleton

The Python package should be minimal and honest.

### `src/npc_compiler/contracts.py`

Defines typed data contracts for the future compiler:

- `TaskType`
- `PrimitiveType`
- `FallbackType`
- `CompileConfig`
- `PrimitiveSpec`
- `FallbackSpec`
- `CollisionPackage`
- `CompileReport`

These contracts make the project concrete without requiring geometry fitting or Newton integration in the first commit.

### `src/npc_compiler/config.py`

Provides config loading for YAML files. It should parse repository config files into `CompileConfig` or lightweight dictionaries.

### `src/npc_compiler/cli.py`

Provides a small `npc-compile` CLI. In this phase it should support `--help` and a dry-run validation path that reads a config and prints the intended compile request. It must not claim to compile real collision geometry yet.

### Tests

Tests should cover:

- Contract defaults and serialization-friendly output.
- CLI help.
- Dry-run config validation.

The tests should prove the skeleton is coherent, not that the research system works.

## Config System

Configs mirror `genesis-llm/configs/` but stay small:

- `configs/deepdive/mvp.yaml`: the DeepDive MVP target config.
- `configs/experiments/phase0_baseline.yaml`: future Phase 0 baseline harness config.

These files are documentation and future run inputs. They should avoid large or environment-specific paths.

## Evidence Boundaries

The repository must maintain strict claim boundaries:

- Current status: proposal and project bootstrap.
- No implemented primitive fitting.
- No Newton verifier results.
- No benchmark metrics.
- No LLM/VLM ablation evidence.

All DeepDive materials should phrase the work as a pre-research proposal with a practical first milestone: non-LLM baseline plus Newton verifier.

Leadership-facing language should connect the work to AI model physical safety constraints, but should not inflate current evidence into safety guarantees.

## Initial README Positioning

The README should say:

- The project proposes a Newton Primitive Collision Compiler.
- The current goal is DeepDive application and project bootstrap.
- The recommended technical claim is primitive-first, simulation-verified, fallback-aware collision asset compilation.
- The unsafe claim is complete replacement of convex decomposition.
- Quick start is limited to installing the package and running skeleton validation/tests.

## Agent Rules

`AGENTS.md` should encode repository-specific rules:

- DeepDive materials are the active priority.
- Source code lives under `src/npc_compiler/`.
- Do not implement research algorithms in `docs/tmp/`.
- Do not claim experimental results unless backed by records and artifacts.
- Keep configs under `configs/`.
- Do not commit large assets, generated reports, binary meshes, videos, or local environments.

## Bootstrap Implementation Strategy

1. Initialize git if the directory is not already a repository.
2. Add the full skeleton with conservative files.
3. Keep existing `docs/tmp/` files untouched.
4. Add minimal tests and a documentation validation script.
5. Run verification:
   - `python scripts/validate_docs.py`
   - `PYTHONPATH=src python -m pytest`
6. Commit the bootstrap if verification passes.

## Non-Goals For This Bootstrap

- No real mesh processing.
- No Newton API calls.
- No CoACD or V-HACD invocation.
- No LLM/VLM integration.
- No benchmark execution.
- No paper LaTeX tree.
- No generated images, videos, or large assets.

## Success Criteria

The bootstrap is successful when:

- A reviewer or teammate can understand the project from `README.md` and `docs/index.md`.
- DeepDive application materials are easy to edit and present.
- The future engineering path is visible without overclaiming current implementation.
- The repository has a minimal importable Python package and passing skeleton tests.
- The docs clearly separate current proposal evidence from future experimental evidence.
