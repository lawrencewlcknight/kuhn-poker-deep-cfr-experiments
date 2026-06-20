"""Tests for optional MLP architecture variants."""

from __future__ import annotations

import pytest

pytest.importorskip("pyspiel")
torch = pytest.importorskip("torch")

from deep_cfr_poker.networks import build_network


@pytest.mark.parametrize(
    "network_type",
    ["mlp", "residual_mlp", "layer_norm_mlp", "residual_layer_norm_mlp"],
)
def test_network_variants_forward_and_reset(network_type):
    net = build_network(
        network_type,
        input_size=6,
        hidden_sizes=(8, 8, 8),
        output_size=3,
    )
    x = torch.randn(4, 6)
    y = net(x)
    assert y.shape == (4, 3)
    net.reset()
    y_after_reset = net(x)
    assert y_after_reset.shape == (4, 3)


def test_unknown_network_type_is_rejected():
    with pytest.raises(ValueError, match="Unknown network_type"):
        build_network("not_a_network", 6, (8, 8), 3)
