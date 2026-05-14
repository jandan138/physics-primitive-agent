# Newton Primitive Collision Compiler

## Current Status

This repository is a proposal/bootstrap for a DeepDive-first Newton primitive collision
compiler. It does not implement real mesh processing yet, and the `src/` package and test
suite are intentionally deferred to later bootstrap tasks.

## Strategic Framing

The project explores whether primitive collision representations can be compiled from
research-backed descriptions, source notes, and simulation-checked records before committing
to a production mesh-processing implementation. The bootstrap phase keeps claims narrow so
the repository can separate documented intent from executable behavior.

## Recommended Claim

Use this framing for current work:

The Newton Primitive Collision Compiler is a bootstrap-stage proposal for a DeepDive-first
workflow that will compile Newton primitive collision artifacts from documented, reviewed,
and simulation-checked inputs.

## Unsafe Claims

Do not claim that this repository currently:

- Implements a working collision compiler.
- Performs real mesh processing.
- Produces production-ready Newton collision primitives.
- Provides simulation-verified results. In this repository, simulation-checked means records
  have been checked against planned or documented simulation evidence; simulation-verified
  would imply a stronger validation standard that is not established here.

## Repository Layout

- `docs/`: research notes, source records, and bootstrap planning materials.
- `pyproject.toml`: project metadata, packaging configuration, pytest configuration, and
  Ruff configuration.
- `requirements.txt`: editable development install entry point.
- `Makefile`: common development commands.

Future source code is expected under `src/primitive_collision_compiler/`.

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

## DeepDive Materials

DeepDive source notes and bootstrap records live under `docs/`. These materials are the
current basis for project framing, claim boundaries, and future implementation plans.

## Non-Goals For Current Bootstrap

- No real mesh processing implementation.
- No source package implementation.
- No generated collision artifact pipeline.
- No claim of production readiness.
