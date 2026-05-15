# CPD Paper Story Status

This page explains where the repository sits in the story of reproducing
Convex Primitive Decomposition for Collision Detection. It is a status map, not new experiment
evidence, and not a claim that the paper algorithm has been reproduced.

## Plain Summary

The paper story is about turning a complex mesh into a small set of simple collision primitives
that make collision detection faster or more reliable.

The repository has not reached that full result. It has reached the workbench stage:

1. USD assets can be opened and capped meshes can be extracted.
2. A simple CPD-like face-merge baseline can produce primitive proposals.
3. Those proposals can be wrapped as a collision package.
4. An offline objective report can summarize paper-aligned surrogate geometry terms.
5. Newton can run narrow smoke diagnostics against that package.
6. Records and configs can preserve exactly what was run.

This means the reproduction infrastructure is in place. The paper-faithful decomposition and
evaluation story still needs to be implemented.

## Paper Story Layers

The CPD paper story can be read as six layers.

| Layer | Paper-story question | Repository status |
| --- | --- | --- |
| 1. Asset input | Can a complex mesh enter the pipeline? | Partially in place through USD-open and capped first-mesh extraction smokes. |
| 2. Primitive proposal | Can the mesh become a small set of primitive candidates? | In place only as a restricted geometry-only CPD-like baseline, not the paper algorithm. |
| 3. Objective and cost | Can the system expose diagnostic accounting terms for a decomposition? | Narrowly in place as an offline paper-aligned surrogate objective report. It summarizes primitive budget, volume proxy, merge excess, containment proxy, and unsupported paper primitive gaps, but it is not the full paper objective. |
| 4. Search or optimization | Can the system find good primitive sets under a budget? | Not implemented at paper scope. Current behavior is greedy face/component merging. |
| 5. Collision integration | Can generated primitives be consumed by a physics or collision path? | Narrowly in place through Newton contact, drop/settle, and sphere-rain smokes on recorded assets. |
| 6. Evaluation | Do the results improve collision detection under benchmark settings? | Not started. No benchmark superiority or collision-quality claim is supported. |

## What The Current Baseline Is

The current baseline is a CPD-like geometry smoke path. It groups mesh faces, fits restricted
primitive proposals, and records the result. It exists because later paper-faithful work will need
the same asset intake, report schema, collision-package bridge, and Newton diagnostic plumbing.

The current baseline is useful for pipeline validation. It is not a substitute for the paper's
primitive coverage, objective formulation, optimization procedure, or benchmark evaluation.

## What The Component-Merge Gate Adds

The component-merge gate is a small algorithmic extension to the baseline. It keeps the default
topology-only merge behavior, and when explicitly enabled it can consider disconnected-component
pairwise merge candidates after topology adjacency merges are exhausted.

Its value is auditability:

- it records the merge policy;
- it records initial and final component counts;
- it separates topology merges from virtual component merges;
- it records blocked merge counts;
- it normalizes excess-volume accounting by the mesh AABB volume.

This is still below paper reproduction. It is a controlled way to start collecting the information
needed by a future paper-aligned objective.

## What The Offline Objective Report Adds

The offline objective report is the first explicit Layer 3 artifact. It does not change the
baseline algorithm. It reads a CPD-like decomposition report and emits reviewable terms:

- primitive budget pressure;
- AABB-normalized primitive volume proxy;
- accepted and blocked merge excess accounting;
- assigned-point containment proxy;
- unsupported paper primitive gaps;
- component merge and fallback labels.

This is a paper-aligned surrogate report, not a paper-faithful objective implementation. It gives
future merge-search and primitive-fitting work stable comparison fields before those algorithms
change.

## What Newton Probes Mean Here

Newton probes are downstream diagnostic checks. They answer a narrow question:

Can this primitive package be mapped into Newton shapes and participate in a named smoke task under
recorded settings?

They do not answer the stronger question:

Is this decomposition a good collision representation?

For that stronger claim, the repository still needs paper-aligned objective metrics, broader asset
coverage, task-level comparison reports, and dated benchmark records.

## Current Story Position

The current position is:

```text
USD assets
-> CPD-like primitive proposals
-> paper-aligned surrogate objective report
-> collision package
-> Newton smoke diagnostics
-> dated records
```

The next paper-story position should be:

```text
USD assets
-> CPD-like primitive proposals
-> improved fitting or merge search
-> Newton task probe
-> comparison record
```

## Safe Current Wording

Use:

- "CPD reproduction workbench";
- "geometry-only CPD-like primitive proposal baseline";
- "paper-story infrastructure for CPD reproduction";
- "component-merge gate for audit-friendly merge-cost reporting";
- "paper-aligned surrogate objective report";
- "Newton diagnostic smoke over a CPD-like collision package";
- "below full CPD paper reproduction."

Avoid:

- "CPD reproduced";
- "paper-faithful CPD implementation";
- "collision-quality validation";
- "benchmark result";
- "safe collider";
- "validated robot collider."

## Recommended Next Slices

The next slices should move toward the paper core without overclaiming:

1. Add small synthetic meshes where the expected primitive decomposition is inspectable.
2. Compare topology-only and component-merge gate outputs using the same report schema.
3. Add one improved primitive-fitting or merge-search step only after the objective report is
   stable.
4. Run Newton drop/settle or sphere-rain only as a downstream diagnostic, not as the primary
   optimization target.

## Claim Boundary

This page does not add new supported claims. It clarifies the roadmap between the current
CPD-like smoke infrastructure and a future paper-scope reproduction.
