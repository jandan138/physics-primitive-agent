# Native Selection Audit Design

## Context

The repository can now run a synthetic native fitting comparison and a capped bed/Franka real-USD
probe comparison. The synthetic comparison shows that `cylinder`, `cone`, and `ellipsoid` can be
selected on controlled toy meshes. The real-USD probe currently selects only boxes in both lanes.

The next useful slice should not claim better real-USD collision quality. It should make the
synthetic primitive-choice evidence easier to audit: for each toy fixture, show the candidate
primitive costs that caused the selected native primitive to win.

## Decision

Add a native selection audit to the existing synthetic Newton-native fitting comparison report.
The report should keep the same CLI and config surface, but each lane summary should include a
machine-readable candidate table.

The selection policy is still simple:

```text
fit every requested primitive kind
-> compute each candidate's weighted primitive volume
-> choose the candidate with the lowest weighted primitive volume
-> break ties by primitive subset order
```

This is a surrogate fitting cost, not the paper's full objective or optimizer.

## Report Additions

Each native fitting lane should include:

- `selection_policy`: `min_weighted_volume_surrogate_v0`;
- `selection_cost_name`: `weighted_primitive_volume`;
- `selection_cost_units`: `source_mesh_volume_units`;
- `candidate_audit`: ordered candidates with primitive kind, rank, selected flag, raw volume,
  weighted volume, normalized weighted volume, containment flag, and dimensions;
- `selected_candidate_rank`: `1` when the chosen primitive has the lowest reported surrogate cost.

The case-level comparison should include:

- `native_selection_margin_vs_legacy_best`;
- `native_selection_margin_vs_next_native_candidate`;
- `native_selected_kind_cost_explained`;
- `selection_claim_boundary`.

## Claim Boundary

Allowed wording:

- "synthetic native selection audit";
- "candidate weighted-volume table";
- "surrogate primitive-choice explanation";
- "not paper-faithful CPD optimization";
- "not collision-quality or benchmark evidence."

Disallowed wording:

- "CPD optimizer implemented";
- "paper objective reproduced";
- "native primitives are better on real USD";
- "collision quality improved";
- "validated collider."

## Files

- `src/primitive_collision_compiler/baselines/cpd_like/primitives.py`
- `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- `tests/test_cpd_like_synthetic.py`
- `tests/test_cli.py`
- `configs/experiments/newton_native_fitting_comparison.yaml`
- `docs/reference/newton-native-fitting-comparison.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/reference/real-usd-native-probe-paper-story-explainer.md`
- `docs/deepdive/evidence-status.md`
- `docs/reference/claim-boundaries.md`
- `docs/index.md`
- `docs/records/README.md`

## Verification

- Targeted pytest for synthetic report and CLI.
- Full pytest.
- `python scripts/validate_docs.py`.
- `git diff --check`.
