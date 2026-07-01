# ICE/BofA credit-spread first-vintage ETF allocator source scout v1

AR-188 tested whether official ICE/BofA option-adjusted credit-spread series
could support a timestamp-safe ETF risk-rotation allocator using first-vintage
history.

## Decision

**Rejected at source gate.** The model is disabled and `generate_signals` returns
zero weights.

## Source evidence

Representative public ICE/BofA OAS series were checked on FRED/ALFRED:

- `BAMLH0A0HYM2` — ICE BofA US High Yield Index OAS
- `BAMLC0A0CM` — ICE BofA US Corporate Index OAS
- `BAMLC0A4CBBB` — ICE BofA BBB US Corporate Index OAS
- `BAMLH0A1HYBB` — ICE BofA BB US High Yield Index OAS

The public graph CSVs and ALFRED page descriptions showed only a 2023-07-03 to
2026-06-30 public window for the representative series. That is not enough to
validate an ETF allocator across credit cycles or random windows, and it does
not prove durable first-vintage availability. Public FRED pages also identify
Ice Data Indices, LLC as the source/release owner and tag the series as
copyrighted/pre-approval required, so no direct licensed history was assumed or
stored.

## Evaluation

No market-data performance evaluator was run. This scout intentionally stopped
before ETF backtesting because the source/vintage gate failed.

Artifacts:

- `model.py` — disabled zero-weight qfa scaffold exposing `generate_signals`.
- `config.yaml` and `metadata.yaml` — model/source-gate metadata.
- `evaluations/latest.json` and `.md` — source-gate rejection record.
- `evaluations/runs/ar188_source_gate_20260701T164407Z.json` and `.md` — immutable run record.

No CSV-backed market data, daemon, orders, raw daily paths, DBs, caches, or raw
bars were used or retained.
