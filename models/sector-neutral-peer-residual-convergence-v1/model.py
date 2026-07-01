"""Sector-neutral peer-cluster residual convergence alpha (AR-177).

QFA contract: expose generate_signals(context) -> dict[symbol, weight].
Research-only; no orders or external side effects.
"""
from __future__ import annotations

import math
from collections import defaultdict

import numpy as np
import pandas as pd

CONTROL_SYMBOLS = {"SPY", "QQQ", "IWM", "XLK", "XLF", "XLV", "XLY", "XLP", "XLI", "XLE", "XLC", "XLU", "XLRE", "XLB"}

SECTOR = {
    "AAPL":"tech","MSFT":"tech","NVDA":"tech","AVGO":"tech","AMD":"tech","CRM":"tech","ADBE":"tech","ORCL":"tech","CSCO":"tech","ACN":"tech","INTU":"tech","IBM":"tech","QCOM":"tech","TXN":"tech","AMAT":"tech","MU":"tech","LRCX":"tech","NOW":"tech","PANW":"tech","SNPS":"tech",
    "GOOGL":"comm","GOOG":"comm","META":"comm","NFLX":"comm","DIS":"comm","CMCSA":"comm","TMUS":"comm","VZ":"comm","T":"comm","CHTR":"comm","EA":"comm","TTWO":"comm",
    "AMZN":"consumer_discretionary","TSLA":"consumer_discretionary","HD":"consumer_discretionary","MCD":"consumer_discretionary","NKE":"consumer_discretionary","SBUX":"consumer_discretionary","LOW":"consumer_discretionary","TJX":"consumer_discretionary","BKNG":"consumer_discretionary","CMG":"consumer_discretionary","MAR":"consumer_discretionary","ORLY":"consumer_discretionary","AZO":"consumer_discretionary","GM":"consumer_discretionary","F":"consumer_discretionary",
    "JPM":"financials","BAC":"financials","WFC":"financials","GS":"financials","MS":"financials","C":"financials","BLK":"financials","AXP":"financials","SCHW":"financials","USB":"financials","PNC":"financials","CME":"financials","ICE":"financials","COF":"financials","AIG":"financials","MET":"financials","PRU":"financials",
    "LLY":"healthcare","UNH":"healthcare","JNJ":"healthcare","MRK":"healthcare","ABBV":"healthcare","PFE":"healthcare","TMO":"healthcare","ABT":"healthcare","DHR":"healthcare","BMY":"healthcare","AMGN":"healthcare","GILD":"healthcare","ISRG":"healthcare","SYK":"healthcare","MDT":"healthcare","CVS":"healthcare","CI":"healthcare","HUM":"healthcare",
    "WMT":"staples","COST":"staples","PG":"staples","KO":"staples","PEP":"staples","PM":"staples","MO":"staples","MDLZ":"staples","CL":"staples","KMB":"staples","GIS":"staples","K":"staples","KR":"staples","EL":"staples",
    "CAT":"industrials","GE":"industrials","RTX":"industrials","HON":"industrials","UNP":"industrials","UPS":"industrials","BA":"industrials","LMT":"industrials","DE":"industrials","ADP":"industrials","ETN":"industrials","ITW":"industrials","FDX":"industrials","CSX":"industrials","NSC":"industrials","EMR":"industrials","MMM":"industrials",
    "XOM":"energy","CVX":"energy","COP":"energy","SLB":"energy","EOG":"energy","MPC":"energy","PSX":"energy","VLO":"energy","OXY":"energy","HAL":"energy","KMI":"energy","WMB":"energy",
    "LIN":"materials","APD":"materials","SHW":"materials","ECL":"materials","FCX":"materials","NEM":"materials","DOW":"materials","DD":"materials","NUE":"materials","MLM":"materials","VMC":"materials",
    "NEE":"utilities","SO":"utilities","DUK":"utilities","AEP":"utilities","SRE":"utilities","D":"utilities","EXC":"utilities","XEL":"utilities","ED":"utilities","PEG":"utilities",
    "PLD":"real_estate","AMT":"real_estate","EQIX":"real_estate","CCI":"real_estate","PSA":"real_estate","WELL":"real_estate","SPG":"real_estate","O":"real_estate","DLR":"real_estate","CBRE":"real_estate",
}
SECTOR_ETF = {"tech":"XLK","comm":"XLC","consumer_discretionary":"XLY","financials":"XLF","healthcare":"XLV","staples":"XLP","industrials":"XLI","energy":"XLE","materials":"XLB","utilities":"XLU","real_estate":"XLRE"}

class Params:
    lookback = 126
    min_lookback = 90
    residual_z_window = 60
    min_cluster_size = 6
    cluster_count_per_sector = 2
    quantile = 0.20
    max_abs_weight = 0.025
    min_active_names = 20

PARAMS = Params()

def _zero(symbols):
    return {s: 0.0 for s in symbols}

def _cap_gross(weights, cap):
    clean = {s: float(w) for s, w in weights.items() if math.isfinite(float(w)) and abs(float(w)) > 0}
    if not clean:
        return {s: 0.0 for s in weights}
    # dollar-neutral: normalize positive and negative books to 0.5 gross each
    pos = {s:w for s,w in clean.items() if w > 0}
    neg = {s:-w for s,w in clean.items() if w < 0}
    out = {s:0.0 for s in weights}
    for side, sign in ((pos, 1.0), (neg, -1.0)):
        total = sum(side.values())
        if total <= 0:
            continue
        for s, mag in side.items():
            out[s] = sign * min(cap, 0.5 * mag / total)
    gross = sum(abs(v) for v in out.values())
    if gross > 0:
        out = {s: v / gross for s, v in out.items()}
    return out

def _wide(prices, symbols):
    px = prices[prices["symbol"].isin(symbols)].copy()
    if px.empty:
        return None
    px["timestamp"] = pd.to_datetime(px["timestamp"], utc=True)
    px = px.sort_values(["timestamp", "symbol"])
    return px.pivot(index="timestamp", columns="symbol", values="close").sort_index().ffill()

def _kmeans_1d2(features: pd.DataFrame, k: int) -> dict[str, int]:
    # deterministic small k-means over beta/vol/momentum features, no sklearn dependency.
    x = features.dropna().to_numpy(dtype=float)
    syms = list(features.dropna().index)
    if len(syms) < k:
        return {s: 0 for s in syms}
    qs = np.linspace(0, len(syms) - 1, k).astype(int)
    order = np.argsort(x[:, 0])
    centers = x[order[qs]].copy()
    labels = np.zeros(len(syms), dtype=int)
    for _ in range(8):
        dist = ((x[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
        labels = dist.argmin(axis=1)
        for j in range(k):
            if np.any(labels == j):
                centers[j] = x[labels == j].mean(axis=0)
    return {s: int(label) for s, label in zip(syms, labels)}

def generate_signals(context):
    output_symbols = list(context.symbols)
    stocks = [s for s in output_symbols if s not in CONTROL_SYMBOLS and s in SECTOR]
    if len(stocks) < PARAMS.min_active_names or context.prices.empty:
        return _zero(output_symbols)
    need = set(stocks) | {"SPY", "QQQ", "IWM"} | {SECTOR_ETF.get(SECTOR[s], "SPY") for s in stocks}
    close = _wide(context.prices, list(need))
    if close is None or len(close) < PARAMS.lookback + PARAMS.residual_z_window + 2:
        return _zero(output_symbols)
    ret = close.pct_change().replace([np.inf, -np.inf], np.nan)
    mkt = ret.get("SPY")
    if mkt is None or mkt.tail(PARAMS.lookback).isna().any():
        return _zero(output_symbols)
    resid = pd.DataFrame(index=ret.index, columns=stocks, dtype=float)
    lb = PARAMS.lookback
    for s in stocks:
        if s not in ret:
            continue
        sec_proxy = ret.get(SECTOR_ETF.get(SECTOR[s], "SPY"), mkt).fillna(mkt)
        y = ret[s]
        x1 = mkt
        x2 = sec_proxy - mkt
        cov1 = y.rolling(lb, min_periods=PARAMS.min_lookback).cov(x1)
        var1 = x1.rolling(lb, min_periods=PARAMS.min_lookback).var().replace(0, np.nan)
        b1 = (cov1 / var1).clip(-3, 3).shift(1)
        y1 = y - b1 * x1
        cov2 = y1.rolling(lb, min_periods=PARAMS.min_lookback).cov(x2)
        var2 = x2.rolling(lb, min_periods=PARAMS.min_lookback).var().replace(0, np.nan)
        b2 = (cov2 / var2).clip(-3, 3).shift(1).fillna(0)
        resid[s] = y - b1 * x1 - b2 * x2
    latest = ret.index[-1]
    # Clusters use only trailing returns ending at latest completed bar; next-bar return is never included.
    hist = ret.loc[:latest].tail(lb)
    scores = {}
    for sector, members in defaultdict(list, {k: [s for s in stocks if SECTOR[s] == k] for k in set(SECTOR.values())}).items():
        members = [s for s in members if s in hist and hist[s].notna().sum() >= PARAMS.min_lookback]
        if len(members) < PARAMS.min_cluster_size:
            continue
        feat = pd.DataFrame(index=members)
        feat["beta"] = [hist[s].cov(mkt.reindex(hist.index)) / max(mkt.reindex(hist.index).var(), 1e-9) for s in members]
        feat["vol"] = [hist[s].std() for s in members]
        feat["mom"] = [(close[s].pct_change(60).loc[latest] if s in close else np.nan) for s in members]
        feat = (feat - feat.mean()) / feat.std(ddof=0).replace(0, np.nan)
        labels = _kmeans_1d2(feat.fillna(0), min(PARAMS.cluster_count_per_sector, max(1, len(members)//PARAMS.min_cluster_size)))
        by_label = defaultdict(list)
        for s, label in labels.items():
            by_label[label].append(s)
        for group in by_label.values():
            if len(group) < PARAMS.min_cluster_size:
                continue
            rz = resid[group].rolling(PARAMS.residual_z_window, min_periods=40).mean().iloc[-1]
            rs = resid[group].rolling(PARAMS.residual_z_window, min_periods=40).std().iloc[-1].replace(0, np.nan)
            z = ((resid[group].iloc[-1] - rz) / rs).dropna()
            if len(z) < PARAMS.min_cluster_size:
                continue
            peer = z.mean()
            dev = z - peer
            n = max(1, int(math.ceil(PARAMS.quantile * len(dev))))
            for s in dev.nsmallest(n).index:
                scores[s] = scores.get(s, 0.0) + float(-dev[s])
            for s in dev.nlargest(n).index:
                scores[s] = scores.get(s, 0.0) - float(dev[s])
    if len(scores) < PARAMS.min_active_names:
        return _zero(output_symbols)
    raw = {s: scores.get(s, 0.0) for s in output_symbols}
    for c in CONTROL_SYMBOLS:
        if c in raw:
            raw[c] = 0.0
    return _cap_gross(raw, PARAMS.max_abs_weight)
