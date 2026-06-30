# sec-form144-affiliate-sale-pressure-scout-v1

AR-154 researched whether public SEC Form 144 notices of proposed affiliate/control-person sales can form a timestamp-safe sale-pressure signal for liquid U.S. common stocks.

## Result

**Rejected at source/event-table gate.** The model is disabled (`weight: 0.0`) and `generate_signals(context)` returns an empty target-weight mapping.

## Source probe summary

A bounded recovery probe checked SEC submissions metadata for 10 large issuer CIKs. All 10 metadata files were reachable, and their recent filings contained 1,646 `144` or `144/A` rows. Five sample accession metadata rows were observed, three primary archive document URLs were reachable, and one complete-submission text file showed embedded Form 144 fields such as issuer name/CIK, securities class, aggregate market value, units outstanding, and exchange name.

The probe did not satisfy the issue's required source gate because no durable Form 144 parser/event table was built after the prior timeout. Conservative issuer-to-liquid-common-stock mapping, duplicate/amendment clustering, breadth/concentration gates, and a real-data performance evaluator were also not built.

## Performance

No performance evaluation was run. No market bars, CSV market data, daemon, orders, event-window returns, shifted/shuffled controls, Form 4 controls, generic filing-day controls, momentum/reversal controls, sector/beta controls, or cost sensitivity tests were used.

## Files

- `model.py` — disabled zero-weight model
- `config.yaml` — source-gate rejection configuration
- `metadata.yaml` — compact model metadata
- `evaluations/latest.json` — machine-readable source-gate result
- `evaluations/latest.md` — human-readable source-gate summary
- `evaluations/runs/ar154_form144_source_gate_20260630T055303Z.json` — immutable copy of the run result
