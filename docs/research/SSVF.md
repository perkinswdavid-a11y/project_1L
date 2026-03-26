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

### 3.3 Current ORB benchmark parent

Current ORB benchmark parent:

- ORB-v6A

Reason:

- ORB-v6A is the first ORB child in the current Project 1L lineage to beat the prior parent on both Dev-A and Dev-B and survive promotion review.
- ORB-v2 remains the superseded prior ORB benchmark and an important historical comparison anchor.
- ORB remains a live strategy family, but it is no longer treated as the entire project.

### 3.4 Current family status

The ORB family has already consumed significant historical exposure on MES.

Therefore:

- later ORB work must remain honest about spent data status
- ORB child branching should now be more selective and more diagnostic-driven
- repeated local child branching is not automatically good research allocation
- ORB is one strategy family inside Project 1L, not the whole project

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

- `scripts/replay_backtest_v4b.py`

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

## 15. Historical V4 Testing Plan (Archived Example)

This section is retained as historical research context only.
It is not the current live Project 1L research anchor.
The current benchmark parent and current research allocation rules are defined elsewhere in this framework.

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

### Evidence Memo
- Target pattern frequency:
- Relative performance of targeted pattern:
- Already covered by existing rule/module?:
- Sample size adequate?:
- Expected effect if branch works:
- Main risk of false story:

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

### Diagnostic Follow-Up
- Mechanism cluster tested:
- Whether the targeted pattern actually appeared:
- Whether the branch removed weak trades or merely delayed/shifted fills:
- Whether this mechanism cluster should now be paused:
- Whether a parent postmortem is required before more local branches:
- Whether research allocation should shift to another family:

---

## 18. Enforcement Rule

If a branch result creates temptation to rewrite the rules after viewing the result, that is precisely when SSVF applies most strongly.

The process is designed to protect Project 1L from false confidence.

If the framework feels restrictive, that usually means it is doing its job.

---

## 19. Research Allocation Rules

Project 1L distinguishes between:

- correct branch discipline
- correct research allocation

A team may run branches honestly and still allocate effort poorly by spending too many cycles in a low-yield mechanism cluster.

This distinction is mandatory.

### 19.1 Branch discipline is necessary but not sufficient

It is not enough to say:

- the branch was thin
- the branch was tested honestly
- the branch was rejected properly

That is good process, but it does not automatically mean the next nearby branch is a good use of research time.

Project 1L must evaluate both:

- whether a branch was tested correctly
- whether the next branch is justified by evidence rather than intuition alone

### 19.2 Do not choose child branches from story alone

A plausible story is not enough to justify a new child branch.

Before coding a new child branch, Project 1L should ask:

- how often does the targeted pattern actually occur in the parent trade set
- are those trades materially worse than the rest
- is that pattern already mostly covered by an existing filter
- is the sample size large enough to matter
- would the proposed change truly remove weak trades, or would it mostly delay or shift fills

If those questions cannot be answered, the next step should usually be diagnostics, not coding.

### 19.3 Mandatory pre-code evidence memo

Before launching a new child branch off a mature parent, record a short evidence memo.

The memo must answer:

- target pattern frequency
- target pattern relative performance
- overlap with existing filters or protections
- sample size adequacy
- expected effect: remove bad trades vs delay entries vs reduce activity

If the memo cannot be completed honestly, the branch should normally not be coded yet.

### 19.4 Mechanism-cluster budget

After three failed thin children in the same mechanism cluster, that cluster should normally be paused.

A paused cluster may only be resumed if diagnostics reveal a specific, untested failure mode.

Examples of mechanism clusters:

- breakout-bar geometry filters
- anti-chase gates
- freshness cutoffs
- immediate failed-breakout exits
- context filters
- post-entry protection rules

This rule exists to prevent local over-mining of one idea neighborhood.

### 19.5 Mandatory parent postmortem before continued local branching

When a benchmark parent survives promotion but several nearby child branches fail, Project 1L should run a parent postmortem before launching more local children.

The postmortem should include, when available:

- signal time after OR completion
- signal bar close-location
- signal bar body fraction
- extension from trigger
- first-bar follow-through after entry
- MAE
- MFE
- exit reason
- hold time
- PnL grouped by meaningful bins
- contribution of top winners versus broad trade distribution

The goal is to select the next branch from observed leak points, not from general intuition.

---

## 20. Parent-Family Discovery Rules

### 20.1 A strategy family is not the project

Project 1L must not treat one strategy family as the entire project.

A benchmark ORB strategy may become one valuable sleeve.
It is not automatically the final system.

### 20.2 Parallel parent-family discovery is allowed

When one family becomes locally exhausted, Project 1L should open disciplined discovery in other parent strategy families rather than endlessly forcing more nearby child branches.

Examples of separate parent families may include:

- failed opening-range breakout reversal
- pullback continuation after initial breakout
- opening drive exhaustion / mean reversion
- range re-expansion after initial balance
- intraday trend continuation outside pure OR logic

These are examples of distinct families, not instructions to test all of them at once.

### 20.3 New families must still follow SSVF

Opening a new parent family does not relax discipline.

Each new family still requires:

- written hypothesis
- fixed parent definition
- predeclared gates
- honest Dev-A and Dev-B handling
- honest data exposure tracking

### 20.4 Discovery breadth is part of robustness

A serious intraday research program should usually maintain some controlled breadth.

This does not mean random idea sprawl.
It means not allowing one family to consume all research effort after local evidence has weakened.

---

## 21. Portfolio Sleeve Principle

Project 1L should assume that robust intraday performance may eventually come from a small group of distinct, validated strategy sleeves rather than one holy-grail setup.

This means:

- one family does not have to do everything
- a family may earn retention even if it is not the full system
- final system quality may come from combining distinct, independently validated edges later

A sleeve must still stand on its own before any combination work begins.

Combination is not a rescue device.

---

## 22. Current Process Guidance

### 22.1 Current ORB benchmark status

Current ORB benchmark parent:

- ORB-v6A

ORB remains active and important.
It is not abandoned.

### 22.2 Current ORB research guidance

Further ORB child branching should not proceed by default from intuition alone.

Before additional ORB child branches are launched, Project 1L should normally require either:

- a completed pre-code evidence memo, or
- a benchmark-parent postmortem showing a specific leak point worth testing

### 22.3 Current research allocation priority

Current priority should be:

- keep ORB-v14A as the active benchmark parent (promoted from v6A)
- perform a formal ORB-v14A postmortem
- open at least two non-ORB parent-family discovery tracks
- use evidence to decide which family deserves the next heavy research allocation

### 22.4 High rejection rate is normal

A high rejection rate in systematic strategy research is normal.

Months-long development timelines are normal.

What is not acceptable is allowing repeated rejections to produce little new information.

The goal is not to avoid rejection.
The goal is to make each rejection informative.