# CPD Paper-Faithful Offline Lane Spec

This spec defines the first offline lane needed before claiming a paper-faithful CPD
implementation. It is not an implementation record. It does not add benchmark, Newton runtime, or
real-asset evidence.

For the gap matrix, see [CPD paper reproduction gap matrix](cpd-paper-reproduction-gap-matrix.md).
For the current fixture-breadth plan, see
[CPD paper fixture-breadth expansion plan](cpd-paper-fixture-breadth-expansion-plan.md).
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

These names are lane interfaces. `cpd_paper_offline_report` is currently implemented as a
multi-slice `partial` report rather than `paper_faithful_offline`.

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
| `paper_faithful_offline_scope_audit` | Offline criteria table that compares fixture-scoped evidence against the gap matrix, keeps the lane partial, and now points follow-on work to planning-only offline generalization. |
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
- the current top-level failure label after the native-fixture PrimitiveSpec-like dict generation,
  serialization, runtime-boundary preflight, runtime-construction, collision-package generation
  preflight, collision-package generation, runtime-admissibility preflight, and offline/static
  runtime-admissibility contracts, plus the Newton shape-mapping preflight and descriptor
  contracts, plus the Newton shape runtime-boundary preflight, runtime-construction, and
  builder-preflight, builder-construction, engine-builder boundary-preflight, and
  engine-builder environment-probe, API-surface, entry, smoke, runtime-execution,
  runtime-lane review, configured-runtime design, configured-runtime preflight,
  configured-runtime validation, configured-runtime source-resolution, configured-runtime
  device-resolution, configured-runtime entry-decision, configured-runtime smoke, and
  configured-runtime execution contracts:
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review_contract_missing`.

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
12. Scope-audit gate: a top-level criteria table records which paper-lane mechanics are still
    fixture-scoped, which boundaries are out of offline scope, and why the report remains
    `partial`.

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

## Twelfth Implementation Slice

The twelfth implementation slice is now:

```text
paper_faithful_offline_scope_audit
-> check every gap-matrix row and every offline-lane criterion
-> decide which fixture-scoped mechanics are still partial
-> reject stronger `paper_faithful_offline` wording for this fixture scope
-> record non-blocking package/Newton/real-USD/benchmark boundary rows
-> advance the next gate to `paper_fixture_breadth_expansion_plan`
-> keep package generation, Newton, real USD, and benchmarks blocked unless a later slice creates
   an explicit package boundary with dated mapping and diagnostic records
```

This slice is a decision table, not a new decomposition algorithm. It records
`decision: remain_partial`, `paper_faithful_offline_allowed: false`, and the nine blocking
fixture-scope criteria that need a fixture-breadth plan before any stronger offline wording.

## Current Fixture-Breadth Position

The paper-lane gate immediately after the fixture-breadth completion review was closed by a
command-only generalization planning table. Later source-policy, primitive-fit engine,
search-engine, postprocess-policy, package-boundary readiness, changed-decomposition output,
package-adapter, unsupported-primitive policy, mapped-subset plan, candidate-matrix,
adapter-preflight, PrimitiveSpec dry-run, validation, generation-preflight, generation,
candidate-source, native-current fixture, native-fixture serialization/runtime-boundary,
runtime-construction, package-generation preflight, and package-generation contract gates are also
now closed:

```text
paper_faithful_offline_generalization_plan
-> planning-only gate for broadening the offline algorithm beyond named toy fixtures
-> keep report status partial
-> keep paper_faithful_offline_supported false
-> keep runtime admissibility, Newton, real USD, and benchmarks out of scope
-> current next gate after the later closed gates: paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review_contract
```

Batch A broadens mesh policy, source-face accounting, and operator evidence. Batch B broadens
primitive-fit evidence for OBB, sphere, capsule, capped cylinder, frustum, and trapezoidal prism
without adding Newton runtime support. Batch C broadens weighted-priority ordering, queue
tie/eager-stale-prune behavior, and positive nonzero threshold blocking without adding Newton
runtime support. Batch D broadens disconnected component-pair ordering and capped skipped-pair
accounting without adding Newton runtime support. Batch E broadens rotated nested OBB postprocess
accounting and cross-type unsupported no-cull accounting without adding Newton runtime support. The
completion review closes only the planned Batch A-E breadth gate. The source-policy
generalization slice is now implemented as an offline report-only matrix, not as
`paper_faithful_offline` support, package generation, Newton runtime execution, real USD, or
benchmarking.

`paper_generalization_batch_a_source_policy` closes only the source-policy gate. It records
bounded source mesh, exact-coordinate preprocessing, source-face intake/remap, concave rejection,
and source-face `Q` aggregation accounting for deterministic synthetic meshes. It is not robust
mesh cleanup, general polygon intake, package generation, Newton runtime execution, real-USD
evidence, benchmark evidence, `paper_faithful_offline` support, full CPD reproduction,
collision-quality evidence, deployment readiness, or safety certification. This gate led to the
now-implemented primitive-fit engine generalization matrix.

`paper_generalization_batch_b_primitive_fit_engine` closes only the primitive-fit engine
generalization gate. It records an offline matrix over deterministic in-memory probes for all six
paper primitive names, including candidate generation, selected-candidate accounting, containment
checks, finite numeric fields, and offline-only boundaries for paper-only primitives. It is not
robust primitive fitting, package generation, Newton runtime execution, real-USD evidence,
benchmark evidence, `paper_faithful_offline` support, full CPD reproduction, collision-quality
evidence, deployment readiness, or safety certification. It led to the now-implemented
search-engine generalization matrix.

`paper_generalization_batch_c_search_engine` closes only the search-engine generalization gate. It
records an offline matrix over existing deterministic topology queue, weighted-priority,
equal-cost tie, threshold-stop, and component-pair traces. It is not a generalized optimizer,
package generation, Newton runtime execution, real-USD evidence, benchmark evidence,
`paper_faithful_offline` support, full CPD reproduction, collision-quality evidence, deployment
readiness, or safety certification. At that historical Batch C stage the follow-up gate was
`paper_generalization_batch_d_postprocess_policy`.

`paper_generalization_batch_d_postprocess_policy` closes only the postprocess-policy
generalization gate. It records an offline matrix over existing deterministic postprocess audit
fixtures: identity-axis OBB culling, rotated OBB culling, conservative unsupported cross-type
no-cull accounting, before/after primitive counts, cull or unsupported reasons, and false package,
Newton, real-USD, and benchmark triggers. It is not a general primitive containment library,
package generation, Newton runtime execution, real-USD evidence, benchmark evidence,
`paper_faithful_offline` support, full CPD reproduction, collision-quality evidence, deployment
readiness, or safety certification. At that Batch D stage the follow-up gate was
`paper_generalization_batch_e_package_boundary_readiness`.

`paper_generalization_batch_e_package_boundary_readiness` closes only the package-boundary
readiness gate. It records an offline package-boundary readiness matrix before package conversion:
the current source-policy, primitive-fit, search-engine, and postprocess-policy outputs are audit
matrices rather than a durable changed-decomposition output contract; package generation and
Newton runtime execution remain blocked; real-USD and benchmark gates remain later work. It is not
package readiness, Newton readiness, package generation, Newton runtime execution, real-USD
evidence, benchmark evidence, `paper_faithful_offline` support, full CPD reproduction,
collision-quality evidence, deployment readiness, or safety certification. At the historical Batch
E stage the follow-up gate was `paper_offline_changed_decomposition_output_contract`.

`paper_offline_changed_decomposition_output_contract` closes only the offline output-contract
gate. It records an offline changed-decomposition output contract, not a `CollisionPackage`, over
synthetic toy fixture evidence. The payload carries decomposition output rows, stable offline
primitive ids, source-face/group ids, selected paper primitive audit fields, explicit postprocess
state rows, unsupported runtime boundaries, and package/Newton/real-USD/benchmark false triggers.
It is not package readiness, Newton readiness, package generation, Newton runtime execution,
real-USD evidence, benchmark evidence, `paper_faithful_offline` support, full CPD reproduction,
collision-quality evidence, deployment readiness, or safety certification. At that stage the
follow-up gate was `paper_package_adapter_contract`.

`paper_package_adapter_contract` closes only the offline adapter-contract gate. It records a
command-only package-adapter contract, not a `CollisionPackage`, over the changed-decomposition
primitive records. The payload carries an input-contract summary, an adapter decision contract, and
16 primitive adapter decision rows. All current `trapezoidal_prism` /
`offline_only_unmapped` rows are classified as `later_policy_required`, so no package generation,
Newton mapping, runtime admissibility, real-USD, or benchmark work is unlocked. It is not package
readiness, Newton readiness, package generation, Newton runtime execution, real-USD evidence,
benchmark evidence, `paper_faithful_offline` support, full CPD reproduction, collision-quality
evidence, deployment readiness, or safety certification. At that stage the follow-up gate was
`paper_package_adapter_unsupported_primitive_policy`.

`paper_package_adapter_unsupported_primitive_policy` closes only the offline unsupported-primitive
policy gate. It records a command-only policy table, not a `CollisionPackage`, over the adapter
decision rows. The payload classifies all six paper primitive families, keeps all current
`trapezoidal_prism` / `offline_only_unmapped` rows offline with
`block_package_conversion`, and records zero package-candidate rows. It is not package readiness,
Newton readiness, runtime admissibility, approximation support, package generation, Newton
runtime execution, real-USD evidence, benchmark evidence, `paper_faithful_offline` support, full
CPD reproduction, collision-quality evidence, deployment readiness, or safety certification. The
follow-up gate at that stage was `paper_package_conversion_mapped_subset_plan`.

`paper_package_conversion_mapped_subset_plan` closes only the offline mapped-subset planning gate.
It records a command-only package-conversion planning table, not a `CollisionPackage`, over the
unsupported-primitive policy rows. The payload identifies `oriented_bounding_box`, `sphere`, and
`capsule` as native-family review rows, keeps all current `trapezoidal_prism` /
`offline_only_unmapped` rows offline, records zero current package-conversion candidates, and
keeps package generation, Newton runtime execution, real-USD, and benchmark triggers false. It is
not package readiness, Newton readiness, runtime admissibility, approximation support, package
generation, Newton runtime execution, real-USD evidence, benchmark evidence,
`paper_faithful_offline` support, full CPD reproduction, collision-quality evidence, deployment
readiness, or safety certification. The follow-up gate at that stage was
`paper_mapped_subset_conversion_candidate_matrix`.

`paper_mapped_subset_conversion_candidate_matrix` closes only the offline candidate-matrix gate. It
records a command-only review matrix, not a `CollisionPackage`, over the mapped-subset plan rows.
The payload records three future-family review rows, keeps all current `trapezoidal_prism` /
`offline_only_unmapped` rows blocked and offline, records zero current package-conversion
candidates, and keeps PrimitiveSpec generation, CollisionPackage generation, runtime
admissibility, Newton runtime execution, real-USD, and benchmark triggers false. It is not package
readiness, Newton readiness, runtime admissibility, approximation support, package generation,
Newton runtime execution, real-USD evidence, benchmark evidence, `paper_faithful_offline` support,
full CPD reproduction, collision-quality evidence, deployment readiness, or safety certification.
At that stage the follow-up gate was `paper_mapped_subset_adapter_preflight_contract`.

`paper_mapped_subset_adapter_preflight_contract` closes only the offline adapter-preflight gate. It
records a command-only contract, not `PrimitiveSpec` generation and not a `CollisionPackage`, over
the candidate-matrix rows. The payload records future adapter requirements, records no-op behavior
for the current zero package-conversion-candidate state, keeps all current
`trapezoidal_prism` / `offline_only_unmapped` rows offline, keeps package generation disabled, and
keeps PrimitiveSpec generation, CollisionPackage generation, runtime admissibility, Newton runtime
execution, real-USD, and benchmark triggers false. It is not package readiness, Newton readiness,
runtime admissibility, approximation support, `PrimitiveSpec` readiness, package generation,
Newton runtime execution, real-USD evidence, benchmark evidence, `paper_faithful_offline` support,
full CPD reproduction, collision-quality evidence, deployment readiness, or safety certification.
At that stage the follow-up gate was `paper_mapped_subset_primitivespec_dry_run_contract`.

`paper_mapped_subset_primitivespec_dry_run_contract` closes only the offline PrimitiveSpec dry-run
gate. It records a command-only contract, not real `PrimitiveSpec` generation and not a
`CollisionPackage`, over the adapter-preflight rows. The payload records future PrimitiveSpec shape
requirements for OBB/box, sphere, and capsule, keeps capped cylinder and frustum blocked behind an
approximation policy, keeps all current `trapezoidal_prism` / `offline_only_unmapped` rows
offline/no-op, records zero current PrimitiveSpec candidates, records zero generated PrimitiveSpec
rows, and keeps CollisionPackage generation, runtime admissibility, Newton runtime execution,
real-USD, and benchmark triggers false. It is not package readiness, Newton readiness, runtime
admissibility, approximation support, `PrimitiveSpec` readiness, package generation, Newton
runtime execution, real-USD evidence, benchmark evidence, `paper_faithful_offline` support, full
CPD reproduction, collision-quality evidence, deployment readiness, or safety certification. The
validation, generation-preflight, generation, candidate-source, and native-current fixture
contracts are now implemented. The native-fixture PrimitiveSpec-like dict generation and
serialization contracts are also implemented. The runtime-boundary preflight contract is also
implemented as an offline boundary check. The runtime-construction contract is now implemented as
a single-fixture offline contract that constructs exactly one runtime `PrimitiveSpec` from the
canonical `paper_single_box` OBB/box preflight JSON after checking the preflight row's canonical
JSON SHA-256 fingerprint, and stores only `PrimitiveSpec.to_dict()` in the report. The
collision-package generation preflight contract is now implemented as a single-fixture offline
preflight that records one later package-generation candidate from that dict while still creating
zero CollisionPackages and zero runtime-admissibility checks. The current next gate is
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review_contract`
after the later single-fixture collision-package generation contract constructs one synthetic,
report-scoped `CollisionPackage.to_dict()` artifact, the runtime-admissibility preflight contract
records one later runtime-admissibility candidate row for the same `paper_single_box` OBB/box row,
the offline/static runtime-admissibility contract records one finite-geometry and box-schema
check, the Newton shape-mapping preflight records one static mapper-handoff row, and the Newton
shape-mapping contract records one static report-scoped descriptor dict. The Newton shape
runtime-boundary preflight contract then records one later runtime-construction candidate for that
descriptor. The Newton shape runtime-construction contract then records exactly one repo-local
`NewtonShapeMapping.to_dict()` mapping record for that descriptor while keeping Newton engine
shape objects, builder shape calls, and Newton execution at zero. The Newton shape runtime
builder-preflight contract then records one JSON-safe future box builder call plan while keeping
Newton engine shape objects, builder shape calls, and Newton execution at zero. The Newton shape
runtime builder-construction contract then records one JSON-safe repo-local recording-builder
`add_shape_box` call artifact through the repo-local static shape dispatch helper and fake
Warp-like module while keeping real Newton imports, Newton `ModelBuilder` instantiation, Newton
engine shape objects, real Newton builder shape calls, and Newton execution at zero. Those checks
are still report-only; they are not real Newton shape object construction, real builder
invocation, or Newton execution. The later runtime-execution and runtime-lane review gates keep
that same boundary and do not validate runtime compatibility.

`paper_mapped_subset_primitivespec_validation_contract` closes only the offline PrimitiveSpec
validation gate. It validates the dry-run contract field list, mapped future shape labels, six
family rows, 16 current no-op rows, source traceability, zero current candidates, zero generated
PrimitiveSpecs, and false runtime/evaluation triggers. It is not real `PrimitiveSpec` generation,
not a `CollisionPackage`, not package readiness, not Newton readiness, not runtime admissibility,
and not collision-quality evidence. The generation-preflight contract now closes only the offline
PrimitiveSpec generation-preflight gate, records zero current generation candidates, zero generated
PrimitiveSpecs, zero generated CollisionPackages, and zero runtime-admissibility checks, and keeps
the lane partial. The generation contract now closes only the offline PrimitiveSpec generation
contract, emits native-family template rows for box/sphere/capsule, records zero runtime
PrimitiveSpecs, zero CollisionPackages, and zero runtime-admissibility checks, and keeps current
unmapped rows offline/no-op. The candidate-source contract now closes only the offline
PrimitiveSpec source-audit gate, keeps template rows future-only, records two blocked
approximation-policy rows, one no-op trapezoidal-prism family row, 16 traceable but ineligible
current unmapped trapezoidal-prism rows, zero eligible current PrimitiveSpec candidate sources,
zero generated PrimitiveSpecs, zero CollisionPackages, and zero runtime-admissibility checks. The
native-current fixture contract now closes only the offline source-row gate, records exactly one
synthetic `paper_single_box` selected OBB/box source row, one eligible current candidate source,
one report-only PrimitiveSpec generation candidate, zero generated PrimitiveSpecs, zero
CollisionPackages, and zero runtime-admissibility checks. The native-fixture PrimitiveSpec-like
dict generation contract now closes only the offline dict-generation gate, emits one
JSON-serializable report-only dict for that source row, keeps runtime PrimitiveSpec objects,
CollisionPackages, runtime-admissibility, Newton, real-USD, benchmark, collision-quality,
deployment, and certification triggers at zero or false, and led to the later serialization gate.
The native-fixture serialization contract now closes only the offline JSON serialization/schema
stability gate, validates strict canonical JSON and round-trip equality for that same report-only
dict, keeps runtime PrimitiveSpec objects, CollisionPackages, runtime-admissibility, Newton,
real-USD, benchmark, collision-quality, deployment, and certification triggers at zero or false,
and at that stage advanced the next gate to
`paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`. The runtime-boundary
preflight contract now closes only the offline boundary-preflight gate, records one later runtime
`PrimitiveSpec` construction candidate for that same row, keeps runtime construction disallowed in
the current gate, keeps runtime PrimitiveSpec objects, CollisionPackages, runtime-admissibility,
Newton, real-USD, benchmark, collision-quality, deployment, and certification triggers at zero or
false, records a canonical JSON SHA-256 fingerprint for the later construction gate, and at that
stage advanced the next gate to
`paper_mapped_subset_primitivespec_runtime_construction_contract`. The runtime-construction
contract now closes only the single-fixture offline runtime-construction gate, constructs one
runtime `PrimitiveSpec` object from the canonical preflight JSON after verifying that fingerprint,
stores only the resulting `PrimitiveSpec.to_dict()` payload, records runtime PrimitiveSpec
generation counts as one, keeps CollisionPackages, runtime-admissibility, Newton, real-USD,
benchmark, collision-quality, deployment, and certification triggers at zero or false, and
at that stage advanced the next gate to
`paper_mapped_subset_collision_package_generation_preflight_contract`. The collision-package
generation preflight contract now closes only the single-fixture offline preflight gate, records
one later package-generation candidate from that `PrimitiveSpec.to_dict()` payload, keeps package
generation disallowed in the current gate, keeps generated CollisionPackages and
runtime-admissibility checks at zero, and advances the next gate at that stage to
`paper_mapped_subset_collision_package_generation_contract`. The collision-package generation
contract now closes only the single-fixture offline generation gate, constructs exactly one
synthetic, report-scoped `CollisionPackage.to_dict()` artifact for the same `paper_single_box`
OBB/box row, records `generated_collision_package_count: 1`, keeps runtime-admissibility checks,
Newton, real-USD, benchmark, collision-quality, deployment, and certification triggers at zero or
false, and advances the next gate at that stage to
`paper_mapped_subset_runtime_admissibility_preflight_contract`.
The runtime-admissibility preflight contract now closes only the single-fixture offline preflight
gate, consumes that one synthetic package artifact, records one later runtime-admissibility
candidate row without copying the full package dict, keeps runtime-admissibility checks, Newton,
real-USD, benchmark, collision-quality, deployment, and certification triggers at zero or false,
and advances the next gate at that stage to `paper_mapped_subset_runtime_admissibility_contract`. It is
not package readiness, not executable runtime-admissibility, not Newton readiness, not Newton
support or execution, not real-USD evidence, not benchmark or collision-quality evidence, not
paper primitive vocabulary coverage, not approximation support, not full CPD reproduction, not
`paper_faithful_offline`, and not deployment, safety, or certification evidence.
The runtime-admissibility contract now closes only the single-fixture offline/static
admissibility gate, consumes that preflight row, records one finite center, right-handed
orthonormal-axis, positive-half-extent, target box-schema, source-face, containment, and volume
check for the same synthetic package, and at that stage advances the next gate to
`paper_mapped_subset_newton_shape_mapping_preflight_contract`. It records
`runtime_admissibility_check_count: 1` only as report-side static accounting. It is not package
readiness, not Newton readiness, not Newton shape mapping, not Newton execution, not real-USD
evidence, not benchmark or collision-quality evidence, not paper primitive vocabulary coverage,
not approximation support, not full CPD reproduction, not `paper_faithful_offline`, and not
deployment, safety, or certification evidence.
The Newton shape-mapping preflight contract now closes only the single-fixture offline/static
preflight gate, consumes that runtime-admissibility row, records one mapper-handoff row for target
kind `box`, center, axes, dimensions, and half-extents fields, and advances the next gate at that stage
to `paper_mapped_subset_newton_shape_mapping_contract`. It records `mapping_attempt_count: 0`,
`newton_mapping_record_count: 0`, and `newton_runtime_execution_count: 0`. It is not Newton
readiness, not Newton support, not Newton execution, not real-USD evidence, not benchmark or
collision-quality evidence, not paper primitive vocabulary coverage, not approximation support,
not full CPD reproduction, not `paper_faithful_offline`, and not deployment, safety, or
certification evidence.
The Newton shape-mapping contract now closes only the single-fixture offline/static descriptor
gate, consumes that preflight row, records one report-scoped `newton_shape_descriptor_dict` for
target kind `box`, and advances the next gate at that stage to
`paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`. It records
`mapping_attempt_count: 0`, `newton_mapping_record_count: 0`, `newton_shape_object_count: 0`, and
`newton_runtime_execution_count: 0`. It is not Newton readiness, not Newton support, not real
Newton shape mapping, not Newton shape object creation, not Newton execution, not real-USD
evidence, not benchmark or collision-quality evidence, not paper primitive vocabulary coverage,
not approximation support, not full CPD reproduction, not `paper_faithful_offline`, and not
deployment, safety, or certification evidence.
The Newton shape runtime-boundary preflight contract now closes only the single-fixture
offline/static runtime-boundary preflight gate, consumes that descriptor row, records one later
Newton shape runtime-construction candidate for target kind `box`, and at that stage advanced the
next gate to `paper_mapped_subset_newton_shape_runtime_construction_contract`. It records
`mapping_attempt_count: 0`, `newton_mapping_record_count: 0`, `newton_shape_object_count: 0`, and
`newton_runtime_execution_count: 0`. It is not Newton readiness, not Newton support, not real
Newton shape mapping, not Newton shape object creation, not Newton execution, not real-USD
evidence, not benchmark or collision-quality evidence, not paper primitive vocabulary coverage,
not approximation support, not full CPD reproduction, not `paper_faithful_offline`, and not
deployment, safety, or certification evidence.
The Newton shape runtime-construction contract now closes only the single-fixture
offline/report-scoped construction gate, consumes that runtime-boundary candidate row, records
exactly one repo-local `NewtonShapeMapping.to_dict()` mapping record for target kind `box`, and at
that stage advanced the next gate to
`paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`. It records
`constructed_newton_shape_mapping_record_count: 1`, `newton_mapping_record_count: 1`,
`newton_mapper_call_count: 0`, `newton_engine_shape_object_count: 0`,
`newton_builder_shape_call_count: 0`, and `newton_runtime_execution_count: 0`. It is not Newton
readiness, not Newton support, not real Newton shape object creation, not Newton execution, not
real-USD evidence, not benchmark or collision-quality evidence, not paper primitive vocabulary
coverage, not approximation support, not full CPD reproduction, not `paper_faithful_offline`, and
not deployment, safety, or certification evidence.
The Newton shape runtime builder-preflight contract now closes only the single-fixture
offline/static builder-preflight gate, consumes that mapping record, records exactly one JSON-safe
future box builder call plan, and at that stage advanced the next gate to
`paper_mapped_subset_newton_shape_runtime_builder_construction_contract`. It records
`builder_call_plan_count: 1`, `builder_call_allowed_count: 0`,
`newton_engine_shape_object_count: 0`, `newton_builder_shape_call_count: 0`, and
`newton_runtime_execution_count: 0`. It is not Newton readiness, not Newton support, not real
Newton shape object creation, not Newton execution, not real-USD evidence, not benchmark or
collision-quality evidence, not paper primitive vocabulary coverage, not approximation support,
not full CPD reproduction, not `paper_faithful_offline`, and not deployment, safety, or
certification evidence.
The Newton shape runtime builder-construction contract now closes only the single-fixture
offline/report-only builder-construction gate, consumes that builder-preflight row, records
exactly one JSON-safe repo-local recording-builder `add_shape_box` call artifact, and advances the
next gate at that stage to
`paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract`. It records
`recording_builder_shape_call_count: 1`, `recorded_builder_call_count: 1`,
`repo_local_static_shape_helper_call_count: 1`, `real_newton_import_count: 0`,
`newton_model_builder_instantiated_count: 0`, `newton_engine_shape_object_count: 0`,
`newton_builder_shape_call_count: 0`, and `newton_runtime_execution_count: 0`. It is not Newton
readiness, not Newton support, not real Newton shape object creation, not Newton execution, not
real-USD evidence, not benchmark or collision-quality evidence, not paper primitive vocabulary
coverage, not approximation support, not full CPD reproduction, not `paper_faithful_offline`, and
not deployment, safety, or certification evidence.
The Newton engine-builder boundary-preflight contract now closes only the single-fixture
offline/static boundary-preflight gate, consumes that recording-builder artifact, records one
future-boundary checklist row for the later real `newton.ModelBuilder` / `add_shape_box`
environment boundary, and at that stage advanced the stage-local next gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract`. It keeps
real Newton imports, `newton.ModelBuilder` instantiation, real builder shape calls, model
finalization, collision pipeline calls, and Newton execution at zero. It is not Newton readiness,
not Newton support, not real Newton execution, not real-USD evidence, not benchmark or
collision-quality evidence, not full CPD reproduction, not `paper_faithful_offline`, and not
deployment, safety, or certification evidence.
The Newton engine-builder environment-probe contract now closes only the single-fixture bounded
environment-provenance gate, consumes the boundary-preflight row, records configured-source-dir
status and JSON-safe Newton/Warp `find_spec` provenance shape, and at that stage advanced the next gate
to `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract`. The default
report remains no-config and imports no real Newton or Warp runtime. It keeps
`newton.ModelBuilder` instantiation, real builder shape calls, model finalization, collision
pipeline calls, Newton execution, real USD, benchmarks, and collision-quality measurements at zero.
It is not Newton readiness, not Newton support, not real Newton execution, not real-USD evidence,
not benchmark or collision-quality evidence, not full CPD reproduction, not
`paper_faithful_offline`, and not deployment, safety, or certification evidence.
The Newton engine-builder API-surface contract now closes only the single-fixture bounded
source-AST API-surface gate, consumes the environment-probe row, records default no-config
API-surface status for the future `newton.ModelBuilder` / `add_shape_box` boundary, and at that
stage advanced the stage-local next gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract`. When
a Newton source directory is explicitly passed, this lane may read source files and parse AST only.
It keeps real Newton/Warp imports, `newton.ModelBuilder` instantiation, real builder shape calls,
model finalization, collision pipeline calls, Newton execution, real USD, benchmarks, and
collision-quality measurements at zero. It is not Newton readiness, not runtime compatibility, not
Newton support, not real Newton execution, not real-USD evidence, not benchmark or
collision-quality evidence, not full CPD reproduction, not `paper_faithful_offline`, and not
deployment, safety, or certification evidence.

The Newton engine-builder entry contract now closes only the single-fixture report-only entry
decision gate. It consumes the API-surface row, records the default no-config
`defer_real_runtime_entry` decision, keeps real Newton/Warp imports, `newton.ModelBuilder`
instantiation, real builder shape calls, model finalization, collision pipeline calls, Newton
execution, real USD, benchmarks, and collision-quality measurements at zero. The Newton
engine-builder smoke contract now closes only a report-only skipped-smoke decision for the same
lineage, records `smoke_decision: skip_real_runtime_smoke`, keeps runtime-smoke attempts and
Newton execution at zero. The Newton engine-builder runtime-execution contract now closes only a
report-only skipped-runtime-execution decision for the same lineage, records
`runtime_execution_decision: skip_real_runtime_execution`, keeps runtime-execution attempts and
Newton execution at zero. The Newton engine-builder runtime-lane review contract now closes only a
report-only claim-boundary review for the same skipped-runtime-execution row, records
`runtime_lane_review_decision: keep_real_runtime_execution_blocked`, keeps runtime compatibility
unvalidated, and advances the stage-local next gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract`. The
Newton engine-builder configured-runtime design contract now closes only a report-only runtime
input design record, keeps runtime config validation false, keeps all real runtime counters zero,
and advances the stage-local next gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract`.
The configured-runtime preflight contract now closes only a report-only preflight record, keeps
runtime config validation, runtime source/device resolution, and all real runtime counters false
or zero, and at that stage advanced the next gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_validation_contract`.
The configured-runtime validation contract now closes only a report-only missing-config validation
record, reads no config file or environment, keeps runtime source/device resolution and all real
runtime counters false or zero, and at that stage advanced the next gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract`.
The configured-runtime source-resolution contract now closes only a report-only missing-source
resolution record, performs no filesystem probe, keeps runtime source/device resolution and all
real runtime counters false or zero, and at that stage advanced the next gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract`.
The configured-runtime device-resolution contract now closes only a report-only missing-device
resolution record, creates no runtime device object, keeps runtime source/device resolution and all
real runtime counters false or zero, and at that stage advanced the next gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract`.

The configured-runtime entry-decision contract now closes only a report-only no-runtime-entry
decision record, keeps runtime entry allowed/attempted/passed false, keeps all real runtime
counters false or zero, and at that stage advanced the next gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract`.

The configured-runtime smoke contract now closes only a report-only skipped-smoke decision record,
keeps runtime smoke allowed/attempted/passed false, keeps all real runtime counters false or zero,
and at that stage advanced the next gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract`.
The configured-runtime execution contract now closes only a report-only skipped-execution decision
record, keeps configured-runtime execution allowed/attempted/passed false, keeps all real runtime
counters false or zero, and advances the current next gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review_contract`.

The entry contract is intentionally broader than the previously planned pair of small import
gates. It reviews import-boundary preconditions and the first Newton entry decision together,
because those facts depend on the same package lineage, source/environment evidence, and
API-surface row. Splitting them further would increase maintenance cost without adding a clear
new audit surface.
