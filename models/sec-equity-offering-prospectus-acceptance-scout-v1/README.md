# SEC equity offering prospectus acceptance scout v1

Issue: AR-153

Decision: **rejected at source/event-table gate**.

This is a compact bounded-recovery artifact. A quick SEC metadata probe confirmed that public company ticker metadata and submissions metadata were reachable and that recent offering-related form metadata exists. However, the run did not complete the conservative parser and mapping requirements needed for a timestamp-safe table of at least 150 liquid mapped common-stock offering events.

No performance backtest was run. No market bars, raw SEC documents, event rows, caches, helper scripts, daemon, or orders were retained. The model is intentionally inert and `generate_signals(context)` returns an empty weight dictionary.

Primary failure reason: SEC form metadata alone is too noisy for this alpha. It over-includes generic 8-Ks, shelf registrations, debt, preferreds, warrants, units, mixed shelf supplements, amendments, and other cases that require document-level parsing plus conservative ticker/liquidity validation before any performance claim.
