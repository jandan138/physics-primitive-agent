# DeepDive Pitch Outline

Target length: 20-30 minutes, followed by review questions.

## 1. Core Problem

Time: 4-5 minutes.

- Physical-intelligence workflows depend on simulator checks.
- Collision geometry is a hidden contract between assets, robots, policies, and physics.
- Geometry-only collider generation can miss engine-level failures.
- A primitive package may look plausible but change COM/inertia, contact behavior, or robot
  articulation.
- The problem is not only "generate colliders"; it is "accept colliders only after executable
  diagnostics".

## 2. Strategic Story

Time: 4-5 minutes.

- Physical Intelligence Center needs AI outputs that can be checked against physical constraints.
- Physics engines are executable diagnostic layers under named assumptions.
- Collision packages are safety-affecting artifacts that need provenance, metrics, and fallback.
- The project focuses on simulation-checked primitive collider compilation for Newton workflows.

## 3. Technical Route

Time: 6-8 minutes.

- Candidate Generator: simple primitives, authored colliders, native lanes, or CPD-style outputs.
- Package Guard: scale, provenance, body-state risk, primitive-budget, and link-boundary checks.
- Newton Checker: drop/settle, sphere-rain/contact stress, and body-state diagnostics.
- Robot Operation Gates: joint tree import, gravity hold, joint trajectory, self-collision sanity,
  and end-effector pose sanity.
- Fallback: CoACD, V-HACD, SDF, hydroelastic, convex mesh, triangle mesh where valid, or manual
  review.
- Export/Report: accepted package, failed gates, fallback reason, metrics, asset hash, config, and
  Newton provenance.

Important boundary: LLM/VLM is not first. It is deferred until deterministic baselines and checker
records justify a semantic-planning or repair-critique role.

## 4. Current Preparation

Time: 4-5 minutes.

- Repository skeleton and dry-run package contracts exist.
- CPD-like and native primitive diagnostic lanes exist.
- Newton environment and task-smoke records exist.
- Capped bed/Franka cylinder records show a real full-compound body-state failure mode.
- An opt-in body-state guard has recorded task-path evidence.
- A bed-aligned collision-only pressure test gives an early performance hook: 2.21x
  generated-contact throughput for Newton-native boxes versus same-count convex64 mesh proxies.
- Current status is still proposal/bootstrap, not broad benchmark-suite, full-simulation speedup,
  or whole-robot validation.

## 5. Next Milestones

Time: 4-5 minutes.

0-4 weeks:

- run a small provenance-clear asset set;
- include one articulated robot smoke asset if reproducible;
- forbid cross-link primitive merges;
- run body-state, contact, and articulation gates;
- compare simple baselines plus CoACD/V-HACD/CPD-style candidates when available;
- report accept/reject/fallback evidence.

4-12 weeks:

- broaden assets and robot-operation tasks;
- add checker-guided repair only after failure labels are stable;
- introduce LLM/VLM only after non-LLM value is demonstrated;
- decide continue, narrow, pivot, or stop.

## 6. Support Request

Time: 2-4 minutes.

- Newton, robotics simulation, geometry, and physical-intelligence safety reviewers.
- Representative assets and robot descriptions with clear source/license policy.
- Newton task and solver-setting guidance.
- Small compute and engineering allocation.
- Downstream feedback from robotics, RL, digital-twin, and asset-import workflows.

## Non-Goals

Canonical wording: [message-map.md](message-map.md).

Current non-goals: safety guarantee, real-world transfer, deployment readiness, broad benchmark
superiority, full-simulation speedup, full CPD reproduction, complete replacement of convex
decomposition, whole-robot robot-operation claims before articulated records, and LLM/VLM claims
before baseline evidence.
