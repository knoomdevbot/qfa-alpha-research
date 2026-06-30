# AR-166 — ToM ETF Seasonality Expanded-Universe Validator

Validator artifact for `tom-etf-seasonality-expanded-universe-validator-v1`.

## Decision

**Rejected.** The frozen AR-021-style turn-of-month timing rule did not survive broad ETF universe validation.

- Primary 10 bps Sharpe: `-0.069250`
- Primary 10 bps total return: `-3.55%`
- Primary 20 bps Sharpe: `-0.438174`
- 50 random/stress windows: median Sharpe `-0.400729`, p25 `-0.560565`, positive-window rate `20.0%`
- Max absolute daily-return correlation to controls: `1.000000`

## Method

- Data: qfa/Alpaca real daily ETF market data only, configured paper/market-data access with values redacted.
- No CSV, no `--data-csv`, no daemon, no orders, no raw daily data retained.
- Candidate pool: 85 predeclared non-levered ETFs across broad U.S. equity, style/size, sectors, international/country, duration/Treasury, credit, inflation, real assets, commodities/metals/oil and FX proxies.
- Universe selection: ex-ante liquidity/coverage filters (history, missingness, median dollar volume, price floor) plus sleeve cap by liquidity only; 48 ETFs selected before scoring.
- Frozen rule: long equal-weight selected ETFs on first 4 and final 1 observed market sessions of each calendar month; flat otherwise.
- Costs: one-way 5/10/20 bps turnover haircuts, with 10 bps decision gate.

## Controls / falsifiers

SPY ToM, equal-weight selected universe, generic month-end, unconditional equal-weight exposure, shifted and random labels, original narrow basket, and ETF TSMOM/carry variants were evaluated. Controls and correlations did not support promotion.

See `evaluations/latest.json` for the compact machine-readable record and `evaluations/latest.md` for a human summary.
