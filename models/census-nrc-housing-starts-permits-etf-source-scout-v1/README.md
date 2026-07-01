# Census NRC housing starts/permits ETF source scout v1

AR-183 source/vintage feasibility scout for official Census/HUD New Residential Construction releases.

## Decision

**Source gate passed for parser feasibility only; performance not evaluated.** This folder is a disabled, zero-weight qfa wrapper. It must not place orders or claim ETF alpha until a later real-data evaluator fixes daily-bar timing, ETF coverage, controls, and random-window validation.

## Source findings

- Official archive page reachable: `https://www.census.gov/construction/nrc/data/releases.html`.
- Archive discovery found 298 modern official `newresconst_YYYYMM.pdf` release PDFs from 2001-04 through 2026-05 and 149 legacy official `c20_YYMM.txt` / `c22_YYMM.txt` release text files from 1995-01 through 2001-03.
- Current Census economic-indicator calendar page reachable and confirms Census economic release infrastructure; the modern PDFs themselves carry `FOR RELEASE AT 8:30 AM ...` timestamps.
- Bounded in-memory samples extracted first-published headline SAAR thousand values from official PDFs:
  - 2024-05 release PDF: June 20, 2024 8:30 AM EDT; permits 1,386; starts 1,277; completions 1,514.
  - 2023-01 release PDF: February 16, 2023 8:30 AM EST; permits 1,339; starts 1,309; completions 1,406.
  - 2020-01 release PDF: February 19, 2020 8:30 AM EST; permits 1,551; starts 1,567; completions 1,280.
- Legacy TXT samples are parseable for timestamp and narrative headline starts/permits (`c20`) and completions (`c22`) but have split release timing before the unified modern PDF format.
- ALFRED graph CSV vintage endpoints for `HOUST`, `PERMIT`, and `COMPUTSA` were probed with bounded observation/vintage queries but timed out or closed without response from this environment. Therefore the official Census/HUD archive is the source of record for first-vintage values; ALFRED remains a non-blocking cross-check to retry later.

## Usage

`model.py` exposes parser helpers:

- `discover_archive_links(html_text)`
- `parse_release_text(text, source_url, release_month='')`
- `fetch_official_event(url)`
- `build_event_table(urls, limit=None)`
- `generate_signals(context)` — disabled zero-weight wrapper.

The parser does not persist raw downloads. Future evaluators should persist only normalized event tables/diagnostics and should use next-session timing unless a same-day close convention is explicitly proven safe.

## Guardrails

- No CSV market data was used.
- No `data.csv` argument was used.
- No daemon or orders were started.
- Raw daily paths are not retained.
- Metrics are null because no market-data performance run occurred.
