# CPD Paper Package Adapter Contract Design

## Purpose

Close `paper_package_adapter_contract` by adding a command-only offline adapter-contract payload
to `cpd_paper_offline_report`.

This contract classifies the primitive records emitted by
`paper_offline_changed_decomposition_output_contract` as future adapter inputs. It is not a
`CollisionPackage`, does not call package builders, does not import or instantiate package/runtime
types, does not map Newton shapes, does not load real USD assets, and does not run benchmarks.

## Current Context

The changed-decomposition output contract currently emits:

- 9 decomposition output rows;
- 16 offline primitive records;
- 3 explicit postprocess state rows;
- false package/Newton/real-USD/benchmark triggers;
- `next_required_gate: paper_package_adapter_contract`.

The 16 current primitive records all resolve to:

```text
paper_primitive: trapezoidal_prism
newton_runtime_kind: offline_only_unmapped
conversion_status: offline_contract_only_not_package_candidate
```

That means this slice should not claim any direct adapter eligibility. The correct first adapter
contract result is a partition table where all current primitive records require later policy.

## Selected Approach

Add a top-level payload:

```text
paper_package_adapter_contract
```

The payload should:

- consume the existing changed-decomposition output contract inside the same report;
- summarize the input row and primitive-record counts;
- emit one adapter decision row per offline primitive record;
- classify records as `adapter_eligible`, `blocked`, or `later_policy_required`;
- keep current records at `later_policy_required` because they are unmapped
  `trapezoidal_prism` records;
- advance the next gate to `paper_package_adapter_unsupported_primitive_policy`;
- preserve all false package/Newton/real-USD/benchmark triggers.

The next gate intentionally avoids `paper_package_generation_contract`. The unresolved hard issue
is unsupported paper primitive disposition, especially paper-only primitives that do not have a
direct Newton primitive mapping. Naming the next gate as an unsupported-primitive policy keeps the
work offline and avoids implying package readiness.

## Report Contract

The new top-level payload must include:

- `gate_id: paper_package_adapter_contract`
- `gate_status: implemented_offline_adapter_contract_only_partial`
- `closed_gate: paper_package_adapter_contract`
- `input_gate_id: paper_offline_changed_decomposition_output_contract`
- `next_required_gate: paper_package_adapter_unsupported_primitive_policy`
- `decision: remain_partial`
- `decision_reason: package_adapter_contract_complete_unsupported_primitive_policy_missing`
- `paper_faithful_offline_allowed: false`
- `package_generation_allowed: false`
- `artifact_kind: offline_package_adapter_contract_not_collision_package`
- `schema_version: 1`
- `source_scope: synthetic_toy_fixtures_only`
- `implementation_boundary: offline_adapter_contract_no_collision_package_no_newton`
- `input_contract_summary`
- `adapter_decision_contract`
- `primitive_adapter_decision_rows`
- `coverage_summary`
- `remaining_gaps`
- false triggers for package generation, Newton runtime, real USD, and benchmarks.

After this slice, the report itself must remain:

```text
status: partial
paper_faithful_offline_supported: false
next_required_gate: paper_package_adapter_unsupported_primitive_policy
failure_labels: ["paper_package_adapter_unsupported_primitive_policy_missing"]
```

## Adapter Decision Rules

Each primitive record from the changed-decomposition output contract maps to one adapter decision
row.

`adapter_eligible` means:

- required fields are present;
- numeric fields are finite;
- `contains_assigned_points` is true;
- all forbidden triggers are false;
- the primitive family has an explicit direct adapter policy.

`later_policy_required` means:

- the record is structurally complete;
- the primitive family or postprocess state still needs an explicit policy before any adapter or
  package generation can be attempted.

`blocked` means:

- required fields are missing;
- numeric fields are invalid or non-finite;
- containment is false;
- source-face mapping is missing;
- duplicate adapter ids are detected;
- any forbidden trigger is true.

The current changed-decomposition records are structurally complete but all use
`offline_only_unmapped` `trapezoidal_prism`, so the expected partition is:

```text
adapter_eligible_record_count: 0
blocked_record_count: 0
later_policy_required_record_count: 16
offline_only_unmapped_record_count: 16
```

## Adapter Decision Rows

Each row should contain:

- `adapter_decision_id`
- `source_output_id`
- `evidence_case_id`
- `offline_primitive_id`
- `paper_primitive`
- `offline_runtime_kind_label`
- `record_field_status`
- `postprocess_state`
- `adapter_decision`
- `adapter_decision_reason`
- `required_later_gate`
- `package_generation_triggered: false`
- `newton_runtime_triggered: false`
- `real_usd_triggered: false`
- `benchmark_triggered: false`

The current `trapezoidal_prism` rows should use:

```text
adapter_decision: later_policy_required
adapter_decision_reason: unsupported_paper_primitive_requires_adapter_policy
required_later_gate: paper_package_adapter_unsupported_primitive_policy
```

## Invariants

Tests must assert:

- the new payload exists and closes only `paper_package_adapter_contract`;
- top-level `next_required_gate` moves to
  `paper_package_adapter_unsupported_primitive_policy`;
- top-level failure labels remove `paper_package_adapter_contract_missing`;
- `paper_faithfulness.implemented_output_contract_scope` now contains both
  `paper_offline_changed_decomposition_output_contract` and `paper_package_adapter_contract`;
- report status remains partial and `paper_faithful_offline_supported` remains false;
- adapter decision rows match the changed-decomposition primitive record count;
- decision counts partition the primitive record count exactly;
- current counts are 0 eligible, 0 blocked, 16 later-policy-required;
- all rows preserve false package/Newton/real-USD/benchmark triggers;
- no `CollisionPackage`, `PrimitiveSpec`, runtime result, real USD path, benchmark, timing,
  surface-distance, or collision-quality output is introduced.

## Claim Boundaries

This slice supports only:

```text
command-only offline package-adapter contract over deterministic synthetic fixture records
```

It does not support claims of:

- `CollisionPackage` generation;
- package readiness;
- Newton readiness;
- runtime readiness;
- runtime admissibility;
- `paper_faithful_offline` support;
- full CPD paper reproduction;
- direct support for paper-only primitives;
- real-USD evidence;
- benchmark or collision-quality evidence;
- deployment readiness or safety certification.

## Documentation Updates

Update current status and boundary docs:

- `README.md`
- `docs/index.md`
- `docs/deepdive/evidence-status.md`
- `docs/reference/claim-boundaries.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/records/README.md`
- `experiments/registry.yaml`
- `docs/records/2026-05-17-cpd-paper-package-adapter-contract.md`

## Self-Review

- No placeholder sections remain.
- The design keeps package generation and Newton runtime out of scope.
- The next gate is `paper_package_adapter_unsupported_primitive_policy`, not a package-generation
  claim.
- The report remains partial and keeps `paper_faithful_offline_supported: false`.
