# ETF defensive-rotation expanded-universe validator v1 (AR-178)

This is a promotion/pruning validator for the AR-039/AR-051 ETF defensive-rotation family. It freezes the parent rule form and tests whether it survives a broader ETF universe, realistic costs, hostile controls, and redundancy gates.

## Rule

- Monthly calendar proxy: every in-month signal uses only data available before that calendar month.
- Score = blended 126/63 trading-day momentum divided by 63-day realized volatility.
- AR-051-style penalty subtracts 0.50 × trailing absolute correlation to simple TSMOM and carry/defensive proxy streams.
- Select risk-on sleeve only when risk-on median score beats defensive median and SPY blended momentum is positive; otherwise select defensive sleeve.
- Hold top 2 ETFs, inverse-vol scaled, gross normalized, max 50% per ETF.
- Evaluation shifts weights by at least one trading day and subtracts one-way turnover costs.

## Universe

Candidate pool contained broad U.S.-listed ETFs spanning equity sectors/styles/factors, Treasuries/TIPS/credit/cash, commodities/gold, volatility proxies, and international equity. Leveraged/inverse products were excluded. Selection was fixed before scoring by Alpaca bar coverage, history length, recent dollar-volume, and economic exposure diversity.

Selected 56-symbol universe:

`SPY, QQQ, IWM, MDY, RSP, VTI, IWF, IWD, MTUM, QUAL, USMV, SPLV, SCHD, XLK, XLY, XLF, XLI, XLB, XLE, XLV, XLP, XLU, XLRE, VNQ, SMH, IBB, KRE, XRT, XHB, IYT, EFA, EEM, EWJ, EWG, EWU, FXI, EWZ, EWC, EWA, SHY, IEF, TLT, BIL, SHV, TIP, LQD, HYG, AGG, MBB, EMB, GLD, IAU, SLV, DBC, USO, VIXY`.

## Result

Decision: **rejected / do not promote**.

Primary 10 bps random-window median Sharpe was positive (0.114596), but p25 was hostile (-0.306367), worst window was -1.566440, 20 bps positive-window rate fell to 0.533333, multiple controls dominated, and the max retained-stream correlation was 0.646579 versus the 0.60 hard gate.

## Artifacts

- `model.py` — qfa `generate_signals(context)` implementation.
- `config.yaml` — universe, frozen parameters, and gates.
- `metadata.yaml` — status and summary metadata.
- `evaluations/latest.json` / `latest.md` — compact real-data evaluation.
- `evaluations/runs/ar178_qfa_alpaca_real_20260701T071153Z.json/.md` — immutable compact run copy.

Guardrails: Alpaca real daily bars via qfa source/venv only; no CSV, no `--data-csv`, no daemon, no orders, no raw daily bars retained.
