# Bed And Franka Native Fitting Next Steps

This page turns the current CPD paper story into the next executable slice. It is a planning
guide for the bed and Franka real-USD scope, not completed experiment evidence.

## One-Sentence Summary

The synthetic native-fitting comparison is complete; the next step is to run the same old/new
comparison on capped bed and capped Franka USD meshes, inspect the offline reports first, and only
then decide whether the generated packages are ready for Newton contact and task smokes.

## Current Starting Point

Completed narrow evidence:

```text
synthetic mesh
-> legacy subset or native subset
-> objective/report diagnostics
-> one-primitive CollisionPackage
-> Newton shape mapping check
```

The completed synthetic cases show:

- `cylindrical_rod`: legacy selects `capsule`, native selects `cylinder`;
- `tapered_cone`: legacy selects `capsule`, native selects `cone`;
- `ellipsoid_blob`: legacy selects `box`, native selects `ellipsoid`.

The real-USD scope is declared but not run:

```text
bed_dev_smoke
franka_import_smoke
```

These roles live in `assets/manifests/cpd_like_smoke_assets.yaml`, and the next-scope config is
`configs/experiments/newton_native_fitting_comparison.yaml`.

## Why This Is The Next Slice

The CPD paper story needs more than "Newton can consume shapes." It needs a decomposition path
that can choose a useful primitive set from mesh geometry.

The repository now has two ingredients:

```text
runtime support:
CollisionPackage can map box/sphere/capsule/cylinder/cone/ellipsoid into Newton diagnostics

synthetic fitting support:
CPD-like fitter can opt into cylinder/cone/ellipsoid on tiny toy meshes
```

The missing bridge is:

```text
real USD mesh
-> old/new CPD-like primitive proposal reports
-> same objective fields
-> mapping-gap inspection
-> Newton smoke only if the package is mappable
```

Bed and Franka are the right next assets because they are already in the repo manifests and cover
two different shapes of risk: furniture geometry and robot asset intake.

## Exact Old/New Comparison

For each real USD role, run two decomposition paths under the same face cap and merge policy.

Legacy path:

```text
primitive_subset = box, sphere, capsule
```

Native path:

```text
primitive_subset = box, sphere, capsule, cylinder, cone, ellipsoid
```

Compare these fields:

- selected primitive kind counts;
- primitive budget pressure;
- normalized weighted primitive volume;
- accepted and blocked merge-excess accounting;
- assigned-point containment proxy;
- unsupported paper primitive gap;
- Newton shape mapping status;
- failure labels.

This is still an offline diagnostic comparison. It is not a collision-quality metric.

## Recommended Execution Order

### Step 1: Add A Real-USD Old/New Report Runner

Add a config-driven report path that consumes:

- `cpd_like.asset_roles`;
- `cpd_like.legacy_primitive_subset`;
- `cpd_like.native_primitive_subset`;
- `cpd_like.max_source_faces_by_role`;
- `native_fitting_comparison.real_usd_roles`.

The output should contain one row per asset role and per subset:

```text
bed_dev_smoke / legacy
bed_dev_smoke / native
franka_import_smoke / legacy
franka_import_smoke / native
```

The first implementation should stop at offline objective plus mapping summary. It should not run
Newton simulation yet.

### Step 2: Run Offline Bed And Franka Reports

Use the face caps already declared in config:

```text
bed_dev_smoke: 256 faces
franka_import_smoke: 128 faces
```

The report should answer:

- Did native fitting actually select any `cylinder`, `cone`, or `ellipsoid`?
- Did primitive count stay within budget?
- Did normalized volume improve, worsen, or stay similar?
- Did any primitive produce a Newton mapping gap?
- Did the old or native path add new failure labels?

If the native path does not select new primitives, that is still useful evidence. It means the
simple synthetic proxy fitters are not yet useful on that capped real mesh.

### Step 3: Decide Whether Contact Canary Is Allowed

Run Newton contact canary only if:

- all primitives in the package map to Newton shapes;
- the package status is not a dependency or mapping gap;
- failure labels are understood and recorded;
- the claim boundary remains diagnostic smoke only.

The contact canary answers only:

```text
Can representative mapped primitive types enter Newton contact generation?
```

It does not answer whether the collider is good.

### Step 4: Run Drop/Settle Or Sphere-Rain Only After Contact Canary

If contact canary is clean, run:

```text
old bed package -> drop/settle and sphere-rain
native bed package -> drop/settle and sphere-rain
old Franka capped package -> contact first, then task smoke only if appropriate
native Franka capped package -> contact first, then task smoke only if appropriate
```

Franka remains a capped first-mesh geometry smoke unless a separate whole-robot/articulation plan
exists. Do not turn this into a whole-robot collider-quality claim.

## Stop Conditions

Stop and record a failure or partial result if:

- the USD asset cannot be opened;
- capped mesh extraction changes unexpectedly;
- either old or native report cannot produce finite JSON;
- native primitives produce mapping gaps;
- primitive count exceeds budget;
- expected claim boundaries cannot be preserved;
- Newton environment readiness is missing.

Failure records are useful. They tell the project which part of the CPD reproduction story is
still weak.

## Paper-Story Interpretation

If this slice succeeds, the story becomes:

```text
synthetic toy meshes show native primitive fitting can work in controlled cases
bed/Franka capped USD reports show whether the same option is useful on real assets
Newton contact/task smokes show whether the resulting package can enter diagnostics
```

It still will not mean:

- full CPD paper reproduction;
- paper-faithful objective optimization;
- benchmark superiority;
- collision-quality improvement;
- whole-robot collider quality;
- safety certification.

## Recommended Next Commits

1. `feat: add real usd native fitting comparison report`
2. `docs: record bed franka native fitting offline comparison`
3. `feat: add native fitting contact canary comparison`
4. `docs: record native fitting newton contact comparison`

Only after those records exist should drop/settle and sphere-rain old/new task comparisons become
the main focus.
