# Claim Boundaries

This file is the source of truth for reviewer-facing claims. If a stronger claim becomes
necessary, add the evidence requirement here before using it in the DeepDive package.

## Allowed Current Claims

- The repository is a DeepDive-first proposal and bootstrap, not a completed compiler.
- The intended direction is primitive-first, Newton-checker-planned, fallback-aware collision
  asset generation for Newton workflows, with named Newton diagnostic records required for any
  simulation-checked wording.
- The first proof point is diagnostic: measure whether primitive collision contracts expose
  failures that mesh-only or visual-only asset review would miss.
- The Physical Intelligence Center story is that AI models need physical safety constraints;
  physics engines provide an executable diagnostic layer for those constraints.
- The current code defines installable package contracts, config loading, dry-run reporting, USD
  asset-open smoke diagnostics, Newton source import diagnostics, and environment-readiness
  diagnostics.
- The current code can materialize manifest USD assets into ignored repo-local
  `assets/raw/mirrors/` paths and prefer those local paths at runtime when present. Current bed
  materialization records the material/texture closure; current Franka materialization records a
  USD layer mirror with unresolved `OmniPBR.mdl`. This is asset intake and reproducibility
  diagnostics, not benchmark evidence, collision-quality validation, compiler completeness,
  complete visual/material packaging, or deployment readiness.
- The current code can run a geometry-only CPD-like face-merge primitive proposal smoke path for
  a restricted primitive subset, when tied to a dated record and capped asset/config settings.
- The current code can run an opt-in geometry-only CPD-like component-merge gate that reports
  disconnected-component merge candidates and normalized excess-volume accounting for a restricted
  baseline. This is not full CPD paper reproduction or collision-quality evidence.
- The current code can run an offline paper-aligned surrogate objective report over a CPD-like
  decomposition. This reports primitive-budget pressure, AABB-normalized volume proxy,
  merge-excess accounting, assigned-point containment proxy, unsupported paper primitive gaps, and
  component/fallback labels. This is not full CPD paper reproduction, paper-faithful optimization,
  benchmark evidence, or collision-quality validation. "Paper-aligned" means design-aligned with
  the paper story's accounting categories, not the paper's collapse-cost rule, primitive
  weighting, or search procedure.
- The current objective report can include structured Eq.4 alignment metadata that maps current
  surrogate merge-excess fields to the CPD paper's collapse-cost role for audit. This is metadata,
  not Eq.4 implementation, paper-faithful scoring, benchmark evidence, or collision-quality
  validation.
- The documentation can define a planned `paper_faithful_offline` status for future
  fixture-scoped paper mechanics. That status is not currently supported by code. When implemented,
  it may only describe the declared offline fixture scope and must remain separate from full CPD
  paper reproduction, Newton runtime support, benchmark evidence, collision-quality validation,
  deployment readiness, or safety certification.
- The current code can run a command-only partial `cpd_paper_offline_report` over
  `paper_single_box`, `paper_two_face_merge`, `paper_three_face_chain`,
  `paper_disconnected_components`, `paper_component_pair_threshold_blocked`,
  `paper_tiny_sphere_clamp`, `paper_duplicate_vertex_preprocessing`, `paper_frustum_like`,
  `paper_trapezoid_prism_like`, `paper_nested_primitive`, `paper_quad_face_intake`, and
  `paper_polygon_face_intake` synthetic fixtures. It reports triangle-only mesh intake,
  fan-triangulated quad/polygon source-face intake policy, paper-side operator audit fields,
  offline paper-shaped OBB/sphere fit-audit rows, an offline paper-shaped capsule axis fit-audit
  row, offline-only flat-capped-cylinder, frustum, and trapezoidal-prism fit-audit candidate rows,
  separate paper base collapse-cost versus weighted-priority-cost fields, a topology-only
  priority-queue trace with eager stale-pruning records, a threshold-disabled component-pair
  insertion trace, a finite-threshold component-pair blocked trace, and one explicit identity-axis
  OBB enclosed-primitive postprocess cull audit. It also reports one exact-coordinate
  duplicate-vertex preprocessing fixture with before/after vertex counts, source-face remap,
  topology-change accounting, and a topology trace over the deduplicated executable mesh. The
  report now also includes a `paper_faithful_offline_scope_audit` criteria table with
  `decision: remain_partial`, non-blocking package/Newton/real-USD/benchmark boundary rows, and
  prior scope-audit gate `paper_fixture_breadth_expansion_plan`; later fixture-breadth slices below
  close only the planned Batch A-E breadth gate, and the command-only generalization planning table
  advances the current report gate to `paper_generalization_batch_a_source_policy`. The report now
  also closes only that source-policy gate with an offline source-policy matrix. At that
  source-policy stage the follow-up gate was
  `paper_generalization_batch_b_primitive_fit_engine`. The report now also closes only that
  primitive-fit engine gate with an offline matrix over deterministic in-memory
  probes for all six paper primitive names. The report now also closes only the search-engine gate
  with an offline search-trace matrix and at that stage advanced the next gate to
  `paper_generalization_batch_d_postprocess_policy`. The report now also closes only that
  postprocess-policy gate with an offline matrix over existing deterministic postprocess audit
  fixtures and at that stage advanced the next gate to
  `paper_generalization_batch_e_package_boundary_readiness`. The report now also closes only that
  package-boundary readiness gate with an offline package-boundary readiness matrix before package
  conversion and at that stage advanced the next gate to
  `paper_offline_changed_decomposition_output_contract`. The report now also closes only that
  output-contract gate with an offline changed-decomposition output contract, not a
  `CollisionPackage`. The report now also closes only `paper_package_adapter_contract` with a
  command-only offline package-adapter contract, not a `CollisionPackage`. The report now also
  closes only `paper_package_adapter_unsupported_primitive_policy` with a command-only offline
  unsupported-primitive policy table, not a `CollisionPackage`. The report now also closes only
  `paper_package_conversion_mapped_subset_plan` with a command-only offline mapped-subset planning
  table, not a `CollisionPackage`. The report now also closes only
  `paper_mapped_subset_conversion_candidate_matrix` with a command-only offline candidate matrix,
  not a `CollisionPackage`, and at that stage advanced the next gate to
  `paper_mapped_subset_adapter_preflight_contract`. The report now also closes only
  `paper_mapped_subset_adapter_preflight_contract` with a command-only offline adapter-preflight
  contract, not `PrimitiveSpec` generation and not a `CollisionPackage`; that closed gate led to
  the later `paper_mapped_subset_primitivespec_dry_run_contract` gate. The report now also closes
  only `paper_mapped_subset_primitivespec_dry_run_contract` with a command-only offline
  PrimitiveSpec dry-run contract, not real `PrimitiveSpec` generation and not a
  `CollisionPackage`; that closed gate led to the later
  `paper_mapped_subset_primitivespec_validation_contract` gate. The report now also closes only
  `paper_mapped_subset_primitivespec_validation_contract` with a command-only offline
  validation contract, not real `PrimitiveSpec` generation and not a `CollisionPackage`, and
  now also closes only `paper_mapped_subset_primitivespec_generation_preflight_contract` with a
  command-only offline generation-preflight contract, not real `PrimitiveSpec` generation and not
  a `CollisionPackage`; that closed gate led to the later
  `paper_mapped_subset_primitivespec_generation_contract` gate. The report now also closes only
  `paper_mapped_subset_primitivespec_generation_contract` with a command-only offline generation
  contract that emits future native-family template rows, not runtime `PrimitiveSpec` objects and
  not a `CollisionPackage`. The report now also closes only
  `paper_mapped_subset_primitivespec_candidate_source_contract` with a command-only offline
  candidate-source audit that classifies future templates separately from current rows, records
  zero eligible current PrimitiveSpec candidate sources, and led to the later
  `paper_mapped_subset_native_current_fixture_contract` gate. Later native-current and
  native-fixture PrimitiveSpec-like dict generation, serialization, and runtime-boundary preflight
  gates remain offline/report-only. The runtime-construction gate constructs exactly one runtime
  `PrimitiveSpec` object from the deterministic synthetic `paper_single_box` OBB/box preflight JSON
  after checking the runtime-boundary preflight row's canonical JSON SHA-256 fingerprint, and stores
  only `PrimitiveSpec.to_dict()` in the report. The collision-package generation preflight gate
  then records one later package-generation candidate while still creating zero CollisionPackages.
  The collision-package generation gate then constructs exactly one synthetic, report-scoped
  `CollisionPackage.to_dict()` artifact for the same `paper_single_box` OBB/box row, records
  `generated_collision_package_count: 1`, keeps runtime-admissibility checks at zero, and advances
  the next gate at that stage to `paper_mapped_subset_runtime_admissibility_preflight_contract`.
  The runtime-admissibility preflight gate then consumes that one synthetic package artifact,
  records one later runtime-admissibility candidate row without copying the full package dict,
  keeps runtime-admissibility checks at zero, and advances the next gate at that stage to
  `paper_mapped_subset_runtime_admissibility_contract`. The runtime-admissibility contract then
  records one offline/static finite-geometry and box-schema check for that same synthetic package,
  keeps Newton shape mapping and Newton execution at zero, and advances the next gate at that
  stage to `paper_mapped_subset_newton_shape_mapping_preflight_contract`. The Newton
  shape-mapping preflight contract then records one offline/static mapper-handoff row for the same
  synthetic box dict, keeps mapping attempts, Newton mapping records, and Newton execution at
  zero, and advances the next gate at that stage to
  `paper_mapped_subset_newton_shape_mapping_contract`. The Newton shape-mapping contract then
  records one offline/static report-scoped descriptor dict for the same synthetic box dict, keeps
  mapping attempts, Newton mapping records, Newton shape objects, and Newton execution at zero. The
  later Newton shape runtime-boundary preflight contract then records one later
  runtime-construction candidate and advances that stage to
  `paper_mapped_subset_newton_shape_runtime_construction_contract`. The Newton shape
  runtime-construction contract then consumes that runtime-boundary candidate and records exactly
  one repo-local `NewtonShapeMapping.to_dict()` mapping record for the synthetic
  `paper_single_box` box descriptor, with zero Newton mapper calls, zero Newton engine shape
  objects, zero builder shape calls, and zero Newton runtime executions. The builder-preflight
  contract then records exactly one JSON-safe future box builder call plan while still allowing
  zero builder calls, creating zero Newton engine shape objects, and running zero Newton code. It
  led to the builder-construction gate. The builder-construction contract then records one
  JSON-safe repo-local recording-builder `add_shape_box` call artifact while still importing no
  real Newton runtime, instantiating no `newton.ModelBuilder`, creating zero Newton engine shape
  objects, making zero real Newton builder shape calls, and running zero Newton code. The
  following engine-builder boundary-preflight contract records one future-boundary checklist row
  while still importing no real Newton runtime, instantiating no `newton.ModelBuilder`, making no
  real builder calls, finalizing no model, creating no collision pipeline, and running zero Newton
  code. The environment-probe contract then records configured-source-dir status and JSON-safe
  Newton/Warp `find_spec` provenance shape while keeping runtime imports and execution out of
  scope. The API-surface contract then records default no-config source-AST API-surface status
  while keeping real runtime imports, `newton.ModelBuilder`, real builder calls, model
  finalization, collision pipeline calls, and runtime execution at zero. The entry contract then
  records a report-only default no-runtime-entry decision for the same synthetic box lineage,
  keeps real runtime imports, `newton.ModelBuilder`, real builder calls, model finalization,
  collision pipeline calls, and runtime execution at zero. The smoke contract then records a
  report-only `skip_real_runtime_smoke` decision for that same lineage, keeps real runtime-smoke
  attempts and Newton execution at zero. The runtime-execution contract then records a
  report-only `skip_real_runtime_execution` decision for that same lineage, keeps real
  runtime-execution attempts and Newton execution at zero. The runtime-lane review contract then
  records a report-only claim-boundary review for that skipped-runtime-execution row, keeps
  runtime compatibility unvalidated, keeps all real runtime counters at zero, and advances the
  stage-local next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract`.
  The configured-runtime design contract then records report-only runtime input requirements for
  that same lineage, keeps runtime config validation false, keeps all real runtime counters at
  zero, and advances the stage-local next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract`.
  The configured-runtime preflight contract then records the bounded preflight row for that same
  lineage, keeps runtime config validation false, keeps runtime source/device resolution false,
  keeps all real runtime counters at zero, and at that stage advanced the next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_validation_contract`.
  The configured-runtime validation contract then records the default missing-config validation
  result for that same lineage, reads no config file or environment, keeps runtime source/device
  resolution false, keeps all real runtime counters at zero, and at that stage advanced the next
  gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract`.
  The configured-runtime source-resolution contract then records the default missing-source
  resolution result for that same lineage, performs no filesystem probe, keeps runtime
  source/device resolution false, keeps all real runtime counters at zero, and at that stage
  advanced the next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract`.
  The configured-runtime device-resolution contract then records the default missing-device
  resolution result for that same lineage, creates no runtime device object, keeps runtime
  source/device resolution false, keeps all real runtime counters at zero, and at that stage
  advanced the next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract`.
  The configured-runtime entry-decision contract then records the default no-runtime-entry decision
  for that same lineage, keeps runtime entry allowed/attempted/passed false, keeps all real runtime
  counters at zero, and advances the current next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract`.
  The entry gate is a consolidation boundary, not an extra claim. It combines the remaining
  import-boundary preconditions and the first Newton entry decision into one audit point instead
  of adding separate import-preflight and import-contract gates.
  The
  report remains `status: partial` with
  `paper_faithful_offline_supported: false`. This is fixture-scoped offline audit data for exact
  overlaps and scope accounting only, not nonzero-threshold mesh cleanup, not
  `paper_faithful_offline`, not full CPD paper reproduction, not Newton runtime support, not
  runtime admissibility, not real-USD evidence, not benchmark evidence, not collision-quality
  validation, and not paper primitive vocabulary coverage.
- The documentation can define a fixture-breadth expansion plan for the nine blocking
  scope-audit rows. The plan is a planning artifact for future batches; implemented evidence must
  still come from code, tests, and dated records. The plan alone does not support
  `paper_faithful_offline`, package generation, Newton runtime, real-USD, benchmark,
  collision-quality, deployment, or safety evidence.
- The partial `cpd_paper_offline_report` includes the Batch A source/preprocess/intake/operator
  fixture-breadth cases: `paper_mixed_face_preprocess_operator`,
  `paper_degenerate_preprocess_face_drop`, and `paper_concave_polygon_rejected`. This is an
  intermediate synthetic offline fixture-accounting slice; later fixture-breadth batches advance
  the current report gate beyond Batch A. It does not support broad mesh cleanup, general
  polygon intake, `paper_faithful_offline`, full CPD reproduction, package generation, Newton
  runtime support, real-USD evidence, benchmark evidence, collision-quality validation,
  deployment readiness, or safety certification.
- The partial `cpd_paper_offline_report` includes the Batch B primitive-fit fixture-breadth cases:
  `paper_rotated_box_fit`, `paper_offset_sphere_fit`, `paper_off_axis_capsule_fit`,
  `paper_flat_capped_cylinder_axis_fit`, `paper_tapered_frustum_fit`, and
  `paper_asymmetric_trapezoid_fit`. This is synthetic offline primitive-fit fixture accounting
  only. It does not support `paper_faithful_offline`, full CPD reproduction, package generation,
  Newton runtime support, real-USD evidence, benchmark evidence, collision-quality validation,
  deployment readiness, or safety certification.
- The partial `cpd_paper_offline_report` includes the Batch C cost/search/stop fixture-breadth
  cases: `paper_branching_cost_order`, `paper_equal_cost_queue_tie`, and
  `paper_nonzero_threshold_block`. This is synthetic offline cost/search/threshold-stop accounting
  only, including one component-pair positive finite threshold block. It does not support
  `paper_faithful_offline`, full CPD reproduction, package generation, Newton runtime support,
  real-USD evidence, benchmark evidence, collision-quality validation, deployment readiness, or
  safety certification.
- The partial `cpd_paper_offline_report` includes the Batch D component-pair fixture-breadth cases:
  `paper_component_pair_multi_candidate_order` and `paper_component_pair_cap_skipped`. This is
  synthetic offline component-pair candidate ordering and skipped-pair accounting only. It does not
  support `paper_faithful_offline`, full CPD reproduction, package generation, Newton runtime
  support, real-USD evidence, benchmark evidence, collision-quality validation, deployment
  readiness, or safety certification.
- The partial `cpd_paper_offline_report` includes the Batch E postprocess fixture-breadth cases:
  `paper_rotated_nested_primitive` and `paper_cross_type_enclosure_boundary`. This is synthetic
  offline rotated OBB containment and unsupported cross-type no-cull accounting only. It does not
  support `paper_faithful_offline`, full CPD reproduction, package generation, Newton runtime
  support, real-USD evidence, benchmark evidence, collision-quality validation, deployment
  readiness, or safety certification.
- The partial `cpd_paper_offline_report` includes a command-only synthetic fixture-breadth
  completion review for planned Batches A-E. It closes only `paper_fixture_breadth_expansion`,
  keeps `paper_faithful_offline_supported: false`, and records the planning-only
  `paper_faithful_offline_generalization_plan` as the follow-up gate for that closed review. That
  nested follow-up gate is planning-only for broadening the offline algorithm beyond named toy
  fixtures; it is not `paper_faithful_offline` support. This review does not support
  `paper_faithful_offline`, full CPD reproduction, package generation, Newton runtime support,
  real-USD evidence, benchmark evidence, collision-quality validation, deployment readiness, or
  safety certification.
- The partial `cpd_paper_offline_report` includes a command-only offline generalization planning
  table. It closes only `paper_faithful_offline_generalization_plan`, keeps
  `paper_faithful_offline_supported: false`, and now reports the first unresolved runtime-lane
  gate as
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract`
  after the
  source-policy,
  primitive-fit engine, search-engine, postprocess-policy, package-boundary readiness, offline
  changed-decomposition output contract, offline package-adapter contract, offline
  unsupported-primitive policy, mapped-subset planning, candidate-matrix, adapter-preflight,
  PrimitiveSpec dry-run, PrimitiveSpec validation, PrimitiveSpec generation-preflight,
  PrimitiveSpec generation-contract, candidate-source-contract, native-current-fixture,
  native-fixture PrimitiveSpec-like dict generation, native-fixture serialization, and
  runtime-boundary preflight, runtime-construction, collision-package generation preflight,
  collision-package generation, runtime-admissibility preflight, and offline/static
  runtime-admissibility contract, offline/static Newton shape-mapping preflight, offline/static
  Newton shape-mapping descriptor, offline/static Newton shape runtime-boundary preflight,
  offline/report-scoped Newton shape runtime-construction, offline/static Newton shape runtime
  builder-preflight, offline/report-only Newton shape runtime recording-builder construction, and
  offline/static Newton engine-builder boundary-preflight, bounded Newton/Warp environment-probe,
  bounded source-AST API-surface, report-only engine-builder entry, report-only skipped-smoke,
  report-only skipped-runtime-execution, report-only runtime-lane review, report-only
  configured-runtime design/preflight/validation/source-resolution/device-resolution/entry-decision
  slices.
- The partial `cpd_paper_offline_report` now includes
  `paper_generalization_batch_a_source_policy`, an offline report-only source-policy matrix for
  deterministic synthetic meshes. It records exact-coordinate dedup policy, source-face
  intake/remap policy, concave-polygon rejection, and source-face `Q` aggregation accounting. At
  that source-policy stage the follow-up gate was
  `paper_generalization_batch_b_primitive_fit_engine`. It is not robust
  mesh cleanup, general polygon intake, package generation, Newton runtime execution, real-USD
  asset evidence, benchmark evidence, `paper_faithful_offline` support, full CPD reproduction,
  collision-quality evidence, deployment readiness, or safety certification.
- The partial `cpd_paper_offline_report` now includes
  `paper_generalization_batch_b_primitive_fit_engine`, an offline report-only primitive-fit engine
  matrix over deterministic in-memory probes for all six paper primitive names. It records
  candidate generation, selected-candidate accounting, containment checks, finite numeric fields,
  and the offline-only boundary for paper-only primitives. It is not robust primitive fitting,
  package generation, Newton runtime execution, real-USD asset evidence, benchmark evidence,
  `paper_faithful_offline` support, full CPD reproduction, collision-quality evidence, deployment
  readiness, or safety certification.
- The partial `cpd_paper_offline_report` now includes
  `paper_generalization_batch_c_search_engine`, an offline report-only search-trace matrix over
  existing deterministic topology queue, weighted-priority, equal-cost tie, threshold-stop, and
  component-pair traces. It closes only that search-engine gate and advances the next gate to
  `paper_generalization_batch_d_postprocess_policy`. It is not a generalized optimizer, package
  generation, Newton runtime execution, real-USD asset evidence, benchmark evidence,
  `paper_faithful_offline` support, full CPD reproduction, collision-quality evidence, deployment
  readiness, or safety certification.
- The partial `cpd_paper_offline_report` now includes
  `paper_generalization_batch_d_postprocess_policy`, an offline report-only postprocess-policy
  matrix over existing deterministic postprocess audit fixtures. It records identity-axis OBB
  culling, rotated OBB culling, conservative unsupported cross-type no-cull accounting,
  before/after primitive counts, cull or unsupported reasons, and false package, Newton, real-USD,
  and benchmark triggers. It closes only that postprocess-policy gate and at that stage advanced
  the next gate to `paper_generalization_batch_e_package_boundary_readiness`. It is not a general
  primitive containment library, package generation, Newton runtime execution, real-USD asset evidence,
  benchmark evidence, `paper_faithful_offline` support, full CPD reproduction,
  collision-quality evidence, deployment readiness, or safety certification.
- The partial `cpd_paper_offline_report` now includes
  `paper_generalization_batch_e_package_boundary_readiness`, an offline report-only
  package-boundary readiness matrix before package conversion. It records that the current
  source-policy, primitive-fit, search-engine, and postprocess-policy outputs are audit matrices
  rather than a durable changed-decomposition output contract. It closes only that
  package-boundary readiness gate and advances the next gate to
  `paper_offline_changed_decomposition_output_contract`. It is not package readiness, Newton
  readiness, package generation, Newton runtime execution, real-USD asset evidence, benchmark
  evidence, `paper_faithful_offline` support, full CPD reproduction, collision-quality evidence,
  deployment readiness, or safety certification.
- The partial `cpd_paper_offline_report` now includes
  `paper_offline_changed_decomposition_output_contract`, an offline changed-decomposition output
  contract, not a `CollisionPackage`. It records synthetic toy fixture decomposition rows, stable
  offline primitive ids, source-face/group ids, selected paper primitive audit fields, explicit
  postprocess state rows, unsupported runtime boundaries, and package/Newton/real-USD/benchmark
  false triggers. It closes only that output-contract gate and advances the next gate to
  `paper_package_adapter_contract`. It is not package readiness, Newton readiness, package
  generation, Newton runtime execution, real-USD asset evidence, benchmark evidence,
  `paper_faithful_offline` support, full CPD reproduction, collision-quality evidence, deployment
  readiness, or safety certification.
- The partial `cpd_paper_offline_report` now includes `paper_package_adapter_contract`, a
  command-only offline package-adapter contract, not a `CollisionPackage`. It consumes the offline
  changed-decomposition primitive records as adapter input rows, emits 16 adapter decision rows,
  classifies all current `trapezoidal_prism` / `offline_only_unmapped` records as
  `later_policy_required`. At that adapter-contract stage the follow-up gate was
  `paper_package_adapter_unsupported_primitive_policy`; after the unsupported-primitive policy the
  follow-up gate was `paper_package_conversion_mapped_subset_plan`, which is now closed by the
  mapped-subset planning table below. It
  is not package readiness, Newton
  readiness, runtime admissibility, package generation, Newton runtime execution, real-USD asset
  evidence, benchmark evidence, `paper_faithful_offline` support, full CPD reproduction,
  collision-quality evidence, deployment readiness, or safety certification.
- The partial `cpd_paper_offline_report` now includes
  `paper_package_adapter_unsupported_primitive_policy`, a command-only offline unsupported-primitive
  policy table, not a `CollisionPackage`. It classifies all six paper primitive families, keeps
  the current 16 `trapezoidal_prism` / `offline_only_unmapped` rows offline with
  `block_package_conversion`, records zero package-candidate rows, and advances the next gate to
  `paper_package_conversion_mapped_subset_plan` at that unsupported-policy stage. It is not
  package readiness, Newton readiness,
  runtime admissibility, approximation support, package generation, Newton runtime execution,
  real-USD asset evidence, benchmark evidence, `paper_faithful_offline` support, full CPD
  reproduction, collision-quality evidence, deployment readiness, or safety certification.
- The partial `cpd_paper_offline_report` now includes
  `paper_package_conversion_mapped_subset_plan`, a command-only offline mapped-subset
  package-conversion planning table, not a `CollisionPackage`. It identifies
  `oriented_bounding_box`, `sphere`, and `capsule` as native-family review rows, keeps the
  current 16 `trapezoidal_prism` / `offline_only_unmapped` rows offline, records zero current
  package-conversion candidates, and at that stage advanced the next gate to
  `paper_mapped_subset_conversion_candidate_matrix`. It is not package readiness, Newton
  readiness, runtime admissibility, approximation support, package generation, Newton runtime
  execution, real-USD asset evidence, benchmark evidence, `paper_faithful_offline` support, full
  CPD reproduction, collision-quality evidence, deployment readiness, or safety certification.
- The partial `cpd_paper_offline_report` includes
  `paper_mapped_subset_native_current_fixture_contract`, a command-only offline native-current
  fixture source contract, not real `PrimitiveSpec` generation and not a `CollisionPackage`. It
  records exactly one synthetic `paper_single_box` selected OBB/box source row traced to the OBB
  template, one eligible current candidate source, one report-only PrimitiveSpec generation
  candidate, zero generated PrimitiveSpecs, zero generated CollisionPackages, and zero
  runtime-admissibility checks. It led to the later
  `paper_mapped_subset_primitivespec_native_fixture_generation_contract` gate. It is not package
  readiness, Newton readiness, runtime admissibility, approximation support, `PrimitiveSpec`
  readiness, real PrimitiveSpec generation, CollisionPackage generation, package generation,
  Newton runtime execution, real-USD asset evidence, benchmark evidence,
  `paper_faithful_offline` support, full CPD reproduction, collision-quality evidence, deployment
  readiness, or safety certification.
- The partial `cpd_paper_offline_report` now includes
  `paper_mapped_subset_primitivespec_native_fixture_generation_contract`, a command-only offline
  native-fixture PrimitiveSpec-like dict generation contract, not real runtime `PrimitiveSpec`
  object creation and not a `CollisionPackage`. It emits exactly one JSON-serializable,
  report-only PrimitiveSpec-like dict for the deterministic synthetic `paper_single_box` OBB/box
  source row, keeps generated runtime PrimitiveSpecs, generated CollisionPackages,
  runtime-admissibility checks, Newton runtime execution, real-USD asset evidence, benchmark
  evidence, collision-quality measurement, deployment, and certification triggers at zero or
  false, and led to the later serialization gate. The partial report now also includes
  `paper_mapped_subset_primitivespec_native_fixture_serialization_contract`, a command-only
  offline JSON serialization/schema-stability contract for that one report-only dict. It validates
  strict canonical JSON and round-trip equality, keeps runtime/package/Newton/evaluation triggers
  false, and advances the next gate to
  `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`. The partial report now
  also includes `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`, a
  command-only offline boundary preflight for that one report-only dict. It records one later
  runtime `PrimitiveSpec` construction candidate, keeps runtime construction disallowed in the
  current gate, keeps runtime/package/Newton/evaluation triggers false, and advances the next gate
  to `paper_mapped_subset_primitivespec_runtime_construction_contract`. The partial report now also
  includes `paper_mapped_subset_primitivespec_runtime_construction_contract`, a single-fixture
  offline runtime-construction contract. It constructs exactly one runtime `PrimitiveSpec` object
  from the canonical `paper_single_box` OBB/box preflight JSON after checking the runtime-boundary
  preflight row's canonical JSON SHA-256 fingerprint, stores only `PrimitiveSpec.to_dict()` in the
  JSON report, records runtime PrimitiveSpec generation counts as one, keeps
  runtime/package/Newton/evaluation triggers false, and advances the next gate to
  `paper_mapped_subset_collision_package_generation_preflight_contract`. It is not package
  readiness, Newton readiness, runtime admissibility, approximation support, general
  `PrimitiveSpec` readiness, CollisionPackage generation, package generation, Newton runtime
  execution, real-USD asset evidence, benchmark evidence, `paper_faithful_offline` support, full
  CPD reproduction, collision-quality evidence, deployment readiness, or safety certification.
  The partial report now also includes
  `paper_mapped_subset_collision_package_generation_preflight_contract`, a single-fixture offline
  package-generation preflight contract. It consumes that `PrimitiveSpec.to_dict()` payload,
  records exactly one later package-generation candidate, keeps package generation disallowed in
  the current gate, keeps generated CollisionPackages and runtime-admissibility checks at zero,
  and advances the next gate to `paper_mapped_subset_collision_package_generation_contract`. It is
  not package readiness, Newton readiness, runtime admissibility, approximation support,
  CollisionPackage generation, Newton runtime execution, real-USD asset evidence, benchmark
  evidence, `paper_faithful_offline` support, full CPD reproduction, collision-quality evidence,
  deployment readiness, or safety certification.
- The partial `cpd_paper_offline_report` now includes
  `paper_mapped_subset_collision_package_generation_contract`, a single-fixture offline
  CollisionPackage generation contract. It consumes the package-generation preflight row,
  constructs exactly one synthetic, report-scoped `CollisionPackage.to_dict()` artifact for the
  deterministic `paper_single_box` OBB/box row, records
  `generated_collision_package_count: 1`, keeps runtime-admissibility checks at zero, records
  only `box` as the evaluated fixture primitive family in this gate, and advances the next gate to
  `paper_mapped_subset_runtime_admissibility_preflight_contract`. It is not package readiness,
  Newton readiness, Newton support, runtime admissibility, paper primitive vocabulary coverage,
  approximation support, general `PrimitiveSpec` readiness, Newton runtime execution, real-USD asset evidence,
  benchmark evidence, `paper_faithful_offline` support, full CPD reproduction, collision-quality
  evidence, deployment readiness, or safety certification.
- The partial `cpd_paper_offline_report` now includes
  `paper_mapped_subset_runtime_admissibility_preflight_contract`, a single-fixture offline
  runtime-admissibility preflight contract. It consumes the one synthetic `paper_single_box`
  `CollisionPackage.to_dict()` artifact, validates identity, source metadata, schema, primitive
  subset, and false trigger flags, records exactly one later runtime-admissibility candidate row
  without copying the full package dict, keeps runtime-admissibility checks at zero, and advances
  the next gate to `paper_mapped_subset_runtime_admissibility_contract`. It is not package
  readiness, Newton readiness, Newton support, runtime admissibility, paper primitive vocabulary coverage,
  approximation support, general `PrimitiveSpec` readiness, Newton runtime execution, real-USD
  asset evidence, benchmark evidence, `paper_faithful_offline` support, full CPD reproduction,
  collision-quality evidence, deployment readiness, or safety certification.
- The partial `cpd_paper_offline_report` now includes
  `paper_mapped_subset_runtime_admissibility_contract`, a single-fixture offline/static
  runtime-admissibility contract. It consumes the runtime-admissibility preflight row for the one
  synthetic `paper_single_box` OBB/box `CollisionPackage.to_dict()` artifact and records one
  report-only static check for finite center, right-handed orthonormal axes, positive box half
  extents, target box dimension schema, expected source faces, containment flag, and positive
  volume accounting. It advances the runtime-lane next gate to
  `paper_mapped_subset_newton_shape_mapping_preflight_contract` while keeping Newton shape
  mapping, Newton runtime execution, real-USD asset evidence, benchmark evidence,
  collision-quality evidence, deployment, and certification triggers at zero or false. It is not
  package readiness, Newton readiness, Newton support, Newton execution, real-USD evidence,
  benchmark evidence, collision-quality validation, paper primitive vocabulary coverage,
  approximation support, `paper_faithful_offline` support, full CPD reproduction, deployment
  readiness, or safety certification.
- The partial `cpd_paper_offline_report` now includes
  `paper_mapped_subset_newton_shape_mapping_preflight_contract`, a single-fixture offline/static
  Newton shape-mapping preflight contract. It consumes the runtime-admissibility row for the same
  synthetic `paper_single_box` OBB/box artifact and records one static mapper-handoff row with
  target kind `box`, field-transfer checks, `mapping_attempt_count: 0`,
  `newton_mapping_record_count: 0`, and `newton_runtime_execution_count: 0`. It advances the
  runtime-lane next gate to `paper_mapped_subset_newton_shape_mapping_contract` while keeping
  Newton support claims, Newton shape mapping, Newton runtime execution, real-USD asset evidence,
  benchmark evidence, collision-quality evidence, deployment, and certification triggers at zero
  or false. It is not Newton readiness, Newton support, Newton execution, real-USD evidence,
  benchmark evidence, collision-quality validation, paper primitive vocabulary coverage,
  approximation support, `paper_faithful_offline` support, full CPD reproduction, deployment
  readiness, safety certification, or general package readiness.
- The partial `cpd_paper_offline_report` now includes
  `paper_mapped_subset_newton_shape_mapping_contract`, a single-fixture offline/static Newton
  shape descriptor contract. It consumes the shape-mapping preflight row for the same synthetic
  `paper_single_box` OBB/box artifact and records exactly one report-scoped
  `newton_shape_descriptor_dict` for target kind `box`, with `mapping_attempt_count: 0`,
  `newton_mapping_record_count: 0`, `newton_shape_object_count: 0`, and
  `newton_runtime_execution_count: 0`. It advances the runtime-lane next gate to
  `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract` while keeping Newton
  support claims, real Newton shape mapping, Newton shape object creation, Newton runtime
  execution, real-USD asset evidence, benchmark evidence, collision-quality evidence, deployment,
  and certification triggers at zero or false. It is not Newton readiness, Newton support, Newton
  execution, real-USD evidence, benchmark evidence, collision-quality validation, paper primitive
  vocabulary coverage, approximation support, `paper_faithful_offline` support, full CPD
  reproduction, deployment readiness, safety certification, or general package readiness.
- The partial `cpd_paper_offline_report` now includes
  `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`, a single-fixture
  offline/static Newton shape runtime-boundary preflight contract. It consumes the static
  descriptor row for the same synthetic `paper_single_box` OBB/box artifact and records exactly
  one later Newton shape runtime-construction candidate with `mapping_attempt_count: 0`,
  `newton_mapping_record_count: 0`, `newton_shape_object_count: 0`, and
  `newton_runtime_execution_count: 0`. It advances the runtime-lane next gate to
  `paper_mapped_subset_newton_shape_runtime_construction_contract` while keeping Newton support
  claims, real Newton shape mapping, Newton shape object creation, Newton runtime execution,
  real-USD asset evidence, benchmark evidence, collision-quality evidence, deployment, and
  certification triggers at zero or false. It is not Newton readiness, Newton support, Newton
  execution, real-USD evidence, benchmark evidence, collision-quality validation, paper primitive
  vocabulary coverage, approximation support, `paper_faithful_offline` support, full CPD
  reproduction, deployment readiness, safety certification, or general package readiness.
- The partial `cpd_paper_offline_report` now includes
  `paper_mapped_subset_newton_shape_runtime_construction_contract`, a single-fixture
  offline/report-scoped Newton shape runtime-construction contract. It consumes the
  runtime-boundary candidate and records exactly one repo-local `NewtonShapeMapping.to_dict()`
  mapping record for the synthetic `paper_single_box` box descriptor, with zero Newton mapper
  calls, zero Newton engine shape objects, zero builder shape calls, and zero Newton runtime
  executions. It advances the runtime-lane next gate to
  `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract` while keeping Newton
  support, real Newton shape object construction, Newton execution, USD, benchmark,
  collision-quality, `paper_faithful_offline`, deployment, and safety claims unsupported.
- The partial `cpd_paper_offline_report` now includes
  `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`, a single-fixture
  offline/static Newton shape runtime builder-preflight contract. It consumes the repo-local
  `NewtonShapeMapping.to_dict()` mapping record, records exactly one JSON-safe future box builder
  call plan with signature fields `body`, `xform`, `hx`, `hy`, and `hz`, keeps builder calls,
  Newton engine shape object construction, and Newton execution at zero, and advances the
  runtime-lane next gate to
  `paper_mapped_subset_newton_shape_runtime_builder_construction_contract` while keeping Newton
  support, real Newton shape object construction, Newton execution, USD, benchmark,
  collision-quality, `paper_faithful_offline`, deployment, and safety claims unsupported.
- The partial `cpd_paper_offline_report` now includes
  `paper_mapped_subset_newton_shape_runtime_builder_construction_contract`, a single-fixture
  offline/report-only Newton shape runtime recording-builder construction contract. It consumes
  that builder-preflight row, records one JSON-safe fake `add_shape_box` call artifact through the
  repo-local static shape helper, keeps real Newton imports, Newton `ModelBuilder`
  instantiation, Newton engine shape object construction, real Newton builder shape calls, and
  Newton execution at zero, and advances the runtime-lane next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract` while
  keeping Newton support, real Newton shape object construction, Newton execution, USD,
  benchmark, collision-quality, `paper_faithful_offline`, deployment, and safety claims
  unsupported.
- The partial `cpd_paper_offline_report` now includes
  `paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract`, a
  single-fixture offline/static Newton engine-builder boundary preflight contract. It consumes the
  repo-local recording-builder artifact, records the future real `newton.ModelBuilder` /
  `add_shape_box` boundary requirements and provenance checks needed before an environment probe,
  keeps real Newton imports, Newton `ModelBuilder` instantiation, real Newton builder shape calls,
  Newton engine shape objects, model finalization, collision pipeline calls, and Newton execution
  at zero, and at that stage advanced the runtime-lane next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract` while
  keeping Newton support, real Newton execution, USD, benchmark, collision-quality,
  `paper_faithful_offline`, deployment, and safety claims unsupported.
- The partial `cpd_paper_offline_report` now includes
  `paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract`, a
  single-fixture bounded Newton/Warp environment-provenance contract. It consumes the
  engine-builder boundary-preflight row, records configured-source-dir status and JSON-safe
  `find_spec` provenance shape, keeps real runtime imports, `newton.ModelBuilder`
  instantiation, real Newton builder shape calls, Newton engine shape objects, model finalization,
  collision pipeline calls, and runtime counters at zero, and at that stage advanced the
  stage-local runtime-lane next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract` while keeping
  Newton support, real Newton execution, USD, benchmark, collision-quality,
  `paper_faithful_offline`, deployment, and safety claims unsupported.
- The partial `cpd_paper_offline_report` now includes
  `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract`, a
  single-fixture bounded source-AST API-surface contract. It consumes the environment-probe row,
  records default no-config API-surface status for the future `newton.ModelBuilder` /
  `add_shape_box` boundary, may read and parse Newton source files only when a source directory is
  explicitly passed, keeps real runtime imports, `newton.ModelBuilder` instantiation, real Newton
  builder shape calls, Newton engine shape objects, model finalization, collision pipeline calls,
  and runtime counters at zero, and at that stage advanced the stage-local runtime-lane next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract`
  while keeping Newton support, real Newton execution, USD, benchmark, collision-quality,
  `paper_faithful_offline`, deployment, and safety claims unsupported.
- The partial `cpd_paper_offline_report` now includes
  `paper_mapped_subset_conversion_candidate_matrix`, a command-only offline candidate matrix, not a
  `CollisionPackage`. It records three future-family review rows, keeps the current 16
  `trapezoidal_prism` / `offline_only_unmapped` rows blocked and offline, records zero current
  package-conversion candidates, and at that stage advanced the next gate to
  `paper_mapped_subset_adapter_preflight_contract`. It is not package readiness, Newton readiness,
  runtime admissibility, approximation support, PrimitiveSpec generation, CollisionPackage
  generation, package generation, Newton runtime execution, real-USD asset evidence, benchmark
  evidence, `paper_faithful_offline` support, full CPD reproduction, collision-quality evidence,
  deployment readiness, or safety certification.
- The partial `cpd_paper_offline_report` now includes
  `paper_mapped_subset_adapter_preflight_contract`, a command-only offline adapter-preflight
  contract, not `PrimitiveSpec` generation and not a `CollisionPackage`. It records future
  adapter requirements, records no-op behavior for the current zero package-conversion-candidate
  state, keeps all current unmapped trapezoidal-prism rows offline, keeps package generation
  disabled, and advances the next gate to
  `paper_mapped_subset_primitivespec_dry_run_contract`. It is not package readiness, Newton
  readiness, runtime admissibility, approximation support, `PrimitiveSpec` readiness,
  PrimitiveSpec generation, CollisionPackage generation, package generation, Newton runtime
  execution, real-USD asset evidence, benchmark evidence, `paper_faithful_offline` support, full
  CPD reproduction, collision-quality evidence, deployment readiness, or safety certification.
- The partial `cpd_paper_offline_report` now includes
  `paper_mapped_subset_primitivespec_dry_run_contract`, a command-only offline PrimitiveSpec
  dry-run contract, not real `PrimitiveSpec` generation and not a `CollisionPackage`. It records
  future PrimitiveSpec shape requirements for OBB/box, sphere, and capsule, keeps capped cylinder
  and frustum blocked behind an approximation policy, keeps current unmapped trapezoidal-prism
  rows offline/no-op, records zero current PrimitiveSpec candidates, records zero generated
  PrimitiveSpec rows, and advances the next gate to
  `paper_mapped_subset_primitivespec_validation_contract`. It is not package readiness, Newton
  readiness, runtime admissibility, approximation support, `PrimitiveSpec` readiness,
  PrimitiveSpec generation, CollisionPackage generation, package generation, Newton runtime
  execution, real-USD asset evidence, benchmark evidence, `paper_faithful_offline` support, full
  CPD reproduction, collision-quality evidence, deployment readiness, or safety certification.
- The partial `cpd_paper_offline_report` now includes
  `paper_mapped_subset_primitivespec_validation_contract`, a command-only offline PrimitiveSpec
  validation contract, not real `PrimitiveSpec` generation and not a `CollisionPackage`. It
  validates the dry-run contract field list, mapped future shape labels, six family rows, 16
  current no-op rows, source traceability, zero current candidates, zero generated PrimitiveSpecs,
  and false runtime/evaluation triggers. It advances the next gate to
  `paper_mapped_subset_primitivespec_generation_preflight_contract`. It is not package readiness,
  Newton readiness, runtime admissibility, approximation support, `PrimitiveSpec` readiness,
  PrimitiveSpec generation, CollisionPackage generation, package generation, Newton runtime
  execution, real-USD asset evidence, benchmark evidence, `paper_faithful_offline` support, full
  CPD reproduction, collision-quality evidence, deployment readiness, or safety certification.
- The partial `cpd_paper_offline_report` now includes
  `paper_mapped_subset_primitivespec_generation_preflight_contract`, a command-only offline
  PrimitiveSpec generation-preflight contract, not real `PrimitiveSpec` generation and not a
  `CollisionPackage`. It consumes the validation contract, records future native-family generation
  requirements for OBB/box, sphere, and capsule, keeps capped cylinder and frustum blocked behind
  approximation policy, keeps trapezoidal prism no-op/unmapped, keeps current generation
  candidates at zero, keeps generated PrimitiveSpecs, generated CollisionPackages, and
  runtime-admissibility checks at zero, and advances the next gate to
  `paper_mapped_subset_primitivespec_generation_contract`. It is not package readiness, Newton
  readiness, runtime admissibility, approximation support, `PrimitiveSpec` readiness, real
  PrimitiveSpec generation, CollisionPackage generation, package generation, Newton runtime
  execution, real-USD asset evidence, benchmark evidence, `paper_faithful_offline` support, full
  CPD reproduction, collision-quality evidence, deployment readiness, or safety certification.
- The partial `cpd_paper_offline_report` now includes
  `paper_mapped_subset_primitivespec_generation_contract`, a command-only offline PrimitiveSpec
  generation contract with template rows, not runtime `PrimitiveSpec` generation and not a
  `CollisionPackage`. It consumes the generation-preflight contract, emits future native-family
  templates for box/sphere/capsule, keeps capped cylinder and frustum blocked behind later
  approximation policy, keeps trapezoidal prism and all current unmapped rows offline/no-op, keeps
  generated runtime PrimitiveSpecs, generated CollisionPackages, and runtime-admissibility checks
  at zero, and advances the next gate to
  `paper_mapped_subset_primitivespec_candidate_source_contract`. It is not package readiness,
  Newton readiness, runtime admissibility, approximation support, `PrimitiveSpec` readiness, real
  PrimitiveSpec generation, CollisionPackage generation, package generation, Newton runtime
  execution, real-USD asset evidence, benchmark evidence, `paper_faithful_offline` support, full
  CPD reproduction, collision-quality evidence, deployment readiness, or safety certification.
- The partial `cpd_paper_offline_report` now includes
  `paper_mapped_subset_primitivespec_candidate_source_contract`, a command-only offline
  PrimitiveSpec candidate-source audit, not runtime `PrimitiveSpec` generation and not a
  `CollisionPackage`. It consumes the generation contract, emits three future-only native-template
  source audit rows, two blocked approximation-policy family source rows, one no-op
  trapezoidal-prism family source row, and 16 traceable but ineligible current
  `trapezoidal_prism` / `offline_only_unmapped` rows. It keeps eligible current PrimitiveSpec
  candidate sources, generated PrimitiveSpecs, generated CollisionPackages, and
  runtime-admissibility checks at zero, and advances the next gate to
  `paper_mapped_subset_native_current_fixture_contract`. It is not package readiness, Newton
  readiness, runtime admissibility, approximation support, `PrimitiveSpec` readiness, real
  PrimitiveSpec generation, CollisionPackage generation, package generation, Newton runtime
  execution, real-USD asset evidence, benchmark evidence, `paper_faithful_offline` support, full
  CPD reproduction, collision-quality evidence, deployment readiness, or safety certification.
- The current code can run a command-only deterministic synthetic objective comparison over
  in-memory toy meshes. This compares topology-only and component-merge diagnostic accounting for
  inspection only. This is not benchmark evidence, broad asset evidence, full CPD paper
  reproduction, or collision-quality validation.
- The current code can run a focused geometry-only CPD-like cost-guided merge-search smoke that
  uses AABB-normalized merge-excess as a decision-making cost and compares old/new diagnostic
  accounting on a deterministic synthetic fixture. This is not full CPD paper reproduction,
  paper-faithful optimization, benchmark evidence, or collision-quality validation.
- The current code can run synthetic offline merge-step trace diagnostic accounting for the
  cost-guided merge-search smoke when `report_merge_trace: steps` is requested. The trace records
  accepted or blocked merge decisions, source faces/components, merged primitive type, and
  raw/normalized merge-excess for inspection. This is not a merge-policy improvement,
  collision-quality result, benchmark result, Newton task result, paper-faithful search trace, or
  CPD optimizer implementation.
- The current code can run a deterministic expected-failure synthetic workbench over in-memory
  fixtures that checks whether known CPD-like limitation flags remain visible. A `smoke_passed`
  result means expected limitation flags matched observed flags, not decomposition success,
  collision-quality validation, benchmark evidence, or full CPD paper reproduction.
- The current code can run an opt-in offline `capped_cylinder` geometry proposal proxy and report
  that the named objective smoke reduces unsupported paper primitive vocabulary from three types to
  two. This is primitive-vocabulary accounting for a restricted proposal baseline, not
  paper-faithful CPD primitive fitting, Newton support, benchmark evidence, or collision-quality
  validation.
- The current primitive roadmap is Newton-native first. The code can map and construct diagnostic
  Newton shapes for a synthetic package containing `box`, `sphere`, `capsule`, `cylinder`,
  `cone`, and `ellipsoid`, with dated clean-env contact, drop/settle, and sphere-rain smoke
  evidence. This is synthetic diagnostic-path evidence, not broad asset evidence or a claim that
  the CPD-like generator emits all six kinds by default.
- The current code can run an opt-in deterministic synthetic native fitting comparison where the
  six-kind Newton-native subset selects `cylinder`, `cone`, and `ellipsoid` on deterministic toy
  meshes, including a squat-cylinder fixture that exercises the controlled cylinder-axis search,
  and maps the resulting one-primitive packages through Newton shape mapping. This is synthetic
  fitting evidence, not collision-quality validation, default asset behavior, paper-faithful CPD
  primitive fitting, broad asset evidence, or completed bed/Franka evidence.
- The current synthetic native fitting comparison can include a candidate weighted-volume audit
  table that explains why the toy fixtures selected `cylinder`, `cone`, or `ellipsoid` under the
  current support-aware surrogate primitive-choice rule. This is synthetic diagnostic accounting,
  not a paper-faithful CPD optimizer, real-USD improvement evidence, benchmark evidence, or
  collision-quality validation.
- The current code can run a deterministic low-support native-extension admissibility fixture and
  can rank `cylinder`, `cone`, and `ellipsoid` candidates as selection-inadmissible when they have
  too few source faces or unique assigned points and a fallback primitive exists. This is a local
  diagnostic selection guard, not paper-faithful primitive fitting, not benchmark evidence, and not
  collision-quality validation.
- The current code can run a real-USD old/new native fitting diagnostic over capped
  `bed_dev_smoke` and capped `franka_import_smoke` first-mesh scope. The current support-aware
  dated run keeps bed at `32` boxes in both lanes and capped Franka at `32` boxes in both lanes,
  while reporting three Franka cheaper raw-cost cylinder candidates as support-blocked extension
  candidates. This is selection/accounting evidence, not evidence that boxes or cylinders improved
  those assets.
- The real-USD native fitting diagnostic can include a per-selected-cluster candidate audit
  summary that reports whether `cylinder`, `cone`, or `ellipsoid` was the cheapest raw-cost
  candidate and whether it was support-admissible under the current surrogate. This is diagnostic
  accounting for why the current lanes select their primitives, not a quality metric or native
  primitive improvement claim.
- The current code can run a real-USD candidate-loss diagnosis over capped bed and capped Franka
  native lanes. It reports per-cluster selected primitive ranks, extension-candidate margins,
  support-aware selection admissibility, simple cluster geometry hints, and likely surrogate
  bottleneck labels. This is diagnostic accounting, not collision-quality evidence, benchmark
  evidence, or a paper-faithful optimizer.
- The real-USD candidate-loss diagnosis can include next-slice triage metadata. It ranks
  near-miss extension candidates and low-support native-extension selections so the next synthetic
  fixture can be chosen from recorded accounting. This is planning metadata, not evidence that the
  ranked primitive kind is better.
- The current code can include a direct synthetic `cylinder_near_miss_cluster` fixture where `box`
  still wins, `cylinder` is support-admissible, and the relative weighted-volume gap is small.
  The fixture can be exposed through `cpd_like_near_miss_fixture_workbench`. This is a
  primitive-ranking diagnostic target for future fitting or merge/search work, not a native
  primitive success case and not collision-quality evidence.
- The current code can run `cpd_like_cylinder_near_miss_fit_ablation`, a synthetic offline report
  for the `cylinder_near_miss_cluster` fixture that records the current containing-cylinder radius
  and a pairwise radial lower bound. It can say that radial-center refinement cannot flip this
  fixture under containment and the current surrogate. This is diagnostic accounting, not a
  primitive-selection change, native primitive improvement, real-USD result, Newton task result,
  benchmark, collision-quality validation, or CPD paper reproduction.
- The current code can run `cpd_like_cylinder_near_miss_scoring_sensitivity`, a synthetic offline
  report for the same fixture that computes the counterfactual cylinder score multiplier and cost
  reduction required to tie the selected box under the current weighted-volume surrogate. This is
  sensitivity accounting for planning, not a scoring-policy change, primitive-selection
  improvement, evidence that cylinder is better, real-USD result, Newton task result, benchmark,
  collision-quality validation, or CPD paper reproduction.
- The current code can run `cpd_like_cylinder_near_miss_scoring_policy_ablation`, a synthetic
  offline report that applies a fixed counterfactual cylinder multiplier inside the report only.
  It records that the cylinder near-miss fixture would flip under that hypothetical scoring policy
  and that a clearly boxy cuboid guardrail fixture remains `box`. This is report-only
  sensitivity/guardrail accounting for planning, not a default scoring-policy change,
  primitive-selection improvement, evidence that cylinder is better, evidence the multiplier is
  safe or calibrated, real-USD result, Newton task result, benchmark, collision-quality validation,
  or CPD paper reproduction.
- The current code can run `cpd_like_cylinder_scoring_policy_selection_probe`, a synthetic offline
  opt-in selection probe that applies the same fixed cylinder multiplier to candidate selection
  only when explicitly requested by the probe. It records that the near-miss fixture flips while a
  clearly boxy cuboid guardrail remains `box`. This is a synthetic opt-in primitive-choice probe,
  not a default scoring-policy change, primitive-selection improvement, evidence that cylinder is
  better, evidence the multiplier is safe or calibrated, real-USD result, Newton task result,
  benchmark, collision-quality validation, or CPD paper reproduction.
- The current code can run `cpd_like_cylinder_scoring_policy_package_probe`, an explicitly opt-in
  synthetic package probe that passes `primitive_score_multipliers={"cylinder": 0.88}` through
  `decompose_mesh`, produces a changed synthetic `CollisionPackage` for the near-miss fixture,
  keeps the boxy guardrail package unchanged, and records Newton shape-mapping coverage. This is
  package-path and mapping-accounting evidence only, not default package behavior, scoring
  calibration, real-USD evidence, Newton contact/task evidence, collision-quality validation,
  benchmark evidence, or CPD paper reproduction.
- The current code can run `cpd_like_controlled_merge_search_package_probe`, a command-only
  synthetic package-path probe that carries the existing `cost_guided_pair_choice` fixture through
  `CollisionPackage` generation for `topology_then_virtual` versus `cost_guided_pairwise` lanes and
  records Newton shape-mapping coverage. This is package-path and mapping-accounting evidence only,
  not a default merge-policy change, merge-policy superiority result, real-USD evidence, Newton
  contact/task evidence, collision-quality validation, benchmark evidence, or CPD paper
  reproduction.
- The current code can run `cpd_like_controlled_merge_search_newton_probe`, a synthetic Newton
  diagnostic over the changed `cost_guided_pair_choice` package pair. It runs named
  `newton_contact_smoke`, `newton_drop_settle`, and `newton_sphere_rain` smokes behind the contact
  gate and records task status under recorded settings. This is synthetic task-smoke execution
  evidence for one changed merge/search package pair, not default merge behavior, merge-policy
  superiority, real-USD evidence, collision-quality validation, benchmark evidence, real
  contact-stress measurement, safety certification, or CPD paper reproduction.
- The current code can run `cpd_like_cost_guided_lookahead_merge_report`, a command-only
  synthetic two-step lookahead merge/search diagnostic over one deterministic trap fixture. It
  records that `two_step_lookahead` changes the toy grouping relative to greedy
  `cost_guided_pairwise` and lowers projected two-step normalized merge-excess under the current
  surrogate. This is offline synthetic merge/search accounting only, not default merge behavior,
  merge-policy superiority, package-path evidence, Newton contact/task evidence, real-USD evidence,
  collision-quality validation, benchmark evidence, or CPD paper reproduction.
- The current code can run `cpd_like_cost_guided_lookahead_package_probe`, a command-only
  synthetic package-path probe over the existing `lookahead_merge_trap` fixture. It converts greedy
  `cost_guided_pairwise` and opt-in `two_step_lookahead` decompositions into `CollisionPackage`,
  compares source-face groupings, and records Newton shape-mapping coverage. This is package-path
  and mapping-accounting evidence only; it does not change default merge behavior, rank merge
  policies, run Newton runtime tasks, touch real assets, measure collision geometry quality,
  compare against a benchmark suite, or complete paper-level reproduction.
- The current code can run `cpd_like_cost_guided_lookahead_newton_probe`, an explicitly opt-in
  synthetic Newton diagnostic over the lookahead-changed `lookahead_merge_trap` package pair. It
  runs named `newton_contact_smoke`, `newton_drop_settle`, and `newton_sphere_rain` smokes behind
  per-lane contact gates and records task status under recorded settings. This is synthetic
  task-smoke status only; it does not change default merge behavior, rank merge policies, touch
  real assets, report bed or Franka results, measure collision geometry quality, compare against a
  benchmark suite, support deployment or certification conclusions, find or rule out broad failure
  modes, or complete paper-level reproduction.
- The current code can run `cpd_like_four_block_slice_report`, a command-only evidence map for the
  already recorded `cost_guided_lookahead` synthetic slice. It summarizes primitive
  fitting/selection, merge/search, offline diagnostics, and recorded Newton task-smoke evidence by
  linking to dated records. This report does not invoke decomposition, USD loading, package
  builders, Newton runtime tasks, real assets, benchmark measurement, collision-quality
  evaluation, policy ranking, deployment/certification checks, or paper-level reproduction.
- The current code can run `cpd_like_cylinder_scoring_policy_newton_probe`, an explicitly opt-in
  synthetic Newton diagnostic over the changed `cylinder_near_miss_cluster` package pair. It runs
  named `newton_contact_smoke`, `newton_drop_settle`, and `newton_sphere_rain` smokes behind the
  contact gate and records task status under recorded settings. This is synthetic task-smoke
  execution evidence for one opt-in changed package, not default package behavior, scoring
  calibration, real-USD evidence, collision-quality validation, benchmark evidence, real
  contact-stress measurement, safety certification, or CPD paper reproduction.
- The current code can run a gated real-USD Newton probe comparison for capped bed and capped
  Franka first-mesh packages: full package mapping, contact canary, then drop/settle and
  sphere-rain only after contact passes. This is named diagnostic smoke evidence under recorded
  settings, not collision-quality validation, benchmark evidence, or whole-robot Franka collider
  quality evidence.
- The current code can run a contact-only Newton canary for representative Newton-mapped primitive
  types from a CPD-like collision package. This is not task-level simulation evidence.
- The current code can run the named `newton_drop_settle` task-level smoke diagnostic for the
  capped bed CPD-like collision package under the recorded config and environment. This is not
  collision quality validation, benchmark evidence, or CPD paper reproduction.
- The current code can run the named `newton_sphere_rain` task-level smoke diagnostic for the
  capped bed CPD-like collision package under the recorded config and environment. This is a
  contact-density proxy smoke, not a real contact-stress measurement, collision quality validation,
  benchmark evidence, or CPD paper reproduction.
- The current code can open the recorded local Franka USD and run a capped geometry-only CPD-like
  smoke over the first extracted mesh. This is robot asset import and geometry smoke only, not
  whole-robot collider quality, articulated dynamics, aggregate robot evidence, or benchmark
  evidence.
- The current clean local Python/Newton environment-readiness report can be described as
  `smoke_passed` evidence for the named environment path, Newton source checkout, and hardware
  environment in the dated record.

## Claims Requiring Phase 0 Evidence

Use these only after a dated record links them to Phase 0 assets, configs, logs, and reports.

- A non-LLM primitive baseline has been tested on the 5-10 asset proof point.
- Newton checker probes have found or ruled out specific failure modes for specific assets.
- Robot asset coverage beyond the recorded Franka USD-open and first-mesh geometry smoke.
- A baseline comparison includes primitive count, fallback ratio, step time, contact count, and
  penetration or jitter measurements.
- A generated collision package is simulation-checked for a named task in a named environment,
  beyond the recorded capped-bed, capped-Franka first-mesh, synthetic native-bundle, synthetic
  cylinder scoring-policy, synthetic controlled merge-search, and synthetic lookahead smokes.
- A DLC-worker or experiment-specific Python/Newton environment has passed readiness checks for a
  named source checkout and hardware environment.

## Claims Requiring Phase 1 Or Phase 2 Evidence

Use these only after broader benchmark records exist.

- The approach improves a metric relative to bounding primitives, convex hulls, decomposition
  baselines, or VisACD when available.
- Checker-guided repair reduces fallback rate on a documented asset set.
- The system supports a repeatable asset ingestion workflow beyond the DeepDive proof point.
- LLM/VLM planning adds value beyond deterministic baselines.

## Forbidden Claims

- Do not claim the repository guarantees real-world safety.
- Do not claim the compiler is deployment-ready.
- Do not claim any package is certified safe.
- Do not claim the method is proven safe.
- Do not claim the method fully replaces convex decomposition, SDFs, or human review.
- Do not claim benchmark superiority before the benchmark record exists.
- Do not treat environment-readiness diagnostics as Newton simulation checker results.
- Do not treat asset mirror materialization as dataset licensing review, benchmark evidence,
  complete visual/material packaging, collision-quality validation, or deployment readiness.
- Do not claim full CPD paper reproduction before paper-scope primitive coverage, benchmark
  settings, and dated experiment records exist.
- Do not describe the CPD-like component-merge gate as the CPD paper algorithm; it is a restricted
  baseline extension and report-audit slice.
- Do not describe the offline objective report as a collision-quality metric or proof that the
  decomposition is good; it is diagnostic accounting for future algorithm work.
- Do not describe "paper-aligned surrogate objective report" as equivalent to a paper-faithful
  objective implementation.
- Do not describe Eq.4 alignment metadata as Eq.4 implementation, paper-faithful objective
  scoring, or proof that the current merge search matches the paper.
- Do not describe the synthetic objective comparison as benchmark evidence or proof that one merge
  policy is better; it is fixture-level diagnostic accounting.
- Do not describe the cost-guided merge-search improvement as the CPD paper optimizer or as proof
  that one decomposition is better collision geometry; it is a restricted algorithmic smoke slice
  under diagnostic objective accounting.
- Do not describe the expected-failure synthetic workbench as a benchmark, validation, failure
  detector, proof that the baseline catches bad decompositions, collision-quality score, safe
  collider rejection step, or complete coverage of CPD-like limitations.
- Do not describe the capped-cylinder proxy as paper-faithful capped-cylinder support, CPD
  primitive fitting implementation, Newton capped-cylinder support, collision-quality improvement,
  benchmark evidence, or asset/task improvement.
- Do not claim broad Newton-native primitive quality for `cylinder`, `cone`, or `ellipsoid`
  beyond the dated synthetic diagnostic-path, opt-in synthetic fitting, and capped real-USD
  diagnostic records. Do not claim the CPD-like generator emits these kinds by default for normal
  asset configs. Do not claim bed or Franka native-fitting improvement from the current
  support-aware real-USD records; bed and Franka currently select boxes, and the three
  support-blocked Franka cylinder candidates are surrogate accounting, not quality evidence.
- Do not describe the synthetic native selection audit as a quality metric, paper-faithful
  optimizer, proof that native primitives are broadly better, real-USD improvement, or collision
  validation. It is a candidate-cost diagnostic table over toy meshes.
- Do not describe support-aware native-extension admissibility as a paper objective, learned
  classifier, safety filter, or proof that low-support native primitives are bad. It is a local
  face/point support guard for the current diagnostic workbench.
- Do not describe the real-USD native probe comparison as a benchmark, collision-quality
  validation, whole-robot Franka collider-quality result, or native primitive improvement result.
- Do not describe the real-USD candidate audit summary as proof that the selected primitives are
  good. It is a surrogate candidate-accounting summary over selected clusters.
- Do not describe the real-USD candidate-loss diagnosis as a quality metric, benchmark result,
  proof that boxes or cylinders are better, or evidence that the Franka collider is good.
- Do not describe candidate-loss triage as an optimizer or as proof of the next algorithmic
  direction. It is a deterministic sorting aid for choosing the next synthetic diagnostic target.
- Do not describe the `cylinder_near_miss_cluster` fixture as a resolved near miss, a native
  fitting improvement, or a real-USD package improvement. It is a synthetic limitation target.
- Do not describe `cpd_like_cylinder_near_miss_fit_ablation` as fixing cylinder fitting or proving
  cylinder quality. It is a containment-preserving lower-bound diagnostic that keeps default
  selection and Newton packages unchanged.
- Do not describe `cpd_like_cylinder_near_miss_scoring_sensitivity` as improving the objective,
  calibrating scoring, proving boxes are wrong, or recommending a cylinder bias. It is
  counterfactual sensitivity accounting and does not apply the multiplier it reports.
- Do not describe `cpd_like_cylinder_near_miss_scoring_policy_ablation` as a new default scoring
  policy, calibrated objective, selection improvement, recommended cylinder bias, or Newton-checked
  flip. It is a report-only counterfactual over deterministic synthetic fixtures.
- Do not describe `cpd_like_cylinder_scoring_policy_package_probe` as a default package change,
  calibrated scoring policy, Newton diagnostic run, simulation-checked package, real-USD package
  improvement, or collision-quality result. It is an explicitly opt-in synthetic package and
  Newton shape-mapping summary only.
- Do not describe `cpd_like_controlled_merge_search_package_probe` as a default merge-policy change,
  merge-policy superiority result, Newton diagnostic run, simulation-checked package, real-USD
  package improvement, or collision-quality result. It is a single-fixture synthetic package-path
  and Newton shape-mapping summary only.
- Do not use the synthetic `cpd_like_controlled_merge_search_newton_probe` as evidence that
  `cost_guided_pairwise` is better than `topology_then_virtual`, that merge policy was validated,
  that real-USD/bed/Franka packages improved, or that collision quality was validated. It is a named
  synthetic task-smoke diagnostic over one changed package pair.
- Do not use the synthetic `cpd_like_cylinder_scoring_policy_newton_probe` as evidence that the
  cylinder multiplier is calibrated, that cylinder is better than box, that real-USD/bed/Franka
  packages improved, that failure modes were found or ruled out, or that collision quality was
  validated. It is a named synthetic task-smoke diagnostic over one opt-in changed package pair.
- Do not use CPD paper primitive-vocabulary completeness as a runtime support claim. Paper-only
  primitives remain offline diagnostics unless separately mapped and verified.
- Do not describe `paper_package_adapter_unsupported_primitive_policy` as package readiness,
  Newton support, runtime admissibility, approximation support, or package-generation gate
  completion. It is offline policy accounting only.
- Do not describe `paper_package_conversion_mapped_subset_plan` as package readiness, package
  conversion execution, Newton support, runtime admissibility, approximation support, or
  package-generation gate completion. It is offline mapped-subset planning only.
- Do not describe `paper_mapped_subset_conversion_candidate_matrix` as package readiness,
  package conversion execution, PrimitiveSpec generation, CollisionPackage generation, Newton
  support, runtime admissibility, approximation support, or package-generation gate completion. It
  is offline candidate-matrix review only.
- Do not describe `paper_mapped_subset_adapter_preflight_contract` as package readiness,
  PrimitiveSpec readiness, package conversion execution, PrimitiveSpec generation,
  CollisionPackage generation, Newton support, runtime admissibility, approximation support, or
  package-generation gate completion. It is offline adapter-preflight contract accounting only.
- Do not describe `paper_mapped_subset_primitivespec_dry_run_contract` as PrimitiveSpec readiness,
  PrimitiveSpec generation, package readiness, package conversion execution, CollisionPackage
  generation, Newton support, runtime admissibility, approximation support, or package-generation
  gate completion. It is offline PrimitiveSpec dry-run contract accounting only.
- Do not describe `paper_mapped_subset_primitivespec_validation_contract` as PrimitiveSpec
  readiness, PrimitiveSpec generation, package readiness, package conversion execution,
  CollisionPackage generation, Newton support, runtime admissibility, approximation support, or
  package-generation gate completion. It is offline PrimitiveSpec dry-run validation accounting
  only.
- Do not describe `paper_mapped_subset_primitivespec_generation_preflight_contract` as
  PrimitiveSpec readiness, real PrimitiveSpec generation, package readiness, package conversion
  execution, CollisionPackage generation, Newton support, runtime admissibility, approximation
  support, or package-generation gate completion. It is offline PrimitiveSpec generation-preflight
  accounting only.
- Do not describe `paper_mapped_subset_primitivespec_generation_contract` as PrimitiveSpec
  readiness, real PrimitiveSpec generation, package readiness, package conversion execution,
  CollisionPackage generation, Newton support, runtime admissibility, approximation support, or
  package-generation gate completion. It is offline PrimitiveSpec generation-contract template
  accounting only.
- Do not describe `paper_mapped_subset_native_current_fixture_contract` as PrimitiveSpec
  readiness, real PrimitiveSpec generation, package readiness, package conversion execution,
  CollisionPackage generation, Newton support, runtime admissibility, approximation support,
  real-USD evidence, benchmark evidence, or package-generation gate completion. It is offline
  native-current fixture source accounting only.
- Do not describe `paper_mapped_subset_primitivespec_native_fixture_generation_contract` as
  runtime PrimitiveSpec object creation, package readiness, package conversion execution,
  CollisionPackage generation, Newton support, runtime admissibility, approximation support,
  real-USD evidence, benchmark evidence, collision-quality evidence, deployment readiness, safety
  certification, or package-generation gate completion. It is offline serialized
  PrimitiveSpec-like dict accounting only.
- Do not describe `paper_mapped_subset_primitivespec_native_fixture_serialization_contract` as
  runtime PrimitiveSpec object creation, package readiness, package conversion execution,
  CollisionPackage generation, Newton support, runtime admissibility, approximation support,
  real-USD evidence, benchmark evidence, collision-quality evidence, deployment readiness, safety
  certification, or package-generation gate completion. It is offline JSON serialization and
  schema-stability accounting for one report-only PrimitiveSpec-like dict only.
- Do not describe `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract` as
  runtime PrimitiveSpec construction, package readiness, package conversion execution,
  CollisionPackage generation, Newton support, runtime admissibility, approximation support,
  real-USD evidence, benchmark evidence, collision-quality evidence, deployment readiness, safety
  certification, package-generation gate completion, full CPD reproduction, or
  `paper_faithful_offline` support. It is a command-only offline boundary preflight that records
  one later runtime-construction candidate while creating zero runtime objects.
- Do not describe `paper_mapped_subset_primitivespec_runtime_construction_contract` as
  package readiness, package conversion execution, CollisionPackage generation, Newton support,
  runtime admissibility, approximation support, real-USD evidence, benchmark evidence,
  collision-quality evidence, deployment readiness, safety certification, package-generation gate
  completion, full CPD reproduction, `paper_faithful_offline` support, or general PrimitiveSpec
  readiness. It constructs exactly one runtime `PrimitiveSpec` object from the deterministic
  synthetic `paper_single_box` OBB/box preflight row and stores only `PrimitiveSpec.to_dict()` in
  the partial offline report.
- Do not describe `paper_mapped_subset_collision_package_generation_preflight_contract` as
  package readiness, package conversion execution, CollisionPackage generation, Newton support,
  runtime admissibility, approximation support, real-USD evidence, benchmark evidence,
  collision-quality evidence, deployment readiness, safety certification, full CPD reproduction,
  `paper_faithful_offline` support, or runtime-check completion. It records exactly one later
  package-generation candidate from the deterministic synthetic `paper_single_box` OBB/box
  `PrimitiveSpec.to_dict()` row and still creates zero CollisionPackages.
- Do not describe `paper_mapped_subset_collision_package_generation_contract` as package
  readiness, Newton support, runtime admissibility, real-USD evidence, benchmark evidence,
  collision-quality evidence, deployment readiness, safety certification, full CPD reproduction,
  `paper_faithful_offline` support, paper primitive vocabulary coverage, or runtime-check
  completion. It constructs exactly one synthetic, report-scoped `CollisionPackage.to_dict()`
  artifact for the deterministic `paper_single_box` OBB/box row, records no runtime-admissibility
  checks, and marks the next required gate as
  `paper_mapped_subset_runtime_admissibility_preflight_contract`.
- Do not describe `paper_mapped_subset_runtime_admissibility_preflight_contract` as package
  readiness, Newton support, Newton execution, runtime admissibility, real-USD evidence, benchmark
  evidence, collision-quality evidence, deployment readiness, safety certification, full CPD
  reproduction, `paper_faithful_offline` support, paper primitive vocabulary coverage, or
  runtime-check completion. It records one later runtime-admissibility candidate row from the one
  synthetic `paper_single_box` package artifact and marks the next required gate as
  `paper_mapped_subset_runtime_admissibility_contract`.
- Do not describe `paper_mapped_subset_runtime_admissibility_contract` as package readiness,
  Newton readiness, Newton support, Newton execution, real-USD evidence, benchmark evidence,
  collision-quality validation, paper primitive vocabulary coverage, approximation support,
  `paper_faithful_offline` support, full CPD reproduction, deployment readiness, safety
  certification, or general package readiness. It records one offline/static geometry and schema
  check for one synthetic `paper_single_box` package artifact and marks the next runtime-lane gate
  as `paper_mapped_subset_newton_shape_mapping_preflight_contract`.
- Do not describe `paper_mapped_subset_newton_shape_mapping_preflight_contract` as Newton
  readiness, Newton support, Newton execution, real-USD evidence, benchmark evidence,
  collision-quality validation, paper primitive vocabulary coverage, approximation support,
  `paper_faithful_offline` support, full CPD reproduction, deployment readiness, safety
  certification, or general package readiness. It records one offline/static mapper-handoff row
  for one synthetic `paper_single_box` box artifact and marks the next runtime-lane gate as
  `paper_mapped_subset_newton_shape_mapping_contract`.
- Do not describe `paper_mapped_subset_newton_shape_mapping_contract` as Newton readiness, Newton
  support, Newton execution, real-USD evidence, benchmark evidence, collision-quality validation,
  paper primitive vocabulary coverage, approximation support, `paper_faithful_offline` support,
  full CPD reproduction, deployment readiness, safety certification, or general package readiness.
  It records one offline/static report-scoped descriptor dict for one synthetic
  `paper_single_box` box artifact, keeps all Newton runtime/object counters zero, and marks the
  next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`.
- Do not describe `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract` as Newton
  readiness, Newton support, Newton execution, real-USD evidence, benchmark evidence,
  collision-quality validation, paper primitive vocabulary coverage, approximation support,
  `paper_faithful_offline` support, full CPD reproduction, deployment readiness, safety
  certification, or general package readiness. It records one offline/static later
  runtime-construction candidate row for one synthetic `paper_single_box` box descriptor, keeps
  all Newton runtime/object counters zero, and marks the next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_construction_contract`.
- Do not describe `paper_mapped_subset_newton_shape_runtime_construction_contract` as Newton
  readiness, Newton support, Newton execution, real-USD evidence, benchmark evidence,
  collision-quality validation, paper primitive vocabulary coverage, approximation support,
  `paper_faithful_offline` support, full CPD reproduction, deployment readiness, safety
  certification, or general package readiness. It records one repo-local
  `NewtonShapeMapping.to_dict()` mapping record for one synthetic `paper_single_box` box descriptor,
  keeps all Newton engine shape object, builder shape call, and runtime counters zero, and marks
  the next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`.
- Do not describe `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract` as Newton
  readiness, Newton support, Newton execution, real-USD evidence, benchmark evidence,
  collision-quality validation, paper primitive vocabulary coverage, approximation support,
  `paper_faithful_offline` support, full CPD reproduction, deployment readiness, safety
  certification, or general package readiness. It records one JSON-safe future builder call plan
  for one synthetic `paper_single_box` box mapping record, keeps all Newton engine shape object,
  builder shape call, and runtime counters zero, and marks the next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_builder_construction_contract`.
- Do not describe `paper_mapped_subset_newton_shape_runtime_builder_construction_contract` as
  Newton readiness, Newton support, Newton execution, real-USD evidence, benchmark evidence,
  collision-quality validation, paper primitive vocabulary coverage, approximation support,
  `paper_faithful_offline` support, full CPD reproduction, deployment readiness, safety
  certification, or general package readiness. It records one JSON-safe fake `add_shape_box` call
  artifact through a repo-local recording builder and fake Warp-like module for one synthetic
  `paper_single_box` box mapping record. It keeps real Newton imports, Newton `ModelBuilder`
  instantiation, Newton engine shape objects, real Newton builder shape calls, and runtime
  counters zero, and at that stage marks the next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract`.
- Do not describe
  `paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract` as Newton
  readiness, Newton support, Newton execution, real-USD evidence, benchmark evidence,
  collision-quality validation, paper primitive vocabulary coverage, approximation support,
  `paper_faithful_offline` support, full CPD reproduction, deployment readiness, safety
  certification, real Newton environment success, or general package readiness. It records one
  offline/static future-boundary checklist row for one synthetic `paper_single_box` box mapping
  record. It keeps real Newton imports, Newton `ModelBuilder` instantiation, real Newton builder
  shape calls, Newton engine shape objects, model finalization, collision pipeline calls, and
  runtime counters zero. The later environment-probe slice marked the stage-local next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract`; the later
  API-surface slice marked the stage-local next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract`; the later
  entry slice marked the stage-local next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract`; the later smoke
  slice marked the stage-local next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract`; the later
  runtime-execution slice marked the stage-local next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract`; the later
  runtime-lane review slice marked the stage-local next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract`;
  the later configured-runtime design slice marked the stage-local next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract`;
  the later configured-runtime preflight slice marked the stage-local next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_validation_contract`;
  the later configured-runtime validation slice marked the stage-local next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract`;
  the later configured-runtime source-resolution slice marked the stage-local next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract`;
  the later configured-runtime device-resolution slice marked the stage-local next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract`;
  the later configured-runtime entry-decision slice marks the current next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract`.
- Do not describe
  `paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract` as Newton
  readiness, Newton support, Newton execution, real-USD evidence, benchmark evidence,
  collision-quality validation, paper primitive vocabulary coverage, approximation support,
  `paper_faithful_offline` support, full CPD reproduction, deployment readiness, safety
  certification, real Newton environment success, or general package readiness. It records one
  bounded environment-provenance row for one synthetic `paper_single_box` box mapping record. It
  uses JSON-safe `find_spec` provenance shape and keeps real runtime imports,
  `newton.ModelBuilder` instantiation, real Newton builder shape calls, Newton engine shape
  objects, model finalization, collision pipeline calls, and runtime counters zero. It marked the
  next runtime-lane gate as `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract`.
- Do not describe
  `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract` as Newton
  readiness, Newton support, Newton execution, runtime compatibility, real-USD evidence,
  benchmark evidence, collision-quality validation, paper primitive vocabulary coverage,
  approximation support, `paper_faithful_offline` support, full CPD reproduction, deployment
  readiness, safety certification, real Newton environment success, or general package readiness.
  It records one bounded source-AST API-surface row for one synthetic `paper_single_box` box
  mapping record. It may read source files and parse AST only when a Newton source directory is
  explicitly passed, and it keeps real runtime imports, `newton.ModelBuilder` instantiation, real
  Newton builder shape calls, Newton engine shape objects, model finalization, collision pipeline
  calls, and runtime counters zero. It marked the
  stage-local next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract`.
- Do not describe
  `paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract` as Newton readiness,
  Newton support, Newton execution, runtime compatibility, real-USD evidence, benchmark evidence,
  collision-quality validation, paper primitive vocabulary coverage, approximation support,
  `paper_faithful_offline` support, full CPD reproduction, deployment readiness, safety
  certification, real Newton environment success, or general package readiness. It records one
  report-only default no-runtime-entry decision for one synthetic `paper_single_box` lineage. It
  keeps real runtime imports, `newton.ModelBuilder` instantiation, Newton engine shape objects,
  real Newton builder shape calls, model finalization, collision pipeline calls, runtime entry
  attempts, and runtime execution counters zero. It marked the stage-local next runtime-lane gate
  as `paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract`.
- Do not describe
  `paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract` as Newton readiness,
  Newton support, Newton execution, runtime compatibility, real-USD evidence, benchmark evidence,
  collision-quality validation, paper primitive vocabulary coverage, approximation support,
  `paper_faithful_offline` support, full CPD reproduction, deployment readiness, safety
  certification, real Newton environment success, runtime smoke success, or general package
  readiness. It records one report-only `skip_real_runtime_smoke` decision for one synthetic
  `paper_single_box` lineage. It keeps real runtime imports, `newton.ModelBuilder` instantiation,
  Newton engine shape objects, real Newton builder shape calls, model finalization, collision
  pipeline calls, runtime-smoke attempts, and runtime execution counters zero. It marked the
  stage-local next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract`.
- Do not describe
  `paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract` as Newton
  readiness, Newton support, Newton execution, runtime compatibility, real-USD evidence,
  benchmark evidence, collision-quality validation, paper primitive vocabulary coverage,
  approximation support, `paper_faithful_offline` support, full CPD reproduction, deployment
  readiness, safety certification, real Newton environment success, runtime execution success, or
  general package readiness. It records one report-only `skip_real_runtime_execution` decision for
  one synthetic `paper_single_box` lineage. It keeps real runtime imports,
  `newton.ModelBuilder` instantiation, Newton engine shape objects, real Newton builder shape
  calls, model finalization, collision pipeline calls, runtime-execution attempts, and runtime
  execution counters zero. It marked the stage-local next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract`.
- Do not describe
  `paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract` as Newton
  readiness, Newton support, Newton execution, runtime compatibility, real-USD evidence,
  benchmark evidence, collision-quality validation, paper primitive vocabulary coverage,
  approximation support, `paper_faithful_offline` support, full CPD reproduction, deployment
  readiness, safety certification, real Newton environment success, runtime execution success, or
  general package readiness. It records one report-only claim-boundary review for one synthetic
  `paper_single_box` skipped-runtime-execution lineage. It keeps real runtime imports,
  `newton.ModelBuilder` instantiation, Newton engine shape objects, real Newton builder shape
  calls, model finalization, collision pipeline calls, runtime-execution attempts, and runtime
  execution counters zero. It marked the stage-local next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract`.
- Do not describe
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract` as
  Newton readiness, Newton support, Newton execution, runtime config validation, runtime
  compatibility, real-USD evidence, benchmark evidence, collision-quality validation, paper
  primitive vocabulary coverage, approximation support, `paper_faithful_offline` support, full
  CPD reproduction, deployment readiness, safety certification, real Newton environment success,
  runtime execution success, or general package readiness. It records one report-only configured
  runtime input design for one synthetic `paper_single_box` skipped-runtime lineage. It keeps
  runtime config validation false, real runtime imports, `newton.ModelBuilder` instantiation,
  Newton engine shape objects, real Newton builder shape calls, model finalization, collision
  pipeline calls, runtime-execution attempts, and runtime execution counters zero. The follow-on
  configured-runtime preflight record keeps runtime config validation and runtime source/device
  resolution false. The follow-on configured-runtime validation record keeps runtime source/device
  resolution false and reads no config file or environment. The follow-on configured-runtime
  source-resolution record keeps runtime source/device resolution false and performs no filesystem
  probe. The follow-on configured-runtime device-resolution record keeps runtime source/device
  resolution false and creates no runtime device object. The follow-on configured-runtime
  entry-decision record keeps runtime entry allowed/attempted/passed false and attempts no runtime
  entry. It marks the current next runtime-lane gate as
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract`.

## Wording Rules

- Use "simulation-checked" only for artifacts with a named task-level Newton diagnostic record.
  Contact-only canary records do not qualify. For the recorded capped-bed drop/settle and
  sphere-rain smokes, prefer the exact diagnostic names unless reviewer context specifically needs
  the "simulation-checked" term.
- Use "simulation-verified" only after a specific verification standard is documented.
- Say "measure whether" instead of "prove whether" for research questions.
- Say "fallback-aware" instead of "fallback-free" unless a record shows zero fallback.
- Treat generated collision packages as safety-affecting artifacts, not as safety-certified
  artifacts.
- Prefer "diagnostic checker" over "verifier" in leadership-facing material.
- Prefer "higher-fidelity reference comparison" over "oracle" unless a task-specific reference
  standard is defined.
