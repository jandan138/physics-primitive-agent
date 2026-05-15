# Newton-Native Fitting Comparison

This page explains the opt-in Newton-native fitting comparison in the CPD paper story. It is a
plain-language guide to the new workbench slice, not a benchmark report.

## One-Sentence Summary

The CPD-like baseline can now opt in to simple `cylinder`, `cone`, and `ellipsoid` proposal
fitters and compare them against the older `box`/`sphere`/`capsule` subset on deterministic
synthetic meshes; bed and Franka USD assets are declared as the next real-asset scope, but they
are not yet reported as completed old/new native-fitting evidence.

## What Changed

The previous native primitive bundle proved that Newton diagnostic paths could map and construct
six native primitive kinds:

```text
box, sphere, capsule, cylinder, cone, ellipsoid
```

This slice moves one step earlier in the pipeline. The CPD-like primitive fitter can now opt in
to three simple native proxy fits:

- `cylinder`: axis-span radial proxy;
- `cone`: right-circular cone axis-span proxy;
- `ellipsoid`: scaled local ellipsoid proxy.

The new command is:

```bash
python -m primitive_collision_compiler.cli \
  --config configs/experiments/newton_native_fitting_comparison.yaml \
  --run-newton-native-fitting-comparison
```

Without `--config`, the command still runs the same default in-memory synthetic comparison. With
the config, the primitive subsets, claim boundary, evidence level, and bed/Franka next-scope roles
are owned by `configs/experiments/newton_native_fitting_comparison.yaml`.

It compares:

```text
legacy subset: box, sphere, capsule
native subset: box, sphere, capsule, cylinder, cone, ellipsoid
```

on three synthetic fixtures:

- `cylindrical_rod`;
- `tapered_cone`;
- `ellipsoid_blob`.

For each fixture, the report records the selected primitive kind, objective-report volume proxy,
collision package mapping status, and whether the native subset selected the expected new native
kind.

## What It Does Not Claim

This is not a paper-faithful CPD implementation. The new fitters are simple geometric proxies.
They do not implement the paper's full primitive fitting, search, objective, collision benchmark,
or performance comparison.

It also does not claim that real USD assets improved. The report includes a `real_usd_scope`
section for:

```text
bed_dev_smoke
franka_import_smoke
```

with status:

```text
scope_declared_not_run
```

That means bed and Franka are now explicitly in the next experiment scope. It does not mean the
old/new native-fitting comparison has already been run on those assets.

## Where This Sits In The Paper Story

The story is now:

```text
synthetic mesh
-> old primitive subset or native primitive subset
-> objective/report diagnostics
-> collision package
-> Newton shape mapping check
```

This is the first narrow bridge between "Newton can consume native shapes" and "the CPD-like
proposal path can emit native shapes when explicitly asked." The default asset configs still keep
the older restricted subset unless a native-fitting comparison config opts into the six-kind
subset.

## Why Synthetic Comes Before Bed And Franka

The synthetic fixtures are intentionally tiny and inspectable. They let reviewers see whether the
native subset picks the intended primitive:

- a rod should prefer `cylinder` over `capsule`;
- a tapered shape should prefer `cone` over `capsule`;
- a rounded anisotropic blob should prefer `ellipsoid` over `box`.

If that does not work on toy meshes, running bed or Franka only creates noisy failure output. Once
the synthetic report is stable, the next step is to run the same old/new comparison on capped bed
and capped Franka USD meshes under explicit face caps.

## Current Narrow Evidence

The current synthetic report supports this narrow statement:

```text
On three deterministic toy meshes, the opt-in six-kind native subset can select cylinder, cone,
and ellipsoid proposals and map the resulting one-primitive packages through Newton shape mapping.
```

It does not support:

- better collision quality;
- better Newton task behavior;
- broad asset coverage;
- whole-robot collider quality;
- paper-faithful CPD reproduction;
- benchmark superiority.

## Next Steps

1. Run old/new CPD-like objective reports on capped bed and capped Franka meshes.
2. Compare primitive kind counts, volume proxy, merge-excess accounting, mapping gaps, and failure
   labels.
3. If both real USD packages map cleanly, run contact canary first.
4. Then run drop/settle and sphere-rain for the old/new package pair.
5. Keep all results claim-bounded as diagnostic smoke evidence, not benchmark or collision-quality
   evidence.
