from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from PIL import Image, ImageOps

from primitive_collision_compiler.paper.fig1_franka_rtx_slots import (
    DEFAULT_FRANKA_ASSET_MANIFEST,
    DEFAULT_NEWTON_PYTHON,
    DEFAULT_NEWTON_ROOT,
    DEFAULT_PHASE0_REPORT,
    REPO_ROOT,
    RTX_RENDERER,
    _build_franka_rtx_scene,
    _camera_for_slot,
    _git_commit,
    _installed_version,
    _prepend_pythonpath,
    _render_model_rtx,
    _sha256_file,
    select_franka_articulation_case,
    source_artifact_path,
)


NEWTON_RTX_SUPPLEMENT_RENDERER = RTX_RENDERER
SUPPLEMENT_RTX_CLAIM_BOUNDARY = (
    "Newton RTX supplement scene slots are visual exposition only; not experimental evidence, "
    "not benchmark evidence, not deployment readiness, not whole-robot collision quality, "
    "and not safety certification."
)
SUPPLEMENT_NEWTON_RTX_SLOT_IDS = (
    "supplement_predicate_drop_settle",
    "supplement_predicate_stack_slide",
    "supplement_predicate_sphere_rain",
    "supplement_generated_package_consumption",
    "supplement_compound_body_state_teaching",
    "supplement_franka_link_frames",
    "supplement_franka_source_suppression",
    "supplement_failure_storyboard_bowl",
    "supplement_failure_storyboard_cup_tray",
)
DEFAULT_OUTPUT_DIR = REPO_ROOT / "paper/shared/figures/assets/supplement_ai_slots"
DEFAULT_PANEL_DIR = Path(os.environ.get("PPA_SUPPLEMENT_RTX_PANEL_DIR", "/tmp/ppa_supplement_newton_rtx_panels"))
DEFAULT_SOURCE_ARTIFACT_ROOT = Path(
    os.environ.get("PPA_SUPPLEMENT_SOURCE_ARTIFACT_ROOT", str(REPO_ROOT))
)
RTX_PANEL_SIZE = (620, 620)
SLOT_TILE_SIZE = (620, 760)
FRANKA_SCENE_IDS = {
    "supplement_generated_package_consumption",
    "supplement_franka_link_frames",
    "supplement_franka_source_suppression",
}
GEOMETRIC_SCENE_BUILDERS: dict[str, tuple[str, ...]] = {
    "supplement_predicate_drop_settle": ("initial height", "settle window", "accept terms"),
    "supplement_predicate_stack_slide": ("terminal contact", "lateral drift", "residual speed"),
    "supplement_predicate_sphere_rain": ("probe cloud", "contact bins", "diagnostic label"),
    "supplement_compound_body_state_teaching": ("primitive COM", "package COM", "diagnostic gate"),
    "supplement_failure_storyboard_bowl": ("initial", "final", "metric", "label"),
    "supplement_failure_storyboard_cup_tray": ("cup", "tray", "metric", "label"),
}


def build_supplement_newton_rtx_worker_command(
    *,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    panel_dir: str | Path = DEFAULT_PANEL_DIR,
    source_artifact_root: str | Path = DEFAULT_SOURCE_ARTIFACT_ROOT,
    python_executable: str | Path = DEFAULT_NEWTON_PYTHON,
    newton_root: str | Path = DEFAULT_NEWTON_ROOT,
    phase0_report: str | Path = DEFAULT_PHASE0_REPORT,
    asset_manifest: str | Path = DEFAULT_FRANKA_ASSET_MANIFEST,
    figure_ids: Sequence[str] = SUPPLEMENT_NEWTON_RTX_SLOT_IDS,
) -> tuple[list[str], dict[str, str]]:
    env = os.environ.copy()
    newton_root_path = Path(newton_root)
    env["PPA_SUPPLEMENT_SOURCE_ARTIFACT_ROOT"] = str(source_artifact_root)
    env["PYTHONPATH"] = _prepend_pythonpath(
        [newton_root_path, REPO_ROOT / "src", REPO_ROOT],
        env.get("PYTHONPATH", ""),
    )
    command = [
        str(python_executable),
        "-m",
        "primitive_collision_compiler.paper.supplement_newton_rtx_slots",
        "--worker-render",
        "--output-dir",
        str(output_dir),
        "--panel-dir",
        str(panel_dir),
        "--source-artifact-root",
        str(source_artifact_root),
        "--phase0-report",
        str(phase0_report),
        "--asset-manifest",
        str(asset_manifest),
        "--newton-root",
        str(newton_root_path),
    ]
    for figure_id in figure_ids:
        command.extend(["--figure-id", figure_id])
    return command, env


def render_supplement_newton_rtx_slots_via_worker(
    *,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    panel_dir: str | Path = DEFAULT_PANEL_DIR,
    source_artifact_root: str | Path = DEFAULT_SOURCE_ARTIFACT_ROOT,
    python_executable: str | Path = DEFAULT_NEWTON_PYTHON,
    newton_root: str | Path = DEFAULT_NEWTON_ROOT,
    phase0_report: str | Path = DEFAULT_PHASE0_REPORT,
    asset_manifest: str | Path = DEFAULT_FRANKA_ASSET_MANIFEST,
    figure_ids: Sequence[str] = SUPPLEMENT_NEWTON_RTX_SLOT_IDS,
) -> list[Path]:
    for figure_id in figure_ids:
        command, env = build_supplement_newton_rtx_worker_command(
            output_dir=output_dir,
            panel_dir=panel_dir,
            source_artifact_root=source_artifact_root,
            python_executable=python_executable,
            newton_root=newton_root,
            phase0_report=phase0_report,
            asset_manifest=asset_manifest,
            figure_ids=(figure_id,),
        )
        subprocess.run(command, cwd=REPO_ROOT, env=env, check=True)
    return [Path(output_dir) / f"{figure_id}_slot.png" for figure_id in figure_ids]


def compose_slot_strip(
    panel_assets: Sequence[str | Path],
    *,
    output: str | Path,
    panel_size: tuple[int, int] = SLOT_TILE_SIZE,
) -> Path:
    if not panel_assets:
        raise ValueError("at least one RTX panel is required")
    panels = [Image.open(path).convert("RGB") for path in panel_assets]
    strip = Image.new("RGB", (panel_size[0] * len(panels), panel_size[1]), "#ffffff")
    for index, panel in enumerate(panels):
        tile = Image.new("RGB", panel_size, "#ffffff")
        fitted = ImageOps.contain(panel, panel_size, method=Image.Resampling.LANCZOS)
        tile.paste(fitted, ((panel_size[0] - fitted.width) // 2, (panel_size[1] - fitted.height) // 2))
        strip.paste(tile, (index * panel_size[0], 0))
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    strip.save(output_path)
    return output_path


def write_supplement_newton_rtx_sidecar(
    *,
    figure_id: str,
    output_sidecar: str | Path,
    slot_asset: str | Path,
    panel_assets: Sequence[str | Path],
    newton_root: str | Path,
    newton_commit: str,
    ovrtx_version: str,
    recipe: str,
) -> Path:
    slot_path = Path(slot_asset)
    panel_paths = [Path(path) for path in panel_assets]
    payload = {
        "schema_version": 1,
        "figure_id": figure_id,
        "renderer": NEWTON_RTX_SUPPLEMENT_RENDERER,
        "recipe": recipe,
        "slot_asset": _anonymous_path(slot_path),
        "slot_sha256": _sha256_file(slot_path),
        "slot_composition": {
            "tile_size": list(SLOT_TILE_SIZE),
            "source_panel_size": list(RTX_PANEL_SIZE),
        },
        "panel_count": len(panel_paths),
        "panels": [
            {
                "asset": _anonymous_path(path),
                "sha256": _sha256_file(path),
            }
            for path in panel_paths
        ],
        "newton": {
            "root": "external/newton",
            "commit": newton_commit,
        },
        "rtx": {
            "renderer": NEWTON_RTX_SUPPLEMENT_RENDERER,
            "ovrtx_version": ovrtx_version,
        },
        "claim_boundary": SUPPLEMENT_RTX_CLAIM_BOUNDARY,
    }
    sidecar = Path(output_sidecar)
    sidecar.parent.mkdir(parents=True, exist_ok=True)
    sidecar.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return sidecar


def _worker_render(args: argparse.Namespace) -> int:
    import newton
    import warp as wp

    output_dir = Path(args.output_dir)
    panel_dir = Path(args.panel_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    panel_dir.mkdir(parents=True, exist_ok=True)
    newton_commit = _git_commit(Path(args.newton_root))
    ovrtx_version = _installed_version("ovrtx")
    franka_context: dict[str, Any] | None = None

    for figure_id in args.figure_id:
        if figure_id not in SUPPLEMENT_NEWTON_RTX_SLOT_IDS:
            raise ValueError(f"unknown supplement RTX slot id: {figure_id}")
        if figure_id in FRANKA_SCENE_IDS:
            if franka_context is None:
                franka_context = _load_franka_context(args)
            panel_assets = _render_franka_slot_panels(
                newton=newton,
                wp=wp,
                figure_id=figure_id,
                output_dir=panel_dir,
                context=franka_context,
            )
            recipe = "recorded_franka_smoke_rebuilt_in_newton_viewer_rtx"
        else:
            panel_assets = _render_geometric_slot_panels(
                newton=newton,
                wp=wp,
                figure_id=figure_id,
                output_dir=panel_dir,
            )
            recipe = "newton_primitive_scene_rebuilt_for_supplement_viewer_rtx"
        slot_asset = output_dir / f"{figure_id}_slot.png"
        compose_slot_strip(panel_assets, output=slot_asset)
        sidecar = output_dir / f"{figure_id}_slot.json"
        write_supplement_newton_rtx_sidecar(
            figure_id=figure_id,
            output_sidecar=sidecar,
            slot_asset=slot_asset,
            panel_assets=panel_assets,
            newton_root=args.newton_root,
            newton_commit=newton_commit,
            ovrtx_version=ovrtx_version,
            recipe=recipe,
        )
        print(slot_asset)
    return 0


def _load_franka_context(args: argparse.Namespace) -> dict[str, Any]:
    source_root = Path(args.source_artifact_root)
    report_path = source_artifact_path(args.phase0_report, source_artifact_root=source_root)
    asset_manifest_path = source_artifact_path(args.asset_manifest, source_artifact_root=source_root)
    report = json.loads(report_path.read_text(encoding="utf-8"))
    case = select_franka_articulation_case(report)
    asset_path = source_artifact_path(str(case["local_path"]), source_artifact_root=source_root)
    if not asset_path.is_file():
        raise FileNotFoundError(asset_path)
    return {
        "case": case,
        "asset_path": asset_path,
        "report_path": report_path,
        "asset_manifest_path": asset_manifest_path,
    }


def _render_franka_slot_panels(
    *,
    newton: Any,
    wp: Any,
    figure_id: str,
    output_dir: Path,
    context: Mapping[str, Any],
) -> list[Path]:
    slots = ("asset_intake", "candidate_package", "newton_diagnostics")
    outputs: list[Path] = []
    for index, slot in enumerate(slots):
        builder, _details = _build_franka_rtx_scene(
            newton=newton,
            wp=wp,
            slot=slot,
            case=context["case"],
            asset_path=Path(context["asset_path"]),
        )
        output = output_dir / f"{figure_id}_{index + 1:02d}_{slot}.png"
        _render_model_rtx(
            newton=newton,
            wp=wp,
            builder=builder,
            output=output,
            camera=_supplement_franka_camera(figure_id, slot),
            image_size=RTX_PANEL_SIZE,
        )
        outputs.append(output)
    return outputs


def _render_geometric_slot_panels(
    *,
    newton: Any,
    wp: Any,
    figure_id: str,
    output_dir: Path,
) -> list[Path]:
    labels = GEOMETRIC_SCENE_BUILDERS[figure_id]
    outputs: list[Path] = []
    for index, label in enumerate(labels):
        builder = newton.ModelBuilder(up_axis=newton.Axis.Z)
        _add_scene_ground(builder)
        _GEOMETRIC_RECIPES[figure_id](builder, wp, index)
        output = output_dir / f"{figure_id}_{index + 1:02d}_{_slug(label)}.png"
        _render_model_rtx(
            newton=newton,
            wp=wp,
            builder=builder,
            output=output,
            camera=_camera_for_geometric_scene(figure_id, index),
            image_size=RTX_PANEL_SIZE,
        )
        outputs.append(output)
    return outputs


def _add_scene_ground(builder: Any) -> None:
    builder.add_ground_plane(color=(0.70, 0.72, 0.76))


def _add_box_body(
    builder: Any,
    wp: Any,
    *,
    label: str,
    pos: tuple[float, float, float],
    half_extents: tuple[float, float, float],
    color: tuple[float, float, float],
) -> int:
    body = builder.add_body(xform=wp.transform(p=wp.vec3(*pos), q=wp.quat_identity()), label=label)
    builder.add_shape_box(body, hx=half_extents[0], hy=half_extents[1], hz=half_extents[2], color=color)
    return body


def _add_static_box(
    builder: Any,
    wp: Any,
    *,
    label: str,
    pos: tuple[float, float, float],
    half_extents: tuple[float, float, float],
    color: tuple[float, float, float],
) -> None:
    builder.add_shape_box(
        -1,
        xform=wp.transform(p=wp.vec3(*pos), q=wp.quat_identity()),
        hx=half_extents[0],
        hy=half_extents[1],
        hz=half_extents[2],
        color=color,
        label=label,
    )


def _add_sphere_body(
    builder: Any,
    wp: Any,
    *,
    label: str,
    pos: tuple[float, float, float],
    radius: float,
    color: tuple[float, float, float],
) -> int:
    body = builder.add_body(xform=wp.transform(p=wp.vec3(*pos), q=wp.quat_identity()), label=label)
    builder.add_shape_sphere(body, radius=radius, color=color)
    return body


def _add_static_sphere(
    builder: Any,
    wp: Any,
    *,
    label: str,
    pos: tuple[float, float, float],
    radius: float,
    color: tuple[float, float, float],
) -> None:
    builder.add_shape_sphere(
        -1,
        xform=wp.transform(p=wp.vec3(*pos), q=wp.quat_identity()),
        radius=radius,
        color=color,
        label=label,
    )


def _add_drop_settle(builder: Any, wp: Any, panel: int) -> None:
    if panel == 0:
        _add_box_body(builder, wp, label="elevated_cube", pos=(0.0, 0.0, 0.68), half_extents=(0.18, 0.18, 0.18), color=(0.12, 0.42, 0.82))
        _add_static_box(builder, wp, label="height_ruler", pos=(-0.34, 0.0, 0.38), half_extents=(0.018, 0.018, 0.38), color=(0.86, 0.36, 0.22))
        _add_static_sphere(builder, wp, label="start_marker", pos=(-0.34, 0.0, 0.73), radius=0.035, color=(0.86, 0.36, 0.22))
    elif panel == 1:
        _add_box_body(builder, wp, label="settled_cube", pos=(0.0, 0.0, 0.18), half_extents=(0.18, 0.18, 0.18), color=(0.10, 0.46, 0.76))
        for x in (-0.28, 0.28):
            _add_static_box(builder, wp, label=f"settle_window_{x}", pos=(x, 0.0, 0.08), half_extents=(0.018, 0.30, 0.018), color=(0.18, 0.58, 0.34))
    else:
        _add_box_body(builder, wp, label="accepted_cube", pos=(0.0, -0.02, 0.18), half_extents=(0.18, 0.18, 0.18), color=(0.12, 0.42, 0.82))
        for idx, pos in enumerate(((-0.25, 0.22, 0.21), (0.0, 0.25, 0.34), (0.25, 0.22, 0.21))):
            _add_static_sphere(builder, wp, label=f"accept_term_{idx}", pos=pos, radius=0.055, color=[(0.18, 0.58, 0.34), (0.86, 0.36, 0.22), (0.24, 0.46, 0.80)][idx])


def _add_stack_slide(builder: Any, wp: Any, panel: int) -> None:
    _add_static_box(builder, wp, label="support", pos=(0.0, 0.0, 0.14), half_extents=(0.42, 0.28, 0.14), color=(0.30, 0.47, 0.62))
    if panel == 0:
        _add_sphere_body(builder, wp, label="probe_on_support", pos=(0.0, 0.0, 0.38), radius=0.12, color=(0.86, 0.36, 0.22))
    elif panel == 1:
        for idx, x in enumerate((-0.18, 0.02, 0.24)):
            _add_static_sphere(builder, wp, label=f"drift_trace_{idx}", pos=(x, 0.0, 0.37), radius=0.075, color=(0.86, 0.36, 0.22))
        _add_static_box(builder, wp, label="drift_limit", pos=(0.34, 0.0, 0.39), half_extents=(0.016, 0.23, 0.016), color=(0.70, 0.18, 0.18))
    else:
        _add_sphere_body(builder, wp, label="residual_probe", pos=(0.08, 0.0, 0.39), radius=0.12, color=(0.86, 0.36, 0.22))
        _add_static_box(builder, wp, label="speed_bar", pos=(0.36, 0.0, 0.42), half_extents=(0.20, 0.018, 0.018), color=(0.70, 0.18, 0.18))


def _add_sphere_rain(builder: Any, wp: Any, panel: int) -> None:
    _add_static_box(builder, wp, label="target_body", pos=(0.0, 0.0, 0.16), half_extents=(0.34, 0.22, 0.16), color=(0.26, 0.40, 0.55))
    positions = [(-0.28, -0.18), (-0.08, -0.20), (0.14, -0.18), (-0.20, 0.05), (0.04, 0.05), (0.26, 0.04)]
    for idx, (x, y) in enumerate(positions):
        z = 0.74 - 0.08 * (idx % 3) if panel == 0 else 0.38 + 0.04 * (idx % 2)
        color = (0.18, 0.58, 0.34) if (idx + panel) % 3 else (0.86, 0.36, 0.22)
        _add_static_sphere(builder, wp, label=f"rain_probe_{idx}", pos=(x, y, z), radius=0.055, color=color)
    if panel == 2:
        _add_static_box(builder, wp, label="label_bar", pos=(0.0, 0.34, 0.35), half_extents=(0.34, 0.022, 0.022), color=(0.18, 0.58, 0.34))


def _add_compound_body(builder: Any, wp: Any, panel: int) -> None:
    colors = ((0.12, 0.42, 0.82), (0.86, 0.36, 0.22), (0.18, 0.58, 0.34))
    parts = [(-0.20, 0.0, 0.18, (0.18, 0.16, 0.18)), (0.14, 0.03, 0.20, (0.16, 0.20, 0.20)), (0.02, -0.18, 0.48, (0.12, 0.12, 0.10))]
    for idx, (x, y, z, half) in enumerate(parts):
        _add_box_body(builder, wp, label=f"compound_part_{idx}", pos=(x, y, z), half_extents=half, color=colors[idx])
    if panel == 0:
        for idx, (x, y, z, _half) in enumerate(parts):
            _add_static_sphere(builder, wp, label=f"local_com_{idx}", pos=(x, y, z), radius=0.04, color=(1.0, 0.82, 0.20))
    elif panel == 1:
        _add_static_sphere(builder, wp, label="aggregate_com", pos=(0.00, -0.02, 0.30), radius=0.075, color=(1.0, 0.82, 0.20))
        _add_static_box(builder, wp, label="com_axis", pos=(0.0, -0.02, 0.30), half_extents=(0.34, 0.012, 0.012), color=(1.0, 0.82, 0.20))
    else:
        _add_static_box(builder, wp, label="diagnostic_gate", pos=(0.0, 0.36, 0.22), half_extents=(0.42, 0.025, 0.12), color=(0.18, 0.58, 0.34))


def _add_bowl_storyboard(builder: Any, wp: Any, panel: int) -> None:
    _add_static_box(builder, wp, label="table", pos=(0.0, 0.0, 0.08), half_extents=(0.46, 0.34, 0.08), color=(0.34, 0.39, 0.45))
    if panel in {0, 1}:
        height = 0.32 if panel == 0 else 0.20
        _add_sphere_body(builder, wp, label="bowl_outer", pos=(0.0, 0.0, height), radius=0.23, color=(0.18, 0.38, 0.62))
        _add_static_sphere(builder, wp, label="bowl_opening", pos=(0.0, 0.0, height + 0.06), radius=0.16, color=(0.86, 0.88, 0.90))
    elif panel == 2:
        for idx, x in enumerate((-0.24, -0.08, 0.08, 0.24)):
            _add_static_sphere(builder, wp, label=f"metric_probe_{idx}", pos=(x, 0.02, 0.34), radius=0.05, color=(0.86, 0.36, 0.22))
    else:
        _add_static_box(builder, wp, label="failure_token", pos=(0.0, 0.0, 0.28), half_extents=(0.28, 0.08, 0.16), color=(0.70, 0.18, 0.18))


def _add_cup_tray_storyboard(builder: Any, wp: Any, panel: int) -> None:
    if panel == 0:
        _add_static_box(builder, wp, label="cup_support", pos=(0.0, 0.0, 0.08), half_extents=(0.38, 0.28, 0.08), color=(0.34, 0.39, 0.45))
        body = builder.add_body(xform=wp.transform(p=wp.vec3(0.0, 0.0, 0.36), q=wp.quat_identity()), label="cup")
        builder.add_shape_cylinder(body, radius=0.16, half_height=0.24, color=(0.12, 0.42, 0.82))
    elif panel == 1:
        _add_static_box(builder, wp, label="tray", pos=(0.0, 0.0, 0.12), half_extents=(0.46, 0.30, 0.05), color=(0.16, 0.50, 0.54))
        _add_static_box(builder, wp, label="tray_lip", pos=(0.0, 0.32, 0.20), half_extents=(0.46, 0.035, 0.12), color=(0.16, 0.50, 0.54))
    elif panel == 2:
        _add_static_box(builder, wp, label="support_loss_bar", pos=(0.0, 0.0, 0.22), half_extents=(0.38, 0.026, 0.026), color=(0.70, 0.18, 0.18))
        for idx, x in enumerate((-0.18, 0.0, 0.18)):
            _add_static_sphere(builder, wp, label=f"support_probe_{idx}", pos=(x, 0.02, 0.36), radius=0.055, color=(0.86, 0.36, 0.22))
    else:
        _add_static_box(builder, wp, label="diagnostic_label", pos=(0.0, 0.0, 0.28), half_extents=(0.30, 0.09, 0.16), color=(0.70, 0.18, 0.18))


_GEOMETRIC_RECIPES: dict[str, Callable[[Any, Any, int], None]] = {
    "supplement_predicate_drop_settle": _add_drop_settle,
    "supplement_predicate_stack_slide": _add_stack_slide,
    "supplement_predicate_sphere_rain": _add_sphere_rain,
    "supplement_compound_body_state_teaching": _add_compound_body,
    "supplement_failure_storyboard_bowl": _add_bowl_storyboard,
    "supplement_failure_storyboard_cup_tray": _add_cup_tray_storyboard,
}


def _camera_for_geometric_scene(figure_id: str, panel: int) -> dict[str, Any]:
    if figure_id in {"supplement_failure_storyboard_bowl", "supplement_failure_storyboard_cup_tray"}:
        return {"pos": (-1.15, -1.35, 0.74), "target": (0.0, 0.0, 0.25), "fov": 42.0}
    if figure_id == "supplement_predicate_sphere_rain":
        return {"pos": (-1.10, -1.28, 0.92), "target": (0.0, 0.0, 0.38), "fov": 44.0}
    if figure_id == "supplement_compound_body_state_teaching":
        return {"pos": (-1.20, -1.24, 0.86), "target": (0.0, 0.0, 0.30), "fov": 45.0}
    return {"pos": (-1.12, -1.30, 0.82), "target": (0.0, 0.0, 0.30), "fov": 42.0}


def _supplement_franka_camera(figure_id: str, slot: str) -> dict[str, Any]:
    camera = dict(_camera_for_slot(slot))
    if figure_id == "supplement_franka_link_frames":
        camera["pos"] = (-1.38, -1.05, 1.02)
        camera["target"] = (0.02, 0.0, 0.50)
        camera["fov"] = 48.0
    elif figure_id == "supplement_franka_source_suppression":
        camera["pos"] = (-1.12, -1.48, 0.92)
        camera["target"] = (0.02, 0.0, 0.46)
        camera["fov"] = 46.0
    else:
        camera["fov"] = float(camera.get("fov", 48.0)) + 1.5
    return camera


def _anonymous_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return f"external_artifact/{path.name}"


def _slug(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value.lower()).strip("_")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Newton RTX supplement scene slot images.")
    parser.add_argument("--worker-render", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--panel-dir", type=Path, default=DEFAULT_PANEL_DIR)
    parser.add_argument("--source-artifact-root", type=Path, default=DEFAULT_SOURCE_ARTIFACT_ROOT)
    parser.add_argument("--phase0-report", type=Path, default=DEFAULT_PHASE0_REPORT)
    parser.add_argument("--asset-manifest", type=Path, default=DEFAULT_FRANKA_ASSET_MANIFEST)
    parser.add_argument("--newton-root", type=Path, default=DEFAULT_NEWTON_ROOT)
    parser.add_argument("--python-executable", type=Path, default=DEFAULT_NEWTON_PYTHON)
    parser.add_argument(
        "--figure-id",
        action="append",
        choices=SUPPLEMENT_NEWTON_RTX_SLOT_IDS,
        default=[],
    )
    args = parser.parse_args(argv)
    if not args.figure_id:
        args.figure_id = list(SUPPLEMENT_NEWTON_RTX_SLOT_IDS)
    if args.worker_render:
        return _worker_render(args)
    render_supplement_newton_rtx_slots_via_worker(
        output_dir=args.output_dir,
        panel_dir=args.panel_dir,
        source_artifact_root=args.source_artifact_root,
        python_executable=args.python_executable,
        newton_root=args.newton_root,
        phase0_report=args.phase0_report,
        asset_manifest=args.asset_manifest,
        figure_ids=args.figure_id,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
