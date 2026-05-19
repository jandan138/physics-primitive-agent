# CPD Paper Fixture Breadth Expansion Plan

This page turns the completed `paper_faithful_offline_scope_audit` blockers into planned
synthetic fixture coverage. It is a planning document, not experiment evidence, not a new
implementation, and not a claim that `paper_faithful_offline` is supported.

For the current scope-audit result, see
[CPD paper faithful offline scope audit](../records/2026-05-16-cpd-paper-faithful-offline-scope-audit.md).
For the row-by-row paper gap map, see
[CPD paper reproduction gap matrix](cpd-paper-reproduction-gap-matrix.md).

## Scope

The plan answers:

- which blocking paper-lane criteria need more synthetic fixture breadth;
- which future fixture ids should be added first;
- what each fixture must record when implemented;
- which claims remain blocked.

The plan does not:

- add new fixtures to `cpd_paper_offline_report`;
- generate a `CollisionPackage`;
- run Newton;
- load bed, Franka, or other real USD assets;
- run benchmarks;
- support collision-quality, deployment, or safety-certification claims.

## Source Blockers

The scope audit keeps these nine criteria blocking before stronger offline wording:

| Blocking criterion | Current blocker meaning |
| --- | --- |
| `source_mesh_and_preprocessing_policy` | Current preprocessing evidence is one exact-overlap toy fixture, not broad mesh cleanup. |
| `source_face_intake_policy` | Current non-triangle source-face evidence is one quad and one convex five-vertex polygon. |
| `operator_q_audit` | Operator evidence exists for named fixtures, but not enough degeneracy or source-policy breadth. |
| `primitive_vocabulary_and_fit` | All six paper primitive names have audit rows, but fitting breadth is limited. |
| `paper_collapse_cost_and_weighting` | Cost evidence is still toy-scoped after Batch E, even though weighted ordering, positive finite threshold, and component-pair candidate accounting now exist. |
| `greedy_priority_queue_trace` | Queue traces remain toy-scoped after Batch E and completion review; they still need generalization beyond named synthetic fixtures before stronger wording. |
| `target_count_and_threshold_stop` | Target and threshold stops remain toy-scoped after Batch E, including one positive finite component-pair threshold fixture and one capped skipped-pair fixture. |
| `component_pair_edge_handling` | Component-pair evidence now includes accepted, blocked, multi-candidate, and capped skipped-pair toy cases only. |
| `enclosed_primitive_postprocess` | Postprocess evidence now includes identity-axis and rotated OBB cull canaries plus an explicit unsupported cross-type no-cull boundary. |

## Fixture Batches

The next implementation work should use small batches rather than one broad algorithm change.

| Batch | Planned fixture ids | Primary blockers covered | Purpose |
| --- | --- | --- | --- |
| A. Source/preprocess/intake/operator breadth | `paper_mixed_face_preprocess_operator`, `paper_degenerate_preprocess_face_drop`, `paper_concave_polygon_rejected` | source mesh/preprocessing, source-face intake, operator `Q` | Broaden mesh policy beyond current exact-overlap and simple convex source-face fixtures. |
| B. Primitive fit breadth | `paper_rotated_box_fit`, `paper_offset_sphere_fit`, `paper_off_axis_capsule_fit`, `paper_flat_capped_cylinder_axis_fit`, `paper_tapered_frustum_fit`, `paper_asymmetric_trapezoid_fit` | primitive vocabulary and fit | Broaden all six paper primitive names beyond current named minimal cases without changing Newton runtime support. |
| C. Cost/search/stop breadth | `paper_branching_cost_order`, `paper_equal_cost_queue_tie`, `paper_nonzero_threshold_block` | collapse cost, priority queue, target/threshold stop | Test weighted-priority ordering, queue tie/eager-stale-prune behavior, and nonzero finite threshold blocking. |
| D. Component-pair breadth | `paper_component_pair_multi_candidate_order`, `paper_component_pair_cap_skipped` | component-pair edge handling, target/threshold stop | Broaden disconnected-component pair insertion beyond one accepted and one blocked all-pairs case. |
| E. Postprocess breadth | `paper_rotated_nested_primitive`, `paper_cross_type_enclosure_boundary` | enclosed primitive postprocess | Broaden postprocess from one explicit identity-axis OBB canary to additional containment boundaries. |

Batch A was the first implementation batch. It broadens source mesh policy, source-face intake, and
operator accounting at the same time, while still staying offline-only.

## Fixture Rows

| Fixture id | Covers | Geometry idea | Report additions | Tests | Non-goals | Claim boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `paper_mixed_face_preprocess_operator` | source mesh/preprocessing, source-face intake, operator `Q` | One small source mesh containing a triangle, a quad, and a convex five-vertex polygon, with one exact duplicate coordinate pair shared across source-face boundaries. | Source-face arities, original vertex ids, deduplicated vertex ids, generated triangle ids, per-generated-triangle `Q`, source-face aggregate `Q`, aggregate eigenvalues/eigenvectors, and before/after component accounting. | Assert source-face ids survive preprocessing and fan triangulation; assert aggregate `Q` equals the sum of generated triangle `Q` rows; assert aggregate eigen fields exist and are finite. | No general polygon mesh support, no nonzero-distance cleanup, no Newton mapping. | Fixture-scoped operator/source-policy breadth only. |
| `paper_degenerate_preprocess_face_drop` | source mesh/preprocessing, operator `Q` | Exact-coordinate deduplication collapses one source triangle into a degenerate face while another face remains valid. | Dropped source-face id, drop reason `degenerate_after_preprocessing`, retained source-face ids, before/after face count, no executable `Q` row for the dropped face, retained-face eigenvalues/eigenvectors, and degeneracy label. | Assert the degenerate face is dropped deterministically; assert it cannot contribute `Q`, primitive-fit, or queue rows; assert retained-face operator eigen fields remain finite. | No broad mesh repair, no topology healing, no runtime package generation. | Deterministic dropped-face accounting only. |
| `paper_concave_polygon_rejected` | source-face intake policy | One concave non-triangle source face that the current conservative fan policy must reject for this lane. | Source-face arity, case-local failure label `source_face_intake_unsupported_concave_polygon`, no generated triangles, and `case_status: unsupported_fixture_policy`. | Assert the report does not silently fan-triangulate concave input; assert the unsupported label is case-local and does not become a top-level report failure label. | No general concave polygon triangulation claim. | Conservative unsupported-intake accounting only. |
| `paper_rotated_box_fit` | primitive vocabulary and fit | A rotated cuboid-like point set whose OBB should not use identity world axes. | Paper OBB axes, projected bounds, local/world center, containment checks, and volume formula for a non-axis-aligned fixture. | Assert axes are orthonormal and non-identity; assert all points are contained under the projected-bounds OBB. | No Newton runtime package or collision-quality claim. | Offline OBB fit breadth only. |
| `paper_offset_sphere_fit` | primitive vocabulary and fit | Point set whose paper sphere center comes from an offset OBB center rather than the world origin or point centroid. | OBB-derived sphere center, unclamped and clamped radius, containment checks, volume formula, and paper weight. | Assert the sphere center equals the paper OBB center and differs from the point centroid for the fixture. | No runtime sphere execution from this offline row. | Offline sphere fit breadth only. |
| `paper_off_axis_capsule_fit` | primitive vocabulary and fit | Elongated point set around a non-world-aligned axis. | Three capsule axis candidates, selected axis id, radius, cap-adjusted height, paper weight, and containment status. | Assert the selected capsule axis follows the operator-basis policy and records dimensions with positive radius and height. | No runtime capsule execution from this offline row. | Offline capsule fit breadth only. |
| `paper_flat_capped_cylinder_axis_fit` | primitive vocabulary and fit | Flat-capped cylinder point set whose best axis is not a world basis axis. | Three capped-cylinder axis candidates, selected axis id, radius, height, flat-cap formula, paper weight, containment status, and offline-only runtime boundary. | Assert a capped-cylinder-specific row exists, records flat-cap semantics, and remains distinct from Newton `cylinder`. | No Newton capped-cylinder support or cylinder approximation policy. | Offline capped-cylinder fit breadth only. |
| `paper_tapered_frustum_fit` | primitive vocabulary and fit | Tapered point set with different top and bottom radii along a declared axis. | Frustum axis policy, top/bottom radius fields, height, volume formula, paper weight, containment status, and offline-only runtime boundary. | Assert unequal radii are recorded and the fixture remains offline-only. | No Newton cone approximation policy. | Offline frustum fit breadth only. |
| `paper_asymmetric_trapezoid_fit` | primitive vocabulary and fit | Wedge-like point set that exercises six axis orderings for the trapezoidal-prism audit row. | Axis-order candidate table, selected ordering, side lengths, volume formula, paper weight, containment status, and offline-only runtime boundary. | Assert all six orderings are considered or explicitly reported with deterministic reasons. | No convex-hull adapter or Newton mapping. | Offline trapezoidal-prism fit breadth only. |
| `paper_branching_cost_order` | collapse cost, priority queue | A four-face branching topology with two initial adjacent candidates and known cost ordering. | Candidate table with raw `paper_base_cost`, weighted priority cost, queue keys, first pop, accepted merge, and updated neighbor insertion. | Assert the lower weighted priority candidate is popped first and base cost remains separately recorded. | No benchmark or merge-policy superiority claim. | Toy cost-order accounting only. |
| `paper_equal_cost_queue_tie` | priority queue | Two equal-cost adjacent candidates whose deterministic tie key decides first pop; one later entry becomes stale after a merge. | Equal priority costs, deterministic tie key fields, accepted event, stale-prune event, and final active groups. | Assert repeated report generation gives the same event order and stale-entry label. | No alternative optimizer or lookahead behavior. | Toy queue determinism accounting only. |
| `paper_nonzero_threshold_block` | target/threshold stop, collapse cost | Candidate merge with positive paper base cost and a positive finite threshold lower than that cost. | Nonzero threshold value, threshold metric, blocked event, stop reason, and accepted count `0` for the blocked candidate. | Assert the block is caused by a nonzero finite threshold, not the previous zero-threshold canary. | No threshold policy tuning or benchmark claim. | Toy threshold-stop accounting only. |
| `paper_component_pair_multi_candidate_order` | component-pair edge handling, target/threshold stop | Three disconnected components produce multiple component-pair candidates after topology edges cannot reach the target. | Component-pair candidate count, queue keys, selected pair, accepted merge, and final component count. | Assert more than one component-pair candidate is considered and the selected pair follows the recorded priority. | No broad real-asset disconnected-component evidence. | Toy component-pair ordering only. |
| `paper_component_pair_cap_skipped` | component-pair edge handling | More component pairs exist than a future configured pair cap permits. | Attempted pair count, cap value, skipped pair count greater than zero, skipped pair ids or deterministic skipped policy, and stop reason. | Assert skipped pairs are counted and do not disappear from accounting. | No production-scale pair search optimization. | Toy skipped-pair accounting only. |
| `paper_rotated_nested_primitive` | enclosed primitive postprocess | Inner and outer OBBs share a rotated non-identity axis frame, with the inner primitive fully enclosed. | Rotated axes, inner and outer ids, corner containment status, before/after count, and cull reason. | Assert the inner OBB is culled only after all transformed corners are contained. | No general containment library claim. | Toy postprocess containment breadth only. |
| `paper_cross_type_enclosure_boundary` | enclosed primitive postprocess | A sphere or capsule lies inside an OBB, or the report explicitly marks cross-type culling unsupported. | Containment test type, supported or unsupported label, cull/no-cull decision, and claim boundary. | Assert cross-type containment is either implemented with a deterministic check or explicitly blocked with no silent cull. | No broad redundant primitive removal quality claim. | Toy cross-type containment boundary only. |

## Batch Status

Batch A is now implemented in `cpd_paper_offline_report`:

```text
paper_fixture_breadth_batch_a
-> `paper_mixed_face_preprocess_operator`
-> `paper_degenerate_preprocess_face_drop`
-> `paper_concave_polygon_rejected`
-> report remains partial
-> no package generation, Newton, real USD, or benchmark work
```

Batch B is now implemented in `cpd_paper_offline_report`:

```text
paper_fixture_breadth_batch_b
-> `paper_rotated_box_fit`
-> `paper_offset_sphere_fit`
-> `paper_off_axis_capsule_fit`
-> `paper_flat_capped_cylinder_axis_fit`
-> `paper_tapered_frustum_fit`
-> `paper_asymmetric_trapezoid_fit`
-> report remains partial
-> no package generation, Newton, real USD, or benchmark work
```

Batch C is now implemented in `cpd_paper_offline_report`:

```text
paper_fixture_breadth_batch_c
-> `paper_branching_cost_order`
-> `paper_equal_cost_queue_tie`
-> `paper_nonzero_threshold_block`
-> report remains partial
-> no package generation, Newton, real USD, or benchmark work
```

Batch D is now implemented in `cpd_paper_offline_report`:

```text
paper_fixture_breadth_batch_d
-> `paper_component_pair_multi_candidate_order`
-> `paper_component_pair_cap_skipped`
-> report remains partial
-> no package generation, Newton, real USD, or benchmark work
```

Batch E is now implemented in `cpd_paper_offline_report`:

```text
paper_fixture_breadth_batch_e
-> `paper_rotated_nested_primitive`
-> `paper_cross_type_enclosure_boundary`
-> report remains partial
-> no package generation, Newton, real USD, or benchmark work
```

The fixture-breadth completion review is now implemented:

```text
paper_fixture_breadth_completion_review
-> review fixture-breadth evidence against the scope-audit blockers
-> report remains partial
-> paper_faithful_offline_supported remains false
-> no package generation, Newton, real USD, or benchmark work
```

The now-closed planning gate after fixture-breadth completion was:

```text
paper_faithful_offline_generalization_plan
-> planning-only gate for broadening the offline algorithm beyond named toy fixtures
-> not paper_faithful_offline support
-> no package generation, Newton, real USD, or benchmark work
```

This planning gate is implemented as a command-only table inside `cpd_paper_offline_report`. The
report remains partial, keeps `paper_faithful_offline_supported: false`, and now also includes the
offline source-policy matrix for `paper_generalization_batch_a_source_policy`.

The first implementation gate after this plan is now implemented:

```text
paper_generalization_batch_a_source_policy
-> implemented as an offline source-policy matrix over deterministic synthetic meshes
-> record exact-coordinate dedup, source-face remap, concave rejection, and Q aggregation
-> stay offline report-only
-> not generate packages, run Newton, use real USD, or claim benchmark/collision quality
```

Batch A stays important because it broadens source mesh, source-face intake, and operator audit
coverage that every later primitive-fit and search fixture depends on. Batch B stays important
because it broadens primitive-fit evidence before cost/search fixtures start comparing
candidate-engine behavior. The primitive-fit engine generalization gate is now implemented as an
offline report-only matrix over deterministic in-memory probes. The search-engine generalization
gate is now also implemented as an offline report-only matrix over existing deterministic topology,
threshold, and component-pair traces. The postprocess-policy generalization gate is now implemented
as an offline report-only matrix, and the package-boundary readiness gate is now implemented as an
offline matrix before package conversion. The changed-decomposition output contract is now
implemented as an offline changed-decomposition output contract, not a `CollisionPackage`. The
package-adapter contract is now implemented as a command-only offline adapter decision table, not a
`CollisionPackage`. The unsupported-primitive policy is now implemented as a command-only offline
policy table, not a `CollisionPackage`. The mapped-subset package-conversion plan is now
implemented as a command-only offline planning table, not a `CollisionPackage`; it keeps the
current unmapped trapezoidal-prism rows offline and records zero current package-conversion
candidates. The mapped-subset candidate matrix is now implemented as a command-only offline
review matrix, not a `CollisionPackage`; it records three future-family review rows and keeps
current package-conversion candidates at zero. The mapped-subset adapter-preflight contract is now
implemented as a command-only offline contract, not `PrimitiveSpec` generation and not a
`CollisionPackage`; it records future adapter requirements, keeps current unmapped rows offline,
and keeps package generation disabled. The mapped-subset PrimitiveSpec dry-run contract is now
implemented as a command-only offline contract, not real `PrimitiveSpec` generation and not a
`CollisionPackage`; it records zero current PrimitiveSpec candidates and keeps current unmapped
rows offline/no-op. The mapped-subset PrimitiveSpec validation contract is now implemented as a
command-only offline validation contract, not real `PrimitiveSpec` generation and not a
`CollisionPackage`; it validates the dry-run contract and keeps current unmapped rows offline/no-op.
The mapped-subset PrimitiveSpec generation-preflight contract is now implemented as a command-only
offline preflight contract, not real `PrimitiveSpec` generation and not a `CollisionPackage`; it
records zero current generation candidates, zero generated PrimitiveSpecs, zero generated
CollisionPackages, and zero runtime-admissibility checks. The mapped-subset PrimitiveSpec
generation contract is now also implemented as a command-only offline template contract, not
runtime `PrimitiveSpec` generation and not a `CollisionPackage`; it emits native-family templates
for box/sphere/capsule, keeps current unmapped rows offline/no-op, and keeps runtime/package checks
at zero. The mapped-subset PrimitiveSpec candidate-source contract is now implemented as a
command-only offline source audit, not runtime `PrimitiveSpec` generation and not a
`CollisionPackage`; it keeps the native templates future-only, classifies the current 16 unmapped
trapezoidal-prism rows as traceable but ineligible, records zero eligible current PrimitiveSpec
candidate sources, and keeps runtime/package checks at zero. The mapped-subset native-current
fixture contract is now implemented as a command-only offline source-row contract, not runtime
`PrimitiveSpec` generation and not a `CollisionPackage`; it records exactly one synthetic
`paper_single_box` selected OBB/box source row, one eligible current candidate source, one
report-only PrimitiveSpec generation candidate, zero generated PrimitiveSpecs, zero generated
CollisionPackages, and zero runtime-admissibility checks. The native-fixture PrimitiveSpec-like
dict generation contract is now implemented as a command-only offline dict-generation contract,
not runtime `PrimitiveSpec` object creation and not a `CollisionPackage`; it emits one
JSON-serializable report-only dict for the same synthetic source row and keeps runtime/package
checks at zero. The native-fixture serialization contract is now also implemented as a
command-only offline JSON serialization/schema-stability contract, not runtime `PrimitiveSpec`
object creation and not a `CollisionPackage`; it validates strict canonical JSON and round-trip
equality for that one report-only dict and keeps runtime/package checks at zero. The
runtime-boundary preflight contract is now implemented as a command-only offline boundary check,
not runtime `PrimitiveSpec` construction and not a `CollisionPackage`; it records one later
runtime-construction candidate for that row while keeping runtime construction disallowed and
runtime/package checks at zero. The runtime-construction contract is now implemented as a
single-fixture offline construction check; it constructs exactly one runtime `PrimitiveSpec` from
the canonical `paper_single_box` OBB/box preflight JSON, stores only `PrimitiveSpec.to_dict()` in
the report, records runtime PrimitiveSpec generation counts as one, and still keeps package,
Newton, real-USD, benchmark, collision-quality, deployment, and certification checks at zero or
false. The collision-package generation preflight contract is now implemented as a single-fixture
offline preflight that records one later package-generation candidate from the runtime
`PrimitiveSpec.to_dict()` row while still creating zero CollisionPackage artifacts and zero
runtime-admissibility checks. The collision-package generation contract is now implemented as a
single-fixture offline generation check that constructs exactly one synthetic, report-scoped
`CollisionPackage.to_dict()` artifact for the same `paper_single_box` OBB/box row while still
creating zero runtime-admissibility checks and no Newton, real-USD, benchmark, collision-quality,
deployment, or certification evidence. The runtime-admissibility preflight then records one later
runtime-admissibility candidate row without running the check. The runtime-admissibility contract
now records one offline/static finite-geometry and box-schema check for that same synthetic
package. The Newton shape-mapping preflight now records one offline/static mapper-handoff row for
that same box artifact while still running zero mapping attempts and zero Newton code. The
shape-mapping contract now records one offline/static report-scoped descriptor dict for that same
box artifact while still running zero mapping attempts, creating zero Newton shape objects, and
running zero Newton code. The Newton shape runtime-boundary preflight contract now records one
later runtime-construction candidate for that descriptor row while still creating zero Newton shape
objects and running zero Newton code. The Newton shape runtime-construction contract now records
exactly one repo-local `NewtonShapeMapping.to_dict()` mapping record for that descriptor row while
still creating zero Newton engine shape objects, making zero builder shape calls, and running zero
Newton code. The Newton shape runtime builder-preflight contract now records one JSON-safe future
box builder call plan for that mapping record while still creating zero Newton engine shape
objects, making zero builder shape calls, and running zero Newton code. The Newton shape runtime
builder-construction contract now records one JSON-safe repo-local recording-builder
`add_shape_box` call artifact while still importing no real Newton runtime, creating zero Newton
engine shape objects, making zero real Newton builder shape calls, and running zero Newton code.
The Newton engine-builder boundary-preflight contract now records one offline/static checklist row
for the future real `newton.ModelBuilder` / `add_shape_box` environment boundary while still
importing no real Newton runtime, instantiating no real `newton.ModelBuilder`, making zero real
builder shape calls, finalizing no model, creating no collision pipeline, and running zero Newton
code.
The Newton engine-builder environment-probe contract now records one bounded environment-provenance
row for the same synthetic box mapping, including configured-source-dir status and JSON-safe
Newton/Warp `find_spec` provenance shape. The default report remains no-config and imports no real
Newton or Warp runtime.
The Newton engine-builder API-surface contract now records one bounded source-AST API-surface row
for the same synthetic box mapping. The default report records no configured source directory; an
explicit source directory may be read and parsed as AST only.
The Newton engine-builder entry contract now records one report-only default no-runtime-entry
decision for the same synthetic box mapping. It keeps real Newton imports, `newton.ModelBuilder`,
real builder shape calls, model finalization, collision pipeline calls, and Newton execution at
zero.
The current next gate is
`paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract`, not
Newton execution.
Batch C
stays important because it checks
weighted-priority ordering, deterministic queue ties/eager-stale-prune events, and one positive
finite threshold block before broader component-pair cases. Batch D stays important because it
checks multiple component-pair candidates and capped
skipped-pair accounting before postprocess breadth. Batch E stays important because it checks
rotated OBB containment and explicitly records the unsupported cross-type boundary without silently
culling. The generalization Batch D postprocess-policy matrix now summarizes those existing
postprocess audit fixtures without adding a general containment library.

## Claim Boundary

This plan supports only this statement:

```text
The repository has an offline-only fixture-breadth expansion plan and a Batch A synthetic
source/preprocess/intake/operator implementation plus a Batch B primitive-fit implementation
plus a Batch C cost/search/stop implementation plus a Batch D component-pair implementation plus a
Batch E postprocess implementation plus a command-only synthetic fixture-breadth completion review,
a source-policy generalization matrix, a primitive-fit engine generalization matrix, and a
search-engine generalization matrix, plus a postprocess-policy generalization matrix, a
package-boundary readiness matrix, an offline changed-decomposition output contract, an offline
package-adapter contract, an offline unsupported-primitive policy, an offline mapped-subset
package-conversion plan, an offline mapped-subset candidate matrix, and an offline mapped-subset
adapter-preflight contract, plus an offline mapped-subset PrimitiveSpec dry-run contract inside
the partial paper report, plus an offline mapped-subset PrimitiveSpec validation contract that
validates the dry-run shape while still generating zero real PrimitiveSpec and zero
CollisionPackage artifacts, plus an offline mapped-subset PrimitiveSpec generation-preflight
contract that still generates zero real PrimitiveSpec, zero CollisionPackage artifacts, and zero
runtime-admissibility checks, plus an offline mapped-subset PrimitiveSpec candidate-source
contract that records zero eligible current PrimitiveSpec candidate sources and still generates
zero real PrimitiveSpec, zero CollisionPackage artifacts, and zero runtime-admissibility checks,
plus an offline mapped-subset native-current fixture source-row contract that records one
synthetic `paper_single_box` OBB/box source row and one report-only PrimitiveSpec generation
candidate while still generating zero real PrimitiveSpec, zero CollisionPackage artifacts, and
zero runtime-admissibility checks, plus an offline mapped-subset native-fixture PrimitiveSpec-like
dict generation contract and serialization contract for that row, plus an offline runtime-boundary
preflight that records one later runtime-construction candidate while generating zero runtime
objects, plus a single-fixture offline runtime-construction contract that constructs exactly one
runtime `PrimitiveSpec` object from canonical `paper_single_box` OBB/box preflight JSON and stores
only `PrimitiveSpec.to_dict()` in the report while still generating zero CollisionPackage
artifacts, zero runtime-admissibility checks, and no Newton, real-USD, benchmark,
collision-quality, deployment, or certification evidence, plus a single-fixture offline
collision-package generation preflight that records one later package-generation candidate while
still generating zero CollisionPackage artifacts and zero runtime-admissibility checks, plus a
single-fixture offline collision-package generation contract that generates exactly one synthetic
`CollisionPackage.to_dict()` artifact while still generating zero runtime-admissibility checks,
plus a single-fixture runtime-admissibility preflight contract that records exactly one later
runtime-admissibility candidate row while still generating zero runtime-admissibility checks, plus
a single-fixture offline/static runtime-admissibility contract that records exactly one
finite-geometry and box-schema check while still generating zero Newton shape mappings and zero
Newton runtime executions, plus a single-fixture offline/static Newton shape-mapping preflight
contract that records exactly one mapper-handoff row while still generating zero Newton shape
mappings and zero Newton runtime executions, plus a single-fixture offline/static Newton
shape-mapping contract that records exactly one report-scoped descriptor dict while still creating
zero Newton shape objects and zero Newton runtime executions, plus a single-fixture offline/static
Newton shape runtime-boundary preflight contract that records one later runtime-construction
candidate while still creating zero Newton shape objects and zero Newton runtime executions, plus a
single-fixture offline/report-scoped Newton shape runtime-construction contract that records
exactly one repo-local `NewtonShapeMapping.to_dict()` mapping record while still creating zero
Newton engine shape objects, zero builder shape calls, and zero Newton runtime executions, plus a
single-fixture offline/static Newton shape runtime builder-preflight contract that records exactly
one JSON-safe future box builder call plan while still allowing zero builder calls, creating zero
Newton engine shape objects, and running zero Newton runtime executions, plus a single-fixture
offline/report-only Newton shape runtime builder-construction contract that records one JSON-safe
repo-local recording-builder `add_shape_box` call artifact while still importing no real Newton
runtime, creating zero Newton engine shape objects, making zero real Newton builder shape calls,
and running zero Newton runtime executions, plus a single-fixture offline/static Newton
engine-builder boundary-preflight contract that records one future-boundary checklist row while
still importing no real Newton runtime, instantiating no real `newton.ModelBuilder`, making zero
real builder shape calls, finalizing no model, creating no collision pipeline, and running zero
Newton runtime executions, plus a single-fixture bounded Newton/Warp environment-probe contract
that records configured-source-dir status and JSON-safe `find_spec` provenance shape while keeping
real runtime imports and Newton execution at zero, plus a single-fixture bounded source-AST
API-surface contract that records default no-config API-surface status while keeping real runtime
imports, `newton.ModelBuilder` instantiation, real builder shape calls, model finalization,
collision pipeline calls, and Newton execution at zero, plus a single-fixture report-only
engine-builder entry contract that records `defer_real_runtime_entry` while keeping real runtime
imports, `newton.ModelBuilder` instantiation, real builder shape calls, model finalization,
collision pipeline calls, and Newton execution at zero.
```

It does not support:

- `paper_faithful_offline`;
- full CPD paper reproduction;
- general package readiness;
- executable runtime-admissibility execution beyond the one report-only static check;
- Newton runtime support;
- Newton execution;
- real-USD evidence;
- benchmark evidence;
- collision-quality validation;
- deployment readiness;
- safety certification.
