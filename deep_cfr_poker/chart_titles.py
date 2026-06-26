"""Chart title helpers with consistent experiment context prefixes."""

from __future__ import annotations

import re
from typing import Any, Optional


DEFAULT_ALGORITHM_VARIANT = "Deep CFR"
DEFAULT_POKER_VARIANT = "Kuhn"


def normalise_algorithm_variant(value: Optional[object] = None) -> str:
    """Returns a presentation label for an algorithm variant."""
    if value is None:
        return DEFAULT_ALGORITHM_VARIANT
    raw = str(value).strip()
    if not raw:
        return DEFAULT_ALGORITHM_VARIANT
    compact = re.sub(r"[\s_-]+", "", raw).lower()
    if compact == "deepcfr":
        return "Deep CFR"
    if compact == "escher":
        return "ESCHER"
    if compact == "dream":
        return "DREAM"
    if raw.isupper():
        return raw
    return raw.replace("_", " ").replace("-", " ").title()


def normalise_poker_variant(value: Optional[object] = None) -> str:
    """Returns a short presentation label for a poker game variant."""
    if value is None:
        return DEFAULT_POKER_VARIANT
    raw = str(value).strip()
    if not raw:
        return DEFAULT_POKER_VARIANT
    compact = re.sub(r"[\s_-]+", "", raw).lower()
    if "kuhn" in compact:
        return "Kuhn"
    if "leduc" in compact:
        return "Leduc"
    if "hunl" in compact:
        return "HUNL"
    label = re.sub(r"[_-]+", " ", raw)
    label = re.sub(r"\bpoker\b", "", label, flags=re.IGNORECASE).strip()
    return label.title() if label else DEFAULT_POKER_VARIANT


def chart_title_prefix(
    *,
    algorithm_variant: Optional[object] = None,
    poker_variant: Optional[object] = None,
) -> str:
    """Builds the required ``Algorithm - Poker`` chart-title prefix."""
    return (
        f"{normalise_algorithm_variant(algorithm_variant)} - "
        f"{normalise_poker_variant(poker_variant)}"
    )


def _strip_existing_context(
    title: str,
    *,
    algorithm_label: str,
    poker_label: str,
) -> str:
    """Removes older title context so the new prefix is not duplicated."""
    stripped = title.strip()
    legacy_patterns = (
        rf"^{re.escape(algorithm_label)}\s*-\s*{re.escape(poker_label)}\s*-\s*",
        rf"^{re.escape(poker_label)}\s+Poker\s+{re.escape(algorithm_label)}\s*[:\-]\s*",
        rf"^{re.escape(poker_label)}\s+{re.escape(algorithm_label)}\s*[:\-]\s*",
        rf"^{re.escape(algorithm_label)}\s+{re.escape(poker_label)}\s*[:\-]\s*",
    )
    for pattern in legacy_patterns:
        stripped = re.sub(pattern, "", stripped, flags=re.IGNORECASE).strip()
    return stripped


def format_chart_title(
    title: object,
    *,
    algorithm_variant: Optional[object] = None,
    poker_variant: Optional[object] = None,
) -> str:
    """Prefixes a chart title with algorithm and poker variants.

    The repository convention is ``Algorithm - Poker - Chart Title``. Existing
    titles that already contain the requested prefix are left unchanged, and
    older titles such as ``Kuhn Poker Deep CFR: Exploitability`` are normalised.
    """
    algorithm_label = normalise_algorithm_variant(algorithm_variant)
    poker_label = normalise_poker_variant(poker_variant)
    prefix = f"{algorithm_label} - {poker_label}"
    raw_title = str(title).strip()
    if raw_title.lower().startswith(f"{prefix} - ".lower()):
        return raw_title
    core_title = _strip_existing_context(
        raw_title,
        algorithm_label=algorithm_label,
        poker_label=poker_label,
    )
    return f"{prefix} - {core_title}" if core_title else prefix


def set_chart_title(
    ax: Any,
    title: object,
    *,
    algorithm_variant: Optional[object] = None,
    poker_variant: Optional[object] = None,
    **kwargs: Any,
) -> Any:
    """Sets a Matplotlib axis title using the repository naming convention."""
    return ax.set_title(
        format_chart_title(
            title,
            algorithm_variant=algorithm_variant,
            poker_variant=poker_variant,
        ),
        **kwargs,
    )


__all__ = [
    "chart_title_prefix",
    "format_chart_title",
    "normalise_algorithm_variant",
    "normalise_poker_variant",
    "set_chart_title",
]
