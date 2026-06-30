# AR-158 Reg SHO threshold-list add/remove persistence scout

**Decision:** rejected / blocking source-gate incomplete; zero weight.

This scout tested whether official exchange Reg SHO threshold-list files are reproducible enough to support add, persistence, and removal events for a short-horizon equity event alpha.  The model scaffold contains only parser helpers and `generate_signals(context)` returns an empty signal map.

## Source evidence

Official timestamped sources were reachable:

- Nasdaq Trader dated file pattern: `https://www.nasdaqtrader.com/dynamic/symdir/regsho/nasdaqthYYYYMMDD.txt`.
- NYSE regulatory download endpoint: `https://www.nyse.com/api/regulatory/threshold-securities/download?selectedDate=YYYY-MM-DD&market=NYSE`.
- Same NYSE endpoint with `market=NYSE American` and `market=NYSE Arca`.

Bounded month-end probe: 102 requested dates from 2018-01 through 2026-06, four markets. Nasdaq returned 102/102 valid timestamped files. NYSE-family markets were initially reachable and timestamped, but the session became unstable/rate-limited after early samples: NYSE 17/102, NYSE American 17/102, NYSE Arca 16/102 valid files.

Raw sampled breadth was large (1,580 unique symbols; 3,127 sampled rows; 2,487 add and 2,392 removal observations vs previous monthly sample), but this is **not** accepted liquid qfa/Alpaca mapped breadth.

## Why rejected

The issue's hard rule says source reachability alone is not a completed alpha result.  This run did not complete a full daily archive, did not build a durable liquid-mapped event table, and did not run required no-CSV qfa/Alpaca real daily-bar event-window performance.  Therefore the only safe result is a zero-weight rejected/blocking artifact.

## Handles

- Latest JSON: `evaluations/latest.json`
- Immutable run JSON: `evaluations/runs/ar158_regsho_source_gate_20260630T094900Z.json`
- Parser/zero-weight scaffold: `model.py`
- Config: `config.yaml`
- Metadata: `metadata.yaml`

## Reopen conditions

Only reopen if a controller can run a throttling-safe full daily source ingestion, map symbols to liquid tradables with real qfa/Alpaca bars, and evaluate add/remove/persistence event windows after 10 bps costs with 5/20 bps sensitivity and the declared controls.
