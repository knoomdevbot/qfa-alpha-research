# AR-190 latest evaluation

- Run ID: `ar190_source_gate_20260701T181400Z`
- Decision: `source_gate_passed_needs_realdata_evaluation`
- Source gate: passed
- Performance evaluated: false
- Enabled/weight: false / 0.0
- Asset bucket: etf
- Safety: no_csv_used=true; no_data_csv_argument_used=true; no_daemon=true; no_orders=true; raw_daily_paths_retained=false

## Summary

Official Treasury auction result rows and result file handles were verified across sampled regimes. Result XML retrieval is available from TreasuryDirect and includes `ReleaseTime`, which can be combined with `AuctionDate` for a timestamp-safe event parser. Announcement-only future rows have null result fields and null result file handles and can be excluded.

No qfa/Alpaca real-market ETF performance evaluator was run, so AR-190 remains queued and requires real-data evaluation.
