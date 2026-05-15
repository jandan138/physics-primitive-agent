# CPD Synthetic Comparison Design

## Goal

Add a small offline synthetic comparison harness that runs the existing CPD-like objective report on
deterministic toy meshes under two merge policies: `topology_only` and `virtual_pairwise`.

## Context

The repository now has an offline `cpd_like_offline_objective` report for a capped bed USD. That is
useful for real-asset smoke, but the next paper-story step needs tiny meshes where a reviewer can
inspect the expected behavior without opening a large USD asset. The intended use is algorithm
iteration, not benchmark evidence.

## Claim Boundary

This slice supports only:

- synthetic, offline comparison records for the current CPD-like baseline;
- diagnostic accounting of how topology-only and component-merge policies differ;
- deterministic fixtures that future primitive-fitting and merge-search changes can reuse.

It does not support:

- full CPD paper reproduction;
- collision-quality validation;
- benchmark superiority;
- broad asset coverage;
- robot or real-scene collider-quality claims;
- safety, deployment, or certification claims.

Use wording like `synthetic objective comparison` and `diagnostic comparison record`. Avoid wording
like `quality benchmark`, `validation`, `better decomposition`, or `paper-faithful CPD`.

## Design

Create `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py` with three responsibilities:

1. define a small named mesh suite;
2. run `decompose_mesh(...)` and `build_cpd_like_objective_report(...)` for each named case and
   merge policy;
3. return a compact comparison report that is strict-JSON serializable.

The initial suite should stay intentionally small:

- `adjacent_square`: two adjacent triangles that topology can merge to one primitive;
- `disconnected_pair`: two separated triangles where topology-only stays partial and
  `virtual_pairwise` can merge;
- `blocked_disconnected_pair`: the same separated triangles with a zero component-merge threshold,
  making the blocked-merge label inspectable.

The public API should be:

```python
SYNTHETIC_COMPARISON_CLAIM_BOUNDARY = (
    "synthetic_objective_comparison_not_collision_quality_validation"
)


def build_cpd_like_synthetic_comparison_report(
    *,
    primitive_subset: tuple[str, ...] = ("box",),
    objective_options: CPDLikeObjectiveOptions | None = None,
) -> dict[str, object]:
    ...
```

The report should include:

- `stage`: `cpd_like_synthetic_objective_comparison`
- `status`: `smoke_passed` when all case-level expectations pass, otherwise `partial`
- `claim_boundary`
- `objective_version`
- `cases`: list of case summaries

Each case summary should include:

- `case_id`
- `description`
- `expectation`
- `policies`: keyed by policy label, each containing selected objective report fields:
  `status`, `decomposition_stage`, `primitive_count`, `failure_labels`, `primitive_budget`,
  `merge_excess_terms`, and `component_accounting`
- `comparison`: small derived fields such as primitive-count delta and whether
  `virtual_pairwise` cleared the topology-only failure labels for the disconnected case

Do not write generated reports into the repository. The report can be emitted by tests and the CLI;
durable evidence should be summarized in `docs/records/`.

## CLI

Add:

```text
--run-cpd-like-synthetic-comparison
```

The command should not require `--config`; it uses the synthetic in-memory suite only. It should
emit strict JSON with `allow_nan=False` and return `0` only when the report status is
`smoke_passed`.

## Tests

Use TDD:

1. Unit-test the comparison report structure and the three case-level expectations.
2. Unit-test that the report is strict-JSON serializable with `allow_nan=False`.
3. CLI-test that `--run-cpd-like-synthetic-comparison` emits JSON and requires no config.
4. CLI-test that non-finite payloads are rejected cleanly if a report builder regresses.

## Documentation

Add a dated record and update:

- `docs/reference/cpd-paper-story-status.md`
- `docs/reference/cpd-like-face-merge-explainer.md`
- `docs/deepdive/evidence-status.md`
- `docs/reference/claim-boundaries.md`
- `docs/index.md`
- `docs/records/README.md`
- `experiments/registry.yaml`

## Verification

Required before completion:

- `python -m pytest -q`
- `python scripts/validate_docs.py`
- `git diff --check`
- `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-synthetic-comparison`

## Self-Review

No placeholders remain. The scope is deliberately offline and synthetic. It adds no new primitive
fitting algorithm, no Newton probe, and no benchmark claim.
