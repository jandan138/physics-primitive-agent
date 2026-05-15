# Newton-Native Fitting Comparison

This page explains the opt-in Newton-native fitting comparison in the CPD paper story. It is a
plain-language guide to the new workbench slice, not a benchmark report.

## One-Sentence Summary

The CPD-like baseline can now opt in to simple `cylinder`, `cone`, and `ellipsoid` proposal
fitters and compare them against the older `box`/`sphere`/`capsule` subset on deterministic
synthetic meshes; bed and Franka now also have a separate real-USD old/new diagnostic probe
comparison. The synthetic report now includes a candidate weighted-volume audit table that
explains why each native primitive won on the toy fixtures.

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
the config, the primitive subsets, claim boundary, evidence level, and pointer to the bed/Franka
probe scope are owned by `configs/experiments/newton_native_fitting_comparison.yaml`.

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

## What The Selection Audit Adds

The report now includes a `candidate_audit` table for each lane. The table lists every primitive
kind considered by that lane, sorted by the same simple surrogate used by the fitter:

```text
weighted primitive volume
```

Lower is better under this narrow proxy. Ties are broken by the order in the primitive subset.

Each candidate row records:

- primitive kind;
- original candidate order;
- rank after sorting by weighted volume;
- selected flag;
- raw volume;
- weighted volume;
- AABB-normalized weighted volume;
- containment proxy flag;
- fitted dimensions.

This makes the synthetic result easier to inspect. For example, on the current fixtures, the
native lane's first-ranked candidate is:

- `cylindrical_rod`: `cylinder`;
- `tapered_cone`: `cone`;
- `ellipsoid_blob`: `ellipsoid`.

The report also records the native candidate's margin against the legacy lane's best candidate
and against the next native candidate. This is still only a toy-mesh surrogate-cost explanation.
It is not a paper-faithful CPD objective, a benchmark metric, or a collision-quality result.

For a more detailed field-by-field guide, see
[Synthetic native selection audit explainer](synthetic-native-selection-audit-explainer.md).

## What It Does Not Claim

This is not a paper-faithful CPD implementation. The new fitters are simple geometric proxies.
They do not implement the paper's full primitive fitting, search, objective, collision benchmark,
or performance comparison.

It also does not claim that real USD assets improved. The original synthetic report includes a
`real_usd_scope` section for:

```text
bed_dev_smoke
franka_import_smoke
```

That older synthetic report used status:

```text
scope_declared_not_run
```

The follow-up real-USD probe comparison has now been run through a separate config and report path.
After the controlled cylinder-axis fitting update, bed still selects only `box` primitives in both
old and native lanes, while capped Franka's native lane selects `29` boxes plus `3` cylinders. The
real-USD result is a selection/accounting milestone, not native primitive quality evidence.

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
- a rounded anisotropic blob should prefer `ellipsoid` over `box`;
- a squat cylinder should prefer `cylinder` after axis search.

If that does not work on toy meshes, running bed or Franka only creates noisy failure output. That
follow-up has now been run under explicit face caps in
`configs/experiments/bed_franka_native_probe_comparison.yaml`; the current real-USD run keeps bed
at boxes and changes capped Franka's native lane to 3 cylinders under the surrogate.

## Current Narrow Evidence

The current synthetic report supports this narrow statement:

```text
On deterministic toy meshes, the opt-in six-kind native subset can select cylinder, cone, and
ellipsoid proposals, explain those selections with candidate weighted-volume audit tables, and map
the resulting one-primitive packages through Newton shape mapping.
```

It does not support:

- better collision quality;
- better Newton task behavior;
- broad asset coverage;
- whole-robot collider quality;
- paper-faithful CPD reproduction;
- benchmark superiority.

## Real-USD Follow-Up

The completed follow-up is documented in
[Bed And Franka Native Probe Comparison](bed-franka-native-probe-comparison.md).

The real-USD result is:

1. old/new CPD-like objective reports ran on capped bed and capped Franka meshes;
2. bed selected `32` boxes in both lanes, while Franka selected `32` boxes in the legacy lane and
   `29` boxes plus `3` cylinders in the native lane;
3. all packages mapped cleanly into Newton shape descriptors;
4. contact canaries passed for all four lanes;
5. gated drop/settle and sphere-rain task smokes passed under the recorded config.

Keep all results claim-bounded as diagnostic smoke evidence, not benchmark or collision-quality
evidence.

For the detailed bed/Franka execution sequence, see
[Bed And Franka Native Probe Comparison](bed-franka-native-probe-comparison.md).
