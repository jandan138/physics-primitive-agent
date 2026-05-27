# Rendered Fig 2 and Fig 7 Design

## Goal

Replace the current hand-drawn Fig 2 and Fig 7 schematics with deterministic rendered scene figures
plus paper annotations, matching the evidence style established by the rendered Fig 6 collision
probe figure.

## Motivation

Fig 6 now shows rendered collision-probe scenes, while Fig 2 and Fig 7 still use schematic
Matplotlib drawings. That mismatch weakens the visual story. The replacement figures should look
like evidence-bearing renderings while keeping the existing claim boundaries:

- Fig 2 explains package-context sensitivity for the capped bed/Franka cylinder records.
- Fig 7 explains link-aware generated-package consumption for one Franka smoke asset.
- Neither figure should claim whole-robot collision quality, manipulation performance, deployment
  readiness, or safety certification.

## Fig 2 Design

Fig 2 remains a mechanism diagnostic, but the scene panel is rendered instead of drawn.

The rendered scene bundle contains three subscenes:

1. `bed_full_package_fail`: a bed-like support body with the recorded full package context and the
   large flat cylinder highlighted in red.
2. `isolated_target_pass`: the same target cylinder rendered as an isolated primitive on a support
   plane and highlighted in green.
3. `franka_link_local_pass`: a Franka-style link-local package chain with small link-local
   cylinders or boxes highlighted in green.

The paper composer overlays compact labels after rendering:

- `full package fails`
- `0.082 > 0.05 m/s`
- `isolated target passes`
- `Franka link-local package passes`
- `COM/inertia sensitivity supported`

The right-side audit table stays in the paper composer because it is textual evidence, not 3D
geometry. It should preserve the existing rows: isolated target check, full bed package,
contact/floor sole cause, mass-only explanation, and COM/inertia sensitivity.

## Fig 7 Design

Fig 7 remains a generated-package Franka task-smoke visual, but the left scene is rendered instead
of drawn.

The rendered scene bundle contains a Franka-style articulated chain with generated link-local
package primitives attached to the detected links. The meshless `panda_link8` sentinel is colored
amber. A short trajectory marker is rendered as a blue cue.

The paper composer overlays compact labels after rendering:

- `generated link packages`
- `meshless sentinel`
- `short trajectory`
- `task outcome: accept`

The right-side metrics table stays in the paper composer. It should preserve the recorded values:
12 detected links, 12 generated primitives, 0 missing body links, 0 source USD shapes, 66
self-collision filters, and `accept`.

## Renderer Contract

`newton-render` will expose two deterministic paper recipes:

- `mechanism_diagnostic_scene`
- `franka_task_scene`

Each recipe accepts a bundle directory with:

- `meta.yaml`: recipe name, figure id, and camera/readability metadata.
- `scene.json`: structured scene primitives and annotation anchors.

The recipes render PNG panels into ignored `reports/generated/` paths. The main repository then
composes committed PDF figures from those PNGs. If `newton-render` is unavailable and no explicit
`NEWTON_RENDER_ROOT` is configured, the old schematic path remains a fallback. If
`NEWTON_RENDER_ROOT` is explicitly configured and rendering fails, figure generation raises an error.

## Data And Artifacts

The figure data comes from existing records and manifests:

- `docs/records/2026-05-21-cylinder-stability-mechanism-diagnosis.md`
- `docs/records/2026-05-26-link-aware-robot-package-generation.md`
- `docs/records/2026-05-26-generated-package-robot-task-probe.md`
- `assets/manifests/cpd_like_smoke_assets.yaml`
- `assets/manifests/franka_usd_smoke_assets.yaml`

Large raw assets, render bundles, and intermediate PNGs stay ignored under `reports/generated/`.
Only small source code, tests, generated PDF figures, and the manifest are commit-safe.

## Testing

Main repository tests should verify:

- mechanism scene bundle payloads preserve the recorded labels and metrics;
- Franka scene bundle payloads preserve link counts, sentinel labeling, trajectory cue, and metric
  values;
- renderer invocation uses the expected recipe names;
- fallback behavior remains available when `newton-render` is not present;
- composed PDFs are produced with readable panel/table layout.

`newton-render` tests should verify:

- both new recipes load bundle metadata and scene payloads;
- rendered PNGs and JSON sidecars are produced;
- sidecars record the recipe name, readability metadata, and key labels;
- no code path requires committing raw USD assets or render directories.

Visual review must run on the final Fig 2 and Fig 7 PNG previews. A PASS requires recognizable
rendered scene content, readable labels at full text width, no blank panels, no severe crop, and no
claim-boundary wording stronger than the recorded evidence.

## Out Of Scope

- No new Newton experiment reruns.
- No new benchmark superiority claim.
- No photorealism claim.
- No whole-robot Franka quality or manipulation claim.
- No raw or generated asset commits.
