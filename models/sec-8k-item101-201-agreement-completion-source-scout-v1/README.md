# sec-8k-item101-201-agreement-completion-source-scout-v1

AR-191 rejected source-gate scaffold for SEC 8-K Item 1.01/2.01 agreement/completion event classes.

The micro-scout was intentionally hard-capped: SEC `company_tickers.json` plus 30 fixed large/liquid issuer submission JSON probes, no deep document crawl, and no performance backtest.

Result: `rejected_source_gate`. SEC metadata was reachable and included acceptance timestamps, but the scout did not build a durable class-separated parser/event table. The bounded sample found 111 Item 1.01 and 16 Item 2.01 8-K metadata rows (121 candidates), below source-gate requirements once parser/mapping/deduplication/audit obligations are considered.

The included `model.py` is a zero-weight/no-signal scaffold.
