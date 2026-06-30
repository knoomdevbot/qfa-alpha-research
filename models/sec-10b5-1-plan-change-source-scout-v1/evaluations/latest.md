# AR-161 source-gate result

Decision: **rejected**  
Run: `ar161_sourcegate_20260630T141002Z`

A bounded recovery micro-scout scanned official SEC 10-Q/10-K primary documents for Regulation S-K Item 408 / Rule 10b5-1 director/officer trading-arrangement adoption, modification, and termination disclosures. The probe used SEC company tickers plus submissions metadata and stopped at the required 120-filing budget. No raw filing text, event table, CSV market data, daemon output, or order artifacts were retained.

## Source-gate metrics

| Metric | Value |
|---|---:|
| Sampled issuers before filing cap | 10 |
| SEC filings inspected | 120 |
| Candidate 10b5-1 text hits | 111 |
| Item 408 context hits | 71 |
| Parsed valid plan-change event estimate | 130 |
| Mapped liquid event estimate | 130 |
| Gate-required liquid mapped events | 150 |
| Issuers/tickers with parsed events | 9 |
| Max ticker-level event share | 20.8% |
| Forms inspected | 89 10-Q; 31 10-K |

Action-type estimates: 70 adopted, 49 modified, 11 terminated. Filing years inspected: 2023: 28, 2024: 34, 2025: 38, 2026: 20.

## Rejection rationale

The official source is reachable and contains relevant Item 408 / 10b5-1 text, but the bounded probe did not establish at least 150 timestamp-safe liquid mapped issuer events after filters. The estimate remained 130 before deeper de-duplication, and breadth was weak: only 9 sampled liquid tickers produced parsed events, with duplicate share-class issuer exposure from GOOG/GOOGL and a largest ticker-level event share of about 20.8%. This is not a clear source-gate pass, so no market-data performance evaluation was run.

## Required safety flags

- `no_csv_used`: true
- `no_data_csv_argument_used`: true
- `no_daemon`: true
- `no_orders`: true
- `raw_daily_paths_retained`: false
