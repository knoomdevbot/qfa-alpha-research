# sec-nport-holdings-change-pressure-scout-v1

AR-152 researched whether public SEC N-PORT/NPORT-P fund holdings disclosures can form a timestamp-safe holdings-change pressure signal for U.S.-listed common stocks or ETFs.

## Result

**Rejected at source/event-table gate.** The model is disabled (`weight: 0.0`) and `generate_signals(context)` returns an empty target-weight mapping.

## Source probe summary

A bounded SEC EDGAR probe checked quarterly master indexes from 2024Q4 through 2026Q1 and found 78,079 `NPORT-P` filings. The first 80 sampled filings were reachable as public archive documents, all had EDGAR acceptance timestamps, all contained parseable XML, and the parsed sample produced 21,697 holdings rows.

The probe did not satisfy the issue's required source gate because the sample contained no filing-provided tickers, a reliable public CUSIP-to-ticker mapping was not established, and no reproducible same-series prior-holding change event table was built. Without that conservative mapped event table, liquid U.S. common-stock/ETF coverage and concentration controls could not be evaluated.

## Performance

No performance evaluation was run. No market bars, CSV market data, daemon, orders, event-window returns, shifted/shuffled controls, or cost sensitivity tests were used.

## Files

- `model.py` — disabled zero-weight model
- `config.yaml` — source-gate rejection configuration
- `metadata.yaml` — compact model metadata
- `evaluations/latest.json` — machine-readable source-gate result
- `evaluations/latest.md` — human-readable source-gate summary
