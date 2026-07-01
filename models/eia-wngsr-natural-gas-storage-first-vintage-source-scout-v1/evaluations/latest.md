# AR-192 source-gate run — 2026-07-01T20:32:03Z

Decision: `source_gate_passed_needs_realdata_evaluation`.

## Compact findings

- Official EIA archive index `https://www.eia.gov/naturalgas/weekly/includes/archive.php` was reachable and a bounded probe counted about 1,507 `archivenew_ngwu` dated archive links.
- Four official dated EIA archive pages were sampled; all contained a release date and a WNGSR-sourced working-gas storage table with total stock levels and net change:
  - 2025-12-18 page: total 3,579 Bcf vs 3,746 Bcf, net change -167 Bcf.
  - 2024-12-19 page: total 3,622 Bcf vs 3,747 Bcf, net change -125 Bcf.
  - 2023-09-28 page: total 3,359 Bcf vs 3,269 Bcf, net change +90 Bcf.
  - 2022-12-22 page: total 3,325 Bcf vs 3,412 Bcf, net change -87 Bcf.
- Current official WNGSR files (`wngsr.json`, `wngsr.csv`, `wngsr.txt`) were reachable. Current CSV includes exact 10:30 a.m. Eastern release-time wording for the current release.
- Current/revised history workbooks (`ngshistory.xls`, `archngshistory.xls`) are reachable but were not counted as first-vintage proof by themselves.

## Caveat for later evaluator

Historical archive pages directly provide dated values/net changes; the exact intraday timestamp should be normalized conservatively using official WNGSR schedule/current-release convention and audited for holiday exceptions before any market-data evaluation.

No qfa/Alpaca performance run was executed. Metrics remain null.
