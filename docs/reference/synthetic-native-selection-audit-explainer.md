# Synthetic Native Selection Audit Explainer

This page explains the candidate audit table in the synthetic Newton-native fitting comparison.
It is a plain-language guide for reading the report, not a benchmark or a paper-faithful CPD
objective description.

## Short Version

The audit table answers one narrow question:

```text
For this toy mesh, among the primitive kinds we allowed, why did the fitter pick this one?
```

It does that by listing every candidate primitive and sorting them by the current simple surrogate
selection cost:

```text
weighted primitive volume
```

Lower cost wins. If two candidates have the same cost, the earlier primitive in the configured
primitive subset wins.

## Why We Added It

Before this audit, the synthetic native fitting comparison could say:

```text
cylindrical_rod -> cylinder
tapered_cone -> cone
ellipsoid_blob -> ellipsoid
squat_cylinder -> cylinder
```

That showed the fitter could emit the new Newton-native primitive kinds on controlled toy meshes.
But it did not make the choice easy to inspect.

The audit table adds the missing explanation layer:

```text
candidate primitive
-> fitted dimensions
-> volume proxy
-> normalized cost
-> selected or not
```

This is useful because the next algorithmic step should be based on visible failure modes, not on
guessing. If bed still selects only boxes or Franka mostly selects boxes, the synthetic audit gives
us a smaller place to debug selection logic before returning to real assets.

## What The Fields Mean

Each lane has a `candidate_audit` list.

`primitive_type`
: The primitive kind being fitted, such as `box`, `capsule`, `cylinder`, `cone`, or `ellipsoid`.

`candidate_order`
: The order in which that primitive kind appeared in the lane's primitive subset after duplicate
  kinds are removed.

`rank`
: The candidate's rank after sorting by weighted primitive volume and then by candidate order.
  Rank `1` is the candidate the simple selection rule should choose.

`selected`
: Whether this row is the primitive kind selected by the lane.

`selection_objective`
: The current selection cost name, `weighted_primitive_volume`.

`selection_objective_units`
: A reminder that this is a raw weighted-volume proxy, not a collision-quality unit.

`volume`
: The primitive's fitted proxy volume in source mesh units.

`weighted_volume`
: The volume after primitive-type weighting. In the current native fitting comparison, this is
  effectively the same as `volume` because the selection path does not use extra primitive-type
  weights.

`normalized_weighted_volume`
: The weighted volume divided by the source mesh AABB volume, with a small floor to avoid division
  by zero.

`contains_assigned_points`
: Whether the fitted proxy contains the assigned mesh vertices under the current narrow
  containment check.

`dimensions`
: The primitive-specific fitted dimensions, such as box half-extents, cylinder radius and
  half-height, cone radius and half-height, or ellipsoid radii.

The lane summary also records scope fields:

`candidate_audit_scope`
: The intended audit scope. The current value is `single_primitive_full_mesh_fixture`.

`candidate_audit_face_count`
: The number of mesh faces covered by the synthetic fixture.

`candidate_audit_matches_selection_scope`
: Whether the selected primitive covers the same full face set as the candidate audit table. This
  should be `true` for the current one-primitive synthetic fixtures.

## What The Margins Mean

The case-level comparison includes two selection margins.

`native_selection_margin_vs_legacy_best`
: Native lane best normalized cost minus legacy lane best normalized cost. A negative number means
  the native lane's selected candidate has a lower surrogate volume cost than the best candidate
  available to the legacy lane on that toy fixture.

`native_selection_margin_vs_next_native_candidate`
: Native lane best normalized cost minus the second-best native candidate's normalized cost. A
  negative number means the selected native primitive beat the next native candidate under the
  same surrogate cost.

These margins are diagnostic accounting only. They do not measure penetration, contact stability,
simulation quality, runtime speed, or paper benchmark performance.

## Scope Guard

The current audit is intended for deterministic synthetic fitting cases where the target output is
one primitive for the whole toy mesh:

```text
full synthetic fixture mesh -> one selected primitive
```

That makes the audit easy to read because the candidate table and selected primitive cover the
same face set.

Do not generalize this table to multi-primitive real USD decompositions without a separate design.
For multi-primitive decompositions, a correct audit would need one candidate table per cluster or
per merge decision, not one table for the whole mesh.

The report carries this boundary as data through `candidate_audit_scope` and
`candidate_audit_matches_selection_scope`, not only as prose.

The real-USD fitting report uses a different form: `candidate_audit_summary`. It summarizes
candidate ranks per selected cluster rather than emitting one full table for the whole mesh. That
keeps the real-USD report small while still showing whether extension primitives ever win under
the current surrogate.

## What It Means In The CPD Story

The CPD paper story is about selecting compact primitive decompositions that improve collision
detection. The audit table is far below that final goal, but it is useful infrastructure:

```text
paper goal: good primitive decomposition for collision detection
current audit: explain a toy primitive choice under a surrogate volume cost
```

So the audit is a stepping stone toward better primitive fitting and merge search. It is not the
paper optimizer.

## Safe Interpretation

Safe wording:

- "synthetic native selection audit";
- "candidate weighted-volume table";
- "toy-mesh selection explanation";
- "surrogate cost accounting";
- "not collision-quality evidence";
- "not real-USD improvement evidence."

Unsafe wording:

- "native lane is better";
- "collision quality improved";
- "validated primitive selection";
- "CPD optimizer implemented";
- "paper objective reproduced";
- "bed or Franka improved."

## Next Step

Use this audit to find the smallest primitive-fitting or merge-search change that creates a clear,
inspectable selection improvement on synthetic fixtures. Only after that should the bed/Franka
real-USD probe be rerun for native primitive value evidence.
