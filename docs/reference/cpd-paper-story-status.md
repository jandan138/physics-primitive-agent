# CPD Paper Story Status

This page explains where the repository sits in the story of reproducing
Convex Primitive Decomposition for Collision Detection. It is a status map, not new experiment
evidence, and not a claim that the paper algorithm has been reproduced.

## Plain Summary

The paper story is about turning a complex mesh into a small set of simple collision primitives
that make collision detection faster or more reliable.

The repository has not reached that full result. It has reached the workbench stage:

1. USD assets can be opened, mirrored into ignored repo-local paths, and capped meshes can be
   extracted.
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
11. An opt-in native fitting comparison can make the CPD-like fitter choose simple `cylinder`,
    `cone`, and `ellipsoid` proposals on deterministic synthetic meshes, including a
    squat-cylinder fixture for the controlled cylinder-axis search.
12. A synthetic native selection audit can explain those toy choices with candidate
    weighted-volume tables and surrogate-cost margins.
13. Capped bed and capped Franka real-USD lanes can run through fitting reports, candidate audit
    summaries, candidate-loss diagnosis, Newton contact canaries, and gated task smokes.
14. An explicitly opt-in synthetic package probe can carry the cylinder scoring-policy multiplier
    through `decompose_mesh` into a changed synthetic `CollisionPackage` and record a Newton
    shape-mapping summary only. It does not change default package generation and does not run
    Newton contact or task diagnostics.
15. A follow-on explicitly opt-in synthetic Newton diagnostic can run named contact, drop/settle,
    and sphere-rain smokes over that changed near-miss package pair under recorded settings.
16. A command-only synthetic controlled merge-search package-path probe can carry the existing
    `cost_guided_pair_choice` grouping difference into `CollisionPackage` and Newton shape-mapping
    accounting, without running Newton contact or task diagnostics.
17. A follow-on synthetic controlled merge-search Newton diagnostic can run named contact,
    drop/settle, and sphere-rain smokes over that changed package pair under recorded settings.
18. A command-only synthetic two-step lookahead merge/search diagnostic can show one bounded
    non-greedy grouping change on a deterministic trap fixture, without package or Newton task
    evidence.
19. A command-only synthetic lookahead package-path probe can carry that bounded grouping change
    into `CollisionPackage` lanes and Newton shape-mapping accounting, without contact/task
    execution.
20. An explicitly opt-in synthetic lookahead Newton diagnostic can run named contact, drop/settle,
    and sphere-rain smokes over that changed package pair under recorded settings.
21. A command-only four-block slice report can link the recorded lookahead evidence across
    primitive fitting/selection, merge/search, offline diagnostics, and recorded Newton task-smoke
    status without rerunning source reports, USD loading, real assets, or Newton tasks.
22. A command-only partial `cpd_paper_offline_report` can audit the first paper-lane toy fixtures
    with paper-side operator fields, current surrogate OBB/sphere rows, a paper-shaped capsule
    axis row, offline-only flat capped-cylinder/frustum/trapezoidal-prism rows, collapse-cost
    fields, a topology-only priority-queue trace, threshold-disabled and finite-threshold
    component-pair traces, and one explicit enclosed-primitive postprocess cull audit.
23. Records and configs can preserve exactly what was run.

The capped-cylinder proxy change is small but important in this story, but it is not the runtime
roadmap. It responds to the expected-failure workbench's primitive-vocabulary gap by adding one
opt-in offline proposal proxy and recording that the unsupported paper primitive gap can decrease
from 3 to 2 in a named report. The runtime roadmap now stays Newton-native first: `cylinder`,
`cone`, and `ellipsoid` have dated synthetic diagnostic-path evidence before any paper-only
primitive is considered for Newton tasks.

This means the reproduction infrastructure is in place, and the first native primitive fitting
hook exists for synthetic toy meshes. The paper-lane primitive-fit audit has also started, but the
paper-faithful decomposition and evaluation story still needs to be implemented.

The 2026-05-16 four-block status audit summarized this position as an internal diagnostic
workbench that was mostly missing integration/report ergonomics rather than Newton plumbing. The
follow-on command-only four-block slice report now gathers primitive-selection, merge/search,
offline report, package/mapping, and recorded Newton task-gate status for the recorded
`cost_guided_lookahead` synthetic slice.

For a step-by-step explanation of how mesh input, primitive fitting, objective terms,
merge/search, `CollisionPackage`, Newton mapping, task smokes, and benchmark claims differ, see
[CPD pipeline step-by-step explainer](cpd-pipeline-step-by-step-explainer.md).

For the current row-by-row paper reproduction gap and the offline-first lane that should close
the next gap, see [CPD paper reproduction gap matrix](cpd-paper-reproduction-gap-matrix.md) and
[CPD paper-faithful offline lane spec](cpd-paper-faithful-offline-lane-spec.md).

## Paper Story Layers

The CPD paper story can be read as eight layers.

| Layer | Paper-story question | Repository status |
| --- | --- | --- |
| 1. Asset input | Can a complex mesh enter the pipeline? | Partially in place through USD-open and capped first-mesh extraction smokes. |
| 2. Primitive proposal | Can the mesh become a small set of primitive candidates? | In place only as a restricted geometry-only CPD-like baseline, not the paper algorithm. An opt-in synthetic comparison can now include simple `cylinder`, `cone`, and `ellipsoid` proxy fits. |
| 3. Objective and cost | Can the system expose diagnostic accounting terms for a decomposition? | Narrowly in place as an offline paper-aligned surrogate objective report with structured Eq.4 alignment metadata. It summarizes primitive budget, volume proxy, raw and AABB-normalized merge excess, containment proxy, and unsupported paper primitive gaps, but it is not the paper collapse-cost rule plus primitive weighting. |
| 4. Search or optimization | Can the system find good primitive sets under a budget? | Partially audited in the paper offline lane through toy priority-queue and component-pair traces. This is still not full paper-scope search or benchmark evidence. |
| 5. Expected limitations | Can known CPD-paper gaps stay visible before algorithmic changes? | Narrowly in place as a deterministic expected-failure synthetic workbench over three in-memory fixtures. This is diagnostic limitation accounting, not validation or benchmark evidence. |
| 6. Primitive vocabulary | Can paper primitive categories enter a restricted proposal lane? | Narrowly in place in two different lanes: the older CPD-like objective report has an opt-in offline `capped_cylinder` proxy, and the partial paper offline report now has current surrogate OBB/sphere rows, a paper-shaped capsule axis row, and offline-only flat capped-cylinder/frustum/trapezoidal-prism audit rows. This is still not paper-faithful primitive fitting. |
| 7. Collision integration | Can generated primitives be consumed by a physics or collision path? | Narrowly in place through Newton contact, drop/settle, and sphere-rain smokes on recorded mapped primitives. The synthetic native bundle also covers `cylinder`, `cone`, and `ellipsoid`; `capped_cylinder` is not Newton-mapped in this slice. |
| 8. Evaluation | Do the results improve collision detection under benchmark settings? | Not started. No benchmark superiority or collision-quality claim is supported. |

## What The Current Baseline Is

The current baseline is a CPD-like geometry smoke path. It groups mesh faces, fits restricted
primitive proposals, and records the result. It exists because later paper-faithful work will need
the same asset intake, report schema, collision-package bridge, and Newton diagnostic plumbing.

The current baseline is useful for pipeline diagnostic plumbing. It is not a substitute for the
paper's primitive coverage, collapse-cost rule, primitive weighting, optimization procedure, or
benchmark evaluation.

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

For a plain-language explanation of the latest Newton-native runtime bundle, see
[Newton-native primitive bundle explainer](newton-native-primitive-bundle-explainer.md).

For a plain-language explanation of the latest opt-in native fitting comparison, see
[Newton-native fitting comparison](newton-native-fitting-comparison.md).

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

The 2026-05-16 controlled merge-search package probe carries the same toy decision one step
farther: the default package groups source faces as `[[0, 1], [2]]`, while the opt-in cost-guided
package groups them as `[[0, 2], [1]]`. Both packages map to Newton shapes. This is package-path
and mapping accounting only; it is not a Newton contact/task diagnostic, real-USD result, or
collision-quality result.

The 2026-05-16 controlled merge-search Newton probe is the next task-smoke layer for that same
package pair. It runs `newton_contact_smoke` first, then runs `newton_drop_settle` and
`newton_sphere_rain` only when contact passes. This shows that the changed synthetic package pair
can enter named Newton diagnostics under recorded settings. It does not show that the opt-in
merge/search policy is better, that a real USD package improved, or that collision quality was
validated.

The 2026-05-16 cost-guided lookahead merge report is a non-paper surrogate extension slice. It
adds `two_step_lookahead` for tiny synthetic fixtures and compares it against greedy
`cost_guided_pairwise` on `lookahead_merge_trap`. The paper method itself is greedy
priority-queue collapse, not lookahead. The lookahead lane changes the toy grouping from
`[[0, 2, 3], [1]]` to `[[0, 1], [2, 3]]` and records lower projected two-step normalized
merge-excess. This is still only offline merge/search accounting. It does not create a package,
run Newton tasks, prove merge-policy superiority, reproduce the paper optimizer, or touch real USD
assets.

Why this still matters for the workbench: CPD is ultimately about selecting a compact primitive
set under geometric and collision-detection constraints. A face-merge baseline that only follows
local adjacency is too weak to explore that engineering space. The lookahead smoke does not solve
the paper problem, but it stress-tests whether a surrogate cost term can change a toy
decomposition decision without confusing that result with paper-faithful search.

The 2026-05-16 cost-guided lookahead package probe is the follow-on package-path gate for that
same toy decision. It converts the greedy and lookahead decompositions into synthetic
`CollisionPackage` lanes and records that both lanes map to Newton shapes. This matters because a
Newton workbench needs an auditable path from a merge/search decision to an engine-facing package
before it can run a task smoke. It still does not run Newton contact, drop/settle, or sphere-rain
diagnostics, and it does not upgrade the lookahead result into a quality or superiority claim.

What it does not yet cover:

- global search over many primitive sets;
- the paper collapse-cost rule plus primitive weighting;
- richer primitive fitting beyond the current restricted proposals;
- collision-quality measurement;
- benchmark comparison.

So the right interpretation is: this is the first cost-aware decision hook in the workbench, not
the CPD optimizer.

The next paper-aligned step is therefore not another Newton task or real-USD rerun. It is an
offline paper lane that can compute and audit paper-side operator, primitive-fit, and collapse-cost
fields on tiny synthetic fixtures first.

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

## What The Paper Offline Primitive Audit Adds

The newer `cpd_paper_offline_report` is a different lane from the older CPD-like
`capped_cylinder` proxy report. It is command-only and synthetic-fixture-only. Its current role is
to audit paper-side mechanics before any package generation or Newton runtime work.

That partial report now records:

- paper-side operator fields on named toy fixtures;
- current surrogate OBB and sphere rows;
- a paper-shaped capsule row with one candidate per operator axis;
- offline-only flat capped-cylinder, frustum, and trapezoidal-prism rows;
- paper base collapse cost and separate weighted-priority cost fields for the first merge-cost
  fixture;
- a topology-only priority-queue trace over `paper_three_face_chain`, including deterministic
  queue keys, accepted merges, eager stale-prune events, updated neighbor insertion counts, and
  target-count stop reason;
- a threshold-disabled component-pair insertion trace over `paper_disconnected_components`,
  including topology-queue exhaustion, one `component_pair` candidate, accepted merge record, and
  target-count stop reason;
- a finite-threshold component-pair blocked trace over `paper_component_pair_threshold_blocked`,
  including attempted count `1`, skipped count `0`, blocked reason, and threshold stop reason.
- an explicit enclosed-primitive postprocess cull audit over `paper_nested_primitive`, including
  two identity-axis OBB audit rows, before/after primitive counts, enclosed/enclosing ids, one cull
  reason, and false package/Newton/real-USD/benchmark triggers.
- a fan-triangulated quad/polygon source-face intake policy audit over `paper_quad_face_intake` and
  `paper_polygon_face_intake`, including source vertex ids, generated triangle vertex triples,
  source-face remap, and source-face aggregate operator matrices.

This closes the narrow capsule axis-policy audit gap and adds the first topology-only
priority-queue trace plus component-pair accepted/blocked toy events, postprocess culling, and
source-face intake policy fixtures inside the report, but it does not make the lane
`paper_faithful_offline`. The next paper-lane gate is
`paper_obb_sphere_fit_faithfulness_audit`.

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
sphere-rain, tests, and records. The dated native-bundle record documents diagnostic-path evidence
for each primitive kind through mapping and diagnostic construction, plus a synthetic clean-env
runtime smoke.

`frustum` and `trapezoidal_prism` should remain in the offline paper-alignment lane for now. They
can still appear in `paper_primitive_gap` accounting, but they should not enter Newton task claims
without a separate mapping and diagnostic record.

## What The Newton-Native Fitting Comparison Adds

The native fitting comparison is the first narrow Layer 2 step after the runtime bundle. It lets
the CPD-like fitter opt into the six-kind Newton-native subset:

```text
box, sphere, capsule, cylinder, cone, ellipsoid
```

and compares it against the older subset:

```text
box, sphere, capsule
```

on deterministic toy meshes:

- `cylindrical_rod`, where the native subset selects `cylinder`;
- `tapered_cone`, where the native subset selects `cone`;
- `ellipsoid_blob`, where the native subset selects `ellipsoid`;
- `squat_cylinder`, where the updated cylinder fitter selects `cylinder` after searching axes.

The report also checks that the resulting one-primitive synthetic packages map through Newton
shape mapping. It now includes candidate weighted-volume audit tables so reviewers can see why the
native primitive ranked first on each toy fixture. This is still a synthetic fitting and
diagnostic-accounting smoke, not Newton task evidence and not collision-quality evidence.

The follow-up bed/Franka probe config now runs the real-USD scope. It records old/new objective
reports on capped bed and capped Franka meshes, inspects mapping gaps and failure labels, then runs
Newton contact canaries and gated task smokes.

## What The Bed/Franka Native Probe Comparison Adds

The bed/Franka native probe comparison completes that next concrete step for two capped real-USD
smoke roles:

```text
bed_dev_smoke
franka_import_smoke
```

For each role, it runs the legacy `box`/`sphere`/`capsule` lane and the six-kind Newton-native
lane under the same face cap and merge policy. After the controlled cylinder-axis fitting update,
bed still selected only `box` primitives in both lanes, while capped Franka's native lane selected
`29` boxes plus `3` cylinders. The subsequent support-aware admissibility slice reclassified those
three Franka cylinder wins as cheaper raw-cost extension candidates with insufficient face/point
support, so the current capped Franka support-aware native lane selects `32` boxes. That means the
pipeline can expose and then constrain a native-lane selection change, but it does not show that
either selection is better collision geometry.

The probe comparison then requires full Newton mapping before contact canary, and gates
drop/settle plus sphere-rain behind contact success. Under the clean Newton conda environment, the
bed and Franka old/new packages passed the recorded contact and task smokes.

This is a real-USD diagnostic smoke milestone, not a benchmark or collision-quality milestone.

## What The Support-Aware Native-Extension Rule Adds

The support-aware rule is a narrow Layer 2 guardrail. It changes primitive selection only when a
Newton-native extension candidate (`cylinder`, `cone`, or `ellipsoid`) has too little local
support and a fallback primitive is available. The current thresholds are three source faces and
five unique assigned points.

The report keeps the distinction between raw cost rank and support-aware selection rank. This
matters because a cylinder can be cheapest under the raw weighted-volume surrogate while still
being blocked from replacing a box because it was fit from only a tiny patch.

This rule is not the CPD paper algorithm. It does not implement the paper's full objective,
priority-queue collapse procedure, primitive vocabulary, or benchmark evaluation. It is a local
diagnostic selection guard that makes the next fitting or clustering experiment easier to inspect.

For a more detailed plain-language explanation of why this slice matters but does not prove native
primitive value, see
[Real USD native probe in the CPD paper story](real-usd-native-probe-paper-story-explainer.md).

For a step-by-step explanation of the latest candidate-loss diagnosis, controlled cylinder-axis
update, synthetic rerun, and bed/Franka Newton-gated rerun as one repeatable loop, see
[CPD latest diagnostic loop explainer](cpd-latest-diagnostic-loop-explainer.md).

For the next algorithmic sequence after local USD mirrors, see
[CPD next steps after real USD mirrors](cpd-next-steps-after-real-usd-mirrors.md).

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
-> ignored repo-local mirrors for current bed/Franka smoke roles
-> CPD-like primitive proposals
-> paper-aligned surrogate objective report
-> synthetic objective comparison
-> focused cost-guided merge-search smoke using one objective term
-> synthetic offline merge-step trace diagnostic accounting for the cost-guided fixture
-> expected-failure workbench for known CPD-paper gaps
-> opt-in capped-cylinder proxy objective report (offline only; not Newton-mapped)
-> historical mapped collision package using Newton-supported primitives
-> Newton smoke diagnostics for recorded mapped primitives
-> synthetic Newton-native primitive bundle smoke
-> synthetic native selection audit for toy primitive choices
-> real-USD old/new native probe comparison for capped bed and capped Franka
-> candidate-loss diagnosis and controlled cylinder-axis fitting smoke
-> support-aware low-support native-extension admissibility guard
-> synthetic cylinder near-miss fixture
-> synthetic cylinder near-miss fit-ablation report
-> synthetic cylinder near-miss scoring-sensitivity report
-> synthetic cylinder near-miss report-only scoring-policy ablation
-> synthetic cylinder scoring-policy guardrail on a clearly boxy cuboid
-> synthetic offline opt-in scoring-policy selection probe
-> explicitly opt-in synthetic package probe plus Newton shape-mapping summary only
-> explicitly opt-in synthetic Newton contact/drop/sphere-rain task smokes
-> synthetic controlled merge-search package-path probe plus Newton shape-mapping summary only
-> synthetic controlled merge-search Newton contact/drop/sphere-rain task smokes
-> synthetic two-step lookahead merge/search diagnostic accounting
-> synthetic lookahead package-path probe plus Newton shape-mapping summary only
-> synthetic lookahead Newton contact/drop/sphere-rain task smokes
-> command-only four-block slice report linking the recorded lookahead evidence
-> partial cpd_paper_offline_report over toy fixtures
-> paper-shaped capsule axis audit row, offline-only paper primitive rows, and collapse-cost fields
-> topology-only paper priority-queue trace audit
-> threshold-disabled component-pair edge insertion audit
-> finite-threshold component-pair blocked audit
-> enclosed-primitive postprocess cull audit
-> polygon/quad source-face intake policy audit
-> dated records
```

The current paper-story position is now:

```text
local USD mirrors or synthetic fixtures
-> use current candidate-loss labels
-> direct cylinder near-miss fixture
-> diagnostic fit-ablation report for containment-preserving cylinder fits
-> diagnostic scoring-sensitivity report for the current surrogate
-> report-only scoring-policy ablation for one synthetic near miss
-> use the boxy guardrail to decide whether one later scoring, primitive-fitting, or merge-search
   change is justified
-> run a synthetic offline opt-in selection probe before any package or Newton task rerun
-> run an explicitly opt-in synthetic package probe before any Newton contact or task rerun
-> run an explicitly opt-in synthetic Newton diagnostic before any real-USD rerun
-> use that synthetic evidence to justify one separate controlled merge/search behavior change
-> synthetic package-path and mapping rerun for the behavior change
-> synthetic Newton task probe for the behavior change, if the changed package maps fully and has
   not already been task-smoked
-> synthetic Newton task probe for the two-step lookahead package pair
-> four-block status audit that identifies the missing workbench integration/report slice
-> command-only four-block slice report for the recorded cost-guided lookahead synthetic slice
-> command-only partial paper offline report for toy paper mechanics
-> topology-only paper priority-queue trace audit, still without package/Newton/real-USD
-> threshold-disabled component-pair edge insertion audit, still without package/Newton/real-USD
-> finite-threshold component-pair blocked audit, still without package/Newton/real-USD
-> enclosed-primitive postprocess cull audit, still without package/Newton/real-USD
-> polygon/quad source-face intake policy audit, still without package/Newton/real-USD
-> next: paper_obb_sphere_fit_faithfulness_audit
-> bed/Franka rerun under full mapping, contact, task, and dated-record gates only after a real
   package change is explicit
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
- "synthetic offline merge-step trace diagnostic accounting";
- "deterministic expected-failure synthetic workbench";
- "expected limitation fixtures";
- "opt-in offline capped-cylinder geometry proposal proxy";
- "primitive-vocabulary accounting for a restricted proposal baseline";
- "Newton-native primitive roadmap";
- "native analytic primitive bundle";
- "synthetic Newton-native primitive diagnostic smoke";
- "controlled cylinder-axis fitting smoke";
- "real-USD candidate-loss diagnosis";
- "synthetic report-only scoring-policy ablation";
- "counterfactual scoring-policy ablation over one synthetic fixture";
- "synthetic report-only scoring-policy guardrail";
- "counterfactual selectivity check over deterministic synthetic fixtures";
- "synthetic offline opt-in scoring-policy selection probe";
- "explicitly opt-in synthetic package probe";
- "Newton shape-mapping summary";
- "explicitly opt-in synthetic Newton diagnostic";
- "named synthetic contact/drop/sphere-rain task smokes";
- "synthetic controlled merge-search Newton task-smoke probe";
- "synthetic two-step merge-search lookahead smoke";
- "bounded diagnostic merge/search heuristic";
- "real-USD native probe diagnostic smoke";
- "capped bed and capped Franka first-mesh scope";
- "paper-alignment offline lane";
- "partial `cpd_paper_offline_report`";
- "paper-shaped capsule axis audit row";
- "offline paper priority-queue trace audit";
- "threshold-disabled component-pair edge insertion audit";
- "finite-threshold component-pair blocked audit";
- "offline enclosed-primitive postprocess cull audit";
- "offline polygon/quad source-face intake policy audit";
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
- "Newton task checked" for package-probe-only reports;
- "simulation-checked" for shape-mapping-only reports;
- "synthetic task smoke proves collision quality";
- "paper primitive vocabulary is runtime-supported";
- "safe collider";
- "validated robot collider."

## Recommended Next Slices

The immediate next slice should now make the algorithm itself more paper-aligned without adding
stronger evaluation claims:

1. Add `paper_obb_sphere_fit_faithfulness_audit` for the current OBB and sphere rows.
2. Build it first on synthetic toy meshes with explicit paper-construction versus surrogate
   labeling.
3. Keep the lane `partial` until the fit-faithfulness audit has tests and a dated record.
4. Keep bed/Franka reruns blocked until a separate real package change passes full mapping,
   contact, task, and dated-record gates.
5. Treat the gap matrix and offline lane spec as the review checklist, not as benchmark or quality
   evidence.

## Claim Boundary

This page adds narrow synthetic native-bundle, opt-in synthetic native-fitting, synthetic
native-selection audit, synthetic cylinder near-miss fixture, fit-ablation, scoring-sensitivity,
report-only scoring-policy ablation, report-only scoring-policy guardrail, synthetic offline
opt-in scoring-policy selection probe, explicitly opt-in synthetic package probe, synthetic
controlled merge-search package-path probe, and capped bed/Franka first-mesh real-USD
diagnostic-smoke claims. It also adds narrow explicitly opt-in synthetic Newton task-smoke claims
for the changed near-miss package pair and the changed controlled merge/search package pair, plus
a narrow offline synthetic two-step lookahead merge/search accounting claim, a narrow
lookahead-changed package-pair synthetic Newton task-smoke claim under recorded settings, and a
command-only four-block evidence-map claim for the recorded lookahead slice. It does not add
benchmark, collision-quality, native primitive improvement, asset-wide, whole-robot,
scoring-policy improvement, merge-policy superiority, package-path evidence for the offline
lookahead report, Newton contact/task evidence for package-probe-only records, general
postprocess-quality evidence, general polygon mesh support, or paper-scope reproduction claims.
