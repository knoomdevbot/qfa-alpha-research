# AR-176 evaluation — source/vintage gate

- Run ID: `ar176_source_gate_20260701T053515Z`
- Decision: **rejected at source gate**
- qfa market-data evaluation: **not run**

## Official-source probe

Bounded sample: official BEA dated Personal Income and Outlays May-release pages for 2010, 2015, 2020, 2025, and 2026.

| Metric | Count |
|---|---:|
| Official pages probed | 5 |
| Reachable pages | 5 |
| Pages with 8:30 a.m. embargo/release text | 5 |
| Pages with release artifact links | 5 |
| Recent XLSX artifact smoke parses | 3 |
| Full component pages | 1 |
| Near-full component pages | 1 |
| Partial component pages | 3 |
| Dropped/ineligible releases | 3 |

Dropped reasons: incomplete component coverage (3); legacy binary XLS without local parser support (2).

## Rationale

The official BEA pages establish useful release-time and dated-page reachability, and recent releases can expose parser-readable XLSX workbooks. However, the bounded parser did not reproducibly extract the full required first-vintage component set across older and recent releases. Legacy pages rely on PDF/TXT/binary-XLS combinations and did not yield saving-rate, real-DPI, real-PCE, PCE-price, and core-PCE coverage with the current bounded parser.

Because the source/vintage gate did not pass, no ETF universe was selected beyond the predeclared candidate pool and no qfa real-data ETF evaluation was run.

## Required invariants

- no_csv_used: true
- no_data_csv_argument_used: true
- no_daemon: true
- no_orders: true
- raw_daily_paths_retained: false
