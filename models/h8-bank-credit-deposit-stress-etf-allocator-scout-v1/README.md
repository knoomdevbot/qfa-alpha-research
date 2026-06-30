# H.8 bank credit/deposit stress ETF allocator scout (AR-160)

This is a disabled scaffold created by bounded recovery. The compact source/vintage gate passed, but no qfa/Alpaca real-market-data performance evaluation was run. `generate_signals` therefore returns `{}` and the configured model weight is zero.

## Source/vintage observations

- Federal Reserve H.8 release pages state the public lag: data are released each Friday generally at 4:15 p.m. ET, or Thursday generally at 4:15 p.m. ET when Friday is a federal holiday.
- Federal Reserve `releaseDates.json` exposes dated H.8 archive pages; sampled 20260626, 20260618, 20210108, and 20180316 archives contained the required Bank credit, Deposits, and Borrowings rows.
- ALFRED pages confirmed archival real-time revision availability for weekly H.8 bank credit (`TOTBKCR`) and weekly H.8 deposits (`DPSACBW027SBOG`).
- ALFRED confirmed archival real-time revision availability for monthly H.8 borrowings (`H8B3094NCBCMG`); the weekly borrowings row must be parsed from dated official H.8 archive pages if included in the real-data evaluator.

## Status

AR-160 remains queued with priority `source_gate_passed_needs_realdata_evaluation`. Before any completion/rejection/watchlist decision or nonzero weight, a durable qfa/Alpaca real daily market-data random-period evaluation with controls is required.

## Provenance

No CSV market data, daemon, orders, raw daily bar paths, equity paths, databases, credentials, or environment variable snippets are included in this artifact set.
