# AR-189 source/vintage evaluation — ar189_source_gate_20260701T172843Z

Decision: **rejected_source_gate**.

No qfa/Alpaca market-data or performance run was attempted because the source/vintage gate did not pass.

## Evidence summary

- Official Fed CP release pages and DDP landing page were reachable.
- Official timing language supports a conservative one-day/next-session concept only partially: rates/volumes are typically posted daily with one-day lag and the daily release is usually 1:00 p.m. EST, but the Fed explicitly gives no guarantee on posting timing.
- ALFRED vintage snapshots were reachable for some representative commercial-paper series.
- Required multi-regime proof was incomplete: the `COMPOUT` 2008 vintage probe returned current-vintage `COMPOUT_20260701` rather than a 2008 vintage column, so first-vintage outstanding history was not proven for the 2008 stress regime.
- Rate vintages such as `DCPF3M_20081016`, `DCPN3M_20081016`, and `DCPF1M_20200402` were reachable, but the full outstanding + AA financial/nonfinancial daily rate source map/parser was not proven in the bounded scout.

## Result

The model is committed only as a disabled zero-weight scaffold. Metrics are unavailable/null. No children were spawned.
