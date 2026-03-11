> Historical status note:
> This document is an archived predeclared branch record for ORB-v4A against ORB-v2.
> It is retained as part of the Project 1L audit trail and as an example of SSVF branch documentation.
> It is not the current benchmark parent, not the current ORB research anchor, and not the current Project 1L testing plan.

Predeclared V4A branch record

Use this in SSVF before the run:

Branch Identity

Strategy family: ORB

Branch label: ORB-v4A

Parent: ORB-v2

Date: 2026-03-08

Scope of Change

Changed: add VWAP alignment filter at signal time

Unchanged: OR duration, buffers, long-only direction, OR-width filter, cost-protect, ATR trail, time stop, position size, costs

Hypothesis

Primary hypothesis: Requiring the long breakout signal bar to close above RTH VWAP may remove lower-quality breakouts and improve robustness relative to ORB-v2.

Why it should help: Breakouts occurring above session VWAP are more likely to reflect acceptance above morning value rather than transient pokes.

Parent weakness targeted: ORB-v2 likely admits some breakouts occurring in weaker contextual structure.

Mechanism

Expected market mechanism: A breakout aligned above RTH VWAP should have better continuation odds than one occurring below or into VWAP resistance.

Why plausible: VWAP is a widely used intraday value reference and helps distinguish accepted directional movement from noisier structure.

Windows

Dev-A: 2023-02-26 to 2023-08-31

Dev-B: 2023-09-01 to 2024-02-29

Secondary OOS: later only if Dev-A and Dev-B pass

Cross-instrument: later only if MES branch is frozen enough

Discovery Gate

Improve PF above 1.307, or materially reduce DD below 0.420% without broken economics

Closed trades should remain at least about 38

No negative net PnL

No PF below 1.00

Internal Confirm Gate

Net PnL positive

PF at least 1.05

DD not materially worse than 0.740%

Trade count remains meaningful

Failure Conditions

Immediate reject if Dev-A is net negative

Immediate reject if Dev-A PF < 1.00

Reject if trade count collapses below meaningful level without exceptional DD benefit

Reject if Dev-B fails positivity/PF gate