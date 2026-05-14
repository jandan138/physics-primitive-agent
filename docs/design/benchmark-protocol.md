# Benchmark Protocol

This protocol defines how future evidence should be collected for the Newton Primitive Collision Compiler. It exists before benchmark execution so the project does not retrofit metrics to outcomes.

The benchmark is a scoped diagnostic for AI model physical safety constraints: it makes candidate collision-proxy failures observable in Newton, but it does not certify real-world safety.

## Phase 0 Asset Subset

Use 5-10 provenance-clear assets for the 0-4 week diagnostic proof point:

- 2-3 simple rigid props;
- 1-2 stackable objects;
- 1-2 graspable objects with handles or contact affordances;
- 1 container or bowl if available;
- 1 negative-control precision or thin-wall asset if available, used only to test rejection or
  fallback behavior.

## Later Candidate Asset Categories

After the proof point is stable, include representative assets across:

- simple rigid props;
- stackable household objects;
- graspable objects with handles or contact affordances;
- containers and bowls;
- thin-walled or concave objects;
- articulated or multi-link assets where collision proxies are per-link;
- precision or near-precision assets such as holes, slots, pegs, gears, and threads for explicit rejection or fallback;
- visual-detail-heavy assets where collision simplification should ignore irrelevant geometry.

## Licenses/Source Policy

Every asset must record:

- source;
- license or internal ownership status;
- permitted use for benchmark, demo, paper, and repository artifacts;
- asset hash;
- conversion history;
- author or dataset attribution where required.

Assets without clear provenance must not be used for public claims or demos.

## Scale Normalization

Normalize and record:

- units;
- bounding dimensions;
- mass/inertia assumptions when needed;
- origin and orientation conventions;
- task-specific placement frame;
- any mesh cleanup or simplification applied before collision compilation.

Scale changes must be reproducible from config, not applied manually without record.

## Splits

Use fixed splits:

- development assets for implementation debugging;
- validation assets for milestone reporting;
- held-out assets for later claims;
- stress assets for failure taxonomy and no-go checks.

Do not tune primitive budgets, fallback thresholds, or repair rules on held-out assets.

## Phase 0 Executable Protocol

These defaults make the first proof point executable. A record may override them, but any override
must be written into the config before a result supports a claim.

| Probe | Initial Conditions | Solver And Duration | Seeds | Required Metrics | Pass/Fail Interpretation |
|---|---|---|---|---|---|
| drop | asset origin centered 0.25 m above a static plane; gravity enabled; zero initial velocity | Newton default solver, fixed time step recorded from environment, 2 s simulated duration | 3 | step time, contact count p95, penetration or rest jitter | passes if the run completes and reports whether gross missed collision, excessive penetration, or unstable rest occurs |
| stack or slide | asset on a simple support plane or box; slide variant applies a fixed lateral velocity or impulse recorded in config | Newton default solver, 2 s simulated duration | 3 | displacement, contact count p95, penetration or jitter | passes if support/contact behavior is measurable and failure labels are assigned |
| sphere rain/contact stress | 32 spheres of radius 0.025 m spawned in a fixed grid or seeded random pattern above/around the asset | Newton default solver, 2 s simulated duration | 3 | contact count p95, penetration or jitter, step time | passes if blocked openings, false clearances, or excessive contacts are observable when present |
| precision rejection | one peg/hole, thin-wall, gear, slot, or thread-like asset-task pair | compile/check only; simulation optional unless the task is simple to configure | 1 | rejection/fallback decision and reason | passes only if primitive-only output is rejected or locally falls back |

Phase 0 should not claim that these thresholds certify correctness. The goal is executable
diagnostics and reportable failure modes.

## Later Candidate Task Templates

Later benchmark task templates include:

- drop;
- stack;
- slide;
- sphere rain;
- roll;
- grasp proxy;
- container;
- hole traversal;
- explicit precision-task rejection.

Each later template must define solver settings, duration, seeds, and pass/fail interpretation before it can support claims.

## Failure Taxonomy

Classify failures as:

- under-conservative proxy causing missed collision or excessive penetration;
- over-conservative proxy blocking valid motion or contact;
- contact instability or jitter;
- contact normal mismatch;
- excessive contact count;
- excessive broadphase pair count;
- primitive budget exceeded;
- fallback dominates output;
- generation failure;
- scale/provenance error;
- unsupported precision geometry;
- checker instability;
- manual-review-required ambiguity.

## Strategic Story

The benchmark supports the physical-intelligence safety-constraint story by making collision proxy failures executable and observable in Newton, under recorded assumptions.

## Narrow First Milestone

Use the Phase 0 asset subset and executable protocol above for the 0-4 week non-LLM primitive baseline plus Newton diagnostic checker. Broader task and asset coverage belongs to later phase gates.

## Current Non-Goals

No safety guarantee, real-world transfer, deployment readiness, benchmark superiority, primitive-only sufficiency, or complete replacement of convex decomposition.
