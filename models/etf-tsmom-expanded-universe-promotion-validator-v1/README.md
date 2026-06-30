# ETF TSMOM expanded-universe promotion validator v1

AR-156 stress-tests AR-003/AR-015 ETF time-series momentum on an expanded ETF universe. The model is fixed-rule, not optimized: 126-day time-series momentum, 20-day realized-volatility scaling, weekly rebalance, max 15% per ETF, gross exposure 1.0.

Latest decision: **rejected**. See `evaluations/latest.json` and `evaluations/latest.md`.

Execution constraints satisfied: real qfa/Alpaca daily data, no CSV-backed market data, no daemon, no orders, no raw bars or daily return arrays retained.
