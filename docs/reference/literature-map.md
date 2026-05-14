# Literature Map

This map keeps the research backlog separate from DeepDive application claims. Entries here are
directions to verify, not evidence that the project has already produced results.

## Primitive And Decomposition Baselines

- Bounding boxes, spheres, capsules, and cylinders: minimum viable primitives for the 0-4 week
  proof point.
- Single convex hull: simple geometry baseline for visible over-approximation and contact stress.
- Convex decomposition families: CoACD and V-HACD are candidate baselines for Phase 0/1 when
  local tooling is available.
- VisACD: candidate visual-aware decomposition baseline for Phase 1 when source, build, and
  licensing checks are complete.

## Physics-Engine Checks

- Newton drop, stack or slide, and contact stress probes are the first diagnostic tasks.
- The checks should report failure modes rather than collapse them into a single score.
- Environment versions, solver settings, and asset normalization must be recorded with every run.

## Learning Components

- LLM/VLM components are intentionally deferred until deterministic baselines show a useful gap.
- Any future learning claim needs an ablation against non-LLM primitive search and repair.

## Source Review Backlog

- Verify primary papers and repositories for CoACD, V-HACD, VisACD, and Newton-specific collision
  guidance.
- Record licenses and citation requirements before adding baselines to reports.
- Move durable findings into `docs/reference/related-work-notes.md`; keep rough intake in
  `docs/tmp/`.
