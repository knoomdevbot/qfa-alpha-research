# AR-156 latest evaluation — ETF TSMOM expanded-universe validator

- Run: `ar156_expanded_etf_tsmom_validator_20260630T072808Z`
- Decision: **rejected**
- Data: real qfa/Alpaca daily bars via configured paper-data access; no CSV, no daemon, no orders.
- Selected universe: 45 ETFs — SPY, QQQ, IWM, DIA, MDY, RSP, VTI, VNQ, VEA, VWO, EFA, EEM, EWJ, EWG, EWU, EWZ, FXI, XLB, XLE, XLF, XLI, XLK, XLP, XLU, XLV, XLY, XLRE, TLT, IEF, SHY, SHV, AGG, LQD, HYG, TIP, MBB, GLD, SLV, USO, DBC, DBA, UUP, FXE, FXY, VIXY

## Primary 5 bps random-window metrics
- Windows: 50 x 252 trading days
- Median Sharpe: -0.611333
- P25 Sharpe: -0.896227
- Worst Sharpe: -2.211089
- Positive-window rate: 0.28
- Median annualized return / vol: -0.030165 / 0.046453
- Worst max drawdown: -0.118929
- Median annualized turnover: 12.67377

## Controls
- SPY_buy_hold_0bps: median Sharpe 0.699561, p25 0.170816, positive rate 0.8
- equal_weight_selected_0bps: median Sharpe 0.833491, p25 0.035875, positive rate 0.76
- price_only_tsmom_5bps: median Sharpe -0.4266, p25 -0.925103, positive rate 0.26
- narrow_AR015_style_tsmom_5bps: median Sharpe 0.034806, p25 -0.296298, positive rate 0.58
- inverted_primary_5bps: median Sharpe 0.330939, p25 -0.466017, positive rate 0.66
- shifted_weights_21d_5bps: median Sharpe -0.097898, p25 -0.476282, positive rate 0.42

## Gates
- median_sharpe_gt_0: False
- p25_sharpe_gt_0_or_not_materially_negative: False
- positive_window_rate_ge_55pct: False
- controls_do_not_dominate: False
- max_relevant_corr_le_0_60_when_available: True

## Warnings / limitations
- None

Artifacts: `/Users/moonk/qfa-alpha-research/models/etf-tsmom-expanded-universe-promotion-validator-v1/evaluations/runs/ar156_expanded_etf_tsmom_validator_20260630T072808Z.json`, `/Users/moonk/qfa-alpha-research/models/etf-tsmom-expanded-universe-promotion-validator-v1/evaluations/latest.json`
