# Benchmark Protocol

This protocol defines how future evidence should be collected for the Newton Primitive Collision
Compiler. It exists before benchmark execution so the project does not retrofit metrics to
outcomes.

The benchmark is a scoped diagnostic: it makes candidate collision-package failures observable in
Newton, but it does not certify real-world safety.

## Phase 0 Asset Subset

The current Phase 0 rigid-asset subset is tracked in `assets/manifests/phase0_assets.yaml` and
materialized into ignored repo-local mirrors. It currently contains:

- one simple rigid prop;
- one stackable object;
- one contact-affordance object;
- one container/bowl;
- one precision negative control.

The articulated robot smoke asset remains separate and should be added only if licensing and
runtime setup are reproducible.

## Robot Package Rules

For articulated assets:

- preserve the source joint tree;
- preserve link frames and body identities;
- forbid primitive merges across link/joint boundaries;
- record whether collision proxies are allowed to affect dynamic inertial properties;
- run articulation smoke before any whole-robot claim.

## Phase 0 Executable Protocol

| Probe | Initial Conditions | Solver And Duration | Seeds | Required Metrics | Pass/Fail Interpretation |
|---|---|---|---|---|---|
| body-state/drop-settle | asset above static plane; gravity enabled; zero initial velocity | Newton settings recorded in config, 2 s target duration unless overridden | 3 | body-state delta, final speed, contact count, jitter or penetration | passes if run completes and labels rest/contact failure modes |
| sphere rain/contact stress | fixed or seeded sphere pattern above/around asset | Newton settings recorded in config, 2 s target duration unless overridden | 3 | contact count p95, step time, jitter or penetration | passes if false clearances, blocked openings, or excessive contacts are observable when present |
| collision-only contact throughput | fixed or seeded probe pattern around asset; no dynamics integration | Newton collision pipeline only, repeated collide calls with warmup and repeats | 3-5 | contacts per second, microseconds per contact, wall time, contacted probe count | supports scoped throughput evidence only; does not imply full simulation speedup |
| stack or slide | asset on static plane or support; optional lateral impulse | Newton settings recorded in config | 3 | displacement, contact count, jitter or penetration | passes if support/slide behavior is measurable and labeled |
| link-boundary audit | robot asset with source link/joint graph | compile/check only | 1 | cross-link merge count, per-link primitive count | passes only if cross-link merges are zero |
| articulation smoke | robot loaded with generated package | Newton settings recorded in config | 1-3 | joint tree import, gravity-hold drift, trajectory completion, self-collision sanity, end-effector pose error | passes if the robot remains a valid articulated system under the recorded gates |
| precision rejection | peg/hole, thin-wall, gear, slot, or thread-like asset-task pair | compile/check; simulation optional | 1 | rejection/fallback decision and reason | passes only if primitive-only output is rejected or locally falls back |

Phase 0 should not claim that these thresholds certify correctness. The goal is executable
diagnostics and reportable failure modes.

## Later Candidate Tasks

Later benchmark task templates include:

- drop;
- stack;
- slide;
- sphere rain;
- roll;
- grasp proxy;
- push or place;
- container interaction;
- hole traversal;
- drawer or handle interaction;
- explicit precision-task rejection.

Each later template must define solver settings, duration, seeds, and pass/fail interpretation
before it can support claims.

## Failure Taxonomy

Classify failures as:

- under-conservative proxy causing missed collision or excessive penetration;
- over-conservative proxy blocking valid motion or contact;
- full-compound body-state risk;
- contact instability or jitter;
- contact normal mismatch;
- excessive contact count;
- primitive budget exceeded;
- fallback dominates output;
- generation failure;
- scale/provenance error;
- unsupported precision geometry;
- cross-link merge violation;
- joint tree import failure;
- gravity-hold drift;
- trajectory failure;
- self-collision mismatch;
- end-effector pose mismatch;
- checker instability;
- manual-review-required ambiguity.

## Baseline Matrix

Phase 0 required/best-effort baselines:

- bounding primitive;
- single convex hull;
- CoACD, V-HACD, or CPD-style candidate when available.

Later baselines:

- VisACD when available;
- authored/manual colliders when available;
- SDF or hydroelastic reference where task-valid;
- original triangle mesh where valid for the simulator/task;
- Newton-native approximation modes.

## Current Non-Goals

No safety guarantee, real-world transfer, deployment readiness, broad benchmark superiority,
full-simulation speedup, primitive-only sufficiency, full CPD reproduction, or complete replacement
of convex decomposition.
