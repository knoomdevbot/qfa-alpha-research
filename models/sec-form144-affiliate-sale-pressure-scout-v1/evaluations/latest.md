# AR-154 source-gate evaluation — SEC Form 144 affiliate-sale pressure scout

Run: `ar154_form144_source_gate_20260630T055303Z`  
Decision: **rejected at source/event-table gate**. No performance evaluation was run.

## What was checked

- A bounded SEC submissions probe checked 10 large-issuer CIKs.
- All 10 submissions metadata files were reachable.
- The recent submissions metadata contained 1,646 `144` or `144/A` rows across the checked CIKs.
- Five sample Form 144 accession metadata rows were observed; three sampled primary archive document URLs were reachable.
- One complete-submission text file was reachable and showed embedded fields including issuer name/CIK, securities class, aggregate market value, units outstanding, and exchange name.

## Gate result

The required alpha source gate did **not** pass:

- No durable Form 144 XML/text parser was implemented after the prior timeout.
- No reproducible timestamp-safe parsed event table was retained.
- Conservative issuer-to-liquid-common-stock mapping was not built.
- Duplicate/amendment clustering by issuer/filer/broker/approximate sale date was not built.
- Breadth and issuer/filer/broker/sector/year concentration checks were not possible.
- No real-data performance evaluator, controls, random windows, or costs were run.

Because the issue falsifier requires a parsed timestamp-safe Form 144 event table with conservative mapping, clustering, breadth/concentration gates, and real-data performance before any alpha claim, this run is rejected before performance.

## Performance metrics

Null. No market data, CSV data, random windows, shifted/shuffled controls, cost tests, daemon, or orders were used.

## Artifact status

The model is intentionally disabled and returns zero target weights.
