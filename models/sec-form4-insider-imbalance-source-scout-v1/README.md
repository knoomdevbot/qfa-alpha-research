# SEC Form 4 insider imbalance source scout v1

Issue: AR-159  
Decision: **rejected at source/event-table gate**  
Created: 2026-06-30T09:09:18Z

## Summary

This bounded recovery artifact confirms that SEC EDGAR submissions metadata and raw Form 4 ownership XML are reachable and parseable in a small sample. It does **not** build the required durable 2018-2026 timestamp-safe event table with conservative issuer-to-liquid-common-stock mapping, duplicate/amendment clustering, sale-to-purchase imbalance clusters, breadth/concentration gates, or any real-data performance evaluation.

Because the required event table with at least 500 mapped clustered events was not produced, the research result is a source-gate rejection rather than a held or accepted alpha.

## Bounded probe

- CIKs checked: 5 (`0000320193`, `0000789019`, `0001018724`, `0001045810`, `0001326801`)
- SEC submissions files reachable: 5 / 5
- Recent Form 4 / 4-A metadata rows observed in those submissions: 2,969
- Rows with acceptance timestamps: 2,969
- Raw Form 4 XML documents attempted: 10
- Raw Form 4 XML documents reachable and parsed: 10
- Non-derivative transactions observed in parsed sample: 22
- Transaction codes observed: `M`: 6, `F`: 6, `S`: 8, `G`: 2
- Acquired/disposed flags observed: `A`: 6, `D`: 16

Important path note: sampled `primaryDocument` values used an XSL path such as `xslF345X06/form4.xml`; raw XML was resolved from the accession directory basename (`form4.xml`) instead of the XSL subdirectory URL.

## Non-results

No returns, Sharpe, drawdown, hit-rate, random-window, control, or cost metrics were computed. No qfa/market daily bars were requested. No CSV data, daemon, or orders were used.

## Model behavior

`model.py` is intentionally disabled. `generate_signals(context)` returns an empty target-weight mapping.
