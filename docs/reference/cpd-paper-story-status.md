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
7. A deterministic expected-failure workbench can keep known CPD-paper gaps visible as diagnostic
   flags.
8. An opt-in offline `capped_cylinder` proxy can reduce the named unsupported paper primitive gap
   from 3 to 2.
9. Newton can run narrow smoke diagnostics against the already mapped primitive package.
10. A synthetic Newton-native package can exercise `box`, `sphere`, `capsule`, `cylinder`, `cone`,
    and `ellipsoid` through contact, drop/settle, and sphere-rain diagnostics.
11. Records and configs can preserve exactly what was run.

The capped-cylinder proxy change is small but important in this story, but it is not the runtime
roadmap. It responds to the expected-failure workbench's primitive-vocabulary gap by adding one
opt-in offline proposal proxy and recording that the unsupported paper primitive gap can decrease
from 3 to 2 in a named report. The runtime roadmap now stays Newton-native first: `cylinder`,
`cone`, and `ellipsoid` have been added together as a verified synthetic native analytic bundle
before any paper-only primitive is considered for Newton tasks.

This means the reproduction infrastructure is in place. The paper-faithful decomposition and
evaluation story still needs to be implemented.

## Paper Story Layers

The CPD paper story can be read as eight layers.

| Layer | Paper-story question | Repository status |
| --- | --- | --- |
| 1. Asset input | Can a complex mesh enter the pipeline? | Partially in place through USD-open and capped first-mesh extraction smokes. |
| 2. Primitive proposal | Can the mesh become a small set of primitive candidates? | In place only as a restricted geometry-only CPD-like baseline, not the paper algorithm. |
| 3. Objective and cost | Can the system expose diagnostic accounting terms for a decomposition? | Narrowly in place as an offline paper-aligned surrogate objective report with structured Eq.4 alignment metadata. It summarizes primitive budget, volume proxy, raw and AABB-normalized merge excess, containment proxy, and unsupported paper primitive gaps, but it is not the full paper objective. |
| 4. Search or optimization | Can the system find good primitive sets under a budget? | Not implemented at paper scope. A restricted opt-in cost-guided merge-search smoke now exists for one deterministic synthetic fixture only. |
| 5. Expected limitations | Can known CPD-paper gaps stay visible before algorithmic changes? | Narrowly in place as a deterministic expected-failure synthetic workbench over three in-memory fixtures. This is diagnostic limitation accounting, not validation or benchmark evidence. |
| 6. Primitive vocabulary | Can one missing paper primitive category enter a restricted proposal lane? | Narrowly in place as an opt-in offline `capped_cylinder` proxy. This reduces the unsupported paper primitive count from 3 to 2 in one named report, but it is not paper-faithful primitive fitting. |
| 7. Collision integration | Can generated primitives be consumed by a physics or collision path? | Narrowly in place through Newton contact, drop/settle, and sphere-rain smokes on recorded mapped primitives. The synthetic native bundle also covers `cylinder`, `cone`, and `ellipsoid`; `capped_cylinder` is not Newton-mapped in this slice. |
| 8. Evaluation | Do the results improve collision detection under benchmark settings? | Not started. No benchmark superiority or collision-quality claim is supported. |

## What The Current Baseline Is

The current baseline is a CPD-like geometry smoke path. It groups mesh faces, fits restricted
primitive proposals, and records the result. It exists because later paper-faithful work will need
the same asset intake, report schema, collision-package bridge, and Newton diagnostic plumbing.

The current baseline is useful for pipeline diagnostic plumbing. It is not a substitute for the
paper's primitive coverage, objective formulation, optimization procedure, or benchmark evaluation.

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
- accepted and blocked raw Eq.4-like merge delta plus AABB-normalized merge excess accounting;
- structured Eq.4 alignment metadata for audit;
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

The structured Eq.4 metadata makes that boundary machine-readable. It points reviewers to the
paper's Eq.4 collapse-cost role and to the current JSON fields that carry the analogous surrogate
terms, while also recording `computes_paper_eq4: false` and the remaining non-faithful gaps.

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

That term is an "extra wrapper volume" penalty. For a candidate merge, the baseline fits one
primitive to the merged face group, subtracts the weighted volumes of the two separate primitives,
and divides the result by the source mesh's AABB volume. Lower is better under this proxy.

The simple mental model is:

- the old/default policy says: first try merging neighboring face groups; only after those are
  exhausted, consider disconnected component pairs;
- the new/opt-in policy says: at the same loop step, compare the best neighboring merge and the
  best allowed disconnected-component merge by the recorded merge-excess cost;
- if the disconnected-component merge has much lower surrogate cost, the opt-in policy can choose
  it first.

The dedicated `cost_guided_pair_choice` fixture compares:

- old/default `topology_then_virtual`: adjacent topology merges are considered before virtual
  component merges;
- new/opt-in `cost_guided_pairwise`: the best adjacent topology candidate and the best virtual
  component candidate are compared by normalized merge-excess at the same loop step.

This is still below paper-scope search or optimization. It shows that one surrogate cost can affect
a merge decision on an inspectable toy mesh. It does not prove better collision geometry,
benchmark quality, or paper-faithful CPD behavior.

On the current toy fixture, the default policy records accepted normalized merge-excess
`0.010062106570764756`, about one percent of the mesh AABB volume. The opt-in cost-guided policy
records `0.000055121`, about five thousandths of one percent. The smoke uses that difference only
as diagnostic accounting for the toy decision.

Why this matters for the paper story: CPD is ultimately about selecting a compact primitive set
under geometric and collision-detection constraints. A face-merge baseline that only follows local
adjacency is too weak to tell that story. The new smoke does not solve that problem, but it creates
the first auditable place where a paper-shaped cost term changes a decomposition decision.

What it does not yet cover:

- global search over many primitive sets;
- the paper's full objective formula;
- richer primitive fitting beyond the current restricted proposals;
- collision-quality measurement;
- benchmark comparison.

So the right interpretation is: this is the first cost-aware decision hook in the workbench, not
the CPD optimizer.

## What The Expected-Failure Workbench Adds

The expected-failure workbench is a small but important audit layer. It turns known CPD-paper gaps
into deterministic expected limitation fixtures and diagnostic flags.

The current fixture set asks three questions:

- Does the current restricted `box` subset still report the missing paper primitive vocabulary and
  paper-scope primitive-fitting gap?
- Does a virtual component merge over disconnected triangles still expose that one proxy can wrap
  empty space?
- Does a zero virtual-merge threshold still expose blocked component merge, unmerged components,
  and primitive-budget pressure?

For each fixture, the report records expected, observed, missing, and unexpected flags. A
`smoke_passed` workbench result means those expected flags matched. It does not mean the
decomposition succeeded, and it does not validate collision quality.

This layer matters because the next algorithmic slices should not be chosen blindly. The workbench
points to two concrete next capabilities:

- `primitive_fit_extension` for restricted vocabulary and empty wrapper proxy cases;
- `merge_search_extension` for threshold-blocked component merge behavior.

The workbench is still below paper-scope reproduction. It is not a benchmark, not a failure
detector for arbitrary meshes, and not proof that the baseline catches bad decompositions.

## What The Capped-Cylinder Proxy Adds

The capped-cylinder proxy is the first direct response to the primitive-vocabulary gap. It adds an
opt-in offline `capped_cylinder` geometry proposal proxy and a named objective-report smoke. In
that report, the unsupported paper primitive count decreases from 3 to 2:
`frustum` and `trapezoidal_prism` remain unsupported.

This is useful because it moves one paper primitive category from "outside the proposal vocabulary"
to "available in a restricted report lane." It is still not paper-faithful primitive fitting. The
proxy is marked as `axis_span_radial_proxy` with `hemisphere_caps`, and it does not imply
surface-distance quality, collision quality, or benchmark performance.

Newton integration is intentionally unchanged. `capped_cylinder` remains a Newton mapping gap until
a separate Newton mapping and task-level diagnostic record exists.

## What The Newton-Native Policy Changes

The capped-cylinder proxy exposed a useful distinction:

```text
paper primitive vocabulary != Newton runtime roadmap
```

For runtime work, the project should prefer primitives that Newton can build and diagnose directly.
The native runtime bundle now adds `cylinder`, `cone`, and `ellipsoid` together on top of the
already mapped `box`, `sphere`, and `capsule`.

This bundle was implemented together because the work touches the same surfaces: shape validation,
Newton builder calls, package bounds, support-height estimates, contact canaries, drop/settle,
sphere-rain, tests, and records. The dated native-bundle record proves each primitive kind through
mapping and diagnostic construction, plus a synthetic clean-env runtime smoke.

`frustum` and `trapezoidal_prism` should remain in the offline paper-alignment lane for now. They
can still appear in `paper_primitive_gap` accounting, but they should not enter Newton task claims
without a separate mapping and diagnostic record.

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
-> focused cost-guided merge-search smoke using one objective term
-> expected-failure workbench for known CPD-paper gaps
-> opt-in capped-cylinder proxy objective report (offline only; not Newton-mapped)
-> historical mapped collision package using Newton-supported primitives
-> Newton smoke diagnostics for recorded mapped primitives
-> synthetic Newton-native primitive bundle smoke
-> dated records
```

The next paper-story position should be:

```text
USD assets or synthetic fixtures
-> CPD-like primitive proposals
-> objective comparison record
-> native primitive comparison report
-> CPD-like generator extension only if native primitive fitting is justified
-> Newton task probe after generation support and a named diagnostic record
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
- "deterministic expected-failure synthetic workbench";
- "expected limitation fixtures";
- "opt-in offline capped-cylinder geometry proposal proxy";
- "primitive-vocabulary accounting for a restricted proposal baseline";
- "Newton-native primitive roadmap";
- "native analytic primitive bundle";
- "synthetic Newton-native primitive diagnostic smoke";
- "paper-alignment offline lane";
- "Newton diagnostic smoke over a CPD-like collision package";
- "below full CPD paper reproduction."

Avoid:

- "CPD reproduced";
- "paper-faithful CPD implementation";
- "CPD optimizer implemented";
- "collision-quality validation";
- "benchmark result";
- "validated expected-failure detector";
- "paper-faithful capped cylinder support";
- "Newton supports capped cylinders";
- "broad Newton-native primitive quality";
- "CPD-like generator emits new native primitive kinds by default";
- "paper primitive vocabulary is runtime-supported";
- "safe collider";
- "validated robot collider."

## Recommended Next Slices

The next slices should move toward runtime usefulness without overclaiming:

1. Compare the native bundle against the current `box`/`sphere`/`capsule` path on synthetic
   packages before broadening asset claims.
2. Decide whether restricted `cylinder`, `cone`, or `ellipsoid` fitting belongs in the CPD-like
   generator.
3. Re-run bed and Franka smokes only after generation support has tests and a named diagnostic
   record.

## Claim Boundary

This page adds only the narrow synthetic native-bundle diagnostic claim. It does not add
benchmark, collision-quality, asset-wide, or paper-scope reproduction claims.
