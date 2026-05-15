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
5. A synthetic objective comparison can exercise the same accounting on inspectable toy meshes.
6. A focused cost-guided merge-search smoke can use one objective-report term as a toy-fixture
   merge decision cost.
7. Newton can run narrow smoke diagnostics against that package.
8. Records and configs can preserve exactly what was run.

This means the reproduction infrastructure is in place. The paper-faithful decomposition and
evaluation story still needs to be implemented.

## Paper Story Layers

The CPD paper story can be read as six layers.

| Layer | Paper-story question | Repository status |
| --- | --- | --- |
| 1. Asset input | Can a complex mesh enter the pipeline? | Partially in place through USD-open and capped first-mesh extraction smokes. |
| 2. Primitive proposal | Can the mesh become a small set of primitive candidates? | In place only as a restricted geometry-only CPD-like baseline, not the paper algorithm. |
| 3. Objective and cost | Can the system expose diagnostic accounting terms for a decomposition? | Narrowly in place as an offline paper-aligned surrogate objective report. It summarizes primitive budget, volume proxy, merge excess, containment proxy, and unsupported paper primitive gaps, but it is not the full paper objective. |
| 4. Search or optimization | Can the system find good primitive sets under a budget? | Not implemented at paper scope. A restricted opt-in cost-guided merge-search smoke now exists for deterministic synthetic fixtures only. |
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

For a plain-language explanation of this boundary, see
[CPD objective report alignment](cpd-objective-report-alignment.md).

## Is The Objective Report Paper-Consistent?

The short answer is: consistent in design intent, not yet consistent as a paper-faithful
mathematical implementation.

The report asks paper-shaped engineering questions: how many primitives were used, how much proxy
volume was introduced, what the accepted or blocked merges cost, whether assigned points are
contained under a narrow proxy, which paper primitive types are missing, and which failure labels
should block stronger interpretation.

It does not yet implement the paper's full objective formula, search procedure, primitive
vocabulary, containment model, collision-quality evaluation, or benchmark protocol. Treat it as a
reviewable health check that prepares the repository for paper-aligned algorithm work.

## What The Synthetic Comparison Adds

The synthetic objective comparison is the first inspectable toy-mesh layer around the objective
report. It runs the same report on three deterministic in-memory fixtures:

- adjacent square;
- disconnected pair;
- blocked disconnected pair.

For each fixture it records topology-only and `virtual_pairwise` component-merge accounting. The
disconnected fixture no longer reports the topology-only unmerged-component label under
`virtual_pairwise`; the blocked fixture records the `component_merge_blocked` label. These are
fixture-level diagnostic differences, not proof that one policy is better collision geometry.

## What The Cost-Guided Merge Smoke Adds

The cost-guided merge smoke is the first restricted Layer 4 step. It uses one existing surrogate
objective-report term, AABB-normalized merge-excess, to choose among merge candidates on a
deterministic synthetic fixture.

The dedicated `cost_guided_pair_choice` fixture compares:

- old/default `topology_then_virtual`: adjacent topology merges are considered before virtual
  component merges;
- new/opt-in `cost_guided_pairwise`: the best adjacent topology candidate and the best virtual
  component candidate are compared by normalized merge-excess at the same loop step.

This is still below paper-scope search or optimization. It shows that one surrogate cost can affect
a merge decision on an inspectable toy mesh. It does not prove better collision geometry,
benchmark quality, or paper-faithful CPD behavior.

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
-> synthetic objective comparison
-> focused cost-guided merge-search smoke
-> collision package
-> Newton smoke diagnostics
-> dated records
```

The next paper-story position should be:

```text
USD assets or synthetic fixtures
-> CPD-like primitive proposals
-> objective comparison record
-> broader expected-failure synthetic fixtures or improved primitive fitting
-> Newton task probe
```

## Safe Current Wording

Use:

- "CPD reproduction workbench";
- "geometry-only CPD-like primitive proposal baseline";
- "paper-story infrastructure for CPD reproduction";
- "component-merge gate for audit-friendly merge-cost reporting";
- "paper-aligned surrogate objective report";
- "synthetic objective comparison";
- "focused CPD-like cost-guided merge-search smoke";
- "Newton diagnostic smoke over a CPD-like collision package";
- "below full CPD paper reproduction."

Avoid:

- "CPD reproduced";
- "paper-faithful CPD implementation";
- "CPD optimizer implemented";
- "collision-quality validation";
- "benchmark result";
- "safe collider";
- "validated robot collider."

## Recommended Next Slices

The next slices should move toward the paper core without overclaiming:

1. Add broader synthetic fixtures only when they expose a specific expected failure mode.
2. Add one primitive-fitting improvement against those fixtures.
3. Re-run bed and Franka smoke paths after the synthetic comparison shows a clear diagnostic
   difference.
4. Run Newton drop/settle or sphere-rain only as downstream diagnostics, not as the primary
   optimization target.

## Claim Boundary

This page does not add new supported claims. It clarifies the roadmap between the current
CPD-like smoke infrastructure and a future paper-scope reproduction.
