# CPD Cost-Guided Merge Design

## Goal

Add the first restricted algorithmic improvement after the synthetic objective comparison: an
opt-in CPD-like merge-search policy that uses AABB-normalized merge-excess as a decision-making
cost on deterministic toy meshes.

## Context

The current baseline already records merge-excess accounting after decomposition. The next paper
story step is to use one of those recorded terms during decomposition, without claiming the CPD
paper objective or optimizer has been implemented.

The current default behavior should remain unchanged:

1. merge adjacent topology candidates first;
2. only try virtual disconnected-component candidates when topology adjacency is exhausted;
3. use the objective report afterward as diagnostic accounting.

The new behavior should be opt-in and synthetic-first:

1. evaluate the best adjacent topology candidate and the best virtual disconnected-component
   candidate at the same loop step;
2. choose the candidate with lower AABB-normalized merge-excess;
3. keep the virtual merge threshold gate for virtual candidates;
4. record which policy was used so reviewers can compare old and new accounting.

## Claim Boundary

This slice supports only a focused CPD-like cost-guided merge-search smoke over deterministic
synthetic fixtures. It is diagnostic accounting for future CPD reproduction work, not full CPD
paper reproduction, paper-faithful optimization, collision-quality validation, benchmark evidence,
broad asset/task evidence, robot collider quality, or safety/deployment evidence.

Use wording like:

- "focused CPD-like cost-guided merge-search smoke";
- "uses one existing objective-report term as a decision-making cost";
- "old/new diagnostic accounting on deterministic synthetic fixtures";
- "restricted algorithmic smoke slice."

Avoid wording like:

- "CPD optimizer implemented";
- "CPD objective implemented";
- "paper-faithful CPD implementation";
- "better collision geometry";
- "decomposition quality validated";
- "benchmark result."

## Design

Add merge-search policy constants to `decompose.py`:

- `MERGE_SEARCH_TOPOLOGY_THEN_VIRTUAL = "topology_then_virtual"`
- `MERGE_SEARCH_COST_GUIDED_PAIRWISE = "cost_guided_pairwise"`

Extend `decompose_mesh(...)` with:

```python
merge_search_policy: str = MERGE_SEARCH_TOPOLOGY_THEN_VIRTUAL
```

The default policy keeps current behavior exactly. The cost-guided policy is valid only with
`component_merge="virtual_pairwise"` because it compares adjacent and non-adjacent pair candidates.

Extend `CPDLikeDecompositionReport` with `merge_search_policy` and include it in `to_dict()`.
Also expose the value in objective-report `component_accounting`.

For candidate selection, add a boolean to `_MergeCandidate`:

```python
is_virtual_component_merge: bool
```

The existing `_best_merge(..., require_adjacency=True/False)` helper can stay mostly intact. The
new policy should call it twice, once for topology candidates and once for virtual candidates, then
select the lower normalized merge-excess candidate. Ties should prefer topology candidates to keep
behavior stable.

If the selected candidate is virtual and exceeds `excess_volume_threshold_fraction`, record
`component_merge_threshold_blocked` and stop. Do not silently fall back to a more expensive topology
candidate; the blocked decision is part of the smoke evidence.

## Synthetic Comparison

Extend `synthetic.py` with one additional case:

`cost_guided_pair_choice`: a three-face toy mesh where faces 0 and 1 are adjacent but expensive to
merge under the current box volume proxy, while faces 0 and 2 are disconnected but much cheaper to
merge. With `max_primitives=2`:

- old/default `topology_then_virtual` should take one topology merge;
- new `cost_guided_pairwise` should take one virtual component merge;
- the new accepted normalized merge-excess sum should be lower on this toy case.

This is not proof of better collision geometry. It is only evidence that the cost term now affects
the merge decision on an inspectable fixture.

## CLI

Add a no-config command:

```text
--run-cpd-like-cost-guided-synthetic-comparison
```

It should emit strict JSON with:

- `stage`: `cpd_like_cost_guided_synthetic_objective_comparison`
- `claim_boundary`: `cost_guided_synthetic_comparison_not_collision_quality_validation`
- `evidence_level`: `offline_cpd_like_cost_guided_synthetic_comparison_smoke`

The existing `--run-cpd-like-synthetic-comparison` path should keep working. It may include the new
case only if the original claim boundary remains intact. The dedicated cost-guided CLI path makes
the new smoke record easier to cite.

## Tests

Use TDD:

1. Add decomposition tests proving the default policy still chooses topology first while
   `cost_guided_pairwise` chooses the lower-cost virtual candidate on the toy mesh.
2. Add a threshold test proving a selected virtual candidate is blocked rather than replaced by a
   more expensive topology candidate.
3. Add validation coverage for unknown `merge_search_policy`.
4. Add synthetic-report tests for the cost-guided case and strict JSON.
5. Add CLI tests for the new no-config command and non-finite JSON rejection.

## Documentation

Add a dated record and update:

- `docs/records/2026-05-15-cpd-like-cost-guided-merge.md`
- `docs/records/README.md`
- `docs/reference/claim-boundaries.md`
- `docs/deepdive/evidence-status.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/reference/cpd-objective-report-alignment.md`
- `docs/reference/cpd-like-face-merge-explainer.md`
- `docs/index.md`
- `README.md`
- `experiments/registry.yaml`

## Verification

Required before completion:

- `python -m pytest tests/test_cpd_like_decompose.py tests/test_cpd_like_synthetic.py tests/test_cli.py -q -k "cost_guided or synthetic_comparison or cpd_like_synthetic"`
- `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cost-guided-synthetic-comparison`
- `python -m pytest -q`
- `python scripts/validate_docs.py`
- `git diff --check`

## Self-Review

No placeholders remain. The design is one focused algorithmic smoke slice. It preserves default
behavior, keeps generated outputs out of git, and avoids paper-faithful CPD claims.
