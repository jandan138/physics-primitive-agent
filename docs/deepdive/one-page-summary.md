# One-Page Summary

## Project

Newton Primitive Collision Compiler: a primitive-first, simulation-checked, fallback-aware collision asset compiler proposal for Newton.

## Why It Matters

Physical Intelligence Center needs AI models whose outputs can be tested against physical safety constraints. Physics engines provide an executable diagnostic layer for those constraints, but the layer depends on collision geometry. If a collision proxy is wrong, simulation can produce false confidence or false failures.

This project treats collision geometry as a low-level physical contract. It aims to make that contract editable, measurable, and explicit about fallback.

## Technical Thesis

Try primitives first when the asset and task permit it. Check task behavior in Newton. Fall back locally when primitives are not enough.

The project does not claim that primitives fully replace convex decomposition. CoACD, V-HACD, SDF, hydroelastic, convex mesh, triangle mesh, and manual review remain baselines or fallbacks depending on the task.

## First Milestone

0-4 weeks:

- build a non-LLM primitive baseline;
- build a Newton checker/verifier harness;
- run a small provenance-clear asset set;
- compare against simple and existing baselines;
- report primitive count, fallback surface ratio, generation failure rate, runtime, contact counts, penetration, jitter, and task success.

LLM/VLM is deferred until the non-LLM baseline demonstrates value.

## Current Status

- Proposal and project bootstrap.
- Minimal package skeleton and dry-run CLI exist.
- DeepDive documentation defines scope and evidence boundaries.
- No primitive fitting implementation, Newton checker results, or benchmark metrics exist yet.

## Support Requested

- Reviewers from Newton, robotics simulation, geometry processing, and physical-intelligence safety.
- Representative internal assets with clear source/license policy.
- Newton checker scenario and solver-setting guidance.
- Small compute and engineering allocation for the first milestone.
- Downstream user input from asset import, robotics, RL, and digital-twin workflows.

## Non-Goals

No safety guarantee, no real-world transfer claim, no deployment readiness, no benchmark superiority claim, no primitive-only sufficiency claim, and no complete replacement of convex decomposition.

Canonical wording: [message-map.md](message-map.md).
