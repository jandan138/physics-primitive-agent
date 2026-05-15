# Bed And Franka Native Probe Comparison

This page explains the completed real-USD old/new native primitive probe comparison for the bed
and Franka smoke roles. It is a diagnostic record guide, not a benchmark report.

## One-Sentence Summary

The repository can now run capped bed and capped Franka first-mesh USDs through an old/new
primitive fitting comparison, require full Newton shape mapping before contact canaries, and run
gated drop/settle plus sphere-rain task smokes after contact passes.

## The Pipeline

The completed path is:

```text
bed or Franka USD
-> legacy CPD-like proposal lane
-> native CPD-like proposal lane
-> CollisionPackage summaries
-> full Newton mapping gate
-> Newton contact canary
-> gated drop/settle and sphere-rain task smokes
```

The command config is:

```text
configs/experiments/bed_franka_native_probe_comparison.yaml
```

Generated JSON reports are written under:

```text
reports/generated/bed_franka_native_probe_comparison/
```

That directory is intentionally gitignored. The committed records link the paths and summarize the
important statuses.

## Old Lane And New Lane

For each real USD role, the comparison runs two lanes under the same face cap, merge policy, and
primitive budget.

Legacy lane:

```text
box, sphere, capsule
```

Native lane:

```text
box, sphere, capsule, cylinder, cone, ellipsoid
```

The native lane is allowed to choose Newton-native `cylinder`, `cone`, or `ellipsoid`. After the
controlled cylinder-axis fitting update, bed still selects `box` primitives in both lanes, while
Franka's native lane selects `29` boxes plus `3` cylinders under the current surrogate.

That is useful selection/accounting evidence. It says the simple native proxy fitters can now
change one capped real-USD lane, but it still does not prove collision-quality improvement.

The offline fitting report now also includes `candidate_audit_summary` for each lane, and the
candidate-loss diagnosis report adds per-cluster reasons for remaining box selections. These are
diagnostic explanation layers, not collision-quality metrics.

## Current Results

Offline fitting report after the controlled cylinder-axis update:

- `bed_dev_smoke`: legacy `32` boxes, native `32` boxes, mapping clean, normalized volume delta
  `0.0`.
- `franka_import_smoke`: legacy `32` boxes, native `29` boxes plus `3` cylinders, mapping clean.
- real-USD candidate-loss diagnosis: bed has `32` box-selected clusters where extension
  candidates are more expensive under the surrogate; Franka has `29` such box-selected clusters
  and `3` clusters where `cylinder` is selected.

Contact comparison:

- all four lanes passed the contact canary;
- all four packages had `32` mapped primitives;
- box-only lanes produced representative `box` canary contacts;
- capped Franka native also produced a representative `cylinder` canary contact.

Task comparison:

- all four lanes passed drop/settle and sphere-rain under the recorded config;
- bed drop/settle final speed was about `0.0404565 m/s`;
- Franka legacy drop/settle final speed was about `0.0005830 m/s`, and Franka native was about
  `0.0004622 m/s`;
- both assets reported sphere-rain contact-density proxy `0.1111111111111111`.

## What This Means In The CPD Story

This moves the repository one step beyond synthetic native fitting:

```text
synthetic native fitting works on controlled toy meshes
-> real bed/Franka old/new reports run under face caps
-> Newton can consume the resulting mapped packages
-> named task smokes can run after contact canary passes
```

It does not mean the native lane is better. In this run, one capped Franka lane changes primitive
selection, but the record is still a diagnostic-gate and surrogate-accounting result, not a
collision-quality result.

The simple mental model is:

```text
paper goal: choose better convex primitives for collision detection
current slice: prove real-USD packages can reach Newton diagnostics
current diagnostic add-on: expose why remaining real-USD clusters still select boxes
next algorithm slice: use diagnosis labels to target the next primitive-choice change
```

For a more detailed paper-story walkthrough, see
[Real USD native probe in the CPD paper story](real-usd-native-probe-paper-story-explainer.md).

## Claim Boundary

Allowed wording:

- "real-USD old/new diagnostic smoke";
- "capped bed and capped Franka first-mesh scope";
- "full Newton mapping gate";
- "contact-canary smoke";
- "drop/settle and sphere-rain task smokes under recorded settings."
- "real-USD per-cluster candidate audit summary."
- "real-USD per-cluster candidate-loss diagnosis."

Do not claim:

- collision-quality improvement;
- benchmark superiority;
- whole-robot Franka collider quality;
- paper-faithful CPD reproduction;
- safety certification or deployment readiness;
- that `cylinder`, `cone`, or `ellipsoid` improved bed/Franka collision quality in this run.

## Commands

Offline fitting:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m primitive_collision_compiler.cli \
  --config configs/experiments/bed_franka_native_probe_comparison.yaml \
  --run-real-usd-native-fitting-comparison
```

Candidate-loss diagnosis:

```bash
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m primitive_collision_compiler.cli \
  --config configs/experiments/bed_franka_native_probe_comparison.yaml \
  --run-real-usd-candidate-loss-diagnosis
```

Contact canary:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m primitive_collision_compiler.cli \
  --config configs/experiments/bed_franka_native_probe_comparison.yaml \
  --run-real-usd-native-contact-comparison
```

Gated task smokes:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m primitive_collision_compiler.cli \
  --config configs/experiments/bed_franka_native_probe_comparison.yaml \
  --run-real-usd-native-task-comparison
```
