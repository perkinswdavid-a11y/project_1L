# lbr_anti_3_10_16_v1 — Implementation Specification

**Memo reference:** `docs/research/strategies/lbr_anti_3_10_16_v1_memo.md`
**Date:** 2026-03-11

---

## 1. Data Specification
- **Bar type:** OHLCV at 1m granularity only. 
- **Timestamp convention:** bar_close CT.
- **Session window:** 08:30–15:00 CT.
- **Session timezone:** America/Chicago.
- **Instrument:** MES.v.0 (dominant-by-day).
- **Context instrument:** none (single-leg alpha).

## 2. Signal Computation
The core engine requires a stateful tracking of a modified MACD oscillator using Simple Moving Averages.
- `close_series`: Rolling window of the most recent 16+ bar closes within the current session.
- `sma_3`: `mean(close_series[-3:])`
- `sma_10`: `mean(close_series[-10:])`
- `fast_line`: `sma_3 - sma_10`
- `fast_line_series`: Rolling window of the most recent 16 `fast_line` values.
- `slow_line`: `mean(fast_line_series[-16:])` (This is the 16-period smoothing of the 3/10 difference).
- **Directional Slope computation:** Calculate the delta between the current `slow_line` and the previous `slow_line` to determine the intermediate momentum direction.

## 3. Entry Logic
- **Long Setup Conditions (All must be true):**
    1. **Intermediate Up-Trend:** `slow_line[0] > slow_line[1]` (Slow line is sloping up).
    2. **Pullback Confirmation:** The `fast_line` has been correcting downward toward the `slow_line` for at least 2–3 bars.
    3. **Price Condition (Shallow Flag):** The price pullback forms a shallow flag, demonstrating limited give-back against the prior impulse.
    4. **Hook Initiation:** The current bar closes with the `fast_line` hooking back up (`fast_line[0] > fast_line[1]`).
- **Short Setup Conditions:** Fully symmetric inverse of the Long logic.
- **Execution / Trigger:** Do not enter at market on the close. Instead, place a pending stop-market entry order at the high (for long) or low (for short) of the confirming signal bar.

## 4. Exit Logic
- **Primary Exit (Time-Based):** Exactly 3 bars after entry. Send a flatten signal.
- **Secondary Exit (Session End):** Forced flatten on the last bar of the session (14:59 CT).
- **Hard Stop:** Placed exactly 1 tick below the low of the signal bar (for longs) or 1 tick above the high of the signal bar (for shorts). No ATR trail.

## 5. Parameter Surface (Thin Parent Default)
- `session_start`: "08:30"
- `session_end`: "15:00"
- `osc_fast`: 3
- `osc_slow`: 10
- `osc_smooth`: 16
- `time_stop_bars`: 3
- `contract_multiplier`: 5.0 (MES)

## 6. Translation Discrepancy Risk (Audit)
- **Bar-Close vs Mid-Bar Hooks:** The "Anti" pattern is subjectively traded by looking at the oscillator intra-bar. A fast-line hook mid-bar might visually trigger discretion before the close. The replay agent can only see bar-closes. *Risk Status:* Medium. We might arrive late to the pullback resumption.
- **Regime Identification:** Discretionary traders visually identify a "fresh" trend breakout before trading the first pullback. The systematic parent relies purely on the 16-SMA slope as a proxy for "trend". It will indiscriminately trigger in chop rectangles when the MACD lines are woven together. *Risk Status:* High. This is the primary point of failure for systematic oscillators. Falsification tests must evaluate whether the raw hook edge survives the chop bleed.
- **Moving Average Types:** Some modern charting platforms substitute EMAs for Linda's original SMAs. We will strictly adhere to the 3-10-16 Simple Moving Averages. *Risk Status:* Low. Adherence is mechanically simple.
