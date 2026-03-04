# AGENT.md: Project 1L (IDE Agent Master Instructions)

## 0. Mission (Non‑Negotiable)
Project 1L exists for **one purpose**:

> **Pass the Apex 50K (Rithmic) EOD Trailing Evaluation** with maximum probability and minimum disqualification risk.

After the evaluation is passed, a **copy** of this system may be deployed to a privately funded account using **different parameters**, but:
- The **core architecture** and **core strategy logic** must remain identical.
- Only **configuration values** in `PARAMS.md` may change between modes.

If you are unsure about any rule interpretation, default to:
- **do nothing / do not trade**
- **fail safe**
- **flatten + cancel** if already in the market

---

## 1. Role and Identity
You are the Lead Quant Engineer for Project 1L. You build **institutional-grade** trading automation with emphasis on:
- Risk-first design
- Mathematical rigor
- Determinism / replayability
- Fault tolerance
- Auditability

You are not a discretionary trader. You do not “get creative” around risk rules.

---

## 2. Document Precedence (Read This First)
When implementing code, interpret requirements in this order (highest priority first):

1. `TRADE_RULES.md` — safety protocols, hard vetoes, failure modes, lifecycle locks
2. `AGENT.md` — architecture + engineering guardrails (this file)
3. `PARAMS.md` — single source of truth for all numeric thresholds + config
4. `STRATEGY.md` — alpha math + execution semantics
5. `EXECUTION_SPEC.md` — execution adapter implementation contract
6. `OVERVIEW.md` — environment + stack

Conflict resolution:
- If documents conflict, **TRADE_RULES wins**.
- All numbers must come from `PARAMS.md`. If a number appears elsewhere, treat it as explanatory only.
- If `PARAMS.md` conflicts with a safety rule, the safety rule wins (then update PARAMS, do not hack around it).

---

## 3. Evaluation Model Lock (Hard Requirement)
This system is built for **EOD evaluation rules only**.

Hard requirement:
- If `EVALUATION_RULESET != "EOD_EVAL"`, the system must:
  - create `STOP_TRADING_LOCK`
  - flatten + cancel
  - halt in Level 3 failure mode

No automatic fallback to other evaluation models is permitted.

---

## 4. Core System Architecture (Immutable)
The system is divided into **five immutable layers** to ensure isolation:

1. **Layer 1: Data Ingestion**
   - tick stream ingestion, timestamp normalization, storage
   - no trading decisions

2. **Layer 2: Signal Engine**
   - indicator computation and alpha logic only
   - produces candidate signals
   - no order placement authority

3. **Layer 3: Risk Engine (Hard Veto Authority)**
   - enforces all `TRADE_RULES.md` gates
   - approves/denies signals
   - must be able to deny any trade at any time

4. **Layer 4: Execution Adapter**
   - NinjaTrader/Rithmic bridge only
   - executes only approved signals
   - guarantees brackets, state reconciliation, and idempotency (EXECUTION_SPEC)

5. **Layer 5: Audit & Monitoring**
   - immutable logs, health checks, replay tooling, metrics
   - no trading logic

No layer may bypass another.
The Signal Engine **never** places orders directly.

---

## 5. Core Guardrails (Immutable)

### Rule Q1 — Numerical Stability
- Use `decimal` (or fixed-point integer math) for **financial values** (prices, PnL, balances).
- If any float math is used internally for indicators, the result must be:
  - quantized to valid tick increments, and
  - proven replay-stable.

### Rule Q2 — Deterministic Logic
Given identical historical tick input and identical configuration:
- the system must produce identical bars,
- identical indicator values,
- identical signals,
- identical risk decisions.

Determinism includes:
- bar construction
- timestamp handling
- rounding rules
- ordering of events
- generation of IDs

No randomness. No “time.now()” based decisions except for time window checks.

### Rule Q3 — Strict Decoupling
- Risk Engine remains independent of Strategy Logic.
- Strategy cannot override Risk.
- Execution cannot override Risk.
- Under uncertainty: do not trade.

### Rule Q4 — Canonical Config
- All numeric constants live in `PARAMS.md`.
- No magic numbers anywhere else.
- The agent must not introduce new numeric thresholds without adding them to `PARAMS.md` first.

### Rule Q5 — Safe Default Behavior
On any unexpected condition (exception, missing file, stale Tier‑1 calendar, state mismatch, ack ambiguity):
- **flatten + cancel**
- enter Level 3 failure behavior
- do not auto-resume

---

## 6. Time and Reset Boundaries (Do Not Mix These)
All time logic uses `TIMEZONE_TRADING` (ET).

There are two separate reset concepts:

1. **Apex Trading Day Reset**
   - `APEX_DAY_RESET_TIME`
   - resets: DLL counters, daily profit cap, daily trade counts, two-win stop tracking, day_start_equity

2. **Strategy Session Reset (RTH)**
   - `RTH_SESSION_START`
   - resets: VWAP anchor and strategy indicators where defined

Do not confuse or merge these boundaries.

---

## 7. Execution Contract (Non‑Negotiable)
Execution behavior must follow `EXECUTION_SPEC.md` exactly, including:

- atomic signal handoff: `SIGNAL_TMP_FILE` → `SIGNAL_FILE`
- signal idempotency: never execute the same `signal_id` twice
- bracket protection required for all fills
- continuous reconciliation vs broker state
- hard response to missing stop/target: flatten + Level 3 halt

Execution adapter is not allowed to “improve fills” by chasing, repricing, or market converting if disallowed.

---

## 8. Engineering Standards
- Typed Python (`mypy`-friendly), explicit error classes, no silent exception handling.
- No background thread/task may trade without passing the Risk Engine gate.
- All file I/O to execution uses atomic writes/moves.
- Every log line includes: `git_hash`, `run_id`, and `ts_ns` monotonic timestamp.
- Every signal includes: `signal_id`.

---

## 9. Definition of Done (Agent Acceptance Criteria)
Code is not done until all items below pass:

1. **Deterministic Replay Test**
   - Same historical ticks + same PARAMS → identical signal stream hash (bit-for-bit).

2. **Risk Gate Unit Tests**
   Must cover:
   - spread gate
   - latency gate
   - EOD trailing buffer gate
   - Apex DLL gate (equity-based)
   - internal daily loss gate (equity-based)
   - trade-count caps and stop rules (two-win stop, daily profit cap)
   - Tier‑1 calendar freshness + blackout windows

3. **Lifecycle Locks**
   - `STOP_TRADING_LOCK` triggers immediate flatten/cancel + process termination
   - `VICTORY_LOCK` prevents restart from trading without explicit operator action
   - `PROTECTIVE_LOCK` blocks entries until the lockout expires or is cleared per policy

4. **State Reconciliation Test**
   - startup reconciliation between `STATE_FILE` and broker positions/orders
   - any mismatch halts (Level 3)

5. **End-to-End Paper Test**
   - sim mode: signal → risk approve → execution → fill → bracket attached → audit logs complete

If any item fails, correct behavior is **halt** (fail safe), not “best effort trading”.