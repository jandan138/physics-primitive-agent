# CPD Paper Mapped-Subset CollisionPackage Generation Contract Design

## Context

The current CPD paper offline report ends at
`paper_mapped_subset_collision_package_generation_preflight_contract`. That gate records one
later package-generation candidate from the deterministic `paper_single_box` OBB/box
`PrimitiveSpec.to_dict()` payload, but deliberately creates zero `CollisionPackage`s and zero
runtime-admissibility checks.

The next gate is `paper_mapped_subset_collision_package_generation_contract`.

## Goal

Add a bounded, single-fixture offline contract that converts the existing preflight candidate into
exactly one report-scoped `CollisionPackage.to_dict()` artifact while keeping runtime
admissibility, Newton execution, real-USD evidence, benchmark evidence, collision-quality evidence,
deployment, and safety claims unsupported.

## Non-Goals

- Do not run Newton.
- Do not run runtime-admissibility checks.
- Do not load bed, Franka, or any other real USD asset.
- Do not broaden beyond the deterministic synthetic `paper_single_box` OBB/box row.
- Do not support paper-only primitives, approximations, fallback hulls, or multi-primitive
  packages in this gate.
- Do not claim package readiness for users, full CPD reproduction, benchmark quality, or safety.

## Options Considered

### Option A: Keep Another Dict-Only Candidate

This would advance slowly and avoid constructing a real dataclass. It is too weak for the current
next gate because the preflight already produced a dict candidate.

### Option B: Construct `CollisionPackage` Dataclass, Store Only `to_dict()`

This is the recommended path. It exercises the `CollisionPackage` serialization/schema path for
one synthetic fixture while keeping the artifact report-scoped. The gate may transiently construct
one `CollisionPackage` dataclass only to produce deterministic `to_dict()` output; the report
persists only that dict and records zero runtime-admissibility checks and zero Newton execution.

### Option C: Construct Package And Immediately Run Newton Canary

This is out of scope. Newton canary requires a separate runtime-admissibility boundary so the
report does not silently equate "package object exists" with "runtime checked."

## Design

Add a new report payload named `paper_mapped_subset_collision_package_generation_contract`.

The payload will consume `paper_mapped_subset_collision_package_generation_preflight_contract`,
validate that:

- the input gate id and next gate match exactly;
- exactly one preflight row exists;
- the preflight row is for `paper_single_box`, `oriented_bounding_box`, and runtime kind `box`;
- the previous preflight payload matches a recomputed deterministic upstream preflight anchor for
  gate id, next gate, counts, persisted lineage, constructed primitive dict, generated primitive
  dict, and candidate `PrimitiveSpec.to_dict()`;
- the preflight candidate `PrimitiveSpec.to_dict()` matches the anchored preflight source row;
- the preflight row has `later_collision_package_generation_candidate: true`;
- package generation was disallowed in the previous gate;
- no runtime-admissibility, Newton, real-USD, benchmark, or collision-quality triggers are present.

The new gate will reconstruct exactly one `PrimitiveSpec` from the candidate dict, then construct
exactly one `CollisionPackage` from that primitive. Before construction, the candidate dict must
pass the existing strict primitive-shape validator; after construction,
`PrimitiveSpec.to_dict()` must exactly equal the candidate dict. The report stores one package dict
only at `collision_package_generation_rows[0]["generated_collision_package"]`; payload-level and
coverage-level fields store counts and row ids, not a second copy of the package.

The generated package will use deterministic metadata:

- `asset_id`: `paper_single_box`
- `package_id`: `paper_single_box:paper_mapped_subset_collision_package_generation_contract`
- `source_path`: `synthetic://cpd-paper/paper_single_box`
- `source_sha256`: SHA-256 of the canonical synthetic source manifest below, not a real asset
  digest
- `method`: `cpd_paper_mapped_subset_offline`
- `stage`: `paper_mapped_subset_collision_package_generation_contract`
- `status`: `offline_synthetic_candidate_not_runtime_admissible`
- `claim_boundary`: `single_fixture_box_only_offline_collision_package_artifact_not_paper_vocabulary_runtime_admissibility_or_newton`
- `mesh_point_count`: `8`
- `mesh_face_count`: `12`
- `max_source_faces`: `12`
- `primitive_subset`: `["box"]`
- `unsupported_primitives`: `[]`, meaning no unsupported primitive appears in this one
  `paper_single_box` box fixture; this is not paper-vocabulary coverage
- `fallback`: `None`

The deterministic source manifest is serialized with
`json.dumps(manifest, allow_nan=False, sort_keys=True, separators=(",", ":"))`:

```json
{
  "contract_gate": "paper_mapped_subset_collision_package_generation_contract",
  "fixture_id": "paper_single_box",
  "fixture_scope": "synthetic_toy_mesh",
  "mesh_face_count": 12,
  "mesh_point_count": 8,
  "primitive_id": "paper_single_box__oriented_bounding_box__box",
  "primitive_kind": "box",
  "source_faces": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
}
```

The payload will set:

- `generated_collision_package_count: 1`
- `runtime_admissibility_check_count: 0`
- `collision_package_generated: true`
- `package_generation_allowed: true`
- `collision_package_generation_allowed: true`
- `package_generation_triggered: true`
- `collision_package_generation_triggered: true`
- `runtime_admissibility_checked: false`
- `runtime_admissibility_triggered: false`
- `runtime_admissibility_supported: false`
- `newton_runtime_triggered: false`
- `newton_support_claimed: false`
- `newton_runtime_allowed: false`
- `real_usd_triggered: false`
- `real_usd_loaded: false`
- `benchmark_triggered: false`
- `benchmark_run: false`
- `collision_quality_measured: false`
- `deployment_or_certification_claimed: false`
- `approximation_policy_applied: false`
- `approximation_policy_enabled: false`
- `silent_drop_allowed: false`
- `paper_faithful_offline_supported: false`

The row will also include:

- `unsupported_primitives_in_this_single_fixture: []`
- `primitive_families_not_evaluated_by_this_gate: ["sphere", "capsule", "capped_cylinder",
  "frustum", "trapezoidal_prism"]`

The top-level report will advance from
`paper_mapped_subset_collision_package_generation_contract_missing` to the next gate:

`paper_mapped_subset_runtime_admissibility_preflight_contract`

## Claim Boundary

This gate supports only:

- one synthetic, report-scoped `CollisionPackage.to_dict()` artifact stored once in the
  collision-package generation row;
- one `box` primitive constructed from the existing deterministic `PrimitiveSpec.to_dict()` row;
- deterministic package metadata and lineage accounting.

This gate does not support:

- runtime admissibility;
- Newton execution or Newton support;
- real-USD behavior;
- benchmark behavior;
- collision-quality evidence;
- package readiness for users;
- full CPD reproduction;
- paper primitive vocabulary coverage;
- deployment readiness or safety certification.

Add the following allowed-claim wording to `docs/reference/claim-boundaries.md` before broader docs
use it:

> The partial `cpd_paper_offline_report` can construct exactly one synthetic, report-scoped
> `CollisionPackage` dataclass for `paper_single_box` OBB/box and persist only
> `CollisionPackage.to_dict()` after lineage checks. This is offline serialization/contract
> accounting, not package readiness, runtime admissibility, Newton support, real-USD evidence,
> benchmark evidence, collision-quality validation, full CPD reproduction, deployment readiness,
> safety certification, or paper primitive vocabulary coverage.

## Tests

Add tests that first fail, then pass:

- report-level next gate changes to `paper_mapped_subset_runtime_admissibility_preflight_contract`;
- the package-generation payload has exact schema and counts;
- exactly one recursively discovered package-shaped dict exists in the entire payload, at
  `collision_package_generation_rows[0]["generated_collision_package"]`;
- package-generation flags are true only for this gate, while runtime-admissibility, Newton,
  real-USD, benchmark, collision-quality, deployment, approximation, and silent-drop flags remain
  false;
- source manifest canonical JSON and SHA-256 are exact;
- the nested primitive equals the preflight candidate dict;
- `PrimitiveSpec.to_dict()` round-trips exactly before package construction;
- malformed input gate, row count, candidate flag, package generation boundary, lineage drift,
  package dict drift, and forbidden runtime/Newton triggers are rejected;
- static and payload checks prevent Newton, real-USD, benchmark, and collision-quality leakage.

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

The docs must distinguish "one synthetic report-scoped package artifact exists" from package
readiness, runtime admissibility, Newton execution, real-USD evidence, benchmark evidence, and
collision-quality evidence.
