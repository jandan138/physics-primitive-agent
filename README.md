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
`paper_mapped_subset_primitivespec_native_fixture_serialization_contract`. These
source-policy,
primitive-fit-engine, search-engine, postprocess-policy, package-boundary-readiness, and
changed-decomposition-contract, adapter-contract, unsupported-primitive-policy, and
mapped-subset-planning/candidate-matrix/preflight/primitivespec-dry-run/validation/generation-preflight/generation-contract/candidate-source/native-current-fixture/native-fixture-primitivespec-dict slices do not
support full CPD reproduction, package generation, Newton runtime execution, real-USD evidence,
collision-quality evidence, benchmark evidence, deployment readiness, or safety certification. See
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
