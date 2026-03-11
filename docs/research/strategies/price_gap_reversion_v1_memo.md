# price_gap_reversion_v1 — Strategy Memo

**Date:** 2026-03-10
**Author:** Antigravity
**Source:** QuantConnect Algorithm.Python (PriceGapMeanReversionAlpha)
**Gate A Outcome:** proceed-to-memo

---

## 0. Gate A Evaluation
| Dimension | Evaluation | Pass? |
|---|---|---|
| **Market mechanism** | Gap-fill mean reversion driven by overnight liquidity voids and early cash-session profit taking. Extreme gaps (>3 sigma) represent structural overreactions rather than fundamental repricing. | YES |
| **Trigger condition** | 08:30 CT open price vs Prior Cash Close. Gap absolute magnitude >= 3x rolling standard deviation of historical gaps. | YES |
| **Execution path** | Next-bar open at 08:31 CT. Fade the gap (if gap up, short; if gap down, long). Exit on gap fill (target) or time stop. | YES |
| **Futures relevance** | Highly relevant. Equity index futures have distinct overnight vs RTH sessions, making opening gaps a primary structural feature. | YES |
| **Data availability** | Requires only 1m MES bars (prior close, 08:30 open). Readily available. | YES |

---

## 1. Core Concept
Fading the opening gap is a classic trading strategy. This variant filters out noise by enforcing a strict volatility threshold: it only fades *extreme* opening gaps that exceed 3 times the rolling standard deviation of recent gaps. By isolating the most violent overnight moves, it seeks to fade structural overreactions rather than fundamentally justified trend days.

## 2. Market Mechanism
The mechanism is **liquidity-driven overreaction and inventory unwinding**. Strong overnight moves are often driven by thin Globex liquidity reacting to international news or macroeconomic data releases (e.g., 07:30 CT CPI). When the cash session opens at 08:30 CT, massive institutional liquidity enters. Participants who rode the overnight move lock in profits (unwinding inventory), while market makers fade the extreme deviation to provide liquidity, forcing the price to partially or cleanly revert back toward the prior day's close (the "gap fill"). The 3-sigma threshold ensures we only trade when the imbalance is historically severe.

## 3. Instrument Scope
- **Primary:** MES (Micro E-mini S&P 500)
- **Context instrument:** None (single leg pure directional fade)
- **Session:** Intraday (08:31 CT entry, same-day exit)

## 4. Trigger Definition (Thin Parent)
- **Anchor:** 08:30 CT 1m bar.
- **Computation:** 
  - `gap = open_0830 - prior_cash_close`
  - `abs_gap = |gap|`
  - `rolling_gap_vol = std_dev(gap)` over the last 60 sessions.
- **Threshold:** `abs_gap >= 3.0 * rolling_gap_vol`
- **Direction:** 
  - If `gap > 0` (gap up), go SHORT.
  - If `gap < 0` (gap down), go LONG.

## 5. Exit Definition (Thin Parent)
- **Primary Exit (Target):** The gap fills. `current_price` crosses `prior_cash_close`.
- **Time Stop:** 11:30 CT (most structural reversion happens in the morning; holding into the afternoon exposes the trade to macro drift).
- **Hard Stop:** $150 per contract (equivalent to 30 MES points).

## 6. Thin Parent Rules
- No daily bias filter (no SMA/trend filter).
- No VIX filter.
- Fixed sizing: 1 MES contract.
- Max one trade per day.
- Hard threshold of 3.0 sigma; no parameter optimization.

## 7. Falsification Tests
- **Minimum PF threshold:** 1.10 (to warrant Dev-B).
- **Minimum trade count:** 30 closed trades in Dev-A. (If < 30, extend window or categorize as inconclusive).
- **Payoff ratio floor:** Average winner must be > 0.8x Average loser given the expected high win rate of gap fills.
- **Rejection condition:** If the extended backtest hits 30+ trades and the Profit Factor is < 1.00 net of costs, the 3-sigma gap fade does not carry alpha in MES and the parent is rejected.

## 8. Known Risks and Failure Modes
- **Trend-Day Steamroller:** Extreme gaps are sometimes the start of massive, fundamentally-driven trend days (e.g., a surprise Fed rate cut). Fading these days results in immediate maximum loss.
- **Sample Size:** 3-sigma events are by definition rare (~0.3% of a normal distribution). Reaching the 30-trade minimum may require testing 3–5 years of data.
- **Slippage at Open:** The 08:31 bar open can be extremely volatile; entering via market order next-bar might absorb severe adverse slippage.

## 9. Infrastructure Requirements
- **New engine features:** None.
- **New data:** None.
- **Implementation difficulty:** Low. Standard single-leg strategy.
