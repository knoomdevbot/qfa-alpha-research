# AR-181 FTC/DOJ HSR and merger-enforcement event-table scout

Decision: **rejected_source_gate**.

A bounded official-source probe verified that the FTC Legal Library HSR early-termination notice corpus is reachable and broad: the page displayed 27,907 notices, and 6 listing pages / 120 notices were scanned. Seventeen HSR detail pages exposed official transaction number, date, acquiring party, acquired party, granting status, and acquired-entity fields. The FTC API documentation page was reachable, but direct `api.ftc.gov/v0/hsr-early-termination-notices` requests returned 403 without an API key, so an unauthenticated reproducible official API path was not established.

The scout also checked official FTC press-release search pages and DOJ Antitrust Division press pages. FTC press search was reachable but noisy for a simple merger query. DOJ base press pages were reachable and DOJ detail pages can expose `article:published_time` metadata, while a DOJ query URL returned 403. These sources are useful for manual case research but did not provide a compact, durable, automated event table in this run.

Source-gate counts:

- official_endpoints_probed: 6
- hsr_total_displayed_by_ftc: 27,907
- hsr_listing_pages_scanned: 6
- hsr_listing_events_scanned: 120
- hsr_detail_pages_scanned: 17
- hsr_details_with_transaction_fields: 17
- hsr_sample_private_or_fund_indicator_count: 69 / 120
- ftc_press_results_first_page: 21, with duplicates/noise under a simple merger query
- doj_base_press_links_seen: 6
- doj_merger_query_status: 403
- conservatively_mapped_liquid_common_stock_events: 0
- accepted_event_table_rows: 0

Manual audit finding: official HSR records give legal party names and date-only notice fields suitable only for conservative next-session handling, not a verified first-public timestamp per notice. Party-to-issuer/security mapping is the binding failure: many sampled parties are funds, partnerships, private companies, subsidiaries, foreign issuers, or ambiguous legal names. No durable point-in-time ticker/security-master mapping or dropped-event log meeting the >=150 liquid U.S. common-stock requirement was constructed.

No qfa/Alpaca performance was run. The model scaffold returns zero weights/no signals.

Rejection reason: official source breadth exists, but source access/API reproducibility, timestamp granularity, party-to-ticker mapping, dropped-event logging, and >=150 conservatively mapped liquid U.S. common-stock events did not pass the source gate.
