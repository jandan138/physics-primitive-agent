# Real USD Native Probe In The CPD Paper Story

This page gives a plain-language explanation of the latest bed/Franka native probe slice in the
story of reproducing Convex Primitive Decomposition for Collision Detection. It is explanatory
documentation, not new evidence beyond the dated records.

## Short Version

The CPD paper story is:

```text
complex mesh
-> compact convex primitive decomposition
-> collision detection with those primitives
-> quality and speed evaluation
```

The latest repository slice does not implement the paper algorithm. It records a narrower
diagnostic path:

```text
real bed or Franka USD
-> simple CPD-like primitive proposals
-> CollisionPackage
-> full Newton mapping gate
-> Newton contact canary
-> gated Newton drop/settle and sphere-rain smokes
```

That means the downstream diagnostic path can run on capped real USD inputs. It does not mean the
primitive decomposition is good, paper-faithful, or better than the previous baseline.

## Why This Slice Exists

Before improving the decomposition algorithm, the repository needs to know whether algorithm
outputs can survive the downstream collision path. A primitive set is not useful for this project
unless it can be packaged, mapped into Newton-supported shapes, and exercised by small diagnostic
tasks.

This slice answers that plumbing question for two real-USD smoke roles:

- `bed_dev_smoke`;
- `franka_import_smoke`.

It intentionally uses capped first-mesh scope. It does not claim full-asset coverage or
whole-robot Franka collider quality.

## Old Lane And Native Lane

The comparison runs two lanes under the same caps and merge settings.

Legacy lane:

```text
box, sphere, capsule
```

Native lane:

```text
box, sphere, capsule, cylinder, cone, ellipsoid
```

The native lane is allowed to choose the extra Newton-native primitive kinds. After the controlled
cylinder-axis fitting update, bed still selected only `box` primitives in both lanes, while capped
Franka's native lane selected `29` boxes plus `3` cylinders under the raw surrogate. The follow-up
support-aware admissibility rule now blocks those three low-support raw-cost cylinder wins, so the
current capped Franka native lane selects `32` boxes and reports the blocked cylinders in
candidate-loss diagnosis.

That result matters because it keeps the interpretation honest:

```text
what passed: real-USD diagnostic pipeline
what changed: capped Franka native-lane primitive selection and support-aware accounting under a surrogate
what did not happen: collision-quality validation or whole-robot collider-quality validation
```

The fitting report now adds a diagnostic candidate summary for each real-USD lane. Instead of only
saying "the lane selected boxes," it can summarize whether any final cluster would have preferred
`cylinder`, `cone`, or `ellipsoid` under the current weighted-volume surrogate. This still does
not make the native lane better; it tells us where the next fitting or search change should focus.

## What Changed Compared With The Previous State

Before this slice, the native fitting story was mostly synthetic:

```text
toy rod -> cylinder
toy cone -> cone
toy blob -> ellipsoid
```

That was useful because the fitter could be inspected on controlled shapes. It was not enough for
the bed/Franka story.

After this slice, the repository has a config-driven real-USD comparison:

```text
bed first mesh: legacy lane vs native lane
Franka first mesh: legacy lane vs native lane
```

It also has downstream Newton checks:

```text
full mapping required
-> contact canary required
-> drop/settle and sphere-rain task smokes allowed
```

The important improvement is not algorithmic quality. The important improvement is that real-USD
algorithm outputs now have a recorded path into Newton diagnostics.

## Why Passing Newton Smokes Is Not A Collision-Quality Claim

The Newton smokes answer a narrow engineering question:

```text
Can this package be mapped into Newton and participate in a small recorded task?
```

They do not answer:

```text
Is this the right collision decomposition?
Is it better than another decomposition?
Does it match the CPD paper objective?
Does it improve benchmark collision detection?
```

For those stronger claims, the repository still needs better primitive fitting, stronger
merge-search logic, paper-aligned objective selection, broader asset coverage, and benchmark
records.

## Where This Sits In The Paper Reproduction Story

The current story position is:

```text
asset intake exists
-> simple CPD-like baseline exists
-> surrogate objective reports exist
-> cost-guided toy merge smoke exists
-> Newton-native primitive mapping exists
-> synthetic native fitting can choose cylinder/cone/ellipsoid
-> synthetic native selection audit explains those toy choices
-> real-USD per-cluster candidate-loss diagnosis explains why remaining box clusters beat extensions
-> real bed/Franka diagnostic path now runs
```

The missing paper-reproduction work is still substantial:

- the paper's full primitive vocabulary is not implemented in the runtime path;
- the paper's full objective and optimizer are not implemented;
- the current native fitter is still simple and local;
- bed and capped Franka do not select extra native primitive kinds in the current support-aware
  run; capped Franka only reports three cheaper raw-cost `cylinder` candidates as support-blocked
  diagnostic accounting;
- there is no benchmark or collision-quality comparison.

## How To Read The Latest Result

Correct reading:

```text
The repository can run capped bed and capped Franka through an old/new primitive-package
diagnostic path and then through Newton contact/task smokes.
```

Incorrect reading:

```text
The CPD paper has been reproduced.
The native primitive lane is better on real USDs.
The Franka collider is validated.
The collision package is safe or production-ready.
```

## Next Steps

The next work should move from "the path runs" to "the selection logic is meaningful."

1. Use the synthetic audits and real-USD candidate-loss diagnosis to identify where primitive
   fitting or merge search is still too weak.
2. Improve one primitive-fitting or merge-search piece at a time, starting from an inspectable
   synthetic fixture.
3. Re-run bed/Franka only after the synthetic diagnostic points to an interpretable selection
   change.
4. Keep Newton contact and task probes behind the full-mapping gate.
5. Avoid benchmark or quality wording until dated comparison records exist.

## Related Pages

- [CPD paper story status](cpd-paper-story-status.md)
- [CPD latest diagnostic loop explainer](cpd-latest-diagnostic-loop-explainer.md)
- [Bed and Franka native probe comparison](bed-franka-native-probe-comparison.md)
- [Newton-native fitting comparison](newton-native-fitting-comparison.md)
- [Claim boundaries](claim-boundaries.md)
