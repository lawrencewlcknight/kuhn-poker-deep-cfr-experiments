"""Shared pytest fixtures."""

from __future__ import annotations

import pytest


@pytest.fixture
def kuhn_game():
    """Returns an OpenSpiel Kuhn poker game, skipping if pyspiel is missing."""
    pyspiel = pytest.importorskip("pyspiel")
    return pyspiel.load_game("kuhn_poker")
