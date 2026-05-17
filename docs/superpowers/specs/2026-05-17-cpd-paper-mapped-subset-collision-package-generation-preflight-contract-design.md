# CPD Paper Mapped-Subset CollisionPackage Generation Preflight Contract Design

## Goal

Close the next CPD paper-lane gate,
`paper_mapped_subset_collision_package_generation_preflight_contract`, by validating that the
single synthetic `paper_single_box` runtime `PrimitiveSpec.to_dict()` row is eligible for a later
CollisionPackage-generation gate.

This is a preflight gate only. It must not create a `CollisionPackage`, must not call Newton, must
not run a runtime-admissibility check, and must not claim package readiness, Newton support,
benchmark evidence, collision-quality evidence, `paper_faithful_offline` support, or full CPD
reproduction.

## Context

The current report chain is:

```text
native fixture PrimitiveSpec-like dict
-> canonical JSON serialization
-> runtime-boundary preflight
-> runtime PrimitiveSpec construction
```

The runtime-construction gate now constructs exactly one runtime `PrimitiveSpec` object from the
canonical synthetic `paper_single_box` OBB/box row and stores only `PrimitiveSpec.to_dict()` in the
JSON report. The next gate must decide whether that report-scoped runtime PrimitiveSpec output can
be treated as a candidate for a later package-generation step. It should not perform that later
step.

## Selected Approach

Add one in-report preflight helper in
`src/primitive_collision_compiler/baselines/cpd_paper/offline.py`.

The helper will:

- consume `paper_mapped_subset_primitivespec_runtime_construction_contract`;
- verify the input gate, expected next gate, row count, one constructed runtime PrimitiveSpec,
  zero generated CollisionPackages, zero runtime-admissibility checks, and false package/Newton
  execution triggers;
- validate that the runtime-construction row still describes `paper_single_box`,
  `oriented_bounding_box`, `box`, and Newton runtime kind `box`;
- validate that `generated_primitive_spec` equals `constructed_primitivespec_dict` and is JSON
  serializable;
- validate that the constructed dict contains the supported mapped-subset fields needed for a
  later package row: `primitive_id`, `kind`, `pose`, `center`, `axes`, `dimensions`,
  `source_faces`, `volume`, `weighted_volume`, `frame`, `contains_assigned_points`, and
  `conversion_status`;
- record exactly one later collision-package generation candidate row;
- keep `package_generation_allowed_in_current_gate`, `collision_package_generated`,
  `runtime_admissibility_checked`, and all Newton/real-USD/benchmark/collision-quality triggers
  false;
- advance the next gate to `paper_mapped_subset_collision_package_generation_contract`.

The `generated_runtime_primitive_spec_count: 1` and `generated_primitive_spec_count: 1` fields in
this gate describe consumed upstream runtime-construction evidence. This preflight gate must not
construct another `PrimitiveSpec`.

## Alternatives Considered

Construct a `CollisionPackage` immediately.

This crosses the current boundary. It would mix package schema work, runtime-admissibility work,
and Newton-facing risk into a gate that is supposed to be only a preflight check.

Only update documentation and leave the report unchanged.

This would preserve safety but would not close the current report gate. The report would still
point at the preflight contract as missing.

Add a preflight candidate row without package construction.

This is the selected approach. It reduces the current report gap while keeping package generation
as a separate, reviewable gate.

## Data Contract

The new payload key will be:

```text
paper_mapped_subset_collision_package_generation_preflight_contract
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
- `artifact_kind`
- `schema_version`
- `source_scope`
- `implementation_boundary`
- `package_generation_preflight_action`
- `package_generation_preflight_requirements`
- `package_generation_preflight_row_count`
- `later_collision_package_generation_candidate_count`
- `package_generation_allowed_in_current_gate`
- `generated_runtime_primitive_spec_count`
- `generated_primitive_spec_count`
- `generated_collision_package_count`
- `runtime_admissibility_check_count`
- `package_generation_preflight_contract`
- `input_contract_summary`
- `package_generation_preflight_rows`
- `coverage_summary`
- `remaining_gaps`
- package, runtime-admissibility, Newton, real-USD, benchmark, collision-quality, deployment,
  certification, approximation-policy, and silent-drop false flags.

Required row fields:

- `package_generation_preflight_row_id`
- `source_runtime_construction_row_id`
- `source_runtime_boundary_preflight_row_id`
- all upstream lineage ids carried by the runtime-construction row
- `fixture_id`
- `paper_primitive`
- `primitive_spec_kind`
- `candidate_mapping_label`
- `newton_runtime_kind`
- `primitive_id`
- `kind`
- `generated_primitive_spec`
- `constructed_primitivespec_dict`
- `candidate_primitivespec_dict`
- `candidate_package_primitive_kind`
- `candidate_package_scope`
- `later_collision_package_generation_candidate`
- `package_generation_allowed_in_current_gate`
- `required_later_gate`
- `preflight_decision`
- `preflight_reason`
- `collision_package_generated`
- `generated_collision_package`
- `runtime_admissibility_checked`
- package, runtime-admissibility, Newton, real-USD, benchmark, collision-quality, deployment,
  certification, approximation-policy, and silent-drop false flags.

## Count Semantics

This gate is not package generation. Counts should be:

- `package_generation_preflight_row_count: 1`
- `later_collision_package_generation_candidate_count: 1`
- `generated_runtime_primitive_spec_count: 1`
- `generated_primitive_spec_count: 1`
- `generated_collision_package_count: 0`
- `runtime_admissibility_check_count: 0`

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

- reading the runtime-construction report payload;
- copying the already serialized `PrimitiveSpec.to_dict()` dict into a candidate row;
- validating JSON-serializable fields and mapped-subset kind metadata;
- recording one later package-generation candidate.

Forbidden in this gate:

- importing or instantiating `CollisionPackage`;
- creating `FallbackSpec` rows;
- importing or calling Newton;
- loading USD assets;
- checking runtime admissibility;
- running benchmarks, timing, surface-distance, or collision-quality metrics;
- mutating the `PrimitiveSpec` output from the runtime-construction gate;
- claiming package readiness, Newton readiness, collision quality, deployment readiness, safety
  certification, `paper_faithful_offline` support, or full CPD reproduction.

## Tests

Use TDD. Add failing tests first for:

- top-level report next gate and failure label changing to
  `paper_mapped_subset_collision_package_generation_contract`;
- exact payload schema for the package-generation preflight contract;
- exact row schema for the preflight row;
- one lineage row whose `candidate_primitivespec_dict` equals the source
  `generated_primitive_spec`;
- counts showing one later package-generation candidate and zero generated CollisionPackages;
- false package/Newton/real-USD/benchmark/collision-quality/deployment flags on the payload and
  row;
- strict JSON serialization with `json.dumps(payload, allow_nan=False, sort_keys=True)`;
- static source guard over only the new preflight helper block, not the whole file. It must forbid
  `CollisionPackage`, `FallbackSpec`, `PrimitiveSpec(`, Newton imports/calls, USD loading,
  benchmarks, executable runtime-admissibility helper calls, and collision-quality metric tokens.
  Field names such as `runtime_admissibility_checked` remain allowed because this gate must report
  them as false.
- malformed input rejection for stale input gate, stale input next gate, row-count drift,
  missing runtime PrimitiveSpec, mismatched generated/constructed PrimitiveSpec dicts, unsupported
  kind, true package/Newton flags, nonzero generated CollisionPackage count, and prior
  runtime-admissibility leakage.

## Documentation

Update:

- `README.md`
- `docs/index.md`
- `docs/deepdive/evidence-status.md`
- `docs/deepdive/message-map.md`
- `docs/reference/claim-boundaries.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/records/README.md`

Add:

- `docs/records/2026-05-17-cpd-paper-mapped-subset-collision-package-generation-preflight-contract.md`

All wording must say this is a single synthetic preflight candidate only. It must not claim
CollisionPackage generation, package readiness, Newton support, real-USD support, benchmark
evidence, collision quality, deployment readiness, safety certification, `paper_faithful_offline`,
or full CPD reproduction.
