# low-vol-quality-expanded-universe-validator-v1

AR-164 promotion/pruning validator for AR-010's low-volatility / smooth-return quality proxy on an expanded liquid U.S. single-name universe.

## Decision

**Rejected.** Real qfa/Alpaca daily-bar validation did not support promotion/retention of the AR-010 low-vol-quality family as a durable standalone expanded-universe alpha.

Primary 10 bps one-way cost metrics:

- Sharpe: **-0.870**
- Annualized return: **-9.81%**
- Annualized volatility: **11.15%**
- Max drawdown: **-48.43%**
- Average daily turnover: **0.021**
- Random-window median Sharpe: **-0.981**
- Random-window p25 Sharpe: **-1.378**
- Positive-window rate: **7.5%**

Controls dominated: SPY Sharpe 0.832, equal-weight selected universe Sharpe 0.929, sector equal-weight Sharpe 0.922, USMV/SPLV/QUAL Sharpes 0.602/0.522/0.753. The inverted rank was positive (Sharpe 0.774), a direct falsifier.

## Universe and limitations

Candidate pool was a predeclared liquid common-stock proxy list across 11 sectors, selected before scoring using minimum history, missing-bar, price-floor, dollar-volume, corporate-action/data sanity, and sector-cap filters. Selected universe count: **133**.

Limitations: qfa/Alpaca access in this workflow does not provide a full point-in-time security master, so the proxy list is current-liquid-large-cap and survivorship-biased. Sector mapping is manual and predeclared. No raw daily paths, CSV/parquet, SQLite DB, bytecode, or caches are retained.

## Data and safety

- Data source: qfa/Alpaca real daily bars only.
- `no_csv_used`: true
- `no_data_csv_argument_used`: true
- `no_daemon`: true
- `no_orders`: true
- `raw_daily_paths_retained`: false

## Files

- `model.py` — qfa-compatible `generate_signals(context)` implementation of the frozen validator signal.
- `config.yaml` — signal/evaluation contract.
- `metadata.yaml` — model metadata and decision.
- `evaluations/latest.json` and `evaluations/runs/ar164_realdata_20260630T163134Z.json` — compact real-data results.
- `evaluations/latest.md` — human-readable result summary.
