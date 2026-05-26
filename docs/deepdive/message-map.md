# DeepDive Message Map

This is the canonical DeepDive-facing wording. Other current-facing docs should preserve these
claims and boundaries.

## Leadership Narrative

Physical Intelligence Center needs AI systems whose generated assets, scenes, and robot behaviors
can be checked against physical constraints. Physics engines are the executable diagnostic layer
for those constraints, but they depend on collision geometry. If the collision proxy is wrong, the
simulator can create false confidence, false failure, unstable contact, or misleading robot-task
results.

The project treats generated collision packages as safety-affecting artifacts that require
diagnosis before use. Primitive colliders are useful because they are editable, inspectable, and
fast in many physics engines, but geometry-only primitive fitting is not enough. A primitive package
can be visually plausible and still change compound body state, contact behavior, or robot
articulation in a way that breaks simulation.

## Technical Thesis

Build a simulation-checked, fallback-aware primitive collider compiler for Newton workflows.

The compiler should:

- generate or import primitive collider candidates from assets, robots, or CPD-style algorithms;
- preserve asset provenance, scale, body boundaries, and link/joint structure;
- run Newton diagnostics before accepting a package;
- reject or fall back when body-state, contact, or robot-operation checks fail;
- report why a package was accepted, rejected, or routed to fallback.

The thesis is not that primitive generation is new. The thesis is that primitive generation must be
closed by physics-engine execution and robot-operation checks before the package is trusted.

## Safe One-Liner

Newton Primitive Collision Compiler is a DeepDive-stage proposal for simulation-checked primitive
collider generation: create editable primitive collision packages, run Newton diagnostics over body
state, contact, and robot operation, and fall back when primitive packages are not physically
usable.

## What Changed In The Story

Earlier framing emphasized primitive-first collision asset compilation and CPD-like reproduction
gates. The sharper current framing treats CPD-style primitive decomposition as a candidate
generator and shifts the contribution to the downstream checker:

- geometry and primitive count are candidate-quality signals;
- Newton drop/contact/body-state/articulation results are acceptance signals;
- fallback is a normal compiler result, not a failure to hide.

The capped bed/Franka cylinder mechanism record is the first concrete story: a geometry-plausible
bed cylinder is safe as an isolated primitive but fails in the full compound package because of
COM/inertia body-state sensitivity, while recorded Franka cylinder packages pass in their smaller
package context.

The bed-aligned contact-throughput microbenchmark adds the first positive performance hook: in one
collision-only pressure scene, accepted Newton-native box primitives achieved 2.21x higher
generated-contact throughput than same-count 64-vertex convex-mesh proxies. This supports the
primitive-aware acceptance story, while staying below any full-simulation or broad benchmark
superiority claim.

The scoped Phase 0 follow-up run adds stack-or-slide execution, CoACD executable convex-mesh
packages, V-HACD runtime evidence, one Franka USD articulation smoke, and one generated-package
Franka task smoke to the five-asset GRScenes
diagnostic table. V-HACD now generates packages for all five selected rigid assets, with recorded
probe failures on bowl/cup/tray. The same report now records a Franka link-aware package with all
detected links covered, zero cross-link merges, a meshless `/panda/panda_link8` placeholder, and
12 generated package primitives consumed by Newton in the generated-package task smoke. It is still
not complete Phase 0 coverage because broader robot task coverage and broader pass criteria remain
open.

## DeepDive Proof Point

The narrow first proof point should demonstrate that the checker can expose errors that
geometry-only primitive generation would miss.

Minimum proof point:

- the materialized Phase 0 GRScenes rigid-asset manifest;
- at least one articulated robot smoke asset if licensing and runtime setup are reproducible;
- primitive candidates from deterministic heuristics, existing native lanes, or CPD-style outputs;
- Newton body-state, drop/settle, and contact-stress diagnostics;
- articulation smoke gates for robot assets: link-boundary preservation, joint tree import,
  gravity hold, simple joint trajectory, self-collision sanity, and end-effector pose sanity;
- fallback reporting against simple baselines and CoACD/V-HACD/CPD-style candidates when available.

## Unsafe Claims

Do not claim:

- do not claim a physical safety guarantee or real-world transfer;
- deployment readiness;
- broad benchmark superiority or full-simulation speedup;
- complete replacement of convex decomposition;
- novelty in automatic primitive collider generation itself;
- full CPD paper reproduction;
- calibrated default selector policy;
- whole-robot Franka or broad robot-operation validation before generated link-aware packages are
  exercised under robot task probes and broader articulation records exist;
- that simulation checks prove collision correctness outside named simulator assumptions.

## Support Request

Requested DeepDive support:

- Newton and robotics-simulation review for diagnostic tasks, solver settings, and failure labels;
- geometry-processing review for primitive candidate generation and CPD/CoACD/V-HACD baselines;
- representative internal assets and robots with clear license/provenance boundaries;
- small compute and engineering allocation for the first simulation-checked proof point;
- downstream user input from robotics, RL, digital-twin, and asset-import workflows.

The ask remains milestone-based. If the checker cannot expose useful failures or acceptance/fallback
decisions, the project should narrow before adding LLM/VLM complexity.
