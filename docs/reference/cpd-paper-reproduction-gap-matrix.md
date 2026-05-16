# CPD Paper Reproduction Gap Matrix

This page maps the Convex Primitive Decomposition for Collision Detection paper requirements to
the repository's current Newton CPD workbench. It is a planning and audit document, not new
experiment evidence, and not a claim that the paper algorithm has been reproduced.

For the plain-language pipeline map, see
[CPD pipeline step-by-step explainer](cpd-pipeline-step-by-step-explainer.md). For current claim
limits, see [Claim Boundaries](claim-boundaries.md). For the planned fixture-scoped offline lane,
see [CPD paper-faithful offline lane spec](cpd-paper-faithful-offline-lane-spec.md).

## Scope

The matrix answers six questions for each paper requirement:

- what the paper requires;
- what the repository has now;
- whether the current artifact is a surrogate or paper-faithful;
- what must be implemented in an offline paper lane first;
- what can enter the Newton runtime lane;
- what claim boundary applies.

The source-paper intake used for this matrix lives under
`docs/tmp/papers/arXiv-2602.07369v1/`. The durable statement is this reference page, not the raw
temporary intake.

## Status Terms

| Term | Meaning |
| --- | --- |
| `not_started` | No repository artifact implements the paper requirement yet. |
| `surrogate` | A current artifact asks a similar engineering question, but does not implement the paper method. |
| `partial` | A current artifact overlaps with the paper requirement, but misses material details or scope. |
| `paper_faithful_offline` | The declared fixture scope implements the paper-side mechanic offline with tests and dated records. No current row has this status yet, and the term does not imply benchmark, Newton runtime, or full reproduction evidence. |
| `newton_runtime_mapped` | A primitive or package can be constructed in Newton diagnostic code under recorded settings. This is separate from paper faithfulness. |

## Primitive Terminology

| Paper concept | Current CPD-like kind | Newton runtime kind | Current mapping status |
| --- | --- | --- | --- |
| Oriented bounding box | `box` | `box` | Runtime-mapped when package validation passes. |
| Sphere | `sphere` | `sphere` | Runtime-mapped when package validation passes. |
| Capsule | `capsule` | `capsule` | Runtime-mapped when package validation passes. |
| Paper capped cylinder | Current `capped_cylinder` is a hemisphere-cap proxy, not the paper fit. | Newton `cylinder` is separate. | The current `capped_cylinder` package kind is not Newton-mapped; any future paper capped-cylinder adapter needs a dated conversion spec. |
| Frustum | offline fit-audit candidate row for named toy fixtures only | no direct runtime primitive | Keep offline unless an explicit approximation policy exists. Newton `cone` is not general frustum support. |
| Isosceles trapezoidal prism | offline fit-audit candidate row under the report label `trapezoidal_prism` for named toy fixtures only | no direct runtime primitive | Keep offline unless converted through a recorded convex-hull or other adapter. |
| Paper extension not in the original primitive set | `cone`, `ellipsoid` | `cone`, `ellipsoid` | Newton-native diagnostics only; not paper-faithful primitive support. |

## Gap Matrix

| Paper requirement | Current repository artifact | Status | Surrogate or paper-faithful? | Offline paper-lane work first | Newton runtime lane | Claim boundary |
| --- | --- | --- | --- | --- | --- | --- |
| Input mesh with face-based decomposition. The paper starts from mesh vertices and polygonal faces, then assigns primitives to faces so the surface is covered by primitive groups. | `TriangleMesh` is triangle-only. USD intake can extract capped first meshes, and synthetic fixtures can feed the CPD-like baseline. | partial | Partial infrastructure, not paper-scope mesh intake. | Preserve source-face accounting, document polygon-to-triangle handling, and add deterministic fixtures that check face coverage. | Newton should only consume already generated packages; it should not decide paper face grouping. | Asset intake is plumbing, not collider-quality evidence. |
| Preprocessing for overlapped or duplicate vertices. The paper discusses vertex deduplication because unclean meshes can change topology and decomposition. | Asset mirror and USD-open diagnostics exist. There is no paper-faithful duplicate-vertex preprocessing lane for CPD output. | not_started | Not paper-faithful. | Add an offline preprocessing report with duplicate-distance policy, before/after topology summary, and source-face remap. | Not a Newton runtime concern except through the final package produced later. | Do not claim robust unclean-mesh handling before records exist. |
| Per-face linear operator `Q`: area-weighted normal outer product plus optional tangent-stability term, summed when face groups merge. | `TriangleMesh.face_operator()` computes an area-weighted triangle normal/tangent matrix. The partial `cpd_paper_offline_report` now records per-face and merged-group operator audit fields for two triangle-only toy fixtures. | partial | Paper-shaped for triangle fixtures, but not full paper handling for polygons, quad tangent policy, or full paper-lane coverage. | Extend the audit beyond triangle-only fixtures and make polygon/quad tangent policy explicit before `paper_faithful_offline` wording. | No Newton mapping; this is algorithm-side data. | This supports "paper-shaped operator audit for named fixtures", not paper-faithful CPD. |
| Primitive vocabulary: oriented bounding box, sphere, capsule, capped cylinder, frustum, and isosceles trapezoidal prism. | Current CPD-like candidates include `box`, `sphere`, `capsule`, `cylinder`, `cone`, `ellipsoid`, and an opt-in `capped_cylinder` proxy. Current Newton mapping supports `box`, `sphere`, `capsule`, `cylinder`, `cone`, and `ellipsoid`. The partial `cpd_paper_offline_report` now includes offline-only frustum and trapezoidal-prism fit-audit rows for named toy fixtures. | partial | Mixed. `box`/`sphere`/`capsule` overlap with paper intent but remain current surrogate fit rows. Current `capped_cylinder` is a proxy package kind, not the paper fit and not Newton-mapped. `frustum` and `trapezoidal_prism` now have offline audit rows only, not runtime support or full paper-faithful coverage. `cone` and `ellipsoid` are Newton-native extensions, not paper primitives. | Add paper-style flat capped-cylinder fitting, one-candidate-per-axis paper capsule/cylinder policy, and broader paper-lane fixtures before stronger paper-lane wording. | Only the intersection with Newton-native support should run in Newton directly after package conversion and runtime admissibility checks. Paper-only primitives need either an explicit approximation report or must stay offline. | Primitive support is not evidence of better collision quality or full CPD reproduction. |
| Primitive construction from operator eigenvectors and assigned points. The paper fits each primitive by expanding parameters to enclose the assigned point set. | Current fitters use operator axes and point bounds/radial spans, but several are simplified proxies. The partial `cpd_paper_offline_report` audits all six paper primitive names: OBB, sphere, capsule, current `capped_cylinder` proxy, offline-only frustum, and offline-only trapezoidal-prism rows. It records the current parameter clamp, axis policy, volume formulas, containment checks, and runtime-unmapped status for paper-only rows. | partial | Surrogate and partial. It produces useful audit rows, but it does not implement paper-flat capped-cylinder fitting, full paper capsule/cylinder axis policy, polygon/quad intake, or full decomposition search. | Add paper-style flat capped-cylinder fitting and then full priority-queue trace before stronger paper-lane wording. | Newton should receive only mapped package primitives after a separate package conversion and runtime-admissibility check. | Candidate audit tables explain current choices only under the current partial offline slice. |
| Collapse cost: merge two primitives by the added volume of the merged primitive over the previous two, with optional primitive type weighting. | Current objective reports include raw and AABB-normalized merge-excess fields. The partial `cpd_paper_offline_report` now records unnormalized `paper_base_cost` separately from `weighted_priority_cost` for one two-face toy fixture and includes the left, right, and merged fit-audit payloads that feed the cost. | partial | Paper-shaped and fixture-scoped. The cost fields match the planned split for one toy edge, but full priority-queue search, thresholding, and all primitive fits are missing. | Extend from one toy edge to a deterministic priority-queue trace with thresholds, stale-entry handling, and all required primitive fits. | Newton should not use cost terms directly; it consumes packages generated after offline selection. | A lower paper-shaped toy cost is not a benchmark or quality result. |
| Priority-queue greedy collapse over adjacent face groups. The paper initializes adjacent face-pair candidates and repeatedly collapses the minimum-cost candidate. | Current baseline has greedy/rule-based face merging, optional component merging, cost-guided pairwise toy behavior, and two-step lookahead on one synthetic trap fixture. | surrogate | Surrogate. The current search experiments are controlled workbench slices, not the paper collapse algorithm. | Add a deterministic offline priority-queue collapse loop with stale-entry pruning, adjacency updates, and per-step trace output. | Newton package probes should wait until the offline paper lane produces a changed package. | Toy search changes do not prove merge-policy superiority. |
| Target primitive count `N` and optional excess-volume threshold. The paper stops when no collapses remain or the target count is reached; thresholding can block high-excess merges. | Current configs have max primitive limits and some threshold-style component-merge gates. | partial | Partial and surrogate. | Define paper lane fields for `target_primitive_count`, `excess_volume_threshold`, threshold units, blocked edge counts, and final stop reason. | Newton should inherit the selected package only after the offline lane records final count and stop reason. | A stopped run is not success unless the report states which target and gates passed. |
| Pairwise component merging when disconnected topology prevents reaching the target. | Current `virtual_pairwise` component-merge diagnostics and synthetic fixtures cover a restricted version. | partial | Paper-shaped but not paper-faithful. | Rebuild component-pair edges inside the paper priority-queue lane with the same cost, threshold, and trace schema as topology edges. | Runtime should only see the resulting package. | Component merging evidence is diagnostic accounting, not broad asset evidence. |
| Postprocessing to remove primitives enclosed by other primitives. | Current reports include containment proxies for assigned points, but there is no paper-faithful enclosed-primitive culling pass. | not_started | Not paper-faithful. | Add pairwise enclosed-primitive checks, cull reasons, and before/after primitive counts in the offline report. | Newton should consume postprocessed packages only after culling is recorded. | Do not claim redundant primitive removal before this pass exists. |
| Evaluation: qualitative simulation similarity, wall-time with many dropped spheres, one-way surface distances, byte cost, primitive/hull comparisons, and CoACD/V-HACD-style baselines. | Repository has Newton smoke diagnostics and workbench reports, but no paper benchmark reproduction. | not_started | Not paper-faithful. | Defer benchmark design until offline paper decomposition is implemented on toy fixtures and then selected small assets. | Newton benchmark tasks are a later phase, not the current offline lane. | No benchmark superiority, collision-quality validation, deployment readiness, or safety certification is supported. |

## Current Surrogates

The current repository has useful surrogates, but each must stay labeled:

- CPD-like face merge: useful for plumbing, not paper collapse.
- Offline objective report: paper-aligned accounting, not paper objective.
- AABB-normalized merge-excess: scale-aware diagnostic cost, not the paper's unnormalized collapse
  cost by itself.
- Candidate weighted-volume tables: current selection explanation, not proof of better primitive
  fitting.
- Cost-guided pairwise and two-step lookahead fixtures: toy merge/search behavior, not paper
  priority-queue optimization.
- Newton contact, drop/settle, and sphere-rain smokes: diagnostic runtime gates, not benchmark
  evaluation.

## Paper-Faithful Offline Lane Criteria

A future lane can be called `paper_faithful_offline` only after it records all of the following
for deterministic synthetic fixtures:

- source mesh, face groups, and preprocessing policy;
- per-face and merged-group `Q` operators with eigen decomposition;
- all six paper primitive fits and containment checks;
- paper collapse cost and weighted volume fields;
- priority-queue collapse trace with stale-entry handling;
- target-count and threshold stop reasons;
- component-pair edge handling when needed;
- enclosed-primitive postprocessing;
- report schema, tests, and dated records.

Until then, use "paper-aligned surrogate", "paper-shaped", or "offline paper-lane planned" wording.

## Newton Entry Rule

The offline paper lane and Newton runtime lane must stay separate:

```text
paper-faithful offline report
-> explicit runtime admissibility check
-> recorded package conversion
-> Newton shape mapping
-> Newton diagnostic smoke
```

Only primitives with recorded Newton mapping should enter Newton directly. Paper primitives without
native Newton support should either remain offline or be converted through an explicitly recorded
approximation policy. That approximation would be a Newton diagnostic adapter, not the paper
primitive itself.

Runtime admissibility means the converted package passes finite center checks, right-handed
orthonormal axis checks where axes are present, positive dimension checks, and the target Newton
shape's expected dimension schema. Passing those checks is still runtime compatibility, not paper
faithfulness.

## Future Benchmark Gate Checklist

Benchmark work should stay blocked until the offline paper lane exists for toy fixtures. When it
starts, the benchmark spec should preserve these paper-side requirements:

- qualitative simulation-similarity review as a correctness signal;
- dropped-sphere wall-time task with the paper-scale sphere count and frame window recorded;
- simulator and CPU/GPU/runtime settings recorded rather than assumed interchangeable;
- one-way collider-to-input Hausdorff and Chamfer distances normalized by input bounding-box
  diagonal;
- byte-cost accounting for primitives and hulls;
- primitive and component counts by kind;
- CoACD and V-HACD comparison settings;
- manually chosen target primitive counts or a documented replacement policy.

## Recommended Next Slice

The next implementation slice should be offline only:

1. Add tiny synthetic fixtures for operator, primitive-fit, and collapse-cost audits.
2. Implement or report the paper `Q` and exact paper collapse-cost fields for those fixtures.
3. Keep Newton, bed, Franka, and benchmark work out of scope until the offline lane has a dated
   paper-lane report.
