"""AR-166 ToM ETF seasonality expanded-universe validator.

Research-only qfa-compatible model exposing generate_signals(context). The
associated real-data AR-166 evaluation rejected promotion of AR-006/AR-021
turn-of-month ETF seasonality after broad-universe, costs, controls, and random
window validation. This artifact preserves the frozen validator rule; it never
places orders and reads only qfa context prices/as_of.

Frozen rule: long equal-weight selected non-levered liquid ETF universe on the
first 4 and final 1 observed market sessions of each calendar month; flat
otherwise. No post-hoc window or sleeve optimization.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

SELECTED_UNIVERSE = (
    "SPY",
    "QQQ",
    "IWM",
    "IVV",
    "VOO",
    "DIA",
    "RSP",
    "VTI",
    "IWF",
    "VTV",
    "IWD",
    "VUG",
    "QUAL",
    "SPLV",
    "MTUM",
    "USMV",
    "SMH",
    "XLK",
    "XLF",
    "XLV",
    "XLE",
    "XLI",
    "XLY",
    "XLP",
    "EEM",
    "EFA",
    "FXI",
    "IEFA",
    "EWZ",
    "EWY",
    "IEMG",
    "VEA",
    "LQD",
    "HYG",
    "TLT",
    "SGOV",
    "AGG",
    "BIL",
    "IEF",
    "BND",
    "GLD",
    "SLV",
    "IAU",
    "USO",
    "VNQ",
    "UNG",
    "PDBC",
    "REET",
)

DEFAULT_PARAMS = {
    "pre_month_end_sessions": 1,
    "post_month_start_sessions": 4,
    "min_observations": 20,
    "max_abs_weight": 0.05,
}


def _params(context: Any) -> dict:
    metadata = getattr(context, "metadata", {}) or {}
    provided = metadata.get("params", {}) if isinstance(metadata, dict) else {}
    params = DEFAULT_PARAMS.copy()
    params.update({k: provided[k] for k in params.keys() & provided.keys()})
    return params


def _as_timestamp(context: Any) -> pd.Timestamp | None:
    as_of = getattr(context, "as_of", None)
    if as_of is not None:
        ts = pd.Timestamp(as_of)
        return ts.tz_convert("UTC") if ts.tzinfo else ts.tz_localize("UTC")
    prices = getattr(context, "prices", pd.DataFrame())
    if prices.empty or "timestamp" not in prices:
        return None
    return pd.to_datetime(prices["timestamp"], utc=True, errors="coerce").max()


def _observed_sessions(prices: pd.DataFrame) -> list[pd.Timestamp]:
    if prices.empty or "timestamp" not in prices:
        return []
    stamps = pd.to_datetime(prices["timestamp"], utc=True, errors="coerce").dropna()
    if stamps.empty:
        return []
    dates = stamps.dt.tz_convert("UTC").dt.normalize().drop_duplicates().sort_values()
    return list(dates)


def _is_turn_window(as_of: pd.Timestamp, prices: pd.DataFrame, pre_sessions: int, post_sessions: int) -> bool:
    sessions = _observed_sessions(prices)
    if not sessions:
        return False
    day = as_of.tz_convert("UTC").normalize()
    if day not in set(sessions):
        return False
    month_sessions = [s for s in sessions if s.year == day.year and s.month == day.month]
    if not month_sessions:
        return False
    first_sessions = set(month_sessions[: max(int(post_sessions), 0)])
    last_sessions = set(month_sessions[-max(int(pre_sessions), 0):]) if int(pre_sessions) > 0 else set()
    return day in first_sessions or day in last_sessions


def _active_symbols(context: Any, symbols: list[str], min_observations: int) -> list[str]:
    prices = getattr(context, "prices", pd.DataFrame())
    if prices.empty or "symbol" not in prices or "close" not in prices:
        return symbols
    active = []
    for symbol in symbols:
        series = prices.loc[prices["symbol"] == symbol, "close"].dropna()
        if len(series) >= int(min_observations):
            active.append(symbol)
    return active


def generate_signals(context: Any) -> dict[str, float]:
    """Return frozen ToM validator weights for qfa context symbols."""
    output_symbols = list(getattr(context, "symbols", []) or [])
    if not output_symbols:
        return {}
    prices = getattr(context, "prices", pd.DataFrame())
    as_of = _as_timestamp(context)
    params = _params(context)
    zeros = {symbol: 0.0 for symbol in output_symbols}
    if as_of is None or prices.empty:
        return zeros
    if not _is_turn_window(as_of, prices, int(params["pre_month_end_sessions"]), int(params["post_month_start_sessions"])):
        return zeros
    eligible = [s for s in output_symbols if s in SELECTED_UNIVERSE]
    active = _active_symbols(context, eligible, int(params["min_observations"]))
    if not active:
        return zeros
    weight = min(1.0 / len(active), float(params["max_abs_weight"]))
    return {symbol: (float(weight) if symbol in active else 0.0) for symbol in output_symbols}
