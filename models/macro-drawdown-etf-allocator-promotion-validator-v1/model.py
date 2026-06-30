"""AR-157 OHLCV-only macro-drawdown ETF allocator promotion/pruning validator.

Research-only qfa model. The allocator reconstructs stress states from ETF daily
OHLCV histories only: broad-market drawdowns, realized volatility shocks, credit
vs duration/gold/defensive relative moves, and recovery stabilization. It does
not use fabricated macro-surprise data, external calendars, daemon logic, or
order submission.
"""
from __future__ import annotations

import math
from typing import Any

import pandas as pd

MAX_WEIGHT = 0.18
DEFENSIVE_EQ = ["XLU", "XLP", "XLV"]


def _pivot(prices: pd.DataFrame) -> pd.DataFrame:
    px = prices.copy()
    px["timestamp"] = pd.to_datetime(px["timestamp"], utc=True)
    return px.pivot(index="timestamp", columns="symbol", values="close").sort_index().ffill()


def _z_last(series: pd.Series, window: int = 63) -> float:
    s = pd.to_numeric(series, errors="coerce").dropna().tail(window)
    if len(s) < max(20, window // 2):
        return 0.0
    sd = float(s.std(ddof=1))
    if not math.isfinite(sd) or sd <= 0:
        return 0.0
    return float((s.iloc[-1] - s.mean()) / sd)


def _ret(close: pd.DataFrame, symbol: str, days: int) -> float:
    if symbol not in close:
        return 0.0
    s = close[symbol].dropna()
    if len(s) <= days:
        return 0.0
    return float(s.iloc[-1] / s.iloc[-days - 1] - 1.0)


def _dd(close: pd.DataFrame, symbol: str, lookback: int) -> float:
    if symbol not in close:
        return 0.0
    s = close[symbol].dropna().tail(lookback)
    if len(s) < 40:
        return 0.0
    peak = float(s.max())
    return float(s.iloc[-1] / peak - 1.0) if peak > 0 else 0.0


def _normalize(raw: dict[str, float], symbols: list[str]) -> dict[str, float]:
    clean = {s: max(0.0, float(raw.get(s, 0.0))) for s in symbols}
    gross = sum(clean.values())
    if gross <= 0:
        return {s: (1.0 if s == "SHY" else 0.0) for s in symbols}
    clean = {s: v / gross for s, v in clean.items()}
    for _ in range(4):
        capped = {s: min(v, MAX_WEIGHT) for s, v in clean.items()}
        remaining = 1.0 - sum(capped.values())
        free = [s for s, v in clean.items() if v < MAX_WEIGHT]
        if remaining <= 1e-12 or not free:
            clean = capped
            break
        free_sum = sum(clean[s] for s in free)
        clean = {s: (capped[s] if s not in free else capped[s] + remaining * clean[s] / free_sum) for s in symbols}
    total = sum(clean.values())
    return {s: float(clean.get(s, 0.0) / total) if total > 0 else 0.0 for s in symbols}


def generate_signals(context: Any) -> dict[str, float]:
    """Return timestamp-safe target weights by symbol using historical OHLCV only."""
    symbols = list(getattr(context, "symbols", []))
    prices = getattr(context, "prices", None)
    if prices is None or len(prices) < 160 or not symbols:
        return {s: 0.0 for s in symbols}
    close = _pivot(prices)
    if "SPY" not in close or len(close["SPY"].dropna()) < 160:
        return {s: 0.0 for s in symbols}

    rets = close.pct_change()
    ret5 = close.pct_change(5)
    dd63 = _dd(close, "SPY", 63)
    dd126 = _dd(close, "SPY", 126)
    dd252 = _dd(close, "SPY", 252)
    vol_z = _z_last(rets["SPY"].rolling(10).std() * math.sqrt(252), 63)
    credit_z = _z_last(ret5.get("HYG", pd.Series(dtype=float)) - ret5.get("LQD", pd.Series(dtype=float)), 63)
    duration_z = _z_last(ret5.get("TLT", pd.Series(dtype=float)) - ret5.get("IEF", pd.Series(dtype=float)), 63)
    gold_z = _z_last(ret5.get("GLD", pd.Series(dtype=float)) - ret5.get("SPY", pd.Series(dtype=float)), 63)
    defensive_rel = sum(ret5.get(s, pd.Series(dtype=float)) for s in DEFENSIVE_EQ) / len(DEFENSIVE_EQ) - ret5.get("SPY", pd.Series(dtype=float))
    defensive_z = _z_last(defensive_rel, 63)

    stress_score = 0.0
    stress_score += max(0.0, (-dd63 - 0.05) / 0.10)
    stress_score += max(0.0, (-dd126 - 0.08) / 0.14)
    stress_score += max(0.0, (-dd252 - 0.12) / 0.20)
    stress_score += max(0.0, vol_z / 2.0)
    stress_score += max(0.0, -credit_z / 2.0)
    stress_score += max(0.0, defensive_z / 3.0)
    stress_score = min(2.5, stress_score)

    spy20 = _ret(close, "SPY", 20)
    spy5 = _ret(close, "SPY", 5)
    recovering = dd126 < -0.04 and spy20 > 0.025 and spy5 > -0.015 and credit_z > -0.25
    severe = stress_score >= 1.05 or (dd126 < -0.14 and vol_z > 0.25)

    if severe and not recovering:
        raw = {"TLT": 0.18, "IEF": 0.14, "SHY": 0.08, "SHV": 0.08, "AGG": 0.08, "LQD": 0.08, "GLD": 0.14, "UUP": 0.05, "XLU": 0.06, "XLP": 0.06, "XLV": 0.05}
        if duration_z < -0.8:
            raw["TLT"] -= 0.08
            raw["SHY"] += 0.04
            raw["SHV"] += 0.04
    elif recovering:
        raw = {"SPY": 0.15, "QQQ": 0.10, "IWM": 0.06, "RSP": 0.06, "VEA": 0.06, "VWO": 0.04, "HYG": 0.12, "LQD": 0.08, "GLD": 0.08, "IEF": 0.08, "TIP": 0.06, "DBC": 0.04, "SHY": 0.07}
    elif stress_score > 0.35:
        raw = {"SPY": 0.08, "QQQ": 0.04, "RSP": 0.04, "TLT": 0.13, "IEF": 0.12, "AGG": 0.08, "LQD": 0.10, "GLD": 0.13, "TIP": 0.06, "UUP": 0.04, "XLU": 0.07, "XLP": 0.06, "XLV": 0.05, "SHY": 0.10}
    else:
        raw = {"SPY": 0.10, "QQQ": 0.08, "IWM": 0.04, "DIA": 0.04, "MDY": 0.04, "RSP": 0.05, "VEA": 0.05, "VWO": 0.04, "HYG": 0.08, "LQD": 0.07, "AGG": 0.06, "TIP": 0.05, "GLD": 0.07, "DBC": 0.04, "VNQ": 0.04, "IEF": 0.06, "XLF": 0.03, "XLK": 0.03, "XLV": 0.03, "SHY": 0.10}

    if gold_z > 1.0:
        raw["GLD"] = raw.get("GLD", 0.0) + 0.03
        raw["SPY"] = max(0.0, raw.get("SPY", 0.0) - 0.02)
        raw["HYG"] = max(0.0, raw.get("HYG", 0.0) - 0.01)
    if credit_z < -0.75:
        raw["HYG"] = max(0.0, raw.get("HYG", 0.0) - 0.04)
        raw["LQD"] = raw.get("LQD", 0.0) + 0.02
        raw["SHY"] = raw.get("SHY", 0.0) + 0.02
    return _normalize(raw, symbols)
