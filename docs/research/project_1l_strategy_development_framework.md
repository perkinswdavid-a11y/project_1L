# Project 1L Strategy Development Framework
**Version:** 1.0 — 2026-03-10
**Scope:** MES and MNQ futures research pipeline

This document is the operational framework for all Project 1L strategy research.
It governs how ideas enter, are evaluated, implemented, tested, and either promoted or closed out.

---

## Pipeline Overview

```
IDEA → Gate A (intake screen) → Hypothesis → Memo → Gate B (memo approval) → Spec → Implementation → Dev-A → Dev-B → Promote or Reject
```

Professional practitioner playbooks, discretionary desk knowledge, and empirical observation are valid idea sources and do not require academic citation to pass Gate A.
Academic papers strengthen Gate A arguments but do not substitute for mechanism quality.

---

## 1. Gate A — Strategy Intake Screen

Gate A determines whether a raw idea represents a legitimate strategy family before any coding begins.

### Gate A Criteria

Each idea is evaluated on five dimensions:

| Dimension | Question | Pass Condition |
|---|---|---|
| **Market mechanism** | Is there a structural reason this should work? | A specific named mechanism: liquidity, flow, information, structural constraint |
| **Trigger condition** | Can the signal be defined in concrete observable terms? | Yes — with specific bars, prices, times, or ratios |
| **Execution path** | Can the trade be entered and exited without exotic infrastructure? | Yes — bar-based replay on currently supported infrastructure, standard order types |
| **Futures relevance** | Is this native to futures or has a credible transfer path? | Instrument-specific argument, not just "works in stocks" |
| **Data availability** | Is the required data already in Project 1L catalog? | Available OHLCV data at approved research granularity (1m/5m/15m as applicable); primary catalog is MES/MNQ 1m bars |

### Gate A Classification

| Outcome | Meaning |
|---|---|
| **Proceed to memo** | All five dimensions pass. Write the hypothesis and memo. |
| **Park** | Mechanism is plausible but data, infrastructure, or source quality is insufficient now. Log in source library. |
| **Discard** | No identifiable mechanism, too vague, or requires infrastructure that does not exist. |

### Gate A Admission Note

**Professional practitioner families do not require academic proof of profitability to pass Gate A.**
ORB, VWAP reversion, time-of-day effects, gap fades, spread reversion, and similar practitioner families pass on mechanism argument alone, provided the execution path and data are clear.

Academic papers strengthen Gate A but are not required. What is required is a specific, named mechanism that explains *why* the trade should work.

### What Fails Gate A Unconditionally

- Vague descriptions: "mean reversion," "momentum," "breakout" with no specific trigger
- ML-only frameworks with no interpretable trade logic
- Ideas that require Level 2/MBP data, colocation, or event-driven tick execution
- Generic equity portfolio selection with no futures transfer argument
- Any idea that cannot produce a concrete trigger and exit without further research

---

## 2. Hypothesis Formation

Before the memo is written, the raw idea must be converted into a formal trading hypothesis.

### Hypothesis Structure

```
When [observable condition in terms of price/volume/time/session structure],
in [instrument and session context],
[directional position] in [leg(s)],
expecting [specific outcome] within [holding period],
because [named mechanism].
```

### Required Elements

| Element | Description |
|---|---|
| **Dependent variable** | The specific observed outcome (e.g., price reverts, leg catches up, gap fills) |
| **Independent variables** | The observable trigger conditions (e.g., gap > X points at 08:30 CT bar close) |
| **Mechanism** | The named structural reason the effect should exist |
| **Falsification** | Under what conditions would results prove the hypothesis false, not merely unlucky |

### Falsification Conditions (defined before Dev-A runs)

A hypothesis must state, before any backtest:
- Minimum profit factor to consider "raw life" (typically > 1.10 for parents, > 1.20 for children)
- Minimum trade count to consider the result signal-bearing (framework default: **30 closed trades in Dev-A minimum; 20 for spread or paired families**)
- Win rate / payoff ratio combination that constitutes failure
- Whether a poor Dev-A result rejects the hypothesis or only the parent implementation

If the Dev-A closed trade count falls below the framework minimum, the run is considered statistically inconclusive, not a pass or a fail. The trigger threshold or session window must be revisited before a meaningful evaluation can be made.

---

## 3. Strategy Memo Template

The memo is written before any spec or code work begins. It gates the decision to spend implementation effort.

### Memo Structure

```markdown
# [family_name] — Strategy Memo

**Date:** YYYY-MM-DD
**Author:** [researcher]
**Source:** [primary source citation or "practitioner playbook"]
**Gate A Outcome:** proceed-to-memo

---

## 1. Core Concept
One paragraph. What is this strategy and what does it do?

## 2. Market Mechanism
Why should this work structurally? Name the specific driver:
- liquidity mechanism
- structural flow / scheduled rebalancing
- information asymmetry
- crowd behavioral bias
- physical or regulatory constraint
- session microstructure

## 3. Instrument Scope
- Primary: MES or MNQ (specify)
- Context instrument if paired: (specify or none)
- Session: full RTH, specified window, or overnight

## 4. Trigger Definition (Thin Parent)
Exact observable conditions that cause trade entry. No vagueness.
- Signal anchor (time, price level, session event)
- Threshold (specific numeric or computed value)
- Direction logic (long, short, or conditional)

## 5. Exit Definition (Thin Parent)
- Primary exit (time, level, or event)
- Hard stop (specific rule)
- No trailing stops, no targets unless central to the hypothesis

## 6. Thin Parent Rules
What is explicitly excluded to keep the parent thin:
- No additional filters unless they are mandatory for the hypothesis
- No regime detection, no signal stacking
- No cross-instrument validation unless the hypothesis requires it
- Maximum one or two parameters beyond the basic trigger

## 7. Falsification Tests
Before running Dev-A, state:
- Minimum PF threshold for "raw life"
- Minimum trade count
- Payoff ratio floor
- Specific result that would constitute rejection (not just weakness)

## 8. Known Risks and Failure Modes
What would cause this to fail structurally:
- Regime dependency
- Publication / practitioner decay
- Cost drag at realistic slippage
- Trade count starvation

## 9. Infrastructure Requirements
- Any new engine features required? (YES/NO — specify)
- New data required beyond 1m MES/MNQ bars? (YES/NO — specify)
- Estimated implementation difficulty: low / medium / high
```

---

## 4. Implementation Specification Template

The spec is written after memo approval and before any code. It must be engineering-complete.

### Spec Structure

```markdown
# [family_name]_v1 — Implementation Specification

**Memo reference:** [link or filename]
**Date:** YYYY-MM-DD

---

## 1. Data Specification
- Bar type: OHLCV at approved granularity (1m / 5m / 15m — specify)
- Timestamp convention: bar_close CT (or specify)
- Session window: 08:30–15:00 CT (or specify for the instrument)
- Session timezone: America/Chicago (or specify)
- Instrument: specify (e.g., MES.v.0 dominant-by-day, MNQ.v.0, etc.)
- Context instrument (if paired): specify or none

## 2. Signal Computation
Step-by-step formula for the signal:
- Define all computed values (anchors, rolling windows, ratios)
- State what bar closes trigger evaluation
- State what data lookback is required
- State what state must persist across bars / across days

## 3. Entry Logic
- Entry trigger: exact condition (e.g., close of the X bar crosses Y)
- Entry fill model: next-bar open (standard Project 1L model)
- Slippage assumption: N ticks per side
- Commission: $1.25 per side per contract
- Position size: 1 contract per leg

## 4. Exit Logic
- Primary exit trigger: exact condition
- Time stop trigger: exact bar or wall-clock time
- Hard stop trigger: N points / ticks below entry
- Exit fill model: next-bar open (standard)
- One trade per day: YES/NO

## 5. Cost Model
- Slippage: N ticks × tick_size × contracts per side
- Commission: $1.25 × contracts per side
- Total round-trip cost per trade: (computed)

## 6. Risk Controls
- Max loss per trade (hard stop)
- Max trades per session
- Daily flatten: YES (standard)
- Any pair-level stop (if spread): combined open PnL threshold

## 7. Contract Roll Handling
- Instrument mode: dominant_by_day
- Roll dates: handled automatically by engine roll logic
- No strategy-side roll handling required

## 8. Required Outputs
- closed_trades.csv
- daily_equity.csv
- executions.csv
- summary.json
- Auto-log to strategy_experiment_log.md via research_logger

## 9. Edge Cases
- What happens if the session open bar is missing
- What happens if the signal fires near the time stop window
- What happens if both legs miss fill (paired strategies)
```

---

## 5. Thin-Parent Design Rules
The thin parent must be the simplest possible expression of the hypothesis. It isolates the mechanism to see if raw edge exists before any rescue-optimization can obscure it.

- Minimum mechanism-complete structure must be preserved. Do NOT remove elements that define the mechanism (e.g., threshold *is* the mechanism for extreme mean-reversion).
- One mechanism only. Do not mix trend following and mean reversion in the parent.
- Minimum possible parameters. Use static time-of-day anchors if possible.
- No filters (no VIX filter, no SMA filter, no day-of-week filter) unless the filter is explicitly the independent variable in the hypothesis.
- Fixed ratio chosen ex ante for the parent. No dynamic re-hedging or ratio optimization inside the parent. A pre-defined dollar- or beta-normalized ratio is acceptable.
- Maximum one entry per day (unless structural to the mechanism, like grid trading, which is rare for 1L).
- Defined time exit (e.g., fixed session time).
- Hard stop (e.g., $500 max loss) to prevent outlier days dragging the metric, but no trailing stops unless trailing stop behavior is the hypothesis being tested.

### Why Thin Parents Work

A thin parent produces a clear answer to one question: **does this mechanism show raw life in this instrument?**

If the parent fails, the parent is rejected. The family is not automatically invalidated unless the failure clearly attacks the mechanism itself — a failure caused by bad mapping to the instrument, cost drag, or regime dependence does not prove the mechanism is fake. If the parent passes Dev-A and Dev-B, the mechanism is confirmed and children can add reasonable sophistication.

A fat parent (with filters, regime detection, multiple conditions) cannot answer this question — a positive result might be from the filters, not the mechanism. A negative result might be a bad filter choice, not a dead mechanism.

### What Counts as Adding Thickness

The following additions make a parent fat and should be deferred to child branches:
- Volatility filters (ATR thresholds, VIX overlays)
- Volume filters
- Session time restrictors beyond the primary exit
- VWAP conditions
- Multi-bar signal confirmation
- Signal stacking (two independent criteria must both be true)
- Dynamic sizing or position scaling

---

## 6. Backtest Evaluation Framework

### Three-Layer Evaluation

#### Layer 1 — Signal Behavior
Before reading PnL, evaluate the signal itself:
- How many days triggered?
- What percentage of available sessions produced a trade?
- Is the trigger firing in conditions that match the hypothesis?
- Is there evidence of direction bias (long vs flat vs wrong-direction)?

A strategy that triggers rarely may have a statistical noise problem, not an alpha problem.

#### Layer 2 — Trade Simulation With Realistic Costs
Read PnL only after confirming signal behavior is sensible:
- Net PnL, Profit Factor
- Win rate and payoff ratio (both required — neither alone is sufficient)
- Max drawdown absolute and percent
- Avg winner vs avg loser
- Cost drag: what does the strategy look like at zero slippage/commission?

**Raw Life Standard (thin parent):**
- Profit Factor > 1.10 in Dev-A = weak raw life (warrants Dev-B)
- Profit Factor > 1.25 in Dev-A = meaningful raw life
- Profit Factor < 1.00 in Dev-A = dead (no rescue optimization)

**Minimum Trade Count Floor (framework default):**
- Standard families: **30 closed trades minimum in Dev-A**
- Spread / paired families: **20 closed trades minimum in Dev-A**
- Below floor: result is **inconclusive** — not a pass or fail. Revisit trigger or session window before evaluating PnL.

#### Layer 3 — Robustness and OOS Validation
Only tested after Layer 2 passes:
- Dev-B (out-of-sample confirmation window)
- Trade count consistency between Dev-A and Dev-B
- Win rate stability (collapse > 10pp = suspect)
- Drawdown path comparison

### Distinguishing Strategy Failure from Implementation Failure

| Symptom | Likely Cause | Action |
|---|---|---|
| PF < 1.00, win rate near 50%, inverted payoff | Strategy mechanism not working at this sizing/timing | Reject parent |
| PF < 1.00, zero trades or near-zero trades | Threshold too tight, wrong time window | Revisit spec before rejecting |
| PF > 1.0 in Dev-A, collapses in Dev-B | Overfitting or regime dependency | Reject and log |
| Win rate drops 10pp+ in Dev-B | Train/test population shift | Reject and log |
| PF > 1.25 in Dev-A, holds in Dev-B | Mechanism confirmed | Promote to children |
| Fills at wrong time, execution count unexpected | Engine bug or config error | Fix implementation, re-run |

**Never optimize parameters on a failed parent to rescue it.**

---

## 7. Controlled Iteration Framework

After Dev-A and Dev-B, a passing parent can spawn children. The following rules govern iteration.

### Iteration Control Rules

1. **One variable per branch.** Each child changes exactly one thing from the parent.
2. **Document before running.** Every branch must have a hypothesis for why the change should help.
3. **Freeze Dev-B before branching.** Once Dev-A passes, Dev-B is frozen. Children must be evaluated on Dev-B as a confirmation window, not a training window.
4. **No parameter sweeps.** Picking the best value from a range constitutes optimization. A specific value must be chosen from first principles or a single midpoint test.
5. **Cumulative data exposure tracking.** Log which windows have been used for design vs confirmation. A window used more than twice is no longer pristine.
6. **Promotion requires both Dev-A and Dev-B.** A child that beats Dev-A but fails Dev-B is rejected. Do not promote on Dev-A alone.
7. **Close dead branches explicitly.** Every failed branch must be logged in the experiment log with a reason code. No branch is abandoned silently.

### Allowed Iteration Types (after parent confirmation)

| Change Type | Allowed After | Notes |
|---|---|---|
| Tighter threshold | Parent Dev-B pass | Single specific tighter value |
| Different exit time | Parent Dev-B pass | Single alternative time |
| One additional filter | Parent Dev-B pass | Must have a hypothesis for why |
| Different session window | Parent Dev-B pass | Not a parameter sweep |
| Paired leg ratio change | Parent Dev-B pass (spread only) | Single alternative ratio |

### Prohibited After Dev-B

- Changing the core signal definition
- Adding multiple filters at once
- Using Dev-B results to select parameters for the next child
- Retroactively redefining the falsification conditions

---

## 8. Research Audit Trail

Every strategy must produce a complete audit trail from idea to decision.

| Artifact | When Created | Location |
|---|---|---|
| Source library entry | At intake | `docs/research/source_library.md` |
| Strategy memo | Before spec | `docs/research/strategies/[name]_memo.md` |
| Strategy spec | Before implementation | `docs/research/strategies/[name]_spec.md` |
| Config file | Before run | `configs/active/[name]_dev_a.json` |
| Experiment log entry | After run (auto) | `docs/research/strategy_experiment_log.md` |
| Closeout note | At rejection | Appended to experiment log |

---

## 9. SSVF Gate Summary

| Gate | When | Question | Output |
|---|---|---|---|
| **Gate A** | Intake | Does this idea have a named mechanism and testable trigger? | proceed / park / discard |
| **Gate B** | Memo approval | Is the hypothesis precise enough to implement without ambiguity? | approved / revise |
| **Dev-A** | First in-sample | Does the parent show raw life? | promote / reject |
| **Dev-B** | OOS confirmation | Does the result hold out-of-sample? | promote / reject |
| **Promotion** | After Dev-B | Is this mechanism confirmed for child branching? | branch / maintain / close |
