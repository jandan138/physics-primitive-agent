# One-Page Summary

## Project

Newton Primitive Collision Compiler: a DeepDive-stage proposal for simulation-checked primitive
collider generation in Newton workflows.

## Why It Matters

Collision geometry is a low-level physical contract. A generated or imported asset can look correct
while its collider blocks valid contacts, permits impossible motion, changes body state, or breaks
robot behavior. Physics engines can expose those failures only if collider packages are treated as
diagnostic artifacts rather than trusted conversion outputs.

## Technical Thesis

Primitive colliders should be generated as candidates, not accepted as final output. A candidate
package should pass named Newton diagnostics for body state, contact behavior, and robot operation,
or fall back to another representation.

This is different from claiming that primitive collider generation itself is new. CPD-style
primitive decomposition is an important related candidate generator and baseline.

## First Milestone

0-4 weeks:

- build a non-LLM candidate-generator plus Newton checker loop;
- include body-state and contact diagnostics;
- add generated-package robot task probes for a reproducible robot smoke asset;
- compare simple baselines and CPD/CoACD/V-HACD-style candidates where available;
- report accept/reject/fallback decisions with metrics and provenance.

## Current Status

- Proposal and project bootstrap.
- CPD-like geometry smoke paths and Newton task smokes exist.
- A recorded bed/Franka cylinder mechanism shows why engine-level body-state diagnostics matter.
- An opt-in package body-state guard task path has real Newton task-smoke evidence for the capped
  bed/Franka slice.
- A scoped Phase 0 follow-up run exists over the repo-local materialized GRScenes assets and one
  Franka USD smoke asset, with accept/fallback/failure outcomes and zero dependency gaps for
  bounding, CPD-style, CoACD convex-mesh, V-HACD, stack-or-slide, and articulation-smoke lanes.
  V-HACD generates packages for all five selected rigid assets and records probe failures on bowl/cup/tray.
  Franka link-aware package generation records 12 link-framed primitives over 12 detected links
  with zero cross-link merges and `/panda/panda_link8` as a meshless placeholder.
- A preliminary bed-aligned collision-only pressure test records 2.21x generated-contact throughput
  for Newton-native boxes versus same-count convex64 mesh proxies.
- No broad benchmark-suite, complete collision-quality validation, or whole-robot
  articulated-dynamics evidence exists yet.

## Support Requested

- Newton and robotics-simulation review.
- Geometry-processing and collider-generation review.
- Representative assets and robot descriptions with clear provenance.
- Guidance on diagnostic tasks, solver settings, and acceptance thresholds.
- Small compute and engineering allocation for the first proof point.

## Non-Goals

No safety guarantee, no real-world transfer claim, no deployment readiness, no broad benchmark
superiority or full-simulation speedup claim, no primitive-only sufficiency claim, no full CPD
reproduction claim, and no whole-robot robot-operation claim before generated link-aware packages
are exercised under robot task probes and broader articulation records exist.

Canonical wording: [message-map.md](message-map.md).
