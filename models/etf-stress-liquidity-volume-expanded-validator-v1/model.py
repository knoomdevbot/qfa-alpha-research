"""AR-187 expanded-universe validator for AR-043 ETF stress-liquidity-volume.

Research-only qfa contract: expose generate_signals(context) -> dict[str, float].
The rule is a frozen AR-043-like daily OHLCV stress/volume/range allocator
expanded to a broad U.S.-listed ETF universe.  It uses completed daily bars only,
places no orders, and is intended as a terminal promotion/pruning validator.
"""

from __future__ import annotations

import math

import pandas as pd

UNIVERSE = (
    "SPY", "QQQ", "IWM", "DIA", "VTI", "MDY", "IJR", "EFA", "EEM", "EWJ", "EWZ", "FXI",
    "XLB", "XLE", "XLF", "XLI", "XLK", "XLP", "XLU", "XLV", "XLY", "IWF", "IWD", "MTUM",
    "QUAL", "USMV", "VLUE", "TLT", "IEF", "SHY", "BIL", "AGG", "BND", "LQD", "HYG", "TIP",
    "EMB", "GLD", "SLV", "DBC", "DBA", "USO", "UNG", "VNQ", "REM", "UUP", "FXE", "FXY",
)
RISK_ASSETS = (
    "SPY", "QQQ", "IWM", "DIA", "VTI", "MDY", "IJR", "EFA", "EEM", "EWJ", "EWZ", "FXI",
    "XLB", "XLE", "XLF", "XLI", "XLK", "XLY", "IWF", "IWD", "MTUM", "QUAL", "USMV", "VLUE", "HYG",
    "EMB", "DBC", "DBA", "USO", "UNG", "VNQ", "REM",
)
DEFENSIVE_ASSETS = ("TLT", "IEF", "SHY", "BIL", "AGG", "BND", "LQD", "TIP", "GLD", "SLV", "XLU", "XLP", "XLV", "UUP", "FXE", "FXY")

MIN_HISTORY = 130
BASELINE_WINDOW = 90
TREND_WINDOW = 40
VOL_WINDOW = 40
MAX_SINGLE_WEIGHT = 0.12
MIN_GROSS = 0.80


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        out = float(value)  # type: ignore[arg-type]
    except Exception:
        return default
    return out if math.isfinite(out) else default


def _clip(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def _zscore(current: float, hist: pd.Series) -> float:
    clean = hist.replace([math.inf, -math.inf], pd.NA).dropna()
    if len(clean) < 30:
        return 0.0
    mu = _safe_float(clean.mean())
    sd = _safe_float(clean.std(ddof=1))
    if sd <= 1e-12:
        return 0.0
    return _clip((current - mu) / sd, -3.0, 3.0)


def _ret(close: pd.DataFrame, symbol: str, window: int) -> float:
    if symbol not in close.columns:
        return 0.0
    series = close[symbol].dropna()
    if len(series) <= window or series.iloc[-window - 1] <= 0:
        return 0.0
    return _safe_float(series.iloc[-1] / series.iloc[-window - 1] - 1.0)


def _vol(close: pd.DataFrame, symbol: str, window: int) -> float:
    if symbol not in close.columns:
        return 0.0
    returns = close[symbol].dropna().pct_change().dropna().tail(window)
    if len(returns) < 10:
        return 0.0
    return _safe_float(returns.std(ddof=1) * math.sqrt(252.0))


def _basket_avg(values: list[float]) -> float:
    vals = [v for v in values if math.isfinite(v)]
    return sum(vals) / len(vals) if vals else 0.0


def _normalize_capped(scores: dict[str, float], budget: float) -> dict[str, float]:
    positives = {symbol: max(0.0, _safe_float(score)) for symbol, score in scores.items()}
    total = sum(positives.values())
    if budget <= 0 or total <= 0:
        return {symbol: 0.0 for symbol in scores}
    weights = {symbol: budget * score / total for symbol, score in positives.items()}
    for _ in range(8):
        excess = sum(max(0.0, weight - MAX_SINGLE_WEIGHT) for weight in weights.values())
        if excess <= 1e-12:
            break
        capped = {symbol for symbol, weight in weights.items() if weight >= MAX_SINGLE_WEIGHT}
        for symbol in capped:
            weights[symbol] = min(weights[symbol], MAX_SINGLE_WEIGHT)
        uncapped = {symbol: positives[symbol] for symbol in weights if symbol not in capped and positives[symbol] > 0}
        total_uncapped = sum(uncapped.values())
        if total_uncapped <= 0:
            break
        for symbol, score in uncapped.items():
            weights[symbol] += excess * score / total_uncapped
    return weights


def generate_signals(context) -> dict[str, float]:
    """Return qfa target weights from completed daily OHLCV bars in context."""
    symbols = list(getattr(context, "symbols", []))
    prices_obj = getattr(context, "prices", None)
    if prices_obj is None or getattr(prices_obj, "empty", True):
        return {symbol: 0.0 for symbol in symbols}

    prices = prices_obj.copy()
    prices["timestamp"] = pd.to_datetime(prices["timestamp"], utc=True)
    prices = prices[prices["symbol"].isin(UNIVERSE)].sort_values(["timestamp", "symbol"])
    close = prices.pivot(index="timestamp", columns="symbol", values="close").sort_index().ffill()
    high = prices.pivot(index="timestamp", columns="symbol", values="high").sort_index().ffill()
    low = prices.pivot(index="timestamp", columns="symbol", values="low").sort_index().ffill()
    volume = prices.pivot(index="timestamp", columns="symbol", values="volume").sort_index().ffill()
    if len(close) < MIN_HISTORY:
        return {symbol: 0.0 for symbol in symbols}

    available = [symbol for symbol in symbols if symbol in UNIVERSE and symbol in close.columns]
    if len(available) < 20:
        return {symbol: 0.0 for symbol in symbols}

    stress_components: dict[str, float] = {}
    clv_components: dict[str, float] = {}
    for symbol in available:
        c = close[symbol].dropna()
        h = high[symbol].reindex(c.index).ffill()
        lows = low[symbol].reindex(c.index).ffill()
        v = volume[symbol].reindex(c.index).ffill()
        if len(c) < MIN_HISTORY:
            continue
        hl_range = ((h - lows) / c.shift(1)).replace([math.inf, -math.inf], pd.NA).dropna()
        dollar_vol = (c * v).replace([math.inf, -math.inf], pd.NA).dropna()
        if len(hl_range) < BASELINE_WINDOW + 2 or len(dollar_vol) < BASELINE_WINDOW + 2:
            continue
        range_z = _zscore(_safe_float(hl_range.iloc[-1]), hl_range.iloc[-BASELINE_WINDOW - 1 : -1])
        log_dvol = dollar_vol.apply(lambda x: math.log(max(float(x), 1.0)))
        dvol_z = _zscore(_safe_float(log_dvol.iloc[-1]), log_dvol.iloc[-BASELINE_WINDOW - 1 : -1])
        denom = max(_safe_float(h.iloc[-1] - lows.iloc[-1]), 1e-9)
        close_location = _clip(_safe_float((c.iloc[-1] - lows.iloc[-1]) / denom), 0.0, 1.0)
        poor_close = 1.0 - close_location
        stress = 0.42 * max(0.0, range_z) + 0.38 * max(0.0, dvol_z) + 0.20 * poor_close
        stress_components[symbol] = _clip(stress / 2.2, 0.0, 1.0)
        clv_components[symbol] = close_location

    if len(stress_components) < 20:
        return {symbol: 0.0 for symbol in symbols}

    equity_stress = _basket_avg([stress_components.get(symbol, 0.0) for symbol in RISK_ASSETS if symbol in stress_components])
    defensive_stress = _basket_avg([stress_components.get(symbol, 0.0) for symbol in DEFENSIVE_ASSETS if symbol in stress_components])
    breadth = sum(1 for value in stress_components.values() if value > 0.55) / max(len(stress_components), 1)
    risk_stress = _clip(0.58 * equity_stress + 0.27 * breadth + 0.15 * max(0.0, equity_stress - defensive_stress), 0.0, 1.0)

    risk_off_budget = 0.22 + 0.58 * risk_stress
    risk_on_budget = 0.72 - 0.50 * risk_stress
    gross_target = _clip(risk_off_budget + risk_on_budget - 0.14 * max(0.0, risk_stress - 0.75), MIN_GROSS, 1.0)
    scale = gross_target / max(risk_off_budget + risk_on_budget, 1e-12)
    risk_off_budget *= scale
    risk_on_budget *= scale

    risk_scores: dict[str, float] = {}
    for symbol in RISK_ASSETS:
        if symbol not in available:
            continue
        stress_penalty = stress_components.get(symbol, 0.0)
        trend = _clip(_ret(close, symbol, TREND_WINDOW) / 0.08, -1.0, 1.0)
        realized_vol = _vol(close, symbol, VOL_WINDOW)
        risk_scores[symbol] = max(0.05, 1.0 + 0.35 * trend - 0.65 * stress_penalty - 0.30 * realized_vol)

    defensive_scores: dict[str, float] = {}
    for symbol in DEFENSIVE_ASSETS:
        if symbol not in available:
            continue
        trend = _clip(_ret(close, symbol, TREND_WINDOW) / 0.06, -1.0, 1.0)
        stress_penalty = stress_components.get(symbol, 0.0)
        clv = clv_components.get(symbol, 0.5)
        defensive_scores[symbol] = max(0.05, 1.0 + 0.45 * trend + 0.20 * clv - 0.45 * stress_penalty)

    weights = {symbol: 0.0 for symbol in symbols}
    for symbol, weight in _normalize_capped(risk_scores, risk_on_budget).items():
        weights[symbol] = weights.get(symbol, 0.0) + weight
    for symbol, weight in _normalize_capped(defensive_scores, risk_off_budget).items():
        weights[symbol] = weights.get(symbol, 0.0) + weight
    return {symbol: _safe_float(weights.get(symbol, 0.0)) for symbol in symbols}
