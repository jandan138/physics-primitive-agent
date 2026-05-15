# CPD Synthetic Expected-Failure Workbench Design

## Context

The repository now has a CPD-like baseline, synthetic objective comparisons, a cost-guided toy
merge-search smoke, and structured Eq.4 alignment metadata. The next CPD reproduction step should
not jump straight to a larger optimizer. It should first make current known gaps inspectable in a
deterministic synthetic workbench.

This slice adds an expected-failure workbench. "Expected failure" means the report intentionally
looks for known limitations in the current CPD-like baseline and records whether those limitation
labels remain visible. It does not mean the code failed unexpectedly. A top-level `smoke_passed`
result means "the expected limitation was reported," not "the decomposition succeeded."

## Goal

Add a command-only synthetic workbench that classifies current CPD-like baseline limitations as
named diagnostic flags while preserving the claim boundary: this is paper-story accounting, not
paper-faithful CPD reproduction, benchmark evidence, general failure detection, or
collision-quality validation.

## Recommended Approach

Use a new report builder and CLI flag instead of expanding the existing synthetic comparison report.
The existing report answers "do topology-only and virtual-pairwise policies behave as expected?"
The new report answers "which known CPD-paper gaps are visible on controlled toy fixtures?"

This separation keeps the current smoke comparisons stable and lets downstream records refer to a
specific expected-failure stage.

## Report Shape

Add `build_cpd_like_expected_failure_synthetic_workbench_report()` under
`src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`.

The returned JSON includes:

- `stage`: `cpd_like_expected_failure_synthetic_workbench`;
- `status`: `smoke_passed` only when every case's expected diagnostic flags match observed flags;
- `status_semantics`: `expected_limitations_reported_not_decomposition_success`;
- `claim_boundary`: `synthetic_expected_failure_workbench_not_collision_quality_validation`;
- `evidence_level`: `offline_cpd_like_expected_failure_workbench_smoke`;
- `objective_version`;
- `cases`.

Each case includes:

- `case_id`;
- `description`;
- `paper_story_gap`;
- `paper_gap_tags`;
- `limitation_class`;
- `next_capability_needed`;
- `fixture_geometry_summary`;
- `expected_diagnostic_flags`;
- `expectation_status`;
- `policy`;
- `metrics`.

`expected_diagnostic_flags` is a deterministic object:

```python
{
    "expected": [...],
    "observed": [...],
    "missing": [...],
    "unexpected": [...],
    "match_status": "matched" | "mismatched",
}
```

This avoids pass rates, scores, or rankings. The object says whether known limitation labels remain
visible on a fixture.

`fixture_geometry_summary` records:

- `point_count`;
- `face_count`;
- `connected_component_count`;
- `mesh_aabb_volume`;
- `normalizer_floor_applied`.

The floor flag matters because planar toy meshes can have zero AABB volume, making normalized
excess values intentionally use the existing floor.

## Fixtures

Use three deterministic in-memory fixtures already compatible with the current mesh helpers:

1. `restricted_primitive_vocabulary_gap`
   - Mesh: adjacent square.
   - Policy: topology only, target one primitive, primitive subset `("box",)`.
   - `limitation_class`: `expected_primitive_fit_gap`.
   - `next_capability_needed`: `primitive_fit_extension`.
   - `paper_gap_tags`: `restricted_primitive_vocabulary`, `paper_scope_primitive_fitting`.
   - Expected flags:
     - `unsupported_paper_primitives_present`;
     - `paper_alignment_surrogate_not_paper_faithful`.
   - Purpose: pin the paper primitive vocabulary gap without adding unsupported fitting code.

2. `single_proxy_wraps_disconnected_components`
   - Mesh: two disconnected triangles.
   - Policy: virtual pairwise, target one primitive.
   - `limitation_class`: `expected_empty_wrapper_proxy`.
   - `next_capability_needed`: `primitive_fit_extension`.
   - `paper_gap_tags`: `assigned_vertex_containment_proxy_only`,
     `no_surface_distance_or_collision_benchmark`.
   - Expected flags:
     - `unsupported_paper_primitives_present`;
     - `paper_alignment_surrogate_not_paper_faithful`;
     - `virtual_component_merge_used`;
     - `empty_space_wrap_proxy_present`.
   - Purpose: show a case that can reach the primitive budget while still creating a diagnostic
     empty-wrapper-space risk under the current volume proxy.

3. `threshold_blocks_component_merge`
   - Mesh: two disconnected triangles.
   - Policy: virtual pairwise, target one primitive, threshold `0.0`.
   - `limitation_class`: `expected_threshold_block`.
   - `next_capability_needed`: `merge_search_extension`.
   - `paper_gap_tags`: `threshold_applies_only_to_virtual_component_merges`,
     `candidate_graph_restricted`.
   - Expected flags:
     - `unsupported_paper_primitives_present`;
     - `paper_alignment_surrogate_not_paper_faithful`;
     - `component_merge_blocked`;
     - `unmerged_components`;
     - `primitive_budget_not_met`.
   - Purpose: keep the blocked component merge failure mode explicit and reproducible.

## Flag Semantics

The report derives flags from existing objective/decomposition fields:

- `unsupported_paper_primitives_present`: `paper_primitive_gap.unsupported_paper_primitive_count > 0`;
- `paper_alignment_surrogate_not_paper_faithful`: `paper_alignment.paper_faithfulness == "surrogate_not_paper_faithful"`;
- `virtual_component_merge_used`: `component_accounting.virtual_component_merge_count > 0`;
- `empty_space_wrap_proxy_present`: accepted raw Eq.4-like cost is positive after a virtual
  component merge;
- `component_merge_blocked`: failure labels include `component_merge_blocked`;
- `unmerged_components`: failure labels include `unmerged_components`;
- `primitive_budget_not_met`: failure labels include `primitive_budget_not_met`.

These flags are diagnostic labels. They are not a scalar quality score and not proof that bad
colliders are caught generally.

## CLI

Add:

```bash
python -m primitive_collision_compiler.cli --run-cpd-like-expected-failure-workbench
```

The command emits strict JSON and returns exit code `0` only when report status is `smoke_passed`.
It mirrors the existing synthetic comparison error handling for non-finite JSON.

## Documentation

Update:

- `docs/reference/cpd-objective-report-alignment.md`;
- `docs/reference/cpd-paper-story-status.md`;
- `docs/reference/claim-boundaries.md`;
- `docs/deepdive/evidence-status.md`;
- `docs/index.md`;
- `docs/records/README.md`;
- `README.md`;
- add a dated record under `docs/records/`.

Use safe wording:

- "deterministic expected-failure synthetic workbench";
- "expected limitation fixtures";
- "diagnostic flags";
- "known CPD-paper gaps";
- "not benchmark evidence";
- "not collision-quality validation";
- "not paper-faithful CPD reproduction."

Avoid:

- "expected-failure benchmark";
- "failure detector validation";
- "proves the baseline catches bad decompositions";
- "quality score";
- "validated failures";
- "algorithm superiority";
- "paper objective reproduced";
- "prevents false contacts";
- "safe collider rejection."

## Tests

Add tests that first fail because the new builder and CLI do not exist:

- report schema and case ids;
- each case's expected flags match observed flags with empty `missing` and `unexpected`;
- fixture geometry summary fields;
- paper gap tags and limitation classes;
- strict JSON serialization;
- CLI emits strict JSON and returns `0`;
- CLI maps non-finite JSON serialization to exit code `2`.

## Out Of Scope

- New primitive fitting algorithms.
- New merge-search algorithms.
- Newton task execution.
- Asset-level bed or Franka reruns.
- Benchmark, general failure-detection, or collision-quality claims.

