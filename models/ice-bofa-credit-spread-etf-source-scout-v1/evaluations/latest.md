# AR-188 source-gate evaluation — ICE/BofA credit-spread first-vintage scout

- Run ID: `ar188_source_gate_20260701T164407Z`
- Checked at: 2026-07-01T16:44:07Z
- Decision: **rejected**
- Source gate passed: **false**
- Performance evaluation run: **false**
- Asset bucket: etf
- Crypto label: false

## Gate result

The scout stopped at the source/vintage gate. Representative official ICE/BofA
option-adjusted spread series were reachable through public FRED graph CSVs and
ALFRED pages, but public access did not prove durable timestamp-safe first-vintage
coverage across multiple credit cycles.

Observed public windows:

| Series | Description | Public rows | First obs | Last obs | ALFRED page window |
|---|---|---:|---|---|---|
| BAMLH0A0HYM2 | ICE BofA US High Yield Index OAS | 786 | 2023-07-03 | 2026-06-30 | 2023-07-03 to 2026-06-30 |
| BAMLC0A0CM | ICE BofA US Corporate Index OAS | 785 | 2023-07-03 | 2026-06-30 | 2023-07-03 to 2026-06-30 |
| BAMLC0A4CBBB | ICE BofA BBB US Corporate Index OAS | 786 | 2023-07-03 | 2026-06-30 | 2023-07-03 to 2026-06-30 |
| BAMLH0A1HYBB | ICE BofA BB US High Yield Index OAS | 786 | 2023-07-03 | 2026-06-30 | 2023-07-03 to 2026-06-30 |

Public FRED pages identify Ice Data Indices, LLC as the source/release owner and
tag the series as copyrighted/pre-approval required. No licensed direct ICE/BofA
history was used or stored.

## Decision rationale

A roughly three-year public window is too short for robust random-window ETF
allocator testing over credit regimes, and the ALFRED pages checked did not prove
pre-2023 first-vintage history. Per AR-188 scope, no qfa/Alpaca performance
backtest was run after the source gate failed.

Required booleans: no CSV used, no data CSV argument used, no daemon, no orders,
and no raw daily paths retained.
