# AR-170 source/vintage scout — rejected at gate

Decision: **rejected / hold at source-vintage gate**. The model scaffold is intentionally non-tradable and emits zero weights.

## What passed

- Official Treasury FiscalData DTS endpoints were reachable with HTTP 200:
  - `v1/accounting/dts/operating_cash_balance`
  - `v1/accounting/dts/deposits_withdrawals_operating_cash`
- Schema/line fields needed for a parser were visible: `record_date`, `account_type`, `open_today_bal`, `table_nbr`, `table_nm`, `src_line_nbr`, and table-II transaction fields.
- TGA table-I lines were stable in the spot check:
  - line 1: TGA opening balance
  - line 2: total TGA deposits
  - line 3: total TGA withdrawals
  - line 4: TGA closing balance

## What failed

The required AR-170 vintage/publication convention was **not proven**. FiscalData rows expose `record_date` plus fiscal/calendar dimensions, but the API response checked here did not provide a per-record publication timestamp, immutable vintage id, or official release-time field. Because the issue explicitly required resolving whether `record_date` is statement date, publication date, or both before performance scoring, I did not assume a lag convention and did not run qfa/Alpaca performance evaluation.

## Diagnostics

- Latest DTS `record_date` observed: `2026-06-26`.
- Operating cash balance filtered TGA rows checked: `2022-04-18` to `2026-06-26`, 1,050 rows per table-I line reported by the API.
- Deposits/withdrawals detail rows checked: `2021-10-01` to `2026-06-26`; 88,590 TGA deposit rows and 119,110 TGA withdrawal rows reported by the API.
- Note: the TGA closing balance row currently carries the closing-balance value in `open_today_bal`; `close_today_bal` is the string `null` in sampled responses.

## Performance and controls

Not run. No SPY/equal-weight/TSMOM/shifted/inverted/calendar/macro-control metrics were computed or invented because the source/vintage gate failed first.

## Safety flags

- no_csv_used: true
- no_data_csv_argument_used: true
- no_daemon: true
- no_orders: true
- raw_daily_paths_retained: false
