# QC-001 Follow-Up Memo — Paired Futures Transfer Design

- **Memo Date:** 2026-03-10
- **Researcher:** manual-entry
- **Candidate:** `QC-001 — spread_residual_cointegration`
- **Prior Gate Status:** parked-approved for further research

---

## 1. Purpose

Determine whether Project 1L should build **thin, reusable paired-futures spread infrastructure now**, and if so:

- which futures relationships are the best first candidates
- whether **substitute spreads** or **calendar spreads** should be the first lane
- what the **minimum honest infrastructure scope** is
- whether the expected research value justifies the cost now

This memo is a **go / park / reject** gate for the paired-futures transfer path. It is not a strategy spec or coding approval by itself.

---

## 2. Candidate Summary

QC-001 originated as a spread-residual mean-reversion family based on the idea that two economically related instruments can temporarily diverge from a stable relationship and later reconverge.

The original source was not futures-native, but the source library now contains enough futures-specific spread material to evaluate whether Project 1L should support a narrow paired-spread research lane.

Relevant futures spread archetypes now present in the source library include:

- WTI / Brent substitute spreads
- Treasury curve spreads
- energy crack spreads
- agricultural and STIR calendar spreads
- equity index intermarket spreads

That is sufficient to make an honest lane decision.

---

## 3. Core Decision

## Decision: APPROVE THIN PAIRED-SPREAD INFRA AND ADVANCE TO FORMAL SPEC PATH

But only under strict scope control:

- **first lane:** synchronous **two-leg substitute spread** research
- **not first lane:** calendar spreads
- **not first lane:** crack spreads or other complex multi-leg spreads
- **not first lane:** asynchronous lead-lag work
- **not first lane:** dynamic multi-pair selection or portfolio spread engines

Project 1L should not build a general spread platform now.

Project 1L should build only the **thinnest paired-spread lane necessary to test one fixed pilot pair honestly**.

---

## 4. Why This Lane Survives the Gate

This lane survives because it is:

- structurally different from the ORB / gap / late-day momentum neighborhoods already tested
- supported by real futures-native examples in the source library
- likely to produce reusable research infrastructure rather than one-off strategy code
- still narrow enough to build without turning the project into a spread-engine science fair

The key point is not that every spread family is attractive now.

The key point is that **paired spread capability has crossed the threshold from "interesting later" to "justified now," provided the build stays narrow**.

---

## 5. Which Futures Relationships Are Actually Candidates

## 5.1 First-wave candidates

### A. Same-session equity index substitute spreads

This is the cleanest first-wave bucket.

Examples:
- ES / RTY-style relative value
- other same-session, same-complex equity index relationships

Why this bucket is attractive:
- synchronous trading hours
- same broad asset class
- easier operationally than energy or calendar structures
- easier to reason about in Project 1L's current intraday framework

### B. Treasury yield-curve spreads

Treasury curve spreads are institutionally important and structurally strong.

Why this bucket is attractive:
- real relative-value logic
- exchange-standardized spread conventions exist
- highly reusable if the project later expands into rates

Why this is not the best first pilot:
- rates-specific sizing logic is a bigger domain jump
- likely heavier than needed for the first spread build

## 5.2 Strong later candidates

### C. WTI / Brent spread

This is a legitimate substitute spread family with real structural logic.

Why it belongs in the library:
- strong intuitive convergence case
- classic relative-value spread family

Why it is not first:
- more market-structure complexity
- less convenient as a first pilot than same-session equity index spreads

### D. Crack spreads

Crack spreads are a real structural family, but they are not a thin first build.

Why they should wait:
- multi-leg
- more complex sizing
- more operational burden than needed for the first pilot

## 5.3 Not first-wave candidates

### E. Calendar spreads

Calendar spreads are important and futures-native, but they are the wrong first lane.

They immediately introduce:
- multi-expiry contract handling
- roll logic
- month mapping
- contract lifecycle complexity

That is too much for the first paired-spread pilot.

---

## 6. Substitute Spread vs. Calendar Spread

## Decision: Start with substitute spreads, not calendar spreads

Why substitute spreads first:
- same-session, same-style two-leg evaluation is easier to implement honestly
- can be expressed with a fixed pair and fixed ratio
- no multi-expiry lifecycle required
- easier to isolate whether the edge is truly in relative-value reversion

Why calendar spreads should wait:
- they may be excellent long-term futures-native families
- but they are heavier operationally on day one
- they would force infrastructure decisions unrelated to the first QC-001 research question

Inference:
Project 1L should begin with **substitute spreads** because they minimize infrastructure cost while preserving the core spread-residual hypothesis.

---

## 7. Minimum Infrastructure Required

Project 1L should build only the following minimum paired-spread infrastructure:

## 7.1 Paired position object

Must support:
- leg A instrument
- leg B instrument
- side for each leg
- quantity / fixed ratio for each leg
- shared entry timestamp
- shared exit timestamp

## 7.2 Combined PnL accounting

Must support:
- realized PnL by leg
- total spread PnL
- combined commissions / slippage
- pair-level mark-to-market

## 7.3 Pair-level lifecycle handling

Must support:
- synchronized entry
- synchronized exit
- pair-level time exit
- pair-level hard stop
- emergency flatten if one leg fails

## 7.4 Minimal spread diagnostics

Must export:
- spread value at entry
- spread value at exit
- max favorable excursion of spread
- max adverse excursion of spread
- bars held
- exit reason

## 7.5 Fixed-ratio v1 only

For the first build:
- use a **fixed ratio** or explicitly fixed quantities
- do **not** build dynamic hedge-ratio estimation into infrastructure
- do **not** build rolling pair selection into infrastructure
- do **not** build portfolio-of-pairs support

## 7.6 Matched-timestamp rule stays in place for v1

Do **not** lift the matched-timestamp constraint yet.

Asynchronous lead-lag work is a separate infrastructure lane and should remain parked.

---

## 8. What Must Be Explicitly Excluded from v1

To keep the first spread build honest, the following must stay out:

- dynamic pair discovery
- intraday re-estimation of hedge ratios
- asynchronous lead-lag logic
- three-leg or four-leg spreads
- crack-spread modeling
- calendar-spread month selection
- portfolio optimization
- volatility targeting
- filter stacking
- machine-learning overlays

The first build is not a spread platform.

It is a **single fixed-pair, synchronous, two-leg spread test**.

---

## 9. Research Value vs. Cost

## Cost

The infrastructure cost is **medium**, not low.

It is materially more than adding another single-leg parent family because it requires:
- new position representation
- new PnL handling
- new diagnostics
- new failure handling

## Value

The research value is also real.

A successful thin spread lane would unlock:
- QC-001-style residual reversion
- equity index relative-value testing
- Treasury curve relative-value testing later
- WTI / Brent later
- broader spread-family research with real institutional structure

That is reusable research infrastructure, not one-off coding.

## Value vs. cost decision

The expected value justifies the cost **only if the build is narrow**.

If the scope expands beyond a thin fixed-pair synchronous pilot, the cost is not justified right now.

---

## 10. Recommendation

## Final Recommendation: GO, but only as a narrow pilot

1. **Advance QC-001 to the formal spec path**
2. **Build thin paired-spread infrastructure now**
3. **Start with substitute spreads, not calendar spreads**
4. **Use one fixed synchronous pair for the first pilot**
5. **Do not build broader spread capability yet**

## Preferred first pilot lane

Prioritize a **same-session, same-exchange, high-liquidity equity index spread** if the required data are already available.

That means:
- if Project 1L already has production-ready synchronized data for a same-complex equity pair, use that first
- do **not** start with WTI / Brent
- do **not** start with crack spreads
- do **not** start with calendar spreads

If existing synchronized production-ready data are currently limited to MES / MNQ, then a true paired MES / MNQ pilot is acceptable as the first operational pilot **only because it minimizes new data work**.

That does **not** mean MES / MNQ is automatically the best long-term spread family.
It means it is the cheapest honest first pilot.

---

## 11. Required Next Step

Create a formal strategy spec for a **single fixed-pair synchronous spread parent**, plus a companion implementation note for the minimum paired-execution infrastructure.

The next strategy spec should explicitly lock:
- the two instruments
- the fixed leg ratio
- the spread definition
- the entry threshold
- the exit logic
- the pair-level hard stop
- the session / flatten rules

No dynamic pair selection.
No calendar spread handling.
No asynchronous logic.

---

## 12. Final Gate Status

| Field | Value |
|---|---|
| **Decision** | APPROVE THIN PAIRED-SPREAD INFRA |
| **Spec path** | YES |
| **Immediate coding approval** | NO — spec first |
| **Preferred first lane** | synchronous two-leg substitute spreads |
| **Calendar spreads first?** | NO |
| **Complex multi-leg spreads first?** | NO |
| **Expected research value** | high enough if scope is narrow |
| **Main risk** | infrastructure bloat before alpha proof |
| **Main control** | one fixed pair, one fixed ratio, one thin parent only |
