# AR-177 Evaluation — ar177_alpaca_real_20260701T062150Z

Decision: **reject**.

Primary 10 bps Sharpe -7.9358, ann return -0.3663, max DD -0.8688, avg daily turnover 1.6128.
Random windows (40 x 126 sessions): median Sharpe -7.7868, p25 -8.9344, worst -11.9416, positive rate 0.0.
Universe: 140/156 liquid common-stock candidates selected using ex-ante filters plus non-performance alphabetical cap; sector counts {'comm': 10, 'consumer_discretionary': 14, 'energy': 9, 'financials': 15, 'healthcare': 17, 'industrials': 15, 'materials': 10, 'real_estate': 9, 'staples': 13, 'tech': 19, 'utilities': 9}.
Controls at 10 bps: reversal1d Sharpe -4.0828, reversal5d -1.9454, no-cluster -7.4062, random-cluster -7.4794, inverted -6.2765, equal-weight 0.545.
Cost stress: {'5bps': {'sharpe': -4.3885, 'annualized_return': -0.2233, 'max_drawdown': -0.6754, 'avg_daily_turnover': 1.6128}, '10bps': {'sharpe': -7.9358, 'annualized_return': -0.3663, 'max_drawdown': -0.8688, 'avg_daily_turnover': 1.6128}, '20bps': {'sharpe': -15.0018, 'annualized_return': -0.5784, 'max_drawdown': -0.9786, 'avg_daily_turnover': 1.6128}}.

No CSV/data-csv/daemon/orders used; raw daily data not retained.

QFA CLI smoke: ok on 49 symbols, 2024-01-02..2025-03-31, temp DB removed; smoke verified qfa/Alpaca/model contract but returned zero performance due breadth/activation gates on the small subset.
