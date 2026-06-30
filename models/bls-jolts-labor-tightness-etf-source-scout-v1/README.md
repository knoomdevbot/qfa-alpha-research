# AR-173 — BLS JOLTS labor-tightness ETF source scout

## Decision
Rejected at source/vintage gate. The allocator is a zero-weight scaffold and no market-data performance was run.

## Source checks
- Official BLS JOLTS schedule/release/archive pages attempted from this environment returned HTTP 403, so a durable official historical release-date/time table could not be established.
- BLS public API returned current JOLTS observations for job openings, hires, quits, and layoffs/discharges for 2024-2026, but those values are not accepted as historical vintages.
- Unauthenticated ALFRED graph CSV downloads were reachable for JTSJOL, JTSHIL, JTSQUR, and JTSLDL with 306 monthly rows each, but the downloaded files contained a single current vintage column dated 2026-06-30. A multi-vintage historical panel was not verified without API-keyed endpoints.
- Because the release timestamp and point-in-time value gates both did not pass, qfa/Alpaca daily ETF evaluation was intentionally skipped.

## Model behavior
`model.py` exposes `generate_signals(context)` and returns empty weights with rejection metadata. This prevents accidental use of revised JOLTS levels as a backtest signal.

## Required invariants
- no CSV market data used
- no data CSV argument used
- no daemon
- no orders
- no raw daily paths retained
