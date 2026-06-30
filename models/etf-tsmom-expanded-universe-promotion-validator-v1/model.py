"""AR-156 ETF TSMOM expanded-universe promotion/pruning validator.

Rule-based qfa model using intermediate time-series momentum and realized-volatility
scaling. This file exposes generate_signals(context) for qfa. It is research-only;
no order submission or daemon behavior is present.
"""
from __future__ import annotations

import math
from typing import Dict

import pandas as pd

LOOKBACK_DAYS = 126
VOL_DAYS = 20
MAX_ABS_WEIGHT = 0.15
GROSS_EXPOSURE = 1.0


def _normalize(raw: Dict[str, float]) -> Dict[str, float]:
    """Gross-normalize inverse-vol scores while enforcing max position caps."""
    weights = {s: float(w) for s, w in raw.items()}
    gross = sum(abs(w) for w in weights.values())
    if gross <= 0:
        return {s: 0.0 for s in raw}
    weights = {s: w / gross * GROSS_EXPOSURE for s, w in weights.items()}
    capped: Dict[str, float] = {}
    free = dict(weights)
    remaining_gross = GROSS_EXPOSURE
    for _ in range(4):
        changed = False
        next_free: Dict[str, float] = {}
        free_gross = sum(abs(w) for w in free.values())
        scale = remaining_gross / free_gross if free_gross > 0 else 0.0
        for s, w in free.items():
            candidate = w * scale
            if abs(candidate) > MAX_ABS_WEIGHT:
                capped[s] = math.copysign(MAX_ABS_WEIGHT, candidate)
                remaining_gross -= MAX_ABS_WEIGHT
                changed = True
            else:
                next_free[s] = candidate
        free = next_free
        if not changed:
            break
    capped.update(free)
    return {s: capped.get(s, 0.0) for s in raw}


def generate_signals(context):
    """Return symbol weights for qfa AlphaContext.

    Signals are based only on bars available up to context.as_of. For each symbol,
    compute 126-day total return and 20-day realized vol. Positive momentum is long,
    negative momentum is short, and raw weights are inverse-vol scaled before gross
    normalization and per-symbol caps.
    """
    prices = context.prices.copy()
    if prices.empty:
        return {s: 0.0 for s in context.symbols}
    prices["timestamp"] = pd.to_datetime(prices["timestamp"], utc=True)
    close = prices.pivot(index="timestamp", columns="symbol", values="close").sort_index().ffill()
    raw: Dict[str, float] = {}
    for symbol in context.symbols:
        if symbol not in close:
            raw[symbol] = 0.0
            continue
        series = close[symbol].dropna()
        if len(series) < LOOKBACK_DAYS + 2:
            raw[symbol] = 0.0
            continue
        lookback_return = float(series.iloc[-1] / series.iloc[-LOOKBACK_DAYS - 1] - 1.0)
        realized_vol = float(series.pct_change().tail(VOL_DAYS).std())
        if not math.isfinite(lookback_return) or not math.isfinite(realized_vol) or realized_vol <= 0:
            raw[symbol] = 0.0
            continue
        raw[symbol] = (1.0 if lookback_return > 0 else -1.0) / (realized_vol * math.sqrt(252.0))
    return _normalize(raw)
