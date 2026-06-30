# AR-157 macro-drawdown ETF allocator promotion/pruning validator

Research-only qfa model exposing `generate_signals(context)`.

Decision: **rejected**. Rejected/pruned: p25_random_sharpe_materially_negative; positive_window_rate_below_55pct; 20bps_cost_collapse; control_dominated_by_SPY_buy_hold_10bps,equal_weight_universe_10bps,etf_tsmom_126d_10bps,risk_off_switch_10bps; correlation_above_0p60

The model reconstructs AR-063-style stress allocation with OHLCV-only ETF state variables: drawdown, realized-volatility shock, credit/duration/gold/defensive relative moves, and recovery stabilization. It uses no fabricated macro-surprise series.

Evaluation artifacts: `evaluations/latest.json`, `evaluations/latest.md`, and `evaluations/runs/ar157_macro_drawdown_validator_20260630T010500Z.json`.
