# CPD-Like Newton Baseline Design

Date: 2026-05-14

## Goal

Define a narrow CPD-like baseline track for Newton diagnostic experiments without changing the
project's claim boundary. The track adapts ideas from *Convex Primitive Decomposition for
Collision Detection* as a measurement baseline, not as this project's algorithmic contribution.

The design converts the current judgment into an implementation-ready boundary:

- CPD-like work is a baseline/reproduction layer.
- Newton probes are an independent measurement layer.
- Reports and records preserve unsupported regions, fallback decisions, and environment settings.
- DeepDive-facing claims remain proposal/bootstrap claims until dated records and reports exist.

## Source Intake

The paper PDF has been downloaded locally under `docs/tmp/papers/`; the source metadata is recorded
in [Temporary paper intake](../../tmp/papers/README.md). This PDF is rough source intake, not
canonical project evidence.

Durable wording must come from:

- [Claim Boundaries](../../reference/claim-boundaries.md)
- [DeepDive Message Map](../../deepdive/message-map.md)
- [Evidence Status](../../deepdive/evidence-status.md)

If this baseline becomes a cited project decision, add a dated record under `docs/records/` and
promote a short literature summary into `docs/reference/`.

## Approved Direction

The accepted direction is:

> Build a Newton-native, CPD-inspired restricted primitive baseline and use it to measure whether
> deterministic primitive collision packages expose useful Newton diagnostic failures.

This is not an attempt to claim full paper reproduction in the first milestone. The paper uses a
broader primitive set, Sketchfab-scale asset evaluation, and its own simulation setup. The first
project milestone should instead produce a small, provenance-clear, paired Newton diagnostic
baseline.

## Alternatives Considered

### Option A: Full CPD Paper Reproduction

This would target the full primitive set, paper-scale assets, geometric distance metrics, and
simulation benchmark parity.

Tradeoff: highest academic fidelity, but too large for the current DeepDive bootstrap and likely
to distract from Newton-specific diagnostic value.

### Option B: CPD-Inspired Newton Subset Baseline

This implements a restricted subset: face/component intake, primitive candidates, bottom-up or
component-level merge logic, Newton export, and paired probes against Newton baselines.

Tradeoff: not a full paper reproduction, but it gives fast evidence about the project-specific
question: whether primitive-first outputs can be checked, rejected, and compared in Newton.

### Option C: Skip CPD-Like Work And Start With Newton Checker Only

This builds probes and reports before any primitive decomposition baseline.

Tradeoff: lower algorithmic scope, but the checker would have too little meaningful candidate
output to evaluate beyond bounding primitives and convex hulls.

Recommended option: Option B.

## Architecture

The baseline should be split into three independent layers.

### 1. Geometry And Baseline Layer

Responsible for reading mesh-level inputs, computing face/component metadata, fitting restricted
primitive candidates, and producing a collision package candidate.

Suggested package boundary:

```text
src/primitive_collision_compiler/
  baselines/
    cpd_like/
      __init__.py
      config.py
      fit.py
      merge.py
      package.py
  geometry/
    mesh.py
    adjacency.py
    primitives.py
```

The baseline layer may use deterministic heuristics and CPD-inspired concepts. It must not call
Newton probes internally. It emits data for later checking.

### 2. Newton Measurement Layer

Responsible for converting a collision package candidate into Newton shapes and running named
diagnostic probes.

Suggested package boundary:

```text
src/primitive_collision_compiler/
  newton/
    export.py
    probes.py
    metrics.py
```

The Newton layer consumes a common collision package spec. It should be equally able to run
CPD-like candidates, bounding primitives, single convex hulls, CoACD/V-HACD outputs, and later
repair/fallback outputs.

### 3. Reporting And Record Layer

Responsible for reproducible evidence, not algorithm execution.

Suggested package and repository boundary:

```text
src/primitive_collision_compiler/
  reports/
    schema.py
    render.py

configs/experiments/
  cpd_like_baseline.yaml

docs/records/
  YYYY-MM-DD-cpd-like-baseline-plan.md
  YYYY-MM-DD-cpd-like-run-001.md

reports/
  README.md
  generated/
    cpd_like_baseline/
```

Committed summaries stay as concise Markdown under `reports/` and link to dated records. Large
generated tables, logs, and run artifacts live under `reports/generated/cpd_like_baseline/` and are
not committed.

## Data Contracts

The current `PrimitiveSpec` and `CollisionPackage` dataclasses are sufficient for bootstrap dry
runs, but CPD-like evidence needs richer records. The implementation plan should extend contracts
conservatively rather than replacing them wholesale.

Required fields for baseline evidence:

- asset ID, source path, source hash, unit scale, and normalization notes;
- primitive type, pose, dimensions, and source face/component IDs;
- implemented primitive types and requested primitive types;
- unsupported primitive types, such as frustum or trapezoidal prism in the restricted subset;
- containment status for the points or faces assigned to each primitive;
- excess volume or fitting cost where available;
- fallback target and fallback reason;
- generation status and failure label.

This makes fallback a first-class outcome instead of a hidden failure.

## Phase 0 Scope

The first implementation should be a vertical slice, not a full benchmark.

Minimum useful slice:

- 2-3 provenance-clear assets;
- restricted primitive set: box, sphere, capsule, cylinder;
- explicit unsupported list: frustum and trapezoidal prism;
- one Newton probe first, preferably drop or sphere-rain/contact stress;
- one paired report comparing CPD-like, bounding box or sphere, and single convex hull;
- dependency-gap reporting for CoACD/V-HACD if unavailable.

Expanded Phase 0:

- 5-10 provenance-clear assets;
- drop, stack or slide, and sphere-rain/contact stress probes;
- paired comparison against bounding primitive, single convex hull, and CoACD/V-HACD when
  available;
- failure taxonomy, fallback ratio, generation failure rate, primitive/hull count, step time,
  contact count p95, displacement, and penetration or rest jitter.

## Fairness Rules

Every paired comparison must use:

- the same asset version, hash, scale, origin, and mass/inertia assumptions;
- the same Newton version, solver settings, device, fixed timestep, seed, and probe duration;
- the same inclusion of failed, unsupported, and fallback cases;
- recorded dependency gaps for optional baselines;
- asset-level tables before aggregate summaries.

The report must not compare a cleaned mesh for one method against a raw mesh for another method
unless the cleaning step is recorded and applied to every method.

## Claim Boundaries

Allowed wording:

- "CPD-like primitive decomposition baseline adapted for Newton diagnostic probes."
- "Newton-native restricted primitive subset baseline."
- "Simulation-checked under named Newton probes, settings, assets, and records."
- "Dependency gap recorded for unavailable optional baselines."

Avoid:

- Do not say "we reproduced CPD".
- Do not say "our CPD method".
- Do not say "state-of-the-art primitive decomposition".
- Do not say "benchmark superiority".
- Do not say "deployment-ready compiler".
- Do not say "safety guarantee".
- Do not say "simulation-verified collision correctness".

The current design supports a future implementation plan. It does not itself support any result
claim.

## Newton Source Strategy

Use official Newton source as a sibling checkout, not as vendored code in this repository.

Preferred source:

```text
Repo URL: https://github.com/newton-physics/newton
Local source directory: /cpfs/user/zhuzihou/dev/newton
Environment variable: NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton
```

The implementation should not import by hardcoded absolute path. Use the installed `newton`
package when available, and record `NEWTON_SOURCE_DIR` in configs or run records when the source
checkout is used for editable development.

Newton source, examples, assets, lockfiles, and run outputs must not be copied into this repo. This
repo owns wrappers, configs, diagnostic records, and reports only.

Required Newton environment fields for any run record:

- `newton.repo_url`;
- `newton.install_mode`;
- `newton.source_dir`;
- `newton.git_tag`;
- `newton.git_commit`;
- `newton.package_version`;
- `python_version`;
- `os`;
- `arch`;
- `gpu_model`;
- `nvidia_driver`;
- `cuda_runtime_or_device`;
- `warp_version`;
- `device`;
- `solver`;
- `contact_or_margin_settings`;
- `seed`;
- `headless_or_viewer_mode`.

If source clone or installation fails, record it as a dependency gap. Do not convert dependency
setup failure into an algorithm result.

## Seed Asset Lanes

The first asset set has two lanes: CPD-like rigid-object smoke assets and Newton import compatibility
assets. Keep them separate in manifests, reports, and summaries.

### Bed Dev Smoke Asset

The user-provided bed USD is suitable as a first development smoke asset, not as benchmark evidence
until provenance and normalization metadata are complete.

```text
asset_id: grscenes_bed_0a85b986de35ccfdec7c686d791fd747
role: dev_smoke_rigid_object
raw_path: /cpfs/user/zhuzihou/assets/dedup_workspaces/test0_transitive_apply_parallel/dataset/GRScenes_assets/bed/0a85b986de35ccfdec7c686d791fd747/usd/0a85b986de35ccfdec7c686d791fd747.usd
file_size: 40M
sha256: 1bc5a26ddb2551de4ac7acbc13a39d118beda10db503419da65ce82528322265
known_license_context: GRScenes README advertises cc-by-nc-sa-4.0 for the dataset tree
benchmark_status: excluded_until_provenance_units_bbox_and_conversion_history_are_recorded
```

Use it to expose USD import, scale, mesh intake, primitive budget, and Newton contact/probe issues.
Do not use it as the only headline benchmark asset.

### Robot Import Compatibility Asset

Franka/Panda-style robot USDs are useful for Newton USD/articulation import smoke testing, but they
should not enter the CPD-like primitive decomposition aggregate in the first phase. Articulated
robots add link frames, joints, existing collision authoring, self-collision, controllers, and pose
state, which would confound the rigid-object baseline.

Local candidate:

```text
asset_id: grscenes_franka_import_smoke
role: newton_import_compat_smoke
raw_path: /cpfs/user/zhuzihou/assets/zzh-grscenes/robots/franka/franka.usd
file_size: 78K
sha256: 2bfd004928d4157ca2fdca3e79bcfb913b4008eef3ec16f839ad89314141976b
known_license_context: /cpfs/user/zhuzihou/assets/zzh-grscenes/README.md advertises cc-by-nc-sa-4.0
dependencies: robots/franka/Props/panda_link*.usd and gripper/link USD references
benchmark_status: excluded_from_cpd_like_aggregate
```

Preferred fallback if Franka provenance or references are unclear: create a minimal two-link or
simple gripper USD fixture with explicit provenance and use it only for import compatibility.

Required asset manifest fields before an asset can support evidence:

- `asset_id`;
- `category`;
- `role`;
- `source_dataset_or_repo`;
- `license`;
- `permitted_uses`;
- `raw_path`;
- `committed_status`;
- `sha256`;
- `file_size`;
- `usd_format`;
- `external_dependencies`;
- `conversion_steps`;
- `unit_or_meter_scale`;
- `up_axis`;
- `bbox_dimensions`;
- `origin_orientation_normalization`;
- `mass_inertia_assumption`;
- `asset_split`;
- `task_probes`;
- `baseline_inclusion_or_exclusion_reason`.

## Non-Conflicts With Later Work

This baseline should make later work cleaner if dependencies stay one-way:

- CPD-like baseline emits candidate packages and generation metadata.
- Newton probes consume packages and emit task metrics and failure labels.
- Repair/fallback consumes probe failures and package metadata.
- Task-aware or LLM/VLM components may later propose budgets, priorities, or repairs, but only
  after deterministic baseline evidence exists.

The baseline must not become the only path through the system. Future methods should be compared
through the same package and probe interface.

## Acceptance Criteria For The Spec

This design is ready for implementation planning when the next plan can point to:

- a standalone CPD-like baseline config;
- a common collision package schema;
- a Newton harness that accepts multiple candidate sources;
- a paired report schema with unsupported and fallback fields;
- tests that validate config parsing, report serialization, and claim-safe dry-run behavior.

## Next Step

Write an implementation plan for the minimal vertical slice. The plan should start with contracts,
config loading, and report schema tests before any Newton execution code.
