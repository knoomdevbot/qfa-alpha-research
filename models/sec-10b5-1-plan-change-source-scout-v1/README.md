# SEC 10b5-1 plan-change source scout v1

Issue: AR-161  
Decision: **rejected at source gate**

This folder contains only compact source-gate artifacts for a bounded recovery micro-scout. It does not contain raw SEC filing text, CSV market data, daemon output, or order/trading artifacts.

## Source-gate result

A deterministic bounded SEC probe inspected official issuer 10-Q/10-K filings for Regulation S-K Item 408 / Rule 10b5-1 trading-arrangement adoption, modification, and termination disclosures.

Key result: the probe found 10b5-1/Item 408 text, but the conservative mapped liquid event count did **not** clear the required gate of 150 events within the 120-filing budget. The apparent hit set was concentrated in a small number of mega-cap issuers and included duplicate-class issuer exposure, so it was not strong enough to justify market-data performance testing.

## Metrics

- Sampled liquid issuers before filing cap: 10
- SEC filings inspected: 120
- Candidate 10b5-1 text hits: 111
- Item 408 context hits: 71
- Parsed valid plan-change event estimate: 130
- Mapped liquid event estimate: 130
- Gate requirement: 150
- Issuers with valid parsed events: 9
- Max issuer event share: 20.8%
- Forms inspected: 89 10-Q, 31 10-K
- No market-data performance run.

## Safety flags

- `no_csv_used`: true
- `no_data_csv_argument_used`: true
- `no_daemon`: true
- `no_orders`: true
- `raw_daily_paths_retained`: false

The model wrapper is intentionally zero-weight: `generate_signals(context)` returns `{}`.
