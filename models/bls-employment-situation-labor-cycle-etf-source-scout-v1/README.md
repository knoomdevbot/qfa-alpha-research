# BLS Employment Situation labor-cycle ETF source scout v1

AR-174 was evaluated as a strict source/vintage-first scout. The result is a source-gate rejection, not a performance result.

## Decision

Rejected at source/vintage gate. The run could not reproducibly retrieve the required official BLS Employment Situation release calendar/archive pages from this environment; attempted official BLS URLs returned HTTP 403 Forbidden. Without official release-date/time and archived release-page proof, the allocator cannot be timestamp-safe.

## Vintage observations

A narrow ALFRED graph CSV smoke test was reachable for vintage date 2020-02-07 and observation month 2020-01-01:

| Component | Series | Smoke value |
|---|---:|---:|
| Nonfarm payrolls | PAYEMS | 152186 |
| Unemployment rate | UNRATE | 3.6 |
| Labor-force participation | CIVPART | 63.4 |
| Avg weekly hours, total private | AWHAETP | 34.3 |
| Avg hourly earnings, total private | CES0500000003 | 28.44 |

This was not enough to pass: ALFRED component vintages alone do not satisfy the issue requirement to prove official BLS release calendar/archive dates and complete first-vintage mapping before testing.

## Candidate product pool

XLY, XLI, IWM, QQQ, XLP, XLU, XLV, SPY, TLT, IEF, HYG, LQD, GLD, DBC.

No selected universe, raw bars, daily paths, CSVs, DBs, caches, daemon, orders, or performance metrics were produced. `model.py` emits zero weights for every candidate symbol.

## Evaluation artifacts

- Latest JSON: `evaluations/latest.json`
- Latest Markdown: `evaluations/latest.md`
- Immutable run JSON: `evaluations/runs/ar174_sourcegate_20260701T001413Z.json`
