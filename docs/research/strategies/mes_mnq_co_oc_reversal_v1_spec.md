# mes_mnq_co_oc_reversal_v1 — Implementation Specification

**Memo reference:** `docs/research/strategies/mes_mnq_co_oc_reversal_v1_memo.md`
**Date:** 2026-03-10
**Status:** APPROVED FOR IMPLEMENTATION

---

## 1. Data Specification

- **Bar type:** 1m OHLCV
- **Timestamp convention:** bar_close CT
- **Session window:** 08:30–15:00 CT
- **Session timezone:** America/Chicago
- **Primary instrument:** MES front-month, dominant_by_day
- **Context instrument:** MNQ front-month, dominant_by_day
- **Required prior-day data:** prior cash close for both legs (last bar close ≤ 15:00 CT prior session)
- **Roll handling:** standard Project 1L front-month continuity; no strategy-side roll logic required

---

## 2. Signal Computation

For each trading day, computed at the `08:30` bar close:

```
prior_close_MES = close of last bar in [session_start, 15:00 CT] on prior session day
prior_close_MNQ = close of last bar in [session_start, 15:00 CT] on prior session day

open_0830_MES   = open of the 08:30 CT bar (current day)
open_0830_MNQ   = open of the 08:30 CT bar (current day)

r_on_MES = ln(open_0830_MES / prior_close_MES)
r_on_MNQ = ln(open_0830_MNQ / prior_close_MNQ)
delta_on = r_on_MNQ - r_on_MES
```

Decision rule:
- `delta_on > 0` → MNQ is overnight winner → long 3 MES, short 2 MNQ
- `delta_on < 0` → MES is overnight winner → long 2 MNQ, short 3 MES
- `delta_on = 0` → no trade

**State that must persist across bars:**
- `prior_close_MES` and `prior_close_MNQ`: captured at end of each session, held for next day
- `pair_open_pnl`: running combined MES + MNQ marked-to-market P&L, updated each bar
- `active_trade`: bool, True if in a position
- `entry_bar_time`: time of entry fill

---

## 3. Entry Logic

- Signal evaluated on: `08:30` bar close
- Entry filled at: `08:31` bar open (next-bar-open standard model)
- Entry condition: `delta_on ≠ 0` and no trade already active today

**Long leg fill:** next-bar open of the overnight loser instrument
**Short leg fill:** same bar open of the overnight winner instrument (synchronized)

- Slippage: 1 tick per leg per entry side
- Commission: $1.25 per leg per entry side
- Position size: fixed spread unit (3 MES + 2 MNQ)

---

## 4. Exit Logic

### Primary exit — time stop
- Signal: `14:59` bar close (last bar before boundary)
- Fill: `15:00` bar open
- Applies to both legs simultaneously

### Hard stop — pair P&L floor
- Evaluated each bar close during active trade
- Condition: `combined_pair_pnl ≤ -$300`
- Fill: next bar open after the bar where threshold is breached
- Applies to both legs simultaneously
- No re-entry after hard stop on the same day

**Exit fill model:** next-bar open (standard)
**Slippage:** 1 tick per leg per exit side
**Commission:** $1.25 per leg per exit side

---

## 5. Pair P&L Computation

```
pnl_MES = (mark_price_MES - entry_price_MES) × direction_MES × contracts_MES × 5.0
pnl_MNQ = (mark_price_MNQ - entry_price_MNQ) × direction_MNQ × contracts_MNQ × 2.0
combined_pair_pnl = pnl_MES + pnl_MNQ
```

Where:
- `direction_MES` = +1 if long MES, -1 if short MES
- `direction_MNQ` = +1 if long MNQ, -1 if short MNQ
- `contracts_MES` = 3
- `contracts_MNQ` = 2

MNQ P&L is injected via `context_leg_cash_delta` (existing split-execution pattern from QC-001 engine modification).

---

## 6. Cost Model

| Item | Value |
|---|---|
| Commission per leg per side | $1.25 |
| Slippage per leg per side | 1 tick = $1.25 MES / $0.50 MNQ |
| Round-trip cost (baseline) | 4 legs × 2 sides × (commission + slippage) |
| MES round-trip per spread | 3 × 2 × ($1.25 + $1.25) = $15.00 |
| MNQ round-trip per spread | 2 × 2 × ($1.25 + $0.50) = $7.00 |
| **Total baseline round-trip** | **~$22 per spread unit** |
| Stress case (2 ticks slippage) | +$11.25 MES + $4.00 MNQ ≈ +$15 additional |

---

## 7. Risk Controls

- Max spread units per session: 1
- Max trades per session: 1 (no re-entry)
- Hard stop: combined pair P&L ≤ -$300
- Daily flatten: all positions closed by 15:00 CT boundary
- No overnight inventory

---

## 8. Contract Roll Handling

- Instrument mode: dominant_by_day for both MES and MNQ
- Roll dates handled automatically by engine
- Prior-close capture must use the same dominant contract as the prior session
- No strategy-side roll handling required

---

## 9. Required Outputs

**Standard outputs:**
- `closed_trades.csv`
- `daily_equity.csv`
- `executions.csv`
- `summary.json`
- Auto-log to `strategy_experiment_log.md` via research_logger

**Required diagnostic outputs (Dev-A evaluation):**
1. Trade count, win rate, avg winner, avg loser
2. Profit factor, net P&L, max drawdown
3. P&L by time bucket: first hour 08:31–09:30 / midday 09:30–12:00 / last hour 12:00–15:00
4. Slippage sensitivity: 0 tick / 1 tick / 2 ticks per leg
5. Date concentration: top 10 best dates and top 10 worst dates share of total P&L
6. Sign-flip control: compare long-loser/short-winner vs long-winner/short-loser over same period

---

## 10. Edge Cases

| Scenario | Handling |
|---|---|
| Missing `08:30` bar for either leg | No trade that day |
| `delta_on = 0` exactly | No trade that day |
| Prior session had no close bar | No trade that day (missing anchor) |
| Hard stop fires on time-exit bar | Hard stop takes priority; flush at same open |
| MES or MNQ leg fill fails | Log as execution error; treat as flat for the session |

---

## 11. Dev-A Window

- Start: `2023-02-26`
- End: `2023-08-31`
- Framework minimum trade count: 30 closed trades (spread family floor: 20)
- Expected approximate trade count: ~120 sessions × ~90% signal rate ≈ ~108 trades

---

## 12. Dev-B Window (reserved)

- Start: `2023-09-01`
- End: `2024-02-29`
- Not to be evaluated until Dev-A passes
