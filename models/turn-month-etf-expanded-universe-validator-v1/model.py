"""AR-193 frozen AR-021 turn-of-month ETF expanded-universe validator.

Contract: expose generate_signals(context) -> dict[str, float].  The rule is
intentionally frozen: long-only equal-weight exposure during the final one
observed market session and first four observed market sessions of each month;
flat otherwise.  There is no parameter search, volatility gate, regime gate, or
performance-selected universe.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import pandas as pd

SELECTED_SYMBOLS = [
    "SPY", "QQQ", "IWM", "DIA", "VTI", "MDY", "IJR", "EFA", "EEM", "EWJ",
    "EWZ", "FXI", "XLB", "XLE", "XLF", "XLI", "XLK", "XLP", "XLU", "XLV",
    "XLY", "IWF", "IWD", "MTUM", "QUAL", "USMV", "VLUE", "TLT", "IEF",
    "SHY", "BIL", "AGG", "BND", "LQD", "HYG", "TIP", "EMB", "GLD", "SLV",
    "DBC", "DBA", "USO", "UNG", "VNQ", "REM", "UUP", "FXE", "FXY",
]
PRE_MONTH_END_SESSIONS = 1
POST_MONTH_START_SESSIONS = 4
MIN_OBSERVATIONS = 20


def _get(context: Any, name: str, default: Any = None) -> Any:
    if isinstance(context, Mapping):
        return context.get(name, default)
    return getattr(context, name, default)


def _as_prices_frame(prices: Any) -> pd.DataFrame:
    if prices is None:
        return pd.DataFrame()
    if isinstance(prices, pd.DataFrame):
        return prices
    try:
        return pd.DataFrame(prices)
    except Exception:
        return pd.DataFrame()


def _as_timestamp(context: Any, prices: pd.DataFrame) -> pd.Timestamp | None:
    as_of = _get(context, "as_of")
    if as_of is not None:
        ts = pd.Timestamp(as_of)
        return ts.tz_convert("UTC") if ts.tzinfo else ts.tz_localize("UTC")
    if prices.empty or "timestamp" not in prices:
        return None
    stamps = pd.to_datetime(prices["timestamp"], utc=True, errors="coerce").dropna()
    if stamps.empty:
        return None
    ts = stamps.max()
    if pd.isna(ts) or not isinstance(ts, pd.Timestamp):
        return None
    return ts


def _observed_sessions(context: Any, prices: pd.DataFrame) -> list[pd.Timestamp]:
    supplied = _get(context, "sessions") or _get(context, "observed_sessions")
    if supplied is not None:
        stamps = pd.to_datetime(pd.Series(list(supplied)), utc=True, errors="coerce").dropna()
        return list(stamps.dt.tz_convert("UTC").dt.normalize().drop_duplicates().sort_values())
    if prices.empty or "timestamp" not in prices:
        return []
    stamps = pd.to_datetime(prices["timestamp"], utc=True, errors="coerce").dropna()
    if stamps.empty:
        return []
    dates = stamps.dt.tz_convert("UTC").dt.normalize().drop_duplicates().sort_values()
    return list(dates)


def _is_turn_window(as_of: pd.Timestamp, sessions: list[pd.Timestamp]) -> bool:
    if not sessions:
        return False
    day = as_of.tz_convert("UTC").normalize()
    session_set = set(sessions)
    if day not in session_set:
        return False
    month_sessions = [s for s in sessions if s.year == day.year and s.month == day.month]
    if not month_sessions:
        return False
    first_sessions = set(month_sessions[:POST_MONTH_START_SESSIONS])
    last_sessions = set(month_sessions[-PRE_MONTH_END_SESSIONS:])
    return day in first_sessions or day in last_sessions


def _active_symbols(symbols: list[str], prices: pd.DataFrame) -> list[str]:
    allowed = [symbol for symbol in symbols if symbol in SELECTED_SYMBOLS]
    if prices.empty or "symbol" not in prices or "close" not in prices:
        return allowed
    counts = {
        symbol: len(prices.loc[prices["symbol"] == symbol, "close"].dropna())
        for symbol in allowed
    }
    if not any(count >= MIN_OBSERVATIONS for count in counts.values()):
        # Simple dict smoke contexts may provide only current bars.  In that
        # case, keep the selected/requested universe rather than failing flat.
        return allowed
    return [symbol for symbol, count in counts.items() if count >= MIN_OBSERVATIONS]


def generate_signals(context: Any) -> dict[str, float]:
    """Return target weights for qfa AlphaContext or a simple dict smoke context."""
    supplied_symbols = list(_get(context, "symbols", []) or [])
    symbols = supplied_symbols if supplied_symbols else SELECTED_SYMBOLS.copy()
    prices = _as_prices_frame(_get(context, "prices"))
    as_of = _as_timestamp(context, prices)
    if as_of is None:
        return {symbol: 0.0 for symbol in symbols}
    sessions = _observed_sessions(context, prices)
    if not _is_turn_window(as_of, sessions):
        return {symbol: 0.0 for symbol in symbols}
    active = _active_symbols(symbols, prices)
    if not active:
        return {symbol: 0.0 for symbol in symbols}
    weight = 1.0 / len(active)
    return {symbol: (weight if symbol in active else 0.0) for symbol in symbols}
