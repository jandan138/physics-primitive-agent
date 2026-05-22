# Project Scope

## Purpose

The project proposes a Newton Primitive Collision Compiler: a simulation-checked, fallback-aware
primitive collider compiler. The repository exists to support a DeepDive application and define the
first evidence-producing milestone.

The project is not centered on claiming a full CPD paper reproduction. CPD-style primitive
decomposition is a related generator and baseline.

## In Scope

- DeepDive application and reviewer materials.
- Deterministic primitive candidate generation as the first engineering baseline.
- Newton diagnostics for body-state, contact, and task behavior.
- Link-aware robot package constraints for articulated assets.
- Articulation smoke checks when a robot asset is in scope.
- Baseline comparison against existing collision approximation methods.
- Explicit fallback to CoACD, V-HACD, SDF, hydroelastic, convex mesh, triangle mesh where valid,
  authored colliders, or manual review.
- Provenance, reporting, and claim-boundary discipline.

## Out Of Scope Today

- Production primitive fitting and collision package generation.
- Broad benchmark-suite results or full-simulation speedup claims.
- Calibrated default selector policy.
- Whole-robot Franka performance validation.
- LLM/VLM primitive generation, planning, repair, or evaluation.
- Real robot deployment.
- Safety certification.

## Strategic Boundary

The leadership story connects the project to AI model physical constraints: physics engines provide
executable diagnostics, and collision packages are critical inputs to those diagnostics. Simulator
checks remain scoped observations under named assumptions; do not claim safety guarantees.

## First Milestone

The first milestone is a non-LLM candidate-generator plus Newton checker loop. It should measure
whether body-state, contact, and articulation diagnostics catch failures that geometry-only
primitive selection would miss.

## Current Non-Goals

No safety guarantee, real-world transfer, deployment readiness, broad benchmark superiority,
full-simulation speedup, primitive-only sufficiency, full CPD reproduction, or complete replacement
of convex decomposition.
