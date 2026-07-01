# BEA Personal Income and Outlays Consumer Impulse Source Scout v1

Issue AR-176 tested whether official BEA Personal Income and Outlays first-vintage release values can support a timestamp-safe ETF rotation signal.

## Decision

Rejected at the source/vintage gate. No qfa market-data evaluation was run.

## Source probe

A bounded official-source probe checked dated BEA Personal Income and Outlays pages for May releases in 2010, 2015, 2020, 2025, and 2026. All five pages were reachable and contained official 8:30 a.m. release/embargo language. Recent releases exposed XLSX artifacts that could be smoke-parsed as zipped Office workbooks. Legacy releases exposed PDF/TXT and binary XLS artifacts, but parser coverage for the full first-vintage component set was incomplete.

## Gate result

The gate required reproducible extraction of first-vintage personal income, disposable personal income, PCE, real PCE, saving rate, PCE price index, and core PCE values plus timestamps from official dated pages/artifacts. The probe extracted full or near-full coverage only for recent pages. Older pages did not yield all required components with the bounded parser and relied on legacy artifacts not handled by the current scaffold.

Because the source/vintage gate failed, the model emits zero weights and no ETF performance claims are made.

## Operational invariants

- no_csv_used: true
- no_data_csv_argument_used: true
- no_daemon: true
- no_orders: true
- raw_daily_paths_retained: false
