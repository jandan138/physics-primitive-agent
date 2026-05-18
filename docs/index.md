# Documentation Index

Current status: this repository is a DeepDive application and project bootstrap for the Newton Primitive Collision Compiler. It now contains config dry-run reporting, USD asset-open smoke diagnostics, repo-local ignored asset mirror materialization for the current bed/Franka smoke USDs, Newton source import diagnostics, local environment-readiness diagnostics, a geometry-only CPD-like face-merge primitive proposal smoke path, an opt-in CPD-like component-merge gate, an offline CPD-like objective report with structured Eq.4 alignment metadata, synthetic objective and expected-limitation workbenches, an opt-in offline `capped_cylinder` proxy, Newton contact canaries, and named Newton task smokes. The Newton-native primitive bundle maps and constructs diagnostic shapes for `box`, `sphere`, `capsule`, `cylinder`, `cone`, and `ellipsoid`, with clean-env contact, drop/settle, and sphere-rain smokes passing under the dated native-bundle record. The opt-in Newton-native fitting comparison chooses `cylinder`, `cone`, and `ellipsoid` on deterministic synthetic meshes and now includes candidate weighted-volume audit tables with explicit one-primitive fixture scope guards plus a squat-cylinder fixture for the controlled cylinder-axis search. The real-USD bed/Franka native probe comparison now runs capped bed and capped Franka first-mesh old/new lanes through offline reports, per-selected-cluster candidate audit and candidate-loss diagnosis summaries with next-slice triage metadata, contact canaries, and gated task smokes; bed and capped Franka both select boxes in the current support-aware lanes, while three capped Franka cheaper raw-cost cylinder candidates are reported as support-blocked. This is selection/accounting evidence rather than native primitive quality evidence. It does not yet contain benchmark results, full CPD paper reproduction, broad asset/task evidence, whole-robot collider-quality evidence, real contact-stress measurement, or LLM/VLM research code.

Current next action: the CPD paper offline lane has closed the mapped-subset native-fixture
PrimitiveSpec-like dict generation contract, the report-only serialization/schema stability
contract, the command-only runtime-boundary preflight, the single-fixture runtime-construction
contract, the single-fixture CollisionPackage generation preflight contract, and the
single-fixture CollisionPackage generation contract for one synthetic `paper_single_box` OBB/box
row, plus the single-fixture runtime-admissibility preflight and runtime-admissibility contract
for that same report-scoped package artifact. It constructs exactly one runtime `PrimitiveSpec`
object from canonical
preflight JSON, stores `PrimitiveSpec.to_dict()` in the report, constructs exactly one
report-scoped `CollisionPackage.to_dict()` artifact for that same box row, then records exactly
one later runtime-admissibility candidate row without copying the full package dict. The package
artifact has `generated_collision_package_count: 1`, status
`offline_synthetic_candidate_runtime_admissibility_not_checked`, and claim boundary
`single_fixture_box_only_offline_collision_package_artifact_not_paper_vocabulary_runtime_admissibility_or_newton`.
The preflight payload keeps `runtime_admissibility_check_count: 0`; the new contract payload
records exactly one offline/static runtime-admissibility check for finite center, right-handed
orthonormal axes, positive half extents, target box schema, source-face coverage, containment
flag, and positive volume accounting. The current top-level
`runtime_admissibility_check_count` is therefore `1`, but runtime execution, Newton mapping,
Newton runtime, real-USD loading, benchmark runs, and collision-quality measurement remain zero or
false. The report now also closes the single-fixture Newton shape-mapping preflight contract for
the same synthetic `paper_single_box` box row. That preflight records one static handoff row with
target shape kind `box`, center/axes/dimensions/half-extents field checks, and a pending support
evidence label for the later mapper. It does not call a mapper, does not import Newton, does not
create a Newton shape, and records `mapping_attempt_count: 0`, `newton_mapping_record_count: 0`,
and `newton_runtime_execution_count: 0`. The report now also closes the single-fixture Newton
shape-mapping contract by recording exactly one report-scoped static `newton_shape_descriptor_dict`
for target kind `box`. That descriptor is JSON-safe report data only: it records the target shape
kind, source fixture/primitive ids, center, axes, half extents, and
`mapping_contract: report_scoped_static_descriptor_no_newton_call`. It still records
`mapping_attempt_count: 0`, `newton_mapping_record_count: 0`, `newton_shape_object_count: 0`, and
`newton_runtime_execution_count: 0`. The report now also closes the single-fixture Newton shape
runtime-boundary preflight contract by recording exactly one later runtime-construction candidate
for that static descriptor row. That preflight is JSON-safe report data only: it checks descriptor
kind, target kind, lineage, center, axes, and half extents, keeps `mapping_attempt_count: 0`,
`newton_mapping_record_count: 0`, `newton_shape_object_count: 0`, and
`newton_runtime_execution_count: 0`, and does not construct a Newton shape object or run Newton.
The report now also closes the single-fixture Newton shape runtime-construction contract by
constructing exactly one repo-local `NewtonShapeMapping.to_dict()` report record for the same
synthetic `paper_single_box` descriptor. It creates no Newton engine shape object, makes no
builder shape call, runs no Newton runtime, and adds no USD, benchmark, collision-quality, Newton
readiness/support, or `paper_faithful_offline` evidence.
The report now also closes the single-fixture Newton shape runtime builder-preflight contract by
recording exactly one JSON-safe future builder call plan for the same synthetic box mapping
record. That plan records the future `box` builder method name and signature fields `body`,
`xform`, `hx`, `hy`, and `hz`, plus body-binding and deferred transform policy text. It allows
zero builder calls, creates zero Newton engine shape objects, and runs zero Newton runtime code.
The report now also closes the single-fixture Newton shape runtime builder-construction and
engine-builder boundary-preflight contracts, then closes the bounded Newton/Warp
environment-probe contract for the same synthetic box mapping. The environment probe records
configured-source-dir status and JSON-safe Newton/Warp `find_spec` provenance shape; the default
offline report remains no-config and records no real Newton/Warp import. It still instantiates no
`newton.ModelBuilder`, creates zero Newton engine shape objects, makes zero real Newton builder
shape calls, finalizes no model, creates no collision pipeline, and runs zero Newton runtime code.
The current next gate is
`paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract`. This is still not package
readiness, not Newton readiness, not Newton support, not Newton execution, not real-USD evidence,
not benchmark evidence, not collision-quality evidence, not deployment/safety evidence, not
full-CPD evidence, not `paper_faithful_offline` evidence, and not paper primitive vocabulary
coverage. The next step is bounded API-surface inspection for the same single synthetic package
boundary, not a capped bed/Franka rerun and not Newton execution. A capped bed/Franka rerun remains blocked
unless a
separate real package change is introduced and passes full mapping, contact-canary, task-gate, and
dated-record gates. The
completed cylinder branch remains useful context: the `cylinder_near_miss_cluster` fixture,
near-miss workbench, fit-ablation report, scoring-sensitivity report, report-only scoring-policy
ablation, and boxy guardrail extension show how synthetic changes are gated before broader runs.
The fit-ablation report shows this fixture cannot be flipped by radial-center refinement while
preserving containment; the sensitivity report quantifies the counterfactual cylinder scoring
change required to tie box; the report-only policy ablation applies a fixed hypothetical
multiplier only inside the synthetic report; and the boxy guardrail remains `box` under the same
multiplier. The synthetic offline opt-in
scoring-policy selection probe now routes the same multiplier through an explicit synthetic
candidate-selection path, flipping the near-miss but not the boxy guardrail. The explicit
synthetic package probe now pushes that opt-in choice through `decompose_mesh` into a changed
synthetic `CollisionPackage` and records a Newton shape-mapping summary only, while the default
package path and the boxy guardrail stay unchanged. It does not run Newton contact or task
diagnostics. The synthetic Newton probe now runs named contact, drop/settle, and sphere-rain task
smokes over the changed near-miss package pair only, with default package generation and all
real-USD packages unchanged. The controlled merge-search package probe now carries the existing
cost-guided toy merge/search behavior difference into synthetic `CollisionPackage` and Newton
shape-mapping accounting. The controlled merge-search Newton probe then runs named contact,
drop/settle, and sphere-rain task smokes over that changed synthetic package pair only. The
bounded synthetic `two_step_lookahead` diagnostic, follow-on package/mapping probe, follow-on
synthetic Newton task-smoke probe, and command-only four-block slice report for the
lookahead-changed package pair are now complete under recorded settings. The first
fixture-scoped `cpd_paper_offline_report` slice is now implemented as a command-only partial
offline paper-lane audit over `paper_single_box`, `paper_two_face_merge`,
`paper_three_face_chain`, `paper_disconnected_components`, `paper_component_pair_threshold_blocked`,
`paper_tiny_sphere_clamp`, `paper_duplicate_vertex_preprocessing`, `paper_frustum_like`,
`paper_trapezoid_prism_like`, `paper_nested_primitive`,
`paper_quad_face_intake`, and `paper_polygon_face_intake`. It records paper operator,
primitive-fit subset, left/right/merged merge-cost inputs, offline paper-shaped OBB/sphere fit
audit rows, an offline paper-shaped capsule axis audit row, offline-only flat
capped-cylinder/frustum/trapezoidal-prism candidate rows,
base-collapse-cost versus weighted-priority-cost fields, a topology-only priority-queue trace with
eager stale pruning, a threshold-disabled component-pair insertion trace, a finite-threshold
component-pair blocked trace, an explicit identity-axis OBB enclosed-primitive postprocess cull
audit, a fan-triangulated quad/polygon source-face intake policy audit, and an exact-coordinate
duplicate-vertex preprocessing audit while keeping Newton, bed/Franka, package generation, and
benchmark work out of scope. The audited primitive rows, postprocess cull, intake policy, and
duplicate-vertex preprocessing fixture are fixture-scoped audit data, not a full decomposition. It
now also records `paper_faithful_offline_scope_audit`, a criteria table that keeps the lane
`partial`, leaves `paper_faithful_offline_supported: false`, and previously advanced the
scope-audit gate to
`paper_fixture_breadth_expansion_plan`.
The fixture-breadth Batch A source/preprocess/intake/operator slice is now implemented with
`paper_mixed_face_preprocess_operator`, `paper_degenerate_preprocess_face_drop`, and
`paper_concave_polygon_rejected`, while keeping the report partial and advancing the next
required gate to `paper_fixture_breadth_batch_b`. Batch B primitive-fit breadth is now also
implemented with synthetic offline fixtures for OBB, sphere, capsule, capped cylinder, frustum,
and trapezoidal prism. Batch B previously advanced the next required gate to
`paper_fixture_breadth_batch_c`; Batch C cost/search/stop breadth is now implemented with synthetic
offline fixtures for weighted-priority ordering, deterministic queue tie/eager-stale-prune
behavior, and one positive finite component-pair threshold block. Batch D component-pair breadth is
now implemented with multi-candidate component-pair ordering and deterministic capped skipped-pair
accounting. Batch E postprocess breadth is now implemented with rotated nested OBB containment and
explicit cross-type unsupported no-cull accounting. The command-only synthetic fixture-breadth
completion review for planned Batches A-E is now also implemented, while keeping the report
partial and keeping `paper_faithful_offline_supported: false`. Its nested review payload records
the planning-only `paper_faithful_offline_generalization_plan` as the follow-up gate for that
closed review. The report now also includes a command-only planning table for offline CPD
paper-lane generalization beyond named toy fixtures. That table closes only the planning gate,
keeps the report partial, keeps
`paper_faithful_offline_supported: false`, and recorded
`paper_generalization_batch_a_source_policy` as the immediate follow-up when the planning gate was
introduced. The report now also closes only that source-policy gate with an offline source-policy
matrix for deterministic synthetic meshes. At that source-policy stage the follow-up gate was
`paper_generalization_batch_b_primitive_fit_engine`. The report now also closes only that
primitive-fit engine gate with an offline matrix over deterministic in-memory probes for all six
paper primitive names. The report now also closes only the search-engine generalization gate with
an offline search-trace matrix over existing deterministic topology, threshold, and component-pair
traces. The report now also closes only the postprocess-policy generalization gate with an offline
matrix over existing identity-axis OBB, rotated OBB, and unsupported cross-type no-silent-cull
postprocess audit fixtures. It now also closes only the package-boundary readiness gate with an
offline package-boundary readiness matrix before package conversion. It now also closes only
`paper_offline_changed_decomposition_output_contract` with an offline changed-decomposition output
contract, not a `CollisionPackage`; at that stage the follow-up gate was
`paper_package_adapter_contract`. The report now also closes only that adapter-contract gate with
a command-only offline package-adapter contract, not a `CollisionPackage`; all 16 current
`trapezoidal_prism` / `offline_only_unmapped` primitive records are classified as
`later_policy_required`. The report now also closes only
`paper_package_adapter_unsupported_primitive_policy` with a command-only offline unsupported
primitive policy table, not a `CollisionPackage`; the six paper primitive families are classified
for future adapter policy, the current 16 unmapped trapezoidal-prism rows stay offline, and the
next gate at that stage was `paper_package_conversion_mapped_subset_plan`. The report now also
closes only that mapped-subset planning gate with a command-only offline package-conversion
planning table, not a `CollisionPackage`; native-family review rows are identified,
the current 16 unmapped trapezoidal-prism rows stay offline, zero current package-conversion
candidates are recorded, and the next gate at that stage was
`paper_mapped_subset_conversion_candidate_matrix`. The report now also closes only that candidate
matrix gate with a command-only offline review matrix, not a `CollisionPackage`; it records three
future-family review rows, keeps the current 16 unmapped rows blocked/offline, records zero current
package-conversion candidates, and at that stage advanced the next gate to
`paper_mapped_subset_adapter_preflight_contract`. The report now also closes only that
adapter-preflight gate with a command-only offline contract, not `PrimitiveSpec` generation and
not a `CollisionPackage`; it records future adapter requirements, keeps the current zero
package-conversion-candidate state as no-op, keeps all current unmapped trapezoidal-prism rows
offline, keeps package generation disabled, and advances the next gate to
`paper_mapped_subset_primitivespec_dry_run_contract`. The report now also closes only that
PrimitiveSpec dry-run gate with a command-only offline contract, not real `PrimitiveSpec`
generation and not a `CollisionPackage`; it records future PrimitiveSpec shape requirements,
keeps current PrimitiveSpec candidates at zero, keeps all current unmapped trapezoidal-prism rows
offline/no-op, and advances the next gate to
`paper_mapped_subset_primitivespec_validation_contract`. The report now also closes only that
PrimitiveSpec validation gate with a command-only offline validation contract, not real
`PrimitiveSpec` generation and not a `CollisionPackage`; it validates the dry-run field list,
mapped future shape labels, six family rows, 16 current no-op rows, source traceability, zero
current candidates, zero generated PrimitiveSpecs, and false runtime/evaluation triggers, and
advances the next gate to
`paper_mapped_subset_primitivespec_generation_preflight_contract`. The report now also closes only
that PrimitiveSpec generation-preflight gate with a command-only offline preflight contract, not
real `PrimitiveSpec` generation and not a `CollisionPackage`; it records the future mapped native
families, blocked approximation-policy families, current no-op rows, zero generation candidates,
zero generated PrimitiveSpecs, zero generated CollisionPackages, and zero runtime-admissibility
checks, and advances the next gate to `paper_mapped_subset_primitivespec_generation_contract`.
The report now also closes only that PrimitiveSpec generation contract with command-only offline
template rows, not runtime `PrimitiveSpec` objects and not a `CollisionPackage`; it records three
native-family templates for box/sphere/capsule, keeps blocked/no-op paper families explicit, keeps
all current unmapped rows offline/no-op, records zero generated runtime PrimitiveSpecs, zero
CollisionPackages, and zero runtime-admissibility checks, and advances the next gate to
`paper_mapped_subset_primitivespec_candidate_source_contract`. The report now also closes only
that PrimitiveSpec candidate-source contract with a command-only offline source audit, not runtime
`PrimitiveSpec` generation and not a `CollisionPackage`; it records three future-only native
template source rows, two blocked approximation-policy source rows, one no-op trapezoidal-prism
family source row, and 16 traceable but ineligible current unmapped trapezoidal-prism rows,
keeps eligible current PrimitiveSpec candidate sources at zero, and advances the next gate to
`paper_mapped_subset_native_current_fixture_contract`. The report now also closes only that
native-current fixture contract with a command-only offline source row, not runtime
`PrimitiveSpec` generation and not a `CollisionPackage`; it records exactly one synthetic
`paper_single_box` selected OBB/box source row, one eligible current candidate source, one
report-only PrimitiveSpec generation candidate, zero generated PrimitiveSpecs, zero generated
CollisionPackages, zero runtime-admissibility checks, and advances the next gate to
`paper_mapped_subset_primitivespec_native_fixture_generation_contract` at that stage. The report now
also closes only that native-fixture generation contract with one JSON-serializable, report-only
PrimitiveSpec-like dict shaped like `PrimitiveSpec.to_dict()` for review, while keeping runtime
`PrimitiveSpec` objects, `CollisionPackage` generation, runtime-admissibility checks, Newton,
real-USD, benchmark, collision-quality, deployment, and certification triggers at zero or false.
The current next gate is now after the command-only runtime-boundary preflight, single-fixture
runtime-construction, package-generation preflight, package-generation, runtime-admissibility
preflight, offline/static runtime-admissibility contract, offline/static Newton shape-mapping
preflight contract, offline/static Newton shape-mapping descriptor contract, offline/static
Newton shape runtime-boundary preflight contract, offline/report-scoped Newton shape
runtime-construction contract, offline/static Newton shape runtime builder-preflight contract,
offline/report-only Newton shape runtime recording-builder construction contract, offline/static
Newton engine-builder boundary-preflight contract, and bounded Newton/Warp environment-probe
contract:
`paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract`. The serialization contract
validates strict canonical JSON and round-trip equality for the one report-only `paper_single_box`
OBB/box PrimitiveSpec-like dict; the runtime-boundary preflight records one later runtime
construction candidate for that row; and the runtime-construction contract constructs exactly one
runtime `PrimitiveSpec` object. The package-generation preflight then records one later
package-generation candidate; the package-generation contract constructs exactly one synthetic,
report-scoped `CollisionPackage.to_dict()` artifact for that same box row; and the
runtime-admissibility preflight contract records one later runtime-admissibility candidate row
while still creating no runtime-admissibility, Newton, real-USD, benchmark, or collision-quality
evidence. The runtime-admissibility contract records one offline/static finite-geometry and
box-schema check; the shape-mapping preflight records one static handoff row while still creating
no Newton shape mapping, no Newton execution, no real-USD evidence, no benchmark evidence, and no
collision-quality evidence. The Newton shape runtime-construction contract constructs exactly one
repo-local `NewtonShapeMapping.to_dict()` report record while still creating no Newton engine
shape object, no Newton builder shape call, no Newton runtime execution, no real-USD evidence, no
benchmark evidence, and no collision-quality evidence.
This review, planning table,
source-policy
matrix, primitive-fit engine matrix, search-engine matrix, postprocess-policy matrix,
package-boundary readiness matrix, changed-decomposition output contract, and package-adapter
contract, unsupported-primitive policy, mapped-subset planning table, candidate matrix,
adapter-preflight contract, PrimitiveSpec dry-run contract, PrimitiveSpec validation contract, and
PrimitiveSpec generation-preflight, generation, candidate-source, and native-current-fixture
contracts, native-fixture serialization, runtime-boundary, runtime-construction,
package-generation, and runtime-admissibility contracts
are not
`paper_faithful_offline` support, and they are not a capped bed/Franka rerun unless a separate real
package change is introduced and passes full mapping, contact-canary, task-gate, and dated-record
gates. The
low-support branch is now guarded by support-aware admissibility, but that is still not
collision-quality evidence. Keep `capped_cylinder`, `frustum`, and
`trapezoidal_prism` in the offline paper-alignment lane until separate mapping and diagnostic
records exist.

## Current CPD Paper Plan

- [CPD paper reproduction gap matrix](reference/cpd-paper-reproduction-gap-matrix.md): current
  paper requirements versus repository surrogates, with Newton runtime boundaries.
- [CPD paper-faithful offline lane spec](reference/cpd-paper-faithful-offline-lane-spec.md):
  planned fixture-scoped offline lane for paper mechanics before real USD, Newton, or benchmark
  expansion.
- [CPD paper fixture-breadth expansion plan](reference/cpd-paper-fixture-breadth-expansion-plan.md):
  documentation-only plan that maps the nine blocking scope-audit rows to future synthetic
  fixture batches; Batch A, Batch B, Batch C, Batch D, and Batch E are now implemented and
  the completion review is now implemented.
- [CPD paper faithful offline generalization plan](reference/cpd-paper-faithful-offline-lane-spec.md):
  command-only planning table for offline generalization beyond named toy fixtures. The planned
  source-policy, primitive-fit engine, search-engine, postprocess-policy, and package-boundary
  readiness matrices are now implemented, the offline changed-decomposition output contract is now
  implemented, the offline package-adapter contract is now implemented, and the offline
  unsupported-primitive policy, mapped-subset package-conversion plan, and mapped-subset
  candidate matrix are now implemented, and the mapped-subset adapter-preflight contract is now
  implemented, the mapped-subset PrimitiveSpec dry-run contract is now implemented, and the
  mapped-subset PrimitiveSpec validation contract, generation-preflight contract, and generation
  contract are now implemented, and the mapped-subset PrimitiveSpec candidate-source contract is
  now implemented, and the mapped-subset native-current fixture contract, native-fixture
  PrimitiveSpec-like dict generation contract, and native-fixture serialization contract are now
  implemented, the runtime-boundary preflight contract is now implemented, the single-fixture
  runtime-construction contract is now implemented, the package-generation preflight contract is
  now implemented, and the single-fixture CollisionPackage generation contract is now implemented,
  the single-fixture runtime-admissibility preflight contract is now implemented, and the
  single-fixture offline/static runtime-admissibility contract is now implemented, and the
  single-fixture offline/static Newton shape-mapping preflight contract is now implemented, the
  single-fixture offline/static Newton shape-mapping descriptor contract is now implemented, and
  the single-fixture offline/static Newton shape runtime-boundary preflight contract is now
  implemented, and the single-fixture offline/report-scoped Newton shape runtime-construction
  contract is now implemented, and the single-fixture offline/static Newton shape runtime
  builder-preflight contract is now implemented, and the single-fixture offline/report-only
  recording-builder construction contract is now implemented, and the single-fixture offline/static
  Newton engine-builder boundary-preflight contract is now implemented, and the single-fixture
  bounded Newton/Warp environment-probe contract is now implemented, while the next gate is
  `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract`.
- [CPD paper generalization Batch A source-policy record](records/2026-05-16-cpd-paper-generalization-batch-a-source-policy.md):
  dated implementation record for the offline report-only source-policy matrix. It keeps the report
  partial and does not add package generation, Newton runtime, real-USD, or benchmark evidence.
- [CPD paper generalization Batch B primitive-fit engine record](records/2026-05-16-cpd-paper-generalization-batch-b-primitive-fit-engine.md):
  dated implementation record for the offline report-only primitive-fit engine generalization
  matrix. It keeps the report partial and does not add package generation, Newton runtime,
  real-USD, or benchmark evidence.
- [CPD paper generalization Batch C search-engine record](records/2026-05-17-cpd-paper-generalization-batch-c-search-engine.md):
  dated implementation record for the offline report-only search-trace generalization matrix. It
  keeps the report partial and does not add package generation, Newton runtime, real-USD, or
  benchmark evidence.
- [CPD paper generalization Batch D postprocess-policy record](records/2026-05-17-cpd-paper-generalization-batch-d-postprocess-policy.md):
  dated implementation record for the offline report-only postprocess-policy generalization
  matrix. It keeps the report partial and does not add a general containment library, package
  generation, Newton runtime, real-USD, or benchmark evidence.
- [CPD paper generalization Batch E package-boundary readiness record](records/2026-05-17-cpd-paper-generalization-batch-e-package-boundary-readiness.md):
  dated implementation record for the offline report-only package-boundary readiness matrix before
  package conversion. It keeps the report partial and does not add package generation, Newton
  runtime, real-USD, or benchmark evidence.
- [CPD paper changed-decomposition output contract record](records/2026-05-17-cpd-paper-changed-decomposition-output-contract.md):
  dated implementation record for the offline changed-decomposition output contract, not a
  `CollisionPackage`. It keeps the report partial and advances the next gate to
  `paper_package_adapter_contract` without package generation, Newton runtime, real-USD, or
  benchmark evidence.
- [CPD paper package-adapter contract record](records/2026-05-17-cpd-paper-package-adapter-contract.md):
  dated implementation record for the command-only offline package-adapter contract, not a
  `CollisionPackage`. It keeps the report partial and advances the next gate to
  `paper_package_adapter_unsupported_primitive_policy` without package generation, Newton runtime,
  real-USD, or benchmark evidence.
- [CPD paper package-adapter unsupported primitive policy record](records/2026-05-17-cpd-paper-package-adapter-unsupported-primitive-policy.md):
  dated implementation record for the command-only offline unsupported-primitive policy, not a
  `CollisionPackage`. It keeps the report partial and advances the next gate to
  `paper_package_conversion_mapped_subset_plan` without package generation, Newton runtime,
  real-USD, or benchmark evidence.
- [CPD paper package conversion mapped-subset plan record](records/2026-05-17-cpd-paper-package-conversion-mapped-subset-plan.md):
  dated implementation record for the command-only offline mapped-subset package-conversion
  planning table, not a `CollisionPackage`. It keeps the report partial, records zero current
  package-conversion candidates, and advances the next gate to
  `paper_mapped_subset_conversion_candidate_matrix` without package generation, Newton runtime,
  real-USD, or benchmark evidence.
- [CPD paper mapped-subset conversion candidate matrix record](records/2026-05-17-cpd-paper-mapped-subset-conversion-candidate-matrix.md):
  dated implementation record for the command-only offline candidate matrix, not a
  `CollisionPackage`. It keeps the report partial, records three future-family review rows, keeps
  current package-conversion candidates at zero, and at that stage advanced the next gate to
  `paper_mapped_subset_adapter_preflight_contract` without PrimitiveSpec generation,
  CollisionPackage generation, Newton runtime, real-USD, or benchmark evidence.
- [CPD paper mapped-subset adapter preflight contract record](records/2026-05-17-cpd-paper-mapped-subset-adapter-preflight-contract.md):
  dated implementation record for the command-only offline adapter-preflight contract, not
  `PrimitiveSpec` generation and not a `CollisionPackage`. It keeps the report partial, records
  future adapter requirements, keeps current package-conversion candidates at zero, keeps current
  unmapped rows offline/no-op, and advances the next gate to
  `paper_mapped_subset_primitivespec_dry_run_contract` without PrimitiveSpec generation,
  CollisionPackage generation, Newton runtime, real-USD, or benchmark evidence.
- [CPD paper mapped-subset PrimitiveSpec dry-run contract record](records/2026-05-17-cpd-paper-mapped-subset-primitivespec-dry-run-contract.md):
  dated implementation record for the command-only offline PrimitiveSpec dry-run contract, not
  real `PrimitiveSpec` generation and not a `CollisionPackage`. It keeps the report partial,
  records future PrimitiveSpec shape requirements, keeps current PrimitiveSpec candidates at zero,
  keeps current unmapped rows offline/no-op, and advances the next gate to
  `paper_mapped_subset_primitivespec_validation_contract` without PrimitiveSpec generation,
  CollisionPackage generation, Newton runtime, real-USD, or benchmark evidence.
- [CPD paper mapped-subset PrimitiveSpec validation contract record](records/2026-05-17-cpd-paper-mapped-subset-primitivespec-validation-contract.md):
  dated implementation record for the command-only offline PrimitiveSpec validation contract, not
  real `PrimitiveSpec` generation and not a `CollisionPackage`. It keeps the report partial,
  validates the dry-run contract shape and zero-candidate/no-op behavior, keeps current unmapped
  rows offline/no-op, and advances the next gate to
  `paper_mapped_subset_primitivespec_generation_preflight_contract` without PrimitiveSpec
  generation, CollisionPackage generation, Newton runtime, real-USD, benchmark, or
  collision-quality evidence.
- [CPD paper mapped-subset PrimitiveSpec generation-preflight contract record](records/2026-05-17-cpd-paper-mapped-subset-primitivespec-generation-preflight-contract.md):
  dated implementation record for the command-only offline PrimitiveSpec generation-preflight
  contract, not real `PrimitiveSpec` generation and not a `CollisionPackage`. It keeps the report
  partial, records future native-family generation requirements, keeps current unmapped rows
  offline/no-op, keeps current generation candidates at zero, and advances the next gate to
  `paper_mapped_subset_primitivespec_generation_contract` without PrimitiveSpec generation,
  CollisionPackage generation, Newton runtime, real-USD, benchmark, or collision-quality evidence.
- [CPD paper mapped-subset PrimitiveSpec generation contract record](records/2026-05-17-cpd-paper-mapped-subset-primitivespec-generation-contract.md):
  dated implementation record for the command-only offline PrimitiveSpec generation contract, not
  runtime `PrimitiveSpec` generation and not a `CollisionPackage`. It keeps the report partial,
  emits native-family template rows for box/sphere/capsule only, keeps current unmapped rows
  offline/no-op, keeps generated runtime PrimitiveSpecs, CollisionPackages, and
  runtime-admissibility checks at zero, and advances the next gate to
  `paper_mapped_subset_primitivespec_candidate_source_contract`.
- [CPD paper mapped-subset PrimitiveSpec candidate-source contract record](records/2026-05-17-cpd-paper-mapped-subset-primitivespec-candidate-source-contract.md):
  dated implementation record for the command-only offline PrimitiveSpec candidate-source audit,
  not runtime `PrimitiveSpec` generation and not a `CollisionPackage`. It keeps the report partial,
  classifies future native templates separately from current rows, records zero eligible current
  PrimitiveSpec candidate sources, and advances the next gate to
  `paper_mapped_subset_native_current_fixture_contract`.
- [CPD paper mapped-subset native-current fixture contract record](records/2026-05-17-cpd-paper-mapped-subset-native-current-fixture-contract.md):
  dated implementation record for the command-only offline native-current fixture source-row
  contract, not runtime `PrimitiveSpec` generation and not a `CollisionPackage`. It records one
  synthetic `paper_single_box` OBB/box source row, one eligible current candidate source, one
  report-only PrimitiveSpec generation candidate, and led to the later
  `paper_mapped_subset_primitivespec_native_fixture_generation_contract` gate.
- [CPD paper mapped-subset PrimitiveSpec native-fixture generation contract record](records/2026-05-17-cpd-paper-mapped-subset-primitivespec-native-fixture-generation-contract.md):
  dated implementation record for the command-only offline native-fixture PrimitiveSpec-like dict
  generation contract, not runtime `PrimitiveSpec` object creation and not a `CollisionPackage`.
  It emits exactly one report-only serialized dict for `paper_single_box` and advances the next
  gate to `paper_mapped_subset_primitivespec_native_fixture_serialization_contract`.
- [CPD paper mapped-subset PrimitiveSpec native-fixture serialization contract record](records/2026-05-17-cpd-paper-mapped-subset-primitivespec-native-fixture-serialization-contract.md):
  dated implementation record for the command-only offline native-fixture serialization/schema
  stability contract, not runtime `PrimitiveSpec` object creation and not a `CollisionPackage`.
  It validates strict canonical JSON and round-trip equality for one report-only `paper_single_box`
  OBB/box dict and advances the next gate to
  `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`.
- [CPD paper mapped-subset PrimitiveSpec runtime-boundary preflight contract record](records/2026-05-17-cpd-paper-mapped-subset-primitivespec-runtime-boundary-preflight-contract.md):
  dated implementation record for the command-only offline runtime-boundary preflight contract,
  not runtime `PrimitiveSpec` construction and not a `CollisionPackage`. It records one later
  runtime-construction candidate for the same `paper_single_box` row and advances the next gate to
  `paper_mapped_subset_primitivespec_runtime_construction_contract`.
- [CPD paper mapped-subset PrimitiveSpec runtime-construction contract record](records/2026-05-17-cpd-paper-mapped-subset-primitivespec-runtime-construction-contract.md):
  dated implementation record for the single-fixture offline runtime-construction contract. It
  constructs exactly one runtime `PrimitiveSpec` object from the canonical `paper_single_box`
  OBB/box preflight JSON after checking the runtime-boundary preflight row's canonical JSON
  SHA-256 fingerprint, stores only `PrimitiveSpec.to_dict()` in the report, keeps package, Newton,
  real-USD, benchmark, collision-quality, deployment, and certification triggers false, and
  advances the next gate to
  `paper_mapped_subset_collision_package_generation_preflight_contract`.
- [CPD paper mapped-subset CollisionPackage generation preflight contract record](records/2026-05-17-cpd-paper-mapped-subset-collision-package-generation-preflight-contract.md):
  dated implementation record for the single-fixture offline package-generation preflight
  contract. It records one later package-generation candidate from the runtime
  `PrimitiveSpec.to_dict()` row, keeps generated CollisionPackages and runtime-admissibility
  checks at zero, and advances the next gate to
  `paper_mapped_subset_collision_package_generation_contract`.
- [CPD paper mapped-subset CollisionPackage generation contract record](records/2026-05-17-cpd-paper-mapped-subset-collision-package-generation-contract.md):
  dated implementation record for the single-fixture offline CollisionPackage generation
  contract. It constructs exactly one synthetic `CollisionPackage.to_dict()` artifact for
  `paper_single_box`, keeps runtime-admissibility checks, Newton runtime, real-USD, benchmark, and
  collision-quality evidence at zero or false, and advances the next gate to
  `paper_mapped_subset_runtime_admissibility_preflight_contract`.
- [CPD paper mapped-subset runtime-admissibility preflight contract record](records/2026-05-17-cpd-paper-mapped-subset-runtime-admissibility-preflight-contract.md):
  dated implementation record for the single-fixture offline runtime-admissibility preflight
  contract. It consumes the one synthetic `paper_single_box` `CollisionPackage.to_dict()` artifact,
  records exactly one later runtime-admissibility candidate row without copying the full package
  dict, keeps runtime-admissibility checks, Newton runtime, real-USD, benchmark, and
  collision-quality evidence at zero or false; it is not package readiness, not executable
  runtime-admissibility, not full CPD reproduction, not `paper_faithful_offline`, and not
  deployment, safety, or certification evidence. It advances the next gate to
  `paper_mapped_subset_runtime_admissibility_contract`.
- [CPD paper mapped-subset runtime-admissibility contract record](records/2026-05-18-cpd-paper-mapped-subset-runtime-admissibility-contract.md):
  dated implementation record for the single-fixture offline/static runtime-admissibility
  contract. It consumes the preflight row for the same synthetic `paper_single_box`
  `CollisionPackage.to_dict()` artifact, records one static box-schema and finite-geometry check,
  keeps Newton mapping, Newton runtime, real-USD, benchmark, and collision-quality evidence at
  zero or false, keeps `paper_faithful_offline` blockers separate from runtime-lane gates, and
  advances the runtime-lane next gate to
  `paper_mapped_subset_newton_shape_mapping_preflight_contract`.
- [CPD paper mapped-subset Newton shape-mapping preflight contract record](records/2026-05-18-cpd-paper-mapped-subset-newton-shape-mapping-preflight-contract.md):
  dated implementation record for the single-fixture offline/static Newton shape-mapping preflight
  contract. It consumes the runtime-admissibility row for the same synthetic `paper_single_box`
  box artifact, records one static mapper-handoff row with target kind `box`, field-transfer
  checks, zero mapping attempts, zero Newton mapping records, and zero Newton runtime executions,
  and advances the runtime-lane next gate to
  `paper_mapped_subset_newton_shape_mapping_contract`.
- [CPD paper mapped-subset Newton shape-mapping contract record](records/2026-05-18-cpd-paper-mapped-subset-newton-shape-mapping-contract.md):
  dated implementation record for the single-fixture offline/static Newton shape descriptor
  contract. It consumes the shape-mapping preflight row for the same synthetic `paper_single_box`
  box artifact, records exactly one report-scoped descriptor dict for target kind `box`, keeps
  mapping attempts, Newton mapping records, Newton shape object construction, and Newton execution
  at zero or false, and advances the runtime-lane next gate to
  `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`.
- [CPD paper mapped-subset Newton shape runtime-boundary preflight contract record](records/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-boundary-preflight-contract.md):
  dated implementation record for the single-fixture offline/static Newton shape runtime-boundary
  preflight contract. It consumes the static descriptor row for the same synthetic
  `paper_single_box` box artifact, records exactly one later runtime-construction candidate row,
  keeps Newton shape object construction and Newton execution at zero or false, and advances the
  runtime-lane next gate to `paper_mapped_subset_newton_shape_runtime_construction_contract`.
- [CPD paper mapped-subset Newton shape runtime-construction contract record](records/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-construction-contract.md):
  dated implementation record for the single-fixture offline/report-scoped Newton shape
  runtime-construction contract. It consumes the runtime-boundary preflight row for the same
  synthetic `paper_single_box` box artifact, constructs exactly one repo-local
  `NewtonShapeMapping.to_dict()` report record, keeps Newton engine shape object construction,
  Newton builder shape calls, and Newton execution at zero or false, and advances the runtime-lane
  next gate to `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`.
- [CPD paper mapped-subset Newton shape runtime builder-preflight contract record](records/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-builder-preflight-contract.md):
  dated implementation record for the single-fixture offline/static Newton shape runtime
  builder-preflight contract. It consumes the repo-local `NewtonShapeMapping.to_dict()` record,
  records one JSON-safe future box builder call plan, keeps Newton engine shape object
  construction, Newton builder shape calls, and Newton execution at zero or false, and advances
  the runtime-lane next gate to
  `paper_mapped_subset_newton_shape_runtime_builder_construction_contract`.
- [CPD paper mapped-subset Newton shape runtime builder-construction contract record](records/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-builder-construction-contract.md):
  dated implementation record for the single-fixture offline/report-only Newton shape runtime
  builder-construction contract. It consumes the builder-preflight row, records one JSON-safe
  repo-local recording-builder `add_shape_box` call artifact through the repo-local static shape
  helper and fake Warp-like module, keeps real Newton imports, Newton `ModelBuilder`
  instantiation, Newton engine shape object construction, Newton builder shape calls, and Newton
  execution at zero or false, and advances the runtime-lane next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract`.
- [CPD paper mapped-subset Newton shape runtime engine-builder boundary preflight contract record](records/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-engine-builder-boundary-preflight-contract.md):
  dated implementation record for the single-fixture offline/static Newton engine-builder boundary
  preflight contract. It consumes the recording-builder artifact, records one future-boundary
  checklist row before any real `newton.ModelBuilder` / `add_shape_box` environment boundary,
  keeps real Newton imports, Newton `ModelBuilder` instantiation, real Newton builder shape calls,
  Newton engine shape object construction, model finalization, collision pipeline calls, and
  Newton execution at zero or false, and advances the runtime-lane next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract`.
- [CPD paper mapped-subset Newton shape runtime engine-builder environment probe contract record](records/2026-05-19-cpd-paper-mapped-subset-newton-shape-runtime-engine-builder-environment-probe-contract.md):
  dated implementation record for the single-fixture bounded Newton/Warp environment-provenance
  contract. It records configured-source-dir status and JSON-safe `find_spec` provenance shape,
  keeps real runtime imports, `newton.ModelBuilder`, real builder shape calls, model finalization,
  collision pipeline calls, Newton execution, real USD, benchmarks, and collision-quality evidence
  at zero or false, and advances the runtime-lane next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract`.
- [Claim Boundaries](reference/claim-boundaries.md): current allowed wording and the boundary for
  the planned `paper_faithful_offline` status.
- [CPD paper gap matrix and offline lane spec record](records/2026-05-16-cpd-paper-gap-matrix-and-offline-lane-spec.md):
  dated record for this planning update and review status.
- [CPD paper offline first fixture slice record](records/2026-05-16-cpd-paper-offline-first-fixture-slice.md):
  dated implementation record for the partial `cpd_paper_offline_report` over two synthetic toy
  fixtures, with no Newton, real-USD, benchmark, or collision-quality claim.
- [CPD paper frustum/trapezoid audit record](records/2026-05-16-cpd-paper-frustum-trapezoid-audit.md):
  dated implementation record for offline-only frustum and trapezoidal-prism fit-audit rows in the
  partial `cpd_paper_offline_report`.
- [CPD paper flat capped-cylinder audit record](records/2026-05-16-cpd-paper-flat-capped-cylinder-audit.md):
  dated implementation record for the offline-only flat capped-cylinder fit-audit row in the
  partial `cpd_paper_offline_report`.
- [CPD paper capsule axis audit record](records/2026-05-16-cpd-paper-capsule-axis-audit.md):
  dated implementation record for the offline paper-shaped capsule axis fit-audit row in the
  partial `cpd_paper_offline_report`.
- [CPD paper priority-queue trace audit record](records/2026-05-16-cpd-paper-priority-queue-trace-audit.md):
  dated implementation record for the topology-only offline priority-queue trace audit in the
  partial `cpd_paper_offline_report`.
- [CPD paper component-pair edge insertion record](records/2026-05-16-cpd-paper-component-pair-edge-insertion.md):
  dated implementation record for the threshold-disabled offline component-pair insertion audit in
  the partial `cpd_paper_offline_report`.
- [CPD paper component-pair threshold blocking record](records/2026-05-16-cpd-paper-component-pair-threshold-blocking.md):
  dated implementation record for the finite-threshold offline component-pair block audit in the
  partial `cpd_paper_offline_report`.
- [CPD paper postprocess audit record](records/2026-05-16-cpd-paper-postprocess-audit.md):
  dated implementation record for the explicit offline enclosed-primitive postprocess cull audit in
  the partial `cpd_paper_offline_report`.
- [CPD paper polygon/quad intake policy record](records/2026-05-16-cpd-paper-polygon-quad-intake-policy.md):
  dated implementation record for the offline fan-triangulated quad and polygon source-face intake
  policy audit in the partial `cpd_paper_offline_report`.
- [CPD paper OBB/sphere fit-faithfulness record](records/2026-05-16-cpd-paper-obb-sphere-fit-faithfulness.md):
  dated implementation record for the offline paper-shaped OBB/sphere fit audit in the partial
  `cpd_paper_offline_report`.
- [CPD paper duplicate-vertex preprocessing record](records/2026-05-16-cpd-paper-duplicate-vertex-preprocessing.md):
  dated implementation record for the exact-coordinate duplicate-vertex preprocessing audit in the
  partial `cpd_paper_offline_report`.
- [CPD paper faithful offline scope audit record](records/2026-05-16-cpd-paper-faithful-offline-scope-audit.md):
  dated implementation record for the offline scope-audit criteria table that keeps the lane
  partial and points the next gate to fixture-breadth expansion.
- [CPD paper fixture-breadth expansion plan record](records/2026-05-16-cpd-paper-fixture-breadth-expansion-plan.md):
  dated documentation record for the offline-only synthetic fixture-breadth plan.
- [CPD paper fixture-breadth Batch A record](records/2026-05-16-cpd-paper-fixture-breadth-batch-a.md):
  dated implementation record for the source/preprocess/intake/operator fixture-breadth slice.
- [CPD paper fixture-breadth Batch B record](records/2026-05-16-cpd-paper-fixture-breadth-batch-b.md):
  dated implementation record for the primitive-fit fixture-breadth slice.
- [CPD paper fixture-breadth Batch C record](records/2026-05-16-cpd-paper-fixture-breadth-batch-c.md):
  dated implementation record for the cost/search/stop fixture-breadth slice.
- [CPD paper fixture-breadth Batch D record](records/2026-05-16-cpd-paper-fixture-breadth-batch-d.md):
  dated implementation record for the component-pair fixture-breadth slice.
- [CPD paper fixture-breadth Batch E record](records/2026-05-16-cpd-paper-fixture-breadth-batch-e.md):
  dated implementation record for the postprocess fixture-breadth slice.
- [CPD paper fixture-breadth completion review record](records/2026-05-16-cpd-paper-fixture-breadth-completion-review.md):
  dated implementation record for the command-only synthetic completion review over planned
  Batches A-E.
- [CPD paper faithful offline generalization plan record](records/2026-05-16-cpd-paper-faithful-offline-generalization-plan.md):
  dated implementation record for the command-only planning table beyond named toy fixtures.
- [Paper reader chrome and permission validator record](records/2026-05-16-paper-reader-chrome-and-permission-validator.md):
  reader-facing CPD paper companion cleanup that removes internal review chrome and tightens paper
  asset permission-evidence validation without changing reproduction or benchmark evidence.

## DeepDive Package

- [DeepDive README](deepdive/README.md): reviewer-facing navigation and editing rules.
- [Message Map](deepdive/message-map.md): canonical story, safe wording, unsafe claims, proof point, and support request.
- [Application Draft](deepdive/application.md): realistic DeepDive application text.
- [One-Page Summary](deepdive/one-page-summary.md): concise leadership and reviewer brief.
- [Pitch Outline](deepdive/pitch-outline.md): 20-30 minute talk structure.
- [Review Q&A](deepdive/review-qa.md): preparation for Taste, Benchmark, User Experience, and Value Delivering.
- [Evidence Status](deepdive/evidence-status.md): what is supported now, what is future evidence, and what must not be claimed.

## Design References

- [Project Scope](design/project-scope.md): project boundaries, current non-goals, and staged ambition.
- [System Architecture](design/system-architecture.md): intended compiler components and current skeleton status.
- [Research Roadmap](design/research-roadmap.md): Phase 0 through Phase 4 route.
- [Evaluation Plan](design/evaluation-plan.md): baselines, tasks, metrics, reporting, phase gates, and no-go criteria.
- [Benchmark Protocol](design/benchmark-protocol.md): asset categories, license policy, normalization, splits, task templates, and failure taxonomy.
- [CPD-like face-merge explainer](reference/cpd-like-face-merge-explainer.md):
  plain-language explanation of the current geometry-only baseline and why it is not a full CPD
  paper reproduction.
- [CPD paper story status](reference/cpd-paper-story-status.md):
  plain-language map from the paper's reproduction story to the repository's current workbench
  status and next slices.
- [CPD pipeline step-by-step explainer](reference/cpd-pipeline-step-by-step-explainer.md):
  plain-language guide to the difference between the CPD algorithm steps, the Newton workbench
  steps, and benchmark/evaluation claims.
- [CPD paper reproduction gap matrix](reference/cpd-paper-reproduction-gap-matrix.md):
  row-by-row audit of paper requirements, current repository artifacts, surrogate status,
  offline-first work, Newton runtime admissibility, and claim boundaries.
- [CPD paper-faithful offline lane spec](reference/cpd-paper-faithful-offline-lane-spec.md):
  offline-only specification for the planned fixture-scoped paper operator, primitive-fit,
  collapse-cost, search, and postprocessing lane before any real-USD, Newton, or benchmark
  expansion.
- [CPD paper fixture-breadth expansion plan](reference/cpd-paper-fixture-breadth-expansion-plan.md):
  offline-only planning artifact that maps the current scope-audit blockers to the next planned
  synthetic fixture batches.
- [CPD objective report alignment](reference/cpd-objective-report-alignment.md):
  plain-language boundary between design-aligned surrogate objective accounting and a
  paper-faithful CPD objective implementation.
- [Newton-native primitive bundle explainer](reference/newton-native-primitive-bundle-explainer.md):
  plain-language explanation of what the latest `cylinder`/`cone`/`ellipsoid` runtime diagnostic
  bundle adds to the CPD paper story, and what it does not claim.
- [Newton-native fitting comparison](reference/newton-native-fitting-comparison.md):
  plain-language explanation of the opt-in synthetic comparison where simple native fitters emit
  `cylinder`, `cone`, and `ellipsoid`, now with candidate weighted-volume audit tables, with bed
  and Franka handled by the separate real-USD probe comparison.
- [Synthetic native selection audit explainer](reference/synthetic-native-selection-audit-explainer.md):
  field-by-field guide to the candidate weighted-volume table and its claim boundary in the CPD
  paper story.
- [Bed and Franka native fitting next steps](reference/bed-franka-native-fitting-next-steps.md):
  historical execution-order guide for the now-completed move from synthetic native fitting to
  real-USD old/new reports and then Newton contact/task smokes.
- [Bed and Franka native probe comparison](reference/bed-franka-native-probe-comparison.md):
  completed real-USD diagnostic-smoke guide for capped bed and capped Franka old/new fitting,
  contact, and gated task probes.
- [Real USD native probe in the CPD paper story](reference/real-usd-native-probe-paper-story-explainer.md):
  plain-language explanation of why the latest bed/Franka slice is a downstream diagnostic
  milestone, not native primitive improvement or full CPD reproduction evidence.
- [CPD latest diagnostic loop explainer](reference/cpd-latest-diagnostic-loop-explainer.md):
  plain-language explanation of the candidate-loss diagnosis, controlled cylinder-axis fitting
  update, synthetic checks, and bed/Franka Newton-gated rerun as one repeatable CPD workbench loop.
- [Asset mirror materialization](reference/asset-mirror-materialization.md):
  guide to the ignored repo-local USD mirrors for bed and Franka, including material/texture
  closure status and claim boundaries.
- [CPD next steps after real USD mirrors](reference/cpd-next-steps-after-real-usd-mirrors.md):
  plain-language roadmap for locking the current real-USD baseline, diagnosing why boxes still
  win, and making the next primitive-fitting or merge-search change safely.

## Source Intake And Planning

- [Temporary source documents](tmp/): quarantined source intake used during bootstrap; not
  canonical reviewer-facing claims.
- [Environment readiness operations](operations/environment.md): local runtime contract, required
  variables, readiness command, status meanings, and artifact policy.
- [Clean Newton environment readiness record](records/2026-05-14-clean-newton-environment-readiness.md):
  current clean local Python/Newton environment readiness evidence.
- [Geometry-only CPD-like smoke record](records/2026-05-14-cpd-like-geometry-smoke-slice.md):
  capped bed USD primitive proposal smoke evidence.
- [CPD-like face-merge explainer record](records/2026-05-14-cpd-like-face-merge-explainer.md):
  documentation clarification for the current baseline's role in the CPD paper story.
- [Current CPD-like status and Newton probe next step](records/2026-05-14-current-cpd-like-status-and-newton-probe-next-step.md):
  separates environment readiness, geometry-only evidence, and the unimplemented Newton simulation
  probe layer.
- [Newton contact smoke record](records/2026-05-14-newton-contact-smoke.md):
  first contact-only Newton canary consuming CPD-like primitive proposals.
- [Newton drop/settle record](records/2026-05-14-newton-drop-settle.md):
  first named task-level Newton smoke diagnostic consuming the CPD-like collision package.
- [Newton sphere-rain record](records/2026-05-15-newton-sphere-rain.md):
  second named task-level Newton smoke diagnostic using a contact-density proxy over the capped
  bed CPD-like collision package.
- [Franka CPD-like smoke record](records/2026-05-15-franka-cpd-like-smoke.md):
  Franka/simple robot USD-open and capped geometry-only CPD-like smoke evidence.
- [CPD-like component-merge gate record](records/2026-05-15-cpd-like-component-merge-gate.md):
  opt-in disconnected-component merge gate and merge-cost reporting evidence.
- [CPD-like objective report record](records/2026-05-15-cpd-like-objective-report.md):
  offline paper-aligned surrogate objective report evidence for the capped bed CPD-like baseline.
- [CPD-like synthetic comparison record](records/2026-05-15-cpd-like-synthetic-comparison.md):
  command-only deterministic synthetic objective comparison for topology-only versus
  component-merge accounting.
- [CPD-like cost-guided merge record](records/2026-05-15-cpd-like-cost-guided-merge.md):
  focused cost-guided merge-search smoke over one deterministic synthetic fixture.
- [Cost-guided merge step trace record](records/2026-05-16-cost-guided-merge-step-trace.md):
  synthetic offline merge-step trace diagnostic accounting for the existing cost-guided fixture.
- [CPD synthetic expected-failure workbench record](records/2026-05-15-cpd-synthetic-expected-failure-workbench.md):
  command-only deterministic expected-failure workbench that reports known CPD-paper gaps as
  diagnostic flags.
- [CPD expected-failure master verification record](records/2026-05-15-cpd-expected-failure-master-verification.md):
  post-merge master verification for the expected-failure workbench slice.
- [CPD capped-cylinder proxy record](records/2026-05-15-cpd-capped-cylinder-proxy.md):
  opt-in offline capped-cylinder geometry proposal proxy and reduced unsupported paper primitive
  gap evidence.
- [CPD capped-cylinder master verification record](records/2026-05-15-cpd-capped-cylinder-master-verification.md):
  post-merge master verification for the capped-cylinder proxy slice.
- [Big Goal 1 completion audit](records/2026-05-15-big-goal-1-completion-audit.md):
  completion audit for the minimal CPD-like diagnostic workbench goal.
- [Newton-native primitive policy record](records/2026-05-15-newton-native-primitive-policy.md):
  policy update that makes runtime primitive expansion Newton-native first.
- [Newton native primitive bundle record](records/2026-05-15-newton-native-primitive-bundle.md):
  mapping, builder dispatch, bounds, and clean-env synthetic smoke evidence for `cylinder`,
  `cone`, and `ellipsoid`.
- [Newton native bundle explainer docs record](records/2026-05-15-newton-native-bundle-explainer-docs.md):
  documentation update that explains the latest native runtime bundle in the CPD paper story.
- [Newton native fitting comparison record](records/2026-05-15-newton-native-fitting-comparison.md):
  opt-in synthetic native fitting comparison and pointer to the bed/Franka probe scope.
- [Synthetic native selection audit record](records/2026-05-15-synthetic-native-selection-audit.md):
  candidate weighted-volume audit tables explaining why the six-kind native lane selects
  `cylinder`, `cone`, and `ellipsoid` on deterministic toy meshes.
- [Synthetic native selection audit explainer docs record](records/2026-05-15-synthetic-native-selection-audit-explainer-docs.md):
  documentation update with a field-by-field explanation of the candidate audit table.
- [Bed Franka native fitting next steps docs record](records/2026-05-15-bed-franka-native-fitting-next-steps-docs.md):
  documentation update that clarifies the next real-USD old/new comparison sequence.
- [Real USD native fitting comparison record](records/2026-05-15-real-usd-native-fitting-comparison.md):
  capped bed and capped Franka old/new offline diagnostic report evidence.
- [Real USD candidate audit record](records/2026-05-15-real-usd-candidate-audit.md):
  pre-cylinder-axis per-selected-cluster candidate accounting, superseded for current status by
  the candidate-loss/cylinder-axis record.
- [Real USD native contact comparison record](records/2026-05-15-real-usd-native-contact-comparison.md):
  capped bed and capped Franka old/new contact-canary evidence under the clean Newton conda
  environment.
- [Real USD native task comparison record](records/2026-05-15-real-usd-native-task-comparison.md):
  gated drop/settle and sphere-rain task-smoke evidence for the capped bed and capped Franka
  old/new packages.
- [Bed Franka native probe completion audit](records/2026-05-15-bed-franka-native-probe-completion-audit.md):
  final checklist mapping the requested five-step objective to code, configs, reports, records,
  verification, and review fixes.
- [Real USD native probe story explainer docs record](records/2026-05-15-real-usd-native-probe-story-explainer-docs.md):
  documentation update that explains the latest real-USD native probe slice in the CPD paper
  reproduction story.
- [Real USD asset mirror materialization record](records/2026-05-15-real-usd-asset-mirror-materialization.md):
  ignored repo-local mirror materialization for the current bed and Franka smoke USDs.
- [Real USD mirrors next steps docs record](records/2026-05-15-real-usd-mirrors-next-steps-docs.md):
  documentation update that expands the asset mirror norm and records the next CPD-like
  candidate-loss diagnosis sequence.
- [Candidate loss diagnosis and cylinder axis record](records/2026-05-15-candidate-loss-diagnosis-and-cylinder-axis.md):
  controlled cylinder-axis fitting update, synthetic rerun, real-USD candidate-loss diagnosis,
  and bed/Franka Newton-gated rerun.
- [Candidate loss triage record](records/2026-05-15-candidate-loss-triage.md):
  next-slice triage metadata for near-miss extension candidates and low-support native-extension
  selections in the real-USD candidate-loss diagnosis.
- [Low-support native extension admissibility record](records/2026-05-15-low-support-native-extension-admissibility.md):
  support-aware admissibility guard for low-support native-extension candidates, with current
  bed/Franka support-aware rerun and Newton diagnostic-gate evidence.
- [Cylinder near-miss cluster fixture record](records/2026-05-16-cylinder-near-miss-cluster-fixture.md):
  synthetic support-admissible cylinder near-miss fixture for the next primitive-fitting or
  merge/search slice.
- [Cylinder near-miss fit ablation record](records/2026-05-16-cylinder-near-miss-fit-ablation.md):
  synthetic lower-bound diagnostic showing this fixture cannot be flipped by radial-center
  refinement while preserving containment.
- [Cylinder near-miss scoring sensitivity record](records/2026-05-16-cylinder-near-miss-scoring-sensitivity.md):
  synthetic counterfactual scoring-sensitivity diagnostic for the same near-miss fixture, without
  applying a scoring-policy change.
- [Cylinder near-miss scoring policy ablation record](records/2026-05-16-cylinder-near-miss-scoring-policy-ablation.md):
  synthetic report-only scoring-policy ablation for the same near-miss fixture, without changing
  default selection or Newton packages.
- [Cylinder scoring policy guardrail record](records/2026-05-16-cylinder-scoring-policy-guardrail.md):
  synthetic boxy cuboid negative-control extension for the report-only scoring-policy ablation.
- [Cylinder scoring policy selection probe record](records/2026-05-16-cylinder-scoring-policy-selection-probe.md):
  synthetic offline opt-in scoring-policy selection probe where the near-miss flips and the boxy
  guardrail remains box, without changing default packages or Newton tasks.
- [Cylinder scoring policy package probe record](records/2026-05-16-cylinder-scoring-policy-package-probe.md):
  explicitly opt-in synthetic package probe where the near-miss package changes to `cylinder`,
  the boxy guardrail remains `box`, and a Newton shape-mapping summary is recorded without
  running Newton contact or task diagnostics.
- [Cylinder scoring policy Newton probe record](records/2026-05-16-cylinder-scoring-policy-newton-probe.md):
  explicitly opt-in synthetic Newton diagnostic over the changed near-miss package pair, with
  contact-gated drop/settle and sphere-rain task-smoke status under recorded settings.
- [Controlled merge-search package probe record](records/2026-05-16-controlled-merge-search-package-probe.md):
  command-only synthetic package-path probe that carries the existing cost-guided merge-search
  fixture into `CollisionPackage` and Newton shape-mapping accounting.
- [Controlled merge-search Newton probe record](records/2026-05-16-controlled-merge-search-newton-probe.md):
  synthetic contact-gated Newton task-smoke probe over the changed controlled merge/search package
  pair.
- [Cost-guided lookahead merge record](records/2026-05-16-cost-guided-lookahead-merge.md):
  command-only synthetic two-step lookahead merge/search diagnostic over one deterministic trap
  fixture.
- [Cost-guided lookahead package probe record](records/2026-05-16-cost-guided-lookahead-package-probe.md):
  command-only synthetic package-path and Newton shape-mapping probe for the lookahead-changed
  toy package pair.
- [Cost-guided lookahead Newton probe record](records/2026-05-16-cost-guided-lookahead-newton-probe.md):
  synthetic contact-gated Newton task-smoke probe for the lookahead-changed toy package pair.
- [Four-block slice report record](records/2026-05-16-four-block-slice-report.md):
  command-only evidence map for the recorded cost-guided lookahead synthetic slice across
  primitive fitting/selection, merge/search, offline diagnostics, and Newton task comparison. It
  links existing dated records and does not rerun source reports, USD loading, or Newton tasks.
- [Newton CPD workbench four-block status audit](records/2026-05-16-newton-cpd-workbench-four-block-status-audit.md):
  status map for primitive fitting/selection, merge/search, offline reports, and Newton task
  comparison, including current gaps and the recommended next slice.
- [Four-block workbench completion audit](records/2026-05-16-four-block-workbench-completion-audit.md):
  completion audit that maps the bounded four-block workbench objective to the report, CLI, tests,
  dated records, review fixes, and verification evidence.
- [CPD pipeline step-by-step explainer record](records/2026-05-16-cpd-pipeline-step-by-step-explainer.md):
  documentation update that explains the whole mesh-to-benchmark pipeline and where the current
  Newton workbench fits relative to the CPD paper algorithm.
- [CPD paper gap matrix and offline lane spec record](records/2026-05-16-cpd-paper-gap-matrix-and-offline-lane-spec.md):
  documentation update that turns the paper reproduction gap into an offline-first paper-lane
  spec, without adding benchmark, Newton runtime, real-USD, or collision-quality evidence.
- [CPD paper offline first fixture slice record](records/2026-05-16-cpd-paper-offline-first-fixture-slice.md):
  partial command-only offline paper-lane audit over `paper_single_box` and `paper_two_face_merge`,
  without Newton, real-USD, package, benchmark, or collision-quality claims.
- [CPD paper frustum/trapezoid audit record](records/2026-05-16-cpd-paper-frustum-trapezoid-audit.md):
  partial command-only offline fit-audit row expansion for `frustum` and `trapezoidal_prism`,
  without Newton, real-USD, package, benchmark, or collision-quality claims.
- [CPD paper flat capped-cylinder audit record](records/2026-05-16-cpd-paper-flat-capped-cylinder-audit.md):
  partial command-only offline fit-audit row expansion for paper flat capped cylinders, without
  Newton, real-USD, package, benchmark, or collision-quality claims.
- [CPD paper capsule axis audit record](records/2026-05-16-cpd-paper-capsule-axis-audit.md):
  partial command-only offline fit-audit row expansion for paper-shaped capsule axis candidates,
  without Newton, real-USD, package, benchmark, or collision-quality claims.
- [CPD paper priority-queue trace audit record](records/2026-05-16-cpd-paper-priority-queue-trace-audit.md):
  partial command-only offline topology priority-queue trace audit with stale-pruning records,
  without Newton, real-USD, package, benchmark, or collision-quality claims.
- [Paper reference numbering fix record](records/2026-05-16-paper-reference-numbering-fix.md):
  reader-facing CPD paper companion import fix that resolves internal source references into paper
  numbers and does not change reproduction or benchmark evidence.
- [Paper reader chrome and permission validator record](records/2026-05-16-paper-reader-chrome-and-permission-validator.md):
  reader-facing CPD paper companion cleanup that removes internal review chrome and tightens paper
  asset permission-evidence validation without changing reproduction or benchmark evidence.
- [CPD latest diagnostic loop explainer docs record](records/2026-05-15-cpd-latest-diagnostic-loop-explainer-docs.md):
  documentation update that explains the latest candidate-loss and cylinder-axis slice as a
  repeatable diagnostic loop in the CPD paper story.
- [CPD paper companion MVP record](records/2026-05-15-cpd-paper-companion-mvp.md):
  Astro + MDX bilingual CPD paper companion scaffold with source-paper claim namespacing,
  permission-record-pending status, and AI-assisted draft translation status.
- [CPD full text import and translation record](records/2026-05-15-cpd-full-text-import-translation.md):
  full-section CPD companion import with AI-assisted draft translations, gated source LaTeX
  blocks, and `not_started` reproduction states.
- [CPD objective alignment and next steps record](records/2026-05-15-cpd-objective-alignment-and-next-steps.md):
  documentation update that clarifies objective-report paper alignment and the next algorithmic
  slices.
- [Three-slice final verification record](records/2026-05-15-three-slice-final-verification.md):
  final verification for sphere-rain, Franka smoke, and component-merge gate.
- [CPD paper story status docs record](records/2026-05-15-cpd-paper-story-status-docs.md):
  documentation update that clarifies where the repository sits in the full CPD paper story.
- [CPD cost-guided story explainer record](records/2026-05-15-cpd-cost-guided-story-explainer.md):
  documentation update that explains the cost-guided merge smoke as the first restricted
  objective-guided decision hook in the CPD paper story.
- [AABB-normalized merge-excess explainer record](records/2026-05-15-aabb-normalized-merge-excess-explainer.md):
  documentation update that explains the merge-excess surrogate cost used by the CPD-like
  cost-guided smoke.
- [CPD Eq.4 alignment metadata record](records/2026-05-15-cpd-eq4-alignment-metadata.md):
  structured metadata update mapping current surrogate merge-excess terms to the CPD paper Eq.4
  role without claiming Eq.4 implementation.
- [Bootstrap plan](superpowers/plans/2026-05-14-deepdive-first-repo-bootstrap.md): implementation checklist.
- [Bootstrap design](superpowers/specs/2026-05-14-deepdive-first-repo-bootstrap-design.md): original design rationale.
- [Environment normalization design](superpowers/specs/2026-05-14-environment-normalization-design.md):
  Phase 1 environment-readiness scope and claim boundary.
- [Environment normalization plan](superpowers/plans/2026-05-14-environment-normalization.md):
  TDD implementation plan for the readiness checker and docs.
- [Newton-native primitive policy design](superpowers/specs/2026-05-15-newton-native-primitive-policy-design.md):
  design decision that separates the Newton-native runtime lane from the CPD paper-alignment
  offline lane.
- [Newton native primitive bundle plan](superpowers/plans/2026-05-15-newton-native-primitive-bundle.md):
  TDD implementation plan for the native `cylinder`, `cone`, and `ellipsoid` runtime bundle.
- [Newton native fitting comparison plan](superpowers/plans/2026-05-15-newton-native-fitting-comparison.md):
  TDD implementation plan for the opt-in native fitting comparison and bed/Franka scope update.
- [Bed Franka native probe completion plan](superpowers/plans/2026-05-15-bed-franka-native-probe-completion.md):
  TDD implementation plan for the real-USD old/new fitting, contact, and gated task comparison
  slice.

## Configs And Artifacts

- `configs/deepdive/mvp.yaml`: DeepDive-facing dry-run MVP config.
- `configs/experiments/phase0_baseline.yaml`: Phase 0 proof-point config scaffold.
- `configs/experiments/cpd_like_component_merge_gate.yaml`: opt-in CPD-like component-merge gate
  smoke config.
- `configs/experiments/cpd_like_objective_report.yaml`: offline CPD-like objective report smoke
  config.
- `configs/experiments/cpd_like_capped_cylinder_proxy.yaml`: opt-in offline capped-cylinder
  proxy objective-report smoke config.
- `configs/experiments/newton_native_fitting_comparison.yaml`: opt-in synthetic native fitting
  comparison config that points to the real-USD probe comparison config.
- `configs/experiments/bed_franka_native_probe_comparison.yaml`: real-USD capped bed and capped
  Franka old/new fitting, contact, and gated task-smoke comparison config.
- `configs/experiments/cylinder_scoring_policy_newton_probe.yaml`: explicitly opt-in synthetic
  near-miss package-pair Newton task-smoke config.
- `npc-compile --run-cpd-like-synthetic-comparison`: command-only deterministic synthetic
  objective comparison, recorded in `experiments/registry.yaml` without a config file.
- `npc-compile --run-cpd-like-cost-guided-synthetic-comparison`: command-only deterministic
  cost-guided synthetic comparison, recorded in `experiments/registry.yaml` without a config file.
- `npc-compile --run-cpd-like-controlled-merge-search-package-probe`: command-only synthetic
  package-path probe for the existing cost-guided merge-search fixture, with Newton shape-mapping
  coverage and no contact/task execution.
- `npc-compile --config configs/experiments/controlled_merge_search_newton_probe.yaml
  --run-cpd-like-controlled-merge-search-newton-probe`: synthetic-only contact-gated Newton
  task-smoke comparison for the controlled merge-search default and opt-in packages.
- `npc-compile --run-cpd-like-cost-guided-lookahead-merge-report`: command-only synthetic
  two-step lookahead merge/search diagnostic over one trap fixture, with no package or Newton task
  execution.
- `npc-compile --run-cpd-like-cost-guided-lookahead-package-probe`: command-only synthetic
  package-path and Newton shape-mapping probe for the lookahead-changed toy package pair, with no
  contact/task execution.
- `npc-compile --config configs/experiments/cost_guided_lookahead_newton_probe.yaml
  --run-cpd-like-cost-guided-lookahead-newton-probe`: synthetic contact-gated Newton task-smoke
  probe for the lookahead-changed toy package pair.
- `npc-compile --run-cpd-like-four-block-slice-report`: command-only evidence map for the
  recorded lookahead slice. It links existing dated records and does not rerun source reports,
  USD loading, real assets, or Newton tasks.
- `npc-compile --run-cpd-paper-offline-report`: command-only partial offline paper-lane audit over
  `paper_single_box`, `paper_two_face_merge`, `paper_three_face_chain`,
  `paper_disconnected_components`, `paper_component_pair_threshold_blocked`,
  `paper_tiny_sphere_clamp`, `paper_duplicate_vertex_preprocessing`, `paper_frustum_like`,
  `paper_trapezoid_prism_like`, `paper_nested_primitive`, `paper_quad_face_intake`, and
  `paper_polygon_face_intake`; exits successfully when the JSON report is emitted, returns
  `status: partial`, records offline paper-shaped OBB/sphere rows, an offline paper-shaped capsule
  axis row, offline-only flat capped-cylinder/frustum/trapezoidal-prism rows, topology-only
  priority-queue trace fields, a threshold-disabled component-pair insertion trace, a
  finite-threshold component-pair blocked trace, one explicit enclosed-primitive postprocess cull
  audit, one quad plus one five-vertex polygon intake policy audit, and one exact-coordinate
  duplicate-vertex preprocessing audit, Batch A fixture-breadth source/preprocess/intake/operator
  cases, Batch B primitive-fit breadth cases for all six paper primitive names, Batch C
  cost/search/stop breadth cases for weighted-priority ordering, equal-cost queue
  tie/eager-stale-prune behavior, and one positive finite component-pair threshold block, plus
  Batch D component-pair breadth cases for multi-candidate ordering and capped skipped-pair
  accounting, plus Batch E postprocess breadth cases for rotated nested OBB containment and
  explicit cross-type unsupported no-cull accounting, plus a fixture-breadth completion review
  that closes only the planned synthetic Batch A-E breadth gate, plus a command-only
  generalization planning table that closes only the planning gate, plus an offline source-policy
  matrix that closes only `paper_generalization_batch_a_source_policy`, plus an offline
  primitive-fit engine matrix that closes only
  `paper_generalization_batch_b_primitive_fit_engine`, plus an offline search-engine matrix that
  closes only `paper_generalization_batch_c_search_engine`, plus an offline postprocess-policy
  matrix that closes only `paper_generalization_batch_d_postprocess_policy`, plus an offline
  package-boundary readiness matrix that closes only
  `paper_generalization_batch_e_package_boundary_readiness`, plus an offline
  changed-decomposition output contract that closes only
  `paper_offline_changed_decomposition_output_contract`, plus an offline package-adapter contract
  that closes only `paper_package_adapter_contract`, plus an offline unsupported-primitive policy
  that closes only `paper_package_adapter_unsupported_primitive_policy`, plus an offline
  mapped-subset package-conversion plan that closes only
  `paper_package_conversion_mapped_subset_plan`, plus an offline mapped-subset candidate matrix
  that closes only `paper_mapped_subset_conversion_candidate_matrix`, plus an offline mapped-subset
  adapter-preflight contract that closes only `paper_mapped_subset_adapter_preflight_contract`,
  plus an offline mapped-subset PrimitiveSpec dry-run contract that closes only
  `paper_mapped_subset_primitivespec_dry_run_contract`, plus an offline mapped-subset
  PrimitiveSpec validation contract that closes only
  `paper_mapped_subset_primitivespec_validation_contract`, plus an offline mapped-subset
  PrimitiveSpec generation-preflight contract that closes only
  `paper_mapped_subset_primitivespec_generation_preflight_contract`, plus an offline mapped-subset
  PrimitiveSpec generation contract that closes only
  `paper_mapped_subset_primitivespec_generation_contract`, plus an offline mapped-subset
  PrimitiveSpec candidate-source audit that closes only
  `paper_mapped_subset_primitivespec_candidate_source_contract`, plus an offline mapped-subset
  native-current fixture source-row contract that closes only
  `paper_mapped_subset_native_current_fixture_contract`, plus an offline native-fixture
  PrimitiveSpec-like dict generation contract that closes only
  `paper_mapped_subset_primitivespec_native_fixture_generation_contract`, plus an offline
  native-fixture serialization/schema-stability contract that closes only
  `paper_mapped_subset_primitivespec_native_fixture_serialization_contract`, plus a
  runtime-boundary preflight contract that closes only
  `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`, plus a single-fixture
  runtime-construction contract that closes only
  `paper_mapped_subset_primitivespec_runtime_construction_contract`, plus a single-fixture
  package-generation preflight contract that closes only
  `paper_mapped_subset_collision_package_generation_preflight_contract`, plus a single-fixture
  CollisionPackage generation contract that closes only
  `paper_mapped_subset_collision_package_generation_contract`, plus a single-fixture
  runtime-admissibility preflight contract that closes only
  `paper_mapped_subset_runtime_admissibility_preflight_contract`. It also records a
  runtime-admissibility contract that closes only
  `paper_mapped_subset_runtime_admissibility_contract` as one offline/static box-schema and
  finite-geometry check for the same synthetic package, plus a Newton shape-mapping preflight
  contract that closes only `paper_mapped_subset_newton_shape_mapping_preflight_contract` as one
  static mapper-handoff row, plus a Newton shape-mapping contract that closes only
  `paper_mapped_subset_newton_shape_mapping_contract` as one report-scoped static descriptor row,
  plus a Newton shape runtime-boundary preflight contract that closes only
  `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract` as one later
  runtime-construction candidate row, plus a Newton shape runtime-construction contract that
  closes only `paper_mapped_subset_newton_shape_runtime_construction_contract` as one repo-local
  `NewtonShapeMapping.to_dict()` report record, plus a Newton shape runtime builder-preflight
  contract that closes only `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`
  as one JSON-safe future box builder call plan with no builder invocation, plus a Newton shape
  runtime builder-construction contract that closes only
  `paper_mapped_subset_newton_shape_runtime_builder_construction_contract` as one JSON-safe
  repo-local recording-builder `add_shape_box` call artifact with no real Newton builder call,
  plus a Newton engine-builder boundary preflight contract that closes only
  `paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract` as one
  offline/static checklist row with no real Newton import, no real `newton.ModelBuilder`, no real
  builder shape call, no model finalization, and no collision pipeline, plus a Newton/Warp
  environment-probe contract that closes only
  `paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract` as one
  bounded provenance row with no runtime execution.
  It keeps
  scope-audit table
  with `decision: remain_partial`, reports
  `next_required_gate: paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract`,
  keeps
  `paper_faithful_offline_supported: false`, and does not run Newton, real USD,
  real Newton engine shape construction, runtime execution, or benchmarks.
- `npc-compile --run-cpd-like-expected-failure-workbench`: command-only deterministic
  expected-failure synthetic workbench, recorded in `experiments/registry.yaml` without a config
  file.
- `npc-compile --config configs/experiments/newton_native_fitting_comparison.yaml
  --run-newton-native-fitting-comparison`: deterministic synthetic old/new comparison for opt-in
  native `cylinder`, `cone`, and `ellipsoid` fitters, including candidate audit tables.
- `npc-compile --config configs/experiments/bed_franka_native_probe_comparison.yaml
  --run-real-usd-native-fitting-comparison`: capped bed and capped Franka real-USD old/new
  offline diagnostic report with candidate audit summaries.
- `npc-compile --config configs/experiments/bed_franka_native_probe_comparison.yaml
  --run-real-usd-native-contact-comparison`: full-mapping-gated contact canary comparison.
- `npc-compile --config configs/experiments/bed_franka_native_probe_comparison.yaml
  --run-real-usd-native-task-comparison`: contact-gated drop/settle and sphere-rain comparison.
- `npc-compile --config configs/experiments/cylinder_scoring_policy_newton_probe.yaml
  --run-cpd-like-cylinder-scoring-policy-newton-probe`: synthetic-only contact-gated Newton
  task-smoke comparison for the default `box` and opt-in `cylinder` near-miss packages.
- `npc-compile --config configs/experiments/bed_franka_native_probe_comparison.yaml
  --materialize-assets`: ignored repo-local USD dependency-closure mirror for the current bed and
  Franka smoke assets.
- `scripts/env/readiness_check.py`: local environment-readiness JSON checker.
- `experiments/registry.yaml`: experiment registry and claim-support status.
- `assets/`, `reports/`, and `archive/`: artifact boundaries; large/generated outputs stay out
  of git.
- `AGENTS.md`: repo-local rules for future agentic work.

## Claim Boundary

Safe current claim: proposal for primitive-first, Newton-checker-planned, fallback-aware collision asset compilation.

Additional current evidence: executable environment-readiness diagnostics can record dependency
gaps, source provenance, and the current clean local env `smoke_passed` status. The CPD-like
geometry path can produce a restricted primitive proposal smoke report. The Newton contact canary
can confirm representative primitive ingestion and contact pipeline output. The Newton drop/settle
and sphere-rain diagnostics can run two named task smokes for the capped bed CPD-like collision
package. The Franka/simple robot smoke can open a second asset class and run capped first-mesh
geometry-only proposals. The CPD-like component-merge gate can report disconnected-component
merge candidates and normalized excess-volume accounting. The offline CPD-like objective report
can summarize paper-aligned surrogate terms and Eq.4 alignment metadata for that baseline. The
synthetic objective comparison can inspect deterministic topology-only versus component-merge
accounting on toy meshes. The cost-guided merge-search smoke can inspect one old/new surrogate-cost
decision on a toy mesh. The expected-failure synthetic workbench can report whether expected
limitation flags are observed for known CPD-paper gaps; its `smoke_passed` status means expected
limitations were reported, not decomposition success. The capped-cylinder proxy can report an
opt-in offline objective smoke where the unsupported paper primitive gap decreases from 3 to 2,
with no Newton mapping or task-level improvement claim.
The runtime primitive roadmap is Newton-native first: the native `cylinder`, `cone`, and
`ellipsoid` bundle now has mapping, diagnostic construction, tests, and a dated synthetic runtime
smoke record. The opt-in native fitting comparison can emit those kinds on deterministic synthetic
meshes, but this does not mean they are default asset behavior or real-USD improvement evidence.
The synthetic cylinder scoring-policy Newton probe can run contact-gated task smokes over one
explicitly opt-in changed near-miss package pair. The controlled merge-search package probe can
carry one synthetic merge/search behavior difference into package and mapping accounting without
running Newton tasks. The controlled merge-search Newton probe can run contact-gated task smokes
over that changed synthetic merge/search package pair, still without default merge-policy,
real-USD, collision-quality, benchmark, or CPD reproduction claims. The synthetic two-step
lookahead merge report can record one bounded offline merge/search decision change. The follow-on
lookahead package probe adds package-path and mapping accounting, and the completed lookahead
Newton probe adds synthetic contact-gated task-smoke status under recorded settings. These
lookahead probes still do not add real-USD, collision-quality, benchmark, or CPD reproduction
evidence. The real-USD bed/Franka probe
comparison can run old/new lanes through offline reports, candidate
diagnostics, contact canaries, and gated task smokes; the current support-aware run keeps bed and
capped Franka at boxes while reporting three capped Franka raw-cost cylinder candidates as
support-blocked accounting, but it still does not prove native primitive quality improvement. It
does not add support for paper-only
`capped_cylinder`, `frustum`, or `trapezoidal_prism` in Newton runtime.
These evidence layers are not benchmark, collision-quality, whole-robot quality, real
contact-stress, or CPD reproduction evidence.

Current non-goals: no safety guarantee, no real-world transfer claim, no deployment readiness claim, no benchmark superiority claim, no CPD reproduction claim, and no complete replacement of convex decomposition.
