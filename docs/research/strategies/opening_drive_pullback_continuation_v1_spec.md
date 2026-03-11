# New Parent Family Spec Draft

**Family:** `opening_drive_pullback_continuation_v1`
**Short Name:** `odpc_v1`
**Status:** parent-family candidate (specification only, do not implement yet)

## Purpose

This is a new parent-family candidate, not an ORB child branch.

**Hypothesis:**
When price establishes a real upside opening drive after the opening range, then pulls back in a controlled way that holds the breakout level, a later continuation through the pullback high may offer a tradable long continuation family.

This family is testing upside drive pullback continuation only.
Do not add the mirrored short side yet.

## Inherited OR Definition

Use the exact same opening-range construction already used by the current ORB family.

Do not change:
- OR duration
- session assumptions
- bar interval
- OR high / OR low computation

## Exact Rule Set To Lock Now

### 1. Upside opening drive definition

An upside opening drive is armed only when a completed bar satisfies both:
- `high > or_high`
- `close > or_high`

**Interpretation:**
- a wick above `or_high` alone does not count
- the completed bar must finish outside the range on the upside
- use the first qualifying completed bar only to arm the drive setup

This drive state becomes active only after OR completion.

### 2. Controlled pullback definition

Once an upside opening drive has been armed, a controlled pullback is registered when a later completed bar satisfies both:
- `low <= or_high`
- `close >= or_high`

**Interpretation:**
- the market revisits the breakout level
- the completed bar tests or touches the OR high area
- the market still holds that level by the close
- this is a pullback-hold event, not a failed breakout

Use the first qualifying completed pullback bar only.

### 3. Continuation confirmation definition

Once a controlled pullback has been registered, continuation confirmation occurs when a later completed bar satisfies:
- `close > pullback_bar_high`

**Interpretation:**
- the market first broke above the range
- then pulled back to the breakout level without failing
- then re-asserted continuation by closing above the high of the pullback bar

This continuation-confirmation event becomes the structural long trigger for the family.

## Additional Structural Limits To Keep This Parent Thin

These are locked for the initial parent-family version:
- side: long only
- one opening-drive sequence per day
- once an upside drive is armed, do not re-arm multiple separate upside drives the same day in v1
- do not add volume filters
- do not add VWAP filters
- do not add overshoot-distance filters
- do not add freshness windows yet
- do not add body-fraction filters
- do not add short-side symmetry yet

### 4. Long entry event

Enter long on the close of the continuation-confirmation bar.

**Interpretation:**
- do not wait for another confirmation bar
- do not use next-bar breakout logic
- the completed bar that closes above `pullback_bar_high` is the long entry event

### 5. Initial stop placement

Initial stop is placed just below the low of the pullback bar.

**Interpretation:**
- use the actual pullback bar that first registered the controlled pullback hold
- do not use the continuation-confirmation bar low
- do not trail yet
- do not add buffers yet unless the engine requires a minimum tick rule already used elsewhere

### 6. Initial target logic

Initial target is:
- `entry_price + or_width`

**Interpretation:**
- the first parent-family test asks whether a resumed upside continuation can produce at least one opening-range-width expansion from the continuation entry
- do not add secondary targets
- do not add runner logic
- do not add trailing logic yet

### 7. Pre-entry invalidation

For v1, do not add extra invalidation logic beyond the structural rules already defined.

**Interpretation:**
- no time invalidation window yet
- no maximum-bars-after-pullback rule yet
- no extra volatility or context invalidation yet

## 8. Parent-family question

The initial family question is simple: Can a real upside opening drive, followed by a controlled pullback that holds `or_high`, then a completed-bar continuation through the pullback high, serve as the foundation for a long continuation family worth developing under SSVF?

v1 is intentionally broad because the purpose of the first parent test is to determine whether upside opening-drive pullback continuation has enough raw life to deserve further family development.

## Current Decision

The following are now provisionally locked for this family draft:
- OR definition: inherited unchanged from current ORB framework
- upside opening drive: `high > or_high` and `close > or_high`
- controlled pullback: later completed bar `low <= or_high` and `close >= or_high`
- continuation confirmation: later completed bar `close > pullback_bar_high`
- side: long only
- status: parent-family candidate, not yet coded
