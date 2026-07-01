# closing-liquidity-exhaustion-single-stock-validator-v1

AR-185 promotion/pruning validator for the AR-028/045/046/056 liquidity-reversal watchlist family.

## Purpose
This is a validation/pruning study, not a newly optimized alpha. The frozen rule tests whether abnormal daily volume plus close-location / same-day move exhaustion in liquid U.S. common stocks creates a robust next-session reversal stream after costs and hostile controls.

## Frozen signal
- Score: `-(0.65 * 1d_return_z60 + 0.35 * 2 * close_location_centered) * max(volume_abnormal_z126, 0)`.
- Active only if volume abnormality is above 0.75 and either absolute return z-score exceeds 0.50 or absolute close-location exceeds 0.25.
- Cross-sectional demean, top/bottom quintile, 3% per-name cap, gross normalized.
- Daily close signal evaluated on next-session close-to-close returns.

## Universe and data
- 192 fixed ex-ante candidate symbols; 150 selected by coverage, price, and liquidity filters before scoring.
- Primary universe excludes identifiable ETFs/ETNs/funds/ADRs/preferreds/REITs where identifiable; SPY/QQQ are controls only.
- Data source: configured qfa/Alpaca real daily bars. No CSV input, no daemon, no orders, no raw bars retained.
- Limitation: current large/liquid common-stock candidate pool has survivorship and index-membership lookahead risk.

## Latest result
Decision: **rejected**.

At 10 bps primary cost, full-period Sharpe was -2.184598, max drawdown -0.880398, average turnover 1.311479/day. Random-window median Sharpe was -2.551807, p25 -2.853475, worst -3.547343, and positive-window rate 0% across 50 windows. The 20 bps stress Sharpe was -4.528473. Controls and buy-hold proxies dominated, and max relevant correlation to transient control streams was 0.999385.

See `evaluations/latest.json` and `evaluations/latest.md` for the compact evaluation record.
