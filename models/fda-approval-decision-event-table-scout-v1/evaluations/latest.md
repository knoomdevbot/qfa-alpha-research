# AR-180 FDA approval-decision event-table source scout

- **Run ID:** `ar180_source_gate_20260701T093534Z`
- **Decision:** `rejected_source_gate`
- **Performance:** not run; metrics null/unavailable
- **Model wrapper:** disabled zero-signal scaffold

## Official FDA source probe

| Source | Result |
|---|---:|
| Drugs@FDA data files page | HTTP 200; Last-Modified Tue, 30 Jun 2026 12:20:32 GMT |
| Drugs@FDA downloadable ZIP | HTTP 200; 6,036,440 bytes; Last-Modified Tue, 30 Jun 2026 12:05:39 GMT |
| Files parsed in memory | Applications, Submissions, Products, ApplicationDocs, lookup tables |

## Compact counts

| Diagnostic | Count |
|---|---:|
| Applications rows | 29,175 |
| Submissions rows | 192,793 |
| Products rows | 51,439 |
| ApplicationDocs rows | 80,370 |
| Original approved NDA/BLA candidates since 2015 | 1,533 |
| Candidate unique sponsors | 666 |
| Candidates with any application doc | 1,530 |
| Candidates with approval-letter-like doc | 1,510 |
| Manual conservative mapping probe events | 255 |
| Manual mapping probe unique tickers | 32 |

Top mapped probe tickers: PFE 41, ABBV 27, LLY 22, MRK 20, AMGN 19, GILD 17, VTRS 12, BMY 11, VRTX 8, BIIB 8.

## Gate result

Rejected despite apparent raw breadth. Drugs@FDA downloadable files are a current snapshot; `SubmissionStatusDate` and `ApplicationDocsDate` are decision/document dates but do not prove first public FDA web availability for each event. Approval letters are addressed to sponsors/applicants, so next-session trading from the letter date would rely on non-official assumptions about when the market could know. No qfa/Alpaca performance was run.
