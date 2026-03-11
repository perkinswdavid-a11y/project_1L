# mes_mnq_co_oc_reversal_v1 — Strategy Memo

**Date:** 2026-03-10
**Author:** manual-entry
**Source:** CO–OC overnight–intraday reversal literature; MES/MNQ paired application
**Gate A Outcome:** PROCEED TO MEMO
**Gate B Status:** APPROVED — advance to implementation

---

## 1. Core Concept and Mechanism

This strategy trades relative overnight overreaction between MES and MNQ.

At the cash open, measure which contract outperformed overnight and which underperformed. Enter long the overnight loser and short the overnight winner, expecting partial relative reversal during the cash session.

**Named mechanism:** Closure-driven overnight relative displacement partially reverses during the next cash-session auction. Overnight positioning/inventory pressure in the outperforming leg creates a mean-reverting imbalance that resolves intraday.

---

## 2. Instrument Scope

- **Instruments:** MES and MNQ
- **Contract economics:** MES multiplier = `$5 × index`, MNQ multiplier = `$2 × index`
- **Minimum tick:** `0.25` for both contracts

---

## 3. Session Scope

- **Signal window:** prior cash close → current cash open
- **Trade window:** current cash session only
- **Session anchors:**
  - Cash open: `08:30 CT`
  - Cash close boundary: `15:00 CT`

---

## 4. Formal Hypothesis

**Dependent variable**
Same-day cash-session pair return of a fixed MES/MNQ spread unit entered after the cash open and exited at the cash-close boundary.

**Independent variable**
Relative overnight return:
```
delta_on = r_on_MNQ - r_on_MES
r_on_i   = ln(open_0830_i / prior_cash_close_i)
```

**Hypothesis statement**
When MNQ outperforms MES overnight (`delta_on > 0`), MES will outperform MNQ during the following cash session; when MES outperforms MNQ overnight (`delta_on < 0`), MNQ will outperform MES during the following cash session.

Trade: **long the overnight loser, short the overnight winner.**

**Falsification conditions** (defined before Dev-A runs):
1. Net expectancy of the long-loser / short-winner pair is non-positive after realistic costs
2. The sign-flipped (long-winner / short-loser) rule performs similarly or better
3. Results collapse under 1–2 ticks of slippage per leg
4. P&L is dominated by a small number of dates rather than broad daily participation
5. The effect exists only in one volatility regime and disappears in another

---

## 5. Trigger Definition

For each instrument:
```
r_on_MES = ln(open_0830_MES / prior_cash_close_MES)
r_on_MNQ = ln(open_0830_MNQ / prior_cash_close_MNQ)
```

Decision rule:
- `delta_on > 0` → MNQ = overnight winner, MES = overnight loser
- `delta_on < 0` → MES = overnight winner, MNQ = overnight loser
- `delta_on = 0` → no trade

**Thin parent uses no threshold filter.** It trades every eligible day.

---

## 6. Entry Logic

Engine model: bar-close-signal / next-bar-open-execution.

- Compute overnight returns using the `08:30` bar open and prior cash close
- Evaluate signal on the `08:30` bar close
- Enter at the `08:31` bar open

**Trade direction:**
- Long overnight loser
- Short overnight winner

---

## 7. Sizing

Fixed ex-ante spread unit: **3 MES vs 2 MNQ**

Approximate notional balance at ~4500 MES / ~16000 MNQ:
- 3 MES ≈ 3 × 5 × 4500 = $67,500
- 2 MNQ ≈ 2 × 2 × 16000 = $64,000

Directional mapping:
- `delta_on > 0` (MES loser) → long `3 MES`, short `2 MNQ`
- `delta_on < 0` (MNQ loser) → long `2 MNQ`, short `3 MES`

**This is the fixed parent ratio. Do not optimize inside the parent.**

---

## 8. Exit Logic

Primary exit: time-based.

- Time-exit signal on the `14:59` bar close
- Time-exit execution at the `15:00` bar open

---

## 9. Hard Stop

- **Pair hard stop: `-$300 per spread unit`**
- Computed from combined MES + MNQ marked-to-market P&L each bar close
- If pair P&L ≤ `-$300` at any bar close → flatten at next bar open
- No re-entry that day

This is a risk cap, not an alpha filter.

---

## 10. Thin-Parent Rules

- One daily decision
- No threshold filter on `delta_on`
- No volatility filter
- No macro filter
- Fixed `3:2` MES/MNQ spread unit
- One entry max per day
- Time exit mandatory (`14:59` bar close signal)
- Hard stop mandatory (`-$300` pair P&L floor)
- No re-entry after stop or exit

---

## 11. Known Risks and Failure Modes

- Real repricing days where the overnight winner continues leading intraday (news continuation)
- Macro-driven or style-rotation days producing persistent MES/MNQ divergence
- Session-boundary or roll-handling errors creating false overnight return measurements
- Notional imbalance at extreme price levels (3:2 ratio drifts if MES/MNQ ratio changes materially)
- Cost drag: two-leg round-trip must clear commission + slippage on both entry and exit

---

## 12. Infrastructure Requirements

- Dual-leg execution infrastructure: already preserved from QC-001 pilot (`context_leg_cash_delta` pattern in engine)
- Synchronized 1m MES and MNQ bars: already in Project 1L catalog
- Prior cash close for each instrument: available from daily session segmentation
- New engine features required: **NO** (existing split-execution model is sufficient)
- Estimated implementation difficulty: **medium** (two-leg P&L accounting, overnight return computation)

---

## 13. Gate A Summary

| Dimension | Status |
|---|---|
| Market mechanism | ✅ Named: closure-driven overnight relative displacement reversal |
| Trigger condition | ✅ Defined: `delta_on = r_on_MNQ - r_on_MES` at `08:30` bar close |
| Execution path | ✅ Bar-based, next-open fill, existing dual-leg infrastructure |
| Futures relevance | ✅ MES/MNQ native, correct multipliers and tick sizes |
| Data availability | ✅ 1m synchronized bars already in catalog |

**Gate A: PASS → PROCEED TO MEMO → APPROVED FOR IMPLEMENTATION**
