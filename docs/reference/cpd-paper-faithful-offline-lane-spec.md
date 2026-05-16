# CPD Paper-Faithful Offline Lane Spec

This spec defines the first offline lane needed before claiming a paper-faithful CPD
implementation. It is not an implementation record. It does not add benchmark, Newton runtime, or
real-asset evidence.

For the gap matrix, see [CPD paper reproduction gap matrix](cpd-paper-reproduction-gap-matrix.md).
For claim limits on the planned `paper_faithful_offline` status, see
[Claim Boundaries](claim-boundaries.md).

## Goal

Build an offline report path that can answer:

```text
For a tiny deterministic mesh, did the implemented subset produce reviewable paper-side audit
fields?
```

The first version should not answer:

```text
Is the collider better?
Does it work on bed or Franka?
Does Newton run faster?
Does this reproduce the paper benchmark?
```

Those questions belong to later package, runtime, and benchmark gates.

## Lane Boundary

The lane is offline by design:

```text
mesh fixture
-> paper mesh intake report
-> paper Q/operator report
-> paper primitive fitting report
-> paper collapse-cost report
-> paper priority-queue search trace
-> paper postprocessing report
-> paper offline decomposition report
```

It must not call Newton, build runtime shapes, run contact canaries, run drop/settle, run
sphere-rain, or read large real USD assets.

## Planned Artifacts

These names are lane interfaces. Only the first `cpd_paper_offline_report` slice is currently
implemented, and it is still a `partial` report rather than `paper_faithful_offline`.

| Artifact | Purpose |
| --- | --- |
| `cpd_paper_offline_report` | Current command/report name for the first partial offline paper-lane slice and the future fuller offline paper lane. |
| `paper_cpd_operator_audit` | Per-face and per-group `Q` operator fields. |
| `paper_cpd_primitive_fit_audit` | All six paper primitive candidates and containment checks in the future full lane; the first slice may audit a subset only if missing paper primitives are explicitly labeled. |
| `paper_cpd_collapse_trace` | Priority-queue merge steps, costs, stale entries, and stop reason. |
| `paper_cpd_postprocess_audit` | Enclosed-primitive culling and before/after primitive counts. |
| `paper_polygon_quad_intake_policy_audit` | Explicit triangle, quad, and polygon intake policy before stronger paper-lane wording. |
| `paper_obb_sphere_fit_faithfulness_audit` | Offline fixture-scoped paper-shaped OBB and sphere fit audit rows. |
| `paper_duplicate_vertex_preprocessing_audit` | Offline duplicate/overlapped vertex preprocessing policy and remap audit. |
| `paper_faithful_offline` | Report status allowed only after the required tests and dated records exist. |

## Canonical Paper Mechanics Checklist

The offline lane is only paper-faithful for a declared fixture scope if it preserves these
mechanics:

- face-based primitive ownership, not vertex-only primitive ownership;
- triangle, quad, and polygon normal/tangent policy, with first fixtures allowed to declare
  triangle-only scope;
- area-weighted `Q` operator with tangent-stability term recorded when used;
- primitive parameter lower clamp recorded as a paper-lane setting;
- OBB fit first, with its center used by dependent primitive fits;
- one capped-cylinder candidate per eigen axis, then minimum-cost selection;
- one capsule candidate per eigen axis, then minimum-cost selection;
- frustum initialized from the minimum-cost cylinder axis;
- isosceles trapezoidal prism evaluated over six axis orderings;
- paper base collapse cost `V(merged) - V(left) - V(right)`;
- primitive weighting recorded separately as `V_prime(p) = k(p)V(p)`;
- default paper weights recorded: cylinder `1.05`, trapezoidal prism `1.4`, box/sphere/capsule
  `1.0`, and frustum `2.1`;
- optional excess-volume threshold recorded relative to the input mesh AABB volume;
- no intersection-volume term in the paper-faithful primary cost;
- greedy priority-queue collapse only, with no lookahead inside the paper-faithful lane.

## Primitive Vocabulary

The offline lane must implement the paper primitive set as paper-side objects:

| Paper primitive | Offline requirement | Newton rule |
| --- | --- | --- |
| `oriented_bounding_box` | Eigen-axis box fit, point containment, volume, weighted volume. | May adapt to Newton `box` only after the report records axis and half extents. |
| `sphere` | OBB-center radius fit, containment, volume, weighted volume. | May adapt to Newton `sphere`. |
| `capsule` | Axis candidate fit, containment, volume, weighted volume. | May adapt to Newton `capsule` if dimensions match the runtime adapter. |
| `capped_cylinder` | Paper-style flat-capped cylinder fit and volume, not the current hemisphere-cap proxy package kind. | May adapt to Newton `cylinder` only after recorded package conversion and runtime admissibility checks. The current `capped_cylinder` proxy remains unmapped. |
| `frustum` | Top/bottom radius fit from the selected axis, containment, volume, weighted volume. | Keep offline unless an explicit Newton approximation policy exists. Newton `cone` is not general frustum support. |
| `isosceles_trapezoidal_prism` | Six axis-order attempts, containment, volume, weighted volume. The current gap-accounting label is `trapezoidal_prism`. | Keep offline unless converted to a recorded convex-hull or primitive adapter. |

Newton-native `cone` and `ellipsoid` are useful runtime diagnostics, but they are not paper
primitives. They should stay out of the paper-faithful lane unless a separate extension study is
being run.

## Report Schema

The current first slice emits these fields inside `cases[]` where appropriate. The future fuller
report should converge on these top-level or per-case fields:

```text
stage
status
claim_boundary
source_mesh
preprocessing
operator_audit
primitive_fit_audit
collapse_cost_audit
collapse_trace
component_merge_audit
postprocess_audit
metrics
failure_labels
next_required_gate
```

Required status values:

| Status | Meaning |
| --- | --- |
| `not_started` | Planned but not implemented. |
| `partial` | Some paper fields exist, but at least one required mechanic is missing. |
| `paper_aligned_surrogate` | Useful accounting exists, but the implementation is intentionally not paper-faithful. |
| `paper_faithful_offline` | All required offline mechanics, tests, and dated records exist for the declared fixture scope. |
| `blocked` | Execution stopped because an explicit requirement, dependency, or input condition failed. |

## Required Fields By Stage

### Mesh Intake

Record:

- fixture id;
- vertex count;
- face count;
- face arity policy;
- duplicate-vertex preprocessing policy;
- source-face remap;
- connected-component count.

First fixtures may be triangle-only, but the report must say so explicitly.

### Operator Audit

Record for each face or merged group:

- area;
- normal;
- tangent;
- epsilon;
- `Q` matrix;
- eigenvalues;
- eigenvectors;
- degeneracy labels.

This is the first place where the lane becomes paper-side rather than Newton-side.

### Primitive Fit Audit

For every face group, record all requested paper primitives:

- primitive type;
- axes;
- center or anchor point;
- dimensions;
- raw volume;
- weighted volume;
- cost weight;
- contains assigned points;
- fit failure reason, when applicable.

Selection must be based on the paper lane cost fields, not on Newton support.

Current `unsupported_primitives` fields in CPD-like reports are paper-vocabulary/proxy accounting
for the restricted baseline. They do not prove that a paper primitive has been implemented
faithfully.

### Collapse Cost Audit

Record the paper base collapse cost as:

```text
paper_base_cost = volume(merged) - volume(left) - volume(right)
```

Record the weighted priority companion as:

```text
weighted_priority_cost =
  weighted_volume(merged) - weighted_volume(left) - weighted_volume(right)
```

Also record:

- unweighted volume delta;
- weighted priority delta;
- primitive type selected for the merged group;
- configured primitive weights;
- optional threshold value;
- whether the threshold blocked the candidate.

Do not use AABB-normalized merge-excess as the primary paper cost. It can be recorded as a
diagnostic companion field, labeled as normalized diagnostic accounting.

Do not add primitive-intersection volume to the primary paper-faithful cost. The paper discusses
that alternative and leaves it out of the main method; adding it would be an extension, not a
paper-faithful primary lane.

### Search Trace

The search trace should make the priority queue reviewable:

- initial edge count;
- edge source: topology or component pair;
- popped candidate cost;
- stale-entry status;
- accepted or blocked decision;
- resulting source-face group;
- updated neighbor count;
- current primitive count;
- stop reason.

This trace is for greedy priority-queue collapse. Two-step lookahead or other non-greedy search
can be studied as a separate surrogate extension, but it must not be labeled paper-faithful.

The minimum valid stop reasons are:

- `target_count_reached`;
- `no_collapsible_edges`;
- `all_remaining_edges_blocked_by_threshold`;
- `blocked_by_missing_primitive_fit`;
- `blocked_by_invalid_input`.

### Component Merge Audit

Disconnected component handling must use the same paper cost and threshold fields as topology
edges. The report should separate:

- topology edges;
- component-pair edges;
- pairs skipped by threshold;
- pairs skipped by configured cap;
- final component count.

### Postprocessing Audit

Record:

- primitive count before culling;
- postprocess input source;
- enclosed primitive ids;
- enclosing primitive ids;
- containment test type;
- cull reasons;
- primitive count after culling;
- package, Newton, real-USD, and benchmark trigger boundaries.

The current `paper_nested_primitive` slice is an explicit two-OBB fixture with shared identity
axes. It records one inner primitive enclosed by one larger outer primitive. This is a deterministic
accounting canary, not a general primitive containment library and not postprocessed package
generation.

### Polygon And Quad Intake Policy

Before `paper_faithful_offline` wording, record:

- whether triangle, quad, and polygon faces are accepted directly or triangulated;
- the source-face remap policy after any triangulation;
- the normal and tangent policy for each accepted face arity;
- whether the operator audit is per original polygon face or per triangulated face;
- fixture coverage for triangle-only, quad, and higher-arity polygon cases.

This gate remains offline. It should not call Newton, generate packages, or load real USD assets.
The current lane records one quad and one five-vertex polygon fixture with fan triangulation from
the first vertex, source-face remap, generated triangle vertex triples, and source-face aggregate
operator matrices for planar, convex, non-degenerate, consistently wound toy faces.

### OBB And Sphere Fit Faithfulness Audit

Before `paper_faithful_offline` wording, record:

- whether `oriented_bounding_box` uses the paper operator eigenbasis, projected vertex bounds,
  `1e-3` parameter clamp, world-space OBB center, containment check, and volume formula;
- whether `sphere` uses the paper OBB world center and a radius equal to the max point distance
  clamped to `1e-3`;
- fixture scope for the comparison;
- failure label `paper_faithful_offline_scope_missing` after duplicate-vertex preprocessing has
  tests and a dated record.

### Duplicate Vertex Preprocessing Audit

Before `paper_faithful_offline` wording, record:

- an exact-coordinate duplicate/overlapped vertex fixture;
- first-occurrence vertex deduplication ordering;
- before/after vertex counts and duplicate clusters;
- source-face remap rows from input vertex ids to deduplicated vertex ids;
- before/after connected-component counts;
- whether any face became degenerate and was dropped;
- evidence that the executable mesh used by operator, primitive-fit, and topology rows is the
  deduplicated mesh.

The current lane records only exact coordinate overlaps with `distance_tolerance: 0.0`. It does
not record nonzero-threshold deduplication, approximate spatial hashing, or broad unclean-mesh
cleanup.

## Minimal Synthetic Fixture Set

The first paper lane should use small synthetic fixtures before any real USD:

| Fixture | Purpose | Expected audit focus |
| --- | --- | --- |
| `paper_single_box` | A simple cuboid-like mesh region. | OBB axes, point bounds, volume, containment. |
| `paper_axis_cylinder` | Points arranged around a cylindrical axis. | Cylinder/capsule axis choice, radius, height, weighted volume. |
| `paper_frustum_like` | Tapered point set. | Frustum top/bottom radius accounting. |
| `paper_trapezoid_prism_like` | Roof-like or wedge-like point set. | Six axis-ordering trapezoidal-prism fit audit. |
| `paper_two_face_merge` | Two adjacent regions with known merge cost ordering. | Collapse-cost formula and priority-queue first pop. |
| `paper_three_face_chain` | Three connected face groups with two topology edges. | Deterministic priority-queue pops, eager stale pruning, updated neighbor insertion, and target-count stop reason. |
| `paper_disconnected_components` | Two disconnected components above target primitive count, with topology unable to reduce them. | Threshold-disabled component-pair edge insertion first, then threshold behavior in a separate gate. |
| `paper_nested_primitive` | A smaller primitive fully enclosed by a larger one. | Postprocessing cull audit. |
| `paper_tiny_sphere_clamp` | One tiny triangle with radius below the primitive parameter clamp. | OBB/sphere `1e-3` parameter clamp accounting. |
| `paper_duplicate_vertex_preprocessing` | Two triangles with distinct vertex ids but exactly overlapping edge coordinates. | Exact-coordinate deduplication, source-face remap, before/after topology, and deduplicated topology trace. |
| `paper_quad_face_intake` | One quad source face fan-triangulated into two triangles. | Source-face remap and operator ownership policy. |
| `paper_polygon_face_intake` | One five-vertex source face fan-triangulated into three triangles. | Source-face remap and operator ownership policy. |

These fixtures are not benchmark assets. They are unit-test-grade checks for the paper mechanics.

## Gate Sequence

1. Source requirement gate: every implemented paper mechanic links back to the gap matrix row it
   closes.
2. Operator gate: `Q` matrices, eigenvalues, and eigenvectors are recorded for toy fixtures.
3. Primitive gate: all six paper primitive fits produce audited candidates or explicit failure
   labels.
4. Cost gate: paper base collapse cost and separate weighted priority cost are recorded and
   tested on a known small fixture.
5. Search gate: a topology priority-queue trace reaches a target count or records a valid stop
   reason.
6. Component-pair insertion gate: disconnected component-pair edges use the same cost and trace
   schema when topology edges cannot reach the target count.
7. Component-pair threshold gate: finite threshold settings record accepted, skipped, and blocked
   component-pair decisions.
8. Postprocess gate: enclosed primitive culling is tested independently.
9. Polygon/quad intake policy gate: non-triangle face policy, source-face remap, and operator
   ownership are explicit and tested.
10. OBB/sphere fit faithfulness gate: OBB and sphere rows use the paper construction for the
    declared fixture scope or explicitly record why they remain surrogates.
11. Record gate: a dated record states the fixture scope and verification commands.

Only after these gates should a separate package-adaptation slice be planned.

## Non-Goals

This lane does not:

- run Newton;
- use bed or Franka;
- run 5000-sphere benchmark tasks;
- compare against CoACD, V-HACD, or any external baseline;
- claim better collision geometry;
- claim runtime speedup;
- replace the Newton-native diagnostic lane.

## First Implementation Slice

The first implementation slice is now:

```text
paper_single_box + paper_two_face_merge
-> operator audit
-> OBB/sphere/capsule/capped-cylinder candidate audit
-> paper collapse-cost fields
-> no Newton
```

At the time of this first slice, this gave the smallest useful evidence slice that the offline lane
could compute paper-side operator, primitive-fit, and cost fields before implementing full
priority-queue search, real USD, or benchmark tasks. That first-slice record labeled the audited
primitive rows as current surrogates/proxies; later slices replace some of those rows inside the
same command report.

## Second Implementation Slice

The second implementation slice is now:

```text
paper_frustum_like + paper_trapezoid_prism_like
-> offline frustum candidate fit audit row
-> offline trapezoidal-prism candidate fit audit row
-> weight, volume, formula, axis-policy, and containment sanity checks
-> no package generation, Newton, real USD, or benchmarks
```

At that point, this slice removed the "missing paper primitive row" gap for `frustum` and
`trapezoidal_prism` inside the fixture-scoped audit report only.

## Third Implementation Slice

The third implementation slice is now:

```text
paper_single_box + paper_two_face_merge + paper_frustum_like + paper_trapezoid_prism_like
-> offline flat-capped-cylinder candidate fit audit row
-> three flat-cylinder axis candidates
-> radius, height, formula, paper weight, and containment sanity checks
-> no package generation, Newton, real USD, or benchmarks
```

This slice replaces the paper-lane `capped_cylinder` row with a flat-cap audit row. The older
CPD-like `capped_cylinder` package proxy remains a separate hemisphere-cap diagnostic outside this
paper lane.

## Fourth Implementation Slice

The fourth implementation slice is now:

```text
paper_single_box + paper_two_face_merge + paper_frustum_like + paper_trapezoid_prism_like
-> offline paper-shaped capsule candidate fit audit row
-> three capsule axis candidates from the operator basis
-> spherical-cap-adjusted height equation, radius, formula, paper weight, and containment checks
-> no package generation, Newton, real USD, or benchmarks
```

This slice replaces the paper-lane capsule row with an offline axis-policy audit row. Capsule is a
Newton-native primitive, so the row can record `newton_runtime_kind: capsule`, but the command still
does not generate a package or call Newton. The report is still not `paper_faithful_offline`
because later search, postprocess, polygon/quad intake, OBB/sphere fit-faithfulness, and
duplicate-vertex preprocessing gates are not implemented in that slice.

## Fifth Implementation Slice

The fifth implementation slice is now:

```text
paper_three_face_chain
-> topology-adjacent priority-queue candidate initialization
-> minimum weighted-priority-cost pops
-> accepted merge records, eager stale-prune records, updated neighbor insertion counts
-> target-count stop reason
-> no package generation, Newton, real USD, or benchmarks
```

This slice adds a topology-only priority-queue trace audit. The follow-on component-pair insertion
slice is recorded separately below.

## Sixth Implementation Slice

The sixth implementation slice is now:

```text
paper_disconnected_components
-> topology queue exhausts before target count
-> insert one threshold-disabled component-pair candidate
-> accept component-pair merge with the same queue event schema
-> target-count stop reason
-> no package generation, Newton, real USD, or benchmarks
```

This slice adds component-pair insertion only under disabled threshold settings. It does not
implement enabled threshold blocking or skipped component-pair accounting.

## Seventh Implementation Slice

The seventh implementation slice is now:

```text
paper_component_pair_threshold_blocked
-> topology queue exhausts before target count
-> insert one component-pair candidate
-> block it with finite paper-base-cost threshold 0.0
-> record blocked event, attempted count 1, skipped count 0, and threshold stop reason
-> no package generation, Newton, real USD, or benchmarks
```

This slice adds a deterministic blocked component-pair event for one all-pairs toy fixture. It does
not implement capped skipped-pair fixtures; skipped count is recorded as `0`.

## Eighth Implementation Slice

The eighth implementation slice is now:

```text
paper_nested_primitive
-> explicit two-OBB postprocess input rows
-> shared identity-axis corner containment check
-> before/after primitive counts, enclosed/enclosing ids, and cull reason
-> no package generation, Newton, real USD, or benchmarks
```

This slice adds one deterministic enclosed-primitive culling audit. The input primitives are
explicit audit rows rather than output from the full paper search, so the report remains
`partial`.

## Ninth Implementation Slice

The ninth implementation slice is now:

```text
paper_quad_face_intake + paper_polygon_face_intake
-> fan triangulation from the first source vertex
-> source-face remap with original vertex ids and generated triangle vertex triples
-> source-face aggregate operator matrices as sums of generated triangle q_matrix rows
-> no package generation, Newton, real USD, or benchmarks
```

This slice records a conservative source-face intake policy for planar, convex, non-degenerate,
consistently wound toy faces. It keeps executable geometry as `TriangleMesh` and does not claim a
general polygon mesh implementation.

## Tenth Implementation Slice

The tenth implementation slice is now:

```text
paper_obb_sphere_fit_faithfulness_audit
-> offline paper-shaped OBB rows with projected vertex bounds, world-space center, 1e-3 clamp,
   and volume formula
-> offline paper-shaped sphere rows using the OBB world center and clamped max-distance radius
-> tiny clamp fixture exercising sphere radius clamping below 1e-3
-> uniqueness checks so OBB/sphere rows replace current surrogate rows rather than duplicate them
-> no package generation, Newton, real USD, or benchmarks
```

This slice records the OBB/sphere paper construction for named toy fixtures only. It does not make
the report `paper_faithful_offline` because duplicate-vertex preprocessing and broader offline lane
coverage remain unresolved.

## Eleventh Implementation Slice

The eleventh implementation slice is now:

```text
paper_duplicate_vertex_preprocessing_audit
-> exact-coordinate duplicate/overlapped vertex preprocessing audit
-> first-occurrence vertex remap, duplicate clusters, retained/dropped face ids, and source-face
   remap rows
-> before/after connected-component counts
-> topology trace over the deduplicated executable mesh
-> status remains partial and paper_faithful_offline_supported remains false
-> no package generation, Newton, real USD, or benchmarks
```

This closes only the named exact-overlap fixture audit. It should not be broadened into package
generation, Newton diagnostics, benchmark work, broad mesh cleanup, or a bed/Franka rerun.

## Next Implementation Slice

The next paper-lane gate is:

```text
paper_faithful_offline_scope_audit
-> check every gap-matrix row and every offline-lane criterion
-> decide which fixture-scoped mechanics are still partial
-> decide whether any bounded `paper_faithful_offline` wording is allowed
-> keep package generation, Newton, real USD, and benchmarks blocked unless a later slice creates
   an explicit package boundary with dated mapping and diagnostic records
```
