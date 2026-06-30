# AR-153 evaluation latest

- Run ID: `ar153_source_gate_20260630T042236Z`
- Decision: **rejected**
- Gate: source/event-table feasibility
- Required gate: conservative parsed timestamp-safe event table with at least 150 liquid mapped common-stock offering events
- Result: gate not passed

## Probe summary

SEC public metadata was reachable. In a bounded first-30-current-ticker submissions probe, offering-related form metadata appeared with acceptance timestamps and primary document names. The probe was not a validated event table: it did not parse offering documents, exclude non-common-stock financing cases, reconstruct historical ticker mappings, apply liquidity screens, or test concentration.

## Performance

No performance backtest was run. Metrics are null. No qfa/Alpaca bars, raw daily paths, raw SEC documents, raw event tables, helper scripts, caches, daemon, CSV data, or orders were produced or retained.
