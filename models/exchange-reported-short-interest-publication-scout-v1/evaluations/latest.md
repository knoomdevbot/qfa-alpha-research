# AR-172 source-gate result — rejected

- **Run ID:** `ar172_short_interest_source_gate_20260630T220639Z`
- **Decision:** rejected at source/vintage/breadth gate; zero-weight scaffold only.
- **Performance:** not run; metrics are null because the source gate failed.
- **Required flags:** `no_csv_used=true`, `no_data_csv_argument_used=true`, `no_daemon=true`, `no_orders=true`, `raw_daily_paths_retained=false`.

## Source metrics

| Source | Result | Blocking issue |
|---|---:|---|
| FINRA Equity Short Interest | API reachable; latest standardized partition `2026-06-15`; sample `record-total=9573`; first 5,000 rows all `marketClassCode=OTC` | Public path did not prove broad exchange-listed common-stock records or publication dates. |
| Nasdaq Trader Short Interest | Public page reachable; states rolling 12 months by issue; broad `.txt` files available by subscription/SFTP | Historical broad files and historical publication schedule were not freely reproducible; schedule URL redirected to Nasdaq Data Link/NSIR. |
| NYSE Group Short Interest | Official catalog reachable; history Jan 1988-present; public FTP sample has 2 files: 5,681 and 5,698 rows | Historical data is order/subscription product; sample-only files lack multi-year coverage and publication-vintage proof. |

## Gate decision

Hard gate required at least 150 liquid mapped common stocks with multi-year official/reproducible exchange-reported short-interest records, settlement dates, publication/dissemination dates, and qfa/Alpaca daily bar coverage. The gate failed before mapping/performance. No direct refinement or short-interest continuation child should be spawned from this rejection.
