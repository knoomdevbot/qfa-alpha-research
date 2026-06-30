"""AR-164 low-vol/smooth-return quality expanded-universe validator.

Research-only qfa-compatible model. It exposes generate_signals(context) and never
places orders. The associated AR-164 evaluation rejected this signal family after
real Alpaca daily-bar validation with costs and controls.
"""

from __future__ import annotations

import math
from typing import Any

import pandas as pd

SELECTED_UNIVERSE = (
    "AAPL", "MSFT", "NVDA", "AVGO", "ORCL", "CRM", "ADBE", "AMD", "INTC", "CSCO",
    "IBM", "QCOM", "TXN", "NOW", "AMAT", "GOOGL", "GOOG", "META", "NFLX", "DIS",
    "CMCSA", "TMUS", "VZ", "T", "EA", "TTWO", "AMZN", "TSLA", "HD", "MCD", "NKE",
    "SBUX", "LOW", "BKNG", "TJX", "GM", "F", "ORLY", "MAR", "WMT", "COST", "PG",
    "KO", "PEP", "PM", "MO", "MDLZ", "CL", "TGT", "KMB", "KR", "LLY", "UNH", "JNJ",
    "ABBV", "MRK", "PFE", "TMO", "ABT", "DHR", "BMY", "AMGN", "GILD", "CVS", "ISRG",
    "JPM", "BAC", "WFC", "GS", "MS", "C", "AXP", "BLK", "SCHW", "USB", "PNC", "AIG",
    "MET", "COF", "GE", "CAT", "HON", "UPS", "RTX", "LMT", "DE", "BA", "UNP", "ADP",
    "MMM", "EMR", "ETN", "XOM", "CVX", "COP", "SLB", "EOG", "MPC", "PSX", "VLO",
    "OXY", "HAL", "KMI", "NEE", "DUK", "SO", "AEP", "EXC", "SRE", "D", "PEG", "ED",
    "XEL", "LIN", "APD", "SHW", "ECL", "FCX", "NEM", "DD", "DOW", "NUE", "MLM",
    "AMT", "PLD", "EQIX", "SPG", "CCI", "PSA", "O", "WELL", "DLR", "VTR",
)

VOL_WINDOW = 63
DOWNSIDE_WINDOW = 63
SMOOTH_WINDOW = 63
MIN_SYMBOLS = 30
LONG_FRACTION = 0.20
SHORT_FRACTION = 0.20
GROSS_EXPOSURE = 1.0


def _zero_weights(symbols: list[str]) -> dict[str, float]:
    return {symbol: 0.0 for symbol in symbols}


def _rank_scores(close: pd.DataFrame) -> pd.Series:
    returns = close.pct_change()
    realized_vol = returns.tail(VOL_WINDOW).std(ddof=1) * math.sqrt(252)
    downside_vol = returns.tail(DOWNSIDE_WINDOW).where(returns < 0.0, 0.0).std(ddof=1) * math.sqrt(252)
    smoothness = returns.tail(SMOOTH_WINDOW).diff().std(ddof=1)
    features = pd.concat(
        [
            realized_vol.rank(pct=True),
            downside_vol.rank(pct=True),
            smoothness.rank(pct=True),
        ],
        axis=1,
    )
    # Lower volatility/downside/smoothness ranks are better; negate so high is good.
    return -features.mean(axis=1).dropna()


def generate_signals(context: Any) -> dict[str, float]:
    """Return market-neutral low-vol-quality validator weights.

    Expected qfa context fields: `symbols` and `prices` with timestamp/symbol/close.
    The signal is intentionally frozen for validation: 63-day realized-volatility,
    downside-volatility, and return-smoothness ranks; long the best 20% and short
    the worst 20%, normalized to 100% gross. No optimization or order placement.
    """
    output_symbols = list(getattr(context, "symbols", []))
    prices = getattr(context, "prices", None)
    if prices is None or prices.empty or not output_symbols:
        return _zero_weights(output_symbols)

    symbols = [symbol for symbol in output_symbols if symbol in SELECTED_UNIVERSE]
    if len(symbols) < MIN_SYMBOLS:
        return _zero_weights(output_symbols)

    frame = prices.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    close = (
        frame[frame["symbol"].isin(symbols)]
        .pivot(index="timestamp", columns="symbol", values="close")
        .sort_index()
        .ffill(limit=3)
        .dropna(axis=1, how="any")
    )
    if len(close) < VOL_WINDOW + 2 or close.shape[1] < MIN_SYMBOLS:
        return _zero_weights(output_symbols)

    scores = _rank_scores(close)
    if len(scores) < MIN_SYMBOLS:
        return _zero_weights(output_symbols)

    ordered = scores.sort_values(ascending=False)
    long_n = max(5, int(len(ordered) * LONG_FRACTION))
    short_n = max(5, int(len(ordered) * SHORT_FRACTION))
    longs = list(ordered.head(long_n).index)
    shorts = list(ordered.tail(short_n).index)
    weights = _zero_weights(output_symbols)
    long_weight = (GROSS_EXPOSURE / 2.0) / len(longs)
    short_weight = -(GROSS_EXPOSURE / 2.0) / len(shorts)
    for symbol in longs:
        if symbol in weights:
            weights[symbol] = float(long_weight)
    for symbol in shorts:
        if symbol in weights:
            weights[symbol] = float(short_weight)
    return weights
