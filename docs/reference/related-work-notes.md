# Related Work Notes

This file captures how the proposal should position itself without overstating novelty.

## Positioning

- This is not a claim that primitives are new.
- This is not a claim that automatic primitive collider generation is new.
- This is not a claim that decomposition methods are obsolete.
- The proposed value is a disciplined compiler/checker loop around generated primitive candidates,
  Newton diagnostics, robot articulation constraints, and explicit fallback.
- The leadership story is about physical constraint diagnostics for AI-generated or AI-selected
  assets, with physics engines acting as executable diagnostics.

## Closest Related Families

- CPD-style primitive decomposition: generates primitive collider packages for rigid-body
  simulation. It is close and must be treated as related work and a possible candidate source.
- CoACD and V-HACD: convex-decomposition baselines and fallbacks.
- DCOL and differentiable primitive collision methods: relevant to primitive collision reasoning,
  but not the same as a compiler/checker acceptance loop.
- Engine collision approximation tools: important industrial baselines for generated collision
  shapes and runtime support.
- Authored/manual colliders: ceiling reference for editability and practical asset workflows.

## Distinctions To Preserve

- "Candidate generator" describes geometry or CPD-style primitive output before Newton checks.
- "Simulation-checked" means a named task was run under a named protocol with a dated record.
- "Articulation-aware" requires link/joint graph preservation and robot-specific smoke records.
- "Fallback" is a normal outcome, not a failure to hide.
- "Research roadmap" is future work unless tied to dated records.
