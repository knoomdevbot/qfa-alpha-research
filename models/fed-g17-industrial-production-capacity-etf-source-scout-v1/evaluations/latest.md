# AR-182 source/vintage gate — 2026-07-01T11:21:40Z

Decision: **source_gate_pass** / `source_gate_passed_needs_realdata_evaluation`.

Official Federal Reserve G.17 source/vintage gate passed for a future real-data evaluator. No ETF market-data performance was run and the qfa wrapper is a disabled zero-weight scaffold.

## Diagnostics

- Release-date rows parsed: 949
- Official text events parsed: 303
- Official text parse failures: 0
- Archive TXT links: 303
- Parser path: `models/fed-g17-industrial-production-capacity-etf-source-scout-v1/model.py`.
- Sample events retained as compact examples only:
  - 2001-02-16 for 2001-01: INDPRO 147.0, TCU 80.2, URL https://www.federalreserve.gov/releases/g17/20010216/g17.txt
  - 2007-05-16 for 2007-04: INDPRO 113.0, TCU 81.6, URL https://www.federalreserve.gov/releases/g17/20070516/g17.txt
  - 2013-09-16 for 2013-08: INDPRO 99.4, TCU 77.8, URL https://www.federalreserve.gov/releases/g17/20130916/g17.txt
  - 2020-01-17 for 2019-12: INDPRO 109.4, TCU 77.0, URL https://www.federalreserve.gov/releases/g17/20200117/g17.txt
  - 2026-05-15 for 2026-04: INDPRO 102.5, TCU 76.1, URL https://www.federalreserve.gov/releases/g17/20260515/g17.txt

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

- This is not an accepted/watchlist alpha. It is a source-gate pass with no performance metrics.
- Future evaluation must use qfa/Alpaca real ETF bars, next-session timing, random windows, 10 bps primary cost, and controls versus static/equal ETF allocations, ETF TSMOM/reversal, shifted/random labels, inverted shocks, and macro-family controls.
