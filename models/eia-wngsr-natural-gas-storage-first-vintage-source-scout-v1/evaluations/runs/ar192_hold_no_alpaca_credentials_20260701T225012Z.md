# AR-192 Hold Artifact: No qfa/Alpaca ETF Market Data

- Run ID: `ar192_hold_no_alpaca_credentials_20260701T225012Z`
- Completed at: 2026-07-01T22:50:12Z
- Status: `hold`
- Decision: `hold_realdata_blocked_no_alpaca_credentials`

The prior official EIA source/vintage gate remains passed, but the required qfa/Alpaca real ETF performance evaluation could not be completed. qfa and alpaca-py were available; this runtime had no usable Alpaca authentication configured, and unauthenticated Alpaca stock bars failed before retrieving any market data.

No substitute CSV-backed market data was used. No daemon was started and no orders were placed.

Required flags: no_csv_used=true, no_data_csv_argument_used=true, no_daemon=true, no_orders=true, raw_daily_paths_retained=false.
