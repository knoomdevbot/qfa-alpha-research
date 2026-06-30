# H.8 bank credit/deposit stress ETF allocator scout v1

AR-160 evaluated the hypothesis that point-in-time Federal Reserve H.8 bank credit, deposit, and borrowing impulses forecast ETF rotation after the official public release timestamp.

## Decision

**rejected** after qfa/Alpaca real daily ETF evaluation (`ar160_qfa_alpaca_real_20260630T122402Z`). The model remains disabled (`generate_signals` returns zero weights).

See `evaluations/latest.json` and `evaluations/latest.md` for metrics, controls, random windows, and required provenance flags.

## Provenance

- Macro source: official Federal Reserve H.8 dated release pages, with first tradable ETF session after the 4:15 p.m. ET release timestamp.
- Market source: qfa `AlpacaGateway.get_bars` real daily bars for the selected ETF universe.
- No CSV, no `--data-csv`, no daemon, no orders; raw daily paths were not retained.
