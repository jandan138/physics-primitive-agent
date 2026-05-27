# Rendered Fig 2 and Fig 7 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace Fig 2 and Fig 7 schematic panels with deterministic rendered scene panels plus paper annotations.

**Architecture:** Add two `newton-render` recipes for deterministic diagnostic scene PNGs, then add main-repo bundle writers and paper composers that call those recipes exactly like the rendered Fig 6 path. Keep all raw assets and intermediate render bundles under ignored `reports/generated/`; commit only code, tests, generated PDF figures, and manifest updates.

**Tech Stack:** Python, pytest, Matplotlib, `newton-render` CLI, existing `primitive_collision_compiler.paper.accv_visuals` figure-generation pipeline.

---

## File Structure

Main repository worktree:

- Modify: `src/primitive_collision_compiler/paper/accv_visuals.py`
  - Add payload and bundle writers for `mechanism_diagnostic_scene` and `franka_task_scene`.
  - Add renderer invocation helpers sharing the existing `NEWTON_RENDER_ROOT` behavior.
  - Compose rendered PNGs into `bed_franka_mechanism_diagnostic.pdf` and `franka_link_aware_task_scene.pdf`.
  - Preserve existing schematic fallbacks when `newton-render` is unavailable.
- Modify: `tests/test_accv_visuals.py`
  - Add TDD coverage for payloads, bundles, renderer invocations, fallback behavior, and composed PDFs.
- Update generated outputs:
  - `paper/shared/figures/generated/bed_franka_mechanism_diagnostic.pdf`
  - `paper/shared/figures/generated/franka_link_aware_task_scene.pdf`
  - `paper/shared/figures/generated/accv_visuals_manifest.json`

Sibling renderer repository:

- Create: `/cpfs/user/zhuzihou/dev/newton-render/src/newton_render/render/paper_diagnostic_scenes.py`
  - Render mechanism and Franka task diagnostic scenes from `scene.json`.
  - Write `.json` sidecars with recipe, output hash, labels, readability metadata, and claim-boundary note.
- Modify: `/cpfs/user/zhuzihou/dev/newton-render/src/newton_render/figures/engine.py`
  - Dispatch `mechanism_diagnostic_scene` and `franka_task_scene`.
- Test: `/cpfs/user/zhuzihou/dev/newton-render/tests/test_paper_diagnostic_scenes.py`
  - Verify recipe loading, PNG output, sidecar metadata, and label preservation.

---

### Task 1: Add `newton-render` Diagnostic Scene Recipes

**Files:**
- Create: `/cpfs/user/zhuzihou/dev/newton-render/src/newton_render/render/paper_diagnostic_scenes.py`
- Modify: `/cpfs/user/zhuzihou/dev/newton-render/src/newton_render/figures/engine.py`
- Test: `/cpfs/user/zhuzihou/dev/newton-render/tests/test_paper_diagnostic_scenes.py`

- [ ] **Step 1: Write failing renderer tests**

Create `/cpfs/user/zhuzihou/dev/newton-render/tests/test_paper_diagnostic_scenes.py` with tests that build minimal bundles and call the new recipes.

```python
from __future__ import annotations

import json
from pathlib import Path

import yaml
from matplotlib import image as mpimg

from newton_render.compose.bundle import load_figure_bundle
from newton_render.figures.engine import render_figure_entry
from newton_render.render.paper_diagnostic_scenes import (
    render_franka_task_scene,
    render_mechanism_diagnostic_scene,
)


def _write_bundle(tmp_path: Path, recipe: str, scene: dict) -> Path:
    bundle = tmp_path / recipe
    bundle.mkdir()
    (bundle / "meta.yaml").write_text(
        yaml.safe_dump(
            {
                "figure_id": recipe,
                "recipe": recipe,
                "paper_readability": {"annotation_scale": "large_paper_panel"},
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    (bundle / "scene.json").write_text(json.dumps(scene, indent=2, sort_keys=True), encoding="utf-8")
    return bundle


def test_render_mechanism_diagnostic_scene_writes_png_and_sidecar(tmp_path: Path) -> None:
    bundle_dir = _write_bundle(
        tmp_path,
        "mechanism_diagnostic_scene",
        {
            "claim_boundary_note": "Diagnostic rendering; not a new Newton run.",
            "subscenes": [
                {"id": "bed_full_package_fail", "status": "failure", "label": "full package fails"},
                {"id": "isolated_target_pass", "status": "accept", "label": "isolated target passes"},
                {"id": "franka_link_local_pass", "status": "accept", "label": "Franka link-local package passes"},
            ],
            "annotations": [
                {"text": "0.082 > 0.05 m/s", "color": "red"},
                {"text": "COM/inertia sensitivity supported", "color": "amber"},
            ],
        },
    )

    out = tmp_path / "mechanism.png"
    path = render_mechanism_diagnostic_scene(load_figure_bundle(bundle_dir), out)

    sidecar = Path(path).with_suffix(".json")
    assert Path(path).is_file()
    pixels = mpimg.imread(path)
    assert pixels.shape[0] >= 500
    assert pixels.shape[1] >= 700
    assert float(pixels[..., :3].std()) > 0.01
    meta = json.loads(sidecar.read_text(encoding="utf-8"))
    assert meta["recipe"] == "mechanism_diagnostic_scene"
    assert meta["subscene_ids"] == [
        "bed_full_package_fail",
        "isolated_target_pass",
        "franka_link_local_pass",
    ]
    assert "COM/inertia sensitivity supported" in meta["labels"]
    assert meta["claim_boundary_note"] == "Diagnostic rendering; not a new Newton run."


def test_render_franka_task_scene_writes_metrics_and_sentinel_sidecar(tmp_path: Path) -> None:
    bundle_dir = _write_bundle(
        tmp_path,
        "franka_task_scene",
        {
            "claim_boundary_note": "Task-smoke rendering; not whole-robot quality evidence.",
            "links": [
                {"name": "panda_link0", "kind": "normal"},
                {"name": "panda_link8", "kind": "meshless_sentinel"},
                {"name": "panda_rightfinger", "kind": "normal"},
            ],
            "metrics": {
                "detected_links": 12,
                "generated_primitives": 12,
                "missing_body_links": 0,
                "source_usd_shapes": 0,
                "self_collision_filters": 66,
                "task_outcome": "accept",
            },
            "trajectory": {"start": [0.5, 0.75], "end": [0.72, 0.58]},
        },
    )

    out = tmp_path / "franka.png"
    path = render_franka_task_scene(load_figure_bundle(bundle_dir), out)

    sidecar = Path(path).with_suffix(".json")
    assert Path(path).is_file()
    pixels = mpimg.imread(path)
    assert pixels.shape[0] >= 500
    assert pixels.shape[1] >= 700
    assert float(pixels[..., :3].std()) > 0.01
    meta = json.loads(sidecar.read_text(encoding="utf-8"))
    assert meta["recipe"] == "franka_task_scene"
    assert meta["sentinel_links"] == ["panda_link8"]
    assert meta["metrics"]["task_outcome"] == "accept"
    assert meta["paper_readability"]["label_contrast"] == "bold_paper_labels"


def test_engine_dispatches_new_paper_scene_recipes(tmp_path: Path) -> None:
    bundle_dir = _write_bundle(
        tmp_path,
        "franka_task_scene",
        {
            "links": [{"name": "panda_link0", "kind": "normal"}],
            "metrics": {"task_outcome": "accept"},
        },
    )

    result = render_figure_entry(
        {
            "id": "franka_task_scene",
            "bundle": str(bundle_dir),
            "output": str(tmp_path / "out.png"),
            "recipe": "franka_task_scene",
        },
        repo_root=tmp_path,
    )

    assert result["recipe"] == "franka_task_scene"
    assert Path(result["output"]).is_file()
    assert Path(result["metadata"]).is_file()
```

- [ ] **Step 2: Run renderer tests to verify RED**

Run:

```bash
cd /cpfs/user/zhuzihou/dev/newton-render
PYTHONPATH=src python -m pytest tests/test_paper_diagnostic_scenes.py -q
```

Expected: FAIL with `ModuleNotFoundError: No module named 'newton_render.render.paper_diagnostic_scenes'`.

- [ ] **Step 3: Implement the renderer module**

Create `/cpfs/user/zhuzihou/dev/newton-render/src/newton_render/render/paper_diagnostic_scenes.py`. The implementation should:

- load `scene.json` directly from `bundle.root`;
- draw deterministic, non-photorealistic 3D rendered scene geometry with Matplotlib 3D axes,
  cuboid/cylinder mesh surfaces, translucent generated package overlays, and perspective cameras;
- use red for failure, green for accept, amber for meshless sentinel;
- write output metadata with `recipe`, `output_png_sha256`, `labels`, `paper_readability`, and `claim_boundary_note`.

Use this public API:

- `render_mechanism_diagnostic_scene(bundle: FigureBundle, output_path: str | Path, *, style: RenderStyle | None = None) -> str`
- `render_franka_task_scene(bundle: FigureBundle, output_path: str | Path, *, style: RenderStyle | None = None) -> str`

Use these concrete helper boundaries:

```python
def _load_scene_payload(bundle: FigureBundle) -> dict[str, Any]:
    path = bundle.root / "scene.json"
    if not path.is_file():
        raise ValueError(f"{bundle.root}: paper diagnostic scene requires scene.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: scene payload must be a mapping")
    return payload


def _draw_box(ax: Any, center: Sequence[float], half_extents: Sequence[float], *, color: str, alpha: float) -> None:
    # Build eight vertices and six Poly3DCollection faces.


def _draw_cylinder(ax: Any, center: Sequence[float], radius: float, half_height: float, *, color: str, alpha: float) -> None:
    # Draw a low-resolution deterministic cylinder surface with np.meshgrid.


def _write_scene_metadata(output: Path, *, recipe: str, payload: Mapping[str, Any], labels: Sequence[str]) -> None:
    write_output_metadata(
        output,
        {
            "recipe": recipe,
            "output_png": str(output.resolve()),
            "output_png_sha256": sha256_file(output),
            "labels": list(labels),
            "claim_boundary_note": str(payload.get("claim_boundary_note", "")),
            "paper_readability": {
                "tight_crop": True,
                "annotation_scale": "large_paper_panel",
                "label_contrast": "bold_paper_labels",
            },
        },
    )
```

The implementation should set fixed figure size and DPI high enough to satisfy the test dimensions:

```python
fig = plt.figure(figsize=(6.2, 4.1), facecolor="#ffffff")
fig.savefig(out, dpi=180, facecolor="#ffffff", bbox_inches="tight", pad_inches=0.04)
```

- [ ] **Step 4: Add engine dispatch**

Modify `/cpfs/user/zhuzihou/dev/newton-render/src/newton_render/figures/engine.py`:

```python
from newton_render.render.paper_diagnostic_scenes import (
    render_franka_task_scene,
    render_mechanism_diagnostic_scene,
)
```

and add recipe branches before the final unsupported-recipe error:

```python
if recipe == "mechanism_diagnostic_scene":
    path = render_mechanism_diagnostic_scene(bundle, output, style=style)
    sidecar = Path(path).with_suffix(".json")
    return {
        "figure_id": entry.get("id", bundle.figure_id),
        "recipe": recipe,
        "output": path,
        "metadata": str(sidecar.resolve()) if sidecar.is_file() else None,
    }

if recipe == "franka_task_scene":
    path = render_franka_task_scene(bundle, output, style=style)
    sidecar = Path(path).with_suffix(".json")
    return {
        "figure_id": entry.get("id", bundle.figure_id),
        "recipe": recipe,
        "output": path,
        "metadata": str(sidecar.resolve()) if sidecar.is_file() else None,
    }
```

- [ ] **Step 5: Run renderer tests to verify GREEN**

Run:

```bash
cd /cpfs/user/zhuzihou/dev/newton-render
PYTHONPATH=src python -m pytest tests/test_paper_diagnostic_scenes.py tests/test_phase0_probe_scene.py -q
```

Expected: all tests pass.

---

### Task 2: Add Main-Repo Bundle Writers And Renderer Invocation

**Files:**
- Modify: `src/primitive_collision_compiler/paper/accv_visuals.py`
- Modify: `tests/test_accv_visuals.py`

- [ ] **Step 1: Write failing tests for payload and bundle contracts**

Add tests to `tests/test_accv_visuals.py`:

```python
from typing import Any


def _franka_task_report_fixture() -> dict:
    return {
        "articulation_cases": [
            {
                "robot_package_result": {
                    "primitive_or_hull_count": 12,
                    "links": [
                        {"link_path": "/panda/panda_link0", "placeholder_primitive_count": 0},
                        {"link_path": "/panda/panda_link8", "placeholder_primitive_count": 1},
                        {"link_path": "/panda/panda_rightfinger", "placeholder_primitive_count": 0},
                    ],
                    "link_boundary_audit": {"metrics": {"link_count": 12}},
                },
                "probe_results": {
                    "generated_package_robot_task_if_robot": {
                        "outcome": "accept",
                        "metrics": {
                            "package_consumption": {
                                "missing_body_link_count": 0,
                                "source_usd_shape_count": 0,
                                "generated_self_collision_filter_pair_count": 66,
                            }
                        },
                    }
                },
            }
        ]
    }


def test_mechanism_scene_payload_preserves_recorded_metrics() -> None:
    entry = _load_result_entry("bed_franka_cylinder_mechanism")
    payload = accv_visuals._mechanism_scene_payload(entry["metrics"])

    assert [scene["id"] for scene in payload["subscenes"]] == [
        "bed_full_package_fail",
        "isolated_target_pass",
        "franka_link_local_pass",
    ]
    assert payload["annotations"]["bed_speed_label"] == "0.082 > 0.05 m/s"
    assert payload["claim_boundary_note"] == "Diagnostic rendering; not a new Newton run."


def test_franka_task_scene_payload_preserves_consumption_metrics() -> None:
    report = _franka_task_report_fixture()
    payload = accv_visuals._franka_task_scene_payload(report)

    assert payload["metrics"]["detected_links"] == 12
    assert payload["metrics"]["generated_primitives"] == 12
    assert payload["metrics"]["missing_body_links"] == 0
    assert payload["metrics"]["source_usd_shapes"] == 0
    assert payload["metrics"]["self_collision_filters"] == 66
    assert payload["metrics"]["task_outcome"] == "accept"
    assert "panda_link8" in payload["sentinel_links"]


def test_write_paper_scene_bundle_uses_newton_render_contract(tmp_path: Path) -> None:
    yaml = pytest.importorskip("yaml")
    bundle = accv_visuals._write_paper_scene_bundle(
        tmp_path / "bundle",
        figure_id="franka_task_scene",
        recipe="franka_task_scene",
        scene_payload={"links": [], "metrics": {"task_outcome": "accept"}},
    )

    assert (bundle / "meta.yaml").is_file()
    assert (bundle / "scene.json").is_file()
    meta = yaml.safe_load((bundle / "meta.yaml").read_text(encoding="utf-8"))
    assert meta["recipe"] == "franka_task_scene"
    assert meta["figure_id"] == "franka_task_scene"
```

- [ ] **Step 2: Run tests to verify RED**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_accv_visuals.py::test_mechanism_scene_payload_preserves_recorded_metrics tests/test_accv_visuals.py::test_franka_task_scene_payload_preserves_consumption_metrics tests/test_accv_visuals.py::test_write_paper_scene_bundle_uses_newton_render_contract -q
```

Expected: FAIL because helper functions do not exist.

- [ ] **Step 3: Implement payload and bundle helpers**

Add helpers in `src/primitive_collision_compiler/paper/accv_visuals.py` near the existing Fig 6 renderer helpers:

- `_mechanism_scene_payload(metrics: Mapping[str, Any]) -> dict[str, Any]`
- `_franka_task_scene_payload(report: Mapping[str, Any]) -> dict[str, Any]`
- `_write_paper_scene_bundle(bundle_dir: Path, *, figure_id: str, recipe: str, scene_payload: Mapping[str, Any]) -> Path`
- `_run_newton_render_paper_scene(*, newton_render_root: Path, bundle_dir: Path, output_png: Path, recipe: str, python_executable: str | None = None) -> Path`

`_run_newton_render_paper_scene` should call:

```bash
python -m newton_render.cli render-figure --bundle <bundle> --recipe <recipe> --output <png>
```

using the same `PYTHONPATH=<newton-render>/src` environment pattern as `_run_newton_render_phase0_panel`.

Use this behavior:

```python
def _paper_scene_renderer_available(root: Path | None) -> bool:
    return root is not None and (root / "src/newton_render/render/paper_diagnostic_scenes.py").is_file()


def _run_newton_render_paper_scene(
    *,
    newton_render_root: Path,
    bundle_dir: Path,
    output_png: Path,
    recipe: str,
    python_executable: str | None = None,
) -> Path:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root / "src") + os.pathsep + env.get("PYTHONPATH", "")
    cmd = [
        str(python_executable or _newton_render_python_executable()),
        "-m",
        "newton_render.cli",
        "render-figure",
        "--bundle",
        str(bundle_dir),
        "--recipe",
        recipe,
        "--output",
        str(output_png),
    ]
    subprocess.run(cmd, check=True, cwd=root, env=env)
    if not output_png.is_file():
        raise RuntimeError(f"newton-render did not create {output_png}")
    return output_png
```

If `NEWTON_RENDER_ROOT` is explicitly present and rendering fails, re-raise the error. If it is not
explicitly present and rendering is unavailable, use the old schematic fallback.

- [ ] **Step 4: Run targeted tests to verify GREEN**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_accv_visuals.py::test_mechanism_scene_payload_preserves_recorded_metrics tests/test_accv_visuals.py::test_franka_task_scene_payload_preserves_consumption_metrics tests/test_accv_visuals.py::test_write_paper_scene_bundle_uses_newton_render_contract -q
```

Expected: all three tests pass.

---

### Task 3: Compose Fig 2 From A Rendered Scene Panel

**Files:**
- Modify: `src/primitive_collision_compiler/paper/accv_visuals.py`
- Modify: `tests/test_accv_visuals.py`

- [ ] **Step 1: Write failing Fig 2 composition tests**

Add tests:

```python
def test_save_mechanism_diagnostic_from_rendered_panel_creates_pdf(tmp_path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    image = np.ones((240, 420, 3), dtype=np.float32)
    image[:, :, 0] = 0.92
    panel = tmp_path / "mechanism.png"
    plt.imsave(panel, image)

    figure = accv_visuals._save_mechanism_diagnostic_from_rendered_panel(panel, tmp_path, plt)

    assert figure.figure_id == "bed_franka_mechanism_diagnostic"
    assert figure.path.is_file()
    assert "newton-render" in figure.evidence


def test_save_mechanism_diagnostic_invokes_renderer_when_available(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    calls: list[str] = []
    fake_root = tmp_path / "newton-render"
    (fake_root / "src/newton_render/render").mkdir(parents=True)
    (fake_root / "src/newton_render/render/paper_diagnostic_scenes.py").write_text("", encoding="utf-8")

    def fake_run(**kwargs: Any) -> Path:
        calls.append(kwargs["recipe"])
        out = kwargs["output_png"]
        plt.imsave(out, np.ones((100, 160, 3)))
        return out

    monkeypatch.setattr(accv_visuals, "_phase0_newton_render_root", lambda: fake_root)
    monkeypatch.setattr(accv_visuals, "_run_newton_render_paper_scene", fake_run)

    figure = accv_visuals._save_mechanism_diagnostic(tmp_path, plt)

    assert calls == ["mechanism_diagnostic_scene"]
    assert figure.path.is_file()


def test_save_mechanism_diagnostic_falls_back_without_renderer(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    monkeypatch.setattr(accv_visuals, "_phase0_newton_render_root", lambda: None)

    figure = accv_visuals._save_mechanism_diagnostic(tmp_path, plt)

    assert figure.path.is_file()
    assert figure.evidence == "2026-05-22 cylinder mechanism records"


def test_save_mechanism_diagnostic_raises_for_explicit_renderer_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    fake_root = tmp_path / "newton-render"
    (fake_root / "src/newton_render/render").mkdir(parents=True)
    (fake_root / "src/newton_render/render/paper_diagnostic_scenes.py").write_text("", encoding="utf-8")

    monkeypatch.setenv("NEWTON_RENDER_ROOT", str(fake_root))
    monkeypatch.setattr(accv_visuals, "_phase0_newton_render_root", lambda: fake_root)

    def fake_run(**kwargs: Any) -> Path:
        raise RuntimeError("renderer failed")

    monkeypatch.setattr(accv_visuals, "_run_newton_render_paper_scene", fake_run)

    with pytest.raises(RuntimeError, match="renderer failed"):
        accv_visuals._save_mechanism_diagnostic(tmp_path, plt)
```

- [ ] **Step 2: Run Fig 2 tests to verify RED**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_accv_visuals.py::test_save_mechanism_diagnostic_from_rendered_panel_creates_pdf tests/test_accv_visuals.py::test_save_mechanism_diagnostic_invokes_renderer_when_available tests/test_accv_visuals.py::test_save_mechanism_diagnostic_falls_back_without_renderer tests/test_accv_visuals.py::test_save_mechanism_diagnostic_raises_for_explicit_renderer_failure -q
```

Expected: FAIL because `_save_mechanism_diagnostic_from_rendered_panel` does not exist and `_save_mechanism_diagnostic` does not invoke the renderer.

- [ ] **Step 3: Implement Fig 2 rendered composition**

Modify `_save_mechanism_diagnostic` so it:

1. loads the existing mechanism metrics;
2. checks `_phase0_newton_render_root()`;
3. writes an ignored bundle under `reports/generated/accv_paper_scene_bundles/bed_franka_mechanism_diagnostic`;
4. renders `reports/generated/accv_paper_scene_panels/bed_franka_mechanism_diagnostic.png`;
5. composes the rendered panel with the existing audit table using `_save_mechanism_diagnostic_from_rendered_panel`;
6. falls back to `_draw_mechanism_scene` if no renderer is available.

- [ ] **Step 4: Run Fig 2 tests to verify GREEN**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_accv_visuals.py::test_save_mechanism_diagnostic_from_rendered_panel_creates_pdf tests/test_accv_visuals.py::test_save_mechanism_diagnostic_invokes_renderer_when_available tests/test_accv_visuals.py::test_save_mechanism_diagnostic_falls_back_without_renderer tests/test_accv_visuals.py::test_save_mechanism_diagnostic_raises_for_explicit_renderer_failure -q
```

Expected: both tests pass.

---

### Task 4: Compose Fig 7 From A Rendered Scene Panel

**Files:**
- Modify: `src/primitive_collision_compiler/paper/accv_visuals.py`
- Modify: `tests/test_accv_visuals.py`

- [ ] **Step 1: Write failing Fig 7 composition tests**

Add tests:

```python
def test_save_franka_task_scene_from_rendered_panel_creates_pdf(tmp_path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    image = np.ones((240, 420, 3), dtype=np.float32)
    image[:, :, 1] = 0.92
    panel = tmp_path / "franka.png"
    plt.imsave(panel, image)
    report = _franka_task_report_fixture()

    figure = accv_visuals._save_franka_task_scene_from_rendered_panel(report, panel, tmp_path, plt)

    assert figure.figure_id == "franka_link_aware_task_scene"
    assert figure.path.is_file()
    assert "newton-render" in figure.evidence


def test_save_franka_task_scene_invokes_renderer_when_available(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    calls: list[str] = []
    fake_root = tmp_path / "newton-render"
    (fake_root / "src/newton_render/render").mkdir(parents=True)
    (fake_root / "src/newton_render/render/paper_diagnostic_scenes.py").write_text("", encoding="utf-8")

    def fake_run(**kwargs: Any) -> Path:
        calls.append(kwargs["recipe"])
        out = kwargs["output_png"]
        plt.imsave(out, np.ones((100, 160, 3)))
        return out

    monkeypatch.setattr(accv_visuals, "_phase0_newton_render_root", lambda: fake_root)
    monkeypatch.setattr(accv_visuals, "_run_newton_render_paper_scene", fake_run)

    figure = accv_visuals._save_franka_task_scene(_franka_task_report_fixture(), tmp_path, plt)

    assert calls == ["franka_task_scene"]
    assert figure.path.is_file()


def test_save_franka_task_scene_falls_back_without_renderer(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    monkeypatch.setattr(accv_visuals, "_phase0_newton_render_root", lambda: None)

    figure = accv_visuals._save_franka_task_scene(_franka_task_report_fixture(), tmp_path, plt)

    assert figure.path.is_file()
    assert figure.evidence == "link-aware package and generated-package robot task records"


def test_save_franka_task_scene_raises_for_explicit_renderer_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    fake_root = tmp_path / "newton-render"
    (fake_root / "src/newton_render/render").mkdir(parents=True)
    (fake_root / "src/newton_render/render/paper_diagnostic_scenes.py").write_text("", encoding="utf-8")

    monkeypatch.setenv("NEWTON_RENDER_ROOT", str(fake_root))
    monkeypatch.setattr(accv_visuals, "_phase0_newton_render_root", lambda: fake_root)

    def fake_run(**kwargs: Any) -> Path:
        raise RuntimeError("renderer failed")

    monkeypatch.setattr(accv_visuals, "_run_newton_render_paper_scene", fake_run)

    with pytest.raises(RuntimeError, match="renderer failed"):
        accv_visuals._save_franka_task_scene(_franka_task_report_fixture(), tmp_path, plt)
```

- [ ] **Step 2: Run Fig 7 tests to verify RED**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_accv_visuals.py::test_save_franka_task_scene_from_rendered_panel_creates_pdf tests/test_accv_visuals.py::test_save_franka_task_scene_invokes_renderer_when_available tests/test_accv_visuals.py::test_save_franka_task_scene_falls_back_without_renderer tests/test_accv_visuals.py::test_save_franka_task_scene_raises_for_explicit_renderer_failure -q
```

Expected: FAIL because rendered Fig 7 helpers do not exist.

- [ ] **Step 3: Implement Fig 7 rendered composition**

Modify `_save_franka_task_scene` so it:

1. checks `_phase0_newton_render_root()`;
2. writes an ignored bundle under `reports/generated/accv_paper_scene_bundles/franka_link_aware_task_scene`;
3. renders `reports/generated/accv_paper_scene_panels/franka_link_aware_task_scene.png`;
4. composes the rendered panel with the existing package consumption metrics table using `_save_franka_task_scene_from_rendered_panel`;
5. falls back to `_draw_franka_task_schematic` if no renderer is available.

- [ ] **Step 4: Run Fig 7 tests to verify GREEN**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_accv_visuals.py::test_save_franka_task_scene_from_rendered_panel_creates_pdf tests/test_accv_visuals.py::test_save_franka_task_scene_invokes_renderer_when_available tests/test_accv_visuals.py::test_save_franka_task_scene_falls_back_without_renderer tests/test_accv_visuals.py::test_save_franka_task_scene_raises_for_explicit_renderer_failure -q
```

Expected: both tests pass.

---

### Task 5: Generate Figures, Review Visually, And Commit

**Files:**
- Update: `paper/shared/figures/generated/bed_franka_mechanism_diagnostic.pdf`
- Update: `paper/shared/figures/generated/franka_link_aware_task_scene.pdf`
- Update: `paper/shared/figures/generated/accv_visuals_manifest.json`
- Possibly update: `paper/shared/sections/experiments.tex` only if captions need to mention rendered diagnostic scene panels.

- [ ] **Step 1: Run targeted tests**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_accv_visuals.py -q
cd /cpfs/user/zhuzihou/dev/newton-render
PYTHONPATH=src python -m pytest tests/test_paper_diagnostic_scenes.py tests/test_phase0_probe_scene.py -q
```

Expected: all tests pass.

- [ ] **Step 2: Regenerate ACCV visuals and paper**

Run from main repo worktree:

```bash
PYTHONPATH=src python scripts/paper/generate_accv_visuals.py \
  --report /cpfs/user/zhuzihou/dev/physics-primitive-agent/reports/generated/phase0_baseline/phase0_grscenes_rigid_plus_franka_newton_2026-05-26.json \
  --asset-root /cpfs/user/zhuzihou/dev/physics-primitive-agent \
  --output-dir paper/shared/figures/generated
make -C paper accv
```

Expected:

- generated Fig 2 and Fig 7 PDFs update;
- `paper/venues/accv/build/main.pdf` builds successfully;
- ACCV paper remains 13-14 pages.

- [ ] **Step 3: Export visual-review PNG previews**

Run:

```bash
pdftoppm -r 220 -png -singlefile paper/shared/figures/generated/bed_franka_mechanism_diagnostic.pdf /tmp/fig2_rendered_current
pdftoppm -r 220 -png -singlefile paper/shared/figures/generated/franka_link_aware_task_scene.pdf /tmp/fig7_rendered_current
```

Expected:

- `/tmp/fig2_rendered_current.png`
- `/tmp/fig7_rendered_current.png`

- [ ] **Step 4: Use render visual review**

Use `render-visual-reviewer` on both PNG previews. PASS requires:

- rendered scene content is visibly present;
- key labels remain readable at full text width;
- Fig 2 still communicates full-package failure vs isolated/Franka passing context;
- Fig 7 still communicates generated-package consumption and sentinel link;
- no stronger claim wording than the source records support.

- [ ] **Step 5: Run final verification**

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_accv_visuals.py -q
python scripts/validate_docs.py
git diff --check
make -C paper accv
pdfinfo paper/venues/accv/build/main.pdf | rg '^Pages:'
```

Expected:

- tests pass;
- docs validation passes;
- whitespace check emits no output;
- paper build succeeds;
- page count remains 13-14.

- [ ] **Step 6: Commit and push**

Run:

```bash
git status --short
git add src/primitive_collision_compiler/paper/accv_visuals.py tests/test_accv_visuals.py paper/shared/figures/generated/bed_franka_mechanism_diagnostic.pdf paper/shared/figures/generated/franka_link_aware_task_scene.pdf paper/shared/figures/generated/accv_visuals_manifest.json docs/superpowers/plans/2026-05-27-rendered-fig2-fig7.md
git commit -m "Add rendered Fig 2 and Fig 7 diagnostics"
git push -u origin fig2-fig7-rendered-scenes
```

Expected: branch pushed and main-repo `git status --short --branch` clean.

Renderer repo note: `/cpfs/user/zhuzihou/dev/newton-render` currently has no committed history and reports all files as untracked. Record the exact modified renderer files and test status in the final handoff instead of claiming that sibling repository is clean.
