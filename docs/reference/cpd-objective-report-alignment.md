# CPD Objective Report Alignment

This page explains how the current CPD-like objective report relates to the
Convex Primitive Decomposition for Collision Detection paper. It is a reader
aid, not new experiment evidence, and not a claim that the paper objective has
been reproduced.

For the broader paper-story map, see
[CPD paper story status](cpd-paper-story-status.md).

## Plain Answer

The current report is design-aligned with the paper story, but not yet
mathematically paper-faithful.

In plain terms: the report is a health check that asks the same kinds of
questions the paper will eventually care about, but it is not yet the paper's
actual scoring function or optimization procedure.

## Why It Is Useful Now

The paper is not only about producing primitives. It is about producing a small,
useful primitive set under geometric and collision-detection constraints. Before
the repository can implement that full algorithm, it needs a stable place to
record the accounting terms that future fitting and merge-search code will use.

The current objective report gives that stable place. It lets us compare runs
without changing the claim boundary.

## What Matches The Paper Story

The current report matches the paper story at the level of engineering
questions:

- Primitive budget: are we using too many primitive pieces?
- Primitive volume proxy: are fitted primitives much larger than the source
  geometry they represent?
- Merge-excess accounting: which merges were accepted, and how much geometric
  extra volume did they introduce?
- Containment proxy: did each current primitive cover its assigned source
  points under the report's restricted proxy check?
- Primitive vocabulary gap: which paper primitive types are still unsupported
  by the current baseline?
- Failure labels: why did a run become partial, blocked, or unsupported?

These are the right categories for a CPD reproduction workbench.

## What Is Not Paper-Faithful Yet

The current report does not yet reproduce the paper objective. In particular,
it does not provide:

- the paper's full objective formula;
- the paper's search or optimization procedure;
- paper-scope primitive coverage;
- exact containment or surface-distance evaluation;
- collision-detection quality measurement;
- benchmark comparison against other decomposition methods.

Because of that, it should be described as a paper-aligned surrogate objective
report, not a paper-faithful CPD objective.

## How To Read The Fields

`primitive_budget` is the "too many pieces?" check. If the decomposition needs
more primitives than the configured budget, it is not ready for the target
collision package shape.

`geometric_excess_proxy` is the "too much extra space?" check. If a primitive
wraps a region much larger than its assigned mesh patch, it can create contacts
where the visual object has no geometry. The current number is a proxy, not a
paper metric.

`merge_excess_terms` is the "what did merging cost?" ledger. It records accepted
topology merges, optional virtual component merges, and blocked component-merge
candidates.

## What AABB-Normalized Merge-Excess Means

In the current CPD-like baseline, a merge candidate joins two face groups into one larger face
group and fits one primitive to the joined group. The merge-excess proxy asks:

```text
How much larger is the new fitted primitive than the two old fitted primitives together?
```

The implementation records it as:

```text
excess_volume =
  merged_primitive_weighted_volume
  - left_primitive_weighted_volume
  - right_primitive_weighted_volume

normalized_excess =
  excess_volume / source_mesh_aabb_volume
```

`source_mesh_aabb_volume` is the volume of the axis-aligned bounding box around the source mesh
points. In plain language, it is the volume of the simple rectangular box that contains the whole
mesh.

The normalization turns an absolute volume into a rough fraction of the object's bounding-box
volume. A normalized excess of `0.01` means the merge added extra primitive volume equal to about
one percent of the source mesh AABB volume. A smaller value means the merge added less extra
wrapper volume under this proxy.

This is useful for comparing merge candidates because a bad merge often creates a primitive that
spans empty space between unrelated pieces. A low merge-excess says "one primitive can cover these
two groups without adding much extra volume." A high merge-excess says "this merge probably wraps a
lot of empty space."

This is not a collision-quality metric. It does not measure penetration, contact stability,
surface distance, or benchmark performance. It is a geometry-only surrogate used for diagnostic
accounting and, in the cost-guided smoke, for one opt-in toy merge decision.

`containment_proxy` is the "did the assigned points fit inside the candidate?"
check. It is deliberately narrower than full geometric containment.

`paper_primitive_gap` is the "what primitive vocabulary is missing?" list. It
keeps the baseline honest when the paper supports primitive types that the
current implementation does not.

`failure_labels` are the "why should a reviewer distrust this run?" labels.
They are part of the evidence, not merely errors to hide.

## Current Algorithmic Step

The repository now has one small step beyond a pure health check: the focused
CPD-like cost-guided merge-search smoke uses AABB-normalized merge-excess as a
decision-making cost on a deterministic synthetic fixture.

That does not make the report paper-faithful. It means one report term has been
connected to one opt-in merge decision in a toy setting.

Put another way: the report used to be only a dashboard after the drive. The new smoke lets one
dashboard number affect one steering decision on a controlled toy road. That is useful for the
paper story because future CPD work needs objective-guided search, but the current scope remains a
single restricted decision hook.

## Next Algorithmic Step

The next step is to broaden or deepen this path only where the expected failure
mode is clear.

The recommended order is:

1. Add one broader synthetic fixture only if it exposes a specific expected
   failure mode.
2. Add one focused primitive-fitting improvement against that fixture.
3. Compare old and new outputs with the same objective report.
4. Re-run the bed and Franka smoke paths only after the synthetic report changes
   in a named, inspectable way.
5. Use Newton drop/settle or sphere-rain as downstream diagnostics, not as the
   primary optimization target.

That keeps the story disciplined: first improve the decomposition logic under a
stable report, then ask whether Newton diagnostics reveal new failure modes.

## Safe Wording

Use:

- "paper-aligned surrogate objective report";
- "diagnostic accounting for future CPD reproduction work";
- "design-aligned with the paper story";
- "focused CPD-like cost-guided merge-search smoke";
- "not a paper-faithful objective implementation";
- "not collision-quality evidence."

Avoid:

- "paper objective reproduced";
- "CPD objective implemented";
- "CPD optimizer implemented";
- "decomposition quality validated";
- "collision quality score";
- "benchmark metric."

## Claim Boundary

This page does not add a new supported claim. It clarifies how to interpret the
existing objective report while preserving the repository's current boundary:
CPD reproduction workbench, not full CPD paper reproduction.
