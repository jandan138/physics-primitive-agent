# CPD Paper Mapped-Subset Newton Shape-Mapping Preflight Contract Design

## Context

The current CPD paper offline report ends at
`paper_mapped_subset_newton_shape_mapping_preflight_contract_missing`.

The previous implemented gate,
`paper_mapped_subset_runtime_admissibility_contract`, records exactly one offline/static
runtime-admissibility row for the synthetic `paper_single_box` OBB/box package artifact. That row
checks finite geometry, right-handed orthonormal axes, positive box half extents, source-face
coverage, containment, and volume accounting. It deliberately keeps Newton shape mapping and
Newton execution at zero.

This design covers only the next preflight gate:

`paper_mapped_subset_newton_shape_mapping_preflight_contract`

## Goal

Add a bounded, single-fixture offline/static preflight contract that records one explicit request
for a later Newton shape-mapping contract. The new gate should say:

- the previous runtime-admissibility row is still the only source row;
- the target mapped subset is exactly one `box`;
- the carried PrimitiveSpec-like dict has the fields a later Newton mapper would need;
- the current static target kind is declared as `box`;
- no Newton mapper, Newton runtime, real USD, benchmark, or collision-quality task has run.

Passing this preflight means only "the report has a well-formed request for a later Newton shape
mapping attempt." It is not Newton shape mapping.

## Non-Goals

- Do not import `primitive_collision_compiler.newton`.
- Do not call the Newton shape mapper.
- Do not instantiate `NewtonShapeMapping`.
- Do not construct another `PrimitiveSpec` or `CollisionPackage`.
- Do not run Newton, Warp, USD, pxr, real-USD asset loading, contact, drop/settle, sphere-rain,
  benchmark, timing, or collision-quality checks.
- Do not broaden beyond the deterministic synthetic `paper_single_box` OBB/box row.
- Do not claim package readiness, Newton readiness, Newton support, Newton execution, benchmark
  quality, collision quality, full CPD reproduction, deployment readiness, or safety
  certification.

## Design

Add a report payload named
`paper_mapped_subset_newton_shape_mapping_preflight_contract`.

The payload consumes `paper_mapped_subset_runtime_admissibility_contract` and validates:

- `gate_id == "paper_mapped_subset_runtime_admissibility_contract"`;
- `next_required_gate == "paper_mapped_subset_newton_shape_mapping_preflight_contract"`;
- exactly one runtime-admissibility row exists;
- exactly one offline/static runtime-admissibility check has passed;
- the source row explicitly has both `offline_static_runtime_admissibility_check_passed` and
  `offline_static_runtime_admissibility_checked` set to true;
- runtime execution, Newton shape mapping, Newton runtime execution, real USD, benchmark,
  collision quality, deployment, certification, approximation, and silent-drop flags are still
  false or zero;
- no copied full `generated_collision_package` dict appears in the input payload;
- the source row is still `runtime_admissibility__paper_single_box__box`;
- the source row target primitive is exactly `box`;
- the carried `candidate_primitivespec_dict` still has the expected `box` kind, `center`, `axes`,
  and `dimensions.half_extents` fields.

The new payload records one compact row in `newton_shape_mapping_preflight_rows`.

The row records:

- `newton_shape_mapping_preflight_row_id`;
- source runtime-admissibility row id;
- fixture id, paper primitive, PrimitiveSpec kind, primitive id, and carried PrimitiveSpec-like
  dict;
- target Newton shape kind label `box`;
- static schema-handoff status for that target kind, with Newton support evidence still pending;
- transfer fields for `center`, `axes`, and `dimensions.half_extents`;
- preflight checks confirming the declared target kind, center transfer, axes transfer, box
  dimension schema, and source package lineage;
- explicit booleans showing mapping was not attempted and no Newton shape mapping record was
  produced.

The top-level report advances from:

`paper_mapped_subset_newton_shape_mapping_preflight_contract_missing`

to:

`paper_mapped_subset_newton_shape_mapping_contract_missing`

The top-level report should also add the preflight gate to
`paper_faithfulness["implemented_output_contract_scope"]`, keep
`paper_faithfulness["missing_before_paper_faithful_offline"]` equal to the paper scope audit
blockers, and set `paper_faithfulness["runtime_lane_remaining_gates"]` to the later mapping
contract only.

## Data Shape

The payload should include:

- `gate_id`;
- `gate_status`;
- `closed_gate`;
- `input_gate_id`;
- `next_required_gate`;
- `decision`;
- `decision_reason`;
- `artifact_kind`;
- `schema_version`;
- `source_scope`;
- `implementation_boundary`;
- `newton_shape_mapping_preflight_action`;
- `newton_shape_mapping_preflight_contract`;
- `input_contract_summary`;
- `newton_shape_mapping_preflight_row_count`;
- `newton_shape_mapping_preflight_rows`;
- `coverage_summary`;
- `remaining_gaps`;
- static count fields for generated package, runtime-admissibility check count, preflight count,
  and zero mapping/runtime counts;
- false claim-boundary flags.

The row should include:

- `newton_shape_mapping_preflight_row_id`;
- `source_runtime_admissibility_row_id`;
- `source_package_id`;
- `source_asset_id`;
- `fixture_id`;
- `paper_primitive`;
- `primitive_spec_kind`;
- `primitive_id`;
- `candidate_primitivespec_dict`;
- `target_newton_shape_kind`;
- `target_newton_shape_kind_declared`;
- `newton_shape_support_evidence_status`;
- `target_newton_shape_kind_handoff_source`;
- `center_transfer_field`;
- `axes_transfer_field`;
- `dimensions_transfer_field`;
- `box_half_extents_transfer_field`;
- `target_kind_declared_check_passed`;
- `center_transfer_check_passed`;
- `axes_transfer_check_passed`;
- `box_dimensions_transfer_check_passed`;
- `source_runtime_admissibility_check_passed`;
- `source_package_lineage_check_passed`;
- `newton_shape_mapping_preflight_passed`;
- `mapping_attempted`;
- `newton_shape_mapping_record_created`;
- false claim-boundary flags.

## Claim Boundary

Supported wording:

> The partial `cpd_paper_offline_report` records one offline/static Newton shape-mapping
> preflight row for the synthetic `paper_single_box` OBB/box artifact. The row says the carried
> box PrimitiveSpec-like dict has the target kind and transfer fields a later Newton shape-mapping
> contract would need. No Newton mapper or Newton runtime is invoked.

Forbidden wording:

- "Newton mapped";
- "Newton-ready";
- "Newton supported";
- "Newton executed";
- "package ready";
- "benchmark-ready";
- "collision-quality validated";
- "real-USD validated";
- "full CPD reproduction";
- "safe" or "safety-certified".

## Tests

Add tests that first fail, then pass:

- the report includes `paper_mapped_subset_newton_shape_mapping_preflight_contract`;
- the top-level next gate advances to `paper_mapped_subset_newton_shape_mapping_contract`;
- the top-level failure label becomes
  `paper_mapped_subset_newton_shape_mapping_contract_missing`;
- output-contract scope includes the new preflight gate;
- runtime-lane remaining gates contain only the later mapping contract;
- paper-faithful offline blockers remain the scope-audit blockers;
- payload schema is exact;
- one preflight row is recorded;
- the row records target kind `box`, transfer fields, and false mapping/runtime flags;
- input gate drift, input next-gate drift, input count drift, row count drift, source row drift,
  PrimitiveSpec kind drift, missing half extents, copied package dicts, and forbidden true flags
  are rejected;
- source-block tests prove this preflight block does not import Newton, call the mapper, construct
  `NewtonShapeMapping`, load USD, run benchmarks, or measure collision quality;
- all existing top-level report next-gate/failure-label assertions are updated to the later
  mapping contract, while the previous runtime-admissibility payload still points to this preflight
  gate;
- CLI JSON exposes the new preflight payload and updated next gate.

## Documentation

Update the durable docs and dated record:

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
- `docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-mapping-preflight-contract.md`

The docs must keep a hard line between "one static preflight row exists" and "Newton shape
mapping happened."
