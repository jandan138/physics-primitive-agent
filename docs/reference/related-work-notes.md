# Related Work Notes

This file captures how the proposal should position itself without overstating novelty.

## Positioning

- This is not a claim that primitives are new.
- This is not a claim that decomposition methods are obsolete.
- The proposed value is a disciplined compiler/checker loop around generated assets, task
  contexts, and explicit fallback.
- The leadership story is about physical constraint enforcement for AI-generated or AI-selected
  assets, with physics engines acting as executable diagnostics.

## Baseline Families

- Primitive fitting: boxes, spheres, capsules, cylinders, and simple unions.
- Convex hulls: low-effort coarse approximation.
- Convex decomposition: CoACD and V-HACD where available.
- Visual-aware decomposition: VisACD when available.
- Manual or authored colliders: useful ceiling reference when assets have high-quality human
  collision metadata.

## Distinctions To Preserve

- "Collision package" is an artifact contract, not a deployed safety product.
- "Simulation-checked" means a named task was run or planned under a named protocol.
- "Fallback" is a normal outcome, not a failure to hide.
- "Research roadmap" is future work unless tied to dated records.
