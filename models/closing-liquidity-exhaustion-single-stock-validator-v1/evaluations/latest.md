# AR-185 real-data evaluation — ar185_real_alpaca_20260701T142849Z

- **Model:** `closing-liquidity-exhaustion-single-stock-validator-v1`
- **Type:** stress-test / promotion-pruning validator
- **Asset bucket:** equity
- **Decision:** rejected
- **Data:** configured qfa/Alpaca real daily OHLCV; no CSV, no daemon, no orders, no raw daily paths retained
- **Evaluation span:** 2020-01-02 to 2026-06-25; fetch span 2018-01-01 to 2026-06-26
- **Universe:** 192 fixed common-stock candidates; 150 selected by data coverage, 2019 median price >= $5, and 2019 median dollar volume >= $50mm before alpha scoring. Identifiable ETFs/ETNs/funds/ADRs/preferreds/REITs excluded where identifiable; SPY/QQQ used only as controls.

## Primary 10 bps gate

| metric | value |
|---|---:|
| Full-period Sharpe | -2.184598 |
| Annualized return | -0.269372 |
| Annualized volatility | 0.139140 |
| Total return | -0.868346 |
| Max drawdown | -0.880398 |
| Hit rate | 0.323096 |
| Average turnover | 1.311479 |
| Total turnover | 2135.087219 |

## Random windows at 10 bps

- Window count: 50
- Median Sharpe: -2.551807
- p25 Sharpe: -2.853475
- Worst Sharpe: -3.547343
- Positive-window rate: 0.000000

## Cost sensitivity

| cost | full-period Sharpe |
|---|---:|
| 5 bps diagnostic | -0.998602 |
| 10 bps primary | -2.184598 |
| 20 bps stress | -4.528473 |

## Controls

| control | Sharpe | comment |
|---|---:|---|
| generic reversal, 10 bps | -3.351805 | worse than candidate but not supportive |
| volume-only, 10 bps | -2.826613 | worse than candidate but highly correlated |
| close-location-only, 10 bps | -3.349745 | worse than candidate |
| shifted labels, 10 bps | -1.989050 | higher than candidate |
| random labels, 10 bps | -10.116975 | cost/turnover sanity check |
| equal-weight selected common stocks | 0.736548 | dominates candidate |
| SPY buy-hold | 0.737463 | dominates candidate |
| QQQ buy-hold | 0.877620 | dominates candidate |

## Orthogonality

No compact AR-046/AR-056 retained return streams were found in the repo search. Orthogonality was therefore computed against transient generic/control streams. Max relevant correlation was 0.999385, above the hard <=0.60 gate; volume-only correlation was 0.646853 and same-signal cost-variant correlations were near 1.0.

## Decision rationale

Rejected / prune. The candidate failed every hard promotion gate: median random-window Sharpe <= 0, p25 materially negative, positive-window rate below 55%, 20 bps stress collapsed, buy-hold/shifted controls dominated, turnover was high, and max relevant correlation breached 0.60.

## Warnings

- Daily OHLCV close-location is only a proxy for closing-auction liquidity exhaustion.
- Security-type filtering is manual/imperfect, though obvious ETF/fund/ADR/preferred/REIT names were excluded from the primary list where identifiable.
- Universe construction uses current large/liquid names, creating survivorship and membership-lookahead risk.
