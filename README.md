# Newton Primitive Collision Compiler

## Overview

The Newton Primitive Collision Compiler is a bootstrap-stage repository for a future
DeepDive-first workflow around Newton primitive collision artifacts.

## Current Status

This repository is a proposal/bootstrap for a DeepDive-first Newton primitive collision
compiler. It now includes a geometry-only CPD-like face-merge smoke path over USD meshes, plus
config dry-runs, USD asset-open smoke diagnostics, Newton source diagnostics, and environment
readiness checks. It also includes a contact-only Newton canary for representative mapped primitive
types, plus named drop/settle and sphere-rain contact-density proxy Newton task smokes for the
capped bed CPD-like package. A separate Franka/simple robot smoke opens the local Franka USD and
runs capped first-mesh CPD-like geometry proposals. An opt-in CPD-like component-merge gate now
reports disconnected-component merge candidates and normalized excess-volume accounting while
remaining below full CPD reproduction. An offline CPD-like objective report now summarizes
paper-aligned surrogate terms for that baseline without claiming collision quality. A synthetic
objective comparison now reuses that report on three deterministic toy meshes to inspect
topology-only versus component-merge accounting without adding benchmark evidence. A focused
CPD-like cost-guided merge-search smoke now uses AABB-normalized merge-excess as a
decision-making cost on one deterministic toy mesh and reports old/new diagnostic accounting. See
`docs/reference/cpd-like-face-merge-explainer.md` for the
plain-language boundary between the current baseline and a full CPD paper reproduction. See
`docs/reference/cpd-paper-story-status.md` for where the repository sits in the broader CPD paper
story. See `docs/reference/cpd-objective-report-alignment.md` for why the objective report is
design-aligned with the paper story but not yet a paper-faithful objective implementation. The
clean local Newton Python environment has recorded readiness evidence, but the
repository does not yet produce benchmark results, broad asset/task evidence, whole-robot
collider-quality evidence, real contact-stress measurement, or a production collision compiler.

## Strategic Framing

The project intends to explore whether primitive collision representations can be compiled
from research-backed descriptions, source notes, and Newton-diagnostic-checker-planned records
before committing to a production mesh-processing implementation. The bootstrap phase keeps
claims narrow so the repository can separate documented intent from executable behavior.

## Safe Claim

Use this framing for current work:

The Newton Primitive Collision Compiler is a bootstrap-stage proposal for a DeepDive-first
future workflow that intends to explore Newton primitive collision artifacts from documented,
reviewed, and Newton-diagnostic-checker-planned inputs.

## Unsafe Claim

Do not claim that this repository currently:

- Implements a finished collision compiler.
- Performs complete production mesh processing.
- Produces production-ready Newton collision primitives.
- Provides simulation-verified results. Use "simulation-checked" only when a dated record links a
  generated package to a named task-level Newton diagnostic probe, settings, asset, environment,
  and report. Contact-only canary records do not qualify. Until then use "geometry-only",
  "contact-only Newton canary", "environment-readiness", or "Newton-checker-planned".

## Repository Layout

- `docs/`: research notes, source records, and bootstrap planning materials.
- `configs/`: DeepDive and Phase 0 config examples.
- `scripts/`: repository maintenance and validation commands.
- `src/primitive_collision_compiler/`: installable package with CLI, diagnostics, and the
  geometry-only CPD-like smoke path.
- `tests/`: bootstrap tests for currently advertised command surfaces.
- `assets/`, `experiments/`, `reports/`, `archive/`: artifact boundaries and registries.
- `AGENTS.md`: rules for future agentic work in this repository.
- `pyproject.toml`: project metadata, packaging configuration, pytest configuration, and
  Ruff configuration.
- `requirements.txt`: editable development install entry point.
- `Makefile`: common development commands.

## Quick Start

Install the project in editable development mode:

```sh
python -m pip install -e ".[dev]"
```

Run test collection:

```sh
python -m pytest --collect-only
```

Run the documented make targets as they become available:

```sh
make install
make test
make docs-check
make validate
```

At this stage `docs-check` enforces required governance docs, claim-boundary linting, and local
Markdown link checks.

## DeepDive Navigation

DeepDive source notes and bootstrap records live under `docs/`. These materials are the
current basis for project framing, claim boundaries, and future implementation plans.

## Current Non-Goals

- No production mesh-processing or collision-compiler implementation.
- No broad task-level Newton simulation coverage yet; current task smokes are limited to the
  recorded capped bed drop/settle and sphere-rain contact-density proxy diagnostics.
- No whole-robot collider-quality or articulated-dynamics evidence; the Franka path is import and
  capped first-mesh geometry smoke only.
- No full CPD paper reproduction; the component-merge gate and objective report are restricted
  CPD-like baseline diagnostics, and the cost-guided merge-search smoke is a restricted synthetic
  algorithmic smoke slice.
- No generated collision artifact pipeline.
- No claim of production readiness.
