# AR-152 source-gate evaluation — SEC N-PORT holdings-change pressure scout

Run: `ar152_nport_source_gate_20260630T050044Z`  
Decision: **rejected at source/event-table gate**. No performance evaluation was run.

## What was checked

- SEC EDGAR quarterly full-index master files for 2024Q4 through 2026Q1 were reachable.
- The checked indexes contained 78,079 `NPORT-P` filings.
- A bounded sample of 80 filings was downloaded from public EDGAR archives.
- All 80 sampled filings had an acceptance timestamp and parseable XML.
- The parsed sample contained 21,697 holdings rows, 80 series IDs, 13 registrant CIKs, and 7,694 distinct CUSIP strings.

## Gate result

The source reachability/parser-reachability portion is promising, but the required alpha gate did **not** pass:

- The bounded sample had **0 filing-provided tickers**.
- A reliable public CUSIP-to-tradable-ticker mapping was not established.
- A same-series prior-holding comparison table was not built.
- Liquid U.S. common-stock/ETF coverage and concentration checks were not possible after the mapping failure.

Because the issue falsifier requires a reproducible timestamp-safe EDGAR holdings-change event table with conservative mapping before any return tests, this run is rejected before performance.

## Performance metrics

Null. No market data, random windows, shifted/shuffled controls, cost tests, daemon, or orders were used.

## Artifact status

The model is intentionally disabled and returns zero target weights.
