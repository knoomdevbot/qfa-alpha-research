# AR-187 — ETF stress-liquidity-volume expanded validator

Terminal promotion/pruning validator for AR-043 (`etf-stress-liquidity-volume-v1`). The model freezes the AR-043-like daily OHLCV stress rule and applies it to a broad ETF universe rather than the original narrow watchlist.

## Rule

- Inputs: completed daily OHLCV bars only.
- Stress features: abnormal high-low range, abnormal dollar volume, poor close-location value, and cross-ETF stress breadth.
- Allocation: long-only blend between risk and defensive ETF sleeves; daily close signal shifted one trading day in evaluation.
- Parameter policy: no optimization; frozen windows and caps inherited from AR-043-like logic with expanded-universe cap adjustment.

## Universe

The candidate pool starts broad ex ante: U.S.-listed liquid ETFs across broad equity, sectors, styles/factors, duration/credit, commodities, real assets, and FX proxies where qfa/Alpaca bars exist. Leveraged/inverse products and ETNs are excluded from primary; VIXY is diagnostic/control only.

Selected primary universe: 48 ETFs (`SPY`, `QQQ`, `IWM`, `DIA`, `VTI`, `MDY`, `IJR`, `EFA`, `EEM`, `EWJ`, `EWZ`, `FXI`, sectors, style/factor ETFs, bond/credit ETFs, commodity/real-asset ETFs, and FX proxies). Selection used data availability and exposure coverage, not performance.

## Evaluation

- Data: qfa/Alpaca real daily OHLCV via configured paper-data / market-data access.
- No CSV, no `--data-csv`, no daemon, no orders, no raw bars retained.
- Primary cost: 10 bps one-way turnover cost.
- Cost sensitivity: 5 and 20 bps.
- Random/stress protocol: 40 seeded random one-year windows and 10 stress windows.
- Controls: SPY buy-hold, equal-weight selected universe, ETF TSMOM, ETF short-term reversal, generic risk-off proxy, VIXY/TLT proxy.

## Result

Decision: **rejected**.

The lower-tail random/stress distribution was positive, but hard gates failed because simple controls dominated and max relevant proxy/control correlation was far above 0.60.

Key 10 bps metrics:

- Full-period Sharpe: `0.617269`
- Median random/stress-window Sharpe: `0.715928`
- p25 random/stress-window Sharpe: `0.219917`
- Worst-window Sharpe: `-0.781526`
- Positive-window rate: `0.8200`
- Max drawdown: `-0.184197`
- Average daily turnover: `0.071320`
- Best control: `spy_buy_hold`, Sharpe `0.799378`
- Max relevant absolute correlation: `0.927251` versus equal-weight selected universe

No children spawned.
