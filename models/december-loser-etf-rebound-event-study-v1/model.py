"""Timestamp-safe December loser ETF rebound event-calendar model.

This qfa-compatible model is intentionally deterministic and stateless. It returns
an equal-weight basket only near the last December trading sessions when the
provided context exposes enough historical daily closes to compute the predeclared
Oct-1 to Dec-20 loser-pressure signal. It performs no data fetching and places no
orders by itself.
"""

from __future__ import annotations

from datetime import date
from typing import Any

CANDIDATE_SYMBOLS = [
    "SPY", "RSP", "QQQ", "DIA", "IWM", "MDY", "XLB", "XLC", "XLE", "XLF", "XLI", "XLK",
    "XLP", "XLU", "XLV", "XLY", "XBI", "KRE", "KBE", "SMH", "IGV", "IYT", "ITB", "XHB",
    "XRT", "IYR", "VNQ", "IBB", "XME", "XOP", "OIH", "TAN", "PBW", "ICLN", "HACK", "ARKK",
    "FDN", "SKYY", "SOXX",
]
SELECTED_COUNT = 5


def _get_prices(context: Any) -> Any:
    if isinstance(context, dict):
        return context.get("prices") or context.get("history")
    return getattr(context, "prices", None) or getattr(context, "history", None)


def _latest_date(prices: Any) -> date | None:
    idx = getattr(prices, "index", None)
    if idx is None or len(idx) == 0:
        return None
    latest = idx[-1]
    if hasattr(latest, "date"):
        return latest.date()
    return latest


def generate_signals(context: Any) -> dict[str, float]:
    """Return equal weights for the predeclared December loser basket when active."""
    prices = _get_prices(context)
    if prices is None:
        return {}
    today = _latest_date(prices)
    if today is None or today.month != 12 or today.day < 20:
        return {}
    try:
        closes = prices["close"] if "close" in prices else prices
        year = today.year
        year_prices = closes.loc[str(year)]
        oct_prices = year_prices.loc[str(year) + "-10-01" : str(year) + "-12-20"]
        if len(oct_prices) < 20:
            return {}
        start = oct_prices.iloc[0]
        end = oct_prices.iloc[-1]
        pressure = (end / start - 1.0).dropna()
        pressure = pressure[[s for s in CANDIDATE_SYMBOLS if s in pressure.index]]
        losers = list(pressure[pressure < 0].sort_values().head(SELECTED_COUNT).index)
    except Exception:
        return {}
    if len(losers) < SELECTED_COUNT:
        return {}
    weight = 1.0 / len(losers)
    return {symbol: weight for symbol in losers}
