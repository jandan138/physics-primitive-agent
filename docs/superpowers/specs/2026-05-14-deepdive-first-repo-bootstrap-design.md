# DeepDive-First Repo Bootstrap Design

Date: 2026-05-14

## Goal

Turn `physics-primitive-agent` from a two-document research note directory into a clean, durable project repository that supports the immediate DeepDive application while leaving a disciplined path for later research and engineering.

The first deliverable is not a working primitive collision compiler. The first deliverable is a credible DeepDive-ready repository: clear project framing, reviewer-facing materials, evidence boundaries, and a minimal Python package skeleton that can grow into implementation after approval.

## Current State

At the start of this bootstrap, the project contained:

- `docs/tmp/newton_llm_primitive_first_research_review.md`: the main technical review for a Newton primitive-first collision compiler.
- `docs/tmp/DeepDive_usage_guide.md`: company DeepDive guidance and examples.

It did not contain a git repository, README, package metadata, source tree, tests, configs, scripts, experiment registry, or organized documentation index.

During the design step, git was initialized so planning artifacts can be tracked. The full repository bootstrap is still pending.

## Design Direction

Use a DeepDive-first full skeleton:

- Make the repository look intentional and maintainable from day one.
- Keep DeepDive application materials as the primary surface.
- Add a minimal engineering skeleton to show feasibility and future execution discipline.
- Avoid pretending that research implementation already exists.
- Preserve the existing long-form review documents under `docs/tmp/` until they are later cleaned or archived.

## Strategic Narrative For Leadership

The DeepDive materials should include a leadership-facing story that connects the project to the Physical Intelligence Center's broader strategy.

Thesis: as physical-intelligence models increasingly generate assets, scenes, and robot behaviors, the center needs simulation checks that turn model outputs into physically testable artifacts. Collision geometry is the hidden contract that makes those checks meaningful.

The strategic framing is:

- Physical intelligence systems need AI models that respect physical safety constraints, not only models that generate plausible actions, assets, or plans.
- A physics engine is the executable diagnostic layer for those constraints: under specified simulator assumptions, test scenarios, and metrics, it can help surface candidate penetrations, unstable contacts, unsafe force-transfer patterns, false collision-clearance assumptions, and task-level physical failures before expensive physical trials or deployment decisions.
- Collision geometry is one of the lowest-level safety interfaces between AI-generated worlds, robot policies, and simulation. If the collision proxy is wrong, downstream policy training, evaluation, and safety claims become untrustworthy.
- For example, an under-conservative collision proxy can let a policy learn motions that pass through objects; an over-conservative proxy can reject valid grasps or navigation paths. In both cases, the model may look capable in simulation while the physical interpretation is wrong.
- A primitive-first, simulation-checked, fallback-aware collision compiler is therefore not just an asset conversion tool. It is one concrete infrastructure component for detecting collision-proxy failures in physical-intelligence workflows.

This story should be used in `docs/deepdive/application.md`, `docs/deepdive/one-page-summary.md`, and `docs/deepdive/pitch-outline.md` so leaders can understand why the project matters strategically.

This narrative does not change the technical substance of the bootstrap. The first engineering milestone is deliberately narrow: build a non-LLM primitive baseline and Newton checker so the team can measure whether primitive collision proxies can be generated, checked, and rejected before adding LLM/VLM components.

## Proposed Top-Level Structure

```text
physics-primitive-agent/
  AGENTS.md
  CONTRIBUTING.md
  README.md
  pyproject.toml
  requirements.txt
  .gitignore
  .python-version
  Makefile
  docs/
    index.md
    deepdive/
      README.md
      application.md
      evidence-status.md
      message-map.md
      pitch-outline.md
      review-qa.md
      one-page-summary.md
    design/
      project-scope.md
      system-architecture.md
      research-roadmap.md
      evaluation-plan.md
      benchmark-protocol.md
    reference/
      claim-boundaries.md
      literature-map.md
      newton-notes.md
      related-work-notes.md
    records/
      README.md
      2026-05-14-project-bootstrap.md
    tmp/
      README.md
      DeepDive_usage_guide.md
      newton_llm_primitive_first_research_review.md
    superpowers/
      README.md
      specs/
      plans/
  src/
    primitive_collision_compiler/
      __init__.py
      contracts.py
      config.py
      cli.py
  tests/
    fixtures/
      dry_run_mvp.yaml
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

- `README.md`: navigation and editing guidance for DeepDive-facing materials.
- `message-map.md`: canonical strategic message source so leadership-facing wording does not drift across files.
- `application.md`: direct DeepDive application draft, written around problem, strategic relevance to physical safety constraints, technical route, current evidence, next plan, and requested support.
- `evidence-status.md`: current supported, unsupported, and future-evidence claims.
- `pitch-outline.md`: 20-30 minute presentation outline matching the DeepDive reporting flow: core problem, strategic story, technical route, current preparation, next milestones, support request.
- `review-qa.md`: reviewer question preparation organized around Taste, Benchmark, User Experience, and Value Delivering.
- `one-page-summary.md`: concise reviewer-facing summary for technical reviewers and leaders.

### `docs/design/`

Design documents for later execution.

- `project-scope.md`: what this project is and is not.
- `system-architecture.md`: future Newton Primitive Collision Compiler architecture.
- `research-roadmap.md`: 0-4, 4-8, 8-12, and 12-24 week research route.
- `evaluation-plan.md`: baseline x task x metric matrix, phase gates, effect-size reporting, and go/no-go criteria.
- `benchmark-protocol.md`: benchmark asset categories, licenses, scale normalization, task templates, splits, and failure taxonomy.

### `docs/reference/`

Reference notes distilled from the current long review:

- `claim-boundaries.md`: canonical safe/unsafe claim register.
- `literature-map.md`: CPD, V-HACD, CoACD, VisACD, PrimitiveAnything, MeshLLM, ResFit, simulator-in-the-loop LLM work.
- `newton-notes.md`: Newton API assumptions and integration notes.
- `related-work-notes.md`: claim boundaries and differentiation.

### `docs/records/`

Append-only progress records similar to `genesis-llm/docs/records/`.

`docs/records/README.md` should define the record template: Date, Status, Changes, Verification, Artifacts, Claim Impact, and Next Action. The first record documents the bootstrap: what was created, what remains deliberately non-implemented, and the current DeepDive-first status.

### `docs/tmp/`

Temporary source intake only. The two existing long documents remain untouched during bootstrap, but `docs/tmp/README.md` should state that this folder is not a durable knowledge layer. Later cleanup can move source materials into `docs/reference/source-materials/` or `archive/`.

### `docs/superpowers/`

Internal agent workflow artifacts. `docs/superpowers/README.md` should explain that `specs/` stores design rationale and `plans/` stores execution checklists. These files should not be the primary reviewer-facing documentation.

## Engineering Skeleton

The Python package should be minimal and honest.

The package should use the explicit import name `primitive_collision_compiler`. `NPC Compiler` can remain an internal shorthand for Newton Primitive Collision Compiler, but public package metadata and CLI help must spell this out.

### `src/primitive_collision_compiler/contracts.py`

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

### `src/primitive_collision_compiler/config.py`

Provides config loading for YAML files. It should parse repository config files into `CompileConfig` or lightweight dictionaries.

### `src/primitive_collision_compiler/cli.py`

Provides a small `npc-compile` CLI. In this phase it should support `--help` and a dry-run validation path that reads a config and prints the intended compile request. It must spell out `Newton Primitive Collision Compiler` in help text and must not claim to compile real collision geometry yet.

### Tests

Tests should cover:

- Contract defaults and serialization-friendly output.
- CLI help.
- Dry-run config validation.
- Claim-boundary linting for DeepDive docs.

The tests should prove the skeleton is coherent, not that the research system works.

Dry-run tests should use `tests/fixtures/dry_run_mvp.yaml`, not the canonical proposal config, so tests do not become brittle as DeepDive materials evolve.

## Config System

Configs mirror `genesis-llm/configs/` but stay small:

- `configs/deepdive/mvp.yaml`: the DeepDive MVP target config.
- `configs/experiments/phase0_baseline.yaml`: future Phase 0 baseline harness config.

These files are documentation and future run inputs. They should avoid large or environment-specific paths.

`pyproject.toml` should be the source of truth for package metadata, Python version, console scripts, pytest config, ruff config, and optional dev dependencies. `requirements.txt` can remain as a simple compatibility install file, but it should not become an independent dependency source.

## Evaluation Plan Requirements

`docs/design/evaluation-plan.md` should promote the strongest material from the long technical review into a formal validation contract. It should include:

- Baselines: single convex hull, bounding box/sphere, V-HACD, CoACD, CPD-like primitive decomposition, VisACD when available, manual primitive colliders, SDF/hydroelastic oracle, original triangle mesh where valid, and Newton-native `approximate_meshes()` modes.
- Tasks: drop, stack, slide, sphere rain, roll, grasp proxy, container, hole traversal, and explicit precision-task rejection.
- Metrics: step time, narrowphase time, broadphase pair count, contact count p95, penetration, jitter, contact normal error, task success, primitive/hull count, fallback surface ratio, generation failure rate, and human edit time.
- Reporting: paired asset-level comparisons, confidence intervals or effect sizes where enough samples exist, seeds/config snapshots, Newton version, hardware, solver settings, asset hashes, baseline parameters, and artifact paths.
- Phase gates: Phase 0 reproduces baselines on about 20 assets; Phase 1 evaluates the non-LLM primitive baseline on about 50 assets; Phase 2 adds verifier and repair; Phase 3 adds LLM/VLM only after non-LLM value is demonstrated.
- No-go criteria: LLM no measurable gain, primitive count exceeds CoACD hull count without runtime/task benefit, fallback dominates the output, Newton checker is unstable, or precision tasks are incorrectly accepted as primitive-only.

`docs/deepdive/review-qa.md` should answer the DeepDive guide dimensions directly: Taste, Benchmark, User Experience, and Value Delivering.

## Safety And Claim Boundaries

The repository must maintain strict claim boundaries:

- Current status: proposal and project bootstrap.
- No implemented primitive fitting.
- No Newton verifier results.
- No benchmark metrics.
- No LLM/VLM ablation evidence.
- No physical-safety guarantee, real-world transfer guarantee, deployment readiness, complete false-negative detection, benchmark superiority, or primitive-only sufficiency claim.

All DeepDive materials should phrase the work as a pre-research proposal with a practical first milestone: non-LLM baseline plus Newton verifier.

Leadership-facing language should connect the work to AI model physical safety constraints, but should not inflate current evidence into safety guarantees.

The term `simulation-checked` is preferred in current materials. If `simulation-verified` is used, it must be defined narrowly: specific Newton checks passed under named assumptions, tasks, metrics, and versions. It does not mean collision correctness, real-world safety, certification, or absence of unsafe behavior.

Generated collision packages should be treated as safety-affecting artifacts. Every future `CollisionPackage` remains untrusted until validated, must carry provenance, and must not be used for robot deployment, policy-training safety claims, or safety certification without independent review.

## Provenance And Regression Expectations

Future generated outputs and experiment records should capture:

- input asset hash and source/license;
- config hash and compiler version/git commit;
- Newton/dependency versions, hardware, and solver settings;
- deterministic seed where applicable;
- fallback reason and fallback region metadata;
- metrics, validation status, timestamp, and artifact path.

Future regression tests should include golden fixtures, deterministic dry-run outputs, fallback behavior, penetration/contact stability thresholds, false-negative checks, and tolerance-based Newton checker comparisons.

## Initial README Positioning

The README should say:

- The project proposes a Newton Primitive Collision Compiler.
- The current goal is DeepDive application and project bootstrap.
- The recommended technical claim is primitive-first, simulation-checked, fallback-aware collision asset compilation.
- The unsafe claim is complete replacement of convex decomposition.
- Quick start is limited to installing the package and running skeleton validation/tests.

## Agent Rules

`AGENTS.md` should encode repository-specific rules:

- DeepDive materials are the active priority.
- Source code lives under `src/primitive_collision_compiler/`.
- Do not implement research algorithms in `docs/tmp/`.
- Do not claim experimental results unless backed by records and artifacts.
- Keep configs under `configs/`.
- Do not commit large assets, generated reports, binary meshes, videos, or local environments.
- Treat `docs/reference/claim-boundaries.md` as the canonical claim register.

## Bootstrap Implementation Strategy

1. Initialize git if the directory is not already a repository.
2. Add the full skeleton with conservative files.
3. Keep existing `docs/tmp/` files untouched.
4. Add minimal tests and a documentation validation script.
5. Run verification:
   - `python scripts/validate_docs.py`
   - `python -m pip install -e ".[dev]"`
   - `python -m pytest`
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
- The DeepDive materials include a concrete 4/8/12-week validation story with baselines, metrics, no-go criteria, and claim boundaries.
