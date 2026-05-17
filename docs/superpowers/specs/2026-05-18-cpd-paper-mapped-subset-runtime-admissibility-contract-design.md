# CPD Paper Mapped-Subset Runtime-Admissibility Contract Design

## Context

The current CPD paper offline report ends at
`paper_mapped_subset_runtime_admissibility_preflight_contract`. That preflight gate consumes the
single synthetic `paper_single_box` `CollisionPackage.to_dict()` artifact produced by
`paper_mapped_subset_collision_package_generation_contract`, records one later
runtime-admissibility candidate row, and deliberately keeps `runtime_admissibility_check_count: 0`.

The next gate is `paper_mapped_subset_runtime_admissibility_contract`.

## Goal

Add a bounded, single-fixture offline/static runtime-admissibility contract for the existing
report-scoped `paper_single_box` package artifact. This gate should verify that the one carried
box primitive is structurally admissible for a later Newton shape-mapping preflight:

- finite center;
- right-handed orthonormal axes;
- positive finite box half extents;
- expected Newton-target dimension schema for mapped `box`;
- exact one-row, one-package, one-primitive lineage from the previous gate.

Passing this gate means only that one synthetic package artifact passed report-scoped offline
runtime-admissibility checks. It does not make the package Newton-ready and does not run Newton.

## Non-Goals

- Do not run Newton.
- Do not call `map_package_shapes`.
- Do not import Newton, Warp, USD, pxr, or real-USD asset helpers.
- Do not load bed, Franka, or any other real USD asset.
- Do not run contact, drop/settle, sphere-rain, benchmark, timing, or collision-quality tasks.
- Do not generate another `CollisionPackage`.
- Do not copy the full generated package dict into the new runtime-admissibility payload.
- Do not broaden beyond the deterministic synthetic `paper_single_box` OBB/box package.
- Do not claim package readiness, Newton support, Newton execution, benchmark quality, collision
  quality, full CPD reproduction, deployment readiness, or safety certification.

## Design

Add a new report payload named `paper_mapped_subset_runtime_admissibility_contract`.

The payload consumes `paper_mapped_subset_runtime_admissibility_preflight_contract` and validates
that:

- the input gate id is exactly `paper_mapped_subset_runtime_admissibility_preflight_contract`;
- the input next gate is exactly `paper_mapped_subset_runtime_admissibility_contract`;
- exactly one runtime-admissibility preflight row exists;
- the preflight row is for fixture `paper_single_box`;
- the paper primitive is `oriented_bounding_box`;
- the PrimitiveSpec/Newton candidate kind is `box`;
- the source package id, asset id, source path, source SHA-256, method, stage, status, primitive
  subset, unsupported primitive list, and claim boundary still match the canonical generated
  package values;
- no copied `generated_collision_package` dict is present in the preflight payload;
- runtime-admissibility, Newton, real-USD, benchmark, collision-quality, deployment,
  approximation, and silent-drop triggers are still false.

The payload then performs one offline/static check against the carried `candidate_primitivespec_dict`:

- schema has exactly the expected PrimitiveSpec-like keys;
- `kind == "box"`;
- `primitive_id == "paper_single_box__oriented_bounding_box__box"`;
- `frame == "asset"`;
- `conversion_status == "runtime_primitivespec_constructed_from_canonical_preflight_payload"`;
- `center` is a length-3 finite numeric list;
- `axes` is a 3x3 finite numeric list;
- each axis has unit length within tolerance;
- axes are pairwise orthogonal within tolerance;
- the axis frame is right-handed, meaning `cross(axis0, axis1)` points along `axis2`;
- `dimensions == {"half_extents": [hx, hy, hz]}`;
- all three half extents are finite and strictly positive;
- `source_faces == list(range(12))`;
- `contains_assigned_points is True`;
- `volume` and `weighted_volume` are finite and strictly positive;
- `volume == 8 * hx * hy * hz` within tolerance;
- `weighted_volume == volume` for this box fixture.

The new payload records a compact `runtime_admissibility_rows` list with exactly one row. The row
stores lineage fields, source package identity fields, static check booleans, and the carried
`candidate_primitivespec_dict`, but it does not store the full source `CollisionPackage.to_dict()`.

The payload will set:

- `runtime_admissibility_row_count: 1`;
- `offline_static_runtime_admissibility_check_count: 1`;
- `offline_static_runtime_admissibility_checked: true`;
- `runtime_admissibility_check_count: 1`;
- `runtime_execution_count: 0`;
- `newton_mapping_record_count: 0`;
- `newton_runtime_execution_count: 0`;
- `generated_collision_package_count: 1`;
- `source_collision_package_available: true`;
- `paper_faithful_offline_allowed: false`;
- `paper_faithful_offline_supported: false`;
- all Newton, USD, benchmark, collision-quality, deployment, certification, approximation, and
  silent-drop flags false.

The top-level report will advance from:

`paper_mapped_subset_runtime_admissibility_contract_missing`

to:

`paper_mapped_subset_newton_shape_mapping_preflight_contract_missing`

The next required gate will be `paper_mapped_subset_newton_shape_mapping_preflight_contract`.
That Newton-lane next gate must not be recorded as the only remaining gap before
`paper_faithful_offline`. The report must keep paper-faithful offline blockers separate from
runtime/Newton-lane gates, for example by preserving the scope-audit blocking criteria as the
paper-faithful offline blocker list and recording the Newton shape-mapping preflight only as the
runtime-lane next gate.

## Claim Boundary

This gate supports only:

- one offline/static runtime-admissibility check for one deterministic synthetic
  `paper_single_box` `CollisionPackage.to_dict()` artifact;
- finite-center, orthonormal/right-handed-axis, positive-dimension, and box-schema accounting for
  that one carried primitive;
- explicit accounting that Newton mapping, Newton runtime execution, real-USD loading, benchmark
  runs, collision-quality measurement, deployment, and certification did not happen.

This gate does not support:

- general package readiness;
- Newton readiness;
- Newton support or Newton execution;
- real-USD evidence;
- benchmark evidence;
- collision-quality validation;
- paper primitive vocabulary coverage;
- approximation support;
- `paper_faithful_offline` support;
- full CPD reproduction;
- deployment readiness or safety certification.

Add allowed wording to `docs/reference/claim-boundaries.md` before broader docs use it:

> The partial `cpd_paper_offline_report` can record exactly one offline/static
> runtime-admissibility check for the synthetic `paper_single_box` OBB/box
> `CollisionPackage.to_dict()` artifact. This means the single carried box primitive passed
> finite-center, right-handed orthonormal-axis, positive-half-extent, and box dimension-schema
> checks for a later Newton shape-mapping preflight. It is not package readiness, Newton
> readiness, Newton support, Newton execution, real-USD evidence, benchmark evidence,
> collision-quality validation, full CPD reproduction, deployment readiness, safety
> certification, or paper primitive vocabulary coverage.

## Tests

Add tests that first fail, then pass:

- report-level next gate advances to
  `paper_mapped_subset_newton_shape_mapping_preflight_contract`;
- top-level failure label becomes
  `paper_mapped_subset_newton_shape_mapping_preflight_contract_missing`;
- the new payload has exact schema, exact counts, and one runtime-admissibility row;
- the row records lineage, package identity, carried `candidate_primitivespec_dict`, static check
  booleans, and final status;
- the payload does not duplicate the full generated package dict;
- input gate drift, input next-gate drift, row count drift, source identity drift, package identity
  drift, package claim-boundary drift, and package-copy drift are rejected;
- primitive-spec drift is rejected for bad kind, non-finite center, malformed axes,
  non-orthonormal axes, left-handed axes, missing/negative half extents, bad source faces,
  `contains_assigned_points: false`, bad volume, bad weighted volume, and bad conversion status;
- runtime-admissibility is counted as one offline/static check, while runtime execution, Newton
  mapping, Newton runtime, real-USD, benchmark, and collision-quality counts stay zero or false;
- static source checks prevent Newton, USD, benchmark, timing, collision-quality, and
  shape-mapping calls in the runtime-admissibility contract block;
- CLI JSON includes the new payload and updated next gate.

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
- a new dated record for this gate

The docs must distinguish "one synthetic package passed offline/static runtime-admissibility
checks" from Newton shape mapping, Newton execution, real-USD behavior, benchmark quality, or
general package readiness.
