# Newton Primitive Collision Compiler

## Overview

This repository is a DeepDive-first bootstrap for a simulation-checked primitive collider
compiler. The current research direction is not to reproduce the 2026 CPD paper as the main
contribution. CPD-style primitive decomposition is treated as one candidate generator. The
proposal is to add a Newton-executed diagnostic layer that decides whether a generated primitive
package is acceptable for physical simulation, robot articulation, and task behavior.

## Current Direction

The main thesis is:

> Primitive collider generation should not stop at geometric fitting. A primitive package should be
> accepted only after named physics-engine diagnostics check body state, contact behavior,
> articulation integrity, and task operation under recorded settings.

This positions the project around a compiler/checker loop:

1. generate or import primitive collider candidates;
2. preserve provenance, scale, link boundaries, and fallback options;
3. run Newton diagnostics for body-state, contact, and task behavior;
4. reject, fall back, or mark packages for review when diagnostics expose risk.

The strongest current evidence is the capped bed/Franka cylinder mechanism slice. The bed failure
is now recorded as a full-compound package effect: one large flat cylinder changes package
COM/inertia body-state enough to leave residual drop/settle speed above the gate. The same records
show that recorded Franka cylinder packages pass in their much smaller package context. This is
evidence for simulation-checked selection, not broad cylinder stability or whole-robot validation.

## How This Differs From CPD 2026

`Convex Primitive Decomposition for Collision Detection` already studies automatic mesh-to-primitive
collider generation for rigid-body simulation. This project should not claim novelty in automatic
primitive collider generation itself.

The intended contribution is downstream of candidate generation:

- CPD-style work asks whether a primitive package is compact, editable, geometrically plausible,
  and efficient.
- This project asks whether that package remains physically usable after it enters Newton, including
  body-state accounting, contact behavior, link/joint constraints, and task-level operation.

The CPD paper is therefore a related baseline and candidate source, not the project identity.

## DeepDive Package

Start with:

- [DeepDive message map](docs/deepdive/message-map.md)
- [DeepDive application draft](docs/deepdive/application.md)
- [Evidence status](docs/deepdive/evidence-status.md)
- [Claim boundaries](docs/reference/claim-boundaries.md)
- [Simulation-checked direction note](docs/reference/simulation-checked-primitive-collider-direction.md)

The current ask is milestone-based support for a narrow proof point, not acceptance of completed
research.

## Current Evidence Boundary

Supported today:

- DeepDive framing, config examples, package skeleton, dry-run/reporting surfaces, USD asset intake
  diagnostics, environment-readiness diagnostics, CPD-like geometry smoke paths, and several named
  Newton diagnostic smokes.
- A Phase 0 GRScenes rigid-asset intake manifest with five repo-local materialized USD dependency
  closures, plus a scoped Newton diagnostic follow-up over bounding-primitive, CPD-style, and CoACD
  convex-mesh candidate lanes. The latest follow-up includes stack-or-slide probes, V-HACD runtime
  evidence for all five selected rigid assets, recorded V-HACD probe failures on bowl/cup/tray,
  one Franka link-aware package generation record with zero cross-link merges, and one Franka USD
  articulation smoke; it is not a complete Phase 0 benchmark or broad
  generalization result.
- A dated capped bed/Franka mechanism audit explaining why the recorded bed cylinder package fails
  while recorded Franka cylinder packages pass.
- An explicitly opt-in package body-state guard task path that falls back only the flagged bed
  package while keeping the unflagged Franka cylinder package in the recorded task smoke.
- A preliminary bed-aligned collision-only contact-throughput microbenchmark where Newton-native
  boxes achieved 2.21x generated-contact throughput versus same-count convex64 mesh proxies in
  one pressure scene.

Not supported today:

- broad benchmark superiority;
- full-simulation speedup;
- full CPD paper reproduction;
- calibrated default selector policy;
- complete Phase 0 coverage with broader pass criteria and generated-package robot task checks;
- complete collision-quality validation;
- whole-robot articulated Franka performance evidence;
- deployment readiness, real-world transfer, or safety certification.

## Phase 0 Proof Point

The next DeepDive-facing proof point should shift from "primitive-first only" to
"simulation-checked and robot-operation-aware":

- add meshless-link policy and generated-package robot task probes;
- triage recorded V-HACD probe failures while keeping them visible as diagnostic failures;
- keep primitive merging link-aware and forbid cross-joint merges;
- run Newton drop/settle, contact stress, and body-state diagnostics;
- add articulation smoke checks: joint tree import, gravity hold, simple joint trajectory,
  self-collision sanity, and end-effector pose sanity;
- compare against simple baselines and CPD/CoACD/V-HACD when available;
- report fallback decisions instead of hiding failed primitive packages.

## Commands

Install locally:

```sh
python -m pip install -e ".[dev]"
```

Install Phase 0 baseline dependencies, including CoACD and V-HACD:

```sh
python -m pip install -e ".[dev,phase0]"
```

Run fast tests:

```sh
make test
```

Run CPD paper offline contract tests:

```sh
make test-paper
```

Run the pre-merge validation lane:

```sh
make validate-full
```

Use `make test` for normal development. Use `make test-paper` when changing CPD paper offline
contracts or report gates. Use `make validate-full` before merging.

Validate docs and claims with the fast lane:

```sh
make validate
```

Whitespace check:

```sh
git diff --check
```

## Paper Workspace

Multi-venue LaTeX sources for the ACCV-facing draft:

```sh
cd paper && make list
cd paper && make accv      # primary draft
cd paper && make all       # all venue wrappers
```

Shared manuscript sections live in `paper/shared/`; venue wrappers live in `paper/venues/`.
Evidence registries: `paper/shared/evidence/claims.yaml` and `results_manifest.yaml`.

## Repository Layout

- `paper/`: multi-venue LaTeX paper (ACCV primary; arXiv/ECCV/NeurIPS transfer candidates).
- `docs/deepdive/`: application-facing framing and reviewer materials.
- `docs/design/`: roadmap, architecture, evaluation, and benchmark protocols.
- `docs/reference/`: claim boundaries, related-work notes, and direction references.
- `docs/records/`: dated evidence and decision records.
- `configs/`: DeepDive and experiment configuration examples.
- `src/primitive_collision_compiler/`: current package and diagnostic code.
- `tests/`: tests for advertised command surfaces.
- `assets/`, `reports/`, `archive/`: artifact boundaries and generated-output policy.

## Current Non-Goals

- No finished production compiler claim.
- No claim that primitive colliders replace convex decomposition.
- No broad robot-operation evidence yet; current Franka evidence includes a first link-aware
  package record but not whole-robot articulated performance validation.
- No broad benchmark superiority or full-simulation speedup claim.
- No deployment, real-world transfer, or safety guarantee.
