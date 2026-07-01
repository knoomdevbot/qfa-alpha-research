"""AR-178 frozen ETF defensive-rotation expanded-universe validator.

Research-only qfa model.  This deliberately freezes the AR-039/AR-051
monthly defensive-rotation form: 63/126-day momentum divided by 63-day
volatility, AR-051-style proxy-correlation penalty, risk-on vs defensive sleeve
selection, top-2 inverse-vol-scaled long-only allocation, and monthly holding.
The only material change is the predeclared expanded ETF universe supplied by
config/evaluation; no parameter optimization is performed here.
"""

from __future__ import annotations

import math

import pandas as pd

DEFAULT_PARAMS = {
    "momentum_lookback": 126,
    "secondary_lookback": 63,
    "vol_window": 63,
    "corr_window": 63,
    "min_periods": 190,
    "top_n": 2,
    "corr_penalty": 0.50,
    "target_vol": 0.10,
    "max_abs_weight": 0.50,
    "risk_on_symbols": (
        "SPY", "QQQ", "IWM", "MDY", "VTI", "RSP", "XLK", "XLY", "XLF",
        "XLI", "XLB", "XLE", "XLV", "SMH", "EFA", "EEM", "VNQ", "IYR",
    ),
    "defensive_symbols": (
        "XLU", "XLP", "TLT", "IEF", "SHY", "BIL", "SGOV", "SHV", "TIP",
        "GLD", "IAU", "LQD", "AGG", "BND", "MBB", "USMV", "SPLV", "QUAL", "SCHD",
    ),
    "tsmom_proxy_symbols": ("SPY", "QQQ", "TLT", "GLD"),
    "carry_defensive_proxy_symbols": ("IEF", "TLT", "GLD", "XLP", "XLU", "SHY"),
}


def _params(context) -> dict:
    metadata = getattr(context, "metadata", {}) or {}
    provided = metadata.get("params", {}) if isinstance(metadata, dict) else {}
    params = DEFAULT_PARAMS.copy()
    params.update({k: provided[k] for k in params.keys() & provided.keys()})
    return params


def _gross_normalize(weights: dict[str, float]) -> dict[str, float]:
    gross = sum(abs(v) for v in weights.values())
    if gross <= 0:
        return {symbol: 0.0 for symbol in weights}
    return {symbol: float(v / gross) for symbol, v in weights.items()}


def _cap_and_renormalize(weights: dict[str, float], cap: float) -> dict[str, float]:
    if not weights:
        return {}
    capped = {symbol: max(min(float(value), cap), -cap) for symbol, value in weights.items()}
    return _gross_normalize(capped)


def _monthly_decision_frame(close: pd.DataFrame, as_of: pd.Timestamp) -> pd.DataFrame:
    """Use data through prior month end so signals are lagged and monthly-held."""
    if close.empty:
        return close
    as_of = pd.Timestamp(as_of)
    month_start = pd.Timestamp(year=as_of.year, month=as_of.month, day=1, tz=as_of.tz)
    prior = close[close.index < month_start]
    if len(prior) >= 2:
        return prior
    return close[close.index <= as_of]


def _proxy_correlation_penalty(returns: pd.DataFrame, symbols: list[str], params: dict, corr_window: int) -> pd.Series:
    """AR-051-style penalty to simple TSMOM/carry-defensive proxy streams."""
    tail = returns.tail(corr_window).dropna(how="all")
    if len(tail) < 20:
        return pd.Series(0.0, index=symbols)
    proxy_series = []
    for key in ("tsmom_proxy_symbols", "carry_defensive_proxy_symbols"):
        members = [s for s in params[key] if s in tail.columns]
        if members:
            proxy_series.append(tail[members].mean(axis=1))
    if not proxy_series:
        return pd.Series(0.0, index=symbols)
    penalties = {}
    for symbol in symbols:
        if symbol not in tail.columns:
            penalties[symbol] = 0.0
            continue
        corrs = []
        for proxy in proxy_series:
            corr = tail[symbol].corr(proxy)
            if pd.notna(corr):
                corrs.append(abs(float(corr)))
        penalties[symbol] = max(corrs) if corrs else 0.0
    return pd.Series(penalties)


def generate_signals(context):
    """Return long-only monthly defensive-rotation target weights.

    Data use is restricted to same-source OHLCV in context.prices.  Decision
    history is truncated at the prior calendar month start and qfa applies the
    resulting weights after the current signal call, so the evaluation also
    shifts weights one trading day.
    """
    symbols = list(getattr(context, "symbols", []) or [])
    if not symbols:
        return {}

    params = _params(context)
    prices = getattr(context, "prices", pd.DataFrame()).copy()
    required = {"timestamp", "symbol", "close"}
    if prices.empty or not required.issubset(prices.columns):
        return {symbol: 0.0 for symbol in symbols}

    prices["timestamp"] = pd.to_datetime(prices["timestamp"], utc=True)
    close = (
        prices[prices["symbol"].isin(symbols)]
        .pivot(index="timestamp", columns="symbol", values="close")
        .sort_index()
        .ffill()
    )
    close = close.reindex(columns=symbols).dropna(how="all")
    if close.empty:
        return {symbol: 0.0 for symbol in symbols}
    as_of = pd.Timestamp(getattr(context, "as_of", close.index[-1]))
    decision_close = _monthly_decision_frame(close, as_of).dropna(how="all")
    if len(decision_close) < int(params["min_periods"]):
        return {symbol: 0.0 for symbol in symbols}

    long_lb = min(int(params["momentum_lookback"]), len(decision_close) - 1)
    short_lb = min(int(params["secondary_lookback"]), len(decision_close) - 1)
    vol_window = min(int(params["vol_window"]), len(decision_close) - 1)
    corr_window = min(int(params["corr_window"]), len(decision_close) - 1)
    if min(long_lb, short_lb, vol_window, corr_window) < 20:
        return {symbol: 0.0 for symbol in symbols}

    returns = decision_close.pct_change()
    ret_long = decision_close.iloc[-1] / decision_close.iloc[-1 - long_lb] - 1.0
    ret_short = decision_close.iloc[-1] / decision_close.iloc[-1 - short_lb] - 1.0
    realized_vol = (returns.tail(vol_window).std(ddof=1) * math.sqrt(252)).replace(0.0, pd.NA)
    realized_vol = realized_vol.fillna(float(params["target_vol"]))

    blended_momentum = 0.65 * ret_long + 0.35 * ret_short
    raw_score = (blended_momentum / realized_vol.clip(lower=0.05)).replace(
        [float("inf"), float("-inf")], pd.NA
    )
    corr_penalty = _proxy_correlation_penalty(returns, symbols, params, corr_window)
    score = (raw_score - float(params["corr_penalty"]) * corr_penalty).dropna()

    risk_on = [s for s in params["risk_on_symbols"] if s in symbols and s in score.index]
    defensive = [s for s in params["defensive_symbols"] if s in symbols and s in score.index]
    weights = {symbol: 0.0 for symbol in symbols}
    if not risk_on or not defensive:
        return weights

    risk_on_median = float(score.reindex(risk_on).dropna().median())
    defensive_median = float(score.reindex(defensive).dropna().median())
    spy_momentum = float(blended_momentum.get("SPY", 0.0) or 0.0)
    candidate_symbols = risk_on if (risk_on_median > defensive_median and spy_momentum > 0.0) else defensive

    ranked = score.reindex(candidate_symbols).dropna().sort_values(ascending=False)
    selected = list(ranked.head(max(1, int(params["top_n"]))).index)
    if not selected:
        selected = candidate_symbols[: max(1, int(params["top_n"]))]

    raw: dict[str, float] = {}
    for symbol in selected:
        positive_score = max(float(score.get(symbol, 0.0) or 0.0), 0.0)
        vol = float(realized_vol.get(symbol, params["target_vol"]) or params["target_vol"])
        raw[symbol] = (positive_score + 0.01) * min(float(params["target_vol"]) / max(vol, 1e-8), 3.0)
    if sum(abs(v) for v in raw.values()) <= 0.0:
        raw = {symbol: 1.0 for symbol in selected}

    weights.update(_cap_and_renormalize(raw, float(params["max_abs_weight"])))
    return weights
