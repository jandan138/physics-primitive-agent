# Project Scope

## Purpose

The project proposes a Newton Primitive Collision Compiler: a primitive-first, simulation-checked, fallback-aware collision asset compiler. The current repository exists to support a DeepDive application and to define the first implementation milestone.

## In Scope

- DeepDive application and reviewer materials.
- A non-LLM primitive baseline as the first engineering milestone.
- Newton diagnostic checker design for named tasks and metrics.
- Baseline comparison against existing collision approximation methods.
- Explicit fallback to CoACD, V-HACD, SDF, hydroelastic, convex mesh, triangle mesh where valid, or manual review.
- Provenance, reporting, and claim-boundary discipline.

## Out Of Scope Today

- Primitive fitting implementation.
- Newton checker execution.
- Benchmark results.
- LLM/VLM primitive generation, planning, repair, or evaluation.
- Real robot deployment.
- Safety certification.

## Strategic Boundary

The leadership story connects the project to AI model physical safety constraints: physics engines provide executable diagnostic layers, and collision proxies are critical inputs to those diagnostics. This does not convert simulator checks into safety guarantees.

## First Milestone

The first 0-4 week milestone is non-LLM primitive baseline plus Newton diagnostic checker. The milestone should measure whether primitive-first compilation is worth expanding before LLM/VLM is introduced.

## Current Non-Goals

No safety guarantee, real-world transfer, deployment readiness, benchmark superiority, primitive-only sufficiency, or complete replacement of convex decomposition.
