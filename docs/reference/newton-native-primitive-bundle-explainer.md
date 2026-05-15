# Newton-Native Primitive Bundle Explainer

This page explains the latest Newton-native primitive bundle in the CPD paper story. It is a
plain-language guide, not new experiment evidence.

## One-Sentence Summary

The repository can send a synthetic collision package containing `box`, `sphere`, `capsule`,
`cylinder`, `cone`, and `ellipsoid` through Newton diagnostic paths, and a later opt-in synthetic
comparison can make the CPD-like fitter emit the three new native kinds on toy meshes; this still
is not default broad-asset behavior or full CPD reproduction.

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

The native runtime bundle improved the last two arrows:

```text
collision package
-> Newton shape mapping
-> contact/drop/sphere-rain diagnostics
```

By itself, the runtime bundle did not improve the first arrow:

```text
mesh -> primitive proposals
```

That distinction matters. Runtime support means Newton can consume a primitive if it appears in a
package. Generator support means the decomposition algorithm can discover and emit that primitive
from mesh geometry. The native bundle was runtime support. The later native-fitting comparison
adds opt-in synthetic generator support for simple `cylinder`, `cone`, and `ellipsoid` proxies.

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

The default CPD-like asset configs still primarily emit the old restricted runtime set:

```text
box, sphere, capsule
```

The native comparison config can opt into:

```text
box, sphere, capsule, cylinder, cone, ellipsoid
```

but that opt-in path is currently supported only as a synthetic fitting comparison plus declared
bed/Franka next scope. It is not yet a completed real-USD old/new comparison.

The offline capped-cylinder proxy remains separate:

```text
capped_cylinder
```

It is useful for paper-vocabulary accounting, but it is not Newton runtime support. The following
paper-scope primitives are still not Newton runtime primitives in this repository:

```text
capped_cylinder, frustum, trapezoidal_prism
```

The native bundle and fitting comparison also do not prove:

- the decomposition is better on real assets;
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

The runtime slice removed that blocker. The later native-fitting comparison begins the following
experiment on synthetic toy meshes:

```text
old generator:
mesh -> box/sphere/capsule package -> Newton diagnostics

new generator:
mesh -> box/sphere/capsule/cylinder/cone/ellipsoid package -> Newton diagnostics
```

Only after both paths run through the same real-USD objective reports and Newton diagnostics can
the project ask whether the new primitive fitting is useful for bed or Franka.

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

The native-fitting comparison record adds a separate narrow statement:

```text
On three deterministic toy meshes, the opt-in six-kind native subset can select cylinder, cone,
and ellipsoid proposals and map the resulting one-primitive packages through Newton shape mapping.
```

That statement is synthetic fitting evidence only. It is not a completed bed/Franka result.

## Next Steps In The Story

The next work should stay narrow:

1. Run old/new CPD-like objective reports on capped bed and capped Franka meshes.
2. Compare primitive kind counts, volume proxy, merge-excess accounting, mapping gaps, and failure
   labels.
3. If both real USD packages map cleanly, run contact canary first.
4. Then run drop/settle and sphere-rain for the old/new package pair.
5. Keep all outputs claim-bounded as diagnostic smoke evidence.

The synthetic comparison has now been added. It makes it easier to inspect whether a cylinder,
cone, or ellipsoid can be selected in controlled cases before interpreting noisy real assets.

## Safe Wording

Use:

- "Newton-native primitive diagnostic bundle";
- "synthetic six-kind native package smoke";
- "runtime diagnostic-path support for `cylinder`, `cone`, and `ellipsoid`";
- "opt-in synthetic native fitting comparison";
- "CPD-like generator does not emit the new native kinds by default asset configs";
- "bed and Franka are next-scope real USD assets, not completed native-fitting evidence";
- "not collision-quality evidence";
- "not full CPD paper reproduction."

Avoid:

- "CPD primitive vocabulary is supported";
- "paper primitive fitting is implemented";
- "Newton supports capped cylinders";
- "collision quality improved";
- "generator now improves bed or Franka collision proxies";
- "bed/Franka native-fitting comparison passed";
- "benchmark result."
