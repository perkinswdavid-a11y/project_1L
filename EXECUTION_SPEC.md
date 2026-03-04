# EXECUTION_SPEC.md
Project 1L – Execution Adapter Specification (NinjaTrader 8 via Rithmic)

---

## 1. Purpose

This document defines the exact behavior of the **Execution Adapter**.

The Execution Adapter is the bridge between:
- The **Signal Engine / Risk Engine** (produces *approved* trade instructions)
- The **Broker Platform** (NinjaTrader 8 connected to Rithmic)

Responsibilities (execution only):
- Read approved signals from the atomic signal file handoff
- Submit entry orders exactly as specified
- Attach OCO bracket protection (stop + target) immediately upon fill
- Track and reconcile broker state vs local state
- Enforce emergency flatten/cancel on hard locks and failures
- Produce audit logs for every action and broker update

The Execution Adapter MUST NOT:
- compute indicators (VWAP/ATR/RSI/Z)
- decide whether a trade “should” happen (Risk Engine owns that)
- loosen any safety rule from `TRADE_RULES.md`

All thresholds, filenames, and time windows referenced below come from `PARAMS.md` (canonical).

---

## 2. Inputs, Outputs, and Files

### 2.1 Canonical Files (from PARAMS)
- `SIGNAL_TMP_FILE`
- `SIGNAL_FILE`
- `STATE_FILE`
- `STOP_TRADING_LOCK`
- `PROTECTIVE_LOCK`
- `VICTORY_LOCK`

### 2.2 Signal Handoff (Atomic)
Signal pipeline is always:

    SIGNAL_TMP_FILE → SIGNAL_FILE

Rules:
- The Execution Adapter MUST NEVER read `SIGNAL_TMP_FILE`.
- The Execution Adapter reads `SIGNAL_FILE` only after it exists and is stable.
- If the signal is malformed or missing required fields, the adapter must reject it and log the reason (and must NOT “guess”).

---

## 3. Signal Schema (Execution Contract)

The signal file contains a single JSON object (one signal per file write). Example:

    {
      "signal_id": "uuid",
      "timestamp": "2026-03-04T10:45:00-05:00",
      "symbol": "MES",
      "side": "BUY",
      "contracts": 1,
      "entry_type": "LIMIT_AT_TOUCH",
      "stop_loss_ticks": 8,
      "take_profit_ticks": 4,
      "risk_decision": "APPROVE",
      "risk_reason": "OK",
      "git_hash": "abc123",
      "run_id": "run-uuid"
    }

Required fields:
- `signal_id` (unique)
- `timestamp` (ISO8601 with timezone)
- `symbol` (must be in `INSTRUMENTS`)
- `side` ("BUY" or "SELL")
- `contracts` (must be <= `SYSTEM_MAX_CONTRACTS` and <= `APEX_MAX_CONTRACTS`)
- `entry_type` (must equal `ENTRY_ORDER_TYPE`)
- `stop_loss_ticks` (integer ticks)
- `take_profit_ticks` (integer ticks)
- `risk_decision` must be `"APPROVE"` (Execution Adapter rejects anything else)

Optional fields (allowed, not required):
- `entry_limit_price` (if present, must be used; if absent, adapter uses LIMIT_AT_TOUCH semantics)
- `stop_price`, `target_price` (if present, adapter may prefer prices over ticks)
- `strategy_snapshot` (logging only)

If `risk_decision != "APPROVE"`, the adapter MUST NOT place orders.

---

## 4. Global Safety Checks (Always-On)

Before doing anything (including reading signals), the adapter must enforce:

### 4.1 Lock Files
- If `STOP_TRADING_LOCK` exists:
  - immediately request NinjaTrader “Flatten and Cancel”
  - log the event
  - terminate the process (hard stop)

- If `VICTORY_LOCK` exists:
  - ensure flat + canceled
  - do not process new signals
  - remain idle or exit (implementation choice; must be deterministic)

- If `PROTECTIVE_LOCK` exists:
  - ensure flat + canceled
  - do not process new signals until the lock is cleared by policy in `TRADE_RULES.md`

### 4.2 Hard Flatten Time
Using `TIMEZONE_TRADING`:
- If current time >= `HARD_FLATTEN_TIME`:
  - ensure flat + canceled
  - reject all new signals until the next allowed session

---

## 5. Idempotency (At-Most-Once Execution)

The adapter MUST NEVER execute the same `signal_id` twice.

Requirements:
- Maintain a persisted cache of processed `signal_id` values (in `STATE_FILE` or a dedicated persisted set).
- If a signal arrives with a `signal_id` already marked processed:
  - ignore it
  - log an idempotency skip
  - do not place any orders

---

## 6. Entry Order Placement

### 6.1 Allowed Entry Type
The only allowed entry type in evaluation mode is:

    ENTRY_ORDER_TYPE = "LIMIT_AT_TOUCH"

The adapter must validate `signal.entry_type == ENTRY_ORDER_TYPE` or reject.

### 6.2 LIMIT_AT_TOUCH Semantics
- Long entry:
  - submit a LIMIT BUY at current bid
- Short entry:
  - submit a LIMIT SELL at current ask

If `entry_limit_price` is supplied in the signal:
- use it exactly (after tick-size rounding per instrument rules)
- log both the supplied price and the final rounded price

### 6.3 Entry Timeout
- The maximum time an entry may remain unfilled is `ENTRY_MAX_WAIT_SECONDS`.
- If not filled by timeout:
  - cancel the entry order
  - log cancel + reason `"ENTRY_TIMEOUT"`
  - mark the signal as processed (to avoid repeated attempts)
  - return to idle

### 6.4 No Chasing Policy
If `ENTRY_ALLOW_REPRICE = false`:
- do not reprice
- do not convert to market
- do not submit follow-up “replacement” entries

---

## 7. Order Acknowledgement Rule (No Duplicate Orders)

Never submit a new order while any prior order is awaiting broker acknowledgement.

State machine requirement:
- Submit order
- Wait for broker ACK / order-id confirmation
- Only then proceed (e.g., submit bracket, cancel, or accept next signal)

If ACK is not received within a reasonable time:
- treat as execution integrity risk
- enter failure handling per §12 (typically Level 3: flatten + halt)

---

## 8. Bracket Orders (Mandatory Protection)

### 8.1 Bracket Structure
All trades must be protected using an OCO bracket:

    Entry
     ├── Stop Loss (STOP MARKET)
     └── Take Profit (LIMIT)

Stop and target must share the same OCO group.

### 8.2 Stop Loss
- Stop order type: STOP MARKET
- Stop distance is provided by the signal:
  - prefer `stop_price` if provided
  - otherwise compute from `stop_loss_ticks`
- The stop must be placed immediately upon fill.

If the stop cannot be confirmed as working:
- immediately flatten the position
- cancel all
- enter Level 3 failure behavior (see §12)

### 8.3 Take Profit
- Target order type: LIMIT
- Target is provided by the signal:
  - prefer `target_price` if provided
  - otherwise compute from `take_profit_ticks`
- The target must be placed immediately upon fill.

If the target cannot be confirmed as working:
- immediately flatten the position
- cancel all
- enter Level 3 failure behavior (see §12)

### 8.4 Partial Fills
If an entry partially fills:
- immediately attach protection sized to the currently filled quantity
- if filled quantity changes (additional partials), update bracket quantities to match
- if the adapter cannot keep brackets synchronized to filled quantity:
  - flatten and halt (integrity failure)

---

## 9. State Tracking (STATE_FILE)

The adapter must update `STATE_FILE` (append-only log + latest snapshot pattern is acceptable) with:

- current broker position (qty, avg price, symbol, side)
- all working orders (ids, types, prices, quantities, OCO ids)
- last processed `signal_id`
- processed `signal_id` cache (persisted)
- last reconcile timestamp

The adapter must treat broker/platform state as the source of truth.

---

## 10. Continuous Reconciliation

At minimum every bar close (or faster if events are available), reconcile:

- local position == broker position
- local working orders == broker working orders
- bracket existence for any open position

If mismatch occurs:
- immediately flatten all positions
- cancel all orders
- enter Level 3 failure behavior (see §12)

---

## 11. Cancel Logic

The adapter must cancel orders when:
- entry timeout occurs (§6.3)
- trading window is closed (Risk Engine should prevent signals; adapter still defends)
- `HARD_FLATTEN_TIME` reached (§4.2)
- any lock file requires it (§4.1)
- a critical integrity failure is detected (§10)

Every cancel request must be followed by cancel confirmation validation and logging.

---

## 12. Failure Handling (Execution-Side)

Failure levels align with `TRADE_RULES.md` taxonomy.

### Level 1 – Soft Failure (Recoverable)
Examples:
- transient disconnect with full state recoverable

Actions:
- reconnect
- reconcile state
- resume only if state is consistent and flat (or protected)

### Level 2 – Risk Failure (Halt Entries)
Examples:
- latency/spread issues detected upstream
- protective lock active

Actions:
- do not submit new entries
- maintain protection on any existing position (or flatten if required)

### Level 3 – Critical Failure (Flatten + Halt)
Examples:
- state desynchronization
- missing bracket protection on an open position
- duplicate/unacknowledged order ambiguity
- heartbeat/kill switch triggers (handled immediately)

Actions:
- flatten all positions immediately
- cancel all working orders
- log a critical failure event
- halt the system (do not auto-resume)

---

## 13. Logging (Execution Adapter)

Every action must be logged with:
- `git_hash`, `run_id`, monotonic `ts_ns`
- `signal_id` when applicable
- broker order ids + OCO ids
- event type (SUBMIT_ENTRY, ENTRY_ACK, ENTRY_FILL, SUBMIT_STOP, SUBMIT_TARGET, CANCEL, FLATTEN, RECONCILE_OK, RECONCILE_FAIL)
- reason codes for rejects, cancels, and failures
