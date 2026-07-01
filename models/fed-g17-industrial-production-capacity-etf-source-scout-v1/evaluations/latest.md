# AR-182 real-data evaluation — Federal Reserve G.17 ETF allocator

- Run ID: `ar182_realdata_g17_etf_allocator_20260701T050000Z`
- Completed: 2026-07-01T12:03:13Z
- Decision: **rejected**
- Market data: qfa `AlpacaGateway.get_bars` real daily ETF bars; no CSV/`--data-csv`; no daemon; no orders.
- Universe: selected all candidates XLI, XLB, XLE, SPY, IWM, TLT, IEF, HYG, LQD, DBC, GLD after pre-performance coverage/economic-exposure checks; dropped: none. qfa/Alpaca common daily-bar evaluation span is 2016-01-04 through 2026-06-30.

## Primary metrics (10 bps one-way)

- Full-sample Sharpe: -0.203554
- Annual return / vol: -0.01155 / 0.05707
- Max drawdown: -0.212752
- Random-window median / p25 / worst Sharpe: -0.386432 / -0.463945 / -2.013603
- Positive random-window rate: 0.06
- Events total / active: 303 / 186
- Event hit rate: 0.790323
- Activation rate: 0.144158
- Avg daily turnover: 0.057633

## Controls

- Equal-weight static Sharpe: 0.565437
- SPY / IWM static Sharpe: 0.798783 / 0.534783
- ETF TSMOM / reversal Sharpe: 0.181869 / -0.029116
- Shifted / random / inverted labels Sharpe: -0.358338 / -0.316701 / -0.308896

## Decision rationale

- primary 10bps full-sample Sharpe not positive
- lower-tail random-window Sharpe materially negative
- positive random-window rate below 55%
- does not beat equal-weight ETF static control

Orthogonality vs accepted/watchlist alphas: deferred_due_rejection; rejected before promotion because lower-tail/random-window and control gates failed
