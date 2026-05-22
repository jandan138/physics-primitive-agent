# System Architecture

Current implementation status: documentation, package skeleton, config/reporting surfaces, USD
asset diagnostics, Newton environment diagnostics, CPD-like smoke paths, and several named Newton
task smokes exist today. The components below describe the intended compiler architecture, not a
completed compiler.

## Environment Readiness And Source Provenance

Records Python executable, interpreter realpath, module provenance, Newton source checkout, GPU
visibility, setup fingerprint, output writability, and repository diagnostic status before any
Newton simulation claim. This is diagnostic provenance, not an environment installer.

## Asset And Robot Intake

Prepares mesh, USD, URDF, MJCF, or other asset descriptions for collision compilation. It records
source, license/provenance, asset hash, units, scale, source frames, connected components, and
robot link/joint structure when present.

## Candidate Generator

Produces candidate collision packages from deterministic primitive heuristics, native approximation
lanes, authored colliders, or CPD-style outputs. Candidate generation is not acceptance.

## Package Guard

Checks finite geometry, primitive budgets, scale anomalies, large-flat or degenerate primitive
classes, compound body-state proxy deltas, and robot link-boundary constraints. For articulated
assets, the guard must reject cross-link primitive merges.

## Newton Checker

Runs simulation probes in Newton under recorded assumptions: source version, solver settings,
hardware, seeds, task templates, and metric definitions. It records body-state behavior, contact
behavior, penetration or jitter, step time, and task labels.

## Articulation Checker

For robot assets, runs link/joint-specific gates: joint tree import, gravity hold, simple scripted
joint trajectory, self-collision sanity, and end-effector pose sanity. These gates are required
before any whole-robot claim.

## Repair/Fallback

Uses checker output to split, merge, expand, shrink, reject, or fall back. Fallback options include
CoACD, V-HACD, SDF, hydroelastic, convex mesh, triangle mesh where valid, authored primitive
colliders, or manual review.

## Export/Report

Writes collision packages and reports with primitives, fallback regions, task labels, source
hashes, config hashes, metrics, failure reasons, and artifact paths. Every package remains
untrusted until checked and reviewed.

## First Milestone

Only the Asset/Robot Intake subset, Candidate Generator, Package Guard, Newton Checker,
Articulation Checker for one robot smoke if available, and Export/Report are needed for the first
proof point.

## Current Non-Goals

No safety guarantee, real-world transfer, deployment readiness, benchmark superiority,
primitive-only sufficiency, full CPD reproduction, or complete replacement of convex decomposition.
