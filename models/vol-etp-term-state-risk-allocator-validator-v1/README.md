# AR-168 — Vol-ETP term-state risk allocator validator

Decision: **Rejected**.

This folder contains the durable qfa-compatible model and compact real-data evaluation artifacts for `vol-etp-term-state-risk-allocator-validator-v1`.

## Files

- `model.py` — exposes `generate_signals(context)` and uses only completed daily OHLCV prices supplied by qfa/Alpaca.
- `config.yaml` — frozen predeclared universe, feature, cost, and gate settings.
- `metadata.yaml` — issue and artifact metadata.
- `evaluations/latest.json` / `latest.md` — compact latest real-data evaluation.
- `evaluations/runs/*.json` — immutable compact run payload.

## Rule summary

The validator uses public volatility ETP closes as proxies, not true VIX futures or options data. Inputs are VIXY, VXX, VXZ, and SVXY. The model checks 20-day changes in the VIXY/VXZ ratio plus VIXY, VXZ, VXX, and SVXY trends. When short-end volatility ETP pressure is easing and inverse-vol appetite is positive, it allocates equally to a predeclared risk sleeve. Otherwise it uses a predeclared defensive sleeve of TLT, IEF, GLD, UUP, and SHY.

Evaluation used weekly Friday-close rebalancing with weights shifted one trading day and 5/10/20 bps one-way turnover cost haircuts.

## Result

Alpaca real daily OHLCV common history ran from 2018-01-18 through 2026-06-29. CSV market data, `--data-csv`, daemons, and orders were not used; raw daily paths were not retained.

At 10 bps one-way cost the model had Sharpe 0.182, annualized return 1.44%, annualized volatility 11.51%, and max drawdown -33.02%. Random-window median Sharpe was positive (0.225) and positive-window rate was 61.7%, but p25 Sharpe was hostile at -0.424. The simple SPY control dominated with Sharpe 0.705, and the model's correlation to a simple VIXY/TLT stress control was 0.830, breaching the hard 0.60 correlation cap.

The issue is therefore rejected as mostly a stress-beta allocator, not a robust orthogonal volatility-term-state alpha.
