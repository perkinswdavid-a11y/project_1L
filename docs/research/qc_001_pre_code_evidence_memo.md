# QC-001 Pre-Code Evidence Memo — spread_residual_cointegration

## 1. Purpose

Evaluate whether `spread_residual_cointegration` deserves:
- infrastructure support beyond current matched-timestamp context handling
- formal strategy spec creation
- Dev-A implementation inside Project 1L

This memo is a **go / park / reject** gate.
It is not implementation approval by itself.

---

## 2. Candidate Summary

- **family name:** `spread_residual_cointegration`
- **source type:** platform research tutorial / secondary implementation source
- **current source quality:** medium
- **current status:** active pre-code memo candidate

Core idea:
- identify two closely related instruments
- estimate a stable spread / residual relationship
- wait for abnormal residual displacement
- trade the residual back toward equilibrium through a **true two-leg position**

This is a **spread family**, not a one-leg context-filter strategy.

---

## 3. Why This Family Is Being Considered

This family survives initial screening because it is:
- materially different from the exhausted ORB neighborhood
- based on spread-residual mean reversion rather than breakout geometry
- structurally compatible with Project 1L’s growing multi-instrument research direction
- potentially reusable as a broader research lane if true paired execution is supported

This family also aligns with a newly confirmed Project 1L willingness to eventually support:

- true two-leg positions
- combined spread PnL tracking
- paired exit logic
- multi-leg research infrastructure

That willingness keeps QC-001 alive.
Without it, QC-001 would be non-viable or would risk mutating into a fake one-leg proxy.

---

## 4. Core Market Logic

The market logic is:

1. two instruments with a strong economic or structural relationship can trade around a relatively stable spread relationship
2. short-term dislocations can occur because of liquidity shocks, temporary imbalance, or differing order-flow pressure
3. if the relationship remains sufficiently stable, extreme residual deviations may mean-revert
4. a paired long/short position can isolate the spread move better than outright directional exposure

This is important:
the claim is **not** that one instrument is “weak” or “strong” in isolation.
The claim is that the **relationship itself** becomes temporarily mispriced.

---

## 5. Why It Might Exist

Possible reasons this edge could exist:

- short-lived execution imbalance between close substitutes
- differing liquidity pressure across related contracts
- temporary overreaction in one leg relative to the other
- slow re-linking of correlated instruments after displacement
- structural trader behavior that reprices the relationship after transient shocks

This logic is plausible enough to justify memo status.

---

## 6. Why It Is Not Automatically Approved

QC-001 should **not** move directly to implementation for several reasons:

### 6.1 It requires true two-leg execution
This family is only valid if Project 1L can eventually model:

- long leg + short leg simultaneously
- spread PnL
- leg-aware entry / exit handling
- paired risk logic

A one-leg MES trade using MNQ only as context would **not** be the same family.

### 6.2 Source quality is not strong enough for blind porting
The current source is useful as a conceptual seed, but not strong enough to copy directly into production research code without translation and tightening.

### 6.3 Relationship stability is the central risk
Pairs / spread logic can fail if:
- cointegration is unstable
- the relationship changes regime
- roll behavior distorts the spread
- apparent stationarity is weak or temporary
- execution costs dominate a small residual edge

### 6.4 Infrastructure cost is real
Compared with a normal one-instrument parent-family test, this candidate likely requires:
- multi-leg position representation
- spread-aware accounting
- more careful fills / slippage assumptions
- more complex reporting and diagnostics

So QC-001 is not a “thin cheap test.”
It is a strategy-family candidate with meaningful infra implications.

---

## 7. Project 1L Transfer Assessment

### 7.1 What transfers well
Project 1L already has:
- replay research discipline
- good documentation standards
- stronger diagnostics than before
- matched-timestamp context support that is directionally helpful

### 7.2 What does not yet exist cleanly
Project 1L does **not yet** have confirmed full support for:
- true paired position objects
- combined multi-leg PnL attribution
- spread-aware entry / exit lifecycle handling
- leg-weight / hedge-ratio-aware accounting

So current Project 1L is **adjacent** to QC-001 readiness, but not yet ready for honest implementation.

---

## 8. Required Infrastructure If Advanced

If QC-001 ever advances past memo approval, the likely minimum infrastructure scope includes:

1. paired trade representation
   - leg A instrument
   - leg B instrument
   - side for each leg
   - quantity / ratio for each leg

2. paired entry / exit handling
   - synchronized open and close logic
   - combined lifecycle tracking

3. spread PnL accounting
   - realized PnL by leg
   - combined spread PnL
   - cost attribution across both legs

4. spread diagnostics
   - residual at entry
   - residual at exit
   - max favorable / adverse spread excursion
   - holding time
   - exit reason

5. futures-specific controls
   - contract-roll handling
   - ratio / weighting policy
   - liquidity / session overlap checks

This is reusable infrastructure if built carefully.
That makes the work potentially defensible even if QC-001 later fails.

---

## 9. Likely Best Conditions

QC-001 would most likely perform best when:

- instruments are highly liquid
- relationship is economically sensible and persistent
- session overlap is strong
- dislocations are real but not regime-breaking
- spread noise is tradable after costs

---

## 10. Likely Failure Modes

Main failure risks:

- unstable residual relationship
- structural regime shift
- poor pair selection
- contract-roll distortion
- overly small edge after slippage / fees
- false mean-reversion assumptions
- implementation complexity creating research drag before alpha proof

These failure modes are serious enough that this family must be screened carefully before coding.

---

## 11. Research Value Even If Rejected

Even if QC-001 is later rejected as alpha, it could still justify useful reusable infrastructure work if we decide Project 1L should eventually support:

- true spread research
- paired futures ideas
- cross-instrument mean-reversion families
- future calendar-spread or substitute-spread testing

This must still be labeled honestly as **infrastructure value**, not alpha progress.

---

## 12. Recommendation

### Current recommendation: APPROVE FOR FURTHER RESEARCH, NOT IMPLEMENTATION

QC-001 should advance to the next stage only as:

- a formal pre-code research candidate
- a family requiring tighter evidence gathering
- a gating decision on whether paired-spread infrastructure is worth building soon

It should **not** yet advance to:
- formal strategy spec
- Dev-A implementation
- branch creation
- coding work

---

## 13. Required Next Step

Before implementation approval, perform a focused follow-up memo on:

**paired futures transfer design**

That memo should answer:
1. which futures relationships are actually candidates
2. whether substitute-spread logic or calendar-spread logic is the better first lane
3. whether hedge-ratio / weighting can be kept thin and honest
4. what minimum paired execution infrastructure would be required
5. whether the expected research value justifies the infrastructure cost now

---

## 14. Final Gate Status

- **Decision:** PARKED-APPROVED FOR FURTHER RESEARCH
- **Implementation approval:** NO
- **Formal spec approval:** NO
- **Follow-up memo required:** YES
- **Reason:** real family, credible market logic, but infrastructure-gated and not yet implementation-ready
