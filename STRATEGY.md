# STRATEGY.md: Project 1L Alpha Generation (MES/MNQ Mean Reversion)

## 0. Purpose
The Alpha Engine generates **mean reversion** signals designed for **evaluation passing**, not maximum trade frequency.

Primary priorities:
- Controlled variance
- High signal quality over quantity
- Deterministic replay capability
- Seamless integration with the Risk Engine hard gate (TRADE_RULES)

This strategy is intentionally **fixed-parameter** during evaluation (no adaptive thresholds, no ML, no randomness).

---

## 1. Parameterization (Hard Requirement)
All thresholds and constants referenced in this document MUST be pulled from `PARAMS.md`.
No hard-coded numbers are allowed in implementation.

---

## 2. Timezone, Session, and Data Scope
- Trading timezone: `TIMEZONE_TRADING` (ET)
- Strategy session anchor: `RTH_SESSION_START` (used for VWAP reset + strategy session logic)
- Trading window: entries only between `TRADING_WINDOW_START` and `TRADING_WINDOW_END` (Risk Engine enforces)
- Hard flatten: must be flat by `HARD_FLATTEN_TIME` (Risk Engine + Execution enforce)

Important boundary note:
- **Apex “trading day” resets at `APEX_DAY_RESET_TIME`** for daily risk counters (DLL, daily caps, trade counts). This is handled by the Risk Engine per `TRADE_RULES.md`.

Data requirements:
- RTH-only logic for VWAP anchor and strategy statistics.
- No extended-hours carryover influence for indicators.
- Signal generation must be deterministic in replay (same ticks → same bars → same signals).

---

## 3. Bar Construction (Determinism Requirement)
Signals are evaluated on **bar close** only:
- Bar type: `BAR_TYPE`
- Bar interval: `BAR_INTERVAL_SECONDS`
- Evaluation timing: `SIGNAL_EVALUATION = BAR_CLOSE`

VWAP may update tick-by-tick, but **signal decisions** occur only at the deterministic bar boundary.

Price definitions:
- `LastPrice` used in formulas below is the bar-close last traded price (deterministic from the bar builder).
- Bar volume is the total traded volume aggregated into the bar.

---

## 4. Core Thesis
Exploit statistically significant deviations from session fair value (VWAP) during the stable midday RTH regime.

Exclusions:
- No breakout trading
- No trend continuation logic
- No open/close volatility participation

---

## 5. Primary Signal Construction

### 5.1 Fair Value Anchor — Session VWAP
VWAP is computed as:

- VWAP = Σ(price × volume) / Σ(volume)

Rules:
- VWAP anchor: `VWAP_ANCHOR` (expected: RTH session)
- Reset at `RTH_SESSION_START`
- Updated tick-by-tick (or bar-by-bar) but must be replay-stable.

### 5.2 Deviation Metric — VWAP Z-Score (Critical)
Compute:

- Z = (LastPrice − VWAP) / σ

Where:
- σ is the rolling standard deviation of **deviations from VWAP**, not raw price:
  - deviation_t = (Price_t − VWAP_t)
  - σ = std(deviation) over `Z_SCORE_PERIOD_BARS`

Requirements:
- Z is computed at bar close.
- No smoothing.
- No forward fill.
- No lookahead.

Entry thresholds:
- Long candidate: `Z < -Z_SCORE_THRESHOLD`
- Short candidate: `Z > +Z_SCORE_THRESHOLD`

### 5.3 Exhaustion Confirmation Filters
Momentum filter (RSI):
- RSI length: `RSI_PERIOD_BARS`
- Long: `RSI < RSI_OVERSOLD`
- Short: `RSI > RSI_OVERBOUGHT`
- Wilder smoothing (deterministic)

Volume confirmation:
- Volume_current > `VOLUME_MULTIPLIER` × SMA(volume, `VOLUME_SMA_PERIOD_BARS`)
- If volume is unavailable or zero, treat as “no confirmation” (no entry).

---

## 6. Entry Conditions (Signal → Risk Gate → Execution)
A valid entry signal requires ALL conditions:

Long:
- `Z < -Z_SCORE_THRESHOLD`
- `RSI < RSI_OVERSOLD`
- Volume confirmation satisfied
- Within trading window
- Risk Engine approval

Short:
- `Z > +Z_SCORE_THRESHOLD`
- `RSI > RSI_OVERBOUGHT`
- Volume confirmation satisfied
- Within trading window
- Risk Engine approval

No partial-condition entries.
No predictive bias.
No discretionary overrides.

---

## 7. Entry Execution Specification (Deterministic)
Entry order semantics are fixed and evaluation-safe:

- `ENTRY_ORDER_TYPE = LIMIT_AT_TOUCH`
  - Long: join bid with a limit buy
  - Short: join ask with a limit sell
- If not filled within `ENTRY_MAX_WAIT_SECONDS`, cancel and discard the signal (no chasing).
- `ENTRY_ALLOW_REPRICE = false` (no re-pricing, no market conversion).

Cooldown:
- After any filled trade, enforce `COOLDOWN_SECONDS` before the next entry attempt.

Concurrency:
- Enforce `MAX_OPEN_POSITIONS_TOTAL` and `MAX_OPEN_POSITIONS_PER_INSTRUMENT`.
- Never exceed `SYSTEM_MAX_CONTRACTS`.

---

## 8. Exit Logic (Bracket Orders Required)
All entries must be protected with bracket orders immediately upon fill.

### 8.1 Stop Loss (Hard)
- Stop sizing: `STOP_LOSS_ATR_MULTIPLIER` × ATR(`ATR_PERIOD_BARS`)
- ATR computed on the same bar series using True Range
- Stop must be placed immediately upon entry confirmation

### 8.2 Take Profit (Primary + Fallback)
Primary target:
- Reversion to VWAP (mean)

Fallback target (if VWAP distance is too small):
- MES: `MES_FIXED_TP_TICKS`
- MNQ: `MNQ_FIXED_TP_TICKS`

Evaluation mode prohibits trailing stops.

---

## 9. Position Sizing & Capital Path (Evaluation-Safe)
Position sizing is governed by **NET PnL relative to STARTING_BALANCE_USD** and capped by `SYSTEM_MAX_CONTRACTS`.

Stage definitions:
- Stage 1 (Grind): NetPnL < `STAGE1_MAX_NETPNL_USD`
- Stage 2 (Push): `STAGE1_MAX_NETPNL_USD` ≤ NetPnL ≤ `STAGE2_MAX_NETPNL_USD`
- Stage 3 (Defense): NetPnL > `STAGE2_MAX_NETPNL_USD`

Stage caps:
- Stage 1: max contracts = `STAGE1_MAX_CONTRACTS`, max trades = `STAGE1_MAX_TRADES`
- Stage 2: max contracts = `STAGE2_MAX_CONTRACTS`, max trades = `STAGE2_MAX_TRADES`
- Stage 3: max contracts = `STAGE3_MAX_CONTRACTS`, max trades = `STAGE3_MAX_TRADES`

Optional defense delay:
- If `ENABLE_DEFENSE_DELAY = true`, Stage 3 entries are not allowed before `DEFENSE_DELAY_START` (ET).

Win-rate confirmation for Stage 2 scaling:
- Allow size=2 only if rolling win rate (last `WINRATE_WINDOW_TRADES`) ≥ `WINRATE_SCALE_THRESHOLD`.
- If size=2 is active and consecutive losses reach `SIZE2_MAX_CONSEC_LOSSES`, revert to size=1 for the remainder of the Apex day/session (Risk Engine enforcement).

Hard constraints:
- No averaging down
- No pyramiding into losers
- No martingale or loss-based scaling
- Never exceed `SYSTEM_MAX_CONTRACTS`

---

## 10. Risk Engine Authority (Hard Gate)
The Signal Engine has **no execution authority**.

Before any signal is released to the Execution Adapter, the Risk Engine (TRADE_RULES) must verify:
- Market quality gates (spread, latency)
- Position limits and trade-count limits
- EOD trailing floor proximity buffer
- Apex DLL gate (equity-based)
- Internal circuit breakers:
  - equity-based day PnL circuit breaker (`INTERNAL_MAX_DAILY_LOSS_USD`)
  - consecutive losses
  - statistical freeze
- News blackout windows (Tier-1 events file)
- Daily stop rules (Two-Win stop, Daily Profit cap) when enabled in PARAMS

If any check fails, the signal is discarded.

---

## 11. Logging Requirements (At Decision Time)
At each decision moment (bar close), log:
- Z-score
- RSI value
- Volume ratio
- ATR value
- VWAP value
- Stage (1/2/3) and current caps (size/trades)
- Risk gate decision (approved/denied + reason code)

---

## 12. Non-Goals (Explicit)
The following are prohibited in evaluation mode:
- Adaptive volatility scaling of thresholds
- ML-based prediction
- Randomized behavior
- Any bypass of Risk Engine veto authority
- Any execution “chasing” (market conversion / repricing)