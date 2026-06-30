# AR-171 latest evaluation

Decision: **source_gate_passed_needs_realdata_evaluation** (disabled zero-weight scaffold; not accepted/watchlist).

## Metrics

| Metric | Value |
|---|---:|
| SEC ticker rows reachable | 10433 |
| Sampled current SEC ticker rows | 500 |
| Submissions fetch OK | 500 |
| Recent 8-K rows | 41345 |
| Item 2.02 timestamp-safe events | 13088 |
| Mapped issuers with Item 2.02 | 375 |
| Accession proof count | 13088 |
| Primary document proof count | 13088 |
| Filing index reachable | 40/40 |
| Exhibit/press-like names found | 16/40 |
| qfa/Alpaca symbols with bars | 119/120 |
| qfa/Alpaca coverage rate | 99.17% |
| Top issuer event share | 0.79% |
| Top 10 issuer event share | 6.21% |

Root safeguards in latest JSON: `no_csv_used=true`, `no_data_csv_argument_used=true`, `no_daemon=true`, `no_orders=true`, `raw_daily_paths_retained=false`.

## Rationale

The bounded source gate exceeded the issue thresholds (>=1,000 timestamp-safe Item 2.02 events and >=200 mapped issuers). qfa/Alpaca daily coverage was checked on a compact 120-symbol mapped candidate sample. Because no durable parser/event table and no timestamp-safe real-data performance evaluation has been run, the correct state is active/queued scaffold, not completion, rejection, acceptance, or watchlist.
