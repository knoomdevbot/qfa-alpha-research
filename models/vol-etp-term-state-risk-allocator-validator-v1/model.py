"""AR-168 Vol-ETP term-state risk allocator fast-falsification validator.

Research-only qfa contract: expose generate_signals(context) -> dict[str, float].
The rule uses only completed daily OHLCV closes supplied by qfa/Alpaca. Volatility
ETPs are inputs only; the allocation universe is non-levered ETFs across risk and
defensive sleeves. No orders are placed by this model.
"""

from __future__ import annotations

import math

import pandas as pd

VOL_PROXIES = ("VIXY", "VXX", "VXZ", "SVXY")
RISK_SLEEVE = ("SPY", "QQQ", "IWM", "EFA", "EEM", "XLF", "XLE", "XLK", "HYG", "LQD", "DBC")
DEFENSIVE_SLEEVE = ("TLT", "IEF", "GLD", "UUP", "SHY")
UNIVERSE = VOL_PROXIES + RISK_SLEEVE + DEFENSIVE_SLEEVE
MIN_HISTORY = 80
STATE_WINDOW = 20


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        out = float(value)  # type: ignore[arg-type]
    except Exception:
        return default
    return out if math.isfinite(out) else default


def _window_return(close: pd.DataFrame, symbol: str, window: int = STATE_WINDOW) -> float:
    if symbol not in close.columns:
        return 0.0
    s = close[symbol].dropna()
    if len(s) <= window or s.iloc[-window - 1] <= 0:
        return 0.0
    return _safe_float(s.iloc[-1] / s.iloc[-window - 1] - 1.0)


def _ratio_return(close: pd.DataFrame, a: str, b: str, window: int = STATE_WINDOW) -> float:
    if a not in close.columns or b not in close.columns:
        return 0.0
    ratio = (close[a] / close[b]).replace([math.inf, -math.inf], pd.NA).dropna()
    if len(ratio) <= window or ratio.iloc[-window - 1] <= 0:
        return 0.0
    return _safe_float(ratio.iloc[-1] / ratio.iloc[-window - 1] - 1.0)


def _risk_on(close: pd.DataFrame) -> bool:
    ratio_mom = _ratio_return(close, "VIXY", "VXZ")
    short_vol_mom = _window_return(close, "VIXY")
    mid_vol_mom = _window_return(close, "VXZ")
    inverse_vol_mom = _window_return(close, "SVXY")
    # Predeclared term-state proxy: short-end vol ETP pressure falling and
    # inverse-vol appetite positive. This is intentionally simple for falsification.
    return ratio_mom < -0.02 and short_vol_mom < 0.0 and mid_vol_mom <= 0.05 and inverse_vol_mom > 0.0


def generate_signals(context) -> dict[str, float]:
    """Return target weights for qfa using completed daily prices in context."""
    output_symbols = list(getattr(context, "symbols", []))
    weights = {s: 0.0 for s in output_symbols}
    prices = getattr(context, "prices", None)
    if prices is None or prices.empty:
        return weights

    frame = prices.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    close = frame.pivot(index="timestamp", columns="symbol", values="close").sort_index().ffill()
    if len(close) < MIN_HISTORY or not all(s in close.columns for s in VOL_PROXIES):
        return weights

    if _risk_on(close):
        available = [s for s in RISK_SLEEVE if s in output_symbols and s in close.columns]
        if not available:
            return weights
        for symbol in available:
            weights[symbol] = 1.0 / len(available)
    else:
        defensive = {"TLT": 0.35, "IEF": 0.25, "GLD": 0.20, "UUP": 0.10, "SHY": 0.10}
        for symbol, weight in defensive.items():
            if symbol in weights and symbol in close.columns:
                weights[symbol] = weight
        gross = sum(weights.values())
        if gross > 0 and abs(gross - 1.0) > 1e-9:
            weights = {s: w / gross for s, w in weights.items()}
    return weights
