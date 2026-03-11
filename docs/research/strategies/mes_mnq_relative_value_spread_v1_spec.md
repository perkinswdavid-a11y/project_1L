# MES / MNQ Relative Value Spread (v1)

## 1. Strategy Name
`mes_mnq_relative_value_spread_v1`

## 2. Parent Family Classification
`relative_value_spread`

## 3. Source Basis
This strategy is the first **Project 1L operational pilot** for the QC-001 spread lane approved in the paired-futures transfer design memo.

It is **not** a faithful port of a dynamic multi-pair cointegration paper. It is a deliberately reduced, fixed-pair, synchronous two-leg parent intended to answer one narrow question:

**Can a simple, intraday, fixed-ratio relative-value spread between MES and MNQ show raw life inside current Project 1L constraints?**

This v1 parent is intentionally narrow:
- one fixed pair only
- synchronous matched-timestamp bars only
- fixed leg ratio
- no dynamic hedge ratio
- no pair selection
- no async lead-lag logic
- no portfolio-of-pairs behavior

## 4. Core Hypothesis
MES and MNQ are highly related U.S. equity index futures that often move together intraday but can temporarily diverge in a way that overshoots fair short-horizon relative value. When that divergence becomes sufficiently large over a short intraday window, the relative move partially mean-reverts. A paired long/short spread entered against the divergence may capture that reversion while reducing outright market-direction exposure compared with a single-leg trade.

## 5. Market Logic
1. Use MES and MNQ as a fixed intraday substitute pair.
2. Observe their matched-timestamp percent move from a fixed session anchor.
3. Compute the divergence between the two normalized moves.
4. When one leg has meaningfully outperformed the other beyond a fixed threshold, enter a spread betting on partial reversion:
   - long the lagging leg
   - short the leading leg
5. Hold the spread for a fixed intraday window or until a pair-level hard stop is hit.
6. Flatten both legs together.

This is a **relative-value mean-reversion** family, not a directional momentum or breakout family.

## 6. Instrument Scope
- **Leg A:** MES
- **Leg B:** MNQ
- **Bars:** 1-minute matched-timestamp bars
- **Session timezone:** CT
- **Multi-instrument requirement:** yes, but fixed to MES/MNQ only
- **Data rule:** use only bars where both instruments have the same completed timestamp

## 7. Session Definitions
- **RTH Open:** 08:30 CT
- **Signal Anchor Time:** 08:30 CT bar open
- **Evaluation Time:** 10:00 CT bar close
- **Primary Exit Time:** 14:30 CT bar close
- **Session-End Backstop Flatten:** 15:00 CT

The spread signal is measured only during the same RTH session. No overnight carry. No cross-session spread holding.

## 8. Spread Definition
At any matched timestamp `t`, compute normalized intraday move since the session anchor:

- `MES_Move(t) = (MES_Close(t) - MES_Open(08:30)) / MES_Open(08:30)`
- `MNQ_Move(t) = (MNQ_Close(t) - MNQ_Open(08:30)) / MNQ_Open(08:30)`

Define spread divergence as:

- `Spread_Divergence(t) = MNQ_Move(t) - MES_Move(t)`

Interpretation:
- positive divergence means MNQ has outperformed MES since the open
- negative divergence means MES has outperformed MNQ since the open

## 9. Entry Logic
Evaluate once per day at the **close of the 10:00 CT bar** using only matched completed MES/MNQ bars.

### Threshold rule
- If `Spread_Divergence >= +0.0030`:
  - **Long MES**
  - **Short MNQ**

- If `Spread_Divergence <= -0.0030`:
  - **Short MES**
  - **Long MNQ**

- If `|Spread_Divergence| < 0.0030`:
  - no trade

### Fixed ratio
For v1, use a simple fixed **1:1 contract count**:
- 1 MES
- 1 MNQ

This is intentionally crude and exists only to keep the parent thin. Ratio refinement belongs to later children if the parent survives.

### Entry timing rule
- Evaluate at the close of the 10:00 CT bar
- Submit both legs immediately after the 10:00 CT bar closes
- Fill both legs at the next available price under normal engine slippage assumptions
- Maximum 1 spread trade per day

## 10. Exit Logic
Exit both legs together under either condition:

### Primary time exit
- Flatten both legs at the **close of the 14:30 CT bar**

### Backstop session exit
- If still open for any reason, flatten both legs at session-end backstop 15:00 CT

No profit target in v1.

## 11. Risk / Stop Logic
Use a **pair-level hard stop** based on combined marked-to-market spread PnL.

### Hard stop
- Exit both legs immediately if combined open spread PnL reaches **-$200.00** or worse

This stop is pair-level, not per-leg.

### No other risk logic
- no trailing stop
- no profit target
- no dynamic resizing
- no volatility filter
- no correlation filter
- no hedge-ratio re-estimation

## 12. Time Constraints
- one evaluation time only: 10:00 CT bar close
- one maximum spread trade per day
- no entries after 10:00 CT
- no overnight hold
- no re-entry after stopout or time exit

## 13. Required Inputs
- 1-minute MES bars
- 1-minute MNQ bars
- matched completed timestamps only
- session anchor open prices for both instruments at 08:30 CT
- combined spread PnL tracking across two legs

No:
- options data
- level-2/order-book data
- async lead-lag logic
- rolling pair selection
- hedge-ratio estimation
- external indicators

## 14. What Is Fixed vs What Is Tunable

### Fixed for v1
- fixed pair = MES / MNQ
- matched-timestamp synchronous bars only
- one evaluation time = 10:00 CT bar close
- one exit time = 14:30 CT bar close
- fixed 1:1 contract count
- one spread definition
- one pair-level hard stop
- no targets
- no trailing
- no extra filters

### Locked initial values
| Parameter | v1 Value |
|---|---|
| Evaluation time | 10:00 CT bar close |
| Exit time | 14:30 CT bar close |
| Divergence threshold | 0.0030 |
| Contract ratio | 1 MES : 1 MNQ |
| Pair-level hard stop | -$200.00 |

These values are fixed for the parent Dev-A test.

## 15. Dev-A Test Intent
The Dev-A test answers one question:

**Does a simple fixed-ratio MES/MNQ relative-value divergence entered once intraday show positive raw expectancy before any ratio tuning, hedge-ratio work, filter stacking, or spread-engine expansion?**

The parent is not trying to prove the best spread construction. It is trying to prove that the spread lane has enough raw life to justify more infrastructure and more refined children later.

If the parent fails cleanly, then:
- no child branching
- no ratio tuning
- no threshold optimization
- no infrastructure expansion based on this lane alone

If it shows raw life, then later children may test:
- better ratio logic
- alternate evaluation times
- alternate spread thresholds
- better pair-level stop logic

## 16. Known Risks / Failure Modes
1. **1:1 ratio distortion:** MES and MNQ are not economically equivalent at a 1:1 count, so outright beta leakage may dominate the spread.
2. **False substitute assumption:** MES and MNQ may co-move, but the relative move may not mean-revert cleanly on the chosen intraday window.
3. **Trend day failure:** on powerful tech-led or broad-risk trend days, divergence may continue rather than revert.
4. **Threshold misspecification:** too low admits noise; too high produces too few trades.
5. **Spread lane too crude:** if the edge requires proper hedge ratio or volatility normalization, v1 may understate the lane unfairly.
6. **Execution asymmetry:** one leg may fill worse than the other under real slippage conditions.
7. **Residual directional exposure:** even as a spread, the position may still retain substantial market beta.

## 17. Disqualifying Drift Rules
Any modification introducing the following disqualifies the result as a test of `mes_mnq_relative_value_spread_v1` and must be branched separately:

1. dynamic hedge-ratio estimation
2. rolling pair discovery or pair selection
3. asynchronous lead-lag logic
4. multiple evaluation windows per day
5. VWAP filters
6. moving average filters
7. ORB logic
8. volatility filters
9. news filters
10. profit targets
11. trailing stops
12. ratio optimization inside the parent test

## 18. Notes for Future Children
*(Only applicable if the v1 parent survives Dev-A with evidence of raw edge)*

Potential child directions:
- ratio refinement child
- threshold sweep child
- alternate evaluation time child
- earlier exit / later exit child
- pair-level trailing stop child
- beta-normalized or volatility-normalized spread child

None of these belong in v1.
