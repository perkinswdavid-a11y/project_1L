# OVERVIEW.md: Project 1L System Overview

## 0. Purpose
Project 1L is an automated futures trading system designed for **one objective**:

> **Pass the Apex 50K (Rithmic) EOD Trailing Evaluation with maximum probability and minimal variance.**

The system prioritizes:

- Risk containment over profit maximization  
- Deterministic behavior over adaptive complexity  
- Stability over trade frequency  
- Strict enforcement of evaluation rules  

Project 1L is intentionally engineered to behave like a **prop-desk risk engine first and a strategy second**.

---

## 1. System Architecture Summary

Project 1L is composed of five isolated layers to prevent cross-contamination of logic:

1. **Data Layer**
   - Tick ingestion
   - Time normalization
   - Bar construction
   - Persistent storage

2. **Signal Engine**
   - VWAP-anchored mean reversion logic
   - Indicator calculations
   - Deterministic signal generation

3. **Risk Engine**
   - Hard veto authority over all trades
   - Enforcement of evaluation constraints
   - Enforcement of internal variance controls

4. **Execution Adapter**
   - Converts approved signals into broker orders
   - Manages OCO bracket orders
   - Maintains broker/system state synchronization

5. **Audit & Monitoring**
   - Immutable logging
   - Deterministic replay validation
   - Health checks and system watchdogs

No layer may bypass another.

The **Risk Engine must always have final authority** over trade execution.

---

## 2. Documentation Structure

The system specification is defined by the following documents.

They must be read in this order of precedence:

1. `TRADE_RULES.md`  
   Defines risk gates, safety protocols, failure modes, and lifecycle locks.

2. `AGENT.md`  
   Defines engineering standards, system architecture rules, and IDE agent behavior.

3. `PARAMS.md`  
   The **canonical source of truth** for all configuration values.

4. `STRATEGY.md`  
   Defines alpha generation logic and signal mathematics.

5. `EXECUTION_SPEC.md`  
   Defines order handling and broker interaction rules.

6. `OVERVIEW.md`  
   High-level system description (this file).

If any documents conflict:

- `TRADE_RULES.md` takes precedence.
- Numeric values must always be sourced from `PARAMS.md`.

---

## 3. Operating Modes

The system supports two operational profiles.

### Mode A — Evaluation Mode (Primary)

This is the default operating mode.

Characteristics:

- Strict adherence to Apex evaluation rules
- Conservative risk management
- Low trade frequency
- Variance suppression

The objective is **consistent equity growth until the evaluation target is reached**.

### Mode B — Private Funded Mode

After passing the evaluation:

- The same strategy and architecture are used.
- Only parameter values in `PARAMS.md` may change.

All safety systems remain active.

---

## 4. Software Stack

Primary language:

- Python 3.13.12 (asyncio architecture)

Core libraries:

- DuckDB — historical data storage and query engine
- Polars — high-performance dataframe processing
- PyArrow — Parquet serialization
- Loguru — structured logging
- Databento — tick-level data source

Execution environment:

- NinjaTrader 8
- Rithmic data and execution gateway

---

## 5. Hosting Environment

Evaluation environment:

- QuantVPS (Chicago data center)

Research environment:

- Local workstation with high-capacity SSD storage

Deployment separation:

| Environment | Purpose |
|--------------|---------|
| Research | Strategy development and backtesting |
| Evaluation | Apex challenge execution |
| Production | Private funded trading |

State files and logs must **never be shared across environments**.

---

## 6. Required External Inputs

The system requires the following external inputs to operate.

1. **Live market data feed**
   - Rithmic connection through NinjaTrader

2. **Historical tick data**
   - Databento `.dbn.zst` archives for research and replay

3. **Tier-1 economic calendar**
   - Maintained locally and referenced in `PARAMS.md`

If any required input is unavailable or stale:

- The system must **fail safe**
- Trading must be disabled

---

## 7. System Design Philosophy

Project 1L follows five core principles.

### Determinism
Given identical data inputs and parameters, the system must produce identical outputs.

### Isolation
Signal logic, risk logic, and execution logic are strictly separated.

### Auditability
All actions must be reproducible via deterministic replay.

### Fail-Safe Behavior
Unexpected states always resolve to **flatten + halt**.

### Evaluation Discipline
The system prioritizes **evaluation completion**, not profit maximization.

---

## 8. Success Condition

The system is considered successful when:

- Account equity reaches the configured `VICTORY_EQUITY_USD`
- All positions are flattened
- The `VICTORY_LOCK` file is created
- Trading terminates automatically

No further trades are allowed without explicit operator intervention.

---