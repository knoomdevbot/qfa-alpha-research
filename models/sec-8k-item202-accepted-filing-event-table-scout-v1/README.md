# sec-8k-item202-accepted-filing-event-table-scout-v1

AR-171 bounded feasibility scout for SEC 8-K Item 2.02 accepted-filing event tables.

## Decision

**Source gate passed, but no performance evaluation was run.** The model is a disabled, zero-weight scaffold and must not be accepted/watchlisted until a durable parser/event table plus timestamp-safe qfa/Alpaca real-data performance evaluator are completed.

## Key source-gate metrics

- SEC company ticker mapping reachable: `True` (10433 rows).
- Sample: first 500 current SEC exchange ticker rows after simple common-like filters.
- SEC submissions fetched: 500/500.
- Recent 8-K rows observed: 41345.
- Item 2.02 8-K accepted events with timestamp/accession: 13088.
- Mapped issuers with Item 2.02 events: 375.
- Accession and primary-document proof counts: 13088 / 13088.
- Filing archive index probe: 40/40 reachable.
- Exhibit-99 or press-release-like attachment names found: 16/40.
- qfa/Alpaca coverage probe: 119/120 symbols had daily bars (99.17%); compact counts retained only.
- Concentration: top issuer share 0.79%; top 10 issuer share 6.21%.

## Warnings

- Current SEC ticker mapping is not a historical common-stock security master; production work must handle ticker changes, share classes, ADRs, funds, warrants, preferreds, and issuer/security ambiguity more conservatively.
- Attachment discovery is incomplete. Several issuers embed Item 2.02 earnings content in the primary inline document rather than a separate Exhibit 99, so a robust parser is still required.
- No raw SEC cache, raw bars, SQLite database, daily equity path, order, daemon, or CSV market data is retained in this artifact.
