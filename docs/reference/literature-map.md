# Literature Map

This map keeps the research backlog separate from DeepDive application claims. Entries here are
directions to verify, not evidence that the project has already produced results.

## Primitive And Decomposition Baselines

- CPD-style primitive decomposition: strong related work for automatic primitive collider
  generation. Treat as a candidate generator and baseline, not as the project novelty claim.
- CoACD and V-HACD: convex-decomposition baselines and fallback candidates.
- Bounding boxes, spheres, capsules, and cylinders: minimum viable primitives for candidate
  packages and simple baselines.
- Single convex hull: simple geometry baseline for visible over-approximation and contact stress.
- VisACD: candidate later baseline after source, build, and licensing checks.
- Authored/manual colliders: useful ceiling reference where available.

## Physics-Engine Checks

- Newton body-state/drop-settle, sphere-rain/contact stress, and stack/slide probes are the first
  rigid-asset diagnostics.
- Diagnostics should report failure modes rather than collapse them into one score.
- Environment versions, solver settings, seeds, and asset normalization must be recorded with
  every run.

## Robot Operation Checks

- Link-boundary preservation: primitive merges must not cross robot joints.
- Articulation smoke: joint tree import, gravity hold, simple joint trajectory, self-collision
  sanity, and end-effector pose sanity.
- Contact-operation smoke: push/place/grasp-like tasks only after the basic articulation gate is
  reproducible.

## Learning Components

- LLM/VLM components are deferred until deterministic candidate generation and diagnostics show a
  useful gap.
- Any future learning claim needs an ablation against non-LLM primitive search and repair.

## Source Review Backlog

- Verify primary papers and repositories for CPD-style primitive decomposition, CoACD, V-HACD,
  VisACD, DCOL, and engine-specific collision guidance.
- Record licenses and citation requirements before adding baselines to reports.
- Move durable findings into [related-work-notes.md](related-work-notes.md); keep rough intake in
  `docs/tmp/`.
