# AR-171 real-data performance evaluation — rejected_realdata_performance

- Data: SEC submissions + qfa/Alpaca real daily bars; no CSV, no `--data-csv`, no daemon, no orders.
- Source breadth: 14029 timestamp-safe Item 2.02 events, 471 mapped issuers in the SEC sample; 220 liquid symbols selected; 2914 conditioned event signals.
- Primary event continuation h=5, 10 bps: median Sharpe -0.47363199, p25 -0.91711744, worst -1.76430976, positive-window rate 0.14285714.
- 5/20 bps primary Sharpe: -0.53321611 / -1.43787702.
- Controls: shifted +20 sessions median Sharpe -0.13063936; matched non-event median Sharpe -1.04837663; generic OHLCV reversal median Sharpe -0.31639056.

Decision: **rejected_realdata_performance**. Event source remains feasible, but compact timestamp-safe real-data performance did not clear the predeclared 10 bps cost/control gate.

Caveats: survivorship-biased current SEC ticker mapping; conservative but imperfect common-stock filtering; daily bars only; raw bars not retained.
