# Project 1L Opening Range Breakout Strategy Lineage
Version: v2.0
Status: Draft research specification
Design instrument: MES
Validation instrument: MNQ (frozen rules only)

---

## 1. Purpose

ORB-v2 is the first **trader-grade** version of the Opening Range Breakout family for Project 1L.

This version is not meant to be a "perfect strategy."
It is meant to be:

- explicit,
- testable,
- risk-defined,
- reproducible,
- and hard to overfit.

The goal is to move from:

- ORB-v0 = simple archetype screen

to:

- ORB-v2 = complete rule-based trading system

---

## 2. Core Design Principles

These are non-negotiable.

1. **Risk is defined before entry.**
2. **Initial stop is placed immediately.**
3. **Stops are never widened.**
4. **Trade management begins only after the trade has proven itself.**
5. **Trail is volatility-based, not emotional.**
6. **One good setup is enough; we do not machine-gun re-entries.**
7. **We validate on chronological out-of-sample data before even thinking about paper trading.**
8. **MES is the design market; MNQ is for frozen-rule validation, not re-optimization.**

---

## 3. Market / Data / Session

### Instrument
- MES only for design and initial validation

### Bar Interval
- 1-minute bars

### Session
- Regular trading hours only
- 08:30 to 15:00 America/Chicago

### Trade Direction for v2.0
- **Long-only**

Rationale:
- ORB-v1 testing showed the short side degraded the strategy materially on MES.
- v2.0 is not trying to be universal; it is trying to test the best current ORB branch cleanly.

---

## 4. Strategy Hypothesis

A disciplined ORB should work best when:

- the opening range is meaningful but not chaotic,
- price breaks the range with enough intent,
- the initial risk is defined structurally,
- the strategy removes full-loss risk once the breakout has proven itself,
- and the trade is trailed by volatility rather than by arbitrary percentages.

---

## 5. Definitions

### Opening Range (OR)
- The opening range is the first 15 minutes of the regular session:
- **08:30:00 through 08:44:59 CT**

### Opening Range Values
- `OR_high = highest high during opening range`
- `OR_low = lowest low during opening range`
- `OR_width = OR_high - OR_low`

### Entry Buffer
- `entry_buffer = 1 tick`

### Initial Stop Buffer
- `stop_buffer = 1 tick`

### Cost Buffer (in points)
This is the minimum favorable stop offset needed to cover modeled round-trip friction.

Formula:

`cost_buffer_points = (2 * slippage_ticks * tick_size) + (2 * commission_per_side / contract_multiplier)`

Under the current MES assumptions:
- slippage = 1 tick per side
- commission = 1.25 per side
- tick size = 0.25
- multiplier = 5.0

This yields:

`cost_buffer_points = 1.0 point`

### R-Multiple
For a long trade:

`R = entry_price - initial_stop_price`

This is the unit of risk used for all later management.

---

## 6. No-Trade Filter

v2.0 includes one broad, theory-driven opening-range quality filter.

### Opening Range Width Filter
Compute:

- `median_OR_width_20 = median of the prior 20 session OR_width values`

Trade only if:

- `OR_width >= 0.5 * median_OR_width_20`
- and
- `OR_width <= 2.0 * median_OR_width_20`

Interpretation:
- skip extremely quiet opens
- skip extremely chaotic opens

This is intentionally broad.
It is a structure filter, not a fine-tuned optimization knob.

### Additional no-trade rules
Do not trade if:
- fewer than 20 prior sessions exist for the filter
- the breakout has not triggered by the entry cutoff time
- the system has already taken its one allowed long attempt for the day

---

## 7. Entry Logic

### Entry Window
- Earliest possible entry: **08:45:00 CT**
- Latest new entry: **11:00:00 CT**

### Long Entry Trigger
Enter long when the **first 1-minute bar close** is:

`close > OR_high + 1 tick`

### Execution Model
For backtesting in the current bar-based engine:
- signal is generated on the close of the trigger bar
- fill is modeled on the next bar open

### Daily Attempt Limit
- **Maximum 1 long trade per day**
- No same-day re-entry after stop-out or exit

---

## 8. Initial Stop Logic

The stop is placed immediately upon entry.

### Initial Stop
`initial_stop = OR_low - 1 tick`

This is a **structural invalidation stop**.
The thesis is wrong if price breaks the opening range high and then fully fails back through the opening range low.

### Stop Behavior
- stop is live immediately
- stop is never widened
- stop can only move in the trade’s favor

---

## 9. Trade Management Logic

This is where ORB-v2 becomes a trader-grade system instead of a toy baseline.

### Phase 0: Fresh Entry
At entry:
- initial stop is active
- no trailing stop yet
- no discretionary action

### Phase 1: Prove the Trade
Do nothing until the trade reaches:

`+1.25R unrealized`

Reason:
- breakout systems often need some room
- moving to breakeven too early chokes trades
- we only reduce risk after the trade has actually shown follow-through

### Phase 2: Cost-Protected Stop
When maximum favorable excursion reaches `+1.25R`:
move stop to:

`entry_price + cost_buffer_points`

This does **not** mean emotional breakeven.
It means:
- the trade has proven itself,
- and we now require the worst-case exit to cover modeled round-trip friction.

### Phase 3: Volatility Trail Activation
When maximum favorable excursion reaches `+2.0R`:
activate a volatility trail.

Use:

`trail_stop = highest_close_since_entry - (3.0 * ATR_1m_20)`

Where:
- `ATR_1m_20` = 20-period ATR on 1-minute bars
- `highest_close_since_entry` = highest 1-minute close seen since the trade was opened

### Ratchet Rule
Once the ATR trail is active:

`active_stop = max(existing_stop, trail_stop)`

The stop ratchets upward only.
It never loosens.

---

## 10. Exit Logic

A long trade exits on the first event that occurs:

1. **Initial stop or active stop is triggered**
2. **Time stop at 13:30 CT**
3. **Session flatten at 15:00 CT** (safety / platform-level cleanup only)

### Time Stop
At **13:30 CT**, exit any open trade at market.

Reason:
- ORB is a morning-expansion strategy
- if the move has not resolved by early afternoon, the edge is weaker
- this prevents dead capital and late-session drift from dominating the trade

### No Profit Target in v2.0
There is **no fixed profit target** in v2.0.

Reason:
- breakout systems should be allowed to express positive skew
- the stop and trail should define the exit, not a capped target

---

## 11. Position Sizing

### Research Mode
- Fixed size: **1 MES contract**

Reason:
- first prove the edge
- do not let sizing hide weak logic

### Not Included in v2.0
- dynamic sizing
- volatility parity sizing
- Kelly-style sizing
- scaling in
- scaling out

Those come later, only after edge is proven.

---

## 12. Implementation Notes

### Important Backtest Reality Note
The current engine is a 1-minute bar replay engine, not a full intrabar stop simulator.

Therefore, the first implementation should be honest about the fill model:

- stop and trail behavior may initially be modeled from 1-minute bar closes with next-bar execution
- this is acceptable for research stage
- if ORB-v2 survives out-of-sample testing, then we improve the execution model

### Translation Rule
Any rule that sounds like:
- "the way a good trader would feel it"
must be translated into:
- a formula,
- a timestamp,
- a threshold,
- or a state transition.

No vibes.
Only rules.

---

## 13. What Is Explicitly NOT In ORB-v2

To keep this version testable and not overfit, v2.0 does **not** include:

- short-side logic
- news filters
- higher-timeframe trend filters
- VWAP filters
- overnight inventory filters
- multiple entries per day
- discretionary stop movement
- fixed profit targets
- partial exits

If v2.0 is promising, those become future experiments.
Not before.

---

## 14. Validation Plan

We do **not** optimize on the full three-year blob.

We validate chronologically.

### Proposed Split

#### Development Window
- 2023-02-26 to 2024-02-29

Use this window to:
- implement the strategy
- verify logic
- allow only limited, pre-declared rule adjustments

#### Validation Window
- 2024-03-01 to 2025-02-28

Use this window to:
- test the frozen rules
- judge whether the strategy survives outside the design period

#### Final Holdout Window
- 2025-03-01 to 2026-02-22

This is the final untouched MES confirmation set.

### Cross-Instrument Validation
Only after MES rules are frozen:
- run the exact same rule set on MNQ
- do not retune the logic for MNQ
- only update instrument-specific execution math (multiplier, tick value, costs)

---

## 15. Allowed Parameter Families

To avoid parameter explosion, ORB-v2 only allows a very small number of parameter families for controlled research.

Allowed families:
1. `opening_range_minutes`
2. `cost_protect_trigger_R`
3. `ATR_trail_period`
4. `ATR_trail_multiple`
5. `time_stop`
6. `OR_width_filter_bounds`

Not allowed:
- random indicator stacking
- multiple simultaneous filters
- 20 different exit modes at once

---

## 16. Promotion Gates

### Gate A: Worth Refining Further
ORB-v2 is worth refining only if:

1. Validation window is not economically broken
2. Holdout window is not economically broken
3. Combined out-of-sample behavior is meaningfully better than ORB-v1
4. Trade count is sufficient to trust the result
5. The strategy is not surviving on one lucky month

### Gate B: Paper-Ready Candidate
ORB-v2 is a paper-trade candidate only if all of these are true:

1. Rules are fully frozen
2. Validation window is positive after costs
3. Final holdout window is positive after costs
4. Combined out-of-sample profit factor is at least **1.10**
5. Combined out-of-sample average net trade is at least **1.5x modeled round-trip cost**
6. Max drawdown is acceptable for the intended deployment size
7. Frozen-rule MNQ validation is non-broken

If those conditions are not met:
- it is not paper-ready
- no matter how nice one backtest chart looks

---

## 17. Summary of the ORB-v2 Rule Set

### ORB-v2.0
- MES
- 1-minute bars
- RTH only
- Long-only
- 15-minute opening range
- 1-tick breakout buffer
- 1-tick stop buffer
- structural initial stop below OR low
- one long attempt per day
- no new entries after 11:00
- cost-protected stop at +1.25R
- 3 x ATR(20) trailing stop after +2R
- hard time exit at 13:30
- fixed 1-contract research sizing
- chronological validation before MNQ validation
- no paper trading until frozen-rule out-of-sample survival

---

## 18. Current Decision

This is the strategy spec to implement next.

Not because it is guaranteed to work.
But because it is the correct next scientific step:

- specific enough to test,
- disciplined enough to avoid vibes,
- and complete enough to resemble how a strong manual trader would actually manage the trade.

---

## 19. Benchmark Status
*Status updated: 2026-03-09*

ORB-v2 holds the historical record as the first fully specified baseline logic.
It has now been **superseded** as the official benchmark parent by **ORB-v6a**.

ORB-v6a retains all ORB-v2 logic but adds a single structural breakout bar close-location gate `(close - low) / (high - low) >= 0.70`, which demonstrably improved risk-adjusted performance on both Dev-A and Dev-B out-of-sample slices without breaking any other mechanics.

All future ORB research should branch from `opening_range_breakout_v6a` unless explicitly testing an isolated bare-bones structure.