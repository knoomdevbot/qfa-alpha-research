# AR-167 defensive-carry expanded-universe validator evaluation

- Run ID: `ar167_qfa_alpaca_real_20260630T181153Z`
- Data: qfa/Alpaca real daily OHLCV, 2019-01-02 to 2026-06-26; no CSV, no daemon, no orders.
- Universe evaluated: 41 / 41 requested ETFs.
- Primary 10 bps Sharpe: `-0.34633238`; annualized return: `-0.01697512`; max drawdown: `-0.17673322`; annualized turnover: `13.36731246`.
- Cost sensitivity Sharpe: 5 bps `-0.2021884`, 10 bps `-0.34633238`, 20 bps `-0.63391374`.
- Random windows (10 bps): completed 50/50, median Sharpe `-0.07285195`, p25 `-0.82061204`, worst `-2.37592866`, positive rate `0.46`.
- Controls 10 bps Sharpe: SPY `0.86055226`, equal-weight `0.70942908`, TLT `-0.20769148`, IEF `-0.15289694`, SHY `-0.12804111`, carry proxy `0.20270384`, TSMOM proxy `-0.00200325`.
- Max absolute control correlation: `0.55827879`.
- Decision: **REJECTED**. Rationale: 10 bps random-window median Sharpe is not positive; positive random-window rate below 55%; 20 bps cost sensitivity is not positive; simple SPY/equal-weight controls are not both beaten.

Root JSON booleans confirm `no_csv_used`, `no_data_csv_argument_used`, `no_daemon`, `no_orders`; `raw_daily_paths_retained` is false.
