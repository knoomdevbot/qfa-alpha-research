# AR-173 source-gate evaluation — ar173_source_gate_20260630T224939Z

Decision: **rejected_source_gate**.

The required source/vintage gate did not pass, so no ETF performance test was run and all performance metrics are null.

## Counts

| Check | Result |
|---|---:|
| Official BLS release/schedule/archive pages attempted | 3 |
| Official BLS pages returning HTTP 403 | 3 |
| BLS current API JOLTS series checked | 4 |
| BLS current API JOLTS series succeeded | 4 |
| ALFRED series checked | 4 |
| ALFRED series reachable | 4 |
| ALFRED rows per series | 306 |
| Verified historical vintage columns | 0 |

## Rationale

Accessible BLS API and ALFRED graph CSV data are useful for identifying current/revised JOLTS levels, but they do not satisfy the issue's timestamp-safety requirement. The unauthenticated ALFRED CSV downloads contained only a single current vintage column dated 2026-06-30 for each checked series. Official BLS release calendar/release/archive pages were blocked from this environment, preventing construction of an official historical release timestamp table.

## Trading outcome

`generate_signals(context)` is a zero-weight scaffold. No qfa/Alpaca market-data evaluation was run; no CSV market data, daemon, or orders were used.
