# Real USD Candidate Audit Design

## Context

The synthetic native selection audit explains why `cylinder`, `cone`, and `ellipsoid` win on
single-primitive toy meshes. The real-USD bed/Franka probe still selects only boxes in both legacy
and native lanes. Before changing primitive fitting or merge search, the repository needs a
diagnostic view of why the native lane still picks boxes on real capped meshes.

## Decision

Add a lightweight per-cluster candidate audit summary to the existing real-USD native fitting
comparison report. This does not change decomposition behavior. It only recomputes candidate fits
for each final selected cluster using the same primitive fitting helper as the selector, then
summarizes the result.

## Report Fields

Each lane summary should include `candidate_audit_summary` with:

- `scope`: `per_selected_cluster`;
- `cluster_count`;
- `primitive_subset`;
- `selected_kind_counts`;
- `selected_rank_counts`;
- `extension_candidate_kinds`;
- `clusters_with_extension_best`;
- `extension_best_kind_counts`;
- `clusters_where_extension_beats_selected`;
- `box_selected_cluster_count`;
- `box_selected_with_extension_second_count`;
- `margin_sign_convention`;
- `mean_selected_minus_best_nonselected_cost`;
- `mean_selected_minus_best_extension_cost`;

The report should not include every raw candidate for every real-USD cluster by default. The
summary is enough for the next algorithm decision and avoids large JSON churn.

## Claim Boundary

Allowed:

- "real-USD candidate audit summary";
- "per-selected-cluster surrogate candidate accounting";
- "diagnostic explanation for why current native lane still selects boxes."

Not allowed:

- "native primitives improved bed/Franka";
- "collision quality improved";
- "paper objective implemented";
- "benchmark evidence";
- "validated collider."

## Verification

- Unit test over the tiny USD manifest fixture.
- Strict JSON serialization test.
- Regenerate the real-USD fitting report under the clean conda environment if available.
- `python -m pytest -q`.
- `python scripts/validate_docs.py`.
- `git diff --check`.
