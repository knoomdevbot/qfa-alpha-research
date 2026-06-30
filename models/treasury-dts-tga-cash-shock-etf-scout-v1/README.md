# Treasury DTS TGA cash-balance shock ETF scout v1

AR-170 source/vintage-first scout for an official Treasury FiscalData Daily Treasury Statement TGA cash-balance shock ETF allocator.

## Decision

**Rejected at source/vintage gate.** The official DTS endpoints were reachable and the table-I TGA line/schema spot check was stable enough for a parser, but the API rows checked did not expose the publication timestamp or immutable vintage identifier required to prove a non-lookahead `record_date` convention. No performance backtest was run and no performance metrics were invented.

## Model behavior

`model.py` exposes `generate_signals(context)` and returns zero weights for every requested symbol. This is intentional: the allocator is disabled until an official publication/vintage convention can be proven.

## Source diagnostics

- Official endpoint checked: FiscalData `accounting/dts/operating_cash_balance`.
- Official endpoint checked: FiscalData `accounting/dts/deposits_withdrawals_operating_cash`.
- Latest sampled `record_date`: 2026-06-26.
- Stable table-I TGA lines observed in the source check: opening balance, total deposits, total withdrawals, closing balance.
- Missing requirement: per-record publication timestamp / immutable vintage marker / official release-time proof.

## Artifacts

- `model.py` — zero-weight qfa scaffold.
- `config.yaml` — disabled-source-gate configuration.
- `metadata.yaml` — research metadata.
- `evaluations/latest.json` — compact source-gate result with required safety booleans.
- `evaluations/latest.md` — human-readable source-gate result.
- `evaluations/runs/ar170_source_gate_20260630T194244Z.json` — immutable compact run copy.

## Safety

No CSV market data, no `--data-csv`, no daemon, no orders, and no raw daily paths/bars/equity/weights/cache are retained.
