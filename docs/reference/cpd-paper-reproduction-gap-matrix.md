# CPD Paper Reproduction Gap Matrix

This page maps the Convex Primitive Decomposition for Collision Detection paper requirements to
the repository's current Newton CPD workbench. It is a planning and audit document, not new
experiment evidence, and not a claim that the paper algorithm has been reproduced.

For the plain-language pipeline map, see
[CPD pipeline step-by-step explainer](cpd-pipeline-step-by-step-explainer.md). For current claim
limits, see [Claim Boundaries](claim-boundaries.md). For the planned fixture-scoped offline lane,
see [CPD paper-faithful offline lane spec](cpd-paper-faithful-offline-lane-spec.md). For the
current fixture-breadth plan, see
[CPD paper fixture-breadth expansion plan](cpd-paper-fixture-breadth-expansion-plan.md).

## Scope

The matrix answers six questions for each paper requirement:

- what the paper requires;
- what the repository has now;
- whether the current artifact is a surrogate or paper-faithful;
- what must be implemented in an offline paper lane first;
- what can enter the Newton runtime lane;
- what claim boundary applies.

The source-paper intake used for this matrix lives under
`docs/tmp/papers/arXiv-2602.07369v1/`. The durable statement is this reference page, not the raw
temporary intake.

## Status Terms

| Term | Meaning |
| --- | --- |
| `not_started` | No repository artifact implements the paper requirement yet. |
| `surrogate` | A current artifact asks a similar engineering question, but does not implement the paper method. |
| `partial` | A current artifact overlaps with the paper requirement, but misses material details or scope. |
| `paper_faithful_offline` | The declared fixture scope implements the paper-side mechanic offline with tests and dated records. No current row has this status yet, and the term does not imply benchmark, Newton runtime, or full reproduction evidence. |
| `newton_runtime_mapped` | A primitive or package can be constructed in Newton diagnostic code under recorded settings. This is separate from paper faithfulness. |

## Primitive Terminology

| Paper concept | Current CPD-like kind | Newton runtime kind | Current mapping status |
| --- | --- | --- | --- |
| Oriented bounding box | `box` | `box` | Runtime-mapped when package validation passes. |
| Sphere | `sphere` | `sphere` | Runtime-mapped when package validation passes. |
| Capsule | paper-shaped offline axis fit-audit row in `cpd_paper_offline_report`; the older CPD-like `capsule` package kind remains a separate runtime-mapped primitive outside this paper audit row. | `capsule` | Newton-native in principle, but the paper-lane capsule row is not packaged or run in Newton by this report. Any runtime use still needs package conversion and admissibility records. |
| Paper capped cylinder | Offline flat-capped-cylinder fit-audit candidate row for named toy fixtures only; the older CPD-like `capped_cylinder` package kind remains a hemisphere-cap proxy outside this paper lane. | Newton `cylinder` is separate. | The paper-lane capped-cylinder row is not Newton-mapped; any future runtime adapter needs a dated conversion spec. |
| Frustum | offline fit-audit candidate row for named toy fixtures only | no direct runtime primitive | Keep offline unless an explicit approximation policy exists. Newton `cone` is not general frustum support. |
| Isosceles trapezoidal prism | offline fit-audit candidate row under the report label `trapezoidal_prism` for named toy fixtures only | no direct runtime primitive | Keep offline unless converted through a recorded convex-hull or other adapter. |
| Paper extension not in the original primitive set | `cone`, `ellipsoid` | `cone`, `ellipsoid` | Newton-native diagnostics only; not paper-faithful primitive support. |

## Gap Matrix

| Paper requirement | Current repository artifact | Status | Surrogate or paper-faithful? | Offline paper-lane work first | Newton runtime lane | Claim boundary |
| --- | --- | --- | --- | --- | --- | --- |
| Input mesh with face-based decomposition. The paper starts from mesh vertices and polygonal faces, then assigns primitives to faces so the surface is covered by primitive groups. | `TriangleMesh` is triangle-only. USD intake can extract capped first meshes, and synthetic fixtures can feed the CPD-like baseline. | partial | Partial infrastructure, not paper-scope mesh intake. | Preserve source-face accounting, document polygon-to-triangle handling, and add deterministic fixtures that check face coverage. | Newton should only consume already generated packages; it should not decide paper face grouping. | Asset intake is plumbing, not collider-quality evidence. |
| Preprocessing for overlapped or duplicate vertices. The paper discusses vertex deduplication because unclean meshes can change topology and decomposition. | The partial `cpd_paper_offline_report` now includes `paper_duplicate_vertex_preprocessing`, plus Batch A `paper_mixed_face_preprocess_operator` and `paper_degenerate_preprocess_face_drop`. These record exact-coordinate duplicate clusters, source-face remaps, executable deduplicated faces, and one dropped degenerate source face after preprocessing. | partial | Paper-shaped for exact-overlap synthetic fixtures only. It is not nonzero-threshold deduplication, approximate spatial hashing, or general mesh cleanup. | The package-adapter contract, unsupported-primitive policy, mapped-subset plan, candidate matrix, adapter-preflight contract, PrimitiveSpec dry-run contract, PrimitiveSpec validation contract, PrimitiveSpec generation-preflight contract, PrimitiveSpec generation contract, PrimitiveSpec candidate-source contract, native-current fixture contract, native-fixture PrimitiveSpec-like dict generation contract, native-fixture serialization contract, runtime-boundary preflight contract, runtime-construction contract, collision-package generation preflight contract, collision-package generation contract, runtime-admissibility preflight contract, and runtime-admissibility contract, Newton shape-mapping preflight contract, Newton shape-mapping contract, Newton shape runtime-boundary preflight contract, Newton shape runtime-construction contract, Newton shape runtime builder-preflight contract, Newton shape runtime builder-construction contract, and Newton shape runtime engine-builder boundary preflight contract and Newton shape runtime engine-builder environment-probe contract are now implemented as bounded offline/static/report-only contracts; proceed to `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract` for bounded API-surface inspection before any real Newton engine-builder boundary crossing, actual Newton builder shape call, Newton shape object construction, Newton runtime execution, real-USD evaluation, benchmark work, or collision-quality claim. Broader unclean-mesh policy remains future work. | Not a Newton runtime concern except through the final package produced later. | Do not claim robust unclean-mesh handling, paper-faithful preprocessing, or collision quality from these fixtures. |
| Per-face linear operator `Q`: area-weighted normal outer product plus optional tangent-stability term, summed when face groups merge. | `TriangleMesh.face_operator()` computes an area-weighted triangle normal/tangent matrix. The partial `cpd_paper_offline_report` now records per-face and merged-group operator audit fields for triangle fixtures, quad/polygon source-face aggregate `Q`, Batch A mixed source-face aggregate `Q` with eigenvalues/eigenvectors, and retained-face eigen fields after a degenerate source face is dropped. | partial | Paper-shaped for named fixtures. The quad/polygon path records a conservative fan-triangulation policy for planar, convex, consistently wound toy faces; the concave fixture is explicitly rejected. This is not a general polygon mesh implementation. | The package-adapter contract, unsupported-primitive policy, mapped-subset plan, candidate matrix, adapter-preflight contract, PrimitiveSpec dry-run contract, PrimitiveSpec validation contract, PrimitiveSpec generation-preflight contract, PrimitiveSpec generation contract, PrimitiveSpec candidate-source contract, native-current fixture contract, native-fixture PrimitiveSpec-like dict generation contract, native-fixture serialization contract, runtime-boundary preflight contract, runtime-construction contract, collision-package generation preflight contract, collision-package generation contract, runtime-admissibility preflight contract, and runtime-admissibility contract, Newton shape-mapping preflight contract, Newton shape-mapping contract, Newton shape runtime-boundary preflight contract, Newton shape runtime-construction contract, Newton shape runtime builder-preflight contract, Newton shape runtime builder-construction contract, and Newton shape runtime engine-builder boundary preflight contract and Newton shape runtime engine-builder environment-probe contract are now implemented as bounded offline/static/report-only contracts; proceed to `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract` for bounded API-surface inspection before any real Newton engine-builder boundary crossing, actual Newton builder shape call, Newton shape object construction, Newton runtime execution, real-USD evaluation, benchmark work, or collision-quality claim. | No Newton mapping; this is algorithm-side data. | This supports "paper-shaped operator/intake audit for named fixtures", not paper-faithful CPD. |
| Primitive vocabulary: oriented bounding box, sphere, capsule, capped cylinder, frustum, and isosceles trapezoidal prism. | Current CPD-like candidates include `box`, `sphere`, `capsule`, `cylinder`, `cone`, `ellipsoid`, and an opt-in `capped_cylinder` proxy. Current Newton mapping supports `box`, `sphere`, `capsule`, `cylinder`, `cone`, and `ellipsoid`. The partial `cpd_paper_offline_report` now includes offline paper-shaped OBB/sphere fit-audit rows, a paper-shaped capsule axis fit-audit row, offline-only flat-capped-cylinder, frustum, and trapezoidal-prism fit-audit rows, Batch B primitive-fit breadth fixtures covering all six paper primitive names, and a `paper_generalization_batch_b_primitive_fit_engine` matrix that reuses the same candidate families over deterministic in-memory probes. The scope audit marks this criterion `partial_fixture_scope`. | partial | Mixed. `box` and `sphere` are paper-shaped offline fit-audit rows for named fixtures and generated probes, but this is still not general paper-faithful primitive fitting. `capsule` has paper-shaped offline axis audit rows with Newton-native kind metadata but no package/runtime execution. `capped_cylinder`, `frustum`, and `trapezoidal_prism` remain offline audit rows only, not runtime support or full paper-faithful coverage. `cone` and `ellipsoid` are Newton-native extensions, not paper primitives. | The package-adapter contract, unsupported-primitive policy, mapped-subset plan, candidate matrix, adapter-preflight contract, PrimitiveSpec dry-run contract, PrimitiveSpec validation contract, PrimitiveSpec generation-preflight contract, PrimitiveSpec generation contract, PrimitiveSpec candidate-source contract, native-current fixture contract, native-fixture PrimitiveSpec-like dict generation contract, native-fixture serialization contract, runtime-boundary preflight contract, runtime-construction contract, collision-package generation preflight contract, collision-package generation contract, runtime-admissibility preflight contract, and runtime-admissibility contract, Newton shape-mapping preflight contract, Newton shape-mapping contract, Newton shape runtime-boundary preflight contract, Newton shape runtime-construction contract, Newton shape runtime builder-preflight contract, Newton shape runtime builder-construction contract, and Newton shape runtime engine-builder boundary preflight contract and Newton shape runtime engine-builder environment-probe contract are now implemented as bounded offline/static/report-only contracts; proceed to `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract` for bounded API-surface inspection before any real Newton engine-builder boundary crossing, actual Newton builder shape call, Newton shape object construction, Newton runtime execution, real-USD evaluation, benchmark work, or collision-quality claim. | Only the intersection with Newton-native support should run in Newton directly after package conversion and runtime admissibility checks. Paper-only primitives need either an explicit approximation report or must stay offline. | Primitive support is not evidence of better collision quality or full CPD reproduction. |
| Primitive construction from operator eigenvectors and assigned points. The paper fits each primitive by expanding parameters to enclose the assigned point set. | Current fitters use operator axes and point bounds/radial spans, but several are simplified proxies. The partial `cpd_paper_offline_report` audits all six paper primitive names: paper-shaped OBB, paper-shaped sphere, paper-shaped capsule, offline-only flat capped cylinder, offline-only frustum, and offline-only trapezoidal-prism rows. Batch B adds rotated OBB, offset OBB-centered sphere, off-axis capsule, off-axis flat capped cylinder, tapered frustum, and asymmetric trapezoidal-prism fixtures. The generalization Batch B matrix now summarizes the reusable primitive-fit engine over six deterministic probes and records candidate order, target candidate rows, selected candidate rows, containment checks, finite numeric fields, and runtime mapping boundaries. The scope audit marks this criterion `partial_fixture_scope`. | partial | Paper-shaped and fixture-scoped for OBB/sphere/capsule/capped-cylinder/frustum/trapezoidal-prism audit rows. This remains partial because robust fitting, package adaptation, and evaluation are not complete. | The package-adapter contract, unsupported-primitive policy, mapped-subset plan, candidate matrix, adapter-preflight contract, PrimitiveSpec dry-run contract, PrimitiveSpec validation contract, PrimitiveSpec generation-preflight contract, PrimitiveSpec generation contract, PrimitiveSpec candidate-source contract, native-current fixture contract, native-fixture PrimitiveSpec-like dict generation contract, native-fixture serialization contract, runtime-boundary preflight contract, runtime-construction contract, collision-package generation preflight contract, collision-package generation contract, runtime-admissibility preflight contract, and runtime-admissibility contract, Newton shape-mapping preflight contract, Newton shape-mapping contract, Newton shape runtime-boundary preflight contract, Newton shape runtime-construction contract, Newton shape runtime builder-preflight contract, Newton shape runtime builder-construction contract, and Newton shape runtime engine-builder boundary preflight contract and Newton shape runtime engine-builder environment-probe contract are now implemented as bounded offline/static/report-only contracts; proceed to `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract` for bounded API-surface inspection before any real Newton engine-builder boundary crossing, actual Newton builder shape call, Newton shape object construction, Newton runtime execution, real-USD evaluation, benchmark work, or collision-quality claim. | Newton should receive only mapped package primitives after a separate package conversion and runtime-admissibility check. | Candidate audit tables explain current choices only under the current partial offline slice. |
| Collapse cost: merge two primitives by the added volume of the merged primitive over the previous two, with optional primitive type weighting. | Current objective reports include raw and AABB-normalized merge-excess fields. The partial `cpd_paper_offline_report` now records unnormalized `paper_base_cost` separately from `weighted_priority_cost` for one two-face toy fixture, topology priority-queue candidate summaries, Batch C weighted-priority ordering, one threshold-disabled accepted component-pair candidate, one zero-threshold blocked component-pair candidate, one positive finite-threshold blocked component-pair candidate, and Batch D component-pair candidate ordering. The scope audit marks this criterion `partial_fixture_scope`. | partial | Paper-shaped and fixture-scoped. The cost fields match the planned split for named toy topology and component-pair edges, but this is still not a broad optimizer or benchmark. | The package-adapter contract, unsupported-primitive policy, mapped-subset plan, candidate matrix, adapter-preflight contract, PrimitiveSpec dry-run contract, PrimitiveSpec validation contract, PrimitiveSpec generation-preflight contract, PrimitiveSpec generation contract, PrimitiveSpec candidate-source contract, native-current fixture contract, native-fixture PrimitiveSpec-like dict generation contract, native-fixture serialization contract, runtime-boundary preflight contract, runtime-construction contract, collision-package generation preflight contract, collision-package generation contract, runtime-admissibility preflight contract, and runtime-admissibility contract, Newton shape-mapping preflight contract, Newton shape-mapping contract, Newton shape runtime-boundary preflight contract, Newton shape runtime-construction contract, Newton shape runtime builder-preflight contract, Newton shape runtime builder-construction contract, and Newton shape runtime engine-builder boundary preflight contract and Newton shape runtime engine-builder environment-probe contract are now implemented as bounded offline/static/report-only contracts; proceed to `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract` for bounded API-surface inspection before any real Newton engine-builder boundary crossing, actual Newton builder shape call, Newton shape object construction, Newton runtime execution, real-USD evaluation, benchmark work, or collision-quality claim. | Newton should not use cost terms directly; it consumes packages generated after offline selection. | A lower paper-shaped toy cost or blocked toy merge is not a benchmark or quality result. |
| Priority-queue greedy collapse over adjacent face groups. The paper initializes adjacent face-pair candidates and repeatedly collapses the minimum-cost candidate. | The partial `cpd_paper_offline_report` now includes a topology-only priority-queue trace over `paper_three_face_chain`, Batch C branching weighted-priority ordering where base-cost and weighted-priority choices differ, Batch C equal-cost deterministic tie and eager-stale-prune behavior, a threshold-disabled component-pair insertion trace over `paper_disconnected_components`, finite-threshold blocked component-pair traces, Batch D multi-candidate component-pair ordering and capped skipped-pair accounting, and a deduplicated-topology trace over `paper_duplicate_vertex_preprocessing`, with deterministic queue keys, accepted/blocked decisions, stale-prune fields where applicable, component-pair insertion metadata, final active groups, and stop reasons. The scope audit marks this criterion `partial_fixture_scope`. | partial | Paper-shaped for named toy fixtures. It is not full paper decomposition because search traces remain toy-scoped and the scope audit keeps the lane partial. | The package-adapter contract, unsupported-primitive policy, mapped-subset plan, candidate matrix, adapter-preflight contract, PrimitiveSpec dry-run contract, PrimitiveSpec validation contract, PrimitiveSpec generation-preflight contract, PrimitiveSpec generation contract, PrimitiveSpec candidate-source contract, native-current fixture contract, native-fixture PrimitiveSpec-like dict generation contract, native-fixture serialization contract, runtime-boundary preflight contract, runtime-construction contract, collision-package generation preflight contract, collision-package generation contract, runtime-admissibility preflight contract, and runtime-admissibility contract, Newton shape-mapping preflight contract, Newton shape-mapping contract, Newton shape runtime-boundary preflight contract, Newton shape runtime-construction contract, Newton shape runtime builder-preflight contract, Newton shape runtime builder-construction contract, and Newton shape runtime engine-builder boundary preflight contract and Newton shape runtime engine-builder environment-probe contract are now implemented as bounded offline/static/report-only contracts; proceed to `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract` for bounded API-surface inspection before any real Newton engine-builder boundary crossing, actual Newton builder shape call, Newton shape object construction, Newton runtime execution, real-USD evaluation, benchmark work, or collision-quality claim. | Newton package probes should wait until the offline paper lane produces a changed package. | Toy search traces do not prove merge-policy superiority. |
| Target primitive count `N` and optional excess-volume threshold. The paper stops when no collapses remain or the target count is reached; thresholding can block high-excess merges. | Current configs have max primitive limits and some threshold-style component-merge gates. The partial `cpd_paper_offline_report` now records `target_primitive_count`, disabled, zero finite, and positive finite `excess_volume_threshold` cases, accepted and blocked component-pair counts, skipped component-pair counts including Batch D capped skipped pairs, and target-count or threshold-blocked stop reasons for named toy traces. The scope audit marks this criterion `partial_fixture_scope`. | partial | Partial and fixture-scoped. Batch C adds a positive nonzero finite threshold block and Batch D adds capped component-pair skip accounting, but these are still toy fixtures rather than a full threshold/search policy implementation. | The package-adapter contract, unsupported-primitive policy, mapped-subset plan, candidate matrix, adapter-preflight contract, PrimitiveSpec dry-run contract, PrimitiveSpec validation contract, PrimitiveSpec generation-preflight contract, PrimitiveSpec generation contract, PrimitiveSpec candidate-source contract, native-current fixture contract, native-fixture PrimitiveSpec-like dict generation contract, native-fixture serialization contract, runtime-boundary preflight contract, runtime-construction contract, collision-package generation preflight contract, collision-package generation contract, runtime-admissibility preflight contract, and runtime-admissibility contract, Newton shape-mapping preflight contract, Newton shape-mapping contract, Newton shape runtime-boundary preflight contract, Newton shape runtime-construction contract, Newton shape runtime builder-preflight contract, Newton shape runtime builder-construction contract, and Newton shape runtime engine-builder boundary preflight contract and Newton shape runtime engine-builder environment-probe contract are now implemented as bounded offline/static/report-only contracts; proceed to `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract` for bounded API-surface inspection before any real Newton engine-builder boundary crossing, actual Newton builder shape call, Newton shape object construction, Newton runtime execution, real-USD evaluation, benchmark work, or collision-quality claim. | Newton should inherit the selected package only after the offline lane records final count and stop reason. | A stopped run is not success unless the report states which target and gates passed. |
| Pairwise component merging when disconnected topology prevents reaching the target. | Current `virtual_pairwise` component-merge diagnostics and synthetic fixtures cover a restricted CPD-like version. The partial `cpd_paper_offline_report` now inserts and accepts threshold-disabled `component_pair` queue events, inserts then blocks finite-threshold `component_pair` events for threshold fixtures, records three-way multi-candidate component-pair ordering, and records deterministic skipped-pair accounting under a fixture cap. The scope audit marks this criterion `partial_fixture_scope`. | partial | Paper-shaped but not paper-faithful. It records accepted, blocked, multi-candidate, and capped skipped-pair behavior on toy component fixtures only. | The package-adapter contract, unsupported-primitive policy, mapped-subset plan, candidate matrix, adapter-preflight contract, PrimitiveSpec dry-run contract, PrimitiveSpec validation contract, PrimitiveSpec generation-preflight contract, PrimitiveSpec generation contract, PrimitiveSpec candidate-source contract, native-current fixture contract, native-fixture PrimitiveSpec-like dict generation contract, native-fixture serialization contract, runtime-boundary preflight contract, runtime-construction contract, collision-package generation preflight contract, collision-package generation contract, runtime-admissibility preflight contract, and runtime-admissibility contract, Newton shape-mapping preflight contract, Newton shape-mapping contract, Newton shape runtime-boundary preflight contract, Newton shape runtime-construction contract, Newton shape runtime builder-preflight contract, Newton shape runtime builder-construction contract, and Newton shape runtime engine-builder boundary preflight contract and Newton shape runtime engine-builder environment-probe contract are now implemented as bounded offline/static/report-only contracts; proceed to `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract` for bounded API-surface inspection before any real Newton engine-builder boundary crossing, actual Newton builder shape call, Newton shape object construction, Newton runtime execution, real-USD evaluation, benchmark work, or collision-quality claim. | Runtime should only see a package after runtime admissibility and Newton-entry gates are separately recorded. | Component merging evidence is diagnostic accounting, not broad asset evidence. |
| Postprocessing to remove primitives enclosed by other primitives. | The partial `cpd_paper_offline_report` now includes `paper_nested_primitive`, an explicit identity-axis OBB cull fixture, plus Batch E `paper_rotated_nested_primitive` and `paper_cross_type_enclosure_boundary`. It now also includes `paper_generalization_batch_d_postprocess_policy`, an offline postprocess-policy matrix over those existing audit fixtures. It records before/after counts, cull reason, rotated corner containment status, conservative unsupported cross-type no-cull accounting, and package/Newton/real-USD/benchmark false triggers. | partial | Paper-shaped fixture accounting only. The input primitives are explicit audit rows, not generated by the full paper search. The rotated OBB check is a toy containment fixture, and the cross-type fixture is an explicit unsupported boundary, not a general primitive containment library. | The package-adapter contract, unsupported-primitive policy, mapped-subset plan, candidate matrix, adapter-preflight contract, PrimitiveSpec dry-run contract, PrimitiveSpec validation contract, PrimitiveSpec generation-preflight contract, PrimitiveSpec generation contract, PrimitiveSpec candidate-source contract, native-current fixture contract, native-fixture PrimitiveSpec-like dict generation contract, native-fixture serialization contract, runtime-boundary preflight contract, runtime-construction contract, collision-package generation preflight contract, collision-package generation contract, runtime-admissibility preflight contract, and runtime-admissibility contract, Newton shape-mapping preflight contract, Newton shape-mapping contract, Newton shape runtime-boundary preflight contract, Newton shape runtime-construction contract, Newton shape runtime builder-preflight contract, Newton shape runtime builder-construction contract, and Newton shape runtime engine-builder boundary preflight contract and Newton shape runtime engine-builder environment-probe contract are now implemented as bounded offline/static/report-only contracts; proceed to `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract` for bounded API-surface inspection before any real Newton engine-builder boundary crossing, actual Newton builder shape call, Newton shape object construction, Newton runtime execution, real-USD evaluation, benchmark work, or collision-quality claim. | Newton should consume postprocessed packages only after package generation and runtime admissibility are separately recorded. | This supports offline postprocess breadth accounting, not redundant primitive removal quality, runtime support, or full CPD reproduction. |
| Evaluation: qualitative simulation similarity, wall-time with many dropped spheres, one-way surface distances, byte cost, primitive/hull comparisons, and CoACD/V-HACD-style baselines. | Repository has Newton smoke diagnostics and workbench reports, but no paper benchmark reproduction. | not_started | Not paper-faithful. | Defer benchmark design until offline paper decomposition is implemented on toy fixtures and then selected small assets. | Newton benchmark tasks are a later phase, not the current offline lane. | No benchmark superiority, collision-quality validation, deployment readiness, or safety certification is supported. |

## Current Surrogates

The current repository has useful surrogates, but each must stay labeled:

- CPD-like face merge: useful for plumbing, not paper collapse.
- Offline objective report: paper-aligned accounting, not paper objective.
- AABB-normalized merge-excess: scale-aware diagnostic cost, not the paper's unnormalized collapse
  cost by itself.
- Candidate weighted-volume tables: current selection explanation, not proof of better primitive
  fitting.
- Cost-guided pairwise and two-step lookahead fixtures: toy merge/search behavior, not paper
  priority-queue optimization.
- Newton contact, drop/settle, and sphere-rain smokes: diagnostic runtime gates, not benchmark
  evaluation.

## Paper-Faithful Offline Lane Criteria

A future lane can be called `paper_faithful_offline` only after it records all of the following
for deterministic synthetic fixtures:

- source mesh, face groups, and preprocessing policy;
- polygon/quad source-face intake policy with generated-triangle remap when non-triangle fixture
  faces are included;
- per-face and merged-group `Q` operators with eigen decomposition;
- all six paper primitive fits and containment checks, including paper OBB/sphere construction
  metadata for the declared fixture scope;
- paper collapse cost and weighted volume fields;
- priority-queue collapse trace with stale-entry handling;
- target-count and threshold stop reasons;
- component-pair edge handling when needed;
- enclosed-primitive postprocessing;
- duplicate-vertex preprocessing policy and source-face remap after preprocessing;
- report schema, tests, and dated records.

Until then, use "paper-aligned surrogate", "paper-shaped", or "offline paper-lane planned" wording.

## Newton Entry Rule

The offline paper lane and Newton runtime lane must stay separate:

```text
paper-faithful offline report
-> explicit runtime admissibility check
-> recorded package conversion
-> Newton shape-mapping preflight
-> report-scoped Newton shape descriptor contract
-> Newton shape runtime-boundary preflight
-> Newton shape construction or mapping, if a later gate records it
-> Newton diagnostic smoke
```

Only primitives with recorded Newton runtime-boundary and mapping/construction evidence should
enter Newton directly. Paper primitives without
native Newton support should either remain offline or be converted through an explicitly recorded
approximation policy. That approximation would be a Newton diagnostic adapter, not the paper
primitive itself.

Runtime admissibility means the converted package passes finite center checks, right-handed
orthonormal axis checks where axes are present, positive dimension checks, and the target Newton
shape's expected dimension schema. Passing those checks is still runtime compatibility, not paper
faithfulness.

## Future Benchmark Gate Checklist

Benchmark work should stay blocked until the offline paper lane exists for toy fixtures. When it
starts, the benchmark spec should preserve these paper-side requirements:

- qualitative simulation-similarity review as a correctness signal;
- dropped-sphere wall-time task with the paper-scale sphere count and frame window recorded;
- simulator and CPU/GPU/runtime settings recorded rather than assumed interchangeable;
- one-way collider-to-input Hausdorff and Chamfer distances normalized by input bounding-box
  diagonal;
- byte-cost accounting for primitives and hulls;
- primitive and component counts by kind;
- CoACD and V-HACD comparison settings;
- manually chosen target primitive counts or a documented replacement policy.

## Recommended Next Slice

Batch A, Batch B, Batch C, Batch D, Batch E, the command-only synthetic fixture-breadth completion
review, and the command-only generalization planning table are now implemented inside the offline
report. The report now also implements `paper_generalization_batch_a_source_policy` as an offline
source-policy matrix for deterministic synthetic meshes and
`paper_generalization_batch_b_primitive_fit_engine` as an offline primitive-fit engine matrix over
deterministic in-memory probes. The report now also implements
`paper_generalization_batch_c_search_engine` as an offline search-trace matrix over deterministic
topology, threshold, and component-pair traces, and
`paper_generalization_batch_d_postprocess_policy` as an offline postprocess-policy matrix over
existing deterministic postprocess audit fixtures. The report now also implements
`paper_generalization_batch_e_package_boundary_readiness` as an offline package-boundary readiness
matrix before package conversion, and `paper_offline_changed_decomposition_output_contract` as an
offline changed-decomposition output contract, not a `CollisionPackage`, and
`paper_package_adapter_contract` as a command-only offline package-adapter contract, not a
`CollisionPackage`. The report now also implements
`paper_package_adapter_unsupported_primitive_policy` as a command-only offline policy table, not a
`CollisionPackage`. The report now also implements
`paper_package_conversion_mapped_subset_plan` as a command-only offline mapped-subset
package-conversion planning table, not a `CollisionPackage`. The report now also implements
`paper_mapped_subset_conversion_candidate_matrix` as a command-only offline candidate matrix, not a
`CollisionPackage`, and now also implements `paper_mapped_subset_adapter_preflight_contract` as a
command-only offline adapter-preflight contract, not `PrimitiveSpec` generation and not a
`CollisionPackage`. The report now also implements
`paper_mapped_subset_primitivespec_dry_run_contract` as a command-only offline PrimitiveSpec
dry-run contract, not real `PrimitiveSpec` generation and not a `CollisionPackage`. The report now
also implements `paper_mapped_subset_primitivespec_validation_contract` as a command-only offline
validation contract, not real `PrimitiveSpec` generation and not a `CollisionPackage`. The report
now also implements `paper_mapped_subset_primitivespec_generation_preflight_contract` as a
command-only offline generation-preflight contract, still not real `PrimitiveSpec` generation and
not a `CollisionPackage`. The report now also implements
`paper_mapped_subset_primitivespec_generation_contract` as a command-only offline generation
contract with template rows, still not real runtime `PrimitiveSpec` generation and not a
`CollisionPackage`. The report now also implements
`paper_mapped_subset_primitivespec_candidate_source_contract` as a command-only offline
candidate-source audit, still not real runtime `PrimitiveSpec` generation and not a
`CollisionPackage`. It keeps future native templates separate from current rows, records zero
eligible current PrimitiveSpec candidate sources, and keeps runtime/package checks at zero. The
report now also implements `paper_mapped_subset_native_current_fixture_contract` as a command-only
offline native-current source-row contract, still not real runtime `PrimitiveSpec` generation and
not a `CollisionPackage`. It records exactly one synthetic `paper_single_box` OBB/box source row,
one eligible current candidate source, one report-only PrimitiveSpec generation candidate, zero
generated PrimitiveSpecs, zero generated CollisionPackages, and zero runtime-admissibility checks.
The report now also implements
`paper_mapped_subset_primitivespec_native_fixture_generation_contract` and
`paper_mapped_subset_primitivespec_native_fixture_serialization_contract` as command-only offline
native-fixture contracts, still not real runtime `PrimitiveSpec` object creation and not a
`CollisionPackage`. They emit and then validate exactly one JSON-serializable report-only dict for
the deterministic synthetic `paper_single_box` OBB/box source row, while keeping generated runtime
PrimitiveSpecs, generated CollisionPackages, and runtime-admissibility checks at zero. The report
now also implements `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract` as a
command-only offline boundary contract, still not runtime `PrimitiveSpec` construction and not a
`CollisionPackage`. It records exactly one later runtime-construction candidate for that same row,
keeps runtime construction disallowed in the current gate, and keeps generated runtime
PrimitiveSpecs, generated CollisionPackages, and runtime-admissibility checks at zero. The report
now also implements `paper_mapped_subset_primitivespec_runtime_construction_contract` as a
single-fixture offline runtime-construction contract. It consumes that boundary preflight row,
constructs exactly one runtime `PrimitiveSpec` object from the canonical `paper_single_box`
OBB/box JSON after checking the runtime-boundary preflight row's canonical JSON SHA-256
fingerprint, stores only `PrimitiveSpec.to_dict()` output in the report, records generated runtime
PrimitiveSpec counts as one, and still records generated CollisionPackages and runtime-admissibility
checks at zero. The report now also implements
`paper_mapped_subset_collision_package_generation_preflight_contract` as a single-fixture offline
preflight contract. It consumes the runtime-construction row's `PrimitiveSpec.to_dict()` payload,
records exactly one later package-generation candidate for the same synthetic `paper_single_box`
OBB/box row, and still records generated CollisionPackages and runtime-admissibility checks at
zero. The report now also implements `paper_mapped_subset_collision_package_generation_contract`
as a single-fixture offline generation contract. It constructs exactly one synthetic,
report-scoped `CollisionPackage.to_dict()` artifact for the same `paper_single_box` OBB/box row,
records `generated_collision_package_count: 1`, keeps runtime-admissibility checks at zero, and
does not add Newton, real-USD, benchmark, or collision-quality evidence. The runtime-admissibility
preflight contract now records one later runtime-admissibility candidate row without running the
check, and the runtime-admissibility contract now records one offline/static finite-geometry and
box-schema check without Newton mapping or Newton execution. The Newton shape-mapping preflight
now records one static handoff row without a mapper call, Newton import, or runtime execution. The
Newton shape-mapping contract now records one static report-scoped descriptor dict without a
mapper call, Newton shape object construction, or runtime execution. The
Newton shape runtime-boundary preflight now records one later runtime-construction candidate, and
the Newton shape runtime-construction contract now records exactly one repo-local
`NewtonShapeMapping.to_dict()` mapping record while keeping Newton engine shape objects, builder
shape calls, and Newton execution at zero. The Newton shape runtime builder-preflight contract now
records exactly one JSON-safe future box builder call plan while keeping builder calls, Newton
engine shape objects, and Newton execution at zero. The Newton shape runtime
builder-construction contract now records one JSON-safe repo-local recording-builder
`add_shape_box` call artifact while keeping real Newton imports, Newton `ModelBuilder`
instantiation, Newton engine shape objects, real Newton builder shape calls, and Newton execution
at zero. The Newton engine-builder boundary-preflight contract now records one offline/static
future-boundary checklist row for that same call artifact while keeping real Newton imports,
`newton.ModelBuilder` instantiation, real builder shape calls, model finalization, collision
pipeline calls, and Newton execution at zero. The Newton engine-builder environment-probe contract
now records configured-source-dir status and JSON-safe Newton/Warp `find_spec` provenance shape
while keeping real runtime imports and Newton execution at zero. The next implementation slice
should keep the same boundary discipline:

1. Implement `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract`
   after the bounded environment-probe row exists.
2. Keep the constructed runtime `PrimitiveSpec` object, preflight candidate, generated
   `CollisionPackage.to_dict()` artifact, runtime-admissibility preflight row, static
   runtime-admissibility row, shape-mapping preflight row, static descriptor row, static
   Newton shape runtime-boundary preflight row, repo-local shape mapping record, and
   builder-preflight call-plan, recording-builder call, engine-builder boundary-preflight, and
   environment-probe records
   synthetic/report-scoped until a separate
   Newton-runtime gate exists.
3. Keep the report partial and keep `paper_faithful_offline_supported: false` until a later dated
   record documents stronger offline mechanics.
4. Keep Newton execution, bed, Franka, real-USD evaluation, benchmark work, and collision-quality
   claims out of scope until a separate dated mapped-subset runtime record says what may be mapped
   and checked.
