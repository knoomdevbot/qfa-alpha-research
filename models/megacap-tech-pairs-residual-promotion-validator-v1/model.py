"""AR-184 mega-cap technology pairs residual promotion/pruning validator.

Research-only qfa model. It consumes historical OHLCV bars supplied in
``context.prices`` (normally qfa/Alpaca real daily bars) and returns target
symbol weights. It does not place orders, start daemons, access credentials, or
load CSV data.

The universe and economically related pair map are frozen ex ante in code; pair
inclusion is based on business/economic exposure, not realized alpha performance,
Sharpe, cointegration p-values, or return review.
"""

from __future__ import annotations

import math

import pandas as pd

UNIVERSE = (
    "AAPL", "ADBE", "ADI", "ADP", "ADSK", "AMAT", "AMD", "AMZN", "ASML", "AVGO",
    "CDNS", "CMCSA", "CRM", "CRWD", "CSCO", "DDOG", "DIS", "EA", "FIS", "FTNT",
    "GOOG", "GOOGL", "HPQ", "IBM", "INTC", "INTU", "KLAC", "LRCX", "MA", "MCHP",
    "MDB", "META", "MRVL", "MSFT", "MU", "NFLX", "NOW", "NVDA", "NXPI", "ON",
    "ORCL", "PANW", "PYPL", "QCOM", "ROP", "SHOP", "SNPS", "T", "TEAM", "TMUS",
    "TSM", "TTWO", "TXN", "UBER", "V", "VZ", "WDAY", "WDC", "XYZ", "ZS",
)

CLUSTERS = {
    "mega_platform_cloud_devices": ("AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "META", "ORCL", "IBM"),
    "ai_semis": ("NVDA", "AVGO", "AMD", "INTC", "QCOM", "TXN", "ADI", "MRVL", "MCHP", "NXPI", "ON"),
    "semi_equipment_foundry": ("AMAT", "LRCX", "KLAC", "ASML", "TSM"),
    "enterprise_software_cloud": ("CRM", "ADBE", "NOW", "INTU", "SHOP", "WDAY", "ADSK", "TEAM", "MDB", "DDOG", "NET"),
    "cybersecurity_infrastructure": ("PANW", "CRWD", "FTNT", "ZS", "ANET"),
    "communications_media": ("NFLX", "DIS", "CMCSA", "TMUS", "T", "VZ"),
    "payments_networks": ("V", "MA", "PYPL", "FIS", "FI", "ADP"),
    "platform_marketplaces": ("UBER", "ABNB", "AMZN", "SHOP", "META", "GOOGL", "GOOG"),
    "hardware_storage": ("DELL",),
    "eda_design": ("CDNS", "SNPS", "ROP", "ADSK"),
    "gaming_interactive": ("NFLX", "DIS"),
}

ADJACENT_PAIRS = (
    ("AAPL", "MSFT"), ("MSFT", "ORCL"), ("GOOGL", "META"), ("GOOG", "META"),
    ("AMZN", "SHOP"), ("NVDA", "AMD"), ("NVDA", "AVGO"), ("AMD", "INTC"),
    ("QCOM", "TXN"), ("AMAT", "LRCX"), ("LRCX", "KLAC"), ("ASML", "TSM"),
    ("CRM", "ADBE"), ("NOW", "CRM"), ("INTU", "ADP"), ("PANW", "CRWD"),
    ("FTNT", "ZS"), ("V", "MA"), ("PYPL", "V"), ("PYPL", "MA"), ("FIS", "FI"),
    ("TMUS", "VZ"), ("T", "VZ"), ("NFLX", "DIS"), ("CMCSA", "DIS"),
    ("UBER", "ABNB"), ("CDNS", "SNPS"),
)

FORMATION_WINDOW = 126
ZSCORE_WINDOW = 60
ENTRY_Z = 1.5
REBALANCE_DAYS = 5
MAX_ABS_WEIGHT = 0.08
MIN_SYMBOLS = 25


def _build_pairs(symbols: set[str]) -> tuple[tuple[str, str], ...]:
    pairs: set[tuple[str, str]] = set()
    for members in CLUSTERS.values():
        present = [s for s in members if s in symbols]
        for i, a in enumerate(present):
            for b in present[i + 1 :]:
                pairs.add((a, b) if a < b else (b, a))
    for a, b in ADJACENT_PAIRS:
        if a in symbols and b in symbols:
            pairs.add((a, b) if a < b else (b, a))
    return tuple(sorted(pairs))


PAIRS = _build_pairs(set(UNIVERSE))


def _zero(symbols):
    return {s: 0.0 for s in symbols}


def _normalize(scores: dict[str, float], output_symbols: list[str]) -> dict[str, float]:
    clean = {s: float(scores.get(s, 0.0)) for s in output_symbols if math.isfinite(float(scores.get(s, 0.0)))}
    if not clean:
        return _zero(output_symbols)
    mean_score = sum(clean.values()) / len(clean)
    clean = {s: v - mean_score for s, v in clean.items()}
    gross = sum(abs(v) for v in clean.values())
    if gross <= 0.0:
        return _zero(output_symbols)
    weights = {s: v / gross for s, v in clean.items()}
    weights = {s: max(-MAX_ABS_WEIGHT, min(MAX_ABS_WEIGHT, v)) for s, v in weights.items()}
    gross = sum(abs(v) for v in weights.values())
    if gross <= 0.0:
        return _zero(output_symbols)
    return {s: float(weights.get(s, 0.0) / gross) for s in output_symbols}


def _pair_residual_signal(log_close: pd.DataFrame, y_symbol: str, x_symbol: str) -> tuple[float, float]:
    pair = log_close[[y_symbol, x_symbol]].dropna()
    required = max(FORMATION_WINDOW, ZSCORE_WINDOW) + 1
    if len(pair) < required:
        return 0.0, 0.0
    formation = pair.iloc[-FORMATION_WINDOW:]
    y = formation[y_symbol]
    x = formation[x_symbol]
    x_var = float(x.var(ddof=0))
    if not math.isfinite(x_var) or x_var <= 0.0:
        return 0.0, 0.0
    beta = float(x.cov(y) / x_var)
    alpha = float(y.mean() - beta * x.mean())
    residual = pair[y_symbol] - (alpha + beta * pair[x_symbol])
    recent = residual.iloc[-ZSCORE_WINDOW:]
    resid_std = float(recent.std(ddof=0))
    if not math.isfinite(resid_std) or resid_std <= 0.0:
        return 0.0, 0.0
    z_score = float((recent.iloc[-1] - recent.mean()) / resid_std)
    if not math.isfinite(z_score) or abs(z_score) < ENTRY_Z:
        return 0.0, 0.0
    strength = max(-3.0, min(3.0, z_score))
    return -strength, strength


def generate_signals(context):
    """Return frozen pair-residual mean-reversion target weights.

    High residual ``y - beta*x`` means y is rich vs x, so the model shorts y and
    longs x; low residual does the reverse. Scores across frozen economic pairs
    are aggregated, demeaned, capped to 8% per name, and gross-normalized.
    """
    output_symbols = list(getattr(context, "symbols", ()))
    tradable = [s for s in output_symbols if s in UNIVERSE]
    if len(tradable) < MIN_SYMBOLS:
        return _zero(output_symbols)

    prices = getattr(context, "prices", pd.DataFrame()).copy()
    if prices.empty or "timestamp" not in prices or "symbol" not in prices or "close" not in prices:
        return _zero(output_symbols)
    prices["timestamp"] = pd.to_datetime(prices["timestamp"], utc=True)
    close = (
        prices[prices["symbol"].isin(tradable)]
        .pivot(index="timestamp", columns="symbol", values="close")
        .sort_index()
        .ffill()
    )
    close = close.dropna(axis=1, how="any")
    tradable = [s for s in tradable if s in close.columns]
    if len(tradable) < MIN_SYMBOLS or len(close) < FORMATION_WINDOW + 1:
        return _zero(output_symbols)

    log_close = close[tradable].map(lambda value: math.log(float(value)) if float(value) > 0.0 else float("nan"))
    tradable_set = set(tradable)
    scores = {s: 0.0 for s in output_symbols}
    active_pairs = 0
    for y_symbol, x_symbol in PAIRS:
        if y_symbol not in tradable_set or x_symbol not in tradable_set:
            continue
        y_signal, x_signal = _pair_residual_signal(log_close, y_symbol, x_symbol)
        if y_signal == 0.0 and x_signal == 0.0:
            continue
        scores[y_symbol] += y_signal
        scores[x_symbol] += x_signal
        active_pairs += 1
    if active_pairs == 0:
        return _zero(output_symbols)
    return _normalize(scores, output_symbols)
