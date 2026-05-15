# 2026-05-15 Big Goal 1 Completion Audit

## Date

2026-05-15

## Status

Complete for Big Goal 1 as a minimal CPD-like diagnostic workbench.

## Objective Restatement

Big Goal 1 is the first minimal end-to-end CPD reproduction workbench, not a full reproduction of
the Convex Primitive Decomposition for Collision Detection paper. The concrete deliverable is a
claim-safe diagnostic loop:

```text
USD / mesh input
-> CPD-like primitive proposals
-> paper-aligned surrogate objective and quality reports
-> CollisionPackage bridge
-> Newton diagnostic probes
-> dated records and reproducible configs
```

The goal is complete only if every step above has executable code, a config or command surface,
tests or recorded smoke evidence, and claim-boundary documentation.

## Prompt-To-Artifact Checklist

| Requirement | Evidence | Audit result |
| --- | --- | --- |
| Use a real USD or mesh input path, without committing raw assets. | `assets/manifests/cpd_like_smoke_assets.yaml`, `assets/manifests/franka_usd_smoke_assets.yaml`, and records `2026-05-14-newton-usd-smoke.md`, `2026-05-15-franka-cpd-like-smoke.md`. | Covered. |
| Produce CPD-like primitive proposals from capped mesh geometry. | `src/primitive_collision_compiler/baselines/cpd_like/decompose.py`, `--run-cpd-like`, `configs/experiments/cpd_like_baseline.yaml`, and record `2026-05-14-cpd-like-geometry-smoke-slice.md`. | Covered as a restricted baseline, not the paper algorithm. |
| Provide an audit-friendly merge policy and component accounting. | `configs/experiments/cpd_like_component_merge_gate.yaml` and record `2026-05-15-cpd-like-component-merge-gate.md`. | Covered. |
| Provide paper-aligned surrogate objective and quality reporting. | `src/primitive_collision_compiler/baselines/cpd_like/objective.py`, `configs/experiments/cpd_like_objective_report.yaml`, and record `2026-05-15-cpd-like-objective-report.md`. | Covered as surrogate reporting, not paper-faithful objective implementation. |
| Add structured paper-objective alignment metadata. | `docs/records/2026-05-15-cpd-eq4-alignment-metadata.md` and `docs/reference/cpd-objective-report-alignment.md`. | Covered. |
| Compare old/new accounting on inspectable synthetic toy meshes. | `--run-cpd-like-synthetic-comparison`, `--run-cpd-like-cost-guided-synthetic-comparison`, and records `2026-05-15-cpd-like-synthetic-comparison.md`, `2026-05-15-cpd-like-cost-guided-merge.md`. | Covered for restricted synthetic smokes. |
| Keep known CPD-paper gaps visible before stronger claims. | `--run-cpd-like-expected-failure-workbench` and record `2026-05-15-cpd-synthetic-expected-failure-workbench.md`. | Covered as expected limitation accounting, not validation. |
| Add the first primitive-vocabulary extension selected from the expected-failure gap. | `configs/experiments/cpd_like_capped_cylinder_proxy.yaml` and records `2026-05-15-cpd-capped-cylinder-proxy.md`, `2026-05-15-cpd-capped-cylinder-master-verification.md`. | Covered for opt-in offline capped-cylinder proxy accounting. |
| Convert CPD-like reports into a collision package contract. | `src/primitive_collision_compiler/baselines/cpd_like/package.py`, `src/primitive_collision_compiler/contracts.py`, and `tests/test_cpd_like_package.py`. | Covered. |
| Run Newton diagnostics against mapped package primitives. | `--run-newton-contact-smoke`, `--run-newton-drop-settle`, `--run-newton-sphere-rain`, configs `configs/experiments/newton_drop_settle.yaml`, `configs/experiments/newton_sphere_rain.yaml`, and records `2026-05-14-newton-contact-smoke.md`, `2026-05-14-newton-drop-settle.md`, `2026-05-15-newton-sphere-rain.md`. | Covered for recorded mapped primitives. |
| Preserve claim boundaries and DeepDive readiness. | `docs/reference/claim-boundaries.md`, `docs/deepdive/evidence-status.md`, `docs/reference/cpd-paper-story-status.md`, and `docs/index.md`. | Covered. |
| Keep reproducible configs, records, and verification gates. | `configs/`, `experiments/registry.yaml`, `docs/records/README.md`, and master verification records through commit `0fab303`. | Covered. |

## Verification Inspected

- `python scripts/validate_docs.py`: exit 0, `docs validation passed` after the capped-cylinder
  master verification record.
- `git diff --check`: exit 0, no whitespace errors after the capped-cylinder master verification
  record.
- `python -m pytest tests/test_cpd_like_decompose.py tests/test_cpd_like_objective.py tests/test_newton_shapes.py tests/test_cli.py tests/test_cpd_like_config.py -q -k "capped_cylinder or unsupported_gap or equal_proxy"`:
  exit 0, `7 passed, 88 deselected`.
- `python -m pytest -q`: exit 0, `180 passed`.
- `PYTHONPATH=src python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_capped_cylinder_proxy.yaml --run-cpd-like-objective-report`:
  exit 0, with `decomposition_stage` `cpd_like_component_merge_gate` and unsupported paper
  primitives `frustum` and `trapezoidal_prism`.

Focused implementation and claim-boundary agent re-review found no blocking or important issues
for the capped-cylinder proxy slice before it was merged.

## Missing But Not Required For Big Goal 1

The following are still missing and must not be claimed:

- full CPD paper reproduction;
- paper-faithful primitive fitting, objective implementation, or global optimization;
- Newton mapping for `capped_cylinder`, `frustum`, or `trapezoidal_prism`;
- collision-quality validation or benchmark superiority;
- broad 5-10 asset proof-point benchmark evidence;
- whole-robot collider-quality evidence;
- deployment readiness, safety certification, or real-world transfer.

These are later research goals, not blockers for Big Goal 1 as defined above.

## Decision

Big Goal 1 is achieved as a minimal, claim-safe CPD-like diagnostic workbench. The repository now
has executable intake, restricted proposal generation, surrogate reporting, package conversion,
Newton diagnostic probes, synthetic limitation accounting, one primitive-vocabulary extension, and
dated verification records.

## Next Action

Start the next goal only after this audit: move from the completed diagnostic workbench toward
paper-core algorithm work, beginning with one named primitive-fit quality or merge-search target
selected from the expected-failure workbench.
