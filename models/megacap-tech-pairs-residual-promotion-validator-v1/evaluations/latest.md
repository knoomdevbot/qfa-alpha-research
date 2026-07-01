# AR-184 Real-data Validator Summary

- Created: 2026-07-01T13:46:28Z
- Decision: **rejected**
- Data: configured qfa/Alpaca real daily bars, no CSV, no daemon, no orders.
- Universe: 60 selected common-stock symbols from 71 candidates; ETFs excluded from primary validator.
- Frozen pairs: 196 economically related pairs across predeclared clusters.

## Headline metrics

Primary 10 bps full-period Sharpe: -0.186061

Random windows, 10 bps: median Sharpe -0.064667, p25 -0.387306, worst -1.627871, positive rate 0.48, median turnover 0.181053.

20 bps stress: median Sharpe -0.683501, p25 -1.034056.

## Controls

Higher full-period Sharpe controls: ar005_original_six_name_residual, random_non_economic_pairs_same_count, raw_5d_cross_sectional_reversal, spy_static_buy_hold, qqq_static_buy_hold, xlk_static_buy_hold, equal_weight_selected_common_stocks.
Max relevant correlation proxy: 0.988978.

## Decision rationale

median after-cost random-window Sharpe <= 0; p25 after-cost random-window Sharpe <= 0; 20 bps stress collapsed/nonpositive; controls with higher full-period Sharpe: ar005_original_six_name_residual, random_non_economic_pairs_same_count, raw_5d_cross_sectional_reversal, spy_static_buy_hold, qqq_static_buy_hold, xlk_static_buy_hold; max relevant correlation 0.989 > 0.60.

Artifacts retain compact scalar/count summaries only. Raw bars, daily return paths, equity curves, weight tails, SQLite DBs and caches were not retained.
