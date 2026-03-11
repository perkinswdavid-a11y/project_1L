# Hedging Demand Intraday Momentum (v1)

## 1. Strategy Name
`hedging_demand_intraday_momentum_v1`

## 2. Parent Family Classification
`hedging_demand_intraday_momentum`

## 3. Source Basis
This strategy is based on the academic SSRN paper "Hedging Demand and Market Intraday Momentum." It exploits the finding that on trend days, the return of the last 30 to 45 minutes before the market close is positively predicted by the return from the open until that late-day window.

## 4. Core Hypothesis
Institutional administrators of leveraged ETFs and options market makers are structurally short gamma. On days where the market trends strongly in one direction, their delta exposure becomes severely unbalanced. To neutralize their books, they are mechanically forced to execute hedging trades in the same direction as the trend aggressively into the close, creating a predictable, self-fulfilling price continuation.

## 5. Market Logic
Measure the directional return of the session from the Regular Trading Hours (RTH) open until a late-day evaluation window. If the accumulated directional return exceeds a minimum strength threshold, enter a market order in the direction of the trend. Hold the trade through the anticipated hedging flow, exiting strictly before the closing bell settlement volatility.

## 6. Instrument Scope
- **Target:** MES (Micro E-mini S&P 500)
- **Why:** ES derivates possess the deepest options chains and the highest corresponding leveraged ETF flows (e.g., SPXL, SPXS), making them the optimum targets for structural hedging demand capture. 

## 7. Session Definitions
- **RTH Open:** 09:30 EST
- **Evaluation Time:** 15:30 EST
- **Exit Time:** 16:00 EST (Hard time stop to avoid the extreme volatility of the 16:15 settlement print)

## 8. Entry Logic
- At exactly the **15:30 EST** bar close, compute the session point move so far:
  `Point_Move = Close[15:30] - Open[09:30]`
- If `Point_Move >= 30.0` (a strong 30-point up day), go **Long** at the market.
- If `Point_Move <= -30.0` (a strong 30-point down day), go **Short** at the market.
- If the absolute `Point_Move` is less than 30.0 points, take no trades.
  *(Justification for v1: 30.0 points represents a solidly established directional trend in modern ES/MES regimes without being so extreme that it only triggers on outlier macro news days. It is cleanly transportable across price levels, unlike fixed percentages.)*

## 9. Exit Logic
- **Primary Exit:** Time-based exit exactly at the **16:00 EST** bar close.
- No profit targets in v1. The intent is to capture the full 30-minute structural flow window without artificial ceiling constraints.

## 10. Risk / Stop Logic
- **Initial Stop Loss:** Catastrophic hard stop only to protect against late-day news shocks. Fixed at **8.0 index points (32 ticks for MES)**.
  *(Justification for v1: A 15.0-point stop is disproportionately wide for a short 30-minute holding window. An 8.0-point stop tighter bound caps tail risk if MOC flows violently reverse the trend, but remains wide enough to survive standard 1-minute bar noise going into the close constraints.)*
- **Trailing Stop:** None. Keep the v1 implementation perfectly thin and transparent to measure raw expectancy.

## 11. Time Constraints
- Maximum **1 trade per day**.
- Strict entry only at the 15:30 EST trigger time. Any earlier signals are invalid. 

## 12. Required Inputs
- 1-minute primary continuous futures bar data (MES).
- No multi-leg data, no options flow feeds, and no level-2 order book required for the initial Dev-A test.

## 13. What Is Fixed vs What Is Tunable
- **Fixed:** The evaluation window (15:30 EST), the exit time (16:00 EST), and the requirement to only trade exactly with the day's trend. 
- **Tunable (Locked for Dev-A test):** 
  - Trend strength threshold: 30.0 index points
  - Hard stop loss: 8.0 points `(32 ticks)`

## 14. Dev-A Test Intent
The intent is to prove whether the raw, simplistic time-window momentum exhibits a statistically significant positive expectancy without overriding filters. If it has raw life, it proves the baseline structural flow exists and provides a framework for advanced optimizations. If it fails terribly, the generic "trade the trend into the close" adage is functionally un-tradable noise.

## 15. Known Risks / Failure Modes
- The 30.0-point threshold is theoretically arbitrary and may trigger on volatile, news-chop days lacking the necessary institutional gamma imbalance.
- Slippage and commission drag (1 to 2 ticks) consuming the entire late-day drift.
- Market-on-Close (MOC) flows activating early and forcing violent reversions at 15:45 EST.

## 16. Disqualifying Drift Rules
To preserve an honest, orthogonal test that avoids bleeding into existing Project 1L neighborhoods, it is absolutely forbidden to:
1. Contaminate this entry logic with Opening Range Breakout (ORB) signals or anchors.
2. Embed VWAP mean-reversion rules or moving average confirmation filters.
3. Turn this into a continuous intraday trend-following system (only the isolated 15:30 window matters).

## 17. Notes for Future Children
*(Only applicable if the v1 parent survives the Dev-A gate)*
If basic flow exhibits an edge, the next generation should seek to approximate actual "gamma imbalance." This could utilize VIX relative action, ETF volume spikes, or absolute point range rather than percentage range as a dynamic threshold. None of these belong in v1.
