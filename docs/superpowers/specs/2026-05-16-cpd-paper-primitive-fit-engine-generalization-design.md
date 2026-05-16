# CPD Paper Primitive Fit Engine Generalization Design

## Date

2026-05-16

## Goal

Close only `paper_generalization_batch_b_primitive_fit_engine` by adding an offline
report-only primitive-fit engine generalization payload to `cpd_paper_offline_report`.

The gate must not claim `paper_faithful_offline`, package generation, Newton runtime execution,
real-USD evidence, benchmark evidence, or collision-quality evidence.

## Current Context

The report already has named fixture-breadth cases for all six CPD paper primitive names:

- `oriented_bounding_box`
- `sphere`
- `capsule`
- `capped_cylinder`
- `frustum`
- `trapezoidal_prism`

Those cases prove that specific toy fixtures are represented in the report. They do not yet prove
that the primitive-fit path is reported as a reusable offline engine boundary. The existing helper
`_primitive_fit_audit_payload()` already evaluates all six paper primitive candidates for a
`TriangleMesh` plus face group and selects by weighted volume. Batch B should expose that reusable
contract without adding a new runtime path.

## Design

Add a top-level payload:

```text
paper_generalization_batch_b_primitive_fit_engine
```

This payload is a report summary over deterministic in-memory parametric primitive-fit probes.
It is separate from the `cases` fixture list, so Batch B is not just another fixture-breadth batch.

The payload should include:

- `gate_id: paper_generalization_batch_b_primitive_fit_engine`
- `gate_status: implemented_offline_report_only_partial`
- `closed_gate: paper_generalization_batch_b_primitive_fit_engine`
- `next_required_gate: paper_generalization_batch_c_search_engine`
- `decision: remain_partial`
- `decision_reason: primitive_fit_engine_generalization_complete_search_engine_missing`
- `paper_faithful_offline_allowed: false`
- `source_scope: deterministic_in_memory_parametric_primitive_fit_probes`
- `implementation_boundary: offline_report_only_no_package_or_newton`
- an `engine_contract` that records the input contract, candidate set, candidate evaluation policy,
  selection rule, containment scope, axis policy, and offline-only unmapped paper primitives;
- a `primitive_family_matrix` with probe rows for every paper primitive family;
- a `coverage_summary` with primitive count, probe count, candidate row count, closed gate count,
  and remaining gate count;
- `remaining_gaps` containing only Batch C, Batch D, and Batch E;
- package, Newton, real-USD, and benchmark trigger booleans set to false.

## Probe Matrix

Use deterministic generated probes, not real assets and not benchmark data. Reuse the current
synthetic mesh helpers where they already encode useful non-degenerate shapes, and keep the probes
outside `_paper_toy_cases()`:

- OBB probe: rotated nonuniform cuboid.
- Sphere probe: offset cuboid with an asymmetric extra point.
- Capsule probe: elongated off-axis cuboid.
- Capped-cylinder probe: off-axis flat capped cylinder-like shape.
- Frustum probe: tapered shape with unequal top and bottom radii.
- Trapezoidal-prism probe: asymmetric wedge.

Each row should record:

- `probe_id`
- `target_paper_primitive`
- `variant_parameters`
- `candidate_row_count`
- `candidate_order`
- `target_candidate`
- `selected_candidate`
- `target_candidate_selected`
- `contains_assigned_points`
- `finite_numeric_fields`
- `newton_runtime_kind`
- package/Newton/real-USD/benchmark false triggers

The rows may record whether the target primitive was selected, but selection is not required for
closing the gate. This gate is about candidate generation and bounded primitive-fit accounting, not
about proving a primitive is best.

## Gate Progression

After this gate closes:

- top-level `next_required_gate` moves to `paper_generalization_batch_c_search_engine`;
- top-level `failure_labels` contain only Batch C, Batch D, and Batch E missing labels;
- `paper_faithfulness["implemented_generalization_scope"]` contains Batch A and Batch B;
- `paper_faithful_offline_supported` remains false;
- `_paper_faithful_offline_scope_criteria()` remains blocking for primitive vocabulary and fit.

## Claim Boundary

Supported wording:

- "The offline CPD paper report includes a primitive-fit engine generalization matrix over
  deterministic synthetic probes."
- "Batch B closes only as offline report-only partial evidence."
- "The next required gate is Batch C search-engine generalization."

Unsupported wording:

- `paper_faithful_offline`
- full CPD reproduction
- robust primitive fitting
- collision-quality improvement
- benchmark evidence
- Newton support for paper-only primitives
- package generation
- real-USD evidence

## Tests

Add failing tests before implementation:

- top-level gate moves from Batch B to Batch C;
- Batch B payload exists and keeps the report partial;
- Batch B payload has all false runtime/package/asset/benchmark triggers;
- every probe row has six candidates and no missing paper primitive rows;
- candidate numeric fields are finite;
- offline-only paper primitives remain `offline_only_unmapped`;
- CLI JSON exposes the same Batch B payload and C-E remaining labels.

## Review Notes

Two read-only review agents converged on the same boundary:

- close Batch B through a report payload, not a new CLI or runtime path;
- keep `_primitive_fit_audit_payload()` as the engine being summarized;
- do not mark primitive-fit scope as non-blocking for `paper_faithful_offline`;
- avoid real USD, Newton, package generation, and benchmark work in this gate.
