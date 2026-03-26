# New Parent Family Spec Draft

**Family:** `mes_mnq_relative_mean_reversion_v1`
**Short Name:** `mes_mnq_rmr_v1`
**Status:** parent-family candidate (specification only, do not implement yet)

## Purpose

This is a new parent-family candidate, not an ORB child branch.

**Hypothesis:**
When MES and MNQ diverge abnormally on a normalized intraday basis after the opening range is complete, the relative divergence may mean-revert enough to support a tradable signal in MES.

This family is intentionally defined as a **raw market-edge test**.
Do not include specific payout-rule adaptations in this family spec.

## Instrument Roles

- **Traded instrument:** MES
- **Context instrument:** MNQ

**Interpretation:**
- this is not a full paired-trade hedge engine in v1
- MNQ is used as the relative-value context instrument
- MES is the only instrument traded in v1

## Inherited Session / OR Definition

Use the exact same session framework and opening-range construction already used by the current Project 1L futures research environment.

Do not change:
- session assumptions
- bar interval
- OR duration
- OR high / OR low computation

The family may reference OR-completion state, but it is not an ORB continuation family.

## Exact Rule Set To Lock Now

### 1. Bar synchronization rule

All relative-value calculations must use **completed bars with matched timestamps** between MES and MNQ.

**Interpretation:**
- use only timestamps where both instruments have completed bars available
- do not interpolate missing bars
- do not let one market lead or lag the other artificially in v1
- if one side is missing a completed bar for the timestamp, do not update the relative signal state for that timestamp

### 2. OR-completion anchor definition

For each instrument, define its post-OR reference anchor as:
- the close of the final completed bar inside that instrument’s opening-range window

Lock these terms conceptually:
- `mes_or_anchor_close`
- `mnq_or_anchor_close`

Also retain:
- `mes_or_width`
- `mnq_or_width`

### 3. Normalized post-OR move definition

For each matched completed timestamp after both OR windows are complete, define:
- `mes_normalized_move = (mes_close - mes_or_anchor_close) / mes_or_width`
- `mnq_normalized_move = (mnq_close - mnq_or_anchor_close) / mnq_or_width`

**Interpretation:**
- each market is normalized by its own OR width
- this keeps the family from comparing raw point moves across dissimilar contracts
- do not introduce rolling volatility normalization yet
- do not introduce beta adjustment yet

### 4. Relative divergence definition

Define relative divergence as:
- `relative_divergence = mes_normalized_move - mnq_normalized_move`

**Interpretation:**
- positive divergence means MES is relatively rich / extended versus MNQ
- negative divergence means MES is relatively cheap / lagging versus MNQ

### 5. Directional scope for v1

For v1, trade one side only:

- long MES only

**Interpretation:**
- v1 tests whether MES being abnormally weak versus MNQ creates a tradable long mean-reversion response
- do not add the short-MES mirror side yet

### 6. Divergence threshold

Arm the setup only when:

- `relative_divergence <= -0.75`

**Interpretation:**
- MES must be meaningfully weak relative to MNQ after OR normalization
- do not optimize this threshold yet
- do not add multi-threshold logic

### 7. Entry trigger

After the divergence threshold has been reached, enter long MES only when a later completed MES bar satisfies:

- `mes_close > prior_mes_bar_high`

**Interpretation:**
- do not buy immediately on extreme divergence
- require a completed-bar reversal confirmation in MES itself
- use the immediately prior completed MES bar high as the confirmation reference

### 8. Initial stop placement

Initial stop is placed just below the signal bar low.

**Interpretation:**
- use the completed MES bar that triggered the long entry
- do not use OR low
- do not use divergence-based stop distance
- do not trail yet
- if the engine already requires a minimum tick rule already used elsewhere, use only that existing minimum convention

### 9. Initial exit logic

Primary exit is divergence compression back to:

- `relative_divergence >= -0.25`

**Interpretation:**
- the trade is attempting to capture partial normalization, not necessarily full overcorrection
- do not add secondary targets
- do not add runner logic
- do not add trailing logic yet

### 10. Time stop

Apply a fixed time stop of 60 completed bars after entry when using 1-minute bars.

**Interpretation:**
- if the engine remains on 1-minute bars, implement as 60 completed bars after entry
- if implementation uses a different bar interval later, that assumption must be documented clearly

### 11. Trade frequency

- one trade per day maximum
- once the setup is consumed, do not re-arm additional sequences that day

### 12. Pre-entry invalidation

For v1, do not add extra invalidation beyond:
- OR completion for both instruments
- valid matched timestamps
- positive OR width for both instruments
- divergence threshold reached
- long reversal confirmation bar appears

No extra time-window invalidation yet.

## Parent-Family Context

**Note:** v1 is intentionally one-sided and thin because the purpose of the first parent test is to determine whether MES weakness versus MNQ after OR normalization has enough raw mean-reversion life to deserve further family development.
