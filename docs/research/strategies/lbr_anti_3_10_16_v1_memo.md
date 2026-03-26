# lbr_3_10_16_anti — Strategy Memo

**Date:** 2026-03-11
**Author:** Antigravity / Agent
**Source:** Linda Bradford Raschke (LBR) "The Anti" (Street Smarts playbook)
**Gate A Outcome:** proceed-to-memo

**Gate A Verdict:** PASS
- **Market mechanism:** Profit-taking fade against intermediate momentum that is absorbed by larger trend participants re-entering.
- **Trigger condition:** Concrete 3-10-16 SMA oscillator hook against a 16-period slope.
- **Execution path:** Readily executable on standard 1m or 5m bar replay.
- **Futures relevance:** Intimately relevant to intraday ES/NQ where sharp pullbacks frequently trap counter-trend scalpers before the dominant session trend resumes.
- **Data availability:** 1m MES/MNQ OHLCV is abundant and cataloged.

---

## 1. Core Concept
The "Anti" is a classic pullback setup designed by Linda Raschke. It uses a customized 3-10-16 Simple Moving Average (SMA) oscillator to identify the first pullback after a trend shift. Traders enter when the fast short-term momentum (3/10 SMA difference) briefly hooks against the newly established medium-term momentum (16-period smoothing of the 3/10 difference), and then resumes in the direction of the medium-term trend.

## 2. Market Mechanism
**Institutional Absorption / Counter-Trend Trap:** When a new directional impulse establishes itself (slow line slopes up), the first counter-trend pullback (fast line hooks down) is often driven by early profit-taking or aggressive counter-trend scalping rather than a structural reversal. The "Anti" setup triggers when this counter-flow exhausts and the dominant impulse reasserts itself (fast line hooks back up), effectively trapping the counter-trend participants and forcing them to cover, which fuels the resumption of the trend.

## 3. Instrument Scope
- **Primary:** MES
- **Context instrument:** none
- **Session:** RTH (08:30–15:00 CT)

## 4. Trigger Definition (Thin Parent)
- **Signal Anchor:** 3-10-16 SMA Oscillator.
    - `Fast Line` = 3-period SMA of Close - 10-period SMA of Close.
    - `Slow Line` = 16-period SMA of the `Fast Line`.
- **Threshold for Long:** 
    1. **Trend:** Slow Line is sloping UP (positive).
    2. **Pullback:** Fast Line corrects downward toward the Slow Line for at least 2–3 bars.
    3. **Price Condition:** The pullback forms a shallow flag / limited give-back.
    4. **Hook:** Fast Line hooks UP (`Fast Line[0] > Fast Line[1]`).
- **Direction logic:** Place a pending stop-market buy order at the high of the signal bar after the hook. Short logic is fully symmetric.

## 5. Exit Definition (Thin Parent)
- **Primary exit:** Fixed hold time of exactly 3 bars.
- **Secondary exit:** Session flush at 14:59 CT.
- **Hard stop:** Placed exactly 1 tick below the signal bar low (for longs) or 1 tick above the signal bar high (for shorts). No ATR trailing stop. No recent swing low fallback.

## 6. Thin Parent Rules
- 1m bars only.
- MES only.
- No additional volume or VWAP filters.
- No time-of-day execution filters beyond standard RTH bounds.
- No profit targets; let the strict time exit or ATR flush rule represent the naked edge.
- Symmetrical parameters for longs and shorts.

## 7. Falsification Tests
- **Minimum PF threshold:** > 1.10 for "raw life".
- **Minimum trade count:** 30 closed trades minimum in Dev-A.
- **Payoff ratio floor:** 0.80 (win rate must compensate if payoff drops).
- **Specific rejection condition:** If the strategy hits its hard stop at a rate higher than 50% producing a heavy negative Net PnL, the 1-minute temporal resolution is likely aggregating away the micro-structural edge of the hook. 

## 8. Known Risks and Failure Modes
- **Regime dependency:** Range-bound chop will cause the 3-10-16 oscillator to generate excessive false hooks, bleeding capital to the spread.
- **Publication / practitioner decay:** As a classic textbook setup, the exact mechanic may have been front-run or squeezed by algos over the last two decades.
- **Execution latency:** The turning point of a fast moving average difference may occur rapidly mid-bar. Waiting for the 1-minute close might give up too much of the edge.

## 9. Infrastructure Requirements
- **New engine features required?** NO.
- **New data required?** NO. Standard 1m MES/MNQ bars.
- **Estimated implementation difficulty:** Low.
