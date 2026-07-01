# AR-190 Real-Data Evaluation — treasury-auction-result-demand-share-source-scout-v1

- Decision: `rejected_realdata_performance_gate_failed`; accepted: `false`; enabled: `false`; weight: `0.0`.
- Data: official Treasury FiscalData/TreasuryDirect auction results plus Alpaca/qfa real ETF daily bars; no CSV/no `--data-csv`; no daemon; no orders.
- Timestamp convention: XML `AuctionDate` + `ReleaseTime` in America/New_York; `record_date` ignored; next-session ETF return after result timestamp.
- Primary 10 bps metrics: Sharpe `-7.477436`, annualized return `-0.33328501`, max drawdown `-0.97005281`, hit rate `0.184471`, events `1816`.
- Random/stress windows at 10 bps: median Sharpe `-6.305271`, p25 `-8.337412`, worst `-11.158621`, positive-window rate `0.0`.
- Controls: calendar-only Sharpe `-5.211989`, maturity-only `-20.362367`, reopening-only `-7.128782`, random-label median `-7.068231`.
- Acceptance gate: failed. Performance is not robust enough after costs and controls; no children spawned.
- Immutable run JSON: `evaluations/runs/ar190_qfa_alpaca_real_20260701T184846Z.json`.
