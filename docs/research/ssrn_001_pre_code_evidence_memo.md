# SSRN-001 Pre-Code Evidence Memo — hedging_demand_intraday_momentum

## 1. Purpose
Evaluate whether `hedging_demand_intraday_momentum` deserves a formal strategy spec creation and Dev-A implementation in Project 1L, or whether it should be parked. This memo serves as a firm **go / park / reject** gate.

## 2. Candidate Summary
- **Source Family:** `hedging_demand_intraday_momentum`
- **Reference:** Academic paper, "Hedging Demand and Market Intraday Momentum."
- **Scope of Study:** Analyzed over 60 futures contracts across equities, bonds, commodities, and currencies from 1974 to 2020.
- **Core Finding:** The return of the last 30 minutes before the market close is positively predicted by the return evaluated throughout the rest of the trading day.
- **Underlying Mechanism:** Strongly linked to mechanical hedging demand from short-gamma market participants (e.g., options market makers and leveraged ETFs).

## 3. Why This Family Is Being Considered
This strategy is being considered as the inaugural non-ORB candidate to break outside the opening range discovery phase of the trading day. It is structurally sound, widely validated across decades of futures data, and built on known institutional order flow mechanics rather than price-action curve-fitting.

## 4. Core Market Logic
If the market trends significantly in one direction from the open until the final hour of trading, take a position in the direction of that trend for the final 30 minutes of the session. Exit at the close. 

## 5. Why It Might Exist
Institutional participants such as market makers who provide liquidity for options, and administrators of daily-reset leveraged ETFs, are often inherently "short gamma." As the market trends strongly in one direction during the day, their exposure becomes heavily skewed. To remain neutral and fulfill mandates, they are mechanically forced to execute hedging trades in the same direction as the trend aggressively into the close, creating a self-fulfilling price acceleration independent of fundamental news.

## 6. Why It Is Not Automatically Approved
A simplistic implementation risks becoming a naive "trade with the day trend into the close" toy. The engine could accidentally capture generalized end-of-day market-on-close (MOC) flows rather than true hedging-driven momentum. Without proper filtering (e.g., classifying a strong pre-existing trend threshold), the strategy will bleed slippage on choppy, mean-reverting days where hedging demand is nonexistent.

## 7. Project 1L Transfer Assessment
- **Parent-Family Status:** This is a true parent-family candidate rooted in microstructure mechanics, not just a narrow execution pattern.
- **Futures Compatibility:** Exceptionally high. The strategy was explicitly discovered and backtested on a broad universe of 60+ futures contracts.
- **Distinct from ORB:** Completely distinct. It operates at the extreme opposite end of the session (close vs. open) and exploits structural hedging flows rather than overnight information discovery. 

## 8. Required Data / Engine Fit
- **Data Availability:** Price-only intraday futures data (1-minute bars) is entirely sufficient for an honest baseline test. 
- **Engine Capabilities:** The current replay engine seamlessly supports this without any core architectural rewrites. The engine only needs to compute the return from the open up to a trigger point (e.g., 30 minutes before the close) and execute a time-stopped trade to the close.
- **Options Data Necessity:** While the underlying cause is options hedging, the effect manifests cleanly in the underlying futures price. Options data is not strictly required for a first-pass Dev-A implementation.

## 9. Likely Best Conditions
- **Regime:** High options volume, heavy speculative index usage, and clear, unidirectional trend days without overriding midday macroeconomic news prints.
- **Instruments:** Liquid equity index futures with massive corresponding options and leveraged ETF markets (e.g., ES, NQ).

## 10. Likely Failure Modes
- **Weak Trends:** Choppy or range-bound days where the pre-close trend threshold is met mechanically but lacks the underlying exposure imbalance to trigger a late-day squeeze.
- **MOC Volatility:** Getting chopped out by erratic market-on-close rebalancing that occurs precisely in the final 10 minutes, overshadowing the 30-minute structural flow.

## 11. Research Value Even If Rejected
If rejected at Dev-A, this effort still provides immense value by confirming whether late-day momentum is a myth in the modern ES/MNQ microstructure. It forces us to define what constitutes a "strong trend day" quantitatively within the Project 1L framework, creating reusable classification code for future regime filters.

## 12. Recommendation
**APPROVE FOR SPECIFICATION AND DEV-A.** Both the market logic and the data footprint are perfect matches for a thin, zero-friction implementation in Project 1L. It diversifies out of the ORB neighborhood while requiring zero infrastructure rebuilding.

## 13. Required Next Step
Draft the formal strategy specification (`docs/research/strategies/hedging_demand_intraday_momentum_v1_spec.md`) strictly defining the trigger threshold and timing mechanics for the MES benchmark.

## 14. Final Gate Status
**ACTIVE-GO**
