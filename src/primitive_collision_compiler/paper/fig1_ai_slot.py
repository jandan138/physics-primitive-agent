from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml
from PIL import Image, ImageDraw, ImageFont, ImageOps

from primitive_collision_compiler.paper.accv_visuals import FigureOutput


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MANIFEST = REPO_ROOT / "paper/shared/figures/assets/fig1_ai_slots/manifest.yaml"
DEFAULT_OUTPUT = REPO_ROOT / "paper/shared/figures/generated/pipeline_schematic_ai_slot.pdf"
FIG1_OUTPUT_SIZE = (2400, 1180)
REQUIRED_SLOTS = (
    "asset_intake",
    "candidate_package",
    "newton_diagnostics",
    "decision_report",
)
VALID_MANIFEST_MODES = {
    "visual_composition",
    "hybrid_newton_visual_composition",
}
NEWTON_RENDERED_SLOTS = (
    "asset_intake",
    "candidate_package",
    "newton_diagnostics",
)
VALID_NEWTON_RENDERERS = {
    "newton_sensor_tiled_camera",
    "newton_viewer_rtx_ovrtx",
}


def load_fig1_slot_manifest(manifest_path: str | Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    path = Path(manifest_path)
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if payload.get("figure_id") != "pipeline_schematic_ai_slot":
        raise ValueError("Fig.1 manifest must use figure_id: pipeline_schematic_ai_slot")
    mode = payload.get("mode")
    if mode not in VALID_MANIFEST_MODES:
        raise ValueError(
            "Fig.1 manifest must use mode: visual_composition or hybrid_newton_visual_composition"
        )
    slots = payload.get("slots")
    if not isinstance(slots, Mapping):
        raise ValueError("Fig.1 manifest missing slots mapping")
    missing = [slot for slot in REQUIRED_SLOTS if not slots.get(slot)]
    if missing:
        raise ValueError(f"Fig.1 manifest missing slots: {', '.join(missing)}")
    for slot in REQUIRED_SLOTS:
        slot_path = _repo_path(str(slots[slot]))
        if not slot_path.is_file():
            raise FileNotFoundError(slot_path)
    if mode == "hybrid_newton_visual_composition":
        _validate_hybrid_slot_sources(payload)
    return dict(payload)


def compose_fig1_ai_slot(
    manifest_path: str | Path = DEFAULT_MANIFEST,
    output_path: str | Path = DEFAULT_OUTPUT,
) -> FigureOutput:
    manifest = load_fig1_slot_manifest(manifest_path)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    image = _draw_figure(manifest)
    png_sidecar = output.with_suffix(".png")
    image.save(png_sidecar)
    image.save(output, "PDF", resolution=300.0)
    slot_hashes = {
        slot: _sha256_file(_repo_path(str(manifest["slots"][slot]))) for slot in REQUIRED_SLOTS
    }
    mode = str(manifest.get("mode", "visual_composition"))
    metadata = {
        "mode": mode,
        "manifest": str(Path(manifest_path)),
        "png_sidecar": str(png_sidecar),
        "output_size_px": list(FIG1_OUTPUT_SIZE),
        "replaceable_by_real_render": list(manifest.get("replaceable_by_real_render", [])),
        "claim_boundary": manifest.get("claim_boundary", ""),
        "slot_sha256": slot_hashes,
        "slot_sources": dict(manifest.get("slot_sources", {})),
    }
    evidence = (
        "Hybrid Newton protocol schematic; exposition only"
        if mode == "hybrid_newton_visual_composition"
        else "Protocol schematic; exposition only"
    )
    return FigureOutput(
        "pipeline_schematic_ai_slot",
        output,
        evidence,
        renderer_metadata=metadata,
    )


def _validate_hybrid_slot_sources(payload: Mapping[str, Any]) -> None:
    slot_sources = payload.get("slot_sources")
    if not isinstance(slot_sources, Mapping):
        raise ValueError("hybrid Fig.1 manifest missing slot_sources mapping")
    missing = [slot for slot in REQUIRED_SLOTS if slot not in slot_sources]
    if missing:
        raise ValueError(f"hybrid Fig.1 manifest missing slot_sources: {', '.join(missing)}")
    for slot in NEWTON_RENDERED_SLOTS:
        source = slot_sources.get(slot)
        if not isinstance(source, Mapping) or source.get("renderer") not in VALID_NEWTON_RENDERERS:
            valid = ", ".join(sorted(VALID_NEWTON_RENDERERS))
            raise ValueError(f"hybrid Fig.1 slot must use a Newton renderer ({valid}): {slot}")
    decision_source = slot_sources.get("decision_report")
    if not isinstance(decision_source, Mapping):
        raise ValueError("hybrid Fig.1 decision_report slot source must be a mapping")
    renderer = str(decision_source.get("renderer", ""))
    if not renderer:
        raise ValueError("hybrid Fig.1 decision_report slot must preserve renderer metadata")


def _draw_figure(manifest: Mapping[str, Any]) -> Image.Image:
    width, height = FIG1_OUTPUT_SIZE
    image = Image.new("RGB", (width, height), "#f7f9fc")
    draw = ImageDraw.Draw(image)
    _background_grid(draw, width, height)

    panel_w = 475
    panel_h = 785
    top = 120
    left = 92
    gap = 88
    xs = [left + i * (panel_w + gap) for i in range(4)]
    specs = (
        ("01", "Asset intake", "USD provenance + link frames", "#1f66a6", "asset_intake"),
        ("02", "Candidate packages", "link-aware box package", "#2e7d59", "candidate_package"),
        ("03", "Newton diagnostics", "body state, contact, robot", "#b46918", "newton_diagnostics"),
        ("04", "Decision report", "accept, reject, fallback", "#293f66", "decision_report"),
    )
    for x, spec in zip(xs, specs):
        _panel(image, draw, x, top, panel_w, panel_h, spec, manifest)

    center_y = top + 355
    for i, color in enumerate(("#2d6cdf", "#4b9f57", "#c27a1a")):
        _arrow(draw, (xs[i] + panel_w + 20, center_y), (xs[i + 1] - 20, center_y), color)

    _feedback_loop(draw, xs, top, panel_w, panel_h)
    _footer(draw, width, height)
    return image


def _panel(
    canvas: Image.Image,
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    w: int,
    h: int,
    spec: tuple[str, str, str, str, str],
    manifest: Mapping[str, Any],
) -> None:
    number, title, subtitle, color, slot = spec
    _rounded(draw, (x, y, x + w, y + h), 28, "#ffffff", color, 5)
    _rounded(draw, (x, y, x + w, y + 116), 28, color, color, 0)
    draw.rectangle((x, y + 88, x + w, y + 116), fill=color)
    draw.text((x + 28, y + 24), number, font=_font(38, True), fill="#ffffff")
    draw.text((x + 100, y + 25), title, font=_font(30, True), fill="#ffffff")
    draw.text((x + 100, y + 72), subtitle, font=_font(20), fill="#f3f7ff")

    slots = manifest["slots"]
    slot_path = _repo_path(str(slots[slot]))
    image_box = (x + 34, y + 150, x + w - 34, y + 535)
    _paste_slot(canvas, slot_path, image_box)
    for idx, label in enumerate(_badges_for_slot(slot)):
        bx = x + 42 + idx * 142
        by = y + 575
        _rounded(draw, (bx, by, bx + 126, by + 54), 16, "#f8fafc", "#d3dbe8", 2)
        _center_text(draw, (bx + 63, by + 28), label, _font(19, True), color)
    _status_strip(draw, (x + 42, y + 675, x + w - 42, y + 716), color, slot)


def _badges_for_slot(slot: str) -> tuple[str, ...]:
    return {
        "asset_intake": ("scale", "links", "hash"),
        "candidate_package": ("links", "frames", "boxes"),
        "newton_diagnostics": ("drop", "contact", "robot"),
        "decision_report": ("accept", "reject", "fallback"),
    }[slot]


def _status_strip(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], color: str, slot: str) -> None:
    x0, y0, x1, y1 = box
    _rounded(draw, box, 16, "#ffffff", "#d7dee9", 2)
    if slot == "decision_report":
        segments = (("#2e7d59", "accept"), ("#b94b48", "reject"), ("#2d6cdf", "fallback"))
    elif slot == "newton_diagnostics":
        segments = ((color, "named probes"), ("#6c7480", "record settings"))
    elif slot == "candidate_package":
        segments = ((color, "candidate"), ("#6c7480", "not accepted yet"))
    else:
        segments = ((color, "provenance"), ("#6c7480", "body boundaries"))
    cursor = x0 + 12
    for fill, label in segments:
        text_width = int(_text_size(label, _font(17, True))[0])
        seg_w = max(116, text_width + 32)
        _rounded(draw, (cursor, y0 + 7, cursor + seg_w, y1 - 7), 12, fill, fill, 0)
        _center_text(draw, (cursor + seg_w // 2, (y0 + y1) // 2), label, _font(17, True), "#ffffff")
        cursor += seg_w + 10


def _feedback_loop(draw: ImageDraw.ImageDraw, xs: Sequence[int], top: int, panel_w: int, panel_h: int) -> None:
    y = top + panel_h + 54
    start = (xs[-1] + panel_w // 2, top + panel_h + 8)
    end = (xs[1] + panel_w // 2, top + panel_h + 8)
    draw.line((start[0], start[1], start[0], y, end[0], y, end[0], end[1]), fill="#293f66", width=8)
    draw.polygon([(end[0], end[1]), (end[0] - 18, end[1] + 30), (end[0] + 18, end[1] + 30)], fill="#293f66")
    label_box = (xs[1] + 8, y + 28, xs[-1] + panel_w - 8, y + 86)
    _rounded(draw, label_box, 17, "#ffffff", "#293f66", 3)
    _center_text(
        draw,
        ((label_box[0] + label_box[2]) // 2, (label_box[1] + label_box[3]) // 2),
        "diagnostic failures route to fallback or review, then candidates iterate",
        _font(22, True),
        "#293f66",
    )


def _footer(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
    note = "Fig. 1 visuals are exposition only; evidence remains in dated Newton diagnostics and manifests."
    _center_text(draw, (width // 2, height - 38), note, _font(21), "#596372")


def _paste_slot(canvas: Image.Image, path: Path, box: tuple[int, int, int, int]) -> None:
    source = _trim_light_border(Image.open(path).convert("RGB"))
    frame_size = (box[2] - box[0], box[3] - box[1])
    fitted = ImageOps.contain(source, frame_size, method=Image.Resampling.LANCZOS)
    frame = Image.new("RGB", frame_size, "#ffffff")
    frame.paste(fitted, ((frame.width - fitted.width) // 2, (frame.height - fitted.height) // 2))
    mask = Image.new("L", frame.size, 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle((0, 0, frame.width - 1, frame.height - 1), radius=22, fill=255)
    canvas.paste(frame, box[:2], mask)
    ImageDraw.Draw(canvas).rounded_rectangle(box, radius=22, outline="#cad3df", width=2)


def _trim_light_border(source: Image.Image, threshold: int = 248, margin: int = 24) -> Image.Image:
    uniform_trimmed = _trim_uniform_background(source, margin=margin)
    if uniform_trimmed.size != source.size:
        return uniform_trimmed
    width, height = source.size
    pixels = source.load()
    xs: list[int] = []
    ys: list[int] = []
    for y in range(height):
        for x in range(width):
            if min(pixels[x, y]) < threshold:
                xs.append(x)
                ys.append(y)
    if not xs:
        return source
    left = max(0, min(xs) - margin)
    top = max(0, min(ys) - margin)
    right = min(width, max(xs) + 1 + margin)
    bottom = min(height, max(ys) + 1 + margin)
    if left == 0 and top == 0 and right == width and bottom == height:
        return source
    return source.crop((left, top, right, bottom))


def _trim_uniform_background(
    source: Image.Image,
    *,
    tolerance: int = 7,
    min_background_fraction: float = 0.35,
    margin: int = 24,
) -> Image.Image:
    width, height = source.size
    background = source.getpixel((0, 0))
    pixels = source.load()
    xs: list[int] = []
    ys: list[int] = []
    background_pixels = 0
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            if sum(abs(int(pixel[index]) - int(background[index])) for index in range(3)) <= tolerance:
                background_pixels += 1
            else:
                xs.append(x)
                ys.append(y)
    if not xs:
        return source
    background_fraction = background_pixels / float(width * height)
    if background_fraction < min_background_fraction:
        return source
    left = max(0, min(xs) - margin)
    top = max(0, min(ys) - margin)
    right = min(width, max(xs) + 1 + margin)
    bottom = min(height, max(ys) + 1 + margin)
    if (right - left) * (bottom - top) > width * height * 0.92:
        return source
    return source.crop((left, top, right, bottom))


def _background_grid(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
    for x in range(0, width, 80):
        draw.line((x, 0, x, height), fill="#edf1f6", width=1)
    for y in range(0, height, 80):
        draw.line((0, y, width, y), fill="#edf1f6", width=1)
    draw.rectangle((0, 0, width, height), outline="#f7f9fc", width=20)


def _arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str) -> None:
    draw.line((start, end), fill=color, width=8)
    x, y = end
    draw.polygon([(x, y), (x - 24, y - 18), (x - 24, y + 18)], fill=color)


def _rounded(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill: str,
    outline: str | None,
    width: int,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def _center_text(
    draw: ImageDraw.ImageDraw,
    center: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: str,
) -> None:
    tw, th = _text_size(text, font)
    draw.text((center[0] - tw / 2, center[1] - th / 2 - 2), text, font=font, fill=fill)


def _text_size(text: str, font: ImageFont.FreeTypeFont) -> tuple[float, float]:
    bbox = font.getbbox(text)
    return float(bbox[2] - bbox[0]), float(bbox[3] - bbox[1])


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    )
    for candidate in candidates:
        path = Path(candidate)
        if path.is_file():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def _repo_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else REPO_ROOT / path


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate the ACCV Fig.1 hybrid slot schematic.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    figure = compose_fig1_ai_slot(args.manifest, args.output)
    print(f"{figure.figure_id}: {figure.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
