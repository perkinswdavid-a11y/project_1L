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
