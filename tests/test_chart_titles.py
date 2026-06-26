"""Tests for repository-wide chart title conventions."""

from __future__ import annotations

from pathlib import Path

from deep_cfr_poker.chart_titles import format_chart_title


def test_format_chart_title_prefixes_algorithm_and_poker_variant():
    assert (
        format_chart_title(
            "Exploitability",
            algorithm_variant="ESCHER",
            poker_variant="kuhn_poker",
        )
        == "ESCHER - Kuhn - Exploitability"
    )
    assert (
        format_chart_title(
            "Average Policy Value",
            algorithm_variant="dream",
            poker_variant="leduc_poker",
        )
        == "DREAM - Leduc - Average Policy Value"
    )


def test_format_chart_title_normalises_legacy_and_existing_titles():
    assert (
        format_chart_title("Kuhn Poker Deep CFR: Exploitability Across Seeds")
        == "Deep CFR - Kuhn - Exploitability Across Seeds"
    )
    assert (
        format_chart_title("Deep CFR - Kuhn - Exploitability Across Seeds")
        == "Deep CFR - Kuhn - Exploitability Across Seeds"
    )


def test_plotting_code_uses_chart_title_helper():
    root = Path(__file__).resolve().parents[1]
    offenders = []
    for folder in ("deep_cfr_poker", "experiments"):
        for path in (root / folder).rglob("*.py"):
            if path.match("*/chart_titles.py"):
                continue
            text = path.read_text(encoding="utf-8")
            if ".set_title(" in text:
                offenders.append(str(path.relative_to(root)))

    assert offenders == []
