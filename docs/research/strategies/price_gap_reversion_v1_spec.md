# price_gap_reversion_v1 — Implementation Specification

**Memo reference:** `docs/research/strategies/price_gap_reversion_v1_memo.md`
**Date:** 2026-03-10

---

## 1. Data Specification
- **Bar type:** 1m OHLCV
- **Timestamp convention:** bar_close CT
- **Session window:** 08:30–15:00 CT
- **Session timezone:** America/Chicago
- **Instrument:** MES.v.0 (dominant_by_day)
- **Context instrument:** none

## 2. Signal Computation
1. Collect the `prior_cash_close` (15:00 CT bar close) each day.
2. Collect the `08:30` open price for the current day.
3. Compute daily gap: `gap = open_0830 - prior_cash_close`
4. Maintain a rolling 60-day history of raw gap values (including zeros on non-gap days).
5. Before evaluating today's gap, compute the standard deviation of the history:
   `sigma_gap = std_dev(gap_history)`
6. Check signal instantly at the 08:30 bar close:
   - Calculate absolute gap: `abs_gap = |gap|`
   - Threshold met if: `abs_gap >= 3.0 * sigma_gap`
7. Determine direction:
   - If `gap > 0` (gap up), Signal = **SHORT**
   - If `gap < 0` (gap down), Signal = **LONG**
8. Append today's gap to the rolling history (pop oldest if > 60).

## 3. Entry Logic
- **Entry trigger:** 08:30 bar close signal.
- **Entry fill model:** next-bar open (08:31 bar open).
- **Slippage assumption:** 1.0 ticks.
- **Commission:** $1.25 per side per contract.
- **Position size:** 1 contract (MES).

## 4. Exit Logic
- **Primary exit (Target):** First bar whose range touches or crosses `prior_cash_close`.
  - Short position: `low <= prior_cash_close`
  - Long position: `high >= prior_cash_close`
- **Execution model:** Exit at next-bar open.
- **Time stop trigger:** 11:30 CT bar close.
- **Hard stop trigger:** $150 floating P&L loss on the position.
- **One trade per day:** YES. The strategy can only trigger at 08:30 and never re-enters.

## 5. Cost Model
- **Slippage:** 1 tick × 0.25 × $5 = $1.25 per side
- **Commission:** $1.25 per side
- **Total round-trip cost per trade:** $5.00 fixed.

## 6. Risk Controls
- **Max loss per trade (hard stop):** $150 (30 MES points).
- **Max trades per session:** 1.
- **Daily flatten:** YES (15:00 safety flat, though 11:30 time stop should handle it).
- **Pair-level stop:** N/A.

## 7. Contract Roll Handling
- **Instrument mode:** dominant_by_day. Handled by engine.

## 8. Required Outputs
- closed_trades.csv
- daily_equity.csv
- executions.csv
- summary.json
- Auto-log to strategy_experiment_log.md via research_logger (using specific extended window).

## 9. Edge Cases
- **Missing prior close:** No trade.
- **Missing 08:30 open:** No trade (anchor missing).
- **History < 2 days:** No trade (cannot compute sigma).
- **Sigma = 0:** No trade (avoid div/0 or false positives).
- **Gap already filled on the 08:30 bar itself:** No trade (if the 08:30 bar low/high touches the prior close, the opportunity is gone before the 08:31 open).
