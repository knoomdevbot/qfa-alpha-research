# AR-186 qfa/Alpaca-only replication audit

Decision: **rejected**.

Provider-correct qfa/Alpaca daily ETF bars were fetched into memory only. No CSV, `--data-csv`, daemon, orders, raw bars, equity paths, weights, helper scripts, caches, or SQLite DBs are retained.

## Primary findings
- Universe: 56 selected of 56 predeclared broad liquid ETFs.
- 10 bps random-window Sharpe: median 0.6460, p25 0.0052, worst -1.8371; positive-window rate 74.55%.
- Full-sample 10 bps Sharpe 0.0675; max drawdown -24.14%; mean daily turnover 0.0739.
- Controls dominated: True; max relevant compact/proxy correlation: None.

## Conclusion
AR-063 remains pruned/rejected. The provider-correct qfa/Alpaca-only reconstruction does not materially overturn AR-157's rejection and triggers: controls_dominate.
