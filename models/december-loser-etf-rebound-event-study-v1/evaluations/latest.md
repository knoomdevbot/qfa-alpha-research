# Evaluation latest — AR-163 december-loser-etf-rebound-event-study-v1

- **Decision:** rejected
- **Data:** Alpaca/qfa real daily ETF OHLCV; no CSV; no daemon; no orders.
- **Usable annual events:** 7
- **Primary 10 bps median event return:** 0.019687
- **Primary 10 bps p25 event return:** 0.015561
- **Primary 10 bps event Sharpe:** 0.898481
- **Positive event rate:** 0.857143
- **January/no-loser median:** 0.016037
- **All-ETF equal-weight median:** 0.02043
- **SPY median:** 0.012422
- **Random-label yearly mean median:** 0.020871
- **Reject reasons:** fewer_than_8_usable_annual_events_after_filters; primary_dominated_or_matched_by_controls: all_etf_equal_weight_10bps, etf_short_term_reversal_control_10bps, randomized_loser_labels_year_mean_10bps

The primary sparse event study fails the hard January/no-loser, generic calendar-window, and placebo/control gates. No children/refinements were spawned.
