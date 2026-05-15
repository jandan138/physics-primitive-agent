# Newton-Native Primitive Bundle Explainer

This page explains the latest Newton-native primitive bundle in the CPD paper story. It is a
plain-language guide, not new experiment evidence.

## One-Sentence Summary

The repository can now send a synthetic collision package containing `box`, `sphere`, `capsule`,
`cylinder`, `cone`, and `ellipsoid` through Newton diagnostic paths, but the CPD-like generator
does not yet produce the three new native kinds by default.

## Where This Sits In The Paper Story

The CPD paper story can be simplified as:

```text
mesh
-> decompose into a small set of primitives
-> use those primitives for collision detection
-> compare collision-detection quality and speed
```

The repository is still below full paper reproduction. Its current workbench story is:

```text
USD or synthetic mesh
-> CPD-like baseline proposals
-> objective/report diagnostics
-> collision package
-> Newton smoke diagnostics
```

The native bundle improves the last two arrows:

```text
collision package
-> Newton shape mapping
-> contact/drop/sphere-rain diagnostics
```

It does not yet improve the first arrow:

```text
mesh -> primitive proposals
```

That distinction matters. Runtime support means Newton can consume a primitive if it appears in a
package. Generator support means the decomposition algorithm can discover and emit that primitive
from mesh geometry. The latest slice is runtime support, not generator support.

## What Changed

Before this slice, the Newton runtime path accepted only:

```text
box, sphere, capsule
```

Now the runtime diagnostic path accepts:

```text
box, sphere, capsule, cylinder, cone, ellipsoid
```

The implementation added:

- shape mapping and dimension validation for `cylinder`, `cone`, and `ellipsoid`;
- contact-canary builder calls for the three new kinds;
- drop/settle dynamic-body builder calls for the three new kinds;
- sphere-rain static-package builder calls for the three new kinds;
- conservative bounds and support-height estimates needed by task setup;
- tests that keep `capped_cylinder` as a Newton mapping gap;
- a clean-env synthetic smoke record showing contact, drop/settle, and sphere-rain can run on a
  six-kind native package.

## What Did Not Change

The CPD-like primitive generator still primarily emits the old restricted runtime set:

```text
box, sphere, capsule
```

The offline capped-cylinder proxy remains separate:

```text
capped_cylinder
```

It is useful for paper-vocabulary accounting, but it is not Newton runtime support. The following
paper-scope primitives are still not Newton runtime primitives in this repository:

```text
capped_cylinder, frustum, trapezoidal_prism
```

The latest native bundle also does not prove:

- the decomposition is better;
- collision quality improved;
- the CPD paper algorithm is reproduced;
- benchmark superiority;
- broad asset coverage;
- whole-robot collider quality.

## Why Not Force Paper Primitives Into Newton Runtime

The paper primitive vocabulary and Newton runtime vocabulary are related, but they are not the
same thing.

For paper alignment, it is useful to track missing paper categories:

```text
capped_cylinder, frustum, trapezoidal_prism
```

For Newton diagnostics, it is better to use shapes Newton can build directly:

```text
box, sphere, capsule, cylinder, cone, ellipsoid
```

That keeps the runtime path simple and auditable. If the project later adds a paper-only primitive
to runtime, it needs a separate mapping design, tests, diagnostic record, and claim boundary.

## Why This Step Was Needed Before Better Fitting

Suppose the next algorithm learns to fit a cylinder to a chair leg or an ellipsoid to a rounded
part. Without this runtime bundle, that new primitive could appear in a collision package but fail
when it reaches Newton diagnostics.

This slice removes that blocker. It makes the following future experiment possible:

```text
old generator:
mesh -> box/sphere/capsule package -> Newton diagnostics

new generator:
mesh -> box/sphere/capsule/cylinder/cone/ellipsoid package -> Newton diagnostics
```

Only after both paths run through the same diagnostics can the project ask whether the new
primitive fitting is useful.

## The Current Evidence

The dated native-bundle record supports this narrow statement:

```text
The repository can map and construct Newton diagnostic shapes for a synthetic package containing
box, sphere, capsule, cylinder, cone, and ellipsoid.
```

The clean-env smoke was run from the current worktree with `PYTHONPATH=src` so the external Python
used the reviewed code. The synthetic package passed:

- contact canary;
- drop/settle;
- sphere-rain.

This is diagnostic-path evidence only. It is not a collision-quality metric.

## Next Steps In The Story

The next work should stay narrow:

1. Build synthetic native-package comparisons.
2. Compare old `box/sphere/capsule` packages against packages that include
   `cylinder/cone/ellipsoid`.
3. Use the same objective report and Newton diagnostics for both paths.
4. Decide which new primitive fitting target is worth adding first.
5. Only then teach the CPD-like generator to emit one or more of the new native kinds.

The first comparison should use synthetic toy meshes, not broad asset claims. Synthetic fixtures
make it easier to inspect whether a cylinder, cone, or ellipsoid is actually a better proxy than a
box or capsule.

## Safe Wording

Use:

- "Newton-native primitive diagnostic bundle";
- "synthetic six-kind native package smoke";
- "runtime diagnostic-path support for `cylinder`, `cone`, and `ellipsoid`";
- "CPD-like generator does not yet emit the new native kinds by default";
- "not collision-quality evidence";
- "not full CPD paper reproduction."

Avoid:

- "CPD primitive vocabulary is supported";
- "paper primitive fitting is implemented";
- "Newton supports capped cylinders";
- "collision quality improved";
- "generator now finds cylinders/cones/ellipsoids";
- "benchmark result."
