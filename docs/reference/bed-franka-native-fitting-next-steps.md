# Bed And Franka Native Fitting Next Steps

This page records the execution sequence that moved the bed and Franka real-USD scope from a
planned slice to completed diagnostic smoke records. The completed results live in
[Bed And Franka Native Probe Comparison](bed-franka-native-probe-comparison.md).

## One-Sentence Summary

The synthetic native-fitting comparison is complete, and the follow-up real-USD diagnostic path has
now run on capped bed and capped Franka USD meshes: offline old/new reports, contact canaries, and
gated drop/settle plus sphere-rain task smokes.

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

The real-USD scope has now been run:

```text
bed_dev_smoke
franka_import_smoke
```

These roles live in `assets/manifests/cpd_like_smoke_assets.yaml`, and the completed probe config
is `configs/experiments/bed_franka_native_probe_comparison.yaml`.

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

## Completed Execution Order

### Step 1: Add A Real-USD Old/New Report Runner

Completed. The config-driven report path consumes:

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

The offline implementation stops at objective summaries, package summaries, and mapping summaries.

### Step 2: Run Offline Bed And Franka Reports

Use the face caps already declared in config:

```text
bed_dev_smoke: 256 faces
franka_import_smoke: 128 faces
```

Completed. The report answers:

- Did native fitting actually select any `cylinder`, `cone`, or `ellipsoid`?
- Did primitive count stay within budget?
- Did normalized volume improve, worsen, or stay similar?
- Did any primitive produce a Newton mapping gap?
- Did the old or native path add new failure labels?

After the support-aware admissibility update, the native path still selects boxes for bed and
capped Franka. Three capped Franka raw-cost cylinder candidates are now reported as
support-blocked. This is useful selection/accounting evidence, but it is not native primitive
quality or collision-quality improvement evidence.

### Step 3: Decide Whether Contact Canary Is Allowed

Completed. The comparison runs Newton contact canary only if:

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

Completed. After contact canary passed, the comparison ran:

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

## Completed Records

1. [Real USD Native Fitting Comparison](../records/2026-05-15-real-usd-native-fitting-comparison.md)
2. [Real USD Native Contact Comparison](../records/2026-05-15-real-usd-native-contact-comparison.md)
3. [Real USD Native Task Comparison](../records/2026-05-15-real-usd-native-task-comparison.md)

The next algorithmic focus is improving primitive fitting or merge search so real USD assets can
exercise native `cylinder`, `cone`, or `ellipsoid` choices before any native primitive value claim.
