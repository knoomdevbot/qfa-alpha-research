# AR-191 source gate — rejected

Run: `ar191_source_gate_20260701T193819Z`  
Completed: 2026-07-01T19:38:19Z

Decision: `rejected_source_gate`.

A hard-capped SEC metadata micro-scout probed `company_tickers.json` plus 30 fixed large/liquid company-submission JSON files. SEC metadata was reachable, but the scout did **not** build a durable class-separated event parser/table.

Counts from the bounded metadata probe:

- company tickers rows: 10,426
- company-submission probes: 30 / 30 successful
- recent 8-K rows seen: 2,435
- Item 1.01 8-K metadata rows: 111
- Item 2.01 8-K metadata rows: 16
- Item 1.01-or-2.01 candidate metadata rows: 121
- accepted durable event-table rows: 0
- mapped liquid common-stock events: 0

Rejection reason: metadata reachability is adequate, but no parser/event table satisfying the gates was produced: >=150 mapped liquid events overall, >=75 per primary class, >=75 issuers, concentration limits, audited precision, and dropped-event logs.

No CSV market data, daemon, orders, raw bars, or performance backtest were used.
