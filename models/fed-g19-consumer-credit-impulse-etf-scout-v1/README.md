# fed-g19-consumer-credit-impulse-etf-scout-v1

Zero-weight recovery micro-scout artifact for AR-162.

## Decision

Rejected at source/vintage gate for this bounded recovery pass. The official Federal Reserve G.19 dated-release archive is reachable and contains enough dated releases to make a future parser plausible, but this pass did not produce a durable cross-vintage parser, retained event table, qfa/Alpaca ETF evaluator, or performance result.

## Source findings

- `https://www.federalreserve.gov/releases/g19/releaseDates.json` returned 361 dated releases across 31 years, from `19960611` through `20260605`.
- Sampled release URLs: `20260605`, `20241206`, `20201207`, `20101207`, `20001207`.
- 2026/2024/2020 samples exposed three semantic HTML tables: Consumer Credit Outstanding, Levels, and Flows.
- 2010/2000 samples were reachable but used fixed-width `<pre>` text with no semantic table titles, although revolving/nonrevolving/outstanding text was present.

## No alpha conclusion

No market-data backtest was attempted. No CSV market data, daemon, orders, or raw daily paths were used or retained. This artifact emits zero weights only.
