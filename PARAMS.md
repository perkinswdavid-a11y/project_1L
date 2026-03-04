# =========================
# ACCOUNT PROFILE (EOD EVAL)
# =========================
ACCOUNT_PROVIDER = "Apex"
ACCOUNT_SIZE = "50K"
BROKER = "Rithmic"

# Project 1L is built ONLY for EOD evaluation.
EVALUATION_RULESET = "EOD_EVAL"

STARTING_BALANCE_USD = 50000
PROFIT_TARGET_USD = 3000

# EOD trailing drawdown threshold (updates per Apex EOD rules).
MAX_DRAWDOWN_USD = 2000

# Apex EOD Daily Loss Limit (DLL). Monitored on EQUITY (realized + unrealized).
APEX_DAILY_LOSS_LIMIT_USD = 1000

# Internal early-warning buffer to flatten BEFORE hitting the DLL.
APEX_DAILY_LOSS_BUFFER_USD = 150

# Apex-enforced contract limit for the evaluation plan (do not exceed)
APEX_MAX_CONTRACTS = 6

# System goal (Victory lock)
VICTORY_BUFFER_USD = 100
VICTORY_EQUITY_USD = 53100  # STARTING_BALANCE_USD + PROFIT_TARGET_USD + VICTORY_BUFFER_USD


# ===========================================
# TIME, SESSION, AND RESET BOUNDARIES (ET/NY)
# ===========================================
TIMEZONE_TRADING = "America/New_York"

# Strategy session anchor (used for VWAP reset + strategy session logic)
RTH_SESSION_START = "09:30:00"

# Apex "trading day" boundary for evaluation rules that reset daily (DLL, daily counters).
# EOD evaluations reset at 18:00 ET.
APEX_DAY_RESET_TIME = "18:00:00"

# Trading window (no entries outside this window)
TRADING_WINDOW_START = "10:45:00"
TRADING_WINDOW_END = "13:30:00"

# Absolute flat time (must be flat by this time)
HARD_FLATTEN_TIME = "15:55:00"

# Signal evaluation cadence (deterministic)
BAR_TYPE = "TIME"
BAR_INTERVAL_SECONDS = 60
SIGNAL_EVALUATION = "BAR_CLOSE"  # BAR_CLOSE only


# =================================
# INSTRUMENTS + MARKET QUALITY GATE
# =================================
INSTRUMENTS = ["MES", "MNQ"]

# Spread gate (ticks)
MES_MAX_SPREAD_TICKS = 4
MNQ_MAX_SPREAD_TICKS = 10

# Latency gate
MAX_RTT_MS = 150


# ==========================
# ALPHA ENGINE (MEAN REVERT)
# ==========================
VWAP_ANCHOR = "RTH_SESSION"

# Z-score construction
Z_SCORE_PERIOD_BARS = 50
Z_SCORE_THRESHOLD = 2.5

# RSI filter
RSI_PERIOD_BARS = 5
RSI_OVERSOLD = 25
RSI_OVERBOUGHT = 75

# Volume confirmation
VOLUME_SMA_PERIOD_BARS = 20
VOLUME_MULTIPLIER = 1.5

# Volatility for stop sizing
ATR_PERIOD_BARS = 14
STOP_LOSS_ATR_MULTIPLIER = 2.0


# ===================
# EXECUTION PARAMETERS
# ===================
ENTRY_ORDER_TYPE = "LIMIT_AT_TOUCH"
ENTRY_MAX_WAIT_SECONDS = 10
ENTRY_ALLOW_REPRICE = false

# Take profit fallback targets (if VWAP distance is too small)
MES_FIXED_TP_TICKS = 4
MNQ_FIXED_TP_TICKS = 10

# Cooldown between new entries (prevents signal spam)
COOLDOWN_SECONDS = 60


# ==================================
# POSITION LIMITS + CAPITAL PATH RULE
# ==================================
# System-imposed caps (must be <= Apex limits)
SYSTEM_MAX_CONTRACTS = 2
MAX_OPEN_POSITIONS_TOTAL = 1
MAX_OPEN_POSITIONS_PER_INSTRUMENT = 1

# Hard cap for the day (absolute)
HARD_MAX_TRADES_PER_DAY = 3

# Capital staging based on NET PnL relative to STARTING_BALANCE_USD
STAGE1_MAX_NETPNL_USD = 1000
STAGE2_MAX_NETPNL_USD = 2000

# Stage contract caps
STAGE1_MAX_CONTRACTS = 1
STAGE2_MAX_CONTRACTS = 2
STAGE3_MAX_CONTRACTS = 1

# Stage trade caps (MUST be <= HARD_MAX_TRADES_PER_DAY)
STAGE1_MAX_TRADES = 3
STAGE2_MAX_TRADES = 3
STAGE3_MAX_TRADES = 2

# Optional defense-stage delay (disabled by default)
ENABLE_DEFENSE_DELAY = false
DEFENSE_DELAY_START = "11:00:00"

# Stage2 scaling requires winrate confirmation
WINRATE_WINDOW_TRADES = 20
WINRATE_SCALE_THRESHOLD = 0.55

# If trading at size=2 and we take this many consecutive losses, revert to size=1 for session
SIZE2_MAX_CONSEC_LOSSES = 2


# ===========================================
# RISK CONTROLS + DAILY STOP RULES (INTERNAL)
# ===========================================
# IMPORTANT:
# Daily counters MUST reset at APEX_DAY_RESET_TIME (18:00 ET), not RTH open.
# day_pnl must be equity-based:
#   day_pnl = current_equity - day_start_equity
# and day_start_equity is measured at APEX_DAY_RESET_TIME.

# Internal daily loss circuit breaker (buffer before Apex DLL liquidation)
INTERNAL_MAX_DAILY_LOSS_USD = 500

# Trailing floor proximity buffer (EOD trailing)
TRAILING_FLOOR_BUFFER_USD = 200
PROTECTIVE_LOCKOUT_HOURS = 24

# Consecutive loss circuit breaker
CONSECUTIVE_LOSS_LIMIT = 3

# Statistical freeze (regime protection)
WINRATE_FREEZE_THRESHOLD = 0.30
WINRATE_FREEZE_WINDOW_TRADES = 20

# Daily profit stop (evaluation variance control)
ENABLE_DAILY_PROFIT_CAP = true
DAILY_PROFIT_CAP_USD = 300

# Two-win stop rule (evaluation variance control)
ENABLE_TWO_WIN_STOP = true
TWO_WIN_STOP_TRADES = 2
# If true, requires the first N completed trades to be winners (not any two winners later).
TWO_WIN_STOP_ONLY_IF_FIRST_N_TRADES = true


# ==========================
# NEWS / VOLATILITY (TIER-1)
# ==========================
TIER1_BLACKOUT_BEFORE_MIN = 5
TIER1_BLACKOUT_AFTER_MIN = 5

# Operator-maintained schedule for Tier-1 releases (CSV; deterministic local file)
TIER1_EVENTS_FILE = "calendar/tier1_events.csv"
TIER1_EVENTS_MAX_AGE_HOURS = 168  # 7 days


# ============================
# SAFETY, HEARTBEAT, FILE LOCKS
# ============================
HEARTBEAT_INTERVAL_SEC = 5
HEARTBEAT_TIMEOUT_SEC = 15

# Lock files
STOP_TRADING_LOCK = "STOP_TRADING.lock"
VICTORY_LOCK = "VICTORY_ACHIEVED.lock"
PROTECTIVE_LOCK = "PROTECTIVE_LOCK.lock"

# State + signals
STATE_FILE = "state.json"
SIGNAL_TMP_FILE = "signal.tmp"
SIGNAL_FILE = "signal.txt"


# ===============================
# BACKTEST / SIMULATION ASSUMPTIONS
# ===============================
# Slippage assumptions (per side, in ticks) for evaluation realism
BACKTEST_SLIPPAGE_TICKS_MES = 1
BACKTEST_SLIPPAGE_TICKS_MNQ = 2

# Queue position model:
# Limit order fill requires price to trade THROUGH the limit price
BACKTEST_REQUIRE_TRADE_THROUGH_FOR_LIMIT_FILL = true