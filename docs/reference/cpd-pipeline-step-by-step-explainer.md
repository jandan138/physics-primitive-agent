# CPD Pipeline Step-By-Step Explainer

This page explains the difference between the CPD paper pipeline and the current Newton CPD
workbench pipeline. It is a plain-language guide for readers who need the whole story one step at
a time.

It does not add new experiment evidence. It does not claim full CPD paper reproduction,
benchmark superiority, collision-quality validation, real-asset improvement, deployment
readiness, or safety certification.

## One-Sentence Summary

The CPD paper is mainly about how to automatically decompose a mesh into a good set of collision
primitives. This repository currently focuses on building the diagnostic workbench that lets each
small decomposition change be inspected, packaged, run through Newton smokes, and recorded with
clear claim boundaries.

## The Whole Pipeline

The full story can be read as:

```text
mesh
-> primitive candidates
-> primitive fitting
-> objective / cost
-> search / decomposition
-> collision package
-> Newton mapping
-> Newton task smokes
-> benchmark / quality evaluation
```

The first five steps are mostly the CPD algorithm story. The next three steps are mostly this
project's Newton workbench story. The final step is the paper-style evaluation story.

## Step 1: Mesh

Question:

```text
What geometry enters the pipeline?
```

In the paper story, the input is a mesh that should be approximated by convex primitive shapes for
collision detection.

In the repository, the input can be:

- a USD asset opened through the asset intake path;
- a capped first mesh from a real USD smoke asset;
- a deterministic synthetic toy mesh.

Current status: partially in place. The repository can open and mirror selected USD assets and can
also run deterministic synthetic fixtures.

Boundary: this is input plumbing, not a claim that the final decomposition is good.

## Step 2: Primitive Candidates

Question:

```text
Which simple shapes are even allowed to represent the mesh?
```

The CPD paper primitive vocabulary is:

- `oriented_bounding_box`;
- `sphere`;
- `capsule`;
- `capped_cylinder`;
- `frustum`;
- `isosceles_trapezoidal_prism`.

The current Newton runtime vocabulary used by this repository is a separate engineering set:

- `box`;
- `sphere`;
- `capsule`;
- `cylinder`;
- `cone`;
- `ellipsoid`.

The CPD paper has its own primitive vocabulary and fitting story. Newton has its own runtime shape
support. Those two sets are not automatically the same.

Current status: the repository is Newton-native first for runtime diagnostics. It can exercise
Newton-supported primitive kinds in synthetic paths, but the CPD-like default baseline is still
restricted and not paper-faithful.

Boundary: supporting a primitive in a diagnostic path does not mean the CPD-like generator emits
that primitive by default or that the primitive improves collision quality.

## Step 3: Primitive Fitting

Question:

```text
Given one mesh region, how do we place a primitive so it covers or approximates that region?
```

For example, a thin cylindrical part might be tested against a `box` fit and a `cylinder` fit.
Fitting decides the primitive parameters: position, size, axis, radius, and related values.

In the CPD paper story, fitting is a core algorithmic piece.

In the repository, fitting exists as a restricted diagnostic implementation. It is enough to run
toy probes and candidate audits, but it is not the full paper fitting method.

Current status: early algorithmic support, usable for controlled diagnostics.

Boundary: the current fitting reports explain why a candidate was selected or blocked under the
current surrogate. They do not prove paper-faithful primitive fitting or better collision
geometry.

## Step 4: Objective / Cost

Question:

```text
How do we score one primitive choice or one merge choice?
```

The paper's core scoring rule is a collapse cost: how much extra primitive volume is introduced by
merging two primitive groups. The paper also records primitive type weighting so a primitive that
is cheap or common in a downstream physics engine can be preferred.

The repository's current reports add extra diagnostic fields such as primitive-budget pressure,
proxy volume, containment proxy, and AABB-normalized merge-excess. Those are useful health-check
fields, but they are not the paper's primary collapse rule by themselves.

The repository has a paper-aligned surrogate objective report. "Paper-aligned" means it records
paper-shaped accounting categories. It does not mean it computes the paper's full objective.

Current status: useful diagnostic accounting exists.

Boundary: the current objective report is a reviewable health check, not the paper's exact
objective implementation.

## Step 5: Search / Decomposition

Question:

```text
How does the system choose the final set of mesh regions and primitives under a budget?
```

This is one of the biggest differences between the paper and the repository today.

The CPD paper is about a systematic decomposition method. The repository currently has smaller
controlled pieces:

- greedy face merge;
- opt-in component merge;
- cost-guided pairwise merge on toy fixtures;
- two-step lookahead on one deterministic trap fixture, explicitly as a non-paper surrogate
  extension.

Current status: restricted synthetic merge/search diagnostics, not paper-scope search.

Boundary: a toy fixture where a heuristic changes grouping is not evidence that the heuristic is
better in general.

## Step 6: CollisionPackage

Question:

```text
Can the selected primitives be stored in a structured engine-facing package?
```

`CollisionPackage` is the repository bridge between decomposition output and Newton diagnostics.
It records the generated primitives and the package metadata needed by later stages.

This step is not the core CPD paper algorithm. It is engineering infrastructure required by this
project.

Current status: in place for current diagnostic lanes.

Boundary: generating a package does not mean the package has been validated as good collision
geometry.

## Step 7: Newton Mapping

Question:

```text
Can each package primitive become an actual Newton diagnostic shape?
```

This matters because a primitive can exist in an offline report while still not being supported by
the runtime diagnostic path.

Current status: Newton-native primitives can be mapped and constructed in the diagnostic path.
Paper-only or unsupported primitive types stay outside runtime claims until separate mapping and
diagnostic records exist.

Boundary: shape mapping is not a Newton task result and not collision-quality evidence.

## Step 8: Newton Task Smokes

Question:

```text
Can the mapped package enter small Newton diagnostic tasks without failing the smoke gates?
```

Current task smokes include:

- contact canary;
- drop/settle;
- sphere-rain.

These are diagnostic gates. They show that a named package can enter specific Newton task-smoke
paths under recorded settings.

Current status: in place for selected synthetic package pairs and capped first-mesh real-USD
diagnostic lanes.

Boundary: a task smoke is not a benchmark, not a broad failure search, not real contact-stress
measurement, and not proof that the collision representation is better.

## Step 9: Benchmark / Quality Evaluation

Question:

```text
Does the method improve collision detection under benchmark conditions?
```

This is where paper-level claims would need broader assets, baselines, metrics, and repeatable
reports.

Current status: not started for paper-level claims.

Boundary: no benchmark superiority, collision-quality validation, deployment readiness, or safety
certification is supported.

## Where The Latest Four-Block Report Fits

The latest four-block report is not a new decomposition algorithm. It is a workbench status
report.

It summarizes one already recorded synthetic slice:

```text
cost_guided_lookahead synthetic fixture
-> primitive fitting/selection status
-> merge/search status
-> offline diagnostic/package status
-> recorded Newton task-smoke status
-> command-only four-block evidence map
```

The report answers:

```text
For this one recorded slice, which blocks have evidence and which claims are still out of scope?
```

It does not rerun decomposition, USD loading, package generation, or Newton tasks. It links dated
records and keeps the claim boundary visible.

## Practical Reading Guide

Use this mental separation:

```text
CPD paper algorithm = how to choose and optimize primitives
Newton workbench = how to inspect, package, run, and record a candidate primitive result
Benchmark = how to prove the result is better under evaluation settings
```

Current repository strength:

- asset intake and reproducible records;
- CPD-like diagnostic plumbing;
- surrogate objective accounting;
- Newton package and task-smoke gates;
- four-block evidence reporting.

Current repository gaps:

- paper-faithful primitive fitting;
- paper collapse-cost rule plus primitive weighting;
- paper-scope search / optimization;
- paper primitive vocabulary alignment;
- benchmark and collision-quality evaluation.

## Recommended Next Step

The next algorithmic slice should follow the paper gap matrix and offline lane spec:

- start with an offline-only synthetic toy fixture;
- record paper-side `Q` operator fields;
- record paper primitive-fit audit fields;
- record paper collapse-cost fields;
- keep Newton, bed, Franka, and benchmark work out of scope for that slice.

Only after a changed package is explained on synthetic fixtures should it move through package,
mapping, contact, task, and dated-record gates. Real-asset reruns should wait for a separate
real-package change.

See [CPD paper reproduction gap matrix](cpd-paper-reproduction-gap-matrix.md) and
[CPD paper-faithful offline lane spec](cpd-paper-faithful-offline-lane-spec.md) for the detailed
next-lane boundary.
