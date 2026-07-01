# fed-g17-industrial-production-capacity-etf-source-scout-v1

## Hypothesis

Timestamp-safe first-vintage Federal Reserve G.17 industrial production/capacity-utilization releases may contain ETF allocation information.

## Signal Definition

Disabled source-gate scaffold; `generate_signals(context)` returns zero weights until a separate real-data evaluator is implemented.

## Evaluation Summary

Source/vintage gate passed using official FRB release-date and dated `g17.txt` archive probes. No qfa/Alpaca performance run was completed. See `evaluations/latest.json` and `evaluations/latest.md`.

## Orthogonality / Redundancy

Not evaluated; performance metrics are null.

## Known Risks

- Macro releases are well-known and may be absorbed intraday.
- ALFRED/FRED probes were unavailable or API-key gated in bounded checks.
- The scaffold must remain queued/active until a real-data performance evaluator runs.

## Change Log

- 2026-07-01: Source/vintage gate scaffold created.
