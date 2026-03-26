# Implementation Plan: Phase 2 - Institutional Liquidity Hunter (ILH-001)

## Goal
Build a market microstructure strategy that detects institutional participation via passive absorption and liquidity sweeps using MBP-1 (Market-By-Price Level 1) data.

## Phase 1 Archive Status
- [x] Create `archive/Phase_1_ORB` structure.
- [x] Move all ORB scripts, configs, and logs.
- [x] Rename old research log to `archive/strategy_experiment_log_PHASE1.md`.
- [x] Start fresh `docs/research/strategy_experiment_log.md`.

## Infrastructure Requirements (Phase 2)
### 1. CVD Engine (Cumulative Volume Delta)
- **Input:** MBP-1 Parquet files.
- **Logic:** Filter for `action='T'`. Accumulate `size` with sign based on `side` (B = +, S = -).
- **Output:** Tick-by-tick delta series.

### 2. Absorption Detector
- **Logic:**
    - Monitor `action='T'` events.
    - If `side='B'` (Buyer) and `price == ask_px_00`, increment `ask_absorption_volume`.
    - If `ask_px_00` moves higher, reset `ask_absorption_volume`.
    - **Signal:** If `ask_absorption_volume` > `Threshold` while price is stationary, flag "Institutional Selling Absorption".
    - Repeat for Bid side (Buying Absorption).

### 3. Tick-Based Backtest Engine (New)
- The ORB engine was candle-based (1m).
- Phase 2 requires a **TickReplay** engine to process MBP-1 events in sequence.
- **Location:** `src/project_1l/execution_adapter/tick_replay.py`

## Roadmap
### Step 1: MBP Data Access Layer
- Build a Python generator that yields MBP events from Parquet files ordered by `ts_event`.
- Handle MES/MNQ synchronization (sorting by timestamp).

### Step 2: CVD & Absorption Logic
- Create a `MicrostructureMonitor` class that maintains state for multiple instruments.

### Step 3: Trigger Logic
- **Sweep Trigger:** Detected when a large order consumes all liquidity at a level instantly.
- **Absorption Trigger:** High delta at a fixed price level without breakout.

### Step 4: Verification
- Backtest on 2023 Summer (High Volatility) to calibrate thresholds.
