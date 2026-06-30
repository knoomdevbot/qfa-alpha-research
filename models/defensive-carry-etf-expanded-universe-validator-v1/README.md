# defensive-carry-etf-expanded-universe-validator-v1

## Hypothesis

AR-037/AR-049 ETF defensive-carry watchlist behavior may be stable and performant when audited on a broader ex-ante liquid ETF universe, but it must beat simple bond/equity/carry/TSMOM controls after realistic turnover costs.

## Signal Definition

Rule-based, long-only defensive/carry allocator over a predeclared ETF pool covering Treasury duration, TIPS, investment-grade/high-yield credit, broad equity/style/sector ETFs, gold/commodity, and FX/USD proxies. The model uses lagged daily close/return/volatility/drawdown features only and returns qfa-compatible weights via `generate_signals(context)`.

## Evaluation Summary

- Issue: AR-167
- Data: qfa/Alpaca real daily OHLCV; no CSV; no daemon; no orders.
- Period: 2019-01-02 to 2026-06-26.
- Random windows: 50 one-year windows.
- Primary cost: 10 bps one-way turnover.
- Decision: rejected.

Primary 10 bps result:

- Full-period Sharpe: -0.3463
- Annualized return: -1.70%
- Annualized volatility: 4.63%
- Max drawdown: -17.67%
- Mean daily one-way turnover: 5.30%

Random-window 10 bps result:

- Median Sharpe: -0.0729
- p25 Sharpe: -0.8206
- Worst-window Sharpe: -2.3759
- Positive-window rate: 46%

The validator failed the promotion gates: median random-window Sharpe was negative, positive-window rate was below 55%, 20 bps cost sensitivity collapsed further, and simple SPY/equal-weight controls dominated.

## Orthogonality / Redundancy

Maximum recorded relevant control correlation was below the 0.60 hard gate, but orthogonality did not rescue the result because performance and control-dominance gates failed.

## Known Risks / Limitations

- Static ETF availability can create survivorship bias.
- Parent/control streams are compact reconstructions/proxies where exact prior model return paths were not available.
- This is a promotion/pruning validator, not an optimized new alpha.
- Compact artifacts intentionally omit raw bars, equity curves, and weight tails.

## Change Log

- 2026-06-30: Initial real-data promotion/pruning evaluation; rejected.
