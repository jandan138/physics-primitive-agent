# Documentation Index

Current status: this repository is a DeepDive application and project bootstrap for the Newton
Primitive Collision Compiler. The current direction is simulation-checked primitive collider
generation: primitive packages are candidates until Newton diagnostics accept, reject, or route
them to fallback.

## Current Story

The project is no longer best described as a CPD reproduction effort. CPD-style primitive
decomposition remains important related work and a possible candidate generator. The proposed
contribution is the downstream compiler/checker loop:

- preserve provenance, scale, and robot link/joint boundaries;
- generate or import primitive collider candidates;
- run Newton body-state, contact, and articulation diagnostics;
- fall back when primitive packages are not physically usable.

## Primary DeepDive Docs

- [DeepDive message map](deepdive/message-map.md)
- [DeepDive application draft](deepdive/application.md)
- [One-page summary](deepdive/one-page-summary.md)
- [Pitch outline](deepdive/pitch-outline.md)
- [Review Q&A](deepdive/review-qa.md)
- [Evidence status](deepdive/evidence-status.md)

## Design Docs

- [Project scope](design/project-scope.md)
- [System architecture](design/system-architecture.md)
- [Research roadmap](design/research-roadmap.md)
- [Evaluation plan](design/evaluation-plan.md)
- [Benchmark protocol](design/benchmark-protocol.md)

## Reference Docs

- [Claim boundaries](reference/claim-boundaries.md)
- [Simulation-checked primitive collider direction](reference/simulation-checked-primitive-collider-direction.md)
- [Related work notes](reference/related-work-notes.md)
- [Literature map](reference/literature-map.md)
- [Newton-in-the-loop selector story](reference/newton-in-the-loop-selector-story.md)
- [CPD paper story status](reference/cpd-paper-story-status.md)

## Key Evidence Records

- [Phase 0 GRScenes asset intake](records/2026-05-25-phase0-grscenes-asset-intake.md)
- [Phase 0 V-HACD runtime follow-up](records/2026-05-26-phase0-vhacd-runtime-followup.md)
- [Link-aware robot package generation](records/2026-05-26-link-aware-robot-package-generation.md)
- [Phase 0 stack/CoACD/articulation follow-up](records/2026-05-25-phase0-stack-coacd-articulation-followup.md)
- [Cylinder goal completion audit after contact closure](records/2026-05-22-cylinder-goal-completion-audit-after-contact-closure.md)
- [Package body-state guard task path](records/2026-05-22-package-body-state-guard-task-path.md)
- [Bed-aligned box primitive contact-throughput microbenchmark](records/2026-05-22-bed-aligned-box-primitive-contact-throughput.md)
- [DeepDive direction shift record](records/2026-05-22-deepdive-direction-shift-to-simulation-checked-robotics.md)

## Current Non-Goals

- No production compiler claim.
- No full CPD paper reproduction claim.
- No broad benchmark, full-simulation speedup, or collision-quality validation claim.
- No whole-robot articulated robot-operation claim before dedicated records exist.
- No deployment readiness, real-world transfer, or safety guarantee.
