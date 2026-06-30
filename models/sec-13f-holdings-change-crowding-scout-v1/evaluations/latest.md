# SEC 13F holdings-change crowding/uncrowding scout

Issue: AR-169  
Model: `sec-13f-holdings-change-crowding-scout-v1`  
Decision: **rejected at source/mapping gate**; zero-weight scaffold only.

## Summary

A bounded source probe confirmed that SEC EDGAR can support the mechanical parts of a 13F holdings-change table:

- `data.sec.gov` submissions metadata were reachable for 12 large 13F manager CIKs.
- Recent 13F-HR / 13F-HR/A rows exposed `acceptanceDateTime` suitable for public-time discipline.
- Archive `index.json` plus information-table XML files were parseable in all 36 sampled filings.
- The parser saw 573,744 holdings rows and 13,513 distinct CUSIPs in the sample.
- Same-filer quarter-to-quarter CUSIP comparisons were feasible in the bounded sample.

The hard source gate still failed because the scout did **not** establish a conservative, timestamp-safe CUSIP-to-ticker/common-stock mapping with qfa/Alpaca liquid daily-bar coverage. Filing information tables generally provide CUSIP, issuer name, class, value, shares, and PUT/CALL flags rather than a durable ticker. Inferring tickers from current names would be ambiguous and survivorship-prone.

## Bounded probe diagnostics

| Diagnostic | Value |
|---|---:|
| Filer CIKs checked | 12 |
| CIK submissions reachable | 12 |
| Recent 13F rows in submissions | 379 |
| Sampled filings | 36 |
| Sampled filings with acceptance datetime | 36 |
| Parseable information-table XML filings | 36 |
| Parsed holdings rows | 573,744 |
| Distinct CUSIPs in sample | 13,513 |
| PUT rows seen/excluded | 15,173 |
| CALL rows seen/excluded | 17,684 |
| Same-filer quarter pairs checked | 24 |
| Same-CUSIP pairs compared | 77,375 |
| New positions | 16,224 |
| Exit positions | 15,265 |
| Increased positions | 35,884 |
| Decreased positions | 32,886 |
| Unchanged positions | 8,605 |

Sampled filers: Berkshire Hathaway, BlackRock, Vanguard, State Street, JPMorgan Chase, Morgan Stanley, Goldman Sachs, Citadel Advisors, Bridgewater Associates, Renaissance Technologies, Two Sigma Investments, and AQR Capital Management.

## Gate decision

Passed source subcomponents:

- SEC submissions metadata reachability.
- EDGAR acceptance timestamp availability in sampled filings.
- Archive index and information-table XML resolution.
- CUSIP/share/value parser sufficient for bounded same-filer quarterly changes.

Failed hard-gate components:

- Conservative CUSIP-to-ticker/common-stock mapping was not established.
- Mapped liquid common-stock issuer breadth of at least 150-250 was not proven.
- qfa/Alpaca daily-bar coverage was not checked because the mapping gate failed.
- Issuer/filer/sector/quarter/year concentration safety was not completed.
- Amendment de-duplication/replacement policy remains incomplete.

## Performance

No qfa/Alpaca event/ranker evaluation was run. Metrics are null by design because the source/mapping gate failed. No market-data CSV, daemon, orders, raw bars, caches, databases, or helper scripts were retained.
