# december-loser-etf-rebound-event-study-v1

## Hypothesis
Liquid sector/industry/theme ETFs with large Oct-1 to Dec-20 drawdowns may rebound from the last December close through the fifth January trading day.

## Signal Definition
Rank eligible ETFs by close-to-close return from the first trading day on or after Oct 1 through the last trading day on or before Dec 20. Buy the five worst negative-return ETFs at the last December close and hold through the fifth January trading day close. Costs use a 10 bps total event haircut, with 5 and 20 bps sensitivity.

## Evaluation Summary
Decision: **rejected**. The primary leg produced median event return 0.019687 after 10 bps with p25 0.015561 across 7 usable annual events. It failed hard controls versus January/no-loser, all-ETF/SPY calendar-window, TSMOM/reversal/placebo, and shifted-label diagnostics.

## Orthogonality / Redundancy
Deferred due to rejection: the sparse annual stream failed decisive hard gates and compact accepted/watchlist return streams were not consistently reconstructable enough to alter the result.

## Known Risks
Daily OHLCV cannot identify actual tax-loss selling flows; this is a timestamp-safe fast-falsification event study only. The prompt-supplied current ETF pool creates survivorship/product-list limitations.
