# CPD Paper Story Status

This page explains where the repository sits in the story of reproducing
Convex Primitive Decomposition for Collision Detection. It is a status map, not new experiment
evidence, and not a claim that the paper algorithm has been reproduced.

## Plain Summary

The paper story is about turning a complex mesh into a small set of simple collision primitives
that make collision detection faster or more reliable.

The repository has not reached that full result. It has reached the workbench stage:

1. USD assets can be opened, mirrored into ignored repo-local paths, and capped meshes can be
   extracted.
2. A simple CPD-like face-merge baseline can produce primitive proposals.
3. Those proposals can be wrapped as a collision package.
4. An offline objective report can summarize paper-aligned surrogate geometry terms.
5. A synthetic objective comparison can exercise the same accounting on inspectable toy meshes.
6. A focused cost-guided merge-search smoke can use one objective-report term as a toy-fixture
   merge decision cost.
7. A deterministic expected-failure workbench can keep known CPD-paper gaps visible as diagnostic
   flags.
8. An opt-in offline `capped_cylinder` proxy can reduce the named unsupported paper primitive gap
   from 3 to 2.
9. Newton can run narrow smoke diagnostics against the already mapped primitive package.
10. A synthetic Newton-native package can exercise `box`, `sphere`, `capsule`, `cylinder`, `cone`,
    and `ellipsoid` through contact, drop/settle, and sphere-rain diagnostics.
11. An opt-in native fitting comparison can make the CPD-like fitter choose simple `cylinder`,
    `cone`, and `ellipsoid` proposals on deterministic synthetic meshes, including a
    squat-cylinder fixture for the controlled cylinder-axis search.
12. A synthetic native selection audit can explain those toy choices with candidate
    weighted-volume tables and surrogate-cost margins.
13. Capped bed and capped Franka real-USD lanes can run through fitting reports, candidate audit
    summaries, candidate-loss diagnosis, Newton contact canaries, and gated task smokes.
14. An explicitly opt-in synthetic package probe can carry the cylinder scoring-policy multiplier
    through `decompose_mesh` into a changed synthetic `CollisionPackage` and record a Newton
    shape-mapping summary only. It does not change default package generation and does not run
    Newton contact or task diagnostics.
15. A follow-on explicitly opt-in synthetic Newton diagnostic can run named contact, drop/settle,
    and sphere-rain smokes over that changed near-miss package pair under recorded settings.
16. A command-only synthetic controlled merge-search package-path probe can carry the existing
    `cost_guided_pair_choice` grouping difference into `CollisionPackage` and Newton shape-mapping
    accounting, without running Newton contact or task diagnostics.
17. A follow-on synthetic controlled merge-search Newton diagnostic can run named contact,
    drop/settle, and sphere-rain smokes over that changed package pair under recorded settings.
18. A command-only synthetic two-step lookahead merge/search diagnostic can show one bounded
    non-greedy grouping change on a deterministic trap fixture, without package or Newton task
    evidence.
19. A command-only synthetic lookahead package-path probe can carry that bounded grouping change
    into `CollisionPackage` lanes and Newton shape-mapping accounting, without contact/task
    execution.
20. An explicitly opt-in synthetic lookahead Newton diagnostic can run named contact, drop/settle,
    and sphere-rain smokes over that changed package pair under recorded settings.
21. A command-only four-block slice report can link the recorded lookahead evidence across
    primitive fitting/selection, merge/search, offline diagnostics, and recorded Newton task-smoke
    status without rerunning source reports, USD loading, real assets, or Newton tasks.
22. A command-only partial `cpd_paper_offline_report` can audit the first paper-lane toy fixtures
    with paper-side operator fields, offline paper-shaped OBB/sphere rows, a paper-shaped capsule
    axis row, offline-only flat capped-cylinder/frustum/trapezoidal-prism rows, collapse-cost
    fields, a topology-only priority-queue trace, threshold-disabled and finite-threshold
    component-pair traces, one explicit enclosed-primitive postprocess cull audit,
    fan-triangulated quad/polygon source-face intake policy fixtures, and one exact-coordinate
    duplicate-vertex preprocessing audit.
23. The same report now includes a scope-audit criteria table that decides the current fixture
    scope must remain `partial`, keeps `paper_faithful_offline_supported: false`, and points the
    next paper-lane gate to `paper_fixture_breadth_expansion_plan`.
24. A documentation-only fixture-breadth expansion plan now turns that gate into planned
    synthetic fixture batches.
25. Batch A of that plan is now implemented as synthetic source/preprocess/intake/operator
    fixture breadth, while the report remains partial and points next to
    `paper_fixture_breadth_batch_b`.
26. Batch B of that plan is implemented as synthetic primitive-fit breadth for all six paper
    primitive names.
27. Batch C of that plan is now implemented as synthetic cost/search/stop breadth.
28. Batch D of that plan is now implemented as synthetic component-pair breadth.
29. Batch E of that plan is now implemented as synthetic postprocess breadth.
30. A command-only synthetic fixture-breadth completion review is now implemented for planned
    Batches A-E. The report remains partial and keeps
    `paper_faithful_offline_supported: false`; the review payload records the planning-only
    `paper_faithful_offline_generalization_plan` as its follow-up gate.
31. A command-only generalization planning table is now implemented inside the same report. It
    closes only `paper_faithful_offline_generalization_plan`, keeps the report partial, keeps
    `paper_faithful_offline_supported: false`, and recorded
    `paper_generalization_batch_a_source_policy` as the immediate follow-up at the planning stage.
32. `paper_generalization_batch_a_source_policy` is now implemented as an offline source-policy
    matrix for deterministic synthetic meshes. It closes only that source-policy gate, keeps the
    report partial, and points next to
    `paper_generalization_batch_b_primitive_fit_engine`.
33. `paper_generalization_batch_b_primitive_fit_engine` is now implemented as an offline
    primitive-fit engine matrix over deterministic in-memory probes for all six paper primitive
    names. It closes only that primitive-fit engine gate, keeps the report partial, and points next
    to `paper_generalization_batch_c_search_engine`.
34. `paper_generalization_batch_c_search_engine` is now implemented as an offline search-trace
    matrix over existing deterministic topology queue, weighted-priority, equal-cost tie,
    threshold-stop, and component-pair traces. It closes only that search-engine gate, keeps the
    report partial, and points next to `paper_generalization_batch_d_postprocess_policy`.
35. `paper_generalization_batch_d_postprocess_policy` is now implemented as an offline
    postprocess-policy matrix over existing deterministic postprocess audit fixtures. It closes
    only that postprocess-policy gate, keeps the report partial, and points next to
    `paper_generalization_batch_e_package_boundary_readiness`.
36. `paper_generalization_batch_e_package_boundary_readiness` is now implemented as an offline
    package-boundary readiness matrix before package conversion. It closes only that readiness
    gate, keeps package generation/Newton/real-USD/benchmark triggers false, keeps the report
    partial, and points next to `paper_offline_changed_decomposition_output_contract`.
37. `paper_offline_changed_decomposition_output_contract` is now implemented as an offline
    changed-decomposition output contract, not a `CollisionPackage`. It closes only that output
    contract gate, keeps package generation/Newton/real-USD/benchmark triggers false, keeps the
    report partial, and points next to `paper_package_adapter_contract`.
38. `paper_package_adapter_contract` is now implemented as a command-only offline package-adapter
    contract, not a `CollisionPackage`. It closes only that adapter-contract gate, consumes the 16
    offline primitive records from the changed-decomposition output contract, classifies all
    current `trapezoidal_prism` / `offline_only_unmapped` records as
    `later_policy_required`, keeps package generation/Newton/real-USD/benchmark triggers false,
    keeps the report partial, and at that adapter-contract stage pointed to
    `paper_package_adapter_unsupported_primitive_policy`.
39. `paper_package_adapter_unsupported_primitive_policy` is now implemented as a command-only
    offline unsupported-primitive policy table, not a `CollisionPackage`. It closes only that
    policy gate, classifies all six paper primitive families, keeps the current 16
    `trapezoidal_prism` / `offline_only_unmapped` rows offline with
    `block_package_conversion`, records zero package-candidate rows, keeps
    package generation/Newton/real-USD/benchmark triggers false, keeps the report partial, and
    points next to `paper_package_conversion_mapped_subset_plan`.
40. `paper_package_conversion_mapped_subset_plan` is now implemented as a command-only offline
    mapped-subset package-conversion planning table, not a `CollisionPackage`. It closes only that
    planning gate, identifies `oriented_bounding_box`, `sphere`, and `capsule` as native-family
    review rows, keeps the current 16 `trapezoidal_prism` / `offline_only_unmapped`
    rows offline, records zero current package-conversion candidates, keeps
    package generation/Newton/real-USD/benchmark triggers false, keeps the report partial, and
    points next to `paper_mapped_subset_conversion_candidate_matrix`.
41. `paper_mapped_subset_conversion_candidate_matrix` is now implemented as a command-only offline
    candidate matrix, not a `CollisionPackage`. It closes only that candidate-matrix gate, records
    three future-family review rows, keeps the current 16 `trapezoidal_prism` /
    `offline_only_unmapped` rows blocked and offline, records zero current package-conversion
    candidates, keeps PrimitiveSpec/CollisionPackage/runtime-admissibility/Newton/real-USD/
    benchmark triggers false, keeps the report partial, and at that stage pointed next to
    `paper_mapped_subset_adapter_preflight_contract`.
42. `paper_mapped_subset_adapter_preflight_contract` is now implemented as a command-only offline
    adapter-preflight contract, not `PrimitiveSpec` generation and not a `CollisionPackage`. It
    closes only that preflight gate, records future adapter requirements, records no-op behavior
    for the current zero package-conversion-candidate state, keeps all current unmapped
    trapezoidal-prism rows offline, keeps package generation disabled, keeps
    PrimitiveSpec/CollisionPackage/runtime-admissibility/Newton/real-USD/benchmark triggers false,
    keeps the report partial, and points next to
    `paper_mapped_subset_primitivespec_dry_run_contract`.
43. `paper_mapped_subset_primitivespec_dry_run_contract` is now implemented as a command-only
    offline PrimitiveSpec dry-run contract, not real `PrimitiveSpec` generation and not a
    `CollisionPackage`. It closes only that dry-run gate, records future PrimitiveSpec shape
    requirements for OBB/box, sphere, and capsule, keeps capped cylinder and frustum blocked
    behind an approximation policy, keeps all current unmapped trapezoidal-prism rows offline/no-op,
    records zero current PrimitiveSpec candidates, records zero generated PrimitiveSpec rows,
    keeps CollisionPackage/runtime-admissibility/Newton/real-USD/benchmark triggers false, keeps
    the report partial, and points next to
    `paper_mapped_subset_primitivespec_validation_contract`.
44. `paper_mapped_subset_primitivespec_validation_contract` is now implemented as a command-only
    offline validation contract, not real `PrimitiveSpec` generation and not a `CollisionPackage`.
    It closes only that validation gate, validates the dry-run field list, mapped future shape
    labels, six family rows, 16 current no-op rows, source traceability, zero current candidates,
    zero generated PrimitiveSpecs, and false runtime/evaluation triggers, keeps the report
    partial, and points next to
    `paper_mapped_subset_primitivespec_generation_preflight_contract`.
45. `paper_mapped_subset_primitivespec_generation_preflight_contract` is now implemented as a
    command-only offline generation-preflight contract, not real `PrimitiveSpec` generation and
    not a `CollisionPackage`. It closes only that preflight gate, records the future native-family
    requirements for OBB/box, sphere, and capsule, records capped cylinder and frustum as blocked
    behind approximation policy, records trapezoidal prism as no-op/unmapped, keeps current
    generation candidates, generated PrimitiveSpecs, generated CollisionPackages, and
    runtime-admissibility checks at zero, keeps the report partial, and points next to
    `paper_mapped_subset_primitivespec_generation_contract`.
46. `paper_mapped_subset_primitivespec_generation_contract` is now implemented as a command-only
    offline PrimitiveSpec generation contract, not runtime `PrimitiveSpec` generation and not a
    `CollisionPackage`. It closes only that generation-contract gate, emits future native-family
    template rows for box/sphere/capsule, records blocked approximation-policy rows for capped
    cylinder and frustum, records trapezoidal prism as no-op/unmapped, keeps all current unmapped
    rows offline/no-op, keeps generated runtime PrimitiveSpecs, generated CollisionPackages, and
    runtime-admissibility checks at zero, keeps the report partial, and points next to
    `paper_mapped_subset_primitivespec_candidate_source_contract`.
47. `paper_mapped_subset_primitivespec_candidate_source_contract` is now implemented as a
    command-only offline PrimitiveSpec candidate-source audit, not runtime `PrimitiveSpec`
    generation and not a `CollisionPackage`. It closes only that candidate-source gate, records
    three future-only native template source rows, two blocked approximation-policy source rows,
    one no-op trapezoidal-prism family source row, and 16 traceable but ineligible current
    `trapezoidal_prism` / `offline_only_unmapped` rows. It keeps eligible current PrimitiveSpec
    candidate sources, generated PrimitiveSpecs, generated CollisionPackages, and
    runtime-admissibility checks at zero, keeps the report partial, and points next to
    `paper_mapped_subset_native_current_fixture_contract`.
48. `paper_mapped_subset_native_current_fixture_contract` is now implemented as a command-only
    offline native-current fixture source-row contract, not runtime `PrimitiveSpec` generation and
    not a `CollisionPackage`. It closes only that source-row gate, records exactly one synthetic
    `paper_single_box` selected OBB/box source row traced to the future OBB template, records one
    eligible current candidate source and one report-only PrimitiveSpec generation candidate,
    keeps generated PrimitiveSpecs, generated CollisionPackages, runtime-admissibility checks,
    Newton runtime, real-USD, benchmark, collision-quality, deployment, and certification triggers
    at zero or false, keeps the report partial, and led to the later
    `paper_mapped_subset_primitivespec_native_fixture_generation_contract` gate.
49. `paper_mapped_subset_primitivespec_native_fixture_generation_contract` is now implemented as
    a command-only offline native-fixture PrimitiveSpec-like dict generation contract, not runtime
    `PrimitiveSpec` object creation and not a `CollisionPackage`. It closes only that
    native-fixture generation gate, emits exactly one JSON-serializable report-only dict shaped
    like `PrimitiveSpec.to_dict()` for the deterministic synthetic `paper_single_box` OBB/box
    source row, keeps generated runtime PrimitiveSpecs, generated CollisionPackages,
    runtime-admissibility checks, Newton runtime, real-USD, benchmark, collision-quality,
    deployment, and certification triggers at zero or false, keeps the report partial, and points
    next to `paper_mapped_subset_primitivespec_native_fixture_serialization_contract`.
50. `paper_mapped_subset_primitivespec_native_fixture_serialization_contract` is now implemented
    as a command-only offline native-fixture serialization/schema-stability contract, not runtime
    `PrimitiveSpec` object creation and not a `CollisionPackage`. It closes only that
    serialization gate, validates strict canonical JSON and round-trip equality for exactly one
    report-only `paper_single_box` OBB/box PrimitiveSpec-like dict, keeps generated runtime
    PrimitiveSpecs, generated CollisionPackages, runtime-admissibility checks, Newton runtime,
    real-USD, benchmark, collision-quality, deployment, and certification triggers at zero or
    false, keeps the report partial, and led to the later
    `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract` gate.
51. `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract` is now implemented as a
    command-only offline runtime-boundary preflight contract, not runtime `PrimitiveSpec`
    construction and not a `CollisionPackage`. It closes only that boundary gate, consumes the
    strict native-fixture serialization row, records one later runtime-construction candidate,
    keeps runtime construction disallowed in the current gate, keeps generated runtime
    PrimitiveSpecs, generated CollisionPackages, runtime-admissibility checks, Newton runtime,
    real-USD, benchmark, collision-quality, deployment, and certification triggers at zero or
    false, keeps the report partial, and points next to
    `paper_mapped_subset_primitivespec_runtime_construction_contract`.
52. `paper_mapped_subset_primitivespec_runtime_construction_contract` is now implemented as a
    single-fixture offline runtime-construction contract, not a `CollisionPackage` and not Newton
    execution. It closes only that construction gate, consumes the runtime-boundary preflight row,
    constructs exactly one runtime `PrimitiveSpec` object from the canonical `paper_single_box`
    OBB/box preflight JSON after checking the runtime-boundary preflight row's canonical JSON
    SHA-256 fingerprint, stores only `PrimitiveSpec.to_dict()` in the report, records generated
    runtime PrimitiveSpec counts as one, keeps generated CollisionPackages, runtime-admissibility
    checks, Newton runtime, real-USD, benchmark, collision-quality, deployment, and certification
    triggers at zero or false, keeps the report partial, and points next to
    `paper_mapped_subset_collision_package_generation_preflight_contract`.
53. `paper_mapped_subset_collision_package_generation_preflight_contract` is now implemented as a
    single-fixture offline package-generation preflight contract, not actual package generation
    and not Newton execution. It consumes the runtime-construction row's
    `PrimitiveSpec.to_dict()` payload, records exactly one later package-generation candidate for
    the synthetic `paper_single_box` OBB/box row, keeps package generation disallowed in the
    current gate, keeps generated CollisionPackages, runtime-admissibility checks, Newton runtime,
    real-USD, benchmark, collision-quality, deployment, and certification triggers at zero or
    false, keeps the report partial, and points next to
    `paper_mapped_subset_collision_package_generation_contract`.
54. `paper_mapped_subset_collision_package_generation_contract` is now implemented as a
    single-fixture offline CollisionPackage generation contract, not runtime admissibility and not
    Newton execution. It consumes the package-generation preflight row, constructs exactly one
    synthetic, report-scoped `CollisionPackage.to_dict()` artifact for the deterministic
    `paper_single_box` OBB/box row, records generated CollisionPackage counts as one, keeps
    runtime-admissibility checks, Newton runtime, real-USD, benchmark, collision-quality,
    deployment, and certification triggers at zero or false, keeps the report partial, and points
    next to `paper_mapped_subset_runtime_admissibility_preflight_contract`.
55. `paper_mapped_subset_runtime_admissibility_preflight_contract` is now implemented as a
    single-fixture offline runtime-admissibility preflight contract, not a runtime-admissibility
    check and not Newton execution. It consumes the one synthetic `paper_single_box`
    `CollisionPackage.to_dict()` artifact, validates identity/source/schema/subset fields, records
    exactly one later runtime-admissibility candidate row without copying the full package dict,
    keeps runtime-admissibility checks, Newton runtime, real-USD, benchmark, collision-quality,
    deployment, and certification triggers at zero or false, keeps the report partial, and points
    next to `paper_mapped_subset_runtime_admissibility_contract`.
56. `paper_mapped_subset_runtime_admissibility_contract` is now implemented as a single-fixture
    offline/static runtime-admissibility contract, not Newton shape mapping and not Newton
    execution. It consumes the runtime-admissibility preflight row for the same synthetic
    `paper_single_box` package, records exactly one finite center, right-handed orthonormal-axis,
    positive-half-extent, target box-schema, source-face, containment, and volume check, records
    `runtime_admissibility_check_count: 1` only as report-side static accounting, keeps Newton
    mapping, Newton runtime, real-USD, benchmark, collision-quality, deployment, and certification
    triggers at zero or false, keeps the report partial, and points next to
    `paper_mapped_subset_newton_shape_mapping_preflight_contract`.
57. `paper_mapped_subset_newton_shape_mapping_preflight_contract` is now implemented as a
    single-fixture offline/static shape-mapping handoff preflight, not Newton shape mapping and
    not Newton execution. It consumes the runtime-admissibility row for the same synthetic
    `paper_single_box` box artifact, records exactly one target-kind/field-transfer row for a
    later mapper, keeps mapping attempts, Newton mapping records, Newton runtime, real-USD,
    benchmark, collision-quality, deployment, and certification triggers at zero or false, keeps
    the report partial, and points next to
    `paper_mapped_subset_newton_shape_mapping_contract`.
58. `paper_mapped_subset_newton_shape_mapping_contract` is now implemented as a single-fixture
    offline/static Newton shape descriptor contract, not Newton object construction and not Newton
    execution. It consumes the shape-mapping preflight row for the same synthetic
    `paper_single_box` box artifact, records exactly one report-scoped
    `newton_shape_descriptor_dict` for target kind `box`, keeps mapping attempts, Newton mapping
    records, Newton shape objects, Newton runtime, real-USD, benchmark, collision-quality,
    deployment, and certification triggers at zero or false, keeps the report partial, and points
    next to `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`.
59. `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract` is now implemented as a
    single-fixture offline/static Newton shape runtime-boundary preflight, not Newton object
    construction and not Newton execution. It consumes the descriptor row for the same synthetic
    `paper_single_box` box artifact, records exactly one later runtime-construction candidate,
    keeps mapping attempts, Newton mapping records, Newton shape objects, Newton runtime,
    real-USD, benchmark, collision-quality, deployment, and certification triggers at zero or
    false, keeps the report partial, and points next to
    `paper_mapped_subset_newton_shape_runtime_construction_contract`.
60. `paper_mapped_subset_newton_shape_runtime_construction_contract` is now implemented as a
    single-fixture offline/report-scoped Newton shape mapping-record construction gate, not Newton
    engine shape object construction and not Newton execution. It consumes that runtime-boundary
    preflight row, records exactly one repo-local `NewtonShapeMapping.to_dict()` mapping record for
    the same synthetic `paper_single_box` box descriptor, keeps Newton mapper calls, Newton engine
    shape objects, builder shape calls, Newton runtime, real-USD, benchmark, collision-quality,
    deployment, and certification triggers at zero or false, keeps the report partial, and points
    next to `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`.
61. `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract` is now implemented as a
    single-fixture offline/static Newton shape runtime builder-preflight gate, not a Newton
    builder call and not Newton execution. It consumes that repo-local
    `NewtonShapeMapping.to_dict()` mapping record, records exactly one JSON-safe future box builder
    call plan with signature fields `body`, `xform`, `hx`, `hy`, and `hz`, keeps builder calls,
    Newton engine shape objects, Newton runtime, real-USD, benchmark, collision-quality,
    deployment, and certification triggers at zero or false, keeps the report partial, and points
    next to `paper_mapped_subset_newton_shape_runtime_builder_construction_contract`.
62. `paper_mapped_subset_newton_shape_runtime_builder_construction_contract` is now implemented as
    a single-fixture offline/report-only Newton shape runtime builder-construction gate, not a
    real Newton builder call and not Newton execution. It consumes that builder-preflight row,
    reconstructs the repo-local mapping record, calls only the repo-local static shape dispatch
    helper with a recording builder and fake Warp-like module, records exactly one JSON-safe
    fake-builder `add_shape_box` call artifact, keeps real Newton imports, Newton `ModelBuilder`
    instantiation, Newton engine shape objects, real Newton builder calls, Newton runtime,
    real-USD, benchmark, collision-quality, deployment, and certification triggers at zero or
    false, keeps the report partial, and points next to
    `paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract`.
63. `paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract` is now
    implemented as a single-fixture offline/static Newton engine-builder boundary-preflight gate,
    not a real Newton import, not a `newton.ModelBuilder` instantiation, not a real builder call,
    not model finalization, not a collision pipeline, and not Newton execution. It consumes that
    recording-builder artifact, records one future-boundary checklist row for the later real
    `newton.ModelBuilder` / `add_shape_box` environment boundary, keeps all real Newton, real-USD,
    benchmark, collision-quality, deployment, and certification triggers at zero or false, keeps
    the report partial, and points next to
    `paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract`.
64. `paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract` is now
    implemented as a single-fixture bounded Newton/Warp environment-provenance gate, not a real
    Newton import, not a `newton.ModelBuilder` instantiation, not a real builder call, not model
    finalization, not a collision pipeline, and not Newton execution. It consumes that
    boundary-preflight row, records configured-source-dir status and JSON-safe `find_spec`
    provenance shape, keeps all real Newton, real-USD, benchmark, collision-quality, deployment,
    and certification triggers at zero or false, keeps the report partial, and points next to
    `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract`.
65. `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract` is now
    implemented as a single-fixture bounded source-AST API-surface gate, not a real Newton import,
    not a `newton.ModelBuilder` instantiation, not a real builder call, not model finalization, not
    a collision pipeline, and not Newton execution. It consumes the environment-probe row, records
    default no-config API-surface status for the future `newton.ModelBuilder` / `add_shape_box`
    boundary, keeps all real Newton, real-USD, benchmark, collision-quality, deployment, and
    certification triggers at zero or false, keeps the report partial, and points next to
    `paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract`.
66. Records and configs can preserve exactly what was run.

The capped-cylinder proxy change is small but important in this story, but it is not the runtime
roadmap. It responds to the expected-failure workbench's primitive-vocabulary gap by adding one
opt-in offline proposal proxy and recording that the unsupported paper primitive gap can decrease
from 3 to 2 in a named report. The runtime roadmap now stays Newton-native first: `cylinder`,
`cone`, and `ellipsoid` have dated synthetic diagnostic-path evidence before any paper-only
primitive is considered for Newton tasks.

This means the workbench/reporting infrastructure is in place, and the first native primitive
fitting hook exists for synthetic toy meshes. The paper-lane audit now has an explicit scope
decision, but the paper-faithful decomposition and evaluation story still needs to be implemented.

The 2026-05-16 four-block status audit summarized this position as an internal diagnostic
workbench that was mostly missing integration/report ergonomics rather than Newton plumbing. The
follow-on command-only four-block slice report now gathers primitive-selection, merge/search,
offline report, package/mapping, and recorded Newton task-gate status for the recorded
`cost_guided_lookahead` synthetic slice.

For a step-by-step explanation of how mesh input, primitive fitting, objective terms,
merge/search, `CollisionPackage`, Newton mapping, task smokes, and benchmark claims differ, see
[CPD pipeline step-by-step explainer](cpd-pipeline-step-by-step-explainer.md).

For the current row-by-row paper reproduction gap and the offline-first lane that should close
the next gap, see [CPD paper reproduction gap matrix](cpd-paper-reproduction-gap-matrix.md) and
[CPD paper-faithful offline lane spec](cpd-paper-faithful-offline-lane-spec.md). For the current
synthetic fixture plan, see
[CPD paper fixture-breadth expansion plan](cpd-paper-fixture-breadth-expansion-plan.md).

## Paper Story Layers

The CPD paper story can be read as eight layers.

| Layer | Paper-story question | Repository status |
| --- | --- | --- |
| 1. Asset input | Can a complex mesh enter the pipeline? | Partially in place through USD-open and capped first-mesh extraction smokes. |
| 2. Primitive proposal | Can the mesh become a small set of primitive candidates? | In place only as a restricted geometry-only CPD-like baseline, not the paper algorithm. An opt-in synthetic comparison can now include simple `cylinder`, `cone`, and `ellipsoid` proxy fits. |
| 3. Objective and cost | Can the system expose diagnostic accounting terms for a decomposition? | Narrowly in place as an offline paper-aligned surrogate objective report with structured Eq.4 alignment metadata. It summarizes primitive budget, volume proxy, raw and AABB-normalized merge excess, containment proxy, and unsupported paper primitive gaps, but it is not the paper collapse-cost rule plus primitive weighting. |
| 4. Search or optimization | Can the system find good primitive sets under a budget? | Partially audited in the paper offline lane through toy priority-queue and component-pair traces. This is still not full paper-scope search or benchmark evidence. |
| 5. Expected limitations | Can known CPD-paper gaps stay visible before algorithmic changes? | Narrowly in place as a deterministic expected-failure synthetic workbench over three in-memory fixtures. This is diagnostic limitation accounting, not validation or benchmark evidence. |
| 6. Primitive vocabulary | Can paper primitive categories enter a restricted proposal lane? | Narrowly in place in two different lanes: the older CPD-like objective report has an opt-in offline `capped_cylinder` proxy, and the partial paper offline report now has offline paper-shaped OBB/sphere rows, a paper-shaped capsule axis row, and offline-only flat capped-cylinder/frustum/trapezoidal-prism audit rows. This is still not full paper-faithful primitive fitting. |
| 7. Collision integration | Can generated primitives be consumed by a physics or collision path? | Narrowly in place through Newton contact, drop/settle, and sphere-rain smokes on recorded mapped primitives. The synthetic native bundle also covers `cylinder`, `cone`, and `ellipsoid`; `capped_cylinder` is not Newton-mapped in this slice. |
| 8. Evaluation | Do the results improve collision detection under benchmark settings? | Not started. No benchmark superiority or collision-quality claim is supported. |

## What The Current Baseline Is

The current baseline is a CPD-like geometry smoke path. It groups mesh faces, fits restricted
primitive proposals, and records the result. It exists because later paper-faithful work will need
the same asset intake, report schema, collision-package bridge, and Newton diagnostic plumbing.

The current baseline is useful for pipeline diagnostic plumbing. It is not a substitute for the
paper's primitive coverage, collapse-cost rule, primitive weighting, optimization procedure, or
benchmark evaluation.

## What The Component-Merge Gate Adds

The component-merge gate is a small algorithmic extension to the baseline. It keeps the default
topology-only merge behavior, and when explicitly enabled it can consider disconnected-component
pairwise merge candidates after topology adjacency merges are exhausted.

Its value is auditability:

- it records the merge policy;
- it records initial and final component counts;
- it separates topology merges from virtual component merges;
- it records blocked merge counts;
- it normalizes excess-volume accounting by the mesh AABB volume.

This is still below paper reproduction. It is a controlled way to start collecting the information
needed by a future paper-aligned objective.

## What The Offline Objective Report Adds

The offline objective report is the first explicit Layer 3 artifact. It does not change the
baseline algorithm. It reads a CPD-like decomposition report and emits reviewable terms:

- primitive budget pressure;
- AABB-normalized primitive volume proxy;
- accepted and blocked raw Eq.4-like merge delta plus AABB-normalized merge excess accounting;
- structured Eq.4 alignment metadata for audit;
- assigned-point containment proxy;
- unsupported paper primitive gaps;
- component merge and fallback labels.

This is a paper-aligned surrogate report, not a paper-faithful objective implementation. It gives
future merge-search and primitive-fitting work stable comparison fields before those algorithms
change.

For a plain-language explanation of this boundary, see
[CPD objective report alignment](cpd-objective-report-alignment.md).

For a plain-language explanation of the latest Newton-native runtime bundle, see
[Newton-native primitive bundle explainer](newton-native-primitive-bundle-explainer.md).

For a plain-language explanation of the latest opt-in native fitting comparison, see
[Newton-native fitting comparison](newton-native-fitting-comparison.md).

## Is The Objective Report Paper-Consistent?

The short answer is: consistent in design intent, not yet consistent as a paper-faithful
mathematical implementation.

The report asks paper-shaped engineering questions: how many primitives were used, how much proxy
volume was introduced, what the accepted or blocked merges cost, whether assigned points are
contained under a narrow proxy, which paper primitive types are missing, and which failure labels
should block stronger interpretation.

It does not yet implement the paper's full objective formula, search procedure, primitive
vocabulary, containment model, collision-quality evaluation, or benchmark protocol. Treat it as a
reviewable health check that prepares the repository for paper-aligned algorithm work.

The structured Eq.4 metadata makes that boundary machine-readable. It points reviewers to the
paper's Eq.4 collapse-cost role and to the current JSON fields that carry the analogous surrogate
terms, while also recording `computes_paper_eq4: false` and the remaining non-faithful gaps.

## What The Synthetic Comparison Adds

The synthetic objective comparison is the first inspectable toy-mesh layer around the objective
report. It runs the same report on three deterministic in-memory fixtures:

- adjacent square;
- disconnected pair;
- blocked disconnected pair.

For each fixture it records topology-only and `virtual_pairwise` component-merge accounting. The
disconnected fixture no longer reports the topology-only unmerged-component label under
`virtual_pairwise`; the blocked fixture records the `component_merge_blocked` label. These are
fixture-level diagnostic differences, not proof that one policy is better collision geometry.

## What The Cost-Guided Merge Smoke Adds

The cost-guided merge smoke is the first restricted Layer 4 step. It uses one existing surrogate
objective-report term, AABB-normalized merge-excess, to choose among merge candidates on a
deterministic synthetic fixture.

That term is an "extra wrapper volume" penalty. For a candidate merge, the baseline fits one
primitive to the merged face group, subtracts the weighted volumes of the two separate primitives,
and divides the result by the source mesh's AABB volume. Lower is better under this proxy.

The simple mental model is:

- the old/default policy says: first try merging neighboring face groups; only after those are
  exhausted, consider disconnected component pairs;
- the new/opt-in policy says: at the same loop step, compare the best neighboring merge and the
  best allowed disconnected-component merge by the recorded merge-excess cost;
- if the disconnected-component merge has much lower surrogate cost, the opt-in policy can choose
  it first.

The dedicated `cost_guided_pair_choice` fixture compares:

- old/default `topology_then_virtual`: adjacent topology merges are considered before virtual
  component merges;
- new/opt-in `cost_guided_pairwise`: the best adjacent topology candidate and the best virtual
  component candidate are compared by normalized merge-excess at the same loop step.

This is still below paper-scope search or optimization. It shows that one surrogate cost can affect
a merge decision on an inspectable toy mesh. It does not prove better collision geometry,
benchmark quality, or paper-faithful CPD behavior.

On the current toy fixture, the default policy records accepted normalized merge-excess
`0.010062106570764756`, about one percent of the mesh AABB volume. The opt-in cost-guided policy
records `0.000055121`, about five thousandths of one percent. The smoke uses that difference only
as diagnostic accounting for the toy decision.

The 2026-05-16 controlled merge-search package probe carries the same toy decision one step
farther: the default package groups source faces as `[[0, 1], [2]]`, while the opt-in cost-guided
package groups them as `[[0, 2], [1]]`. Both packages map to Newton shapes. This is package-path
and mapping accounting only; it is not a Newton contact/task diagnostic, real-USD result, or
collision-quality result.

The 2026-05-16 controlled merge-search Newton probe is the next task-smoke layer for that same
package pair. It runs `newton_contact_smoke` first, then runs `newton_drop_settle` and
`newton_sphere_rain` only when contact passes. This shows that the changed synthetic package pair
can enter named Newton diagnostics under recorded settings. It does not show that the opt-in
merge/search policy is better, that a real USD package improved, or that collision quality was
validated.

The 2026-05-16 cost-guided lookahead merge report is a non-paper surrogate extension slice. It
adds `two_step_lookahead` for tiny synthetic fixtures and compares it against greedy
`cost_guided_pairwise` on `lookahead_merge_trap`. The paper method itself is greedy
priority-queue collapse, not lookahead. The lookahead lane changes the toy grouping from
`[[0, 2, 3], [1]]` to `[[0, 1], [2, 3]]` and records lower projected two-step normalized
merge-excess. This is still only offline merge/search accounting. It does not create a package,
run Newton tasks, prove merge-policy superiority, reproduce the paper optimizer, or touch real USD
assets.

Why this still matters for the workbench: CPD is ultimately about selecting a compact primitive
set under geometric and collision-detection constraints. A face-merge baseline that only follows
local adjacency is too weak to explore that engineering space. The lookahead smoke does not solve
the paper problem, but it stress-tests whether a surrogate cost term can change a toy
decomposition decision without confusing that result with paper-faithful search.

The 2026-05-16 cost-guided lookahead package probe is the follow-on package-path gate for that
same toy decision. It converts the greedy and lookahead decompositions into synthetic
`CollisionPackage` lanes and records that both lanes map to Newton shapes. This matters because a
Newton workbench needs an auditable path from a merge/search decision to an engine-facing package
before it can run a task smoke. It still does not run Newton contact, drop/settle, or sphere-rain
diagnostics, and it does not upgrade the lookahead result into a quality or superiority claim.

What it does not yet cover:

- global search over many primitive sets;
- the paper collapse-cost rule plus primitive weighting;
- richer primitive fitting beyond the current restricted proposals;
- collision-quality measurement;
- benchmark comparison.

So the right interpretation is: this is the first cost-aware decision hook in the workbench, not
the CPD optimizer.

The next paper-aligned step is therefore not another Newton task or real-USD rerun. It is an
offline paper lane that can compute and audit paper-side operator, primitive-fit, and collapse-cost
fields on tiny synthetic fixtures first.

## What The Expected-Failure Workbench Adds

The expected-failure workbench is a small but important audit layer. It turns known CPD-paper gaps
into deterministic expected limitation fixtures and diagnostic flags.

The current fixture set asks three questions:

- Does the current restricted `box` subset still report the missing paper primitive vocabulary and
  paper-scope primitive-fitting gap?
- Does a virtual component merge over disconnected triangles still expose that one proxy can wrap
  empty space?
- Does a zero virtual-merge threshold still expose blocked component merge, unmerged components,
  and primitive-budget pressure?

For each fixture, the report records expected, observed, missing, and unexpected flags. A
`smoke_passed` workbench result means those expected flags matched. It does not mean the
decomposition succeeded, and it does not validate collision quality.

This layer matters because the next algorithmic slices should not be chosen blindly. The workbench
points to two concrete next capabilities:

- `primitive_fit_extension` for restricted vocabulary and empty wrapper proxy cases;
- `merge_search_extension` for threshold-blocked component merge behavior.

The workbench is still below paper-scope reproduction. It is not a benchmark, not a failure
detector for arbitrary meshes, and not proof that the baseline catches bad decompositions.

## What The Capped-Cylinder Proxy Adds

The capped-cylinder proxy is the first direct response to the primitive-vocabulary gap. It adds an
opt-in offline `capped_cylinder` geometry proposal proxy and a named objective-report smoke. In
that report, the unsupported paper primitive count decreases from 3 to 2:
`frustum` and `trapezoidal_prism` remain unsupported.

This is useful because it moves one paper primitive category from "outside the proposal vocabulary"
to "available in a restricted report lane." It is still not paper-faithful primitive fitting. The
proxy is marked as `axis_span_radial_proxy` with `hemisphere_caps`, and it does not imply
surface-distance quality, collision quality, or benchmark performance.

Newton integration is intentionally unchanged. `capped_cylinder` remains a Newton mapping gap until
a separate Newton mapping and task-level diagnostic record exists.

## What The Paper Offline Primitive Audit Adds

The newer `cpd_paper_offline_report` is a different lane from the older CPD-like
`capped_cylinder` proxy report. It is command-only and synthetic-fixture-only. Its current role is
to audit paper-side mechanics before any package generation or Newton runtime work.

That partial report now records:

- paper-side operator fields on named toy fixtures;
- offline paper-shaped OBB and sphere rows with projected vertex bounds, OBB world center, `1e-3`
  clamp, sphere radius from the OBB center, and `paper_tiny_sphere_clamp` coverage for the radius
  clamp path;
- a paper-shaped capsule row with one candidate per operator axis;
- offline-only flat capped-cylinder, frustum, and trapezoidal-prism rows;
- paper base collapse cost and separate weighted-priority cost fields for the first merge-cost
  fixture;
- a topology-only priority-queue trace over `paper_three_face_chain`, including deterministic
  queue keys, accepted merges, eager stale-prune events, updated neighbor insertion counts, and
  target-count stop reason;
- a threshold-disabled component-pair insertion trace over `paper_disconnected_components`,
  including topology-queue exhaustion, one `component_pair` candidate, accepted merge record, and
  target-count stop reason;
- a finite-threshold component-pair blocked trace over `paper_component_pair_threshold_blocked`,
  including attempted count `1`, skipped count `0`, blocked reason, and threshold stop reason.
- an explicit enclosed-primitive postprocess cull audit over `paper_nested_primitive`, including
  two identity-axis OBB audit rows, before/after primitive counts, enclosed/enclosing ids, one cull
  reason, and false package/Newton/real-USD/benchmark triggers.
- a fan-triangulated quad/polygon source-face intake policy audit over `paper_quad_face_intake` and
  `paper_polygon_face_intake`, including source vertex ids, generated triangle vertex triples,
  source-face remap, and source-face aggregate operator matrices.
- an exact-coordinate duplicate-vertex preprocessing audit over
  `paper_duplicate_vertex_preprocessing`, including first-occurrence vertex remap, duplicate
  clusters, source-face remap, before/after component counts, retained/dropped source-face ids,
  and a topology trace over the deduplicated executable mesh.
- a top-level `paper_faithful_offline_scope_audit` criteria table with
  `decision: remain_partial`, nine blocking fixture-scope criteria, non-blocking
  package/Newton/real-USD/benchmark boundary rows, and next gate
  `paper_fixture_breadth_expansion_plan`.
- a documentation-only fixture-breadth expansion plan that maps those nine blocking rows to
  planned synthetic fixture batches.
- Batch A source/preprocess/intake/operator fixture-breadth cases:
  `paper_mixed_face_preprocess_operator`, `paper_degenerate_preprocess_face_drop`, and
  `paper_concave_polygon_rejected`.
- Batch B primitive-fit fixture-breadth cases:
  `paper_rotated_box_fit`, `paper_offset_sphere_fit`, `paper_off_axis_capsule_fit`,
  `paper_flat_capped_cylinder_axis_fit`, `paper_tapered_frustum_fit`, and
  `paper_asymmetric_trapezoid_fit`.
- Batch C cost/search/stop fixture-breadth cases:
  `paper_branching_cost_order`, `paper_equal_cost_queue_tie`, and
  `paper_nonzero_threshold_block`.
- Batch D component-pair fixture-breadth cases:
  `paper_component_pair_multi_candidate_order` and `paper_component_pair_cap_skipped`.
- Batch E postprocess fixture-breadth cases:
  `paper_rotated_nested_primitive` and `paper_cross_type_enclosure_boundary`.

This closes the narrow capsule axis-policy audit gap and adds the first topology-only
priority-queue trace plus component-pair accepted/blocked toy events, postprocess culling,
source-face intake policy fixtures, OBB/sphere fit-faithfulness rows, and exact-overlap
duplicate-vertex preprocessing inside the report. The scope audit then records why these remain
fixture-scoped and why the lane is still not `paper_faithful_offline`. The fixture-breadth plan
has now completed Batch A, Batch B, Batch C, Batch D, Batch E, and the command-only synthetic
fixture-breadth completion review. The planning-only `paper_faithful_offline_generalization_plan`
is now also recorded as a command-only table. The source-policy generalization gate is now
implemented as an offline report-only matrix. The primitive-fit engine generalization gate is now
implemented as an offline report-only matrix over deterministic in-memory probes. The search-engine
generalization gate is now implemented as an offline report-only matrix over deterministic trace
summaries. The postprocess-policy generalization gate is now implemented as an offline report-only
matrix over deterministic postprocess audit fixtures. The package-boundary readiness gate is now
implemented as an offline matrix before package conversion. The changed-decomposition output
contract is now implemented as an offline changed-decomposition output contract, not a
`CollisionPackage`. The package-adapter contract now also exists as a command-only offline
adapter decision table, not a `CollisionPackage`. The unsupported-primitive policy now also exists
as a command-only offline policy table, not a `CollisionPackage`. The mapped-subset
package-conversion plan and candidate matrix now also exist as command-only offline tables, not a
`CollisionPackage`. The mapped-subset adapter-preflight contract now also exists as a
command-only offline contract, not `PrimitiveSpec` generation and not a `CollisionPackage`. The
mapped-subset PrimitiveSpec dry-run contract now also exists as a command-only offline contract,
not real `PrimitiveSpec` generation and not a `CollisionPackage`. The mapped-subset
PrimitiveSpec validation contract now also exists as a command-only offline validation contract,
not real `PrimitiveSpec` generation and not a `CollisionPackage`. The mapped-subset
PrimitiveSpec generation-preflight contract now also exists as a command-only offline preflight
contract, still not real `PrimitiveSpec` generation and not a `CollisionPackage`. The mapped-subset
PrimitiveSpec generation contract now also exists as a command-only offline template contract,
still not runtime `PrimitiveSpec` generation and not a `CollisionPackage`. The mapped-subset
PrimitiveSpec candidate-source contract now also exists as a command-only offline source audit,
still not runtime `PrimitiveSpec` generation and not a `CollisionPackage`. The mapped-subset
native-current fixture contract now also exists as a command-only offline source-row contract,
still not runtime `PrimitiveSpec` generation and not a `CollisionPackage`. The native-fixture
PrimitiveSpec-like dict generation contract now also exists as a command-only offline report
artifact, still not runtime `PrimitiveSpec` object creation and not a `CollisionPackage`. The
native-fixture serialization contract now also exists as a command-only offline JSON
serialization/schema-stability contract for that one report-only dict. The runtime-boundary
preflight contract now also exists as a command-only offline boundary contract for that same row;
the runtime-construction contract now also exists as a single-fixture offline contract that
constructs exactly one runtime `PrimitiveSpec` object and stores only `PrimitiveSpec.to_dict()` in
the report. The package-generation preflight contract now also exists as a single-fixture offline
contract that records one later package-generation candidate while creating zero
CollisionPackages. The package-generation contract now also exists as a single-fixture offline
contract that constructs one synthetic, report-scoped `CollisionPackage.to_dict()` artifact. The
runtime-admissibility preflight contract now also exists as a single-fixture offline contract that
records one later runtime-admissibility candidate row while running zero runtime-admissibility
checks and zero Newton code. The runtime-admissibility contract now also exists as a
single-fixture offline/static contract that records one finite-geometry and box-schema check while
running zero Newton mapping and zero Newton code. The shape-mapping preflight now also exists as a
single-fixture offline/static contract that records one mapper-handoff row for the same synthetic
box dict while running zero mapping attempts and zero Newton code. The shape-mapping contract now
also exists as a single-fixture offline/static contract that records one report-scoped descriptor
dict for the same synthetic box dict while creating zero Newton shape objects and running zero
Newton code. The later runtime-boundary, runtime-construction, builder-preflight,
builder-construction, engine-builder boundary-preflight, environment-probe, and API-surface
contracts now also exist as bounded offline/report-only gates. The next code slice is
`paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract`.

## What The Newton-Native Policy Changes

The capped-cylinder proxy exposed a useful distinction:

```text
paper primitive vocabulary != Newton runtime roadmap
```

For runtime work, the project should prefer primitives that Newton can build and diagnose directly.
The native runtime bundle now adds `cylinder`, `cone`, and `ellipsoid` together on top of the
already mapped `box`, `sphere`, and `capsule`.

This bundle was implemented together because the work touches the same surfaces: shape validation,
Newton builder calls, package bounds, support-height estimates, contact canaries, drop/settle,
sphere-rain, tests, and records. The dated native-bundle record documents diagnostic-path evidence
for each primitive kind through mapping and diagnostic construction, plus a synthetic clean-env
runtime smoke.

`frustum` and `trapezoidal_prism` should remain in the offline paper-alignment lane for now. They
can still appear in `paper_primitive_gap` accounting, but they should not enter Newton task claims
without a separate mapping and diagnostic record.

## What The Newton-Native Fitting Comparison Adds

The native fitting comparison is the first narrow Layer 2 step after the runtime bundle. It lets
the CPD-like fitter opt into the six-kind Newton-native subset:

```text
box, sphere, capsule, cylinder, cone, ellipsoid
```

and compares it against the older subset:

```text
box, sphere, capsule
```

on deterministic toy meshes:

- `cylindrical_rod`, where the native subset selects `cylinder`;
- `tapered_cone`, where the native subset selects `cone`;
- `ellipsoid_blob`, where the native subset selects `ellipsoid`;
- `squat_cylinder`, where the updated cylinder fitter selects `cylinder` after searching axes.

The report also checks that the resulting one-primitive synthetic packages map through Newton
shape mapping. It now includes candidate weighted-volume audit tables so reviewers can see why the
native primitive ranked first on each toy fixture. This is still a synthetic fitting and
diagnostic-accounting smoke, not Newton task evidence and not collision-quality evidence.

The follow-up bed/Franka probe config now runs the real-USD scope. It records old/new objective
reports on capped bed and capped Franka meshes, inspects mapping gaps and failure labels, then runs
Newton contact canaries and gated task smokes.

## What The Bed/Franka Native Probe Comparison Adds

The bed/Franka native probe comparison completes that next concrete step for two capped real-USD
smoke roles:

```text
bed_dev_smoke
franka_import_smoke
```

For each role, it runs the legacy `box`/`sphere`/`capsule` lane and the six-kind Newton-native
lane under the same face cap and merge policy. After the controlled cylinder-axis fitting update,
bed still selected only `box` primitives in both lanes, while capped Franka's native lane selected
`29` boxes plus `3` cylinders. The subsequent support-aware admissibility slice reclassified those
three Franka cylinder wins as cheaper raw-cost extension candidates with insufficient face/point
support, so the current capped Franka support-aware native lane selects `32` boxes. That means the
pipeline can expose and then constrain a native-lane selection change, but it does not show that
either selection is better collision geometry.

The probe comparison then requires full Newton mapping before contact canary, and gates
drop/settle plus sphere-rain behind contact success. Under the clean Newton conda environment, the
bed and Franka old/new packages passed the recorded contact and task smokes.

This is a real-USD diagnostic smoke milestone, not a benchmark or collision-quality milestone.

## What The Support-Aware Native-Extension Rule Adds

The support-aware rule is a narrow Layer 2 guardrail. It changes primitive selection only when a
Newton-native extension candidate (`cylinder`, `cone`, or `ellipsoid`) has too little local
support and a fallback primitive is available. The current thresholds are three source faces and
five unique assigned points.

The report keeps the distinction between raw cost rank and support-aware selection rank. This
matters because a cylinder can be cheapest under the raw weighted-volume surrogate while still
being blocked from replacing a box because it was fit from only a tiny patch.

This rule is not the CPD paper algorithm. It does not implement the paper's full objective,
priority-queue collapse procedure, primitive vocabulary, or benchmark evaluation. It is a local
diagnostic selection guard that makes the next fitting or clustering experiment easier to inspect.

For a more detailed plain-language explanation of why this slice matters but does not prove native
primitive value, see
[Real USD native probe in the CPD paper story](real-usd-native-probe-paper-story-explainer.md).

For a step-by-step explanation of the latest candidate-loss diagnosis, controlled cylinder-axis
update, synthetic rerun, and bed/Franka Newton-gated rerun as one repeatable loop, see
[CPD latest diagnostic loop explainer](cpd-latest-diagnostic-loop-explainer.md).

For the next algorithmic sequence after local USD mirrors, see
[CPD next steps after real USD mirrors](cpd-next-steps-after-real-usd-mirrors.md).

## What Newton Probes Mean Here

Newton probes are downstream diagnostic checks. They answer a narrow question:

Can this primitive package be mapped into Newton shapes and participate in a named smoke task under
recorded settings?

They do not answer the stronger question:

Is this decomposition a good collision representation?

For that stronger claim, the repository still needs paper-aligned objective metrics, broader asset
coverage, task-level comparison reports, and dated benchmark records.

## Current Story Position

The current position is:

```text
USD assets
-> ignored repo-local mirrors for current bed/Franka smoke roles
-> CPD-like primitive proposals
-> paper-aligned surrogate objective report
-> synthetic objective comparison
-> focused cost-guided merge-search smoke using one objective term
-> synthetic offline merge-step trace diagnostic accounting for the cost-guided fixture
-> expected-failure workbench for known CPD-paper gaps
-> opt-in capped-cylinder proxy objective report (offline only; not Newton-mapped)
-> historical mapped collision package using Newton-supported primitives
-> Newton smoke diagnostics for recorded mapped primitives
-> synthetic Newton-native primitive bundle smoke
-> synthetic native selection audit for toy primitive choices
-> real-USD old/new native probe comparison for capped bed and capped Franka
-> candidate-loss diagnosis and controlled cylinder-axis fitting smoke
-> support-aware low-support native-extension admissibility guard
-> synthetic cylinder near-miss fixture
-> synthetic cylinder near-miss fit-ablation report
-> synthetic cylinder near-miss scoring-sensitivity report
-> synthetic cylinder near-miss report-only scoring-policy ablation
-> synthetic cylinder scoring-policy guardrail on a clearly boxy cuboid
-> synthetic offline opt-in scoring-policy selection probe
-> explicitly opt-in synthetic package probe plus Newton shape-mapping summary only
-> explicitly opt-in synthetic Newton contact/drop/sphere-rain task smokes
-> synthetic controlled merge-search package-path probe plus Newton shape-mapping summary only
-> synthetic controlled merge-search Newton contact/drop/sphere-rain task smokes
-> synthetic two-step lookahead merge/search diagnostic accounting
-> synthetic lookahead package-path probe plus Newton shape-mapping summary only
-> synthetic lookahead Newton contact/drop/sphere-rain task smokes
-> command-only four-block slice report linking the recorded lookahead evidence
-> partial cpd_paper_offline_report over toy fixtures
-> paper-shaped capsule axis audit row, offline-only paper primitive rows, and collapse-cost fields
-> topology-only paper priority-queue trace audit
-> threshold-disabled component-pair edge insertion audit
-> finite-threshold component-pair blocked audit
-> enclosed-primitive postprocess cull audit
-> polygon/quad source-face intake policy audit
-> dated records
```

The current paper-story position is now:

```text
local USD mirrors or synthetic fixtures
-> use current candidate-loss labels
-> direct cylinder near-miss fixture
-> diagnostic fit-ablation report for containment-preserving cylinder fits
-> diagnostic scoring-sensitivity report for the current surrogate
-> report-only scoring-policy ablation for one synthetic near miss
-> use the boxy guardrail to decide whether one later scoring, primitive-fitting, or merge-search
   change is justified
-> run a synthetic offline opt-in selection probe before any package or Newton task rerun
-> run an explicitly opt-in synthetic package probe before any Newton contact or task rerun
-> run an explicitly opt-in synthetic Newton diagnostic before any real-USD rerun
-> use that synthetic evidence to justify one separate controlled merge/search behavior change
-> synthetic package-path and mapping rerun for the behavior change
-> synthetic Newton task probe for the behavior change, if the changed package maps fully and has
   not already been task-smoked
-> synthetic Newton task probe for the two-step lookahead package pair
-> four-block status audit that identifies the missing workbench integration/report slice
-> command-only four-block slice report for the recorded cost-guided lookahead synthetic slice
-> command-only partial paper offline report for toy paper mechanics
-> topology-only paper priority-queue trace audit, still without package/Newton/real-USD
-> threshold-disabled component-pair edge insertion audit, still without package/Newton/real-USD
-> finite-threshold component-pair blocked audit, still without package/Newton/real-USD
-> enclosed-primitive postprocess cull audit, still without package/Newton/real-USD
-> polygon/quad source-face intake policy audit, still without package/Newton/real-USD
-> OBB/sphere fit-faithfulness audit, still without package/Newton/real-USD
-> exact-coordinate duplicate-vertex preprocessing audit, still without package/Newton/real-USD
-> scope-audit criteria table, still without package/Newton/real-USD
-> fixture-breadth expansion plan, documentation-only
-> fixture-breadth Batch A source/preprocess/intake/operator audit, still without package/Newton/real-USD
-> fixture-breadth Batch B primitive-fit audit, still without package/Newton/real-USD
-> fixture-breadth Batch C cost/search/stop audit, still without package/Newton/real-USD
-> fixture-breadth Batch D component-pair audit, still without package/Newton/real-USD
-> fixture-breadth Batch E postprocess audit, still without package/Newton/real-USD
-> fixture-breadth completion review, still partial and still without package/Newton/real-USD
-> generalization planning table, still partial and still without package/Newton/real-USD
-> source-policy generalization matrix, still partial and still without package/Newton/real-USD
-> primitive-fit engine generalization matrix, still partial and still without package/Newton/real-USD
-> search-engine generalization matrix, still partial and still without package/Newton/real-USD
-> postprocess-policy generalization matrix, still partial and still without package/Newton/real-USD
-> package-boundary readiness matrix, still partial and still without package/Newton/real-USD
-> changed-decomposition output contract, still partial and still without package/Newton/real-USD
-> package-adapter contract, still partial and still without package/Newton/real-USD
-> unsupported-primitive policy, still partial and still without package/Newton/real-USD
-> mapped-subset package-conversion plan, still partial and still without package/Newton/real-USD
-> mapped-subset conversion candidate matrix, still partial and still without package/Newton/real-USD
-> mapped-subset adapter preflight contract, still partial and still without PrimitiveSpec/package/Newton/real-USD
-> mapped-subset PrimitiveSpec dry-run contract, still partial and still without real PrimitiveSpec/package/Newton/real-USD
-> mapped-subset PrimitiveSpec validation contract, still partial and still without real PrimitiveSpec/package/Newton/real-USD
-> mapped-subset PrimitiveSpec generation preflight contract, still partial and still without real PrimitiveSpec/package/Newton/real-USD
-> mapped-subset PrimitiveSpec generation contract, still partial and still without runtime PrimitiveSpec/package/Newton/real-USD
-> mapped-subset PrimitiveSpec candidate-source contract, still partial and still without runtime PrimitiveSpec/package/Newton/real-USD
-> mapped-subset native-current fixture contract, still partial and still without runtime PrimitiveSpec/package/Newton/real-USD
-> mapped-subset native-fixture PrimitiveSpec-like dict generation contract, still partial and still without runtime PrimitiveSpec/package/Newton/real-USD
-> mapped-subset native-fixture serialization contract, still partial and still without runtime PrimitiveSpec/package/Newton/real-USD
-> mapped-subset PrimitiveSpec runtime-boundary preflight contract, still partial and still without runtime PrimitiveSpec/package/Newton/real-USD
-> mapped-subset PrimitiveSpec runtime-construction contract, still partial and still without CollisionPackage/Newton/real-USD
-> mapped-subset CollisionPackage generation preflight contract, still partial and still without CollisionPackage/Newton/real-USD
-> mapped-subset CollisionPackage generation contract, still partial and still without runtime admissibility/Newton/real-USD
-> mapped-subset runtime-admissibility preflight contract, still partial and still without runtime admissibility/Newton/real-USD
-> mapped-subset runtime-admissibility contract, still partial and still without Newton shape mapping/Newton/real-USD
-> mapped-subset Newton shape-mapping preflight contract, still partial and still without Newton shape mapping/Newton/real-USD
-> mapped-subset Newton shape-mapping contract, still partial and still without Newton shape object construction/Newton execution/real-USD
-> mapped-subset Newton shape runtime-boundary preflight contract, still partial and still without Newton shape object construction/Newton execution/real-USD
-> mapped-subset Newton shape runtime-construction contract, still partial and still without Newton engine shape object construction/builder shape call/Newton execution/real-USD
-> mapped-subset Newton shape runtime builder-preflight contract, still partial and still without builder shape call/Newton engine shape object construction/Newton execution/real-USD
-> mapped-subset Newton shape runtime builder-construction contract, still partial and still without real Newton builder shape call/Newton engine shape object construction/Newton execution/real-USD
-> mapped-subset Newton engine-builder boundary-preflight contract, still partial and still without real Newton import/ModelBuilder/builder shape call/finalize/collision pipeline/Newton execution/real-USD
-> mapped-subset Newton engine-builder environment-probe contract, still partial and still without real Newton import/ModelBuilder/builder shape call/finalize/collision pipeline/Newton execution/real-USD
-> mapped-subset Newton engine-builder API-surface contract, still partial and still without real Newton import/ModelBuilder/builder shape call/finalize/collision pipeline/Newton execution/real-USD
-> next: paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract
-> bed/Franka rerun under full mapping, contact, task, and dated-record gates only after a real
   package change is explicit
```

## Safe Current Wording

Use:

- "CPD reproduction workbench";
- "geometry-only CPD-like primitive proposal baseline";
- "paper-story infrastructure for CPD reproduction";
- "component-merge gate for audit-friendly merge-cost reporting";
- "paper-aligned surrogate objective report";
- "synthetic objective comparison";
- "focused CPD-like cost-guided merge-search smoke";
- "synthetic offline merge-step trace diagnostic accounting";
- "deterministic expected-failure synthetic workbench";
- "expected limitation fixtures";
- "opt-in offline capped-cylinder geometry proposal proxy";
- "primitive-vocabulary accounting for a restricted proposal baseline";
- "Newton-native primitive roadmap";
- "native analytic primitive bundle";
- "synthetic Newton-native primitive diagnostic smoke";
- "controlled cylinder-axis fitting smoke";
- "real-USD candidate-loss diagnosis";
- "synthetic report-only scoring-policy ablation";
- "counterfactual scoring-policy ablation over one synthetic fixture";
- "synthetic report-only scoring-policy guardrail";
- "counterfactual selectivity check over deterministic synthetic fixtures";
- "synthetic offline opt-in scoring-policy selection probe";
- "explicitly opt-in synthetic package probe";
- "Newton shape-mapping summary";
- "explicitly opt-in synthetic Newton diagnostic";
- "named synthetic contact/drop/sphere-rain task smokes";
- "synthetic controlled merge-search Newton task-smoke probe";
- "synthetic two-step merge-search lookahead smoke";
- "bounded diagnostic merge/search heuristic";
- "real-USD native probe diagnostic smoke";
- "capped bed and capped Franka first-mesh scope";
- "paper-alignment offline lane";
- "partial `cpd_paper_offline_report`";
- "paper-shaped capsule axis audit row";
- "offline paper priority-queue trace audit";
- "threshold-disabled component-pair edge insertion audit";
- "finite-threshold component-pair blocked audit";
- "offline enclosed-primitive postprocess cull audit";
- "offline polygon/quad source-face intake policy audit";
- "offline OBB/sphere fit-faithfulness audit";
- "offline paper scope-audit criteria table";
- "fixture-breadth expansion plan";
- "planned synthetic fixture-breadth batches";
- "fixture-breadth Batch C cost/search/stop audit";
- "fixture-breadth Batch D component-pair audit";
- "fixture-breadth Batch E postprocess audit";
- "offline source-policy generalization matrix";
- "offline primitive-fit engine generalization matrix";
- "offline search-engine generalization matrix";
- "offline postprocess-policy generalization matrix";
- "offline package-boundary readiness matrix";
- "offline changed-decomposition output contract";
- "offline package-adapter contract";
- "offline unsupported-primitive adapter policy";
- "offline PrimitiveSpec candidate-source audit with zero eligible current candidates";
- "offline PrimitiveSpec runtime-boundary preflight contract";
- "single-fixture offline PrimitiveSpec runtime-construction contract";
- "single-fixture offline CollisionPackage generation preflight contract";
- "single-fixture offline CollisionPackage generation contract";
- "Newton diagnostic smoke over a CPD-like collision package";
- "below full CPD paper reproduction."

Avoid:

- "CPD reproduced";
- "paper-faithful CPD implementation";
- "CPD optimizer implemented";
- "collision-quality validation";
- "benchmark result";
- "validated expected-failure detector";
- "paper-faithful capped cylinder support";
- "Newton supports capped cylinders";
- "broad Newton-native primitive quality";
- "CPD-like generator emits new native primitive kinds by default";
- "Newton task checked" for package-probe-only reports;
- "simulation-checked" for shape-mapping-only reports;
- "synthetic task smoke proves collision quality";
- "paper primitive vocabulary is runtime-supported";
- "safe collider";
- "validated robot collider."

## Recommended Next Slices

Fixture-breadth Batch A, Batch B, Batch C, Batch D, Batch E, the command-only synthetic
fixture-breadth completion review, the command-only generalization planning table, and the
source-policy, primitive-fit engine, search-engine, postprocess-policy, and package-boundary
readiness generalization matrices now exist. The offline changed-decomposition output contract,
offline package-adapter contract, offline unsupported-primitive policy, offline mapped-subset
conversion plan, offline candidate matrix, offline adapter-preflight contract, offline
PrimitiveSpec dry-run contract, offline PrimitiveSpec validation contract, offline PrimitiveSpec
generation-preflight contract, offline PrimitiveSpec generation contract, offline PrimitiveSpec
candidate-source contract, offline native-current fixture contract, offline native-fixture
PrimitiveSpec-like dict generation contract, native-fixture serialization contract,
runtime-boundary preflight contract, and single-fixture runtime-construction contract now exist.
The single-fixture package-generation preflight contract and single-fixture CollisionPackage
generation contract now also exist. The single-fixture runtime-admissibility preflight contract
and the single-fixture offline/static runtime-admissibility contract now also exist. The
single-fixture offline/static Newton shape-mapping preflight contract and the single-fixture
offline/static Newton shape-mapping descriptor contract now also exist. The single-fixture
offline/static Newton shape runtime-boundary preflight contract and the single-fixture
offline/report-scoped Newton shape runtime-construction contract now also exist. The
single-fixture offline/static Newton shape runtime builder-preflight contract now also exists. The
single-fixture offline/report-only Newton shape runtime builder-construction contract and the
single-fixture offline/static Newton engine-builder boundary-preflight contract now also exist.
The single-fixture bounded Newton/Warp environment-probe contract now also exists. The
single-fixture bounded source-AST API-surface contract now also exists. The immediate next code
slice should keep the same boundary and implement the bounded
`paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract`
without running Newton task diagnostics:

1. Implement `paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract`
   after the API-surface contract has recorded default no-config source-AST status for the future
   `newton.ModelBuilder` / `add_shape_box` boundary. This single gate replaces the previously
   planned import-boundary-preflight/import-contract split.
2. Keep the constructed runtime `PrimitiveSpec` object, preflight candidate, synthetic
   `CollisionPackage.to_dict()` artifact, runtime-admissibility preflight row, static
   runtime-admissibility row, shape-mapping preflight row, descriptor row, runtime-boundary
   preflight row, repo-local mapping record, builder-call-plan record, and recording-builder call
   artifact, engine-builder boundary-preflight row, environment-probe row, and API-surface row for
   the deterministic `paper_single_box` OBB/box source report-scoped until a later Newton
   execution gate exists.
3. Keep the lane `partial` and keep `paper_faithful_offline_supported: false` until later dated
   records justify narrower bounded wording.
4. Keep `paper_faithful_offline`, full CPD reproduction, Newton support/execution, real USD,
   benchmark, collision-quality, deployment readiness, and safety certification claims
   unsupported; the next gate may only review whether the remaining import-boundary preconditions
   and first Newton entry decision are justified for this one synthetic lineage while keeping no
   real import, no `newton.ModelBuilder` instantiation, no real builder shape call, no
   model finalization, no collision pipeline execution, no real USD, no benchmark, and no quality
   boundary changes.
5. Keep bed/Franka reruns blocked until a separate real package change passes full mapping,
   contact, task, and dated-record gates.
6. Treat the gap matrix and offline lane spec as the review checklist, not as benchmark or quality
   evidence.

## Claim Boundary

This page adds narrow synthetic native-bundle, opt-in synthetic native-fitting, synthetic
native-selection audit, synthetic cylinder near-miss fixture, fit-ablation, scoring-sensitivity,
report-only scoring-policy ablation, report-only scoring-policy guardrail, synthetic offline
opt-in scoring-policy selection probe, explicitly opt-in synthetic package probe, synthetic
controlled merge-search package-path probe, and capped bed/Franka first-mesh real-USD
diagnostic-smoke claims. It also adds narrow explicitly opt-in synthetic Newton task-smoke claims
for the changed near-miss package pair and the changed controlled merge/search package pair, plus
a narrow offline synthetic two-step lookahead merge/search accounting claim, a narrow
lookahead-changed package-pair synthetic Newton task-smoke claim under recorded settings, and a
command-only four-block evidence-map claim for the recorded lookahead slice. It also records the
current offline CPD paper mapped-subset chain through one single-fixture runtime `PrimitiveSpec`,
one synthetic report-scoped `CollisionPackage.to_dict()` artifact, and one
runtime-admissibility preflight handoff row plus one report-only static runtime-admissibility row
for `paper_single_box`. It does not add package readiness, Newton readiness, Newton support or
Newton execution for that CPD paper package, real-USD evidence for that package, benchmark
evidence, collision-quality evidence, native primitive improvement, asset-wide or whole-robot
claims, scoring-policy improvement, merge-policy superiority, `paper_faithful_offline` support,
full CPD reproduction, deployment readiness, safety certification, general postprocess-quality
evidence, or general polygon mesh support.
