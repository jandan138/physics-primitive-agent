# Cylinder Scoring Policy Package Probe Plan

## Task 1: Add RED Tests

**Files:**
- Modify: `tests/test_cpd_like_decompose.py`
- Modify: `tests/test_cpd_like_synthetic.py`
- Modify: `tests/test_cli.py`

- [x] Add a decomposition test that calls:

```python
decompose_mesh(
    cpd_synthetic._cylinder_near_miss_cluster_mesh(),
    max_primitives=1,
    primitive_subset=("box", "cylinder"),
    primitive_score_multipliers={"cylinder": 0.88},
)
```

Expected RED: `decompose_mesh()` rejects the unknown keyword.

- [x] Add synthetic report tests for
  `build_cpd_like_cylinder_scoring_policy_package_probe_report()`.

Expected RED: report builder and claim constant do not exist.

- [x] Add CLI tests for `--run-cpd-like-cylinder-scoring-policy-package-probe`.

Expected RED: parser flag does not exist.

## Task 2: Thread The Multiplier Through Decomposition

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/decompose.py`

- [x] Add optional `primitive_score_multipliers`.
- [x] Validate finite positive values.
- [x] Pass the map into initial `fit_best_primitive()` calls.
- [x] Pass the map into merge-candidate `fit_best_primitive()` calls.
- [x] Serialize the multiplier map only when non-empty.

## Task 3: Add Synthetic Package Probe

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`

- [x] Add package-probe constants.
- [x] Add `build_cpd_like_cylinder_scoring_policy_package_probe_report()`.
- [x] Add near-miss and boxy guardrail cases.
- [x] Convert default and opt-in decompositions into `CollisionPackage` objects.
- [x] Record Newton shape-mapping summaries and `fully_mapped`.

## Task 4: Add CLI Entry Point

**Files:**
- Modify: `src/primitive_collision_compiler/cli.py`

- [x] Import the new builder.
- [x] Add parser flag.
- [x] Emit strict JSON and return non-zero for partial reports.

## Task 5: Update Docs And Registry

**Files:**
- Create: `docs/records/2026-05-16-cylinder-scoring-policy-package-probe.md`
- Modify: `docs/records/README.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/cpd-latest-diagnostic-loop-explainer.md`
- Modify: `docs/reference/cpd-like-face-merge-explainer.md`
- Modify: `docs/index.md`
- Modify: `experiments/registry.yaml`

- [x] Add a dated record.
- [x] Add allowed and forbidden claim wording.
- [x] Update paper-story and latest-loop explainers.
- [x] Register the command and bounded claims.

## Task 6: Review And Verify

- [x] Request implementation review.
- [x] Request documentation/claim-boundary review.
- [x] Fix Critical and Important findings.
- [x] Run focused tests.
- [x] Run full tests, docs validation, site claims, `git diff --check`, and CLI smoke.
