# fed-g17-industrial-production-capacity-etf-source-scout-v1

## Hypothesis

Timestamp-safe first-vintage Federal Reserve G.17 industrial production/capacity-utilization releases may contain ETF allocation information for production-cycle, cyclicals, inflation, duration, and credit sleeves.

## Signal Definition

`model.py` now exposes the fixed AR-182 release-event rule plus the official FRB dated `g17.txt` parser. The allocator uses only prior first-vintage release history:

- trailing 36-release z-scores of total industrial production MoM, manufacturing MoM, capacity-utilization change, and capacity-utilization level;
- fixed risk-on/risk-off/inflation ETF sleeves with gross exposure capped at 1.0;
- active only for five sessions after the next ETF session following the official 9:15 ET release; zero otherwise;
- no performance-optimized parameters, no CSV market data, no daemon, and no orders.

Candidate pool and selected universe: XLI, XLB, XLE, SPY, IWM, TLT, IEF, HYG, LQD, DBC, GLD. All were retained before performance because qfa/Alpaca returned continuous common daily-bar coverage from 2016-01-04 through 2026-06-30 and each is a liquid non-levered ETF with required economic exposure. Dropped symbols: none.

## Evaluation Summary

Real-data qfa/Alpaca daily-bar evaluation completed in `evaluations/runs/ar182_realdata_g17_etf_allocator_20260701T050000Z.json`; `evaluations/latest.json` and `evaluations/latest.md` point to the same run.

Decision: **rejected**.

Primary 10 bps one-way metrics:

- Full-sample Sharpe: -0.203554
- Annual return / volatility: -0.01155 / 0.05707
- Max drawdown: -0.212752
- Random-window median / p25 / worst Sharpe: -0.386432 / -0.463945 / -2.013603
- Positive random-window rate: 0.06
- Active events: 186 of 303 parsed official releases
- Event hit rate: 0.790323
- Average daily turnover: 0.057633

Controls dominated or did not rescue the idea: equal-weight ETF static Sharpe 0.565437, SPY static 0.798783, IWM static 0.534783, simple ETF TSMOM 0.181869, simple 5-day reversal -0.029116. Shifted/random/inverted label controls were also poor; rejection was decisive because the primary full-sample Sharpe was negative, random-window lower tail was materially negative, positive-window rate was far below 55%, and equal-weight static control dominated.

## Orthogonality / Redundancy

Deferred due rejection. The candidate failed performance and control gates before promotion, so full accepted/watchlist alpha-stream orthogonality was not required. Available daily controls show low correlations to static/TSMOM/reversal streams but poor standalone performance.

## Known Risks

- Public macro releases are well-followed and daily bars may miss intraday reaction.
- Alpaca returned common ETF coverage beginning 2016-01-04 for this credential/feed; older official G.17 releases were parsed but not all could be evaluated with retained common market coverage.
- The model is disabled/rejected for research queue purposes; do not place trades.

## Change Log

- 2026-07-01: Source/vintage gate scaffold created.
- 2026-07-01: Real-data qfa/Alpaca ETF evaluation completed; fixed-rule allocator rejected; no children spawned.
