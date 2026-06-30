from __future__ import annotations

import pandas as pd


def generate_signals(context):
    """Generate AR-165 validator target weights from daily OHLCV context.

    Expected context keys: open, high, low, close, volume (DataFrames), optional sector dict
    and beta DataFrame. This is a research validator signal, not an order model.
    """
    high=context["high"]; low=context["low"]; close=context["close"]; volume=context["volume"]
    sectors=context.get("sector", {})
    beta=context.get("beta")
    clv=((close-low)/(high-low).replace(0, pd.NA)-0.5).clip(-0.5,0.5)
    lv=volume.replace(0,pd.NA).apply(lambda s: pd.Series(s, index=volume.index))
    volz=((lv.apply(lambda s: s.astype(float)).pipe(lambda x: x.apply(lambda s: s.map(lambda v: v))).apply(lambda s: s)).copy())
    import numpy as np
    logv=np.log(volume.replace(0,pd.NA).astype(float))
    volz=((logv-logv.rolling(60).mean())/logv.rolling(60).std()).clip(-3,3)
    range_pct=((high-low)/close).replace([np.inf,-np.inf],pd.NA)
    rangez=((range_pct-range_pct.rolling(60).mean())/range_pct.rolling(60).std()).clip(-3,3)
    event=(volz>1.0)&(clv.abs()>0.35)&(rangez>-0.25)
    score=(-clv*volz.clip(lower=0)*rangez.clip(lower=0.25)).where(event,0.0)
    # sector demean only in portable model; beta neutralization is evaluator-side when beta supplied.
    if sectors:
        for sec in set(sectors.values()):
            names=[s for s,v in sectors.items() if v==sec and s in score.columns]
            if names:
                score.loc[:,names]=score.loc[:,names].sub(score.loc[:,names].mean(axis=1),axis=0)
    weights=score.fillna(0.0)
    weights=weights.div(weights.abs().sum(axis=1).replace(0,pd.NA),axis=0).fillna(0.0)
    return weights
