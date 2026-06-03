from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import os
import subprocess
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
FIG1_FRANKA_RTX_SLOT_NAMES = ("asset_intake", "candidate_package", "newton_diagnostics")
DEFAULT_NEWTON_ROOT = Path("/cpfs/shared/simulation/zhuzihou/dev/newton")
DEFAULT_NEWTON_PYTHON = Path(
    "/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python"
)
DEFAULT_SOURCE_ARTIFACT_ROOT = Path(
    os.environ.get("PPA_FIG1_SOURCE_ARTIFACT_ROOT", str(REPO_ROOT))
)
DEFAULT_OUTPUT_DIR = REPO_ROOT / "paper/shared/figures/assets/fig1_franka_rtx_slots"
DEFAULT_PHASE0_REPORT = Path(
    "reports/generated/phase0_baseline/phase0_grscenes_rigid_plus_franka_newton_2026-05-26.json"
)
DEFAULT_FRANKA_ASSET_MANIFEST = Path("assets/manifests/franka_usd_smoke_assets.yaml")
FIG1_FRANKA_RTX_CLAIM_BOUNDARY = (
    "Franka RTX Fig.1 slots are visual exposition from one recorded smoke asset; "
    "not whole-robot collision quality or manipulation evidence."
)
RTX_RENDERER = "newton_viewer_rtx_ovrtx"
FRANKA_DISPLAY_POSE_Q = (
    -3.6802115e-03,
    2.3901723e-02,
    3.6804110e-03,
    -2.3683236e00,
    -1.2918962e-04,
    2.3922248e00,
    7.8549200e-01,
    0.05,
    0.05,
)
FRANKA_DISPLAY_POSE_SOURCE = "newton_examples_franka_ready_pose"
FRANKA_DISPLAY_POSE_CLAIM_BOUNDARY = (
    "Fixed display pose for Fig.1 visual readability; not manipulation evidence."
)


def source_artifact_path(path: str | Path, *, source_artifact_root: Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else Path(source_artifact_root) / candidate


def build_franka_rtx_worker_command(
    *,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    source_artifact_root: str | Path = DEFAULT_SOURCE_ARTIFACT_ROOT,
    python_executable: str | Path = DEFAULT_NEWTON_PYTHON,
    newton_root: str | Path = DEFAULT_NEWTON_ROOT,
    phase0_report: str | Path = DEFAULT_PHASE0_REPORT,
    asset_manifest: str | Path = DEFAULT_FRANKA_ASSET_MANIFEST,
) -> tuple[list[str], dict[str, str]]:
    env = os.environ.copy()
    newton_root_path = Path(newton_root)
    env["PPA_FIG1_SOURCE_ARTIFACT_ROOT"] = str(source_artifact_root)
    env["PYTHONPATH"] = _prepend_pythonpath(
        [newton_root_path, REPO_ROOT / "src", REPO_ROOT],
        env.get("PYTHONPATH", ""),
    )
    command = [
        str(python_executable),
        "-m",
        "primitive_collision_compiler.paper.fig1_franka_rtx_slots",
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
        str(newton_root_path),
    ]
    return command, env


def select_franka_articulation_case(report: Mapping[str, Any]) -> Mapping[str, Any]:
    for case in report.get("articulation_cases", []) or []:
        if not isinstance(case, Mapping) or case.get("asset_role") != "franka_import_smoke":
            continue
        _validate_franka_case(case)
        return case
    raise ValueError("Phase0 report missing franka_import_smoke articulation case")


def franka_case_summary(case: Mapping[str, Any]) -> dict[str, Any]:
    robot_result = _robot_package_result(case)
    audit = _link_boundary_audit(robot_result)
    metrics = audit.get("metrics") or {}
    package = robot_result.get("collision_package") or {}
    primitives = package.get("primitives", []) if isinstance(package, Mapping) else []
    return {
        "asset_id": case.get("asset_id", ""),
        "asset_role": case.get("asset_role", ""),
        "asset_path": case.get("local_path", ""),
        "robot_package_status": robot_result.get("status", ""),
        "primitive_or_hull_count": int(robot_result.get("primitive_or_hull_count", 0) or 0),
        "package_method": package.get("method", "") if isinstance(package, Mapping) else "",
        "package_status": package.get("status", "") if isinstance(package, Mapping) else "",
        "package_primitive_count": len(primitives) if isinstance(primitives, list) else 0,
        "link_boundary_status": audit.get("status", ""),
        "link_count": int(metrics.get("link_count", 0) or 0),
        "primitive_count": int(metrics.get("primitive_count", 0) or 0),
        "cross_link_merge_count": int(metrics.get("cross_link_merge_count", 0) or 0),
        "meshless_link_placeholder_count": int(
            metrics.get("meshless_link_placeholder_count", 0) or 0
        ),
        "links_without_primitive_count": int(metrics.get("links_without_primitive_count", 0) or 0),
    }


def load_franka_rtx_slot_manifest(path: str | Path) -> dict[str, Any]:
    manifest_path = Path(path)
    payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    if payload.get("mode") != "newton_rtx_franka_render_slots":
        raise ValueError("Fig.1 Franka RTX slot manifest must use mode: newton_rtx_franka_render_slots")
    if payload.get("renderer") != RTX_RENDERER:
        raise ValueError(f"Fig.1 Franka RTX slot manifest must use renderer: {RTX_RENDERER}")
    slots = payload.get("slots")
    if not isinstance(slots, Mapping):
        raise ValueError("Fig.1 Franka RTX slot manifest missing slots mapping")
    missing = [slot for slot in FIG1_FRANKA_RTX_SLOT_NAMES if slot not in slots]
    if missing:
        raise ValueError(f"Fig.1 Franka RTX slot manifest missing slots: {', '.join(missing)}")
    for slot in FIG1_FRANKA_RTX_SLOT_NAMES:
        slot_record = slots.get(slot)
        if not isinstance(slot_record, Mapping):
            raise ValueError(f"Fig.1 Franka RTX slot record must be a mapping: {slot}")
        for field in ("image", "sidecar"):
            resolved = _manifest_path_to_file(str(slot_record.get(field, "")))
            if not resolved.is_file():
                raise FileNotFoundError(resolved)
    return dict(payload)


def write_franka_rtx_slot_manifest(
    *,
    output_dir: str | Path,
    slot_artifacts: Mapping[str, Mapping[str, str | Path]],
    source_report: str | Path,
    source_manifest: str | Path,
    source_artifact_root: str | Path | None = None,
    newton_root: str | Path,
    newton_commit: str,
    ovrtx_version: str,
) -> Path:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    missing = [slot for slot in FIG1_FRANKA_RTX_SLOT_NAMES if slot not in slot_artifacts]
    if missing:
        raise ValueError(f"missing Fig.1 Franka RTX slots: {', '.join(missing)}")

    slots: dict[str, dict[str, Any]] = {}
    for slot in FIG1_FRANKA_RTX_SLOT_NAMES:
        record = slot_artifacts[slot]
        png = Path(record["png"])
        sidecar = Path(record["sidecar"])
        if not png.is_file():
            raise FileNotFoundError(png)
        if not sidecar.is_file():
            raise FileNotFoundError(sidecar)
        slots[slot] = {
            "image": _manifest_file_value(png),
            "sidecar": _manifest_file_value(sidecar),
            "image_sha256": _sha256_file(png),
            "sidecar_sha256": _sha256_file(sidecar),
        }

    manifest = {
        "schema_version": 1,
        "mode": "newton_rtx_franka_render_slots",
        "renderer": RTX_RENDERER,
        "slots": slots,
        "source_report": str(source_report),
        "source_report_sha256": _sha256_file(Path(source_report)) if Path(source_report).is_file() else "",
        "source_manifest": str(source_manifest),
        "source_manifest_sha256": (
            _sha256_file(Path(source_manifest)) if Path(source_manifest).is_file() else ""
        ),
        "source_artifact_root": str(source_artifact_root or ""),
        "newton": {
            "root": str(newton_root),
            "commit": newton_commit,
        },
        "rtx": {
            "renderer": RTX_RENDERER,
            "ovrtx_version": ovrtx_version,
        },
        "claim_boundary": FIG1_FRANKA_RTX_CLAIM_BOUNDARY,
    }
    manifest_path = output / "manifest.yaml"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    return manifest_path


def render_franka_rtx_slots_via_worker(
    *,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    source_artifact_root: str | Path = DEFAULT_SOURCE_ARTIFACT_ROOT,
    python_executable: str | Path = DEFAULT_NEWTON_PYTHON,
    newton_root: str | Path = DEFAULT_NEWTON_ROOT,
    phase0_report: str | Path = DEFAULT_PHASE0_REPORT,
    asset_manifest: str | Path = DEFAULT_FRANKA_ASSET_MANIFEST,
) -> Path:
    command, env = build_franka_rtx_worker_command(
        output_dir=output_dir,
        source_artifact_root=source_artifact_root,
        python_executable=python_executable,
        newton_root=newton_root,
        phase0_report=phase0_report,
        asset_manifest=asset_manifest,
    )
    subprocess.run(command, cwd=REPO_ROOT, env=env, check=True)
    return Path(output_dir) / "manifest.yaml"


def _worker_render_all(args: argparse.Namespace) -> int:
    # Worker-only heavy imports. Normal tests can import this module without Newton/OVRTX.
    import newton
    import newton.viewer
    import warp as wp

    source_root = Path(args.source_artifact_root)
    report_path = source_artifact_path(args.phase0_report, source_artifact_root=source_root)
    asset_manifest_path = source_artifact_path(args.asset_manifest, source_artifact_root=source_root)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = json.loads(report_path.read_text(encoding="utf-8"))
    case = select_franka_articulation_case(report)
    asset_path = source_artifact_path(str(case["local_path"]), source_artifact_root=source_root)
    if not asset_path.is_file():
        raise FileNotFoundError(asset_path)

    newton_commit = _git_commit(Path(args.newton_root))
    ovrtx_version = _installed_version("ovrtx")

    slot_artifacts: dict[str, dict[str, Path]] = {}
    for slot in FIG1_FRANKA_RTX_SLOT_NAMES:
        slot_artifacts[slot] = _render_franka_slot(
            newton=newton,
            wp=wp,
            slot=slot,
            case=case,
            asset_path=asset_path,
            report_path=report_path,
            asset_manifest_path=asset_manifest_path,
            output_dir=output_dir,
            newton_root=Path(args.newton_root),
            newton_commit=newton_commit,
            source_artifact_root=source_root,
            ovrtx_version=ovrtx_version,
        )

    manifest = write_franka_rtx_slot_manifest(
        output_dir=output_dir,
        slot_artifacts=slot_artifacts,
        source_report=report_path,
        source_manifest=asset_manifest_path,
        source_artifact_root=source_root,
        newton_root=Path(args.newton_root),
        newton_commit=newton_commit,
        ovrtx_version=ovrtx_version,
    )
    print(f"fig1_franka_rtx_slots: {manifest}")
    return 0


def _render_franka_slot(
    *,
    newton: Any,
    wp: Any,
    slot: str,
    case: Mapping[str, Any],
    asset_path: Path,
    report_path: Path,
    asset_manifest_path: Path,
    output_dir: Path,
    newton_root: Path,
    newton_commit: str,
    source_artifact_root: Path,
    ovrtx_version: str,
) -> dict[str, Path]:
    builder, details = _build_franka_rtx_scene(newton=newton, wp=wp, slot=slot, case=case, asset_path=asset_path)
    png = output_dir / f"{slot}_franka_rtx.png"
    _render_model_rtx(
        newton=newton,
        wp=wp,
        builder=builder,
        output=png,
        camera=_camera_for_slot(slot),
    )
    sidecar = output_dir / f"{slot}_franka_rtx.json"
    _write_sidecar(
        sidecar,
        slot=slot,
        case=case,
        report_path=report_path,
        asset_manifest_path=asset_manifest_path,
        asset_path=asset_path,
        newton_root=newton_root,
        newton_commit=newton_commit,
        source_artifact_root=source_artifact_root,
        ovrtx_version=ovrtx_version,
        details=details,
    )
    return {"png": png, "sidecar": sidecar}


def _build_franka_rtx_scene(
    *,
    newton: Any,
    wp: Any,
    slot: str,
    case: Mapping[str, Any],
    asset_path: Path,
) -> tuple[Any, dict[str, Any]]:
    builder = newton.ModelBuilder(up_axis=newton.Axis.Z)
    import_result = builder.add_usd(
        str(asset_path),
        floating=False,
        collapse_fixed_joints=False,
        enable_self_collisions=False,
        hide_collision_shapes=True,
        load_visual_shapes=True,
        skip_mesh_approximation=True,
    )
    display_pose = _apply_franka_display_pose(builder)
    details: dict[str, Any] = {
        "recipe": "newton_viewer_rtx_render_project_franka_usd_smoke_asset",
        "render_asset_source": str(asset_path),
        "franka_summary": franka_case_summary(case),
        "display_pose": display_pose,
        "usd_import": {
            "body_count": int(builder.body_count),
            "shape_count": int(builder.shape_count),
            "joint_count": int(builder.joint_count),
            "path_body_count": len(import_result.get("path_body_map", {}))
            if isinstance(import_result, Mapping)
            else 0,
        },
    }
    if slot in {"candidate_package", "newton_diagnostics"}:
        box_color = (0.13, 0.55, 0.86) if slot == "candidate_package" else (0.92, 0.52, 0.16)
        package_details = _add_recorded_link_boxes(
            wp=wp,
            builder=builder,
            case=case,
            color=box_color,
            slot=slot,
        )
        details["recorded_package_overlay"] = package_details
    if slot == "newton_diagnostics":
        details["diagnostic_markers"] = _add_diagnostic_markers(wp=wp, builder=builder)
        details["recorded_probe_summary"] = _recorded_probe_summary(case)
    builder.add_ground_plane(color=(0.72, 0.74, 0.77))
    return builder, details


def _apply_franka_display_pose(builder: Any) -> dict[str, Any]:
    if len(builder.joint_q) < len(FRANKA_DISPLAY_POSE_Q):
        raise ValueError(
            f"Franka display pose requires at least {len(FRANKA_DISPLAY_POSE_Q)} joint coordinates"
        )
    builder.joint_q[: len(FRANKA_DISPLAY_POSE_Q)] = list(FRANKA_DISPLAY_POSE_Q)
    return {
        "source": FRANKA_DISPLAY_POSE_SOURCE,
        "joint_q": list(FRANKA_DISPLAY_POSE_Q),
        "claim_boundary": FRANKA_DISPLAY_POSE_CLAIM_BOUNDARY,
    }


def _add_recorded_link_boxes(
    *,
    wp: Any,
    builder: Any,
    case: Mapping[str, Any],
    color: tuple[float, float, float],
    slot: str,
) -> dict[str, Any]:
    package = _robot_package_result(case).get("collision_package") or {}
    primitives = package.get("primitives", []) if isinstance(package, Mapping) else []
    body_by_label = {label: index for index, label in enumerate(builder.body_label)}
    rendered = 0
    missing_frames: list[str] = []
    for index, primitive in enumerate(primitives):
        if not isinstance(primitive, Mapping) or primitive.get("kind") != "box":
            continue
        frame = str(primitive.get("frame") or "")
        body = body_by_label.get(frame)
        if body is None:
            missing_frames.append(frame)
            continue
        dimensions = primitive.get("dimensions") or {}
        half_extents = dimensions.get("half_extents") or []
        center = primitive.get("center") or (0.0, 0.0, 0.0)
        if len(half_extents) != 3 or len(center) != 3:
            continue
        hx, hy, hz = (max(float(value), 0.0035) for value in half_extents)
        cx, cy, cz = (float(value) for value in center)
        builder.add_shape_box(
            body,
            xform=wp.transform(p=wp.vec3(cx, cy, cz), q=wp.quat_identity()),
            hx=hx,
            hy=hy,
            hz=hz,
            color=color,
            label=f"fig1_{slot}_link_box_{index}",
        )
        rendered += 1
    if missing_frames:
        raise ValueError(
            "recorded link-aware box frames missing from imported Franka body labels: "
            + ", ".join(missing_frames)
        )
    if rendered != len(primitives):
        raise ValueError(
            f"rendered {rendered} recorded link-aware boxes, expected {len(primitives)}"
        )
    return {
        "recipe": "recorded_link_aware_box_primitives_attached_to_matching_newton_bodies",
        "package_method": package.get("method", "") if isinstance(package, Mapping) else "",
        "recorded_primitive_count": len(primitives) if isinstance(primitives, list) else 0,
        "rendered_primitive_count": rendered,
        "missing_frames": missing_frames,
    }


def _add_diagnostic_markers(*, wp: Any, builder: Any) -> dict[str, Any]:
    markers = (
        ((0.36, -0.28, 0.72), 0.046, (0.82, 0.20, 0.18), "body_state_probe"),
        ((0.12, -0.36, 0.38), 0.044, (0.18, 0.42, 0.82), "contact_probe"),
        ((0.22, 0.20, 0.80), 0.044, (0.18, 0.58, 0.34), "robot_task_probe"),
    )
    for position, radius, color, label in markers:
        builder.add_shape_sphere(
            -1,
            xform=wp.transform(p=wp.vec3(*position), q=wp.quat_identity()),
            radius=radius,
            color=color,
            label=f"fig1_{label}",
        )
    return {
        "recipe": "world_space_probe_markers_for_recorded_smoke_checks",
        "marker_count": len(markers),
        "marker_labels": [label for _position, _radius, _color, label in markers],
    }


def _render_model_rtx(
    *,
    newton: Any,
    wp: Any,
    builder: Any,
    output: Path,
    camera: Mapping[str, Any],
    image_size: tuple[int, int] = (640, 420),
) -> None:
    from PIL import Image

    output.parent.mkdir(parents=True, exist_ok=True)
    model = builder.finalize()
    state = model.state()
    newton.eval_fk(model, model.joint_q, model.joint_qd, state)

    viewer = newton.viewer.ViewerRTX(
        width=int(image_size[0]),
        height=int(image_size[1]),
        headless=True,
        paused=False,
        num_frames=4,
        environment="studio",
        async_rendering=False,
    )
    try:
        viewer.set_model(model)
        pitch, yaw = _look_at_angles(camera["pos"], camera["target"])
        viewer.set_camera(
            pos=wp.vec3(*camera["pos"]),
            pitch=pitch,
            yaw=yaw,
        )
        if hasattr(viewer, "camera") and hasattr(viewer.camera, "fov"):
            viewer.camera.fov = float(camera.get("fov", 58.0))
        for frame in range(4):
            viewer.begin_frame(frame / 60.0)
            viewer.log_state(state)
            viewer.end_frame()
            wp.synchronize()
        viewer.save_screenshot(str(output))
    finally:
        viewer.close()

    image = Image.open(output).convert("RGB")
    image.save(output)


def _camera_for_slot(slot: str) -> dict[str, Any]:
    return {
        "asset_intake": {
            "pos": (-1.18, -1.36, 0.82),
            "target": (0.0, 0.0, 0.48),
            "fov": 44.0,
        },
        "candidate_package": {
            "pos": (-1.22, -1.28, 0.84),
            "target": (0.0, 0.0, 0.48),
            "fov": 46.0,
        },
        "newton_diagnostics": {
            "pos": (-1.30, -1.18, 0.96),
            "target": (0.04, 0.0, 0.50),
            "fov": 50.0,
        },
    }[slot]


def _look_at_angles(pos: Sequence[float], target: Sequence[float]) -> tuple[float, float]:
    dx = float(target[0]) - float(pos[0])
    dy = float(target[1]) - float(pos[1])
    dz = float(target[2]) - float(pos[2])
    distance = math.sqrt(dx * dx + dy * dy + dz * dz)
    if distance <= 1e-9:
        raise ValueError("camera position and target must be different")
    pitch = math.degrees(math.asin(max(min(dz / distance, 1.0), -1.0)))
    yaw = math.degrees(math.atan2(dy, dx))
    return pitch, yaw


def _recorded_probe_summary(case: Mapping[str, Any]) -> dict[str, Any]:
    probe_results = case.get("probe_results") or {}
    if not isinstance(probe_results, Mapping):
        return {}
    summary: dict[str, Any] = {}
    for probe in (
        "articulation_smoke_if_robot",
        "generated_package_robot_task_if_robot",
        "link_boundary_audit",
    ):
        result = probe_results.get(probe) or {}
        if isinstance(result, Mapping):
            summary[probe] = {
                "status": result.get("status", "unknown"),
                "outcome": result.get("outcome", "unknown"),
                "claim_boundary": result.get("claim_boundary", ""),
            }
    return summary


def _write_sidecar(
    path: Path,
    *,
    slot: str,
    case: Mapping[str, Any],
    report_path: Path,
    asset_manifest_path: Path,
    asset_path: Path,
    newton_root: Path,
    newton_commit: str,
    source_artifact_root: Path,
    ovrtx_version: str,
    details: Mapping[str, Any],
) -> None:
    payload = {
        "schema_version": 1,
        "slot": slot,
        "renderer": RTX_RENDERER,
        "image_size_px": [640, 420],
        "asset_id": case.get("asset_id", ""),
        "asset_role": case.get("asset_role", ""),
        "source_asset": str(asset_path),
        "source_asset_sha256": _sha256_file(asset_path),
        "source_report": str(report_path),
        "source_report_sha256": _sha256_file(report_path),
        "source_manifest": str(asset_manifest_path),
        "source_manifest_sha256": _sha256_file(asset_manifest_path),
        "source_artifact_root": str(source_artifact_root),
        "newton": {
            "root": str(newton_root),
            "commit": newton_commit,
        },
        "rtx": {
            "renderer": RTX_RENDERER,
            "ovrtx_version": ovrtx_version,
        },
        "claim_boundary": FIG1_FRANKA_RTX_CLAIM_BOUNDARY,
        "details": dict(details),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _validate_franka_case(case: Mapping[str, Any]) -> None:
    robot_result = _robot_package_result(case)
    if robot_result.get("status") != "generated":
        raise ValueError("franka_import_smoke robot_package_result must have status=generated")
    audit = _link_boundary_audit(robot_result)
    if audit.get("status") != "smoke_passed":
        raise ValueError("franka_import_smoke link_boundary_audit must have status=smoke_passed")
    summary = franka_case_summary(case)
    if summary["link_count"] < 1 or summary["primitive_count"] < 1:
        raise ValueError("franka_import_smoke link-aware package must include links and primitives")
    if summary["cross_link_merge_count"] != 0:
        raise ValueError("franka_import_smoke link-aware package must not include cross-link merges")


def _robot_package_result(case: Mapping[str, Any]) -> Mapping[str, Any]:
    result = case.get("robot_package_result") or {}
    if not isinstance(result, Mapping):
        raise ValueError("franka_import_smoke case missing robot_package_result")
    return result


def _link_boundary_audit(robot_result: Mapping[str, Any]) -> Mapping[str, Any]:
    audit = robot_result.get("link_boundary_audit") or {}
    if not isinstance(audit, Mapping):
        raise ValueError("franka_import_smoke robot_package_result missing link_boundary_audit")
    return audit


def _git_commit(root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--short=12", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return "unknown"
    return result.stdout.strip()


def _installed_version(package: str) -> str:
    try:
        return importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


def _prepend_pythonpath(paths: Sequence[Path], existing: str) -> str:
    parts = [str(path) for path in paths]
    if existing:
        parts.extend(part for part in existing.split(os.pathsep) if part)
    return os.pathsep.join(parts)


def _manifest_file_value(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def _manifest_path_to_file(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else REPO_ROOT / path


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate ACCV Fig.1 Franka RTX slot images.")
    parser.add_argument("--worker-render", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--source-artifact-root", type=Path, default=DEFAULT_SOURCE_ARTIFACT_ROOT)
    parser.add_argument("--phase0-report", type=Path, default=DEFAULT_PHASE0_REPORT)
    parser.add_argument("--asset-manifest", type=Path, default=DEFAULT_FRANKA_ASSET_MANIFEST)
    parser.add_argument("--newton-root", type=Path, default=DEFAULT_NEWTON_ROOT)
    parser.add_argument("--python-executable", type=Path, default=DEFAULT_NEWTON_PYTHON)
    args = parser.parse_args(argv)
    if args.worker_render:
        return _worker_render_all(args)
    manifest = render_franka_rtx_slots_via_worker(
        output_dir=args.output_dir,
        source_artifact_root=args.source_artifact_root,
        python_executable=args.python_executable,
        newton_root=args.newton_root,
        phase0_report=args.phase0_report,
        asset_manifest=args.asset_manifest,
    )
    print(f"fig1_franka_rtx_slots: {manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
