# AR-179 latest source-gate result

- run_id: `ar179_source_gate_20260701T085214Z`
- decision/status: `rejected` / `rejected_source_gate`
- asset_bucket: equity
- crypto_label: false
- no_csv_used: true
- no_data_csv_argument_used: true
- no_daemon: true
- no_orders: true
- raw_daily_paths_retained: false
- metrics: null

## Bounded SEC EDGAR probe

Official SEC EDGAR only: `company_tickers.json`, 12 issuer submissions, and 30 recent 8-K/10-Q/10-K-related filing documents/exhibits. Network request timeout cap was 10 seconds. Sample included AAPL, NFLX, SNDK, MSFT, GOOGL, AMZN, META, NVDA, JPM, WMT, HD, and XOM.

Counts:

- docs_scanned: 30
- candidate_hits: 10
- confirmed_events_sample: 4
- mapped_liquid_events: 4
- parser_precision_sample: 0.4

Confirmed sample examples included AAPL additional $100B, NFLX additional $25B, SNDK $6B, and NVDA additional $80B buyback authorization wording.

## Rejection

Rejected at source gate: no durable broad parser/event table with >=150 conservatively mapped liquid authorization/increase events was built in this hard-capped micro-scout. No qfa/Alpaca performance was run.
