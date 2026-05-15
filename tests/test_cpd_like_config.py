from pathlib import Path

import yaml

from primitive_collision_compiler.config import load_compile_config


def test_cpd_like_baseline_preserves_newton_and_cpd_sections():
    config = load_compile_config("configs/experiments/cpd_like_baseline.yaml")

    assert config.asset_id == "grscenes_bed_0a85b986_smoke"
    assert config.asset_path == "assets/manifests/cpd_like_smoke_assets.yaml"
    assert config.task == "collision_proxy_diagnostic"
    assert config.method == "cpd_like_baseline"
    assert config.max_primitives == 32
    assert config.allowed_fallback == ("convex_hull",)
    assert config.verify == ("newton_import", "newton_contact_smoke")
    assert config.keep_visual is False
    assert config.protocol["newton"]["source_dir"] == "$NEWTON_SOURCE_DIR"
    assert config.protocol["newton_diagnostic"]["probe_type"] == "contact_canary"
    assert config.protocol["newton_diagnostic"]["device"] == "cpu"
    assert config.protocol["cpd_like"]["asset_manifest"] == "assets/manifests/cpd_like_smoke_assets.yaml"
    assert config.protocol["cpd_like"]["asset_role"] == "bed_dev_smoke"
    assert config.protocol["cpd_like"]["primitive_subset"] == ["sphere", "capsule", "box"]
    assert config.protocol["cpd_like"]["decomposition_stage"] == "cpd_like_face_merge_smoke"
    assert config.protocol["cpd_like"]["max_source_faces"] == 256
    assert config.protocol["cpd_like"]["unsupported_primitives"] == [
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
    assert config.protocol["cpd_like"]["claim_boundary"] == "internal_baseline_not_reproduction_claim"
    assert config.protocol["report"]["output_dir"] == "reports/generated/cpd_like_baseline"
    assert config.protocol["report"]["evidence_level"] == "newton_contact_canary_smoke"


def test_cpd_like_capped_cylinder_proxy_config_is_offline_only():
    config = load_compile_config("configs/experiments/cpd_like_capped_cylinder_proxy.yaml")

    assert config.asset_id == "grscenes_bed_0a85b986_capped_cylinder_proxy"
    assert config.verify == ("cpd_like_objective_report",)
    assert "newton" not in config.protocol
    assert "newton_diagnostic" not in config.protocol
    assert config.protocol["cpd_like"]["primitive_subset"] == ["capped_cylinder"]
    assert config.protocol["cpd_like"]["unsupported_primitives"] == [
        "frustum",
        "trapezoidal_prism",
    ]
    assert config.protocol["cpd_like"]["decomposition_stage"] == "cpd_like_component_merge_gate"
    assert config.protocol["cpd_like_objective"]["primitive_type_weights"] == {
        "capped_cylinder": 1.0
    }


def test_smoke_asset_manifest_records_paths_without_committing_assets():
    manifest = yaml.safe_load(Path("assets/manifests/cpd_like_smoke_assets.yaml").read_text())

    assert manifest["manifest_id"] == "cpd_like_smoke_assets_2026_05_14"
    roles = {asset["role"]: asset for asset in manifest["assets"]}
    assert roles["bed_dev_smoke"]["path"].endswith("0a85b986de35ccfdec7c686d791fd747.usd")
    assert (
        roles["bed_dev_smoke"]["sha256"]
        == "1bc5a26ddb2551de4ac7acbc13a39d118beda10db503419da65ce82528322265"
    )
    assert Path(roles["franka_import_smoke"]["path"]).name == "franka.usd"
    assert roles["franka_import_smoke"]["include_in_cpd_like_aggregate"] is False


def test_franka_smoke_asset_manifest_records_robot_path_without_committing_asset():
    manifest = yaml.safe_load(Path("assets/manifests/franka_usd_smoke_assets.yaml").read_text())

    assert manifest["manifest_id"] == "franka_usd_smoke_assets_2026_05_15"
    roles = {asset["role"]: asset for asset in manifest["assets"]}
    assert Path(roles["franka_import_smoke"]["path"]).name == "franka.usd"
    assert (
        roles["franka_import_smoke"]["sha256"]
        == "2bfd004928d4157ca2fdca3e79bcfb913b4008eef3ec16f839ad89314141976b"
    )
    assert roles["franka_import_smoke"]["include_in_cpd_like_aggregate"] is False


def test_cpd_like_runtime_dependencies_include_numpy():
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")

    assert '"numpy>=1.26"' in pyproject


def test_cpd_like_baseline_config_keeps_machine_paths_in_manifest_not_config():
    config_text = Path("configs/experiments/cpd_like_baseline.yaml").read_text(encoding="utf-8")

    assert "/cpfs/user/" not in config_text
    assert "$NEWTON_SOURCE_DIR" in config_text


def test_newton_drop_settle_config_owns_probe_parameters():
    config_path = Path("configs/experiments/newton_drop_settle.yaml")
    config = load_compile_config(config_path)

    assert config.asset_id == "grscenes_bed_0a85b986_drop_settle"
    assert config.verify == ("newton_drop_settle",)
    assert config.protocol["newton"]["source_dir"] == "$NEWTON_SOURCE_DIR"
    assert config.protocol["newton_diagnostic"]["probe_type"] == "drop_settle"
    assert config.protocol["newton_diagnostic"]["device"] == "cpu"
    assert config.protocol["newton_diagnostic"]["claim_boundary"] == (
        "drop_settle_task_smoke_not_collision_quality_or_safety"
    )
    assert config.protocol["newton_diagnostic"]["drop_settle"]["frames"] == 360
    assert config.protocol["newton_diagnostic"]["drop_settle"]["substeps"] == 8
    assert config.protocol["newton_diagnostic"]["drop_settle"]["height_m"] == 0.25
    assert config.protocol["newton_diagnostic"]["drop_settle"]["max_floor_breach_m"] == 0.05
    assert config.protocol["newton_diagnostic"]["drop_settle"]["max_settle_linear_speed_mps"] == 0.05
    assert config.protocol["report"]["evidence_level"] == "newton_drop_settle_task_smoke"
    assert "/cpfs/user/" not in config_path.read_text(encoding="utf-8")


def test_newton_sphere_rain_config_owns_probe_parameters():
    config_path = Path("configs/experiments/newton_sphere_rain.yaml")
    config = load_compile_config(config_path)

    assert config.asset_id == "grscenes_bed_0a85b986_sphere_rain"
    assert config.verify == ("newton_sphere_rain",)
    assert config.protocol["newton"]["source_dir"] == "$NEWTON_SOURCE_DIR"
    assert config.protocol["newton_diagnostic"]["probe_type"] == "sphere_rain"
    assert config.protocol["newton_diagnostic"]["device"] == "cpu"
    assert config.protocol["newton_diagnostic"]["claim_boundary"] == (
        "sphere_rain_task_smoke_not_collision_quality_or_safety"
    )
    sphere_rain = config.protocol["newton_diagnostic"]["sphere_rain"]
    assert sphere_rain["sphere_count_x"] == 3
    assert sphere_rain["sphere_count_y"] == 3
    assert sphere_rain["sphere_radius_m"] == 0.5
    assert sphere_rain["min_contact_density"] == 0.05
    assert sphere_rain["require_final_contact"] is False
    assert config.protocol["report"]["evidence_level"] == "newton_sphere_rain_task_smoke"
    assert "/cpfs/user/" not in config_path.read_text(encoding="utf-8")


def test_franka_cpd_like_smoke_config_selects_robot_manifest_role():
    config_path = Path("configs/experiments/franka_cpd_like_smoke.yaml")
    config = load_compile_config(config_path)

    assert config.asset_id == "franka_robot_cpd_like_smoke"
    assert config.asset_path == "assets/manifests/franka_usd_smoke_assets.yaml"
    assert config.task == "robot_usd_import_and_cpd_like_smoke"
    assert config.method == "cpd_like_baseline"
    assert config.max_primitives == 16
    assert config.verify == ("usd_open", "cpd_like_geometry")
    assert config.protocol["cpd_like"]["asset_manifest"] == "assets/manifests/franka_usd_smoke_assets.yaml"
    assert config.protocol["cpd_like"]["asset_role"] == "franka_import_smoke"
    assert config.protocol["cpd_like"]["max_source_faces"] == 128
    assert config.protocol["cpd_like"]["claim_boundary"] == "robot_asset_import_smoke_not_collision_quality"
    assert config.protocol["report"]["evidence_level"] == "franka_cpd_like_geometry_smoke"
    assert "/cpfs/user/" not in config_path.read_text(encoding="utf-8")


def test_cpd_like_component_merge_gate_config_is_opt_in_and_claim_bounded():
    config_path = Path("configs/experiments/cpd_like_component_merge_gate.yaml")
    config = load_compile_config(config_path)

    assert config.asset_id == "grscenes_bed_0a85b986_component_merge_gate"
    assert config.task == "collision_proxy_diagnostic"
    assert config.method == "cpd_like_baseline"
    assert config.max_primitives == 32
    assert config.verify == ("cpd_like_component_merge_gate",)
    assert config.protocol["cpd_like"]["component_merge"] == "virtual_pairwise"
    assert config.protocol["cpd_like"]["excess_volume_threshold_fraction"] == 1.0
    assert config.protocol["cpd_like"]["report_merge_trace"] == "summary"
    assert config.protocol["cpd_like"]["claim_boundary"] == "component_merge_gate_not_cpd_reproduction"
    assert config.protocol["report"]["evidence_level"] == "geometry_only_cpd_like_component_merge_smoke"
    assert "/cpfs/user/" not in config_path.read_text(encoding="utf-8")


def test_cpd_like_objective_report_config_is_offline_and_claim_bounded():
    config_path = Path("configs/experiments/cpd_like_objective_report.yaml")
    config = load_compile_config(config_path)

    assert config.asset_id == "grscenes_bed_0a85b986_objective_report"
    assert config.task == "collision_proxy_diagnostic"
    assert config.method == "cpd_like_baseline"
    assert config.max_primitives == 32
    assert config.verify == ("cpd_like_objective_report",)
    assert config.protocol["cpd_like"]["component_merge"] == "virtual_pairwise"
    assert config.protocol["cpd_like"]["asset_role"] == "bed_dev_smoke"
    assert config.protocol["cpd_like_objective"]["objective_version"] == (
        "cpd_paper_aligned_surrogate_v0"
    )
    assert config.protocol["cpd_like_objective"]["claim_boundary"] == (
        "offline_objective_report_not_collision_quality_validation"
    )
    assert config.protocol["cpd_like_objective"]["evidence_level"] == (
        "offline_cpd_like_objective_surrogate_smoke"
    )
    assert config.protocol["cpd_like_objective"]["primitive_type_weights"] == {
        "box": 1.0,
        "sphere": 1.0,
        "capsule": 1.0,
    }
    assert config.protocol["report"]["evidence_level"] == (
        "offline_cpd_like_objective_surrogate_smoke"
    )
    assert "/cpfs/user/" not in config_path.read_text(encoding="utf-8")


def test_newton_native_fitting_comparison_config_includes_bed_and_franka_scope():
    config_path = Path("configs/experiments/newton_native_fitting_comparison.yaml")
    config = load_compile_config(config_path)

    assert config.asset_id == "newton_native_fitting_comparison"
    assert config.asset_path == "assets/manifests/cpd_like_smoke_assets.yaml"
    assert config.task == "native_primitive_fitting_comparison"
    assert config.method == "cpd_like_baseline"
    assert config.verify == (
        "synthetic_native_fitting_comparison",
        "bed_usd_cpd_like_geometry_scope",
        "franka_usd_cpd_like_geometry_scope",
    )
    assert config.protocol["cpd_like"]["asset_roles"] == [
        "bed_dev_smoke",
        "franka_import_smoke",
    ]
    assert config.protocol["cpd_like"]["legacy_primitive_subset"] == [
        "box",
        "sphere",
        "capsule",
    ]
    assert config.protocol["cpd_like"]["native_primitive_subset"] == [
        "box",
        "sphere",
        "capsule",
        "cylinder",
        "cone",
        "ellipsoid",
    ]
    assert config.protocol["native_fitting_comparison"]["real_usd_roles"] == [
        "bed_dev_smoke",
        "franka_import_smoke",
    ]
    assert config.protocol["native_fitting_comparison"]["claim_boundary"] == (
        "native_fitting_comparison_not_collision_quality_validation"
    )
    assert "/cpfs/user/" not in config_path.read_text(encoding="utf-8")
