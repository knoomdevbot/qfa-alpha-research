# AR-184 — Megacap Tech Pairs Residual Promotion/Pruning Validator

This model validates whether AR-005's mega-cap technology pair-residual mean-reversion idea survives a broader, predeclared common-stock universe and hostile controls.

## Design

- Primary universe: liquid U.S.-listed common-stock/ADR technology, communications, semiconductor, payment, platform, and adjacent mega-cap growth names selected before alpha-performance review by deterministic bar-history, liquidity, and economic-exposure filters.
- ETFs are excluded from the primary stock-pair validator; SPY/QQQ/XLK are only static benchmark controls.
- Pair/cluster membership is frozen by economic relatedness, not Sharpe, returns, cointegration p-values, or post-hoc performance.
- Signal: rolling 126-day log-price residual with 60-day residual z-score, 1.5 entry threshold, 5-day rebalance cadence, 8% per-name cap, and gross-normalized dollar-neutral-ish long/short weights.

## Evaluation

The durable evaluation artifacts use qfa/Alpaca real daily bars with compact scalar summaries only. No CSV data, raw daily bars, equity curves, daily return paths, weight tails, SQLite databases, caches, daemons, orders, or credential snippets are retained.

Required artifacts:

- `config.yaml`
- `metadata.yaml`
- `model.py`
- `evaluations/latest.json`
- `evaluations/latest.md`
- immutable run JSON/MD in `evaluations/runs/`
