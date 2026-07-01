# AR-179 SEC buyback authorization event-table scout

Decision: **rejected_source_gate**.

A hard-capped official SEC EDGAR micro-scout checked `company_tickers.json`, 12 issuer submissions (including AAPL, NFLX, SNDK), and 30 recent 8-K/10-Q/10-K-related filing documents/exhibits with request timeouts capped at 10 seconds.

The probe verified that official SEC documents are reachable and that obvious examples exist, including AAPL additional $100B, NFLX additional $25B, SNDK $6B, and NVDA additional $80B authorization language. However, a compact audit also showed the bounded keyword parser still catches routine or stale 10-Q capacity/history language, duplicate primary/exhibit filings, and non-event boilerplate. This is not enough to claim a durable timestamp-safe event table.

Source-gate counts:

- docs_scanned: 30
- candidate_hits: 10
- confirmed_events_sample: 4
- mapped_liquid_events: 4
- parser_precision_sample: 0.4

No qfa/Alpaca performance was run. The model scaffold returns no signals.

Rejection reason: no durable broad parser/event table >=150 conservatively mapped liquid authorization/increase events; source reachability and samples are insufficient for acceptance/performance.
