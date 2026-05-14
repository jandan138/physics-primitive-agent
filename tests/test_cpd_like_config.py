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


def test_smoke_asset_manifest_records_paths_without_committing_assets():
    manifest = yaml.safe_load(Path("assets/manifests/cpd_like_smoke_assets.yaml").read_text())

    assert manifest["manifest_id"] == "cpd_like_smoke_assets_2026_05_14"
    roles = {asset["role"]: asset for asset in manifest["assets"]}
    assert roles["bed_dev_smoke"]["path"].endswith("0a85b986de35ccfdec7c686d791fd747.usd")
    assert (
        roles["bed_dev_smoke"]["sha256"]
        == "1bc5a26ddb2551de4ac7acbc13a39d118beda10db503419da65ce82528322265"
    )
    assert roles["franka_import_smoke"]["path"] == "/cpfs/user/zhuzihou/assets/zzh-grscenes/robots/franka/franka.usd"
    assert roles["franka_import_smoke"]["include_in_cpd_like_aggregate"] is False


def test_cpd_like_runtime_dependencies_include_numpy():
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")

    assert '"numpy>=1.26"' in pyproject


def test_cpd_like_baseline_config_keeps_machine_paths_in_manifest_not_config():
    config_text = Path("configs/experiments/cpd_like_baseline.yaml").read_text(encoding="utf-8")

    assert "/cpfs/user/" not in config_text
    assert "$NEWTON_SOURCE_DIR" in config_text
