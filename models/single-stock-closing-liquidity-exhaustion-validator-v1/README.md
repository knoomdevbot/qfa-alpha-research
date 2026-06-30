# Single-stock closing-liquidity exhaustion validator v1 (AR-165)

Decision: **rejected**.

This validator tests whether AR-046/AR-056-style single-name closing-liquidity exhaustion survives expansion to a frozen broad liquid U.S. common-stock universe using qfa/Alpaca real daily OHLCV only. The daily bars provide abnormal full-day volume and close-location proxies, not true closing-auction imbalance.

Primary 10 bps random-window median Sharpe: `-4.3118`; p25: `-5.0465`; positive-window rate: `0.00%`; median annual turnover: `401.32`. Max relevant correlation: `0.3142`.

See `evaluations/latest.json` and `models/single-stock-closing-liquidity-exhaustion-validator-v1/evaluations/runs/ar165_realdata_20260630T171513Z.json` for compact reproducible handles.
