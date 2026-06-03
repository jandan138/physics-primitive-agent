# Fig1 Franka RTX Slots Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Replace ACCV Fig.1 cards 01-03 with real Newton ViewerRTX Franka smoke visuals while preserving ACCV layout and claim boundaries.

**Architecture:** Add a focused `fig1_franka_rtx_slots.py` module with pure manifest/report helpers plus a worker-only RTX render path. Keep Fig.1 composition deterministic in `fig1_ai_slot.py`, and only switch the three visual slot image paths after render sidecars and manifest validation pass.

**Tech Stack:** Python, pytest, YAML manifests, PIL sidecar checks, Newton checkout at `/cpfs/shared/simulation/zhuzihou/dev/newton`, `newton.viewer.ViewerRTX`, OVRTX, ACCV LaTeX.

---

### Task 1: Report Selection And Manifest Contract

**Files:**
- Create: `tests/test_fig1_franka_rtx_slots.py`
- Create: `src/primitive_collision_compiler/paper/fig1_franka_rtx_slots.py`

- [x] **Step 1: Write failing tests for Franka report selection and RTX manifest metadata**

```python
def test_select_franka_articulation_case_requires_link_aware_smoke() -> None:
    report = {
        "articulation_cases": [
            {
                "asset_id": "franka_import_smoke",
                "asset_role": "franka_import_smoke",
                "local_path": "assets/raw/franka.usd",
                "robot_package_result": {
                    "status": "generated",
                    "primitive_or_hull_count": 12,
                    "collision_package": {"primitives": [{"kind": "box"}] * 12},
                    "link_boundary_audit": {
                        "status": "smoke_passed",
                        "metrics": {
                            "link_count": 12,
                            "primitive_count": 12,
                            "cross_link_merge_count": 0,
                            "meshless_link_placeholder_count": 1,
                        },
                    },
                },
            }
        ]
    }
    case = select_franka_articulation_case(report)
    summary = franka_case_summary(case)
    assert summary["asset_role"] == "franka_import_smoke"
    assert summary["link_count"] == 12
    assert summary["primitive_count"] == 12
    assert summary["cross_link_merge_count"] == 0


def test_write_franka_rtx_slot_manifest_requires_three_slots(tmp_path: Path) -> None:
    slot_artifacts = {}
    for slot in FIG1_FRANKA_RTX_SLOT_NAMES:
        png = tmp_path / f"{slot}_franka_rtx.png"
        Image.new("RGB", (64, 48), "#dde6f2").save(png)
        sidecar = tmp_path / f"{slot}_franka_rtx.json"
        sidecar.write_text(
            json.dumps(
                {
                    "slot": slot,
                    "renderer": "newton_viewer_rtx_ovrtx",
                    "claim_boundary": FIG1_FRANKA_RTX_CLAIM_BOUNDARY,
                }
            ),
            encoding="utf-8",
        )
        slot_artifacts[slot] = {"png": png, "sidecar": sidecar}
    manifest_path = write_franka_rtx_slot_manifest(
        output_dir=tmp_path,
        slot_artifacts=slot_artifacts,
        source_report=Path("/source/report.json"),
        source_manifest=Path("/source/franka.yaml"),
        source_artifact_root=Path("/source"),
        newton_root=Path("/newton"),
        newton_commit="abc123",
        ovrtx_version="0.3.0.312915",
    )
    manifest = load_franka_rtx_slot_manifest(manifest_path)
    assert manifest["mode"] == "newton_rtx_franka_render_slots"
    assert manifest["renderer"] == "newton_viewer_rtx_ovrtx"
    assert manifest["newton"]["commit"] == "abc123"
    assert "not whole-robot collision quality" in manifest["claim_boundary"]
```

- [x] **Step 2: Run tests to verify RED**

Run: `PYTHONPATH=$PWD/src:$PWD python -m pytest tests/test_fig1_franka_rtx_slots.py -q`
Expected: FAIL because `fig1_franka_rtx_slots` is missing.

- [x] **Step 3: Implement pure helpers**

Create `fig1_franka_rtx_slots.py` with constants, `source_artifact_path`, `build_franka_rtx_worker_command`, `select_franka_articulation_case`, `franka_case_summary`, `write_franka_rtx_slot_manifest`, and `load_franka_rtx_slot_manifest`.

- [x] **Step 4: Run tests to verify GREEN**

Run: `PYTHONPATH=$PWD/src:$PWD python -m pytest tests/test_fig1_franka_rtx_slots.py -q`
Expected: PASS.

### Task 2: RTX Worker And Visual Slot Generation

**Files:**
- Modify: `src/primitive_collision_compiler/paper/fig1_franka_rtx_slots.py`
- Create generated assets: `paper/shared/figures/assets/fig1_franka_rtx_slots/*.png`, `*.json`, `manifest.yaml`

- [x] **Step 1: Verify environment imports**

Run: `PYTHONPATH=/cpfs/shared/simulation/zhuzihou/dev/newton:$PWD/src:$PWD /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -c "import newton, ovrtx, pyglet; print(newton.__file__, ovrtx.__version__, pyglet.__version__)"`
Expected: prints shared Newton checkout and installed OVRTX/pyglet versions.

- [x] **Step 2: Add a minimal worker-only ViewerRTX smoke path**

Implement `--worker-render` so heavy imports happen only in the worker. The worker should render three 640x420 PNGs: `asset_intake_franka_rtx.png`, `candidate_package_franka_rtx.png`, and `newton_diagnostics_franka_rtx.png`, each with JSON sidecar metadata from the selected Franka smoke case.

- [x] **Step 3: Generate slots from the recorded report root**

Run: `PYTHONPATH=$PWD/src:$PWD python -m primitive_collision_compiler.paper.fig1_franka_rtx_slots --source-artifact-root /cpfs/user/zhuzihou/dev/physics-primitive-agent`
Expected: three slot PNGs, sidecars, and `paper/shared/figures/assets/fig1_franka_rtx_slots/manifest.yaml`.

- [x] **Step 4: Inspect generated PNGs**

Run: `python -m pytest tests/test_fig1_franka_rtx_slots.py -q`
Expected: PASS and manifest points to `newton_viewer_rtx_ovrtx`.

### Task 3: Fig.1 Composer Integration

**Files:**
- Modify: `src/primitive_collision_compiler/paper/fig1_ai_slot.py`
- Modify: `tests/test_fig1_ai_slot.py`
- Modify: `paper/shared/figures/assets/fig1_ai_slots/manifest.yaml`
- Modify: `paper/shared/figures/sources.yaml`
- Generated: `paper/shared/figures/generated/pipeline_schematic_ai_slot.pdf`
- Generated: `paper/shared/figures/generated/pipeline_schematic_ai_slot.png`

- [x] **Step 1: Write failing composer tests for RTX renderer acceptance**

Update tests so hybrid rendered slots may use `newton_viewer_rtx_ovrtx`, and the committed manifest must point cards 01-03 at `fig1_franka_rtx_slots`.

- [x] **Step 2: Run tests to verify RED**

Run: `PYTHONPATH=$PWD/src:$PWD python -m pytest tests/test_fig1_ai_slot.py -q`
Expected: FAIL until `fig1_ai_slot.py` accepts the RTX renderer and manifest paths are updated.

- [x] **Step 3: Update composer validation and manifests**

Allow rendered slot renderers in `{"newton_sensor_tiled_camera", "newton_viewer_rtx_ovrtx"}`. Update Fig.1 manifest and sources note to name the Franka RTX slots and state they are smoke exposition only.

- [x] **Step 4: Regenerate Fig.1**

Run: `PYTHONPATH=$PWD/src:$PWD python -m primitive_collision_compiler.paper.fig1_ai_slot`
Expected: generated Fig.1 PNG/PDF are updated.

### Task 4: ACCV Build And Review

**Files:**
- Potentially modify: `paper/shared/figures/pipeline_schematic.tex`
- Potentially modify: ACCV caption text under `paper/shared/`
- Generated: `paper/venues/accv/build/main.pdf`
- Review note: `docs/records/2026-06-03-fig1-franka-rtx-visual-review.md`

- [x] **Step 1: Build ACCV PDF**

Run: `cd paper && make accv`
Expected: `paper/venues/accv/build/main.pdf` updated without LaTeX errors.

- [x] **Step 2: Render the Fig.1 PDF page and dense crops**

Use `pdftoppm`/PIL crops to inspect the standalone figure and in-paper page. Record exact image paths in the review note.

- [x] **Step 3: Run independent visual review**

Dispatch or run `render-visual-reviewer` on the three RTX slots, standalone Fig.1 PNG, and ACCV page render. Iterate until visible robot, package, diagnostic story, labels, and caption are readable at paper scale.

### Task 5: Verification, Review, Commit, Push

**Files:**
- All modified files from Tasks 1-4

- [x] **Step 1: Run targeted tests**

Run: `PYTHONPATH=$PWD/src:$PWD python -m pytest tests/test_fig1_franka_rtx_slots.py tests/test_fig1_ai_slot.py tests/test_fig1_newton_slots.py tests/test_paper_layout.py -q`
Expected: PASS.

- [x] **Step 2: Run repository checks**

Run: `git diff --check`
Expected: no whitespace errors.

- [x] **Step 3: Request code review**

Use the code review workflow with the worktree diff against `main`; fix Critical/Important findings.

- [x] **Step 4: Commit and fast-forward main**

Commit on the feature branch, fast-forward main after review, and rebuild/verify
the ACCV PDF on main. Push status is reported in the final operator response
rather than pre-claimed in the plan file.
