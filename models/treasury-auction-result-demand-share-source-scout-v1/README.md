# Treasury auction-result demand-share source scout v1

AR-190 bounded source/vintage scout for official Treasury auction result demand fields. This is a disabled zero-weight scaffold; no qfa/Alpaca performance evaluator was run.

## Decision

`source_gate_passed_needs_realdata_evaluation`

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

## Required next step

Run a real qfa/Alpaca ETF daily evaluation with next-session execution before marking complete, accepting, or spawning children.
