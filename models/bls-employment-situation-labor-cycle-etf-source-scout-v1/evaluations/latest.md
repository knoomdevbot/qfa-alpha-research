# AR-174 source/vintage scout result

- Decision: rejected
- Stage: source/vintage gate
- Run ID: `ar174_sourcegate_20260701T001413Z`
- Market performance run: no
- CSV market data used: no
- Daemon/orders: no/no

## Finding
The source/vintage gate failed. Official BLS Employment Situation release calendar and archived release pages were required to prove timestamp-safe release dates/times before any ETF performance test. The attempted official BLS pages returned HTTP 403 Forbidden from this execution environment, including browser-like header retries, so the official release calendar/archive evidence was not reproducibly verified in-run.

ALFRED graph CSV was reachable for a one-date vintage smoke test across PAYEMS, UNRATE, CIVPART, AWHAETP, and CES0500000003 on vintage date 2020-02-07, but that does not by itself satisfy the issue requirement for official BLS release calendar/archive proof and complete first-vintage mapping.

## Candidate pool and universe
Candidate pool retained for record only: XLY, XLI, IWM, QQQ, XLP, XLU, XLV, SPY, TLT, IEF, HYG, LQD, GLD, DBC. No selected universe or weights were produced because the source gate failed.

## Metrics
Performance metrics are null by design. No qfa/Alpaca OHLCV evaluation was run.
