# Treasury auction-result demand-share source scout v1

AR-190 bounded source/vintage scout for official Treasury auction result demand fields. The official-source gate passed, then a real qfa/Alpaca ETF daily performance evaluation was run with next-session execution. The performance gate failed, so this remains a disabled zero-weight artifact.

## Decision

`rejected_realdata_performance_gate_failed`

## Source/vintage findings

- Official FiscalData endpoint is reachable: `https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/auctions_query`.
- Demand/result fields observed include bid-to-cover, tendered/accepted totals, and direct/indirect/primary-dealer accepted/tendered fields.
- Result file handles are present (`xml_filenm_comp_results`, `pdf_filenm_comp_results`); XML result files are retrievable via `https://www.treasurydirect.gov/xml/{xml_filenm_comp_results}`.
- Publication timing convention: parse official result XML `AuctionDate` plus `AuctionResults/ReleaseTime` as the result release timestamp in America/New_York. Do not use `record_date` as a publication timestamp.
- Future announcement-only rows are separable: the 2026-07-02 sample had 2 announcement-only rows and 0 result-bearing rows.
- Caveat: HTTP `Last-Modified` on older TreasuryDirect files reflects 2026 object/site migration, so it is retrieval/hash evidence, not first-publication evidence.

## Counts

```json
{
  "all_rows_since_2008": 6202,
  "future_announcement_only_sample_rows": 2,
  "sampled_bid_to_cover_nonnull_since_2010": 5654,
  "sampled_rows_since_2010": 5656,
  "sampled_xml_result_file_nonnull_since_2010": 5654
}
```

## Real-data performance result

- Run ID: `ar190_qfa_alpaca_real_20260701T184846Z`.
- Data: configured paper-data access through qfa/AlpacaGateway real ETF 1Day bars; no CSV/no `--data-csv`; no daemon; no orders.
- Execution: next ETF session after Treasury result timestamp; timestamp convention remains XML `AuctionDate` plus `ReleaseTime` in America/New_York, not `record_date`.
- Universe: primary duration/cash/inflation ETFs TLT, IEF, SHY, AGG, BND, GOVT, TIP; diagnostics/controls LQD, HYG, SPY, QQQ, IWM, GLD, UUP, BIL, SGOV where coverage was available.
- Primary 10 bps result: Sharpe `-7.477436`, annualized return `-0.33328501`, max drawdown `-0.97005281`, hit rate `0.184471`, modeled events `1816`.
- Random/stress windows at 10 bps: median Sharpe `-6.305271`, p25 `-8.337412`, worst `-11.158621`, positive-window rate `0.0`.
- Controls were not convincingly dominated; static/calendar/random-label variants were similarly weak or less bad. Acceptance gate failed; no children spawned.

Compact artifacts are under `evaluations/latest.json`, `evaluations/latest.md`, and `evaluations/runs/ar190_qfa_alpaca_real_20260701T184846Z.json`. No raw bars, daily equity paths, SQLite DBs, helper scripts, orders, daemon state, or CSV market data are retained.
