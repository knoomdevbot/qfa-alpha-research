# AR-183 real-data evaluation — Census NRC first-vintage ETF allocator

- Run: `ar183_qfa_alpaca_real_20260701T125402Z`
- Decision: **rejected** (primary full-sample post-cost Sharpe <= 0; random-window p25 Sharpe is negative; positive-window rate below 55% threshold; inverted shock control matches/exceeds primary; SPY next-bar control matches/exceeds primary)
- Source gate: passed; official Census/HUD NRC PDF archive parsed in-memory.
- Market data: configured real daily ETF bars via qfa/Alpaca; no CSV, no daemon, no orders.
- Timing: release-date close to next trading close after 8:30am releases.
- Universe: XHB, ITB, VNQ, XLF, KRE, XLB, SPY, IWM, TLT, IEF, HYG, LQD; effective event-return sample starts in 2016 when all selected symbols had usable next-bar closes.

## Metrics

- Events traded: 123 (2016-01-04 to 2026-06-16).
- Primary 10 bps Sharpe: -0.8560687881774537 ; ann. return: -0.019073618735442777 ; max drawdown: -0.18429893718976942 ; positive event rate: 0.4146341463414634.
- Random windows: median Sharpe -0.7610340704574521, p25 -1.1333121584121155, worst -1.563594988705261, positive-window rate 0.015625.
- Cost sensitivity Sharpe: 5 bps -0.5856829648089552, 10 bps -0.8560687881774537, 20 bps -1.3968404349144503.
- Controls Sharpe: SPY -0.12827608406098637, equal-weight 0.06012851259405224, trend -0.2857263928244362, reversal 0.2857263928244362, inverted -0.22547450529654015, shifted -0.8938663160824819, random labels -0.21249243168541587.

## Conclusion

Rejected after real-data evaluation. The primary post-cost allocator is not robust enough under random windows and controls. No direct Census NRC refinement/extension children were spawned.
