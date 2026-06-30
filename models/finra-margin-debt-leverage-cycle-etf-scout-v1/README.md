# FINRA margin-debt leverage-cycle ETF scout v1

AR-155 tested whether monthly FINRA margin-debt and customer free-credit-balance changes can drive a conservative monthly ETF allocator after a timestamp-safe publication lag.

## Decision

**Rejected — fast falsification.** The official FINRA source was reachable and usable for a bounded scout, but the allocator did not survive hostile controls. The 5 bps post-cost primary Sharpe was positive (0.578) but below static SPY/equal controls, only marginally above ETF TSMOM, and worse than the inverted-signal and shifted-lag controls.

The model in `model.py` is intentionally disabled and returns `{}`.

## Source and lag

- Source: FINRA Margin Statistics webpage and linked Excel workbook.
- Source probe: 353 monthly rows from 1997-01 through 2026-05.
- FINRA page states updates are generally published during the third week of the month following the reference month.
- Evaluation lag: reference month assumed public on the **fourth Friday of the following month**; rebalance only at a month-end on/after that date.
- Caveat: no point-in-time FINRA vintage archive or exact historical publication timestamps were captured in this scout.

## Market data and universe

Market data came from configured qfa/Alpaca daily bars. No CSV market data or `--data-csv` was used. The full candidate pool was checked: SPY, IVV, VOO, QQQ, IWM, HYG, JNK, LQD, TLT, IEF, SHY, GLD, IAU, UUP, DBC, USO, XLP, XLU, XLV, XLF, XLK.

Selected universe: SPY, QQQ, IWM, HYG, LQD, TLT, IEF, SHY, GLD, UUP, DBC, XLP, XLU, XLV, XLF, XLK.

Exclusions: duplicate SPY/gold exposures (IVV, VOO, IAU), narrow oil-futures sleeve (USO), and shorter configured coverage for JNK versus the selected overlap.

## Key metrics

Evaluation window: 2016-03-31 to 2026-06-30, 124 monthly rebalance returns.

- Primary 5 bps: Sharpe 0.578, annual return 5.57%, max drawdown -23.57%.
- 10 bps stress: Sharpe 0.518, annual return 4.93%.
- 20 bps stress: Sharpe 0.398, annual return 3.65%.
- Random windows: median Sharpe 0.580, p25 Sharpe 0.395, positive Sharpe rate 95.0%.
- Controls: SPY Sharpe 0.919; equal-weight Sharpe 0.796; ETF TSMOM Sharpe 0.559; shifted-extra-lag Sharpe 0.843; inverted-signal Sharpe 0.679.

## Artifacts

- Latest compact JSON: `evaluations/latest.json`
- Immutable run JSON: `evaluations/runs/ar155_finra_margin_debt_scout_20260630T064315Z.json`
- Latest markdown: `evaluations/latest.md`
