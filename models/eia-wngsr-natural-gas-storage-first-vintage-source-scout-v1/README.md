# EIA WNGSR Natural Gas Storage First-Vintage Source Scout v1

AR-192 tests whether official EIA Weekly Natural Gas Storage Report first-public storage vintages can support a timestamp-safe ETF allocation signal after the Thursday 10:30 ET-ish public release.

## Current decision

- Status: `hold`
- Decision: `hold_realdata_blocked_no_alpaca_credentials`
- Latest run: `ar192_hold_no_alpaca_credentials_20260701T225012Z`
- Asset bucket: ETF
- Crypto label: false

The official source/vintage gate previously passed: dated EIA Natural Gas Weekly Update archive pages contain release dates, total working-gas storage levels, and weekly net changes. The required qfa/Alpaca real ETF performance evaluation is not complete because this scheduled runtime had no usable Alpaca authentication configured and no Alpaca ETF bars could be retrieved.

## Model behavior

`model.py` defines a qfa-compatible `generate_signals(context)` function that accepts `AlphaContext` objects. It emits zero weights unless the evaluator provides an explicit timestamp-safe metadata field named `eia_wngsr_storage_surprise_z`. This prevents deployment of an unevaluated alpha in normal daemon contexts.

## Future real-data evaluation requirements

Use qfa/Alpaca ETF daily bars only; do not use CSV-backed market data. Select from a broad non-levered/non-inverse universe by Alpaca availability, history, liquidity, and economic exposure: natural gas (UNG, UNL), energy/oil/gas proxies (XLE, XOP, FCG, DBE, USO), pipelines/MLPs/utilities (AMLP, XLU, VPU), commodity baskets and risk controls (DBC, PDBC, GSG, SPY, TLT, IEF, SHY). BOIL, KOLD, and UGA are diagnostics-only.

Evaluate with 5/10/20 bps costs, random/stress windows, turnover, Sharpe distribution, max drawdown, and controls including SPY, equal-weight selected universe, and a trend-only or release-calendar placebo.

## Safety flags

- no_csv_used: true
- no_data_csv_argument_used: true
- no_daemon: true
- no_orders: true
- raw_daily_paths_retained: false
