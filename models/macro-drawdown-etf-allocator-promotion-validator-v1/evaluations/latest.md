# AR-157 Evaluation — macro-drawdown ETF allocator validator

Decision: **rejected**

Rejected/pruned: p25_random_sharpe_materially_negative; positive_window_rate_below_55pct; 20bps_cost_collapse; control_dominated_by_SPY_buy_hold_10bps,equal_weight_universe_10bps,etf_tsmom_126d_10bps,risk_off_switch_10bps; correlation_above_0p60

## Key metrics
- Random windows: 50 two-year windows from 2018-2026 with warmup.
- Primary 10 bps Sharpe: `0.003938`; ann return `0.000291`; ann vol `0.073934`; max drawdown `-0.293758`.
- Random 10 bps median/mean/p25/worst Sharpe: `0.001216` / `-0.204164` / `-1.232636` / `-1.740066`.
- Positive-window rate: `0.5`; median daily turnover `0.208683`; median activation `1.0`; median hit rate `0.521782`.
- 20 bps median Sharpe: `-0.726011`.
- Max absolute correlation vs controls/retained compact curves: `0.859317`.

## Controls
SPY, equal-weight universe, ETF TSMOM, ETF reversal, risk-off switch, shifted signal, date-only placebo, and inverted signal were evaluated at 10 bps. Control domination was: `True`.

## Data and policy
Real daily OHLCV bars were fetched as provider JSON into memory; no CSV input, no `--data-csv`, no daemon, no orders, and no raw market data were retained. Configured paper-data access through the preferred qfa/Alpaca path was unavailable in this scheduled run, so the validator used the JSON fallback and documented that limitation.
