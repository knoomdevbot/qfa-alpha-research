# AR-159 latest evaluation — source-gate rejection

- Run ID: `ar159_form4_source_gate_20260630T090918Z`
- Created: 2026-06-30T09:09:18Z
- Decision: **rejected / source_gate_rejected**
- Performance run: **false**

## What was verified

A bounded SEC EDGAR probe checked 5 large-issuer CIKs and sampled 10 Form 4 filings. Submissions metadata was reachable, Form 4 rows included EDGAR acceptance timestamps, and raw ownership XML parsed successfully after resolving the XSL primary-document path trap.

## Probe metrics

| Metric | Value |
|---|---:|
| CIKs checked | 5 |
| CIKs with submissions metadata | 5 |
| Recent Form 4 / 4-A rows observed | 2,969 |
| Rows with acceptanceDateTime | 2,969 |
| Sampled Form 4 filings parsed | 10 |
| Non-derivative transactions observed | 22 |
| Transaction code counts | M=6, F=6, S=8, G=2 |
| Acquired/disposed counts | A=6, D=16 |

## Gate failure

The required durable 2018-2026 timestamp-safe event table with at least 500 conservatively mapped clustered insider-imbalance events was not built. Conservative ticker/common-stock mapping, duplicate/amendment clustering, concentration gates, controls, and performance evaluation were also not built.

## Provenance controls

`no_csv_used`, `no_data_csv_argument_used`, `no_daemon`, and `no_orders` are true. `raw_daily_paths_retained` is false. No raw SEC documents, event tables, or bar data were retained.
