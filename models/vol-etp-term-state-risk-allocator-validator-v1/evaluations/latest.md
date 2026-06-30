# AR-168 Evaluation — Vol-ETP term-state risk allocator validator

Decision: **REJECTED**

Data: Alpaca real daily OHLCV through qfa `AlpacaGateway`; no CSV market data, no `--data-csv`, no daemon, no orders. Common-history span: 2018-01-18 to 2026-06-29 (2122 trading days). Raw daily paths were not retained.

## Predeclared model
Weekly Friday-close rebalance, weights shifted one trading day. Lagged close-based 20-day term-state features from VIXY, VXX, VXZ, and SVXY choose either an equal-weight risk ETF sleeve (SPY, QQQ, IWM, EFA, EEM, XLF, XLE, XLK, HYG, LQD, DBC) or a defensive sleeve (TLT/IEF/GLD/UUP/SHY).

## Primary 10 bps one-way cost metrics
- Annualized return: 1.44%
- Annualized volatility: 11.51%
- Sharpe: 0.182
- Max drawdown: -33.02%
- Risk-on rate: 55.47%
- Annualized turnover: 21.49x

## Random-window robustness at 10 bps
- Windows: 60
- Median Sharpe: 0.225
- P25 Sharpe: -0.424
- Worst Sharpe: -1.775
- Positive-window rate: 61.7%

## Cost sensitivity
- 5 bps Sharpe: 0.276
- 10 bps Sharpe: 0.182
- 20 bps Sharpe: -0.005

## Hostile controls at 10 bps
- spy: Sharpe 0.705, annualized return 12.29%, corr to model 0.354
- equal_weight: Sharpe 0.568, annualized return 6.08%, corr to model 0.516
- tlt: Sharpe -0.188, annualized return -4.04%, corr to model 0.344
- vixy_tlt_stress: Sharpe 0.244, annualized return 2.39%, corr to model 0.830
- etf_tsmom: Sharpe 0.343, annualized return 3.19%, corr to model 0.528

Max relevant absolute correlation: 0.830. Best control: spy Sharpe 0.705.

## Limitations / falsification notes
- Volatility ETP common history is short and survivorship/issuer-product-definition biased.
- ETP proxies are not true VIX futures curve, implied volatility, or variance-risk-premium data.
- Orthogonality to prior alpha library is approximated with reconstructable controls because durable prior daily return paths are not retained.

## Warnings
- max relevant correlation exceeds 0.60
- model does not beat all simple controls
- p25 random-window Sharpe is negative/hostile
