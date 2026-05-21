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
    assert roles["bed_dev_smoke"]["local_path"].startswith("assets/raw/mirrors/")
    assert roles["bed_dev_smoke"]["materialization"]["status"] == "materialized"
    assert Path(roles["franka_import_smoke"]["path"]).name == "franka.usd"
    assert roles["franka_import_smoke"]["local_path"].startswith("assets/raw/mirrors/")
    assert roles["franka_import_smoke"]["materialization"]["unresolved_dependencies"] == [
        "OmniPBR.mdl"
    ]
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
    assert roles["franka_import_smoke"]["local_path"].startswith("assets/raw/mirrors/")
    assert roles["franka_import_smoke"]["materialization"]["unresolved_dependencies"] == [
        "OmniPBR.mdl"
    ]
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


def test_cylinder_scoring_policy_newton_probe_config_is_synthetic_and_claim_bounded():
    config_path = Path("configs/experiments/cylinder_scoring_policy_newton_probe.yaml")
    config = load_compile_config(config_path)

    assert config.asset_id == "cylinder_scoring_policy_newton_probe"
    assert config.asset_path == "synthetic://cylinder_near_miss_cluster"
    assert config.task == "synthetic_cylinder_scoring_policy_newton_probe"
    assert config.max_primitives == 1
    assert config.verify == ("cpd_like_cylinder_scoring_policy_newton_probe",)
    assert config.protocol["newton"]["source_dir"] == "$NEWTON_SOURCE_DIR"
    assert config.protocol["newton_diagnostic"]["device"] == "cpu"
    assert config.protocol["newton_diagnostic"]["claim_boundary"] == (
        "synthetic_cylinder_scoring_policy_task_smoke_not_collision_quality_or_safety"
    )
    assert config.protocol["report"]["evidence_level"] == (
        "synthetic_cylinder_scoring_policy_contact_gated_task_smoke"
    )
    assert "/cpfs/user/" not in config_path.read_text(encoding="utf-8")


def test_controlled_merge_search_newton_probe_config_is_synthetic_and_claim_bounded():
    config_path = Path("configs/experiments/controlled_merge_search_newton_probe.yaml")
    config = load_compile_config(config_path)

    assert config.asset_id == "controlled_merge_search_newton_probe"
    assert config.asset_path == "synthetic://cost_guided_pair_choice"
    assert config.task == "synthetic_controlled_merge_search_newton_probe"
    assert config.max_primitives == 2
    assert config.verify == ("cpd_like_controlled_merge_search_newton_probe",)
    assert config.protocol["newton"]["source_dir"] == "$NEWTON_SOURCE_DIR"
    assert config.protocol["newton_diagnostic"]["device"] == "cpu"
    assert config.protocol["newton_diagnostic"]["claim_boundary"] == (
        "synthetic_controlled_merge_search_task_smoke_not_collision_quality_or_merge_superiority"
    )
    assert config.protocol["report"]["evidence_level"] == (
        "synthetic_controlled_merge_search_contact_gated_task_smoke"
    )
    assert "/cpfs/user/" not in config_path.read_text(encoding="utf-8")


def test_cost_guided_lookahead_newton_probe_config_is_synthetic_and_claim_bounded():
    config_path = Path("configs/experiments/cost_guided_lookahead_newton_probe.yaml")
    config = load_compile_config(config_path)

    assert config.asset_id == "cost_guided_lookahead_newton_probe"
    assert config.asset_path == "synthetic://lookahead_merge_trap"
    assert config.task == "synthetic_cost_guided_lookahead_newton_probe"
    assert config.max_primitives == 2
    assert config.verify == ("cpd_like_cost_guided_lookahead_newton_probe",)
    assert config.protocol["newton"]["source_dir"] == "$NEWTON_SOURCE_DIR"
    assert config.protocol["newton_diagnostic"]["device"] == "cpu"
    assert config.protocol["newton_diagnostic"]["claim_boundary"] == (
        "synthetic_cost_guided_lookahead_task_smoke_not_quality_or_policy_ranking"
    )
    assert config.protocol["report"]["evidence_level"] == (
        "synthetic_cost_guided_lookahead_contact_gated_task_smoke"
    )
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
        "synthetic_native_selection_audit",
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
    assert config.protocol["native_fitting_comparison"]["selection_audit"] == {
        "enabled": True,
        "claim_boundary": "synthetic_selection_audit_not_paper_optimizer_or_collision_quality",
        "selection_policy": "support_aware_min_weighted_volume_surrogate_v1",
    }
    assert "/cpfs/user/" not in config_path.read_text(encoding="utf-8")


def test_bed_franka_native_probe_config_includes_candidate_loss_diagnosis():
    config_path = Path("configs/experiments/bed_franka_native_probe_comparison.yaml")
    config = load_compile_config(config_path)

    assert "real_usd_candidate_loss_diagnosis" in config.verify
    assert config.protocol["candidate_loss_diagnosis"] == {
        "stage": "cpd_like_real_usd_candidate_loss_diagnosis",
        "claim_boundary": "candidate_loss_diagnosis_not_collision_quality_validation",
        "evidence_level": "offline_candidate_loss_diagnosis_smoke",
    }


def test_franka_native_opt_in_probe_config_is_real_usd_and_claim_bounded():
    config_path = Path("configs/experiments/franka_native_opt_in_probe.yaml")
    config = load_compile_config(config_path)

    assert config.asset_id == "franka_native_opt_in_probe"
    assert config.asset_path == "assets/manifests/cpd_like_smoke_assets.yaml"
    assert config.task == "real_usd_native_opt_in_task_probe"
    assert config.verify == (
        "real_usd_native_fitting_comparison",
        "real_usd_native_task_comparison",
    )
    assert config.protocol["cpd_like"]["asset_roles"] == ["franka_import_smoke"]
    assert config.protocol["cpd_like"]["native_opt_in_primitive_score_multipliers"] == {
        "cylinder": 0.5
    }
    assert "native_opt_in_selection_guard" not in config.protocol["cpd_like"]
    assert config.protocol["newton_diagnostic"]["claim_boundary"] == (
        "real_usd_native_opt_in_task_smoke_not_collision_quality_or_safety"
    )
    assert "/cpfs/user/" not in config_path.read_text(encoding="utf-8")


def test_bed_native_opt_in_probe_config_is_real_usd_and_claim_bounded():
    config_path = Path("configs/experiments/bed_native_opt_in_probe.yaml")
    config = load_compile_config(config_path)

    assert config.asset_id == "bed_native_opt_in_probe"
    assert config.asset_path == "assets/manifests/cpd_like_smoke_assets.yaml"
    assert config.task == "real_usd_bed_native_opt_in_task_probe"
    assert config.verify == (
        "real_usd_native_fitting_comparison",
        "real_usd_native_task_comparison",
    )
    assert config.protocol["cpd_like"]["asset_roles"] == ["bed_dev_smoke"]
    assert config.protocol["cpd_like"]["max_source_faces_by_role"] == {
        "bed_dev_smoke": 256
    }
    assert config.protocol["cpd_like"]["native_opt_in_primitive_score_multipliers"] == {
        "cylinder": 0.88
    }
    assert "native_opt_in_selection_guard" not in config.protocol["cpd_like"]
    assert config.protocol["newton_diagnostic"]["drop_settle"]["frames"] == 360
    assert config.protocol["newton_diagnostic"]["claim_boundary"] == (
        "real_usd_native_opt_in_task_smoke_not_collision_quality_or_safety"
    )
    assert config.protocol["report"]["evidence_level"] == (
        "real_usd_native_opt_in_task_gate_blocker"
    )
    assert "/cpfs/user/" not in config_path.read_text(encoding="utf-8")


def test_native_opt_in_guard_probe_configs_are_real_usd_and_claim_bounded():
    expected = {
        "enabled": True,
        "mode": "reject",
        "target_primitives": ["cylinder"],
        "max_cylinder_radius": 0.5,
        "min_cylinder_half_height_radius_ratio": 0.1,
        "claim_boundary": "diagnostic_selection_guard_not_collision_quality_validation",
    }
    cases = [
        (
            Path("configs/experiments/bed_native_opt_in_guard_probe.yaml"),
            "bed_native_opt_in_guard_probe",
            "real_usd_bed_native_opt_in_guard_task_probe",
            ["bed_dev_smoke"],
            {"cylinder": 0.88},
        ),
        (
            Path("configs/experiments/franka_native_opt_in_guard_probe.yaml"),
            "franka_native_opt_in_guard_probe",
            "real_usd_franka_native_opt_in_guard_task_probe",
            ["franka_import_smoke"],
            {"cylinder": 0.5},
        ),
    ]

    for config_path, asset_id, task, roles, multipliers in cases:
        config = load_compile_config(config_path)

        assert config.asset_id == asset_id
        assert config.asset_path == "assets/manifests/cpd_like_smoke_assets.yaml"
        assert config.task == task
        assert config.verify == (
            "real_usd_native_fitting_comparison",
            "real_usd_native_task_comparison",
        )
        assert config.protocol["cpd_like"]["asset_roles"] == roles
        assert config.protocol["cpd_like"]["native_opt_in_primitive_score_multipliers"] == (
            multipliers
        )
        assert config.protocol["cpd_like"]["native_opt_in_selection_guard"] == expected
        assert config.protocol["newton_diagnostic"]["claim_boundary"] == (
            "real_usd_native_opt_in_guard_task_smoke_not_collision_quality_or_safety"
        )
        assert "/cpfs/user/" not in config_path.read_text(encoding="utf-8")


def test_franka_native_opt_in_support_threshold_probe_config_is_real_usd_and_claim_bounded():
    config_path = Path("configs/experiments/franka_native_opt_in_support_threshold_probe.yaml")
    config = load_compile_config(config_path)

    assert config.asset_id == "franka_native_opt_in_support_threshold_probe"
    assert config.asset_path == "assets/manifests/cpd_like_smoke_assets.yaml"
    assert config.task == "real_usd_franka_native_opt_in_support_threshold_task_probe"
    assert config.verify == (
        "real_usd_native_fitting_comparison",
        "real_usd_native_task_comparison",
    )
    assert config.protocol["cpd_like"]["asset_roles"] == ["franka_import_smoke"]
    assert "native_opt_in_primitive_score_multipliers" not in config.protocol["cpd_like"]
    assert config.protocol["cpd_like"]["native_opt_in_extension_support_thresholds"] == {
        "enabled": True,
        "target_primitives": ["cylinder"],
        "min_extension_source_faces": 2,
        "min_extension_unique_points": 4,
        "claim_boundary": "diagnostic_extension_support_threshold_probe_not_collision_quality_validation",
    }
    assert config.protocol["newton_diagnostic"]["claim_boundary"] == (
        "real_usd_native_opt_in_support_threshold_task_smoke_not_collision_quality_or_safety"
    )
    assert config.protocol["native_fitting_comparison"]["claim_boundary"] == (
        "real_usd_native_opt_in_support_threshold_probe_not_collision_quality_validation"
    )
    assert config.protocol["report"]["evidence_level"] == (
        "real_usd_native_opt_in_support_threshold_contact_gated_task_smoke"
    )
    assert "/cpfs/user/" not in config_path.read_text(encoding="utf-8")


def test_bed_franka_native_opt_in_guarded_support_threshold_probe_config_is_claim_bounded():
    config_path = Path(
        "configs/experiments/bed_franka_native_opt_in_guarded_support_threshold_probe.yaml"
    )
    config = load_compile_config(config_path)

    assert config.asset_id == "bed_franka_native_opt_in_guarded_support_threshold_probe"
    assert config.asset_path == "assets/manifests/cpd_like_smoke_assets.yaml"
    assert config.task == "real_usd_bed_franka_native_opt_in_guarded_support_threshold_task_probe"
    assert config.verify == (
        "real_usd_native_fitting_comparison",
        "real_usd_native_task_comparison",
    )
    cpd_like = config.protocol["cpd_like"]
    assert cpd_like["asset_roles"] == ["bed_dev_smoke", "franka_import_smoke"]
    assert cpd_like["max_source_faces_by_role"] == {
        "bed_dev_smoke": 256,
        "franka_import_smoke": 128,
    }
    assert cpd_like["claim_boundary"] == (
        "real_usd_native_opt_in_guarded_support_threshold_probe_not_collision_quality_validation"
    )
    assert "native_opt_in_primitive_score_multipliers" not in cpd_like
    assert cpd_like["native_opt_in_selection_guard"] == {
        "enabled": True,
        "mode": "reject",
        "target_primitives": ["cylinder"],
        "max_cylinder_radius": 0.5,
        "min_cylinder_half_height_radius_ratio": 0.1,
        "claim_boundary": "diagnostic_selection_guard_not_collision_quality_validation",
    }
    assert cpd_like["native_opt_in_extension_support_thresholds"] == {
        "enabled": True,
        "target_primitives": ["cylinder"],
        "min_extension_source_faces": 2,
        "min_extension_unique_points": 4,
        "claim_boundary": "diagnostic_extension_support_threshold_probe_not_collision_quality_validation",
    }
    assert config.protocol["native_fitting_comparison"]["claim_boundary"] == (
        "real_usd_native_opt_in_guarded_support_threshold_probe_not_collision_quality_validation"
    )
    assert config.protocol["newton_diagnostic"]["claim_boundary"] == (
        "real_usd_native_opt_in_guarded_support_threshold_task_smoke_not_collision_quality_or_safety"
    )
    assert config.protocol["report"]["evidence_level"] == (
        "real_usd_native_opt_in_guarded_support_threshold_contact_gated_task_smoke"
    )
    assert config.protocol["report"]["output_dir"] == (
        "reports/generated/bed_franka_native_opt_in_guarded_support_threshold_probe"
    )
    assert "/cpfs/user/" not in config_path.read_text(encoding="utf-8")


def test_bed_franka_package_body_state_guard_probe_config_is_claim_bounded():
    config_path = Path(
        "configs/experiments/bed_franka_native_opt_in_package_body_state_guard_probe.yaml"
    )
    config = load_compile_config(config_path)

    assert config.asset_id == "bed_franka_native_opt_in_package_body_state_guard_probe"
    assert config.asset_path == "assets/manifests/cpd_like_smoke_assets.yaml"
    assert config.task == "real_usd_bed_franka_package_body_state_guard_task_probe"
    assert config.verify == (
        "real_usd_native_fitting_comparison",
        "real_usd_native_task_comparison",
    )
    cpd_like = config.protocol["cpd_like"]
    assert cpd_like["asset_roles"] == ["bed_dev_smoke", "franka_import_smoke"]
    assert cpd_like["native_opt_in_primitive_score_multipliers"] == {"cylinder": 0.88}
    assert cpd_like["native_opt_in_extension_support_thresholds"] == {
        "enabled": True,
        "target_primitives": ["cylinder"],
        "min_extension_source_faces": 2,
        "min_extension_unique_points": 4,
        "claim_boundary": "diagnostic_extension_support_threshold_probe_not_collision_quality_validation",
    }
    assert "native_opt_in_merge_search_policy" not in cpd_like
    assert cpd_like["native_opt_in_package_body_state_guard"] == {
        "enabled": True,
        "mode": "fallback_to_native_package",
        "claim_boundary": "diagnostic_package_body_state_guard_not_collision_quality",
    }
    assert cpd_like["claim_boundary"] == (
        "real_usd_native_opt_in_package_body_state_guard_probe_not_collision_quality_validation"
    )
    assert config.protocol["native_fitting_comparison"]["claim_boundary"] == (
        "real_usd_native_opt_in_package_body_state_guard_probe_not_collision_quality_validation"
    )
    assert config.protocol["newton_diagnostic"]["claim_boundary"] == (
        "real_usd_native_opt_in_package_body_state_guard_task_smoke_not_collision_quality_or_safety"
    )
    assert config.protocol["report"]["output_dir"] == (
        "reports/generated/bed_franka_native_opt_in_package_body_state_guard_probe"
    )
    assert "/cpfs/user/" not in config_path.read_text(encoding="utf-8")


def test_franka_native_opt_in_cost_guided_merge_probe_config_is_claim_bounded():
    config_path = Path("configs/experiments/franka_native_opt_in_cost_guided_merge_probe.yaml")
    config = load_compile_config(config_path)

    assert config.asset_id == "franka_native_opt_in_cost_guided_merge_probe"
    assert config.asset_path == "assets/manifests/cpd_like_smoke_assets.yaml"
    assert config.task == "real_usd_franka_native_opt_in_cost_guided_merge_task_probe"
    assert config.verify == (
        "real_usd_native_fitting_comparison",
        "real_usd_native_task_comparison",
    )
    cpd_like = config.protocol["cpd_like"]
    assert cpd_like["asset_roles"] == ["franka_import_smoke"]
    assert cpd_like["max_source_faces_by_role"] == {"franka_import_smoke": 64}
    assert cpd_like["component_merge"] == "virtual_pairwise"
    assert cpd_like["merge_search_policy"] == "topology_then_virtual"
    assert cpd_like["native_opt_in_merge_search_policy"] == "cost_guided_pairwise"
    assert "native_opt_in_primitive_score_multipliers" not in cpd_like
    assert cpd_like["claim_boundary"] == (
        "real_usd_franka_native_opt_in_cost_guided_merge_probe_not_collision_quality_validation"
    )
    assert config.protocol["native_fitting_comparison"]["claim_boundary"] == (
        "real_usd_franka_native_opt_in_cost_guided_merge_probe_not_collision_quality_validation"
    )
    assert config.protocol["newton_diagnostic"]["claim_boundary"] == (
        "real_usd_franka_native_opt_in_cost_guided_merge_task_smoke_not_collision_quality_or_safety"
    )
    assert config.protocol["report"]["evidence_level"] == (
        "real_usd_franka_native_opt_in_cost_guided_merge_contact_gated_task_smoke"
    )
    assert config.protocol["report"]["output_dir"] == (
        "reports/generated/franka_native_opt_in_cost_guided_merge_probe"
    )
    assert "/cpfs/user/" not in config_path.read_text(encoding="utf-8")


def test_bed_native_opt_in_frame_sweep_configs_preserve_historical_selection_scope():
    sweep_configs = {
        "configs/experiments/bed_native_opt_in_frame361_probe.yaml": 361,
        "configs/experiments/bed_native_opt_in_frame362_probe.yaml": 362,
        "configs/experiments/bed_native_opt_in_frame363_probe.yaml": 363,
        "configs/experiments/bed_native_opt_in_frame364_probe.yaml": 364,
        "configs/experiments/bed_native_opt_in_frame365_probe.yaml": 365,
        "configs/experiments/bed_native_opt_in_frame375_probe.yaml": 375,
        "configs/experiments/bed_native_opt_in_frame385_probe.yaml": 385,
        "configs/experiments/bed_native_opt_in_frame390_probe.yaml": 390,
        "configs/experiments/bed_native_opt_in_frame420_probe.yaml": 420,
        "configs/experiments/bed_native_opt_in_frame450_probe.yaml": 450,
        "configs/experiments/bed_native_opt_in_frame480_probe.yaml": 480,
        "configs/experiments/bed_native_opt_in_frame600_probe.yaml": 600,
        "configs/experiments/bed_native_opt_in_long_window_probe.yaml": 720,
    }
    baseline = load_compile_config("configs/experiments/bed_native_opt_in_probe.yaml")

    for config_name, frames in sweep_configs.items():
        config_path = Path(config_name)
        config = load_compile_config(config_path)

        assert config.asset_id == f"bed_native_opt_in_frame{frames}_probe"
        assert config.asset_path == "assets/manifests/cpd_like_smoke_assets.yaml"
        assert config.task == f"real_usd_bed_native_opt_in_frame{frames}_probe"
        assert config.method == baseline.method
        assert config.max_primitives == baseline.max_primitives
        assert config.allowed_fallback == baseline.allowed_fallback
        assert config.verify == (
            "real_usd_native_fitting_comparison",
            "real_usd_native_task_comparison",
        )
        assert config.keep_visual == baseline.keep_visual
        assert {
            key: value
            for key, value in config.protocol["cpd_like"].items()
            if key not in {"claim_boundary", "native_opt_in_selection_guard"}
        } == {
            key: value
            for key, value in baseline.protocol["cpd_like"].items()
            if key not in {"claim_boundary", "native_opt_in_selection_guard"}
        }
        assert "native_opt_in_selection_guard" not in config.protocol["cpd_like"]
        assert config.protocol["newton"] == baseline.protocol["newton"]
        assert config.protocol["newton_diagnostic"]["probe_type"] == (
            baseline.protocol["newton_diagnostic"]["probe_type"]
        )
        assert config.protocol["newton_diagnostic"]["device"] == (
            baseline.protocol["newton_diagnostic"]["device"]
        )
        assert config.protocol["newton_diagnostic"]["sphere_rain"] == (
            baseline.protocol["newton_diagnostic"]["sphere_rain"]
        )
        drop_settle = config.protocol["newton_diagnostic"]["drop_settle"]
        baseline_drop_settle = baseline.protocol["newton_diagnostic"]["drop_settle"]
        assert drop_settle["frames"] == frames
        assert drop_settle["substeps"] == 8
        assert {
            key: value for key, value in drop_settle.items() if key != "frames"
        } == {key: value for key, value in baseline_drop_settle.items() if key != "frames"}
        assert config.protocol["newton_diagnostic"]["claim_boundary"] == (
            "real_usd_native_opt_in_frame_sweep_sensitivity_not_collision_quality_or_safety"
        )
        assert config.protocol["cpd_like"]["claim_boundary"] == (
            "real_usd_native_opt_in_frame_sweep_probe_not_collision_quality_validation"
        )
        assert config.protocol["native_fitting_comparison"] == {
            "stage": "cpd_like_real_usd_native_fitting_comparison",
            "real_usd_roles": ["bed_dev_smoke"],
            "real_usd_status": (
                "configured_real_usd_native_opt_in_frame_sweep_smoke_not_benchmark"
            ),
            "claim_boundary": (
                "real_usd_native_opt_in_frame_sweep_probe_not_collision_quality_validation"
            ),
            "evidence_level": "offline_real_usd_native_opt_in_frame_sweep_fitting_smoke",
        }
        assert config.protocol["report"]["evidence_level"] == (
            "real_usd_native_opt_in_frame_sweep_sensitivity"
        )
        assert config.protocol["report"]["output_dir"] == (
            f"reports/generated/bed_native_opt_in_frame{frames}_probe"
        )
        assert "/cpfs/user/" not in config_path.read_text(encoding="utf-8")
