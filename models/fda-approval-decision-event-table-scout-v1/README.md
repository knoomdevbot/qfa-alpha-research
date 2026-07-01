# fda-approval-decision-event-table-scout-v1

AR-180 bounded source/vintage feasibility scout for an official FDA approval-decision event table.

## Decision

Rejected at source gate. No performance backtest was run and the model wrapper emits zero signals.

## What was probed

- Official FDA Drugs@FDA data files page: `https://www.fda.gov/drugs/drug-approvals-and-databases/drugsfda-data-files`
- Official FDA Drugs@FDA downloadable ZIP: `https://www.fda.gov/media/89850/download?attachment`
- Download observed 2026-07-01T09:35:34Z: 6,036,440-byte ZIP, HTTP 200, `Last-Modified: Tue, 30 Jun 2026 12:05:39 GMT`.
- Parsed compactly in memory only; no raw FDA tables, caches, databases, or daily price paths are retained.

## Findings

The official ZIP is broad and parseable: 29,175 applications, 192,793 submissions, 51,439 products, and 80,370 application-document rows. A simple source scout found 1,533 original approved NDA/BLA submissions since 2015 across 666 sponsors; 1,510 had approval-letter-like application documents. A conservative manual sponsor mapping probe found 255 events across 32 liquid U.S. ticker candidates, so raw breadth might be sufficient if timestamp safety were solved.

However, Drugs@FDA is a current downloadable snapshot. `SubmissionStatusDate` and `ApplicationDocsDate` record regulatory/document dates, not durable first-public web-posting timestamps. Approval letters evidence FDA decisions but are addressed to the applicant, so trading next regular session from letter/decision date would require a non-FDA assumption about public dissemination. The source gate therefore fails timestamp/vintage safety before any performance test.

## Operational flags

- `no_csv_used: true`
- `no_data_csv_argument_used: true`
- `no_daemon: true`
- `no_orders: true`
- `raw_daily_paths_retained: false`
