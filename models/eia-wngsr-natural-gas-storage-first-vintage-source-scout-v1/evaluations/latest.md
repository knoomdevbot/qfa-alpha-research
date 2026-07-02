# AR-192 latest evaluation — EIA WNGSR storage-shock ETF scout

- **Decision:** rejected
- **Run ID:** `ar192_realdata_micro_20260701T223000Z`
- **Data:** official EIA dated archive pages plus qfa/Alpaca real daily OHLCV; no CSV, no daemon, no orders.
- **Universe:** `UNG`, `UNL`, `XLE`, `XOP`, `AMLP`, `XLU`, `DBC`, `USO`; controls included `SPY`, `UNG`, and an equal-weight exposed ETF basket.
- **Events:** 108 dated official pages parsed; 80 signal events after same-month seasonal warmup.
- **Protocol:** next-session and five-session event returns, 5/10/20 bps cost sensitivity, 30 contiguous 12-event random/stress windows for the five-session 10 bps decision series.

## Metrics

| Metric | Value |
|---|---:|
| Median random-window Sharpe | -0.2944 |
| p25 random-window Sharpe | -1.6450 |
| Worst random-window Sharpe | -2.6004 |
| Positive-window rate | 0.4000 |
| 5-session 10 bps event Sharpe | 0.0867 |
| 5-session equal-weight control Sharpe | 0.4664 |
| 5-session hit rate | 0.3125 |
| 5-session max drawdown proxy | -0.3132 |

## Rationale

Rejected because the after-cost random-window distribution was hostile and the equal-weight exposed ETF basket control dominated the event rule. The result prunes this simple WNGSR storage-shock ETF allocation hypothesis; no direct refinement child was spawned.

## Process caveat

A subagent timeout produced a partial artifact claiming market-data credentials were unavailable. Controller smoke testing independently verified configured market-data access and recovered with a hard-capped real-data micro-evaluator, so the issue was not placed on hold.
