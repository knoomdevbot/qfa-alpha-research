"""AR-185 closing-volume liquidity-exhaustion single-stock validator.

Research-only model for promotion/pruning validation of the AR-028/045/046/056
liquidity-reversal family. It consumes historical OHLCV bars supplied by qfa
context, returns target weights, and performs no data fetches, CSV loads, daemon
startup, or order placement.

The signal is intentionally frozen: abnormal volume plus close-location and
same-day move exhaustion are mapped to next-session cross-sectional reversal.
"""

from __future__ import annotations

import math

import pandas as pd

UNIVERSE = (
    "A", "AAPL", "ABBV", "ABT", "ADBE", "ADI", "ADP", "AEP", "AFL", "AIG", "AJG", "ALL",
    "AMAT", "AMD", "AMGN", "AMZN", "ANET", "AON", "APD", "APH", "AVGO", "AXP", "AZO", "BA",
    "BAC", "BDX", "BIIB", "BKNG", "BLK", "BMY", "BSX", "C", "CAT", "CB", "CCI", "CDNS", "CI",
    "CL", "CME", "CMG", "COF", "COP", "COST", "CPRT", "CRM", "CSCO", "CSX", "CTAS", "CVX",
    "DAL", "DD", "DE", "DHI", "DHR", "DIS", "DLR", "DUK", "DXCM", "ECL", "ELV", "EMR", "EOG",
    "EQIX", "ETN", "EW", "EXC", "F", "FAST", "FCX", "FDX", "GD", "GE", "GILD", "GM", "GOOG",
    "GOOGL", "GS", "HCA", "HD", "HLT", "HON", "IBM", "ICE", "IDXX", "INTU", "ISRG", "ITW", "JNJ",
    "JPM", "KLAC", "KMB", "KMI", "KO", "LIN", "LLY", "LMT", "LOW", "LRCX", "MA", "MAR", "MCD",
    "MCO", "MDLZ", "MDT", "MET", "META", "MMC", "MMM", "MNST", "MO", "MPC", "MRK", "MS", "MSFT",
    "MSI", "MU", "NEE", "NEM", "NFLX", "NKE", "NOC", "NOW", "NSC", "NVDA", "NXPI", "O", "ODFL",
    "OKE", "ORCL", "ORLY", "OXY", "PANW", "PAYX", "PCAR", "PEP", "PFE", "PG", "PGR", "PH", "PLD",
    "PM", "PNC", "PPG", "PSA", "PSX", "PYPL", "QCOM", "REGN", "ROP", "ROST",
)

RETURN_Z_WINDOW = 60
VOLUME_MEDIAN_WINDOW = 60
VOLUME_Z_WINDOW = 126
VOLUME_Z_GATE = 0.75
RETURN_Z_GATE = 0.50
CLOSE_LOCATION_GATE = 0.25
TOP_BOTTOM_QUANTILE = 0.20
MAX_ABS_WEIGHT = 0.03
MIN_SYMBOLS = 80
MIN_PRICE = 5.0
MIN_DOLLAR_VOLUME = 50_000_000.0


def _zero(symbols: list[str]) -> dict[str, float]:
    return {symbol: 0.0 for symbol in symbols}


def _pivot(prices: pd.DataFrame, field: str, symbols: list[str]) -> pd.DataFrame:
    return (
        prices[prices["symbol"].isin(symbols)]
        .pivot(index="timestamp", columns="symbol", values=field)
        .sort_index()
        .ffill()
    )


def _row_to_weights(row: pd.Series, output_symbols: list[str]) -> dict[str, float]:
    scores = row.dropna()
    scores = scores[scores != 0.0]
    if len(scores) < 10:
        return _zero(output_symbols)
    ranks = scores.rank(pct=True)
    chosen = scores[(ranks >= 1.0 - TOP_BOTTOM_QUANTILE) | (ranks <= TOP_BOTTOM_QUANTILE)]
    if len(chosen) < 10:
        return _zero(output_symbols)
    chosen = chosen.clip(-3.0, 3.0)
    gross = float(chosen.abs().sum())
    if not math.isfinite(gross) or gross <= 0.0:
        return _zero(output_symbols)
    weights = (chosen / gross).clip(-MAX_ABS_WEIGHT, MAX_ABS_WEIGHT)
    gross = float(weights.abs().sum())
    if not math.isfinite(gross) or gross <= 0.0:
        return _zero(output_symbols)
    weights = weights / gross
    return {symbol: float(weights.get(symbol, 0.0)) for symbol in output_symbols}


def generate_signals(context):
    """Return next-session target weights for the frozen validator signal."""
    output_symbols = list(getattr(context, "symbols", ()))
    tradable = [symbol for symbol in output_symbols if symbol in UNIVERSE]
    if len(tradable) < MIN_SYMBOLS:
        return _zero(output_symbols)

    prices = getattr(context, "prices", pd.DataFrame()).copy()
    required = {"timestamp", "symbol", "open", "high", "low", "close", "volume"}
    if prices.empty or not required.issubset(prices.columns):
        return _zero(output_symbols)
    prices["timestamp"] = pd.to_datetime(prices["timestamp"], utc=True)

    close = _pivot(prices, "close", tradable)
    high = _pivot(prices, "high", tradable)
    low = _pivot(prices, "low", tradable)
    volume = _pivot(prices, "volume", tradable)
    tradable = [symbol for symbol in tradable if symbol in close.columns]
    if len(tradable) < MIN_SYMBOLS or len(close) < VOLUME_Z_WINDOW + 2:
        return _zero(output_symbols)

    close = close[tradable]
    high = high[tradable]
    low = low[tradable]
    volume = volume[tradable]
    ret1 = close.pct_change()
    ret_z = (ret1 / ret1.rolling(RETURN_Z_WINDOW).std(ddof=0)).clip(-3.0, 3.0)
    vol_ratio = ((volume + 1.0) / (volume.rolling(VOLUME_MEDIAN_WINDOW).median() + 1.0)).map(math.log)
    vol_z = ((vol_ratio - vol_ratio.rolling(VOLUME_Z_WINDOW).mean()) / vol_ratio.rolling(VOLUME_Z_WINDOW).std(ddof=0)).clip(-3.0, 3.0)
    close_location = ((close - low) / (high - low).replace(0.0, pd.NA) - 0.5).clip(-0.5, 0.5).fillna(0.0)
    dollar_volume = (close * volume).rolling(20).mean()
    liquid = (close > MIN_PRICE) & (dollar_volume > MIN_DOLLAR_VOLUME)

    raw = -(0.65 * ret_z + 0.35 * (2.0 * close_location)) * vol_z.clip(lower=0.0)
    active = (vol_z > VOLUME_Z_GATE) & ((ret_z.abs() > RETURN_Z_GATE) | (close_location.abs() > CLOSE_LOCATION_GATE))
    raw = raw.where(active & liquid, 0.0).replace([float("inf"), float("-inf")], 0.0).fillna(0.0)
    demeaned = raw.sub(raw.mean(axis=1), axis=0)
    return _row_to_weights(demeaned.iloc[-1], output_symbols)
