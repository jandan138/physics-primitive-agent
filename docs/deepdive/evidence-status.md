# Evidence Status

This file separates current evidence from future claims. See [message-map.md](message-map.md) for canonical DeepDive wording.

## Current Supported Claims

- The repository is a DeepDive-first bootstrap for a Newton Primitive Collision Compiler proposal.
- The safe intended framing is primitive-first, Newton-checker-planned, fallback-aware collision
  asset compilation; current executable evidence is config/USD/env diagnostics plus a
  geometry-only CPD-like smoke path.
- The first milestone is a non-LLM primitive baseline plus Newton diagnostic checker.
- LLM/VLM should be deferred until the non-LLM baseline shows value.
- The proposal requires explicit fallback to convex decomposition, SDF, hydroelastic, convex mesh, or manual review.
- The current executable surface can report config dry-runs, USD asset-open smoke diagnostics,
  Newton source import diagnostics, and environment-readiness diagnostics.
- The current executable surface can materialize manifest USD assets into ignored repo-local
  mirrors under `assets/raw/mirrors/` and prefer those local paths at runtime when present. Current
  bed materialization records the material/texture closure; current Franka materialization records
  a USD layer mirror with unresolved `OmniPBR.mdl`. This is asset intake and reproducibility
  diagnostics, not benchmark or collision-quality evidence. See
  [Asset mirror materialization](../reference/asset-mirror-materialization.md).
- The current executable surface can run a geometry-only CPD-like face-merge smoke path that
  extracts a USD mesh, fits restricted `box`/`sphere`/`capsule` primitive candidates plus an
  opt-in offline `capped_cylinder` proposal proxy, greedily merges adjacent face groups by
  weighted excess volume, and emits a JSON diagnostic report.
  The plain-language explanation is in
  [CPD-like face-merge explainer](../reference/cpd-like-face-merge-explainer.md).
- The current executable surface can run an opt-in geometry-only CPD-like component-merge gate
  that tries disconnected-component pairwise merge candidates after topology adjacency merges are
  exhausted, and reports AABB-normalized excess-volume accounting.
- The current executable surface can run `cpd_like_offline_objective`, an offline
  paper-aligned surrogate objective report over the CPD-like baseline. It reports primitive-budget
  pressure, AABB-normalized volume proxy, raw Eq.4-like and AABB-normalized merge-excess
  accounting, assigned-point containment proxy, unsupported paper primitive gaps,
  component/fallback labels, and structured Eq.4 alignment metadata. This is diagnostic
  accounting, not Eq.4 implementation, collision-quality evidence, or full CPD reproduction. The
  alignment boundary is documented in
  [CPD objective report alignment](../reference/cpd-objective-report-alignment.md): design-aligned
  with the paper story, not mathematically paper-faithful.
- The current executable surface can run `cpd_like_synthetic_objective_comparison`, a command-only
  deterministic synthetic comparison over three in-memory toy meshes. It compares topology-only
  and component-merge objective accounting for inspection. This is not benchmark evidence,
  collision-quality evidence, or full CPD reproduction.
- The current executable surface can run `cpd_like_cost_guided_synthetic_objective_comparison`, a
  focused CPD-like cost-guided merge-search smoke that turns AABB-normalized merge-excess into a
  decision-making cost and compares old/new diagnostic accounting on deterministic synthetic
  fixture. This is not benchmark evidence, collision-quality evidence, paper-faithful
  optimization, or full CPD reproduction.
- The current executable surface can run synthetic offline merge-step trace diagnostic accounting
  for the same cost-guided fixture when `report_merge_trace: steps` is requested. The trace makes
  accepted and blocked merge decisions inspectable, but it is not a new merge policy or quality
  result.
- The current executable surface can run `cpd_like_controlled_merge_search_package_probe`, a
  command-only synthetic package-path probe for the same cost-guided fixture. It records that
  `topology_then_virtual` and `cost_guided_pairwise` produce different `CollisionPackage`
  source-face groupings and that both packages map to Newton shapes. This is package-path and
  mapping accounting only, not Newton contact/task evidence, real-USD evidence, collision-quality
  validation, or CPD reproduction.
- The current executable surface can run `cpd_like_controlled_merge_search_newton_probe`, a
  synthetic contact-gated Newton task-smoke probe for the same changed package pair. It records
  contact, drop/settle, and sphere-rain status under recorded settings. This is synthetic task-smoke
  evidence only, not merge-policy superiority, real-USD evidence, collision-quality validation, or
  CPD reproduction.
- The current executable surface can run `cpd_like_cost_guided_lookahead_merge_report`, a
  command-only synthetic two-step lookahead merge/search diagnostic over one deterministic trap
  fixture. It records that `two_step_lookahead` changes the toy grouping relative to greedy
  `cost_guided_pairwise` and lowers projected two-step normalized merge-excess under the current
  surrogate. This is offline merge/search accounting only, not package-path evidence, Newton
  contact/task evidence, real-USD evidence, collision-quality validation, or CPD reproduction.
- The current executable surface can run `cpd_like_cost_guided_lookahead_package_probe`, a
  command-only synthetic package-path and Newton shape-mapping probe over the same trap fixture.
  It records that the greedy and `two_step_lookahead` lanes produce different
  `CollisionPackage` source-face groupings and that both packages map to Newton shapes. This is
  package-path and mapping accounting only; it does not run Newton runtime tasks, touch real
  assets, report bed or Franka results, measure collision geometry quality, or complete
  paper-level reproduction.
- The current executable surface can run `cpd_like_cost_guided_lookahead_newton_probe`, an
  explicitly opt-in synthetic Newton diagnostic over the same changed package pair. It records
  contact-gated `newton_contact_smoke`, `newton_drop_settle`, and `newton_sphere_rain` task status
  under recorded settings. This is synthetic task-smoke status only; it does not touch real assets,
  report bed or Franka results, rank merge policies, measure collision geometry quality, or
  complete paper-level reproduction.
- The current executable surface can run `cpd_like_expected_failure_synthetic_workbench`, a
  command-only deterministic expected-failure synthetic workbench over known CPD-paper gaps. It
  reports expected, observed, missing, and unexpected diagnostic flags for each fixture.
  `smoke_passed` means expected limitations were reported, not decomposition success, benchmark
  evidence, collision-quality validation, or full CPD reproduction.
- The current executable surface can run an opt-in offline capped-cylinder proxy objective smoke.
  In that named report, the unsupported paper primitive gap decreases from 3 to 2:
  `frustum` and `trapezoidal_prism` remain unsupported. This is not Newton support,
  collision-quality evidence, paper-faithful primitive fitting, or full CPD reproduction.
- The current CPD paper-story position is documented as a reproduction workbench, not as a
  paper-faithful implementation. See
  [CPD paper story status](../reference/cpd-paper-story-status.md).
- The current executable surface can run `cpd_paper_offline_report`, a command-only partial
  offline CPD paper-lane audit over deterministic toy fixtures. It now includes a
  `paper_faithful_offline_scope_audit` criteria table with `decision: remain_partial`,
  `paper_faithful_offline_supported: false`, and a prior scope-audit gate of
  `paper_fixture_breadth_expansion_plan`. The current gate is now updated below by the
  fixture-breadth completion review and generalization planning table. This is
  scope accounting for the offline paper lane, not `paper_faithful_offline`, full CPD
  reproduction, package generation, Newton runtime support, real-USD evidence, benchmark
  evidence, or collision-quality validation.
- The current documentation can define an offline-only fixture-breadth expansion plan for the nine
  blocking scope-audit rows. The plan is not executable evidence by itself and does not implement
  package generation, Newton runtime support, real-USD evidence, benchmark evidence, or
  collision-quality validation.
- The report also includes the Batch A fixture-breadth source/preprocess/intake/operator slice
  inside `cpd_paper_offline_report`, adding
  `paper_mixed_face_preprocess_operator`, `paper_degenerate_preprocess_face_drop`, and
  `paper_concave_polygon_rejected` as synthetic offline cases. This is an intermediate synthetic
  offline slice; later fixture-breadth batches advance the current report gate beyond Batch A.
  This is not `paper_faithful_offline`, package generation, Newton runtime support, real-USD
  evidence, benchmark evidence, or collision-quality validation.
- The current executable surface can run the Batch B fixture-breadth primitive-fit slice inside
  `cpd_paper_offline_report`, adding `paper_rotated_box_fit`, `paper_offset_sphere_fit`,
  `paper_off_axis_capsule_fit`, `paper_flat_capped_cylinder_axis_fit`,
  `paper_tapered_frustum_fit`, and `paper_asymmetric_trapezoid_fit` as synthetic offline cases.
  This is synthetic offline primitive-fit accounting only; this is not `paper_faithful_offline`,
  package generation, Newton runtime support, real-USD evidence, benchmark evidence, or
  collision-quality validation.
- The current executable surface can run the Batch C fixture-breadth cost/search/stop slice inside
  `cpd_paper_offline_report`, adding `paper_branching_cost_order`,
  `paper_equal_cost_queue_tie`, and `paper_nonzero_threshold_block` as synthetic offline cases.
  This is not `paper_faithful_offline`, package generation, Newton runtime support, real-USD
  evidence, benchmark evidence, or collision-quality validation.
- The current executable surface can run the Batch D fixture-breadth component-pair slice inside
  `cpd_paper_offline_report`, adding `paper_component_pair_multi_candidate_order` and
  `paper_component_pair_cap_skipped` as synthetic offline cases. This is not
  `paper_faithful_offline`, package generation, Newton runtime support, real-USD evidence,
  benchmark evidence, or collision-quality validation.
- The current executable surface can run the Batch E fixture-breadth postprocess slice inside
  `cpd_paper_offline_report`, adding `paper_rotated_nested_primitive` and
  `paper_cross_type_enclosure_boundary` as synthetic offline cases. This is
  not `paper_faithful_offline`, package generation, Newton runtime support, real-USD evidence,
  benchmark evidence, or collision-quality validation.
- The current executable surface can run the command-only synthetic fixture-breadth completion
  review inside `cpd_paper_offline_report`. It closes only the planned Batch A-E fixture-breadth
  gate and keeps the report partial with `paper_faithful_offline_supported: false`. Its nested
  review payload records the planning-only `paper_faithful_offline_generalization_plan` as the
  follow-up gate for that closed review. This is not
  `paper_faithful_offline`, full CPD reproduction, package generation, Newton runtime support,
  real-USD evidence, benchmark evidence, collision-quality validation, deployment readiness, or
  safety certification.
- The current executable surface can run the command-only CPD paper offline generalization-plan
  table inside `cpd_paper_offline_report`. It closes only
  `paper_faithful_offline_generalization_plan`, keeps the report partial, keeps
  `paper_faithful_offline_supported: false`, and now reports the first unresolved runtime-lane
  gate as
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract`
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
  runtime-admissibility contract, offline/static Newton shape-mapping preflight,
  offline/static Newton shape-mapping descriptor, offline/static Newton shape runtime-boundary
  preflight, offline/report-scoped Newton shape runtime-construction, offline/static Newton shape
  runtime builder-preflight, offline/report-only recording-builder construction,
  offline/static Newton engine-builder boundary-preflight, bounded Newton/Warp environment-probe,
  bounded source-AST API-surface, report-only engine-builder entry, report-only skipped-smoke,
  report-only skipped-runtime-execution, report-only runtime-lane review, and report-only
  configured-runtime design/preflight/validation contracts.
  The
  runtime-construction slice records exactly one repo-local `NewtonShapeMapping.to_dict()` report
  record for the synthetic `paper_single_box` box descriptor while keeping Newton engine shape
  objects, builder shape calls, and Newton runtime execution at zero. The builder-preflight slice
  records exactly one JSON-safe future box builder call plan while keeping builder calls, Newton
  engine shape objects, and Newton runtime execution at zero. The builder-construction slice
  records exactly one JSON-safe repo-local recording-builder `add_shape_box` call artifact through
  a fake Warp-like module while keeping real Newton imports, Newton `ModelBuilder`
  instantiation, Newton engine shape objects, real Newton builder shape calls, and Newton runtime
  execution at zero.
- The current executable surface can also run
  `paper_generalization_batch_a_source_policy` inside `cpd_paper_offline_report`. It closes only
  that source-policy gate by adding an offline source-policy matrix for deterministic synthetic
  meshes. The matrix records exact-coordinate dedup policy, source-face intake/remap policy,
  concave-polygon rejection, and source-face `Q` aggregation accounting. The report remains
  partial and keeps `paper_faithful_offline_supported: false`. At that source-policy stage the
  follow-up gate was `paper_generalization_batch_b_primitive_fit_engine`. This is not robust mesh cleanup, general
  polygon intake, `paper_faithful_offline`, full CPD reproduction, package generation, Newton
  runtime support, real-USD evidence, benchmark evidence, collision-quality validation, deployment
  readiness, or safety certification.
- The current executable surface can also run
  `paper_generalization_batch_b_primitive_fit_engine` inside `cpd_paper_offline_report`. It closes
  only that primitive-fit engine gate by adding an offline matrix over deterministic in-memory
  probes for all six paper primitive names. The matrix records candidate generation,
  selected-candidate accounting, containment checks, finite numeric fields, and the offline-only
  boundary for paper-only primitives. The report remains partial, keeps
  `paper_faithful_offline_supported: false`, and previously advanced the next required gate to
  `paper_generalization_batch_c_search_engine`. This is not robust primitive fitting,
  `paper_faithful_offline`, full CPD reproduction, package generation, Newton runtime support,
  real-USD evidence, benchmark evidence, collision-quality validation, deployment readiness, or
  safety certification.
- The current executable surface can also run
  `paper_generalization_batch_c_search_engine` inside `cpd_paper_offline_report`. It closes only
  that search-engine gate by adding an offline matrix over existing deterministic topology queue,
  weighted-priority, equal-cost tie, threshold-stop, and component-pair traces. The report remains
  partial, keeps `paper_faithful_offline_supported: false`, and at that stage advanced the next
  required gate to `paper_generalization_batch_d_postprocess_policy`. This is not a generalized
  optimizer,
  `paper_faithful_offline`, full CPD reproduction, package generation, Newton runtime support,
  real-USD evidence, benchmark evidence, collision-quality validation, deployment readiness, or
  safety certification.
- The current executable surface can also run
  `paper_generalization_batch_d_postprocess_policy` inside `cpd_paper_offline_report`. It closes
  only that postprocess-policy gate by adding an offline matrix over existing deterministic
  postprocess audit fixtures. The matrix records identity-axis OBB culling, rotated OBB culling,
  conservative unsupported cross-type no-cull accounting, before/after primitive counts, cull or
  unsupported reasons, and false package, Newton, real-USD, and benchmark triggers. The report
  remains partial, keeps `paper_faithful_offline_supported: false`, and at that stage advanced the
  next required gate to `paper_generalization_batch_e_package_boundary_readiness`. This is not a
  general primitive containment library, `paper_faithful_offline`, full CPD reproduction, package
  generation, Newton runtime support, real-USD evidence, benchmark evidence, collision-quality
  validation, deployment readiness, or safety certification.
- The current executable surface can also run
  `paper_generalization_batch_e_package_boundary_readiness` inside
  `cpd_paper_offline_report`. It closes only that package-boundary readiness gate by adding an
  offline package-boundary readiness matrix before package conversion. The matrix records that the
  current source-policy, primitive-fit, search-engine, and postprocess-policy outputs are audit
  matrices rather than a durable changed-decomposition output contract, keeps package generation
  and Newton runtime execution blocked, and advances the next required gate to
  `paper_offline_changed_decomposition_output_contract`. This was package-boundary accounting, not
  package readiness, Newton readiness, `paper_faithful_offline`, full CPD reproduction, package generation, Newton
  runtime support, real-USD evidence, benchmark evidence, collision-quality validation, deployment
  readiness, or safety certification.
- The current executable surface can also run
  `paper_offline_changed_decomposition_output_contract` inside `cpd_paper_offline_report`. It
  closes only that output-contract gate by adding an offline changed-decomposition output contract,
  not a `CollisionPackage`. The contract records synthetic toy fixture decomposition rows, stable
  offline primitive ids, source-face/group ids, selected paper primitive audit fields, explicit
  postprocess state rows, and package/Newton/real-USD/benchmark false triggers. The report remains
  partial, keeps `paper_faithful_offline_supported: false`, and advances the next required gate to
  `paper_package_adapter_contract`. This is not package readiness, Newton readiness,
  `paper_faithful_offline`, full CPD reproduction, package generation, Newton
  runtime support, real-USD evidence, benchmark evidence, collision-quality validation, deployment
  readiness, or safety certification.
- The current executable surface can also run `paper_package_adapter_contract` inside
  `cpd_paper_offline_report`. It closes only that adapter-contract gate by adding a command-only
  offline package-adapter contract, not a `CollisionPackage`. The contract consumes the offline
  changed-decomposition primitive records, emits 16 adapter decision rows, classifies all current
  `trapezoidal_prism` / `offline_only_unmapped` rows as `later_policy_required`, keeps package
  generation and Newton runtime execution blocked. At that adapter-contract stage the follow-up
  gate was `paper_package_adapter_unsupported_primitive_policy`; after the unsupported-primitive
  policy the follow-up gate was `paper_package_conversion_mapped_subset_plan`, which is now closed
  by the mapped-subset planning table below. This is not package readiness, Newton
  readiness, runtime admissibility, `paper_faithful_offline`, full CPD reproduction, package
  generation, Newton runtime support, real-USD evidence, benchmark evidence, collision-quality
  validation, deployment readiness, or safety certification.
- The current executable surface can also run
  `paper_package_adapter_unsupported_primitive_policy` inside `cpd_paper_offline_report`. It
  closes only that unsupported-primitive policy gate by adding a command-only offline policy table,
  not a `CollisionPackage`. The policy classifies all six paper primitive families, keeps the
  current 16 `trapezoidal_prism` / `offline_only_unmapped` rows offline with
  `block_package_conversion`, records zero package-candidate rows, keeps package generation and
  Newton runtime execution blocked, and at that stage advanced the next required gate to
  `paper_package_conversion_mapped_subset_plan`. This is not package readiness, Newton readiness,
  runtime admissibility, approximation support, `paper_faithful_offline`, full CPD reproduction,
  package generation, Newton runtime support, real-USD evidence, benchmark evidence,
  collision-quality validation, deployment readiness, or safety certification.
- The current executable surface can also run
  `paper_package_conversion_mapped_subset_plan` inside `cpd_paper_offline_report`. It closes only
  that mapped-subset planning gate by adding a command-only offline package-conversion planning
  table, not a `CollisionPackage`. The table identifies `oriented_bounding_box`, `sphere`, and
  `capsule` as native-family review rows, keeps the current 16
  `trapezoidal_prism` / `offline_only_unmapped` rows offline, records zero current
  package-conversion candidates, keeps package generation and Newton runtime execution blocked,
  and at that stage advanced the next required gate to
  `paper_mapped_subset_conversion_candidate_matrix`. This is not package readiness, Newton
  readiness, runtime admissibility, approximation support, `paper_faithful_offline`, full CPD
  reproduction, package generation, Newton runtime support, real-USD evidence, benchmark evidence,
  collision-quality validation, deployment readiness, or safety certification.
- The current executable surface can also run
  `paper_mapped_subset_conversion_candidate_matrix` inside `cpd_paper_offline_report`. It closes
  only that candidate-matrix gate by adding a command-only offline review matrix before any package
  generation. The matrix converts the mapped-subset plan into explicit family and current-record
  review rows, records three future-family review rows, keeps the current 16
  `trapezoidal_prism` / `offline_only_unmapped` rows blocked and offline, records zero current
  package-conversion candidates, keeps PrimitiveSpec generation, CollisionPackage generation,
  runtime admissibility, Newton runtime execution, real USD, benchmark, and collision-quality
  triggers false, and at that stage advanced the next required gate to
  `paper_mapped_subset_adapter_preflight_contract`. This is not package readiness, Newton
  readiness, runtime admissibility, approximation support, `paper_faithful_offline`, full CPD
  reproduction, package generation, Newton runtime support, real-USD evidence, benchmark evidence,
  collision-quality validation, deployment readiness, or safety certification.
- The current executable surface can also run
  `paper_mapped_subset_adapter_preflight_contract` inside `cpd_paper_offline_report`. It closes
  only that adapter-preflight gate with a command-only offline contract, not `PrimitiveSpec`
  generation and not a `CollisionPackage`. It records future adapter requirements, records no-op
  behavior for the current zero package-conversion-candidate state, keeps all current unmapped
  trapezoidal-prism rows offline, keeps package generation disabled, keeps PrimitiveSpec
  generation, CollisionPackage generation, runtime admissibility, Newton runtime execution, real
  USD, benchmark, and collision-quality triggers false, and advances the next required gate to
  `paper_mapped_subset_primitivespec_dry_run_contract`. This is not package readiness, Newton
  readiness, runtime admissibility, approximation support, `PrimitiveSpec` readiness,
  `paper_faithful_offline`, full CPD reproduction, package generation, Newton runtime support,
  real-USD evidence, benchmark evidence, collision-quality validation, deployment readiness, or
  safety certification.
- The current executable surface can also run
  `paper_mapped_subset_primitivespec_dry_run_contract` inside `cpd_paper_offline_report`. It
  closes only that PrimitiveSpec dry-run gate with a command-only offline contract, not real
  `PrimitiveSpec` generation and not a `CollisionPackage`. It records future PrimitiveSpec shape
  requirements for OBB/box, sphere, and capsule, keeps capped cylinder and frustum blocked behind
  an approximation policy, keeps current unmapped trapezoidal-prism rows offline/no-op, records
  zero current PrimitiveSpec candidates, records zero generated PrimitiveSpec rows, keeps
  CollisionPackage generation, runtime admissibility, Newton runtime execution, real USD,
  benchmark, and collision-quality triggers false, and advances the next required gate to
  `paper_mapped_subset_primitivespec_validation_contract`. This is not package readiness, Newton
  readiness, runtime admissibility, approximation support, `PrimitiveSpec` readiness,
  `paper_faithful_offline`, full CPD reproduction, package generation, Newton runtime support,
  real-USD evidence, benchmark evidence, collision-quality validation, deployment readiness, or
  safety certification.
- The current executable surface can also run
  `paper_mapped_subset_primitivespec_validation_contract` inside `cpd_paper_offline_report`. It
  closes only that PrimitiveSpec validation gate with a command-only offline validation contract,
  not real `PrimitiveSpec` generation and not a `CollisionPackage`. It validates the dry-run
  field list, mapped future shape labels, six family rows, 16 current no-op rows, source
  traceability, zero current candidates, zero generated PrimitiveSpecs, and false
  runtime/evaluation triggers, and advances the next required gate to
  `paper_mapped_subset_primitivespec_generation_preflight_contract`. This is not package
  readiness, Newton readiness, runtime admissibility, approximation support, `PrimitiveSpec`
  readiness, `paper_faithful_offline`, full CPD reproduction, package generation, Newton runtime
  support, real-USD evidence, benchmark evidence, collision-quality validation, deployment
  readiness, or safety certification.
- The current executable surface can also run
  `paper_mapped_subset_primitivespec_generation_preflight_contract` inside
  `cpd_paper_offline_report`. It closes only that PrimitiveSpec generation-preflight gate with a
  command-only offline preflight contract, not real `PrimitiveSpec` generation and not a
  `CollisionPackage`. It records future native-family generation requirements for OBB/box,
  sphere, and capsule, keeps capped cylinder and frustum blocked behind approximation policy,
  keeps trapezoidal prism no-op/unmapped, keeps current generation candidates at zero, keeps
  generated PrimitiveSpecs, generated CollisionPackages, and runtime-admissibility checks at zero,
  and advances the next required gate to `paper_mapped_subset_primitivespec_generation_contract`.
  This is not package readiness, Newton readiness, runtime admissibility, approximation support,
  `PrimitiveSpec` readiness, real `PrimitiveSpec` generation, `paper_faithful_offline`, full CPD
  reproduction, package generation, Newton runtime support, real-USD evidence, benchmark evidence,
  collision-quality validation, deployment readiness, or safety certification.
- The current executable surface can also run
  `paper_mapped_subset_primitivespec_generation_contract` inside `cpd_paper_offline_report`. It
  closes only that PrimitiveSpec generation contract with command-only offline template rows, not
  runtime `PrimitiveSpec` objects and not a `CollisionPackage`. It records future native-family
  templates for box/sphere/capsule, keeps capped cylinder and frustum blocked behind later
  approximation policy, keeps trapezoidal prism and all current unmapped rows offline/no-op, keeps
  generated runtime PrimitiveSpecs, generated CollisionPackages, runtime-admissibility checks,
  Newton runtime, real-USD loading, benchmark runs, collision-quality measurement, and
  deployment/certification claims at zero or false, and advances the next required gate to
  `paper_mapped_subset_primitivespec_candidate_source_contract`. This is not package readiness,
  Newton readiness, runtime admissibility, approximation support, `PrimitiveSpec` readiness, real
  `PrimitiveSpec` generation, `paper_faithful_offline`, full CPD reproduction, package generation,
  Newton runtime support, real-USD evidence, benchmark evidence, collision-quality validation,
  deployment readiness, or safety certification.
- The current executable surface can also run
  `paper_mapped_subset_primitivespec_candidate_source_contract` inside
  `cpd_paper_offline_report`. It closes only that PrimitiveSpec candidate-source gate with a
  command-only offline source audit, not real `PrimitiveSpec` generation and not a
  `CollisionPackage`. It records three future-only native template candidate-source rows, two
  blocked approximation-policy family source rows, one no-op trapezoidal-prism family source row,
  and 16 traceable but ineligible current `trapezoidal_prism` / `offline_only_unmapped` source
  rows. It keeps eligible current PrimitiveSpec candidate sources, generated PrimitiveSpecs,
  generated CollisionPackages, runtime-admissibility checks, Newton runtime, real-USD loading,
  benchmark runs, collision-quality measurement, and deployment/certification claims at zero or
  false, and advances the next required gate to
  `paper_mapped_subset_native_current_fixture_contract`. This is not package readiness, Newton
  readiness, runtime admissibility, approximation support, `PrimitiveSpec` readiness, real
  `PrimitiveSpec` generation, `paper_faithful_offline`, full CPD reproduction, package generation,
  Newton runtime support, real-USD evidence, benchmark evidence, collision-quality validation,
  deployment readiness, or safety certification.
- The current executable surface can also run
  `paper_mapped_subset_native_current_fixture_contract` inside `cpd_paper_offline_report`. It
  closes only that native-current fixture source gate with a command-only offline contract, not
  real `PrimitiveSpec` generation and not a `CollisionPackage`. It records exactly one synthetic
  `paper_single_box` selected OBB/box source row traced to the OBB template, one eligible current
  candidate source, one report-only PrimitiveSpec generation candidate, zero generated
  PrimitiveSpecs, zero generated CollisionPackages, and zero runtime-admissibility checks. It
  led to the later
  `paper_mapped_subset_primitivespec_native_fixture_generation_contract` gate. This is not package
  readiness, Newton readiness, runtime admissibility, approximation support, `PrimitiveSpec`
  readiness, real `PrimitiveSpec` generation, `paper_faithful_offline`, full CPD reproduction,
  package generation, Newton runtime support, real-USD evidence, benchmark evidence,
  collision-quality validation, deployment readiness, or safety certification.
- The current executable surface can also run
  `paper_mapped_subset_primitivespec_native_fixture_generation_contract` inside
  `cpd_paper_offline_report`. It closes only that native-fixture generation gate with a
  command-only offline contract, not real runtime `PrimitiveSpec` object creation and not a
  `CollisionPackage`. It emits exactly one JSON-serializable, report-only PrimitiveSpec-like dict
  shaped like `PrimitiveSpec.to_dict()` for the deterministic synthetic `paper_single_box`
  OBB/box source row. It keeps generated runtime PrimitiveSpecs, generated CollisionPackages,
  runtime-admissibility checks, Newton runtime, real-USD loading, benchmark runs,
  collision-quality measurement, and deployment/certification claims at zero or false. It
  advances the next required gate to
  `paper_mapped_subset_primitivespec_native_fixture_serialization_contract`. This is not package
  readiness, Newton readiness, runtime admissibility, approximation support, `PrimitiveSpec`
  readiness, real runtime PrimitiveSpec generation, `paper_faithful_offline`, full CPD
  reproduction, package generation, Newton runtime support, real-USD evidence, benchmark
  evidence, collision-quality validation, deployment readiness, or safety certification.
- The current executable surface can also run
  `paper_mapped_subset_primitivespec_native_fixture_serialization_contract` inside
  `cpd_paper_offline_report`. It closes only that native-fixture serialization gate with a
  command-only offline contract, not runtime `PrimitiveSpec` object creation and not a
  `CollisionPackage`. It validates exactly one report-only PrimitiveSpec-like dict for the
  deterministic synthetic `paper_single_box` OBB/box row using strict canonical JSON
  serialization (`allow_nan=False`, sorted keys, compact separators) and round-trip equality. It
  keeps generated runtime PrimitiveSpecs, generated CollisionPackages, runtime-admissibility
  checks, Newton runtime, real-USD loading, benchmark runs, collision-quality measurement, and
  deployment/certification claims at zero or false. It advances the next required gate to
  `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`. The current executable
  surface can also run `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`
  inside `cpd_paper_offline_report`. It closes only that runtime-boundary preflight gate with a
  command-only offline contract, records one later runtime `PrimitiveSpec` construction candidate
  for the same deterministic synthetic `paper_single_box` OBB/box row, keeps runtime construction
  disallowed in the current gate, and keeps generated runtime PrimitiveSpecs, generated
  CollisionPackages, runtime-admissibility checks, Newton runtime, real-USD loading, benchmark
  runs, collision-quality measurement, and deployment/certification claims at zero or false. It
  advances the next required gate to
  `paper_mapped_subset_primitivespec_runtime_construction_contract`. The current executable
  surface can also run `paper_mapped_subset_primitivespec_runtime_construction_contract` inside
  `cpd_paper_offline_report`. It closes only that single-fixture runtime-construction gate,
  constructs exactly one runtime `PrimitiveSpec` object from the canonical synthetic
  `paper_single_box` OBB/box preflight JSON after checking the runtime-boundary preflight row's
  canonical JSON SHA-256 fingerprint, stores only `PrimitiveSpec.to_dict()` in the report, records
  runtime PrimitiveSpec generation counts as one, keeps generated CollisionPackages and
  runtime-admissibility checks at zero, and advances the next required gate to
  `paper_mapped_subset_collision_package_generation_preflight_contract`. This is not package
  readiness, Newton readiness, runtime admissibility, approximation support, general
  `PrimitiveSpec` readiness, `paper_faithful_offline`, full CPD reproduction, package generation,
  Newton runtime support, real-USD evidence, benchmark evidence, collision-quality validation,
  deployment readiness, or safety certification.
- The current executable surface can also run
  `paper_mapped_subset_collision_package_generation_preflight_contract` inside
  `cpd_paper_offline_report`. It closes only that single-fixture package-generation preflight
  gate, consumes the runtime-construction row's `PrimitiveSpec.to_dict()` payload, records exactly
  one later package-generation candidate for the synthetic `paper_single_box` OBB/box row, keeps
  package generation disallowed in the current gate, keeps generated CollisionPackages and
  runtime-admissibility checks at zero, and advances the next required gate to
  `paper_mapped_subset_collision_package_generation_contract`. This is not package readiness,
  Newton readiness, runtime admissibility, approximation support, general `PrimitiveSpec`
  readiness, `paper_faithful_offline`, full CPD reproduction, Newton runtime support, real-USD
  evidence, benchmark evidence, collision-quality validation, deployment readiness, or safety
  certification.
- The current executable surface can also run
  `paper_mapped_subset_collision_package_generation_contract` inside `cpd_paper_offline_report`.
  It closes only that single-fixture offline package-generation gate by constructing exactly one
  synthetic, report-scoped `CollisionPackage.to_dict()` artifact for the deterministic
  `paper_single_box` OBB/box row. It records `generated_collision_package_count: 1`, keeps
  runtime-admissibility checks at zero, marks the package status as
  `offline_synthetic_candidate_runtime_admissibility_not_checked`, records that only the `box` fixture was
  evaluated in this gate, and advances the next required gate to
  `paper_mapped_subset_runtime_admissibility_preflight_contract`. This is not package readiness,
  Newton readiness, runtime admissibility, paper primitive vocabulary coverage, approximation
  support, general `PrimitiveSpec` readiness, `paper_faithful_offline`, full CPD reproduction,
  Newton runtime support, real-USD evidence, benchmark evidence, collision-quality validation,
  deployment readiness, or safety certification.
- The current executable surface can also run
  `paper_mapped_subset_runtime_admissibility_preflight_contract` inside
  `cpd_paper_offline_report`. It closes only that single-fixture offline preflight gate by
  consuming the one synthetic `paper_single_box` `CollisionPackage.to_dict()` artifact, validating
  its identity, source metadata, schema, primitive subset, and false trigger flags, and recording
  exactly one later runtime-admissibility candidate row without copying the full package dict. It
  keeps runtime-admissibility checks, Newton runtime, real-USD loading, benchmark runs,
  collision-quality measurement, deployment, and certification triggers at zero or false, and
  advances the next required gate to `paper_mapped_subset_runtime_admissibility_contract`. This is
  not package readiness, not Newton readiness, not Newton support, not Newton execution, not
  runtime admissibility, not paper primitive vocabulary coverage, not approximation support, not
  `paper_faithful_offline`, not full CPD reproduction, not real-USD evidence, not benchmark
  evidence, not collision-quality validation, not deployment readiness, and not safety
  certification.
- The current executable surface can also run
  `paper_mapped_subset_runtime_admissibility_contract` inside `cpd_paper_offline_report`. It
  closes only that single-fixture offline/static gate by consuming the preflight row for the same
  synthetic `paper_single_box` `CollisionPackage.to_dict()` artifact and recording one finite
  center, right-handed orthonormal-axis, positive-half-extent, target box-schema, source-face,
  containment, and volume check. It records `runtime_admissibility_check_count: 1` as a
  report-only static check, keeps runtime execution, Newton shape mapping, Newton runtime,
  real-USD loading, benchmark runs, collision-quality measurement, deployment, and certification
  triggers at zero or false, keeps `paper_faithful_offline` blockers separate from runtime-lane
  gates, and advances the next required runtime-lane gate to
  `paper_mapped_subset_newton_shape_mapping_preflight_contract`. This is not package readiness,
  not Newton readiness, not Newton support, not Newton execution, not real-USD evidence, not
  benchmark evidence, not collision-quality validation, not paper primitive vocabulary coverage,
  not approximation support, not `paper_faithful_offline`, not full CPD reproduction, not
  deployment readiness, and not safety certification.
- The current executable surface can also run
  `paper_mapped_subset_newton_shape_mapping_preflight_contract` inside
  `cpd_paper_offline_report`. It closes only that single-fixture offline/static preflight gate by
  consuming the runtime-admissibility row for the same synthetic `paper_single_box` box artifact
  and recording one mapper-handoff row with target kind `box`, center, axes, dimensions, and
  half-extents field checks. It records `mapping_attempt_count: 0`,
  `newton_mapping_record_count: 0`, and `newton_runtime_execution_count: 0`, keeps Newton support
  claims false, and advances the next required runtime-lane gate to
  `paper_mapped_subset_newton_shape_mapping_contract`. This is not Newton readiness, not Newton
  support, not Newton execution, not real-USD evidence, not benchmark evidence, not
  collision-quality validation, not paper primitive vocabulary coverage, not approximation
  support, not `paper_faithful_offline`, not full CPD reproduction, not deployment readiness, and
  not safety certification.
- The current executable surface can also run
  `paper_mapped_subset_newton_shape_mapping_contract` inside `cpd_paper_offline_report`. It
  closes only that single-fixture offline/static descriptor contract by consuming the preflight row
  for the same synthetic `paper_single_box` box artifact and recording one report-scoped
  `newton_shape_descriptor_dict` for target kind `box`. It records `mapping_attempt_count: 0`,
  `newton_mapping_record_count: 0`, `newton_shape_object_count: 0`, and
  `newton_runtime_execution_count: 0`, keeps Newton support claims false, and advances the next
  required runtime-lane gate to
  `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`. This is not Newton
  readiness, not Newton support, not Newton execution, not real-USD evidence, not benchmark
  evidence, not collision-quality validation, not paper primitive vocabulary coverage, not
  approximation support, not `paper_faithful_offline`, not full CPD reproduction, not deployment
  readiness, and not safety certification.
- The current executable surface can also run
  `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract` inside
  `cpd_paper_offline_report`. It closes only that single-fixture offline/static runtime-boundary
  preflight by consuming the report-scoped static descriptor row, recording one later Newton shape
  runtime-construction candidate, keeping Newton shape object construction and Newton execution at
  zero, and advancing the next required runtime-lane gate to
  `paper_mapped_subset_newton_shape_runtime_construction_contract`. This is not Newton readiness,
  not Newton support, not Newton execution, not real-USD evidence, not benchmark evidence, not
  collision-quality validation, not paper primitive vocabulary coverage, not approximation
  support, not `paper_faithful_offline`, not full CPD reproduction, not deployment readiness, and
  not safety certification.
- The current executable surface can also run
  `paper_mapped_subset_newton_shape_runtime_construction_contract` inside
  `cpd_paper_offline_report`. It closes only that single-fixture offline/report-scoped runtime
  construction gate by consuming the runtime-boundary preflight row and constructing exactly one
  repo-local `NewtonShapeMapping.to_dict()` report record for the synthetic `paper_single_box` box
  descriptor. It keeps Newton mapper calls, Newton engine shape object construction, Newton
  builder shape calls, and Newton execution at zero, and advances the next required runtime-lane
  gate to `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`. This is not
  Newton readiness, not Newton support, not Newton execution, not real-USD evidence, not benchmark
  evidence, not collision-quality validation, not paper primitive vocabulary coverage, not
  approximation support, not `paper_faithful_offline`, not full CPD reproduction, not deployment
  readiness, and not safety certification.
- The current executable surface can also run
  `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract` inside
  `cpd_paper_offline_report`. It closes only that single-fixture offline/static builder-preflight
  gate by consuming the repo-local `NewtonShapeMapping.to_dict()` mapping record and recording one
  JSON-safe future box builder call plan with signature fields `body`, `xform`, `hx`, `hy`, and
  `hz`. It keeps builder calls, Newton engine shape object construction, and Newton execution at
  zero, and advances the next required runtime-lane gate to
  `paper_mapped_subset_newton_shape_runtime_builder_construction_contract`. This is not Newton
  readiness, not Newton support, not Newton execution, not real-USD evidence, not benchmark
  evidence, not collision-quality validation, not paper primitive vocabulary coverage, not
  approximation support, not `paper_faithful_offline`, not full CPD reproduction, not deployment
  readiness, and not safety certification.
- The current executable surface can also run
  `paper_mapped_subset_newton_shape_runtime_builder_construction_contract` inside
  `cpd_paper_offline_report`. It closes only that single-fixture offline/report-only
  builder-construction gate by consuming the builder-preflight row, reconstructing the repo-local
  mapping record, calling only the repo-local static shape dispatch helper with a recording
  builder and fake Warp-like module, and recording one JSON-safe fake `add_shape_box` call
  artifact. It records one recording-builder shape call and one repo-local helper call, but keeps
  real Newton imports, Newton `ModelBuilder` instantiation, Newton engine shape object
  construction, real Newton builder shape calls, and Newton execution at zero. At that stage it
  advanced the next required runtime-lane gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract`. This is
  not Newton readiness, not Newton support, not Newton execution, not real-USD evidence, not
  benchmark evidence, not collision-quality validation, not paper primitive vocabulary coverage,
  not approximation support, not `paper_faithful_offline`, not full CPD reproduction, not
  deployment readiness, and not safety certification.
- The current executable surface can also run
  `paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract` inside
  `cpd_paper_offline_report`. It closes only that single-fixture offline/static boundary-preflight
  gate by consuming the recording-builder artifact and recording the future real Newton
  `ModelBuilder` / `add_shape_box` boundary requirements before any environment probe. It keeps
  real Newton imports, Newton `ModelBuilder` instantiation, real builder shape calls, model
  finalization, collision pipeline calls, and Newton execution at zero. At that stage it advanced
  the next required runtime-lane gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract`; the later
  environment-probe, API-surface, entry, smoke, runtime-execution, runtime-lane review, and
  configured-runtime design/preflight/validation slices below now advance the current next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract`.
  This is
  not Newton readiness, not Newton support, not Newton execution, not real-USD evidence, not
  benchmark evidence, not collision-quality validation, not paper primitive vocabulary coverage,
  not approximation support, not `paper_faithful_offline`, not full CPD reproduction, not
  deployment readiness, and not safety certification.
- The current executable surface can also run
  `paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract` inside
  `cpd_paper_offline_report`. It closes only that single-fixture bounded environment-provenance
  gate by consuming the engine-builder boundary-preflight row and recording configured-source-dir
  status plus JSON-safe Newton/Warp `find_spec` provenance shape. The default report remains
  no-config, imports no real Newton or Warp runtime, instantiates no `newton.ModelBuilder`, makes
  no real builder shape calls, finalizes no model, creates no collision pipeline, and runs no
  Newton code. At that stage it advanced the stage-local next required runtime-lane gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract`; the later
  API-surface, entry, smoke, runtime-execution, runtime-lane review, and configured-runtime design/preflight/validation
  slices below advance the current next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract`.
  This is not
  Newton readiness, not Newton support, not Newton execution, not real-USD evidence, not
  benchmark evidence, not collision-quality validation, not paper primitive vocabulary coverage,
  not approximation support, not `paper_faithful_offline`, not full CPD reproduction, not
  deployment readiness, and not safety certification.
- The current executable surface can also run
  `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract` inside
  `cpd_paper_offline_report`. It closes only that single-fixture bounded source-AST API-surface
  gate by consuming the environment-probe row and recording default no-config API-surface status
  for the future `newton.ModelBuilder` / `add_shape_box` boundary. When a Newton source directory
  is explicitly passed, this lane may read source files and parse AST only. It imports no real
  Newton or Warp runtime, instantiates no `newton.ModelBuilder`, makes no real builder shape
  calls, finalizes no model, creates no collision pipeline, and runs no Newton code. At that
  stage it advanced the next required runtime-lane gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract`.
  That gate has now been closed as a deliberately consolidated report-only entry audit.
  It records `entry_decision: defer_real_runtime_entry`, keeps real Newton/Warp imports,
  `newton.ModelBuilder`, Newton engine shape objects, real builder calls, model finalization,
  collision pipeline calls, and Newton execution at zero. The bounded smoke slice then records
  `smoke_decision: skip_real_runtime_smoke`, keeps all real runtime-smoke attempts and Newton
  engine shape objects/runtime execution at zero. The bounded runtime-execution slice records
  `runtime_execution_decision: skip_real_runtime_execution`, keeps all real runtime-execution
  attempts and Newton execution at zero. The bounded runtime-lane review slice then records
  `runtime_lane_review_decision: keep_real_runtime_execution_blocked`, keeps skipped execution out
  of runtime-compatibility wording. The bounded configured-runtime design slice records required
  runtime inputs for that same lineage while keeping runtime config validation false and all real
  runtime counters zero. The bounded configured-runtime preflight slice records the preflight
  decision while still reading no config, resolving no runtime source/device, importing no
  Newton/Warp runtime, and running no Newton code. The bounded configured-runtime validation slice
  then records the default missing-config validation result, reads no config file or environment,
  resolves no runtime source/device, imports no Newton/Warp runtime, and runs no Newton code; it
  advances the current next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract`.
  This is not Newton readiness, not Newton support, not Newton execution, not runtime
  compatibility, not real-USD evidence, not benchmark evidence, not collision-quality validation,
  not paper primitive vocabulary coverage, not approximation support, not `paper_faithful_offline`,
  not full CPD reproduction, not deployment readiness, and not safety certification.
- The current executable surface can convert the CPD-like geometry report into a common collision
  package and run `newton_contact_smoke`, a contact-only Newton canary for representative
  Newton-mapped primitive types.
- The current executable surface can run `newton_drop_settle`, a named task-level Newton smoke
  diagnostic over the capped bed CPD-like collision package, with explicit solver settings,
  final-contact, final-speed, support-height metrics, and failure labels.
- The current executable surface can run `newton_sphere_rain`, a named task-level Newton smoke
  diagnostic over the capped bed CPD-like collision package, with explicit solver settings,
  sphere-grid initial conditions, package-probe contact-density proxy metrics, and failure labels.
- The current executable surface can map and construct Newton diagnostic shapes for a synthetic
  native primitive bundle containing `box`, `sphere`, `capsule`, `cylinder`, `cone`, and
  `ellipsoid`, and can run clean-env contact, drop/settle, and sphere-rain smokes for that
  synthetic package. This is diagnostic-path evidence, not broad asset evidence or proof that the
  CPD-like generator emits the new native kinds by default.
- The current executable surface can run `cpd_like_newton_native_fitting_comparison`, an opt-in
  deterministic synthetic comparison where the six-kind Newton-native subset selects `cylinder`,
  `cone`, and `ellipsoid` on toy meshes and maps the resulting one-primitive packages through
  Newton shape mapping. The report now also includes a squat-cylinder fixture that exercises the
  controlled cylinder-axis search, plus candidate weighted-volume audit tables that explain those
  toy selections under the current support-aware surrogate primitive-choice rule. This is
  synthetic fitting and diagnostic accounting evidence, not collision-quality evidence, default
  asset behavior, or bed/Franka improvement evidence.
- The current executable surface can run `cpd_like_real_usd_native_fitting_comparison`, a
  real-USD old/new diagnostic report over capped `bed_dev_smoke` and capped
  `franka_import_smoke` first-mesh scope. The current support-aware run keeps bed at `32` boxes in
  both lanes and capped Franka at `32` boxes in both lanes, while reporting three cheaper raw-cost
  Franka cylinder candidates as support-blocked. This is not evidence that native primitives
  improved bed or Franka. The report can now include per-selected-cluster candidate audit
  summaries that distinguish raw-cost rank from support-aware selection rank.
- The current executable surface can run `cpd_like_real_usd_candidate_loss_diagnosis`, a
  per-selected-cluster diagnosis report for capped real-USD native lanes. The current diagnosis
  records why remaining box-selected clusters beat extension candidates under the current
  surrogate and records the three Franka clusters where cheaper raw-cost `cylinder` candidates are
  blocked by support admissibility. This is surrogate diagnostic accounting, not collision-quality
  evidence or whole-robot collider-quality evidence. The report now also includes next-slice
  triage metadata for near-miss extension candidates and low-support native-extension cases; that
  triage is planning metadata, not an optimizer or quality evidence.
- The current executable surface can run `newton_real_usd_native_contact_comparison`, which
  requires full Newton mapping before contact canaries for the capped bed and capped Franka
  old/new packages.
- The current executable surface can run `newton_real_usd_native_task_comparison`, which gates
  drop/settle and sphere-rain behind contact canary success for the same capped real-USD packages.
  This is named task-smoke evidence under recorded settings, not collision-quality validation,
  benchmark evidence, or whole-robot collider-quality evidence.
- The current clean local Python/Newton environment-readiness evidence is `smoke_passed` for
  `/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310`, Newton source commit
  `96713fa965463b69c229a4d30582c733ff3526bb`, and local RTX 4090 hardware.
- The 2026-05-14 CPD-like bed smoke record reports `smoke_passed` for the first 256 extracted bed
  mesh triangles, reduced to 32 restricted primitives, using the clean Newton Python environment.
- The 2026-05-14 Newton drop/settle record reports `smoke_passed` for the capped bed CPD-like
  collision package in the clean Newton Python environment, with all 32 primitives mapped and no
  floor-breach or unsettled failure label under the recorded `0.05m` support-height tolerance and
  `0.05m/s` final-speed threshold.
- The 2026-05-15 Newton sphere-rain record reports `smoke_passed` for the capped bed CPD-like
  collision package in the clean Newton Python environment, with all 32 primitives mapped, 9 probe
  spheres, max package-probe contact count 1, max contacted probe spheres 1, contact density proxy
  `0.1111111111111111`, and no failure labels under the recorded `0.05` minimum contact-density
  threshold.
- The 2026-05-15 Franka record reports `smoke_passed` for local Franka USD-open smoke and capped
  geometry-only CPD-like first-mesh smoke: 10384 mesh points, 128 capped faces, and 16 restricted
  primitive proposals. It remains excluded from aggregate claims.
- The 2026-05-15 CPD-like component-merge gate record reports `smoke_passed` for the capped bed
  geometry-only smoke: 1898 mesh points, 256 capped faces, 32 restricted primitive proposals,
  224 topology merges, 0 virtual component merges, and 0 blocked merges. Focused tests cover the
  virtual disconnected-component merge behavior.
- The 2026-05-15 CPD-like objective report record reports `smoke_passed` for the capped bed
  offline objective smoke: 32/32 primitive budget, 32/32 assigned-point containment proxy,
  accepted normalized merge-excess sum `0.000996148870132146`, normalized weighted primitive
  volume `0.0009961811821648128`, and 3 unsupported paper primitive types still outside the
  baseline.
- The 2026-05-15 CPD-like synthetic comparison record reports `smoke_passed` for three
  deterministic in-memory fixtures: adjacent square, disconnected pair, and blocked disconnected
  pair. It records fixture-level topology-only versus component-merge objective accounting without
  adding benchmark or collision-quality claims.
- The 2026-05-15 CPD-like cost-guided merge record reports `smoke_passed` for one deterministic
  in-memory fixture, `cost_guided_pair_choice`: the default topology-then-virtual policy takes one
  topology merge with accepted normalized merge-excess sum `0.010062106570764756`, while
  `cost_guided_pairwise` takes one virtual component merge with accepted normalized merge-excess
  sum `0.000055121`. This is old/new diagnostic accounting on a toy mesh, not collision-quality
  evidence.
- The 2026-05-16 cost-guided merge step trace record is complete. It adds synthetic offline
  merge-step trace diagnostic accounting rows for the accepted virtual-component merge and for
  threshold-gated blocked virtual merges.
- The 2026-05-15 CPD synthetic expected-failure workbench record reports `smoke_passed` for three
  deterministic known-gap fixtures: `restricted_primitive_vocabulary_gap`,
  `single_proxy_wraps_disconnected_components`, and `threshold_blocks_component_merge`. All three
  fixtures matched their expected diagnostic flags with no missing or unexpected flags.
- The 2026-05-15 CPD capped-cylinder proxy record reports `smoke_passed` for the opt-in offline
  capped bed objective smoke: 32/32 primitive budget, 32/32 assigned-point containment proxy,
  unsupported paper primitive count 2, and remaining unsupported paper primitive types
  `frustum` and `trapezoidal_prism`.
- The 2026-05-15 Newton native primitive bundle record reports `smoke_passed` for a synthetic
  six-primitive package in the clean Newton environment: contact canaries passed for all six
  representative kinds, drop/settle completed 480 steps with max contact count 10 and no failure
  labels, and sphere-rain completed 480 steps with contact density proxy 1.0 and no failure labels.
- The 2026-05-15 Newton native fitting comparison record reports `smoke_passed` for three
  deterministic synthetic meshes: `cylindrical_rod` selects `cylinder`, `tapered_cone` selects
  `cone`, and `ellipsoid_blob` selects `ellipsoid` under the opt-in six-kind subset. The record
  also declares `bed_dev_smoke` and `franka_import_smoke` as next-scope real USD assets, not as
  completed old/new comparison evidence.
- The 2026-05-15 synthetic native selection audit record reports `smoke_passed` for the same three
  deterministic toy meshes with candidate weighted-volume tables. The selected native candidate
  has rank `1` in each native lane, and the report records surrogate-cost margins against the
  legacy lane and the next native candidate. This is not a quality metric or paper optimizer.
- The earlier 2026-05-15 real-USD native fitting, candidate-audit, contact, task, and completion
  records documented the pre-cylinder-axis baseline where both capped assets selected boxes. Those
  records are superseded for current status by the candidate-loss/cylinder-axis rerun and the
  later low-support native-extension admissibility rerun.
- The 2026-05-15 candidate-loss/cylinder-axis rerun reports `smoke_passed`: synthetic native
  fitting now includes `squat_cylinder -> cylinder`; capped bed remains `32` boxes in both lanes;
  capped Franka native selects `29` boxes plus `3` cylinders under the surrogate.
- The 2026-05-15 low-support native-extension admissibility record reports `smoke_passed` after
  adding a support-aware guard: capped bed remains `32` boxes in both lanes, and capped Franka now
  selects `32` boxes in the support-aware native lane while reporting three cheaper raw-cost
  cylinder candidates as support-blocked.
- The current candidate-loss report records next-slice triage metadata: bed has one `cylinder`
  near-miss target, and Franka has three support-blocked raw-cost `cylinder` candidates plus three
  `cylinder` near-miss targets. The recommended next algorithmic fixture is now the cylinder
  near-miss branch. This sorts future synthetic-fixture choices; it does not validate those
  primitive choices.
- The 2026-05-16 cylinder near-miss fixture record is complete. It adds a direct synthetic
  primitive-ranking fixture where `box` still wins and `cylinder` is support-admissible but close
  under the current surrogate, plus a dedicated near-miss workbench report. This is a diagnostic
  target for the next algorithmic slice, not a native primitive success case or quality result.
- The 2026-05-16 cylinder near-miss fit-ablation record is complete. It reports that the current
  fixture's containing-cylinder radius already matches the pairwise radial lower bound, so
  radial-center refinement cannot make `cylinder` beat `box` under containment and the current
  surrogate. This is synthetic diagnostic accounting only; default packages and Newton task gates
  are unchanged.
- The 2026-05-16 cylinder near-miss scoring-sensitivity record is complete. It reports that the
  support-admissible cylinder would need a counterfactual score multiplier of about `0.8869`, or
  about an `11.31%` cost reduction, to tie the selected box on the same synthetic fixture. This is
  offline sensitivity accounting only; no multiplier is applied and no Newton rerun is triggered.
- The 2026-05-16 cylinder near-miss scoring-policy ablation record is complete. It applies a fixed
  report-only cylinder multiplier of `0.88` inside the synthetic report and records that the
  counterfactual ranking would flip from `box` to `cylinder` for the near-miss fixture.
- The 2026-05-16 cylinder scoring-policy guardrail record is complete. The same report-only `0.88`
  multiplier leaves the clearly boxy cuboid guardrail fixture at `box`. This is synthetic
  selectivity accounting only; it is not a default scoring-policy change, real-USD result, Newton
  task result, collision-quality result, or proof that the multiplier is safe.
- The 2026-05-16 cylinder scoring-policy selection probe record is complete. It adds a synthetic
  offline opt-in candidate-selection path where the `0.88` cylinder multiplier flips the near-miss
  fixture to `cylinder` while the clearly boxy guardrail remains `box`. Default package generation
  and Newton task gates remain unchanged.
- The 2026-05-16 cylinder scoring-policy package probe record is complete. It adds an
  explicitly opt-in synthetic package path where the same multiplier changes the near-miss
  `CollisionPackage` from `box` to `cylinder`, leaves the clearly boxy guardrail package at `box`,
  and records Newton shape-mapping coverage. This is package-path and mapping accounting only; no
  Newton contact/task diagnostic, real-USD package change, collision-quality result, or scoring
  calibration claim is supported.
- The 2026-05-16 controlled merge-search package probe record is complete. It carries the
  existing cost-guided merge-search fixture into synthetic `CollisionPackage` generation and records
  Newton shape-mapping coverage for the default and opt-in package lanes. This is package-path and
  mapping accounting only; no Newton contact/task diagnostic, real-USD package change,
  collision-quality result, or merge-policy superiority claim is supported.
- The 2026-05-16 controlled merge-search Newton probe record is complete. It runs named synthetic
  contact, drop/settle, and sphere-rain smokes over the same default and opt-in package lanes. This
  is task-smoke execution evidence only; it is not merge-policy superiority, collision-quality
  validation, real-USD package evidence, bed/Franka evidence, benchmark evidence, or CPD paper
  reproduction.
- The 2026-05-16 cost-guided lookahead merge record is complete. It adds a bounded
  synthetic-only `two_step_lookahead` merge/search diagnostic over one trap fixture. This is
  offline merge/search accounting only; it is not default merge behavior, merge-policy superiority,
  package-path evidence, Newton contact/task evidence, real-USD package evidence, bed/Franka
  evidence, benchmark evidence, or CPD paper reproduction.
- The 2026-05-16 cost-guided lookahead package probe record is complete. It carries the same
  lookahead-changed toy grouping into synthetic `CollisionPackage` lanes and records Newton
  shape-mapping coverage. This is package-path and mapping accounting only; it does not run
  Newton runtime tasks, touch real assets, report bed or Franka results, compare against a
  benchmark suite, or complete paper-level reproduction.
- The 2026-05-16 cost-guided lookahead Newton probe record is complete. It adds an explicitly
  opt-in synthetic Newton diagnostic over the lookahead-changed package pair with per-lane contact
  gates. Clean Newton runtime smoke reports `smoke_passed` for contact, drop/settle, and
  sphere-rain on both package lanes under recorded settings.
- The 2026-05-16 Newton CPD workbench four-block status audit is complete. It maps primitive
  fitting/selection, merge/search, offline diagnostic reports, and Newton task comparison to
  current records and identified the then-largest MVP gap as a single slice-level four-block
  report. This is a status map, not new experiment or benchmark evidence.
- The 2026-05-16 four-block slice report record is complete. It adds a command-only evidence map
  for the already recorded `cost_guided_lookahead` synthetic slice, linking primitive
  fitting/selection, merge/search, offline diagnostics, and recorded Newton task-smoke evidence
  without running decomposition, USD loading, real assets, Newton runtime tasks, benchmarks, or
  collision-quality evaluation.
- The 2026-05-16 four-block workbench completion audit is complete. It maps the bounded
  four-block objective to code, CLI, tests, dated records, multi-agent review fixes, and
  verification evidence. This closes the internal single-slice workbench objective, not CPD paper
  reproduction or benchmark/evaluation evidence.
- The 2026-05-16 cylinder scoring-policy Newton probe record is complete. It adds an
  explicitly opt-in synthetic Newton diagnostic over the changed near-miss package pair. The clean
  local Newton run reports `smoke_passed` for contact canary, drop/settle, and sphere-rain on both
  the default `box` package and opt-in `cylinder` package. This is named synthetic task-smoke
  execution evidence only; it is not scoring calibration, collision-quality validation, real-USD
  package evidence, bed/Franka evidence, benchmark evidence, or CPD paper reproduction.
- The latest diagnostic loop is explained in
  [CPD latest diagnostic loop explainer](../reference/cpd-latest-diagnostic-loop-explainer.md):
  candidate-loss diagnosis guides a controlled fitting change, synthetic checks run first, and
  capped bed/Franka reruns stay behind Newton diagnostic gates.
- The current support-aware rerun reports `smoke_passed` for contact and task gates: all four
  bed/Franka old/new packages passed contact canaries, drop/settle, and sphere-rain under the
  conda-managed Newton environment. These task smokes are execution diagnostics, not
  collision-quality comparisons.
- The 2026-05-15 real-USD asset mirror materialization record reports local ignored mirrors for
  the current smoke manifests: bed materialized 18 files with no unresolved dependencies; Franka
  materialized 13 USD files and records unresolved `OmniPBR.mdl`. `--check-assets` selected
  `local_path` and reported `smoke_passed` for both manifests.

## Current Unsupported Claims

- General primitive fitting quality across arbitrary assets has not been evaluated.
- Task-level Newton diagnostic evidence beyond the recorded capped bed, capped Franka, synthetic
  native-bundle, synthetic cylinder scoring-policy Newton task, and synthetic controlled
  merge-search and lookahead Newton task smokes has not been evaluated.
- Real contact-stress measurement has not been implemented or calibrated.
- Whole-robot collider quality, articulation-aware robot simulation, and aggregate robot-class
  evidence have not been evaluated.
- The method beats CoACD, V-HACD, CPD-like decomposition, manual primitive colliders, or Newton-native approximate mesh modes.
- The approach improves robot policy training, real robot behavior, or deployment safety.
- LLM/VLM improves primitive generation.
- The compiler can replace convex decomposition.
- Full CPD paper reproduction has been implemented or evaluated.
- The face-merge baseline is the CPD paper algorithm.
- The component-merge gate is the CPD paper algorithm.
- The expected-failure synthetic workbench is a general failure detector, benchmark, validation
  suite, or proof that all bad decompositions are caught.
- The capped-cylinder proxy is paper-faithful primitive fitting, Newton capped-cylinder support,
  collision-quality evidence, benchmark evidence, or an asset/task improvement.
- The CPD-like generator emits `cylinder`, `cone`, or `ellipsoid` by default for normal asset
  configs.
- The real-USD native fitting comparison proves bed or Franka collision-package improvement.
- The synthetic native primitive bundle proves broad asset quality, collision quality, benchmark
  performance, or paper-scope primitive coverage.
- Environment-readiness diagnostics imply Newton simulation readiness.
- Asset mirror materialization implies license review, complete visual/material packaging,
  benchmark readiness, or collision-quality evidence.

## Future Evidence Needed

For the 0-4 week proof point:

- broader small synthetic meshes with inspectable expected decompositions;
- per-run or DLC-worker readiness report with status `smoke_passed` from the selected worker
  Python;
- asset list with source, license, scale, and hashes;
- baseline parameters and versions;
- Newton version, solver settings, hardware, and deterministic seeds;
- task-level metrics for each asset;
- failure examples, fallback reasons, and unsupported regions;
- artifact paths for reports and configs.

For any LLM/VLM claim:

- non-LLM baseline results first;
- ablation comparing planner/critic/repair roles;
- evidence that LLM/VLM adds value beyond geometry and task heuristics;
- failure cases where language or vision semantics changes the decision.

## Strategic Story

Physical intelligence requires model outputs to be checked against physical constraints. Physics engines provide an executable diagnostic layer, and collision proxies are one of the first contracts that layer depends on.

## Narrow First Milestone

The first local clean Newton runtime readiness gap is resolved, a geometry-only CPD-like primitive
proposal smoke path exists, a contact-only Newton canary exists, and the first two named task
smokes exist for the capped bed asset: drop/settle and sphere-rain contact-density proxy. A narrow
Franka USD-open and first-mesh CPD-like geometry smoke now broadens asset-class intake without
making robot-quality claims. The first CPD-like algorithmic extension is an opt-in
component-merge gate with explicit merge-cost reporting, still below full CPD reproduction. The
first synthetic objective comparison now gives deterministic inspection cases for topology-only
versus component-merge accounting. A focused cost-guided merge-search smoke now turns
AABB-normalized merge-excess into an opt-in synthetic merge decision. A deterministic
expected-failure workbench now converts three known CPD-paper gaps into diagnostic flags. The
native fitting comparison now lets the synthetic workbench compare the old `box`/`sphere`/`capsule`
subset against the six-kind Newton-native subset, with a candidate weighted-volume audit table
explaining the toy selections. The real-USD bed/Franka probe comparison now runs the same old/new
lanes through offline reports, candidate-loss diagnosis, contact canaries, and gated task smokes;
it does not show native primitive quality improvement. Bed and capped Franka both select boxes in
the current support-aware lanes, while three capped Franka raw-cost cylinder candidates are
reported as support-blocked diagnostic accounting. Report failures and fallback behavior as
first-class evidence before changing broader asset claims or adding LLM/VLM.

## Current Non-Goals

No safety guarantee, real-world transfer claim, deployment readiness, benchmark superiority claim, primitive-only sufficiency claim, or complete replacement of convex decomposition.
