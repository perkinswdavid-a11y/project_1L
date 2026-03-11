# New Parent Family Spec Draft

**Family:** `failed_opening_range_breakout_reversal_v1`
**Short Name:** `forb_reversal_v1`
**Status:** specification only (do not code yet)

## Purpose

This is a new parent-family candidate, not an ORB child branch.

**Hypothesis:**
When price makes a real upside opening-range breakout attempt but fails to hold above the range, the failure itself may create a tradable short back into the range.

This family is testing failed upside OR breakouts only.
Do not add the mirrored long side yet.

## Inherited OR Definition

Use the exact same opening-range construction already used by the current ORB family.
Do not change:
- OR duration
- session assumptions
- bar interval
- OR high / OR low computation

## Exact Rule Set To Lock Now

### 1. Upside breakout attempt definition

An upside breakout attempt is registered only when a completed bar satisfies both:
- `high > or_high`
- `close > or_high`

**Interpretation:**
- a wick above `or_high` by itself does not count
- the completed bar must finish outside the range on the upside
- use the first qualifying completed bar only to arm the setup

This breakout-attempt state becomes active only after OR completion.

### 2. Failure confirmation definition

Once an upside breakout attempt has been armed, failure confirmation occurs when a later completed bar satisfies:
- `close < or_high`

**Interpretation:**
- the market first proved it could close outside the range
- then it failed by closing back inside the range
- this close back below `or_high` is the failure-confirmation event

This failure-confirmation bar is the structural trigger for the short setup.

## Additional Structural Limits To Keep This Parent Thin

These are locked for the initial parent-family version:
- side: short only
- one breakout-attempt sequence per day
- once an upside breakout attempt is armed, do not re-arm multiple separate upside attempts the same day in v1
- do not add volume filters
- do not add VWAP filters
- do not add overshoot-distance filters
- do not add freshness windows yet
- do not add body-fraction filters
- do not add long-side symmetry yet

### 3. Short entry event

Enter short on the close of the failure-confirmation bar.

**Interpretation:**
- do not wait for another confirmation bar
- do not use next-bar breakout logic
- the completed bar that closes back below `or_high` is the short entry event

### 4. Initial stop placement

Initial stop is placed just above the high of the original upside breakout-attempt bar.

**Interpretation:**
- use the actual breakout-attempt bar that first armed the setup
- do not use the failure-confirmation bar high
- do not trail yet
- do not add buffers yet unless the engine requires a minimum tick rule already used elsewhere

### 5. Initial target logic

Initial target is `or_low`.

**Interpretation:**
- the first parent-family test asks whether failed upside breaks revert back through the range
- do not add secondary targets
- do not add runner logic
- do not add trailing logic yet

### 6. Pre-entry invalidation

For v1, do not add extra invalidation logic beyond the structural rules already defined.

**Interpretation:**
- no time invalidation window yet
- no maximum-bars-after-breakout-attempt rule yet
- no extra volatility or context invalidation yet

## 7. Parent-family question

The initial family question is simple: Can a real upside OR breakout attempt, followed by a close back below `or_high`, serve as the foundation for a short reversal family worth developing under SSVF?

v1 is intentionally broad because the purpose of the first parent test is to determine whether failed upside OR reversals have enough raw life to deserve further family development.

## Current Decision

The following are now provisionally locked for this family draft:
- OR definition: inherited unchanged from current ORB framework
- upside breakout attempt: `high > or_high` and `close > or_high`
- failure confirmation: later completed bar `close < or_high`
- side: short only
- status: parent-family candidate, not yet coded
