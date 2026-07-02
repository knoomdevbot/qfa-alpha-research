# AR-193 — Turn-of-month ETF expanded-universe validator v1

Frozen validation wrapper for AR-006/AR-021. The model is long-only and equal-weight across the ex-ante selected ETF universe during the final 1 observed market session and first 4 observed market sessions of each month, and flat otherwise.

## Decision

**Rejected / pruned.** The expanded-universe validator did not pass the promotion gates. No direct turn-of-month child/refinement was spawned.

Key failed gates:

- random/stress p25 Sharpe materially negative
- 20 bps sensitivity collapses nonpositive
- max relevant correlation 0.876 vs generic_month_start exceeds 0.60
- control dominates full Sharpe: spy_buy_hold_10bps_entry
- control dominates full Sharpe: equal_weight_buy_hold_10bps_entry
- sleeve contribution concentration above 35%


## Real-data evaluation

- Data: real daily market bars through qfa AlpacaGateway using configured paper-data access; no CSV; no `--data-csv`.
- Period: 2014-01-02 to 2026-06-30 (2635 common next-bar return sessions).
- Universe: 48 selected ETFs from the issue candidate pool; VIXY diagnostic-only and excluded.
- Primary cost: 10 bps per gross exposure state turnover; sensitivities at 5 and 20 bps.
- Random/stress windows: 50 random + 4 stress windows.

## Primary metrics (10 bps)

- Sharpe: 0.258
- Annualized return: 1.672%
- Annualized volatility: 7.494%
- Max drawdown: -18.760%
- Activation rate: 23.909%
- Annualized turnover proxy: 24.196

## Robustness summary

- Random/stress median Sharpe: 0.110
- Random/stress p25 Sharpe: -0.317
- Worst window Sharpe: -1.606
- Positive-window rate: 55.6%
- 20 bps Sharpe: -0.065; 20 bps annualized return: -0.762%
- Max relevant correlation: 0.876 vs generic_month_start

## Artifacts

- `evaluations/latest.json`
- `evaluations/runs/ar193_alpaca_real_20260702T015230Z.json`
- `evaluations/latest.md`

Raw bars, daily returns, equity curves, helper scripts, caches, DBs, and credentials were not retained.
