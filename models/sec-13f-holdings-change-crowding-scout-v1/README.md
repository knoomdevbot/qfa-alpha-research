# sec-13f-holdings-change-crowding-scout-v1

Zero-weight source-feasibility scaffold for AR-169.

## Hypothesis

SEC 13F information-table holdings changes, using EDGAR acceptance-time discipline and conservative lag, may identify institutional accumulation/distribution/new/exit positions with post-publication drift or reversal in liquid common stocks.

## Result

**Rejected at source/mapping gate.** A bounded EDGAR probe showed that 13F submissions metadata, acceptance timestamps, information-table XML parsing, and same-filer CUSIP-level quarterly changes are feasible. The scout did not establish the required conservative CUSIP-to-ticker/common-stock mapping with qfa/Alpaca liquid daily-bar coverage and concentration safety.

Because the hard source gate failed, the model is disabled and `generate_signals(context)` returns `{}`.

## Key diagnostics

- 12 manager CIKs checked; all 12 submissions endpoints reachable.
- 36 sampled 13F-HR / 13F-HR/A filings; all had acceptance timestamps and parseable information-table XML.
- 573,744 parsed holdings rows and 13,513 distinct CUSIPs in the bounded sample.
- 24 same-filer quarter pairs compared, producing 77,375 same-CUSIP comparisons, 16,224 new positions, 15,265 exits, 35,884 increases, and 32,886 decreases.
- PUT/CALL rows were observed and would need exclusion/control.
- No conservative mapped liquid common-stock universe was built; no returns test was run.

## Files

- `model.py` — disabled zero-weight scaffold.
- `config.yaml` — source-gate settings and disabled configuration.
- `metadata.yaml` — model metadata.
- `evaluations/latest.json` — full source-gate diagnostics.
- `evaluations/latest.md` — human-readable summary.
- `evaluations/runs/ar169_13f_source_gate_20260630T194017Z.json` — compact immutable run record.
