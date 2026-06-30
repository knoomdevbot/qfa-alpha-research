"""AR-167 expanded-universe defensive/carry ETF validator model.

Research-only qfa contract: expose generate_signals(context) -> dict[str, float].
This freezes a parent-style AR-037/AR-049 defensive/carry allocator over a broader
predeclared non-levered ETF universe. It uses only completed OHLCV bars supplied
by qfa/Alpaca and never places orders.
"""

from __future__ import annotations

import math
from typing import Dict

import pandas as pd

TREASURY = ("SHY", "IEI", "IEF", "TLH", "TLT")
TIPS = ("TIP", "SCHP")
CREDIT = ("LQD", "VCIT", "VCSH", "HYG", "JNK", "BKLN")
EQUITY = ("SPY", "QQQ", "IWM", "DIA", "RSP", "VTV", "VUG", "QUAL", "USMV")
SECTOR = ("XLU", "XLP", "XLV", "XLF", "XLI", "XLE", "XLK", "XLY", "XLB", "XLRE")
REAL_ASSET_FX = ("GLD", "SLV", "DBC", "USO", "UUP", "FXE", "FXY", "FXF", "FXA")
UNIVERSE = TREASURY + TIPS + CREDIT + EQUITY + SECTOR + REAL_ASSET_FX

MIN_HISTORY = 190
VOL_WINDOW = 63
DEF_WINDOW = 63
CARRY_WINDOW = 126
FAST_WINDOW = 21
MAX_SINGLE_WEIGHT = 0.16


def _safe_float(value, default: float = 0.0) -> float:
    try:
        out = float(value)
    except Exception:
        return default
    return out if math.isfinite(out) else default


def _series(close: pd.DataFrame, symbol: str) -> pd.Series:
    if symbol not in close.columns:
        return pd.Series(dtype=float)
    return close[symbol].dropna()


def _ret(close: pd.DataFrame, symbol: str, window: int) -> float:
    s = _series(close, symbol)
    if len(s) <= window or s.iloc[-window - 1] <= 0:
        return 0.0
    return _safe_float(s.iloc[-1] / s.iloc[-window - 1] - 1.0)


def _vol(close: pd.DataFrame, symbol: str, window: int) -> float:
    s = _series(close, symbol)
    if len(s) <= window:
        return 0.0
    return _safe_float(s.pct_change().dropna().tail(window).std() * math.sqrt(252.0))


def _drawdown(close: pd.DataFrame, symbol: str, window: int) -> float:
    s = _series(close, symbol).tail(window)
    if len(s) < 2:
        return 0.0
    peak = s.cummax()
    return _safe_float((s / peak - 1.0).iloc[-1])


def _zscore(values: Dict[str, float]) -> Dict[str, float]:
    vals = [v for v in values.values() if math.isfinite(v)]
    if not vals:
        return {k: 0.0 for k in values}
    mean = sum(vals) / len(vals)
    var = sum((v - mean) ** 2 for v in vals) / max(len(vals) - 1, 1)
    sd = math.sqrt(var)
    if sd <= 1e-12:
        return {k: 0.0 for k in values}
    return {k: max(-3.0, min(3.0, (v - mean) / sd)) for k, v in values.items()}


def _regime(close: pd.DataFrame) -> tuple[float, float]:
    spy_vol = _vol(close, "SPY", FAST_WINDOW) or _vol(close, "SPY", VOL_WINDOW)
    ief_vol = _vol(close, "IEF", VOL_WINDOW) or 0.06
    equity_dd = min(_drawdown(close, "SPY", DEF_WINDOW), _drawdown(close, "QQQ", DEF_WINDOW))
    vol_pressure = max(0.0, min(1.0, (spy_vol - 1.20 * ief_vol) / 0.32))
    dd_pressure = max(0.0, min(1.0, abs(min(0.0, equity_dd)) / 0.15))
    stress = max(0.0, min(1.0, 0.55 * vol_pressure + 0.45 * dd_pressure))
    trend_pack = [_ret(close, s, CARRY_WINDOW) for s in ("SPY", "QQQ", "TLT", "GLD") if s in close.columns]
    trend_penalty = sum(1 for r in trend_pack if r > 0.04) / max(len(trend_pack), 1)
    return stress, trend_penalty


def _allocate(weights: dict[str, float], scores: Dict[str, float], budget: float) -> None:
    if budget <= 0:
        return
    pos = {s: max(0.0, v) for s, v in scores.items() if s in weights}
    total = sum(pos.values())
    if total <= 0:
        names = list(pos)
        if not names:
            return
        for s in names:
            weights[s] += budget / len(names)
        return
    for s, v in pos.items():
        weights[s] += budget * v / total


def generate_signals(context) -> dict[str, float]:
    output_symbols = list(context.symbols)
    if context.prices is None or context.prices.empty:
        return {s: 0.0 for s in output_symbols}
    prices = context.prices.copy()
    prices["timestamp"] = pd.to_datetime(prices["timestamp"], utc=True)
    close = prices.pivot(index="timestamp", columns="symbol", values="close").sort_index().ffill()
    if len(close) < MIN_HISTORY:
        return {s: 0.0 for s in output_symbols}
    available = [s for s in output_symbols if s in UNIVERSE and s in close.columns]
    if len(available) < 12:
        return {s: 0.0 for s in output_symbols}

    stress, trend_penalty = _regime(close)
    weights = {s: 0.0 for s in output_symbols}
    eq_budget = 0.16 * (1.0 - 0.70 * stress) * (1.0 - 0.70 * trend_penalty)
    duration_budget = 0.30 + 0.15 * stress + 0.03 * trend_penalty
    credit_budget = 0.18 * (1.0 - 0.85 * stress)
    defensives_budget = 0.22 + 0.10 * stress
    alt_budget = 0.10 * (1.0 - 0.45 * stress) * (1.0 - 0.55 * trend_penalty)
    # residual deliberately stays cash-like rather than being forced into ETFs

    equity_raw = {s: -0.85 * _vol(close, s, VOL_WINDOW) + 0.25 * _drawdown(close, s, DEF_WINDOW) - 0.25 * max(0.0, _ret(close, s, CARRY_WINDOW)) for s in EQUITY + SECTOR if s in available}
    duration_raw = {s: 0.55 * _ret(close, s, DEF_WINDOW) + 0.20 * _ret(close, s, CARRY_WINDOW) - 0.70 * _vol(close, s, VOL_WINDOW) for s in TREASURY + TIPS if s in available}
    credit_raw = {s: 0.35 * _ret(close, s, DEF_WINDOW) + 0.15 * _ret(close, s, CARRY_WINDOW) - 1.00 * _vol(close, s, VOL_WINDOW) + 0.15 * _drawdown(close, s, DEF_WINDOW) for s in CREDIT if s in available}
    eq_fast = sum(_ret(close, s, FAST_WINDOW) for s in ("SPY", "QQQ", "IWM") if s in available) / max(sum(1 for s in ("SPY", "QQQ", "IWM") if s in available), 1)
    defensive_raw = {s: 0.45 * (_ret(close, s, DEF_WINDOW) - 0.25 * eq_fast) - 0.50 * _vol(close, s, VOL_WINDOW) for s in ("GLD", "UUP", "FXY", "XLU", "XLP", "XLV") if s in available}
    alt_raw = {s: 0.45 * _ret(close, s, CARRY_WINDOW) - 0.35 * abs(_ret(close, s, FAST_WINDOW)) - 0.55 * _vol(close, s, VOL_WINDOW) for s in REAL_ASSET_FX if s in available}

    _allocate(weights, {s: max(0.0, 1.0 + z) for s, z in _zscore(equity_raw).items()}, eq_budget)
    _allocate(weights, {s: max(0.0, 1.0 + z) for s, z in _zscore(duration_raw).items()}, duration_budget)
    _allocate(weights, {s: max(0.0, 1.0 + z) for s, z in _zscore(credit_raw).items()}, credit_budget)
    _allocate(weights, {s: max(0.0, 1.0 + z) for s, z in _zscore(defensive_raw).items()}, defensives_budget)
    _allocate(weights, {s: max(0.0, min(1.75, 1.0 + z)) for s, z in _zscore(alt_raw).items()}, alt_budget)

    capped = {s: max(0.0, min(MAX_SINGLE_WEIGHT, _safe_float(weights.get(s, 0.0)))) for s in output_symbols}
    gross = sum(capped.values())
    if gross > 1.0:
        capped = {s: w / gross for s, w in capped.items()}
    return capped
