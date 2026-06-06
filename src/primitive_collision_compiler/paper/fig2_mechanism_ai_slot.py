from __future__ import annotations

import argparse
import hashlib
import time
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml
from PIL import Image, ImageDraw, ImageFont, ImageOps


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MANIFEST = REPO_ROOT / "paper/shared/figures/assets/fig2_mechanism_ai_slots/manifest.yaml"
DEFAULT_OUTPUT = REPO_ROOT / "paper/shared/figures/generated/bed_franka_mechanism_diagnostic.pdf"
FIG2_OUTPUT_SIZE = (2400, 1280)
DETERMINISTIC_PDF_TIME = time.gmtime(0)
REQUIRED_SLOTS = (
    "isolated_target_pass",
    "full_package_fail",
    "mechanism_audit",
)
AI_SLOT_MODE = "visual_composition"
AI_SLOT_RENDERER_PREFIX = "visual_panel"
CLAIM_BOUNDARY = (
    "Fig.2 visual panels explain the recorded mechanism; quantitative evidence remains "
    "in dated Newton diagnostic records, not in generated imagery."
)

TEXT = "#172033"
MUTED = "#5e6a78"
PANEL_STROKE = "#cbd5e1"
GREEN = "#2e7d59"
RED = "#b94b48"
GOLD = "#a76f1b"
BLUE = "#2767a6"


def load_fig2_slot_manifest(manifest_path: str | Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    path = Path(manifest_path)
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if payload.get("figure_id") != "bed_franka_mechanism_diagnostic":
        raise ValueError("Fig.2 manifest must use figure_id: bed_franka_mechanism_diagnostic")
    if payload.get("mode") != AI_SLOT_MODE:
        raise ValueError(f"Fig.2 manifest must use mode: {AI_SLOT_MODE}")
    slots = payload.get("slots")
    if not isinstance(slots, Mapping):
        raise ValueError("Fig.2 manifest missing slots mapping")
    missing = [slot for slot in REQUIRED_SLOTS if slot not in slots]
    if missing:
        raise ValueError(f"Fig.2 manifest missing slots: {', '.join(missing)}")
    for slot_name in REQUIRED_SLOTS:
        slot = slots[slot_name]
        if not isinstance(slot, Mapping):
            raise ValueError(f"Fig.2 slot entry must be a mapping: {slot_name}")
        asset = slot.get("asset")
        if not isinstance(asset, str) or not asset:
            raise ValueError(f"Fig.2 slot missing asset: {slot_name}")
        asset_path = _repo_path(asset)
        if not asset_path.is_file():
            raise FileNotFoundError(asset_path)
        crop_box = slot.get("crop_box_px")
        if crop_box is not None:
            _validate_crop_box(slot_name, crop_box)
        renderer = str(slot.get("renderer", ""))
        if not renderer.startswith(AI_SLOT_RENDERER_PREFIX):
            raise ValueError(f"Fig.2 slot must use visual-panel renderer metadata: {slot_name}")
        if not slot.get("prompt_summary"):
            raise ValueError(f"Fig.2 slot missing prompt summary: {slot_name}")
        if slot.get("replaceable_by_real_render") is not True:
            raise ValueError(f"Fig.2 slot must remain replaceable by real render: {slot_name}")
    claim_boundary = str(payload.get("claim_boundary", ""))
    required_boundary_terms = ("not experimental evidence", "not benchmark evidence")
    if any(term not in claim_boundary for term in required_boundary_terms):
        raise ValueError("Fig.2 manifest claim_boundary must state evidence limits")
    return dict(payload)


def compose_fig2_mechanism_ai_slot(
    output_path: str | Path = DEFAULT_OUTPUT,
    *,
    manifest_path: str | Path = DEFAULT_MANIFEST,
    metrics: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    manifest = load_fig2_slot_manifest(manifest_path)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    image = _draw_figure(manifest, metrics or {})
    png_sidecar = output.with_suffix(".png")
    image.save(png_sidecar)
    image.save(
        output,
        "PDF",
        resolution=300.0,
        creationDate=DETERMINISTIC_PDF_TIME,
        modDate=DETERMINISTIC_PDF_TIME,
        title="bed_franka_mechanism_diagnostic",
        creator="primitive_collision_compiler.paper.fig2_mechanism_ai_slot",
        producer="primitive_collision_compiler.paper.fig2_mechanism_ai_slot",
    )
    slots = manifest["slots"]
    slot_hashes = {
        slot_name: _sha256_file(_repo_path(str(slots[slot_name]["asset"])))
        for slot_name in REQUIRED_SLOTS
    }
    return {
        "mode": AI_SLOT_MODE,
        "composer": "primitive_collision_compiler.paper.fig2_mechanism_ai_slot",
        "manifest": _portable_manifest_path(Path(manifest_path)),
        "png_sidecar": _portable_manifest_path(png_sidecar),
        "output_size_px": list(FIG2_OUTPUT_SIZE),
        "slot_sha256": slot_hashes,
        "slot_prompt_summary": {
            slot_name: str(slots[slot_name]["prompt_summary"]) for slot_name in REQUIRED_SLOTS
        },
        "claim_boundary": manifest.get("claim_boundary", CLAIM_BOUNDARY),
        "replaceable_by_real_render": list(manifest.get("replaceable_by_real_render", [])),
    }


def _draw_figure(manifest: Mapping[str, Any], metrics: Mapping[str, Any]) -> Image.Image:
    width, height = FIG2_OUTPUT_SIZE
    canvas = Image.new("RGB", (width, height), "#f7f9fc")
    draw = ImageDraw.Draw(canvas)
    _draw_background(draw, width, height)

    draw.text((92, 56), "Package context flips a plausible primitive", font=_font(58, True), fill=TEXT)
    draw.text(
        (96, 130),
        "Same candidate shape, different consumed body state, different Newton diagnostic label.",
        font=_font(31),
        fill=MUTED,
    )

    bed_speed = _metric(metrics, "bed_final_speed_mps", 0.082)
    franka_speed = _metric(metrics, "franka_final_speed_mps", 0.00071)
    gate = _metric(metrics, "settle_gate_mps", 0.01)

    card_w = 690
    card_h = 740
    top = 225
    left = 92
    gap = 72
    specs = (
        {
            "slot": "isolated_target_pass",
            "step": "01",
            "title": "Isolated target primitive",
            "status": "PASS",
            "status_text": "shape alone settles",
            "color": GREEN,
            "body": (
                "Target cylinder is checked as one body.",
                f"Recorded speed stays below the {gate:.2f} m/s gate.",
            ),
        },
        {
            "slot": "full_package_fail",
            "step": "02",
            "title": "Full bed package",
            "status": "FAIL",
            "status_text": f"residual speed {bed_speed:.3f} m/s",
            "color": RED,
            "body": (
                "The same candidate joins a compound package.",
                "The consumed body state exceeds the settle gate.",
            ),
        },
        {
            "slot": "mechanism_audit",
            "step": "03",
            "title": "Mechanism audit",
            "status": "SUPPORTED",
            "status_text": "COM / inertia sensitivity",
            "color": GOLD,
            "body": (
                "Mass-only and contact/floor-only checks\nare insufficient.",
                "This is a bounded diagnostic,\nnot a broad cylinder claim.",
            ),
        },
    )
    xs = [left + index * (card_w + gap) for index in range(3)]
    for x, spec in zip(xs, specs):
        _draw_card(canvas, draw, (x, top, x + card_w, top + card_h), spec, manifest)

    arrow_y = top + 322
    _connector(draw, (xs[0] + card_w + 16, arrow_y), (xs[1] - 16, arrow_y), "same candidate")
    _connector(draw, (xs[1] + card_w + 16, arrow_y), (xs[2] - 16, arrow_y), "audit")
    _draw_bottom_ribbon(draw, bed_speed=bed_speed, franka_speed=franka_speed, gate=gate)
    return canvas


def _draw_card(
    canvas: Image.Image,
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    spec: Mapping[str, Any],
    manifest: Mapping[str, Any],
) -> None:
    x0, y0, x1, y1 = box
    color = str(spec["color"])
    _rounded(draw, box, 24, "#ffffff", PANEL_STROKE, 3)
    _rounded(draw, (x0, y0, x1, y0 + 102), 24, color, color, 0)
    draw.rectangle((x0, y0 + 75, x1, y0 + 102), fill=color)
    draw.text((x0 + 28, y0 + 25), str(spec["step"]), font=_font(34, True), fill="#ffffff")
    draw.text((x0 + 100, y0 + 24), str(spec["title"]), font=_font(31, True), fill="#ffffff")

    image_box = (x0 + 34, y0 + 132, x1 - 34, y0 + 480)
    slot_path = _repo_path(str(manifest["slots"][str(spec["slot"])]["asset"]))
    _paste_slot(canvas, slot_path, image_box, slot=manifest["slots"][str(spec["slot"])])

    pill = (x0 + 42, y0 + 510, x0 + 220, y0 + 566)
    _rounded(draw, pill, 18, color, color, 0)
    _center_text(draw, ((pill[0] + pill[2]) // 2, (pill[1] + pill[3]) // 2), str(spec["status"]), _font(24, True), "#ffffff")
    draw.text((x0 + 240, y0 + 517), str(spec["status_text"]), font=_font(25, True), fill=color)

    body_y = y0 + 600
    body_font = _font(20)
    for line in spec["body"]:
        text_lines = str(line).splitlines() or [""]
        draw.ellipse((x0 + 50, body_y + 9, x0 + 62, body_y + 21), fill=color)
        for line_index, text_line in enumerate(text_lines):
            draw.text((x0 + 78, body_y), text_line, font=body_font, fill=TEXT)
            body_y += 31 if line_index < len(text_lines) - 1 else 38
        body_y += 4


def _draw_bottom_ribbon(
    draw: ImageDraw.ImageDraw,
    *,
    bed_speed: float,
    franka_speed: float,
    gate: float,
) -> None:
    x0, y0, x1, y1 = (92, 1012, 2308, 1208)
    _rounded(draw, (x0, y0, x1, y1), 26, "#ffffff", "#cbd5e1", 3)
    draw.text((x0 + 34, y0 + 28), "Read this figure as a package-level diagnostic.", font=_font(32, True), fill=TEXT)
    draw.text(
        (x0 + 34, y0 + 82),
        "Primitive geometry is only a candidate; Newton consumes the whole package and checks body state.",
        font=_font(26),
        fill=MUTED,
    )
    chips = (
        (GREEN, "isolated target: pass"),
        (RED, f"bed full package: {bed_speed:.3f} > {gate:.2f} m/s"),
        (BLUE, f"scoped contrast: {franka_speed:.5f} <= {gate:.2f} m/s"),
    )
    cursor = x0 + 34
    for color, label in chips:
        tw, _ = _text_size(label, _font(23, True))
        chip_w = int(tw + 48)
        _rounded(draw, (cursor, y0 + 132, cursor + chip_w, y0 + 176), 17, color, color, 0)
        _center_text(draw, (cursor + chip_w // 2, y0 + 154), label, _font(23, True), "#ffffff")
        cursor += chip_w + 22


def _connector(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], label: str) -> None:
    draw.line((start, end), fill="#536174", width=7)
    x, y = end
    draw.polygon([(x, y), (x - 22, y - 16), (x - 22, y + 16)], fill="#536174")
    mid_x = (start[0] + end[0]) // 2
    _rounded(draw, (mid_x - 82, start[1] - 52, mid_x + 82, start[1] - 14), 14, "#f7f9fc", "#cbd5e1", 2)
    _center_text(draw, (mid_x, start[1] - 34), label, _font(18, True), "#536174")


def _paste_slot(
    canvas: Image.Image,
    path: Path,
    box: tuple[int, int, int, int],
    *,
    slot: Mapping[str, Any],
) -> None:
    source = Image.open(path).convert("RGB")
    crop_box = slot.get("crop_box_px")
    if crop_box is not None:
        source = source.crop(tuple(int(value) for value in crop_box))
    source = _trim_light_border(source)
    frame_size = (box[2] - box[0], box[3] - box[1])
    fitted = ImageOps.contain(source, frame_size, method=Image.Resampling.LANCZOS)
    frame = Image.new("RGB", frame_size, "#ffffff")
    frame.paste(fitted, ((frame.width - fitted.width) // 2, (frame.height - fitted.height) // 2))
    mask = Image.new("L", frame.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, frame.width - 1, frame.height - 1), radius=18, fill=255)
    canvas.paste(frame, box[:2], mask)
    ImageDraw.Draw(canvas).rounded_rectangle(box, radius=18, outline="#cbd5e1", width=2)


def _trim_light_border(source: Image.Image, threshold: int = 246, margin: int = 34) -> Image.Image:
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
    right = min(width, max(xs) + margin)
    bottom = min(height, max(ys) + margin)
    if (right - left) * (bottom - top) > width * height * 0.94:
        return source
    return source.crop((left, top, right, bottom))


def _draw_background(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
    for x in range(0, width, 80):
        draw.line((x, 0, x, height), fill="#edf1f6", width=1)
    for y in range(0, height, 80):
        draw.line((0, y, width, y), fill="#edf1f6", width=1)
    draw.rectangle((0, 0, width - 1, height - 1), outline="#f7f9fc", width=18)


def _rounded(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill: str | None,
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


def _metric(metrics: Mapping[str, Any], key: str, fallback: float) -> float:
    try:
        return float(metrics[key])
    except (KeyError, TypeError, ValueError):
        return fallback


def _validate_crop_box(slot_name: str, crop_box: Any) -> tuple[int, int, int, int]:
    if not isinstance(crop_box, Sequence) or isinstance(crop_box, (str, bytes)):
        raise ValueError(f"Fig.2 crop_box_px must be a four-value sequence: {slot_name}")
    try:
        left, top, right, bottom = (int(value) for value in crop_box)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Fig.2 crop_box_px must contain integer values: {slot_name}") from exc
    if left < 0 or top < 0 or right <= left or bottom <= top:
        raise ValueError(f"Fig.2 crop_box_px has invalid bounds: {slot_name}")
    return left, top, right, bottom


def _repo_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else REPO_ROOT / path


def _portable_manifest_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate ACCV Fig.2 mechanism diagnostic.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    metadata = compose_fig2_mechanism_ai_slot(args.output, manifest_path=args.manifest)
    print(f"bed_franka_mechanism_diagnostic: {args.output}")
    print(f"mode: {metadata['mode']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
