from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Any, Mapping, Sequence

from PIL import Image, ImageDraw, ImageFont

from primitive_collision_compiler.paper.fig1_franka_rtx_slots import (
    DEFAULT_FRANKA_ASSET_MANIFEST,
    DEFAULT_NEWTON_PYTHON,
    DEFAULT_NEWTON_ROOT,
    DEFAULT_PHASE0_REPORT,
    DEFAULT_SOURCE_ARTIFACT_ROOT,
    REPO_ROOT,
    RTX_RENDERER,
    _build_franka_rtx_scene,
    _camera_for_slot,
    _git_commit,
    _installed_version,
    _prepend_pythonpath,
    _render_model_rtx,
    _sha256_file,
    franka_case_summary,
    select_franka_articulation_case,
    source_artifact_path,
)


DEFAULT_OUTPUT_PNG = REPO_ROOT / "paper/shared/figures/generated/franka_link_aware_rtx_task_scene.png"
DEFAULT_OUTPUT_PDF = REPO_ROOT / "paper/shared/figures/generated/franka_link_aware_rtx_task_scene.pdf"
DEFAULT_SIDECAR = REPO_ROOT / "paper/shared/figures/assets/franka_rtx_task_scene/franka_link_aware_rtx_task_scene.json"
DEFAULT_RAW_RENDER = REPO_ROOT / "paper/shared/figures/assets/franka_rtx_task_scene/franka_link_aware_rtx_task_scene_raw.png"
DEFAULT_VERIFIED_RTX_RENDER = REPO_ROOT / "paper/shared/figures/assets/fig1_franka_rtx_slots/newton_diagnostics_franka_rtx.png"
DEFAULT_VERIFIED_RTX_SIDECAR = REPO_ROOT / "paper/shared/figures/assets/fig1_franka_rtx_slots/newton_diagnostics_franka_rtx.json"
FRANKA_RTX_TASK_CLAIM_BOUNDARY = (
    "Franka RTX task scene is visual context from one recorded smoke asset/package; "
    "not whole-robot collision quality evidence, not contact-operation evidence, "
    "and not manipulation evidence."
)
RAW_RENDER_SIZE = (640, 420)
PLATE_SIZE = (1500, 850)
VERIFIED_RTX_CROP = (120, 72, 568, 372)


def build_franka_rtx_task_worker_command(
    *,
    output_png: str | Path = DEFAULT_OUTPUT_PNG,
    output_pdf: str | Path = DEFAULT_OUTPUT_PDF,
    sidecar: str | Path = DEFAULT_SIDECAR,
    raw_render: str | Path = DEFAULT_RAW_RENDER,
    source_artifact_root: str | Path = DEFAULT_SOURCE_ARTIFACT_ROOT,
    python_executable: str | Path = DEFAULT_NEWTON_PYTHON,
    newton_root: str | Path = DEFAULT_NEWTON_ROOT,
    phase0_report: str | Path = DEFAULT_PHASE0_REPORT,
    asset_manifest: str | Path = DEFAULT_FRANKA_ASSET_MANIFEST,
) -> tuple[list[str], dict[str, str]]:
    env = os.environ.copy()
    newton_root_path = Path(newton_root)
    env["PPA_FRANKA_RTX_TASK_SOURCE_ARTIFACT_ROOT"] = str(source_artifact_root)
    env["PYTHONPATH"] = _prepend_pythonpath(
        [newton_root_path, REPO_ROOT / "src", REPO_ROOT],
        env.get("PYTHONPATH", ""),
    )
    command = [
        str(python_executable),
        "-m",
        "primitive_collision_compiler.paper.franka_rtx_task_scene",
        "--worker-render",
        "--output-png",
        str(output_png),
        "--output-pdf",
        str(output_pdf),
        "--sidecar",
        str(sidecar),
        "--raw-render",
        str(raw_render),
        "--source-artifact-root",
        str(source_artifact_root),
        "--phase0-report",
        str(phase0_report),
        "--asset-manifest",
        str(asset_manifest),
        "--newton-root",
        str(newton_root_path),
    ]
    return command, env


def render_franka_rtx_task_scene_via_worker(
    *,
    output_png: str | Path = DEFAULT_OUTPUT_PNG,
    output_pdf: str | Path = DEFAULT_OUTPUT_PDF,
    sidecar: str | Path = DEFAULT_SIDECAR,
    raw_render: str | Path = DEFAULT_RAW_RENDER,
    source_artifact_root: str | Path = DEFAULT_SOURCE_ARTIFACT_ROOT,
    python_executable: str | Path = DEFAULT_NEWTON_PYTHON,
    newton_root: str | Path = DEFAULT_NEWTON_ROOT,
    phase0_report: str | Path = DEFAULT_PHASE0_REPORT,
    asset_manifest: str | Path = DEFAULT_FRANKA_ASSET_MANIFEST,
) -> Path:
    command, env = build_franka_rtx_task_worker_command(
        output_png=output_png,
        output_pdf=output_pdf,
        sidecar=sidecar,
        raw_render=raw_render,
        source_artifact_root=source_artifact_root,
        python_executable=python_executable,
        newton_root=newton_root,
        phase0_report=phase0_report,
        asset_manifest=asset_manifest,
    )
    subprocess.run(command, cwd=REPO_ROOT, env=env, check=True)
    return Path(output_pdf)


def compose_franka_rtx_task_scene_from_verified_slot(
    *,
    output_png: str | Path = DEFAULT_OUTPUT_PNG,
    output_pdf: str | Path = DEFAULT_OUTPUT_PDF,
    sidecar: str | Path = DEFAULT_SIDECAR,
    verified_rtx_render: str | Path = DEFAULT_VERIFIED_RTX_RENDER,
    verified_rtx_sidecar: str | Path = DEFAULT_VERIFIED_RTX_SIDECAR,
    source_artifact_root: str | Path = DEFAULT_SOURCE_ARTIFACT_ROOT,
    phase0_report: str | Path = DEFAULT_PHASE0_REPORT,
    asset_manifest: str | Path = DEFAULT_FRANKA_ASSET_MANIFEST,
    newton_root: str | Path = DEFAULT_NEWTON_ROOT,
) -> Path:
    source_root = Path(source_artifact_root)
    report_path = source_artifact_path(phase0_report, source_artifact_root=source_root)
    asset_manifest_path = source_artifact_path(asset_manifest, source_artifact_root=source_root)
    render_path = Path(verified_rtx_render)
    if not render_path.is_file():
        raise FileNotFoundError(render_path)
    report = json.loads(report_path.read_text(encoding="utf-8"))
    case = select_franka_articulation_case(report)
    asset_path = source_artifact_path(str(case["local_path"]), source_artifact_root=source_root)
    verified_sidecar_path = Path(verified_rtx_sidecar)
    metadata = _verified_rtx_metadata(verified_sidecar_path, newton_root=Path(newton_root))
    compose_franka_rtx_task_scene_plate(
        raw_render=render_path,
        output_png=output_png,
        output_pdf=output_pdf,
        sidecar=sidecar,
        case=case,
        source_report=report_path,
        source_manifest=asset_manifest_path,
        source_asset=asset_path,
        source_artifact_root=source_root,
        source_rtx_sidecar=verified_sidecar_path,
        newton_root=Path(newton_root),
        newton_commit=metadata["newton_commit"],
        ovrtx_version=metadata["ovrtx_version"],
    )
    return Path(output_pdf)


def franka_rtx_task_summary(case: Mapping[str, Any]) -> dict[str, Any]:
    summary = franka_case_summary(case)
    probe = ((case.get("probe_results") or {}).get("generated_package_robot_task_if_robot") or {})
    metrics = probe.get("metrics", {}) if isinstance(probe, Mapping) else {}
    package_consumption = metrics.get("package_consumption", {}) if isinstance(metrics, Mapping) else {}
    summary.update(
        {
            "missing_body_link_count": int(
                package_consumption.get("missing_body_link_count", 0)
                if isinstance(package_consumption, Mapping)
                else 0
            ),
            "source_usd_shape_count": int(
                package_consumption.get("source_usd_shape_count", 0)
                if isinstance(package_consumption, Mapping)
                else 0
            ),
            "self_collision_filter_pair_count": int(
                package_consumption.get("generated_self_collision_filter_pair_count", 0)
                if isinstance(package_consumption, Mapping)
                else 0
            ),
            "task_outcome": str(probe.get("outcome", "unknown")) if isinstance(probe, Mapping) else "unknown",
            "task_status": str(probe.get("status", "unknown")) if isinstance(probe, Mapping) else "unknown",
            "claim_boundary": FRANKA_RTX_TASK_CLAIM_BOUNDARY,
        }
    )
    return summary


def compose_franka_rtx_task_scene_plate(
    *,
    raw_render: str | Path,
    output_png: str | Path,
    output_pdf: str | Path,
    sidecar: str | Path,
    case: Mapping[str, Any],
    source_report: str | Path,
    source_manifest: str | Path,
    source_asset: str | Path,
    source_artifact_root: str | Path,
    newton_root: str | Path,
    newton_commit: str,
    ovrtx_version: str,
    source_rtx_sidecar: str | Path | None = None,
) -> None:
    raw_path = Path(raw_render)
    png_path = Path(output_png)
    pdf_path = Path(output_pdf)
    sidecar_path = Path(sidecar)
    summary = franka_rtx_task_summary(case)

    canvas = Image.new("RGB", PLATE_SIZE, "#f7f9fc")
    draw = ImageDraw.Draw(canvas)
    _background_grid(draw, PLATE_SIZE)

    title_font = _font(42, bold=True)
    subtitle_font = _font(24)
    badge_font = _font(23, bold=True)
    small_font = _font(19)
    note_font = _font(17)

    draw.text((64, 44), "Franka link-aware task smoke", font=title_font, fill="#172033")
    draw.text(
        (64, 96),
        "RTX visual context for one recorded generated-package consumption smoke",
        font=subtitle_font,
        fill="#53606d",
    )

    render = Image.open(raw_path).convert("RGB")
    render = render.crop(_bounded_crop(render.size, VERIFIED_RTX_CROP))
    render_box = (355, 148, 1145, 678)
    _rounded(draw, (render_box[0] - 2, render_box[1] - 2, render_box[2] + 2, render_box[3] + 2), 22, "#ffffff", "#cfd8e3", 3)
    _paste_contained(canvas, render, render_box)

    badges = (
        (f"{summary['link_count']}/12 links", "#1f66a6"),
        (f"{summary['primitive_count']} boxes", "#2e7d59"),
        (f"{summary['missing_body_link_count']} missing", "#2e7d59"),
        (f"{summary['self_collision_filter_pair_count']} filters", "#293f66"),
        (str(summary["task_outcome"]), "#2e7d59" if summary["task_outcome"] == "accept" else "#b94b48"),
    )
    cursor = 76
    for label, color in badges:
        text_w = int(draw.textlength(label, font=badge_font))
        width = max(178, text_w + 54)
        _rounded(draw, (cursor, 704, cursor + width, 768), 18, "#ffffff", "#d7dee9", 2)
        _rounded(draw, (cursor, 704, cursor + 18, 768), 18, color, color, 0)
        draw.text((cursor + 34, 722), label, font=badge_font, fill=color)
        cursor += width + 24

    draw.text(
        (76, 796),
        "Visual rendering only; evidence remains in dated link-boundary and package-consumption records.",
        font=note_font,
        fill="#6b7280",
    )
    draw.text((1120, 796), RTX_RENDERER, font=small_font, fill="#53606d")

    png_path.parent.mkdir(parents=True, exist_ok=True)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    sidecar_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(png_path)
    canvas.save(pdf_path, "PDF", resolution=300.0)
    _write_sidecar(
        sidecar_path,
        raw_render=raw_path,
        output_png=png_path,
        output_pdf=pdf_path,
        case=case,
        summary=summary,
        source_report=Path(source_report),
        source_manifest=Path(source_manifest),
        source_asset=Path(source_asset),
        source_artifact_root=Path(source_artifact_root),
        source_rtx_sidecar=Path(source_rtx_sidecar) if source_rtx_sidecar is not None else None,
        newton_root=Path(newton_root),
        newton_commit=newton_commit,
        ovrtx_version=ovrtx_version,
    )


def load_franka_rtx_task_sidecar(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("renderer") != RTX_RENDERER:
        raise ValueError(f"Franka RTX task sidecar must use renderer: {RTX_RENDERER}")
    if payload.get("claim_boundary") != FRANKA_RTX_TASK_CLAIM_BOUNDARY:
        raise ValueError("Franka RTX task sidecar has unexpected claim boundary")
    for field in ("raw_render", "output_png", "output_pdf"):
        if not payload.get(field):
            raise ValueError(f"Franka RTX task sidecar missing {field}")
    return payload


def _worker_render(args: argparse.Namespace) -> int:
    import newton
    import warp as wp

    source_root = Path(args.source_artifact_root)
    report_path = source_artifact_path(args.phase0_report, source_artifact_root=source_root)
    asset_manifest_path = source_artifact_path(args.asset_manifest, source_artifact_root=source_root)
    report = json.loads(report_path.read_text(encoding="utf-8"))
    case = select_franka_articulation_case(report)
    asset_path = source_artifact_path(str(case["local_path"]), source_artifact_root=source_root)
    if not asset_path.is_file():
        raise FileNotFoundError(asset_path)

    builder, _details = _build_franka_rtx_scene(newton=newton, wp=wp, slot="newton_diagnostics", case=case, asset_path=asset_path)
    _render_model_rtx(
        newton=newton,
        wp=wp,
        builder=builder,
        output=Path(args.raw_render),
        camera=_camera_for_slot("newton_diagnostics"),
        image_size=RAW_RENDER_SIZE,
    )
    compose_franka_rtx_task_scene_plate(
        raw_render=args.raw_render,
        output_png=args.output_png,
        output_pdf=args.output_pdf,
        sidecar=args.sidecar,
        case=case,
        source_report=report_path,
        source_manifest=asset_manifest_path,
        source_asset=asset_path,
        source_artifact_root=source_root,
        source_rtx_sidecar=None,
        newton_root=Path(args.newton_root),
        newton_commit=_git_commit(Path(args.newton_root)),
        ovrtx_version=_installed_version("ovrtx"),
    )
    print(f"franka_rtx_task_scene: {args.output_pdf}")
    return 0


def _write_sidecar(
    path: Path,
    *,
    raw_render: Path,
    output_png: Path,
    output_pdf: Path,
    case: Mapping[str, Any],
    summary: Mapping[str, Any],
    source_report: Path,
    source_manifest: Path,
    source_asset: Path,
    source_artifact_root: Path,
    source_rtx_sidecar: Path | None,
    newton_root: Path,
    newton_commit: str,
    ovrtx_version: str,
) -> None:
    payload = {
        "schema_version": 1,
        "figure_id": "franka_link_aware_rtx_task_scene",
        "renderer": RTX_RENDERER,
        "raw_render": _artifact_path_value(raw_render),
        "raw_render_sha256": _maybe_sha256(raw_render),
        "output_png": _artifact_path_value(output_png),
        "output_png_sha256": _maybe_sha256(output_png),
        "output_pdf": _artifact_path_value(output_pdf),
        "output_pdf_sha256": _maybe_sha256(output_pdf),
        "asset_id": case.get("asset_id", ""),
        "asset_role": case.get("asset_role", ""),
        "summary": dict(summary),
        "source_rtx_sidecar": _artifact_path_value(source_rtx_sidecar) if source_rtx_sidecar else "",
        "source_rtx_sidecar_sha256": _maybe_sha256(source_rtx_sidecar) if source_rtx_sidecar else "",
        "source_report": _source_artifact_path_value(source_report, source_artifact_root=source_artifact_root),
        "source_report_sha256": _maybe_sha256(source_report),
        "source_manifest": _source_artifact_path_value(source_manifest, source_artifact_root=source_artifact_root),
        "source_manifest_sha256": _maybe_sha256(source_manifest),
        "source_asset": _source_artifact_path_value(source_asset, source_artifact_root=source_artifact_root),
        "source_asset_sha256": _maybe_sha256(source_asset),
        "source_artifact_root": _artifact_path_value(source_artifact_root),
        "newton": {"root": _artifact_path_value(newton_root), "commit": newton_commit},
        "rtx": {"renderer": RTX_RENDERER, "ovrtx_version": ovrtx_version},
        "claim_boundary": FRANKA_RTX_TASK_CLAIM_BOUNDARY,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _paste_contained(canvas: Image.Image, image: Image.Image, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    target_w = x1 - x0
    target_h = y1 - y0
    scale = min(target_w / image.width, target_h / image.height)
    new_size = (max(1, int(image.width * scale)), max(1, int(image.height * scale)))
    source = image.resize(new_size, Image.Resampling.LANCZOS)
    paste_x = x0 + (target_w - source.width) // 2
    paste_y = y0 + (target_h - source.height) // 2
    canvas.paste(source, (paste_x, paste_y))


def _bounded_crop(size: tuple[int, int], crop: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    width, height = size
    x0, y0, x1, y1 = crop
    return (
        max(0, min(width - 1, x0)),
        max(0, min(height - 1, y0)),
        max(1, min(width, x1)),
        max(1, min(height, y1)),
    )


def _background_grid(draw: ImageDraw.ImageDraw, size: tuple[int, int]) -> None:
    width, height = size
    for x in range(0, width, 48):
        draw.line((x, 0, x, height), fill="#eef2f7", width=1)
    for y in range(0, height, 48):
        draw.line((0, y, width, y), fill="#eef2f7", width=1)


def _rounded(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill: str,
    outline: str,
    width: int,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def _font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    )
    for name in names:
        path = Path(name)
        if path.is_file():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def _maybe_sha256(path: Path) -> str:
    return _sha256_file(path) if path.is_file() else ""


def _artifact_path_value(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def _source_artifact_path_value(path: Path, *, source_artifact_root: Path) -> str:
    try:
        return path.resolve().relative_to(source_artifact_root.resolve()).as_posix()
    except ValueError:
        return _artifact_path_value(path)


def _verified_rtx_metadata(sidecar: Path, *, newton_root: Path) -> dict[str, str]:
    if sidecar.is_file():
        payload = json.loads(sidecar.read_text(encoding="utf-8"))
        if payload.get("renderer") != RTX_RENDERER:
            raise ValueError(f"verified RTX sidecar must use renderer: {RTX_RENDERER}")
        newton = payload.get("newton") or {}
        rtx = payload.get("rtx") or {}
        return {
            "newton_commit": str(newton.get("commit") or _git_commit(newton_root)),
            "ovrtx_version": str(rtx.get("ovrtx_version") or _installed_version("ovrtx")),
        }
    return {"newton_commit": _git_commit(newton_root), "ovrtx_version": _installed_version("ovrtx")}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate the ACCV Franka RTX task-scene figure.")
    parser.add_argument("--worker-render", action="store_true")
    parser.add_argument("--output-png", type=Path, default=DEFAULT_OUTPUT_PNG)
    parser.add_argument("--output-pdf", type=Path, default=DEFAULT_OUTPUT_PDF)
    parser.add_argument("--sidecar", type=Path, default=DEFAULT_SIDECAR)
    parser.add_argument("--raw-render", type=Path, default=DEFAULT_RAW_RENDER)
    parser.add_argument("--verified-rtx-render", type=Path, default=DEFAULT_VERIFIED_RTX_RENDER)
    parser.add_argument("--verified-rtx-sidecar", type=Path, default=DEFAULT_VERIFIED_RTX_SIDECAR)
    parser.add_argument("--source-artifact-root", type=Path, default=DEFAULT_SOURCE_ARTIFACT_ROOT)
    parser.add_argument("--phase0-report", type=Path, default=DEFAULT_PHASE0_REPORT)
    parser.add_argument("--asset-manifest", type=Path, default=DEFAULT_FRANKA_ASSET_MANIFEST)
    parser.add_argument("--newton-root", type=Path, default=DEFAULT_NEWTON_ROOT)
    parser.add_argument("--python-executable", type=Path, default=DEFAULT_NEWTON_PYTHON)
    args = parser.parse_args(argv)
    if args.worker_render:
        return _worker_render(args)
    output = compose_franka_rtx_task_scene_from_verified_slot(
        output_png=args.output_png,
        output_pdf=args.output_pdf,
        sidecar=args.sidecar,
        verified_rtx_render=args.verified_rtx_render,
        verified_rtx_sidecar=args.verified_rtx_sidecar,
        source_artifact_root=args.source_artifact_root,
        newton_root=args.newton_root,
        phase0_report=args.phase0_report,
        asset_manifest=args.asset_manifest,
    )
    print(f"franka_rtx_task_scene: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
