# Simulation-Checked Primitive Collider Direction

## Purpose

This note records the current project direction after the capped bed/Franka cylinder mechanism
work. It should guide DeepDive-facing docs and future implementation goals.

## Core Shift

The project should not be framed as "we invented automatic primitive collider generation."
Adjacent work, including CPD-style primitive decomposition, already covers automatic primitive
collider generation for collision detection and rigid-body simulation.

The sharper contribution is:

> Generated primitive collider packages should be accepted only after physics-engine diagnostics
> check body state, contact behavior, and robot operation under recorded settings.

## Why The Bed/Franka Result Matters

The recorded capped bed/Franka cylinder story shows the difference between geometry-only
candidate selection and simulation-checked acceptance:

- the bed target cylinder passes as an isolated primitive;
- the full bed package with that large flat cylinder fails the recorded drop/settle gate;
- COM/inertia body-state sensitivity is the strongest recorded mechanism;
- recorded Franka cylinder packages pass in their smaller package context;
- an opt-in package body-state guard falls back only the flagged bed package while preserving the
  unflagged Franka cylinder package.

This is not a broad cylinder result. It is a concrete example of why package context matters.

## Why The Contact-Throughput Result Matters

The bed-aligned contact-throughput microbenchmark records the complementary positive case: when a
primitive package is accepted as Newton-native boxes, it can preserve access to primitive collision
paths. In one collision-only pressure scene, the native 32-box package achieved 2.21x higher
generated-contact throughput than same-count 64-vertex convex-mesh proxies.

This is not a full simulation speedup or broad benchmark result. It is a scoped performance hook
for the same compiler principle: accept primitive packages when Newton diagnostics support them,
and fall back when they do not.

## Research Position

Candidate generation layer:

- deterministic primitive heuristics;
- authored colliders;
- CPD-style primitive decomposition;
- CoACD/V-HACD/convex decomposition;
- Newton-native approximations.

Acceptance layer:

- body-state risk guard;
- drop/settle and contact stress;
- contact/floor sanity;
- link-boundary audit for robot assets;
- articulation smoke gates;
- fallback or manual-review decision.

The project contribution should live in the acceptance layer and in the reproducible compiler
contract between candidate generation and Newton execution.

## Robot Extension

For robot assets, primitive merging must be articulation-aware:

- do not merge primitives across different links;
- preserve joint tree and link frames;
- record whether collision proxies affect dynamic inertial properties;
- run joint tree import, gravity hold, simple joint trajectory, self-collision sanity, and
  end-effector pose sanity before any whole-robot claim.

Current Franka evidence does not yet prove whole-robot behavior. A new articulation-specific goal
is required.

## Claim Boundary

Allowed now: simulation-checked direction, capped bed/Franka diagnostic mechanism, opt-in package
body-state guard task-path evidence, and the preliminary bed-aligned collision-only
contact-throughput microbenchmark.

Not allowed now: do not claim broad benchmark superiority, full-simulation speedup, full CPD
reproduction, default selector policy, broad robot operation, deployment readiness, real-world
transfer, or a safety proof.
