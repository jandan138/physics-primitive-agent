# CPD Next Steps After Real USD Mirrors

This page explains the CPD-like algorithm work after the bed and Franka USD mirrors were
materialized into ignored repo-local paths. It is a status and planning guide, not benchmark
evidence.

## Plain Summary

The repository now has stable real-USD smoke inputs:

```text
bed source USD     -> assets/raw/mirrors/.../bed_dev_smoke/
Franka source USD  -> assets/raw/mirrors/.../franka_import_smoke/
```

It also has a downstream diagnostic path:

```text
local USD mirror
-> capped first mesh
-> CPD-like primitive proposals
-> CollisionPackage
-> Newton mapping
-> contact canary
-> gated drop/settle and sphere-rain smokes
```

The important current limitation is simple:

```text
the path runs, and one Franka native-lane selection changed, but quality is still unproven
```

So the next work should not be "add more assets" or "claim native primitives are better." The next
work should use the candidate-loss diagnosis to choose the next primitive-fitting or merge-search
change.

## What We Have Now

Current evidence supports this narrow story:

1. Bed and Franka real USDs can be mirrored locally without committing raw assets.
2. The runtime resolver prefers local mirrors when they exist.
3. Capped bed and capped Franka first meshes can run through old/new CPD-like reports.
4. Bed currently selects `box` primitives in both lanes; Franka's native lane now selects `3`
   cylinders under the current surrogate.
5. The selected packages can map into Newton and run recorded smoke diagnostics.

That is selection/accounting evidence. It is not evidence that the decomposition is good,
paper-faithful, or better than a simpler baseline.

## The Next Five Small Goals

### 1. Lock The Real-USD Baseline

Before changing the algorithm, regenerate the current reports from the local mirrors and treat
them as the reference state:

```text
bed: legacy boxes vs native boxes
Franka: legacy boxes vs native mostly boxes plus 3 cylinders
candidate diagnosis: remaining box clusters lose by surrogate candidate cost
Newton probes: allowed only after full mapping and contact canary
```

The purpose is to make future changes easy to compare against the current known result.

### 2. Diagnose Why Native Primitives Lose

The candidate audit already says that boxes win on current final clusters. The next diagnostic
should explain why in more actionable terms:

```text
is the face cluster too box-shaped?
is the candidate primitive fitting too crude?
is the merge search creating clusters that hide cylindrical/conic/ellipsoid structure?
is the current weighted-volume surrogate over-penalizing non-box primitives?
```

This should produce a small report, not a quality claim.

### 3. Improve One Controlled Algorithm Piece

Pick one narrow algorithm change at a time:

- better `cylinder` axis/radius fitting;
- better `cone` taper fitting;
- better `ellipsoid` axis fitting;
- a merge-search rule that preserves candidate shapes instead of wrapping them into boxes too
  early;
- a primitive-choice cost that uses the existing objective fields more directly.

The change should first pass on synthetic toy meshes where the expected behavior is inspectable.

### 4. Re-Run Synthetic Workbenches Before Real USD

The synthetic sequence should come before bed/Franka reruns:

```text
toy fixture
-> old/new objective report
-> candidate audit
-> expected-failure workbench
-> Newton mapping check if a package is produced
```

This keeps the algorithm work debuggable. If a change cannot explain itself on a tiny mesh, it is
too early to interpret it on bed or Franka.

### 5. Re-Run Bed/Franka With The Same Gates

Only after the synthetic result is clean, re-run the real-USD comparison:

```text
local bed/Franka mirror
-> old/new fitting report
-> candidate audit
-> full Newton mapping gate
-> contact canary
-> gated task smokes
```

If a real asset still chooses only boxes, that is still a useful negative result. Record it and
return to the fitting/search diagnosis instead of overclaiming.

## Completed Candidate-Loss Slice

The implemented slice is:

```text
candidate-loss diagnosis report
```

In plain terms, this is a "why did the box win?" report. For each final cluster in the native
lane, it should record:

- selected primitive kind;
- rank of `cylinder`, `cone`, and `ellipsoid`;
- weighted-volume gap between the selected primitive and the best native extension primitive;
- cluster geometry hints, such as AABB aspect ratios and point count;
- whether the likely bottleneck is primitive fitting, merge search, or objective weighting.

This slice avoids guessing. It turns the current bed/Franka result from:

```text
bed boxes won; Franka mostly boxes won, with 3 cylinders selected
```

into:

```text
remaining box selections won for measurable surrogate-cost reasons
```

That gives the next algorithm change a target.

## Big Goal Versus Small Goals

The first big goal is not "fully reproduce the CPD paper." It is narrower:

```text
build a credible CPD reproduction workbench where each algorithm change is measurable,
claim-bounded, and runnable through Newton diagnostics when appropriate
```

The five small goals are the stepping stones toward that:

```text
lock baseline
-> diagnose selection failure
-> improve one algorithm piece
-> verify on toy meshes
-> re-run bed/Franka under the same gates
```

Completing the small goals would make the next algorithmic result interpretable. It would still
not be benchmark superiority, full paper reproduction, whole-robot Franka collider quality, or
safety certification.

## Related Pages

- [Asset mirror materialization](asset-mirror-materialization.md)
- [Real USD native probe in the CPD paper story](real-usd-native-probe-paper-story-explainer.md)
- [CPD latest diagnostic loop explainer](cpd-latest-diagnostic-loop-explainer.md)
- [Bed and Franka native probe comparison](bed-franka-native-probe-comparison.md)
- [CPD paper story status](cpd-paper-story-status.md)
- [Claim boundaries](claim-boundaries.md)
