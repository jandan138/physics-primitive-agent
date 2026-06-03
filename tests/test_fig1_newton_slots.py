from __future__ import annotations

import os
from pathlib import Path

from PIL import Image

from primitive_collision_compiler.paper.fig1_newton_slots import (
    FIG1_NEWTON_SLOT_NAMES,
    build_newton_slot_worker_command,
    load_newton_slot_manifest,
    source_artifact_path,
    write_newton_slot_manifest,
)


def _slot_png(path: Path, color: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (48, 32), color).save(path)


def test_worker_command_uses_external_newton_python_and_pythonpath(tmp_path: Path) -> None:
    command, env = build_newton_slot_worker_command(
        output_dir=tmp_path / "slots",
        source_artifact_root=Path("/source/root"),
        python_executable=Path("/env/bin/python"),
        newton_root=Path("/newton"),
        phase0_report=Path("reports/generated/phase0.json"),
        asset_manifest=Path("assets/manifests/assets.yaml"),
    )

    assert command[:3] == [
        "/env/bin/python",
        "-m",
        "primitive_collision_compiler.paper.fig1_newton_slots",
    ]
    assert "--worker-render" in command
    assert str(tmp_path / "slots") in command
    assert env["PPA_FIG1_SOURCE_ARTIFACT_ROOT"] == "/source/root"
    pythonpath_parts = env["PYTHONPATH"].split(os.pathsep)
    assert pythonpath_parts[0] == "/newton"
    assert str(Path(__file__).resolve().parents[1] / "src") in pythonpath_parts
    assert str(Path(__file__).resolve().parents[1]) in pythonpath_parts


def test_source_artifact_path_uses_explicit_root_for_ignored_inputs() -> None:
    resolved = source_artifact_path(
        "reports/generated/example.json",
        source_artifact_root=Path("/cpfs/project"),
    )

    assert resolved == Path("/cpfs/project/reports/generated/example.json")


def test_source_artifact_path_preserves_absolute_inputs() -> None:
    resolved = source_artifact_path(
        "/abs/reports/generated/example.json",
        source_artifact_root=Path("/cpfs/project"),
    )

    assert resolved == Path("/abs/reports/generated/example.json")


def test_write_newton_slot_manifest_requires_three_rendered_slots(tmp_path: Path) -> None:
    slot_artifacts = {}
    colors = ("#6e94c4", "#5f9f75", "#c9873f")
    for slot, color in zip(FIG1_NEWTON_SLOT_NAMES, colors):
        png = tmp_path / f"{slot}_newton.png"
        _slot_png(png, color)
        sidecar = tmp_path / f"{slot}_newton.json"
        sidecar.write_text(
            (
                "{\n"
                f'  "slot": "{slot}",\n'
                '  "renderer": "newton_sensor_tiled_camera",\n'
                '  "claim_boundary": "visual exposition only; not experimental evidence"\n'
                "}\n"
            ),
            encoding="utf-8",
        )
        slot_artifacts[slot] = {"png": png, "sidecar": sidecar}

    manifest_path = write_newton_slot_manifest(
        output_dir=tmp_path,
        slot_artifacts=slot_artifacts,
        source_report=Path("/source/report.json"),
        source_manifest=Path("/source/assets.yaml"),
        source_artifact_root=Path("/source"),
        newton_root=Path("/newton"),
        newton_commit="abc123",
    )

    manifest = load_newton_slot_manifest(manifest_path)
    assert manifest["mode"] == "newton_render_slots"
    assert manifest["renderer"] == "newton_sensor_tiled_camera"
    assert set(manifest["slots"]) == set(FIG1_NEWTON_SLOT_NAMES)
    assert manifest["newton"]["commit"] == "abc123"
    assert manifest["source_artifact_root"] == "/source"
    assert "not experimental evidence" in manifest["claim_boundary"]
    for slot in FIG1_NEWTON_SLOT_NAMES:
        assert Path(manifest["slots"][slot]["image"]).is_file()
        assert Path(manifest["slots"][slot]["sidecar"]).is_file()


def test_write_newton_slot_manifest_rejects_missing_slot(tmp_path: Path) -> None:
    png = tmp_path / "asset_intake_newton.png"
    _slot_png(png, "#6e94c4")
    sidecar = tmp_path / "asset_intake_newton.json"
    sidecar.write_text('{"renderer": "newton_sensor_tiled_camera"}', encoding="utf-8")

    try:
        write_newton_slot_manifest(
            output_dir=tmp_path,
            slot_artifacts={"asset_intake": {"png": png, "sidecar": sidecar}},
            source_report=Path("/source/report.json"),
            source_manifest=Path("/source/assets.yaml"),
            newton_root=Path("/newton"),
            newton_commit="abc123",
        )
    except ValueError as exc:
        assert "candidate_package" in str(exc)
        assert "newton_diagnostics" in str(exc)
    else:
        raise AssertionError("missing Fig.1 Newton slots should be rejected")
