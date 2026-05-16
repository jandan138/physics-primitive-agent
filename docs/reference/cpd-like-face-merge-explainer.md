# CPD-Like Face-Merge Explainer

This page explains the current geometry-only CPD-like baseline in plain terms. It is a reader aid,
not new evidence and not a claim that the CPD paper has been reproduced.

For the broader paper-story map, see
[CPD paper story status](cpd-paper-story-status.md). For the objective-report boundary, see
[CPD objective report alignment](cpd-objective-report-alignment.md).

## Plain Summary

The current baseline takes a mesh, groups nearby connected faces with simple geometric rules, and
fits a restricted primitive candidate to each group. It is called CPD-like because the output shape
resembles the paper story: a complex mesh becomes a set of simple primitive collision candidates.

It is not the CPD paper algorithm. It is a temporary geometry baseline that lets the repository test
the asset intake, primitive-reporting, package, and Newton diagnostic plumbing before implementing
paper-scope decomposition and evaluation.

## CPD Story Position

The CPD paper story can be read as four layers:

1. Start from a complex triangle mesh.
2. Decompose or fit it into a set of convex primitives.
3. Feed those primitives to a collision detection or physics-engine path.
4. Evaluate collision quality, speed, failure cases, and baseline comparisons.

The repository has reached a narrow slice of layer 3:

- Layer 1 is partially in place: the smoke path can extract a capped USD mesh.
- Layer 2 exists only as a simple CPD-like baseline, not the paper algorithm.
- Layer 2 now has one opt-in extension: a component-merge gate that can try disconnected-component
  pairwise merges after topological adjacency merges are exhausted.
- Layer 2 also has one restricted cost-guided merge-search smoke over a deterministic toy mesh.
- Layer 2 also has one bounded two-step lookahead merge/search diagnostic over a deterministic
  trap fixture. It is synthetic-only and does not change default behavior.
- Layer 2 now has an opt-in offline capped-cylinder proposal proxy that reduces the named
  unsupported paper primitive gap from 3 to 2 without adding Newton mapping.
- Layer 3 now has an offline paper-aligned surrogate objective report over the capped bed
  CPD-like baseline.
- Layer 3 also has a command-only synthetic objective comparison over deterministic toy meshes.
- Layer 3 now has an explicitly opt-in synthetic package probe that carries one scoring-policy
  multiplier through `decompose_mesh` into `CollisionPackage` generation and records Newton
  shape-mapping coverage. It does not run Newton contact or task diagnostics.
- Layer 3 now also has a follow-on explicitly opt-in synthetic Newton diagnostic over that changed
  near-miss package pair. It runs named contact, drop/settle, and sphere-rain task smokes, but
  only for synthetic packages and not as collision-quality evidence.
- Layer 3 also has a controlled merge-search package-path probe for the existing
  `cost_guided_pair_choice` fixture. It carries the `topology_then_virtual` versus
  `cost_guided_pairwise` grouping difference into `CollisionPackage` and Newton shape-mapping
  accounting, without running Newton contact or task diagnostics.
- Layer 3 also has a follow-on controlled merge-search Newton probe for that changed synthetic
  package pair. It runs contact, drop/settle, and sphere-rain smokes under recorded settings, but
  still only as synthetic task-smoke execution, not merge-policy superiority or collision-quality
  evidence.
- Layer 3 has a contact-only Newton canary plus two named capped-bed task smokes: drop/settle and
  sphere-rain contact-density proxy.
- Benchmark evaluation has not started.

## What Face-Merge Means

In this repository, a mesh is treated as many triangle faces. The face-merge baseline does this:

1. Load a bounded number of source faces from the USD mesh.
2. Build adjacency between faces that share an edge.
3. Start from small face groups.
4. Fit restricted candidate primitives, currently `box`, `sphere`, `capsule`, and an opt-in
   offline `capped_cylinder` proxy.
5. Greedily merge adjacent face groups when the merged candidate has acceptable weighted excess
   volume.
6. Stop at the primitive budget and emit a diagnostic report.

The result is a set of primitive proposals. A proposal is a candidate collision proxy, not a final
validated collider.

## What Component-Merge Gate Adds

The opt-in component-merge gate keeps the default topology-only behavior unchanged. When enabled,
it first runs the same adjacent face-group merge loop. If adjacency is exhausted before the
primitive budget is reached, it can try pairwise merges between disconnected components. Those
virtual merge candidates are ranked by weighted excess volume normalized by the mesh AABB volume,
and an optional threshold can block overly expensive virtual merges.

This is still CPD-like infrastructure, not CPD reproduction. It gives the report a clearer account
of merge policy, component counts, topology merge count, virtual merge count, blocked merge count,
and per-primitive source component IDs.

## What The Cost-Guided Change Means

The latest cost-guided merge-search smoke changes one thing in the toy path: the system can now use
one recorded cost term to choose between two possible merges.

The old/default behavior is like a simple rule of thumb: "merge touching face groups first." The
new opt-in behavior asks one more question: "among the best touching merge and the best allowed
disconnected-component merge, which one adds less extra primitive volume?"

That extra-volume proxy is AABB-normalized merge-excess. On the current `cost_guided_pair_choice`
toy fixture, the opt-in policy chooses the lower-cost virtual component merge while the default
policy chooses the available topology merge first.

The 2026-05-16 synthetic offline merge-step trace diagnostic accounting makes that toy decision
inspectable. With `report_merge_trace: steps`, the report records whether a merge was accepted or
blocked, whether it was a topology or virtual-component merge, which faces/components were joined,
and the raw plus AABB-normalized merge-excess. This is still diagnostic accounting over one
deterministic fixture, not a better merge policy or collision-quality result.

The 2026-05-16 controlled merge-search package probe carries the same toy decision one step farther:
the default package groups source faces as `[[0, 1], [2]]`, while the opt-in cost-guided package
groups them as `[[0, 2], [1]]`. Both packages map to Newton shapes. This is package-path and
mapping accounting only; it is not a Newton contact/task diagnostic, real-USD result, or
collision-quality result.

The 2026-05-16 controlled merge-search Newton probe is the follow-on task-smoke layer. It uses the
same default and opt-in packages, runs `newton_contact_smoke` first, and only then runs
`newton_drop_settle` and `newton_sphere_rain`. This means the changed toy package pair can be
exercised by named Newton diagnostics. It does not mean the opt-in grouping is better, that a real
USD package changed, or that collision quality improved.

The 2026-05-16 cost-guided lookahead merge report adds a second, still-synthetic merge/search
idea. Instead of picking only the locally cheapest first merge, `two_step_lookahead` scores a first
merge plus the best immediate follow-up merge on a tiny trap fixture. On that fixture it changes
the grouping from greedy `[[0, 2, 3], [1]]` to `[[0, 1], [2, 3]]`. This is offline algorithmic
accounting only; it is not a package probe, Newton diagnostic, real-USD result, or quality claim.

The 2026-05-16 cost-guided lookahead package probe takes exactly that toy grouping change and asks
one narrower engineering question: if we package both lanes, do they produce different
`CollisionPackage` source-face groupings and can both lanes map to Newton shapes? The answer is
recorded as package-path and mapping accounting only. It still does not run Newton contact,
drop/settle, or sphere-rain diagnostics, and it still does not say the lookahead grouping is better.

The 2026-05-16 cost-guided lookahead Newton probe is the next gate for that same toy package pair.
It runs contact first for each lane, then only runs drop/settle and sphere-rain for lanes whose
contact canary passes. This is named synthetic task-smoke status under recorded settings, not a
claim that the lookahead grouping is better geometry.

In plain terms, AABB-normalized merge-excess is the "empty wrapper space" penalty for a merge. If
two separate face groups each fit cleanly into small primitives, but one merged primitive must be
much larger to cover both, the merge has high excess. If the merged primitive is only slightly
larger than the two separate primitives together, the merge has low excess.

The AABB part means the extra volume is divided by the whole mesh's axis-aligned bounding-box
volume. That makes the number a rough ratio instead of a raw volume. For example, `0.01` means the
merge added extra primitive volume equal to about one percent of the source mesh's AABB volume.

This matters because a full CPD-style method eventually needs search decisions that are guided by
objective terms, not only by local adjacency rules. The current implementation is only the first
auditable hook for that idea. It is not a global optimizer, not a paper-faithful objective, and not
collision-quality evidence.

## What The Capped-Cylinder Proxy Adds

The capped-cylinder proxy is the first primitive-vocabulary extension. It is opt-in and offline:
the new named objective report requests `capped_cylinder` proposals, records that
`capped_cylinder` is no longer counted as an unsupported paper primitive for that run, and keeps
`frustum` and `trapezoidal_prism` as unsupported.

The proxy is deliberately labeled in output dimensions with `cap_model: hemisphere_caps` and
`proxy_fit: axis_span_radial_proxy`. That makes the boundary explicit: this is a geometry proposal
proxy for accounting and future fitting work, not paper-faithful primitive fitting.

Newton mapping is unchanged. A `capped_cylinder` package primitive remains a Newton mapping gap
until a separate Newton mapping and task-level diagnostic record exists.

## Why This Exists First

This baseline is useful because it exercises the pipeline that a real CPD reproduction will need:

- USD mesh intake and face caps;
- primitive candidate report structure;
- explicit unsupported primitive reporting;
- conversion into a `CollisionPackage`;
- Newton-independent shape mapping;
- explicitly opt-in package-path probes before Newton task reruns;
- contact-only Newton canary execution;
- one named Newton drop/settle task smoke;
- JSON reports and dated evidence records.

Without this plumbing, a later paper-faithful CPD implementation would be hard to test, hard to
record, and easy to overclaim.

## Bed Smoke Example

For the current capped bed smoke:

- source asset: GRScenes bed USD from the local asset path recorded in the manifest;
- capped extraction: 256 mesh faces;
- primitive budget: 32;
- output: 32 restricted primitive proposals, all currently boxes;
- CPD-like component-merge gate smoke: 256 initial components, 224 topology merges, 0 virtual
  component merges needed, 0 blocked merges, and 32 final components;
- CPD-like offline objective smoke: 32/32 primitive budget, 32/32 assigned-point containment
  proxy, accepted normalized merge-excess sum `0.000996148870132146`, and 3 unsupported paper
  primitive types still outside the baseline;
- CPD-like capped-cylinder proxy objective smoke: 32/32 primitive budget, 32/32 assigned-point
  containment proxy, unsupported paper primitive count 2, with `frustum` and
  `trapezoidal_prism` still unsupported and no Newton mapping claim;
- CPD-like synthetic objective comparison: three in-memory fixtures record topology-only versus
  component-merge accounting, including disconnected and blocked-merge labels;
- CPD-like cost-guided merge smoke: one in-memory fixture records old/new diagnostic accounting
  where the opt-in policy uses AABB-normalized merge-excess to choose a virtual component merge
  instead of the default topology merge;
- Newton contact smoke: 32 mapped box descriptors and one representative box contact canary;
- observed representative contact count: 1.
- Newton drop/settle smoke: all 32 proposals mapped into one compound package body, dropped on a
  static plane, with contact, final-speed, and support-height metrics recorded.
- Newton sphere-rain smoke: all 32 proposals mapped as a static package, 9 probe spheres dropped
  over the package footprint, and package-probe contact-density proxy metrics recorded.

This proves the pipeline can produce and ingest a simple primitive proposal report. It does not
prove the proposals are good collision geometry.

## What It Does Not Prove

Do not use the current face-merge baseline to claim:

- full CPD paper reproduction;
- paper-scope primitive coverage;
- paper-faithful component classification or merge optimization;
- paper-scope search or optimization;
- collision quality;
- broad task-level Newton simulation success beyond the recorded capped-bed drop/settle and
  sphere-rain contact-density proxy smokes;
- benchmark superiority over CoACD, V-HACD, convex hulls, manual colliders, or Newton-native
  approximate mesh modes;
- deployment readiness or safety certification.

## Safe Wording

Use:

- "geometry-only CPD-like face-merge primitive proposal smoke";
- "CPD-inspired restricted primitive baseline";
- "opt-in CPD-like component-merge gate";
- "primitive proposals consumed by a contact-only Newton canary";
- "one named capped-bed drop/settle smoke";
- "one named capped-bed sphere-rain contact-density proxy smoke";
- "offline paper-aligned surrogate objective report";
- "synthetic objective comparison";
- "focused CPD-like cost-guided merge-search smoke";
- "not a full CPD paper reproduction";
- "not collision-quality evidence."

Avoid:

- "CPD reproduced";
- "collision package validated";
- "simulation-checked" without naming the exact task record;
- "benchmark result";
- "safe collider."

## Next Step

The next useful step is not to strengthen the claim on this baseline. The repository now has the
second asset-class smoke, the small CPD-like component-merge gate, an offline paper-aligned
surrogate objective report, deterministic synthetic comparison cases, one focused cost-guided
merge-search smoke, deterministic expected-failure workbench coverage, one opt-in offline
capped-cylinder proxy report, synthetic package/Newton probes for controlled primitive selection
and merge/search changes, a bounded two-step lookahead merge/search diagnostic, a follow-on
synthetic package/mapping probe for the lookahead-changed toy grouping, and an in-review synthetic
Newton task-smoke probe for that same package pair. Bed/Franka reruns should wait until a separate
real package changes and passes full mapping, contact-canary, task-gate, and dated-record gates.
Newton probes should not be broadened for new primitive kinds until mapping support and a dated
diagnostic record exist. Paper-faithful CPD decomposition work should still avoid full
reproduction claims until primitive coverage, benchmark settings, and dated experiment records
exist.
