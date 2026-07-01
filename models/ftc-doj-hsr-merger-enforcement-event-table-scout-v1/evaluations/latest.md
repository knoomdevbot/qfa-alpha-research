# AR-181 source-gate evaluation

Run: `ar181_source_gate_20260701T102151Z`

Decision: **rejected_source_gate**.

Official-source scout results:

- FTC HSR Legal Library reachable; displayed 27,907 early-termination notices.
- Scanned 6 HSR listing pages / 120 notice listings and 17 HSR detail pages.
- HSR detail fields seen: transaction number, notice date, acquiring party, acquired party, granting status, and acquired entities.
- FTC HSR API documentation reachable, but direct unauthenticated API requests returned 403.
- FTC press-release search reachable, but a simple merger query was noisy/duplicated on the first page.
- DOJ Antitrust press base reachable; one DOJ query URL returned 403; a DOJ detail sample exposed `article:published_time` metadata.
- 69 of 120 sampled HSR listing titles contained fund/private/holding-company indicators by a rough legal-name screen.
- Conservatively mapped liquid U.S. common-stock events accepted: 0.

Gate outcome: rejected because no durable official event table with >=150 conservatively mapped liquid U.S. common-stock events, timestamp-safe next-session mapping, role labels, dropped-event logs, manual mapping precision audit, and concentration diagnostics was produced.

No qfa/Alpaca performance was run. The committed model wrapper returns no signals.
