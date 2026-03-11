# SSRN-003 Pre-Code Evidence Memo — overnight_intraday_reversal

- **Memo Date:** 2026-03-10
- **Researcher:** manual-entry
- **Source Candidate:** SSRN-003 — overnight_intraday_reversal
- **Source Library Status at Memo Time:** parked parent-family candidate

---

## 1. Purpose

Evaluate whether `overnight_intraday_reversal` deserves:
- formal strategy spec creation
- Dev-A implementation inside Project 1L
- or should be parked or rejected at this gate

This memo is a **go / park / reject** gate only.
It is not implementation approval by itself.
No strategy code, no config, no spec, and no engine changes are authorized by this memo.

---

## 2. Candidate Summary

- **family name:** `overnight_intraday_reversal`
- **source type:** SSRN academic paper (high-quality primary source)
- **source quality:** high
- **current status:** parked parent-family candidate
- **horizon:** intraday
- **implementation difficulty:** low (per source library assessment)
- **transfer risk to Project 1L:** low (per source library assessment)

Core idea as described in the academic source:
- Buy futures with **low past overnight returns** (negative overnight gap)
- Sell futures with **high past overnight returns** (positive overnight gap)
- Hold intraday during the regular session
- Capture the mean-reversion of the overnight gap during the RTH session

Stated rationale: retail-driven over-reaction during the illiquid overnight/Globex window is systematically corrected by institutional order flow during the regular session.

---

## 3. Why This Family Is Being Considered

This candidate survives initial screening because it is:

- based on a **high-quality academic source** with a specific, falsifiable structural claim
- mechanically distinct from the exhausted ORB neighborhood in direction, trigger, and timing
- intraday in horizon, fitting Project 1L's current replay infrastructure
- low in stated implementation difficulty and data complexity
- compatible with Project 1L's existing session-boundary data segmentation
- captured explicitly alongside a note calling it "a direct complement to our existing ORB logic, acting as a structural gap fade"

The source library note confirms the surface-level appeal. This memo tests whether that appeal survives skeptical scrutiny.

---

## 4. Core Market Logic

The academic market logic is:

1. During the overnight / Globex session, volume is thin and participant quality is skewed toward retail
2. Retail traders over-react to news or momentum, pushing prices directionally overnight
3. When institutional participants enter during the RTH session, they recognize the overreaction and fade it
4. This produces a systematic intraday reversal of the prior overnight gap direction

The critical structural claim:
- The **overnight return predicts** the intraday return **in the opposite direction**
- This is not just noise — it is argued to be a replicable, institutional-flow-driven effect
- The signal is the **magnitude and sign of the overnight gap**, not intraday momentum

This is a **gap-fade family**, not a breakout family.
The triggers, directions, and timing windows differ structurally from ORB.

---

## 5. Why It Might Exist

Plausible structural reasons this edge could exist:

- **Liquidity asymmetry between sessions:** overnight markets are thin; retail-initiated price moves encounter little friction
- **Institutional re-anchoring at the open:** large participants reposition against overnight extremes, creating systematic reversal pressure
- **Mean reversion to fair value:** futures prices dislocated from fundamental equilibrium by thin-market noise are pulled back when liquid session opens
- **Structural predictability not yet fully arbitraged:** if the effect is real and documented academically, it exists because it requires patience and tolerance of overnight risk that most retail participants cannot sustain

These reasons are plausible at the conceptual level. They do not, by themselves, prove the effect exists or persists on MES at Project 1L's granularity and cost assumptions.

---

## 6. Why It Is Not Automatically Approved

### 6.1 The source is cross-sectional; Project 1L is single-instrument

The academic study almost certainly constructs returns by ranking a **universe of futures contracts** by overnight return and going long the weakest and short the strongest. This is a **cross-sectional momentum/reversal** strategy.

Project 1L runs single-instrument tests on MES. Applying a cross-sectional ranking strategy to a single instrument does not reproduce the academic family. It creates a version that:
- has no cross-sectional component
- cannot distinguish "relatively weak" versus "absolutely weak"
- must redefine the signal as absolute overnight gap direction, not relative ranking

This is a **meaningful source transfer distortion**. The single-instrument version is not the same family as published.

### 6.2 The single-instrument version may still be honest — but it needs to be explicit

A single-instrument version of this idea would become:
- If MES gapped down overnight: go long at the open, expect intraday reversal
- If MES gapped up overnight: go short at the open, expect intraday reversal
- Exit at session close or at a defined target / stop

This is a **gap fade** strategy on MES. It is a legitimate trade concept with its own academic and practitioner support. But it is **not the SSRN-003 paper's strategy**. The implementation must be labeled as a single-instrument derivative, not a faithful port.

### 6.3 Conceptual proximity to ORB creates contamination risk

ORB on MES also begins at the session open and involves a directional decision. The direction is opposite — ORB fades consolidation and trades breakouts; gap fade trades directional overreactions and reverses them. But the structural neighborhoods overlap sufficiently that:
- parameter choices can bleed between families
- failure to distinguish the hypothesis clearly creates noise in the research log
- if the gap fade improves ORB performance when added as a filter, it may not be a standalone family

The memo must ask: is overnight_intraday_reversal a **standalone parent family** or an **ORB entry-filter idea in disguise**?

Verdict from this memo: it can be structured as a genuine standalone family if the signal is the **overnight return** and the **entry is directionally opposite to that return**, with no ORB range construction involved. The families can be kept orthogonal.

### 6.4 Session segmentation implementation is a real question

A reliable overnight_intraday_reversal implementation requires:
- Clean Globex-to-RTH session segmentation (prior-close to current-open return)
- Consistent overnight return measurement (which close and which open?)
- Threshold logic to decide when the overnight gap is "large enough" to trade
- A decision on whether to trade every gap or only threshold-crossing gaps

This is not a blocker — Project 1L's data has 1-minute bars across both sessions — but it is a **design decision that must be made explicitly** in the spec before coding.

### 6.5 Low stated difficulty may be optimistic

The source library calls this "low" implementation difficulty. That is fair at the logic level. But:
- the threshold definition for "low enough" overnight return is non-obvious
- session-boundary PnL attribution (entry at RTH open, exit at RTH close) must be consistent
- slippage/commission assumptions at the open bar are sensitive assumptions
- detecting overnight direction on 1-minute bar data requires a precise close-to-open calculation

These are solvable, but they are not trivial engineering choices.

---

## 7. Project 1L Transfer Assessment

### 7.1 What transfers well

- **Data:** Project 1L holds continuous MES 1-minute bars that span both Globex and RTH. Overnight sessions are present.
- **Session logic:** Project 1L's engine already supports session-based entry/exit (flatten-daily, RTH-only execution).
- **Directional entry:** the engine supports long-only, short-only, or both directions at the bar level.
- **Horizon fit:** intraday; closes each session. Aligns perfectly with the current engine's flatten-daily behavior.
- **Infrastructure:** no new engine work is needed for a thin first implementation. A strategy class reading the prior-session gap and entering at open is achievable within the current `on_bar()` contract.

### 7.2 What does not transfer cleanly

- **Cross-sectional ranking:** cannot be reproduced with one instrument. The single-instrument version uses absolute gap direction, not relative ranking. This is an honest reduction, not corruption, but it must be labeled explicitly.
- **Academic effect size:** the published edge is measured across a universe. On a single instrument, variance is higher, sample is smaller, and the raw effect may not be detectable.
- **Overnight gap on continuous futures:** overnight sessions have lower volume and potentially wider bid-ask spreads. If the gap is caused by roll or low-liquidity noise rather than genuine retail over-reaction, the hypothesis breaks.

### 7.3 Transfer verdict

The transfer is **defensible but reduced**. A single-instrument MES gap-fade implementation is a credible, honest test of the core idea at Project 1L scale — provided the implementation note explicitly states it is a single-instrument derivative of a cross-sectional source, not a faithful port of the published family.

---

## 8. Required Data / Engine Fit

| Requirement | Status |
|---|---|
| 1-minute MES bars across Globex and RTH | Available |
| Prior-session close price (for overnight return calc) | Derivable from existing data |
| RTH session open price (first RTH bar) | Derivable from existing data |
| Session flatten / EOD exit logic | Existing engine support |
| Directional entry based on prior gap | Within current `on_bar()` contract |
| No new engine work required for thin first test | Confirmed |

No infrastructure blockers. A thin implementation is feasible on current Project 1L replay infrastructure without engine changes.

---

## 9. Likely Best Conditions

The overnight_intraday_reversal family would most likely work when:

- **Overnight move is clear and directional** — not a small, ambiguous drift
- **Overnight move is driven by retail overreaction** rather than fundamental news (e.g., scheduled economic data release that institutional participants treat as informative would not reverse)
- **RTH session is liquid** — strong institutional flow at the open correcting the gap
- **Gap threshold is right-sized** — too small a threshold admits noise; too large reduces trade frequency to the point of statistical irrelevance on MES
- **Post-open reversal window is defined** — gaps that do not reverse quickly may not reverse at all; holding all day amplifies risk

---

## 10. Likely Failure Modes

- **Trend continuation days:** overnight gap is a correct leading indicator, not overreaction. Going against the gap direction is immediately punished.
- **News-driven gaps:** scheduled macro events (CPI, FOMC, NFP) move futures overnight for fundamental, not behavioral, reasons. A gap fade on a genuine fundamental shock is a losing trade category.
- **Ambiguous gap size:** small overnight returns may not carry a directional signal worth fading. Threshold too low = noisy entries; threshold too high = very few trades on MES.
- **ORB overlap confusion:** if the strategy fires on a day where ORB would also fire, the two ideas may trade in opposite directions without clearly attributing which hypothesis is being tested.
- **Commission / slippage at the open:** entry at the first RTH bar may involve elevated slippage if the market is moving quickly from the overnight position. Assumed 1-tick slippage may underestimate true open-bar friction.
- **Roll-induced overnight gaps:** near contract expiration, overnight MES moves can be distorted by rolling behavior rather than genuine directional sentiment.

---

## 11. Research Value Even If Rejected

Even if the family is eventually rejected at Dev-A, it justifies:

- **Explicit session segmentation logic** that could be reusable as an entry filter or regime signal across other strategies
- **Gap measurement infrastructure** (prior-close to RTH-open return) that other intraday families may benefit from
- **Clear empirical test** of whether MES exhibits intraday reversal of overnight gaps — a falsifiable result that is worth having in the research log regardless of direction
- **ORB contamination boundary clarification** — running this separately from ORB forces explicit documentation of where the two hypotheses diverge, which is useful even if both families later fail

This is not rationalization for implementation. It is an honest assessment that the data generated, even from a quick Dev-A run, would have positive information value.

---

## 12. Recommendation

### Current recommendation: ADVANCE TO FORMAL SPEC

`overnight_intraday_reversal` passes the evidence memo gate for the following reasons:

1. **High-quality academic source** with a specific, defensible structural claim
2. **Mechanically distinct from ORB** when implemented faithfully as a gap fade — the signal, direction, and entry timing are all different
3. **No engine work required** for a thin Dev-A implementation on current Project 1L infrastructure
4. **Transfer distortion is honest and containable** — the single-instrument reduction is a labeled derivative, not a corruption of the source family
5. **Low implementation difficulty** is confirmed after memo review; the engineering choices are well-defined
6. **Gap fade logic is behaviorally plausible** and supported by broader practitioner and academic evidence independent of the single cited paper

The family **does not automatically prove** it has edge. The Dev-A test will determine that. But the memo gate is specifically asking whether the idea is credible enough to warrant implementation — and it is.

**Explicit conditions on advancement:**
- The strategy spec must explicitly label this as a single-instrument MES derivative of a cross-sectional source
- The spec must define the gap threshold clearly (not left as a "tune later" variable)
- The spec must define entry timing (first RTH bar vs. N-minute delay)
- The spec must define exit logic (EOD flatten only, or intra-session stop/target)
- ORB must be excluded from the same test windows if possible to prevent cross-contamination in interpretation

---

## 13. Required Next Step

Create a formal **strategy spec** for `overnight_intraday_reversal_v1` that covers:

1. Signal definition — exact overnight return calculation (prior RTH close to RTH open of the current session)
2. Direction rule — short the gap if gap is positive (fade upward overnight move); long the gap if gap is negative (fade downward overnight move)
3. Entry timing — first bar of RTH session, or delayed entry after a defined window
4. Entry threshold — minimum absolute overnight gap size in points to trigger a trade
5. Exit logic — hard stop-loss in points, RTH EOD flatten
6. Single-instrument MES scope — explicitly noted as a derivative, not a faithful cross-sectional port
7. ORB isolation — note whether test windows overlap with ORB and how to attribute results

The spec gates Dev-A implementation. This memo does not authorize coding.

---

## 14. Final Gate Status

| Field | Value |
|---|---|
| **Decision** | ADVANCE TO FORMAL SPEC |
| **Implementation approval** | NO — spec first |
| **Formal spec approval** | NOT YET — required next |
| **Dev-A authorization** | NO — pending spec approval |
| **Follow-up required** | Formal strategy spec for `overnight_intraday_reversal_v1` |
| **Reason** | Credible high-quality source, defensible single-instrument transfer, no engine blockers, genuinely distinct from ORB family if implemented cleanly |
| **ORB contamination risk** | LOW if spec defines signal, threshold, and entry timing tightly |
| **Source distortion risk** | MEDIUM — cross-sectional to single-instrument; must be labeled explicitly in spec and experiment log |
