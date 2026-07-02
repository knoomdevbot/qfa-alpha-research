# AR-192 — EIA Weekly Natural Gas Storage first-vintage source/vintage scout

Decision: `rejected` after real-data micro-evaluation.

This folder records the AR-192 EIA Weekly Natural Gas Storage Report (WNGSR) source/vintage scout and bounded qfa/Alpaca real-market-data evaluation. The official source gate passed earlier: dated EIA Natural Gas Weekly Update archive pages expose historical WNGSR storage table values and net changes, and the archive index exposes about 1,507 `archivenew_ngwu` links.

## Evaluation summary

- Data: official EIA dated archive pages plus qfa/Alpaca real daily OHLCV; no CSV, no daemon, no orders.
- Candidate pool: non-levered natural gas, energy, pipeline/MLP, utility, commodity, and risk-control ETFs.
- Selected universe: `UNG`, `UNL`, `XLE`, `XOP`, `AMLP`, `XLU`, `DBC`, `USO`.
- Source sample: 108 dated pages parsed from a hard-capped 2022–early 2024 recovery run; 80 signal events after seasonal warmup.
- Rule tested: surprise storage draw/tightness goes long the exposed ETF basket; surprise build/looseness goes to `SHY`, evaluated on next-session and five-session returns.

## Key metrics

- Median random-window Sharpe after 10 bps per side: `-0.2944`.
- p25 random-window Sharpe: `-1.6450`.
- Worst random-window Sharpe: `-2.6004`.
- Positive-window rate: `0.40`.
- Five-session 10 bps event Sharpe: `0.0867`; equal-weight exposed ETF control Sharpe: `0.4664`.
- Five-session 10 bps hit rate: `0.3125`; max drawdown proxy: `-31.3%`.

## Decision rationale

Rejected. The simple storage-shock ETF allocation did not clear robustness/control gates: median and lower-quartile random-window Sharpe were negative after costs, and the equal-weight exposed ETF basket control dominated the primary event rule. Orthogonality was deferred because rejection was decisive.

## Process notes

The research subagent timed out and left a partial artifact claiming credential unavailability. Controller smoke testing proved configured market-data access was available, so no market-data hold was accepted. The controller recovered with a stricter hard-capped micro-evaluator and retained only compact summary artifacts.
