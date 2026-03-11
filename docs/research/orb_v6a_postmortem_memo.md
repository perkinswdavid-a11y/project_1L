# ORB-v6A Postmortem Memo

## 1. Purpose
This memo is a diagnostic review of the current ORB benchmark parent. Its purpose is to analyze the source of its edge, identify plausible leak points, and guide future research allocation away from exhausted mechanism clusters and toward evidence-driven discovery.

## 2. Benchmark Context
- **Parent Name:** `opening_range_breakout_v6a`
- **Validated Dev-A Metrics:** Net +687.50, PF 1.3701, Max DD 0.3170%, Trades 63
- **Validated Dev-B Metrics:** Net +441.25, PF 1.1869, Max DD 0.6688%, Trades 68
- **Accepted V6A Rule:** ORB-v2 base behavior + breakout bar close-location gate (`(close - low) / (high - low) >= 0.70`, zero-range bar fails).
- **Recent Child Branches Rejected:** V7A, V8A, V9A, V10A, V11A.

## 3. Artifacts Reviewed
- `E:\project_1L\marketdata\backtests\20260309T185654_opening_range_breakout_v6a_dev_a\summary.json`
- `E:\project_1L\marketdata\backtests\20260309T185654_opening_range_breakout_v6a_dev_a\closed_trades.csv`
- `E:\project_1L\marketdata\backtests\20260309T185710_opening_range_breakout_v6a_dev_b\summary.json`
- `E:\project_1L\marketdata\backtests\20260309T185710_opening_range_breakout_v6a_dev_b\closed_trades.csv`

## 4. Distribution of Edge
The Dev-A and Dev-B run outputs strongly suggest a top-heavy, early-session edge.
- **Signal Timing:** Profitability is concentrated in the immediate post-OR window. In Dev-A, trades opened in the 09:00 (Chicago) hour captured nearly all the Net PnL (898.75), while 10:00 hour trades contributed negatively (-258.75, 0% win rate). Dev-B similarly showed early strength with performance degrading deeper into the session.
- **Top Winner Contribution:** The edge is highly concentrated in a few large winners. The top 5 winners in both Dev-A and Dev-B contributed roughly 34-35% of the gross winning PnL.
- **Hold Times:** Winning trades often endure massive hold times. The average hold time sits near 160 minutes across both splits (Median ~160m, Max 285m), indicating the strategy relies heavily on capturing broad, persistent session trends rather than fast scalps.
- **Later-Session Breakouts:** Breakouts occurring late in the entry window consistently detract from the strategy's equity curve.

## 5. MAE / MFE Diagnostics
With newly exported `mae_r` and `mfe_r` metrics, the following structural dependencies become visible:
- **Winning Trade Profile:** The best winners frequently experience negligible adverse excursion (`mae_r` roughly between 0.35 to 0.54R) while generating extremely deep favorable excursions (`mfe_r` > 1.4R to 2.8R). In simpler terms, winning V6A setups tend to be right cleanly.
- **Losing Trade Profile:** Losers generally trigger `initial_stop` exits without generating substantial intervening favorability. A vast majority of stopped-out losers display `mfe_r` of less than 0.45R, strongly aligning with the observation that fake-out momentum dies quickly.
- **Adverse Excursion Thresholds:** When trades do endure severe adverse excursions approaching 1R (e.g., `mae_r` > 1.1), they almost universally fail.

## 6. Exit Reason Diagnostics
The backtest engine diagnostic upgrade enables us to explicitly categorize edge contribution and hold-time characteristics by ExitReason taxonomy.

| split | exit_reason | Count | Avg Net PnL | Avg MAE_R | Avg MFE_R | Avg Bars Held |
|---|---|---:|---:|---:|---:|---:|
| Dev-A | `initial_stop` | 24 | -$74.01 | 1.20 | 0.41 | 69.8 |
| Dev-A | `time_stop` | 25 | +$59.45 | 0.54 | 1.44 | 258.4 |
| Dev-A | `trailing_stop` | 10 | +$98.62 | 0.43 | 2.23 | 148.8 |
| Dev-A | `cost_protect` | 3 | -$7.08 | 0.20 | 1.81 | 150.7 |
| Dev-A | `daily_flatten` | 1 | +$12.50 | 0.59 | 0.59 | 209.0 |
| Dev-B | `initial_stop` | 33 | -$68.45 | 1.16 | 0.37 | 86.0 |
| Dev-B | `time_stop` | 24 | +$62.29 | 0.44 | 1.40 | 259.4 |
| Dev-B | `trailing_stop` | 9 | +$133.89 | 0.35 | 2.88 | 132.1 |
| Dev-B | `cost_protect` | 2 | $0.00 | 0.27 | 1.47 | 111.0 |

- `time_stop` **Dominance:** `time_stop` trades heavily dominate the positive net PnL generation simply by sheer volume of enduring the session (`258+ bars avg`). While many result in scratch trades, their presence captures outlier trailing trends.
- `initial_stop` **Efficiency:** Full `initial_stop` events accurately purge early failures (~80 bars) without excessive leakage. The average `mfe_r` before stop out is critically weak (`0.37` to `0.41`).
- `trailing_stop` **Contribution:** The undeniable heavy lifter. `trailing_stop` trades yield the highest average `Net PnL` and peak `MFE_R` while holding roughly 130-150 minutes, securing the massive outlier gains.
- **Weaknesses:** `cost_protect` events are present but minimal.

## 7. Leak Points and Failure Patterns
- **Late Entries:** The sharpest measurable leak point is late-session engagement. Trades triggering an hour or more after the OR completes (10:00 hour entries) exhibit materially lower win rates and negative net returns.

## 8. What Recent Rejections Taught Us
The consecutive rejections of V7A, V8A, V9A, V10A, and V11A mapped out several exhausted idea neighborhoods:
- **Null-Delta Rules (V7A, V11A):** Attempting to filter out poor follow-through via stringent signal-bar close constraints (`close >= entry_trigger`) or immediate post-entry reversals (closing back below trigger on bar 1) returned null impacts, definitively indicating these specific weakness patterns were already cured by V6A's close-location gate.
- **Over-filtering (V8A, V9A, V10A):** Targeting geometry (body fractions > 50%), anti-chase limits, or tight freshness cutoffs collapsed the trade count and stripped away necessary runners. The strategy fundamentally requires breathing room; aggressively gate-keeping the setup tends to cut out the highly skewed top 5 winners that float the entire strategy, turning a positive expectancy negative.
- **Summary:** The mechanism clusters surrounding *breakout-bar geometry*, *chase limits*, and *micro-continuation on bar 1* appear locally exhausted.

## 9. Current ORB Research Guidance
- **Paused Clusters:** All further research into breakout-bar geometry, anti-chase filters, freshness cutoffs, and immediate post-entry candlestick failure tests must remain mathematically paused.
- **Pre-Code Evidence Requirement:** No further local ORB child branches may be implemented without a structured pre-code evidence memo demonstrating precisely where targeted leak trades exist in the current parent trade logs.
- **Next Required Diagnostics:** Additional ORB diagnostic efforts should map time-in-trade distributions against `mae_r` specifically targeting how fast fake-outs die.

## 10. Broader Research Allocation Guidance
- The ORB strategy family is just one sleeve, not the totality of Project 1L.
- `opening_range_breakout_v6a` remains the active and successful ORB benchmark parent.
- Research allocation must broaden: broader family discovery outside pure ORB boundaries remains necessary to build an absolute portfolio edge.

## 11. Final Recommendations
1. **Leverage New Diagnostics:** Regularly execute `mae_r` and `mfe_r` diagnostic scans before authoring new branches.
2. **Shift Research Allocation:** Execute independent, non-ORB parent-family discovery tracks. Having already tested and rejected `forb_reversal_v1`, `odpc_v1`, and `gir_v1`, future external discovery lanes must pivot to completely divergent un-tested paradigms (e.g., relative mean reversion logic such as the new `mes_mnq_rmr_v1` spec).
3. **Lock V6A:** Retain `opening_range_breakout_v6a` as the frozen benchmark for the ORB sleeve while external discovery takes priority.
