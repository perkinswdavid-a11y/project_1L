# TRADE_RULES.md: Project 1L Safety and Resilience Protocols (EOD Evaluation)

## 0. Scope and Priority
This document defines **hard safety gates** and **lifecycle locks**. It has the highest priority in the project.

**Primary objective:** Pass the Apex 50K (Rithmic) **EOD evaluation** by preventing:
- EOD trailing drawdown breaches,
- Apex Daily Loss Limit (DLL) breaches,
- software failures,
- state desynchronization,
- uncontrolled variance.

## 1. Parameter Canonicality (Non‑Negotiable)
All numeric thresholds, time windows, filenames, and paths referenced here **MUST** be sourced from `PARAMS.md`.

If a number appears in code that is not in PARAMS (or derived from it), it is a spec violation.

## 2. Evaluation Model Lock (EOD Only)
Project 1L is built for **EOD evaluation rules only**.

Hard requirement:
- If `EVALUATION_RULESET != "EOD_EVAL"`, the system MUST fail safe:
  - Flatten + cancel,
  - create `STOP_TRADING_LOCK`,
  - enter **Level 3** failure and halt.

## 3. Definitions (Risk Math + Reset Boundaries)
All times are interpreted in `TIMEZONE_TRADING` (ET).

### 3.1 Apex Trading Day
- Resets at `APEX_DAY_RESET_TIME`.
- All “daily” counters MUST reset at this boundary:
  - `day_start_equity`
  - daily trade count
  - daily realized profit tracking
  - Two‑Win stop tracking
  - consecutive-loss tracking

### 3.2 Strategy Session (RTH)
- Anchored at `RTH_SESSION_START`.
- Used for strategy math resets (e.g., VWAP anchor), but NOT for Apex daily risk accounting.

### 3.3 Equity (Authoritative)
Equity is defined as:
- `equity = realized_pnl + unrealized_pnl - commissions - fees`

Equity MUST be sourced from broker/platform state (or reconciled local state) and treated as authoritative.

### 3.4 Day PnL (Equity-Based)
- `day_start_equity` is measured at the Apex day reset (`APEX_DAY_RESET_TIME`).
- `day_pnl = equity - day_start_equity`

### 3.5 Apex Daily Loss Limit (DLL) Floor
- `dll_floor = day_start_equity - APEX_DAILY_LOSS_LIMIT_USD`

### 3.6 EOD Trailing Floor (Broker-First)
- If the broker/platform provides the current trailing threshold/floor, it is the source of truth.
- If broker trailing floor is not available, compute and persist a conservative local approximation:

At each Apex day reset:
- `candidate_floor = equity_at_reset - MAX_DRAWDOWN_USD`
- `trailing_floor = max(previous_trailing_floor, candidate_floor)`

During the trading day:
- `trailing_floor` is treated as constant.

`trailing_floor` MUST be persisted in `STATE_FILE` and never “forgotten” across restarts.

### 3.7 Trade Definition (Used by Two‑Win Stop)
A “trade” is a **round trip**:
- flat → position → flat,
measured by **realized PnL** after the position is fully closed.

---

## Rule T1: Atomic Signal Handoff
Signal integrity:
- Use atomic moves only (`SIGNAL_TMP_FILE` → `SIGNAL_FILE`).
- The Execution Adapter MUST NEVER read `SIGNAL_TMP_FILE`.
- No order processing is allowed while the signal file is being replaced.

## Rule T2: Version Stamping and Audit Fields
Every log line MUST include:
- `git_hash`
- `run_id`
- monotonic `ts_ns`

Every signal MUST include:
- `signal_id`
- timestamp
- symbol
- side
- contracts
- all indicator values used to compute it (Z, RSI, volume ratio, ATR, VWAP)
- the exact Risk Engine decision (APPROVE/DENY) and denial reason if denied

## Rule T3: Emergency Brake (Kill Switch)
The kill switch is absolute:
- Every loop MUST check for `STOP_TRADING_LOCK`.
- If found:
  1. Log emergency stop.
  2. Request NinjaTrader “Flatten and Cancel”.
  3. Terminate the process immediately (`os._exit(1)`).

## Rule T4: Signal Idempotency (At‑Most‑Once Execution)
The same `signal_id` MUST NOT be executed more than once.

Execution Adapter requirements:
- Track processed `signal_id` values.
- If a `signal_id` is already processed, ignore it and log an idempotency skip.

## Rule T5: Time Window Enforcement (Hard Gate)
Time gating is enforced by Risk Engine (not only by Strategy):
- Entries are forbidden outside `[TRADING_WINDOW_START, TRADING_WINDOW_END]`.
- At `HARD_FLATTEN_TIME`, the system MUST:
  - flatten all positions,
  - cancel all working orders,
  - reject all new entries until the next strategy day.

## Rule T6: State Synchronization (Startup)
State recovery:
- The system MUST maintain `STATE_FILE`.
- On startup, reconcile local state against broker-reported live state (positions + working orders).
- Any discrepancy triggers **Level 3** failure (flatten + lockdown).

## Rule T7: Dead‑Man’s Switch (Heartbeat)
Heartbeat:
- Interval: `HEARTBEAT_INTERVAL_SEC`
- Timeout: `HEARTBEAT_TIMEOUT_SEC`
- On timeout:
  - Execution side must immediately “Flatten and Cancel”.
  - System enters **Level 3** failure.

## Rule T8: Market Quality Gate (Spread)
Liquidity protection:
- Entries are forbidden if:
  - MES spread > `MES_MAX_SPREAD_TICKS`, or
  - MNQ spread > `MNQ_MAX_SPREAD_TICKS`.

## Rule T9: Latency Gate
Execution quality:
- If RTT > `MAX_RTT_MS`, new entries are prohibited until latency normalizes.

## Rule T10: Volatility Brake (Tier‑1 Events)
News protection:
- Trading is suspended from:
  - `TIER1_BLACKOUT_BEFORE_MIN` minutes before
  - to `TIER1_BLACKOUT_AFTER_MIN` minutes after
  any Tier‑1 release listed in `TIER1_EVENTS_FILE`.

Precondition:
- If the Tier‑1 events file is missing OR older than `TIER1_EVENTS_MAX_AGE_HOURS`,
  the system MUST fail safe (Level 3) and not trade.

## Rule T11: Trailing Floor Safety Buffer (Internal)
Drawdown protection:
- If `equity <= trailing_floor + TRAILING_FLOOR_BUFFER_USD`:
  - Immediately flatten.
  - Cancel all working orders.
  - Create `PROTECTIVE_LOCK`.
  - Disable trading for `PROTECTIVE_LOCKOUT_HOURS`.

## Rule T12: Apex DLL Gate (Hard Stop Before Broker Liquidation)
DLL protection is equity-based and enforced continuously:
- Compute `dll_floor = day_start_equity - APEX_DAILY_LOSS_LIMIT_USD`.
- If `equity <= dll_floor + APEX_DAILY_LOSS_BUFFER_USD`:
  - Immediately flatten (marketable exit is allowed for safety).
  - Cancel all working orders.
  - Disable entries until the next Apex day reset.
  - Record the breach and denial reason in logs.

## Rule T13: Internal Daily Max Loss (Circuit Breaker)
Internal circuit breaker is equity-based:
- If `day_pnl <= -INTERNAL_MAX_DAILY_LOSS_USD`:
  - Immediately flatten.
  - Cancel all working orders.
  - Disable entries until the next Apex day reset.

This is a variance control buffer intended to prevent approaching the DLL boundary.

## Rule T14: Consecutive Loss Circuit Breaker
If consecutive losing trades (as defined in §3.7) reach `CONSECUTIVE_LOSS_LIMIT` within the Apex trading day:
- Disable new entries until the next Apex day reset.
- Existing positions remain protected by brackets; flatten if required by other rules.

## Rule T15: Daily Profit Cap (Variance Control)
If `ENABLE_DAILY_PROFIT_CAP = true` and daily realized profit ≥ `DAILY_PROFIT_CAP_USD`:
- Disable new entries for the remainder of the Apex trading day.

Implementation notes:
- “Daily realized profit” resets at `APEX_DAY_RESET_TIME`.
- This rule is a stop‑trading rule, not a target‑seeking rule.

## Rule T16: Two‑Win Stop Rule (Variance Control)
If `ENABLE_TWO_WIN_STOP = true` then:

- If `TWO_WIN_STOP_ONLY_IF_FIRST_N_TRADES = true`:
  - If the first `TWO_WIN_STOP_TRADES` completed trades of the Apex day are winners,
    disable further entries for the remainder of the Apex day.
- Otherwise:
  - If `TWO_WIN_STOP_TRADES` wins occur (in any order) within the Apex day,
    disable further entries for the remainder of the Apex day.

## Rule T17: Live Order/Position Reconciliation (Continuous)
Synchronization:
- On every position update (or at minimum every bar close), compare:
  - local `STATE_FILE` vs broker position counts and working orders.
- Any discrepancy triggers immediate **Level 3** failure (flatten + lockdown).

## Rule T18: The Pre‑Trade Gate (Hard Veto)
Before any signal can be released to execution, Risk Engine MUST verify ALL of the following:

A. Evaluation Lock
- `EVALUATION_RULESET == "EOD_EVAL"`

B. Hard Locks
- `STOP_TRADING_LOCK` is absent
- `PROTECTIVE_LOCK` is absent
- `VICTORY_LOCK` is absent

C. Time Gates
- Current time within `[TRADING_WINDOW_START, TRADING_WINDOW_END]`
- Current time < `HARD_FLATTEN_TIME`

D. Market Quality
- Spread gate (T8)
- Latency gate (T9)

E. Event Risk
- Tier‑1 blackout window (T10)

F. Risk Floors (equity-based)
- `equity > trailing_floor + TRAILING_FLOOR_BUFFER_USD` (T11)
- `equity > dll_floor + APEX_DAILY_LOSS_BUFFER_USD` (T12)
- `day_pnl > -INTERNAL_MAX_DAILY_LOSS_USD` (T13)

G. Exposure Limits
- Position caps: `SYSTEM_MAX_CONTRACTS`, max open positions (total + per instrument)
- Caps must be <= `APEX_MAX_CONTRACTS`

H. Trade Count Limits
- Stage trade caps (`STAGE*_MAX_TRADES`)
- `HARD_MAX_TRADES_PER_DAY`
- Daily trade count resets at `APEX_DAY_RESET_TIME`

I. Stop Rules
- Daily profit stop active (T15)
- Two‑Win stop active (T16)
- Consecutive loss stop active (T14)

J. Strategy Freeze
- If T19 freeze condition is active, deny.

If any check fails:
- Discard the signal,
- log a single-line structured denial reason,
- do NOT retry the same signal.

## Rule T19: Statistical Strategy Freeze (Internal)
Regime protection:
- If realized win rate drops below `WINRATE_FREEZE_THRESHOLD` over any `WINRATE_FREEZE_WINDOW_TRADES` trade window:
  - Enter Level 2 failure mode (halt entries).
  - Reset policy MUST be deterministic (next Apex day reset OR explicit manual reset).

## Rule T20: Immutable Audit Trail
Data integrity:
- Every signal, fill, cancel, and system error MUST be logged to an append‑only store.
- Live process MUST never modify prior audit records.

## Rule T21: Deterministic Replay Mode
Auditability:
- The system must be able to consume historical ticks and produce signals identical to live.
- Replay is mandatory for diagnosing “logic vs slippage” issues.

## Rule T22: Failure Severity Taxonomy
- Level 1 (Soft): network/API disconnect  
  Action: auto-reconnect + state sync permitted.
- Level 2 (Risk): spread/latency breach, Tier‑1 window, statistical freeze, circuit breakers, stop rules  
  Action: halt entries; maintain protection on existing positions; flatten if required by specific rule.
- Level 3 (Critical): state desync, determinism violation, kill switch, heartbeat timeout, missing Tier‑1 file/freshness  
  Action: flatten all, cancel all, create lock, require manual intervention.

## Rule T23: Simulation Fidelity Standards
Backtesting MUST model:
- Slippage (use `BACKTEST_SLIPPAGE_TICKS_*`)
- Queue position: limit fills require trade-through (`BACKTEST_REQUIRE_TRADE_THROUGH_FOR_LIMIT_FILL`)
- Commissions via the selected backtest environment configuration

## Rule T24: Deployment Separation
- Research: local machine
- Evaluation: QuantVPS (Rithmic sim feed)
- Production/Private: separate config profile and logs

No cross-contamination of state files between environments.

## Rule T25: Pre‑Flight System Health Check (Daily)
Before trading is permitted for the day, verify:
1. RTT < `MAX_RTT_MS`
2. Local clock is sane vs broker timestamps (no drift large enough to break window logic)
3. Apex day boundary logic is correct:
   - daily counters reset at `APEX_DAY_RESET_TIME`
   - `day_start_equity` captured at last reset
4. Strategy session boundary logic is correct:
   - strategy session reset at `RTH_SESSION_START` (VWAP anchor)
5. `trailing_floor` is sane and persists across restarts (and matches broker value if available)
6. `STOP_TRADING_LOCK` is absent
7. `PROTECTIVE_LOCK` is absent (unless intentionally active)
8. `VICTORY_LOCK` is absent
9. Tier‑1 events file exists and is fresh enough (T10)

If any check fails: Level 3 lockdown.

## Rule T26: Evaluation Termination Condition (Victory Switch)
Goal fulfillment:
- If `equity >= VICTORY_EQUITY_USD`:
  1. Flatten all positions immediately.
  2. Cancel all pending orders.
  3. Create `VICTORY_LOCK`.
  4. Terminate the trading process.
- Restart is prohibited without explicit operator action to switch modes.
