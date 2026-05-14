# DeepDive Application Draft

## Why This Project

AI systems for physical intelligence increasingly generate scenes, assets, and robot behaviors. Those outputs become meaningful only when they can be tested against physical constraints. Today, collision geometry is often treated as a low-level asset conversion detail, but it is actually a hidden contract between model output, simulator behavior, and downstream robotics evaluation.

The project asks whether we can build a Newton Primitive Collision Compiler: a primitive-first, simulation-checked, fallback-aware tool that turns visual assets into editable collision proxies, checks them in Newton, and records when existing methods such as CoACD, SDF, hydroelastic, or manual review are still required.

The immediate DeepDive goal is not to claim a finished compiler. It is to get review and support for a narrow first milestone that can quickly prove whether the non-LLM baseline has value.

## Strategic Relevance

Physical Intelligence Center needs models that respect physical safety constraints, not only models that produce plausible actions or assets. Physics engines matter because they act as executable diagnostic layers: under specified assumptions, tasks, metrics, solver settings, and versions, they can surface candidate penetrations, unstable contacts, false clearance assumptions, and task-level physical failures.

Collision geometry is a low-level safety interface. If a proxy is too loose, a policy can appear to move through an object. If it is too conservative, valid grasps, stacks, or paths may fail. A collision compiler that checks and reports this boundary supports safer physical-intelligence workflows without claiming to guarantee safety.

## Core Technical Route

The proposed route is:

1. Geometry preprocessing prepares mesh, scale, regions, and provenance.
2. A non-LLM primitive proposal baseline produces boxes, spheres, capsules, cylinders, cones, or ellipsoids under a primitive budget.
3. A constrained optimizer fits primitive parameters while respecting task-specific budgets and basic geometry constraints.
4. A Newton checker/verifier runs task probes and records contact behavior, penetration, jitter, time, and failure modes.
5. A repair/fallback stage splits, merges, adjusts, rejects, or falls back locally to existing collision representations.
6. Export/report writes collision packages with provenance, metrics, fallback reasons, and unsupported regions.

LLM/VLM components are intentionally deferred. They may later help with semantic part planning, task-aware budgets, and repair proposals, but only after the non-LLM baseline shows measurable value.

## Current Preparation

Current repository state:

- project framing and bootstrap documents exist;
- a minimal Python package skeleton and dry-run CLI exist;
- DeepDive application materials are being organized;
- no primitive fitting implementation exists today;
- no Newton checker results exist today;
- no benchmark metrics exist today.

The current evidence supports a project proposal and milestone plan, not research conclusions.

## 0-4 Week Milestone

The first milestone is a non-LLM primitive baseline plus Newton checker/verifier:

- select a small, licensed/provenance-clear asset set;
- normalize scale and task labels;
- generate simple primitive proposals with a fixed budget;
- compare against bounding box, bounding sphere, single convex hull, V-HACD, CoACD, manual primitive colliders where available, and Newton-native approximate mesh modes;
- run Newton task probes such as drop, stack, slide, sphere rain, grasp proxy, container, and hole traversal when applicable;
- report primitive count, fallback surface ratio, generation failure rate, runtime, contact counts, penetration, jitter, and task success;
- decide whether the baseline justifies Phase 1.

Success means useful evidence and clear failure modes, not universal success across assets.

## 4-12 Week Route

Weeks 4-8 should expand the non-LLM baseline to more assets, stabilize the Newton checker, add repair operations, and make fallback reporting precise.

Weeks 8-12 should introduce LLM/VLM only if the non-LLM baseline has shown measurable value. The first LLM/VLM role should be semantic planning, task-aware budget selection, or repair critique, not direct floating-point primitive regression.

The 12-week output should be a measured decision: continue, narrow, pivot to fallback tooling, or stop.

## Support Requested

Requested support:

- reviewers from Newton physics, geometry processing, robotics simulation, and physical-intelligence safety;
- representative internal assets and source/license guidance;
- advice on Newton checker scenarios, solver settings, and metric thresholds;
- small compute and engineering time for the first milestone;
- connections to internal users who import assets, train robot policies, or evaluate physical scenes.

The project should be funded by milestone evidence. If the non-LLM baseline fails to produce value, the project should not spend resources on LLM/VLM expansion.

## Current Non-Goals

- No safety guarantee.
- No real-world transfer or deployment readiness claim.
- No benchmark superiority claim.
- No complete replacement of convex decomposition.
- No promise that primitive-only collision works for precision insertion, thin walls, threads, gears, or all CAD assets.
- No claim that LLM/VLM improves results before ablation evidence exists.

Canonical wording lives in [message-map.md](message-map.md).
