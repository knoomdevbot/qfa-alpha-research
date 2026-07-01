# fed-sloos-credit-tightening-etf-source-scout-v1

AR-175 source/vintage-first scout for a possible Federal Reserve SLOOS credit-tightening ETF allocator.

## Decision

Rejected at the source/vintage gate. No market-data performance test was run and the qfa scaffold returns zero weights.

## Source finding

Official Federal Reserve SLOOS pages were reachable from the research environment. The landing page listed dated survey pages from April 2017 through April 2026, and recent dated pages linked Table 1, Table 2, Chart Data, and PDFs. The dated HTML pages expose `Last Update` dates and parser-readable chart-data tables with lending-standards/demand diffusion rows.

However, the issue required proof of official release dates **and times** and vintage-safe first-vintage component values from dated Federal Reserve pages before any ETF performance work. The inspected dated SLOOS pages did not expose an official historical release-time field; the RSS/DDP feed contains timestamped DDP notices/corrections but not the required per-survey release timestamps. The dated chart-data pages are useful evidence but were not sufficient to prove immutable first-vintage values rather than mutable/current release-page content. Current FRED/DDP-only history was explicitly not acceptable.

## Candidate pool

XLF, KRE, HYG, LQD, IWM, SPY, XLP, TLT, IEF. No selected universe because the gate failed.

## Safety

No CSV market data, no daemon, no orders, and no raw daily bars retained.
