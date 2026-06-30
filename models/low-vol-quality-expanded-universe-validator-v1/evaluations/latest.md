# AR-164 latest evaluation

Run: `ar164_realdata_20260630T163134Z`  
Decision: **rejected**  
Data: qfa/Alpaca real daily bars, 2021-01-01 to 2026-06-29.

## Primary 10 bps result

| Metric | Value |
|---|---:|
| Sharpe | -0.870 |
| Annualized return | -9.81% |
| Annualized volatility | 11.15% |
| Max drawdown | -48.43% |
| Avg daily turnover | 0.0213 |
| Total return | -43.09% |

## Random windows at 10 bps

| Metric | Value |
|---|---:|
| Count | 80 |
| Median Sharpe | -0.981 |
| P25 Sharpe | -1.378 |
| Worst Sharpe | -2.561 |
| Positive-window rate | 7.5% |

## Falsifier controls

| Control | Sharpe / diagnostic |
|---|---:|
| SPY | 0.832 |
| Equal-weight selected universe | 0.929 |
| Sector equal-weight | 0.922 |
| USMV | 0.602 |
| SPLV | 0.522 |
| QUAL | 0.753 |
| Inverted rank, 10 bps | 0.774 |
| Shifted extra day, 10 bps | -0.876 |
| Original AR-010 basket, 10 bps | -0.328 |
| Random rank median, 10 bps | -0.572 |

## Acceptance gates

{
  "controls_do_not_dominate": false,
  "max_corr_le_0_60": false,
  "median_random_window_sharpe_gt_0": false,
  "p25_non_hostile": false,
  "positive_window_rate_ge_55pct": false
}

Rejected because median/p25 random-window Sharpe and positive-window rate were hostile, simple long-only controls dominated, correlation preference failed, and inverted ranks were positive. No direct low-vol-quality children spawned.

Root booleans: `no_csv_used=true`, `no_data_csv_argument_used=true`, `no_daemon=true`, `no_orders=true`, `raw_daily_paths_retained=false`.
