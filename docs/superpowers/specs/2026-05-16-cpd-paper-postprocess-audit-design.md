# CPD Paper Postprocess Audit Design

## Context

The partial `cpd_paper_offline_report` now records paper-side primitive rows, collapse costs,
topology priority-queue behavior, threshold-disabled component-pair insertion, and one
finite-threshold component-pair blocked event. The next paper-lane gate is
`paper_cpd_postprocess_audit`.

The remaining postprocess gap is enclosed-primitive culling: after the paper search creates a set
of primitives, a primitive fully enclosed by another can be removed. This slice should make that
mechanic reviewable on a tiny synthetic fixture without generating packages or invoking Newton.

## Goal

Add a deterministic fixture-scoped enclosed-primitive postprocess audit to
`cpd_paper_offline_report`.

## Scope

- Add one `paper_nested_primitive` synthetic fixture.
- Keep the postprocess input explicit rather than deriving it from the search trace.
- Record exactly two audit primitives:
  - primitive `0`: an outer `oriented_bounding_box` centered at the origin with half extents
    `[1, 1, 1]` and identity axes;
  - primitive `1`: an inner `oriented_bounding_box` centered at the origin with half extents
    `[0.25, 0.25, 0.25]` and identity axes.
- Record that primitive `1` is enclosed by primitive `0`.
- Record before/after primitive counts, enclosed ids, enclosing ids, containment test type, cull
  reason, and package/Newton/real-USD/benchmark trigger boundaries.

## Non-Scope

- No package generation.
- No Newton runtime invocation.
- No real USD, bed, Franka, benchmark, speed, or collision-quality claim.
- No general primitive-vs-primitive containment library.
- No polygon/quad intake policy.
- No broad postprocess quality claim.

## Design

Extend `_PaperToyCase` with an optional `postprocess_fixture` flag. For `paper_nested_primitive`,
the normal mesh/operator/primitive-fit audit remains a synthetic toy fixture, but the postprocess
audit uses explicit audit primitives so the culling decision is deterministic and independent of the
current simplified primitive fitters.

The `postprocess_audit` payload should contain:

```text
audit_scope: enclosed_primitive_culling_fixture
postprocess_input_source: explicit_audit_primitives_not_search_trace
input_primitive_count: 2
output_primitive_count: 1
postprocess_policy: remove_primitives_enclosed_by_another_primitive
containment_test_type: obb_corners_inside_obb
axis_policy: shared_identity_axes
input_primitives: [...]
cull_records: [...]
enclosed_primitive_ids: [1]
enclosing_primitive_ids: [0]
kept_primitive_ids: [0]
culled_primitive_ids: [1]
package_generation_triggered: false
newton_runtime_triggered: false
real_usd_triggered: false
benchmark_triggered: false
```

For this first fixture, only identity-axis `oriented_bounding_box` rows are audited. Each primitive
records:

```text
primitive_id
kind: oriented_bounding_box
center
half_extents
axes: [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
```

The containment test checks all eight corners of the inner box against the outer box in the outer
box's local frame. Because both boxes share center and identity axes, this fixture is a
deterministic canary for cull accounting, not a general OBB-vs-OBB containment library.

The tests should also assert cross-field consistency:

- `len(input_primitives) == input_primitive_count`;
- `len(kept_primitive_ids) == output_primitive_count`;
- `culled_primitive_ids` matches the ids in `cull_records`;
- `enclosed_primitive_ids` and `enclosing_primitive_ids` match the cull record ids.

## Report And Claim Boundary

After this slice, `postprocess_enclosed_primitive_culling_missing` should be removed from
`failure_labels`, and `next_required_gate` should advance to `paper_polygon_quad_intake_policy_audit`.

The report is still partial because polygon/quad intake remains missing. The postprocess audit is
only evidence that one named toy fixture records enclosed-primitive culling accounting offline.
The implementation must update the canonical lane spec and gap matrix so
`paper_polygon_quad_intake_policy_audit` is defined as the next partial-status gate rather than only
appearing in tests or temporary planning docs.

## Verification

- RED/GREEN tests for `paper_nested_primitive`.
- Preserve existing queue and component-pair fixtures.
- CLI smoke for `--run-cpd-paper-offline-report`.
- `python -m pytest -q`.
- `python scripts/validate_docs.py`.
- `python scripts/validate_site_claims.py`.
- `git diff --check`.
