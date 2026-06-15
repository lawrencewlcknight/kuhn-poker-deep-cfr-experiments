"""Tiny smoke test for the network-size ablation export path."""

from __future__ import annotations

import json

import pytest

pytest.importorskip("pyspiel")
pytest.importorskip("torch")

from experiments.kuhn_poker.deep_cfr_network_size_ablation.config import (
    make_architecture_variant,
)
from experiments.kuhn_poker.deep_cfr_network_size_ablation.run import (
    _augment_result,
    _variant_config,
    export_ablation_results,
)
from deep_cfr_poker.experiment_utils import run_single_seed


SMOKE_VARIANTS = (
    make_architecture_variant(2, 8),
    make_architecture_variant(4, 8),
)

SMOKE_CONFIG = {
    "experiment_name": "network_size_smoke",
    "game_name": "kuhn_poker",
    "num_iterations": 3,
    "num_traversals": 4,
    "evaluation_interval": 1,
    "policy_network_layers": (8, 8),
    "advantage_network_layers": (8, 8),
    "learning_rate": 0.003,
    "batch_size_advantage": 2,
    "batch_size_strategy": 2,
    "memory_capacity": 256,
    "reinitialize_advantage_networks": False,
    "policy_network_train_steps": 1,
    "advantage_network_train_steps": 1,
    "policy_network_train_every": 1,
    "policy_training_mode": "intermittent",
    "final_policy_network_train_steps": None,
    "compute_exploitability": True,
    "exploitability_threshold": 0.5,
    "average_policy_value_target": -1.0 / 18.0,
    "architecture_variants": SMOKE_VARIANTS,
    "baseline_variant_id": "layers2_width8",
}


@pytest.mark.smoke
def test_network_size_ablation_writes_expected_artifacts(tmp_path):
    results = []
    for variant in SMOKE_CONFIG["architecture_variants"]:
        variant_config = _variant_config(SMOKE_CONFIG, variant)
        result = run_single_seed(1234, variant_config, export_dir=tmp_path)
        results.append(
            _augment_result(
                result,
                variant_config,
                final_window=2,
                exploitability_threshold=SMOKE_CONFIG["exploitability_threshold"],
            )
        )

    info = export_ablation_results(results, tmp_path, SMOKE_CONFIG, [1234])

    for path in (
        info["summary_csv"],
        info["curve_csv"],
        info["aggregate_summary"],
        info["metadata"],
        info["architecture_grid_summary_csv"],
        info["ablation_curves_npz"],
        info["paired_differences_csv"],
        info["paired_difference_summary"],
    ):
        assert path is not None
        assert path.exists()

    aggregate = json.loads(info["aggregate_summary"].read_text(encoding="utf-8"))
    assert "by_variant_id" in aggregate
    assert "layers4_width8" in aggregate["by_variant_id"]

    summary_header = info["summary_csv"].read_text(encoding="utf-8").splitlines()[0]
    assert "architecture_depth" in summary_header
    assert "architecture_width" in summary_header

    grid_header = info["architecture_grid_summary_csv"].read_text(
        encoding="utf-8"
    ).splitlines()[0]
    assert "final_exploitability_mean" in grid_header

    paired = json.loads(info["paired_difference_summary"].read_text(encoding="utf-8"))
    assert "layers4_width8" in paired
    assert "delta_final_exploitability_vs_baseline" in paired["layers4_width8"]

