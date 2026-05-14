# CPD-Like Face-Merge Explainer

This page explains the current geometry-only CPD-like baseline in plain terms. It is a reader aid,
not new evidence and not a claim that the CPD paper has been reproduced.

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

The repository is currently between layers 2 and 3:

- Layer 1 is partially in place: the smoke path can extract a capped USD mesh.
- Layer 2 exists only as a simple CPD-like baseline, not the paper algorithm.
- Layer 3 has a contact-only Newton canary, not a task-level simulation checker.
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

## Why This Exists First

This baseline is useful because it exercises the pipeline that a real CPD reproduction will need:

- USD mesh intake and face caps;
- primitive candidate report structure;
- explicit unsupported primitive reporting;
- conversion into a `CollisionPackage`;
- Newton-independent shape mapping;
- contact-only Newton canary execution;
- JSON reports and dated evidence records.

Without this plumbing, a later paper-faithful CPD implementation would be hard to test, hard to
record, and easy to overclaim.

## Bed Smoke Example

For the current capped bed smoke:

- source asset: GRScenes bed USD from the local asset path recorded in the manifest;
- capped extraction: 256 mesh faces;
- primitive budget: 32;
- output: 32 restricted primitive proposals, all currently boxes;
- Newton contact smoke: 32 mapped box descriptors and one representative box contact canary;
- observed representative contact count: 1.

This proves the pipeline can produce and ingest a simple primitive proposal report. It does not
prove the proposals are good collision geometry.

## What It Does Not Prove

Do not use the current face-merge baseline to claim:

- full CPD paper reproduction;
- paper-scope primitive coverage;
- collision quality;
- task-level Newton simulation success;
- benchmark superiority over CoACD, V-HACD, convex hulls, manual colliders, or Newton-native
  approximate mesh modes;
- deployment readiness or safety certification.

## Safe Wording

Use:

- "geometry-only CPD-like face-merge primitive proposal smoke";
- "CPD-inspired restricted primitive baseline";
- "primitive proposals consumed by a contact-only Newton canary";
- "not a full CPD paper reproduction";
- "not collision-quality evidence."

Avoid:

- "CPD reproduced";
- "collision package validated";
- "simulation-checked";
- "benchmark result";
- "safe collider."

## Next Step

The next useful step is not to strengthen the claim on this baseline. The next useful step is to add
a task-level Newton diagnostic probe, such as a small drop or settle test with explicit solver
settings, timestep, seed, and metrics. After that, paper-faithful CPD decomposition work will have a
clearer evaluation harness.
