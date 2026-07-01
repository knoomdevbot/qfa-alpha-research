# AR-178 evaluation — etf-defensive-rotation-expanded-universe-validator-v1

Decision: **rejected**

Primary 10 bps random windows: median Sharpe 0.114596, p25 -0.306367, worst -1.56644, positive rate 0.555556 across 45 windows.

20 bps stress median Sharpe 0.068257 (p25 -0.350953). Full-period 10 bps Sharpe 0.427084, return 0.795979, max DD -0.307429.

Dominant controls: SPY, equal_weight_selected_universe, static_defensive_basket, static_risk_on_basket, risk_off_switch_spy_or_shy. Max retained artifact correlation: 0.647.

Selected universe (56): SPY, QQQ, IWM, MDY, RSP, VTI, IWF, IWD, MTUM, QUAL, USMV, SPLV, SCHD, XLK, XLY, XLF, XLI, XLB, XLE, XLV, XLP, XLU, XLRE, VNQ, SMH, IBB, KRE, XRT, XHB, IYT, EFA, EEM, EWJ, EWG, EWU, FXI, EWZ, EWC, EWA, SHY, IEF, TLT, BIL, SHV, TIP, LQD, HYG, AGG, MBB, EMB, GLD, IAU, SLV, DBC, USO, VIXY.

Reasons: 10bps p25 random-window Sharpe negative/hostile; controls dominate or match: SPY,equal_weight_selected_universe,static_defensive_basket,static_risk_on_basket,risk_off_switch_spy_or_shy; max artifact/control retained-stream correlation 0.65 exceeds 0.60.

Guardrails: no CSV, no --data-csv, no daemon, no orders, no raw daily paths retained.
