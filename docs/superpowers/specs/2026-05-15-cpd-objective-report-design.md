# CPD Objective Report Design

## Goal

Add an offline CPD-like objective report that summarizes the existing CPD-like primitive proposals
with paper-aligned surrogate accounting terms, without claiming full CPD paper reproduction or
collision quality.

## Context

The repository currently has:

- USD mesh intake and capped first-mesh extraction;
- a geometry-only CPD-like face/component merge baseline;
- primitive proposal reports with merge-cost accounting;
- collision-package bridging;
- Newton contact, drop/settle, and sphere-rain smoke diagnostics.

The next CPD paper-story step is not a stronger Newton probe. It is an offline report that exposes
stable diagnostic accounting fields for later algorithm iteration.

## Claim Boundary

Use the phrase `paper-aligned surrogate objective report`, not `paper-faithful objective` or
`CPD reproduced`.

This slice supports only:

- offline geometry diagnostic reporting over a CPD-like baseline;
- explicit cost terms inspired by the CPD paper story;
- comparison-ready JSON fields for future topology-only/component-merge/better-fitting work.

It does not support:

- full CPD paper reproduction;
- paper-faithful primitive optimization;
- benchmark superiority;
- collision-quality validation;
- robot collider-quality claims;
- safety or deployment claims.

## Report Shape

Create `src/primitive_collision_compiler/baselines/cpd_like/objective.py`.

The public API is:

```python
@dataclass(frozen=True)
class CPDLikeObjectiveOptions:
    objective_version: str = "cpd_paper_aligned_surrogate_v0"
    primitive_type_weights: Mapping[str, float] | None = None
    claim_boundary: str = "offline_objective_report_not_collision_quality_validation"
    evidence_level: str = "offline_cpd_like_objective_smoke"


@dataclass(frozen=True)
class CPDLikeObjectiveReport:
    ...


def build_cpd_like_objective_report(
    decomposition: CPDLikeDecompositionReport,
    *,
    asset_id: str,
    source_path: str,
    max_source_faces: int | None = None,
    options: CPDLikeObjectiveOptions | None = None,
) -> CPDLikeObjectiveReport:
    ...
```

The report emits:

- `stage`: `cpd_like_offline_objective`
- `status`: `smoke_passed` when the source decomposition passed and no diagnostic failure labels
  are present, otherwise `partial`
- `objective_version`: `cpd_paper_aligned_surrogate_v0`
- `claim_boundary`
- `evidence_level`
- `asset_id`, `source_path`, `decomposition_stage`
- `primitive_budget`: target, actual, over-budget count, within-budget flag
- `geometric_excess_proxy`: total primitive volume, weighted primitive volume, AABB normalizer,
  normalized weighted volume
- `merge_excess_terms`: accepted merge count, accepted normalized excess sum/max, blocked count
- `containment`: primitive count containing assigned points, uncontained count,
  containment ratio
- `paper_primitive_gap`: supported current primitives and unsupported paper primitives still
  reported by the baseline
- `component_accounting`: initial/final components, topology/virtual/blocked merge counts,
  fallback reason
- `failure_labels`: stable list of strings for downstream comparison and review
- `decomposition`: compact source decomposition summary

## CLI

Add:

```text
--run-cpd-like-objective-report
```

The command runs the existing CPD-like geometry path, then wraps it with the offline objective
report. It does not call Newton.

Config section:

```yaml
cpd_like_objective:
  objective_version: cpd_paper_aligned_surrogate_v0
  claim_boundary: offline_objective_report_not_collision_quality_validation
  evidence_level: offline_cpd_like_objective_surrogate_smoke
  primitive_type_weights:
    box: 1.0
    sphere: 1.0
    capsule: 1.0
```

Weights are finite non-negative floats. They are report weights only. They do not change the
baseline merge search in this slice.

## Config

Add `configs/experiments/cpd_like_objective_report.yaml` for the bed smoke asset. It should reuse
the bed manifest role and component-merge gate settings, and set the report evidence level to
`offline_cpd_like_objective_surrogate_smoke`.

## Tests

Use TDD:

1. Add unit tests for `build_cpd_like_objective_report` over a simple square mesh.
2. Add unit tests for partial disconnected topology-only decomposition flags.
3. Add unit tests for primitive weight validation and weighted volume terms.
4. Add CLI test for a tiny USD and `--run-cpd-like-objective-report`.
5. Add config test that the new experiment config points to the manifest and uses the safe claim
   boundary.

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
- `PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_objective_report.yaml --run-cpd-like-objective-report`

## Self-Review

No placeholders remain. The slice is intentionally narrow: it adds an offline report and does not
alter the baseline search or Newton diagnostics.
