# Benchmark Protocol

This protocol defines how future evidence should be collected for the Newton Primitive Collision Compiler. It exists before benchmark execution so the project does not retrofit metrics to outcomes.

## Asset Categories

Include representative assets across:

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

## Task Templates

Benchmark task templates include:

- drop;
- stack;
- slide;
- sphere rain;
- roll;
- grasp proxy;
- container;
- hole traversal;
- explicit precision-task rejection.

Each template must define initial conditions, solver settings, duration, metrics, seeds, and pass/fail interpretation.

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

Use a small provenance-clear subset for the 0-4 week non-LLM primitive baseline plus Newton checker/verifier.

## Current Non-Goals

No safety guarantee, real-world transfer, deployment readiness, benchmark superiority, primitive-only sufficiency, or complete replacement of convex decomposition.
