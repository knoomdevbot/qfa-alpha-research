# AR-192 — EIA Weekly Natural Gas Storage first-vintage source/vintage scout

Decision: `source_gate_passed_needs_realdata_evaluation`.

This folder is a disabled zero-weight scaffold. It records a compact official-source/vintage scout for EIA Weekly Natural Gas Storage Report (WNGSR) values as embedded in dated official EIA Natural Gas Weekly Update archive pages, plus current WNGSR machine-readable files and release-schedule probes.

No qfa/Alpaca market-data performance run was executed. The model wrapper returns no weights until a separate real-data evaluation is approved.

Key source-gate finding: official EIA dated archive pages contain historical storage table values and net changes for sampled releases, and the archive index exposes about 1,507 `archivenew_ngwu` links. Current WNGSR JSON/CSV/TXT files expose the current release values and the standard 10:30 a.m. Eastern WNGSR release timestamp format. Historical archive pages provide release dates and storage values; intraday time is supported operationally by official WNGSR schedule/current-release convention and must be normalized conservatively in later evaluation.
