# System Architecture

Current implementation status: only documentation and a package skeleton exist today. The components below describe the intended architecture, not a completed compiler.

## Geometry Preprocessor

Prepares incoming mesh, USD, URDF, or MJCF assets for collision compilation. Responsibilities include source tracking, asset hash capture, unit and scale normalization, mesh cleanup checks, connected-component inspection, coarse region extraction, and task metadata validation.

## Semantic/Task Planner

Defines which contact behavior matters for the asset and task. In the first milestone this is rule-based or config-driven. LLM/VLM semantic planning is deferred until the non-LLM baseline shows value.

## Primitive Proposal Bank

Generates candidate boxes, spheres, capsules, cylinders, cones, and ellipsoids. The first version should be non-LLM and conservative, using simple geometry heuristics and fixed primitive budgets.

## Constrained Optimizer

Fits primitive parameters while respecting task budgets, scale, containment/coverage checks, and shape count limits. It should avoid producing many small primitives that erase the runtime or editability advantage.

## Newton Checker

Runs simulation probes in Newton under recorded assumptions: version, solver settings, hardware, seeds, task templates, and metric definitions. It records runtime, contact behavior, penetration, jitter, task success, and failure traces. The checker is a diagnostic layer, not proof of real-world safety.

## Repair/Fallback

Uses checker output to split, merge, expand, shrink, reject, or fall back. Fallback options include CoACD, V-HACD, SDF, hydroelastic, convex mesh, triangle mesh where valid, manual primitive colliders, or manual review. The system must preserve the nuanced claim: primitive-first and fallback-aware, not a full replacement of convex decomposition.

## Export/Report

Writes collision packages and reports with primitives, fallback regions, task labels, source hashes, config hashes, metrics, failure reasons, and artifact paths. Every package remains untrusted until checked and reviewed.

## First Milestone

Only the Geometry Preprocessor subset, non-LLM Primitive Proposal Bank, minimal Constrained Optimizer, Newton Checker, and Export/Report are needed for the first 0-4 week proof point.

## Current Non-Goals

No safety guarantee, real-world transfer, deployment readiness, benchmark superiority, primitive-only sufficiency, or complete replacement of convex decomposition.
