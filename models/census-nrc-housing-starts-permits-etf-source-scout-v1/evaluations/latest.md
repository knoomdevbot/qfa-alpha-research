# AR-183 source/vintage gate — 2026-07-01T11:19:52Z

Decision: **source_gate_passed_no_performance_disabled_scaffold**.

Official Census/HUD New Residential Construction archive/source feasibility passed for a future real-data evaluator. No ETF market-data performance was run and the qfa wrapper emits zero weights.

## Diagnostics

- Official NRC archive reachable: `https://www.census.gov/construction/nrc/data/releases.html`.
- Discovered official archived releases: 298 modern PDFs (`newresconst_200104.pdf` through `newresconst_202605.pdf`) and 149 legacy TXT files (`c20`/`c22`, 1995-01 through 2001-03).
- Parser path: `models/census-nrc-housing-starts-permits-etf-source-scout-v1/model.py`.
- Modern PDF bounded samples extracted timestamps and first-published headline values:
  - 2024-05: June 20, 2024 8:30 AM EDT; permits 1,386; starts 1,277; completions 1,514.
  - 2023-01: February 16, 2023 8:30 AM EST; permits 1,339; starts 1,309; completions 1,406.
  - 2020-01: February 19, 2020 8:30 AM EST; permits 1,551; starts 1,567; completions 1,280.
- Legacy TXT bounded samples parsed split releases:
  - `c20_0001.txt`: February 16, 2000 8:30 AM EST; starts 1,775; permits 1,763.
  - `c22_0001.txt`: March 6, 2000 10:00 AM EST; completions 1,556.
- Census current calendar page was reachable. A separate historical release-date Excel link was not discovered in bounded official-page probes; the archived official release files themselves contain timestamp text.
- ALFRED bounded vintage CSV probes for `HOUST`, `PERMIT`, and `COMPUTSA` timed out or closed without response in this environment, so ALFRED is not used as the primary source.

## Required booleans

- `no_csv_used`: true
- `no_data_csv_argument_used`: true
- `no_daemon`: true
- `no_orders`: true
- `raw_daily_paths_retained`: false
- `asset_bucket`: etf
- `crypto_label`: false
- `metrics`: null

## Warnings

- This is not an accepted/watchlist alpha. It is a source-gate pass with a disabled scaffold and no performance metrics.
- Future evaluation must use official first-vintage event tables, qfa/Alpaca real ETF bars, next-session timing unless same-day timing is proven safe, random windows, and controls versus static ETF allocations, TSMOM/reversal, CPI/PPI/labor/FOMC controls, shifted/random labels, and inverted shocks.
