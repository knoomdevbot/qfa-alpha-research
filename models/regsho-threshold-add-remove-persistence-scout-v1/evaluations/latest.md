# AR-158 latest evaluation: Reg SHO threshold-list add/remove persistence scout

**Run:** `ar158_regsho_source_gate_20260630T094900Z`  
**Decision:** rejected / blocking source-gate incomplete; zero-weight scaffold only.  
**Flags:** no CSV, no data CSV argument, no daemon, no orders, no raw daily paths retained.

## Findings

- Official sources are partially feasible:
  - Nasdaq Trader `nasdaqthYYYYMMDD.txt` files were valid and repeatable across 102/102 month-end probes from 2018-01 through 2026-06.
  - NYSE regulatory threshold-securities download endpoint was confirmed for NYSE, NYSE American, and NYSE Arca with 14-digit timestamp trailers, but repeated bounded probing became unstable/rate-limited: NYSE 17/102 valid, NYSE American 17/102 valid, NYSE Arca 16/102 valid.
- Raw sampled breadth was ample but not a hard-gate pass:
  - 1,580 unique raw symbols.
  - 3,127 sampled rows.
  - 2,487 sampled adds and 2,392 sampled removals vs previous monthly sample; 640 sampled persists.
- Timestamp/vintage evidence exists in official file trailers, e.g. Nasdaq `20180131230022`, NYSE-family `20180131210502`, Nasdaq latest probe `20260629230020`.

## Performance and controls

No qfa/Alpaca daily-bar performance was run.  No controls or orthogonality checks were run because the full source archive, liquid mapping, and concentration-safe event table were not completed.

## Gate conclusion

Rejected/blocking.  Source reachability without a durable full event table and real-data performance is explicitly insufficient for this issue.  Do not spawn threshold-list continuation children from this run.
