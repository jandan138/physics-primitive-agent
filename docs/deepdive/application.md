# DeepDive Application Draft

## Why This Project

AI systems for physical intelligence increasingly generate assets, scenes, and robot behaviors.
Those outputs become meaningful only when they can be checked against physical constraints.
Collision geometry is one of the hidden contracts behind that check. A visual asset can look
correct while its collision proxy blocks a handle, opens a false gap, changes contact behavior, or
alters robot dynamics.

Existing primitive and convex-decomposition methods can generate useful collider candidates. The
missing layer for our target workflow is a compiler/checker that treats those candidates as
untrusted until Newton has executed task diagnostics over them.

The project asks whether we can build a simulation-checked primitive collider compiler for Newton:
generate editable primitive packages, run engine-level diagnostics over body state, contact, and
robot operation, then accept, reject, or fall back with a reproducible report.

## Strategic Relevance

Physical Intelligence Center needs models that respect physical constraints, not only models that
produce plausible geometry or action plans. Physics engines are executable diagnostic layers under
specified assumptions, tasks, metrics, solver settings, and versions.

This project focuses on one concrete infrastructure point: collision packages should become
reviewable artifacts with recorded physics evidence. The system does not certify safety. It makes
collision-proxy failure modes visible before downstream users trust a simulated asset or robot
task.

## Core Technical Route

The proposed route is:

1. Asset intake records provenance, scale, units, mesh source, and robot link/joint structure.
2. Candidate generation creates primitive packages from simple heuristics, native lanes, authored
   colliders, or CPD-style outputs.
3. Package guards check geometry risk, compound body-state deltas, and link-boundary constraints.
4. Newton diagnostics run drop/settle, contact stress, and body-state probes under recorded
   settings.
5. Robot assets also run articulation gates: joint tree import, gravity hold, simple joint
   trajectory, self-collision sanity, and end-effector pose sanity.
6. Export/report records accepted packages, fallback regions, failed gates, configs, asset hashes,
   and runtime provenance.

LLM/VLM components are deferred. They may later help with semantic part planning or repair
critique, but only after the non-LLM checker loop shows value.

## Current Preparation

Current repository state:

- DeepDive framing and claim-boundary documents exist;
- a Python package skeleton and dry-run CLI exist;
- CPD-like geometry smoke paths and paper-lane audit records exist;
- Newton environment, source, contact, drop/settle, and sphere-rain diagnostic records exist;
- capped bed/Franka records show a real Newton package-context failure mode for a selected
  cylinder package;
- an opt-in body-state guard task path falls back only the flagged bed package while preserving the
  unflagged Franka cylinder package in the recorded smoke.
- a preliminary bed-aligned collision-only microbenchmark shows 2.21x generated-contact throughput
  for Newton-native boxes versus same-count convex64 mesh proxies in one pressure scene.
- a scoped Phase 0 follow-up run records bounding-primitive, CPD-style, and CoACD convex-mesh
  candidate lanes across five materialized GRScenes assets with Newton contact, drop/settle,
  stack-or-slide, and sphere-rain probes; it also records V-HACD as a dependency gap and records
  one Franka USD articulation smoke.

The current evidence supports a project proposal, a narrow diagnostic mechanism story, and a
scoped Phase 0 diagnostic table with CoACD and robot-smoke entries. It does not support broad
benchmark-suite, full-simulation speedup, link-aware robot package generation, whole-robot
collider quality, or safety claims.

## 0-4 Week Milestone

The first milestone should demonstrate that simulation checks catch errors that geometry-only
primitive generation would miss:

- add link-aware robot package generation and link-boundary package probes;
- install or configure V-HACD and rerun the current materialized Phase 0 asset set;
- generate primitive candidate packages and baseline colliders;
- forbid primitive merging across robot link/joint boundaries;
- run Newton body-state, drop/settle, and contact-stress probes;
- run articulation smoke gates for robot packages;
- compare simple baselines plus CoACD/V-HACD/CPD-style candidates when available;
- report primitive count, fallback ratio, failure rate, step time, contact count, jitter or
  penetration, articulation drift, and task failure labels.

Success means useful accept/reject/fallback evidence, not universal primitive success.

## 4-12 Week Route

Weeks 4-8 should expand asset coverage and stabilize the checker/fallback loop. The priority is
not adding more paper-lane gates; it is broadening simulation-checked evidence.

Weeks 8-12 should add checker-guided repair only after failure labels are stable. LLM/VLM should
remain optional and should be introduced only as semantic planning or repair critique after
deterministic baselines justify it.

## Support Requested

Requested support:

- Newton and robotics-simulation reviewers;
- geometry-processing reviewers familiar with CPD, CoACD, V-HACD, and authored collider workflows;
- representative assets and robot descriptions with clear source/license policy;
- advice on Newton task probes, articulation metrics, solver settings, and acceptance thresholds;
- small compute and engineering time for the first simulation-checked proof point;
- connections to users in asset import, robotics, RL, and digital-twin workflows.

## Current Non-Goals

- No safety guarantee.
- No real-world transfer or deployment readiness claim.
- No broad benchmark superiority or full-simulation speedup claim.
- No complete replacement of convex decomposition.
- No novelty claim for automatic primitive collider generation itself.
- No whole-robot Franka performance claim before link-aware package generation, link-boundary
  probes, and articulation records exist.
- No LLM/VLM improvement claim before ablation evidence exists.

Canonical wording lives in [message-map.md](message-map.md).
