# Fig.1 Newton Render Slots Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the first three ACCV Fig.1 card images with real Newton-rendered slot PNGs while keeping the fourth AI/report card and the current ACCV figure integration.

**Architecture:** Add a focused Fig.1 renderer module that runs Newton in the external Python environment and writes small committed slot PNGs plus sidecar provenance. Keep deterministic PIL composition in `fig1_ai_slot.py`; update its manifest validation and metadata from pure AI-slot mode to hybrid Newton-rendered exposition. Read ignored raw USD/report inputs from an explicit source-artifact root and record hashes instead of committing those inputs.

**Tech Stack:** Python, pytest, PyYAML, Pillow, Newton `SensorTiledCamera`, Warp raytrace, USD mesh loading via existing ACCV helpers, LaTeX ACCV build.

---

## File Structure

- Create: `src/primitive_collision_compiler/paper/fig1_newton_slots.py`
  - CLI and helpers for building the external Newton worker command, locating source artifacts, rendering three slot images, and writing `manifest.yaml` plus per-slot JSON sidecars.
- Modify: `src/primitive_collision_compiler/paper/fig1_ai_slot.py`
  - Accept hybrid manifest mode, validate first three Newton-rendered slots, and expose hybrid renderer metadata while preserving current layout and output filename.
- Modify: `tests/test_fig1_ai_slot.py`
  - Update manifest/composer expectations to hybrid mode and source/provenance wording.
- Create: `tests/test_fig1_newton_slots.py`
  - Contract tests for command construction, source-artifact resolution, sidecar/manifest schema, and no runtime import dependency on Newton in normal tests.
- Modify: `paper/shared/figures/assets/fig1_ai_slots/manifest.yaml`
  - Point `asset_intake`, `candidate_package`, and `newton_diagnostics` to Newton-rendered slot PNGs; leave `decision_report` as the existing AI/report slot.
- Create: `paper/shared/figures/assets/fig1_newton_slots/asset_intake_newton.png`
- Create: `paper/shared/figures/assets/fig1_newton_slots/candidate_package_newton.png`
- Create: `paper/shared/figures/assets/fig1_newton_slots/newton_diagnostics_newton.png`
- Create: `paper/shared/figures/assets/fig1_newton_slots/manifest.yaml`
- Create: `paper/shared/figures/assets/fig1_newton_slots/*.json`
  - Small sidecars only: input paths, input hashes, Newton checkout hash, renderer recipe, slot purpose, and claim boundary.
- Modify: `paper/shared/figures/sources.yaml`
  - Update Fig.1 status/mode/note/source artifacts to hybrid Newton-rendered slots plus AI report card.
- Modify: `paper/shared/figures/pipeline_schematic.tex`
  - Keep `generated/pipeline_schematic_ai_slot.pdf`; update caption from pure AI-slot wording to hybrid visual-exposition wording.
- Create: `docs/records/2026-06-03-accv-fig1-newton-render-slots.md`
  - Record render inputs, visual review evidence, verification commands, and claim impact.
- Modify: `docs/records/README.md`
  - Add the new record to the index.

---

### Task 1: Add Fig.1 Newton Slot Contract Tests

**Files:**
- Create: `tests/test_fig1_newton_slots.py`
- Modify: `tests/test_fig1_ai_slot.py`

- [ ] **Step 1: Write failing tests for command and manifest contracts**

Add tests that express the public API before implementation:

```python
from pathlib import Path

import yaml

from primitive_collision_compiler.paper.fig1_newton_slots import (
    FIG1_NEWTON_SLOT_NAMES,
    build_newton_slot_worker_command,
    load_newton_slot_manifest,
    source_artifact_path,
    write_newton_slot_manifest,
)


def test_worker_command_uses_external_newton_python_and_pythonpath(tmp_path: Path) -> None:
    command, env = build_newton_slot_worker_command(
        output_dir=tmp_path / "slots",
        source_artifact_root=Path("/source/root"),
        python_executable=Path("/env/bin/python"),
        newton_root=Path("/newton"),
    )

    assert command[:3] == ["/env/bin/python", "-m", "primitive_collision_compiler.paper.fig1_newton_slots"]
    assert "--worker-render" in command
    assert str(tmp_path / "slots") in command
    assert env["PPA_FIG1_SOURCE_ARTIFACT_ROOT"] == "/source/root"
    assert "/newton" in env["PYTHONPATH"].split(":")
```

```python
def test_source_artifact_path_uses_explicit_root_for_ignored_inputs() -> None:
    resolved = source_artifact_path(
        "reports/generated/example.json",
        source_artifact_root=Path("/cpfs/project"),
    )

    assert resolved == Path("/cpfs/project/reports/generated/example.json")
```

```python
def test_write_newton_slot_manifest_requires_three_rendered_slots(tmp_path: Path) -> None:
    sidecars = {}
    for slot in FIG1_NEWTON_SLOT_NAMES:
        png = tmp_path / f"{slot}.png"
        png.write_bytes(b"png bytes")
        sidecar = tmp_path / f"{slot}.json"
        sidecar.write_text('{"slot": "%s", "renderer": "newton_sensor_tiled_camera"}' % slot, encoding="utf-8")
        sidecars[slot] = {"png": png, "sidecar": sidecar}

    manifest_path = write_newton_slot_manifest(
        output_dir=tmp_path,
        slot_artifacts=sidecars,
        source_report=Path("/source/report.json"),
        source_manifest=Path("/source/assets.yaml"),
        newton_root=Path("/newton"),
        newton_commit="abc123",
    )

    manifest = load_newton_slot_manifest(manifest_path)
    assert manifest["mode"] == "newton_render_slots"
    assert set(manifest["slots"]) == set(FIG1_NEWTON_SLOT_NAMES)
    assert "not experimental evidence" in manifest["claim_boundary"]
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
python -m pytest tests/test_fig1_newton_slots.py -q
```

Expected: FAIL with `ModuleNotFoundError` or missing functions in `fig1_newton_slots`.

- [ ] **Step 3: Update existing Fig.1 tests to expect hybrid mode**

Change temporary manifests in `tests/test_fig1_ai_slot.py` from:

```python
"mode": "ai_slot_composition",
```

to:

```python
"mode": "hybrid_newton_ai_slot_composition",
"slot_sources": {
    "asset_intake": {"renderer": "newton_sensor_tiled_camera"},
    "candidate_package": {"renderer": "newton_sensor_tiled_camera"},
    "newton_diagnostics": {"renderer": "newton_sensor_tiled_camera"},
    "decision_report": {"renderer": "built_in_imagegen_slots_plus_deterministic_pil_composition"},
},
```

Update assertions to require:

```python
assert composed.renderer_metadata["mode"] == "hybrid_newton_ai_slot_composition"
assert composed.renderer_metadata["slot_sources"]["asset_intake"]["renderer"] == "newton_sensor_tiled_camera"
assert composed.renderer_metadata["slot_sources"]["decision_report"]["renderer"].startswith("built_in_imagegen")
```

- [ ] **Step 4: Run updated Fig.1 tests to verify hybrid assertions fail**

Run:

```bash
python -m pytest tests/test_fig1_ai_slot.py -q
```

Expected: FAIL because `load_fig1_slot_manifest()` still only accepts `ai_slot_composition`.

---

### Task 2: Implement Normal-Runtime Fig.1 Newton Slot Helpers

**Files:**
- Create: `src/primitive_collision_compiler/paper/fig1_newton_slots.py`

- [ ] **Step 1: Implement constants and pure helpers**

Add a module with these interfaces:

```python
FIG1_NEWTON_SLOT_NAMES = ("asset_intake", "candidate_package", "newton_diagnostics")
DEFAULT_NEWTON_ROOT = Path("/cpfs/shared/simulation/zhuzihou/dev/newton")
DEFAULT_NEWTON_PYTHON = Path("/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python")
DEFAULT_SOURCE_ARTIFACT_ROOT = REPO_ROOT
DEFAULT_OUTPUT_DIR = REPO_ROOT / "paper/shared/figures/assets/fig1_newton_slots"
DEFAULT_PHASE0_REPORT = Path("reports/generated/phase0_baseline/phase0_grscenes_rigid_plus_franka_newton_2026-05-26.json")
DEFAULT_PHASE0_ASSET_MANIFEST = Path("assets/manifests/phase0_assets.yaml")
```

Implement:

```python
def source_artifact_path(path: str | Path, *, source_artifact_root: Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else source_artifact_root / candidate
```

```python
def build_newton_slot_worker_command(... ) -> tuple[list[str], dict[str, str]]:
    env = os.environ.copy()
    env["PPA_FIG1_SOURCE_ARTIFACT_ROOT"] = str(source_artifact_root)
    env["PYTHONPATH"] = _prepend_pythonpath([newton_root, REPO_ROOT], env.get("PYTHONPATH"))
    command = [
        str(python_executable),
        "-m",
        "primitive_collision_compiler.paper.fig1_newton_slots",
        "--worker-render",
        "--output-dir",
        str(output_dir),
        "--source-artifact-root",
        str(source_artifact_root),
        "--phase0-report",
        str(phase0_report),
        "--asset-manifest",
        str(asset_manifest),
        "--newton-root",
        str(newton_root),
    ]
    return command, env
```

- [ ] **Step 2: Implement manifest and sidecar writers**

The writer must output `manifest.yaml` with:

```yaml
schema_version: 1
mode: newton_render_slots
renderer: newton_sensor_tiled_camera
slots:
  asset_intake:
    image: paper/shared/figures/assets/fig1_newton_slots/asset_intake_newton.png
    sidecar: paper/shared/figures/assets/fig1_newton_slots/asset_intake_newton.json
claim_boundary: Newton-rendered Fig.1 slots are visual exposition only; not experimental evidence.
```

- [ ] **Step 3: Run contract tests**

Run:

```bash
python -m pytest tests/test_fig1_newton_slots.py -q
```

Expected: PASS for pure helper tests.

---

### Task 3: Implement Newton Worker Rendering

**Files:**
- Modify: `src/primitive_collision_compiler/paper/fig1_newton_slots.py`

- [ ] **Step 1: Add worker-only imports inside worker functions**

Do not import Newton/Warp at module import time. Import them only from `_worker_render_all()` and lower-level render functions:

```python
def _worker_render_all(args: argparse.Namespace) -> int:
    import newton
    import warp as wp
    from newton.sensors import SensorTiledCamera
```

- [ ] **Step 2: Load the Phase0 bowl case from the source-artifact root**

Use the recorded report at:

```text
reports/generated/phase0_baseline/phase0_grscenes_rigid_plus_franka_newton_2026-05-26.json
```

Select `asset_role == "container"` and resolve its `local_path` under the source-artifact root. Use existing `_load_mesh()` from `accv_visuals.py` to load a visual USD mesh with a face cap.

- [ ] **Step 3: Render `asset_intake` from the source USD mesh**

Normalize mesh points for display, convert to Newton mesh:

```python
mesh = newton.Mesh(vertices.astype(np.float32), faces.reshape(-1).astype(np.int32), compute_inertia=False)
body = builder.add_body(xform=wp.transform(p=wp.vec3(0.0, 0.0, z_lift), q=wp.quat_identity()), label="source_mesh")
builder.add_shape_mesh(body, mesh=mesh, color=(0.48, 0.64, 0.82))
```

Render with `SensorTiledCamera` at 640x420 and save `asset_intake_newton.png`.

- [ ] **Step 4: Render `candidate_package` from recorded primitive lanes**

Build a scene with three small lane groups:

```python
lanes = (
    ("BBox", "bounding_primitive", (0.24, 0.48, 0.82)),
    ("CPD", "cpd_style_primitive_candidate_if_available", (0.24, 0.62, 0.42)),
    ("V-HACD", "vhacd_if_available", (0.83, 0.55, 0.22)),
)
```

For boxes use `builder.add_shape_box()`. For convex meshes use `newton.Mesh(vertices, faces_flat, compute_inertia=False)` and `builder.add_shape_mesh()`. Limit high-count lanes to representative first 3 primitives and record the full primitive count in the sidecar.

- [ ] **Step 5: Render `newton_diagnostics` from recorded package/probe reconstruction**

Use the bowl `vhacd_if_available` package, the recorded probe result keys, and simple Newton geometry:

```python
builder.add_ground_plane(color=(0.82, 0.84, 0.86))
render representative package primitives
add several small spheres above/in the opening for sphere-rain/contact visual context
add a translucent-looking fallback marker by color choice only; do not claim a new simulation run
```

Record in the sidecar:

```json
{
  "reconstruction_semantics": "visual reconstruction from recorded report/package fields; not a new diagnostic run"
}
```

- [ ] **Step 6: Run the worker manually**

Run:

```bash
PYTHONPATH=/cpfs/shared/simulation/zhuzihou/dev/newton:$PWD \
/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
-m primitive_collision_compiler.paper.fig1_newton_slots \
--worker-render \
--output-dir paper/shared/figures/assets/fig1_newton_slots \
--source-artifact-root /cpfs/user/zhuzihou/dev/physics-primitive-agent
```

Expected: three PNGs plus JSON sidecars and `manifest.yaml` under `paper/shared/figures/assets/fig1_newton_slots/`.

---

### Task 4: Update Fig.1 Composer And Paper Provenance

**Files:**
- Modify: `src/primitive_collision_compiler/paper/fig1_ai_slot.py`
- Modify: `paper/shared/figures/assets/fig1_ai_slots/manifest.yaml`
- Modify: `paper/shared/figures/sources.yaml`
- Modify: `paper/shared/figures/pipeline_schematic.tex`

- [ ] **Step 1: Let the composer accept hybrid mode**

Change manifest validation to allow:

```python
VALID_MANIFEST_MODES = {
    "ai_slot_composition",
    "hybrid_newton_ai_slot_composition",
}
```

Require `slot_sources` in hybrid mode and require first three slots to have `renderer: newton_sensor_tiled_camera`.

- [ ] **Step 2: Preserve layout and update metadata**

Keep the output path:

```python
DEFAULT_OUTPUT = REPO_ROOT / "paper/shared/figures/generated/pipeline_schematic_ai_slot.pdf"
```

Change metadata mode to the manifest mode and include `slot_sources`.

- [ ] **Step 3: Update manifest and paper source text**

Use the generated Newton slot paths in `paper/shared/figures/assets/fig1_ai_slots/manifest.yaml`. Update `sources.yaml` and caption wording to say hybrid Newton-rendered visual slots plus AI/report card, still exposition only.

- [ ] **Step 4: Regenerate Fig.1**

Run:

```bash
python -m primitive_collision_compiler.paper.fig1_ai_slot
```

Expected: regenerated `paper/shared/figures/generated/pipeline_schematic_ai_slot.pdf` and `.png`.

---

### Task 5: Visual Review And Iteration

**Files:**
- Create: `docs/records/2026-06-03-accv-fig1-newton-render-slots.md`
- Modify: `docs/records/README.md`

- [ ] **Step 1: Inspect standalone slot images and composed Fig.1**

Use `view_image` for:

```text
paper/shared/figures/assets/fig1_newton_slots/asset_intake_newton.png
paper/shared/figures/assets/fig1_newton_slots/candidate_package_newton.png
paper/shared/figures/assets/fig1_newton_slots/newton_diagnostics_newton.png
paper/shared/figures/generated/pipeline_schematic_ai_slot.png
```

Expected: target objects visible, no blank images, no severe clipping, and card slot content contained.

- [ ] **Step 2: Dispatch independent visual QA**

Use `render-visual-reviewer` with only image paths and expectations. If verdict is WARN/FAIL, adjust camera/framing/composition and regenerate.

- [ ] **Step 3: Build ACCV PDF and inspect Fig.1 page**

Run:

```bash
make -C paper accv
```

Inspect page 1 of `paper/build/accv-main.pdf` or the generated ACCV PDF path. Expected: Fig.1 readable at paper scale, caption not colliding, no clipping.

- [ ] **Step 4: Write the dated record**

Record:

```md
## Artifacts
- paper/shared/figures/assets/fig1_newton_slots/*.png
- paper/shared/figures/assets/fig1_newton_slots/*.json
- paper/shared/figures/generated/pipeline_schematic_ai_slot.png
- paper/shared/figures/generated/pipeline_schematic_ai_slot.pdf

## Claim Impact
- Does not add new quantitative evidence.
- Replaces three exposition slots with Newton-rendered visuals derived from recorded Phase0 assets/packages.
```

---

### Task 6: Verification, Review, Commit, Push

**Files:**
- All changed files.

- [ ] **Step 1: Run focused tests**

Run:

```bash
python -m pytest tests/test_fig1_newton_slots.py tests/test_fig1_ai_slot.py tests/test_paper_layout.py -q
```

Expected: all pass.

- [ ] **Step 2: Run paper checks**

Run:

```bash
make -C paper check-template-accv
make -C paper accv
```

Expected: both exit 0.

- [ ] **Step 3: Run broad validation**

Run:

```bash
make validate
make test-paper
git diff --check
```

Expected: all exit 0.

- [ ] **Step 4: Dispatch final code/claim-boundary review**

Ask a subagent reviewer to check the full diff for:

```text
unsupported claims, raw asset commits, broken ACCV integration, stale provenance, and tests missing the hybrid contract.
```

Fix any findings and rerun relevant verification.

- [ ] **Step 5: Commit and push**

Run:

```bash
git status --short
git add src/primitive_collision_compiler/paper/fig1_newton_slots.py \
  src/primitive_collision_compiler/paper/fig1_ai_slot.py \
  tests/test_fig1_newton_slots.py \
  tests/test_fig1_ai_slot.py \
  paper/shared/figures/assets/fig1_ai_slots/manifest.yaml \
  paper/shared/figures/assets/fig1_newton_slots \
  paper/shared/figures/generated/pipeline_schematic_ai_slot.pdf \
  paper/shared/figures/generated/pipeline_schematic_ai_slot.png \
  paper/shared/figures/sources.yaml \
  paper/shared/figures/pipeline_schematic.tex \
  docs/records/2026-06-03-accv-fig1-newton-render-slots.md \
  docs/records/README.md \
  docs/superpowers/plans/2026-06-03-fig1-newton-render-slots.md
git commit -m "Add Newton-rendered Fig. 1 slots"
git push origin fig1-newton-render-slots
```

If the branch is clean and verified, merge to `main` and push `main` per the user's previous `commit+push` instruction.

---

## Self-Review

- Spec coverage: the plan covers three Newton-rendered cards, fourth AI/report card preservation, ACCV layout preservation, visual review, claim boundaries, commit, and push.
- Placeholder scan: no task uses TBD/TODO/implement-later language.
- Type consistency: the module names, slot names, and manifest mode are consistent across tasks.
