# Phase 2 Research Log: Institutional Liquidity Hunter (ILH-001)

## Overview
Phase 2 shifts focus from candle-based breakouts to **Market Microstructure**. We are utilizing MBP (Market By Price) data from the Chicago-based VPS to identify institutional imbalances, passive absorption, and liquidity sweeps.

## Strategy Archetype: Microstructure / Order Flow
**Objective:** Gain an edge by detecting institutional participation before price action confirms.

---

## PILLAR 1: Infrastructure Setup (MBP Ingestion)
[ ] Define MBP schema in DuckDB.
[ ] Create CVD (Cumulative Volume Delta) engine.
[ ] Build Order Book Depth tracker (Level 2/3).

## PILLAR 2: Alpha Generation (The Signal)
[ ] Identify Passive Absorption levels.
[ ] Create Liquidity Sweep indicators.
[ ] Statistical Arbitrage (MES vs MNQ lead-lag).

---

## Experiments Log

### EXP-20260312-001 | ILH-001 | MBP Data Ingestion Verification
- **Status:** PLANNED
- **Hypothesis:** We can correctly extract bid/ask volume delta from the DuckDB MBP catalog.

## EXP-20260317-001 | opening_range_breakout_v5c | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv5c #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260317T104340_opening_range_breakout_v5c_smoke`
- **Run Date:** `2026-03-17`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260317T104340_opening_range_breakout_v5c_smoke`
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
| Max Drawdown % | 0.17 |
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
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260317T104340_opening_range_breakout_v5c_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260317T104340_opening_range_breakout_v5c_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260317T104340_opening_range_breakout_v5c_smoke\daily_equity.csv`

---

## EXP-20260318-001 | opening_range_breakout_v5c | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv5c #family/MES #interval/1m #sample/smoke #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `Config: configs\Archive\opening_range_breakout_v5c_smoke.json`
- **Strategy:** `opening_range_breakout_v5c`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2026-01-01 -> 2026-02-22`
- **Days Tested:** `1`
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
Run failed with error:
```
Unknown strategy 'opening_range_breakout_v5c'.
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
- **Report Directory:** `Config: configs\Archive\opening_range_breakout_v5c_smoke.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260318-002 | opening_range_breakout_v5c | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv5c #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260318T151759_opening_range_breakout_v5c_smoke`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T151759_opening_range_breakout_v5c_smoke`
- **Strategy:** `opening_range_breakout_v5c`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2026-01-01 -> 2026-02-22`
- **Days Tested:** `36`
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
| Final Equity | 99828.75 |
| Net PnL | -171.25 |
| Total Return % | -0.1713 |
| Max Drawdown Abs | 390.00 |
| Max Drawdown % | 0.39 |
| Daily Sharpe Approx | -1.1798 |
| Execution Count | 14 |
| Closed Trade Count | 7 |
| Win Rate % | 42.8571 |
| Gross Profit | 390.00 |
| Gross Loss | 561.25 |
| Profit Factor | 0.6949 |
| Trades / Tested Day | 0.19 |
| Approx Winning Trades | 3 |
| Approx Losing Trades | 4 |
| Approx Average Winner | 130.00 |
| Approx Average Loser | 140.31 |
| Approx Winner / Loser Ratio | 0.93 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T151759_opening_range_breakout_v5c_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260318T151759_opening_range_breakout_v5c_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260318T151759_opening_range_breakout_v5c_smoke\daily_equity.csv`

---

## EXP-20260318-003 | opening_range_breakout_v5c | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv5c #family/MES #interval/1m #sample/smoke #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `Config: configs\Archive\opening_range_breakout_v5c_smoke.json`
- **Strategy:** `opening_range_breakout_v5c`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2026-01-01 -> 2026-02-22`
- **Days Tested:** `1`
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
Run failed with error:
```
Parser Error: syntax error at or near "ROWS"

LINE 5:                         FIRST(open ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING...
                                           ^
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
- **Report Directory:** `Config: configs\Archive\opening_range_breakout_v5c_smoke.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260318-004 | opening_range_breakout_v5c | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv5c #family/MES #interval/1m #sample/smoke #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `Config: configs\Archive\opening_range_breakout_v5c_smoke.json`
- **Strategy:** `opening_range_breakout_v5c`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2026-01-01 -> 2026-02-22`
- **Days Tested:** `1`
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
Run failed with error:
```
Parser Error: syntax error at or near "ROWS"

LINE 5:                         FIRST(open ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING...
                                           ^
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
- **Report Directory:** `Config: configs\Archive\opening_range_breakout_v5c_smoke.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260318-005 | opening_range_breakout_v5c | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv5c #family/MES #interval/1m #sample/smoke #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `Config: configs\Archive\opening_range_breakout_v5c_smoke.json`
- **Strategy:** `opening_range_breakout_v5c`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2026-01-01 -> 2026-02-22`
- **Days Tested:** `1`
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
Run failed with error:
```
Parser Error: syntax error at or near "ROWS"

LINE 5:                         FIRST(open ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING...
                                           ^
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
- **Report Directory:** `Config: configs\Archive\opening_range_breakout_v5c_smoke.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260318-006 | opening_range_breakout_v5c | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv5c #family/MES #interval/1m #sample/smoke #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `Config: configs\Archive\opening_range_breakout_v5c_smoke.json`
- **Strategy:** `opening_range_breakout_v5c`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2026-01-01 -> 2026-02-22`
- **Days Tested:** `1`
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
Run failed with error:
```
Binder Error: Table function "read_parquet" does not support lateral join column parameters - cannot use column "catalog.stage5_bar_files.parquet_path" in this context.
The function only supports literals as parameters.

LINE 8:                     JOIN read_parquet(catalog.stage5_bar_files.parquet_path) on true
                                              ^
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
- **Report Directory:** `Config: configs\Archive\opening_range_breakout_v5c_smoke.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260318-007 | opening_range_breakout_v5c | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv5c #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260318T152657_opening_range_breakout_v5c_smoke`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T152657_opening_range_breakout_v5c_smoke`
- **Strategy:** `opening_range_breakout_v5c`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2026-01-01 -> 2026-02-22`
- **Days Tested:** `36`
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
| Final Equity | 99837.85 |
| Net PnL | -162.15 |
| Total Return % | -0.1622 |
| Max Drawdown Abs | 384.80 |
| Max Drawdown % | 0.38 |
| Daily Sharpe Approx | -1.1181 |
| Execution Count | 14 |
| Closed Trade Count | 7 |
| Win Rate % | 42.8571 |
| Gross Profit | 391.95 |
| Gross Loss | 558.65 |
| Profit Factor | 0.7016 |
| Trades / Tested Day | 0.19 |
| Approx Winning Trades | 3 |
| Approx Losing Trades | 4 |
| Approx Average Winner | 130.65 |
| Approx Average Loser | 139.66 |
| Approx Winner / Loser Ratio | 0.94 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T152657_opening_range_breakout_v5c_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260318T152657_opening_range_breakout_v5c_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260318T152657_opening_range_breakout_v5c_smoke\daily_equity.csv`

---

## EXP-20260318-008 | opening_range_breakout_v4 | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv4 #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260318T152754_opening_range_breakout_v4b_smoke`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T152754_opening_range_breakout_v4b_smoke`
- **Strategy:** `opening_range_breakout_v4`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2023-02-26 -> 2026-02-22`
- **Days Tested:** `31`
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
| Final Equity | 100011.45 |
| Net PnL | 11.45 |
| Total Return % | 0.0114 |
| Max Drawdown Abs | 81.10 |
| Max Drawdown % | 0.08 |
| Daily Sharpe Approx | 0.2241 |
| Execution Count | 8 |
| Closed Trade Count | 4 |
| Win Rate % | 50.0000 |
| Gross Profit | 148.80 |
| Gross Loss | 139.95 |
| Profit Factor | 1.0632 |
| Trades / Tested Day | 0.13 |
| Approx Winning Trades | 2 |
| Approx Losing Trades | 2 |
| Approx Average Winner | 74.40 |
| Approx Average Loser | 69.97 |
| Approx Winner / Loser Ratio | 1.06 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T152754_opening_range_breakout_v4b_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260318T152754_opening_range_breakout_v4b_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260318T152754_opening_range_breakout_v4b_smoke\daily_equity.csv`

---

## EXP-20260318-009 | opening_range_breakout_v5a | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv5a #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260318T153501_opening_range_breakout_v5a_smoke`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T153501_opening_range_breakout_v5a_smoke`
- **Strategy:** `opening_range_breakout_v5a`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2026-01-20 -> 2026-02-20`
- **Days Tested:** `24`
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
| Final Equity | 100063.90 |
| Net PnL | 63.90 |
| Total Return % | 0.0639 |
| Max Drawdown Abs | 132.45 |
| Max Drawdown % | 0.13 |
| Daily Sharpe Approx | 0.9644 |
| Execution Count | 6 |
| Closed Trade Count | 3 |
| Win Rate % | 66.6667 |
| Gross Profit | 195.05 |
| Gross Loss | 133.10 |
| Profit Factor | 1.4654 |
| Trades / Tested Day | 0.12 |
| Approx Winning Trades | 2 |
| Approx Losing Trades | 1 |
| Approx Average Winner | 97.53 |
| Approx Average Loser | 133.10 |
| Approx Winner / Loser Ratio | 0.73 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T153501_opening_range_breakout_v5a_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260318T153501_opening_range_breakout_v5a_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260318T153501_opening_range_breakout_v5a_smoke\daily_equity.csv`

---

## EXP-20260318-010 | opening_range_breakout_v5b | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv5b #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260318T153505_opening_range_breakout_v5b_smoke`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T153505_opening_range_breakout_v5b_smoke`
- **Strategy:** `opening_range_breakout_v5b`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2026-01-20 -> 2026-02-20`
- **Days Tested:** `24`
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
| Final Equity | 100063.90 |
| Net PnL | 63.90 |
| Total Return % | 0.0639 |
| Max Drawdown Abs | 132.45 |
| Max Drawdown % | 0.13 |
| Daily Sharpe Approx | 0.9644 |
| Execution Count | 6 |
| Closed Trade Count | 3 |
| Win Rate % | 66.6667 |
| Gross Profit | 195.05 |
| Gross Loss | 133.10 |
| Profit Factor | 1.4654 |
| Trades / Tested Day | 0.12 |
| Approx Winning Trades | 2 |
| Approx Losing Trades | 1 |
| Approx Average Winner | 97.53 |
| Approx Average Loser | 133.10 |
| Approx Winner / Loser Ratio | 0.73 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T153505_opening_range_breakout_v5b_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260318T153505_opening_range_breakout_v5b_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260318T153505_opening_range_breakout_v5b_smoke\daily_equity.csv`

---

## EXP-20260318-011 | opening_range_breakout_v2 | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv2 #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260318T153850_opening_range_breakout_v2_1m_smoke`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T153850_opening_range_breakout_v2_1m_smoke`
- **Strategy:** `opening_range_breakout_v2`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2025-12-20 -> 2026-02-20`
- **Days Tested:** `31`
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
| Final Equity | 99960.20 |
| Net PnL | -39.80 |
| Total Return % | -0.0398 |
| Max Drawdown Abs | 142.45 |
| Max Drawdown % | 0.14 |
| Daily Sharpe Approx | -0.6833 |
| Execution Count | 8 |
| Closed Trade Count | 4 |
| Win Rate % | 50.0000 |
| Gross Profit | 112.55 |
| Gross Loss | 154.95 |
| Profit Factor | 0.7264 |
| Trades / Tested Day | 0.13 |
| Approx Winning Trades | 2 |
| Approx Losing Trades | 2 |
| Approx Average Winner | 56.28 |
| Approx Average Loser | 77.47 |
| Approx Winner / Loser Ratio | 0.73 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T153850_opening_range_breakout_v2_1m_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260318T153850_opening_range_breakout_v2_1m_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260318T153850_opening_range_breakout_v2_1m_smoke\daily_equity.csv`

---

## EXP-20260318-012 | opening_range_breakout_v4 | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv4 #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260318T153854_opening_range_breakout_v4a_smoke`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T153854_opening_range_breakout_v4a_smoke`
- **Strategy:** `opening_range_breakout_v4`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2025-12-20 -> 2026-02-20`
- **Days Tested:** `31`
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
| Final Equity | 99960.20 |
| Net PnL | -39.80 |
| Total Return % | -0.0398 |
| Max Drawdown Abs | 142.45 |
| Max Drawdown % | 0.14 |
| Daily Sharpe Approx | -0.6833 |
| Execution Count | 8 |
| Closed Trade Count | 4 |
| Win Rate % | 50.0000 |
| Gross Profit | 112.55 |
| Gross Loss | 154.95 |
| Profit Factor | 0.7264 |
| Trades / Tested Day | 0.13 |
| Approx Winning Trades | 2 |
| Approx Losing Trades | 2 |
| Approx Average Winner | 56.28 |
| Approx Average Loser | 77.47 |
| Approx Winner / Loser Ratio | 0.73 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T153854_opening_range_breakout_v4a_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260318T153854_opening_range_breakout_v4a_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260318T153854_opening_range_breakout_v4a_smoke\daily_equity.csv`

---

## EXP-20260318-013 | opening_range_breakout | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakout #family/MES #interval/1m #sample/smoke #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260318T154152_opening_range_breakout_1m_smoke`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T154152_opening_range_breakout_1m_smoke`
- **Strategy:** `opening_range_breakout`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2025-12-20 -> 2026-02-20`
- **Days Tested:** `31`
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
| Final Equity | 99810.30 |
| Net PnL | -189.70 |
| Total Return % | -0.1897 |
| Max Drawdown Abs | 466.20 |
| Max Drawdown % | 0.47 |
| Daily Sharpe Approx | -1.7063 |
| Execution Count | 62 |
| Closed Trade Count | 31 |
| Win Rate % | 9.6774 |
| Gross Profit | 375.70 |
| Gross Loss | 585.55 |
| Profit Factor | 0.6416 |
| Trades / Tested Day | 1.00 |
| Approx Winning Trades | 3 |
| Approx Losing Trades | 28 |
| Approx Average Winner | 125.23 |
| Approx Average Loser | 20.91 |
| Approx Winner / Loser Ratio | 5.99 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T154152_opening_range_breakout_1m_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260318T154152_opening_range_breakout_1m_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260318T154152_opening_range_breakout_1m_smoke\daily_equity.csv`

---

## EXP-20260318-014 | opening_range_breakout_v3 | MES | 1m | SMOKE

**Tags:** #strategy/openingrangebreakoutv3 #family/MES #interval/1m #sample/smoke #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `Config: configs\Archive\opening_range_breakout_v3B_1m_smoke.json`
- **Strategy:** `opening_range_breakout_v3`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `SMOKE`
- **Date Range:** `2025-12-20 -> 2026-02-20`
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
- **Report Directory:** `Config: configs\Archive\opening_range_breakout_v3B_1m_smoke.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260318-015 | opening_range_breakout | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakout #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260318T154212_opening_range_breakout_15m_buffer_2ticks_1m`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T154212_opening_range_breakout_15m_buffer_2ticks_1m`
- **Strategy:** `opening_range_breakout`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2025-12-20 -> 2026-02-20`
- **Days Tested:** `43`
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
| Final Equity | 100177.15 |
| Net PnL | 177.15 |
| Total Return % | 0.1771 |
| Max Drawdown Abs | 487.45 |
| Max Drawdown % | 0.49 |
| Daily Sharpe Approx | 0.6532 |
| Execution Count | 86 |
| Closed Trade Count | 43 |
| Win Rate % | 9.3023 |
| Gross Profit | 995.10 |
| Gross Loss | 845.90 |
| Profit Factor | 1.1764 |
| Trades / Tested Day | 1.00 |
| Approx Winning Trades | 4 |
| Approx Losing Trades | 39 |
| Approx Average Winner | 248.77 |
| Approx Average Loser | 21.69 |
| Approx Winner / Loser Ratio | 11.47 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T154212_opening_range_breakout_15m_buffer_2ticks_1m`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260318T154212_opening_range_breakout_15m_buffer_2ticks_1m\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260318T154212_opening_range_breakout_15m_buffer_2ticks_1m\daily_equity.csv`

---

## EXP-20260318-016 | opening_range_breakout | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakout #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260318T154609_opening_range_breakout_15m_long_only_1m`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T154609_opening_range_breakout_15m_long_only_1m`
- **Strategy:** `opening_range_breakout`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2025-12-20 -> 2026-02-20`
- **Days Tested:** `43`
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
| Final Equity | 99622.75 |
| Net PnL | -377.25 |
| Total Return % | -0.3773 |
| Max Drawdown Abs | 411.15 |
| Max Drawdown % | 0.41 |
| Daily Sharpe Approx | -7.5574 |
| Execution Count | 60 |
| Closed Trade Count | 30 |
| Win Rate % | 6.6667 |
| Gross Profit | 112.55 |
| Gross Loss | 509.30 |
| Profit Factor | 0.2210 |
| Trades / Tested Day | 0.70 |
| Approx Winning Trades | 2 |
| Approx Losing Trades | 28 |
| Approx Average Winner | 56.27 |
| Approx Average Loser | 18.19 |
| Approx Winner / Loser Ratio | 3.09 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T154609_opening_range_breakout_15m_long_only_1m`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260318T154609_opening_range_breakout_15m_long_only_1m\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260318T154609_opening_range_breakout_15m_long_only_1m\daily_equity.csv`

---

## EXP-20260318-017 | opening_range_breakout | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakout #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260318T154613_opening_range_breakout_30m_1m`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T154613_opening_range_breakout_30m_1m`
- **Strategy:** `opening_range_breakout`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2025-12-20 -> 2026-02-20`
- **Days Tested:** `43`
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
| Final Equity | 99703.40 |
| Net PnL | -296.60 |
| Total Return % | -0.2966 |
| Max Drawdown Abs | 419.25 |
| Max Drawdown % | 0.42 |
| Daily Sharpe Approx | -2.7474 |
| Execution Count | 86 |
| Closed Trade Count | 43 |
| Win Rate % | 11.6279 |
| Gross Profit | 424.50 |
| Gross Loss | 749.05 |
| Profit Factor | 0.5667 |
| Trades / Tested Day | 1.00 |
| Approx Winning Trades | 5 |
| Approx Losing Trades | 38 |
| Approx Average Winner | 84.90 |
| Approx Average Loser | 19.71 |
| Approx Winner / Loser Ratio | 4.31 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T154613_opening_range_breakout_30m_1m`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260318T154613_opening_range_breakout_30m_1m\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260318T154613_opening_range_breakout_30m_1m\daily_equity.csv`

---

## EXP-20260318-018 | opening_range_breakout | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakout #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260318T154752_opening_range_breakout_30m_long_only_1m`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T154752_opening_range_breakout_30m_long_only_1m`
- **Strategy:** `opening_range_breakout`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2025-12-20 -> 2026-02-20`
- **Days Tested:** `43`
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
| Final Equity | 99885.15 |
| Net PnL | -114.85 |
| Total Return % | -0.1149 |
| Max Drawdown Abs | 233.75 |
| Max Drawdown % | 0.23 |
| Daily Sharpe Approx | -1.6298 |
| Execution Count | 56 |
| Closed Trade Count | 28 |
| Win Rate % | 14.2857 |
| Gross Profit | 252.60 |
| Gross Loss | 385.65 |
| Profit Factor | 0.6550 |
| Trades / Tested Day | 0.65 |
| Approx Winning Trades | 4 |
| Approx Losing Trades | 24 |
| Approx Average Winner | 63.15 |
| Approx Average Loser | 16.07 |
| Approx Winner / Loser Ratio | 3.93 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T154752_opening_range_breakout_30m_long_only_1m`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260318T154752_opening_range_breakout_30m_long_only_1m\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260318T154752_opening_range_breakout_30m_long_only_1m\daily_equity.csv`

---

## EXP-20260318-019 | opening_range_breakout | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakout #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260318T154756_opening_range_breakout_1m`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T154756_opening_range_breakout_1m`
- **Strategy:** `opening_range_breakout`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2025-12-20 -> 2026-02-20`
- **Days Tested:** `43`
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
| Final Equity | 100217.15 |
| Net PnL | 217.15 |
| Total Return % | 0.2171 |
| Max Drawdown Abs | 466.20 |
| Max Drawdown % | 0.47 |
| Daily Sharpe Approx | 0.7941 |
| Execution Count | 86 |
| Closed Trade Count | 43 |
| Win Rate % | 9.3023 |
| Gross Profit | 995.10 |
| Gross Loss | 805.90 |
| Profit Factor | 1.2348 |
| Trades / Tested Day | 1.00 |
| Approx Winning Trades | 4 |
| Approx Losing Trades | 39 |
| Approx Average Winner | 248.77 |
| Approx Average Loser | 20.66 |
| Approx Winner / Loser Ratio | 12.04 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T154756_opening_range_breakout_1m`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260318T154756_opening_range_breakout_1m\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260318T154756_opening_range_breakout_1m\daily_equity.csv`

---

## EXP-20260318-020 | hedging_demand_intraday_momentum_v1 | MES | 1m | FULL

**Tags:** #strategy/hedgingdemandintradaymomentumv1 #family/MES #interval/1m #sample/full #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `Config: configs\Archive\hedging_demand_intraday_momentum_v1_dev_a.json`
- **Strategy:** `hedging_demand_intraday_momentum_v1`
- **Strategy Archetype:** `unknown`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2025-12-20 -> 2026-02-20`
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
Unknown strategy 'hedging_demand_intraday_momentum_v1'.
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
- **Report Directory:** `Config: configs\Archive\hedging_demand_intraday_momentum_v1_dev_a.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260318-021 | opening_range_breakout_v5c | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv5c #family/MES #interval/1m #sample/full #status/failed #decision/tbd

**Status:** `FAILED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `unknown`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `Config: configs\active\opening_range_breakout_v5c_smoke.json`
- **Strategy:** `opening_range_breakout_v5c`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2025-12-20 -> 2026-02-20`
- **Days Tested:** `1`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Re-Test of V5c architecture over 40 days.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `V5c validation structure.`
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
  "volume_lookback_days": 20,
  "volume_surge_factor": 1.5,
  "signal_close_above_vwap": true,
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
Unknown strategy 'opening_range_breakout_v5c'.
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
- **Report Directory:** `Config: configs\active\opening_range_breakout_v5c_smoke.json`
- **Closed Trades CSV:** `unknown`
- **Daily Equity CSV:** `unknown`

---

## EXP-20260318-022 | opening_range_breakout_v5c | MES | 1m | FULL

**Tags:** #strategy/openingrangebreakoutv5c #family/MES #interval/1m #sample/full #status/completed #decision/tbd

**Status:** `COMPLETED`  
**Decision:** `TBD`

### Metadata
- **Run ID:** `20260318T163802_opening_range_breakout_v5c_smoke`
- **Run Date:** `2026-03-18`
- **Researcher:** `auto`
- **Code Version / Commit:** `main @ 63ed733`
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T163802_opening_range_breakout_v5c_smoke`
- **Strategy:** `opening_range_breakout_v5c`
- **Strategy Archetype:** `breakout`
- **Family:** `MES`
- **Interval:** `1m`
- **Sample Type:** `FULL`
- **Date Range:** `2025-12-20 -> 2026-02-20`
- **Days Tested:** `43`
- **Instrument Mode:** `dominant_by_day`
- **Instrument Key:** `None`

### Research Question / Hypothesis
Re-Test of V5c architecture over 40 days.

### Change Description
- **Parent Experiment:** `none`
- **What changed:** `V5c validation structure.`
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
  "volume_lookback_days": 20,
  "volume_surge_factor": 1.5,
  "signal_close_above_vwap": true,
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
| Final Equity | 99850.00 |
| Net PnL | -150.00 |
| Total Return % | -0.1500 |
| Max Drawdown Abs | 467.50 |
| Max Drawdown % | 0.47 |
| Daily Sharpe Approx | -0.9051 |
| Execution Count | 22 |
| Closed Trade Count | 11 |
| Win Rate % | 45.4545 |
| Gross Profit | 501.25 |
| Gross Loss | 651.25 |
| Profit Factor | 0.7697 |
| Trades / Tested Day | 0.26 |
| Approx Winning Trades | 5 |
| Approx Losing Trades | 6 |
| Approx Average Winner | 100.25 |
| Approx Average Loser | 108.54 |
| Approx Winner / Loser Ratio | 0.92 |

### Behavioral Read
TBD

### Interpretation
TBD

### Risk Notes
TBD

### Recommendation / Next Action
TBD

### Artifacts
- **Report Directory:** `E:\project_1L\marketdata\backtests\20260318T163802_opening_range_breakout_v5c_smoke`
- **Closed Trades CSV:** `E:\project_1L\marketdata\backtests\20260318T163802_opening_range_breakout_v5c_smoke\closed_trades.csv`
- **Daily Equity CSV:** `E:\project_1L\marketdata\backtests\20260318T163802_opening_range_breakout_v5c_smoke\daily_equity.csv`

---
