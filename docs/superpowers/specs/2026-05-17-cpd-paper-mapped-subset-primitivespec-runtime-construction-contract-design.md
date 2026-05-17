# CPD Paper Mapped-Subset PrimitiveSpec Runtime Construction Contract Design

## Goal

Close the next CPD paper-lane gate,
`paper_mapped_subset_primitivespec_runtime_construction_contract`, by constructing exactly one
runtime `PrimitiveSpec` object from the already validated synthetic `paper_single_box` OBB/box
serialization row.

This is a narrow runtime-construction smoke for one deterministic mapped-subset fixture. It is not
package generation, Newton execution, real-USD evidence, benchmark evidence, collision-quality
evidence, `paper_faithful_offline` support, or full CPD reproduction.

## Context

The current report chain already closed:

```text
native fixture PrimitiveSpec-like dict
-> canonical JSON serialization
-> runtime-boundary preflight
```

The runtime-boundary preflight gate records one later runtime construction candidate but explicitly
keeps runtime construction disallowed. The next step should consume only that preflight payload,
validate that the row is still the same canonical `paper_single_box` box payload, construct one
`PrimitiveSpec`, serialize it back through `PrimitiveSpec.to_dict()`, and report the result.

## Selected Approach

Use a single in-report helper in
`src/primitive_collision_compiler/baselines/cpd_paper/offline.py`.

The helper will:

- import `PrimitiveSpec` locally inside the construction helper;
- validate the input preflight gate, expected next gate, counts, row count, row lineage, and false
  package/Newton/real-USD/benchmark flags;
- load the canonical JSON payload from the preflight row;
- require the loaded payload to match the strict PrimitiveSpec-like schema and source row values;
- instantiate one `PrimitiveSpec` with tuple-normalized fields and an explicit runtime
  construction `conversion_status`;
- immediately store only `constructed_primitivespec_dict = primitive.to_dict()` in the JSON report;
- record that one runtime `PrimitiveSpec` was constructed for this gate;
- keep `generated_collision_package_count` and `runtime_admissibility_check_count` at zero;
- advance the next gate to `paper_mapped_subset_collision_package_generation_preflight_contract`.

## Alternatives Considered

Use only another report-only preflight gate.

This would be safest but too small: the previous gate already did this. It would not reduce the
current gap because no runtime `PrimitiveSpec` would exist.

Construct a `CollisionPackage` immediately after `PrimitiveSpec`.

This crosses two boundaries at once. It would make it harder to isolate object construction bugs
from package schema bugs and would weaken claim boundaries. Package work should be a separate gate.

Construct one runtime `PrimitiveSpec` now and defer package generation.

This is the selected approach. It reduces the exact current gap while keeping the runtime surface
small, deterministic, and reviewable.

## Data Contract

The new payload key will be:

```text
paper_mapped_subset_primitivespec_runtime_construction_contract
```

Required payload fields:

- `gate_id`
- `gate_status`
- `closed_gate`
- `input_gate_id`
- `next_required_gate`
- `decision`
- `decision_reason`
- `paper_faithful_offline_allowed`
- `package_generation_allowed`
- `artifact_kind`
- `schema_version`
- `source_scope`
- `implementation_boundary`
- `runtime_construction_action`
- `runtime_construction_requirements`
- `runtime_construction_row_count`
- `constructed_runtime_primitivespec_count`
- `generated_runtime_primitive_spec_count`
- `generated_primitive_spec_count`
- `generated_collision_package_count`
- `runtime_admissibility_check_count`
- `runtime_construction_contract`
- `input_contract_summary`
- `runtime_construction_rows`
- `coverage_summary`
- `remaining_gaps`

The row will include source lineage from the preflight row, the canonical JSON input, the loaded
payload dict, the constructed `PrimitiveSpec.to_dict()` output, the conversion-status transition,
and explicit package/Newton/real-USD false flags.

Required row fields:

- `runtime_construction_row_id`
- `source_runtime_boundary_preflight_row_id`
- all lineage ids carried by the preflight row;
- `fixture_id`
- `paper_primitive`
- `primitive_spec_kind`
- `candidate_mapping_label`
- `newton_runtime_kind`
- `primitive_id`
- `kind`
- `canonical_primitivespec_json`
- `loaded_primitivespec_payload`
- `constructed_primitivespec_dict`
- `conversion_status_transition`
- `runtime_instance_generated`
- `generated_primitive_spec`
- package, runtime-admissibility, Newton, real-USD, benchmark, collision-quality, deployment,
  certification, approximation-policy, and silent-drop false flags. These include both generated
  flags, allowed flags, triggered flags, and support-claim flags for the forbidden runtime/package
  boundaries.

## Count Semantics

This gate is the first gate allowed to construct a runtime `PrimitiveSpec` object.

The payload should therefore report:

- `constructed_runtime_primitivespec_count: 1`
- `generated_runtime_primitive_spec_count: 1`
- `generated_primitive_spec_count: 1`
- `generated_collision_package_count: 0`
- `runtime_admissibility_check_count: 0`

The new gate must not reuse the previous all-false PrimitiveSpec-generation flag bundle blindly.
PrimitiveSpec construction indicators are true/count one for this gate; package, runtime
admissibility, Newton, real-USD, benchmark, collision-quality, deployment, certification,
approximation-policy, and silent-drop indicators remain false/count zero.

The top-level report remains partial and must still report:

- `paper_faithful_offline_supported: false`
- `package_generation_triggered: false`
- `newton_runtime_triggered: false`
- `real_usd_triggered: false`
- `benchmark_triggered: false`
- `collision_quality_measured: false`
- `deployment_or_certification_claimed: false`

## Boundary Rules

Allowed in this gate:

- one local import of `PrimitiveSpec` inside the construction helper;
- one `PrimitiveSpec(...)` call for the canonical `paper_single_box` OBB/box row;
- changing only `conversion_status` from the previous report-only value to
  `runtime_primitivespec_constructed_from_canonical_preflight_payload`;
- preserving dict-shaped `dimensions`, including `half_extents`, when constructing and serializing
  the `PrimitiveSpec`;
- storing `primitive.to_dict()` in the report.

Forbidden in this gate:

- `CollisionPackage(...)`;
- Newton imports or calls;
- real USD loading;
- benchmark/timing/surface-distance metrics;
- collision-quality measurement;
- package generation or runtime-admissibility checks;
- storing a live Python object in the JSON report.

The existing static guard for runtime-boundary preflight must be narrowed so it guards only the
preflight block. A new static guard must allow `PrimitiveSpec(` in the construction block while
still forbidding `CollisionPackage(` and Newton imports/calls.

## Tests

Use TDD. Add failing tests first for:

- top-level report next gate and failure label changing to
  `paper_mapped_subset_collision_package_generation_preflight_contract`;
- exact payload schema for the runtime-construction contract;
- exact row schema for the runtime-construction row;
- one lineage row with geometry/source fields equal to the canonical source payload after
  `PrimitiveSpec.to_dict()` normalization, plus an explicit conversion-status transition from
  report-only input to runtime-construction output;
- counts showing exactly one runtime `PrimitiveSpec` and zero package/runtime-admissibility work;
- static import/call boundaries over the entire runtime-construction block, allowing exactly one
  local `PrimitiveSpec` import/call and forbidding `CollisionPackage`, Newton, USD-loading,
  benchmark execution, and collision-quality metric tokens;
- malformed input rejection for stale gates, count drift, missing candidate flag, canonical JSON
  drift, canonical payload value drift, and previous preflight runtime-object leakage.

## Documentation

Update:

- `README.md`
- `docs/index.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- `docs/reference/claim-boundaries.md`
- `docs/records/README.md`

Add:

- `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-runtime-construction-contract.md`

All wording must say this is one deterministic synthetic runtime `PrimitiveSpec` construction
smoke only. It must not claim PrimitiveSpec readiness, package readiness, Newton support, real-USD
support, benchmark evidence, collision quality, deployment readiness, safety certification,
`paper_faithful_offline`, or full CPD reproduction.

## Verification

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_construction or runtime_boundary_preflight' -q
PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report >/tmp/cpd_paper_runtime_construction_report.json
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

## Spec Review

- Placeholder scan: no placeholder sections remain.
- Internal consistency: the selected approach constructs only `PrimitiveSpec` and leaves package,
  runtime-admissibility, Newton, real-USD, benchmark, and collision-quality work outside scope.
- Scope check: this is one narrow contract gate, not a broad package or benchmark implementation.
- Ambiguity check: counts and next gate are explicit.
