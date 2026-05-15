# CPD-Like Face-Merge Explainer

This page explains the current geometry-only CPD-like baseline in plain terms. It is a reader aid,
not new evidence and not a claim that the CPD paper has been reproduced.

For the broader paper-story map, see
[CPD paper story status](cpd-paper-story-status.md).

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
- Layer 3 now has an offline paper-aligned surrogate objective report over the capped bed
  CPD-like baseline.
- Layer 3 also has a command-only synthetic objective comparison over deterministic toy meshes.
- Layer 3 has a contact-only Newton canary plus two named capped-bed task smokes: drop/settle and
  sphere-rain contact-density proxy.
- Layer 4 has not started.

## What Face-Merge Means

In this repository, a mesh is treated as many triangle faces. The face-merge baseline does this:

1. Load a bounded number of source faces from the USD mesh.
2. Build adjacency between faces that share an edge.
3. Start from small face groups.
4. Fit restricted candidate primitives, currently `box`, `sphere`, and `capsule`.
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

## Why This Exists First

This baseline is useful because it exercises the pipeline that a real CPD reproduction will need:

- USD mesh intake and face caps;
- primitive candidate report structure;
- explicit unsupported primitive reporting;
- conversion into a `CollisionPackage`;
- Newton-independent shape mapping;
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
- CPD-like synthetic objective comparison: three in-memory fixtures record topology-only versus
  component-merge accounting, including disconnected and blocked-merge labels;
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
surrogate objective report, and deterministic synthetic comparison cases. The next paper-story
slice should use those cases to guide one focused primitive-fitting or merge-search improvement
before changing Newton probes or making any collision-quality claim. Paper-faithful CPD
decomposition work should still avoid full reproduction claims until primitive coverage, benchmark
settings, and dated experiment records exist.
