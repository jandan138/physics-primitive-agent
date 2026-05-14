from pathlib import Path

import yaml

from primitive_collision_compiler.config import load_compile_config


def test_cpd_like_baseline_preserves_newton_and_cpd_sections():
    config = load_compile_config("configs/experiments/cpd_like_baseline.yaml")

    assert config.asset_id == "grscenes_bed_0a85b986_smoke"
    assert config.task == "collision_proxy_diagnostic"
    assert config.method == "cpd_like_baseline"
    assert config.max_primitives == 32
    assert config.allowed_fallback == ("convex_hull",)
    assert config.verify == ("newton_import",)
    assert config.keep_visual is False
    assert config.protocol["newton"]["source_dir"] == "/cpfs/user/zhuzihou/dev/newton"
    assert config.protocol["cpd_like"]["asset_manifest"] == "assets/manifests/cpd_like_smoke_assets.yaml"
    assert config.protocol["cpd_like"]["primitive_subset"] == ["sphere", "capsule", "box"]
    assert config.protocol["cpd_like"]["claim_boundary"] == "internal_baseline_not_reproduction_claim"
    assert config.protocol["report"]["output_dir"] == "reports/generated/cpd_like_baseline"


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
