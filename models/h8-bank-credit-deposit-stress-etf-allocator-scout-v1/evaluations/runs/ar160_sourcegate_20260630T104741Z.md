# AR-160 latest evaluation — source gate passed, real-data evaluation queued

- Run ID: `ar160_sourcegate_20260630T104741Z`
- Created: 2026-06-30T10:47:41Z
- Decision: **source gate passed / keep queued for real-data evaluation**
- Performance run: **false**
- Model enabled: **false**; target weight: **0.0**

## Source/vintage gate findings

| Check | Result |
|---|---|
| H.8 public release lag | Passed: official Fed pages state Friday generally 4:15 p.m. ET, or Thursday generally 4:15 p.m. ET before federal-holiday Fridays. |
| Dated official H.8 archives | Passed: `releaseDates.json` exposed 31 year buckets; sampled 20260626, 20260618, 20210108, and 20180316 archive pages. |
| Required rows in archives | Passed: sampled archives included Bank credit, Deposits, and Borrowings rows with matching Last Update dates. |
| ALFRED bank credit | Passed: `TOTBKCR`, weekly ending Wednesday, archival real-time page observed. |
| ALFRED deposits | Passed: `DPSACBW027SBOG`, weekly ending Wednesday, archival real-time page observed. |
| ALFRED borrowings | Partial but usable with caveat: `H8B3094NCBCMG` archival real-time page is monthly; weekly borrowings must be parsed from dated official H.8 archive pages or excluded. |

## Required next step

Run a durable qfa/Alpaca real daily market-data random-period evaluation and controls before any completion, rejection, watchlist status, nonzero weight, or child issue decision. The first eligible ETF trade must be after the public H.8 release timestamp.

## Provenance controls

`no_csv_used`, `no_data_csv_argument_used`, `no_daemon`, and `no_orders` are true. `raw_daily_paths_retained` is false. No raw bars/equity paths/databases/credential snippets are retained.
