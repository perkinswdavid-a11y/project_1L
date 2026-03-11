# Translation Failure Audit — mes_mnq_co_oc_reversal_v1

**Date:** 2026-03-10
**Family:** CO–OC overnight–intraday reversal (MES/MNQ pair)
**Subject:** Evaluation of thin-parent implementation vs real-world strategy setup

---

## 1. Real setup
The professional or discretionary version of the overnight winner/loser intraday reversal trade (CO-OC fade) is an opportunistic, context-dependent relative value setup. It is deployed when one highly correlated instrument has made an extreme, outsized move overnight relative to its pair, driven by thin liquidity, specific regional flow, or positioning imbalances.

The contextual elements normally determining whether this trade is taken include:
- A significant, quantifiable minimum dislocation threshold (e.g., a divergence that is 2+ standard deviations above the rolling mean, or an absolute percent difference that is visually obvious).
- Confirmation that the divergence is not driven by instrument-specific hard news (e.g., an earnings gap in a major component that justifies the permanent repricing).
- A conviction that early cash-session liquidity is entering to normalize the structural imbalance, often seen in the first 15-30 minutes of cash trading.

## 2. What I coded
The implementation tested the following exact logic:
- **Trade every eligible day:** Zero threshold required. Even a 0.0001% overnight divergence triggered a trade.
- **08:31 entry:** Blindly execute at the open of the first 1-minute bar following the 08:30 evaluation.
- **15:00 exit:** Hold the position absolutely until the end of the cash session boundary, ignoring any intraday convergence.
- **Fixed 3:2 ratio:** Hardcoded contract ratio regardless of exact relative notional parity on the day.
- **No threshold:** Any non-zero `delta_on` fired the signal.
- **No selection filter:** No volatility regime, macro event, or news exclusion.
- **Next-bar-open execution:** Suffer 1 tick of slippage per leg on the entry bar open, absorbing early volatility.
- **Pair hard stop:** A strict -$300 marked-to-market stop enforced at the end of each completed 1-minute bar.

## 3. Translation gap
The following core attributes were lost in translation between the real strategy and the coded thin parent:
- **Selective participation:** The real setup trades the extremes (e.g., 20 times a year). The coded setup traded the median (132 times in 6 months).
- **Thresholding:** Ignoring the magnitude of the divergence means fading random noise. Reversals require an overreaction to fade; the thin parent defined *every* move as an overreaction.
- **Regime context:** No filtering for trending vs mean-reverting broader market environments.
- **Event-day exclusion:** No logic to avoid trading into CPI, NFP, or FOMC days where overnight moves are fundamental, not structural imbalances.
- **Execution style:** Real setups might enter via limit orders against the extreme, or wait for the first 5-minute break back inside the range. The coded version slammed market orders at exactly 08:31 regardless of tape structure.
- **Holding-window mismatch:** Most overnight reversions resolve in the first 1-2 hours of the cash session. Holding until 15:00 exposed the pair trade to the entire afternoon macro drift, long after the overnight positioning had been flushed.
- **Spread construction mismatch:** A fixed 3:2 ratio drifts as the underlying index prices drift. Real pairs use dynamic beta-weighting or exact dollar-neutrality at the time of entry.

## 4. Execution-model audit
The real setup likely depended on several execution elements that the bar-replay engine does not replicate well:
- **Open auction behavior:** Real practitioners might participate directly in or immediately after the cross. A 08:31 next-bar-open entry might be systematically after the sharpest part of the opening reversion has already occurred.
- **Limit participation instead of market entry:** Fading an extreme often involves posting resting limit orders to capture the spread differential, rather than crossing the spread twice and paying aggressive slippage.
- **Shorter hold window:** Professional discretionary traders do not hold a morning mean-reversion trade until 15:00. They exit early when convergence happens, or trailing stop the position.
- **Partial exits or trade management:** Taking off risk as the gap fills is a standard discretionary tactic not captured by a strict 15:00 time exit.

## 5. Participation audit
Trading every eligible day was **structurally wrong**. The mechanism relies on the unwinding of unsustainable overnight inventory. In normal overnight sessions with balanced, low-volume trading, there is no inventory pressure to unwind. By forcing the strategy to trade on days with mere noise-level divergences, the implementation guaranteed that the majority of trades lacked any statistical edge. The real setup plausibly trades only on *extreme overnight dislocations*.

## 6. Cost-drag audit
The negative Net PnL (-$2,632) was primarily caused by:
- **Overtrading and Two-leg cost drag:** The gross profit ($16,785) and gross loss (-$23,347) show significant churn. Paying two commissions and two sides of slippage every single day to capture a non-existent edge on median-noise days guaranteed failure.
- **Excessive holding window:** Holding until 15:00 introduced massive intraday variance and noise, diluting any potential morning reversion alpha and triggering unnecessary -$300 hard stops. 
- **Incorrect direction on noise days:** On days without a true dislocation, there is no edge to fading the "loser". The signal simply picked a side randomly based on microscopic overnight variations and paid the spread to find out.

## 7. Failure classification
**Overtrading / missing threshold**

## 8. Recommendation
**Redesign parent before judging family**
