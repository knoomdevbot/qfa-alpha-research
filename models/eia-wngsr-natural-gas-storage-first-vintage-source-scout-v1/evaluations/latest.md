# AR-192 Latest Evaluation

- Run ID: `ar192_hold_no_alpaca_credentials_20260701T225012Z`
- Completed at: 2026-07-01T22:50:12Z
- Status: `hold`
- Decision: `hold_realdata_blocked_no_alpaca_credentials`
- Asset bucket: ETF
- Crypto label: false

## Result

The source/vintage gate remains passed from the prior official EIA archive probe, but the required qfa/Alpaca real ETF performance evaluation could not be completed in this scheduled runtime.

qfa's virtual environment and `alpaca-py` are installed. The runtime did not expose usable Alpaca authentication, and an unauthenticated Alpaca stock-bars request failed before any market data was retrieved. Because AR-192 explicitly requires qfa/Alpaca real ETF bars and forbids CSV-backed market data, I placed the issue on hold rather than substituting another data source.

## Candidate universe policy

Broad pool considered for the eventual real-data run: UNG, UNL, XLE, XOP, AMLP, XLU, VPU, DBC, DBE, USO, PDBC, GSG, SPY, TLT, IEF, SHY, and FCG. BOIL, KOLD, and UGA are diagnostics-only because of leverage/inverse/special product risks.

Final universe selection is deferred until Alpaca daily-bar availability and history/liquidity can be verified. Direct natural-gas product limitations may require energy-sector/oil/gas proxy ETFs.

## Metrics

No performance metrics are reported because no real market bars were retrieved.

- Event count: null
- Selected universe: none
- Costs planned: 5, 10, and 20 bps; primary 10 bps
- SPY/equal-weight/trend-or-placebo controls: not run
- Turnover / Sharpe / drawdown: null
- Orthogonality: deferred due hold

## Required safety flags

- no_csv_used: true
- no_data_csv_argument_used: true
- no_daemon: true
- no_orders: true
- raw_daily_paths_retained: false
