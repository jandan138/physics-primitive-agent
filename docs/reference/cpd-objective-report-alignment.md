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

`paper_alignment` is the "how does this report relate to the paper?" map. It records the paper
source, Eq.4 reference, which current JSON terms correspond to that paper-story role, and which
paper-faithful parts are still missing. This is metadata for audit, not a new score.

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

## What The Eq.4 Alignment Metadata Adds

The paper's Eq.4 collapse cost has the shape:

```text
C(p0,p1)=V(merge(p0,p1))-(V(p0)+V(p1))
```

The report now separates two related quantities:

- raw Eq.4-like volume delta: `accepted_eq4_cost_*` and `blocked_eq4_cost_*`;
- AABB-normalized diagnostic cost: `accepted_normalized_excess_*` and
  `blocked_normalized_excess_*`.

The raw delta keeps the paper-shaped volume difference visible. The normalized value keeps the
repo's existing diagnostic behavior: divide by the source mesh AABB volume, with a small floor for
degenerate planar meshes, so thresholds and reports are scale-aware.

The `paper_alignment` metadata also records:

- `metadata_scope`: this is term-category mapping, not Eq.4 implementation;
- `implemented_term_path`: the current JSON path is `metrics.merge_excess_terms`;
- `current_cost_units`: mixed raw and AABB-normalized weighted primitive volume;
- `cost_unit_terms`: which JSON paths are raw volume deltas and which are normalized diagnostics;
- `merge_cost_volume_basis`: the current merge history uses `decomposition.weighted_volume`;
- `objective_report_weights_applied_to_merge_history`: false, because report-time weights do not
  rewrite historical merge decisions;
- `threshold_scope`: virtual component merges only;
- `computes_paper_eq4`: false;
- `non_faithful_gaps`: the remaining gaps before paper-faithful objective/search claims.

This keeps the report honest. It says "this is where the current surrogate cost touches the paper
story" without claiming the paper objective has been implemented.

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

## What The Expected-Failure Workbench Adds

The deterministic expected-failure synthetic workbench is a second kind of offline report around
the same objective accounting. Instead of asking "which policy looks cheaper?", it asks:

```text
For a known CPD-paper gap, does the current report still expose the expected limitation flags?
```

Each expected limitation fixture records:

- the fixture id and geometry summary;
- the known CPD-paper gap being exercised;
- expected, observed, missing, and unexpected diagnostic flags;
- the limitation class;
- the next capability needed, such as primitive-fit extension or merge-search extension.

The first three fixtures cover:

- restricted primitive vocabulary and missing paper-scope primitive fitting;
- a single proxy wrapping disconnected components and empty space;
- a virtual component merge blocked by the current threshold path.

`smoke_passed` means the expected limitation flags were observed with no missing or unexpected
flags. It does not mean the decomposition is good, collision-ready, paper-faithful, or validated.
This workbench is not benchmark evidence, not collision-quality validation, and not full CPD paper
reproduction. It is a guardrail that keeps known baseline weaknesses visible before algorithmic
improvements start hiding or changing them.

## What The Capped-Cylinder Proxy Adds

The opt-in offline `capped_cylinder` geometry proposal proxy changes the primitive-vocabulary
accounting in one named report. When the capped-cylinder proxy config requests only
`capped_cylinder`, the `paper_primitive_gap` field reports:

```text
unsupported_paper_primitive_count = 2
unsupported_paper_primitives = ["frustum", "trapezoidal_prism"]
```

That is useful because the objective report can now distinguish "not requested in this run" from
"still outside the restricted proposal vocabulary" for one paper primitive category. It remains a
surrogate report: the proxy uses an axis-span/radial fit with hemisphere caps, not a paper-faithful
primitive-fitting method.

No Newton mapping or task-level improvement is implied. `capped_cylinder` remains outside the
Newton-mapped primitive set until a separate mapping implementation and diagnostic record exist.

## Next Algorithmic Step

The next step is to choose one narrow follow-up after the capped-cylinder proxy: either another
primitive-vocabulary proxy, a primitive-fit quality fixture, or a merge-search improvement against
a known expected-failure case.

The recommended order is:

1. Pick one existing expected limitation or primitive-vocabulary gap as the target.
2. Add one focused primitive-fitting, vocabulary, or merge-search improvement against that target.
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
- "structured Eq.4 alignment metadata";
- "diagnostic accounting for future CPD reproduction work";
- "design-aligned with the paper story";
- "focused CPD-like cost-guided merge-search smoke";
- "opt-in offline capped-cylinder geometry proposal proxy";
- "not a paper-faithful objective implementation";
- "not collision-quality evidence."

Avoid:

- "paper objective reproduced";
- "CPD objective implemented";
- "Eq.4 implemented";
- "CPD optimizer implemented";
- "paper-faithful capped cylinder support";
- "Newton supports capped cylinders";
- "decomposition quality validated";
- "collision quality score";
- "benchmark metric."

## Claim Boundary

This page does not add a new supported claim. It clarifies how to interpret the
existing objective report while preserving the repository's current boundary:
CPD reproduction workbench, not full CPD paper reproduction.
