# exchange-reported-short-interest-publication-scout-v1

AR-172 source/vintage scout for official exchange-reported bi-monthly short-interest publication records.

## Decision

Rejected at the source gate; zero-weight scaffold only. No qfa/Alpaca daily bars were requested and no performance evaluation was run.

## Source findings

- FINRA Equity Short Interest pages are official and reachable, but the public file/API path is OTC-oriented. The FINRA file page states that prior to June 2021 the data contains OTC securities only, and bounded API probes returned only `marketClassCode=OTC` for the 2026-06-15 standardized partition (`record-total=9573`). This does not establish a broad listed common-stock event source.
- Nasdaq Trader's public short-interest page states Nasdaq short interest is rolling 12 months by issue; broad comma-delimited files require subscription via Secure File Transfer Protocol. Its publication schedule link now redirects to Nasdaq Data Link (`https://data.nasdaq.com/databases/NSIR`), not a free reproducible historical schedule table.
- NYSE's official product catalog confirms a semi-monthly NYSE Group Short Interest file with history from Jan 1988-present, but it is an order/subscription product. The public FTP sample directory contains only two 2026 sample files and was last modified on 2026-04-01, which is not an official historical publication-vintage archive.

## Consequence

The hard gate required `>=150` liquid mapped common stocks with multi-year official/reproducible short-interest records, settlement dates, dissemination/publication dates, and qfa/Alpaca bar coverage. That gate was not met; mapped liquid common-stock breadth is recorded as zero and performance metrics are null.

No raw market data, source archives, SQLite DB, caches, weights, or equity curves are retained.
