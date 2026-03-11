# Project 1L — Translation Failure Audit

**Date:** 2026-03-10
**Subject:** Forensic review of strategy implementation failures
**Scope:** ORB variants, mes_mnq_relative_value_spread_v1, mes_mnq_co_oc_reversal_v1

---

## 1. ORB Neighborhood (Opening Range Breakout)

### 1. Real-world setup
Professional ORB trading treats the initial period (e.g., 08:30–08:45 or 08:30–09:30) as price discovery. Discretionary and structural traders mark the high and low of the range. The strategy requires a definitive structural breakout—often confirmed by momentum (tape speed), volume expansion, or a break-and-hold above the level. True professionals filter out "chop" days (trading inside yesterday's value area) and wait for days with clear directional bias. Entries are resting stop-limit orders at the exact breakout level, or limit orders on the first pullback.

### 2. What we coded
Project 1L implemented rigid mechanical variants (V2, V3, V4). The engine calculates the range high/low after $X$ minutes. For the rest of the day, if a bar closes outside the range, it signals. The entry is executed at the **next bar's open**. It trades blindly on any day where an arbitrary crossover occurs.

### 3. Mechanism preservation audit
**Failed.** Breakouts are pure momentum events. By forcing a bar-close-signal / next-bar-open-fill execution model, the system enters the trade *after* the initial breakout thrust has already occurred. Furthermore, by stripping out all context (daily bias, yesterday's value area, volume confirmation), it treats a 2-tick poke outside a narrow chop box identically to a massive trend-day breakout.

### 4. Execution-model audit
**Severe mismatch.** ORB depends heavily on exact pricing. Real setups use resting stop orders at the exact high/low to capture the immediate liquidity cascade. The Project 1L engine's "next-bar open" model absorbs the entire slippage of the breakout bar. In 15-minute or even 5-minute bars, buying the open of the bar *after* a breakout often means buying the exact local top right before the mean-reverting pullback.

### 5. Trade-frequency audit
**Overtrading.** The tested versions were "always on," indiscriminately taking breakouts every single day a boundary was crossed, completely ignoring whether the broader market regime supported trend continuation.

### 6. Thin-parent audit
**Aggressively distorted.** The mandate for a "thin parent" stripped away the essential microstructure and contextual filters required for momentum trading, reducing an execution-sensitive strategy to a crude, delayed crossover system.

### 7. Failure classification
**Execution-model mismatch & Missing context.**

### 8. Recommendation
**Infrastructure mismatch — do not test further in current engine.**
Breakout strategies require intrabar touch execution (resting stops/limits) and cannot be accurately evaluated using a next-bar-open bar-replay framework. The latency introduced by waiting for bar closure destroys the alpha.

---

## 2. `mes_mnq_relative_value_spread_v1` (QC-001)

### 1. Real-world setup
Pairs traders track two highly correlated assets. When the assets decouple beyond a historical or statistical threshold, they put on a spread trade (long the laggard, short the leader), expecting the correlation to reassert itself. The evaluation of the spread is continuous or highly frequent. Sizing is carefully beta-weighted or made strictly dollar-neutral so that directional market drift does not overwhelm the pair P&L.

### 2. What we coded
At exactly 10:00 CT every day, the system measures the percentage move of MES and MNQ from the 08:30 open. If the divergence is greater than 0.3%, it enters a 1:1 spread (Long 1 MES, Short 1 MNQ or vice versa) at 10:01. It holds until exactly 14:30.

### 3. Mechanism preservation audit
**Poor.** Mean-reverting dislocations do not follow wall clocks. A relative-value divergence might peak at 09:42, 11:15, or 13:00. By rigidly checking the divergence *only* at the 10:00 CT bar close, the strategy essentially rolls the dice on whether a structural dislocation happens to exist at that precise minute. Furthermore, sizing 1 MES ($5 multiplier) vs 1 MNQ ($2 multiplier) creates a highly imbalanced position that is overwhelmingly exposed to outright directional market drift, rather than pure relative value.

### 4. Execution-model audit
The execution model itself (split legs, next bar open) is acceptable for a 4.5-hour hold, but the strict time-based evaluation hook is an artificial constraint imposed by the implementation, not the strategy.

### 5. Trade-frequency audit
Under-evaluated. By only looking once per day at a specific minute, it dramatically reduced the opportunity set, missing genuine dislocations that occurred at 09:30 or 10:30.

### 6. Thin-parent audit
**Bad parent design.** The "thin" design requirement was misinterpreted as "must only evaluate once per day." A true thin parent for a divergence spread should evaluate continuously (every bar) but keep the *threshold* and *exit* logic simple. Additionally, failing to normalize the sizing ruined the mechanism.

### 7. Failure classification
**Bad parent design.**

### 8. Recommendation
**Needs context-preserving redesign before any further judgment.**
The arbitrary 10:00 CT evaluation must be removed in favor of continuous bar-close evaluation, and the leg sizing must be beta-normalized or at least dollar-normalized (e.g., 2 MES vs 5 MNQ) to remove directional drift.

---

## 3. `mes_mnq_co_oc_reversal_v1`

### 1. Real-world setup
The Overnight-Intraday (CO-OC) reversal trades on the premise that thin overnight sessions can be overextended by specific regional flows or lack of structural liquidity. When the US cash session opens, "real" liquidity arrives, often reversing the overnight positioning. However, professionals only fade the overnight move when there is a *significant* dislocation or climax.

### 2. What we coded
The system calculates the overnight returns for MES and MNQ. It immediately checks the difference: `delta_on = r_on_MNQ - r_on_MES`. If the difference is anything other than exactly zero (e.g., 0.001%), it enters a 3:2 spread at 08:31, fading the overnight leader. It holds all day until 15:00.

### 3. Mechanism preservation audit
**Poor.** The mechanism requires an overreaction to fade. By stripping out the threshold entirely, the system treats a microscopic 1-tick overnight divergence as identical to a massive 1% dislocation. It faded random noise.

### 4. Execution-model audit
Acceptable. Next-bar open at 08:31 is a realistic, achievable fill for a full-day hold.

### 5. Trade-frequency audit
**Massive overtrading.** The system traded 132 times out of 133 days in the Dev-A window. It forced the setup to be "always on." The real-world strategy is an opportunistic trade setup deployed 2-3 times a month, not an automatic daily ritual.

### 6. Thin-parent audit
**Aggressively distorted.** In the effort to make the parent "thin" (no parameters, no optimization), the implementation removed the core requirement for the mechanism to exist at all: a quantifiable dislocation. A setup that requires an extreme cannot be tested by feeding it the median.

### 7. Failure classification
**Overtrading / bad participation logic & missing context.**

### 8. Recommendation
**New parent warranted.**
The mechanism might still hold alpha, but it strictly requires an absolute minimum divergence threshold to activate. Testing an overreaction strategy without defining an overreaction guarantees failure via noise and cost drag.
