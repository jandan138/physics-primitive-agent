# Benchmark Protocol

This protocol defines how future evidence should be collected for the Newton Primitive Collision Compiler. It exists before benchmark execution so the project does not retrofit metrics to outcomes.

The benchmark is a scoped diagnostic for AI model physical safety constraints: it makes candidate collision-proxy failures observable in Newton, but it does not certify real-world safety.

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

Minimal initial templates:

| Task | Initial Conditions | Metrics | Pass/Fail Interpretation |
|---|---|---|---|
| drop | object above plane, fixed gravity, fixed duration | penetration, jitter, contact count, step time | detects gross missed collision or unstable rest |
| stack or slide | object placed on support or pushed along plane | stability time, contact count, jitter, displacement | detects over/under-conservative support behavior |
| sphere rain/contact stress | small spheres above/around asset | contact count p95, penetration, runtime | detects blocked openings, excess contacts, and false clearances |
| precision rejection | peg/hole or thin-wall stress asset | rejection/fallback decision, reason | passes only if primitive-only output is rejected or locally falls back |

Later templates may add roll, grasp proxy, container, and hole traversal after the proof point is stable. Each template must define solver settings, duration, seeds, and pass/fail interpretation before it can support claims.

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

Use 5-10 provenance-clear assets for the 0-4 week non-LLM primitive baseline plus Newton checker/verifier. Broader task and asset coverage belongs to later phase gates.

## Current Non-Goals

No safety guarantee, real-world transfer, deployment readiness, benchmark superiority, primitive-only sufficiency, or complete replacement of convex decomposition.
