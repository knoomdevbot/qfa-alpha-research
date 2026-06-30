# AR-165 evaluation latest

Decision: **rejected**

- Data: Alpaca real daily OHLCV via qfa AlpacaGateway; no CSV, no `--data-csv`, no daemon, no orders.
- Universe: 120 frozen liquid common stocks from 132 candidates.
- Primary 10 bps median random-window Sharpe: `-4.311790`
- p25 Sharpe: `-5.046487`; worst: `-5.417283`; positive-window rate: `0.00%`
- 20 bps median Sharpe: `-8.335323`
- Median annual turnover: `401.322189`
- Max relevant corr: `0.314246`
- Full model beats controls: `False`

Acceptance tests: `{'median_random_window_sharpe_gt_0': False, 'p25_non_hostile': False, 'positive_window_rate_ge_55pct': False, 'twenty_bps_not_collapsed': False, 'turnover_below_prior_bad_broadening_proxy': False, 'max_corr_le_0_60': True, 'full_model_beats_controls': False}`

Warnings: daily bars do not contain true closing-auction volume; universe is survivorship-biased; cost model is a turnover haircut.
