# AR-166 ToM ETF expanded-universe validator

Decision: **rejected**.

Primary 10 bps Sharpe: -0.0692; total return -3.55%; max DD -16.08%.
Random/stress 50-window median Sharpe -0.4007, p25 -0.5606, worst -2.2834, positive rate 20.0%.
20 bps Sharpe -0.4382. Max abs corr to controls 1.0000.

Selected 48 ETFs: SPY, QQQ, IWM, IVV, VOO, DIA, RSP, VTI, IWF, VTV, IWD, VUG, QUAL, SPLV, MTUM, USMV, SMH, XLK, XLF, XLV, XLE, XLI, XLY, XLP, EEM, EFA, FXI, IEFA, EWZ, EWY, IEMG, VEA, LQD, HYG, TLT, SGOV, AGG, BIL, IEF, BND, GLD, SLV, IAU, USO, VNQ, UNG, PDBC, REET.

Acceptance tests: {"20bps_not_collapsed": false, "controls_not_dominant": false, "max_corr_le_0_60": false, "median_random_window_sharpe_gt_0": false, "p25_non_hostile": false, "positive_window_rate_ge_55pct": false}

Data: qfa/Alpaca real daily ETF data, no CSV, no --data-csv, no daemon, no orders; configured access values redacted. Raw daily paths retained: false.
