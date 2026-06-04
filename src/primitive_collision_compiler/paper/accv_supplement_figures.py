from __future__ import annotations

import argparse
import hashlib
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml
from PIL import Image, ImageDraw, ImageFont, ImageOps

from primitive_collision_compiler.paper.supplement_newton_rtx_slots import (
    NEWTON_RTX_SUPPLEMENT_RENDERER,
    SUPPLEMENT_NEWTON_RTX_SLOT_IDS,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "paper/shared/figures/generated/supplement"
DEFAULT_SLOT_MANIFEST = REPO_ROOT / "paper/shared/figures/assets/supplement_ai_slots/manifest.yaml"
CANVAS_SIZE = (1800, 1120)
DETERMINISTIC_PDF_TIME = time.gmtime(0)
PANEL_FILL = "#ffffff"
PANEL_STROKE = "#ccd5e3"
TEXT = "#172033"
MUTED = "#5e6a78"
BLUE = "#2767a6"
GREEN = "#2e7d59"
RED = "#b94b48"
GOLD = "#a76f1b"
PURPLE = "#6b4fa3"
TEAL = "#247f86"
CLAIM_BOUNDARY = (
    "Supplement tutorial visualization only; not benchmark superiority, not deployment "
    "readiness, not whole-robot collision quality, and not safety certification."
)
AI_SLOT_MODE = "ai_slot_composition"
AI_SLOT_RENDERER_PREFIX = "built_in_imagegen"
SCENE_EXPLANATION_FIGURE_IDS = SUPPLEMENT_NEWTON_RTX_SLOT_IDS


@dataclass(frozen=True)
class SupplementFigureSpec:
    figure_id: str
    title: str
    subtitle: str
    kind: str
    panels: tuple[str, ...]
    shows: str
    does_not_show: str
    source_records: tuple[str, ...]
    claim_boundary: str = CLAIM_BOUNDARY


FIGURE_SPECS: tuple[SupplementFigureSpec, ...] = (
    SupplementFigureSpec(
        figure_id="supplement_predicate_drop_settle",
        title="Drop/settle predicate anatomy",
        subtitle="Final speed, floor breach, and descent terms are checked together.",
        kind="drop_settle",
        panels=("initial height", "settle window", "accept terms"),
        shows="How one vertical probe becomes velocity, height, and descent clauses.",
        does_not_show="It does not certify behavior outside the recorded diagnostic scene.",
        source_records=("docs/records/2026-05-14-newton-drop-settle.md",),
    ),
    SupplementFigureSpec(
        figure_id="supplement_predicate_stack_slide",
        title="Stack-or-slide predicate anatomy",
        subtitle="Terminal contact, lateral drift, support height, and speed form the gate.",
        kind="stack_slide",
        panels=("contact", "drift", "residual speed"),
        shows="Why a package can touch the probe yet still fail by sliding away.",
        does_not_show="It is not a manipulation-stability benchmark.",
        source_records=("configs/experiments/phase0_baseline.yaml",),
    ),
    SupplementFigureSpec(
        figure_id="supplement_predicate_sphere_rain",
        title="Sphere-rain contact coverage",
        subtitle="Many lightweight probes reveal missing or overly permissive contact zones.",
        kind="sphere_rain",
        panels=("probe cloud", "contact bins", "diagnostic label"),
        shows="How repeated contact probes turn spatial coverage into a diagnostic symptom.",
        does_not_show="It is not exhaustive geometric coverage of every possible contact.",
        source_records=("docs/records/2026-05-26-phase0-paper-evidence-closure.md",),
    ),
    SupplementFigureSpec(
        figure_id="supplement_generated_package_consumption",
        title="Generated-package consumption check",
        subtitle="The checker accounts for missing bodies, suppressed source shapes, and filters.",
        kind="package_consumption",
        panels=("source", "generated", "scene accounting"),
        shows="The bookkeeping that makes a package auditable before probe outcomes are read.",
        does_not_show="It is not whole-arm robot performance evidence.",
        source_records=("docs/records/2026-05-26-generated-package-robot-task-probe.md",),
    ),
    SupplementFigureSpec(
        figure_id="supplement_compound_body_state_teaching",
        title="Compound body-state mechanism",
        subtitle="Local primitive plausibility can diverge from aggregate mass properties.",
        kind="compound",
        panels=("primitive COM", "package COM", "diagnostic gate"),
        shows="How COM and inertia aggregation enter the body-level diagnostic path.",
        does_not_show="It does not claim a general optimal primitive decomposition.",
        source_records=("docs/records/2026-05-26-accv-paper-visual-expansion-plan.md",),
    ),
    SupplementFigureSpec(
        figure_id="supplement_franka_link_frames",
        title="Franka link ownership frames",
        subtitle="Each primitive keeps the source link owner before simulation consumption.",
        kind="franka_links",
        panels=("link graph", "body attachment", "merge violation"),
        shows="The structural reason cross-link primitive merges are rejected.",
        does_not_show="It is not a whole-robot collision-quality claim.",
        source_records=("docs/records/2026-05-26-link-aware-robot-package-generation.md",),
    ),
    SupplementFigureSpec(
        figure_id="supplement_franka_source_suppression",
        title="Source-shape suppression accounting",
        subtitle="Generated shapes are inserted while source collision shapes are removed.",
        kind="source_suppression",
        panels=("before", "after", "accounting"),
        shows="Which scene counts must match before the generated package is trusted.",
        does_not_show="It is not deployment readiness for a robot application.",
        source_records=("docs/records/2026-05-26-generated-package-robot-task-probe.md",),
    ),
    SupplementFigureSpec(
        figure_id="supplement_failure_storyboard_bowl",
        title="Bowl failure storyboard",
        subtitle="Initial state, terminal state, measured symptom, and label are separated.",
        kind="storyboard_bowl",
        panels=("initial", "final", "metric", "label"),
        shows="How a failure label is backed by a measured diagnostic symptom.",
        does_not_show="It is not a new quantitative result table.",
        source_records=("docs/records/2026-05-26-phase0-paper-evidence-closure.md",),
    ),
    SupplementFigureSpec(
        figure_id="supplement_failure_storyboard_cup_tray",
        title="Cup and tray failure storyboards",
        subtitle="Two assets show different symptoms under the same audit template.",
        kind="storyboard_cup_tray",
        panels=("cup", "tray", "metric", "label"),
        shows="Why failure categories should be read as diagnostic labels, not rankings.",
        does_not_show="It does not compare methods beyond the recorded smoke settings.",
        source_records=("docs/records/2026-05-26-phase0-vhacd-runtime-followup.md",),
    ),
    SupplementFigureSpec(
        figure_id="supplement_candidate_lane_anatomy",
        title="Candidate-lane anatomy",
        subtitle="Each generator lane produces candidates that pass through the same probes.",
        kind="candidate_lane",
        panels=("generator lane", "package", "diagnostic gate"),
        shows="The reviewer-facing path from candidate package to accepted or fallback label.",
        does_not_show="It is not a claim that one lane is broadly superior.",
        source_records=("paper/shared/evidence/results_manifest.yaml",),
    ),
    SupplementFigureSpec(
        figure_id="supplement_provenance_flow",
        title="Artifact and provenance flow",
        subtitle="Configs, records, generated figures, and LaTeX sources remain linked.",
        kind="provenance",
        panels=("config", "record", "manifest", "supplement"),
        shows="How the supplement avoids committing raw assets while preserving audit trails.",
        does_not_show="It is not an external-link dependency for ACCV review.",
        source_records=("docs/reference/claim-boundaries.md",),
    ),
)
SUPPLEMENT_FIGURE_IDS: tuple[str, ...] = tuple(spec.figure_id for spec in FIGURE_SPECS)


def load_supplement_slot_manifest(
    manifest_path: str | Path = DEFAULT_SLOT_MANIFEST,
    *,
    required_ids: Sequence[str] = SUPPLEMENT_FIGURE_IDS,
) -> dict[str, Any]:
    path = Path(manifest_path)
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if payload.get("mode") != AI_SLOT_MODE:
        raise ValueError(f"Supplement AI slot manifest must use mode: {AI_SLOT_MODE}")
    slots = payload.get("slots")
    if not isinstance(slots, Mapping):
        raise ValueError("Supplement AI slot manifest missing slots mapping")
    missing = [figure_id for figure_id in required_ids if figure_id not in slots]
    if missing:
        raise ValueError(f"Supplement AI slot manifest missing slots: {', '.join(missing)}")
    for figure_id in required_ids:
        slot = slots[figure_id]
        if not isinstance(slot, Mapping):
            raise ValueError(f"Supplement AI slot entry must be a mapping: {figure_id}")
        asset = slot.get("asset")
        if not asset:
            raise ValueError(f"Supplement AI slot missing asset: {figure_id}")
        asset_path = _repo_path(str(asset))
        if not asset_path.is_file():
            raise FileNotFoundError(asset_path)
        renderer = str(slot.get("renderer", ""))
        if figure_id in SCENE_EXPLANATION_FIGURE_IDS:
            if renderer != NEWTON_RTX_SUPPLEMENT_RENDERER:
                raise ValueError(
                    f"Supplement scene slot must use Newton RTX renderer: {figure_id}"
                )
            sidecar = slot.get("sidecar")
            if not sidecar:
                raise ValueError(f"Supplement Newton RTX scene slot missing sidecar: {figure_id}")
            sidecar_path = _repo_path(str(sidecar))
            if not sidecar_path.is_file():
                raise FileNotFoundError(sidecar_path)
            sidecar_text = sidecar_path.read_text(encoding="utf-8")
            if "/cpfs/" in sidecar_text or "zhuzihou" in sidecar_text:
                raise ValueError(f"Supplement Newton RTX sidecar leaks local path: {figure_id}")
        elif not renderer.startswith(AI_SLOT_RENDERER_PREFIX):
            raise ValueError(f"Supplement AI slot must use built-in imagegen renderer: {figure_id}")
        if not slot.get("prompt_summary"):
            raise ValueError(f"Supplement AI slot missing prompt summary: {figure_id}")
        if slot.get("replaceable_by_real_render") is not True:
            raise ValueError(f"Supplement AI slot must remain replaceable by real render: {figure_id}")
    return dict(payload)


def generate_supplement_figures(
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    *,
    slot_manifest_path: str | Path = DEFAULT_SLOT_MANIFEST,
) -> dict[str, Any]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    slot_manifest = load_supplement_slot_manifest(slot_manifest_path)
    slots = slot_manifest["slots"]
    figures: list[dict[str, Any]] = []
    for spec in FIGURE_SPECS:
        slot = slots[spec.figure_id]
        slot_path = _repo_path(str(slot["asset"]))
        image = _compose_plate(spec, slot)
        png_path = out / f"{spec.figure_id}.png"
        pdf_path = out / f"{spec.figure_id}.pdf"
        image.save(png_path)
        image.save(
            pdf_path,
            "PDF",
            resolution=180.0,
            creationDate=DETERMINISTIC_PDF_TIME,
            modDate=DETERMINISTIC_PDF_TIME,
            title=spec.figure_id,
            creator="primitive_collision_compiler.paper.accv_supplement_figures",
            producer="primitive_collision_compiler.paper.accv_supplement_figures",
        )
        spec_hash = _sha256_text(_canonical_spec(spec))
        figure_record: dict[str, Any] = {
            "figure_id": spec.figure_id,
            "title": spec.title,
            "png": png_path.name,
            "pdf": pdf_path.name,
            "png_sha256": _sha256_file(png_path),
            "pdf_sha256": _sha256_file(pdf_path),
            "source_sha256": spec_hash,
            "source_records": list(spec.source_records),
            "slot_asset": _portable_manifest_path(slot_path),
            "slot_sha256": _sha256_file(slot_path),
            "slot_prompt_summary": slot["prompt_summary"],
            "slot_renderer": slot["renderer"],
            "slot_replaceable_by_real_render": slot["replaceable_by_real_render"],
            "composer": "AI slot / Newton RTX deterministic composer: primitive_collision_compiler.paper.accv_supplement_figures",
            "claim_boundary": spec.claim_boundary,
        }
        if slot.get("sidecar"):
            sidecar_path = _repo_path(str(slot["sidecar"]))
            figure_record["slot_sidecar"] = _portable_manifest_path(sidecar_path)
            figure_record["slot_sidecar_sha256"] = _sha256_file(sidecar_path)
        figures.append(figure_record)
    manifest_path = out / "manifest.json"
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "mode": AI_SLOT_MODE,
        "manifest_path": _portable_manifest_path(manifest_path),
        "slot_manifest": _portable_manifest_path(Path(slot_manifest_path)),
        "slot_manifest_sha256": _sha256_file(Path(slot_manifest_path)),
        "slot_claim_boundary": slot_manifest.get("claim_boundary", ""),
        "figure_count": len(figures),
        "figures": figures,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--slot-manifest", type=Path, default=DEFAULT_SLOT_MANIFEST)
    args = parser.parse_args(argv)
    manifest = generate_supplement_figures(
        output_dir=args.output_dir,
        slot_manifest_path=args.slot_manifest,
    )
    print(manifest["manifest_path"])
    return 0


def _compose_plate(spec: SupplementFigureSpec, slot: Mapping[str, Any]) -> Image.Image:
    canvas = Image.new("RGB", CANVAS_SIZE, "#f7f9fc")
    draw = ImageDraw.Draw(canvas)
    _draw_background(draw)
    title_font = _font(54, bold=True)
    subtitle_font = _font(30)
    label_font = _font(26, bold=True)
    body_font = _font(25)
    small_font = _font(22)

    draw.text((78, 58), spec.title, font=title_font, fill=TEXT)
    draw.text((82, 126), spec.subtitle, font=subtitle_font, fill=MUTED)

    panel_boxes = _panel_boxes(len(spec.panels))
    for idx, (label, box) in enumerate(zip(spec.panels, panel_boxes)):
        _rounded(draw, box, 24, PANEL_FILL, PANEL_STROKE, 3)
        draw.text((box[0] + 28, box[1] + 24), label.upper(), font=label_font, fill=_palette(idx))
    _paste_slot_strip(canvas, _repo_path(str(slot["asset"])), panel_boxes)
    for box in panel_boxes:
        _rounded(draw, (box[0] + 34, box[1] + 82, box[2] - 34, box[3] - 32), 18, None, "#cad3df", 2)

    show_box = (78, 846, 850, 1034)
    limit_box = (950, 846, 1722, 1034)
    _callout(draw, show_box, "What this shows", spec.shows, GREEN, body_font, small_font)
    _callout(draw, limit_box, "What this does not show", spec.does_not_show, RED, body_font, small_font)
    draw.text((78, 1060), spec.claim_boundary, font=small_font, fill="#6b7280")
    return canvas


def _panel_boxes(count: int) -> list[tuple[int, int, int, int]]:
    top, bottom = 210, 812
    if count <= 3:
        width = 520
        gap = 40
        return [(78 + n * (width + gap), top, 78 + n * (width + gap) + width, bottom) for n in range(count)]
    width = 380
    gap = 36
    return [(78 + n * (width + gap), top, 78 + n * (width + gap) + width, bottom) for n in range(count)]


def _paste_slot_strip(canvas: Image.Image, path: Path, boxes: Sequence[tuple[int, int, int, int]]) -> None:
    inner_boxes = [(box[0] + 34, box[1] + 82, box[2] - 34, box[3] - 32) for box in boxes]
    source = _trim_light_border(Image.open(path).convert("RGB"))
    for inner, segment in zip(inner_boxes, _slot_segments(source, len(inner_boxes))):
        tile = Image.new("RGB", (inner[2] - inner[0], inner[3] - inner[1]), "#ffffff")
        fitted = ImageOps.contain(segment, tile.size, method=Image.Resampling.LANCZOS)
        tile.paste(fitted, ((tile.width - fitted.width) // 2, (tile.height - fitted.height) // 2))
        mask = Image.new("L", tile.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, tile.width - 1, tile.height - 1), radius=18, fill=255)
        canvas.paste(tile, inner[:2], mask)


def _slot_segments(source: Image.Image, count: int) -> list[Image.Image]:
    width, height = source.size
    segments: list[Image.Image] = []
    for index in range(count):
        left = round(index * width / count)
        right = round((index + 1) * width / count)
        segments.append(source.crop((left, 0, right, height)))
    return segments


def _trim_light_border(source: Image.Image, threshold: int = 248, margin: int = 20) -> Image.Image:
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
    left = max(min(xs) - margin, 0)
    top = max(min(ys) - margin, 0)
    right = min(max(xs) + margin, width - 1)
    bottom = min(max(ys) + margin, height - 1)
    if left <= 0 and top <= 0 and right >= width - 1 and bottom >= height - 1:
        return source
    return source.crop((left, top, right + 1, bottom + 1))


def _draw_background(draw: ImageDraw.ImageDraw) -> None:
    for x in range(0, CANVAS_SIZE[0], 48):
        draw.line((x, 0, x, CANVAS_SIZE[1]), fill="#edf1f6", width=1)
    for y in range(0, CANVAS_SIZE[1], 48):
        draw.line((0, y, CANVAS_SIZE[0], y), fill="#edf1f6", width=1)


def _callout(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    body: str,
    color: str,
    title_font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    body_font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
) -> None:
    _rounded(draw, box, 22, "#ffffff", "#d7dee9", 2)
    draw.rectangle((box[0], box[1], box[0] + 14, box[3]), fill=color)
    draw.text((box[0] + 36, box[1] + 24), title, font=title_font, fill=color)
    y = box[1] + 72
    for line in _wrap(body, 66):
        draw.text((box[0] + 36, y), line, font=body_font, fill=TEXT)
        y += 31


def _center_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    box: tuple[int, int, int, int],
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    fill: str,
) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    x = box[0] + max((box[2] - box[0] - width) // 2, 0)
    y = box[1] + max((box[3] - box[1] - height) // 2, 0)
    draw.text((x, y), text, font=font, fill=fill)


def _rounded(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill: str | None,
    outline: str,
    width: int,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def _palette(index: int) -> str:
    colors = (BLUE, GREEN, GOLD, PURPLE, TEAL, RED)
    return colors[index % len(colors)]


def _font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for base in (Path("/usr/share/fonts/truetype/dejavu"), Path("/usr/local/share/fonts")):
        path = base / name
        if path.is_file():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def _wrap(text: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _canonical_spec(spec: SupplementFigureSpec) -> str:
    return json.dumps(asdict(spec), sort_keys=True, separators=(",", ":"))


def _portable_manifest_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return resolved.name


def _repo_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
