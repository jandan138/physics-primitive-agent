# 2026-05-17 CPD Paper Mapped-Subset PrimitiveSpec Native-Fixture Generation Contract

## Status

Complete.

## Context

The previous gate, `paper_mapped_subset_native_current_fixture_contract`, recorded exactly one
eligible synthetic `paper_single_box` selected OBB/box source row and one report-only
PrimitiveSpec generation candidate. It deliberately kept generated runtime PrimitiveSpecs,
generated CollisionPackages, runtime-admissibility checks, Newton runtime, real-USD loading,
benchmark runs, collision-quality measurement, deployment, and certification triggers at zero or
false.

This record closes only the next command-only offline gate:

`paper_mapped_subset_primitivespec_native_fixture_generation_contract`

## What Changed

The partial `cpd_paper_offline_report` now includes
`paper_mapped_subset_primitivespec_native_fixture_generation_contract`.

The new payload:

- consumes `paper_mapped_subset_native_current_fixture_contract`;
- validates that the input has exactly one eligible `paper_single_box` OBB/box source row;
- emits exactly one JSON-serializable, report-only PrimitiveSpec-like dictionary shaped like
  `PrimitiveSpec.to_dict()`;
- records `offline_serialized_primitivespec_like_dict_count: 1`;
- records `generated_runtime_primitive_spec_count: 0`;
- keeps `generated_primitive_spec_count: 0` for the existing runtime-generation count semantics;
- keeps generated CollisionPackages and runtime-admissibility checks at zero;
- advances the next gate to
  `paper_mapped_subset_primitivespec_native_fixture_serialization_contract`.

The emitted dict is review data only. It is not a runtime `PrimitiveSpec` object and is not part
of a `CollisionPackage`.

Review follow-up tightened the source-face lineage check: `fixture_source_faces` must be a nonempty
list or tuple of non-negative integer ids. Floats, booleans, negative ids, and empty source-face
lists are rejected instead of being silently coerced into different face ids.

## Evidence

Command:

```bash
PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report
```

The relevant report fields are:

- `next_required_gate: paper_mapped_subset_primitivespec_native_fixture_serialization_contract`
- `failure_labels: [paper_mapped_subset_primitivespec_native_fixture_serialization_contract_missing]`
- `paper_mapped_subset_primitivespec_native_fixture_generation_contract.offline_serialized_primitivespec_like_dict_count: 1`
- `paper_mapped_subset_primitivespec_native_fixture_generation_contract.generated_runtime_primitive_spec_count: 0`
- `paper_mapped_subset_primitivespec_native_fixture_generation_contract.generated_collision_package_count: 0`
- `paper_mapped_subset_primitivespec_native_fixture_generation_contract.runtime_admissibility_check_count: 0`
- malformed native-fixture source-face ids fail with
  `primitivespec_native_fixture_generation_invalid_source_face_id`

## Claim Boundary

Supported:

- partial command-only offline native-fixture PrimitiveSpec-like dict generation for one
  deterministic synthetic fixture;
- source traceability from the generated dict back to the selected `paper_single_box` OBB/box
  native-current fixture source row;
- explicit accounting that runtime PrimitiveSpec objects, CollisionPackages, runtime-admissibility
  checks, Newton runtime, real-USD, benchmark, collision-quality, deployment, and certification
  triggers remain zero or false.

Not supported:

- runtime `PrimitiveSpec` object creation;
- package readiness or `CollisionPackage` generation;
- runtime admissibility;
- Newton support or Newton execution;
- real-USD evidence;
- benchmark evidence;
- collision-quality evidence;
- `paper_faithful_offline` support;
- full CPD reproduction;
- deployment readiness or safety certification.

## Next Gate

`paper_mapped_subset_primitivespec_native_fixture_serialization_contract`

The next gate should validate serialization/schema stability for the report-only dict before any
package adapter, runtime-admissibility, or Newton wording is allowed.
