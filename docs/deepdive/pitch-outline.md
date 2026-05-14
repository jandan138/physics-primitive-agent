# DeepDive Pitch Outline

Target length: 20-30 minutes, followed by review questions.

## 1. Core Problem

Time: 4-5 minutes.

- Physical-intelligence workflows depend on simulation checks.
- Collision geometry is a hidden contract between assets, models, policies, and physics.
- A concrete failure case: a visual handle or gap can be open in the render mesh but blocked by a coarse collider, while an under-conservative proxy can let a policy appear to pass through a surface.
- Render meshes are not reliable dynamic collision assets.
- Existing automated convex decomposition is useful but can be hard to edit, explain, or tune for tasks.

## 2. Strategic Story

Time: 4-5 minutes.

- Physical Intelligence Center needs AI models that respect physical safety constraints.
- Physics engines are executable diagnostic layers under named assumptions, tasks, metrics, and versions.
- Wrong collision proxies can create false confidence or false failures.
- This project focuses on one concrete infrastructure layer: primitive-first, simulation-checked, fallback-aware collision asset compilation.

## 3. Technical Route

Time: 5-7 minutes.

- Geometry Preprocessor: normalize mesh, scale, regions, and provenance.
- Primitive Proposal Bank: produce simple non-LLM primitive candidates first.
- Constrained Optimizer: fit primitive parameters with budgets and constraints.
- Newton Checker: run task probes and record runtime/contact/penetration/jitter/task metrics.
- Repair/Fallback: adjust, reject, or fall back locally to CoACD, SDF, hydroelastic, convex mesh, or manual review.
- Export/Report: write collision package plus provenance and failure reasons.

Important boundary: LLM/VLM is not first. It is a later semantic planner, critic, or repair component only if the non-LLM baseline earns it.

## 4. Current Preparation

Time: 3-4 minutes.

- Repository skeleton exists.
- Dry-run package contracts exist.
- DeepDive docs define claim boundaries.
- Current status is proposal/bootstrap only.
- No primitive fitting, Newton checker results, or benchmark metrics exist yet.

## 5. Next Milestones

Time: 4-5 minutes.

0-4 weeks:

- build a non-LLM primitive baseline for 5-10 provenance-clear assets;
- build 2-3 Newton probes: drop, stack or slide, and sphere-rain/contact stress;
- compare against 2-3 baselines: bounding box or sphere, single convex hull, and CoACD or V-HACD when available;
- report failures, fallback ratio, step time, contact count, and penetration or jitter.

4-12 weeks:

- broaden assets and tasks;
- add repair/fallback logic;
- introduce LLM/VLM only after baseline evidence supports it;
- make a continue/narrow/pivot/stop decision.

## 6. Support Request

Time: 2-4 minutes.

- Newton, robotics simulation, geometry, and physical-intelligence safety reviewers.
- Representative assets with clear source/license policy.
- Newton scenario and solver-setting guidance.
- Small compute and engineering allocation for the first proof point.
- Downstream user feedback from robotics, RL, digital twin, and asset import workflows.

## Strategic Story, Milestone, And Non-Goals

Canonical wording: [message-map.md](message-map.md).

Narrow first milestone: non-LLM primitive baseline plus Newton diagnostic checker.

Current non-goals: safety guarantee, real-world transfer, deployment readiness, benchmark superiority, complete replacement of convex decomposition, and LLM/VLM claims before baseline evidence.
