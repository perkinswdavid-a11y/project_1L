# Project 1L Strategy Experiment Log

Canonical research record for Project 1L strategy experiments.

This document is the human-readable source of truth for:
- what was tested,
- why it was tested,
- what configuration was used,
- what the result was,
- what we think happened,
- and what we should do next.

## Why this file exists

Without a disciplined research log, systematic strategy development turns into noise:
- the same ideas get retested accidentally,
- failed ideas are rediscovered and repeated,
- good ideas lose context,
- and results become hard to compare across time.

This file is meant to function like an institutional research notebook:
- searchable,
- reproducible,
- append-only,
- and readable months later.

## Operating Rules

1. One completed run = one experiment record.
2. Never overwrite old records. Add new records.
3. Every record must include:
   - metadata,
   - configuration,
   - results,
   - interpretation,
   - recommendation.
4. Every follow-up test should change only one meaningful variable whenever possible.
5. A baseline that is clearly weak should be rejected quickly.
6. A baseline that is close enough to viability should be promoted and refined deliberately.
7. The top index table should always let us scan the research state in under one minute.
8. The detailed experiment entries should always let us reconstruct exactly what happened.

## Status Legend

- `COMPLETED` = run finished successfully
- `FAILED` = run failed and result is invalid
- `ABORTED` = run intentionally stopped
- `SUPERSEDED` = historically kept, but no longer an active reference baseline

## Decision Legend

- `PROMOTE` = continue testing this strategy / parameter direction
- `HOLD` = inconclusive, can revisit later
- `REJECT_CURRENT_BASELINE` = do not spend more time on this version right now
- `INVALID_RUN` = config / data / runtime issue prevents interpretation
- `SUPERSEDED` = replaced by a newer preferred baseline

---

## Experiment Index

| Experiment ID | Date | Status | Strategy | Family | Interval | Sample | Closed Trades | Trades/Tested Day | Profit Factor | Net PnL | Max DD % | Decision | Next Action | Run ID |
|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| EXP-20260310-018 | 2026-03-10 | COMPLETED | price_gap_reversion_v1 | MES | 1m | FULL | 0 | 0.00 | N/A | 0.00 | N/A | INVALID_RUN | Data catalog spans ~2.5 years; 0 trades matches expected stat freq for 3-sigma event, but fails 30-trade minimum | 20260310T211028_price_gap_reversion_v1_extended_dev_a |
| EXP-20260310-017 | 2026-03-10 | COMPLETED | price_gap_reversion_v1 | MES | 1m | FULL | 0 | 0.00 | N/A | 0.00 | N/A | INVALID_RUN | Data catalog only contains 133 days; test cannot capture 30-trade minimum for 3-sigma events | 20260310T210359_price_gap_reversion_v1_extended_dev_a |
| EXP-20260310-016 | 2026-03-10 | COMPLETED | price_gap_reversion_v1 | MES | 1m | FULL | 0 | 0.00 | N/A | 0.00 | N/A | TBD | TBD | 20260310T210338_price_gap_reversion_v1_extended_dev_a |
| EXP-20260310-015 | 2026-03-10 | FAILED | price_gap_reversion_v1 | MES | 1m | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260310-014 | 2026-03-10 | FAILED | price_gap_reversion_v1 | MES | 1m | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260310-013 | 2026-03-10 | FAILED | price_gap_reversion_v1 | MES | 1m | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260310-012 | 2026-03-10 | FAILED | price_gap_reversion_v1 | MES | 1m | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260310-011 | 2026-03-10 | FAILED | price_gap_reversion_v1 | MES | 1m | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260310-010 | 2026-03-10 | COMPLETED | mes_mnq_co_oc_extreme_reversal_v1 | MES | 1m | FULL | 8 | 0.06 | 1.6768 | -939.75 | 1.17 | TBD | TBD | 20260310T205233_mes_mnq_co_oc_extreme_reversal_v1_extended_dev_a |
| EXP-20260310-009 | 2026-03-10 | COMPLETED | mes_mnq_co_oc_extreme_reversal_v1 | MES | 1m | FULL | 8 | 0.06 | 1.6768 | -939.75 | 1.17 | TBD | TBD | 20260310T205042_mes_mnq_co_oc_extreme_reversal_v1_dev_a |
| EXP-20260310-008 | 2026-03-10 | COMPLETED | mes_mnq_co_oc_reversal_v1 | MES | 1m | FULL | 132 | 0.99 | 1.1777 | -1772.75 | 3.01 | TBD | TBD | 20260310T203852_mes_mnq_co_oc_reversal_v1_sign_flip_dev_a |
| EXP-20260310-007 | 2026-03-10 | COMPLETED | mes_mnq_co_oc_reversal_v1 | MES | 1m | FULL | 132 | 0.99 | 0.7189 | -2632.50 | 4.50 | TBD | TBD | 20260310T202924_mes_mnq_co_oc_reversal_v1_dev_a |
| EXP-20260310-006 | 2026-03-10 | FAILED | opening_range_breakout_v5a | MES | 1m | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260310-005 | 2026-03-10 | COMPLETED | mes_mnq_relative_value_spread_v1 | MES | 1m | FULL | 47 | 0.35 | 0.7513 | -308.25 | 0.72 | TBD | TBD | 20260310T134625_mes_mnq_relative_value_spread_v1_dev_a |
| EXP-20260310-004 | 2026-03-10 | FAILED | mes_mnq_relative_value_spread_v1 | MES | 1m | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260310-003 | 2026-03-10 | FAILED | mes_mnq_relative_value_spread_v1 | MES | 1m | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260310-002 | 2026-03-10 | COMPLETED | overnight_intraday_reversal_v1 | MES | 1m | FULL | 75 | 0.59 | 0.7539 | -691.25 | 1.19 | TBD | TBD | 20260310T084539_overnight_intraday_reversal_v1_dev_b |
| EXP-20260310-001 | 2026-03-10 | COMPLETED | overnight_intraday_reversal_v1 | MES | 1m | FULL | 86 | 0.65 | 1.3582 | 1007.50 | 0.43 | TBD | TBD | 20260310T084154_overnight_intraday_reversal_v1_dev_a |
| EXP-20260309-042 | 2026-03-09 | COMPLETED | hedging_demand_intraday_momentum_v1 | MES | 1m | DEV_A | 36 | 0.27 | 0.4348 | -373.75 | 0.48 | REJECT_CURRENT_BASELINE | No further testing; parent failed Dev-A with no raw life | 20260309T220049_hedging_demand_intraday_momentum_v1_dev_a |
| EXP-20260309-041 | 2026-03-09 | COMPLETED | hedging_demand_intraday_momentum_v1 | MES | 1m | FULL | 36 | 0.27 | 0.4348 | -373.75 | 0.48 | TBD | TBD | 20260309T220017_hedging_demand_intraday_momentum_v1_dev_a |
| EXP-20260309-040 | 2026-03-09 | FAILED | hedging_demand_intraday_momentum_v1 | MES | 1m | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260309-039 | 2026-03-09 | FAILED | hedging_demand_intraday_momentum_v1 | MES | 1m | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260309-038 | 2026-03-09 | FAILED | hedging_demand_intraday_momentum_v1 | MES | 1m | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260309-037 | 2026-03-09 | FAILED | hedging_demand_intraday_momentum_v1 | MES | 1m | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260309-036 | 2026-03-09 | FAILED | hedging_demand_intraday_momentum_v1 | MES | 1m | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260309-035 | 2026-03-09 | FAILED | hedging_demand_intraday_momentum_v1 | MES | 1m | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260309-034 | 2026-03-09 | COMPLETED | mes_mnq_rmr_v1 | MES | 1m | FULL | 68 | 0.51 | 0.9733 | -25.00 | 0.26 | TBD | TBD | 20260309T193920_mes_mnq_rmr_v1_dev_a |
| EXP-20260309-033 | 2026-03-09 | COMPLETED | mes_mnq_rmr_v1 | MES | 1m | SMOKE | 21 | 0.66 | 1.2797 | 91.25 | 0.15 | TBD | TBD | 20260309T193730_mes_mnq_rmr_v1_smoke |
| EXP-20260309-032 | 2026-03-09 | COMPLETED | opening_range_breakout_v6a | MES | 1m | FULL | 68 | 0.53 | 1.1869 | 441.25 | 0.67 | TBD | TBD | 20260309T191007_opening_range_breakout_v6a_dev_b |
| EXP-20260309-031 | 2026-03-09 | COMPLETED | opening_range_breakout_v6a | MES | 1m | FULL | 63 | 0.47 | 1.3701 | 687.50 | 0.32 | TBD | TBD | 20260309T190952_opening_range_breakout_v6a_dev_a |
| EXP-20260309-030 | 2026-03-09 | COMPLETED | opening_range_breakout_v6a | MES | 1m | SMOKE | 7 | 0.22 | 0.8681 | -38.75 | 0.24 | TBD | TBD | 20260309T190938_opening_range_breakout_v6a_smoke |
| EXP-20260309-029 | 2026-03-09 | COMPLETED | gir_v1 | MES | 1m | FULL | 26 | 0.20 | 1.0451 | 27.50 | 0.43 | TBD | TBD | 20260309T190409_gir_v1_dev_a |
| EXP-20260309-028 | 2026-03-09 | COMPLETED | gir_v1 | MES | 1m | SMOKE | 5 | 0.16 | N/A | 305.00 | N/A | TBD | TBD | 20260309T190348_gir_v1_smoke |
| EXP-20260309-027 | 2026-03-09 | FAILED | gir_v1 | MES | 1m | SMOKE | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260309-026 | 2026-03-09 | FAILED | gir_v1 | MES | 1m | SMOKE | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260309-025 | 2026-03-09 | COMPLETED | opening_range_breakout_v6a | MES | 1m | FULL | 68 | 0.53 | 1.1869 | 441.25 | 0.67 | TBD | TBD | 20260309T185710_opening_range_breakout_v6a_dev_b |
| EXP-20260309-024 | 2026-03-09 | COMPLETED | opening_range_breakout_v6a | MES | 1m | FULL | 63 | 0.47 | 1.3701 | 687.50 | 0.32 | TBD | TBD | 20260309T185654_opening_range_breakout_v6a_dev_a |
| EXP-20260309-023 | 2026-03-09 | COMPLETED | opening_range_breakout_v6a | MES | 1m | SMOKE | 7 | 0.22 | 0.8681 | -38.75 | 0.24 | TBD | TBD | 20260309T185157_opening_range_breakout_v6a_smoke |
| EXP-20260309-022 | 2026-03-09 | COMPLETED | opening_range_breakout_v6a | MES | 1m | SMOKE | 7 | 0.22 | 0.8681 | -38.75 | 0.24 | TBD | TBD | 20260309T185051_opening_range_breakout_v6a_smoke |
| EXP-20260309-021 | 2026-03-09 | COMPLETED | odpc_v1 | MES | 1m | FULL | 94 | 0.71 | 0.7508 | -410.00 | 0.42 | TBD | TBD | 20260309T173634_odpc_v1_dev_a |
| EXP-20260309-020 | 2026-03-09 | COMPLETED | odpc_v1 | MES | 1m | SMOKE | 25 | 0.78 | 0.4226 | -363.75 | 0.42 | TBD | TBD | 20260309T173616_odpc_v1_smoke |
| EXP-20260309-019 | 2026-03-09 | COMPLETED | forb_reversal_v1 | MES | 1m | FULL | 96 | 0.72 | 0.5562 | -716.25 | 0.81 | TBD | TBD | 20260309T171844_forb_reversal_v1_dev_a |
| EXP-20260309-018 | 2026-03-09 | COMPLETED | forb_reversal_v1 | MES | 1m | SMOKE | 27 | 0.84 | 0.5954 | -196.25 | 0.31 | TBD | TBD | 20260309T171817_forb_reversal_v1_smoke |
| EXP-20260309-017 | 2026-03-09 | COMPLETED | opening_range_breakout_v11a | MES | 1m | FULL | 63 | 0.47 | 1.3701 | 687.50 | 0.32 | TBD | TBD | 20260309T133459_opening_range_breakout_v11a_dev_a |
| EXP-20260309-016 | 2026-03-09 | COMPLETED | opening_range_breakout_v6a | MES | 1m | FULL | 63 | 0.47 | 1.3701 | 687.50 | 0.32 | TBD | TBD | 20260309T133337_opening_range_breakout_v6a_dev_a |
| EXP-20260309-015 | 2026-03-09 | COMPLETED | opening_range_breakout_v6a | MES | 1m | FULL | 63 | 0.47 | 1.3701 | 687.50 | 0.32 | TBD | TBD | 20260309T133311_opening_range_breakout_v6a_dev_a |
| EXP-20260309-014 | 2026-03-09 | COMPLETED | opening_range_breakout_v11a | MES | 1m | SMOKE | 7 | 0.22 | 0.8681 | -38.75 | 0.24 | TBD | TBD | 20260309T133259_opening_range_breakout_v11a_smoke |
| EXP-20260309-013 | 2026-03-09 | COMPLETED | opening_range_breakout_v10a | MES | 1m | FULL | 22 | 0.17 | 0.9015 | -81.25 | 0.35 | TBD | TBD | 20260309T123024_opening_range_breakout_v10a_dev_a |
| EXP-20260309-012 | 2026-03-09 | COMPLETED | opening_range_breakout_v10a | MES | 1m | SMOKE | 2 | 0.06 | 0.0000 | -158.75 | 0.16 | TBD | TBD | 20260309T122128_opening_range_breakout_v10a_smoke |
| EXP-20260309-011 | 2026-03-09 | COMPLETED | opening_range_breakout_v9a | MES | 1m | FULL | 62 | 0.47 | 1.3074 | 572.50 | 0.32 | TBD | TBD | 20260309T114835_opening_range_breakout_v9a_dev_a |
| EXP-20260309-010 | 2026-03-09 | COMPLETED | opening_range_breakout_v9a | MES | 1m | SMOKE | 7 | 0.22 | 0.8681 | -38.75 | 0.24 | TBD | TBD | 20260309T114814_opening_range_breakout_v9a_smoke |
| EXP-20260309-009 | 2026-03-09 | COMPLETED | opening_range_breakout_v8a | MES | 1m | FULL | 63 | 0.47 | 1.3531 | 661.25 | 0.33 | TBD | TBD | 20260309T113507_opening_range_breakout_v8a_dev_a |
| EXP-20260309-008 | 2026-03-09 | COMPLETED | opening_range_breakout_v8a | MES | 1m | SMOKE | 7 | 0.22 | 0.8298 | -50.00 | 0.25 | TBD | TBD | 20260309T113349_opening_range_breakout_v8a_smoke |
| EXP-20260309-007 | 2026-03-09 | COMPLETED | opening_range_breakout_v7a | MES | 1m | FULL | 63 | 0.47 | 1.3701 | 687.50 | 0.32 | TBD | TBD | 20260309T095003_opening_range_breakout_v7a_dev_a |
| EXP-20260309-006 | 2026-03-09 | COMPLETED | opening_range_breakout_v7a | MES | 1m | SMOKE | 7 | 0.22 | 0.8681 | -38.75 | 0.24 | TBD | TBD | 20260309T094954_opening_range_breakout_v7a_smoke |
| EXP-20260309-005 | 2026-03-09 | COMPLETED | opening_range_breakout_v6a | MES | 1m | FULL | 68 | 0.53 | 1.1869 | 441.25 | 0.67 | BASELINE_MEASUREMENT | Official new benchmark parent. | 20260309T091129_opening_range_breakout_v6a_dev_b |
| EXP-20260309-004 | 2026-03-09 | COMPLETED | opening_range_breakout_v6a | MES | 1m | FULL | 63 | 0.47 | 1.3701 | 687.50 | 0.32 | BASELINE_MEASUREMENT | Official new benchmark parent. | 20260309T090108_opening_range_breakout_v6a_dev_a |
| EXP-20260309-003 | 2026-03-09 | COMPLETED | opening_range_breakout_v6a | MES | 1m | SMOKE | 7 | 0.22 | 0.8681 | -38.75 | 0.24 | TBD | TBD | 20260309T090049_opening_range_breakout_v6a_smoke |
| EXP-20260309-002 | 2026-03-09 | COMPLETED | opening_range_breakout_v6a | MES | 1m | FULL | 63 | 0.47 | 1.3701 | 687.50 | 0.32 | TBD | TBD | 20260309T082206_opening_range_breakout_v6a_dev_a |
| EXP-20260309-001 | 2026-03-09 | COMPLETED | opening_range_breakout_v6a | MES | 1m | SMOKE | 7 | 0.22 | 0.8681 | -38.75 | 0.24 | TBD | TBD | 20260309T082140_opening_range_breakout_v6a_smoke |
| EXP-20260308-027 | 2026-03-08 | COMPLETED | opening_range_breakout_v5c | MES | 1m | FULL | 39 | 0.29 | 1.1833 | 231.25 | 0.47 | TBD | TBD | 20260308T222819_opening_range_breakout_v5c_dev_a |
| EXP-20260308-026 | 2026-03-08 | COMPLETED | opening_range_breakout_v5c | MES | 1m | SMOKE | 5 | 0.16 | 0.7120 | -66.25 | 0.17 | TBD | TBD | 20260308T222758_opening_range_breakout_v5c_smoke |
| EXP-20260308-025 | 2026-03-08 | COMPLETED | opening_range_breakout_v5b | MES | 1m | FULL | 26 | 0.20 | 1.2559 | 216.25 | 0.23 | TBD | TBD | 20260308T221446_opening_range_breakout_v5b_dev_a |
| EXP-20260308-024 | 2026-03-08 | COMPLETED | opening_range_breakout_v5b | MES | 1m | SMOKE | 4 | 0.12 | 0.4101 | -131.25 | 0.22 | TBD | TBD | 20260308T221424_opening_range_breakout_v5b_smoke |
| EXP-20260308-023 | 2026-03-08 | COMPLETED | opening_range_breakout_v5a | MES | 1m | FULL | 17 | 0.13 | 0.9521 | -31.25 | 0.26 | TBD | TBD | 20260308T220149_opening_range_breakout_v5a_dev_a |
| EXP-20260308-022 | 2026-03-08 | COMPLETED | opening_range_breakout_v5a | MES | 1m | SMOKE | 2 | 0.06 | 0.0000 | -158.75 | 0.16 | TBD | TBD | 20260308T220135_opening_range_breakout_v5a_smoke |
| EXP-20260308-021 | 2026-03-08 | FAILED | opening_range_breakout_v5a | MES | 1m | SMOKE | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260308-020 | 2026-03-08 | FAILED | opening_range_breakout_v5a | MES | 1m | SMOKE | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260308-019 | 2026-03-08 | COMPLETED | perknasty_original | MES | 5m | FULL | 121 | 0.95 | 0.9639 | -147.50 | 0.74 | TBD | TBD | 20260308T212604_perknasty_original_dev_b |
| EXP-20260308-018 | 2026-03-08 | COMPLETED | perknasty_original | MES | 5m | FULL | 123 | 0.92 | 1.2852 | 1215.00 | 0.95 | TBD | TBD | 20260308T212433_perknasty_original_dev_a |
| EXP-20260308-017 | 2026-03-08 | COMPLETED | perknasty_original | MES | 5m | FULL | 9 | 0.90 | 0.9637 | -17.50 | 0.26 | TBD | TBD | 20260308T212229_perknasty_original_smoke |
| EXP-20260308-016 | 2026-03-08 | FAILED | perknasty_original | MES | 5m | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | INVALID_RUN | Fix error in config or execution | unknown |
| EXP-20260308-015 | 2026-03-08 | COMPLETED | opening_range_breakout_v4 | MES | 1m | FULL | 35 | 0.27 | 0.9578 | -56.25 | 0.57 | TBD | TBD | 20260308T162057_opening_range_breakout_v4b_dev_b |
| EXP-20260308-014 | 2026-03-08 | COMPLETED | opening_range_breakout_v4 | MES | 1m | FULL | 44 | 0.33 | 1.2804 | 368.75 | 0.25 | TBD | TBD | 20260308T161727_opening_range_breakout_v4b_dev_a |
| EXP-20260308-013 | 2026-03-08 | COMPLETED | opening_range_breakout_v4 | MES | 1m | SMOKE | 5 | 0.16 | 0.6629 | -75.00 | 0.17 | TBD | TBD | 20260308T161526_opening_range_breakout_v4b_smoke |
| EXP-20260308-012 | 2026-03-08 | FAILED | opening_range_breakout_v4 | MES | 1m | SMOKE | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260308-011 | 2026-03-08 | COMPLETED | opening_range_breakout_v4 | MES | 1m | FULL | 64 | 0.48 | 1.3070 | 587.50 | 0.42 | TBD | TBD | 20260308T155123_opening_range_breakout_v4a_dev_a |
| EXP-20260308-010 | 2026-03-08 | COMPLETED | opening_range_breakout_v4 | MES | 1m | SMOKE | 7 | 0.22 | 0.8681 | -38.75 | 0.24 | TBD | TBD | 20260308T154918_opening_range_breakout_v4a_smoke |
| EXP-20260308-009 | 2026-03-08 | FAILED | unknown | unknown | unknown | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | INVALID_RUN | Fix error in config or execution | unknown |
| EXP-20260308-008 | 2026-03-08 | COMPLETED | opening_range_breakout_v2 | MES | 1m | FULL | 70 | 0.55 | 1.1594 | 391.25 | 0.74 | SUPERSEDED | Superseded by ORB-v6a benchmark. | 20260308T122226_opening_range_breakout_v2_dev_b |
| EXP-20260308-007 | 2026-03-08 | COMPLETED | opening_range_breakout_v2 | MES | 1m | FULL | 64 | 0.48 | 1.3070 | 587.50 | 0.42 | SUPERSEDED | Superseded by ORB-v6a benchmark. | 20260308T122126_opening_range_breakout_v2_dev_a |
| EXP-20260308-006 | 2026-03-08 | FAILED | unknown | unknown | unknown | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | INVALID_RUN | Fix error in config or execution | unknown |
| EXP-20260308-005 | 2026-03-08 | FAILED | unknown | unknown | unknown | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | INVALID_RUN | Fix error in config or execution | unknown |
| EXP-20260308-004 | 2026-03-08 | FAILED | unknown | unknown | unknown | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | INVALID_RUN | Fix error in config or execution | unknown |
| EXP-20260308-003 | 2026-03-08 | FAILED | unknown | unknown | unknown | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | INVALID_RUN | Fix error in config or execution | unknown |
| EXP-20260308-002 | 2026-03-08 | COMPLETED | opening_range_breakout_v3 | MES | 1m | FULL | 52 | 0.20 | 0.8448 | -283.75 | 0.60 | TBD | TBD | 20260308T000454_opening_range_breakout_v3B_1m_validation |
| EXP-20260308-001 | 2026-03-08 | FAILED | unknown | unknown | unknown | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | INVALID_RUN | Fix error in config or execution | unknown |
| EXP-20260307-030 | 2026-03-07 | FAILED | unknown | unknown | unknown | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | INVALID_RUN | Fix error in config or execution | unknown |
| EXP-20260307-029 | 2026-03-07 | FAILED | unknown | unknown | unknown | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | INVALID_RUN | Fix error in config or execution | unknown |
| EXP-20260307-028 | 2026-03-07 | FAILED | opening_range_breakout_v3B | MES | 1m | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260307-027 | 2026-03-07 | FAILED | unknown | unknown | unknown | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | INVALID_RUN | Fix error in config or execution | unknown |
| EXP-20260307-026 | 2026-03-07 | COMPLETED | opening_range_breakout_v3 | MES | 1m | FULL | 70 | 0.27 | 1.1732 | 373.75 | 0.39 | TBD | TBD | 20260307T233418_opening_range_breakout_v3B_1m_dev |
| EXP-20260307-025 | 2026-03-07 | COMPLETED | opening_range_breakout_v3 | MES | 1m | SMOKE | 4 | 0.12 | 0.4101 | -131.25 | 0.22 | TBD | TBD | 20260307T232722_opening_range_breakout_v3_1m_smoke |
| EXP-20260307-024 | 2026-03-07 | COMPLETED | opening_range_breakout_v3 | MES | 1m | FULL | 55 | 0.21 | 1.0119 | 20.00 | 0.54 | TBD | TBD | 20260307T231235_opening_range_breakout_v3_1m_dev |
| EXP-20260307-023 | 2026-03-07 | COMPLETED | opening_range_breakout_v3 | MES | 1m | SMOKE | 4 | 0.12 | 0.4101 | -131.25 | 0.22 | TBD | TBD | 20260307T225809_opening_range_breakout_v3_1m_smoke |
| EXP-20260307-022 | 2026-03-07 | FAILED | opening_range_breakout_v3 | MES | 1m | SMOKE | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260307-021 | 2026-03-07 | FAILED | opening_range_breakout_v3 | MES | 1m | SMOKE | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260307-020 | 2026-03-07 | COMPLETED | opening_range_breakout_v2 | MES | 1m | FULL | 150 | 0.60 | 1.0263 | 192.50 | 1.11 | TBD | TBD | 20260307T192841_opening_range_breakout_v2_1m_holdout |
| EXP-20260307-019 | 2026-03-07 | COMPLETED | opening_range_breakout_v2 | MES | 1m | FULL | 141 | 0.55 | 1.2256 | 1108.75 | 1.01 | TBD | TBD | 20260307T191320_opening_range_breakout_v2_1m_validation |
| EXP-20260307-018 | 2026-03-07 | COMPLETED | opening_range_breakout_v2 | MES | 1m | FULL | 143 | 0.55 | 1.2109 | 965.00 | 0.74 | TBD | TBD | 20260307T184945_opening_range_breakout_v2_1m_dev |
| EXP-20260307-017 | 2026-03-07 | COMPLETED | opening_range_breakout_v2 | MES | 1m | SMOKE | 7 | 0.22 | 0.8681 | -38.75 | 0.24 | TBD | TBD | 20260307T183750_opening_range_breakout_v2_1m_smoke |
| EXP-20260307-016 | 2026-03-07 | COMPLETED | opening_range_breakout_v2 | MES | 1m | SMOKE | 7 | 0.22 | 0.8681 | -38.75 | 0.24 | TBD | TBD | 20260307T183713_opening_range_breakout_v2_1m_smoke |
| EXP-20260307-015 | 2026-03-07 | FAILED | opening_range_breakout_v2 | MES | 1m | SMOKE | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260307-014 | 2026-03-07 | FAILED | opening_range_breakout_v2 | MES | 1m | SMOKE | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260307-013 | 2026-03-07 | FAILED | opening_range_breakout_v2 | MES | 1m | SMOKE | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | TBD | Fix error in config or execution | unknown |
| EXP-20260307-012 | 2026-03-07 | COMPLETED | previous_day_high_low_breakout | MES | 1m | FULL | 635 | 0.82 | 0.7687 | -5261.25 | 5.85 | TBD | TBD | 20260307T131539_previous_day_high_low_breakout_1m |
| EXP-20260307-011 | 2026-03-07 | COMPLETED | previous_day_high_low_breakout | MES | 1m | FULL | 635 | 0.82 | 0.7687 | -5261.25 | 5.85 | TBD | TBD | 20260307T131313_previous_day_high_low_breakout_1m |
| EXP-20260307-010 | 2026-03-07 | COMPLETED | previous_day_high_low_breakout | MES | 1m | SMOKE | 7 | 0.88 | 2.3006 | 265.00 | 0.13 | TBD | TBD | 20260307T131211_previous_day_high_low_breakout_1m_smoke |
| EXP-20260307-009 | 2026-03-07 | COMPLETED | opening_range_breakout | MES | 1m | FULL | 454 | 0.59 | 0.7479 | -1991.25 | 2.24 | TBD | TBD | 20260307T124643_opening_range_breakout_30m_long_only_1m |
| EXP-20260307-008 | 2026-03-07 | COMPLETED | opening_range_breakout | MES | 1m | FULL | 454 | 0.59 | 0.7479 | -1991.25 | 2.24 | TBD | TBD | 20260307T123534_opening_range_breakout_15m_long_only_1m |
| EXP-20260307-007 | 2026-03-07 | COMPLETED | opening_range_breakout | MES | 1m | FULL | 761 | 0.99 | 0.8632 | -2003.75 | 2.85 | TBD | TBD | 20260307T121204_opening_range_breakout_15m_buffer_2ticks_1m |
| EXP-20260307-006 | 2026-03-07 | COMPLETED | opening_range_breakout | MES | 1m | FULL | 524 | 0.68 | 0.9099 | -812.50 | 1.05 | TBD | TBD | 20260307T121132_opening_range_breakout_15m_long_only_1m |
| EXP-20260307-005 | 2026-03-07 | COMPLETED | opening_range_breakout | MES | 1m | FULL | 749 | 0.97 | 0.8641 | -1843.75 | 2.50 | TBD | TBD | 20260307T121025_opening_range_breakout_30m_1m |
| EXP-20260307-004 | 2026-03-07 | FAILED | unknown | unknown | unknown | FULL | 0 | 0.00 | 0.0000 | 0.00 | 0.00 | INVALID_RUN | Fix error in config or execution | unknown |
| EXP-20260307-003 | 2026-03-07 | COMPLETED | opening_range_breakout | MES | 1m | SMOKE | 8 | 1.00 | 1.4186 | 67.50 | 0.12 | TBD | TBD | 20260307T120807_opening_range_breakout_1m_smoke |
| EXP-20260307-001 | 2026-03-07 | COMPLETED | opening_range_breakout | MES | 1m | FULL | 764 | 0.99 | 0.8949 | -1462.50 | 2.35 | PROMOTE | Test ORB 30m, long-only, and wider entry buffers | 20260307T102722_opening_range_breakout_1m |
| EXP-20260307-002 | 2026-03-07 | COMPLETED | vwap_reversion | MES | 1m | FULL | 4159 | 5.40 | 0.6501 | -31110.00 | 31.77 | REJECT_CURRENT_BASELINE | Do not tune now; revisit only later with strong trade-reduction filters | 20260307T104541_vwap_reversion_1m |

---

# Experiment Records

---

## EXP-20260307-001 | opening_range_breakout | MES | 1m | FULL

**Tags:** `#strategy/opening_range_breakout` `#family/MES` `#interval/1m` `#sample/full` `#status/completed` `#decision/promote`

**Status:** `COMPLETED`  
**Decision:** `PROMOTE`

### Metadata
- **Run ID:** `20260307T102722_opening_range_breakout_1m`
- **Run Date:** `2026-03-07`
- **Researcher:** `manual-entry`
- **Code Version / Commit:** `not-captured-pre-automation`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T102722_opening_range_breakout_1m`
- **Strategy:** `opening_range_breakout`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `770`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `null`

### Research Question / Hypothesis
Test whether a simple session-based opening range breakout baseline on MES 1-minute bars can survive realistic friction and produce a workable breakout profile over the full sample.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `baseline full-run validation of the opening range breakout strategy`
- **Why this run exists:** `determine whether ORB deserves promotion as the primary refinement candidate`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "allow_long": true,
  "allow_short": true,
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 98537.50 |
| Net PnL | -1462.50 |
| Total Return % | -1.4625 |
| Max Drawdown Abs | 2352.50 |
| Max Drawdown % | 2.3499 |
| Daily Sharpe Approx | -0.4147 |
| Execution Count | 1528 |
| Closed Trade Count | 764 |
| Win Rate % | 10.7330 |
| Gross Profit | 12447.50 |
| Gross Loss | 13910.00 |
| Profit Factor | 0.8949 |
| Trades / Tested Day | 0.99 |
| Approx Winning Trades | 82 |
| Approx Losing Trades | 682 |
| Approx Average Winner | 151.80 |
| Approx Average Loser | 20.40 |
| Approx Winner / Loser Ratio | 7.44 |

### Behavioral Read
- Trade frequency is controlled at roughly one closed trade per tested day.
- Drawdown is modest for a raw intraday baseline.
- The trade shape is consistent with a breakout system: low hit rate with much larger winners than losers.
- The strategy is not profitable yet, but it is close enough to breakeven to deserve further research.

### Interpretation
This is a **promising but incomplete** baseline. It failed economically over the full sample, but it did not fail in a chaotic or overtrading way. The profile suggests the core breakout idea may be valid, but false breakouts, weak side selection, and/or noisy early-session entries are likely pushing the baseline below breakeven.

### Risk Notes
- Low hit rate means entry quality is critical.
- Poor short-side behavior may be dragging down the full result.
- Small changes to entry logic may materially affect outcome.

### Recommendation / Next Action
1. Keep ORB as the primary strategy research candidate.
2. Only change one variable at a time.
3. Immediate follow-up experiments:
   - `range_minutes = 30`
   - long-only vs long+short
   - wider entry buffer
4. Inspect trade behavior by side and time-of-day before making bigger changes.

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T102722_opening_range_breakout_1m`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260307T102722_opening_range_breakout_1m\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260307T102722_opening_range_breakout_1m\daily_equity.csv`

---

## EXP-20260307-002 | vwap_reversion | MES | 1m | FULL

**Tags:** `#strategy/vwap_reversion` `#family/MES` `#interval/1m` `#sample/full` `#status/completed` `#decision/reject_current_baseline`

**Status:** `COMPLETED`  
**Decision:** `REJECT_CURRENT_BASELINE`

### Metadata
- **Run ID:** `20260307T104541_vwap_reversion_1m`
- **Run Date:** `2026-03-07`
- **Researcher:** `manual-entry`
- **Code Version / Commit:** `not-captured-pre-automation`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T104541_vwap_reversion_1m`
- **Strategy:** `vwap_reversion`
- **Strategy Archetype:** `mean_reversion`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `770`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `null`

### Research Question / Hypothesis
Test whether a simple intraday VWAP reversion baseline can capture session mean reversion on MES 1-minute bars after realistic slippage and commissions.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `baseline full-run validation of the VWAP reversion strategy`
- **Why this run exists:** `determine whether VWAP reversion deserves promotion as a baseline candidate`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "deviation_ticks": 12,
  "exit_band_ticks": 2,
  "min_bars_before_entry": 30,
  "position_size": 1,
  "tick_size": 0.25,
  "session_start": "08:30",
  "no_new_entries_after": "14:30",
  "allow_long": true,
  "allow_short": true,
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 68890.00 |
| Net PnL | -31110.00 |
| Total Return % | -31.1100 |
| Max Drawdown Abs | 31760.00 |
| Max Drawdown % | 31.7675 |
| Daily Sharpe Approx | -3.6801 |
| Execution Count | 8318 |
| Closed Trade Count | 4159 |
| Win Rate % | 74.3448 |
| Gross Profit | 57792.50 |
| Gross Loss | 88902.50 |
| Profit Factor | 0.6501 |
| Trades / Tested Day | 5.40 |
| Approx Winning Trades | 3092 |
| Approx Losing Trades | 1067 |
| Approx Average Winner | 18.69 |
| Approx Average Loser | 83.32 |
| Approx Winner / Loser Ratio | 0.22 |

### Behavioral Read
- Trade frequency is extremely high for a 1-contract MES baseline.
- The strategy wins often, but does not win enough per trade.
- The payoff profile is fragile and highly sensitive to friction.
- This version is structurally inferior to ORB as a next-step research candidate.

### Interpretation
This baseline is **economically weak and friction-sensitive**. The raw idea may still have some value in a more filtered form, but the current implementation trades too often and does not retain enough gross edge after realistic costs. It should not be the main focus right now.

### Risk Notes
- Very high trade count creates large cost exposure.
- High win rate is misleading because payoff ratio is poor.
- Drawdown is far too large for a baseline of this quality.

### Recommendation / Next Action
1. Reject the current VWAP reversion baseline.
2. Do not spend today tuning it.
3. Only revisit later if ORB research stalls.
4. If revisited, require trade-reduction changes first:
   - larger deviation threshold
   - stricter session/time filter
   - regime/volatility filter
   - possible one-side-only testing

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T104541_vwap_reversion_1m`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260307T104541_vwap_reversion_1m\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260307T104541_vwap_reversion_1m\daily_equity.csv`

## EXP-20260307-003 | opening_range_breakout | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakout #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260307T120807_opening_range_breakout_1m_smoke`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 7eee5cc`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T120807_opening_range_breakout_1m_smoke`
- **Strategy:** `opening_range_breakout`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `8`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
TBD

### Change Description
- **Parent Experiment:** `TBD`
- **What changed:** `TBD`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "allow_long": true,
  "allow_short": true,
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100067.50 |
| Net PnL | 67.50 |
| Total Return % | 0.0675 |
| Max Drawdown Abs | 115.00 |
| Max Drawdown % | 0.1150 |
| Daily Sharpe Approx | 2.2683 |
| Execution Count | 16 |
| Closed Trade Count | 8 |
| Win Rate % | 12.5000 |
| Gross Profit | 228.75 |
| Gross Loss | 161.25 |
| Profit Factor | 1.4186 |
| Trades / Tested Day | 1.00 |
| Approx Winning Trades | 1 |
| Approx Losing Trades | 7 |
| Approx Average Winner | 228.75 |
| Approx Average Loser | 23.04 |
| Approx Winner / Loser Ratio | 9.93 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T120807_opening_range_breakout_1m_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260307T120807_opening_range_breakout_1m_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260307T120807_opening_range_breakout_1m_smoke\daily_equity.csv`

---

## EXP-20260307-004 | unknown | unknown | unknown | FULL

**Tags:** #sample/full #status/failed #decision/invalid_run

**Status:** `FAILED`  
**Decision:** `INVALID_RUN`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 7eee5cc`
- **Report Directory:** `Config: configs/vwap_reversion_1m_smoke_DOESNTEXIST.json`
- **Strategy:** `unknown`
- **Strategy Archetype:** `unknown`
- **Family:** `unknown`
- **Interval:** `unknown`
- **Sample Type:** `FULL`
- **Date Range:** `unknown -> unknown`
- **Days Tested:** `1`
- **Instrument Mode:** `unknown`
- **Instrument Key:** `null`

### Research Question / Hypothesis
TBD

### Change Description
- **Parent Experiment:** `TBD`
- **What changed:** `TBD`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `unknown`
- **Session:** `unknown -> unknown`
- **Flatten Daily:** `unknown`
- **Flatten On Last Bar:** `unknown`
- **Initial Cash:** `unknown`
- **Contract Multiplier:** `unknown`
- **Tick Size:** `unknown`
- **Slippage Ticks:** `unknown`
- **Commission Per Side:** `unknown`

### Strategy Parameters
```json
{}
```

### Results
Run failed with error:
```
[Errno 2] No such file or directory: 'configs\\vwap_reversion_1m_smoke_DOESNTEXIST.json'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/vwap_reversion_1m_smoke_DOESNTEXIST.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260307-005 | opening_range_breakout | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakout #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260307T121025_opening_range_breakout_30m_1m`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 7eee5cc`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T121025_opening_range_breakout_30m_1m`
- **Strategy:** `opening_range_breakout`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `770`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Increasing the opening range from 15 minutes to 30 minutes will reduce false breakouts and improve ORB trade quality.

### Change Description
- **Parent Experiment:** `EXP-20260307-001`
- **What changed:** `Baseline ORB refinement: change range_minutes from 15 to 30. All other parameters unchanged.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 30,
  "buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "allow_long": true,
  "allow_short": true,
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 98156.25 |
| Net PnL | -1843.75 |
| Total Return % | -1.8437 |
| Max Drawdown Abs | 2506.25 |
| Max Drawdown % | 2.4969 |
| Daily Sharpe Approx | -0.5497 |
| Execution Count | 1498 |
| Closed Trade Count | 749 |
| Win Rate % | 10.8144 |
| Gross Profit | 11720.00 |
| Gross Loss | 13563.75 |
| Profit Factor | 0.8641 |
| Trades / Tested Day | 0.97 |
| Approx Winning Trades | 81 |
| Approx Losing Trades | 668 |
| Approx Average Winner | 144.69 |
| Approx Average Loser | 20.31 |
| Approx Winner / Loser Ratio | 7.13 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T121025_opening_range_breakout_30m_1m`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260307T121025_opening_range_breakout_30m_1m\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260307T121025_opening_range_breakout_30m_1m\daily_equity.csv`

---

## EXP-20260307-006 | opening_range_breakout | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakout #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260307T121132_opening_range_breakout_15m_long_only_1m`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 7eee5cc`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T121132_opening_range_breakout_15m_long_only_1m`
- **Strategy:** `opening_range_breakout`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `770`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
The short side may be degrading ORB performance, so disabling shorts may improve baseline performance.

### Change Description
- **Parent Experiment:** `EXP-20260307-001`
- **What changed:** `Baseline ORB refinement: disable shorts. All other parameters unchanged from the 15-minute baseline.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "allow_long": true,
  "allow_short": false,
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99187.50 |
| Net PnL | -812.50 |
| Total Return % | -0.8125 |
| Max Drawdown Abs | 1052.50 |
| Max Drawdown % | 1.0500 |
| Daily Sharpe Approx | -0.3069 |
| Execution Count | 1048 |
| Closed Trade Count | 524 |
| Win Rate % | 11.2595 |
| Gross Profit | 8210.00 |
| Gross Loss | 9022.50 |
| Profit Factor | 0.9099 |
| Trades / Tested Day | 0.68 |
| Approx Winning Trades | 59 |
| Approx Losing Trades | 465 |
| Approx Average Winner | 139.15 |
| Approx Average Loser | 19.40 |
| Approx Winner / Loser Ratio | 7.17 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T121132_opening_range_breakout_15m_long_only_1m`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260307T121132_opening_range_breakout_15m_long_only_1m\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260307T121132_opening_range_breakout_15m_long_only_1m\daily_equity.csv`

---

## EXP-20260307-007 | opening_range_breakout | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakout #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260307T121204_opening_range_breakout_15m_buffer_2ticks_1m`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 7eee5cc`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T121204_opening_range_breakout_15m_buffer_2ticks_1m`
- **Strategy:** `opening_range_breakout`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `770`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
A wider entry buffer may reduce noisy, low-quality ORB entries and improve payoff quality.

### Change Description
- **Parent Experiment:** `EXP-20260307-001`
- **What changed:** `Baseline ORB refinement: change buffer_ticks from 1 to 2. All other parameters unchanged.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "buffer_ticks": 2,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "allow_long": true,
  "allow_short": true,
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 97996.25 |
| Net PnL | -2003.75 |
| Total Return % | -2.0038 |
| Max Drawdown Abs | 2856.25 |
| Max Drawdown % | 2.8531 |
| Daily Sharpe Approx | -0.5690 |
| Execution Count | 1522 |
| Closed Trade Count | 761 |
| Win Rate % | 11.1695 |
| Gross Profit | 12643.75 |
| Gross Loss | 14647.50 |
| Profit Factor | 0.8632 |
| Trades / Tested Day | 0.99 |
| Approx Winning Trades | 85 |
| Approx Losing Trades | 676 |
| Approx Average Winner | 148.75 |
| Approx Average Loser | 21.67 |
| Approx Winner / Loser Ratio | 6.86 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T121204_opening_range_breakout_15m_buffer_2ticks_1m`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260307T121204_opening_range_breakout_15m_buffer_2ticks_1m\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260307T121204_opening_range_breakout_15m_buffer_2ticks_1m\daily_equity.csv`

---

## EXP-20260307-008 | opening_range_breakout | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakout #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260307T123534_opening_range_breakout_15m_long_only_1m`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 7eee5cc`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T123534_opening_range_breakout_15m_long_only_1m`
- **Strategy:** `opening_range_breakout`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `770`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
The short side may be degrading ORB performance, so disabling shorts may improve baseline performance.

### Change Description
- **Parent Experiment:** `EXP-20260307-001`
- **What changed:** `Baseline ORB refinement: disable shorts. All other parameters unchanged from the 15-minute baseline.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 30,
  "buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "allow_long": true,
  "allow_short": false,
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 98008.75 |
| Net PnL | -1991.25 |
| Total Return % | -1.9912 |
| Max Drawdown Abs | 2242.50 |
| Max Drawdown % | 2.2369 |
| Daily Sharpe Approx | -1.0075 |
| Execution Count | 908 |
| Closed Trade Count | 454 |
| Win Rate % | 11.0132 |
| Gross Profit | 5907.50 |
| Gross Loss | 7898.75 |
| Profit Factor | 0.7479 |
| Trades / Tested Day | 0.59 |
| Approx Winning Trades | 50 |
| Approx Losing Trades | 404 |
| Approx Average Winner | 118.15 |
| Approx Average Loser | 19.55 |
| Approx Winner / Loser Ratio | 6.04 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T123534_opening_range_breakout_15m_long_only_1m`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260307T123534_opening_range_breakout_15m_long_only_1m\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260307T123534_opening_range_breakout_15m_long_only_1m\daily_equity.csv`

---

## EXP-20260307-009 | opening_range_breakout | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakout #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260307T124643_opening_range_breakout_30m_long_only_1m`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 7eee5cc`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T124643_opening_range_breakout_30m_long_only_1m`
- **Strategy:** `opening_range_breakout`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `770`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Testing whether the longer 30-minute opening range improves the long-only ORB variant by reducing false breakout entries.

### Change Description
- **Parent Experiment:** `EXP-20260307-006`
- **What changed:** `ORB refinement from the promoted 15-minute long-only baseline: change range_minutes from 15 to 30 while keeping allow_short=false and all other parameters unchanged.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 30,
  "buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "allow_long": true,
  "allow_short": false,
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 98008.75 |
| Net PnL | -1991.25 |
| Total Return % | -1.9912 |
| Max Drawdown Abs | 2242.50 |
| Max Drawdown % | 2.2369 |
| Daily Sharpe Approx | -1.0075 |
| Execution Count | 908 |
| Closed Trade Count | 454 |
| Win Rate % | 11.0132 |
| Gross Profit | 5907.50 |
| Gross Loss | 7898.75 |
| Profit Factor | 0.7479 |
| Trades / Tested Day | 0.59 |
| Approx Winning Trades | 50 |
| Approx Losing Trades | 404 |
| Approx Average Winner | 118.15 |
| Approx Average Loser | 19.55 |
| Approx Winner / Loser Ratio | 6.04 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T124643_opening_range_breakout_30m_long_only_1m`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260307T124643_opening_range_breakout_30m_long_only_1m\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260307T124643_opening_range_breakout_30m_long_only_1m\daily_equity.csv`

---

## EXP-20260307-010 | previous_day_high_low_breakout | MES | 1m | SMOKE

**Tags:** #strategy/previousdayhighlowbreakout #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260307T131211_previous_day_high_low_breakout_1m_smoke`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 7eee5cc`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T131211_previous_day_high_low_breakout_1m_smoke`
- **Strategy:** `previous_day_high_low_breakout`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `8`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
A breakout through the previous regular-session high or low may capture stronger directional continuation than the ORB baseline.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `New baseline strategy: previous day high/low breakout with one-trade-per-side-per-day behavior and breakout-failure exits.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:30",
  "allow_long": true,
  "allow_short": true,
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100265.00 |
| Net PnL | 265.00 |
| Total Return % | 0.2650 |
| Max Drawdown Abs | 128.75 |
| Max Drawdown % | 0.1288 |
| Daily Sharpe Approx | 4.4373 |
| Execution Count | 14 |
| Closed Trade Count | 7 |
| Win Rate % | 28.5714 |
| Gross Profit | 468.75 |
| Gross Loss | 203.75 |
| Profit Factor | 2.3006 |
| Trades / Tested Day | 0.88 |
| Approx Winning Trades | 2 |
| Approx Losing Trades | 5 |
| Approx Average Winner | 234.38 |
| Approx Average Loser | 40.75 |
| Approx Winner / Loser Ratio | 5.75 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T131211_previous_day_high_low_breakout_1m_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260307T131211_previous_day_high_low_breakout_1m_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260307T131211_previous_day_high_low_breakout_1m_smoke\daily_equity.csv`

---

## EXP-20260307-011 | previous_day_high_low_breakout | MES | 1m | FULL

**Tags:** #strategy/previousdayhighlowbreakout #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260307T131313_previous_day_high_low_breakout_1m`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 7eee5cc`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T131313_previous_day_high_low_breakout_1m`
- **Strategy:** `previous_day_high_low_breakout`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `770`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
A breakout through the previous regular-session high or low may capture stronger directional continuation than the ORB baseline.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `New baseline strategy: previous day high/low breakout with one-trade-per-side-per-day behavior and breakout-failure exits.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:30",
  "allow_long": true,
  "allow_short": true,
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 94738.75 |
| Net PnL | -5261.25 |
| Total Return % | -5.2612 |
| Max Drawdown Abs | 5887.50 |
| Max Drawdown % | 5.8509 |
| Daily Sharpe Approx | -1.0540 |
| Execution Count | 1270 |
| Closed Trade Count | 635 |
| Win Rate % | 17.3228 |
| Gross Profit | 17490.00 |
| Gross Loss | 22751.25 |
| Profit Factor | 0.7687 |
| Trades / Tested Day | 0.82 |
| Approx Winning Trades | 110 |
| Approx Losing Trades | 525 |
| Approx Average Winner | 159.00 |
| Approx Average Loser | 43.34 |
| Approx Winner / Loser Ratio | 3.67 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T131313_previous_day_high_low_breakout_1m`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260307T131313_previous_day_high_low_breakout_1m\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260307T131313_previous_day_high_low_breakout_1m\daily_equity.csv`

---

## EXP-20260307-012 | previous_day_high_low_breakout | MES | 1m | FULL

**Tags:** #strategy/previousdayhighlowbreakout #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260307T131539_previous_day_high_low_breakout_1m`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 7eee5cc`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T131539_previous_day_high_low_breakout_1m`
- **Strategy:** `previous_day_high_low_breakout`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `770`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
A breakout through the previous regular-session high or low may capture stronger directional continuation than the ORB baseline.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `New baseline strategy: previous day high/low breakout with one-trade-per-side-per-day behavior and breakout-failure exits.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:30",
  "allow_long": true,
  "allow_short": true,
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 94738.75 |
| Net PnL | -5261.25 |
| Total Return % | -5.2612 |
| Max Drawdown Abs | 5887.50 |
| Max Drawdown % | 5.8509 |
| Daily Sharpe Approx | -1.0540 |
| Execution Count | 1270 |
| Closed Trade Count | 635 |
| Win Rate % | 17.3228 |
| Gross Profit | 17490.00 |
| Gross Loss | 22751.25 |
| Profit Factor | 0.7687 |
| Trades / Tested Day | 0.82 |
| Approx Winning Trades | 110 |
| Approx Losing Trades | 525 |
| Approx Average Winner | 159.00 |
| Approx Average Loser | 43.34 |
| Approx Winner / Loser Ratio | 3.67 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T131539_previous_day_high_low_breakout_1m`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260307T131539_previous_day_high_low_breakout_1m\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260307T131539_previous_day_high_low_breakout_1m\daily_equity.csv`

---

## EXP-20260307-013 | opening_range_breakout_v2 | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv2 #family/MES #interval/1m #sample/smoke #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 7eee5cc`
- **Report Directory:** `Config: configs/opening_range_breakout_v2_1m_smoke.json`
- **Strategy:** `opening_range_breakout_v2`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
A trader-grade ORB with structural stop placement, cost-protected stop movement, ATR-based trailing, and an opening-range quality filter may outperform the toy ORB baseline on MES.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for ORB-v2 implementation on MES 1-minute data. Extended smoke horizon to 40 days so the 20-day opening-range-width filter can warm up and still generate trades.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
Run failed with error:
```
Unknown strategy 'opening_range_breakout_v2'.
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/opening_range_breakout_v2_1m_smoke.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260307-014 | opening_range_breakout_v2 | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv2 #family/MES #interval/1m #sample/smoke #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 7eee5cc`
- **Report Directory:** `Config: configs/opening_range_breakout_v2_1m_smoke.json`
- **Strategy:** `opening_range_breakout_v2`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
A trader-grade ORB with structural stop placement, cost-protected stop movement, ATR-based trailing, and an opening-range quality filter may outperform the toy ORB baseline on MES.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for ORB-v2 implementation on MES 1-minute data. Extended smoke horizon to 40 days so the 20-day opening-range-width filter can warm up and still generate trades.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
Run failed with error:
```
name 'OpeningRangeBreakoutV2Strategy' is not defined
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/opening_range_breakout_v2_1m_smoke.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260307-015 | opening_range_breakout_v2 | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv2 #family/MES #interval/1m #sample/smoke #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 7eee5cc`
- **Report Directory:** `Config: configs/opening_range_breakout_v2_1m_smoke.json`
- **Strategy:** `opening_range_breakout_v2`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
A trader-grade ORB with structural stop placement, cost-protected stop movement, ATR-based trailing, and an opening-range quality filter may outperform the toy ORB baseline on MES.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for ORB-v2 implementation on MES 1-minute data. Extended smoke horizon to 40 days so the 20-day opening-range-width filter can warm up and still generate trades.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
Run failed with error:
```
OpeningRangeBreakoutV2Strategy.__init__() got an unexpected keyword argument 'allow_short'. Did you mean 'allow_long'?
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/opening_range_breakout_v2_1m_smoke.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260307-016 | opening_range_breakout_v2 | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv2 #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260307T183713_opening_range_breakout_v2_1m_smoke`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 7eee5cc`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T183713_opening_range_breakout_v2_1m_smoke`
- **Strategy:** `opening_range_breakout_v2`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
A trader-grade ORB with structural stop placement, cost-protected stop movement, ATR-based trailing, and an opening-range quality filter may outperform the toy ORB baseline on MES.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for ORB-v2 implementation on MES 1-minute data. Extended smoke horizon to 40 days so the 20-day opening-range-width filter can warm up and still generate trades.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99961.25 |
| Net PnL | -38.75 |
| Total Return % | -0.0387 |
| Max Drawdown Abs | 237.50 |
| Max Drawdown % | 0.2375 |
| Daily Sharpe Approx | -0.5102 |
| Execution Count | 14 |
| Closed Trade Count | 7 |
| Win Rate % | 42.8571 |
| Gross Profit | 255.00 |
| Gross Loss | 293.75 |
| Profit Factor | 0.8681 |
| Trades / Tested Day | 0.22 |
| Approx Winning Trades | 3 |
| Approx Losing Trades | 4 |
| Approx Average Winner | 85.00 |
| Approx Average Loser | 73.44 |
| Approx Winner / Loser Ratio | 1.16 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T183713_opening_range_breakout_v2_1m_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260307T183713_opening_range_breakout_v2_1m_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260307T183713_opening_range_breakout_v2_1m_smoke\daily_equity.csv`

---

## EXP-20260307-017 | opening_range_breakout_v2 | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv2 #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260307T183750_opening_range_breakout_v2_1m_smoke`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 7eee5cc`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T183750_opening_range_breakout_v2_1m_smoke`
- **Strategy:** `opening_range_breakout_v2`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
A trader-grade ORB with structural stop placement, cost-protected stop movement, ATR-based trailing, and an opening-range quality filter may outperform the toy ORB baseline on MES.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for ORB-v2 implementation on MES 1-minute data. Extended smoke horizon to 40 days so the 20-day opening-range-width filter can warm up and still generate trades.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99961.25 |
| Net PnL | -38.75 |
| Total Return % | -0.0387 |
| Max Drawdown Abs | 237.50 |
| Max Drawdown % | 0.2375 |
| Daily Sharpe Approx | -0.5102 |
| Execution Count | 14 |
| Closed Trade Count | 7 |
| Win Rate % | 42.8571 |
| Gross Profit | 255.00 |
| Gross Loss | 293.75 |
| Profit Factor | 0.8681 |
| Trades / Tested Day | 0.22 |
| Approx Winning Trades | 3 |
| Approx Losing Trades | 4 |
| Approx Average Winner | 85.00 |
| Approx Average Loser | 73.44 |
| Approx Winner / Loser Ratio | 1.16 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T183750_opening_range_breakout_v2_1m_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260307T183750_opening_range_breakout_v2_1m_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260307T183750_opening_range_breakout_v2_1m_smoke\daily_equity.csv`

---

## EXP-20260307-018 | opening_range_breakout_v2 | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv2 #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260307T184945_opening_range_breakout_v2_1m_dev`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 7eee5cc`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T184945_opening_range_breakout_v2_1m_dev`
- **Strategy:** `opening_range_breakout_v2`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2024-02-29`
- **Days Tested:** `261`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v2 may create a more robust long-only morning breakout system on MES by combining structural OR entry, structural initial stop, cost-protected stop escalation, ATR trailing, and a broad OR-width quality filter.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Development-window run for ORB-v2 on MES. This is the design-period evaluation for the frozen v2.0 rule set.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100965.00 |
| Net PnL | 965.00 |
| Total Return % | 0.9650 |
| Max Drawdown Abs | 747.50 |
| Max Drawdown % | 0.7363 |
| Daily Sharpe Approx | 0.9464 |
| Execution Count | 286 |
| Closed Trade Count | 143 |
| Win Rate % | 46.8531 |
| Gross Profit | 5541.25 |
| Gross Loss | 4576.25 |
| Profit Factor | 1.2109 |
| Trades / Tested Day | 0.55 |
| Approx Winning Trades | 67 |
| Approx Losing Trades | 76 |
| Approx Average Winner | 82.71 |
| Approx Average Loser | 60.21 |
| Approx Winner / Loser Ratio | 1.37 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T184945_opening_range_breakout_v2_1m_dev`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260307T184945_opening_range_breakout_v2_1m_dev\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260307T184945_opening_range_breakout_v2_1m_dev\daily_equity.csv`

---

## EXP-20260307-019 | opening_range_breakout_v2 | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv2 #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260307T191320_opening_range_breakout_v2_1m_validation`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 41ade39`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T191320_opening_range_breakout_v2_1m_validation`
- **Strategy:** `opening_range_breakout_v2`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2024-03-01 -> 2025-02-28`
- **Days Tested:** `257`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Frozen ORB-v2 rules should remain economically non-broken on the validation window if the design has real edge rather than development-period luck.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Validation-window run for ORB-v2 on MES using the exact frozen v2.0 rule set from the development phase.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 101108.75 |
| Net PnL | 1108.75 |
| Total Return % | 1.1087 |
| Max Drawdown Abs | 1012.50 |
| Max Drawdown % | 1.0056 |
| Daily Sharpe Approx | 1.0182 |
| Execution Count | 282 |
| Closed Trade Count | 141 |
| Win Rate % | 46.0993 |
| Gross Profit | 6022.50 |
| Gross Loss | 4913.75 |
| Profit Factor | 1.2256 |
| Trades / Tested Day | 0.55 |
| Approx Winning Trades | 65 |
| Approx Losing Trades | 76 |
| Approx Average Winner | 92.65 |
| Approx Average Loser | 64.65 |
| Approx Winner / Loser Ratio | 1.43 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T191320_opening_range_breakout_v2_1m_validation`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260307T191320_opening_range_breakout_v2_1m_validation\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260307T191320_opening_range_breakout_v2_1m_validation\daily_equity.csv`

---

## EXP-20260307-020 | opening_range_breakout_v2 | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv2 #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** PROMOTE_TO_VALIDATION

### Metadata
- **Run ID:** `20260307T192841_opening_range_breakout_v2_1m_holdout`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 41ade39`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T192841_opening_range_breakout_v2_1m_holdout`
- **Strategy:** `opening_range_breakout_v2`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2025-03-01 -> 2026-02-22`
- **Days Tested:** `252`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
If ORB-v2 has genuine robustness, it should still behave reasonably on the untouched MES holdout window without any rule changes.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Final untouched holdout-window run for ORB-v2 on MES using the exact frozen v2.0 rule set.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100192.50 |
| Net PnL | 192.50 |
| Total Return % | 0.1925 |
| Max Drawdown Abs | 1115.00 |
| Max Drawdown % | 1.1114 |
| Daily Sharpe Approx | 0.1366 |
| Execution Count | 300 |
| Closed Trade Count | 150 |
| Win Rate % | 47.3333 |
| Gross Profit | 7517.50 |
| Gross Loss | 7325.00 |
| Profit Factor | 1.0263 |
| Trades / Tested Day | 0.60 |
| Approx Winning Trades | 71 |
| Approx Losing Trades | 79 |
| Approx Average Winner | 105.88 |
| Approx Average Loser | 92.72 |
| Approx Winner / Loser Ratio | 1.14 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
ORB-v3B materially improved on v3A by restoring trade opportunity while preserving low drawdown. Development-window performance remains weaker than ORB-v2 on raw profitability, but the lower-drawdown profile is credible enough to justify a validation-window robustness test.

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T192841_opening_range_breakout_v2_1m_holdout`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260307T192841_opening_range_breakout_v2_1m_holdout\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260307T192841_opening_range_breakout_v2_1m_holdout\daily_equity.csv`

---

## EXP-20260307-021 | opening_range_breakout_v3 | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv3 #family/MES #interval/1m #sample/smoke #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 41ade39`
- **Report Directory:** `Config: configs/opening_range_breakout_v3_1m_smoke.json`
- **Strategy:** `opening_range_breakout_v3`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v3A may improve ORB-v2 robustness by requiring close-confirmed breakouts, stronger opening-range close location, and a cap on oversized initial structural risk.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for ORB-v3A on MES. This branch keeps ORB-v2 trade management but adds close-confirmed breakout entry, OR close location filtering, and max initial risk cap.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "entry_trigger_mode": "close",
  "or_close_location_min": 0.6,
  "max_initial_risk_ticks": 60,
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
Run failed with error:
```
Unknown strategy 'opening_range_breakout_v3'.
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/opening_range_breakout_v3_1m_smoke.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260307-022 | opening_range_breakout_v3 | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv3 #family/MES #interval/1m #sample/smoke #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 41ade39`
- **Report Directory:** `Config: configs/opening_range_breakout_v3_1m_smoke.json`
- **Strategy:** `opening_range_breakout_v3`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v3A may improve ORB-v2 robustness by requiring close-confirmed breakouts, stronger opening-range close location, and a cap on oversized initial structural risk.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for ORB-v3A on MES. This branch keeps ORB-v2 trade management but adds close-confirmed breakout entry, OR close location filtering, and max initial risk cap.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "entry_trigger_mode": "close",
  "or_close_location_min": 0.6,
  "max_initial_risk_ticks": 60,
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
Run failed with error:
```
Unknown strategy 'opening_range_breakout_v3'.
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/opening_range_breakout_v3_1m_smoke.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260307-023 | opening_range_breakout_v3 | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv3 #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260307T225809_opening_range_breakout_v3_1m_smoke`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 41ade39`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T225809_opening_range_breakout_v3_1m_smoke`
- **Strategy:** `opening_range_breakout_v3`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v3A may improve ORB-v2 robustness by requiring close-confirmed breakouts, stronger opening-range close location, and a cap on oversized initial structural risk.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for ORB-v3A on MES. This branch keeps ORB-v2 trade management but adds close-confirmed breakout entry, OR close location filtering, and max initial risk cap.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "entry_trigger_mode": "close",
  "or_close_location_min": 0.6,
  "max_initial_risk_ticks": 60,
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99868.75 |
| Net PnL | -131.25 |
| Total Return % | -0.1313 |
| Max Drawdown Abs | 222.50 |
| Max Drawdown % | 0.2225 |
| Daily Sharpe Approx | -2.3510 |
| Execution Count | 8 |
| Closed Trade Count | 4 |
| Win Rate % | 25.0000 |
| Gross Profit | 91.25 |
| Gross Loss | 222.50 |
| Profit Factor | 0.4101 |
| Trades / Tested Day | 0.12 |
| Approx Winning Trades | 1 |
| Approx Losing Trades | 3 |
| Approx Average Winner | 91.25 |
| Approx Average Loser | 74.17 |
| Approx Winner / Loser Ratio | 1.23 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T225809_opening_range_breakout_v3_1m_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260307T225809_opening_range_breakout_v3_1m_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260307T225809_opening_range_breakout_v3_1m_smoke\daily_equity.csv`

---

## EXP-20260307-024 | opening_range_breakout_v3 | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv3 #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `REJECT_AT_DEV`

### Metadata
- **Run ID:** `20260307T231235_opening_range_breakout_v3_1m_dev`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 41ade39`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T231235_opening_range_breakout_v3_1m_dev`
- **Strategy:** `opening_range_breakout_v3`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2024-02-29`
- **Days Tested:** `261`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v3 may create a more robust long-only morning breakout system on MES by combining structural OR entry, structural initial stop, cost-protected stop escalation, ATR trailing, and a broad OR-width quality filter.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Development-window run for ORB-v3 on MES. This is the design-period evaluation for the frozen v2.0 rule set.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "entry_trigger_mode": "close",
  "or_close_location_min": 0.6,
  "max_initial_risk_ticks": 60,
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100020.00 |
| Net PnL | 20.00 |
| Total Return % | 0.0200 |
| Max Drawdown Abs | 538.75 |
| Max Drawdown % | 0.5366 |
| Daily Sharpe Approx | 0.0386 |
| Execution Count | 110 |
| Closed Trade Count | 55 |
| Win Rate % | 41.8182 |
| Gross Profit | 1705.00 |
| Gross Loss | 1685.00 |
| Profit Factor | 1.0119 |
| Trades / Tested Day | 0.21 |
| Approx Winning Trades | 23 |
| Approx Losing Trades | 32 |
| Approx Average Winner | 74.13 |
| Approx Average Loser | 52.66 |
| Approx Winner / Loser Ratio | 1.41 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
ORB-v3A reduced trade count and drawdown, but also removed too much of the profit engine. Development-window performance was effectively flat after costs, so this branch does not earn promotion to validation. Next step is a controlled follow-up branch that relaxes OR close-location strictness while keeping the initial risk cap in place.

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T231235_opening_range_breakout_v3_1m_dev`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260307T231235_opening_range_breakout_v3_1m_dev\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260307T231235_opening_range_breakout_v3_1m_dev\daily_equity.csv`

---

## EXP-20260307-025 | opening_range_breakout_v3B | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv3B #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260307T232722_opening_range_breakout_v3B_1m_smoke`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 41ade39`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T232722_opening_range_breakout_v3B_1m_smoke`
- **Strategy:** `opening_range_breakout_v3B`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v3B may improve ORB-v3 robustness by requiring close-confirmed breakouts, stronger opening-range close location, and a cap on oversized initial structural risk.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for ORB-v3B on MES. This branch keeps ORB-3A trade management but adds close-confirmed breakout entry, OR close location filtering, and max initial risk cap.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "entry_trigger_mode": "close",
  "or_close_location_min": 0.5,
  "max_initial_risk_ticks": 60,
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99868.75 |
| Net PnL | -131.25 |
| Total Return % | -0.1313 |
| Max Drawdown Abs | 222.50 |
| Max Drawdown % | 0.2225 |
| Daily Sharpe Approx | -2.3510 |
| Execution Count | 8 |
| Closed Trade Count | 4 |
| Win Rate % | 25.0000 |
| Gross Profit | 91.25 |
| Gross Loss | 222.50 |
| Profit Factor | 0.4101 |
| Trades / Tested Day | 0.12 |
| Approx Winning Trades | 1 |
| Approx Losing Trades | 3 |
| Approx Average Winner | 91.25 |
| Approx Average Loser | 74.17 |
| Approx Winner / Loser Ratio | 1.23 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T232722_opening_range_breakout_v3_1m_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260307T232722_opening_range_breakout_v3_1m_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260307T232722_opening_range_breakout_v3_1m_smoke\daily_equity.csv`

---

## EXP-20260307-026 | opening_range_breakout_v3 | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv3 #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** REJECT_AT_VALIDATION

### Metadata
- **Run ID:** `20260307T233418_opening_range_breakout_v3B_1m_dev`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 41ade39`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T233418_opening_range_breakout_v3B_1m_dev`
- **Strategy:** `opening_range_breakout_v3`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2024-02-29`
- **Days Tested:** `261`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v3B may recover too much-filtered profit opportunity from v3A by relaxing the opening-range close-location threshold while preserving the max-initial-risk cap.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `ORB-v3B did not validate. Although the branch reduced drawdown and activity in development, out-of-sample validation turned clearly negative with sub-1.0 profit factor and materially worse performance than ORB-v2 on the same window. Do not continue this branch. Archive as an informative failed attempt and return to new ORB hypothesis design rather than further tuning this line.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "entry_trigger_mode": "close",
  "or_close_location_min": 0.5,
  "max_initial_risk_ticks": 60,
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100373.75 |
| Net PnL | 373.75 |
| Total Return % | 0.3737 |
| Max Drawdown Abs | 390.00 |
| Max Drawdown % | 0.3884 |
| Daily Sharpe Approx | 0.5459 |
| Execution Count | 140 |
| Closed Trade Count | 70 |
| Win Rate % | 42.8571 |
| Gross Profit | 2531.25 |
| Gross Loss | 2157.50 |
| Profit Factor | 1.1732 |
| Trades / Tested Day | 0.27 |
| Approx Winning Trades | 30 |
| Approx Losing Trades | 40 |
| Approx Average Winner | 84.38 |
| Approx Average Loser | 53.94 |
| Approx Winner / Loser Ratio | 1.56 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260307T233418_opening_range_breakout_v3B_1m_dev`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260307T233418_opening_range_breakout_v3B_1m_dev\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260307T233418_opening_range_breakout_v3B_1m_dev\daily_equity.csv`

---

## EXP-20260307-027 | unknown | unknown | unknown | FULL

**Tags:** #sample/full #status/failed #decision/invalid_run

**Status:** `FAILED`  
**Decision:** `INVALID_RUN`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 41ade39`
- **Report Directory:** `Config: configs/opening_range_breakout_v3B_1m_validation.json`
- **Strategy:** `unknown`
- **Strategy Archetype:** `unknown`
- **Family:** `unknown`
- **Interval:** `unknown`
- **Sample Type:** `FULL`
- **Date Range:** `unknown -> unknown`
- **Days Tested:** `1`
- **Instrument Mode:** `unknown`
- **Instrument Key:** `null`

### Research Question / Hypothesis
TBD

### Change Description
- **Parent Experiment:** `TBD`
- **What changed:** `TBD`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `unknown`
- **Session:** `unknown -> unknown`
- **Flatten Daily:** `unknown`
- **Flatten On Last Bar:** `unknown`
- **Initial Cash:** `unknown`
- **Contract Multiplier:** `unknown`
- **Tick Size:** `unknown`
- **Slippage Ticks:** `unknown`
- **Commission Per Side:** `unknown`

### Strategy Parameters
```json
{}
```

### Results
Run failed with error:
```
[Errno 2] No such file or directory: 'configs\\opening_range_breakout_v3B_1m_validation.json'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/opening_range_breakout_v3B_1m_validation.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260307-028 | opening_range_breakout_v3B | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv3B #family/MES #interval/1m #sample/full #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 41ade39`
- **Report Directory:** `Config: configs/opening_range_breakout_v3B_1m_validation.json`
- **Strategy:** `opening_range_breakout_v3B`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2024-03-01 -> 2025-02-28`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v3B may improve out-of-sample robustness versus ORB-v2 by preserving the max initial risk cap while relaxing the OR close-location filter enough to restore viable trade opportunity.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Validation-window run for ORB-v3B on MES. Same ORB-v3 structure as v3A, but with OR close location minimum relaxed from 0.60 to 0.50 while keeping close-confirmed breakout entry and max initial risk cap unchanged.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
Run failed with error:
```
Unknown strategy 'opening_range_breakout_v3B'.
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/opening_range_breakout_v3B_1m_validation.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260307-029 | unknown | unknown | unknown | FULL

**Tags:** #sample/full #status/failed #decision/invalid_run

**Status:** `FAILED`  
**Decision:** `INVALID_RUN`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 41ade39`
- **Report Directory:** `Config: configs/opening_range_breakout_v3B_1m_validation.json`
- **Strategy:** `unknown`
- **Strategy Archetype:** `unknown`
- **Family:** `unknown`
- **Interval:** `unknown`
- **Sample Type:** `FULL`
- **Date Range:** `unknown -> unknown`
- **Days Tested:** `1`
- **Instrument Mode:** `unknown`
- **Instrument Key:** `null`

### Research Question / Hypothesis
TBD

### Change Description
- **Parent Experiment:** `TBD`
- **What changed:** `TBD`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `unknown`
- **Session:** `unknown -> unknown`
- **Flatten Daily:** `unknown`
- **Flatten On Last Bar:** `unknown`
- **Initial Cash:** `unknown`
- **Contract Multiplier:** `unknown`
- **Tick Size:** `unknown`
- **Slippage Ticks:** `unknown`
- **Commission Per Side:** `unknown`

### Strategy Parameters
```json
{}
```

### Results
Run failed with error:
```
[Errno 2] No such file or directory: 'configs\\opening_range_breakout_v3B_1m_validation.json'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/opening_range_breakout_v3B_1m_validation.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260307-030 | unknown | unknown | unknown | FULL

**Tags:** #sample/full #status/failed #decision/invalid_run

**Status:** `FAILED`  
**Decision:** `INVALID_RUN`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-07`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 41ade39`
- **Report Directory:** `Config: configs/opening_range_breakout_v3B.json`
- **Strategy:** `unknown`
- **Strategy Archetype:** `unknown`
- **Family:** `unknown`
- **Interval:** `unknown`
- **Sample Type:** `FULL`
- **Date Range:** `unknown -> unknown`
- **Days Tested:** `1`
- **Instrument Mode:** `unknown`
- **Instrument Key:** `null`

### Research Question / Hypothesis
TBD

### Change Description
- **Parent Experiment:** `TBD`
- **What changed:** `TBD`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `unknown`
- **Session:** `unknown -> unknown`
- **Flatten Daily:** `unknown`
- **Flatten On Last Bar:** `unknown`
- **Initial Cash:** `unknown`
- **Contract Multiplier:** `unknown`
- **Tick Size:** `unknown`
- **Slippage Ticks:** `unknown`
- **Commission Per Side:** `unknown`

### Strategy Parameters
```json
{}
```

### Results
Run failed with error:
```
[Errno 2] No such file or directory: 'configs\\opening_range_breakout_v3B.json'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/opening_range_breakout_v3B.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260308-001 | unknown | unknown | unknown | FULL

**Tags:** #sample/full #status/failed #decision/invalid_run

**Status:** `FAILED`  
**Decision:** `INVALID_RUN`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 41ade39`
- **Report Directory:** `Config: configs/opening_range_breakout_v3B.json`
- **Strategy:** `unknown`
- **Strategy Archetype:** `unknown`
- **Family:** `unknown`
- **Interval:** `unknown`
- **Sample Type:** `FULL`
- **Date Range:** `unknown -> unknown`
- **Days Tested:** `1`
- **Instrument Mode:** `unknown`
- **Instrument Key:** `null`

### Research Question / Hypothesis
TBD

### Change Description
- **Parent Experiment:** `TBD`
- **What changed:** `TBD`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `unknown`
- **Session:** `unknown -> unknown`
- **Flatten Daily:** `unknown`
- **Flatten On Last Bar:** `unknown`
- **Initial Cash:** `unknown`
- **Contract Multiplier:** `unknown`
- **Tick Size:** `unknown`
- **Slippage Ticks:** `unknown`
- **Commission Per Side:** `unknown`

### Strategy Parameters
```json
{}
```

### Results
Run failed with error:
```
[Errno 2] No such file or directory: 'configs\\opening_range_breakout_v3B.json'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/opening_range_breakout_v3B.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260308-002 | opening_range_breakout_v3 | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv3 #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260308T000454_opening_range_breakout_v3B_1m_validation`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `begin_backtesting @ 41ade39`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T000454_opening_range_breakout_v3B_1m_validation`
- **Strategy:** `opening_range_breakout_v3`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2024-03-01 -> 2025-02-28`
- **Days Tested:** `257`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v3B may improve out-of-sample robustness versus ORB-v2 by preserving the max initial risk cap while relaxing the OR close-location filter enough to restore viable trade opportunity.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Validation-window run for ORB-v3B on MES. Same ORB-v3 structure as v3A, but with OR close location minimum relaxed from 0.60 to 0.50 while keeping close-confirmed breakout entry and max initial risk cap unchanged.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "entry_trigger_mode": "close",
  "or_close_location_min": 0.5,
  "max_initial_risk_ticks": 60,
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99716.25 |
| Net PnL | -283.75 |
| Total Return % | -0.2838 |
| Max Drawdown Abs | 605.00 |
| Max Drawdown % | 0.6041 |
| Daily Sharpe Approx | -0.5147 |
| Execution Count | 104 |
| Closed Trade Count | 52 |
| Win Rate % | 36.5385 |
| Gross Profit | 1545.00 |
| Gross Loss | 1828.75 |
| Profit Factor | 0.8448 |
| Trades / Tested Day | 0.20 |
| Approx Winning Trades | 19 |
| Approx Losing Trades | 33 |
| Approx Average Winner | 81.32 |
| Approx Average Loser | 55.42 |
| Approx Winner / Loser Ratio | 1.47 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T000454_opening_range_breakout_v3B_1m_validation`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260308T000454_opening_range_breakout_v3B_1m_validation\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260308T000454_opening_range_breakout_v3B_1m_validation\daily_equity.csv`

---

## EXP-20260308-003 | unknown | unknown | unknown | FULL

**Tags:** #sample/full #status/failed #decision/invalid_run

**Status:** `FAILED`  
**Decision:** `INVALID_RUN`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `Config: configs/opening_range_breakout_v2_dev_a.json`
- **Strategy:** `unknown`
- **Strategy Archetype:** `unknown`
- **Family:** `unknown`
- **Interval:** `unknown`
- **Sample Type:** `FULL`
- **Date Range:** `unknown -> unknown`
- **Days Tested:** `1`
- **Instrument Mode:** `unknown`
- **Instrument Key:** `null`

### Research Question / Hypothesis
TBD

### Change Description
- **Parent Experiment:** `TBD`
- **What changed:** `TBD`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `unknown`
- **Session:** `unknown -> unknown`
- **Flatten Daily:** `unknown`
- **Flatten On Last Bar:** `unknown`
- **Initial Cash:** `unknown`
- **Contract Multiplier:** `unknown`
- **Tick Size:** `unknown`
- **Slippage Ticks:** `unknown`
- **Commission Per Side:** `unknown`

### Strategy Parameters
```json
{}
```

### Results
Run failed with error:
```
[Errno 2] No such file or directory: 'configs\\opening_range_breakout_v2_dev_a.json'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/opening_range_breakout_v2_dev_a.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260308-004 | unknown | unknown | unknown | FULL

**Tags:** #sample/full #status/failed #decision/invalid_run

**Status:** `FAILED`  
**Decision:** `INVALID_RUN`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `Config: configs/opening_range_breakout_v2_dev_a.json`
- **Strategy:** `unknown`
- **Strategy Archetype:** `unknown`
- **Family:** `unknown`
- **Interval:** `unknown`
- **Sample Type:** `FULL`
- **Date Range:** `unknown -> unknown`
- **Days Tested:** `1`
- **Instrument Mode:** `unknown`
- **Instrument Key:** `null`

### Research Question / Hypothesis
TBD

### Change Description
- **Parent Experiment:** `TBD`
- **What changed:** `TBD`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `unknown`
- **Session:** `unknown -> unknown`
- **Flatten Daily:** `unknown`
- **Flatten On Last Bar:** `unknown`
- **Initial Cash:** `unknown`
- **Contract Multiplier:** `unknown`
- **Tick Size:** `unknown`
- **Slippage Ticks:** `unknown`
- **Commission Per Side:** `unknown`

### Strategy Parameters
```json
{}
```

### Results
Run failed with error:
```
[Errno 2] No such file or directory: 'configs\\opening_range_breakout_v2_dev_a.json'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/opening_range_breakout_v2_dev_a.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260308-005 | unknown | unknown | unknown | FULL

**Tags:** #sample/full #status/failed #decision/invalid_run

**Status:** `FAILED`  
**Decision:** `INVALID_RUN`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `Config: opening_range_breakout_v2_dev_a.json`
- **Strategy:** `unknown`
- **Strategy Archetype:** `unknown`
- **Family:** `unknown`
- **Interval:** `unknown`
- **Sample Type:** `FULL`
- **Date Range:** `unknown -> unknown`
- **Days Tested:** `1`
- **Instrument Mode:** `unknown`
- **Instrument Key:** `null`

### Research Question / Hypothesis
TBD

### Change Description
- **Parent Experiment:** `TBD`
- **What changed:** `TBD`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `unknown`
- **Session:** `unknown -> unknown`
- **Flatten Daily:** `unknown`
- **Flatten On Last Bar:** `unknown`
- **Initial Cash:** `unknown`
- **Contract Multiplier:** `unknown`
- **Tick Size:** `unknown`
- **Slippage Ticks:** `unknown`
- **Commission Per Side:** `unknown`

### Strategy Parameters
```json
{}
```

### Results
Run failed with error:
```
[Errno 2] No such file or directory: 'opening_range_breakout_v2_dev_a.json'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: opening_range_breakout_v2_dev_a.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260308-006 | unknown | unknown | unknown | FULL

**Tags:** #sample/full #status/failed #decision/invalid_run

**Status:** `FAILED`  
**Decision:** `INVALID_RUN`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `Config: opening_range_breakout_v2_dev_a.json`
- **Strategy:** `unknown`
- **Strategy Archetype:** `unknown`
- **Family:** `unknown`
- **Interval:** `unknown`
- **Sample Type:** `FULL`
- **Date Range:** `unknown -> unknown`
- **Days Tested:** `1`
- **Instrument Mode:** `unknown`
- **Instrument Key:** `null`

### Research Question / Hypothesis
TBD

### Change Description
- **Parent Experiment:** `TBD`
- **What changed:** `TBD`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `unknown`
- **Session:** `unknown -> unknown`
- **Flatten Daily:** `unknown`
- **Flatten On Last Bar:** `unknown`
- **Initial Cash:** `unknown`
- **Contract Multiplier:** `unknown`
- **Tick Size:** `unknown`
- **Slippage Ticks:** `unknown`
- **Commission Per Side:** `unknown`

### Strategy Parameters
```json
{}
```

### Results
Run failed with error:
```
[Errno 2] No such file or directory: 'opening_range_breakout_v2_dev_a.json'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: opening_range_breakout_v2_dev_a.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260308-007 | opening_range_breakout_v2 | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv2 #family/MES #interval/1m #sample/full #status/completed #decision/baseline_measurement

**Status:** `COMPLETED`  
**Decision:** `BASELINE_MEASUREMENT`

### Metadata
- **Run ID:** `20260308T122126_opening_range_breakout_v2_dev_a`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T122126_opening_range_breakout_v2_dev_a`
- **Strategy:** `opening_range_breakout_v2`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v2 benchmark split run on MES Dev-A. This establishes the discovery-slice parent baseline before any V4 context modules are introduced.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Benchmark parent run for ORB-v2 on the Dev-A discovery window. No strategy changes; this run is for split-window baseline measurement only.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100587.50 |
| Net PnL | 587.50 |
| Total Return % | 0.5875 |
| Max Drawdown Abs | 423.75 |
| Max Drawdown % | 0.4197 |
| Daily Sharpe Approx | 1.2214 |
| Execution Count | 128 |
| Closed Trade Count | 64 |
| Win Rate % | 48.4375 |
| Gross Profit | 2501.25 |
| Gross Loss | 1913.75 |
| Profit Factor | 1.3070 |
| Trades / Tested Day | 0.48 |
| Approx Winning Trades | 31 |
| Approx Losing Trades | 33 |
| Approx Average Winner | 80.69 |
| Approx Average Loser | 57.99 |
| Approx Winner / Loser Ratio | 1.39 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
Record benchmark parent performance on Dev-A before testing any V4 modules.

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T122126_opening_range_breakout_v2_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260308T122126_opening_range_breakout_v2_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260308T122126_opening_range_breakout_v2_dev_a\daily_equity.csv`

---

## EXP-20260308-008 | opening_range_breakout_v2 | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv2 #family/MES #interval/1m #sample/full #status/completed #decision/baseline_measurement

**Status:** `COMPLETED`  
**Decision:** `BASELINE_MEASUREMENT`

### Metadata
- **Run ID:** `20260308T122226_opening_range_breakout_v2_dev_b`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T122226_opening_range_breakout_v2_dev_b`
- **Strategy:** `opening_range_breakout_v2`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-09-01 -> 2024-02-29`
- **Days Tested:** `128`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v2 benchmark split run on MES Dev-B. This establishes the internal-confirm parent baseline before any V4 context modules are introduced.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Benchmark parent run for ORB-v2 on the Dev-B internal confirm window. No strategy changes; this run is for split-window baseline measurement only.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100391.25 |
| Net PnL | 391.25 |
| Total Return % | 0.3912 |
| Max Drawdown Abs | 747.50 |
| Max Drawdown % | 0.7404 |
| Daily Sharpe Approx | 0.7499 |
| Execution Count | 140 |
| Closed Trade Count | 70 |
| Win Rate % | 44.2857 |
| Gross Profit | 2846.25 |
| Gross Loss | 2455.00 |
| Profit Factor | 1.1594 |
| Trades / Tested Day | 0.55 |
| Approx Winning Trades | 31 |
| Approx Losing Trades | 39 |
| Approx Average Winner | 91.81 |
| Approx Average Loser | 62.95 |
| Approx Winner / Loser Ratio | 1.46 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
Record benchmark parent performance on Dev-B before testing any V4 modules.

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T122226_opening_range_breakout_v2_dev_b`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260308T122226_opening_range_breakout_v2_dev_b\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260308T122226_opening_range_breakout_v2_dev_b\daily_equity.csv`

---

## EXP-20260308-009 | unknown | unknown | unknown | FULL

**Tags:** #sample/full #status/failed #decision/invalid_run

**Status:** `FAILED`  
**Decision:** `INVALID_RUN`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `Config: configs/active/opening_range_breakout_v4a_smoke.json`
- **Strategy:** `unknown`
- **Strategy Archetype:** `unknown`
- **Family:** `unknown`
- **Interval:** `unknown`
- **Sample Type:** `FULL`
- **Date Range:** `unknown -> unknown`
- **Days Tested:** `1`
- **Instrument Mode:** `unknown`
- **Instrument Key:** `null`

### Research Question / Hypothesis
TBD

### Change Description
- **Parent Experiment:** `TBD`
- **What changed:** `TBD`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `unknown`
- **Session:** `unknown -> unknown`
- **Flatten Daily:** `unknown`
- **Flatten On Last Bar:** `unknown`
- **Initial Cash:** `unknown`
- **Contract Multiplier:** `unknown`
- **Tick Size:** `unknown`
- **Slippage Ticks:** `unknown`
- **Commission Per Side:** `unknown`

### Strategy Parameters
```json
{}
```

### Results
Run failed with error:
```
[Errno 2] No such file or directory: 'configs\\active\\opening_range_breakout_v4a_smoke.json'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/active/opening_range_breakout_v4a_smoke.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260308-010 | opening_range_breakout_v4 | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv4 #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260308T154918_opening_range_breakout_v4a_smoke`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T154918_opening_range_breakout_v4a_smoke`
- **Strategy:** `opening_range_breakout_v4`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v4A may improve ORB-v2 robustness by requiring the long breakout signal bar to close above RTH VWAP, filtering out weaker contextual breakouts while leaving the rest of the ORB-v2 structure unchanged.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for ORB-v4A on MES. This branch keeps ORB-v2 unchanged except for a VWAP alignment filter requiring the signal bar close to be above RTH session VWAP.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "vwap_filter_mode": "signal_close_above_vwap",
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99961.25 |
| Net PnL | -38.75 |
| Total Return % | -0.0387 |
| Max Drawdown Abs | 237.50 |
| Max Drawdown % | 0.2375 |
| Daily Sharpe Approx | -0.5102 |
| Execution Count | 14 |
| Closed Trade Count | 7 |
| Win Rate % | 42.8571 |
| Gross Profit | 255.00 |
| Gross Loss | 293.75 |
| Profit Factor | 0.8681 |
| Trades / Tested Day | 0.22 |
| Approx Winning Trades | 3 |
| Approx Losing Trades | 4 |
| Approx Average Winner | 85.00 |
| Approx Average Loser | 73.44 |
| Approx Winner / Loser Ratio | 1.16 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T154918_opening_range_breakout_v4a_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260308T154918_opening_range_breakout_v4a_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260308T154918_opening_range_breakout_v4a_smoke\daily_equity.csv`

---

## EXP-20260308-011 | opening_range_breakout_v4 | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv4 #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `REJECT_NON_CONTRIBUTORY`

### Metadata
- **Run ID:** `20260308T155123_opening_range_breakout_v4a_dev_a`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T155123_opening_range_breakout_v4a_dev_a`
- **Strategy:** `opening_range_breakout_v4`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v4A may improve ORB-v2 discovery-slice performance by filtering long breakouts that confirm below RTH VWAP, keeping only signals aligned with accepted intraday value.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Dev-A discovery run for ORB-v4A on MES. This branch keeps ORB-v2 unchanged except for a VWAP alignment filter requiring the signal bar close to be above RTH session VWAP.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "vwap_filter_mode": "signal_close_above_vwap",
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100587.50 |
| Net PnL | 587.50 |
| Total Return % | 0.5875 |
| Max Drawdown Abs | 423.75 |
| Max Drawdown % | 0.4197 |
| Daily Sharpe Approx | 1.2214 |
| Execution Count | 128 |
| Closed Trade Count | 64 |
| Win Rate % | 48.4375 |
| Gross Profit | 2501.25 |
| Gross Loss | 1913.75 |
| Profit Factor | 1.3070 |
| Trades / Tested Day | 0.48 |
| Approx Winning Trades | 31 |
| Approx Losing Trades | 33 |
| Approx Average Winner | 80.69 |
| Approx Average Loser | 57.99 |
| Approx Winner / Loser Ratio | 1.39 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
ORB-v4A produced results identical to the ORB-v2 parent on Dev-A, indicating that the signal-close-above-VWAP filter was non-binding for this strategy on the discovery slice. Reject this module in its current form and move to a more discriminating context hypothesis rather than promoting a redundant filter.

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T155123_opening_range_breakout_v4a_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260308T155123_opening_range_breakout_v4a_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260308T155123_opening_range_breakout_v4a_dev_a\daily_equity.csv`

---

## EXP-20260308-012 | opening_range_breakout_v4 | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv4 #family/MES #interval/1m #sample/smoke #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `Config: configs/active/opening_range_breakout_v4b_smoke.json`
- **Strategy:** `opening_range_breakout_v4`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v4B may improve ORB-v2 robustness by requiring the opening-range close itself to be above RTH VWAP before any long breakout is allowed, filtering out weaker morning structure before signal formation.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for ORB-v4B on MES. This branch keeps ORB-v2 unchanged except for a VWAP context filter requiring the opening-range close to be above RTH session VWAP before long breakout eligibility is allowed.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "vwap_filter_mode": "or_close_above_vwap",
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
Run failed with error:
```
vwap_filter_mode must be either 'none' or 'signal_close_above_vwap'.
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/active/opening_range_breakout_v4b_smoke.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260308-013 | opening_range_breakout_v4 | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv4 #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260308T161526_opening_range_breakout_v4b_smoke`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T161526_opening_range_breakout_v4b_smoke`
- **Strategy:** `opening_range_breakout_v4`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v4B may improve ORB-v2 robustness by requiring the opening-range close itself to be above RTH VWAP before any long breakout is allowed, filtering out weaker morning structure before signal formation.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for ORB-v4B on MES. This branch keeps ORB-v2 unchanged except for a VWAP context filter requiring the opening-range close to be above RTH session VWAP before long breakout eligibility is allowed.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "vwap_filter_mode": "or_close_above_vwap",
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99925.00 |
| Net PnL | -75.00 |
| Total Return % | -0.0750 |
| Max Drawdown Abs | 166.25 |
| Max Drawdown % | 0.1662 |
| Daily Sharpe Approx | -1.2544 |
| Execution Count | 10 |
| Closed Trade Count | 5 |
| Win Rate % | 40.0000 |
| Gross Profit | 147.50 |
| Gross Loss | 222.50 |
| Profit Factor | 0.6629 |
| Trades / Tested Day | 0.16 |
| Approx Winning Trades | 2 |
| Approx Losing Trades | 3 |
| Approx Average Winner | 73.75 |
| Approx Average Loser | 74.17 |
| Approx Winner / Loser Ratio | 0.99 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T161526_opening_range_breakout_v4b_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260308T161526_opening_range_breakout_v4b_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260308T161526_opening_range_breakout_v4b_smoke\daily_equity.csv`

---

## EXP-20260308-014 | opening_range_breakout_v4 | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv4 #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `PROMOTE_TO_DEV_B`

### Metadata
- **Run ID:** `20260308T161727_opening_range_breakout_v4b_dev_a`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T161727_opening_range_breakout_v4b_dev_a`
- **Strategy:** `opening_range_breakout_v4`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v4B may improve ORB-v2 discovery-slice performance by requiring the opening-range close to be above RTH VWAP before any long breakout day is eligible, filtering out weaker morning structure at the context stage.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Dev-A discovery run for ORB-v4B on MES. This branch keeps ORB-v2 unchanged except for a VWAP context filter requiring the opening-range close to be above RTH session VWAP before long breakout eligibility is allowed.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "vwap_filter_mode": "or_close_above_vwap",
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100368.75 |
| Net PnL | 368.75 |
| Total Return % | 0.3688 |
| Max Drawdown Abs | 252.50 |
| Max Drawdown % | 0.2512 |
| Daily Sharpe Approx | 0.9288 |
| Execution Count | 88 |
| Closed Trade Count | 44 |
| Win Rate % | 50.0000 |
| Gross Profit | 1683.75 |
| Gross Loss | 1315.00 |
| Profit Factor | 1.2804 |
| Trades / Tested Day | 0.33 |
| Approx Winning Trades | 22 |
| Approx Losing Trades | 22 |
| Approx Average Winner | 76.53 |
| Approx Average Loser | 59.77 |
| Approx Winner / Loser Ratio | 1.28 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
ORB-v4B passed the Dev-A discovery gate. Although raw net PnL and profit factor were slightly below the ORB-v2 parent, the branch materially reduced drawdown while preserving positive economics and meaningful trade count. Promote to Dev-B internal confirm to test whether the lower-drawdown context filter survives on a separate slice.

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T161727_opening_range_breakout_v4b_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260308T161727_opening_range_breakout_v4b_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260308T161727_opening_range_breakout_v4b_dev_a\daily_equity.csv`

---

## EXP-20260308-015 | opening_range_breakout_v4 | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv4 #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `REJECT_AT_DEV_B`

### Metadata
- **Run ID:** `20260308T162057_opening_range_breakout_v4b_dev_b`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T162057_opening_range_breakout_v4b_dev_b`
- **Strategy:** `opening_range_breakout_v4`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-09-01 -> 2024-02-29`
- **Days Tested:** `128`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
If the OR-close-above-VWAP context module adds real value rather than discovery-slice luck, ORB-v4B should remain economically healthy on the Dev-B internal confirm window.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Dev-B internal confirm run for ORB-v4B on MES. This branch keeps ORB-v2 unchanged except for a VWAP context filter requiring the opening-range close to be above RTH session VWAP before long breakout eligibility is allowed.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "vwap_filter_mode": "or_close_above_vwap",
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99943.75 |
| Net PnL | -56.25 |
| Total Return % | -0.0563 |
| Max Drawdown Abs | 567.50 |
| Max Drawdown % | 0.5661 |
| Daily Sharpe Approx | -0.1533 |
| Execution Count | 70 |
| Closed Trade Count | 35 |
| Win Rate % | 40.0000 |
| Gross Profit | 1276.25 |
| Gross Loss | 1332.50 |
| Profit Factor | 0.9578 |
| Trades / Tested Day | 0.27 |
| Approx Winning Trades | 14 |
| Approx Losing Trades | 21 |
| Approx Average Winner | 91.16 |
| Approx Average Loser | 63.45 |
| Approx Winner / Loser Ratio | 1.44 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
ORB-v4B did not survive internal confirmation. Although the OR-close-above-VWAP filter reduced drawdown and activity on Dev-A, Dev-B turned slightly negative with sub-1.0 profit factor and insufficient retained opportunity. Reject this branch and move to a different context-module family rather than further tuning the VWAP filter line.

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T162057_opening_range_breakout_v4b_dev_b`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260308T162057_opening_range_breakout_v4b_dev_b\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260308T162057_opening_range_breakout_v4b_dev_b\daily_equity.csv`

---

## EXP-20260308-016 | perknasty_original | MES | 5m | FULL

**Tags:** #strategy/perknastyoriginal #family/MES #interval/5m #sample/full #status/failed #decision/invalid_run

**Status:** `FAILED`  
**Decision:** `INVALID_RUN`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `Config: configs/active/perknasty_original_smoke.json`
- **Strategy:** `perknasty_original`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `5m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-03-10`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `null`

### Research Question / Hypothesis
TBD

### Change Description
- **Parent Experiment:** `TBD`
- **What changed:** `TBD`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `false`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_offset_ticks": 2.0,
  "position_size": 2,
  "tick_size": 0.25,
  "session_open": "08:30",
  "force_exit": "14:30",
  "timezone": "America/Chicago"
}
```

### Results
Run failed with error:
```
Unknown strategy 'perknasty_original'.
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/active/perknasty_original_smoke.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260308-017 | perknasty_original | MES | 5m | FULL

**Tags:** #strategy/perknastyoriginal #family/MES #interval/5m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260308T212229_perknasty_original_smoke`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `reports\20260308T212229_perknasty_original_smoke`
- **Strategy:** `perknasty_original`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `5m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-03-10`
- **Days Tested:** `10`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `null`

### Research Question / Hypothesis
TBD

### Change Description
- **Parent Experiment:** `TBD`
- **What changed:** `TBD`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `false`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_offset_ticks": 2.0,
  "position_size": 2,
  "tick_size": 0.25,
  "session_open": "08:30",
  "force_exit": "14:30",
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99982.50 |
| Net PnL | -17.50 |
| Total Return % | -0.0175 |
| Max Drawdown Abs | 260.00 |
| Max Drawdown % | 0.2594 |
| Daily Sharpe Approx | 1.1865 |
| Execution Count | 18 |
| Closed Trade Count | 9 |
| Win Rate % | 11.1111 |
| Gross Profit | 465.00 |
| Gross Loss | 482.50 |
| Profit Factor | 0.9637 |
| Trades / Tested Day | 0.90 |
| Approx Winning Trades | 1 |
| Approx Losing Trades | 8 |
| Approx Average Winner | 465.00 |
| Approx Average Loser | 60.31 |
| Approx Winner / Loser Ratio | 7.71 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `reports\20260308T212229_perknasty_original_smoke`
- **Closed Trades CSV:** `reports\20260308T212229_perknasty_original_smoke\closed_trades.csv`
- **Daily Equity CSV:** `reports\20260308T212229_perknasty_original_smoke\daily_equity.csv`

---

## EXP-20260308-018 | perknasty_original | MES | 5m | FULL

**Tags:** #strategy/perknastyoriginal #family/MES #interval/5m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260308T212433_perknasty_original_dev_a`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `reports\20260308T212433_perknasty_original_dev_a`
- **Strategy:** `perknasty_original`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `5m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `null`

### Research Question / Hypothesis
TBD

### Change Description
- **Parent Experiment:** `TBD`
- **What changed:** `TBD`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `false`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_offset_ticks": 2.0,
  "position_size": 2,
  "tick_size": 0.25,
  "session_open": "08:30",
  "force_exit": "14:30",
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 101215.00 |
| Net PnL | 1215.00 |
| Total Return % | 1.2150 |
| Max Drawdown Abs | 952.50 |
| Max Drawdown % | 0.9502 |
| Daily Sharpe Approx | 1.2909 |
| Execution Count | 246 |
| Closed Trade Count | 123 |
| Win Rate % | 20.3252 |
| Gross Profit | 5475.00 |
| Gross Loss | 4260.00 |
| Profit Factor | 1.2852 |
| Trades / Tested Day | 0.92 |
| Approx Winning Trades | 25 |
| Approx Losing Trades | 98 |
| Approx Average Winner | 219.00 |
| Approx Average Loser | 43.47 |
| Approx Winner / Loser Ratio | 5.04 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `reports\20260308T212433_perknasty_original_dev_a`
- **Closed Trades CSV:** `reports\20260308T212433_perknasty_original_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `reports\20260308T212433_perknasty_original_dev_a\daily_equity.csv`

---

## EXP-20260308-019 | perknasty_original | MES | 5m | FULL

**Tags:** #strategy/perknastyoriginal #family/MES #interval/5m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260308T212604_perknasty_original_dev_b`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `reports\20260308T212604_perknasty_original_dev_b`
- **Strategy:** `perknasty_original`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `5m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-09-01 -> 2024-02-29`
- **Days Tested:** `128`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `null`

### Research Question / Hypothesis
TBD

### Change Description
- **Parent Experiment:** `TBD`
- **What changed:** `TBD`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `false`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_offset_ticks": 2.0,
  "position_size": 2,
  "tick_size": 0.25,
  "session_open": "08:30",
  "force_exit": "14:30",
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99852.50 |
| Net PnL | -147.50 |
| Total Return % | -0.1475 |
| Max Drawdown Abs | 747.50 |
| Max Drawdown % | 0.7431 |
| Daily Sharpe Approx | -0.0811 |
| Execution Count | 242 |
| Closed Trade Count | 121 |
| Win Rate % | 22.3140 |
| Gross Profit | 3935.00 |
| Gross Loss | 4082.50 |
| Profit Factor | 0.9639 |
| Trades / Tested Day | 0.95 |
| Approx Winning Trades | 27 |
| Approx Losing Trades | 94 |
| Approx Average Winner | 145.74 |
| Approx Average Loser | 43.43 |
| Approx Winner / Loser Ratio | 3.36 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `reports\20260308T212604_perknasty_original_dev_b`
- **Closed Trades CSV:** `reports\20260308T212604_perknasty_original_dev_b\closed_trades.csv`
- **Daily Equity CSV:** `reports\20260308T212604_perknasty_original_dev_b\daily_equity.csv`

---

## EXP-20260308-020 | opening_range_breakout_v5a | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv5a #family/MES #interval/1m #sample/smoke #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `Config: configs/active/opening_range_breakout_v5a_smoke.json`
- **Strategy:** `opening_range_breakout_v5a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v2 should perform more robustly when the opening range width is constrained to a tighter healthy band relative to recent OR history, and the opening range closes strongly near its high.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for ORB-v5a on MES. This branch adds a tighter OR width band and a strict OR close-location strength filter.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.8,
  "or_width_max_factor": 1.6,
  "or_close_location_min": 0.7,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
Run failed with error:
```
'No time zone found with key America/Chicago'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/active/opening_range_breakout_v5a_smoke.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260308-021 | opening_range_breakout_v5a | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv5a #family/MES #interval/1m #sample/smoke #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `Config: configs/active/opening_range_breakout_v5a_smoke.json`
- **Strategy:** `opening_range_breakout_v5a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v2 should perform more robustly when the opening range width is constrained to a tighter healthy band relative to recent OR history, and the opening range closes strongly near its high.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for ORB-v5a on MES. This branch adds a tighter OR width band and a strict OR close-location strength filter.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.8,
  "or_width_max_factor": 1.6,
  "or_close_location_min": 0.7,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
Run failed with error:
```
Invalid Input Error: Required module 'pytz' failed to import, due to the following Python exception:
ModuleNotFoundError: No module named 'pytz'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/active/opening_range_breakout_v5a_smoke.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260308-022 | opening_range_breakout_v5a | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv5a #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260308T220135_opening_range_breakout_v5a_smoke`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T220135_opening_range_breakout_v5a_smoke`
- **Strategy:** `opening_range_breakout_v5a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v2 should perform more robustly when the opening range width is constrained to a tighter healthy band relative to recent OR history, and the opening range closes strongly near its high.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for ORB-v5a on MES. This branch adds a tighter OR width band and a strict OR close-location strength filter.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.8,
  "or_width_max_factor": 1.6,
  "or_close_location_min": 0.7,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99841.25 |
| Net PnL | -158.75 |
| Total Return % | -0.1587 |
| Max Drawdown Abs | 158.75 |
| Max Drawdown % | 0.1588 |
| Daily Sharpe Approx | -4.0999 |
| Execution Count | 4 |
| Closed Trade Count | 2 |
| Win Rate % | 0.0000 |
| Gross Profit | 0.00 |
| Gross Loss | 158.75 |
| Profit Factor | 0.0000 |
| Trades / Tested Day | 0.06 |
| Approx Winning Trades | 0 |
| Approx Losing Trades | 2 |
| Approx Average Winner | 0.00 |
| Approx Average Loser | 79.38 |
| Approx Winner / Loser Ratio | 0.00 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T220135_opening_range_breakout_v5a_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260308T220135_opening_range_breakout_v5a_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260308T220135_opening_range_breakout_v5a_smoke\daily_equity.csv`

---

## EXP-20260308-023 | opening_range_breakout_v5a | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv5a #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260308T220149_opening_range_breakout_v5a_dev_a`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T220149_opening_range_breakout_v5a_dev_a`
- **Strategy:** `opening_range_breakout_v5a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v2 should perform more robustly when the opening range width is constrained to a tighter healthy band relative to recent OR history, and the opening range closes strongly near its high.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `ORB-v5a run on MES Dev-A. Tests whether a tighter OR width band and a strict OR close-location strength filter improve performance over the parent baseline.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.8,
  "or_width_max_factor": 1.6,
  "or_close_location_min": 0.7,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99968.75 |
| Net PnL | -31.25 |
| Total Return % | -0.0313 |
| Max Drawdown Abs | 255.00 |
| Max Drawdown % | 0.2550 |
| Daily Sharpe Approx | -0.1115 |
| Execution Count | 34 |
| Closed Trade Count | 17 |
| Win Rate % | 41.1765 |
| Gross Profit | 621.25 |
| Gross Loss | 652.50 |
| Profit Factor | 0.9521 |
| Trades / Tested Day | 0.13 |
| Approx Winning Trades | 7 |
| Approx Losing Trades | 10 |
| Approx Average Winner | 88.75 |
| Approx Average Loser | 65.25 |
| Approx Winner / Loser Ratio | 1.36 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T220149_opening_range_breakout_v5a_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260308T220149_opening_range_breakout_v5a_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260308T220149_opening_range_breakout_v5a_dev_a\daily_equity.csv`

---

## EXP-20260308-024 | opening_range_breakout_v5b | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv5b #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260308T221424_opening_range_breakout_v5b_smoke`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T221424_opening_range_breakout_v5b_smoke`
- **Strategy:** `opening_range_breakout_v5b`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v2 may perform more robustly if entries are only allowed when the opening range closes strongly near its high.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `ORB-v5b smoke test. This run adds an OR close-location strength filter to the ORB-v2 parent without modifying OR width filter defaults.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "or_close_location_min": 0.7
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99868.75 |
| Net PnL | -131.25 |
| Total Return % | -0.1313 |
| Max Drawdown Abs | 222.50 |
| Max Drawdown % | 0.2225 |
| Daily Sharpe Approx | -2.3510 |
| Execution Count | 8 |
| Closed Trade Count | 4 |
| Win Rate % | 25.0000 |
| Gross Profit | 91.25 |
| Gross Loss | 222.50 |
| Profit Factor | 0.4101 |
| Trades / Tested Day | 0.12 |
| Approx Winning Trades | 1 |
| Approx Losing Trades | 3 |
| Approx Average Winner | 91.25 |
| Approx Average Loser | 74.17 |
| Approx Winner / Loser Ratio | 1.23 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T221424_opening_range_breakout_v5b_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260308T221424_opening_range_breakout_v5b_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260308T221424_opening_range_breakout_v5b_smoke\daily_equity.csv`

---

## EXP-20260308-025 | opening_range_breakout_v5b | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv5b #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260308T221446_opening_range_breakout_v5b_dev_a`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T221446_opening_range_breakout_v5b_dev_a`
- **Strategy:** `opening_range_breakout_v5b`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v2 may perform more robustly if entries are only allowed when the opening range closes strongly near its high.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `ORB-v5b run on MES Dev-A. This run adds an OR close-location strength filter to the ORB-v2 parent without modifying OR width filter defaults.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "or_close_location_min": 0.7
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100216.25 |
| Net PnL | 216.25 |
| Total Return % | 0.2163 |
| Max Drawdown Abs | 230.00 |
| Max Drawdown % | 0.2295 |
| Daily Sharpe Approx | 0.6698 |
| Execution Count | 52 |
| Closed Trade Count | 26 |
| Win Rate % | 50.0000 |
| Gross Profit | 1061.25 |
| Gross Loss | 845.00 |
| Profit Factor | 1.2559 |
| Trades / Tested Day | 0.20 |
| Approx Winning Trades | 13 |
| Approx Losing Trades | 13 |
| Approx Average Winner | 81.63 |
| Approx Average Loser | 65.00 |
| Approx Winner / Loser Ratio | 1.26 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T221446_opening_range_breakout_v5b_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260308T221446_opening_range_breakout_v5b_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260308T221446_opening_range_breakout_v5b_dev_a\daily_equity.csv`

---

## EXP-20260308-026 | opening_range_breakout_v5c | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv5c #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260308T222758_opening_range_breakout_v5c_smoke`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T222758_opening_range_breakout_v5c_smoke`
- **Strategy:** `opening_range_breakout_v5c`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v2 may perform more robustly if the opening range width is constrained to a tighter healthy band relative to recent OR history.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `ORB-v5c smoke test. This run only tightens the opening range width filter constraints.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.8,
  "or_width_max_factor": 1.6,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99933.75 |
| Net PnL | -66.25 |
| Total Return % | -0.0663 |
| Max Drawdown Abs | 173.75 |
| Max Drawdown % | 0.1737 |
| Daily Sharpe Approx | -1.0314 |
| Execution Count | 10 |
| Closed Trade Count | 5 |
| Win Rate % | 40.0000 |
| Gross Profit | 163.75 |
| Gross Loss | 230.00 |
| Profit Factor | 0.7120 |
| Trades / Tested Day | 0.16 |
| Approx Winning Trades | 2 |
| Approx Losing Trades | 3 |
| Approx Average Winner | 81.88 |
| Approx Average Loser | 76.67 |
| Approx Winner / Loser Ratio | 1.07 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T222758_opening_range_breakout_v5c_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260308T222758_opening_range_breakout_v5c_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260308T222758_opening_range_breakout_v5c_smoke\daily_equity.csv`

---

## EXP-20260308-027 | opening_range_breakout_v5c | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv5c #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260308T222819_opening_range_breakout_v5c_dev_a`
- **Run Date:** `2026-03-08`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ a6db564`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T222819_opening_range_breakout_v5c_dev_a`
- **Strategy:** `opening_range_breakout_v5c`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v2 may perform more robustly if the opening range width is constrained to a tighter healthy band relative to recent OR history.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `ORB-v5c run on MES Dev-A. This run only tightens the opening range width filter constraints.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.8,
  "or_width_max_factor": 1.6,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100231.25 |
| Net PnL | 231.25 |
| Total Return % | 0.2312 |
| Max Drawdown Abs | 470.00 |
| Max Drawdown % | 0.4675 |
| Daily Sharpe Approx | 0.5825 |
| Execution Count | 78 |
| Closed Trade Count | 39 |
| Win Rate % | 46.1538 |
| Gross Profit | 1492.50 |
| Gross Loss | 1261.25 |
| Profit Factor | 1.1833 |
| Trades / Tested Day | 0.29 |
| Approx Winning Trades | 18 |
| Approx Losing Trades | 21 |
| Approx Average Winner | 82.92 |
| Approx Average Loser | 60.06 |
| Approx Winner / Loser Ratio | 1.38 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260308T222819_opening_range_breakout_v5c_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260308T222819_opening_range_breakout_v5c_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260308T222819_opening_range_breakout_v5c_dev_a\daily_equity.csv`

---

## EXP-20260309-001 | opening_range_breakout_v6a | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv6a #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T082140_opening_range_breakout_v6a_smoke`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T082140_opening_range_breakout_v6a_smoke`
- **Strategy:** `opening_range_breakout_v6a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v6a modifies ORB-v2 by requiring a breakout bar close location >= 0.70. This ablated branch evaluates breakout bar quality.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for ORB-v6a on MES.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99961.25 |
| Net PnL | -38.75 |
| Total Return % | -0.0387 |
| Max Drawdown Abs | 237.50 |
| Max Drawdown % | 0.2375 |
| Daily Sharpe Approx | -0.5102 |
| Execution Count | 14 |
| Closed Trade Count | 7 |
| Win Rate % | 42.8571 |
| Gross Profit | 255.00 |
| Gross Loss | 293.75 |
| Profit Factor | 0.8681 |
| Trades / Tested Day | 0.22 |
| Approx Winning Trades | 3 |
| Approx Losing Trades | 4 |
| Approx Average Winner | 85.00 |
| Approx Average Loser | 73.44 |
| Approx Winner / Loser Ratio | 1.16 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T082140_opening_range_breakout_v6a_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T082140_opening_range_breakout_v6a_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T082140_opening_range_breakout_v6a_smoke\daily_equity.csv`

---

## EXP-20260309-002 | opening_range_breakout_v6a | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv6a #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T082206_opening_range_breakout_v6a_dev_a`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T082206_opening_range_breakout_v6a_dev_a`
- **Strategy:** `opening_range_breakout_v6a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v6a modifies ORB-v2 by requiring a breakout bar close location >= 0.70. This ablated branch evaluates breakout bar quality.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `ORB-v6a benchmark split run on MES Dev-A.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100687.50 |
| Net PnL | 687.50 |
| Total Return % | 0.6875 |
| Max Drawdown Abs | 320.00 |
| Max Drawdown % | 0.3170 |
| Daily Sharpe Approx | 1.4311 |
| Execution Count | 126 |
| Closed Trade Count | 63 |
| Win Rate % | 50.7937 |
| Gross Profit | 2545.00 |
| Gross Loss | 1857.50 |
| Profit Factor | 1.3701 |
| Trades / Tested Day | 0.47 |
| Approx Winning Trades | 32 |
| Approx Losing Trades | 31 |
| Approx Average Winner | 79.53 |
| Approx Average Loser | 59.92 |
| Approx Winner / Loser Ratio | 1.33 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T082206_opening_range_breakout_v6a_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T082206_opening_range_breakout_v6a_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T082206_opening_range_breakout_v6a_dev_a\daily_equity.csv`

---

## EXP-20260309-003 | opening_range_breakout_v6a | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv6a #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T090049_opening_range_breakout_v6a_smoke`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T090049_opening_range_breakout_v6a_smoke`
- **Strategy:** `opening_range_breakout_v6a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v6a modifies ORB-v2 by requiring a breakout bar close location >= 0.70. This ablated branch evaluates breakout bar quality.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for ORB-v6a on MES.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99961.25 |
| Net PnL | -38.75 |
| Total Return % | -0.0387 |
| Max Drawdown Abs | 237.50 |
| Max Drawdown % | 0.2375 |
| Daily Sharpe Approx | -0.5102 |
| Execution Count | 14 |
| Closed Trade Count | 7 |
| Win Rate % | 42.8571 |
| Gross Profit | 255.00 |
| Gross Loss | 293.75 |
| Profit Factor | 0.8681 |
| Trades / Tested Day | 0.22 |
| Approx Winning Trades | 3 |
| Approx Losing Trades | 4 |
| Approx Average Winner | 85.00 |
| Approx Average Loser | 73.44 |
| Approx Winner / Loser Ratio | 1.16 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T090049_opening_range_breakout_v6a_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T090049_opening_range_breakout_v6a_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T090049_opening_range_breakout_v6a_smoke\daily_equity.csv`

---

## EXP-20260309-004 | opening_range_breakout_v6a | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv6a #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T090108_opening_range_breakout_v6a_dev_a`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T090108_opening_range_breakout_v6a_dev_a`
- **Strategy:** `opening_range_breakout_v6a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v6a modifies ORB-v2 by requiring a breakout bar close location >= 0.70. This ablated branch evaluates breakout bar quality.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `ORB-v6a benchmark split run on MES Dev-A.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100687.50 |
| Net PnL | 687.50 |
| Total Return % | 0.6875 |
| Max Drawdown Abs | 320.00 |
| Max Drawdown % | 0.3170 |
| Daily Sharpe Approx | 1.4311 |
| Execution Count | 126 |
| Closed Trade Count | 63 |
| Win Rate % | 50.7937 |
| Gross Profit | 2545.00 |
| Gross Loss | 1857.50 |
| Profit Factor | 1.3701 |
| Trades / Tested Day | 0.47 |
| Approx Winning Trades | 32 |
| Approx Losing Trades | 31 |
| Approx Average Winner | 79.53 |
| Approx Average Loser | 59.92 |
| Approx Winner / Loser Ratio | 1.33 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T090108_opening_range_breakout_v6a_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T090108_opening_range_breakout_v6a_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T090108_opening_range_breakout_v6a_dev_a\daily_equity.csv`

---

## EXP-20260309-005 | opening_range_breakout_v6a | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv6a #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T091129_opening_range_breakout_v6a_dev_b`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T091129_opening_range_breakout_v6a_dev_b`
- **Strategy:** `opening_range_breakout_v6a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-09-01 -> 2024-02-29`
- **Days Tested:** `128`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v6a modifies ORB-v2 by requiring a breakout bar close location >= 0.70. This ablated branch evaluates breakout bar quality.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `ORB-v6a benchmark split run on MES Dev-B.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100441.25 |
| Net PnL | 441.25 |
| Total Return % | 0.4412 |
| Max Drawdown Abs | 675.00 |
| Max Drawdown % | 0.6688 |
| Daily Sharpe Approx | 0.8591 |
| Execution Count | 136 |
| Closed Trade Count | 68 |
| Win Rate % | 45.5882 |
| Gross Profit | 2802.50 |
| Gross Loss | 2361.25 |
| Profit Factor | 1.1869 |
| Trades / Tested Day | 0.53 |
| Approx Winning Trades | 31 |
| Approx Losing Trades | 37 |
| Approx Average Winner | 90.40 |
| Approx Average Loser | 63.82 |
| Approx Winner / Loser Ratio | 1.42 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T091129_opening_range_breakout_v6a_dev_b`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T091129_opening_range_breakout_v6a_dev_b\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T091129_opening_range_breakout_v6a_dev_b\daily_equity.csv`

---

## EXP-20260309-006 | opening_range_breakout_v7a | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv7a #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T094954_opening_range_breakout_v7a_smoke`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T094954_opening_range_breakout_v7a_smoke`
- **Strategy:** `opening_range_breakout_v7a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
V7A is V6A plus the close-at-trigger gate.

### Change Description
- **Parent Experiment:** `EXP-20260309-003`
- **What changed:** `V7A smoke test evaluation.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7,
  "require_signal_bar_close_at_or_above_trigger": true
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99961.25 |
| Net PnL | -38.75 |
| Total Return % | -0.0387 |
| Max Drawdown Abs | 237.50 |
| Max Drawdown % | 0.2375 |
| Daily Sharpe Approx | -0.5102 |
| Execution Count | 14 |
| Closed Trade Count | 7 |
| Win Rate % | 42.8571 |
| Gross Profit | 255.00 |
| Gross Loss | 293.75 |
| Profit Factor | 0.8681 |
| Trades / Tested Day | 0.22 |
| Approx Winning Trades | 3 |
| Approx Losing Trades | 4 |
| Approx Average Winner | 85.00 |
| Approx Average Loser | 73.44 |
| Approx Winner / Loser Ratio | 1.16 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T094954_opening_range_breakout_v7a_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T094954_opening_range_breakout_v7a_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T094954_opening_range_breakout_v7a_smoke\daily_equity.csv`

---

## EXP-20260309-007 | opening_range_breakout_v7a | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv7a #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T095003_opening_range_breakout_v7a_dev_a`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T095003_opening_range_breakout_v7a_dev_a`
- **Strategy:** `opening_range_breakout_v7a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
V7A is V6A plus the close-at-trigger gate.

### Change Description
- **Parent Experiment:** `EXP-20260309-004`
- **What changed:** `V7A Dev-A evaluation.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7,
  "require_signal_bar_close_at_or_above_trigger": true
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100687.50 |
| Net PnL | 687.50 |
| Total Return % | 0.6875 |
| Max Drawdown Abs | 320.00 |
| Max Drawdown % | 0.3170 |
| Daily Sharpe Approx | 1.4311 |
| Execution Count | 126 |
| Closed Trade Count | 63 |
| Win Rate % | 50.7937 |
| Gross Profit | 2545.00 |
| Gross Loss | 1857.50 |
| Profit Factor | 1.3701 |
| Trades / Tested Day | 0.47 |
| Approx Winning Trades | 32 |
| Approx Losing Trades | 31 |
| Approx Average Winner | 79.53 |
| Approx Average Loser | 59.92 |
| Approx Winner / Loser Ratio | 1.33 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T095003_opening_range_breakout_v7a_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T095003_opening_range_breakout_v7a_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T095003_opening_range_breakout_v7a_dev_a\daily_equity.csv`

---

## EXP-20260309-008 | opening_range_breakout_v8a | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv8a #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T113349_opening_range_breakout_v8a_smoke`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T113349_opening_range_breakout_v8a_smoke`
- **Strategy:** `opening_range_breakout_v8a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
V8A tests whether performance improves if the signal bar must also have enough real bullish body (>= 0.30).

### Change Description
- **Parent Experiment:** `EXP-20260309-003`
- **What changed:** `V8A smoke test evaluation.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7,
  "breakout_bar_body_fraction_min": 0.3
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99950.00 |
| Net PnL | -50.00 |
| Total Return % | -0.0500 |
| Max Drawdown Abs | 248.75 |
| Max Drawdown % | 0.2488 |
| Daily Sharpe Approx | -0.6681 |
| Execution Count | 14 |
| Closed Trade Count | 7 |
| Win Rate % | 42.8571 |
| Gross Profit | 243.75 |
| Gross Loss | 293.75 |
| Profit Factor | 0.8298 |
| Trades / Tested Day | 0.22 |
| Approx Winning Trades | 3 |
| Approx Losing Trades | 4 |
| Approx Average Winner | 81.25 |
| Approx Average Loser | 73.44 |
| Approx Winner / Loser Ratio | 1.11 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T113349_opening_range_breakout_v8a_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T113349_opening_range_breakout_v8a_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T113349_opening_range_breakout_v8a_smoke\daily_equity.csv`

---

## EXP-20260309-009 | opening_range_breakout_v8a | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv8a #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T113507_opening_range_breakout_v8a_dev_a`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T113507_opening_range_breakout_v8a_dev_a`
- **Strategy:** `opening_range_breakout_v8a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
V8A tests whether performance improves if the signal bar must also have enough real bullish body (>= 0.30).

### Change Description
- **Parent Experiment:** `EXP-20260309-004`
- **What changed:** `V8A Dev-A test evaluation.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7,
  "breakout_bar_body_fraction_min": 0.3
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100661.25 |
| Net PnL | 661.25 |
| Total Return % | 0.6612 |
| Max Drawdown Abs | 332.50 |
| Max Drawdown % | 0.3294 |
| Daily Sharpe Approx | 1.3744 |
| Execution Count | 126 |
| Closed Trade Count | 63 |
| Win Rate % | 50.7937 |
| Gross Profit | 2533.75 |
| Gross Loss | 1872.50 |
| Profit Factor | 1.3531 |
| Trades / Tested Day | 0.47 |
| Approx Winning Trades | 32 |
| Approx Losing Trades | 31 |
| Approx Average Winner | 79.18 |
| Approx Average Loser | 60.40 |
| Approx Winner / Loser Ratio | 1.31 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T113507_opening_range_breakout_v8a_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T113507_opening_range_breakout_v8a_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T113507_opening_range_breakout_v8a_dev_a\daily_equity.csv`

---

## EXP-20260309-010 | opening_range_breakout_v9a | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv9a #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T114814_opening_range_breakout_v9a_smoke`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T114814_opening_range_breakout_v9a_smoke`
- **Strategy:** `opening_range_breakout_v9a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
V9A tests whether performance improves if signal bars are rejected when they close too far above the trigger relative to OR width.

### Change Description
- **Parent Experiment:** `EXP-20260309-003`
- **What changed:** `V9A smoke test evaluation.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7,
  "signal_bar_extension_from_trigger_max": 0.25
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99961.25 |
| Net PnL | -38.75 |
| Total Return % | -0.0387 |
| Max Drawdown Abs | 237.50 |
| Max Drawdown % | 0.2375 |
| Daily Sharpe Approx | -0.5102 |
| Execution Count | 14 |
| Closed Trade Count | 7 |
| Win Rate % | 42.8571 |
| Gross Profit | 255.00 |
| Gross Loss | 293.75 |
| Profit Factor | 0.8681 |
| Trades / Tested Day | 0.22 |
| Approx Winning Trades | 3 |
| Approx Losing Trades | 4 |
| Approx Average Winner | 85.00 |
| Approx Average Loser | 73.44 |
| Approx Winner / Loser Ratio | 1.16 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T114814_opening_range_breakout_v9a_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T114814_opening_range_breakout_v9a_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T114814_opening_range_breakout_v9a_smoke\daily_equity.csv`

---

## EXP-20260309-011 | opening_range_breakout_v9a | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv9a #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T114835_opening_range_breakout_v9a_dev_a`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T114835_opening_range_breakout_v9a_dev_a`
- **Strategy:** `opening_range_breakout_v9a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
V9A tests whether performance improves if signal bars are rejected when they close too far above the trigger relative to OR width.

### Change Description
- **Parent Experiment:** `EXP-20260309-004`
- **What changed:** `V9A Dev-A test evaluation.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7,
  "signal_bar_extension_from_trigger_max": 0.25
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100572.50 |
| Net PnL | 572.50 |
| Total Return % | 0.5725 |
| Max Drawdown Abs | 320.00 |
| Max Drawdown % | 0.3173 |
| Daily Sharpe Approx | 1.1958 |
| Execution Count | 124 |
| Closed Trade Count | 62 |
| Win Rate % | 48.3871 |
| Gross Profit | 2435.00 |
| Gross Loss | 1862.50 |
| Profit Factor | 1.3074 |
| Trades / Tested Day | 0.47 |
| Approx Winning Trades | 30 |
| Approx Losing Trades | 32 |
| Approx Average Winner | 81.17 |
| Approx Average Loser | 58.20 |
| Approx Winner / Loser Ratio | 1.39 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T114835_opening_range_breakout_v9a_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T114835_opening_range_breakout_v9a_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T114835_opening_range_breakout_v9a_dev_a\daily_equity.csv`

---

## EXP-20260309-012 | opening_range_breakout_v10a | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv10a #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T122128_opening_range_breakout_v10a_smoke`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T122128_opening_range_breakout_v10a_smoke`
- **Strategy:** `opening_range_breakout_v10a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
V10A tests whether performance improves if the signal bar must occur within the first 6 completed bars after OR completion.

### Change Description
- **Parent Experiment:** `EXP-20260309-003`
- **What changed:** `V10A smoke test evaluation.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7,
  "max_signal_bars_after_or_completion": 6
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99841.25 |
| Net PnL | -158.75 |
| Total Return % | -0.1587 |
| Max Drawdown Abs | 158.75 |
| Max Drawdown % | 0.1588 |
| Daily Sharpe Approx | -4.0999 |
| Execution Count | 4 |
| Closed Trade Count | 2 |
| Win Rate % | 0.0000 |
| Gross Profit | 0.00 |
| Gross Loss | 158.75 |
| Profit Factor | 0.0000 |
| Trades / Tested Day | 0.06 |
| Approx Winning Trades | 0 |
| Approx Losing Trades | 2 |
| Approx Average Winner | 0.00 |
| Approx Average Loser | 79.38 |
| Approx Winner / Loser Ratio | 0.00 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T122128_opening_range_breakout_v10a_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T122128_opening_range_breakout_v10a_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T122128_opening_range_breakout_v10a_smoke\daily_equity.csv`

---

## EXP-20260309-013 | opening_range_breakout_v10a | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv10a #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T123024_opening_range_breakout_v10a_dev_a`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T123024_opening_range_breakout_v10a_dev_a`
- **Strategy:** `opening_range_breakout_v10a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
V10A tests whether performance improves if the signal bar must occur within the first 6 completed bars after OR completion.

### Change Description
- **Parent Experiment:** `EXP-20260309-004`
- **What changed:** `V10A Dev-A test evaluation.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7,
  "max_signal_bars_after_or_completion": 6
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99918.75 |
| Net PnL | -81.25 |
| Total Return % | -0.0812 |
| Max Drawdown Abs | 347.50 |
| Max Drawdown % | 0.3475 |
| Daily Sharpe Approx | -0.2742 |
| Execution Count | 44 |
| Closed Trade Count | 22 |
| Win Rate % | 45.4545 |
| Gross Profit | 743.75 |
| Gross Loss | 825.00 |
| Profit Factor | 0.9015 |
| Trades / Tested Day | 0.17 |
| Approx Winning Trades | 10 |
| Approx Losing Trades | 12 |
| Approx Average Winner | 74.38 |
| Approx Average Loser | 68.75 |
| Approx Winner / Loser Ratio | 1.08 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T123024_opening_range_breakout_v10a_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T123024_opening_range_breakout_v10a_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T123024_opening_range_breakout_v10a_dev_a\daily_equity.csv`

---

## EXP-20260309-014 | opening_range_breakout_v11a | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv11a #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T133259_opening_range_breakout_v11a_smoke`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T133259_opening_range_breakout_v11a_smoke`
- **Strategy:** `opening_range_breakout_v11a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
V11A tests whether performance improves if a newly opened long position is exited early when the first completed bar after entry closes back below the original breakout trigger.

### Change Description
- **Parent Experiment:** `EXP-20260309-003`
- **What changed:** `V11A smoke test evaluation.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7,
  "enable_first_post_entry_close_below_trigger_exit": true
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99961.25 |
| Net PnL | -38.75 |
| Total Return % | -0.0387 |
| Max Drawdown Abs | 237.50 |
| Max Drawdown % | 0.2375 |
| Daily Sharpe Approx | -0.5102 |
| Execution Count | 14 |
| Closed Trade Count | 7 |
| Win Rate % | 42.8571 |
| Gross Profit | 255.00 |
| Gross Loss | 293.75 |
| Profit Factor | 0.8681 |
| Trades / Tested Day | 0.22 |
| Approx Winning Trades | 3 |
| Approx Losing Trades | 4 |
| Approx Average Winner | 85.00 |
| Approx Average Loser | 73.44 |
| Approx Winner / Loser Ratio | 1.16 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T133259_opening_range_breakout_v11a_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T133259_opening_range_breakout_v11a_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T133259_opening_range_breakout_v11a_smoke\daily_equity.csv`

---

## EXP-20260309-015 | opening_range_breakout_v6a | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv6a #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T133311_opening_range_breakout_v6a_dev_a`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T133311_opening_range_breakout_v6a_dev_a`
- **Strategy:** `opening_range_breakout_v6a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v6a modifies ORB-v2 by requiring a breakout bar close location >= 0.70. This ablated branch evaluates breakout bar quality.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `ORB-v6a benchmark split run on MES Dev-A.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100687.50 |
| Net PnL | 687.50 |
| Total Return % | 0.6875 |
| Max Drawdown Abs | 320.00 |
| Max Drawdown % | 0.3170 |
| Daily Sharpe Approx | 1.4311 |
| Execution Count | 126 |
| Closed Trade Count | 63 |
| Win Rate % | 50.7937 |
| Gross Profit | 2545.00 |
| Gross Loss | 1857.50 |
| Profit Factor | 1.3701 |
| Trades / Tested Day | 0.47 |
| Approx Winning Trades | 32 |
| Approx Losing Trades | 31 |
| Approx Average Winner | 79.53 |
| Approx Average Loser | 59.92 |
| Approx Winner / Loser Ratio | 1.33 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T133311_opening_range_breakout_v6a_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T133311_opening_range_breakout_v6a_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T133311_opening_range_breakout_v6a_dev_a\daily_equity.csv`

---

## EXP-20260309-016 | opening_range_breakout_v6a | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv6a #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T133337_opening_range_breakout_v6a_dev_a`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T133337_opening_range_breakout_v6a_dev_a`
- **Strategy:** `opening_range_breakout_v6a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v6a modifies ORB-v2 by requiring a breakout bar close location >= 0.70. This ablated branch evaluates breakout bar quality.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `ORB-v6a benchmark split run on MES Dev-A.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100687.50 |
| Net PnL | 687.50 |
| Total Return % | 0.6875 |
| Max Drawdown Abs | 320.00 |
| Max Drawdown % | 0.3170 |
| Daily Sharpe Approx | 1.4311 |
| Execution Count | 126 |
| Closed Trade Count | 63 |
| Win Rate % | 50.7937 |
| Gross Profit | 2545.00 |
| Gross Loss | 1857.50 |
| Profit Factor | 1.3701 |
| Trades / Tested Day | 0.47 |
| Approx Winning Trades | 32 |
| Approx Losing Trades | 31 |
| Approx Average Winner | 79.53 |
| Approx Average Loser | 59.92 |
| Approx Winner / Loser Ratio | 1.33 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T133337_opening_range_breakout_v6a_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T133337_opening_range_breakout_v6a_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T133337_opening_range_breakout_v6a_dev_a\daily_equity.csv`

---

## EXP-20260309-017 | opening_range_breakout_v11a | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv11a #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T133459_opening_range_breakout_v11a_dev_a`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T133459_opening_range_breakout_v11a_dev_a`
- **Strategy:** `opening_range_breakout_v11a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
V11A tests whether performance improves if a newly opened long position is exited early when the first completed bar after entry closes back below the original breakout trigger.

### Change Description
- **Parent Experiment:** `EXP-20260309-004`
- **What changed:** `V11A Dev-A test evaluation.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7,
  "enable_first_post_entry_close_below_trigger_exit": true
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100687.50 |
| Net PnL | 687.50 |
| Total Return % | 0.6875 |
| Max Drawdown Abs | 320.00 |
| Max Drawdown % | 0.3170 |
| Daily Sharpe Approx | 1.4311 |
| Execution Count | 126 |
| Closed Trade Count | 63 |
| Win Rate % | 50.7937 |
| Gross Profit | 2545.00 |
| Gross Loss | 1857.50 |
| Profit Factor | 1.3701 |
| Trades / Tested Day | 0.47 |
| Approx Winning Trades | 32 |
| Approx Losing Trades | 31 |
| Approx Average Winner | 79.53 |
| Approx Average Loser | 59.92 |
| Approx Winner / Loser Ratio | 1.33 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T133459_opening_range_breakout_v11a_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T133459_opening_range_breakout_v11a_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T133459_opening_range_breakout_v11a_dev_a\daily_equity.csv`

---

## EXP-20260309-018 | forb_reversal_v1 | MES | 1m | SMOKE

**Tags:** #strategy/forbreversalv1 #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T171817_forb_reversal_v1_smoke`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T171817_forb_reversal_v1_smoke`
- **Strategy:** `forb_reversal_v1`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Base parameterization for the initial failed ORB reversal parent family candidate.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for forb_reversal_v1 on MES.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "time_stop": "13:30",
  "timezone": "America/Chicago",
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99803.75 |
| Net PnL | -196.25 |
| Total Return % | -0.1962 |
| Max Drawdown Abs | 311.25 |
| Max Drawdown % | 0.3111 |
| Daily Sharpe Approx | -4.0883 |
| Execution Count | 54 |
| Closed Trade Count | 27 |
| Win Rate % | 29.6296 |
| Gross Profit | 288.75 |
| Gross Loss | 485.00 |
| Profit Factor | 0.5954 |
| Trades / Tested Day | 0.84 |
| Approx Winning Trades | 8 |
| Approx Losing Trades | 19 |
| Approx Average Winner | 36.09 |
| Approx Average Loser | 25.53 |
| Approx Winner / Loser Ratio | 1.41 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T171817_forb_reversal_v1_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T171817_forb_reversal_v1_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T171817_forb_reversal_v1_smoke\daily_equity.csv`

---

## EXP-20260309-019 | forb_reversal_v1 | MES | 1m | FULL

**Tags:** #strategy/forbreversalv1 #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T171844_forb_reversal_v1_dev_a`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T171844_forb_reversal_v1_dev_a`
- **Strategy:** `forb_reversal_v1`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Base parameterization for the initial failed ORB reversal parent family candidate.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `forb_reversal_v1 evaluated on Dev-A.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "time_stop": "13:30",
  "timezone": "America/Chicago",
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99283.75 |
| Net PnL | -716.25 |
| Total Return % | -0.7162 |
| Max Drawdown Abs | 808.75 |
| Max Drawdown % | 0.8083 |
| Daily Sharpe Approx | -3.4800 |
| Execution Count | 192 |
| Closed Trade Count | 96 |
| Win Rate % | 21.8750 |
| Gross Profit | 897.50 |
| Gross Loss | 1613.75 |
| Profit Factor | 0.5562 |
| Trades / Tested Day | 0.72 |
| Approx Winning Trades | 21 |
| Approx Losing Trades | 75 |
| Approx Average Winner | 42.74 |
| Approx Average Loser | 21.52 |
| Approx Winner / Loser Ratio | 1.99 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T171844_forb_reversal_v1_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T171844_forb_reversal_v1_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T171844_forb_reversal_v1_dev_a\daily_equity.csv`

---

## EXP-20260309-020 | odpc_v1 | MES | 1m | SMOKE

**Tags:** #strategy/odpcv1 #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T173616_odpc_v1_smoke`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T173616_odpc_v1_smoke`
- **Strategy:** `odpc_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Base parameterization for the initial opening drive pullback continuation parent family candidate.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for odpc_v1 on MES.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "time_stop": "13:30",
  "timezone": "America/Chicago",
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99636.25 |
| Net PnL | -363.75 |
| Total Return % | -0.3637 |
| Max Drawdown Abs | 423.75 |
| Max Drawdown % | 0.4238 |
| Daily Sharpe Approx | -5.3334 |
| Execution Count | 50 |
| Closed Trade Count | 25 |
| Win Rate % | 20.0000 |
| Gross Profit | 266.25 |
| Gross Loss | 630.00 |
| Profit Factor | 0.4226 |
| Trades / Tested Day | 0.78 |
| Approx Winning Trades | 5 |
| Approx Losing Trades | 20 |
| Approx Average Winner | 53.25 |
| Approx Average Loser | 31.50 |
| Approx Winner / Loser Ratio | 1.69 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T173616_odpc_v1_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T173616_odpc_v1_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T173616_odpc_v1_smoke\daily_equity.csv`

---

## EXP-20260309-021 | odpc_v1 | MES | 1m | FULL

**Tags:** #strategy/odpcv1 #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T173634_odpc_v1_dev_a`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T173634_odpc_v1_dev_a`
- **Strategy:** `odpc_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Base parameterization for the initial opening drive pullback continuation parent family candidate.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `odpc_v1 evaluated on Dev-A.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "time_stop": "13:30",
  "timezone": "America/Chicago",
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99590.00 |
| Net PnL | -410.00 |
| Total Return % | -0.4100 |
| Max Drawdown Abs | 423.75 |
| Max Drawdown % | 0.4238 |
| Daily Sharpe Approx | -1.5907 |
| Execution Count | 188 |
| Closed Trade Count | 94 |
| Win Rate % | 27.6596 |
| Gross Profit | 1235.00 |
| Gross Loss | 1645.00 |
| Profit Factor | 0.7508 |
| Trades / Tested Day | 0.71 |
| Approx Winning Trades | 26 |
| Approx Losing Trades | 68 |
| Approx Average Winner | 47.50 |
| Approx Average Loser | 24.19 |
| Approx Winner / Loser Ratio | 1.96 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T173634_odpc_v1_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T173634_odpc_v1_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T173634_odpc_v1_dev_a\daily_equity.csv`

---

## EXP-20260309-022 | opening_range_breakout_v6a | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv6a #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T185051_opening_range_breakout_v6a_smoke`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T185051_opening_range_breakout_v6a_smoke`
- **Strategy:** `opening_range_breakout_v6a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v6a modifies ORB-v2 by requiring a breakout bar close location >= 0.70. This ablated branch evaluates breakout bar quality.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for ORB-v6a on MES.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99961.25 |
| Net PnL | -38.75 |
| Total Return % | -0.0387 |
| Max Drawdown Abs | 237.50 |
| Max Drawdown % | 0.2375 |
| Daily Sharpe Approx | -0.5102 |
| Execution Count | 14 |
| Closed Trade Count | 7 |
| Win Rate % | 42.8571 |
| Gross Profit | 255.00 |
| Gross Loss | 293.75 |
| Profit Factor | 0.8681 |
| Trades / Tested Day | 0.22 |
| Approx Winning Trades | 3 |
| Approx Losing Trades | 4 |
| Approx Average Winner | 85.00 |
| Approx Average Loser | 73.44 |
| Approx Winner / Loser Ratio | 1.16 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T185051_opening_range_breakout_v6a_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T185051_opening_range_breakout_v6a_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T185051_opening_range_breakout_v6a_smoke\daily_equity.csv`

---

## EXP-20260309-023 | opening_range_breakout_v6a | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv6a #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T185157_opening_range_breakout_v6a_smoke`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T185157_opening_range_breakout_v6a_smoke`
- **Strategy:** `opening_range_breakout_v6a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v6a modifies ORB-v2 by requiring a breakout bar close location >= 0.70. This ablated branch evaluates breakout bar quality.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for ORB-v6a on MES.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99961.25 |
| Net PnL | -38.75 |
| Total Return % | -0.0387 |
| Max Drawdown Abs | 237.50 |
| Max Drawdown % | 0.2375 |
| Daily Sharpe Approx | -0.5102 |
| Execution Count | 14 |
| Closed Trade Count | 7 |
| Win Rate % | 42.8571 |
| Gross Profit | 255.00 |
| Gross Loss | 293.75 |
| Profit Factor | 0.8681 |
| Trades / Tested Day | 0.22 |
| Approx Winning Trades | 3 |
| Approx Losing Trades | 4 |
| Approx Average Winner | 85.00 |
| Approx Average Loser | 73.44 |
| Approx Winner / Loser Ratio | 1.16 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T185157_opening_range_breakout_v6a_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T185157_opening_range_breakout_v6a_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T185157_opening_range_breakout_v6a_smoke\daily_equity.csv`

---

## EXP-20260309-024 | opening_range_breakout_v6a | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv6a #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T185654_opening_range_breakout_v6a_dev_a`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T185654_opening_range_breakout_v6a_dev_a`
- **Strategy:** `opening_range_breakout_v6a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v6a modifies ORB-v2 by requiring a breakout bar close location >= 0.70. This ablated branch evaluates breakout bar quality.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `ORB-v6a benchmark split run on MES Dev-A.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100687.50 |
| Net PnL | 687.50 |
| Total Return % | 0.6875 |
| Max Drawdown Abs | 320.00 |
| Max Drawdown % | 0.3170 |
| Daily Sharpe Approx | 1.4311 |
| Execution Count | 126 |
| Closed Trade Count | 63 |
| Win Rate % | 50.7937 |
| Gross Profit | 2545.00 |
| Gross Loss | 1857.50 |
| Profit Factor | 1.3701 |
| Trades / Tested Day | 0.47 |
| Approx Winning Trades | 32 |
| Approx Losing Trades | 31 |
| Approx Average Winner | 79.53 |
| Approx Average Loser | 59.92 |
| Approx Winner / Loser Ratio | 1.33 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T185654_opening_range_breakout_v6a_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T185654_opening_range_breakout_v6a_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T185654_opening_range_breakout_v6a_dev_a\daily_equity.csv`

---

## EXP-20260309-025 | opening_range_breakout_v6a | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv6a #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T185710_opening_range_breakout_v6a_dev_b`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T185710_opening_range_breakout_v6a_dev_b`
- **Strategy:** `opening_range_breakout_v6a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-09-01 -> 2024-02-29`
- **Days Tested:** `128`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v6a modifies ORB-v2 by requiring a breakout bar close location >= 0.70. This ablated branch evaluates breakout bar quality.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `ORB-v6a benchmark split run on MES Dev-B.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100441.25 |
| Net PnL | 441.25 |
| Total Return % | 0.4412 |
| Max Drawdown Abs | 675.00 |
| Max Drawdown % | 0.6688 |
| Daily Sharpe Approx | 0.8591 |
| Execution Count | 136 |
| Closed Trade Count | 68 |
| Win Rate % | 45.5882 |
| Gross Profit | 2802.50 |
| Gross Loss | 2361.25 |
| Profit Factor | 1.1869 |
| Trades / Tested Day | 0.53 |
| Approx Winning Trades | 31 |
| Approx Losing Trades | 37 |
| Approx Average Winner | 90.40 |
| Approx Average Loser | 63.82 |
| Approx Winner / Loser Ratio | 1.42 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T185710_opening_range_breakout_v6a_dev_b`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T185710_opening_range_breakout_v6a_dev_b\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T185710_opening_range_breakout_v6a_dev_b\daily_equity.csv`

---

## EXP-20260309-026 | gir_v1 | MES | 1m | SMOKE

**Tags:** #strategy/girv1 #family/MES #interval/1m #sample/smoke #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `Config: configs\active\gir_v1_smoke.json`
- **Strategy:** `gir_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Gap up days after bearish prior read exhaustion and offer short trend

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for gir_v1 on MES.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:15`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "atr_period": 14,
  "gap_threshold_atr": 1.0,
  "min_gap_atr": 0.5,
  "opening_drive_minutes": 15,
  "time_stop_minutes": 120,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "session_end": "15:15",
  "timezone": "America/Chicago",
  "allow_long": false,
  "allow_short": true
}
```

### Results
Run failed with error:
```
unsupported format string passed to NoneType.__format__
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs\active\gir_v1_smoke.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260309-027 | gir_v1 | MES | 1m | SMOKE

**Tags:** #strategy/girv1 #family/MES #interval/1m #sample/smoke #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `Config: configs\active\gir_v1_smoke.json`
- **Strategy:** `gir_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Gap up days after bearish prior read exhaustion and offer short trend

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for gir_v1 on MES.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:15`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "atr_period": 14,
  "gap_threshold_atr": 1.0,
  "min_gap_atr": 0.5,
  "opening_drive_minutes": 15,
  "time_stop_minutes": 120,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "session_end": "15:15",
  "timezone": "America/Chicago",
  "allow_long": false,
  "allow_short": true
}
```

### Results
Run failed with error:
```
unsupported format string passed to NoneType.__format__
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs\active\gir_v1_smoke.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260309-028 | gir_v1 | MES | 1m | SMOKE

**Tags:** #strategy/girv1 #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T190348_gir_v1_smoke`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T190348_gir_v1_smoke`
- **Strategy:** `gir_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Gap up days after bearish prior read exhaustion and offer short trend

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for gir_v1 on MES.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:15`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "atr_period": 14,
  "gap_threshold_atr": 1.0,
  "min_gap_atr": 0.5,
  "opening_drive_minutes": 15,
  "time_stop_minutes": 120,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "session_end": "15:15",
  "timezone": "America/Chicago",
  "allow_long": false,
  "allow_short": true
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100305.00 |
| Net PnL | 305.00 |
| Total Return % | 0.3050 |
| Max Drawdown Abs | 0.00 |
| Max Drawdown % | N/A |
| Daily Sharpe Approx | 5.8736 |
| Execution Count | 10 |
| Closed Trade Count | 5 |
| Win Rate % | 100.0000 |
| Gross Profit | 305.00 |
| Gross Loss | -0.00 |
| Profit Factor | N/A |
| Trades / Tested Day | 0.16 |
| Approx Winning Trades | 5 |
| Approx Losing Trades | 0 |
| Approx Average Winner | 61.00 |
| Approx Average Loser | 0.00 |
| Approx Winner / Loser Ratio | 0.00 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T190348_gir_v1_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T190348_gir_v1_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T190348_gir_v1_smoke\daily_equity.csv`

---

## EXP-20260309-029 | gir_v1 | MES | 1m | FULL

**Tags:** #strategy/girv1 #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T190409_gir_v1_dev_a`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T190409_gir_v1_dev_a`
- **Strategy:** `gir_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Gap up days after bearish prior read exhaustion and offer short trend

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Dev-A test for gir_v1 on MES.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:15`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "atr_period": 14,
  "gap_threshold_atr": 1.0,
  "min_gap_atr": 0.5,
  "opening_drive_minutes": 15,
  "time_stop_minutes": 120,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "session_end": "15:15",
  "timezone": "America/Chicago",
  "allow_long": false,
  "allow_short": true
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100027.50 |
| Net PnL | 27.50 |
| Total Return % | 0.0275 |
| Max Drawdown Abs | 436.25 |
| Max Drawdown % | 0.43 |
| Daily Sharpe Approx | 0.1348 |
| Execution Count | 52 |
| Closed Trade Count | 26 |
| Win Rate % | 65.3846 |
| Gross Profit | 637.50 |
| Gross Loss | 610.00 |
| Profit Factor | 1.0451 |
| Trades / Tested Day | 0.20 |
| Approx Winning Trades | 17 |
| Approx Losing Trades | 9 |
| Approx Average Winner | 37.50 |
| Approx Average Loser | 67.78 |
| Approx Winner / Loser Ratio | 0.55 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T190409_gir_v1_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T190409_gir_v1_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T190409_gir_v1_dev_a\daily_equity.csv`

---

## EXP-20260309-030 | opening_range_breakout_v6a | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv6a #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T190938_opening_range_breakout_v6a_smoke`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T190938_opening_range_breakout_v6a_smoke`
- **Strategy:** `opening_range_breakout_v6a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v6a modifies ORB-v2 by requiring a breakout bar close location >= 0.70. This ablated branch evaluates breakout bar quality.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for ORB-v6a on MES.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99961.25 |
| Net PnL | -38.75 |
| Total Return % | -0.0387 |
| Max Drawdown Abs | 237.50 |
| Max Drawdown % | 0.24 |
| Daily Sharpe Approx | -0.5102 |
| Execution Count | 14 |
| Closed Trade Count | 7 |
| Win Rate % | 42.8571 |
| Gross Profit | 255.00 |
| Gross Loss | 293.75 |
| Profit Factor | 0.8681 |
| Trades / Tested Day | 0.22 |
| Approx Winning Trades | 3 |
| Approx Losing Trades | 4 |
| Approx Average Winner | 85.00 |
| Approx Average Loser | 73.44 |
| Approx Winner / Loser Ratio | 1.16 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T190938_opening_range_breakout_v6a_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T190938_opening_range_breakout_v6a_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T190938_opening_range_breakout_v6a_smoke\daily_equity.csv`

---

## EXP-20260309-031 | opening_range_breakout_v6a | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv6a #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T190952_opening_range_breakout_v6a_dev_a`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T190952_opening_range_breakout_v6a_dev_a`
- **Strategy:** `opening_range_breakout_v6a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v6a modifies ORB-v2 by requiring a breakout bar close location >= 0.70. This ablated branch evaluates breakout bar quality.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `ORB-v6a benchmark split run on MES Dev-A.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100687.50 |
| Net PnL | 687.50 |
| Total Return % | 0.6875 |
| Max Drawdown Abs | 320.00 |
| Max Drawdown % | 0.32 |
| Daily Sharpe Approx | 1.4311 |
| Execution Count | 126 |
| Closed Trade Count | 63 |
| Win Rate % | 50.7937 |
| Gross Profit | 2545.00 |
| Gross Loss | 1857.50 |
| Profit Factor | 1.3701 |
| Trades / Tested Day | 0.47 |
| Approx Winning Trades | 32 |
| Approx Losing Trades | 31 |
| Approx Average Winner | 79.53 |
| Approx Average Loser | 59.92 |
| Approx Winner / Loser Ratio | 1.33 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T190952_opening_range_breakout_v6a_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T190952_opening_range_breakout_v6a_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T190952_opening_range_breakout_v6a_dev_a\daily_equity.csv`

---

## EXP-20260309-032 | opening_range_breakout_v6a | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv6a #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T191007_opening_range_breakout_v6a_dev_b`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T191007_opening_range_breakout_v6a_dev_b`
- **Strategy:** `opening_range_breakout_v6a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-09-01 -> 2024-02-29`
- **Days Tested:** `128`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v6a modifies ORB-v2 by requiring a breakout bar close location >= 0.70. This ablated branch evaluates breakout bar quality.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `ORB-v6a benchmark split run on MES Dev-B.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.5,
  "or_width_max_factor": 2.0,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0,
  "breakout_bar_close_location_min": 0.7
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100441.25 |
| Net PnL | 441.25 |
| Total Return % | 0.4412 |
| Max Drawdown Abs | 675.00 |
| Max Drawdown % | 0.67 |
| Daily Sharpe Approx | 0.8591 |
| Execution Count | 136 |
| Closed Trade Count | 68 |
| Win Rate % | 45.5882 |
| Gross Profit | 2802.50 |
| Gross Loss | 2361.25 |
| Profit Factor | 1.1869 |
| Trades / Tested Day | 0.53 |
| Approx Winning Trades | 31 |
| Approx Losing Trades | 37 |
| Approx Average Winner | 90.40 |
| Approx Average Loser | 63.82 |
| Approx Winner / Loser Ratio | 1.42 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T191007_opening_range_breakout_v6a_dev_b`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T191007_opening_range_breakout_v6a_dev_b\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T191007_opening_range_breakout_v6a_dev_b\daily_equity.csv`

---

## EXP-20260309-033 | mes_mnq_rmr_v1 | MES | 1m | SMOKE

**Tags:** #strategy/mesmnqrmrv1 #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T193730_mes_mnq_rmr_v1_smoke`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T193730_mes_mnq_rmr_v1_smoke`
- **Strategy:** `mes_mnq_rmr_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `32`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
MES weakness versus MNQ after OR normalization will support a tradable long mean-reversion response.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Smoke test for mes_mnq_rmr_v1.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:15`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "time_stop_bars": 60,
  "divergence_threshold": -0.75,
  "target_divergence": -0.25,
  "position_size": 1,
  "session_open": "08:30",
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100091.25 |
| Net PnL | 91.25 |
| Total Return % | 0.0913 |
| Max Drawdown Abs | 148.75 |
| Max Drawdown % | 0.15 |
| Daily Sharpe Approx | 1.0791 |
| Execution Count | 42 |
| Closed Trade Count | 21 |
| Win Rate % | 23.8095 |
| Gross Profit | 417.50 |
| Gross Loss | 326.25 |
| Profit Factor | 1.2797 |
| Trades / Tested Day | 0.66 |
| Approx Winning Trades | 5 |
| Approx Losing Trades | 16 |
| Approx Average Winner | 83.50 |
| Approx Average Loser | 20.39 |
| Approx Winner / Loser Ratio | 4.10 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T193730_mes_mnq_rmr_v1_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T193730_mes_mnq_rmr_v1_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T193730_mes_mnq_rmr_v1_smoke\daily_equity.csv`

---

## EXP-20260309-034 | mes_mnq_rmr_v1 | MES | 1m | FULL

**Tags:** #strategy/mesmnqrmrv1 #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T193920_mes_mnq_rmr_v1_dev_a`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T193920_mes_mnq_rmr_v1_dev_a`
- **Strategy:** `mes_mnq_rmr_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
MES weakness versus MNQ after OR normalization will support a tradable long mean-reversion response.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Dev-A benchmark split run for mes_mnq_rmr_v1.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:15`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "time_stop_bars": 60,
  "divergence_threshold": -0.75,
  "target_divergence": -0.25,
  "position_size": 1,
  "session_open": "08:30",
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99975.00 |
| Net PnL | -25.00 |
| Total Return % | -0.0250 |
| Max Drawdown Abs | 263.75 |
| Max Drawdown % | 0.26 |
| Daily Sharpe Approx | -0.0175 |
| Execution Count | 136 |
| Closed Trade Count | 68 |
| Win Rate % | 29.4118 |
| Gross Profit | 911.25 |
| Gross Loss | 936.25 |
| Profit Factor | 0.9733 |
| Trades / Tested Day | 0.51 |
| Approx Winning Trades | 20 |
| Approx Losing Trades | 48 |
| Approx Average Winner | 45.56 |
| Approx Average Loser | 19.51 |
| Approx Winner / Loser Ratio | 2.34 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T193920_mes_mnq_rmr_v1_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T193920_mes_mnq_rmr_v1_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T193920_mes_mnq_rmr_v1_dev_a\daily_equity.csv`

---


## Final Assessment: mes_mnq_rmr_v1
- **Strategy Outcome:** mes_mnq_rmr_v1 was formally tested to its Dev-A bounds and is **REJECTED**.
- **Next Steps:** It does not qualify for Dev-B testing. No child branches should be opened from it at this time.

## Infrastructure Improvement Note: Cross-Market Context
- The replay engine successfully gained thin **MES/MNQ matched-timestamp context support** during this sprint.
- This was purely an infrastructure improvement, isolated via a non-mutating extension (context_family, uses_context_bar).
- It should not be confused with strategy success (the strategy failed, but the engine upgrade succeeded).
- This cleanly mapped timestamp context extension may support future cross-market relative value families.

## EXP-20260309-035 | hedging_demand_intraday_momentum_v1 | MES | 1m | FULL

**Tags:** #strategy/hedgingdemandintradaymomentumv1 #family/MES #interval/1m #sample/full #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `Config: configs/active/hedging_demand_intraday_momentum_v1_dev_a.json`
- **Strategy:** `hedging_demand_intraday_momentum_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Hedging demand drives late-day momentum on strong trend days. Enters at 14:30 CST if the absolute move from the 08:30 CST open exceeds 30 points.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `First Dev-A test of the new SSRN-001 bridging-flow momentum parent family.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "trend_threshold_points": 30.0,
  "time_entry": "14:30",
  "time_exit": "15:00",
  "session_open": "08:30",
  "hard_stop_points": 8.0,
  "position_size": 1,
  "tick_size": 0.25,
  "timezone": "America/Chicago",
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
Run failed with error:
```
int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/active/hedging_demand_intraday_momentum_v1_dev_a.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260309-036 | hedging_demand_intraday_momentum_v1 | MES | 1m | FULL

**Tags:** #strategy/hedgingdemandintradaymomentumv1 #family/MES #interval/1m #sample/full #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `Config: configs/active/hedging_demand_intraday_momentum_v1_dev_a.json`
- **Strategy:** `hedging_demand_intraday_momentum_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Hedging demand drives late-day momentum on strong trend days. Enters at 14:30 CST if the absolute move from the 08:30 CST open exceeds 30 points.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `First Dev-A test of the new SSRN-001 bridging-flow momentum parent family.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "trend_threshold_points": 30.0,
  "time_entry": "14:30",
  "time_exit": "15:00",
  "session_open": "08:30",
  "hard_stop_points": 8.0,
  "position_size": 1,
  "tick_size": 0.25,
  "timezone": "America/Chicago",
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
Run failed with error:
```
int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/active/hedging_demand_intraday_momentum_v1_dev_a.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260309-037 | hedging_demand_intraday_momentum_v1 | MES | 1m | FULL

**Tags:** #strategy/hedgingdemandintradaymomentumv1 #family/MES #interval/1m #sample/full #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `Config: configs/active/hedging_demand_intraday_momentum_v1_dev_a.json`
- **Strategy:** `hedging_demand_intraday_momentum_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Hedging demand drives late-day momentum on strong trend days. Enters at 14:30 CST if the absolute move from the 08:30 CST open exceeds 30 points.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `First Dev-A test of the new SSRN-001 bridging-flow momentum parent family.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "trend_threshold_points": 30.0,
  "time_entry": "14:30",
  "time_exit": "15:00",
  "session_open": "08:30",
  "hard_stop_points": 8.0,
  "position_size": 1,
  "tick_size": 0.25,
  "timezone": "America/Chicago",
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
Run failed with error:
```
int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/active/hedging_demand_intraday_momentum_v1_dev_a.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260309-038 | hedging_demand_intraday_momentum_v1 | MES | 1m | FULL

**Tags:** #strategy/hedgingdemandintradaymomentumv1 #family/MES #interval/1m #sample/full #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `Config: configs/active/hedging_demand_intraday_momentum_v1_dev_a.json`
- **Strategy:** `hedging_demand_intraday_momentum_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Hedging demand drives late-day momentum on strong trend days. Enters at 14:30 CST if the absolute move from the 08:30 CST open exceeds 30 points.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `First Dev-A test of the new SSRN-001 bridging-flow momentum parent family.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "trend_threshold_points": 30.0,
  "time_entry": "14:30",
  "time_exit": "15:00",
  "session_open": "08:30",
  "hard_stop_points": 8.0,
  "position_size": 1,
  "tick_size": 0.25,
  "timezone": "America/Chicago",
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
Run failed with error:
```
int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/active/hedging_demand_intraday_momentum_v1_dev_a.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260309-039 | hedging_demand_intraday_momentum_v1 | MES | 1m | FULL

**Tags:** #strategy/hedgingdemandintradaymomentumv1 #family/MES #interval/1m #sample/full #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `Config: configs/active/hedging_demand_intraday_momentum_v1_dev_a.json`
- **Strategy:** `hedging_demand_intraday_momentum_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Hedging demand drives late-day momentum on strong trend days. Enters at 14:30 CST if the absolute move from the 08:30 CST open exceeds 30 points.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `First Dev-A test of the new SSRN-001 bridging-flow momentum parent family.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "trend_threshold_points": 30.0,
  "time_entry": "14:30",
  "time_exit": "15:00",
  "session_open": "08:30",
  "hard_stop_points": 8.0,
  "position_size": 1,
  "tick_size": 0.25,
  "timezone": "America/Chicago",
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
Run failed with error:
```
int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/active/hedging_demand_intraday_momentum_v1_dev_a.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260309-040 | hedging_demand_intraday_momentum_v1 | MES | 1m | FULL

**Tags:** #strategy/hedgingdemandintradaymomentumv1 #family/MES #interval/1m #sample/full #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `Config: configs/active/hedging_demand_intraday_momentum_v1_dev_a.json`
- **Strategy:** `hedging_demand_intraday_momentum_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Hedging demand drives late-day momentum on strong trend days. Enters at 14:30 CST if the absolute move from the 08:30 CST open exceeds 30 points.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `First Dev-A test of the new SSRN-001 bridging-flow momentum parent family.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "trend_threshold_points": 30.0,
  "time_entry": "14:30",
  "time_exit": "15:00",
  "session_open": "08:30",
  "hard_stop_points": 8.0,
  "position_size": 1,
  "tick_size": 0.25,
  "timezone": "America/Chicago",
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
Run failed with error:
```
int() argument must be a string, a bytes-like object or a real number, not 'Execution'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/active/hedging_demand_intraday_momentum_v1_dev_a.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260309-041 | hedging_demand_intraday_momentum_v1 | MES | 1m | FULL

**Tags:** #strategy/hedgingdemandintradaymomentumv1 #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260309T220017_hedging_demand_intraday_momentum_v1_dev_a`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T220017_hedging_demand_intraday_momentum_v1_dev_a`
- **Strategy:** `hedging_demand_intraday_momentum_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Hedging demand drives late-day momentum on strong trend days. Enters at 14:30 CST if the absolute move from the 08:30 CST open exceeds 30 points.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `First Dev-A test of the new SSRN-001 bridging-flow momentum parent family.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "trend_threshold_points": 30.0,
  "time_entry": "14:30",
  "time_exit": "15:00",
  "session_open": "08:30",
  "hard_stop_points": 8.0,
  "position_size": 1,
  "tick_size": 0.25,
  "timezone": "America/Chicago",
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99626.25 |
| Net PnL | -373.75 |
| Total Return % | -0.3737 |
| Max Drawdown Abs | 482.50 |
| Max Drawdown % | 0.48 |
| Daily Sharpe Approx | -2.6209 |
| Execution Count | 72 |
| Closed Trade Count | 36 |
| Win Rate % | 36.1111 |
| Gross Profit | 287.50 |
| Gross Loss | 661.25 |
| Profit Factor | 0.4348 |
| Trades / Tested Day | 0.27 |
| Approx Winning Trades | 13 |
| Approx Losing Trades | 23 |
| Approx Average Winner | 22.12 |
| Approx Average Loser | 28.75 |
| Approx Winner / Loser Ratio | 0.77 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T220017_hedging_demand_intraday_momentum_v1_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T220017_hedging_demand_intraday_momentum_v1_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T220017_hedging_demand_intraday_momentum_v1_dev_a\daily_equity.csv`

---

## EXP-20260309-042 | hedging_demand_intraday_momentum_v1 | MES | 1m | FULL

**Tags:** `#strategy/hedging_demand_intraday_momentum_v1` `#family/MES` `#interval/1m` `#sample/dev_a` `#status/completed` `#decision/reject_current_baseline` `#ssrn/001` `#stage/dev_a` `#verdict/rejected`

**Status:** `COMPLETED`  
**Decision:** `REJECTED`

### Metadata
- **Run ID:** `20260309T220049_hedging_demand_intraday_momentum_v1_dev_a`
- **Run Date:** `2026-03-09`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T220049_hedging_demand_intraday_momentum_v1_dev_a`
- **Strategy:** `hedging_demand_intraday_momentum_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Hedging demand drives late-day momentum on strong trend days. Enters at 14:30 CST if the absolute move from the 08:30 CST open exceeds 30 points.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `First Dev-A test of the new SSRN-001 bridging-flow momentum parent family.`
- **Why this run exists:** `First and only Dev-A run for the hedging_demand_intraday_momentum_v1 parent family (SSRN-001). Determines whether the family shows any raw live edge before branching or optimization.`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "trend_threshold_points": 30.0,
  "time_entry": "14:30",
  "time_exit": "15:00",
  "session_open": "08:30",
  "hard_stop_points": 8.0,
  "position_size": 1,
  "tick_size": 0.25,
  "timezone": "America/Chicago",
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99626.25 |
| Net PnL | -373.75 |
| Total Return % | -0.3737 |
| Max Drawdown Abs | 482.50 |
| Max Drawdown % | 0.48 |
| Daily Sharpe Approx | -2.6209 |
| Execution Count | 72 |
| Closed Trade Count | 36 |
| Win Rate % | 36.1111 |
| Gross Profit | 287.50 |
| Gross Loss | 661.25 |
| Profit Factor | 0.4348 |
| Trades / Tested Day | 0.27 |
| Approx Winning Trades | 13 |
| Approx Losing Trades | 23 |
| Approx Average Winner | 22.12 |
| Approx Average Loser | -30.06 |
| Approx Winner / Loser Ratio | 0.77 |

### Behavioral Read
Low trade frequency (36 trades over 133 session days; ~27% of days triggered the ±30-point threshold). When trades did fire, winners averaged $22 and losers averaged -$30. The payoff ratio (~0.74) was adverse, and the hit rate of 36% was well below the breakeven required for that ratio.

### Interpretation
The parent parameters show no raw life in the Dev-A window. The core structural hypothesis — that hedging demand drives detectable late-day momentum following strong-trend days — did not produce tradable alpha at this threshold level on MES 1m bars over the 2023-02-26 to 2023-08-31 in-sample window. The payoff ratio and hit rate were jointly unfavorable; this is not a frequency-alone issue that could be rescued by threshold loosening.

> **Infrastructure note (separate from alpha result):** Two engine-level bugs were discovered and patched during this run:
> 1. `BacktestEngine.run()` at line 3353 — `int(next_target)` cast was not null-safe; patched to `int(next_target) if next_target is not None else 0`.
> 2. `HedgingDemandIntradayMomentumV1Strategy.on_bar()` — initially drafted to return `Execution` objects, corrected to return integer target quantities per the engine contract.
>
> These are infrastructure/compatibility corrections only. They have no bearing on the alpha result.

### Risk Notes
N/A — rejected at Dev-A gate. No further risk assessment warranted.

### Recommendation / Next Action
REJECT. No child branching, no parameter rescue, no re-test justified. Family is parked in source library with status `rejected after Dev-A`. The engine infrastructure fixes benefit all future strategy implementations.

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260309T220049_hedging_demand_intraday_momentum_v1_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260309T220049_hedging_demand_intraday_momentum_v1_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260309T220049_hedging_demand_intraday_momentum_v1_dev_a\daily_equity.csv`

---

## EXP-20260310-001 | overnight_intraday_reversal_v1 | MES | 1m | FULL

**Tags:** #strategy/overnightintradayreversalv1 #family/MES #interval/1m #stage/dev_a #ssrn/003 #status/completed #decision/advanced_to_dev_b

**Status:** `COMPLETED`  
**Decision:** `ADVANCED TO DEV-B`

### Metadata
- **Run ID:** `20260310T084154_overnight_intraday_reversal_v1_dev_a`
- **Run Date:** `2026-03-10`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260310T084154_overnight_intraday_reversal_v1_dev_a`
- **Strategy:** `overnight_intraday_reversal_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Fading a qualifying MES overnight gap (prior RTH close to 08:30 CT bar open, threshold 8.0 points) during the RTH session produces positive raw expectancy. Signal evaluated at 08:30 CT bar close; exit at 14:30 CT bar close. Single-instrument derivative of SSRN-003.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `First Dev-A test of the overnight_intraday_reversal parent family (SSRN-003 derivative).`
- **Why this run exists:** `First Dev-A in-sample discovery run for the overnight_intraday_reversal parent family. Evaluates whether fading a qualifying MES overnight gap produces positive raw expectancy.`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "gap_threshold_points": 8.0,
  "time_eval": "08:30",
  "time_exit": "14:30",
  "session_start": "08:30",
  "session_end": "15:00",
  "hard_stop_points": 10.0,
  "position_size": 1,
  "tick_size": 0.25,
  "timezone": "America/Chicago",
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 101007.50 |
| Net PnL | 1007.50 |
| Total Return % | 1.0075 |
| Max Drawdown Abs | 435.00 |
| Max Drawdown % | 0.43 |
| Daily Sharpe Approx | 1.4261 |
| Execution Count | 172 |
| Closed Trade Count | 86 |
| Win Rate % | 37.2093 |
| Gross Profit | 3820.00 |
| Gross Loss | 2812.50 |
| Profit Factor | 1.3582 |
| Trades / Tested Day | 0.65 |
| Approx Winning Trades | 32 |
| Approx Losing Trades | 54 |
| Approx Average Winner | 119.38 |
| Approx Average Loser | 52.08 |
| Approx Winner / Loser Ratio | 2.29 |

### Behavioral Read
Positive payoff asymmetry: avg winner ($119.38) was 2.29× the avg loser ($52.08). Hit rate was low at 37.2% but insufficient to break the edge given the payoff ratio. Max drawdown of $435 (0.43%) indicates controlled drawdown behavior during the Dev-A window. Trade frequency was 86 trades over 133 days, approximately 0.65 trades per day.

### Interpretation
Dev-A showed raw life. Profit factor of 1.36 confirms positive expectancy in-sample. The edge is entirely payoff-asymmetry driven rather than win-rate driven, which is typical for fade strategies holding an adverse selection risk. The parent passed the Dev-A gate and was advanced to Dev-B for out-of-sample confirmation.

### Risk Notes
TBD

### Recommendation / Next Action
Advanced to Dev-B (EXP-20260310-002) for out-of-sample confirmation. No parameter tuning or child branching performed prior to Dev-B.

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260310T084154_overnight_intraday_reversal_v1_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260310T084154_overnight_intraday_reversal_v1_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260310T084154_overnight_intraday_reversal_v1_dev_a\daily_equity.csv`

---

## EXP-20260310-002 | overnight_intraday_reversal_v1 | MES | 1m | FULL

**Tags:** #strategy/overnightintradayreversalv1 #family/MES #interval/1m #stage/dev_b #ssrn/003 #status/completed #decision/rejected #verdict/rejected

**Status:** `COMPLETED`  
**Decision:** `REJECTED`

### Metadata
- **Run ID:** `20260310T084539_overnight_intraday_reversal_v1_dev_b`
- **Run Date:** `2026-03-10`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260310T084539_overnight_intraday_reversal_v1_dev_b`
- **Strategy:** `overnight_intraday_reversal_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-09-01 -> 2024-02-29`
- **Days Tested:** `128`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Out-of-sample confirmation of Dev-A result: fading a qualifying MES overnight gap (prior RTH close to 08:30 CT bar open, threshold 8.0 points) produces positive raw expectancy. No logic or parameter changes from Dev-A.

### Change Description
- **Parent Experiment:** `EXP-20260310-001`
- **What changed:** `Dev-B out-of-sample confirmation run for overnight_intraday_reversal_v1. Identical logic and parameters to Dev-A.`
- **Why this run exists:** `Out-of-sample confirmation required after Dev-A passed. Dev-B tests whether the Dev-A edge persists on unseen data (2023-09-01 to 2024-02-29) without any parameter changes.`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "gap_threshold_points": 8.0,
  "time_eval": "08:30",
  "time_exit": "14:30",
  "session_start": "08:30",
  "session_end": "15:00",
  "hard_stop_points": 10.0,
  "position_size": 1,
  "tick_size": 0.25,
  "timezone": "America/Chicago",
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99308.75 |
| Net PnL | -691.25 |
| Total Return % | -0.6912 |
| Max Drawdown Abs | 1192.50 |
| Max Drawdown % | 1.19 |
| Daily Sharpe Approx | -1.4272 |
| Execution Count | 150 |
| Closed Trade Count | 75 |
| Win Rate % | 26.6667 |
| Gross Profit | 2117.50 |
| Gross Loss | 2808.75 |
| Profit Factor | 0.7539 |
| Trades / Tested Day | 0.59 |
| Approx Winning Trades | 20 |
| Approx Losing Trades | 55 |
| Approx Average Winner | 105.88 |
| Approx Average Loser | 51.07 |
| Approx Winner / Loser Ratio | 2.07 |

### Behavioral Read
Win rate collapsed from 37.2% (Dev-A) to 26.7% (Dev-B), a drop of over 10 percentage points. Payoff structure was broadly preserved: avg winner ($105.88) and avg loser ($51.07) were similar to Dev-A. However, the lower hit rate was sufficient to push the strategy to a net loss. Max drawdown tripled from $435 to $1,192.50. Daily Sharpe flipped from +1.43 to −1.43.

### Interpretation
Dev-B failed to confirm. The payoff structure held, but the directional accuracy of the gap signal degraded materially out of sample. This is consistent with the known risk identified in the pre-code evidence memo and strategy spec: the single-instrument MES implementation is a notable simplification of the academic cross-sectional source, and the overnight gap sign on a single instrument may not provide a stable directional predictive signal across different market regimes. The Dev-A result appears to have benefited from the specific volatility and momentum regime of Q1–Q2 2023 (post-Fed hiking cycle peak, relatively high gap variance). Dev-B (Sep 2023 – Feb 2024) did not exhibit the same gap-reversal tendency.

### Risk Notes
TBD

### Recommendation / Next Action
REJECT. Dev-B out-of-sample confirmation failed. No benchmark promotion, no child branching, no rescue optimization. The family is closed.

### Research Note
This family was an honest single-instrument MES derivative of a cross-sectional academic source (SSRN-003). The Dev-B failure weakens the transfer case from cross-sectional overnight reversal (ranked across a universe of futures) to single-instrument MES gap fade. The Dev-A result was likely regime-specific. This is useful research information: the overnight gap signal on a single MES instrument does not appear to carry a stable, generalizable directional edge at the tested threshold, and the cross-sectional-to-single-instrument reduction is likely a meaningful source of signal degradation.

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260310T084539_overnight_intraday_reversal_v1_dev_b`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260310T084539_overnight_intraday_reversal_v1_dev_b\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260310T084539_overnight_intraday_reversal_v1_dev_b\daily_equity.csv`

---

## CLOSEOUT NOTE | overnight_intraday_reversal_v1 | SSRN-003 | REJECTED AFTER DEV-B

**Family:** `overnight_intraday_reversal_v1`  
**Source Lineage:** `SSRN-003 — overnight_intraday_reversal`  
**Final Decision:** `REJECTED AFTER DEV-B`  
**Date Closed:** `2026-03-10`

**Reason:** Raw life appeared in Dev-A, but out-of-sample confirmation failed. No promotion, no rescue optimization, no child branching justified.

### Dev-A Summary (EXP-20260310-001 | 2023-02-26 → 2023-08-31)
| Metric | Value |
|---|---:|
| Net PnL | +$1,007.50 |
| Profit Factor | 1.36 |
| Max Drawdown % | 0.43% |
| Total Trades | 86 |
| Win Rate | 37.2% |
| Avg Winner | +$119.38 |
| Avg Loser | −$52.08 |

### Dev-B Summary (EXP-20260310-002 | 2023-09-01 → 2024-02-29)
| Metric | Value |
|---|---:|
| Net PnL | −$691.25 |
| Profit Factor | 0.75 |
| Max Drawdown % | 1.19% |
| Total Trades | 75 |
| Win Rate | 26.7% |
| Avg Winner | +$105.88 |
| Avg Loser | −$51.07 |

### Interpretation
- Payoff structure (avg winner / avg loser ratio) remained broadly similar across Dev-A and Dev-B.
- Win rate collapsed materially out of sample (37.2% → 26.7%), which was sufficient to push the strategy to a net loss.
- Profit factor fell below breakeven (1.36 → 0.75).
- The Dev-A result did not confirm; no benchmark promotion, no child branching, no rescue optimization.

### Research Note
- This family was implemented as an honest **single-instrument MES derivative** of a cross-sectional academic source (SSRN-003).
- The Dev-B failure weakens the transfer case from cross-sectional overnight reversal to single-instrument MES gap fade.
- The cross-sectional-to-single-instrument reduction is the most likely source of the instability: the gap sign on one instrument does not carry the same stable signal as relative ranking across a universe.
- This is useful research even in rejection: the overnight gap direction on MES alone is not a reliable standalone entry signal at this parameter set.

---

## EXP-20260310-003 | mes_mnq_relative_value_spread_v1 | MES | 1m | FULL

**Tags:** #strategy/mesmnqrelativevaluespreadv1 #family/MES #interval/1m #sample/full #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-10`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `Config: configs/active/mes_mnq_relative_value_spread_v1_dev_a.json`
- **Strategy:** `mes_mnq_relative_value_spread_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
A fixed-ratio MES/MNQ intraday substitute spread entered against the 10:00 CT normalized percent-move divergence (threshold 0.0030) shows positive raw expectancy. Long MES / Short MNQ when MNQ has outperformed; reversed when MES has outperformed. Single evaluation per day; exit at 14:30 CT or pair hard stop -$200.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `First Dev-A test of the QC-001 pilot spread parent family mes_mnq_relative_value_spread_v1.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "divergence_threshold": 0.003,
  "time_eval": "10:00",
  "time_exit": "14:30",
  "session_start": "08:30",
  "session_end": "15:00",
  "pair_hard_stop_dollars": 200.0,
  "mes_contract_multiplier": 5.0,
  "mnq_contract_multiplier": 2.0,
  "slippage_ticks": 1.0,
  "tick_size_mes": 0.25,
  "tick_size_mnq": 0.25,
  "commission_per_side": 1.25,
  "timezone": "America/Chicago"
}
```

### Results
Run failed with error:
```
Conversion Error: invalid timestamp field format: "20230703T15:00:00-05:00", expected format is (YYYY-MM-DD HH:MM:SS[.US][±HH[:MM[:SS]]| ZONE])
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/active/mes_mnq_relative_value_spread_v1_dev_a.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260310-004 | mes_mnq_relative_value_spread_v1 | MES | 1m | FULL

**Tags:** #strategy/mesmnqrelativevaluespreadv1 #family/MES #interval/1m #sample/full #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-10`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `Config: configs/active/mes_mnq_relative_value_spread_v1_dev_a.json`
- **Strategy:** `mes_mnq_relative_value_spread_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
A fixed-ratio MES/MNQ intraday substitute spread entered against the 10:00 CT normalized percent-move divergence (threshold 0.0030) shows positive raw expectancy. Long MES / Short MNQ when MNQ has outperformed; reversed when MES has outperformed. Single evaluation per day; exit at 14:30 CT or pair hard stop -$200.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `First Dev-A test of the QC-001 pilot spread parent family mes_mnq_relative_value_spread_v1.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "divergence_threshold": 0.003,
  "time_eval": "10:00",
  "time_exit": "14:30",
  "session_start": "08:30",
  "session_end": "15:00",
  "pair_hard_stop_dollars": 200.0,
  "mes_contract_multiplier": 5.0,
  "mnq_contract_multiplier": 2.0,
  "slippage_ticks": 1.0,
  "tick_size_mes": 0.25,
  "tick_size_mnq": 0.25,
  "commission_per_side": 1.25,
  "timezone": "America/Chicago"
}
```

### Results
Run failed with error:
```
Conversion Error: invalid timestamp field format: "20230703 15:00:00", expected format is (YYYY-MM-DD HH:MM:SS[.US][±HH[:MM[:SS]]| ZONE])
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/active/mes_mnq_relative_value_spread_v1_dev_a.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260310-005 | mes_mnq_relative_value_spread_v1 | MES | 1m | FULL

**Tags:** #strategy/mesmnqrelativevaluespreadv1 #family/MES #context/MNQ #interval/1m #stage/dev_a #qc/001 #status/completed #decision/rejected #verdict/rejected

**Status:** `COMPLETED`  
**Decision:** `REJECTED AT DEV-A`

### Metadata
- **Run ID:** `20260310T134625_mes_mnq_relative_value_spread_v1_dev_a`
- **Run Date:** `2026-03-10`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260310T134625_mes_mnq_relative_value_spread_v1_dev_a`
- **Strategy:** `mes_mnq_relative_value_spread_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
A fixed-ratio MES/MNQ intraday substitute spread entered against the 10:00 CT normalized percent-move divergence (threshold 0.0030) shows positive raw expectancy. Long MES / Short MNQ when MNQ has outperformed; reversed when MES has outperformed. Single evaluation per day; exit at 14:30 CT or pair hard stop -$200.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `First Dev-A test of the QC-001 pilot spread parent family mes_mnq_relative_value_spread_v1.`
- **Why this run exists:** `First Dev-A in-sample discovery run for the QC-001 pilot spread parent. Tests whether a thin fixed-ratio MES/MNQ relative-value divergence entered once intraday shows any raw positive expectancy without ratio normalization, filters, or optimization.`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "divergence_threshold": 0.003,
  "time_eval": "10:00",
  "time_exit": "14:30",
  "session_start": "08:30",
  "session_end": "15:00",
  "pair_hard_stop_dollars": 200.0,
  "mes_contract_multiplier": 5.0,
  "mnq_contract_multiplier": 2.0,
  "slippage_ticks": 1.0,
  "tick_size_mes": 0.25,
  "tick_size_mnq": 0.25,
  "commission_per_side": 1.25,
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99691.75 |
| Net PnL | -308.25 |
| Total Return % | -0.3082 |
| Max Drawdown Abs | 723.25 |
| Max Drawdown % | 0.72 |
| Daily Sharpe Approx | -0.6324 |
| Execution Count | 188 |
| Closed Trade Count | 47 |
| Win Rate % | 46.8085 |
| Gross Profit | 1427.50 |
| Gross Loss | 1900.00 |
| Profit Factor | 0.7513 |
| Trades / Tested Day | 0.35 |
| Approx Winning Trades | 22 |
| Approx Losing Trades | 25 |
| Approx Average Winner | 64.89 |
| Approx Average Loser | 76.00 |
| Approx Winner / Loser Ratio | 0.85 |

### Behavioral Read
Win rate of 46.8% (22W / 25L) — close to 50/50 but slightly below. The payoff ratio is inverted: avg winner (+$64.89) is smaller than avg loser (−$76.00). Profit factor 0.75, Daily Sharpe −0.63. Trade count low at 47 over 133 days — the 0.0030 threshold filtered aggressively. Max drawdown $723.25 (0.72%) is controlled. No evidence of directional clustering or stop-cascade. The failure is structural, not due to a single outlier.

### Interpretation
No raw life. The parent failed the primary Dev-A question. The most plausible load-bearing cause is the intentionally crude 1:1 MES/MNQ contract ratio: MES ($5/pt × ~4500 pts ≈ $22,500 notional) and MNQ ($2/pt × ~15,000 pts ≈ $30,000 notional) are not economically equivalent at 1:1. The spread likely carries systematic beta leakage — the strategy is not testing true relative-value isolation, but rather a noisy single-leg proxy dressed as a spread. This was explicitly flagged as Risk #1 in the spec ("1:1 ratio distortion / outright beta leakage"). The parent did exactly what a thin, unoptimized first parent should do: it ran honestly and showed nothing useful.

### Risk Notes
Infrastructure worked correctly. Two-leg execution, per-bar MNQ P&L injection, pair-level hard stop, and execution audit logging all functioned as intended. Engine timing semantics (bar-close signal / next-bar-open fill) were verified and accepted under Outcome B. The failure is in alpha, not in plumbing.

### Recommendation / Next Action
REJECT. No Dev-B. No child branching. No ratio tuning, threshold tuning, stop tuning, or rescue optimization. The family is closed.

### Research Note
A thin synchronous MES/MNQ residual-divergence parent with fixed 1:1 sizing and simple time-based structure did not show raw life in Dev-A. The 1:1 ratio is the most likely structural failure point — MES and MNQ have meaningfully different notional values, so a 1:1 contract count is directionally imbalanced by construction. The infrastructure built for this run (paired-leg execution support, two-leg accounting path, execution auditability, clarified engine timing semantics) is preserved and available for future spread families. The alpha failure does not indict the infrastructure.

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260310T134625_mes_mnq_relative_value_spread_v1_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260310T134625_mes_mnq_relative_value_spread_v1_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260310T134625_mes_mnq_relative_value_spread_v1_dev_a\daily_equity.csv`

---

## CLOSEOUT NOTE | mes_mnq_relative_value_spread_v1 | QC-001 | REJECTED AT DEV-A

**Family:** `mes_mnq_relative_value_spread_v1`  
**Source Lineage:** `QC-001 — spread_residual_cointegration (MES/MNQ pilot derivative)`  
**Final Decision:** `REJECTED AT DEV-A`  
**Date Closed:** `2026-03-10`

**Reason:** No raw life in Dev-A. Profit factor below breakeven, payoff ratio inverted. No promotion, no rescue optimization, no child branching justified.

### Dev-A Summary (EXP-20260310-005 | 2023-02-26 → 2023-08-31)
| Metric | Value |
|---|---:|
| Net PnL | −$308.25 |
| Profit Factor | 0.75 |
| Max Drawdown % | 0.72% |
| Total Trades | 47 |
| Win Rate | 46.8% |
| Avg Winner | +$64.89 |
| Avg Loser | −$76.00 |
| Payoff Ratio | 0.85 : 1 |
| Daily Sharpe | −0.63 |

### Interpretation
- Win rate was close to 50/50 but slightly below; payoff ratio was inverted (avg loser > avg winner).
- Combined, the strategy produced negative expectancy with no ambiguity.
- Most plausible structural cause: fixed 1:1 MES/MNQ contract count produces systematic beta leakage rather than true relative-value isolation. MES and MNQ have materially different notional values at 1:1.
- No child branching, no ratio tuning, no threshold optimization, no rescue optimization.

### Research Lesson
A thin synchronous MES/MNQ residual-divergence parent with fixed 1:1 sizing and simple time-based structure did not show raw life in Dev-A. The infrastructure (two-leg execution, per-bar MNQ P&L injection, execution auditability) worked correctly and is preserved. The failure is in alpha, not in plumbing.

### Infrastructure Note
Paired-leg execution support, two-leg cash accounting via `context_leg_cash_delta`, execution audit logging for the context leg, and engine Outcome B timing semantics were all confirmed working. These remain available for future spread families that survive screening.

---

## EXP-20260310-006 | opening_range_breakout_v5a | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv5a #family/MES #interval/1m #sample/full #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-10`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `Config: configs/Active/opening_range_breakout_v5_orb_v5.json`
- **Strategy:** `opening_range_breakout_v5a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-09-01 -> 2024-02-29`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
ORB-v2 should perform more robustly when the opening range width is constrained to a tighter healthy band relative to recent OR history, and the opening range closes strongly near its high.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `ORB-v5a run on MES Dev-B. Tests whether a tighter OR width band and a strict OR close-location strength filter improve performance over the parent baseline.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "range_minutes": 15,
  "entry_buffer_ticks": 1,
  "stop_buffer_ticks": 1,
  "position_size": 1,
  "tick_size": 0.25,
  "session_open": "08:30",
  "no_new_entries_after": "11:00",
  "time_stop": "13:30",
  "allow_long": true,
  "timezone": "America/Chicago",
  "or_width_lookback_days": 20,
  "or_width_min_factor": 0.8,
  "or_width_max_factor": 1.6,
  "or_close_location_min": 0.7,
  "cost_protect_trigger_r": 1.25,
  "trail_activate_r": 2.0,
  "atr_period": 20,
  "atr_trail_multiple": 3.0,
  "slippage_ticks": 1.0,
  "commission_per_side": 1.25,
  "contract_multiplier": 5.0
}
```

### Results
Run failed with error:
```
Unknown strategy 'opening_range_breakout_v5a'.
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/Active/opening_range_breakout_v5_orb_v5.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260310-007 | mes_mnq_co_oc_reversal_v1 | MES | 1m | FULL

**Tags:** #strategy/mesmnqcoocreversalv1 #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260310T202924_mes_mnq_co_oc_reversal_v1_dev_a`
- **Run Date:** `2026-03-10`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260310T202924_mes_mnq_co_oc_reversal_v1_dev_a`
- **Strategy:** `mes_mnq_co_oc_reversal_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
MES/MNQ overnight relative displacement (CO-OC) partially reverses during the following cash session. Long the overnight loser, short the overnight winner. 3 MES vs 2 MNQ fixed spread unit. No threshold filter.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Thin parent: overnight return ranking as entry signal, 08:30 open anchor, 14:59 time exit, -$300 pair hard stop. No filters.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "session_start": "08:30",
  "time_exit": "14:59",
  "session_end": "15:00",
  "pair_hard_stop_dollars": 300.0,
  "mes_contract_multiplier": 5.0,
  "mnq_contract_multiplier": 2.0,
  "slippage_ticks": 1.0,
  "tick_size_mes": 0.25,
  "tick_size_mnq": 0.25,
  "commission_per_side": 1.25,
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 97367.50 |
| Net PnL | -2632.50 |
| Total Return % | -2.6325 |
| Max Drawdown Abs | 4518.00 |
| Max Drawdown % | 4.50 |
| Daily Sharpe Approx | -1.4529 |
| Execution Count | 527 |
| Closed Trade Count | 132 |
| Win Rate % | 42.4242 |
| Gross Profit | 16785.00 |
| Gross Loss | 23347.50 |
| Profit Factor | 0.7189 |
| Trades / Tested Day | 0.99 |
| Approx Winning Trades | 56 |
| Approx Losing Trades | 76 |
| Approx Average Winner | 299.73 |
| Approx Average Loser | 307.20 |
| Approx Winner / Loser Ratio | 0.98 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260310T202924_mes_mnq_co_oc_reversal_v1_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260310T202924_mes_mnq_co_oc_reversal_v1_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260310T202924_mes_mnq_co_oc_reversal_v1_dev_a\daily_equity.csv`

---

## EXP-20260310-008 | mes_mnq_co_oc_reversal_v1 | MES | 1m | FULL

**Tags:** #strategy/mesmnqcoocreversalv1 #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260310T203852_mes_mnq_co_oc_reversal_v1_sign_flip_dev_a`
- **Run Date:** `2026-03-10`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260310T203852_mes_mnq_co_oc_reversal_v1_sign_flip_dev_a`
- **Strategy:** `mes_mnq_co_oc_reversal_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Sign flip control. Tests if long overnight winner / short overnight loser generates positive expectancy, which would indicate an overnight momentum effect rather than reversal.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `Sign flip control for mes_mnq_co_oc_reversal_v1_dev_a.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "session_start": "08:30",
  "time_exit": "14:59",
  "session_end": "15:00",
  "pair_hard_stop_dollars": 300.0,
  "mes_contract_multiplier": 5.0,
  "mnq_contract_multiplier": 2.0,
  "slippage_ticks": 1.0,
  "tick_size_mes": 0.25,
  "tick_size_mnq": 0.25,
  "commission_per_side": 1.25,
  "timezone": "America/Chicago",
  "invert_signal": true
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 98227.25 |
| Net PnL | -1772.75 |
| Total Return % | -1.7728 |
| Max Drawdown Abs | 3043.75 |
| Max Drawdown % | 3.01 |
| Daily Sharpe Approx | -0.9129 |
| Execution Count | 528 |
| Closed Trade Count | 132 |
| Win Rate % | 53.7879 |
| Gross Profit | 21150.00 |
| Gross Loss | 17958.75 |
| Profit Factor | 1.1777 |
| Trades / Tested Day | 0.99 |
| Approx Winning Trades | 71 |
| Approx Losing Trades | 61 |
| Approx Average Winner | 297.89 |
| Approx Average Loser | 294.41 |
| Approx Winner / Loser Ratio | 1.01 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260310T203852_mes_mnq_co_oc_reversal_v1_sign_flip_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260310T203852_mes_mnq_co_oc_reversal_v1_sign_flip_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260310T203852_mes_mnq_co_oc_reversal_v1_sign_flip_dev_a\daily_equity.csv`

---

## EXP-20260310-009 | mes_mnq_co_oc_extreme_reversal_v1 | MES | 1m | FULL

**Tags:** #strategy/mesmnqcoocextremereversalv1 #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260310T205042_mes_mnq_co_oc_extreme_reversal_v1_dev_a`
- **Run Date:** `2026-03-10`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260310T205042_mes_mnq_co_oc_extreme_reversal_v1_dev_a`
- **Strategy:** `mes_mnq_co_oc_extreme_reversal_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2023-02-26 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Extreme overnight relative moves (>= 2 sigma) between MES and MNQ represent temporary inventory imbalance and partially revert early in the cash session (before 11:30 CT, exiting at 0.25 sigma convergence). 3 MES vs 2 MNQ fixed pair.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `New parent: 2-sigma threshold filter required for entry. Early exit at 11:30 time stop or 0.25 convergence.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "session_start": "08:30",
  "time_exit": "11:30",
  "pair_hard_stop_dollars": 300.0,
  "entry_std_threshold": 2.0,
  "exit_std_threshold": 0.25,
  "rolling_window_days": 60,
  "mes_contract_multiplier": 5.0,
  "mnq_contract_multiplier": 2.0,
  "slippage_ticks": 1.0,
  "tick_size_mes": 0.25,
  "tick_size_mnq": 0.25,
  "commission_per_side": 1.25,
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99060.25 |
| Net PnL | -939.75 |
| Total Return % | -0.9397 |
| Max Drawdown Abs | 1166.75 |
| Max Drawdown % | 1.17 |
| Daily Sharpe Approx | -2.3349 |
| Execution Count | 32 |
| Closed Trade Count | 8 |
| Win Rate % | 37.5000 |
| Gross Profit | 1031.25 |
| Gross Loss | 615.00 |
| Profit Factor | 1.6768 |
| Trades / Tested Day | 0.06 |
| Approx Winning Trades | 3 |
| Approx Losing Trades | 5 |
| Approx Average Winner | 343.75 |
| Approx Average Loser | 123.00 |
| Approx Winner / Loser Ratio | 2.79 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260310T205042_mes_mnq_co_oc_extreme_reversal_v1_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260310T205042_mes_mnq_co_oc_extreme_reversal_v1_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260310T205042_mes_mnq_co_oc_extreme_reversal_v1_dev_a\daily_equity.csv`

---

## EXP-20260310-010 | mes_mnq_co_oc_extreme_reversal_v1 | MES | 1m | FULL

**Tags:** #strategy/mesmnqcoocextremereversalv1 #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260310T205233_mes_mnq_co_oc_extreme_reversal_v1_extended_dev_a`
- **Run Date:** `2026-03-10`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260310T205233_mes_mnq_co_oc_extreme_reversal_v1_extended_dev_a`
- **Strategy:** `mes_mnq_co_oc_extreme_reversal_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2022-01-01 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Extreme overnight relative moves (>= 2 sigma) between MES and MNQ represent temporary inventory imbalance and partially revert early in the cash session. Extended sample window to achieve 20+ trade statistical floor before judgment.

### Change Description
- **Parent Experiment:** `20260310T205042_mes_mnq_co_oc_extreme_reversal_v1_dev_a`
- **What changed:** `Sample extension back to 2022-01-01 to achieve minimum trade count floor. No strategy changes.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "session_start": "08:30",
  "time_exit": "11:30",
  "pair_hard_stop_dollars": 300.0,
  "entry_std_threshold": 2.0,
  "exit_std_threshold": 0.25,
  "rolling_window_days": 60,
  "mes_contract_multiplier": 5.0,
  "mnq_contract_multiplier": 2.0,
  "slippage_ticks": 1.0,
  "tick_size_mes": 0.25,
  "tick_size_mnq": 0.25,
  "commission_per_side": 1.25,
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 99060.25 |
| Net PnL | -939.75 |
| Total Return % | -0.9397 |
| Max Drawdown Abs | 1166.75 |
| Max Drawdown % | 1.17 |
| Daily Sharpe Approx | -2.3349 |
| Execution Count | 32 |
| Closed Trade Count | 8 |
| Win Rate % | 37.5000 |
| Gross Profit | 1031.25 |
| Gross Loss | 615.00 |
| Profit Factor | 1.6768 |
| Trades / Tested Day | 0.06 |
| Approx Winning Trades | 3 |
| Approx Losing Trades | 5 |
| Approx Average Winner | 343.75 |
| Approx Average Loser | 123.00 |
| Approx Winner / Loser Ratio | 2.79 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260310T205233_mes_mnq_co_oc_extreme_reversal_v1_extended_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260310T205233_mes_mnq_co_oc_extreme_reversal_v1_extended_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260310T205233_mes_mnq_co_oc_extreme_reversal_v1_extended_dev_a\daily_equity.csv`

---

## EXP-20260310-011 | price_gap_reversion_v1 | MES | 1m | FULL

**Tags:** #strategy/pricegapreversionv1 #family/MES #interval/1m #sample/full #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-10`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `Config: configs/Active/price_gap_reversion_v1_extended_dev_a.json`
- **Strategy:** `price_gap_reversion_v1`
- **Strategy Archetype:** `mean_reversion`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2019-01-01 -> 2023-08-31`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Extreme opening gaps (>= 3.0 sigma) are liquidity-driven overreactions that get filled by institutional flow in the early cash session. 5-year sample window used to capture minimum trade count floor for an extreme outlier condition.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `First thin-parent run.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "time_anchor": "08:30",
  "time_exit": "11:30",
  "entry_std_threshold": 3.0,
  "rolling_window_days": 60,
  "hard_stop_dollars": 150.0,
  "multiplier": 5.0,
  "timezone": "America/Chicago"
}
```

### Results
Run failed with error:
```
PriceGapReversionV1Strategy.on_bar() missing 2 required positional arguments: 'current_bar' and 'context_bars'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/Active/price_gap_reversion_v1_extended_dev_a.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260310-012 | price_gap_reversion_v1 | MES | 1m | FULL

**Tags:** #strategy/pricegapreversionv1 #family/MES #interval/1m #sample/full #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-10`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `Config: configs/Active/price_gap_reversion_v1_extended_dev_a.json`
- **Strategy:** `price_gap_reversion_v1`
- **Strategy Archetype:** `mean_reversion`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2019-01-01 -> 2023-08-31`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Extreme opening gaps (>= 3.0 sigma) are liquidity-driven overreactions that get filled by institutional flow in the early cash session. 5-year sample window used to capture minimum trade count floor for an extreme outlier condition.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `First thin-parent run.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "time_anchor": "08:30",
  "time_exit": "11:30",
  "entry_std_threshold": 3.0,
  "rolling_window_days": 60,
  "hard_stop_dollars": 150.0,
  "multiplier": 5.0,
  "timezone": "America/Chicago"
}
```

### Results
Run failed with error:
```
'Bar' object has no attribute 'ts'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/Active/price_gap_reversion_v1_extended_dev_a.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260310-013 | price_gap_reversion_v1 | MES | 1m | FULL

**Tags:** #strategy/pricegapreversionv1 #family/MES #interval/1m #sample/full #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-10`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `Config: configs/Active/price_gap_reversion_v1_extended_dev_a.json`
- **Strategy:** `price_gap_reversion_v1`
- **Strategy Archetype:** `mean_reversion`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2019-01-01 -> 2023-08-31`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Extreme opening gaps (>= 3.0 sigma) are liquidity-driven overreactions that get filled by institutional flow in the early cash session. 5-year sample window used to capture minimum trade count floor for an extreme outlier condition.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `First thin-parent run.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "time_anchor": "08:30",
  "time_exit": "11:30",
  "entry_std_threshold": 3.0,
  "rolling_window_days": 60,
  "hard_stop_dollars": 150.0,
  "multiplier": 5.0,
  "timezone": "America/Chicago"
}
```

### Results
Run failed with error:
```
time data '20230227' does not match format '%Y-%m-%d'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/Active/price_gap_reversion_v1_extended_dev_a.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260310-014 | price_gap_reversion_v1 | MES | 1m | FULL

**Tags:** #strategy/pricegapreversionv1 #family/MES #interval/1m #sample/full #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-10`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `Config: configs/Active/price_gap_reversion_v1_extended_dev_a.json`
- **Strategy:** `price_gap_reversion_v1`
- **Strategy Archetype:** `mean_reversion`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2019-01-01 -> 2023-08-31`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Extreme opening gaps (>= 3.0 sigma) are liquidity-driven overreactions that get filled by institutional flow in the early cash session. 5-year sample window used to capture minimum trade count floor for an extreme outlier condition.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `First thin-parent run.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "time_anchor": "08:30",
  "time_exit": "11:30",
  "entry_std_threshold": 3.0,
  "rolling_window_days": 60,
  "hard_stop_dollars": 150.0,
  "multiplier": 5.0,
  "timezone": "America/Chicago"
}
```

### Results
Run failed with error:
```
unsupported operand type(s) for *: 'int' and 'NoneType'
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/Active/price_gap_reversion_v1_extended_dev_a.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260310-015 | price_gap_reversion_v1 | MES | 1m | FULL

**Tags:** #strategy/pricegapreversionv1 #family/MES #interval/1m #sample/full #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-10`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `Config: configs/Active/price_gap_reversion_v1_extended_dev_a.json`
- **Strategy:** `price_gap_reversion_v1`
- **Strategy Archetype:** `mean_reversion`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2019-01-01 -> 2023-08-31`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Extreme opening gaps (>= 3.0 sigma) are liquidity-driven overreactions that get filled by institutional flow in the early cash session. 5-year sample window used to capture minimum trade count floor for an extreme outlier condition.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `First thin-parent run.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "time_anchor": "08:30",
  "time_exit": "11:30",
  "entry_std_threshold": 3.0,
  "rolling_window_days": 60,
  "hard_stop_dollars": 150.0,
  "multiplier": 5.0,
  "timezone": "America/Chicago"
}
```

### Results
Run failed with error:
```
unsupported format string passed to NoneType.__format__
```

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `Config: configs/Active/price_gap_reversion_v1_extended_dev_a.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260310-016 | price_gap_reversion_v1 | MES | 1m | FULL

**Tags:** #strategy/pricegapreversionv1 #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260310T210338_price_gap_reversion_v1_extended_dev_a`
- **Run Date:** `2026-03-10`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260310T210338_price_gap_reversion_v1_extended_dev_a`
- **Strategy:** `price_gap_reversion_v1`
- **Strategy Archetype:** `mean_reversion`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2019-01-01 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Extreme opening gaps (>= 3.0 sigma) are liquidity-driven overreactions that get filled by institutional flow in the early cash session. 5-year sample window used to capture minimum trade count floor for an extreme outlier condition.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `First thin-parent run.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "time_anchor": "08:30",
  "time_exit": "11:30",
  "entry_std_threshold": 3.0,
  "rolling_window_days": 60,
  "hard_stop_dollars": 150.0,
  "multiplier": 5.0,
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100000.00 |
| Net PnL | 0.00 |
| Total Return % | 0.0000 |
| Max Drawdown Abs | 0.00 |
| Max Drawdown % | N/A |
| Daily Sharpe Approx | N/A |
| Execution Count | 0 |
| Closed Trade Count | 0 |
| Win Rate % | 0.0000 |
| Gross Profit | 0.00 |
| Gross Loss | 0.00 |
| Profit Factor | N/A |
| Trades / Tested Day | 0.00 |
| Approx Winning Trades | 0 |
| Approx Losing Trades | 0 |
| Approx Average Winner | 0.00 |
| Approx Average Loser | 0.00 |
| Approx Winner / Loser Ratio | 0.00 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260310T210338_price_gap_reversion_v1_extended_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260310T210338_price_gap_reversion_v1_extended_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260310T210338_price_gap_reversion_v1_extended_dev_a\daily_equity.csv`

---

## EXP-20260310-017 | price_gap_reversion_v1 | MES | 1m | FULL

**Tags:** #strategy/pricegapreversionv1 #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260310T210359_price_gap_reversion_v1_extended_dev_a`
- **Run Date:** `2026-03-10`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260310T210359_price_gap_reversion_v1_extended_dev_a`
- **Strategy:** `price_gap_reversion_v1`
- **Strategy Archetype:** `mean_reversion`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2019-01-01 -> 2023-08-31`
- **Days Tested:** `133`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Extreme opening gaps (>= 3.0 sigma) are liquidity-driven overreactions that get filled by institutional flow in the early cash session. 5-year sample window used to capture minimum trade count floor for an extreme outlier condition.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `First thin-parent run.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "time_anchor": "08:30",
  "time_exit": "11:30",
  "entry_std_threshold": 3.0,
  "rolling_window_days": 60,
  "hard_stop_dollars": 150.0,
  "multiplier": 5.0,
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100000.00 |
| Net PnL | 0.00 |
| Total Return % | 0.0000 |
| Max Drawdown Abs | 0.00 |
| Max Drawdown % | N/A |
| Daily Sharpe Approx | N/A |
| Execution Count | 0 |
| Closed Trade Count | 0 |
| Win Rate % | 0.0000 |
| Gross Profit | 0.00 |
| Gross Loss | 0.00 |
| Profit Factor | N/A |
| Trades / Tested Day | 0.00 |
| Approx Winning Trades | 0 |
| Approx Losing Trades | 0 |
| Approx Average Winner | 0.00 |
| Approx Average Loser | 0.00 |
| Approx Winner / Loser Ratio | 0.00 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260310T210359_price_gap_reversion_v1_extended_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260310T210359_price_gap_reversion_v1_extended_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260310T210359_price_gap_reversion_v1_extended_dev_a\daily_equity.csv`

---

## EXP-20260310-018 | price_gap_reversion_v1 | MES | 1m | FULL

**Tags:** #strategy/pricegapreversionv1 #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260310T211028_price_gap_reversion_v1_extended_dev_a`
- **Run Date:** `2026-03-10`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ b72d9f1`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260310T211028_price_gap_reversion_v1_extended_dev_a`
- **Strategy:** `price_gap_reversion_v1`
- **Strategy Archetype:** `mean_reversion`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2019-01-01 -> 2026-02-22`
- **Days Tested:** `770`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Extreme opening gaps (>= 3.0 sigma) are liquidity-driven overreactions that get filled by institutional flow in the early cash session. 5-year sample window used to capture minimum trade count floor for an extreme outlier condition.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `First thin-parent run using the full available local catalog data.`
- **Why this run exists:** `TBD`

### Execution Assumptions
- **Session Timezone:** `America/Chicago`
- **Session:** `08:30 -> 15:00`
- **Flatten Daily:** `true`
- **Flatten On Last Bar:** `true`
- **Initial Cash:** `100000.0`
- **Contract Multiplier:** `5.0`
- **Tick Size:** `0.25`
- **Slippage Ticks:** `1.0`
- **Commission Per Side:** `1.25`

### Strategy Parameters
```json
{
  "time_anchor": "08:30",
  "time_exit": "11:30",
  "entry_std_threshold": 3.0,
  "rolling_window_days": 60,
  "hard_stop_dollars": 150.0,
  "multiplier": 5.0,
  "timezone": "America/Chicago"
}
```

### Results
| Metric | Value |
|---|---:|
| Final Equity | 100000.00 |
| Net PnL | 0.00 |
| Total Return % | 0.0000 |
| Max Drawdown Abs | 0.00 |
| Max Drawdown % | N/A |
| Daily Sharpe Approx | N/A |
| Execution Count | 0 |
| Closed Trade Count | 0 |
| Win Rate % | 0.0000 |
| Gross Profit | 0.00 |
| Gross Loss | 0.00 |
| Profit Factor | N/A |
| Trades / Tested Day | 0.00 |
| Approx Winning Trades | 0 |
| Approx Losing Trades | 0 |
| Approx Average Winner | 0.00 |
| Approx Average Loser | 0.00 |
| Approx Winner / Loser Ratio | 0.00 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260310T211028_price_gap_reversion_v1_extended_dev_a`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260310T211028_price_gap_reversion_v1_extended_dev_a\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260310T211028_price_gap_reversion_v1_extended_dev_a\daily_equity.csv`

---
