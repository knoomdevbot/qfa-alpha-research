# AR-162 source-gate recovery micro-scout

- Model: `fed-g19-consumer-credit-impulse-etf-scout-v1`
- Run: `ar162_sourcegate_20260630T150906Z`
- Decision: `rejected`
- Priority: `completed_source_gate_rejection`

## Official source evidence

- Release dates URL: `https://www.federalreserve.gov/releases/g19/releaseDates.json`
- Release count: 361
- Year buckets: 31
- Date range: `19960611` to `20260605`
- Sampled dated releases:
  - `https://www.federalreserve.gov/releases/g19/20260605/` — 3 semantic table titles; latest update June 05, 2026; period April 2026.
  - `https://www.federalreserve.gov/releases/g19/20241206/` — 3 semantic table titles; latest update December 06, 2024; period October 2024.
  - `https://www.federalreserve.gov/releases/g19/20201207/` — 3 semantic table titles; latest update December 07, 2020; period October 2020.
  - `https://www.federalreserve.gov/releases/g19/20101207/` — reachable fixed-width `<pre>` page; no semantic table titles; revolving/nonrevolving/outstanding text present.
  - `https://www.federalreserve.gov/releases/g19/20001207/` — reachable fixed-width `<pre>` page; no semantic table titles; revolving/nonrevolving/outstanding text present.

## Reason no real alpha/performance conclusion

The official dated-release source is reachable, but this bounded recovery pass did not build or validate a durable parser/event table across the modern semantic-table and older fixed-width-text vintages. No qfa/Alpaca daily-bar performance evaluator was run. Therefore there is no real alpha, Sharpe, drawdown, or control/orthogonality conclusion.

## Safety flags

- no_csv_used: true
- no_data_csv_argument_used: true
- no_daemon: true
- no_orders: true
- raw_daily_paths_retained: false
