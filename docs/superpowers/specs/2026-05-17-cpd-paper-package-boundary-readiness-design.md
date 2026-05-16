# CPD Paper Package Boundary Readiness Design

## Purpose

Close `paper_generalization_batch_e_package_boundary_readiness` by adding a command-only,
offline report-only readiness matrix inside the partial `cpd_paper_offline_report`.

This slice reviews whether the paper-lane generalization work from Batches A-D has an explicit
boundary before any later package conversion work begins. It does not generate a
`CollisionPackage`, map paper primitives to Newton, call Newton, load real USD assets, run
benchmarks, or claim `paper_faithful_offline` support.

## Current Context

The report currently closes these offline generalization gates:

- `paper_generalization_batch_a_source_policy`
- `paper_generalization_batch_b_primitive_fit_engine`
- `paper_generalization_batch_c_search_engine`
- `paper_generalization_batch_d_postprocess_policy`

The current top-level report still marks
`paper_generalization_batch_e_package_boundary_readiness` as missing. Batch E is the final planned
generalization review gate, but it is not the package generation gate itself. Its job is to make
the next blockers explicit:

- no stable changed-decomposition output contract exists yet;
- no package-generation contract exists yet;
- Newton runtime admissibility has not been checked for the paper-lane output;
- real USD and benchmark work remain later gates.

## Selected Approach

Add a top-level payload:

```text
paper_generalization_batch_e_package_boundary_readiness
```

The payload should contain a small boundary matrix, not geometry rows. Each row summarizes a
package-adjacent boundary and records whether package, Newton, real-USD, or benchmark execution
was triggered. Every trigger must remain false.

This is safer than moving directly to package generation because the current report still contains
offline audit matrices and toy fixtures, not a durable package-ready decomposition artifact.

## Report Contract

The new top-level payload must include:

- `gate_id: paper_generalization_batch_e_package_boundary_readiness`
- `gate_status: implemented_planning_only_partial`
- `closed_gate: paper_generalization_batch_e_package_boundary_readiness`
- `next_required_gate: paper_offline_changed_decomposition_output_contract`
- `decision: remain_partial`
- `decision_reason: package_boundary_readiness_review_complete_changed_decomposition_output_contract_missing`
- `paper_faithful_offline_allowed: false`
- `package_generation_allowed: false`
- `source_scope: offline_generalization_payloads_after_batches_a_to_d`
- `implementation_boundary: planning_only_no_package_or_newton`
- `boundary_review_contract`
- `boundary_review_matrix`
- `coverage_summary`
- `remaining_gaps`
- false triggers for package generation, Newton runtime, real USD, and benchmarks.

After Batch E, the report itself must remain:

```text
status: partial
paper_faithful_offline_supported: false
next_required_gate: paper_offline_changed_decomposition_output_contract
```

Top-level failure labels must become:

```text
paper_offline_changed_decomposition_output_contract_missing
paper_package_generation_contract_missing
```

## Matrix Rows

The Batch E payload should contain these rows:

| Row id | Purpose |
| --- | --- |
| `changed_decomposition_output_contract` | Records that A-D produce audit matrices, but not yet a durable decomposition output contract that a package adapter can consume. |
| `package_generation_boundary` | Records that no `CollisionPackage` generation happens in this lane and a future package contract is required. |
| `newton_runtime_boundary` | Records that Newton runtime admissibility is still a future gate after package conversion. |
| `real_usd_boundary` | Records that bed/Franka and other real assets are outside this offline report gate. |
| `benchmark_evaluation_boundary` | Records that timing, surface distance, collision quality, and benchmark comparisons remain future work. |

Each row should contain:

- `row_id`
- `row_status`
- `required_before_unlock`
- `current_evidence`
- `blocked_reason`
- `next_gate_if_blocked`
- `claim_boundary`
- `package_generation_triggered`
- `newton_runtime_triggered`
- `real_usd_triggered`
- `benchmark_triggered`

## Invariants

Tests must assert:

- Batch E payload exists and closes only `paper_generalization_batch_e_package_boundary_readiness`;
- `implemented_generalization_scope` includes Batches A, B, C, D, and E;
- top-level `next_required_gate` moves to `paper_offline_changed_decomposition_output_contract`;
- top-level failure labels no longer contain `paper_generalization_batch_e_package_boundary_readiness_missing`;
- report status and paper-faithful support remain partial and false;
- `package_generation_allowed` is false;
- all Batch E rows keep package/Newton/real-USD/benchmark triggers false;
- no package, Newton, real-USD, benchmark, timing, surface-distance, or collision-quality output is introduced.

## Claim Boundaries

This slice supports only:

```text
offline package-boundary readiness matrix before package conversion
```

It does not support claims of:

- package readiness;
- Newton readiness;
- `CollisionPackage` generation;
- Newton runtime execution;
- real-USD evidence;
- benchmark or collision-quality evidence;
- `paper_faithful_offline` support;
- full CPD paper reproduction;
- deployment readiness or safety certification.

## Documentation Updates

Update current status and boundary docs:

- `README.md`
- `docs/index.md`
- `docs/deepdive/evidence-status.md`
- `docs/reference/claim-boundaries.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/records/README.md`
- `experiments/registry.yaml`
- `docs/records/2026-05-17-cpd-paper-generalization-batch-e-package-boundary-readiness.md`

Also correct README wording that implies the Franka support-aware native lane selected cylinders
when the current claim boundary says the support-aware lane selected boxes and records cylinders as
support-blocked raw-cost candidates.

## Self-Review

- No placeholder sections remain.
- The design is planning/report-only and does not conflict with Newton-native runtime policy.
- The next gate after Batch E is an offline changed-decomposition output contract, not package
  generation or runtime execution.
- The report remains partial and keeps `paper_faithful_offline_supported: false`.
