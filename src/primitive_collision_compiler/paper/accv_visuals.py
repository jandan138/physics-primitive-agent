from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np


PACKAGE_LANE_ORDER: tuple[str, ...] = (
    "bounding_primitive",
    "cpd_style_primitive_candidate_if_available",
    "coacd_or_vhacd_if_available",
    "vhacd_if_available",
)
MATRIX_LANE_ORDER: tuple[str, ...] = (
    "bounding_primitive",
    "single_convex_hull",
    "cpd_style_primitive_candidate_if_available",
    "coacd_or_vhacd_if_available",
    "vhacd_if_available",
)
LANE_LABELS: Mapping[str, str] = {
    "bounding_primitive": "BBox",
    "cpd_style_primitive_candidate_if_available": "CPD-style",
    "coacd_or_vhacd_if_available": "CoACD",
    "vhacd_if_available": "V-HACD",
    "single_convex_hull": "Single hull",
}
PROBE_ORDER: tuple[str, ...] = (
    "contact_canary",
    "body_state_drop_settle",
    "stack_or_slide",
    "sphere_rain",
)
PROBE_LABELS: Mapping[str, str] = {
    "contact_canary": "Contact",
    "body_state_drop_settle": "Drop",
    "stack_or_slide": "Stack",
    "sphere_rain": "Sphere",
}
PROBE_SHORT_LABELS: Mapping[str, str] = {
    "contact_canary": "Contact",
    "body_state_drop_settle": "Drop",
    "stack_or_slide": "Stack",
    "sphere_rain": "Rain",
}
OUTCOME_TO_VALUE: Mapping[str, int] = {
    "fallback": 0,
    "not_applicable": 1,
    "failure": 2,
    "accept": 3,
}
OUTCOME_COLORS: Mapping[str, str] = {
    "accept": "#2e7d59",
    "failure": "#b94b48",
    "fallback": "#8a8f98",
    "not_applicable": "#d5d8dc",
    "dependency_gap": "#a76f1b",
}
PDF_METADATA: Mapping[str, Any] = {
    "Creator": "primitive_collision_compiler.paper.accv_visuals",
    "Producer": "Matplotlib pdf backend",
    "CreationDate": datetime(2026, 5, 26, tzinfo=timezone.utc),
    "ModDate": datetime(2026, 5, 26, tzinfo=timezone.utc),
}
REPO_ROOT = Path(__file__).resolve().parents[3]
RESULTS_MANIFEST = REPO_ROOT / "paper/shared/evidence/results_manifest.yaml"
PHASE0_SOURCE_RECORDS: tuple[str, ...] = (
    "docs/records/2026-05-26-phase0-vhacd-runtime-followup.md",
    "docs/records/2026-05-26-phase0-paper-evidence-closure.md",
)
FRANKA_SOURCE_RECORDS: tuple[str, ...] = (
    "docs/records/2026-05-26-link-aware-robot-package-generation.md",
    "docs/records/2026-05-26-generated-package-robot-task-probe.md",
)
PAPER_SCENE_RENDERER_SOURCE_FILES: tuple[str, ...] = (
    "src/newton_render/render/paper_diagnostic_scenes.py",
    "src/newton_render/figures/engine.py",
)
PAPER_SCENE_SIDECAR_MANIFEST_KEYS: tuple[str, ...] = (
    "recipe",
    "figure_id",
    "output_png_sha256",
    "input_hashes",
    "claim_boundary_note",
    "source_claim_boundary_note",
    "paper_readability",
    "render_quality",
    "mechanism_visual_mode",
    "rendered_component_ids",
    "subscene_ids",
    "franka_visual_mode",
    "link_count",
    "sentinel_link_names",
    "status_label_layout",
)


@dataclass(frozen=True)
class FigureOutput:
    figure_id: str
    path: Path
    evidence: str
    source_records: tuple[str, ...] = ()
    renderer_metadata: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class Phase0ProbeScenePanelSpec:
    case: Mapping[str, Any]
    panel_kind: str
    probe_name: str
    lane: str = "vhacd_if_available"


@dataclass(frozen=True)
class Phase0RenderedProbePanel:
    spec: Phase0ProbeScenePanelSpec
    output_png: Path
    bundle_dir: Path


def load_phase0_report(path: str | Path) -> dict[str, Any]:
    report_path = Path(path)
    with report_path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ValueError(f"phase0 report must be a JSON object: {report_path}")
    if "cases" not in payload:
        raise ValueError(f"phase0 report missing cases: {report_path}")
    return payload


def case_label(case: Mapping[str, Any]) -> str:
    role = str(case.get("asset_role", "asset")).replace("_", " ")
    asset_id = str(case.get("asset_id", "unknown"))
    if "bowl" in asset_id:
        name = "bowl"
    elif "cup" in asset_id:
        name = "cup"
    elif "tray" in asset_id:
        name = "tray"
    elif "keyboard" in asset_id:
        name = "keyboard"
    elif "box" in asset_id:
        name = "box"
    else:
        name = asset_id.split("_")[1] if "_" in asset_id else asset_id
    return f"{role}\n{name}"


def _phase0_probe_scene_case_label(case: Mapping[str, Any]) -> str:
    role = str(case.get("asset_role", "")).replace("_", " ")
    if role == "contact affordance":
        return "cylindrical contact\nprop"
    return case_label(case)


def resolve_asset_path(case: Mapping[str, Any], asset_root: str | Path) -> Path:
    local_path = case.get("local_path") or case.get("asset_path")
    if not local_path:
        raise ValueError(f"case missing local_path: {case.get('asset_id')}")
    path = Path(str(local_path))
    if path.is_absolute():
        return path
    return Path(asset_root) / path


def primitive_vertices(primitive: Mapping[str, Any]) -> np.ndarray:
    kind = str(primitive.get("kind", ""))
    dimensions = primitive.get("dimensions") or {}
    if kind == "box":
        half_extents = np.asarray(dimensions.get("half_extents", ()), dtype=float)
        if half_extents.shape != (3,):
            return np.empty((0, 3), dtype=float)
        center = np.asarray(primitive.get("center", (0.0, 0.0, 0.0)), dtype=float)
        if center.shape != (3,):
            center = np.zeros(3, dtype=float)
        axes = np.asarray(primitive.get("axes") or np.eye(3), dtype=float)
        if axes.shape != (3, 3):
            axes = np.eye(3, dtype=float)
        signs = np.asarray(
            [
                (-1, -1, -1),
                (1, -1, -1),
                (1, 1, -1),
                (-1, 1, -1),
                (-1, -1, 1),
                (1, -1, 1),
                (1, 1, 1),
                (-1, 1, 1),
            ],
            dtype=float,
        )
        local = signs * half_extents
        return center + local @ axes
    if kind == "convex_mesh":
        vertices = np.asarray(dimensions.get("vertices", ()), dtype=float)
        if vertices.ndim == 2 and vertices.shape[1] == 3:
            return vertices
    return np.empty((0, 3), dtype=float)


def package_vertices(package: Mapping[str, Any] | None) -> np.ndarray:
    if not package:
        return np.empty((0, 3), dtype=float)
    clouds = [
        primitive_vertices(primitive)
        for primitive in package.get("primitives", [])
        if isinstance(primitive, Mapping)
    ]
    clouds = [cloud for cloud in clouds if len(cloud)]
    if not clouds:
        return np.empty((0, 3), dtype=float)
    return np.concatenate(clouds, axis=0)


def package_for_lane(case: Mapping[str, Any], lane: str) -> Mapping[str, Any] | None:
    lane_result = (case.get("baseline_results") or {}).get(lane) or {}
    package = lane_result.get("collision_package")
    return package if isinstance(package, Mapping) else None


def probe_result(case: Mapping[str, Any], lane: str, probe: str) -> Mapping[str, Any] | None:
    lane_probes = ((case.get("probe_results") or {}).get(lane) or {})
    result = lane_probes.get(probe)
    return result if isinstance(result, Mapping) else None


def probe_failure_labels(result: Mapping[str, Any] | None) -> tuple[str, ...]:
    if not result:
        return ()
    labels: list[str] = []
    for run_key in ("drop_settle_runs", "stack_slide_runs", "sphere_rain_runs", "contact_canaries"):
        for run in result.get(run_key, []) or []:
            labels.extend(str(label) for label in run.get("failure_labels", []) or [])
    return tuple(dict.fromkeys(labels))


def _phase0_probe_scene_panel_specs(report: Mapping[str, Any]) -> list[Phase0ProbeScenePanelSpec]:
    selected_roles = ("container", "contact_affordance", "stackable")
    panel_specs: list[Phase0ProbeScenePanelSpec] = []
    for case in report.get("cases", []) or []:
        if case.get("asset_role") not in selected_roles:
            continue
        panel_specs.extend(
            [
                Phase0ProbeScenePanelSpec(case=case, panel_kind="package_overlay", probe_name="package_overlay"),
                Phase0ProbeScenePanelSpec(
                    case=case,
                    panel_kind="drop_settle",
                    probe_name="body_state_drop_settle",
                ),
                Phase0ProbeScenePanelSpec(case=case, panel_kind="stack_slide", probe_name="stack_or_slide"),
            ]
        )
    return panel_specs


def _render_vec3_y_up(value: Sequence[float]) -> list[float]:
    if len(value) != 3:
        raise ValueError(f"expected length-3 vector, got {value!r}")
    x, y, z = (float(value[0]), float(value[1]), float(value[2]))
    return [x, z, y]


def _phase0_render_package_y_up(package: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if not package:
        return None
    converted = copy.deepcopy(dict(package))
    primitives = converted.get("primitives", [])
    if not isinstance(primitives, list):
        return converted
    for primitive in primitives:
        if not isinstance(primitive, dict):
            continue
        center = primitive.get("center")
        if isinstance(center, list) and len(center) == 3:
            primitive["center"] = _render_vec3_y_up(center)
        axes = primitive.get("axes")
        if isinstance(axes, list):
            primitive["axes"] = [
                _render_vec3_y_up(axis)
                for axis in axes
                if isinstance(axis, list) and len(axis) == 3
            ]
        dimensions = primitive.get("dimensions")
        if isinstance(dimensions, dict):
            vertices = dimensions.get("vertices")
            if isinstance(vertices, list):
                dimensions["vertices"] = [
                    _render_vec3_y_up(vertex)
                    for vertex in vertices
                    if isinstance(vertex, list) and len(vertex) == 3
                ]
            half_extents = dimensions.get("half_extents")
            if isinstance(half_extents, list) and len(half_extents) == 3:
                dimensions["half_extents"] = _render_vec3_y_up(half_extents)
    return converted


def _phase0_probe_scene_payload(
    spec: Phase0ProbeScenePanelSpec,
    *,
    report_path: Path,
    report_sha256: str,
) -> dict[str, Any]:
    case = spec.case
    package = package_for_lane(case, spec.lane)
    asset_id = str(case.get("asset_id", ""))
    asset_role = str(case.get("asset_role", ""))
    package_id = str((package or {}).get("package_id", f"{asset_role}_{spec.lane}:phase0_vhacd"))
    if spec.panel_kind == "package_overlay":
        return {
            "schema_version": 1,
            "source_report": report_path.as_posix(),
            "source_report_sha256": report_sha256,
            "asset_id": asset_id,
            "asset_role": asset_role,
            "lane": spec.lane,
            "package_id": package_id,
            "probe_type": "package_overlay",
            "outcome": str(((case.get("baseline_results") or {}).get(spec.lane) or {}).get("outcome", "accept")),
            "failure_labels": [],
            "recorded_metrics": {},
            "reconstruction_semantics": {
                "mode": "collision_package_overlay",
                "full_pose_recorded": True,
                "text": "Asset mesh with selected collision primitive overlay.",
            },
        }

    result = probe_result(case, spec.lane, spec.probe_name) or {}
    runs = result.get("drop_settle_runs" if spec.panel_kind == "drop_settle" else "stack_slide_runs") or []
    first_run = runs[0] if runs and isinstance(runs[0], Mapping) else {}
    initial_conditions = result.get("initial_conditions") or {}
    if spec.panel_kind == "drop_settle":
        metrics = {
            "initial_height": float(initial_conditions.get("height_m", first_run.get("initial_height", 0.25))),
            "final_height": float(first_run.get("final_height", 0.25)),
            "min_height": float(first_run.get("min_height", first_run.get("final_height", 0.25))),
            "horizontal_displacement_m": None,
            "support_top_height": None,
        }
        semantics = {
            "mode": "metric_anchored_reconstruction",
            "full_pose_recorded": False,
            "text": "Start/final placements are visual reconstructions anchored to recorded scalar metrics.",
        }
    elif spec.panel_kind == "stack_slide":
        initial_position = first_run.get("initial_probe_position", [0.0, 0.0, 0.0])
        final_position = first_run.get("final_probe_position", initial_position)
        half_extents = initial_conditions.get("probe_half_extents_m", [0.05, 0.05, 0.05])
        metrics = {
            "initial_probe_position": _render_vec3_y_up(initial_position),
            "final_probe_position": _render_vec3_y_up(final_position),
            "horizontal_displacement_m": float(first_run.get("horizontal_displacement_m", 0.0)),
            "support_top_height": float(first_run.get("support_top_height", 0.0)),
            "probe_half_extents_m": _render_vec3_y_up(half_extents),
        }
        semantics = {
            "mode": "recorded_probe_position_reconstruction",
            "full_pose_recorded": True,
            "text": "Probe start/final centers are read from the recorded stack/slide run.",
        }
    else:
        raise ValueError(f"unsupported phase0 probe panel kind: {spec.panel_kind}")

    return {
        "schema_version": 1,
        "source_report": report_path.as_posix(),
        "source_report_sha256": report_sha256,
        "asset_id": asset_id,
        "asset_role": asset_role,
        "lane": spec.lane,
        "package_id": package_id,
        "probe_type": spec.probe_name,
        "outcome": str(result.get("outcome", "unknown")),
        "failure_labels": list(probe_failure_labels(result)),
        "recorded_metrics": metrics,
        "reconstruction_semantics": semantics,
    }


def _phase0_probe_panel_slug(spec: Phase0ProbeScenePanelSpec) -> str:
    role = str(spec.case.get("asset_role", "asset"))
    asset_id = str(spec.case.get("asset_id", "unknown"))
    if "bowl" in asset_id:
        asset_name = "bowl"
    elif "cup" in asset_id:
        asset_name = "cup"
    elif "tray" in asset_id:
        asset_name = "tray"
    else:
        asset_name = asset_id.split("_")[1] if "_" in asset_id else asset_id
    return f"{role}_{asset_name}_{spec.panel_kind}"


def _phase0_probe_scene_camera(case: Mapping[str, Any]) -> dict[str, float | str]:
    role = str(case.get("asset_role", ""))
    asset_id = str(case.get("asset_id", ""))
    if role == "container" or "bowl" in asset_id:
        return {
            "preset": "phase0_container_open_rim",
            "elev": 38,
            "azim": 10,
            "zoom": 1.35,
        }
    if role == "stackable" or "tray" in asset_id:
        return {
            "preset": "phase0_three_quarter",
            "elev": 22,
            "azim": -42,
            "zoom": 1.22,
        }
    return {
        "preset": "phase0_three_quarter",
        "elev": 22,
        "azim": -42,
        "zoom": 1.35,
    }


def _write_phase0_probe_scene_bundle(
    spec: Phase0ProbeScenePanelSpec,
    *,
    mesh: Any,
    bundle_dir: Path,
    report_path: Path,
    report_sha256: str,
) -> None:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML is required to write newton-render bundles") from exc

    bundle_dir.mkdir(parents=True, exist_ok=True)
    slug = _phase0_probe_panel_slug(spec)
    label = _phase0_probe_scene_case_label(spec.case).replace("\n", " ")
    meta = {
        "figure_id": f"physics_primitive.phase0.{slug}",
        "recipe": "phase0_probe_scene",
        "paper": "physics_primitive",
        "panel_kind": spec.panel_kind,
        "asset_label": label,
        "asset_role": str(spec.case.get("asset_role", "")),
        "asset_id": str(spec.case.get("asset_id", "")),
        "lane": spec.lane,
        "camera": _phase0_probe_scene_camera(spec.case),
        "style": {"background": "paper_light"},
        "overlay_max_primitives": 3,
    }
    if spec.panel_kind == "stack_slide":
        meta["stack_use_package_support"] = True
    (bundle_dir / "meta.yaml").write_text(yaml.safe_dump(meta, sort_keys=False), encoding="utf-8")
    payload = _phase0_probe_scene_payload(
        spec,
        report_path=report_path,
        report_sha256=report_sha256,
    )
    (bundle_dir / "probe_scene.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    package = _phase0_render_package_y_up(package_for_lane(spec.case, spec.lane))
    if package:
        (bundle_dir / "collision_package.json").write_text(json.dumps(package, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_obj_mesh_y_up(mesh, bundle_dir / "mesh.obj")


def _write_obj_mesh_y_up(mesh: Any, path: Path) -> None:
    lines: list[str] = []
    for point in np.asarray(mesh.points, dtype=float):
        x, y, z = _render_vec3_y_up(point.tolist())
        lines.append(f"v {x:.9f} {y:.9f} {z:.9f}")
    for face in np.asarray(mesh.faces, dtype=int):
        indices = [str(int(index) + 1) for index in face]
        lines.append(f"f {' '.join(indices)}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _run_newton_render_phase0_panel(
    *,
    newton_render_root: Path,
    bundle_dir: Path,
    output_png: Path,
    python_executable: str | Path | None = None,
) -> Path:
    root = Path(newton_render_root)
    executable = str(python_executable or _newton_render_python_executable())
    env = os.environ.copy()
    src_path = str((root / "src").resolve())
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = src_path if not existing_pythonpath else f"{src_path}{os.pathsep}{existing_pythonpath}"
    output_png.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        executable,
        "-m",
        "newton_render.cli",
        "render-figure",
        "--bundle",
        str(bundle_dir),
        "--recipe",
        "phase0_probe_scene",
        "--output",
        str(output_png),
    ]
    subprocess.run(cmd, cwd=root, env=env, check=True, capture_output=True, text=True)
    return output_png


def _run_newton_render_paper_scene(
    *,
    newton_render_root: Path,
    bundle_dir: Path,
    output_png: Path,
    recipe: str,
    python_executable: str | Path | None = None,
) -> Path:
    root = Path(newton_render_root)
    executable = str(python_executable or _newton_render_python_executable())
    env = os.environ.copy()
    src_path = str((root / "src").resolve())
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = src_path if not existing_pythonpath else f"{src_path}{os.pathsep}{existing_pythonpath}"
    output_png.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        executable,
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
    subprocess.run(cmd, cwd=root, env=env, check=True, capture_output=True, text=True)
    if not output_png.is_file():
        raise RuntimeError(f"newton-render did not create {output_png}")
    return output_png


def _newton_render_python_executable() -> str:
    configured = os.environ.get("NEWTON_RENDER_PYTHON") or os.environ.get("NR_PYTHON")
    if configured:
        return configured
    sandbox_python = Path("/cpfs/user/zhuzihou/conda-managed/envs/newton-render-py310/bin/python")
    if sandbox_python.exists():
        return str(sandbox_python)
    return sys.executable


def _write_paper_scene_bundle(
    bundle_dir: Path,
    *,
    figure_id: str,
    recipe: str,
    scene_payload: Mapping[str, Any],
) -> Path:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML is required to write newton-render bundles") from exc

    bundle_dir.mkdir(parents=True, exist_ok=True)
    meta = {
        "figure_id": figure_id,
        "recipe": recipe,
        "paper": "physics_primitive",
        "style": {"background": "paper_light"},
        "paper_readability": {
            "tight_crop": True,
            "annotation_scale": "large_paper_panel",
            "label_contrast": "bold_paper_labels",
        },
    }
    (bundle_dir / "meta.yaml").write_text(yaml.safe_dump(meta, sort_keys=False), encoding="utf-8")
    (bundle_dir / "scene.json").write_text(
        json.dumps(dict(scene_payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return bundle_dir


def _paper_scene_renderer_metadata(newton_render_root: Path, panel_png: Path) -> dict[str, Any]:
    sidecar_path = panel_png.with_suffix(".json")
    if not sidecar_path.is_file():
        raise RuntimeError(f"newton-render did not create sidecar metadata: {sidecar_path}")
    sidecar_payload = json.loads(sidecar_path.read_text(encoding="utf-8"))
    if not isinstance(sidecar_payload, dict):
        raise RuntimeError(f"newton-render sidecar must be a JSON object: {sidecar_path}")
    return {
        "recipe": str(sidecar_payload.get("recipe", "")),
        "renderer_source_hashes": _newton_render_source_hashes(newton_render_root),
        "sidecar": {
            key: copy.deepcopy(sidecar_payload[key])
            for key in PAPER_SCENE_SIDECAR_MANIFEST_KEYS
            if key in sidecar_payload
        },
    }


def _newton_render_source_hashes(newton_render_root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    root = Path(newton_render_root)
    for relative_path in PAPER_SCENE_RENDERER_SOURCE_FILES:
        source_path = root / relative_path
        if source_path.is_file():
            hashes[relative_path] = _sha256_file(source_path)
    if not hashes:
        raise RuntimeError(f"newton-render source files not found under {root}")
    return hashes


def _render_phase0_probe_scene_panels(
    report: Mapping[str, Any],
    *,
    asset_root: Path,
    report_path: Path,
    bundle_root: Path,
    panel_output_dir: Path,
    newton_render_root: Path,
) -> list[Phase0RenderedProbePanel]:
    report_sha256 = _sha256_file(report_path)
    bundle_root.mkdir(parents=True, exist_ok=True)
    panel_output_dir.mkdir(parents=True, exist_ok=True)
    panels: list[Phase0RenderedProbePanel] = []
    for spec in _phase0_probe_scene_panel_specs(report):
        slug = _phase0_probe_panel_slug(spec)
        bundle_dir = bundle_root / slug
        mesh = _load_mesh(resolve_asset_path(spec.case, asset_root), max_faces=_phase0_probe_scene_mesh_face_cap(spec.case))
        _write_phase0_probe_scene_bundle(
            spec,
            mesh=mesh,
            bundle_dir=bundle_dir,
            report_path=report_path,
            report_sha256=report_sha256,
        )
        output_png = panel_output_dir / f"{slug}.png"
        rendered = _run_newton_render_phase0_panel(
            newton_render_root=newton_render_root,
            bundle_dir=bundle_dir,
            output_png=output_png,
        )
        panels.append(Phase0RenderedProbePanel(spec=spec, output_png=rendered, bundle_dir=bundle_dir))
    return panels


def _phase0_probe_scene_mesh_face_cap(case: Mapping[str, Any]) -> int:
    if case.get("asset_role") == "precision_negative_control":
        return 1800
    return 1200


def outcome_matrix(report: Mapping[str, Any]) -> tuple[list[str], list[str], np.ndarray]:
    rows = [case_label(case) for case in report.get("cases", [])]
    columns: list[str] = []
    for lane in MATRIX_LANE_ORDER:
        for probe in PROBE_ORDER:
            columns.append(f"{LANE_LABELS[lane]}\n{PROBE_LABELS[probe]}")

    values = np.zeros((len(rows), len(columns)), dtype=int)
    for row_index, case in enumerate(report.get("cases", [])):
        col_index = 0
        for lane in MATRIX_LANE_ORDER:
            for probe in PROBE_ORDER:
                result = probe_result(case, lane, probe)
                outcome = str((result or {}).get("outcome", "not_applicable"))
                values[row_index, col_index] = OUTCOME_TO_VALUE.get(outcome, 1)
                col_index += 1
    return rows, columns, values


def summarize_probe_outcomes(report: Mapping[str, Any]) -> dict[str, int]:
    counts = {"accept": 0, "failure": 0, "fallback": 0, "not_applicable": 0, "dependency_gap": 0}
    for case in report.get("cases", []):
        for lane in MATRIX_LANE_ORDER:
            for probe in PROBE_ORDER:
                result = probe_result(case, lane, probe)
                outcome = str((result or {}).get("outcome", "not_applicable"))
                counts[outcome] = counts.get(outcome, 0) + 1
    return counts


def generate_accv_visuals(
    *,
    report_path: str | Path,
    asset_root: str | Path,
    output_dir: str | Path,
) -> list[FigureOutput]:
    report = load_phase0_report(report_path)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    _configure_matplotlib(plt)

    figures = [
        *_save_asset_package_overlays(report, Path(asset_root), output, plt),
        _save_collision_probe_scenes(report, Path(asset_root), output, plt, report_path=Path(report_path)),
        _save_outcome_matrix(report, output, plt),
        _save_mechanism_diagnostic(output, plt),
        _save_franka_task_scene(report, output, plt),
    ]
    _write_manifest(
        output / "accv_visuals_manifest.json",
        report_path=Path(report_path),
        asset_root=Path(asset_root),
        figures=figures,
    )
    return figures


def _configure_matplotlib(plt: Any) -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8,
            "axes.titlesize": 8,
            "axes.labelsize": 7,
            "xtick.labelsize": 6,
            "ytick.labelsize": 6,
            "legend.fontsize": 7,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def _save_asset_package_overlays(
    report: Mapping[str, Any],
    asset_root: Path,
    output: Path,
    plt: Any,
) -> list[FigureOutput]:
    cases = list(report.get("cases", []))
    primary_roles = {"rigid_prop", "container", "contact_affordance"}
    control_roles = {"stackable", "precision_negative_control"}
    return [
        _save_asset_package_overlay_grid(
            [case for case in cases if case.get("asset_role") in primary_roles],
            asset_root,
            output,
            plt,
            figure_id="phase0_asset_package_overlays",
            filename="phase0_asset_package_overlays.pdf",
            evidence="phase0 report + repo-local USD mirrors",
        ),
        _save_asset_package_overlay_grid(
            [case for case in cases if case.get("asset_role") in control_roles],
            asset_root,
            output,
            plt,
            figure_id="phase0_asset_package_control_overlays",
            filename="phase0_asset_package_control_overlays.pdf",
            evidence="phase0 report + repo-local USD mirrors; precision/control rows",
        ),
    ]


def _save_asset_package_overlay_grid(
    cases: Sequence[Mapping[str, Any]],
    asset_root: Path,
    output: Path,
    plt: Any,
    *,
    figure_id: str,
    filename: str,
    evidence: str,
) -> FigureOutput:
    if not cases:
        raise RuntimeError(f"no cases available for {figure_id}")
    row_height = 2.9 if any(case.get("asset_role") == "precision_negative_control" for case in cases) else 2.62
    fig = plt.figure(figsize=(12.6, row_height * len(cases)), constrained_layout=False)
    columns = ("Input mesh", "BBox", "CPD-style", "CoACD", "V-HACD")
    lanes = (None, *PACKAGE_LANE_ORDER)
    for row, case in enumerate(cases):
        mesh_face_cap = 1500 if case.get("asset_role") == "precision_negative_control" else 1000
        mesh = _load_mesh(resolve_asset_path(case, asset_root), max_faces=mesh_face_cap)
        for col, lane in enumerate(lanes):
            is_precision_row = case.get("asset_role") == "precision_negative_control"
            is_precision_input = lane is None and is_precision_row
            if is_precision_row:
                ax = fig.add_subplot(len(cases), len(columns), row * len(columns) + col + 1)
            else:
                ax = fig.add_subplot(len(cases), len(columns), row * len(columns) + col + 1, projection="3d")
            if row == 0:
                ax.set_title(columns[col], pad=0)
            if col == 0:
                if is_precision_input:
                    ax.text(-0.07, 0.5, case_label(case), transform=ax.transAxes, ha="right", va="center", fontsize=9)
                else:
                    ax.text2D(-0.07, 0.5, case_label(case), transform=ax.transAxes, ha="right", va="center", fontsize=9)
            show_mesh_context = lane is None or not is_precision_row
            if mesh is not None and is_precision_row:
                _draw_keyboard_projection(ax, mesh, context=lane is not None)
                points = mesh.points
            elif mesh is not None and show_mesh_context:
                mesh_alpha, mesh_edge_linewidth = _package_context_mesh_style(lane=lane)
                _draw_mesh(
                    ax,
                    mesh,
                    alpha=mesh_alpha,
                    edge_linewidth=mesh_edge_linewidth,
                )
                points = mesh.points
            else:
                points = np.empty((0, 3), dtype=float)
            if lane is not None:
                package = package_for_lane(case, lane)
                if is_precision_row:
                    _draw_projected_package(
                        ax,
                        package,
                        color=_lane_color(lane),
                        max_primitives=_projected_overlay_max_primitives(package),
                    )
                else:
                    surface_lane = lane in {"coacd_or_vhacd_if_available", "vhacd_if_available"}
                    _draw_package(
                        ax,
                        package,
                        color=_lane_color(lane),
                        max_primitives=_overlay_max_primitives(package, surface=surface_lane),
                        surface=surface_lane,
                    )
                package_points = package_vertices(package)
                if len(package_points):
                    points = package_points
                lane_result = ((case.get("baseline_results") or {}).get(lane) or {})
                label_kwargs = {
                    "transform": ax.transAxes,
                    "ha": "left",
                    "va": "bottom",
                    "color": _lane_color(lane),
                    "fontsize": 12.0 if is_precision_row else 11.8,
                    "bbox": {"facecolor": "white", "edgecolor": "#dddddd", "alpha": 0.90, "pad": 1.25},
                }
                label = f"{lane_result.get('outcome', 'n/a')} / {lane_result.get('primitive_or_hull_count', 0)}"
                if is_precision_row:
                    ax.text(0.02, 0.02, label, **label_kwargs)
                else:
                    ax.text2D(0.02, 0.02, label, **label_kwargs)
            if is_precision_row:
                pass
            else:
                _finish_3d_axis(ax, points, min_radius=0.08 if lane else 0.0, zoom=1.2)
    fig.subplots_adjust(left=0.075, right=0.995, top=0.93, bottom=0.05, wspace=0.02, hspace=0.0)
    path = output / filename
    _save_pdf(fig, path)
    plt.close(fig)
    return FigureOutput(
        figure_id,
        path,
        evidence,
        PHASE0_SOURCE_RECORDS,
    )


def _package_context_mesh_style(lane: str | None) -> tuple[float, float]:
    if lane is None:
        return (0.65, 0.12)
    return (0.028, 0.010)


def _save_collision_probe_scenes(
    report: Mapping[str, Any],
    asset_root: Path,
    output: Path,
    plt: Any,
    *,
    report_path: Path | None = None,
) -> FigureOutput:
    render_root = _phase0_newton_render_root()
    if render_root is not None and report_path is not None and _phase0_probe_scene_assets_available(report, asset_root):
        try:
            panels = _render_phase0_probe_scene_panels(
                report,
                asset_root=asset_root,
                report_path=report_path,
                bundle_root=REPO_ROOT / "reports/generated/accv_phase0_probe_scene_bundles",
                panel_output_dir=REPO_ROOT / "reports/generated/accv_phase0_probe_scene_panels",
                newton_render_root=render_root,
            )
            if panels:
                return _save_collision_probe_scenes_from_rendered_panels(panels, output, plt)
        except Exception:
            if os.environ.get("NEWTON_RENDER_ROOT"):
                raise

    selected_roles = ("container", "contact_affordance", "stackable")
    cases = [case for case in report.get("cases", []) if case.get("asset_role") in selected_roles]
    fig = plt.figure(figsize=(12.6, 7.4), constrained_layout=False)
    grid = fig.add_gridspec(
        len(cases),
        3,
        width_ratios=_collision_scene_width_ratios(),
        left=0.065,
        right=0.995,
        top=0.925,
        bottom=0.06,
        wspace=0.055,
        hspace=0.10,
    )
    for row, case in enumerate(cases):
        package = package_for_lane(case, "vhacd_if_available")
        mesh = _load_mesh(resolve_asset_path(case, asset_root), max_faces=700)
        render_ax = fig.add_subplot(grid[row, 0], projection="3d")
        _draw_mesh(render_ax, mesh, alpha=0.075, edge_linewidth=0.08)
        _draw_package(
            render_ax,
            package,
            color=_lane_color("vhacd_if_available"),
            max_primitives=_collision_scene_package_max_primitives(package),
            surface=True,
            show_overflow=False,
        )
        subset_label = _collision_scene_subset_label(
            package,
            shown_count=_collision_scene_package_max_primitives(package),
        )
        if subset_label:
            render_ax.text2D(
                0.98,
                0.995,
                subset_label,
                transform=render_ax.transAxes,
                ha="right",
                va="top",
                fontsize=8.4,
                color=_lane_color("vhacd_if_available"),
                bbox={"facecolor": "white", "edgecolor": "#dddddd", "alpha": 0.92, "pad": 1.2},
            )
        render_points = _combine_points(mesh.points, package_vertices(package))
        _finish_3d_axis(render_ax, render_points, min_radius=0.12, zoom=1.22)
        render_ax.set_title("V-HACD package" if row == 0 else "")
        render_ax.text2D(
            -0.045,
            0.5,
            _phase0_probe_scene_case_label(case),
            transform=render_ax.transAxes,
            ha="right",
            va="center",
            fontsize=8,
        )

        drop_ax = fig.add_subplot(grid[row, 1])
        _draw_drop_probe_panel(drop_ax, probe_result(case, "vhacd_if_available", "body_state_drop_settle"))
        if row == 0:
            drop_ax.set_title("Drop/settle probe")

        stack_ax = fig.add_subplot(grid[row, 2])
        _draw_stack_probe_panel(stack_ax, probe_result(case, "vhacd_if_available", "stack_or_slide"))
        if row == 0:
            stack_ax.set_title("Stack/slide probe")
    path = output / "phase0_collision_probe_scenes.pdf"
    _save_pdf(fig, path)
    plt.close(fig)
    return FigureOutput(
        "phase0_collision_probe_scenes",
        path,
        "phase0 Newton probe outcomes",
        PHASE0_SOURCE_RECORDS,
    )


def _save_collision_probe_scenes_from_rendered_panels(
    panels: Sequence[Phase0RenderedProbePanel],
    output: Path,
    plt: Any,
) -> FigureOutput:
    if len(panels) % 3 != 0:
        raise ValueError(f"expected rendered probe panels in triples, got {len(panels)}")
    rows = len(panels) // 3
    fig = plt.figure(figsize=(12.6, max(3.05, 3.05 * rows)), constrained_layout=False)
    grid = fig.add_gridspec(
        rows,
        3,
        left=0.065,
        right=0.995,
        top=0.925,
        bottom=0.04,
        wspace=0.035,
        hspace=0.08,
    )
    titles = ("V-HACD package", "Drop/settle probe", "Stack/slide probe")
    for index, panel in enumerate(panels):
        row = index // 3
        col = index % 3
        ax = fig.add_subplot(grid[row, col])
        image = plt.imread(panel.output_png)
        ax.imshow(image)
        ax.axis("off")
        if row == 0:
            ax.set_title(titles[col], pad=2)
        if col == 0:
            ax.text(
                -0.045,
                0.5,
                _phase0_probe_scene_case_label(panel.spec.case),
                transform=ax.transAxes,
                ha="right",
                va="center",
                fontsize=8,
            )
    path = output / "phase0_collision_probe_scenes.pdf"
    _save_pdf(fig, path)
    plt.close(fig)
    return FigureOutput(
        "phase0_collision_probe_scenes",
        path,
        "phase0 report + newton-render diagnostic scene reconstructions",
        PHASE0_SOURCE_RECORDS,
    )


def _newton_render_root_for_module(module_name: str, *, require_explicit: bool = False) -> Path | None:
    disabled = os.environ.get("PPA_DISABLE_NEWTON_RENDER", "").strip().lower()
    if disabled in {"1", "true", "yes"}:
        return None
    configured = os.environ.get("NEWTON_RENDER_ROOT")
    if not configured and require_explicit:
        raise RuntimeError(
            "NEWTON_RENDER_ROOT is required for paper diagnostic scene rendering; "
            "set PPA_DISABLE_NEWTON_RENDER=1 only when intentionally regenerating schematic fallback figures"
        )
    candidates = [Path(configured)] if configured else [Path("/cpfs/user/zhuzihou/dev/newton-render")]
    recipe_path = Path("src/newton_render/render") / f"{module_name}.py"
    for candidate in candidates:
        if (candidate / recipe_path).is_file():
            return candidate
    if configured:
        raise RuntimeError(f"NEWTON_RENDER_ROOT={configured} is missing {recipe_path.as_posix()}")
    return None


def _phase0_newton_render_root() -> Path | None:
    return _newton_render_root_for_module("phase0_probe_scene")


def _paper_scene_newton_render_root() -> Path | None:
    return _newton_render_root_for_module("paper_diagnostic_scenes", require_explicit=True)


def _phase0_probe_scene_assets_available(report: Mapping[str, Any], asset_root: Path) -> bool:
    try:
        return all(resolve_asset_path(spec.case, asset_root).exists() for spec in _phase0_probe_scene_panel_specs(report))
    except Exception:
        return False


def _collision_scene_width_ratios() -> tuple[float, float, float]:
    return (1.58, 1.0, 1.0)


def _collision_scene_package_max_primitives(package: Mapping[str, Any] | None) -> int:
    if not package:
        return 0
    count = len([p for p in package.get("primitives", []) if isinstance(p, Mapping)])
    if count > 4:
        return 3
    return count


def _collision_scene_subset_label(package: Mapping[str, Any] | None, *, shown_count: int) -> str:
    if not package:
        return ""
    count = len([p for p in package.get("primitives", []) if isinstance(p, Mapping)])
    overflow = max(0, count - shown_count)
    if overflow:
        return f"repr. prim. +{overflow}"
    return "repr. prim."


def _save_outcome_matrix(report: Mapping[str, Any], output: Path, plt: Any) -> FigureOutput:
    rows, columns, values = outcome_matrix(report)
    fig, ax = plt.subplots(figsize=(12.8, 5.15), constrained_layout=True)
    colors = ["#8a8f98", "#d5d8dc", "#b94b48", "#2e7d59"]
    from matplotlib.colors import ListedColormap, BoundaryNorm

    cmap = ListedColormap(colors)
    norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap.N)
    ax.imshow(values, cmap=cmap, norm=norm, aspect="auto")
    ax.set_xticks(np.arange(len(columns)))
    ax.set_xticklabels(
        [PROBE_SHORT_LABELS[PROBE_ORDER[index % len(PROBE_ORDER)]] for index in range(len(columns))],
        rotation=24,
        ha="right",
        fontsize=9.0,
    )
    ax.set_yticks(np.arange(len(rows)))
    ax.set_yticklabels(rows, fontsize=8.2)
    title = _outcome_matrix_title()
    if title:
        ax.set_title(title, pad=22)
    ax.set_xticks(np.arange(-0.5, len(columns), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(rows), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=0.35)
    ax.tick_params(which="minor", bottom=False, left=False)
    for group_index, lane in enumerate(MATRIX_LANE_ORDER):
        start = group_index * len(PROBE_ORDER)
        ax.axvline(start - 0.5, color="white", linewidth=1.2)
        ax.text(
            start + 1.5,
            -0.86,
            _outcome_matrix_group_label(lane),
            ha="center",
            va="center",
            fontsize=9.2,
            color="#111111",
            clip_on=False,
        )
    ax.axvline(len(columns) - 0.5, color="white", linewidth=1.2)
    for row in range(values.shape[0]):
        for col in range(values.shape[1]):
            label = _outcome_cell_label(int(values[row, col]))
            if label:
                ax.text(col, row, label, ha="center", va="center", fontsize=7.8, color="#111111")
    _draw_outcome_legend(ax)
    ax.text(
        0.5,
        -0.40,
        "Probe labels repeat within each method group: Contact, Drop, Stack, Rain",
        ha="center",
        va="center",
        fontsize=8.2,
        color="#333333",
        transform=ax.transAxes,
    )
    path = output / "phase0_outcome_matrix.pdf"
    _save_pdf(fig, path)
    plt.close(fig)
    return FigureOutput("phase0_outcome_matrix", path, "phase0 report outcome labels", PHASE0_SOURCE_RECORDS)


def _outcome_cell_label(value: int) -> str:
    return {0: "FB", 1: "NA", 2: "Fail", 3: "OK"}.get(value, "")


def _outcome_matrix_group_label(lane: str) -> str:
    if lane == "single_convex_hull":
        return "Single hull\nfallback lane"
    return LANE_LABELS[lane]


def _outcome_matrix_title() -> str:
    return ""


def _save_mechanism_diagnostic(output: Path, plt: Any) -> FigureOutput:
    entry = _load_result_entry("bed_franka_cylinder_mechanism")
    metrics = entry.get("metrics") or {}
    render_root = _paper_scene_newton_render_root()
    if render_root is not None:
        bundle_dir = _write_paper_scene_bundle(
            REPO_ROOT / "reports/generated/accv_paper_scene_bundles/bed_franka_mechanism_diagnostic",
            figure_id="bed_franka_mechanism_diagnostic",
            recipe="mechanism_diagnostic_scene",
            scene_payload=_mechanism_scene_payload(metrics),
        )
        panel = _run_newton_render_paper_scene(
            newton_render_root=render_root,
            bundle_dir=bundle_dir,
            output_png=REPO_ROOT / "reports/generated/accv_paper_scene_panels/bed_franka_mechanism_diagnostic.png",
            recipe="mechanism_diagnostic_scene",
        )
        return _save_mechanism_diagnostic_from_rendered_panel(
            panel,
            output,
            plt,
            renderer_metadata=_paper_scene_renderer_metadata(render_root, panel),
        )

    fig, ax = plt.subplots(figsize=(12.2, 3.25), constrained_layout=True)
    _draw_mechanism_scene(ax, metrics, plt)
    _draw_mechanism_summary_badges(ax, metrics)
    path = output / "bed_franka_mechanism_diagnostic.pdf"
    _save_pdf(fig, path)
    plt.close(fig)
    return FigureOutput(
        "bed_franka_mechanism_diagnostic",
        path,
        "2026-05-22 cylinder mechanism records",
        _mechanism_source_records(),
    )


def _save_mechanism_diagnostic_from_rendered_panel(
    panel_png: Path,
    output: Path,
    plt: Any,
    *,
    renderer_metadata: Mapping[str, Any] | None = None,
) -> FigureOutput:
    entry = _load_result_entry("bed_franka_cylinder_mechanism")
    metrics = entry.get("metrics") or {}
    fig, ax = plt.subplots(figsize=(12.2, 3.25), constrained_layout=True)
    ax.imshow(plt.imread(panel_png))
    ax.axis("off")
    ax.set_title(_mechanism_scene_title())
    _draw_mechanism_summary_badges(ax, metrics)
    path = output / "bed_franka_mechanism_diagnostic.pdf"
    _save_pdf(fig, path)
    plt.close(fig)
    return FigureOutput(
        "bed_franka_mechanism_diagnostic",
        path,
        "newton-render diagnostic scene reconstruction + 2026-05-22 cylinder mechanism records",
        _mechanism_source_records(),
        renderer_metadata,
    )


def _mechanism_visual_labels(metrics: Mapping[str, Any]) -> tuple[str, ...]:
    return (
        "capped bed: full package fails",
        "isolated target passes",
        "Franka link-local package passes",
        "COM/inertia sensitivity supported",
        f"bed final speed {float(metrics['bed_final_speed_mps']):.3f} m/s",
        f"Franka final speed {float(metrics['franka_final_speed_mps']):.5f} m/s",
    )


def _mechanism_scene_payload(metrics: Mapping[str, Any]) -> dict[str, Any]:
    bed_speed = float(metrics["bed_final_speed_mps"])
    franka_speed = float(metrics["franka_final_speed_mps"])
    gate = float(metrics["settle_gate_mps"])
    return {
        "claim_boundary_note": "Diagnostic rendering; not a new Newton run.",
        "labels": {
            "failure": "",
            "accept": "",
        },
        "status_label_entries": ["failure", "accept"],
        "settle_gate_mps": gate,
        "subscenes": [
            {
                "id": "bed_full_package_fail",
                "status": "failure",
                "label": "full package fails",
                "speed_mps": bed_speed,
                "speed_gate_mps": gate,
                "highlight": "large_flat_cylinder",
            },
            {
                "id": "isolated_target_pass",
                "status": "accept",
                "label": "isolated target passes",
                "speed_gate_mps": gate,
                "highlight": "target_cylinder",
            },
            {
                "id": "franka_link_local_pass",
                "status": "accept",
                "label": "Franka link-local package passes",
                "speed_mps": franka_speed,
                "speed_gate_mps": gate,
                "highlight": "link_local_primitives",
            },
        ],
        "annotations": {
            "bed_speed_label": f"{bed_speed:.3f} > {gate:.2f} m/s",
            "franka_speed_label": f"{franka_speed:.5f} <= {gate:.2f} m/s",
            "root_cause_label": "COM/inertia sensitivity supported",
        },
    }


def _draw_mechanism_summary_badges(ax: Any, metrics: Mapping[str, Any]) -> None:
    del metrics
    _draw_visual_notes(
        ax,
        (
            ("isolated: pass", "#2e7d59"),
            ("full package: fail", "#b94b48"),
            ("COM/inertia supported", "#a76f1b"),
        ),
        columns=3,
    )


def _mechanism_source_records() -> tuple[str, ...]:
    entry = _load_result_entry("bed_franka_cylinder_mechanism")
    return tuple(_split_evidence_sources(entry.get("evidence_source", ""))) + (
        "paper/shared/evidence/results_manifest.yaml",
    )


def _draw_mechanism_scene(ax: Any, metrics: Mapping[str, Any], plt: Any) -> None:
    labels = _mechanism_visual_labels(metrics)
    bed_speed = float(metrics["bed_final_speed_mps"])
    franka_speed = float(metrics["franka_final_speed_mps"])
    gate = float(metrics["settle_gate_mps"])

    ax.axis("off")
    ax.set_title(_mechanism_scene_title())
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)

    ax.plot([0.04, 0.96], [0.50, 0.50], color="#d0d3d8", linewidth=0.8)
    ax.text(0.04, 0.935, labels[0], ha="left", va="top", fontsize=8.6, weight="bold", color="#8f2f2d")
    ax.text(0.04, 0.44, labels[2], ha="left", va="top", fontsize=8.7, weight="bold", color="#1f6b4d")

    _draw_bed_failure_scene(ax, bed_speed, gate, plt)
    _draw_franka_mechanism_scene(ax, franka_speed, gate, plt)

    ax.annotate(
        labels[3],
        xy=(0.43, 0.61),
        xytext=(0.37, 0.50),
        ha="center",
        va="center",
        fontsize=8.4,
        color="#4a3b13",
        bbox={"facecolor": "#fff7dd", "edgecolor": "#d4a72c", "boxstyle": "round,pad=0.25"},
        arrowprops={"arrowstyle": "-|>", "lw": 1.0, "color": "#a76f1b", "shrinkA": 4, "shrinkB": 4},
    )


def _mechanism_scene_title() -> str:
    return "Mechanism diagnostic: package context matters"


def _mechanism_failure_callout_positions() -> dict[str, tuple[float, float]]:
    return {
        "com_label": (0.55, 0.895),
        "settle_label": (0.64, 0.755),
    }


def _draw_bed_failure_scene(ax: Any, speed: float, gate: float, plt: Any) -> None:
    ax.add_patch(plt.Rectangle((0.06, 0.60), 0.38, 0.12, facecolor="#dfe4ea", edgecolor="#30343a", linewidth=0.9))
    ax.add_patch(plt.Rectangle((0.08, 0.72), 0.34, 0.06, facecolor="#b9c3ce", edgecolor="#30343a", linewidth=0.9))
    for x in (0.10, 0.36):
        ax.add_patch(plt.Rectangle((x, 0.52), 0.035, 0.08, facecolor="#8a8f98", edgecolor="#30343a", linewidth=0.7))
    ax.text(0.25, 0.575, "bed body", ha="center", va="center", fontsize=7.8, color="#30343a")

    full_package = [(0.12, 0.79, 0.06, 0.10), (0.20, 0.80, 0.05, 0.08), (0.29, 0.79, 0.08, 0.11)]
    for x, y, width, height in full_package:
        ax.add_patch(
            plt.Rectangle(
                (x, y),
                width,
                height,
                facecolor="#f6d1ce",
                edgecolor="#b94b48",
                linewidth=1.2,
                alpha=0.92,
            )
        )
    ax.scatter([0.36], [0.86], marker="x", s=80, color="#b94b48", linewidth=1.4, zorder=5)
    positions = _mechanism_failure_callout_positions()
    ax.annotate(
        "shifted COM / inertia",
        xy=(0.36, 0.86),
        xytext=positions["com_label"],
        fontsize=7.5,
        ha="left",
        va="center",
        color="#8f2f2d",
        arrowprops={"arrowstyle": "->", "lw": 0.85, "color": "#b94b48", "shrinkA": 2, "shrinkB": 3},
    )
    ax.text(
        *positions["settle_label"],
        f"fails settle\n{speed:.3f} > {gate:.2f} m/s",
        ha="center",
        va="center",
        fontsize=8.0,
        color="#8f2f2d",
        bbox={"facecolor": "white", "edgecolor": "#f0d0cd", "alpha": 0.95, "pad": 1.6},
    )

    ax.add_patch(plt.Rectangle((0.77, 0.64), 0.16, 0.06, facecolor="#e5e8ec", edgecolor="#30343a", linewidth=0.8))
    ax.add_patch(plt.Rectangle((0.82, 0.70), 0.06, 0.10, facecolor="#cfe8d8", edgecolor="#2e7d59", linewidth=1.1))
    ax.text(0.85, 0.835, "isolated target\npasses", ha="center", va="center", fontsize=7.8, color="#2e7d59")


def _draw_franka_mechanism_scene(ax: Any, speed: float, gate: float, plt: Any) -> None:
    points = np.asarray(
        [
            (0.08, 0.17),
            (0.18, 0.19),
            (0.29, 0.26),
            (0.41, 0.31),
            (0.54, 0.30),
            (0.66, 0.24),
            (0.76, 0.18),
        ],
        dtype=float,
    )
    ax.plot([0.04, 0.94], [0.08, 0.08], color="#9aa0a6", linewidth=0.9)
    ax.add_patch(plt.Rectangle((0.055, 0.08), 0.07, 0.06, facecolor="#c9cdd2", edgecolor="#30343a", linewidth=0.8))
    ax.plot(points[:, 0], points[:, 1], color="#cfd4da", linewidth=11.0, solid_capstyle="round", alpha=0.62, zorder=1)
    ax.plot(points[:, 0], points[:, 1], color="#4d5660", linewidth=4.2, solid_capstyle="round", alpha=0.88, zorder=2)
    for index, (x, y) in enumerate(points):
        color = "#a76f1b" if index == len(points) - 2 else "#2e7d59"
        ax.scatter([x], [y], s=86, color="white", edgecolor="#30343a", linewidth=0.7, zorder=5)
        ax.add_patch(
            plt.Rectangle(
                (x - 0.026, y - 0.018),
                0.052,
                0.036,
                facecolor=color,
                edgecolor="#30343a",
                linewidth=0.65,
                zorder=6,
            )
        )
    ax.text(0.44, 0.38, "link-local primitives", ha="center", va="center", fontsize=7.8, color="#2e7d59")
    ax.annotate(
        f"passes task smoke\n{speed:.5f} <= {gate:.2f} m/s",
        xy=(0.73, 0.19),
        xytext=(0.82, 0.33),
        ha="center",
        va="center",
        fontsize=8.0,
        color="#1f6b4d",
        bbox={"facecolor": "white", "edgecolor": "#cfe8d8", "alpha": 0.95, "pad": 1.6},
        arrowprops={"arrowstyle": "-|>", "lw": 1.0, "color": "#2e7d59"},
    )


def _save_franka_task_scene(report: Mapping[str, Any], output: Path, plt: Any) -> FigureOutput:
    render_root = _paper_scene_newton_render_root()
    if render_root is not None:
        bundle_dir = _write_paper_scene_bundle(
            REPO_ROOT / "reports/generated/accv_paper_scene_bundles/franka_link_aware_task_scene",
            figure_id="franka_link_aware_task_scene",
            recipe="franka_task_scene",
            scene_payload=_franka_task_scene_payload(report),
        )
        panel = _run_newton_render_paper_scene(
            newton_render_root=render_root,
            bundle_dir=bundle_dir,
            output_png=REPO_ROOT / "reports/generated/accv_paper_scene_panels/franka_link_aware_task_scene.png",
            recipe="franka_task_scene",
        )
        return _save_franka_task_scene_from_rendered_panel(
            report,
            panel,
            output,
            plt,
            renderer_metadata=_paper_scene_renderer_metadata(render_root, panel),
        )

    articulation = (report.get("articulation_cases") or [{}])[0]
    robot_result = articulation.get("robot_package_result") or {}
    links = robot_result.get("links", []) or []

    fig, ax = plt.subplots(figsize=(12.2, 3.25), constrained_layout=True)
    ax.set_title("Franka generated-package task smoke")
    ax.set_xlim(-0.2, 1.05)
    ax.set_ylim(-0.08, 1.05)
    ax.axis("off")
    _draw_franka_task_schematic(ax, links, plt)
    _draw_franka_summary_badges(ax, _franka_metric_rows(report))

    path = output / "franka_link_aware_task_scene.pdf"
    _save_pdf(fig, path)
    plt.close(fig)
    return FigureOutput(
        "franka_link_aware_task_scene",
        path,
        "link-aware package and generated-package robot task records",
        FRANKA_SOURCE_RECORDS,
    )


def _franka_task_scene_payload(report: Mapping[str, Any]) -> dict[str, Any]:
    articulation = (report.get("articulation_cases") or [{}])[0]
    robot_result = articulation.get("robot_package_result") or {}
    links = robot_result.get("links", []) or []
    rows = dict(_franka_metric_rows(report))
    sentinel_links = [
        _short_link_name(link.get("link_path", ""))
        for link in links
        if _safe_int(link.get("placeholder_primitive_count", 0)) and link.get("link_path")
    ]
    return {
        "claim_boundary_note": "Task-smoke rendering; not whole-robot quality evidence.",
        "labels": {
            "failure": "",
            "accept": "",
            "meshless_sentinel": "",
        },
        "links": [
            {
                "name": _short_link_name(str(link.get("link_path", f"link_{index}"))),
                "kind": "meshless_sentinel"
                if _safe_int(link.get("placeholder_primitive_count", 0))
                else "normal",
                "index": index,
            }
            for index, link in enumerate(links)
        ],
        "sentinel_links": sentinel_links,
        "metrics": {
            "detected_links": _safe_int(rows.get("detected links")) or 0,
            "generated_primitives": _safe_int(rows.get("generated primitives")) or 0,
            "missing_body_links": _safe_int(rows.get("missing body links")) or 0,
            "source_usd_shapes": _safe_int(rows.get("source USD shapes")) or 0,
            "self_collision_filters": _safe_int(rows.get("self-collision filters")) or 0,
            "task_outcome": str(rows.get("task outcome", "n/a")),
        },
        "trajectory": {"start": [0.52, 0.76], "end": [0.72, 0.58]},
    }


def _short_link_name(link_path: str) -> str:
    return link_path.rstrip("/").split("/")[-1]


def _franka_metric_rows(report: Mapping[str, Any]) -> list[tuple[str, Any]]:
    articulation = (report.get("articulation_cases") or [{}])[0]
    robot_result = articulation.get("robot_package_result") or {}
    links = robot_result.get("links", []) or []
    metrics = ((articulation.get("probe_results") or {}).get("generated_package_robot_task_if_robot") or {}).get(
        "metrics", {}
    )
    package_consumption = metrics.get("package_consumption") or {}
    audit_metrics = ((robot_result.get("link_boundary_audit") or {}).get("metrics") or {})
    probe = (articulation.get("probe_results") or {}).get("generated_package_robot_task_if_robot") or {}
    return [
        ("detected links", audit_metrics.get("link_count", len(links))),
        ("generated primitives", robot_result.get("primitive_or_hull_count", 0)),
        ("missing body links", package_consumption.get("missing_body_link_count", 0)),
        ("source USD shapes", package_consumption.get("source_usd_shape_count", 0)),
        ("self-collision filters", package_consumption.get("generated_self_collision_filter_pair_count", 0)),
        ("task outcome", probe.get("outcome", "n/a")),
    ]


def _save_franka_task_scene_from_rendered_panel(
    report: Mapping[str, Any],
    panel_png: Path,
    output: Path,
    plt: Any,
    *,
    renderer_metadata: Mapping[str, Any] | None = None,
) -> FigureOutput:
    fig, ax = plt.subplots(figsize=(12.2, 3.25), constrained_layout=True)
    ax.imshow(plt.imread(panel_png))
    ax.axis("off")
    ax.set_title("Franka generated-package task smoke")
    _draw_franka_summary_badges(ax, _franka_metric_rows(report))
    path = output / "franka_link_aware_task_scene.pdf"
    _save_pdf(fig, path)
    plt.close(fig)
    return FigureOutput(
        "franka_link_aware_task_scene",
        path,
        "newton-render diagnostic scene reconstruction + link-aware package and generated-package robot task records",
        FRANKA_SOURCE_RECORDS,
        renderer_metadata,
    )


def _franka_metric_color(label: str, value: Any) -> str:
    if label in {"missing body links", "source USD shapes"}:
        return "#2e7d59" if _safe_int(value) == 0 else "#b94b48"
    if label == "task outcome":
        outcome = str(value)
        if outcome == "accept":
            return "#2e7d59"
        if outcome in {"failure", "reject", "rejected"}:
            return "#b94b48"
        return "#a76f1b"
    return "#333333"


def _draw_franka_summary_badges(ax: Any, rows: Sequence[tuple[str, Any]]) -> None:
    metrics = dict(rows)
    task_outcome = str(metrics.get("task outcome", "n/a"))
    _draw_visual_notes(
        ax,
        (
            (f"{metrics.get('detected links', 0)}/{metrics.get('generated primitives', 0)} links", "#333333"),
            (f"{metrics.get('missing body links', 0)} missing", _franka_metric_color("missing body links", metrics.get("missing body links", 0))),
            (task_outcome, _franka_metric_color("task outcome", task_outcome)),
        ),
        columns=3,
    )


def _draw_visual_notes(
    ax: Any,
    badges: Sequence[tuple[str, str]],
    *,
    columns: int,
) -> None:
    if columns < 1:
        raise ValueError("columns must be positive")
    column_width = 0.94 / columns
    for index, (label, color) in enumerate(badges):
        row = index // columns
        column = index % columns
        ax.text(
            0.03 + column * column_width,
            0.035 + row * 0.075,
            label,
            transform=ax.transAxes,
            ha="left",
            va="bottom",
            fontsize=7.6,
            weight="normal",
            color=color,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.78, "pad": 0.9},
            zorder=100,
        )


def _safe_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _load_mesh(path: Path, *, max_faces: int) -> Any:
    try:
        from pxr import Gf, Usd, UsdGeom

        from primitive_collision_compiler.baselines.cpd_like.usd import _mesh_to_triangle_mesh
    except Exception as exc:
        raise RuntimeError(f"failed to load source mesh for paper figure: {path}") from exc
    if max_faces < 1:
        raise RuntimeError(f"failed to load source mesh for paper figure: {path}")
    if not path.exists():
        raise RuntimeError(f"failed to load source mesh for paper figure: {path}")

    try:
        stage = Usd.Stage.Open(str(path))
        if stage is None:
            raise RuntimeError(f"usd_open_failed: {path}")
        cache = UsdGeom.XformCache()
        meshes = []
        remaining_faces = max_faces
        for prim in stage.Traverse():
            if not prim.IsA(UsdGeom.Mesh):
                continue
            if not _is_visual_mesh_prim(prim, UsdGeom):
                continue
            component = _mesh_to_triangle_mesh(
                UsdGeom.Mesh(prim),
                max_faces=remaining_faces,
                transform=cache.GetLocalToWorldTransform(prim),
                gf=Gf,
            )
            meshes.append(component)
            remaining_faces -= component.face_count
            if remaining_faces <= 0:
                break
        if not meshes:
            raise RuntimeError("no_usd_mesh_found")
        return _merge_triangle_meshes(meshes)
    except Exception as exc:
        raise RuntimeError(f"failed to load source mesh for paper figure: {path}") from exc


def _is_visual_mesh_prim(prim: Any, usd_geom: Any) -> bool:
    try:
        purpose = str(usd_geom.Imageable(prim).ComputePurpose())
    except Exception:
        purpose_attr = prim.GetAttribute("purpose")
        purpose = str(purpose_attr.Get() if purpose_attr and purpose_attr.HasValue() else "default")
    return purpose in {"default", "render"}


def _merge_triangle_meshes(meshes: Sequence[Any]) -> Any:
    from primitive_collision_compiler.geometry.mesh import TriangleMesh

    points = []
    faces = []
    point_offset = 0
    for mesh in meshes:
        points.append(mesh.points)
        faces.append(mesh.faces + point_offset)
        point_offset += len(mesh.points)
    return TriangleMesh(points=np.concatenate(points, axis=0), faces=np.concatenate(faces, axis=0))


def _draw_mesh(ax: Any, mesh: Any, *, alpha: float, edge_linewidth: float = 0.12) -> None:
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    faces = mesh.faces
    if len(faces) > 700:
        step = max(1, math.ceil(len(faces) / 700))
        faces = faces[::step]
    polygons = mesh.points[faces]
    collection = Poly3DCollection(
        polygons,
        facecolor="#c9cdd2",
        edgecolor="#7b838c",
        linewidth=edge_linewidth,
        alpha=alpha,
        rasterized=True,
    )
    ax.add_collection3d(collection)


def _draw_keyboard_projection(ax: Any, mesh: Any, *, context: bool = False) -> None:
    from matplotlib.patches import Rectangle

    bounds = _projected_component_bounds(mesh)
    coords = np.concatenate([np.asarray([[left, bottom], [right, top]]) for left, bottom, right, top in bounds], axis=0)
    areas = np.asarray([(right - left) * (top - bottom) for left, bottom, right, top in bounds], dtype=float)
    largest = int(np.argmax(areas)) if len(areas) else -1
    for index, (left, bottom, right, top) in sorted(enumerate(bounds), key=lambda item: areas[item[0]], reverse=True):
        is_base = index == largest
        style = _keyboard_component_style(context=context, is_base=is_base)
        ax.add_patch(
            Rectangle(
                (left, bottom),
                right - left,
                top - bottom,
                facecolor=style["facecolor"],
                edgecolor=style["edgecolor"],
                linewidth=style["linewidth"],
                alpha=style["alpha"],
            )
        )
    mins = coords.min(axis=0)
    maxs = coords.max(axis=0)
    pad = np.maximum((maxs - mins) * 0.025, 1.0)
    ax.set_xlim(float(mins[0] - pad[0]), float(maxs[0] + pad[0]))
    ax.set_ylim(float(mins[1] - pad[1]), float(maxs[1] + pad[1]))
    ax.set_aspect("auto")
    ax.axis("off")


def _keyboard_component_style(*, context: bool, is_base: bool) -> dict[str, Any]:
    if context:
        return {
            "facecolor": "#d7dce0" if is_base else "#f0f3f5",
            "edgecolor": "#7d8790",
            "linewidth": 0.40 if is_base else 0.34,
            "alpha": 0.30 if is_base else 0.24,
        }
    return {
        "facecolor": "#d9dde1" if is_base else "#eef1f3",
        "edgecolor": "#8b949e" if is_base else "#4d5660",
        "linewidth": 0.75 if is_base else 0.52,
        "alpha": 0.34 if is_base else 0.72,
    }


def _draw_projected_package(
    ax: Any,
    package: Mapping[str, Any] | None,
    *,
    color: str,
    max_primitives: int,
) -> None:
    from matplotlib.patches import Rectangle

    if not package:
        ax.text(0.5, 0.5, "fallback", transform=ax.transAxes, ha="center", va="center", color="#777777")
        return
    primitives = [p for p in package.get("primitives", []) if isinstance(p, Mapping)]
    shown_primitives = primitives[:max_primitives]
    for marker_index, primitive in enumerate(shown_primitives):
        vertices = primitive_vertices(primitive)
        if not len(vertices):
            continue
        coords = vertices[:, [2, 0]]
        mins = coords.min(axis=0)
        maxs = coords.max(axis=0)
        left, bottom, right, top = _minimum_projected_marker_bounds(
            mins,
            maxs,
            xlim=ax.get_xlim(),
            ylim=ax.get_ylim(),
            min_fraction=0.095,
        )
        ax.add_patch(
            Rectangle(
                (left, bottom),
                right - left,
                top - bottom,
                facecolor=color,
                edgecolor=color,
                linewidth=3.15,
                alpha=0.42,
            )
        )
        ax.plot(
            [left, right, right, left, left],
            [bottom, bottom, top, top, bottom],
            color=color,
            linewidth=2.05,
            alpha=0.98,
        )
        label_x, label_y, label_ha = _projected_package_label_position(
            left=left,
            bottom=bottom,
            right=right,
            top=top,
            xlim=ax.get_xlim(),
            ylim=ax.get_ylim(),
        )
        ax.annotate(
            _projected_package_marker_label(marker_index, total=len(shown_primitives)),
            xy=((left + right) / 2.0, (bottom + top) / 2.0),
            xytext=(label_x, label_y),
            ha=label_ha,
            va="center",
            fontsize=11.2,
            weight="bold",
            color=color,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.84, "pad": 1.1},
            arrowprops={"arrowstyle": "-", "lw": 0.85, "color": color, "shrinkA": 2, "shrinkB": 4},
        )
    if len(primitives) > max_primitives:
        ax.text(
            0.98,
            0.02,
            f"+{len(primitives)-max_primitives}",
            transform=ax.transAxes,
            ha="right",
            va="bottom",
            color=color,
            fontsize=13.2,
            weight="bold",
            bbox={"facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.92, "pad": 1.4},
        )


def _projected_overlay_max_primitives(package: Mapping[str, Any] | None) -> int:
    if not package:
        return 0
    count = len([p for p in package.get("primitives", []) if isinstance(p, Mapping)])
    if count > 4:
        return 1
    return count


def _projected_package_marker_label(index: int, *, total: int) -> str:
    if total <= 1:
        return "pkg"
    return f"pkg {index + 1}"


def _projected_package_label_position(
    *,
    left: float,
    bottom: float,
    right: float,
    top: float,
    xlim: tuple[float, float],
    ylim: tuple[float, float],
) -> tuple[float, float, str]:
    del ylim
    marker_width = max(right - left, 1e-6)
    offset = marker_width * 0.70
    center_y = (bottom + top) / 2.0
    if right + offset <= xlim[1]:
        return (right + offset, center_y, "left")
    return (left - offset, center_y, "right")


def _minimum_projected_marker_bounds(
    mins: np.ndarray,
    maxs: np.ndarray,
    *,
    xlim: tuple[float, float],
    ylim: tuple[float, float],
    min_fraction: float,
) -> tuple[float, float, float, float]:
    center = (mins + maxs) / 2.0
    marker_size = np.asarray(
        [
            max(float(maxs[0] - mins[0]), abs(xlim[1] - xlim[0]) * min_fraction),
            max(float(maxs[1] - mins[1]), abs(ylim[1] - ylim[0]) * min_fraction),
        ],
        dtype=float,
    )
    expanded_min = center - marker_size / 2.0
    expanded_max = center + marker_size / 2.0
    return (float(expanded_min[0]), float(expanded_min[1]), float(expanded_max[0]), float(expanded_max[1]))


def _projected_component_bounds(mesh: Any) -> list[tuple[float, float, float, float]]:
    parent = list(range(len(mesh.points)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    for face in mesh.faces:
        first = int(face[0])
        for point_index in face[1:]:
            union(first, int(point_index))

    components: dict[int, list[int]] = {}
    for point_index in range(len(mesh.points)):
        components.setdefault(find(point_index), []).append(point_index)

    bounds = []
    for indices in components.values():
        coords = mesh.points[np.asarray(indices, dtype=int)][:, [2, 0]]
        mins = coords.min(axis=0)
        maxs = coords.max(axis=0)
        bounds.append((float(mins[0]), float(mins[1]), float(maxs[0]), float(maxs[1])))
    return bounds


def _draw_package(
    ax: Any,
    package: Mapping[str, Any] | None,
    *,
    color: str,
    max_primitives: int,
    surface: bool = False,
    show_overflow: bool = True,
) -> None:
    if not package:
        ax.text2D(0.5, 0.5, "fallback", transform=ax.transAxes, ha="center", va="center", color="#777777")
        return
    primitives = [p for p in package.get("primitives", []) if isinstance(p, Mapping)]
    if not primitives:
        ax.text2D(0.5, 0.5, "no mapped\nprimitive", transform=ax.transAxes, ha="center", va="center", color="#777777")
        return
    for primitive in primitives[:max_primitives]:
        _draw_primitive(ax, primitive, color=color, surface=surface)
    if show_overflow and len(primitives) > max_primitives:
        ax.text2D(
            0.985,
            0.965,
            f"+{len(primitives)-max_primitives}",
            transform=ax.transAxes,
            ha="right",
            va="top",
            color=color,
            fontsize=13.5,
            weight="bold",
            bbox={"facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.96, "pad": 1.7},
        )


def _overlay_max_primitives(package: Mapping[str, Any] | None, *, surface: bool) -> int:
    if not package:
        return 0
    count = len([p for p in package.get("primitives", []) if isinstance(p, Mapping)])
    if count > 4:
        if surface:
            return 1
        return 2
    return count if surface else max(count, 1)


def _surface_overlay_face_limit(*, surface: bool) -> int:
    return 12 if surface else 24


def _primitive_overlay_wire_style(*, surface: bool, kind: str) -> tuple[float, float]:
    if kind == "box":
        return (0.80, 0.58) if surface else (1.08, 0.88)
    return (0.48, 0.46) if surface else (0.62, 0.78)


def _draw_primitive(ax: Any, primitive: Mapping[str, Any], *, color: str, surface: bool = False) -> None:
    kind = str(primitive.get("kind", ""))
    vertices = primitive_vertices(primitive)
    if not len(vertices):
        return
    if kind == "box":
        linewidth, alpha = _primitive_overlay_wire_style(surface=surface, kind=kind)
        for start, end in _BOX_EDGES:
            ax.plot(*zip(vertices[start], vertices[end]), color=color, linewidth=linewidth, alpha=alpha)
        return
    faces = ((primitive.get("dimensions") or {}).get("faces") or [])[: _surface_overlay_face_limit(surface=surface)]
    if surface and faces:
        _draw_convex_surface(ax, vertices, faces, color=color)
    linewidth, alpha = _primitive_overlay_wire_style(surface=surface, kind=kind)
    for face in faces:
        if len(face) < 3:
            continue
        cycle = list(face[:3]) + [face[0]]
        pts = vertices[np.asarray(cycle, dtype=int)]
        ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=color, linewidth=linewidth, alpha=alpha)


def _draw_convex_surface(ax: Any, vertices: np.ndarray, faces: Sequence[Sequence[int]], *, color: str) -> None:
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    polygons = []
    for face in faces[:18]:
        if len(face) < 3:
            continue
        polygons.append(vertices[np.asarray(face[:3], dtype=int)])
    if not polygons:
        return
    collection = Poly3DCollection(
        polygons,
        facecolor=color,
        edgecolor=color,
        linewidth=0.12,
        alpha=0.065,
        rasterized=True,
    )
    ax.add_collection3d(collection)


_BOX_EDGES: tuple[tuple[int, int], ...] = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),
)


def _combine_points(*arrays: np.ndarray) -> np.ndarray:
    valid = [array for array in arrays if isinstance(array, np.ndarray) and len(array)]
    if not valid:
        return np.empty((0, 3), dtype=float)
    return np.concatenate(valid, axis=0)


def _finish_3d_axis(
    ax: Any,
    points: np.ndarray,
    *,
    min_radius: float = 0.0,
    elev: float = 20,
    azim: float = -55,
    roll: float | None = None,
    zoom: float = 1.0,
) -> None:
    ax.view_init(elev=elev, azim=azim, roll=roll)
    ax.set_axis_off()
    if not len(points):
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_zlim(-1, 1)
        return
    mins = points.min(axis=0)
    maxs = points.max(axis=0)
    center = (mins + maxs) / 2.0
    radius = float(np.max(maxs - mins) / 2.0)
    if radius <= 0:
        radius = 1.0
    radius = max(radius, min_radius)
    ax.set_xlim(center[0] - radius, center[0] + radius)
    ax.set_ylim(center[1] - radius, center[1] + radius)
    ax.set_zlim(center[2] - radius, center[2] + radius)
    try:
        ax.set_box_aspect((1, 1, 1), zoom=zoom)
    except Exception:
        pass


def _draw_drop_probe_panel(ax: Any, result: Mapping[str, Any] | None) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.06, 1.03)
    ax.axis("off")
    run = _first_run(result, "drop_settle_runs")
    initial = float(((result or {}).get("initial_conditions") or {}).get("height_m", 0.25))
    final = float((run or {}).get("final_height", 0.0))
    min_height = float((run or {}).get("min_height", min(final, 0.0)))
    status = str((result or {}).get("outcome", "not_applicable"))
    labels = probe_failure_labels(result)
    start_xy = (0.35, _scaled_height(initial))
    final_xy = (0.65, _scaled_height(final))
    ax.plot([0.12, 0.88], [0.15, 0.15], color="#222222", linewidth=1.35)
    ax.scatter([start_xy[0]], [start_xy[1]], s=155, color="#7b838c", zorder=3)
    ax.scatter([final_xy[0]], [final_xy[1]], s=155, color=OUTCOME_COLORS.get(status, "#777777"), zorder=4)
    ax.annotate(
        "",
        xy=final_xy,
        xytext=start_xy,
        arrowprops={"arrowstyle": "-|>", "lw": 1.25, "color": "#777777", "shrinkA": 8, "shrinkB": 8},
    )
    ax.text(start_xy[0] - 0.02, start_xy[1] + 0.075, "start", ha="right", va="bottom", fontsize=8.4, color="#555555")
    ax.text(final_xy[0] + 0.02, final_xy[1] + 0.075, "final", ha="left", va="bottom", fontsize=8.4, color=OUTCOME_COLORS.get(status, "#333333"))
    ax.text(0.5, 0.98, f"outcome: {status}", ha="center", va="top", color=OUTCOME_COLORS.get(status, "#333333"), fontsize=10.0)
    ax.text(0.5, 0.02, f"z final/min: {final:.2f} / {min_height:.2f}", ha="center", va="bottom", fontsize=8.8)
    if labels:
        ax.text(
            0.5,
            0.79,
            "\n".join(_short_failure_label(label) for label in labels[:3]),
            ha="center",
            va="top",
            fontsize=8.8,
            color="#b94b48",
            bbox={"facecolor": "white", "edgecolor": "#eeeeee", "alpha": 0.90, "pad": 1.6},
        )


def _draw_stack_probe_panel(ax: Any, result: Mapping[str, Any] | None) -> None:
    ax.set_xlim(0.0, 1.08)
    ax.set_ylim(-0.05, 1.05)
    ax.axis("off")
    run = _first_run(result, "stack_slide_runs")
    status = str((result or {}).get("outcome", "not_applicable"))
    support = float((run or {}).get("support_top_height", 0.55))
    initial = (run or {}).get("initial_probe_position", [0.2, 0.2, support + 0.06])
    final = (run or {}).get("final_probe_position", [0.75, 0.55, support + 0.03])
    horizontal = float((run or {}).get("horizontal_displacement_m", 0.0))
    labels = probe_failure_labels(result)
    ax.add_patch(plt_rectangle((0.09, 0.15), 0.84, 0.20, "#c9cdd2"))
    start = (0.28, 0.62)
    end_x = min(1.02, 0.28 + max(horizontal, 0.12) / max(horizontal, 0.25) * 0.55) if horizontal else 0.50
    end = (end_x, 0.47 if status == "failure" else 0.62)
    ax.add_patch(plt_rectangle((start[0] - 0.07, start[1] - 0.07), 0.14, 0.14, "#7b838c"))
    ax.add_patch(plt_rectangle((end[0] - 0.07, end[1] - 0.07), 0.14, 0.14, OUTCOME_COLORS.get(status, "#777777")))
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops={"arrowstyle": "-|>", "lw": 1.25, "color": "#555555", "shrinkA": 8, "shrinkB": 8},
    )
    ax.text(start[0], start[1] + 0.115, "start", ha="center", va="bottom", fontsize=8.4, color="#555555")
    final_label = "final low" if status == "failure" else "final stable"
    ax.text(end[0], end[1] + 0.115, final_label, ha="center", va="bottom", fontsize=8.4, color=OUTCOME_COLORS.get(status, "#333333"))
    ax.text(0.5, 0.99, f"outcome: {status}", ha="center", va="top", color=OUTCOME_COLORS.get(status, "#333333"), fontsize=10.0)
    ax.text(0.5, 0.03, f"slide: {horizontal:.3f} m", ha="center", va="bottom", fontsize=8.8)
    if labels:
        ax.text(
            0.5,
            0.83,
            "\n".join(_short_failure_label(label) for label in labels[:3]),
            ha="center",
            va="top",
            fontsize=8.8,
            color="#b94b48",
            bbox={"facecolor": "white", "edgecolor": "#eeeeee", "alpha": 0.90, "pad": 1.6},
        )
    _ = initial, final


def _short_failure_label(label: str) -> str:
    return {
        "excess_horizontal_slide": "excess slide",
        "probe_below_support": "below support",
        "floor_breach": "floor breach",
        "not_settled": "not settled",
        "no_descent": "no descent",
    }.get(label, label.replace("_", " "))


def _draw_franka_task_schematic(ax: Any, links: Sequence[Mapping[str, Any]], plt: Any) -> None:
    points = np.asarray(
        [
            (0.08, 0.18),
            (0.16, 0.23),
            (0.24, 0.34),
            (0.32, 0.48),
            (0.43, 0.58),
            (0.54, 0.55),
            (0.64, 0.45),
            (0.72, 0.34),
            (0.78, 0.26),
            (0.85, 0.24),
            (0.91, 0.30),
            (0.96, 0.38),
        ],
        dtype=float,
    )
    link_count = min(len(links), len(points))
    ax.plot([0.02, 1.0], [0.12, 0.12], color="#9aa0a6", linewidth=1.0)
    ax.add_patch(plt.Rectangle((0.035, 0.12), 0.09, 0.07, facecolor="#c9cdd2", edgecolor="#222222", linewidth=0.8))
    ax.add_patch(plt.Rectangle((0.055, 0.19), 0.05, 0.10, facecolor="#e4e7eb", edgecolor="#4d5660", linewidth=0.8))
    ax.text(0.08, 0.06, "gravity hold floor", ha="center", va="center", fontsize=7, color="#555555")
    if link_count:
        ax.plot(points[:link_count, 0], points[:link_count, 1], color="#cfd4da", linewidth=12.0, solid_capstyle="round", alpha=0.62, zorder=1)
        ax.plot(points[:link_count, 0], points[:link_count, 1], color="#4d5660", linewidth=5.0, solid_capstyle="round", alpha=0.84, zorder=2)
    labels = _franka_label_indices(links[:link_count])
    for index in range(link_count):
        link = links[index]
        is_placeholder = int(link.get("placeholder_primitive_count", 0)) > 0
        color = "#a76f1b" if is_placeholder else "#2e7d59"
        x, y = points[index]
        marker_width = 0.070 if is_placeholder else 0.054
        marker_height = 0.050 if is_placeholder else 0.038
        ax.scatter([x], [y], s=135 if is_placeholder else 105, color="white", edgecolor="#222222", linewidth=0.8, zorder=5)
        ax.add_patch(
            plt.Rectangle(
                (x - marker_width / 2.0, y - marker_height / 2.0),
                marker_width,
                marker_height,
                facecolor=color,
                edgecolor="#222222",
                linewidth=0.72 if is_placeholder else 0.55,
                zorder=6,
            )
        )
        if index in labels:
            label = labels[index]
            label_x, label_y, ha = x, y + 0.06, "center"
            if label == "sentinel link8":
                label_x, label_y, ha = x - 0.14, y - 0.16, "right"
            elif label == "right finger":
                label_x, label_y, ha = x - 0.14, y + 0.14, "right"
            elif label == "base link":
                label_x, label_y, ha = x - 0.055, y + 0.055, "right"
            ax.text(
                label_x,
                label_y,
                label,
                ha=ha,
                va="bottom",
                fontsize=7.4,
                bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.76, "pad": 0.6},
            )
            if label in {"sentinel link8", "right finger"}:
                ax.plot([x, label_x + (0.01 if ha == "right" else -0.01)], [y, label_y - 0.008], color="#4d5660", linewidth=0.75)
    if link_count:
        end_x, end_y = points[link_count - 1]
        ax.plot([end_x + 0.025, end_x + 0.075], [end_y + 0.025, end_y + 0.065], color="#4d5660", linewidth=1.4)
        ax.plot([end_x + 0.025, end_x + 0.075], [end_y - 0.025, end_y - 0.065], color="#4d5660", linewidth=1.4)
        ax.text(
            min(1.035, end_x + 0.075),
            end_y - 0.16,
            "end-effector",
            ha="right",
            va="center",
            fontsize=7.6,
            color="#4d5660",
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.76, "pad": 0.6},
        )
        ax.plot([end_x + 0.025, min(1.01, end_x + 0.055)], [end_y - 0.025, end_y - 0.135], color="#4d5660", linewidth=0.75)
    trajectory = np.asarray([(0.78, 0.70), (0.84, 0.63), (0.90, 0.56), (0.96, 0.49)], dtype=float)
    ax.plot(trajectory[:, 0], trajectory[:, 1], color="#2d6cdf", linewidth=1.15, linestyle="--")
    ax.annotate(
        "",
        xy=tuple(trajectory[-1]),
        xytext=tuple(trajectory[-2]),
        arrowprops={"arrowstyle": "->", "lw": 1.0, "color": "#2d6cdf"},
    )
    ax.scatter(trajectory[[0, -1], 0], trajectory[[0, -1], 1], s=18, color="#2d6cdf", zorder=7)
    ax.text(0.66, 0.81, "short trajectory", ha="left", va="center", color="#2d6cdf", fontsize=8)
    ax.text(0.04, 0.96, "gray: Franka-style link chain", ha="left", va="top", fontsize=8, color="#4d5660")
    ax.text(0.04, 0.89, "green boxes: generated link packages", ha="left", va="top", fontsize=8, color="#2e7d59")
    ax.text(0.04, 0.82, "amber: meshless sentinel link", ha="left", va="top", fontsize=8, color="#a76f1b")


def _franka_label_indices(links: Sequence[Mapping[str, Any]]) -> dict[int, str]:
    labels: dict[int, str] = {}
    for index, link in enumerate(links):
        link_name = str(link.get("link_path", "")).rstrip("/").split("/")[-1]
        is_placeholder = int(link.get("placeholder_primitive_count", 0)) > 0
        if link_name == "panda_link0":
            labels[index] = "base link"
        elif link_name == "panda_rightfinger":
            labels[index] = "right finger"
        elif link_name == "panda_link8" or is_placeholder:
            labels[index] = "sentinel link8"
    return labels


def _first_run(result: Mapping[str, Any] | None, key: str) -> Mapping[str, Any] | None:
    runs = (result or {}).get(key) or []
    return runs[0] if runs and isinstance(runs[0], Mapping) else None


def _scaled_height(height: float) -> float:
    return max(0.18, min(0.88, 0.15 + height * 1.8))


def plt_rectangle(xy: tuple[float, float], width: float, height: float, color: str) -> Any:
    from matplotlib.patches import Rectangle

    return Rectangle(xy, width, height, facecolor=color, edgecolor="#222222", linewidth=0.8)


def _draw_outcome_legend(ax: Any) -> None:
    from matplotlib.patches import Patch

    handles = [
        Patch(facecolor="#2e7d59", label="accept"),
        Patch(facecolor="#b94b48", label="failure"),
        Patch(facecolor="#8a8f98", label="fallback"),
        Patch(facecolor="#d5d8dc", label="not applicable"),
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=4, frameon=False)


def _lane_color(lane: str) -> str:
    return {
        "bounding_primitive": "#2d6cdf",
        "cpd_style_primitive_candidate_if_available": "#7a5195",
        "coacd_or_vhacd_if_available": "#ef7d00",
        "vhacd_if_available": "#b94b48",
    }.get(lane, "#333333")


def _write_manifest(
    path: Path,
    *,
    report_path: Path,
    asset_root: Path,
    figures: Sequence[FigureOutput],
) -> None:
    source_records = tuple(dict.fromkeys(record for figure in figures for record in figure.source_records))
    figure_entries = []
    for figure in figures:
        entry = {
            "id": figure.figure_id,
            "path": str(figure.path),
            "evidence": figure.evidence,
            "source_records": list(figure.source_records),
        }
        if figure.renderer_metadata:
            entry["renderer_metadata"] = copy.deepcopy(dict(figure.renderer_metadata))
        figure_entries.append(entry)
    payload = {
        "schema_version": 1,
        "report_path": str(report_path),
        "report_sha256": _sha256_file(report_path),
        "asset_root": str(asset_root),
        "generation": "deterministic_matplotlib_diagnostic_visualization",
        "claim_boundary": "diagnostic_visualization_not_photorealistic_render_or_new_experiment",
        "source_record_hashes": _source_record_hashes(source_records),
        "figures": figure_entries,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _save_pdf(fig: Any, path: Path) -> None:
    fig.savefig(path, bbox_inches="tight", metadata=dict(PDF_METADATA))


def _load_result_entry(result_id: str) -> Mapping[str, Any]:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML is required to load paper evidence manifests") from exc
    payload = yaml.safe_load(RESULTS_MANIFEST.read_text(encoding="utf-8")) or {}
    for entry in payload.get("results", []) or []:
        if entry.get("id") == result_id:
            return entry
    raise RuntimeError(f"missing result entry {result_id!r} in {RESULTS_MANIFEST}")


def _split_evidence_sources(value: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in value.split(";") if part.strip())


def _source_record_hashes(records: Sequence[str]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for record in records:
        path = Path(record)
        if not path.is_absolute():
            path = REPO_ROOT / path
        if not path.exists():
            raise RuntimeError(f"missing source record for paper figure manifest: {record}")
        hashes[record] = _sha256_file(path)
    return hashes


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate ACCV Phase 0 paper visuals.")
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--asset-root", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args(argv)
    figures = generate_accv_visuals(
        report_path=args.report,
        asset_root=args.asset_root,
        output_dir=args.output_dir,
    )
    for figure in figures:
        print(f"{figure.figure_id}: {figure.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
