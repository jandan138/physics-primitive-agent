# CPD Paper Mapped-Subset Newton Shape Runtime Engine-Builder API-Surface Contract Design

## Goal

Close the next tiny CPD paper runtime-lane gate:
`paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract`.

This is a bounded offline/source-inspection slice. It consumes the single-fixture
environment-probe row for `paper_single_box` and records whether the later Newton boundary appears
to expose the expected source-level API surface for `newton.ModelBuilder` and `add_shape_box`.

## Boundary

Allowed:

- carry forward the exact lineage from the environment-probe row;
- record one API-surface row for the synthetic `paper_single_box` mapped-subset `box`;
- in the default no-config report, record `not_run_source_dir_not_configured`;
- when a Newton source directory is explicitly passed, read source files and parse them with
  Python `ast`;
- record JSON-safe source facts such as exported names, class/method presence, parameter names,
  and source file paths.

Forbidden:

- importing `newton` or `warp`;
- calling `inspect_newton_environment()`;
- instantiating `newton.ModelBuilder`;
- calling `add_shape_box`;
- creating Newton shape objects;
- finalizing a model;
- creating or colliding a Newton collision pipeline;
- running contact, drop/settle, or sphere-rain diagnostics;
- loading real USD assets;
- benchmarking or measuring collision quality;
- claiming Newton support, runtime compatibility, simulation-checking, deployment readiness, safety
  certification, or full CPD paper reproduction.

## Design

Add a helper in `src/primitive_collision_compiler/newton/env.py`:
`inspect_newton_engine_builder_api_surface(source_dir=None)`.

The helper returns JSON-safe data only:

- `probe_mode: source_ast_api_surface_only_no_import`;
- source-dir configured/found/missing status;
- checked source files;
- `ModelBuilder` export/class status;
- `ModelBuilder.__init__` parameter names;
- `ModelBuilder.add_shape_box` parameter names;
- `ModelBuilder.finalize` presence;
- `CollisionPipeline` export status;
- all import, builder, shape, finalize, collision, runtime, USD, benchmark, and quality counters at
  zero.

The offline report adds:

- one payload:
  `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract`;
- one row:
  `newton_shape_runtime_engine_builder_api_surface__paper_single_box__box`;
- exact input validation for the environment-probe payload and row;
- exact schema tests and drift tests;
- static boundary tests that forbid runtime imports, builder construction, shape calls, finalize,
  collide, USD, benchmark, and quality code.

Closing this gate advances the next runtime-lane gate to
`paper_mapped_subset_newton_shape_runtime_engine_builder_import_boundary_preflight_contract`.
That next gate is only a future decision/preflight gate; this slice still does not import Newton.

## Tests

Use TDD:

1. Add helper tests for no-config, missing-source, and fake-source AST cases.
2. Add report payload/row exact schema tests.
3. Add source-row drift tests for lineage IDs, kind fields, source status, module provenance, and
   runtime counters.
4. Add false/true flag drift tests.
5. Add CLI JSON expectations.
6. Run focused RED before implementation, then focused GREEN, then docs validators and the full
   repository suite before merge.

## Documentation

Update:

- `README.md`;
- `docs/index.md`;
- `docs/deepdive/evidence-status.md`;
- `docs/deepdive/message-map.md`;
- `docs/reference/claim-boundaries.md`;
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`;
- `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`;
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`;
- `docs/reference/cpd-paper-story-status.md`;
- `docs/records/README.md`;
- a new dated implementation record.

The docs must describe API-surface inspection as source-level evidence only, not Newton readiness
or runtime compatibility.
