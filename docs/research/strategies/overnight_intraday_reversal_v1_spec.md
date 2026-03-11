# Overnight Intraday Reversal (v1)

## 1. Strategy Name
`overnight_intraday_reversal_v1`

## 2. Parent Family Classification
`overnight_intraday_reversal`

## 3. Source Basis
This strategy is a **single-instrument MES derivative** of the academic family documented as SSRN-003 in the Project 1L source library. The original academic study constructs a cross-sectional portfolio — buying the futures with the weakest recent overnight returns and selling the futures with the strongest recent overnight returns across a broad universe. That cross-sectional structure cannot be faithfully reproduced with a single instrument.

This v1 spec makes an explicit, honest reduction: it applies the same directional logic to a single MES instrument by treating the MES overnight gap itself as the signal. The gap’s sign determines direction; the gap’s magnitude determines whether to trade at all. This is a **labeled derivative**, not a faithful port of the published family. All experiment log entries for this family must note that distinction.

## 4. Core Hypothesis
Retail and low-information participants dominate more of the overnight / Globex session than the regular trading session, operating in thinner liquidity and wider effective spreads. Their directional positioning can overstate fundamental information and create temporary price dislocations relative to fair value. When the RTH session opens and institutional order flow enters, part of that overnight move is corrected. A strategy that fades a sufficiently large MES overnight gap should capture a portion of that correction during the RTH session.

## 5. Market Logic

1. Measure the overnight gap from the prior RTH close to the current RTH open.
2. If the gap is sufficiently large and positive, treat it as an overnight upward overreaction and fade it short.
3. If the gap is sufficiently large and negative, treat it as an overnight downward overreaction and fade it long.
4. Use the **open of the 08:30 CT bar** as the overnight gap anchor, but do not place the trade until the **08:30 CT bar has completed**.
5. Hold the position through the RTH session unless stopped out.
6. Flatten on a fixed intraday schedule before the close to avoid late-session MOC contamination.
7. Apply a hard stop only; no profit target in v1.

The signal is purely the **sign and magnitude of the overnight gap**. There are no intraday confirmation filters, no indicators, and no opening-range logic. This is a gap-first, direction-reversed entry with a time-based exit.

## 6. Instrument Scope
- **Target:** MES (Micro E-mini S&P 500)
- **Bars:** 1-minute continuous bars
- **Why MES:** Retains equity index futures characteristics and institutional flow dynamics while keeping contract risk appropriate for a Dev-A parent test
- **Multi-instrument:** None. This is a single-leg strategy.

## 7. Session Definitions
- **Session Timezone:** CT
- **RTH Open:** 08:30 CT
- **RTH Close / Session-End Flatten:** 15:00 CT
- **Prior RTH Close:** close of the final 1-minute RTH bar of the prior session, as identified by the engine immediately before the 15:00 CT session end
- **Current RTH Open Reference:** open of the 08:30 CT bar
- **Overnight Gap Window:** prior RTH close → current 08:30 CT bar open

The gap is measured strictly between the prior RTH session close and the current RTH session open. Globex activity between those two points is the signal source; it is not traded directly.

## 8. Entry Logic

**Evaluation and execution sequence (implementation-safe):**

1. At the **close of the 08:30 CT bar**, compute the overnight gap using the already-known opening print of that bar:

   `Gap = Open[08:30 CT bar] - Prior_RTH_Close_Price`

   *(in MES index points)*

2. Apply the threshold test:
   - If `Gap >= +8.0 points` → submit **Short** market order
   - If `Gap <= -8.0 points` → submit **Long** market order
   - If `|Gap| < 8.0 points` → **no trade** today

3. The order is generated only after the 08:30 CT bar has completed and fills at the next available price after the 08:30 CT bar close, subject to the engine’s normal slippage assumptions.

4. Maximum 1 trade per day.

**Threshold justification (8.0 MES index points):**  
8.0 points represents a meaningful overnight displacement while avoiding very small gaps that are more likely to be noise. It is intentionally simple for a first parent test and is fixed for Dev-A.

## 9. Exit Logic
- **Primary exit:** time-based flatten at the **close of the 14:30 CT bar**
- **Backstop exit:** engine session-end flatten at 15:00 CT if a position remains for any reason
- **Profit target:** none in v1

**Exit timing justification (14:30 CT):**  
The parent hypothesis is about the RTH reversal of the overnight gap, not late-session MOC behavior. Exiting at 14:30 CT keeps the test focused on the daytime reversal window and reduces contamination from late-session order imbalances.

## 10. Risk / Stop Logic
- **Hard stop:** 10.0 MES index points from entry fill
- **Trailing stop:** none in v1
- **Profit target:** none in v1

**Stop justification (10.0 points):**  
The holding window spans most of the RTH session. A 10.0-point stop keeps tail risk bounded on continuation days while still giving a multi-hour reversal trade enough room to work.

## 11. Time Constraints
- **Signal evaluation time:** close of the 08:30 CT bar
- **Signal anchor for the gap:** open of the 08:30 CT bar
- **Entry window:** one decision only, immediately after the 08:30 CT bar closes
- **Exit deadline:** close of the 14:30 CT bar
- **Maximum trades per day:** 1
- **Days with no qualifying gap:** no trade

## 12. Required Inputs
- 1-minute continuous MES bar data
- Prior RTH close price from the final 1-minute RTH bar of the prior session
- Current RTH open price from the **open of the 08:30 CT bar**

No multi-leg data. No options data. No external feeds. No indicators beyond the raw gap calculation.

## 13. What Is Fixed vs What Is Tunable

### Fixed for v1
- Entry direction logic: always **fade** the overnight gap sign
- Signal definition: prior RTH close → current 08:30 CT bar open
- Signal evaluation time: close of the 08:30 CT bar
- Execution timing: immediately after the 08:30 CT bar closes
- Exit timing: close of the 14:30 CT bar
- Single-leg, single-instrument (MES only)
- No intraday confirmation filters
- No profit target

### Locked initial values (tunable only in child branches after Dev-A result)
| Parameter | v1 Value |
|---|---|
| Gap threshold | 8.0 MES index points |
| Hard stop | 10.0 MES index points |
| Signal evaluation | 08:30 CT bar close |
| Signal anchor | 08:30 CT bar open |
| Exit time | 14:30 CT bar close |

These values are fixed for the Dev-A parent test.

## 14. Dev-A Test Intent
The Dev-A test answers one question:

**Does fading a qualifying MES overnight gap — defined from prior RTH close to current RTH open, entered after the first RTH minute, and held until 14:30 CT unless stopped — produce positive raw expectancy?**

The test is not trying to optimize parameters. It is checking whether:
- trade direction is correct often enough to matter
- the average winner / average loser profile is favorable enough to matter
- the strategy avoids failing simultaneously in both hit rate and payoff

If the parent shows no raw life, no rescue optimization or child branching is justified.

## 15. Known Risks / Failure Modes
1. **Trend continuation days:** strong overnight gaps can reflect real information rather than overreaction, and continuation can overwhelm the fade.
2. **News-driven gaps:** macro or geopolitical shocks may produce overnight moves that do not mean-revert intraday.
3. **Open-to-entry slippage:** the signal uses the 08:30 CT opening print, but execution occurs only after the 08:30 CT bar closes. If the market moves sharply in that first minute, realized entry may be materially worse than the gap anchor.
4. **Roll-induced artifacts:** contract roll behavior can create misleading apparent gaps that do not represent genuine overnight sentiment.
5. **Session-boundary sensitivity:** the prior RTH close must be identified consistently by the engine; boundary mistakes will corrupt the signal.
6. **Cross-sectional distortion:** the academic source is strongest in a ranked multi-instrument setting. A single-instrument MES derivative may be weaker or noisier than the source literature implies.

## 16. Disqualifying Drift Rules
Any modification that introduces the following features disqualifies the result as a test of `overnight_intraday_reversal_v1` and must be branched separately:

1. **Any opening-range or ORB logic**
2. **Any VWAP, moving average, or intraday indicator filter**
3. **Any additional entry delay beyond the 08:30 CT bar close**
4. **Any profit target**
5. **Any multi-instrument context signal**
6. **Any news filter or calendar exclusion rule**

## 17. Notes for Future Children
*(Only applicable if the v1 parent clears the Dev-A gate with evidence of raw edge)*

Possible child directions, one at a time:
- **Gap threshold sweep:** test alternative point thresholds
- **Exit time sweep:** test earlier intraday exits
- **Direction isolation:** long-only and short-only variants
- **Stop sweep:** test tighter and slightly wider hard stops
- **Trailing-stop child:** only if parent edge exists first
- **News-filter child:** only after parent viability is established

None of these belong in v1.
