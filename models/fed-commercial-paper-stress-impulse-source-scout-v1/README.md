# AR-189 — Federal Reserve commercial-paper stress impulse ETF source/vintage scout

Status: **rejected_source_gate**. This is a disabled zero-weight scaffold; no alpha or performance evaluation was run.

## Bounded source/vintage finding

Official Federal Reserve CP pages were reachable and document that CP issuance rates/volumes are typically updated daily with a one-day lag, CP outstanding is available for Wednesdays and month-end with a one-day lag, and the daily release is usually available at 1:00 p.m. EST. The same official text also says the Board makes no guarantee regarding daily posting timing and may change the policy without notice.

ALFRED graph CSV vintage snapshots were reachable for representative series, but the bounded probes did not prove complete first-vintage mechanics across all required regimes:

- `COMPOUT` with `vintage_date=2020-04-02` returned a 2020 vintage column and data through 2020-04-01.
- `COMPOUT` with `vintage_date=2022-06-16` returned a 2022 vintage column and data through 2022-06-08.
- `COMPOUT` with `vintage_date=2008-10-16` fell back to `COMPOUT_20260701`, so the required 2008 outstanding first-vintage check was not proven.
- Representative daily rate vintages such as `DCPF3M_20081016`, `DCPN3M_20081016`, and `DCPF1M_20200402` were reachable, but one selected 1-month nonfinancial ID probe was not found and a complete parser/source map was not established.

Because the source gate required proof before performance and the 2008 outstanding vintage/timing mechanics remained ambiguous, this scout stopped before qfa/Alpaca market-data evaluation.

## Model behavior

`model.py` exposes `generate_signals(context)` and always returns empty weights with rejection metadata. It places no orders, uses no daemon, retains no raw daily paths, and stores no raw CP data.
