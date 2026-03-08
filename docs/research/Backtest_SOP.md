# Strategy Test SOP Template

## 1. Branch Identity
- Strategy family:
- Branch label:
- Parent branch:
- Date started:
- Author/operator:

## 2. Branch Summary
- What changed from parent:
- What stayed unchanged:

## 3. Hypothesis
- Primary hypothesis:
- Why this should help:
- What specific weakness of the parent this branch is trying to fix:

## 4. Market Mechanism
- What market behavior this branch is trying to capture or avoid:
- Why this is structurally plausible:

## 5. Test Windows
- Discovery window (Dev-A):
- Internal confirm window (Dev-B):
- Secondary OOS window:
- Cross-instrument check (later only):

## 6. Evaluation Metrics
- Net PnL
- Profit factor
- Max drawdown %
- Closed trade count
- Win rate %
- Daily Sharpe approx

## 7. Promotion Gate
### Discovery Gate (Dev-A)
- Required improvement vs parent:
- Minimum acceptable trade count:
- Minimum acceptable PF:
- Maximum acceptable drawdown behavior:

### Internal Confirm Gate (Dev-B)
- Net PnL must be:
- Profit factor must be at least:
- Drawdown must remain:
- Trade count must remain:

### Secondary OOS Gate
- Pass/fail standard:

### Cross-Instrument Gate (frozen rules only)
- Pass/fail standard:

## 8. Failure Conditions
- Reject immediately if:
- Reject even if one metric improves if:
- What would count as “trade starvation”:

## 9. Notes on Data Exposure
- Which windows have already been used for design:
- Which windows are no longer pristine:
- Which windows remain lower-contamination checks:

## 10. Config / File Plan
- Config files to create:
- Code changes required:
- Research log label:
- Report tag format:

## 11. Pre-Run Decision
- Approved to run?:
- Reason:
- Expected outcome:
- Main risk of this branch:

## 12. Post-Run Record
- Result summary:
- Decision:
- Recommendation:
- Next action: