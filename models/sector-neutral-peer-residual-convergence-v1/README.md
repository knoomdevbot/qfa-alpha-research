# sector-neutral-peer-residual-convergence-v1 (AR-177)

Interpretable qfa research model for testing whether lagged residual outliers inside trailing peer clusters of broad liquid U.S. common stocks converge over the next session.

## Signal

1. Use daily close-to-close real OHLCV only.
2. For each common stock, estimate trailing, shifted residuals versus SPY and the stock's sector ETF proxy.
3. Form monthly trailing peer clusters within static sectors using beta/volatility/60-day momentum features; no full-sample clustering.
4. Within each peer cluster, long negative residual outliers and short positive residual outliers using a 20% tail rule.
5. Dollar-neutral gross-normalized weights with per-name caps; ETF/control symbols receive zero trading weight.

## Evaluation

`evaluations/latest.json` and `evaluations/latest.md` contain the compact real-data Alpaca/qfa evaluation: universe filters, random-window metrics, cost sensitivity, controls/ablations, and the suggested decision. Raw bars, daily returns, equity curves, DBs, caches, and credentials are intentionally not retained.

## Compliance

No CSV market data, no `--data-csv`, no daemon, and no orders are used by this artifact.
