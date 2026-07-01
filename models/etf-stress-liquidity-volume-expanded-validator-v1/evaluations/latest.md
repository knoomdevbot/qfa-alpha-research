# AR-187 evaluation — ar187_qfa_alpaca_real_20260701T160459Z

Decision: **rejected**.

Data: qfa/Alpaca real daily OHLCV via configured paper-data/market-data access; no CSV, no `--data-csv`, no daemon, no orders, no raw daily paths retained.

Universe: 48 selected ETFs from 48 primary candidates; diagnostic symbols: VIXY. Leveraged/inverse/ETN examples were excluded from primary.

Primary 10 bps metrics: Sharpe 0.617269, annualized return 0.067363, max drawdown -0.184197, avg daily turnover 0.071320.

Random/stress windows (10 bps): median Sharpe 0.715928, p25 0.219917, worst -0.781526, positive-window rate 0.8200.

Cost sensitivity Sharpe: 5 bps 0.694856; 10 bps 0.617269; 20 bps 0.462319.

Controls: best control `spy_buy_hold` Sharpe 0.799378; controls dominate = True.

Correlation/orthogonality: max relevant absolute proxy/control correlation 0.927251; prior-library orthogonality limited because durable daily return streams are not consistently retained.

Falsifiers: controls_dominate, max_relevant_correlation_gt_0_60. No children spawned.
