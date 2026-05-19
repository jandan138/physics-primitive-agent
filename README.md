# Newton Primitive Collision Compiler

## Overview

The Newton Primitive Collision Compiler is a bootstrap-stage repository for a future
DeepDive-first workflow around Newton primitive collision artifacts.

## Current Status

This repository is a proposal/bootstrap for a DeepDive-first Newton primitive collision
compiler. It now includes a geometry-only CPD-like face-merge smoke path over USD meshes, plus
config dry-runs, USD asset-open smoke diagnostics, ignored repo-local USD mirror materialization
for the current bed/Franka smoke assets, Newton source diagnostics, and environment readiness
checks. It also includes a contact-only Newton canary for representative mapped primitive
types, plus named drop/settle and sphere-rain contact-density proxy Newton task smokes for the
capped bed CPD-like package. A separate Franka/simple robot smoke opens the local Franka USD and
runs capped first-mesh CPD-like geometry proposals. An opt-in CPD-like component-merge gate now
reports disconnected-component merge candidates and normalized excess-volume accounting while
remaining below full CPD reproduction. An offline CPD-like objective report now summarizes
paper-aligned surrogate terms for that baseline without claiming collision quality. A synthetic
objective comparison now reuses that report on three deterministic toy meshes to inspect
topology-only versus component-merge accounting without adding benchmark evidence. A focused
CPD-like cost-guided merge-search smoke now uses AABB-normalized merge-excess as a
decision-making cost on one deterministic toy mesh and reports old/new diagnostic accounting.
The expected-failure synthetic workbench now turns three known CPD-paper gaps into deterministic
diagnostic flags and reports whether those expected limitation flags remain visible; its
`smoke_passed` status means expected limitations were reported, not decomposition success. An
opt-in offline `capped_cylinder` geometry proposal proxy now records a named objective-report
smoke where the unsupported paper primitive gap decreases from 3 to 2; this is not Newton support
or paper-faithful primitive fitting. The native fitting/probe path now has a real-USD diagnostic
smoke over capped bed and capped Franka first-mesh scope: bed still selects boxes in both lanes,
while Franka's current support-aware native lane selects boxes and reports three cheaper raw-cost
cylinder candidates as support-blocked. All four packages map cleanly, pass contact canaries, and
pass gated drop/settle plus sphere-rain under recorded settings. This is native
selection/accounting evidence, not native primitive improvement evidence, whole-robot collider
quality, or benchmark evidence. The synthetic native fitting
comparison now also emits candidate weighted-volume audit tables that explain why `cylinder`,
`cone`, and `ellipsoid` win on the named toy fixtures; this is toy diagnostic accounting, not a
real-USD or collision-quality claim. The partial offline CPD paper report now also includes
fixture-breadth Batch A source/preprocess, Batch B primitive-fit, Batch C cost/search/stop,
Batch D component-pair, Batch E postprocess accounting, and a command-only synthetic
fixture-breadth completion review for planned Batches A-E. It now also includes a command-only
planning table for offline generalization beyond named toy fixtures. The report remains partial,
`paper_faithful_offline_supported` remains false. The report now also includes
`paper_generalization_batch_a_source_policy`, a command-only offline source-policy matrix for
deterministic synthetic meshes. That matrix records exact-coordinate dedup policy, source-face
intake/remap policy, concave-polygon rejection, and source-face `Q` aggregation accounting without
claiming robust mesh cleanup or general polygon intake. It now also includes
`paper_generalization_batch_b_primitive_fit_engine`, a command-only offline primitive-fit engine
matrix over deterministic in-memory probes for all six paper primitive names. That matrix records
candidate generation, selected-candidate accounting, containment checks, finite numeric fields,
and the offline-only boundary for paper-only primitives without adding package generation or
Newton runtime execution. It now also includes
`paper_generalization_batch_c_search_engine`, a command-only offline search-trace matrix that
summarizes existing topology queue, weighted-priority, equal-cost tie, threshold-stop, and
component-pair traces without adding a new optimizer. It now also includes
`paper_generalization_batch_d_postprocess_policy`, a command-only offline postprocess-policy
matrix over existing deterministic postprocess audit fixtures. That matrix records identity-axis
OBB culling, rotated OBB culling, conservative unsupported cross-type no-cull accounting,
before/after primitive counts, cull or unsupported reasons, and false package, Newton, real-USD,
and benchmark triggers. It now also includes
`paper_generalization_batch_e_package_boundary_readiness`, a command-only offline
package-boundary readiness matrix before package conversion. That matrix records that Batches A-D
produce audit matrices rather than a durable changed-decomposition output contract, and keeps
package generation and Newton runtime blocked. It now also includes
`paper_offline_changed_decomposition_output_contract`, an offline changed-decomposition output
contract, not a `CollisionPackage`. That contract records synthetic toy fixture decomposition
rows, stable offline primitive ids, source-face/group ids, selected paper primitive audit fields,
explicit postprocess state rows, and package/Newton/real-USD/benchmark false triggers. The report
now also includes `paper_package_adapter_contract`, a command-only offline
package-adapter contract, not a `CollisionPackage`. The adapter contract consumes those 16 offline
primitive records as adapter input rows and classifies all current `trapezoidal_prism`
`offline_only_unmapped` rows as `later_policy_required`. The report now also includes
`paper_package_adapter_unsupported_primitive_policy`, a command-only offline policy table, not a
`CollisionPackage`. That policy keeps the current 16 unmapped trapezoidal-prism rows offline,
records six paper primitive family policy rows, and advances the next paper-lane gate to
`paper_package_conversion_mapped_subset_plan`. The report now also includes
`paper_package_conversion_mapped_subset_plan`, a command-only offline mapped-subset
package-conversion planning table, not a `CollisionPackage`. That table identifies
`oriented_bounding_box`, `sphere`, and `capsule` as native-family review rows, keeps the
current 16 unmapped trapezoidal-prism rows offline, records zero current package-conversion
candidates, keeps package/Newton/real-USD/benchmark triggers false, and advances the next
paper-lane gate to `paper_mapped_subset_conversion_candidate_matrix`. The report now also includes
`paper_mapped_subset_conversion_candidate_matrix`, a command-only offline candidate matrix, not a
`CollisionPackage`. That matrix records three future-family review rows, keeps all 16 current
trapezoidal-prism rows blocked/offline, records zero current package-conversion candidates, keeps
PrimitiveSpec/CollisionPackage/runtime-admissibility/Newton/real-USD/benchmark triggers false,
and at that stage advanced the next paper-lane gate to
`paper_mapped_subset_adapter_preflight_contract`. The report now also includes
`paper_mapped_subset_adapter_preflight_contract`, a command-only offline adapter-preflight
contract, not `PrimitiveSpec` generation and not a `CollisionPackage`. That preflight contract
records future adapter requirements, keeps the current zero package-conversion-candidate state as
no-op, keeps all current unmapped trapezoidal-prism rows offline, keeps package generation
disabled, and advances the next paper-lane gate to
`paper_mapped_subset_primitivespec_dry_run_contract`. The report now also includes
`paper_mapped_subset_primitivespec_dry_run_contract`, a command-only offline PrimitiveSpec
dry-run contract, not real `PrimitiveSpec` generation and not a `CollisionPackage`. That dry-run
contract records future PrimitiveSpec shape requirements for OBB/box, sphere, and capsule,
keeps capped cylinder and frustum blocked behind an approximation policy, keeps all current
unmapped trapezoidal-prism rows offline/no-op, records zero current PrimitiveSpec candidates,
records zero generated PrimitiveSpec rows, and advances the next paper-lane gate to
`paper_mapped_subset_primitivespec_validation_contract`. The report now also includes
`paper_mapped_subset_primitivespec_validation_contract`, a command-only offline validation
contract for that dry-run payload, not real `PrimitiveSpec` generation and not a
`CollisionPackage`. That validation contract checks the declared dry-run field list, mapped
future shape labels for box/sphere/capsule, six family rows, 16 current no-op rows, source
traceability, zero current candidates, zero generated PrimitiveSpecs, and false runtime/evaluation
triggers, then advances the next paper-lane gate to
`paper_mapped_subset_primitivespec_generation_preflight_contract`. The report now also includes
`paper_mapped_subset_primitivespec_generation_preflight_contract`, a command-only offline
generation-preflight contract for that validation payload, not real `PrimitiveSpec` generation
and not a `CollisionPackage`. That generation-preflight contract records future native-family
requirements for OBB/box, sphere, and capsule, keeps capped cylinder and frustum blocked behind
approximation policy, keeps trapezoidal prism no-op/unmapped, records zero current generation
candidates, zero generated PrimitiveSpecs, zero generated CollisionPackages, and zero runtime
admissibility checks, then advances the next paper-lane gate to
`paper_mapped_subset_primitivespec_generation_contract`. The report now also includes
`paper_mapped_subset_primitivespec_generation_contract`, a command-only offline PrimitiveSpec
generation contract that emits template rows for future Newton-native box/sphere/capsule families
only, keeps all current unmapped rows offline/no-op, records zero runtime PrimitiveSpecs, zero
CollisionPackages, and zero runtime-admissibility checks, then advances the next paper-lane gate
to `paper_mapped_subset_primitivespec_candidate_source_contract`. The report now also includes
`paper_mapped_subset_primitivespec_candidate_source_contract`, a command-only offline
candidate-source audit, not runtime `PrimitiveSpec` generation and not a `CollisionPackage`.
That audit keeps the three native-family template rows future-only, records two blocked
approximation-policy family rows, records one no-op trapezoidal-prism family row, classifies all
16 current `trapezoidal_prism` / `offline_only_unmapped` rows as traceable but ineligible, keeps
eligible current PrimitiveSpec candidate sources at zero, and advances the next paper-lane gate to
`paper_mapped_subset_native_current_fixture_contract`. The report now also includes
`paper_mapped_subset_native_current_fixture_contract`, a command-only offline native-current
fixture source contract, not runtime `PrimitiveSpec` generation and not a `CollisionPackage`.
That contract records exactly one synthetic `paper_single_box` selected OBB/box source row traced
to the future OBB template, records one eligible current candidate source and one report-only
PrimitiveSpec generation candidate, keeps generated PrimitiveSpecs, CollisionPackages,
runtime-admissibility checks, Newton runtime, real-USD loading, benchmark runs,
collision-quality measurement, and deployment/certification claims at zero or false, and advances
the next paper-lane gate to
`paper_mapped_subset_primitivespec_native_fixture_generation_contract`. The report now also
includes `paper_mapped_subset_primitivespec_native_fixture_generation_contract`, a command-only
offline native-fixture PrimitiveSpec-like dict generation contract, not runtime `PrimitiveSpec`
object creation and not a `CollisionPackage`. It emits exactly one JSON-serializable,
report-only PrimitiveSpec-like dict for the synthetic `paper_single_box` OBB/box source row,
keeps generated runtime PrimitiveSpecs, CollisionPackages, runtime-admissibility checks, Newton
runtime, real-USD loading, benchmark runs, collision-quality measurement, and
deployment/certification claims at zero or false, and advances the next paper-lane gate to
`paper_mapped_subset_primitivespec_native_fixture_serialization_contract`. The report now also
includes `paper_mapped_subset_primitivespec_native_fixture_serialization_contract`, a
command-only offline serialization/schema-stability contract for that one report-only dict, not
runtime `PrimitiveSpec` object creation and not a `CollisionPackage`. It validates strict
canonical JSON serialization with `allow_nan=False`, sorted keys, compact separators, and a
round-trip equality check for the deterministic `paper_single_box` OBB/box dict, keeps generated
runtime PrimitiveSpecs, CollisionPackages, runtime-admissibility checks, Newton runtime, real-USD
loading, benchmark runs, collision-quality measurement, and deployment/certification claims at
zero or false, and advances the next paper-lane gate to
`paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`. The report now also
includes `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`, a command-only
offline boundary preflight, not runtime `PrimitiveSpec` object creation and not a
`CollisionPackage`. It records exactly one later runtime `PrimitiveSpec` construction candidate
for the same synthetic `paper_single_box` OBB/box row, keeps runtime construction disallowed in
the current gate, keeps generated runtime PrimitiveSpecs, CollisionPackages,
runtime-admissibility checks, Newton runtime, real-USD loading, benchmark runs,
collision-quality measurement, and deployment/certification claims at zero or false, and advances
the next paper-lane gate to
`paper_mapped_subset_primitivespec_runtime_construction_contract`. The report now also includes
`paper_mapped_subset_primitivespec_runtime_construction_contract`, a single-fixture offline
runtime-construction contract, not a `CollisionPackage` and not Newton execution. It constructs
exactly one runtime `PrimitiveSpec` object from the canonical preflight JSON for the same
synthetic `paper_single_box` OBB/box row after checking the runtime-boundary preflight row's
canonical JSON SHA-256 fingerprint, stores only `PrimitiveSpec.to_dict()` in the report, records
generated runtime PrimitiveSpec counts as one, keeps CollisionPackages, runtime-admissibility
checks, Newton runtime, real-USD loading, benchmark runs, collision-quality measurement, and
deployment/certification claims at zero or false, and advances the next paper-lane gate to
`paper_mapped_subset_collision_package_generation_preflight_contract`. The report now also
includes `paper_mapped_subset_collision_package_generation_preflight_contract`, a single-fixture
offline preflight contract, not a `CollisionPackage` and not Newton execution. It records exactly
one later package-generation candidate from that `PrimitiveSpec.to_dict()` payload, keeps package
generation disallowed in the current gate, keeps generated CollisionPackages and
runtime-admissibility checks at zero, and advances the next paper-lane gate to
`paper_mapped_subset_collision_package_generation_contract`. The report now also includes
`paper_mapped_subset_collision_package_generation_contract`, a single-fixture offline
CollisionPackage generation contract. It constructs exactly one synthetic, report-scoped
`CollisionPackage.to_dict()` artifact for the same `paper_single_box` OBB/box row, records
`generated_collision_package_count: 1`, keeps runtime-admissibility checks at zero, marks the
package status as `offline_synthetic_candidate_runtime_admissibility_not_checked`, and advances the next
paper-lane gate to `paper_mapped_subset_runtime_admissibility_preflight_contract`. The report now
also includes `paper_mapped_subset_runtime_admissibility_preflight_contract`, a single-fixture
offline preflight contract, not a runtime-admissibility check and not Newton execution. It consumes
that one synthetic `CollisionPackage.to_dict()` artifact, validates its identity, source metadata,
schema, primitive subset, and false trigger flags, records exactly one later
runtime-admissibility candidate row without copying the full package dict, keeps
`runtime_admissibility_check_count: 0`, and advances the next paper-lane gate to
`paper_mapped_subset_runtime_admissibility_contract`. The report now also includes
`paper_mapped_subset_runtime_admissibility_contract`, a single-fixture offline/static
runtime-admissibility contract, not Newton mapping and not Newton execution. It checks only the
same synthetic `paper_single_box` box package for finite center, right-handed orthonormal axes,
positive half extents, target box dimension schema, source-face coverage, containment flag, and
positive volume accounting. It records `runtime_admissibility_check_count: 1` as one offline
static report check, keeps runtime execution, Newton mapping, Newton runtime, real-USD loading,
benchmark runs, and collision-quality measurement at zero or false, and advances the next
runtime-lane gate to `paper_mapped_subset_newton_shape_mapping_preflight_contract`. The report now
also includes `paper_mapped_subset_newton_shape_mapping_preflight_contract`, a single-fixture
offline/static shape-mapping handoff preflight, not Newton mapping and not Newton execution. It
checks only that the same `paper_single_box` box PrimitiveSpec-like dict has the static fields a
later mapper would need: target kind `box`, center, axes, dimensions, and box half extents. It
records `newton_shape_mapping_preflight_row_count: 1`, `mapping_attempt_count: 0`,
`newton_mapping_record_count: 0`, and `newton_runtime_execution_count: 0`, keeps Newton support
claims false, and advances the current runtime-lane gate to
`paper_mapped_subset_newton_shape_mapping_contract`. The report now also includes
`paper_mapped_subset_newton_shape_mapping_contract`, a single-fixture offline/static Newton shape
descriptor contract, not Newton object construction and not Newton execution. It consumes that
preflight row, records exactly one report-scoped `newton_shape_descriptor_dict` for target kind
`box`, keeps `mapping_attempt_count: 0`, `newton_mapping_record_count: 0`,
`newton_shape_object_count: 0`, and `newton_runtime_execution_count: 0`, keeps Newton support
claims false, and advances the current runtime-lane gate to
`paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`. The report now also
includes `paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract`, a single-fixture
offline/static Newton shape runtime-boundary preflight, not Newton shape object construction and
not Newton execution. It consumes the descriptor row, records exactly one later Newton shape
runtime-construction candidate for the same synthetic `paper_single_box` box descriptor, keeps
`mapping_attempt_count: 0`, `newton_mapping_record_count: 0`,
`newton_shape_object_count: 0`, and `newton_runtime_execution_count: 0`, keeps Newton support
claims false, and advances the current runtime-lane gate to
`paper_mapped_subset_newton_shape_runtime_construction_contract`. The report now also includes
`paper_mapped_subset_newton_shape_runtime_construction_contract`, a single-fixture
offline/report-scoped Newton shape mapping-record construction contract, not a Newton engine
shape, not a Newton builder call, and not Newton execution. It consumes the runtime-boundary
preflight row, constructs exactly one repo-local `NewtonShapeMapping.to_dict()` report record for
the same synthetic `paper_single_box` box descriptor, records
`constructed_newton_shape_mapping_record_count: 1` and `newton_mapping_record_count: 1`, keeps
`newton_shape_object_count: 0`, `newton_engine_shape_object_count: 0`,
`newton_builder_shape_call_count: 0`, and `newton_runtime_execution_count: 0`, keeps Newton
support claims false, and advances the current runtime-lane gate to
`paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`. The report now also
includes `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`, a single-fixture
offline/static Newton builder-call-plan preflight, not a Newton builder call and not Newton
execution. It consumes that repo-local `NewtonShapeMapping.to_dict()` record, records exactly one
JSON-safe plan for the future `box` builder signature fields `body`, `xform`, `hx`, `hy`, and
`hz`, keeps `builder_call_allowed_count: 0`, `newton_engine_shape_object_count: 0`,
`newton_builder_shape_call_count: 0`, and `newton_runtime_execution_count: 0`, keeps Newton
support claims false, and advances the current runtime-lane gate to
`paper_mapped_subset_newton_shape_runtime_builder_construction_contract`. The report now also
includes `paper_mapped_subset_newton_shape_runtime_builder_construction_contract`, a
single-fixture offline/report-only recording-builder construction contract, not a real Newton
builder call and not Newton execution. It consumes that builder-preflight row, reconstructs the
repo-local `NewtonShapeMapping.to_dict()` data, calls the repo-local static shape dispatch helper
with a recording builder and a fake Warp-like module, and records exactly one JSON-safe
`add_shape_box` call artifact with body `-1`, fake transform data, and the actual mapped box
half extents. It records `recording_builder_shape_call_count: 1`,
`recorded_builder_call_count: 1`, and `repo_local_static_shape_helper_call_count: 1`, while
keeping `real_newton_import_count: 0`, `newton_engine_shape_object_count: 0`,
`newton_builder_shape_call_count: 0`, and `newton_runtime_execution_count: 0`. The current
report now also includes
`paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract`, a
single-fixture offline/static boundary-preflight checklist before any real Newton engine-builder
boundary crossing. It consumes the recording-builder call artifact, records the future
`newton.ModelBuilder` / `add_shape_box` boundary requirements and the provenance checks needed
before a later environment probe, and keeps real Newton imports, Newton `ModelBuilder`
instantiation, real Newton builder shape calls, model finalization, collision pipeline calls, and
Newton execution at zero. The report now also includes
`paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract`, a
single-fixture bounded environment/provenance row for that future `newton.ModelBuilder` /
`add_shape_box` boundary. It records the configured-source-dir status and Newton/Warp
`find_spec` provenance shape without returning live runtime modules, without importing Newton or
Warp in the default no-config offline report, and without crossing into builder/runtime code. The
report now also includes
`paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract`, a
single-fixture bounded source-AST API-surface row for the same future builder boundary. The
default no-config report records `not_run_source_dir_not_configured`; when a Newton source
directory is explicitly passed, this lane may read source files and parse AST only. It still
imports no Newton/Warp runtime, instantiates no `newton.ModelBuilder`, makes no real builder
shape call, finalizes no model, creates no collision pipeline, and runs no Newton code. The
report now also includes
`paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract`, a
single-fixture report-only engine-builder entry decision. It consumes the API-surface row,
records the default no-config decision `defer_real_runtime_entry`, keeps real Newton/Warp
imports, `newton.ModelBuilder`, Newton engine shape objects, real builder calls, model
finalization, collision pipeline calls, and Newton execution at zero. The report now also includes
`paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract`, a
single-fixture report-only skipped-smoke decision. It consumes the entry row, records
`smoke_decision: skip_real_runtime_smoke` for the default no-runtime-entry path, keeps real
Newton/Warp imports, `newton.ModelBuilder`, Newton engine shape objects, real builder calls, model
finalization, collision pipeline calls, and Newton execution at zero, and advances the current
runtime-lane gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract`. The package dict,
preflight row, static runtime-admissibility row, shape-mapping preflight row, static shape
descriptor row, runtime-boundary preflight row, runtime-construction mapping record, builder
preflight plan, recording-builder call artifact, engine-builder boundary preflight row, and
environment-probe/API-surface/entry/smoke rows are only serialized offline candidates for one box
fixture: they are not general package readiness, not Newton readiness, not Newton support, not
Newton execution, not real-USD
evidence, not benchmark evidence, not
collision-quality evidence, not paper primitive vocabulary coverage, not `paper_faithful_offline`,
not deployment readiness, and not safety certification. These
source-policy,
primitive-fit-engine, search-engine, postprocess-policy, package-boundary-readiness,
changed-decomposition-contract, adapter-contract, unsupported-primitive-policy, mapped-subset
planning/candidate-matrix/preflight/PrimitiveSpec/runtime/CollisionPackage/admissibility,
Newton shape-mapping, Newton shape runtime, Newton engine-builder boundary-preflight, and
Newton engine-builder environment-probe/API-surface/entry/smoke slices do not
support `paper_faithful_offline`, full CPD reproduction, Newton runtime execution, real-USD
evidence, collision-quality evidence, benchmark evidence, deployment readiness, or safety
certification. The consolidated entry gate is a deliberate anti-overdesign boundary: the earlier
closed boundary-preflight, environment-probe, and API-surface rows remain as evidence, but the
import-boundary preconditions and first Newton entry decision were reviewed together instead of
split across another pair of small gates. The smoke gate is now closed as a skipped-smoke
decision, not a real Newton import or runtime run. The next gate is a future runtime-execution
contract. See
`docs/reference/cpd-like-face-merge-explainer.md` for the
plain-language boundary between the current baseline and a full CPD paper reproduction. See
`docs/reference/cpd-paper-story-status.md` for where the repository sits in the broader CPD paper
story. See `docs/reference/cpd-objective-report-alignment.md` for why the objective report is
design-aligned with the paper story, now including structured Eq.4 alignment metadata, but not yet
a paper-faithful objective implementation. The
clean local Newton Python environment has recorded readiness evidence, but the
repository does not yet produce benchmark results, broad asset/task evidence, whole-robot
collider-quality evidence, real contact-stress measurement, or a production collision compiler.

## Strategic Framing

The project intends to explore whether primitive collision representations can be compiled
from research-backed descriptions, source notes, and Newton-diagnostic-checker-planned records
before committing to a production mesh-processing implementation. The bootstrap phase keeps
claims narrow so the repository can separate documented intent from executable behavior.

## Safe Claim

Use this framing for current work:

The Newton Primitive Collision Compiler is a bootstrap-stage proposal for a DeepDive-first
future workflow that intends to explore Newton primitive collision artifacts from documented,
reviewed, and Newton-diagnostic-checker-planned inputs.

## Unsafe Claim

Do not claim that this repository currently:

- Implements a finished collision compiler.
- Performs complete production mesh processing.
- Produces production-ready Newton collision primitives.
- Provides simulation-verified results. Use "simulation-checked" only when a dated record links a
  generated package to a named task-level Newton diagnostic probe, settings, asset, environment,
  and report. Contact-only canary records do not qualify. Until then use "geometry-only",
  "contact-only Newton canary", "environment-readiness", or "Newton-checker-planned".

## Repository Layout

- `docs/`: research notes, source records, and bootstrap planning materials.
- `configs/`: DeepDive and Phase 0 config examples.
- `scripts/`: repository maintenance and validation commands.
- `src/primitive_collision_compiler/`: installable package with CLI, diagnostics, and the
  geometry-only CPD-like smoke path.
- `tests/`: bootstrap tests for currently advertised command surfaces.
- `assets/`, `experiments/`, `reports/`, `archive/`: artifact boundaries and registries.
- `AGENTS.md`: rules for future agentic work in this repository.
- `pyproject.toml`: project metadata, packaging configuration, pytest configuration, and
  Ruff configuration.
- `requirements.txt`: editable development install entry point.
- `Makefile`: common development commands.

## Quick Start

Install the project in editable development mode:

```sh
python -m pip install -e ".[dev]"
```

Run test collection:

```sh
python -m pytest --collect-only
```

Run the documented make targets as they become available:

```sh
make install
make test
make docs-check
make validate
```

At this stage `docs-check` enforces required governance docs, claim-boundary linting, and local
Markdown link checks.

## DeepDive Navigation

DeepDive source notes and bootstrap records live under `docs/`. These materials are the
current basis for project framing, claim boundaries, and future implementation plans.

## Current Non-Goals

- No production mesh-processing or collision-compiler implementation.
- No broad task-level Newton simulation coverage yet; current task smokes are limited to the
  recorded capped bed, capped Franka first-mesh, and synthetic native-bundle diagnostics.
- No whole-robot collider-quality or articulated-dynamics evidence; the Franka path is import and
  capped first-mesh geometry smoke only.
- No full CPD paper reproduction; the component-merge gate, Eq.4 alignment metadata, and objective
  report are restricted CPD-like baseline diagnostics, and the cost-guided merge-search smoke is a
  restricted synthetic algorithmic smoke slice. The expected-failure synthetic workbench is
  diagnostic limitation accounting, and the capped-cylinder proxy is offline primitive-vocabulary
  accounting. Neither is benchmark evidence, collision-quality validation, Newton capped-cylinder
  support, or a paper-faithful CPD reproduction.
- No generated collision artifact pipeline.
- No claim of production readiness.
