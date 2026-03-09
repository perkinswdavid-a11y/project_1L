# SSVF
## Systematic Strategy Validation Framework

---

## 1. Purpose

The Systematic Strategy Validation Framework (SSVF) governs how Project 1L designs, tests, promotes, rejects, and archives systematic intraday futures strategies.

Its purpose is to prevent:

- accidental overfitting
- moving goalposts after seeing results
- confusing development work with independent confirmation
- promoting weak strategies because they looked good in one viewed sample
- polluting research with undisciplined parameter accumulation

SSVF exists so that strategy development remains:

- hypothesis-first
- modular
- auditable
- reproducible
- technically honest

---

## 2. Core Principles

### 2.1 Hypothesis before testing
Every new strategy branch or module must begin with a written hypothesis before any run is executed.

A valid hypothesis must state:

- what changed
- why it should help
- what weakness of the parent it is intended to address
- what mechanism is expected to improve

No testing begins without this.

### 2.2 Predeclared promotion gates
Before a run is made, the pass/fail gate must be written down.

This includes:

- what counts as success
- what counts as failure
- what metric deterioration is acceptable
- what activity collapse would invalidate the branch

No branch earns promotion based on post hoc interpretation.

### 2.3 One coherent change at a time
A research branch should usually introduce one coherent module or one tightly related rule set at a time.

Examples of coherent changes:

- adding a VWAP context filter
- adding a breakout participation filter
- changing execution from touch-based to close-confirmed
- adding a structural risk cap

Examples of incoherent changes:

- adding VWAP, RSI, moving average, and volume filters together
- changing entries, exits, and time stops all at once
- changing multiple independent mechanisms in a single branch

### 2.4 Modular richness is allowed
Professional strategies may ultimately contain multiple parameters and modules.

That is acceptable.

What is not acceptable is selecting those modules by repeatedly keeping whatever improved the same viewed sample.

Project 1L allows a richer strategy framework, but only under strict validation discipline.

### 2.5 The benchmark parent must stay fixed
Every new branch must identify a parent benchmark.

The branch is judged relative to that parent, not in isolation.

### 2.6 Cross-instrument testing is confirmation, not rescue
Cross-instrument testing, such as MNQ after MES, is useful only after a branch is sufficiently frozen.

It may confirm a frozen rule set.

It may not be used to rescue a weak or unstable MES branch.

### 2.7 Data exposure status must be tracked honestly
A historical window that has influenced design decisions is no longer a pristine holdout.

It may still be used for research, comparison, and postmortem analysis.

It may not be presented as untouched confirmation.

---

## 3. Project 1L Research Context

### 3.1 Design instrument
Primary design instrument:

- MES

### 3.2 Later confirmation instrument
Later frozen-rule confirmation instrument:

- MNQ

### 3.3 Current parent benchmark
Current ORB parent benchmark:

- ORB-v2

Reason:

- ORB-v2 showed credible performance on the original development and validation windows
- ORB-v2 did not fully survive the original holdout, but it remained the most credible ORB family benchmark so far
- ORB-v3 branches did not improve robustness

### 3.4 Current family status
The ORB family has already consumed significant historical exposure on MES.

Therefore, SSVF now treats later windows with honest downgraded status.

---

## 4. Data Window Definitions

### 4.1 Discovery window: Dev-A
Used for first-pass idea discovery and module screening.

Current Dev-A window:

- 2023-02-26 to 2023-08-31

Purpose:

- identify whether a new module has any credible signal improvement versus the benchmark parent

### 4.2 Internal confirm window: Dev-B
Used for internal confirmation of ideas that looked promising in Dev-A.

Current Dev-B window:

- 2023-09-01 to 2024-02-29

Purpose:

- determine whether the Dev-A improvement survives on a separate internal slice

### 4.3 Secondary OOS windows
These are later windows already exposed through prior ORB research.

They remain useful, but are no longer pristine.

Current secondary OOS windows:

- 2024-03-01 to 2025-02-28
- 2025-03-01 to 2026-02-22

Purpose:

- secondary robustness check
- reference comparison
- degradation analysis

Not allowed to be described as untouched holdout proof for newly designed ORB branches.

### 4.4 Frozen cross-instrument confirmation
Only used after MES rules are frozen enough.

Current candidate:

- MNQ

Purpose:

- determine whether a frozen rule set retains behavior on a related but different instrument

---

## 5. Meaning of “Spent Data”

“Spent data” does not mean unusable data.

It means the window has already influenced design or selection decisions and therefore can no longer serve as pristine independent evidence.

Spent windows may still be used for:

- development
- comparison
- debugging
- postmortem analysis
- secondary OOS review

Spent windows may not be used as if they are untouched proof.

This distinction is mandatory.

---

## 6. Branch Workflow

Every branch must follow this order.

### 6.1 Define parent
State the exact parent branch.

Example:

- Parent = ORB-v2 benchmark

### 6.2 Define branch identity
State:

- branch label
- strategy family
- exact rule/module change
- unchanged components

### 6.3 Write hypothesis
State:

- what the new change should improve
- why it should improve it
- what known weakness it is meant to address

### 6.4 Write predeclared gates
State in writing:

- Discovery gate
- Internal confirm gate
- Secondary OOS gate, if applicable
- Frozen cross-instrument gate, if applicable

### 6.5 Run discovery window
Run Dev-A first.

### 6.6 Decide promotion to internal confirm
If Dev-A fails the gate, stop.

If Dev-A passes, continue to Dev-B.

### 6.7 Run internal confirm window
Run Dev-B unchanged.

No retuning between Dev-A and Dev-B.

### 6.8 Decide provisional retention
If the branch survives Dev-B, it earns provisional retention as a candidate module.

If it fails Dev-B, reject it.

### 6.9 Only then consider:
- secondary OOS review
- module combinations
- frozen MNQ confirmation

---

## 7. Required Branch Documentation

Before a run begins, every branch must have the following recorded.

### 7.1 Branch Identity
- Strategy family
- Branch label
- Parent branch
- Date started

### 7.2 Scope of Change
- Exact parameters/modules changed
- Exact components unchanged

### 7.3 Hypothesis
- Primary hypothesis
- Why this should help
- What weakness of the parent it is intended to address

### 7.4 Mechanism
- What market behavior is being captured or avoided
- Why that mechanism is plausible

### 7.5 Test Windows
- Discovery window
- Internal confirm window
- Secondary OOS window, if used
- Cross-instrument window, if used

### 7.6 Promotion Gates
- Discovery gate
- Internal confirm gate
- Further gate, if applicable

### 7.7 Failure Conditions
- what invalidates the branch immediately
- what counts as trade starvation
- what deterioration is unacceptable

---

## 8. Standard Evaluation Metrics

The following metrics must be reviewed for every meaningful run:

- Net PnL
- Profit factor
- Max drawdown absolute
- Max drawdown percent
- Closed trade count
- Win rate percent
- Daily Sharpe approximate

These metrics must be interpreted together.

No single metric is sufficient by itself.

---

## 9. Discovery Gate Rules (Dev-A)

A branch may be promoted from Dev-A to Dev-B only if it meets all of the following:

### 9.1 Relative merit versus parent
It must show at least one of these relative to the parent benchmark on the same Dev-A slice:

- a meaningful profit factor improvement, or
- a meaningful drawdown reduction without destroying economics

### 9.2 Activity must remain meaningful
A branch may not survive Dev-A if trade count collapses so severely that the apparent improvement is likely just inactivity.

Default standard:

- closed trade count should remain at least 60 percent of parent

Exception:

- lower trade count may be tolerated if drawdown reduction is substantial and economics remain clearly healthy

### 9.3 No obviously broken economics
A branch should normally be rejected immediately if Dev-A shows:

- negative net PnL
- profit factor below 1.0
- severe trade starvation
- obviously degraded performance versus parent with no compensating improvement

---

## 10. Internal Confirm Gate Rules (Dev-B)

A branch may be provisionally retained only if Dev-B remains broadly healthy.

Default Dev-B standards:

- net PnL positive
- profit factor at least 1.05
- drawdown not materially worse than parent
- meaningful trade count retained
- no evidence of collapse relative to Dev-A

If a branch passes Dev-A and fails Dev-B, it is rejected.

No rescue tuning is allowed before making that rejection call.

---

## 11. Combination Rules

Two modules may only be combined if both have already survived alone.

A module combination may be tested only if:

- each individual module survived the full internal process first
- the combination is justified by mechanism, not curiosity alone
- the combination is tested first on Dev-A
- the combination remains acceptable on Dev-B unchanged

If the combination helps Dev-A and fails Dev-B, reject the combination.

Do not keep a combination just because it looked best on the discovery slice.

---

## 12. Cross-Instrument Rules

MNQ or any later instrument may only be used after a branch or combination is sufficiently frozen on MES.

Cross-instrument testing is not allowed to serve as:

- rescue evidence for a weak MES branch
- substitute for internal discipline
- replacement for predeclared MES gates

Cross-instrument use is allowed for:

- frozen-rule confirmation
- portability assessment
- robustness assessment after MES selection is complete

---

## 13. File and Config Management Rules

### 13.1 Keep all configs
Old configs must not be deleted.

They form part of the research audit trail.

### 13.2 Archive, do not clutter
Configs no longer in active use should be moved to an archive structure rather than deleted.

Recommended structure:

- `configs/active/`
- `configs/archive/`

### 13.3 One active engine file
Maintain one active backtest engine file:

- `scripts/replay_backtest.py`

Keep archival backups separately, but do not maintain multiple live versions in active use.

### 13.4 Branch naming
Code strategy names should remain stable where appropriate.

Research branch labels may vary independently.

Example:

- code strategy name: `opening_range_breakout_v4`
- research branch label: `ORB-v4A`

---

## 14. Logging Rules

Every run should include:

- research hypothesis
- research change description
- parent experiment reference if applicable
- decision
- recommendation

Completed runs must be logged honestly.

Do not soften rejections.
Do not upgrade weak evidence into pass language.

---

## 15. Current Official V4 Testing Plan

### 15.1 Benchmark parent
- ORB-v2

### 15.2 Benchmark split windows
#### Dev-A
- 2023-02-26 to 2023-08-31

#### Dev-B
- 2023-09-01 to 2024-02-29

### 15.3 First V4 module candidate
- VWAP alignment filter only

This first V4 candidate will be judged against the ORB-v2 parent on Dev-A and Dev-B.

No additional module combination is allowed until the VWAP module is tested on its own.

---

## 16. Pre-Run Branch Record Template

Use this block before each new branch.

### Branch Identity
- Strategy family:
- Branch label:
- Parent:
- Date:

### Scope of Change
- Changed:
- Unchanged:

### Hypothesis
- Primary hypothesis:
- Why it should help:
- Parent weakness targeted:

### Mechanism
- Expected market mechanism:
- Why plausible:

### Windows
- Dev-A:
- Dev-B:
- Secondary OOS:
- Cross-instrument:

### Discovery Gate
- Required improvement:
- Minimum acceptable trade count:
- Minimum acceptable PF:
- Maximum acceptable drawdown behavior:

### Internal Confirm Gate
- Net PnL must be:
- PF must be at least:
- Drawdown must remain:
- Trade count must remain:

### Failure Conditions
- Immediate reject if:
- Reject even if one metric improves if:
- Trade starvation definition:

### Pre-Run Approval
- Approved to run:
- Reason:
- Main risk:

---

## 17. Post-Run Record Template

Use this block after each meaningful run.

### Result Summary
- Net PnL:
- Profit factor:
- Max drawdown %:
- Closed trades:
- Win rate %:
- Daily Sharpe approx:

### Decision
- Promote / Reject / Archive / Baseline measurement

### Recommendation
- Next action:
- Whether to continue:
- Whether to archive:
- Whether to combine later:

---

## 18. Enforcement Rule

If a branch result creates temptation to rewrite the rules after viewing the result, that is precisely when SSVF applies most strongly.

The process is designed to protect Project 1L from false confidence.

If the framework feels restrictive, that usually means it is doing its job.