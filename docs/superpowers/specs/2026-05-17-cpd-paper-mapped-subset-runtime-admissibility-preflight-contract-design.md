# CPD Paper Mapped-Subset Runtime-Admissibility Preflight Contract Design

## Context

The current CPD paper offline report ends at
`paper_mapped_subset_collision_package_generation_contract`. That gate constructs exactly one
synthetic, report-scoped `CollisionPackage.to_dict()` artifact for the deterministic
`paper_single_box` OBB/box fixture. The package status is
`offline_synthetic_candidate_runtime_admissibility_not_checked`, and the report deliberately
records `runtime_admissibility_check_count: 0`.

The next gate is `paper_mapped_subset_runtime_admissibility_preflight_contract`.

## Goal

Add a bounded, single-fixture offline preflight contract that consumes the generated
`CollisionPackage.to_dict()` artifact and records exactly one later runtime-admissibility
candidate row. This gate defines what must be checked before a later runtime-admissibility gate can
claim anything, but it does not run that check and does not run Newton.

## Non-Goals

- Do not run Newton.
- Do not call any runtime-admissibility checker.
- Do not import Newton, Warp, USD, pxr, or real-USD asset helpers.
- Do not load bed, Franka, or any other real USD asset.
- Do not generate another `CollisionPackage`.
- Do not duplicate the full generated package dict inside the new preflight payload.
- Do not broaden beyond the deterministic synthetic `paper_single_box` OBB/box package.
- Do not claim Newton support, package readiness, benchmark quality, collision quality, full CPD
  reproduction, deployment readiness, or safety certification.

## Design

Add a new report payload named
`paper_mapped_subset_runtime_admissibility_preflight_contract`.

The payload will consume `paper_mapped_subset_collision_package_generation_contract` and validate
that:

- the input gate id is exactly `paper_mapped_subset_collision_package_generation_contract`;
- the input next gate is exactly `paper_mapped_subset_runtime_admissibility_preflight_contract`;
- exactly one collision-package generation row exists;
- exactly one generated package dict exists in the input gate;
- the input gate does not contain a second package-shaped dict anywhere else in the payload;
- the generated package dict has the exact `CollisionPackage.to_dict()` key set;
- the package is for `paper_single_box`, package id
  `paper_single_box:paper_mapped_subset_collision_package_generation_contract`, source path
  `synthetic://cpd-paper/paper_single_box`, stage
  `paper_mapped_subset_collision_package_generation_contract`, method
  `cpd_paper_mapped_subset_offline`, and status
  `offline_synthetic_candidate_runtime_admissibility_not_checked`;
- the package contains exactly one primitive and that primitive equals the carried
  `candidate_primitivespec_dict`;
- the package claim boundary still contains
  `not_paper_vocabulary_runtime_admissibility_or_newton`;
- the source manifest SHA is still anchored to the previous synthetic manifest;
- the previous package-generation gate has `generated_collision_package_count: 1` and
  `runtime_admissibility_check_count: 0`;
- runtime-admissibility, Newton, real-USD, benchmark, collision-quality, deployment,
  approximation, and silent-drop triggers are still false.

The new payload will not copy the full package dict. Instead, it will record a compact
`runtime_admissibility_preflight_rows` entry with package identity and lineage fields:

- `runtime_admissibility_preflight_row_id`
- `source_collision_package_generation_row_id`
- `source_package_id`
- `source_asset_id`
- `source_package_stage`
- `source_package_status`
- `source_package_method`
- `source_package_source_path`
- `source_package_source_sha256`
- `source_package_claim_boundary`
- `source_package_primitive_count`
- `source_package_primitive_subset`
- `source_package_unsupported_primitives`
- `fixture_id`
- `primitive_spec_kind`
- `paper_primitive`
- `newton_runtime_kind`
- `candidate_primitivespec_dict`
- `later_runtime_admissibility_candidate`
- `runtime_admissibility_preflight_decision`
- `required_later_gate`
- boundary flags

The payload will set:

- `runtime_admissibility_preflight_row_count: 1`
- `later_runtime_admissibility_candidate_count: 1`
- `generated_collision_package_count: 1`
- `runtime_admissibility_check_count: 0`
- `source_collision_package_available: true`
- `paper_faithful_offline_allowed: false`
- `paper_faithful_offline_supported: false`
- `runtime_admissibility_checked: false`
- `runtime_admissibility_triggered: false`
- `runtime_admissibility_supported: false`
- `newton_runtime_allowed: false`
- `newton_runtime_triggered: false`
- `newton_support_claimed: false`
- `real_usd_loaded: false`
- `real_usd_triggered: false`
- `benchmark_run: false`
- `benchmark_triggered: false`
- `collision_quality_measured: false`
- `deployment_or_certification_claimed: false`
- `approximation_policy_applied: false`
- `approximation_policy_enabled: false`
- `silent_drop_allowed: false`

The top-level report will advance from
`paper_mapped_subset_runtime_admissibility_preflight_contract_missing` to:

`paper_mapped_subset_runtime_admissibility_contract`

That later gate may decide how to perform the actual runtime-admissibility check. This design does
not specify or run that future check.

## Claim Boundary

This gate supports only:

- one offline preflight row for the existing synthetic `paper_single_box` package artifact;
- strict lineage and package-shape checks before a later runtime-admissibility gate;
- explicit accounting that no runtime-admissibility check, Newton runtime, real-USD loading,
  benchmark run, collision-quality measurement, deployment, or certification happened.

This gate does not support:

- runtime admissibility;
- Newton support or Newton execution;
- real-USD behavior;
- benchmark behavior;
- collision-quality evidence;
- user package readiness;
- full CPD reproduction;
- paper primitive vocabulary coverage;
- deployment readiness or safety certification.

Add allowed wording to `docs/reference/claim-boundaries.md` before broader docs use it:

> The partial `cpd_paper_offline_report` can record exactly one synthetic
> `paper_single_box` runtime-admissibility preflight candidate from an existing report-scoped
> `CollisionPackage.to_dict()` artifact. This is offline lineage and preflight accounting, not
> package readiness, runtime admissibility, Newton support, Newton execution, real-USD evidence,
> benchmark evidence, collision-quality validation, full CPD reproduction, deployment readiness,
> safety certification, or paper primitive vocabulary coverage.

## Tests

Add tests that first fail, then pass:

- report-level next gate advances to `paper_mapped_subset_runtime_admissibility_contract`;
- the new payload has exact schema, exact counts, and one preflight row;
- the payload does not duplicate the full generated package dict;
- the preflight row records package id, asset id, stage, status, source SHA, primitive subset, and
  candidate primitive dict;
- package-shape, package status, package stage, source SHA, primitive equality, row count, and
  input gate drift are rejected;
- runtime-admissibility, Newton, real-USD, benchmark, collision-quality, deployment,
  approximation, and silent-drop flags remain false;
- static source checks prevent Newton, USD, benchmark, and collision-quality imports or calls in
  the runtime-admissibility preflight block;
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

The docs must distinguish "one runtime-admissibility preflight candidate exists" from runtime
admissibility itself.
