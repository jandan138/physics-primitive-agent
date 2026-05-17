# 2026-05-17 CPD Paper Mapped-Subset CollisionPackage Generation Contract

## Date

2026-05-17

## Status

Complete.

## Context

The previous gate,
`paper_mapped_subset_collision_package_generation_preflight_contract`, recorded exactly one later
package-generation candidate for the deterministic synthetic `paper_single_box` OBB/box row. That
preflight consumed the runtime `PrimitiveSpec.to_dict()` payload from
`paper_mapped_subset_primitivespec_runtime_construction_contract`, but deliberately created zero
CollisionPackages and zero runtime-admissibility checks.

That previous gate pointed next to:

`paper_mapped_subset_collision_package_generation_contract`

This record covers only that next single-fixture offline package-generation contract.

## What Changed

The partial `cpd_paper_offline_report` now includes
`paper_mapped_subset_collision_package_generation_contract`.

The new payload:

- consumes `paper_mapped_subset_collision_package_generation_preflight_contract`;
- validates the input gate id, expected next gate, one preflight row, candidate lineage, carried
  `PrimitiveSpec.to_dict()` equality, and false boundary flags;
- reconstructs one runtime `PrimitiveSpec` object only as the source primitive for a report-scoped
  package artifact;
- constructs exactly one synthetic `CollisionPackage.to_dict()` artifact for
  `paper_single_box`;
- records package metadata with `asset_id: paper_single_box`,
  `package_id: paper_single_box:paper_mapped_subset_collision_package_generation_contract`,
  `method: cpd_paper_mapped_subset_offline`, and
  `status: offline_synthetic_candidate_runtime_admissibility_not_checked`;
- records `primitive_subset: ["box"]`;
- records `unsupported_primitives: []` only for this one box fixture, not for the full paper
  primitive vocabulary;
- records `primitive_families_not_evaluated_by_this_gate` for `sphere`, `capsule`,
  `capped_cylinder`, `frustum`, and `trapezoidal_prism`;
- records `generated_collision_package_count: 1`;
- records `runtime_admissibility_check_count: 0`;
- advances the next gate to `paper_mapped_subset_runtime_admissibility_preflight_contract`.

The generated package is intentionally a serialized offline candidate. It is not fed to Newton, it
has not passed runtime admissibility, and it is not evidence for real-USD behavior, benchmark
behavior, collision quality, paper primitive vocabulary coverage, or full CPD paper reproduction.

## Verification

Commands run during this branch:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'collision_package_generation_contract or collision_package_generation_preflight or runtime_construction' -q
# exit 0; 225 passed, 307 deselected

PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
# exit 0; 3 passed, 109 deselected

python -m py_compile src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cpd_paper_offline.py tests/test_cli.py
# exit 0

git diff --check
# exit 0
```

The focused RED run before implementation failed as expected because the report lacked the new
contract payload, runtime-admissibility next gate, generated package count, and static boundary
sentinel coverage.

Final branch verification was rerun after the documentation updates and is recorded in the commit
summary for this change.

## Artifacts

- Report key: `paper_mapped_subset_collision_package_generation_contract`
- Previous report gate: `paper_mapped_subset_collision_package_generation_preflight_contract`
- Next report gate: `paper_mapped_subset_runtime_admissibility_preflight_contract`
- Implementation plan:
  `docs/superpowers/plans/2026-05-17-cpd-paper-mapped-subset-collision-package-generation-contract.md`
- Design spec:
  `docs/superpowers/specs/2026-05-17-cpd-paper-mapped-subset-collision-package-generation-contract-design.md`

## Claim Boundary

Supported:

- partial single-fixture offline CollisionPackage generation accounting for one deterministic
  synthetic fixture;
- exactly one report-scoped `CollisionPackage.to_dict()` artifact for `paper_single_box`;
- explicit accounting that runtime-admissibility checks, Newton runtime, real-USD loading,
  benchmark runs, collision-quality measurement, deployment, and certification triggers remain
  zero or false;
- explicit accounting that `unsupported_primitives: []` is scoped only to the one generated box
  fixture, while other paper primitive families are not evaluated by this gate.

Not supported:

- package readiness;
- runtime admissibility;
- Newton support or Newton execution;
- real-USD evidence;
- benchmark evidence;
- collision-quality evidence;
- paper primitive vocabulary coverage;
- `paper_faithful_offline` support;
- full CPD reproduction;
- deployment readiness or safety certification.

## Claim Impact

This record supports only a partial, single-fixture offline package-artifact claim for one
deterministic synthetic `paper_single_box` OBB/box fixture. It moves the CPD paper lane from
"preflight says a package could be generated" to "one bounded package dict exists for review".
It does not make that package runtime-admissible and does not add Newton evidence.

## Next Gate

`paper_mapped_subset_runtime_admissibility_preflight_contract`

That next gate must decide what a report-scoped package artifact must prove before any runtime
admissibility or Newton-related checks are claimed.

## Next Action

- Implement `paper_mapped_subset_runtime_admissibility_preflight_contract` under a separate dated
  record before claiming runtime admissibility, Newton runtime support, or broader package
  readiness.
