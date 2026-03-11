from __future__ import annotations

import argparse
import csv
import json
import logging
import math
import statistics
from collections import deque
from dataclasses import dataclass
from datetime import date, datetime, time
from enum import Enum
from pathlib import Path
from typing import Deque, Dict, List, Optional, Sequence, Tuple
from zoneinfo import ZoneInfo

try:
    import duckdb  # type: ignore
except Exception as exc:  # pragma: no cover
    raise SystemExit(
        "duckdb is required for Stage 6. Install it with: python -m pip install duckdb"
    ) from exc


DATE_FMT = "%Y-%m-%d"


@dataclass(frozen=True)
class BarFile:
    trade_date: str
    parquet_path: str


class ExitReason(str, Enum):
    TARGET = "target"
    TIME_STOP = "time_stop"
    INITIAL_STOP = "initial_stop"
    TRAILING_STOP = "trailing_stop"
    COST_PROTECT = "cost_protect"
    STRATEGY_EXIT = "strategy_exit"
    END_OF_SESSION = "end_of_session"
    INSTRUMENT_ROLL = "instrument_roll"
    SIGNAL_REVERSAL = "signal_reversal"
    DAILY_FLATTEN = "daily_flatten"
    FINAL_FLATTEN = "final_flatten"


@dataclass(frozen=True)
class Bar:
    family: str
    yyyymmdd: str
    instrument_key: str
    bar_ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    trade_count: int


@dataclass(frozen=True)
class Execution:
    ts: str
    family: str
    instrument_key: str
    action: str
    str
    action: str
    qty_delta: int
    fill_price: float
    reference_price: float
    commission: float
    slippage_cost: float
    position_after: int
    reason: str


@dataclass(frozen=True)
class ClosedTrade:
    entry_ts: str
    exit_ts: str
    family: str
    instrument_key: str
    side: str
    qty: int
    entry_price: float
    exit_price: float
    gross_pnl: float
    commission: float
    slippage_cost: float
    net_pnl: float
    mae_points: Optional[float] = None
    mfe_points: Optional[float] = None
    mae_r: Optional[float] = None
    mfe_r: Optional[float] = None
    exit_reason: Optional[str] = None
    initial_stop_price: Optional[float] = None
    initial_target_price: Optional[float] = None
    entry_trigger_price: Optional[float] = None
    bars_held: Optional[int] = None


@dataclass(frozen=True)
class DailyEquityRow:
    trade_date: str
    family: str
    instrument_key: str
    bars_in_session: int
    equity_close: float
    pnl_day: float
    position_close: int


def _parse_time_hhmm(text: str) -> time:
    hh, mm = str(text).strip().split(":", 1)
    return time(hour=int(hh), minute=int(mm))


def _bar_local_time(bar: Bar, tz: ZoneInfo) -> time:
    return bar.bar_ts.astimezone(tz).timetz().replace(tzinfo=None)


def _minutes_since_midnight(value: time) -> int:
    return value.hour * 60 + value.minute


class Strategy:
    exit_reason: Optional[ExitReason] = None

    def on_bar(self, bar: Bar, current_position: int) -> int:
        raise NotImplementedError


class SmaCrossStrategy(Strategy):
    def __init__(
        self,
        fast: int = 20,
        slow: int = 50,
        allow_short: bool = True,
        position_size: int = 1,
    ) -> None:
        if fast <= 0 or slow <= 0 or fast >= slow:
            raise ValueError("SMA strategy requires 0 < fast < slow.")
        self.fast = int(fast)
        self.slow = int(slow)
        self.allow_short = bool(allow_short)
        self.position_size = int(position_size)

        self._fast_window: Deque[float] = deque(maxlen=self.fast)
        self._slow_window: Deque[float] = deque(maxlen=self.slow)
        self._fast_sum = 0.0
        self._slow_sum = 0.0

    def _append_close(self, price: float) -> None:
        if len(self._fast_window) == self.fast:
            self._fast_sum -= self._fast_window[0]
        self._fast_window.append(price)
        self._fast_sum += price

        if len(self._slow_window) == self.slow:
            self._slow_sum -= self._slow_window[0]
        self._slow_window.append(price)
        self._slow_sum += price

    def on_bar(self, bar: Bar, current_position: int) -> int:
        self._append_close(float(bar.close))
        if len(self._slow_window) < self.slow:
            return current_position

        fast_ma = self._fast_sum / len(self._fast_window)
        slow_ma = self._slow_sum / len(self._slow_window)

        if fast_ma > slow_ma:
            return self.position_size
        if fast_ma < slow_ma:
            return -self.position_size if self.allow_short else 0
        return current_position


class VWAPReversionStrategy(Strategy):
    def __init__(
        self,
        deviation_ticks: float = 12.0,
        exit_band_ticks: float = 2.0,
        min_bars_before_entry: int = 30,
        position_size: int = 1,
        tick_size: float = 0.25,
        session_start: str = "08:30",
        no_new_entries_after: str = "14:30",
        allow_long: bool = True,
        allow_short: bool = True,
        timezone: str = "America/Chicago",
    ) -> None:
        self.deviation_ticks = float(deviation_ticks)
        self.exit_band_ticks = float(exit_band_ticks)
        self.min_bars_before_entry = int(min_bars_before_entry)
        self.position_size = int(position_size)
        self.tick_size = float(tick_size)
        self.session_start = _parse_time_hhmm(session_start)
        self.no_new_entries_after = _parse_time_hhmm(no_new_entries_after)
        self.allow_long = bool(allow_long)
        self.allow_short = bool(allow_short)
        self.tz = ZoneInfo(timezone)

        self.current_day: Optional[str] = None
        self.cum_pv = 0.0
        self.cum_vol = 0.0
        self.bars_today = 0

    def _reset_day(self) -> None:
        self.cum_pv = 0.0
        self.cum_vol = 0.0
        self.bars_today = 0

    def on_bar(self, bar: Bar, current_position: int) -> int:
        if bar.yyyymmdd != self.current_day:
            self.current_day = bar.yyyymmdd
            self._reset_day()

        local_time = _bar_local_time(bar, self.tz)
        if local_time < self.session_start:
            return current_position

        vol = float(bar.volume) if float(bar.volume) > 0 else 1.0
        self.cum_pv += float(bar.close) * vol
        self.cum_vol += vol
        self.bars_today += 1

        if self.cum_vol <= 0:
            return current_position

        vwap = self.cum_pv / self.cum_vol
        entry_dist = self.deviation_ticks * self.tick_size
        exit_dist = self.exit_band_ticks * self.tick_size
        price = float(bar.close)

        if current_position > 0 and price >= vwap - exit_dist:
            return 0
        if current_position < 0 and price <= vwap + exit_dist:
            return 0

        if self.bars_today < self.min_bars_before_entry:
            return current_position
        if local_time >= self.no_new_entries_after:
            return current_position

        if current_position == 0:
            if self.allow_short and price >= vwap + entry_dist:
                return -self.position_size
            if self.allow_long and price <= vwap - entry_dist:
                return self.position_size

        return current_position


class OpeningRangeBreakoutStrategy(Strategy):
    def __init__(
        self,
        range_minutes: int = 15,
        buffer_ticks: float = 1.0,
        position_size: int = 1,
        tick_size: float = 0.25,
        session_open: str = "08:30",
        no_new_entries_after: str = "11:00",
        allow_long: bool = True,
        allow_short: bool = True,
        timezone: str = "America/Chicago",
    ) -> None:
        if range_minutes <= 0:
            raise ValueError("range_minutes must be > 0.")
        self.range_minutes = int(range_minutes)
        self.buffer_ticks = float(buffer_ticks)
        self.position_size = int(position_size)
        self.tick_size = float(tick_size)
        self.session_open = _parse_time_hhmm(session_open)
        self.no_new_entries_after = _parse_time_hhmm(no_new_entries_after)
        self.allow_long = bool(allow_long)
        self.allow_short = bool(allow_short)
        self.tz = ZoneInfo(timezone)

        self.current_day: Optional[str] = None
        self.orb_high: Optional[float] = None
        self.orb_low: Optional[float] = None
        self.traded_today = False

    def _reset_day(self) -> None:
        self.orb_high = None
        self.orb_low = None
        self.traded_today = False

    def on_bar(self, bar: Bar, current_position: int) -> int:
        if bar.yyyymmdd != self.current_day:
            self.current_day = bar.yyyymmdd
            self._reset_day()

        local_time = _bar_local_time(bar, self.tz)
        local_minutes = _minutes_since_midnight(local_time)
        open_minutes = _minutes_since_midnight(self.session_open)
        entry_cutoff = _minutes_since_midnight(self.no_new_entries_after)

        if local_minutes < open_minutes:
            return current_position

        in_range_window = open_minutes <= local_minutes < (open_minutes + self.range_minutes)
        if in_range_window:
            high = float(bar.high)
            low = float(bar.low)
            self.orb_high = high if self.orb_high is None else max(self.orb_high, high)
            self.orb_low = low if self.orb_low is None else min(self.orb_low, low)
            return current_position

        if self.orb_high is None or self.orb_low is None:
            return current_position

        buffer_amt = self.buffer_ticks * self.tick_size
        price = float(bar.close)

        if current_position > 0 and price < self.orb_high:
            return 0
        if current_position < 0 and price > self.orb_low:
            return 0

        if current_position == 0 and (not self.traded_today) and local_minutes < entry_cutoff:
            if self.allow_long and price > self.orb_high + buffer_amt:
                self.traded_today = True
                return self.position_size
            if self.allow_short and price < self.orb_low - buffer_amt:
                self.traded_today = True
                return -self.position_size

        return current_position


class MomentumPullbackStrategy(Strategy):
    def __init__(
        self,
        fast: int = 20,
        slow: int = 50,
        entry_buffer_ticks: float = 1.0,
        position_size: int = 1,
        tick_size: float = 0.25,
        allow_short: bool = True,
    ) -> None:
        if fast <= 0 or slow <= 0 or fast >= slow:
            raise ValueError("Momentum pullback requires 0 < fast < slow.")
        self.fast = int(fast)
        self.slow = int(slow)
        self.entry_buffer_ticks = float(entry_buffer_ticks)
        self.position_size = int(position_size)
        self.tick_size = float(tick_size)
        self.allow_short = bool(allow_short)

        self._fast_window: Deque[float] = deque(maxlen=self.fast)
        self._slow_window: Deque[float] = deque(maxlen=self.slow)
        self._fast_sum = 0.0
        self._slow_sum = 0.0

    def _append_close(self, price: float) -> None:
        if len(self._fast_window) == self.fast:
            self._fast_sum -= self._fast_window[0]
        self._fast_window.append(price)
        self._fast_sum += price

        if len(self._slow_window) == self.slow:
            self._slow_sum -= self._slow_window[0]
        self._slow_window.append(price)
        self._slow_sum += price

    def on_bar(self, bar: Bar, current_position: int) -> int:
        price = float(bar.close)
        self._append_close(price)

        if len(self._slow_window) < self.slow:
            return current_position

        fast_ma = self._fast_sum / len(self._fast_window)
        slow_ma = self._slow_sum / len(self._slow_window)
        buffer_amt = self.entry_buffer_ticks * self.tick_size

        if current_position > 0 and price < slow_ma:
            return 0
        if current_position < 0 and price > slow_ma:
            return 0

        if current_position == 0:
            if fast_ma > slow_ma and price <= fast_ma + buffer_amt and price > slow_ma:
                return self.position_size
            if self.allow_short and fast_ma < slow_ma and price >= fast_ma - buffer_amt and price < slow_ma:
                return -self.position_size

        return current_position


class OpeningRangeBreakoutV2Strategy(Strategy):
    def __init__(
        self,
        range_minutes: int = 15,
        entry_buffer_ticks: float = 1.0,
        stop_buffer_ticks: float = 1.0,
        position_size: int = 1,
        tick_size: float = 0.25,
        session_open: str = "08:30",
        no_new_entries_after: str = "11:00",
        time_stop: str = "13:30",
        allow_long: bool = True,
        timezone: str = "America/Chicago",
        or_width_lookback_days: int = 20,
        or_width_min_factor: float = 0.5,
        or_width_max_factor: float = 2.0,
        cost_protect_trigger_r: float = 1.25,
        trail_activate_r: float = 2.0,
        atr_period: int = 20,
        atr_trail_multiple: float = 3.0,
        slippage_ticks: float = 1.0,
        commission_per_side: float = 1.25,
        contract_multiplier: float = 5.0,
        breakout_bar_close_location_min: Optional[float] = None,
        require_signal_bar_close_at_or_above_trigger: bool = False,
        breakout_bar_body_fraction_min: Optional[float] = None,
        signal_bar_extension_from_trigger_max: Optional[float] = None,
        max_signal_bars_after_or_completion: Optional[int] = None,
        enable_first_post_entry_close_below_trigger_exit: bool = False,
    ) -> None:
        if range_minutes <= 0:
            raise ValueError("range_minutes must be > 0.")
        if position_size <= 0:
            raise ValueError("position_size must be > 0.")
        if atr_period <= 0:
            raise ValueError("atr_period must be > 0.")
        if or_width_lookback_days <= 0:
            raise ValueError("or_width_lookback_days must be > 0.")
        if stop_buffer_ticks < 0 or entry_buffer_ticks < 0:
            raise ValueError("entry_buffer_ticks and stop_buffer_ticks must be >= 0.")
        if or_width_min_factor <= 0 or or_width_max_factor <= 0:
            raise ValueError("OR width factors must be > 0.")
        if or_width_min_factor >= or_width_max_factor:
            raise ValueError("or_width_min_factor must be < or_width_max_factor.")

        self.range_minutes = int(range_minutes)
        self.entry_buffer_ticks = float(entry_buffer_ticks)
        self.stop_buffer_ticks = float(stop_buffer_ticks)
        self.position_size = int(position_size)
        self.tick_size = float(tick_size)
        self.session_open = _parse_time_hhmm(session_open)
        self.no_new_entries_after = _parse_time_hhmm(no_new_entries_after)
        self.time_stop = _parse_time_hhmm(time_stop)
        self.allow_long = bool(allow_long)
        self.tz = ZoneInfo(timezone)

        self.or_width_lookback_days = int(or_width_lookback_days)
        self.or_width_min_factor = float(or_width_min_factor)
        self.or_width_max_factor = float(or_width_max_factor)
        self.cost_protect_trigger_r = float(cost_protect_trigger_r)
        self.trail_activate_r = float(trail_activate_r)
        self.atr_period = int(atr_period)
        self.atr_trail_multiple = float(atr_trail_multiple)

        self.slippage_ticks = float(slippage_ticks)
        self.commission_per_side = float(commission_per_side)
        self.contract_multiplier = float(contract_multiplier)
        self.breakout_bar_close_location_min = (
            float(breakout_bar_close_location_min) 
            if breakout_bar_close_location_min is not None 
            else None
        )
        self.require_signal_bar_close_at_or_above_trigger = bool(require_signal_bar_close_at_or_above_trigger)
        self.breakout_bar_body_fraction_min = (
            float(breakout_bar_body_fraction_min)
            if breakout_bar_body_fraction_min is not None
            else None
        )
        self.signal_bar_extension_from_trigger_max = (
            float(signal_bar_extension_from_trigger_max)
            if signal_bar_extension_from_trigger_max is not None
            else None
        )
        self.max_signal_bars_after_or_completion = (
            int(max_signal_bars_after_or_completion)
            if max_signal_bars_after_or_completion is not None
            else None
        )
        self.enable_first_post_entry_close_below_trigger_exit = bool(enable_first_post_entry_close_below_trigger_exit)
        self.cost_buffer_points = (
            2.0 * self.slippage_ticks * self.tick_size
        ) + (
            2.0 * self.commission_per_side / self.contract_multiplier
            if self.contract_multiplier != 0
            else 0.0
        )

        self.current_day: Optional[str] = None
        self.or_high: Optional[float] = None
        self.or_low: Optional[float] = None
        self.current_day_or_width: Optional[float] = None
        self.prior_or_widths: Deque[float] = deque(maxlen=self.or_width_lookback_days)
        self.traded_today = False
        self.bars_since_or_completed = 0

        self.pending_long_entry = False
        self.entry_price: Optional[float] = None
        self.initial_stop: Optional[float] = None
        self.active_stop: Optional[float] = None
        self.risk_per_contract: Optional[float] = None
        self.best_high_since_entry: Optional[float] = None
        self.highest_close_since_entry: Optional[float] = None
        self.cost_protected = False
        self.trail_active = False
        self.original_entry_trigger: Optional[float] = None
        self.first_post_entry_bar_checked = False

        self.prev_close_for_atr: Optional[float] = None
        self._tr_window: Deque[float] = deque(maxlen=self.atr_period)
        self._tr_sum = 0.0

    def _clear_trade_state(self) -> None:
        self.pending_long_entry = False
        self.entry_price = None
        self.initial_stop = None
        self.active_stop = None
        self.risk_per_contract = None
        self.best_high_since_entry = None
        self.highest_close_since_entry = None
        self.cost_protected = False
        self.trail_active = False
        self.original_entry_trigger = None
        self.first_post_entry_bar_checked = False

    def _roll_day(self, new_day: str) -> None:
        if self.current_day is not None and self.current_day_or_width is not None and self.current_day_or_width > 0:
            self.prior_or_widths.append(self.current_day_or_width)

        self.current_day = new_day
        self.or_high = None
        self.or_low = None
        self.current_day_or_width = None
        self.traded_today = False
        self.bars_since_or_completed = 0
        self._clear_trade_state()
        self.prev_close_for_atr = None
        self._tr_window.clear()
        self._tr_sum = 0.0

    def _append_true_range(self, bar: Bar) -> None:
        high = float(bar.high)
        low = float(bar.low)
        if self.prev_close_for_atr is None:
            tr = high - low
        else:
            prev_close = self.prev_close_for_atr
            tr = max(high - low, abs(high - prev_close), abs(low - prev_close))

        if len(self._tr_window) == self.atr_period:
            self._tr_sum -= self._tr_window[0]
        self._tr_window.append(tr)
        self._tr_sum += tr
        self.prev_close_for_atr = float(bar.close)

    def _current_atr(self) -> Optional[float]:
        if len(self._tr_window) < self.atr_period:
            return None
        return self._tr_sum / len(self._tr_window)

    def _or_filter_passes(self) -> bool:
        if self.current_day_or_width is None:
            return False
        if len(self.prior_or_widths) < self.or_width_lookback_days:
            return False
        median_or_width = statistics.median(self.prior_or_widths)
        if median_or_width <= 0:
            return False
        return (
            self.current_day_or_width >= self.or_width_min_factor * median_or_width
            and self.current_day_or_width <= self.or_width_max_factor * median_or_width
        )

    def _initialize_filled_long(self, bar: Bar) -> None:
        if self.or_low is None:
            raise ValueError("ORB-v2 attempted to initialize a long without OR_low.")
        self.pending_long_entry = False
        self.entry_price = float(bar.open) + (self.slippage_ticks * self.tick_size)
        self.initial_stop = self.or_low - (self.stop_buffer_ticks * self.tick_size)
        risk = self.entry_price - self.initial_stop
        self.risk_per_contract = risk if risk > 0 else self.tick_size
        self.active_stop = self.initial_stop
        self.best_high_since_entry = float(bar.high)
        self.highest_close_since_entry = float(bar.close)
        self.cost_protected = False
        self.trail_active = False
        self.first_post_entry_bar_checked = False

    def on_bar(self, bar: Bar, current_position: int) -> int:
        if bar.yyyymmdd != self.current_day:
            self._roll_day(bar.yyyymmdd)

        local_time = _bar_local_time(bar, self.tz)
        if local_time < self.session_open:
            return current_position

        local_minutes = _minutes_since_midnight(local_time)
        open_minutes = _minutes_since_midnight(self.session_open)
        price = float(bar.close)

        self._append_true_range(bar)

        if current_position == 0 and self.entry_price is not None:
            self._clear_trade_state()

        if current_position > 0 and self.pending_long_entry:
            self._initialize_filled_long(bar)

        in_range_window = open_minutes <= local_minutes < (open_minutes + self.range_minutes)
        if in_range_window:
            high = float(bar.high)
            low = float(bar.low)
            self.or_high = high if self.or_high is None else max(self.or_high, high)
            self.or_low = low if self.or_low is None else min(self.or_low, low)
            self.current_day_or_width = (
                (self.or_high - self.or_low)
                if self.or_high is not None and self.or_low is not None
                else None
            )
            return current_position

        if self.or_high is None or self.or_low is None:
            return current_position

        if self.current_day_or_width is None:
            self.current_day_or_width = self.or_high - self.or_low

        self.bars_since_or_completed += 1

        if current_position > 0:
            high = float(bar.high)
            self.best_high_since_entry = high if self.best_high_since_entry is None else max(self.best_high_since_entry, high)
            self.highest_close_since_entry = (
                price if self.highest_close_since_entry is None else max(self.highest_close_since_entry, price)
            )

            if (
                self.entry_price is not None
                and self.risk_per_contract is not None
                and self.active_stop is not None
                and self.best_high_since_entry is not None
            ):
                if (
                    not self.cost_protected
                    and self.best_high_since_entry >= self.entry_price + (self.cost_protect_trigger_r * self.risk_per_contract)
                ):
                    self.active_stop = max(self.active_stop, self.entry_price + self.cost_buffer_points)
                    self.cost_protected = True

                if self.best_high_since_entry >= self.entry_price + (self.trail_activate_r * self.risk_per_contract):
                    atr_value = self._current_atr()
                    if atr_value is not None and self.highest_close_since_entry is not None:
                        trail_stop = self.highest_close_since_entry - (self.atr_trail_multiple * atr_value)
                        self.active_stop = max(self.active_stop, trail_stop)
                        self.trail_active = True

            if self.active_stop is not None and price <= self.active_stop:
                return 0
            if local_time >= self.time_stop:
                return 0
            return current_position

        if not self.allow_long:
            return current_position
        if self.traded_today:
            return current_position
        if not self._or_filter_passes():
            return current_position
        if local_time >= self.no_new_entries_after:
            return current_position

        entry_trigger = self.or_high + (self.entry_buffer_ticks * self.tick_size)
        if price > entry_trigger:
            if self.breakout_bar_close_location_min is not None:
                b_high = float(bar.high)
                b_low = float(bar.low)
                if b_high <= b_low:
                    return current_position
                close_loc = (price - b_low) / (b_high - b_low)
                if close_loc < self.breakout_bar_close_location_min:
                    return current_position

            if self.breakout_bar_body_fraction_min is not None:
                b_high = float(bar.high)
                b_low = float(bar.low)
                if b_high <= b_low:
                    return current_position
                b_open = float(bar.open)
                b_close = float(bar.close)
                body_fraction = (b_close - b_open) / (b_high - b_low)
                if body_fraction < self.breakout_bar_body_fraction_min:
                    return current_position

            if self.require_signal_bar_close_at_or_above_trigger:
                if price < entry_trigger:
                    return current_position

            if self.signal_bar_extension_from_trigger_max is not None:
                if self.current_day_or_width is None or self.current_day_or_width <= 0:
                    return current_position
                extension_from_trigger = (price - entry_trigger) / self.current_day_or_width
                if extension_from_trigger > self.signal_bar_extension_from_trigger_max:
                    return current_position

            if self.max_signal_bars_after_or_completion is not None:
                if self.bars_since_or_completed > self.max_signal_bars_after_or_completion:
                    return current_position

            self.traded_today = True
            self.pending_long_entry = True
            self.original_entry_trigger = entry_trigger
            return self.position_size

        return current_position


class OpeningRangeBreakoutV4Strategy(OpeningRangeBreakoutV2Strategy):
    def __init__(
        self,
        range_minutes: int = 15,
        entry_buffer_ticks: float = 1.0,
        stop_buffer_ticks: float = 1.0,
        position_size: int = 1,
        tick_size: float = 0.25,
        session_open: str = "08:30",
        no_new_entries_after: str = "11:00",
        time_stop: str = "13:30",
        allow_long: bool = True,
        timezone: str = "America/Chicago",
        or_width_lookback_days: int = 20,
        or_width_min_factor: float = 0.5,
        or_width_max_factor: float = 2.0,
        cost_protect_trigger_r: float = 1.25,
        trail_activate_r: float = 2.0,
        atr_period: int = 20,
        atr_trail_multiple: float = 3.0,
        slippage_ticks: float = 1.0,
        commission_per_side: float = 1.25,
        contract_multiplier: float = 5.0,
        vwap_filter_mode: str = "signal_close_above_vwap",
    ) -> None:
        super().__init__(
            range_minutes=range_minutes,
            entry_buffer_ticks=entry_buffer_ticks,
            stop_buffer_ticks=stop_buffer_ticks,
            position_size=position_size,
            tick_size=tick_size,
            session_open=session_open,
            no_new_entries_after=no_new_entries_after,
            time_stop=time_stop,
            allow_long=allow_long,
            timezone=timezone,
            or_width_lookback_days=or_width_lookback_days,
            or_width_min_factor=or_width_min_factor,
            or_width_max_factor=or_width_max_factor,
            cost_protect_trigger_r=cost_protect_trigger_r,
            trail_activate_r=trail_activate_r,
            atr_period=atr_period,
            atr_trail_multiple=atr_trail_multiple,
            slippage_ticks=slippage_ticks,
            commission_per_side=commission_per_side,
            contract_multiplier=contract_multiplier,
        )

        mode = str(vwap_filter_mode).strip().lower()
        if mode not in {"none", "signal_close_above_vwap", "or_close_above_vwap"}:
            raise ValueError(
                "vwap_filter_mode must be one of 'none', 'signal_close_above_vwap', or 'or_close_above_vwap'."
            )

        self.vwap_filter_mode = mode
        self.cum_pv = 0.0
        self.cum_vol = 0.0
        self.or_close: Optional[float] = None
        self.vwap_at_or_close: Optional[float] = None

    def _roll_day(self, new_day: str) -> None:
        super()._roll_day(new_day)
        self.cum_pv = 0.0
        self.cum_vol = 0.0
        self.or_close = None
        self.vwap_at_or_close = None

    def _append_session_vwap(self, bar: Bar) -> None:
        volume = max(float(bar.volume), 0.0)
        if volume <= 0:
            return
        price = float(bar.close)
        self.cum_pv += price * volume
        self.cum_vol += volume

    def _current_session_vwap(self) -> Optional[float]:
        if self.cum_vol <= 0:
            return None
        return self.cum_pv / self.cum_vol

    def _vwap_filter_passes(self, signal_close: float) -> bool:
        if self.vwap_filter_mode == "none":
            return True

        if self.vwap_filter_mode == "signal_close_above_vwap":
            session_vwap = self._current_session_vwap()
            if session_vwap is None:
                return False
            return signal_close > session_vwap

        if self.vwap_filter_mode == "or_close_above_vwap":
            if self.or_close is None or self.vwap_at_or_close is None:
                return False
            return self.or_close > self.vwap_at_or_close

        return True

    def on_bar(self, bar: Bar, current_position: int) -> int:
        if bar.yyyymmdd != self.current_day:
            self._roll_day(bar.yyyymmdd)

        local_time = _bar_local_time(bar, self.tz)
        if local_time < self.session_open:
            return current_position

        local_minutes = _minutes_since_midnight(local_time)
        open_minutes = _minutes_since_midnight(self.session_open)
        price = float(bar.close)

        self._append_true_range(bar)
        self._append_session_vwap(bar)

        if current_position == 0 and self.entry_price is not None:
            self._clear_trade_state()

        if current_position > 0 and self.pending_long_entry:
            self._initialize_filled_long(bar)

        in_range_window = open_minutes <= local_minutes < (open_minutes + self.range_minutes)
        if in_range_window:
            high = float(bar.high)
            low = float(bar.low)
            self.or_high = high if self.or_high is None else max(self.or_high, high)
            self.or_low = low if self.or_low is None else min(self.or_low, low)
            self.or_close = price
            self.vwap_at_or_close = self._current_session_vwap()
            self.current_day_or_width = (
                (self.or_high - self.or_low)
                if self.or_high is not None and self.or_low is not None
                else None
            )
            return current_position

        if self.or_high is None or self.or_low is None:
            return current_position

        if self.current_day_or_width is None:
            self.current_day_or_width = self.or_high - self.or_low

        if current_position > 0:
            high = float(bar.high)
            self.best_high_since_entry = high if self.best_high_since_entry is None else max(self.best_high_since_entry, high)
            self.highest_close_since_entry = (
                price if self.highest_close_since_entry is None else max(self.highest_close_since_entry, price)
            )

            if (
                self.entry_price is not None
                and self.risk_per_contract is not None
                and self.active_stop is not None
                and self.best_high_since_entry is not None
            ):
                if (
                    not self.cost_protected
                    and self.best_high_since_entry >= self.entry_price + (self.cost_protect_trigger_r * self.risk_per_contract)
                ):
                    self.active_stop = max(self.active_stop, self.entry_price + self.cost_buffer_points)
                    self.cost_protected = True

                if self.best_high_since_entry >= self.entry_price + (self.trail_activate_r * self.risk_per_contract):
                    atr_value = self._current_atr()
                    if atr_value is not None and self.highest_close_since_entry is not None:
                        trail_stop = self.highest_close_since_entry - (self.atr_trail_multiple * atr_value)
                        self.active_stop = max(self.active_stop, trail_stop)
                        self.trail_active = True

            if self.active_stop is not None and price <= self.active_stop:
                return 0
            if local_time >= self.time_stop:
                return 0
            return current_position

        if not self.allow_long:
            return current_position
        if self.traded_today:
            return current_position
        if not self._or_filter_passes():
            return current_position
        if not self._vwap_filter_passes(price):
            return current_position
        if local_time >= self.no_new_entries_after:
            return current_position

        entry_trigger = self.or_high + (self.entry_buffer_ticks * self.tick_size)
        if price > entry_trigger:
            self.traded_today = True
            self.pending_long_entry = True
            return self.position_size

        return current_position


class OpeningRangeBreakoutV5AStrategy(OpeningRangeBreakoutV2Strategy):
    def __init__(
        self,
        range_minutes: int = 15,
        entry_buffer_ticks: float = 1.0,
        stop_buffer_ticks: float = 1.0,
        position_size: int = 1,
        tick_size: float = 0.25,
        session_open: str = "08:30",
        no_new_entries_after: str = "11:00",
        time_stop: str = "13:30",
        allow_long: bool = True,
        timezone: str = "America/Chicago",
        or_width_lookback_days: int = 20,
        or_width_min_factor: float = 0.80,
        or_width_max_factor: float = 1.60,
        cost_protect_trigger_r: float = 1.25,
        trail_activate_r: float = 2.0,
        atr_period: int = 20,
        atr_trail_multiple: float = 3.0,
        slippage_ticks: float = 1.0,
        commission_per_side: float = 1.25,
        contract_multiplier: float = 5.0,
        or_close_location_min: float = 0.70,
    ) -> None:
        super().__init__(
            range_minutes=range_minutes,
            entry_buffer_ticks=entry_buffer_ticks,
            stop_buffer_ticks=stop_buffer_ticks,
            position_size=position_size,
            tick_size=tick_size,
            session_open=session_open,
            no_new_entries_after=no_new_entries_after,
            time_stop=time_stop,
            allow_long=allow_long,
            timezone=timezone,
            or_width_lookback_days=or_width_lookback_days,
            or_width_min_factor=or_width_min_factor,
            or_width_max_factor=or_width_max_factor,
            cost_protect_trigger_r=cost_protect_trigger_r,
            trail_activate_r=trail_activate_r,
            atr_period=atr_period,
            atr_trail_multiple=atr_trail_multiple,
            slippage_ticks=slippage_ticks,
            commission_per_side=commission_per_side,
            contract_multiplier=contract_multiplier,
        )
        self.or_close_location_min = float(or_close_location_min)
        self.or_close: Optional[float] = None

    def _roll_day(self, new_day: str) -> None:
        super()._roll_day(new_day)
        self.or_close = None

    def on_bar(self, bar: Bar, current_position: int) -> int:
        result = super().on_bar(bar, current_position)

        local_time = _bar_local_time(bar, self.tz)
        local_minutes = _minutes_since_midnight(local_time)
        open_minutes = _minutes_since_midnight(self.session_open)

        in_range_window = open_minutes <= local_minutes < (open_minutes + self.range_minutes)
        if in_range_window:
            self.or_close = float(bar.close)

        return result

    def _or_filter_passes(self) -> bool:
        if not super()._or_filter_passes():
            return False

        if self.or_close is None or self.or_high is None or self.or_low is None:
            return False

        or_height = self.or_high - self.or_low
        if or_height <= 0:
            return False

        or_close_location = (self.or_close - self.or_low) / or_height
        if or_close_location < self.or_close_location_min:
            return False

        return True


class OpeningRangeBreakoutV5BStrategy(OpeningRangeBreakoutV2Strategy):
    def __init__(
        self,
        range_minutes: int = 15,
        entry_buffer_ticks: float = 1.0,
        stop_buffer_ticks: float = 1.0,
        position_size: int = 1,
        tick_size: float = 0.25,
        session_open: str = "08:30",
        no_new_entries_after: str = "11:00",
        time_stop: str = "13:30",
        allow_long: bool = True,
        timezone: str = "America/Chicago",
        or_width_lookback_days: int = 20,
        or_width_min_factor: float = 0.5,
        or_width_max_factor: float = 2.0,
        cost_protect_trigger_r: float = 1.25,
        trail_activate_r: float = 2.0,
        atr_period: int = 20,
        atr_trail_multiple: float = 3.0,
        slippage_ticks: float = 1.0,
        commission_per_side: float = 1.25,
        contract_multiplier: float = 5.0,
        or_close_location_min: float = 0.70,
    ) -> None:
        super().__init__(
            range_minutes=range_minutes,
            entry_buffer_ticks=entry_buffer_ticks,
            stop_buffer_ticks=stop_buffer_ticks,
            position_size=position_size,
            tick_size=tick_size,
            session_open=session_open,
            no_new_entries_after=no_new_entries_after,
            time_stop=time_stop,
            allow_long=allow_long,
            timezone=timezone,
            or_width_lookback_days=or_width_lookback_days,
            or_width_min_factor=or_width_min_factor,
            or_width_max_factor=or_width_max_factor,
            cost_protect_trigger_r=cost_protect_trigger_r,
            trail_activate_r=trail_activate_r,
            atr_period=atr_period,
            atr_trail_multiple=atr_trail_multiple,
            slippage_ticks=slippage_ticks,
            commission_per_side=commission_per_side,
            contract_multiplier=contract_multiplier,
        )
        self.or_close_location_min = float(or_close_location_min)
        self.or_close: Optional[float] = None

    def _roll_day(self, new_day: str) -> None:
        super()._roll_day(new_day)
        self.or_close = None

    def on_bar(self, bar: Bar, current_position: int) -> int:
        result = super().on_bar(bar, current_position)

        local_time = _bar_local_time(bar, self.tz)
        local_minutes = _minutes_since_midnight(local_time)
        open_minutes = _minutes_since_midnight(self.session_open)

        in_range_window = open_minutes <= local_minutes < (open_minutes + self.range_minutes)
        if in_range_window:
            self.or_close = float(bar.close)

        return result

    def _or_filter_passes(self) -> bool:
        if not super()._or_filter_passes():
            return False

        if self.or_close is None or self.or_high is None or self.or_low is None:
            return False

        or_height = self.or_high - self.or_low
        if or_height <= 0:
            return False

        or_close_location = (self.or_close - self.or_low) / or_height
        if or_close_location < self.or_close_location_min:
            return False

        return True


class OpeningRangeBreakoutV6AStrategy(OpeningRangeBreakoutV2Strategy):
    def __init__(
        self,
        range_minutes: int = 15,
        entry_buffer_ticks: float = 1.0,
        stop_buffer_ticks: float = 1.0,
        position_size: int = 1,
        tick_size: float = 0.25,
        session_open: str = "08:30",
        no_new_entries_after: str = "11:00",
        time_stop: str = "13:30",
        allow_long: bool = True,
        timezone: str = "America/Chicago",
        or_width_lookback_days: int = 20,
        or_width_min_factor: float = 0.5,
        or_width_max_factor: float = 2.0,
        cost_protect_trigger_r: float = 1.25,
        trail_activate_r: float = 2.0,
        atr_period: int = 20,
        atr_trail_multiple: float = 3.0,
        slippage_ticks: float = 1.0,
        commission_per_side: float = 1.25,
        contract_multiplier: float = 5.0,
        breakout_bar_close_location_min: float = 0.70,
    ) -> None:
        super().__init__(
            range_minutes=range_minutes,
            entry_buffer_ticks=entry_buffer_ticks,
            stop_buffer_ticks=stop_buffer_ticks,
            position_size=position_size,
            tick_size=tick_size,
            session_open=session_open,
            no_new_entries_after=no_new_entries_after,
            time_stop=time_stop,
            allow_long=allow_long,
            timezone=timezone,
            or_width_lookback_days=or_width_lookback_days,
            or_width_min_factor=or_width_min_factor,
            or_width_max_factor=or_width_max_factor,
            cost_protect_trigger_r=cost_protect_trigger_r,
            trail_activate_r=trail_activate_r,
            atr_period=atr_period,
            atr_trail_multiple=atr_trail_multiple,
            slippage_ticks=slippage_ticks,
            commission_per_side=commission_per_side,
            contract_multiplier=contract_multiplier,
            breakout_bar_close_location_min=breakout_bar_close_location_min,
        )


class OpeningRangeBreakoutV7AStrategy(OpeningRangeBreakoutV2Strategy):
    def __init__(
        self,
        range_minutes: int = 15,
        entry_buffer_ticks: float = 1.0,
        stop_buffer_ticks: float = 1.0,
        position_size: int = 1,
        tick_size: float = 0.25,
        session_open: str = "08:30",
        no_new_entries_after: str = "11:00",
        time_stop: str = "13:30",
        allow_long: bool = True,
        timezone: str = "America/Chicago",
        or_width_lookback_days: int = 20,
        or_width_min_factor: float = 0.5,
        or_width_max_factor: float = 2.0,
        cost_protect_trigger_r: float = 1.25,
        trail_activate_r: float = 2.0,
        atr_period: int = 20,
        atr_trail_multiple: float = 3.0,
        slippage_ticks: float = 1.0,
        commission_per_side: float = 1.25,
        contract_multiplier: float = 5.0,
        breakout_bar_close_location_min: float = 0.70,
        require_signal_bar_close_at_or_above_trigger: bool = True,
    ) -> None:
        super().__init__(
            range_minutes=range_minutes,
            entry_buffer_ticks=entry_buffer_ticks,
            stop_buffer_ticks=stop_buffer_ticks,
            position_size=position_size,
            tick_size=tick_size,
            session_open=session_open,
            no_new_entries_after=no_new_entries_after,
            time_stop=time_stop,
            allow_long=allow_long,
            timezone=timezone,
            or_width_lookback_days=or_width_lookback_days,
            or_width_min_factor=or_width_min_factor,
            or_width_max_factor=or_width_max_factor,
            cost_protect_trigger_r=cost_protect_trigger_r,
            trail_activate_r=trail_activate_r,
            atr_period=atr_period,
            atr_trail_multiple=atr_trail_multiple,
            slippage_ticks=slippage_ticks,
            commission_per_side=commission_per_side,
            contract_multiplier=contract_multiplier,
            breakout_bar_close_location_min=breakout_bar_close_location_min,
            require_signal_bar_close_at_or_above_trigger=require_signal_bar_close_at_or_above_trigger,
        )


class OpeningRangeBreakoutV8AStrategy(OpeningRangeBreakoutV2Strategy):
    def __init__(
        self,
        range_minutes: int = 15,
        entry_buffer_ticks: float = 1.0,
        stop_buffer_ticks: float = 1.0,
        position_size: int = 1,
        tick_size: float = 0.25,
        session_open: str = "08:30",
        no_new_entries_after: str = "11:00",
        time_stop: str = "13:30",
        allow_long: bool = True,
        timezone: str = "America/Chicago",
        or_width_lookback_days: int = 20,
        or_width_min_factor: float = 0.5,
        or_width_max_factor: float = 2.0,
        cost_protect_trigger_r: float = 1.25,
        trail_activate_r: float = 2.0,
        atr_period: int = 20,
        atr_trail_multiple: float = 3.0,
        slippage_ticks: float = 1.0,
        commission_per_side: float = 1.25,
        contract_multiplier: float = 5.0,
        breakout_bar_close_location_min: float = 0.70,
        breakout_bar_body_fraction_min: float = 0.30,
    ) -> None:
        super().__init__(
            range_minutes=range_minutes,
            entry_buffer_ticks=entry_buffer_ticks,
            stop_buffer_ticks=stop_buffer_ticks,
            position_size=position_size,
            tick_size=tick_size,
            session_open=session_open,
            no_new_entries_after=no_new_entries_after,
            time_stop=time_stop,
            allow_long=allow_long,
            timezone=timezone,
            or_width_lookback_days=or_width_lookback_days,
            or_width_min_factor=or_width_min_factor,
            or_width_max_factor=or_width_max_factor,
            cost_protect_trigger_r=cost_protect_trigger_r,
            trail_activate_r=trail_activate_r,
            atr_period=atr_period,
            atr_trail_multiple=atr_trail_multiple,
            slippage_ticks=slippage_ticks,
            commission_per_side=commission_per_side,
            contract_multiplier=contract_multiplier,
            breakout_bar_close_location_min=breakout_bar_close_location_min,
            breakout_bar_body_fraction_min=breakout_bar_body_fraction_min,
        )


class OpeningRangeBreakoutV9AStrategy(OpeningRangeBreakoutV2Strategy):
    def __init__(
        self,
        range_minutes: int = 15,
        entry_buffer_ticks: float = 1.0,
        stop_buffer_ticks: float = 1.0,
        position_size: int = 1,
        tick_size: float = 0.25,
        session_open: str = "08:30",
        no_new_entries_after: str = "11:00",
        time_stop: str = "13:30",
        allow_long: bool = True,
        timezone: str = "America/Chicago",
        or_width_lookback_days: int = 20,
        or_width_min_factor: float = 0.5,
        or_width_max_factor: float = 2.0,
        cost_protect_trigger_r: float = 1.25,
        trail_activate_r: float = 2.0,
        atr_period: int = 20,
        atr_trail_multiple: float = 3.0,
        slippage_ticks: float = 1.0,
        commission_per_side: float = 1.25,
        contract_multiplier: float = 5.0,
        breakout_bar_close_location_min: float = 0.70,
        signal_bar_extension_from_trigger_max: float = 0.25,
    ) -> None:
        super().__init__(
            range_minutes=range_minutes,
            entry_buffer_ticks=entry_buffer_ticks,
            stop_buffer_ticks=stop_buffer_ticks,
            position_size=position_size,
            tick_size=tick_size,
            session_open=session_open,
            no_new_entries_after=no_new_entries_after,
            time_stop=time_stop,
            allow_long=allow_long,
            timezone=timezone,
            or_width_lookback_days=or_width_lookback_days,
            or_width_min_factor=or_width_min_factor,
            or_width_max_factor=or_width_max_factor,
            cost_protect_trigger_r=cost_protect_trigger_r,
            trail_activate_r=trail_activate_r,
            atr_period=atr_period,
            atr_trail_multiple=atr_trail_multiple,
            slippage_ticks=slippage_ticks,
            commission_per_side=commission_per_side,
            contract_multiplier=contract_multiplier,
            breakout_bar_close_location_min=breakout_bar_close_location_min,
            signal_bar_extension_from_trigger_max=signal_bar_extension_from_trigger_max,
        )


class OpeningRangeBreakoutV10AStrategy(OpeningRangeBreakoutV2Strategy):
    def __init__(
        self,
        range_minutes: int = 15,
        entry_buffer_ticks: float = 1.0,
        stop_buffer_ticks: float = 1.0,
        position_size: int = 1,
        tick_size: float = 0.25,
        session_open: str = "08:30",
        no_new_entries_after: str = "11:00",
        time_stop: str = "13:30",
        allow_long: bool = True,
        timezone: str = "America/Chicago",
        or_width_lookback_days: int = 20,
        or_width_min_factor: float = 0.5,
        or_width_max_factor: float = 2.0,
        cost_protect_trigger_r: float = 1.25,
        trail_activate_r: float = 2.0,
        atr_period: int = 20,
        atr_trail_multiple: float = 3.0,
        slippage_ticks: float = 1.0,
        commission_per_side: float = 1.25,
        contract_multiplier: float = 5.0,
        breakout_bar_close_location_min: float = 0.70,
        max_signal_bars_after_or_completion: int = 6,
    ) -> None:
        super().__init__(
            range_minutes=range_minutes,
            entry_buffer_ticks=entry_buffer_ticks,
            stop_buffer_ticks=stop_buffer_ticks,
            position_size=position_size,
            tick_size=tick_size,
            session_open=session_open,
            no_new_entries_after=no_new_entries_after,
            time_stop=time_stop,
            allow_long=allow_long,
            timezone=timezone,
            or_width_lookback_days=or_width_lookback_days,
            or_width_min_factor=or_width_min_factor,
            or_width_max_factor=or_width_max_factor,
            cost_protect_trigger_r=cost_protect_trigger_r,
            trail_activate_r=trail_activate_r,
            atr_period=atr_period,
            atr_trail_multiple=atr_trail_multiple,
            slippage_ticks=slippage_ticks,
            commission_per_side=commission_per_side,
            contract_multiplier=contract_multiplier,
            breakout_bar_close_location_min=breakout_bar_close_location_min,
            max_signal_bars_after_or_completion=max_signal_bars_after_or_completion,
        )


class OpeningRangeBreakoutV11AStrategy(OpeningRangeBreakoutV2Strategy):
    def __init__(
        self,
        range_minutes: int = 15,
        entry_buffer_ticks: float = 1.0,
        stop_buffer_ticks: float = 1.0,
        position_size: int = 1,
        tick_size: float = 0.25,
        session_open: str = "08:30",
        no_new_entries_after: str = "11:00",
        time_stop: str = "13:30",
        allow_long: bool = True,
        timezone: str = "America/Chicago",
        or_width_lookback_days: int = 20,
        or_width_min_factor: float = 0.5,
        or_width_max_factor: float = 2.0,
        cost_protect_trigger_r: float = 1.25,
        trail_activate_r: float = 2.0,
        atr_period: int = 20,
        atr_trail_multiple: float = 3.0,
        slippage_ticks: float = 1.0,
        commission_per_side: float = 1.25,
        contract_multiplier: float = 5.0,
        breakout_bar_close_location_min: float = 0.70,
        enable_first_post_entry_close_below_trigger_exit: bool = True,
    ) -> None:
        super().__init__(
            range_minutes=range_minutes,
            entry_buffer_ticks=entry_buffer_ticks,
            stop_buffer_ticks=stop_buffer_ticks,
            position_size=position_size,
            tick_size=tick_size,
            session_open=session_open,
            no_new_entries_after=no_new_entries_after,
            time_stop=time_stop,
            allow_long=allow_long,
            timezone=timezone,
            or_width_lookback_days=or_width_lookback_days,
            or_width_min_factor=or_width_min_factor,
            or_width_max_factor=or_width_max_factor,
            cost_protect_trigger_r=cost_protect_trigger_r,
            trail_activate_r=trail_activate_r,
            atr_period=atr_period,
            atr_trail_multiple=atr_trail_multiple,
            slippage_ticks=slippage_ticks,
            commission_per_side=commission_per_side,
            contract_multiplier=contract_multiplier,
            breakout_bar_close_location_min=breakout_bar_close_location_min,
            enable_first_post_entry_close_below_trigger_exit=enable_first_post_entry_close_below_trigger_exit,
        )


class OpeningRangeBreakoutV11AStrategy(OpeningRangeBreakoutV2Strategy):
    def __init__(
        self,
        range_minutes: int = 15,
        entry_buffer_ticks: float = 1.0,
        stop_buffer_ticks: float = 1.0,
        position_size: int = 1,
        tick_size: float = 0.25,
        session_open: str = "08:30",
        no_new_entries_after: str = "11:00",
        time_stop: str = "13:30",
        allow_long: bool = True,
        timezone: str = "America/Chicago",
        or_width_lookback_days: int = 20,
        or_width_min_factor: float = 0.5,
        or_width_max_factor: float = 2.0,
        cost_protect_trigger_r: float = 1.25,
        trail_activate_r: float = 2.0,
        atr_period: int = 20,
        atr_trail_multiple: float = 3.0,
        slippage_ticks: float = 1.0,
        commission_per_side: float = 1.25,
        contract_multiplier: float = 5.0,
        breakout_bar_close_location_min: float = 0.70,
        enable_first_post_entry_close_below_trigger_exit: bool = True,
    ) -> None:
        super().__init__(
            range_minutes=range_minutes,
            entry_buffer_ticks=entry_buffer_ticks,
            stop_buffer_ticks=stop_buffer_ticks,
            position_size=position_size,
            tick_size=tick_size,
            session_open=session_open,
            no_new_entries_after=no_new_entries_after,
            time_stop=time_stop,
            allow_long=allow_long,
            timezone=timezone,
            or_width_lookback_days=or_width_lookback_days,
            or_width_min_factor=or_width_min_factor,
            or_width_max_factor=or_width_max_factor,
            cost_protect_trigger_r=cost_protect_trigger_r,
            trail_activate_r=trail_activate_r,
            atr_period=atr_period,
            atr_trail_multiple=atr_trail_multiple,
            slippage_ticks=slippage_ticks,
            commission_per_side=commission_per_side,
            contract_multiplier=contract_multiplier,
            breakout_bar_close_location_min=breakout_bar_close_location_min,
            enable_first_post_entry_close_below_trigger_exit=enable_first_post_entry_close_below_trigger_exit,
        )


class PerknastyOriginalStrategy(Strategy):
    def __init__(
        self,
        range_minutes: int = 15,
        entry_offset_ticks: float = 2.0,
        position_size: int = 2,
        tick_size: float = 0.25,
        session_open: str = "08:30",
        force_exit: str = "14:30",
        timezone: str = "America/Chicago",
    ) -> None:
        if range_minutes <= 0:
            raise ValueError("range_minutes must be > 0.")
        if position_size <= 0:
            raise ValueError("position_size must be > 0.")
        if entry_offset_ticks < 0:
            raise ValueError("entry_offset_ticks must be >= 0.")

        self.range_minutes = int(range_minutes)
        self.entry_offset_ticks = float(entry_offset_ticks)
        self.position_size = int(position_size)
        self.tick_size = float(tick_size)
        self.session_open = _parse_time_hhmm(session_open)
        self.force_exit = _parse_time_hhmm(force_exit)
        self.tz = ZoneInfo(timezone)

        self.current_day: Optional[str] = None
        self.or_high: Optional[float] = None
        self.or_low: Optional[float] = None
        self.traded_today = False

        self.prev_bar: Optional[Bar] = None

        # Pending retest-limit order state
        self.pending_order_side: Optional[str] = None   # "long" | "short"
        self.pending_order_price: Optional[float] = None
        self.pending_order_active = False

        # Active position state
        self.active_side: Optional[str] = None          # "long" | "short"

    def _reset_day(self) -> None:
        self.or_high = None
        self.or_low = None
        self.traded_today = False
        self.prev_bar = None

        self.pending_order_side = None
        self.pending_order_price = None
        self.pending_order_active = False

        self.active_side = None

    def _clear_pending_order(self) -> None:
        self.pending_order_side = None
        self.pending_order_price = None
        self.pending_order_active = False

    def on_bar(self, bar: Bar, current_position: int) -> int:
        if bar.yyyymmdd != self.current_day:
            self.current_day = bar.yyyymmdd
            self._reset_day()

        local_time = _bar_local_time(bar, self.tz)
        local_minutes = _minutes_since_midnight(local_time)
        open_minutes = _minutes_since_midnight(self.session_open)
        force_exit_minutes = _minutes_since_midnight(self.force_exit)

        if local_minutes < open_minutes:
            self.prev_bar = bar
            return current_position

        # Sync position-side state with engine
        if current_position == 0:
            self.active_side = None
        elif current_position > 0:
            self.active_side = "long"
        else:
            self.active_side = "short"

        # Build opening range from first 15 minutes only
        in_or_window = open_minutes <= local_minutes < (open_minutes + self.range_minutes)
        if in_or_window:
            high = float(bar.high)
            low = float(bar.low)
            self.or_high = high if self.or_high is None else max(self.or_high, high)
            self.or_low = low if self.or_low is None else min(self.or_low, low)
            self.prev_bar = bar
            return current_position

        if self.or_high is None or self.or_low is None:
            self.prev_bar = bar
            return current_position

        # Hard time exit / cancel pending orders at 14:30
        if local_minutes >= force_exit_minutes:
            self._clear_pending_order()
            if current_position != 0:
                self.prev_bar = bar
                return 0
            self.prev_bar = bar
            return current_position

        price_close = float(bar.close)
        price_high = float(bar.high)
        price_low = float(bar.low)
        price_open = float(bar.open)

        # Manage active position
        if current_position > 0:
            # Structural hard stop: long stop at OR low
            if price_low <= self.or_low:
                self.prev_bar = bar
                return 0

            # Invalidation: 5m candle closes back inside OR
            if price_close <= self.or_high:
                self.prev_bar = bar
                return 0

            self.prev_bar = bar
            return current_position

        if current_position < 0:
            # Structural hard stop: short stop at OR high
            if price_high >= self.or_high:
                self.prev_bar = bar
                return 0

            # Invalidation: 5m candle closes back inside OR
            if price_close >= self.or_low:
                self.prev_bar = bar
                return 0

            self.prev_bar = bar
            return current_position

        # No new trades after first trade of day
        if self.traded_today:
            self._clear_pending_order()
            self.prev_bar = bar
            return current_position

        # If a pending retest limit exists, see if this bar fills it
        if self.pending_order_active and self.pending_order_side and self.pending_order_price is not None:
            if self.pending_order_side == "long":
                # Buy limit should fill if bar trades down to or through the limit
                if price_low <= self.pending_order_price <= price_high:
                    self.traded_today = True
                    self._clear_pending_order()
                    self.prev_bar = bar
                    return self.position_size

            elif self.pending_order_side == "short":
                # Sell limit should fill if bar trades up/down through the limit
                if price_low <= self.pending_order_price <= price_high:
                    self.traded_today = True
                    self._clear_pending_order()
                    self.prev_bar = bar
                    return -self.position_size

        # If we already have a pending order, do not generate another one
        if self.pending_order_active:
            self.prev_bar = bar
            return current_position

        # Need a prior 5m candle to evaluate breakout + hold
        if self.prev_bar is None:
            self.prev_bar = bar
            return current_position

        prev_close = float(self.prev_bar.close)

        # Long setup:
        # prior 5m candle closes above OR high
        # current 5m candle opens above OR high
        if prev_close > self.or_high and price_open > self.or_high:
            self.pending_order_side = "long"
            self.pending_order_price = self.or_high + (self.entry_offset_ticks * self.tick_size)
            self.pending_order_active = True

            # Allow same-bar fill after order becomes active
            if price_low <= self.pending_order_price <= price_high:
                self.traded_today = True
                self._clear_pending_order()
                self.prev_bar = bar
                return self.position_size

            self.prev_bar = bar
            return current_position

        # Short setup:
        # prior 5m candle closes below OR low
        # current 5m candle opens below OR low
        if prev_close < self.or_low and price_open < self.or_low:
            self.pending_order_side = "short"
            self.pending_order_price = self.or_low - (self.entry_offset_ticks * self.tick_size)
            self.pending_order_active = True

            # Allow same-bar fill after order becomes active
            if price_low <= self.pending_order_price <= price_high:
                self.traded_today = True
                self._clear_pending_order()
                self.prev_bar = bar
                return -self.position_size

            self.prev_bar = bar
            return current_position

        self.prev_bar = bar
        return current_position


class PreviousDayHighLowBreakoutStrategy(Strategy):
    def __init__(
        self,
        buffer_ticks: float = 1.0,
        position_size: int = 1,
        tick_size: float = 0.25,
        session_open: str = "08:30",
        no_new_entries_after: str = "11:30",
        allow_long: bool = True,
        allow_short: bool = True,
        timezone: str = "America/Chicago",
    ) -> None:
        self.buffer_ticks = float(buffer_ticks)
        self.position_size = int(position_size)
        self.tick_size = float(tick_size)
        self.session_open = _parse_time_hhmm(session_open)
        self.no_new_entries_after = _parse_time_hhmm(no_new_entries_after)
        self.allow_long = bool(allow_long)
        self.allow_short = bool(allow_short)
        self.tz = ZoneInfo(timezone)

        self.current_day: Optional[str] = None
        self.current_day_high: Optional[float] = None
        self.current_day_low: Optional[float] = None

        self.prev_day_high: Optional[float] = None
        self.prev_day_low: Optional[float] = None

        self.traded_long_today = False
        self.traded_short_today = False

    def _roll_day(self, new_day: str) -> None:
        if self.current_day is not None:
            if self.current_day_high is not None and self.current_day_low is not None:
                self.prev_day_high = self.current_day_high
                self.prev_day_low = self.current_day_low

        self.current_day = new_day
        self.current_day_high = None
        self.current_day_low = None
        self.traded_long_today = False
        self.traded_short_today = False

    def on_bar(self, bar: Bar, current_position: int) -> int:
        if bar.yyyymmdd != self.current_day:
            self._roll_day(bar.yyyymmdd)

        local_time = _bar_local_time(bar, self.tz)
        if local_time < self.session_open:
            return current_position

        price = float(bar.close)
        high = float(bar.high)
        low = float(bar.low)

        if self.current_day_high is None or high > self.current_day_high:
            self.current_day_high = high
        if self.current_day_low is None or low < self.current_day_low:
            self.current_day_low = low

        if self.prev_day_high is None or self.prev_day_low is None:
            return current_position

        buffer_amt = self.buffer_ticks * self.tick_size

        if current_position > 0 and price < self.prev_day_high:
            return 0
        if current_position < 0 and price > self.prev_day_low:
            return 0

        if local_time >= self.no_new_entries_after:
            return current_position

        if current_position == 0:
            if (
                self.allow_long
                and not self.traded_long_today
                and price > self.prev_day_high + buffer_amt
            ):
                self.traded_long_today = True
                return self.position_size

            if (
                self.allow_short
                and not self.traded_short_today
                and price < self.prev_day_low - buffer_amt
            ):
                self.traded_short_today = True
                return -self.position_size

        return current_position


class ForbReversalV1Strategy(Strategy):
    def __init__(
        self,
        range_minutes: int = 15,
        position_size: int = 1,
        tick_size: float = 0.25,
        session_open: str = "08:30",
        time_stop: str = "13:30",
        timezone: str = "America/Chicago",
        slippage_ticks: float = 1.0,
        commission_per_side: float = 1.25,
        contract_multiplier: float = 5.0,
    ) -> None:
        if range_minutes <= 0:
            raise ValueError("range_minutes must be > 0.")
        if position_size <= 0:
            raise ValueError("position_size must be > 0.")

        self.range_minutes = int(range_minutes)
        self.position_size = int(position_size)
        self.tick_size = float(tick_size)
        self.session_open = _parse_time_hhmm(session_open)
        self.time_stop = _parse_time_hhmm(time_stop)
        self.tz = ZoneInfo(timezone)

        self.slippage_ticks = float(slippage_ticks)
        self.commission_per_side = float(commission_per_side)
        self.contract_multiplier = float(contract_multiplier)

        self.current_day: Optional[str] = None
        self.or_high: Optional[float] = None
        self.or_low: Optional[float] = None

        self.traded_today = False

        self.upside_breakout_armed = False
        self.breakout_attempt_high: Optional[float] = None

        self.pending_short_entry = False
        self.entry_price: Optional[float] = None
        self.initial_stop: Optional[float] = None
        self.target_price: Optional[float] = None

    def _roll_day(self, new_day: str) -> None:
        self.current_day = new_day
        self.or_high = None
        self.or_low = None

        self.traded_today = False
        self.upside_breakout_armed = False
        self.breakout_attempt_high = None

        self.pending_short_entry = False
        self.entry_price = None
        self.initial_stop = None
        self.target_price = None

    def on_bar(self, bar: Bar, current_position: int) -> int:
        if bar.yyyymmdd != self.current_day:
            self._roll_day(bar.yyyymmdd)

        local_time = _bar_local_time(bar, self.tz)
        if local_time < self.session_open:
            return current_position

        local_minutes = _minutes_since_midnight(local_time)
        open_minutes = _minutes_since_midnight(self.session_open)
        price = float(bar.close)

        if current_position == 0 and self.entry_price is not None:
            self.entry_price = None
            self.initial_stop = None
            self.target_price = None

        if current_position < 0 and self.pending_short_entry:
            self.pending_short_entry = False
            self.entry_price = float(bar.open) - (self.slippage_ticks * self.tick_size)
            self.initial_stop = self.breakout_attempt_high
            self.target_price = self.or_low
            self.traded_today = True
            self.upside_breakout_armed = False

        in_range_window = open_minutes <= local_minutes < (open_minutes + self.range_minutes)
        if in_range_window:
            high = float(bar.high)
            low = float(bar.low)
            self.or_high = high if self.or_high is None else max(self.or_high, high)
            self.or_low = low if self.or_low is None else min(self.or_low, low)
            return current_position

        if self.or_high is None or self.or_low is None:
            return current_position

        if current_position < 0:
            if self.initial_stop is not None and price >= self.initial_stop:
                return 0
            if self.target_price is not None and price <= self.target_price:
                return 0
            if local_time >= self.time_stop:
                return 0
            return current_position

        if self.traded_today:
            return current_position

        high = float(bar.high)

        if not self.upside_breakout_armed:
            if high > self.or_high and price > self.or_high:
                self.upside_breakout_armed = True
                self.breakout_attempt_high = high
            return current_position

        if price < self.or_high:
            self.pending_short_entry = True
            return -self.position_size

        return current_position


class GapImbalanceResolutionV1Strategy(Strategy):
    """
    gap_imbalance_resolution_v1
    Short-only gap-up resolution family.
    Requires bearish prior day, gap up, gap > min/thresh ATR.
    Short entry on completed bar closing below opening drive low.
    """
    def __init__(
        self,
        atr_period: int = 14,
        gap_threshold_atr: float = 1.0,
        min_gap_atr: float = 0.5,
        opening_drive_minutes: int = 15,
        time_stop_minutes: int = 120,
        position_size: int = 1,
        tick_size: float = 0.25,
        session_open: str = "08:30",
        session_end: str = "15:15",
        timezone: str = "America/Chicago",
        allow_long: bool = False,
        allow_short: bool = True,
        **kwargs
    ) -> None:
        self.atr_period = int(atr_period)
        self.gap_threshold_atr = float(gap_threshold_atr)
        self.min_gap_atr = float(min_gap_atr)
        self.opening_drive_minutes = int(opening_drive_minutes)
        self.time_stop_minutes = int(time_stop_minutes)
        self.position_size = int(position_size)
        self.tick_size = float(tick_size)
        self.session_open = _parse_time_hhmm(session_open)
        self.session_end = _parse_time_hhmm(session_end)
        self.tz = ZoneInfo(timezone)
        
        # State: Prior Day Context
        self.current_day: Optional[str] = None
        self.prev_day_open: Optional[float] = None
        self.prev_day_close: Optional[float] = None
        
        self.current_day_open: Optional[float] = None
        self.gap_size: Optional[float] = None
        self.gap_size_atr: Optional[float] = None
        
        # State: ATR Tracking
        self._tr_window: Deque[float] = deque(maxlen=self.atr_period)
        self._tr_sum = 0.0
        self.prev_close_for_atr: Optional[float] = None
        self.current_atr: Optional[float] = None
        
        # State: Intraday
        self.opening_drive_high: Optional[float] = None
        self.opening_drive_low: Optional[float] = None
        self.setup_active = False
        self.setup_invalidated = False
        self.traded_today = False
        
        # State: Trade specific
        self.pending_short_entry = False
        self.entry_price: Optional[float] = None
        self.initial_stop: Optional[float] = None
        self.target_price: Optional[float] = None
        self.bars_in_trade = 0

    def _append_true_range(self, bar: Bar) -> None:
        high = float(bar.high)
        low = float(bar.low)
        if self.prev_close_for_atr is None:
            tr = high - low
        else:
            prev_close = self.prev_close_for_atr
            tr = max(high - low, abs(high - prev_close), abs(low - prev_close))

        if len(self._tr_window) == self.atr_period:
            self._tr_sum -= self._tr_window[0]
        self._tr_window.append(tr)
        self._tr_sum += tr
        self.prev_close_for_atr = float(bar.close)

    def _update_current_atr(self) -> None:
        if len(self._tr_window) < self.atr_period:
            self.current_atr = None
        else:
            self.current_atr = self._tr_sum / len(self._tr_window)

    def _roll_day(self, new_day: str) -> None:
        self.current_day = new_day
        self.current_day_open = None
        self.gap_size = None
        self.gap_size_atr = None
        self.opening_drive_high = None
        self.opening_drive_low = None
        self.setup_active = False
        self.setup_invalidated = False
        self.traded_today = False
        
        self.pending_short_entry = False
        self.entry_price = None
        self.initial_stop = None
        self.target_price = None
        self.bars_in_trade = 0

    def on_bar(self, bar: Bar, current_position: int) -> int:
        local_time = _bar_local_time(bar, self.tz)
        local_minutes = _minutes_since_midnight(local_time)
        open_minutes = _minutes_since_midnight(self.session_open)
        
        is_new_day = (bar.yyyymmdd != self.current_day)
        
        if is_new_day:
            if self.current_day is not None and self.prev_close_for_atr is not None:
                self.prev_day_close = self.prev_close_for_atr
            self._roll_day(bar.yyyymmdd)
            
        self._append_true_range(bar)
        
        if local_time < self.session_open:
            return current_position

        # Force End of Day / Session Exit
        if self.session_end is not None and local_time >= self.session_end and current_position != 0:
            return 0
            
        price = float(bar.close)
        high = float(bar.high)
        low = float(bar.low)

        # Grab Session Open Price Context
        if self.current_day_open is None:
            self.current_day_open = float(bar.open)
            self.prev_day_open = self.current_day_open # Store for next day reference indirectly handled earlier. 
            # Note: We need the actual prior day open for the BEARISH context rule: prior_close < prior_open
        
        # Day Open Logic handling cross-day gaps correctly
        if local_time == self.session_open:
            # First bar of session open. Evaluate the core context constraints.
            self.current_day_open = float(bar.open)
            self._update_current_atr()
            
            # Since prior_open is needed, we must track it properly. 
            # We will grab this day's open now, and store it to prev_day_open at day roll *if* we wanted.
            # But the prompt specifically states prior_day BEARISH: prior_close < prior_open.
            
            # If we don't have prior day open/close, we cannot trade today.
            if self.prev_day_open is None or self.prev_day_close is None or self.current_atr is None:
                self.setup_invalidated = True
            elif self.prev_day_close >= self.prev_day_open:
                 # Prior day must be bearish
                self.setup_invalidated = True
            elif self.current_day_open <= self.prev_day_close:
                # Gap must be positive
                self.setup_invalidated = True
            else:
                self.gap_size = self.current_day_open - self.prev_day_close
                if self.current_atr > 0:
                    self.gap_size_atr = self.gap_size / self.current_atr
                    if self.gap_size_atr < self.min_gap_atr:
                        self.setup_invalidated = True
                    # The setup threshold will be checked at end of opening drive
                else:
                    self.setup_invalidated = True

        # Ensure we always save today's open for tomorrow
        if local_time == self.session_open:
            self.prev_day_open = float(bar.open) # Will become 'prev_day_open' functionally for tomorrow. Note: The variable name applies to *tomorrow* once the day rolls.

        if current_position == 0 and self.entry_price is not None:
            self.entry_price = None
            self.initial_stop = None
            self.target_price = None
            self.bars_in_trade = 0

        # Execute pending short entry on next bar open
        if current_position == 0 and self.pending_short_entry:
            self.pending_short_entry = False
            self.entry_price = float(bar.open)
            self.initial_stop = self.opening_drive_high
            self.target_price = self.prev_day_close
            self.traded_today = True
            self.bars_in_trade = 1
            return -self.position_size

        # Trade Management
        if current_position < 0:
            self.bars_in_trade += 1
            if self.initial_stop is not None and price >= self.initial_stop:
                return 0
            if self.target_price is not None and price <= self.target_price:
                return 0
            if self.bars_in_trade >= self.time_stop_minutes:
                return 0
            return current_position

        if self.traded_today or self.setup_invalidated:
            return current_position

        # Track Opening Drive (First N minutes after open)
        in_opening_drive = open_minutes <= local_minutes < (open_minutes + self.opening_drive_minutes)
        if in_opening_drive:
            self.opening_drive_high = high if self.opening_drive_high is None else max(self.opening_drive_high, high)
            self.opening_drive_low = low if self.opening_drive_low is None else min(self.opening_drive_low, low)
            
            # Early Invalidation checks: More than 50% gap fill during the opening drive
            if self.gap_size is not None and self.current_day_open is not None:
                gap_pullback_dist = self.current_day_open - low
                if gap_pullback_dist > (0.5 * self.gap_size):
                    self.setup_invalidated = True
            return current_position
            
        # Drive Evaluation (happens exactly on the bar *after* the opening drive finishes)
        if not self.setup_active and self.opening_drive_high is not None:
            # Was drive in gap direction?
            # Approximation based on the prompt "drive must close above session open". We evaluate the price of the final bar of the drive window (which is the previous bar's close). We check the current bar since the opening drive just closed. Wait, we must verify the condition. We'll simply enforce that `self.opening_drive_high > self.current_day_open` and `price (close of the first bar out) or something`. The prompt says "opening drive closes above session open price". Since we are on a 1m bar, the current time is e.g. 08:45, meaning the last 15m closed. We need to grab the last bar close or current bar open context. We will use the prior bar close (which we don't explicitly store right now) but this is effectively `self.prev_close_for_atr` on the exact moment the drive ends.
            drive_close = self.prev_close_for_atr
            
            if drive_close is not None and self.current_day_open is not None and drive_close > self.current_day_open:
                if self.gap_size_atr is not None and self.gap_size_atr >= self.gap_threshold_atr:
                    self.setup_active = True
                else:
                    self.setup_invalidated = True
            else:
                self.setup_invalidated = True
                
        # Setup Trigger
        if self.setup_active and not self.pending_short_entry:
            if price < self.opening_drive_low:
                self.pending_short_entry = True

        return current_position


class MesMnqRmrV1Strategy(Strategy):
    uses_context_bar = True

    def __init__(
        self,
        range_minutes: int = 15,
        time_stop_bars: int = 60,
        divergence_threshold: float = -0.75,
        target_divergence: float = -0.25,
        position_size: int = 1,
        session_open: str = "08:30",
        timezone: str = "America/Chicago",
    ) -> None:
        self.range_minutes = int(range_minutes)
        self.time_stop_bars = int(time_stop_bars)
        self.divergence_threshold = float(divergence_threshold)
        self.target_divergence = float(target_divergence)
        self.position_size = int(position_size)
        self.session_open = _parse_time_hhmm(session_open)
        self.tz = ZoneInfo(timezone)

        self.current_day: Optional[str] = None
        
        self.mes_or_high: Optional[float] = None
        self.mes_or_low: Optional[float] = None
        self.mnq_or_high: Optional[float] = None
        self.mnq_or_low: Optional[float] = None
        
        self.mes_or_anchor_close: Optional[float] = None
        self.mnq_or_anchor_close: Optional[float] = None
        
        self.mes_or_width: Optional[float] = None
        self.mnq_or_width: Optional[float] = None
        
        self.armed = False
        self.invalidated = False
        self.traded_today = False
        self.prior_mes_high: Optional[float] = None
        self.bars_in_position = 0
        
        self.initial_stop: Optional[float] = None

    def _reset_day(self) -> None:
        self.mes_or_high = None
        self.mes_or_low = None
        self.mnq_or_high = None
        self.mnq_or_low = None
        self.mes_or_anchor_close = None
        self.mnq_or_anchor_close = None
        self.mes_or_width = None
        self.mnq_or_width = None
        
        self.armed = False
        self.invalidated = False
        self.traded_today = False
        self.prior_mes_high = None
        self.bars_in_position = 0
        self.initial_stop = None
        self.exit_reason = None

    def on_bar(self, bar: Bar, current_position: int, context_bar: Optional[Bar] = None) -> int:
        if bar.yyyymmdd != self.current_day:
            self.current_day = bar.yyyymmdd
            self._reset_day()

        local_time = _bar_local_time(bar, self.tz)
        if local_time < self.session_open:
            return current_position

        open_minutes = _minutes_since_midnight(self.session_open)
        local_minutes = _minutes_since_midnight(local_time)
        
        # Track prior_mes_high for trigger
        cached_prior_mes_high = self.prior_mes_high
        self.prior_mes_high = bar.high

        if self.invalidated:
            return current_position

        in_or = local_minutes < (open_minutes + self.range_minutes)
        if in_or:
            if current_position == 0:
                self.mes_or_high = bar.high if self.mes_or_high is None else max(self.mes_or_high, bar.high)
                self.mes_or_low = bar.low if self.mes_or_low is None else min(self.mes_or_low, bar.low)
                
                if context_bar:
                    self.mnq_or_high = context_bar.high if self.mnq_or_high is None else max(self.mnq_or_high, context_bar.high)
                    self.mnq_or_low = context_bar.low if self.mnq_or_low is None else min(self.mnq_or_low, context_bar.low)
            return current_position
            
        # Final bar of OR establishes anchors
        if self.mes_or_anchor_close is None:
            if not context_bar or self.mes_or_high is None or self.mnq_or_high is None:
                self.invalidated = True
                return current_position

            self.mes_or_width = self.mes_or_high - self.mes_or_low
            self.mnq_or_width = self.mnq_or_high - self.mnq_or_low
            
            if self.mes_or_width <= 0 or self.mnq_or_width <= 0:
                self.invalidated = True
                return current_position
                
            self.mes_or_anchor_close = bar.close
            self.mnq_or_anchor_close = context_bar.close

        if current_position == 0 and self.traded_today:
            return current_position

        # Need matched timestamps
        if not context_bar:
            return current_position
            
        mes_norm = (bar.close - self.mes_or_anchor_close) / self.mes_or_width
        mnq_norm = (context_bar.close - self.mnq_or_anchor_close) / self.mnq_or_width
        relative_dv = mes_norm - mnq_norm
        
        if current_position > 0:
            self.bars_in_position += 1
            if relative_dv >= self.target_divergence:
                self.exit_reason = ExitReason.TARGET.value
                return 0
            
            if self.bars_in_position >= self.time_stop_bars:
                self.exit_reason = ExitReason.TIME_STOP.value
                return 0
                
            if self.initial_stop is not None and bar.close <= self.initial_stop:
                self.exit_reason = ExitReason.INITIAL_STOP.value
                return 0
                
            return current_position

        # Look for Entry
        if not self.armed:
            if relative_dv <= self.divergence_threshold:
                self.armed = True
            return current_position
            
        if self.armed and cached_prior_mes_high is not None:
            if bar.close > cached_prior_mes_high:
                self.initial_stop = bar.low
                self.traded_today = True
                self.bars_in_position = 1
                self.exit_reason = None
                return self.position_size

        return current_position


class MesMnqRelativeValueSpreadV1Strategy(Strategy):
    """
    mes_mnq_relative_value_spread_v1

    Fixed-pair synchronous intraday substitute spread: Long MES / Short MNQ
    (or Short MES / Long MNQ) based on normalized percent-move divergence
    from the 08:30 CT session anchor, evaluated once at the 10:00 CT bar close.

    MES is the engine-tracked primary leg; MNQ is simulated internally.
    Exposes context_leg_cash_delta for the engine to inject MNQ bar P&L each bar.
    Flushes context_executions for the engine to append to the execution log.

    See mes_mnq_relative_value_spread_v1_spec.md.
    """

    uses_context_bar = True

    def __init__(
        self,
        divergence_threshold: float = 0.0030,
        time_eval: str = "10:00",
        time_exit: str = "14:30",
        session_start: str = "08:30",
        session_end: str = "15:00",
        pair_hard_stop_dollars: float = 200.0,
        mes_contract_multiplier: float = 5.0,
        mnq_contract_multiplier: float = 2.0,
        slippage_ticks: float = 1.0,
        tick_size_mes: float = 0.25,
        tick_size_mnq: float = 0.25,
        commission_per_side: float = 1.25,
        timezone: str = "America/Chicago",
    ) -> None:
        self.divergence_threshold = float(divergence_threshold)
        self.time_eval = _parse_time_hhmm(time_eval)
        self.time_exit = _parse_time_hhmm(time_exit)
        self.session_start = _parse_time_hhmm(session_start)
        self.session_end = _parse_time_hhmm(session_end)
        self.pair_hard_stop_dollars = float(pair_hard_stop_dollars)
        self.mes_contract_multiplier = float(mes_contract_multiplier)
        self.mnq_contract_multiplier = float(mnq_contract_multiplier)
        self.slippage_ticks = float(slippage_ticks)
        self.tick_size_mes = float(tick_size_mes)
        self.tick_size_mnq = float(tick_size_mnq)
        self.commission_per_side = float(commission_per_side)
        self.tz = ZoneInfo(timezone)

        # Cross-day session anchors
        self.current_day: Optional[str] = None
        self.mes_anchor_open: Optional[float] = None
        self.mnq_anchor_open: Optional[float] = None
        self.traded_today: bool = False

        # MES leg — engine-tracked; mirrored here for hard-stop computation
        self.mes_entry_fill: Optional[float] = None

        # MNQ leg — internally simulated
        self.mnq_position: int = 0
        self.mnq_entry_fill: Optional[float] = None
        self.mnq_last_close: Optional[float] = None
        self.mnq_pending_entry: bool = False
        self.mnq_pending_entry_qty: int = 0
        self.mnq_pending_exit: bool = False

        # Engine communication hooks
        self.context_leg_cash_delta: float = 0.0   # incremental MNQ bar P&L; reset by engine
        self.context_executions: List[Dict[str, object]] = []  # flushed by engine

    def _roll_day(self, new_day: str) -> None:
        # If MNQ position was still open at the session boundary (engine daily flatten
        # closed MES), record an informational MNQ closing execution at last known close.
        if self.mnq_position != 0 and self.mnq_last_close is not None:
            action = "BUY" if self.mnq_position < 0 else "SELL"
            self.context_executions.append({
                "ts": f"{self.current_day[:4]}-{self.current_day[4:6]}-{self.current_day[6:8]} 15:00:00",
                "instrument_key": "MNQ",
                "action": action,
                "qty_delta": -self.mnq_position,
                "fill_price": self.mnq_last_close,
                "reason": "daily_flatten",
            })
        self.current_day = new_day
        self.mes_anchor_open = None
        self.mnq_anchor_open = None
        self.traded_today = False
        self.mes_entry_fill = None
        self.mnq_position = 0
        self.mnq_entry_fill = None
        self.mnq_last_close = None
        self.mnq_pending_entry = False
        self.mnq_pending_entry_qty = 0
        self.mnq_pending_exit = False
        self.context_leg_cash_delta = 0.0
        self.exit_reason = None

    def _fill_mnq_entry(self, bar: Bar, context_bar: Bar, current_position: int) -> None:
        """Simulate MNQ fill at this bar's open. Matches MES fill timing."""
        slippage_dir = math.copysign(
            self.slippage_ticks * self.tick_size_mnq, self.mnq_pending_entry_qty
        )
        mnq_fill = float(context_bar.open) + slippage_dir
        self.mnq_entry_fill = mnq_fill
        # Also update MES entry fill from actual fill bar (bar.open + slippage)
        mes_slippage_dir = math.copysign(
            self.slippage_ticks * self.tick_size_mes, current_position
        )
        self.mes_entry_fill = float(bar.open) + mes_slippage_dir

        cost = self.commission_per_side + (
            self.slippage_ticks * self.tick_size_mnq * self.mnq_contract_multiplier
        )
        self.context_leg_cash_delta -= cost

        action = "BUY" if self.mnq_pending_entry_qty > 0 else "SELL"
        self.context_executions.append({
            "ts": context_bar.bar_ts.isoformat(),
            "instrument_key": "MNQ",
            "action": action,
            "qty_delta": self.mnq_pending_entry_qty,
            "fill_price": mnq_fill,
            "reason": "signal_entry",
        })
        self.mnq_position = self.mnq_pending_entry_qty
        self.mnq_pending_entry = False
        self.mnq_pending_entry_qty = 0
        # Intrabar P&L for entry bar: open-to-close (matches engine intrabar model)
        intrabar_pnl = (
            self.mnq_position
            * (float(context_bar.close) - float(context_bar.open))
            * self.mnq_contract_multiplier
        )
        self.context_leg_cash_delta += intrabar_pnl
        self.mnq_last_close = float(context_bar.close)

    def _fill_mnq_exit(self, context_bar: Bar, reason: str) -> None:
        """Simulate MNQ closing fill at this bar's open. Matches MES exit timing."""
        slippage_dir = math.copysign(
            self.slippage_ticks * self.tick_size_mnq, -self.mnq_position
        )
        mnq_fill = float(context_bar.open) + slippage_dir
        # Gap P&L: prev close to this bar's open
        if self.mnq_last_close is not None:
            gap_pnl = (
                self.mnq_position
                * (float(context_bar.open) - self.mnq_last_close)
                * self.mnq_contract_multiplier
            )
            self.context_leg_cash_delta += gap_pnl
        cost = self.commission_per_side + (
            self.slippage_ticks * self.tick_size_mnq * self.mnq_contract_multiplier
        )
        self.context_leg_cash_delta -= cost
        action = "BUY" if self.mnq_position < 0 else "SELL"
        self.context_executions.append({
            "ts": context_bar.bar_ts.isoformat(),
            "instrument_key": "MNQ",
            "action": action,
            "qty_delta": -self.mnq_position,
            "fill_price": mnq_fill,
            "reason": reason,
        })
        self.mnq_position = 0
        self.mnq_entry_fill = None
        self.mnq_last_close = None
        self.mnq_pending_exit = False

    def on_bar(self, bar: Bar, current_position: int, context_bar: Optional[Bar] = None) -> int:  # type: ignore[override]
        if bar.yyyymmdd != self.current_day:
            self._roll_day(bar.yyyymmdd)

        bar_time = _bar_local_time(bar, self.tz)

        # --- Step 1: Settle pending MNQ entry or exit at this bar's open ---
        if context_bar is not None:
            if self.mnq_pending_entry:
                self._fill_mnq_entry(bar, context_bar, current_position)
                return current_position  # MES already updated by engine; hold

            if self.mnq_pending_exit:
                self._fill_mnq_exit(context_bar, reason=self.exit_reason or "strategy_exit")
                return current_position  # MES already updated by engine; position now 0

        # --- Step 2: Capture session anchor opens at 08:30 ---
        if bar_time == self.session_start:
            self.mes_anchor_open = float(bar.open)
            if context_bar is not None:
                self.mnq_anchor_open = float(context_bar.open)

        # --- Step 3: Apply per-bar MNQ P&L while position is open ---
        if self.mnq_position != 0 and context_bar is not None:
            if self.mnq_last_close is not None:
                gap_pnl = (
                    self.mnq_position
                    * (float(context_bar.open) - self.mnq_last_close)
                    * self.mnq_contract_multiplier
                )
                self.context_leg_cash_delta += gap_pnl
            intrabar_pnl = (
                self.mnq_position
                * (float(context_bar.close) - float(context_bar.open))
                * self.mnq_contract_multiplier
            )
            self.context_leg_cash_delta += intrabar_pnl
            self.mnq_last_close = float(context_bar.close)

        # --- Step 4: Position management: pair hard stop and timed exit ---
        if current_position != 0 and self.mnq_position != 0:
            # Combined unrealized P&L from fill prices to current bar close
            mes_open_pnl = 0.0
            if self.mes_entry_fill is not None:
                mes_open_pnl = (
                    current_position
                    * (float(bar.close) - self.mes_entry_fill)
                    * self.mes_contract_multiplier
                )
            mnq_open_pnl = 0.0
            if self.mnq_entry_fill is not None and context_bar is not None:
                mnq_open_pnl = (
                    self.mnq_position
                    * (float(context_bar.close) - self.mnq_entry_fill)
                    * self.mnq_contract_multiplier
                )
            combined_open_pnl = mes_open_pnl + mnq_open_pnl

            if combined_open_pnl <= -self.pair_hard_stop_dollars:
                self.exit_reason = ExitReason.INITIAL_STOP.value
                self.mnq_pending_exit = True
                return 0

            if bar_time >= self.time_exit:
                self.exit_reason = ExitReason.TIME_STOP.value
                self.mnq_pending_exit = True
                return 0

            return current_position

        # --- Step 5: Entry signal — evaluated only at the 10:00 CT bar close ---
        if self.traded_today:
            return 0

        if bar_time == self.time_eval:
            if (
                self.mes_anchor_open is None
                or self.mnq_anchor_open is None
                or context_bar is None
            ):
                return 0

            mes_move = (float(bar.close) - self.mes_anchor_open) / self.mes_anchor_open
            mnq_move = (
                (float(context_bar.close) - self.mnq_anchor_open) / self.mnq_anchor_open
            )
            divergence = mnq_move - mes_move  # spec: MNQ_Move - MES_Move

            if divergence >= self.divergence_threshold:
                # MNQ outperformed: fade → Long MES, Short MNQ
                self.traded_today = True
                # Proxy MES fill for stop init; overwritten on fill bar
                self.mes_entry_fill = float(bar.close) + (
                    self.slippage_ticks * self.tick_size_mes
                )
                self.mnq_pending_entry = True
                self.mnq_pending_entry_qty = -1  # short MNQ
                return 1   # long MES

            if divergence <= -self.divergence_threshold:
                # MES outperformed: fade → Short MES, Long MNQ
                self.traded_today = True
                self.mes_entry_fill = float(bar.close) - (
                    self.slippage_ticks * self.tick_size_mes
                )
                self.mnq_pending_entry = True
                self.mnq_pending_entry_qty = 1   # long MNQ
                return -1  # short MES

        return 0


class MesMnqCoOcReversalV1Strategy(Strategy):
    """
    mes_mnq_co_oc_reversal_v1

    CO-OC overnight-intraday reversal pair trade: MES vs MNQ.

    Signal: compute overnight return for each leg (close-to-open).
      r_on_MES = ln(open_0830_MES / prior_cash_close_MES)
      r_on_MNQ = ln(open_0830_MNQ / prior_cash_close_MNQ)
      delta_on  = r_on_MNQ - r_on_MES

    Decision (evaluated at 08:30 bar close, executed at 08:31 bar open):
      delta_on > 0 → MNQ overnight winner, MES overnight loser
                   → LONG 3 MES (engine), SHORT 2 MNQ (context)
      delta_on < 0 → MES overnight winner, MNQ overnight loser
                   → SHORT 3 MES (engine), LONG 2 MNQ (context)
      delta_on = 0 → no trade

    No threshold filter. Fixed 3:2 ratio, not optimized in parent.
    Primary exit: 14:59 bar close signal (fills at 15:00 bar open).
    Pair hard stop: combined open P&L <= -$300.

    MES is the engine-tracked primary leg (qty = 3).
    MNQ is simulated internally via context_leg_cash_delta.
    See mes_mnq_co_oc_reversal_v1_spec.md.
    """

    uses_context_bar = True

    MES_QTY = 3
    MNQ_QTY = 2

    def __init__(
        self,
        session_start: str = "08:30",
        time_exit: str = "14:59",
        session_end: str = "15:00",
        pair_hard_stop_dollars: float = 300.0,
        mes_contract_multiplier: float = 5.0,
        mnq_contract_multiplier: float = 2.0,
        slippage_ticks: float = 1.0,
        tick_size_mes: float = 0.25,
        tick_size_mnq: float = 0.25,
        commission_per_side: float = 1.25,
        timezone: str = "America/Chicago",
        invert_signal: bool = False,
    ) -> None:
        self.invert_signal = bool(invert_signal)
        self.session_start = _parse_time_hhmm(session_start)
        self.time_exit = _parse_time_hhmm(time_exit)
        self.session_end = _parse_time_hhmm(session_end)
        self.pair_hard_stop_dollars = float(pair_hard_stop_dollars)
        self.mes_contract_multiplier = float(mes_contract_multiplier)
        self.mnq_contract_multiplier = float(mnq_contract_multiplier)
        self.slippage_ticks = float(slippage_ticks)
        self.tick_size_mes = float(tick_size_mes)
        self.tick_size_mnq = float(tick_size_mnq)
        self.commission_per_side = float(commission_per_side)
        self.tz = ZoneInfo(timezone)

        # Cross-day state: prior session's cash close for each leg
        self.current_day: Optional[str] = None
        self.prior_cash_close_mes: Optional[float] = None
        self.prior_cash_close_mnq: Optional[float] = None
        self._pending_prior_mes: Optional[float] = None
        self._pending_prior_mnq: Optional[float] = None

        # Intraday
        self.open_0830_mes: Optional[float] = None
        self.open_0830_mnq: Optional[float] = None
        self.traded_today: bool = False

        # MES leg (engine-tracked, mirrored for P&L)
        self.mes_entry_fill: Optional[float] = None
        self.mes_direction: int = 0

        # MNQ leg (internally simulated)
        self.mnq_position: int = 0
        self.mnq_entry_fill: Optional[float] = None
        self.mnq_last_close: Optional[float] = None
        self.mnq_pending_entry: bool = False
        self.mnq_pending_entry_qty: int = 0
        self.mnq_pending_exit: bool = False
        self.exit_reason: Optional[str] = None

        # Engine hooks
        self.context_leg_cash_delta: float = 0.0
        self.context_executions: List[Dict[str, object]] = []

    def _roll_day(self, new_day: str) -> None:
        # Promote pending prior-close captures from the day that just ended
        if self._pending_prior_mes is not None:
            self.prior_cash_close_mes = self._pending_prior_mes
        if self._pending_prior_mnq is not None:
            self.prior_cash_close_mnq = self._pending_prior_mnq
        self._pending_prior_mes = None
        self._pending_prior_mnq = None

        # Flush any open MNQ position via informational execution
        if self.mnq_position != 0 and self.mnq_last_close is not None:
            action = "BUY" if self.mnq_position < 0 else "SELL"
            day_str = self.current_day or new_day
            if len(day_str) == 8:  # yyyymmdd
                ts_str = f"{day_str[:4]}-{day_str[4:6]}-{day_str[6:8]} 15:00:00"
            else:
                ts_str = f"{day_str} 15:00:00"
            self.context_executions.append({
                "ts": ts_str,
                "instrument_key": "MNQ",
                "action": action,
                "qty_delta": -self.mnq_position,
                "fill_price": self.mnq_last_close,
                "reason": "daily_flatten",
            })

        self.current_day = new_day
        self.open_0830_mes = None
        self.open_0830_mnq = None
        self.traded_today = False
        self.mes_entry_fill = None
        self.mes_direction = 0
        self.mnq_position = 0
        self.mnq_entry_fill = None
        self.mnq_last_close = None
        self.mnq_pending_entry = False
        self.mnq_pending_entry_qty = 0
        self.mnq_pending_exit = False
        self.exit_reason = None
        self.context_leg_cash_delta = 0.0

    def _fill_mnq_entry(self, bar: Bar, context_bar: Bar) -> None:
        """Simulate MNQ fill at this bar's open. Matches MES fill timing."""
        slippage_dir = math.copysign(
            self.slippage_ticks * self.tick_size_mnq, self.mnq_pending_entry_qty
        )
        mnq_fill = float(context_bar.open) + slippage_dir
        self.mnq_entry_fill = mnq_fill

        # Mirror MES fill from bar open + directional slippage
        mes_slip = math.copysign(self.slippage_ticks * self.tick_size_mes, self.mes_direction)
        self.mes_entry_fill = float(bar.open) + mes_slip

        cost = self.commission_per_side + (
            self.slippage_ticks * self.tick_size_mnq * self.mnq_contract_multiplier
        )
        self.context_leg_cash_delta -= cost

        action = "BUY" if self.mnq_pending_entry_qty > 0 else "SELL"
        self.context_executions.append({
            "ts": context_bar.bar_ts.isoformat(),
            "instrument_key": "MNQ",
            "action": action,
            "qty_delta": self.mnq_pending_entry_qty,
            "fill_price": mnq_fill,
            "reason": "signal_entry",
        })
        self.mnq_position = self.mnq_pending_entry_qty
        self.mnq_pending_entry = False
        self.mnq_pending_entry_qty = 0

        # Intrabar P&L for entry bar (open-to-close)
        intrabar_pnl = (
            self.mnq_position
            * (float(context_bar.close) - float(context_bar.open))
            * self.mnq_contract_multiplier
        )
        self.context_leg_cash_delta += intrabar_pnl
        self.mnq_last_close = float(context_bar.close)

    def _fill_mnq_exit(self, context_bar: Bar, reason: str) -> None:
        """Simulate MNQ closing fill at this bar's open."""
        slippage_dir = math.copysign(
            self.slippage_ticks * self.tick_size_mnq, -self.mnq_position
        )
        mnq_fill = float(context_bar.open) + slippage_dir

        if self.mnq_last_close is not None:
            gap_pnl = (
                self.mnq_position
                * (float(context_bar.open) - self.mnq_last_close)
                * self.mnq_contract_multiplier
            )
            self.context_leg_cash_delta += gap_pnl

        cost = self.commission_per_side + (
            self.slippage_ticks * self.tick_size_mnq * self.mnq_contract_multiplier
        )
        self.context_leg_cash_delta -= cost

        action = "BUY" if self.mnq_position < 0 else "SELL"
        self.context_executions.append({
            "ts": context_bar.bar_ts.isoformat(),
            "instrument_key": "MNQ",
            "action": action,
            "qty_delta": -self.mnq_position,
            "fill_price": mnq_fill,
            "reason": reason,
        })
        self.mnq_position = 0
        self.mnq_entry_fill = None
        self.mnq_last_close = None
        self.mnq_pending_exit = False

    def on_bar(self, bar: Bar, current_position: int, context_bar: Optional[Bar] = None) -> int:  # type: ignore[override]
        if bar.yyyymmdd != self.current_day:
            self._roll_day(bar.yyyymmdd)

        bar_time = _bar_local_time(bar, self.tz)

        # ---- Step 1: Settle pending MNQ fills at this bar's open ----
        if context_bar is not None:
            if self.mnq_pending_entry and current_position != 0:
                self._fill_mnq_entry(bar, context_bar)
                return current_position

            if self.mnq_pending_exit and current_position == 0:
                self._fill_mnq_exit(context_bar, reason=self.exit_reason or "strategy_exit")
                return 0

        # ---- Step 2: Capture 08:30 bar open as overnight open anchor ----
        if bar_time == self.session_start:
            self.open_0830_mes = float(bar.open)
            if context_bar is not None:
                self.open_0830_mnq = float(context_bar.open)

        # ---- Step 3: Per-bar MNQ P&L while position is live ----
        if self.mnq_position != 0 and context_bar is not None:
            if self.mnq_last_close is not None:
                gap_pnl = (
                    self.mnq_position
                    * (float(context_bar.open) - self.mnq_last_close)
                    * self.mnq_contract_multiplier
                )
                self.context_leg_cash_delta += gap_pnl
            intrabar_pnl = (
                self.mnq_position
                * (float(context_bar.close) - float(context_bar.open))
                * self.mnq_contract_multiplier
            )
            self.context_leg_cash_delta += intrabar_pnl
            self.mnq_last_close = float(context_bar.close)

        # ---- Step 4: Record bar close for next day's prior-close capture ----
        self._pending_prior_mes = float(bar.close)
        if context_bar is not None:
            self._pending_prior_mnq = float(context_bar.close)

        # ---- Step 5: Position management (hard stop + time exit) ----
        if current_position != 0 and self.mnq_position != 0:
            mes_open_pnl = 0.0
            if self.mes_entry_fill is not None:
                mes_open_pnl = (
                    self.mes_direction
                    * (float(bar.close) - self.mes_entry_fill)
                    * self.mes_contract_multiplier
                    * self.MES_QTY
                )
            mnq_open_pnl = 0.0
            if self.mnq_entry_fill is not None and context_bar is not None:
                mnq_open_pnl = (
                    self.mnq_position
                    * (float(context_bar.close) - self.mnq_entry_fill)
                    * self.mnq_contract_multiplier
                )
            combined_open_pnl = mes_open_pnl + mnq_open_pnl

            if combined_open_pnl <= -self.pair_hard_stop_dollars:
                self.exit_reason = ExitReason.INITIAL_STOP.value
                self.mnq_pending_exit = True
                return 0

            if bar_time >= self.time_exit:
                self.exit_reason = ExitReason.TIME_STOP.value
                self.mnq_pending_exit = True
                return 0

            return current_position

        # ---- Step 6: Entry signal at 08:30 bar close ----
        if self.traded_today:
            return 0

        if bar_time == self.session_start:
            if (
                self.prior_cash_close_mes is None
                or self.prior_cash_close_mnq is None
                or self.open_0830_mes is None
                or self.open_0830_mnq is None
                or context_bar is None
                or self.prior_cash_close_mes <= 0
                or self.prior_cash_close_mnq <= 0
            ):
                return 0

            r_on_mes = math.log(self.open_0830_mes / self.prior_cash_close_mes)
            r_on_mnq = math.log(self.open_0830_mnq / self.prior_cash_close_mnq)
            delta_on = r_on_mnq - r_on_mes

            if self.invert_signal:
                delta_on = -delta_on

            if delta_on == 0.0:
                return 0

            self.traded_today = True

            if delta_on > 0.0:
                # MNQ = overnight winner → long 3 MES, short 2 MNQ
                self.mes_direction = 1
                self.mnq_pending_entry = True
                self.mnq_pending_entry_qty = -self.MNQ_QTY
                self.mes_entry_fill = float(bar.close) + (
                    self.slippage_ticks * self.tick_size_mes
                )
                return self.MES_QTY  # engine: long 3 MES

            else:
                # MES = overnight winner → short 3 MES, long 2 MNQ
                self.mes_direction = -1
                self.mnq_pending_entry = True
                self.mnq_pending_entry_qty = self.MNQ_QTY
                self.mes_entry_fill = float(bar.close) - (
                    self.slippage_ticks * self.tick_size_mes
                )
                return -self.MES_QTY  # engine: short 3 MES

        return 0


        return 0


class PriceGapReversionV1Strategy(Strategy):
    """
    price_gap_reversion_v1

    Fades extreme opening gaps (>3.0 standard deviations). Tests the hypothesis
    that massive overnight liquidity gaps are temporary structural overreactions
    that get filled by institutional inventory-unwinding when the cash session opens.
    
    Logic:
    1. Collect prior cash close (15:00 CT).
    2. Collect 08:30 open. compute gap = open_0830 - prior_cash_close.
    3. Maintain rolling 60-day history of gaps.
    4. At 08:30 CT close: if |gap| >= 3.0 * std_dev(gap_history), and the
       gap has not already filled on the 08:30 bar itself, signal entry.
    5. Enter next-bar open (08:31).
    6. Exit (gap fill) when price touches prior_cash_close. Evaluated intrabar -> exit next bar open.
    7. Time stop 11:30 CT. Hard stop $150.
    """

    def __init__(
        self,
        time_anchor: time,
        time_exit: time,
        entry_std_threshold: float = 3.0,
        rolling_window_days: int = 60,
        hard_stop_dollars: float = 150.0,
        multiplier: float = 5.0,
        timezone: ZoneInfo = ZoneInfo("America/Chicago"),
    ):
        self.time_anchor = time_anchor
        self.time_exit = time_exit
        self.entry_std_threshold = entry_std_threshold
        self.rolling_window_days = rolling_window_days
        self.hard_stop_dollars = hard_stop_dollars
        self.multiplier = multiplier
        self.tz = timezone
        
        # State
        self.gap_history: List[float] = []
        self.prior_cash_close: Optional[float] = None
        self.current_day_open: Optional[float] = None
        self.last_evaluated_date: Optional[date] = None

    def on_bar(self, position_qty: int, position_entry_price: float, current_bar: Dict, context_bars: Dict) -> int:
        ts = current_bar["ts"]
        local_time, local_date = _bar_local_time(ts, self.tz)
        
        # Track 15:00 cash close for prior day reference
        if local_time == time(15, 0):
            self.prior_cash_close = current_bar["close"]
            return 0
            
        # Manage active position
        if position_qty != 0:
            # 1. Hard Stop ($150)
            open_pnl = 0.0
            if position_qty > 0:
                open_pnl = (current_bar["close"] - position_entry_price) * self.multiplier
            elif position_qty < 0:
                open_pnl = (position_entry_price - current_bar["close"]) * self.multiplier
                
            if open_pnl <= -self.hard_stop_dollars:
                return -position_qty
                
            # 2. Primary Exit: Gap Fill (Intrabar touching prior cash close)
            if self.prior_cash_close is not None:
                if position_qty > 0 and current_bar["high"] >= self.prior_cash_close:
                    return -position_qty
                if position_qty < 0 and current_bar["low"] <= self.prior_cash_close:
                    return -position_qty
                    
            # 3. Time Stop
            if local_time >= self.time_exit:
                return -position_qty
                
            return 0
            
        # Evaluate entry at the exact anchor bar close (08:30)
        if local_time == self.time_anchor:
            # Don't evaluate multiple times per day
            if self.last_evaluated_date == local_date:
                return 0
            self.last_evaluated_date = local_date
            
            if self.prior_cash_close is None:
                return 0
                
            self.current_day_open = current_bar["open"]
            gap = self.current_day_open - self.prior_cash_close
            
            # Immediately append to history so it builds up over the burn-in period
            self.gap_history.append(gap)
            if len(self.gap_history) > self.rolling_window_days:
                self.gap_history.pop(0)
                
            # Need minimum history to compute meaningful sigma (e.g. 10 days minimum)
            if len(self.gap_history) < 10:
                return 0
                
            # Compute rolling sigma
            avg_gap = sum(self.gap_history) / len(self.gap_history)
            variance = sum((g - avg_gap) ** 2 for g in self.gap_history) / len(self.gap_history)
            sigma_gap = math.sqrt(variance)
            
            if sigma_gap == 0:
                return 0
                
            abs_gap = abs(gap)
            
            # Threshold check
            if abs_gap >= self.entry_std_threshold * sigma_gap:
                # Check if gap already filled on the 08:30 bar itself
                if gap > 0 and current_bar["low"] <= self.prior_cash_close:
                    # Gap up, but low breached prior close -> already filled
                    pass
                elif gap < 0 and current_bar["high"] >= self.prior_cash_close:
                    # Gap down, but high breached prior close -> already filled
                    pass
                else:
                    # Signal is valid, fade the gap
                    if gap > 0:
                        return -1  # Gap up -> Short
                    else:
                        return 1   # Gap down -> Long
                        
        return 0


class MesMnqCoOcExtremeReversalV1Strategy(Strategy):
    """
    mes_mnq_co_oc_extreme_reversal_v1

    Extreme overnight-intraday relative reversal: MES vs MNQ.

    Unlike the base version, this tests a strict OVERREACTION mechanism:
    1. Computes rolling 60-day standard deviation of overnight relative return (delta_on).
    2. Enters only if |delta_on| >= 2.0 * sigma_delta.
    3. Exits early if divergence collapses to <= 0.25 * sigma_delta, or
       at the 11:30 CT time stop, whichever is first.

    Fixed 3 MES : 2 MNQ ratio.
    """

    uses_context_bar = True

    MES_QTY = 3
    MNQ_QTY = 2

    def __init__(
        self,
        session_start: str = "08:30",
        time_exit: str = "11:30",
        pair_hard_stop_dollars: float = 300.0,
        entry_std_threshold: float = 2.0,
        exit_std_threshold: float = 0.25,
        rolling_window_days: int = 60,
        mes_contract_multiplier: float = 5.0,
        mnq_contract_multiplier: float = 2.0,
        slippage_ticks: float = 1.0,
        tick_size_mes: float = 0.25,
        tick_size_mnq: float = 0.25,
        commission_per_side: float = 1.25,
        timezone: str = "America/Chicago",
    ) -> None:
        self.session_start = _parse_time_hhmm(session_start)
        self.time_exit = _parse_time_hhmm(time_exit)
        self.pair_hard_stop_dollars = float(pair_hard_stop_dollars)
        self.entry_std_threshold = float(entry_std_threshold)
        self.exit_std_threshold = float(exit_std_threshold)
        self.rolling_window_days = int(rolling_window_days)

        self.mes_contract_multiplier = float(mes_contract_multiplier)
        self.mnq_contract_multiplier = float(mnq_contract_multiplier)
        self.slippage_ticks = float(slippage_ticks)
        self.tick_size_mes = float(tick_size_mes)
        self.tick_size_mnq = float(tick_size_mnq)
        self.commission_per_side = float(commission_per_side)
        self.tz = ZoneInfo(timezone)

        # Cross-day state
        self.current_day: Optional[str] = None
        self.prior_cash_close_mes: Optional[float] = None
        self.prior_cash_close_mnq: Optional[float] = None
        self._pending_prior_mes: Optional[float] = None
        self._pending_prior_mnq: Optional[float] = None

        # Rolling volatility state
        self.delta_on_history: List[float] = []
        self.current_sigma: Optional[float] = None

        # Intraday
        self.open_0830_mes: Optional[float] = None
        self.open_0830_mnq: Optional[float] = None
        self.traded_today: bool = False

        # MES leg
        self.mes_entry_fill: Optional[float] = None
        self.mes_direction: int = 0

        # MNQ leg
        self.mnq_position: int = 0
        self.mnq_entry_fill: Optional[float] = None
        self.mnq_last_close: Optional[float] = None
        self.mnq_pending_entry: bool = False
        self.mnq_pending_entry_qty: int = 0
        self.mnq_pending_exit: bool = False
        self.exit_reason: Optional[str] = None

        # Engine hooks
        self.context_leg_cash_delta: float = 0.0
        self.context_executions: List[Dict[str, object]] = []

    def _roll_day(self, new_day: str) -> None:
        if self._pending_prior_mes is not None:
            self.prior_cash_close_mes = self._pending_prior_mes
        if self._pending_prior_mnq is not None:
            self.prior_cash_close_mnq = self._pending_prior_mnq
        self._pending_prior_mes = None
        self._pending_prior_mnq = None

        if self.mnq_position != 0 and self.mnq_last_close is not None:
            action = "BUY" if self.mnq_position < 0 else "SELL"
            day_str = self.current_day or new_day
            if len(day_str) == 8:
                ts_str = f"{day_str[:4]}-{day_str[4:6]}-{day_str[6:8]} 15:00:00"
            else:
                ts_str = f"{day_str} 15:00:00"
            self.context_executions.append({
                "ts": ts_str,
                "instrument_key": "MNQ",
                "action": action,
                "qty_delta": -self.mnq_position,
                "fill_price": self.mnq_last_close,
                "reason": "daily_flatten",
            })

        self.current_day = new_day
        self.open_0830_mes = None
        self.open_0830_mnq = None
        self.traded_today = False
        self.mes_entry_fill = None
        self.mes_direction = 0
        self.mnq_position = 0
        self.mnq_entry_fill = None
        self.mnq_last_close = None
        self.mnq_pending_entry = False
        self.mnq_pending_entry_qty = 0
        self.mnq_pending_exit = False
        self.exit_reason = None
        self.context_leg_cash_delta = 0.0

    def _fill_mnq_entry(self, bar: Bar, context_bar: Bar) -> None:
        slippage_dir = math.copysign(
            self.slippage_ticks * self.tick_size_mnq, self.mnq_pending_entry_qty
        )
        mnq_fill = float(context_bar.open) + slippage_dir
        self.mnq_entry_fill = mnq_fill

        mes_slip = math.copysign(self.slippage_ticks * self.tick_size_mes, self.mes_direction)
        self.mes_entry_fill = float(bar.open) + mes_slip

        cost = self.commission_per_side + (
            self.slippage_ticks * self.tick_size_mnq * self.mnq_contract_multiplier
        )
        self.context_leg_cash_delta -= cost

        action = "BUY" if self.mnq_pending_entry_qty > 0 else "SELL"
        self.context_executions.append({
            "ts": context_bar.bar_ts.isoformat(),
            "instrument_key": "MNQ",
            "action": action,
            "qty_delta": self.mnq_pending_entry_qty,
            "fill_price": mnq_fill,
            "reason": "signal_entry",
        })
        self.mnq_position = self.mnq_pending_entry_qty
        self.mnq_pending_entry = False
        self.mnq_pending_entry_qty = 0

        intrabar_pnl = (
            self.mnq_position
            * (float(context_bar.close) - float(context_bar.open))
            * self.mnq_contract_multiplier
        )
        self.context_leg_cash_delta += intrabar_pnl
        self.mnq_last_close = float(context_bar.close)

    def _fill_mnq_exit(self, context_bar: Bar, reason: str) -> None:
        slippage_dir = math.copysign(
            self.slippage_ticks * self.tick_size_mnq, -self.mnq_position
        )
        mnq_fill = float(context_bar.open) + slippage_dir

        if self.mnq_last_close is not None:
            gap_pnl = (
                self.mnq_position
                * (float(context_bar.open) - self.mnq_last_close)
                * self.mnq_contract_multiplier
            )
            self.context_leg_cash_delta += gap_pnl

        cost = self.commission_per_side + (
            self.slippage_ticks * self.tick_size_mnq * self.mnq_contract_multiplier
        )
        self.context_leg_cash_delta -= cost

        action = "BUY" if self.mnq_position < 0 else "SELL"
        self.context_executions.append({
            "ts": context_bar.bar_ts.isoformat(),
            "instrument_key": "MNQ",
            "action": action,
            "qty_delta": -self.mnq_position,
            "fill_price": mnq_fill,
            "reason": reason,
        })
        self.mnq_position = 0
        self.mnq_entry_fill = None
        self.mnq_last_close = None
        self.mnq_pending_exit = False

    def on_bar(self, bar: Bar, current_position: int, context_bar: Optional[Bar] = None) -> int:  # type: ignore[override]
        if bar.yyyymmdd != self.current_day:
            self._roll_day(bar.yyyymmdd)

        bar_time = _bar_local_time(bar, self.tz)

        # ---- Step 1: Settle pending MNQ fills at this bar's open ----
        if context_bar is not None:
            if self.mnq_pending_entry and current_position != 0:
                self._fill_mnq_entry(bar, context_bar)
                return current_position

            if self.mnq_pending_exit and current_position == 0:
                self._fill_mnq_exit(context_bar, reason=self.exit_reason or "strategy_exit")
                return 0

        # ---- Step 2: Capture 08:30 bar open and compute daily signal ----
        if bar_time == self.session_start:
            self.open_0830_mes = float(bar.open)
            if context_bar is not None:
                self.open_0830_mnq = float(context_bar.open)

            # Evaluate overnight divergence and update history
            if (
                self.prior_cash_close_mes is not None
                and self.prior_cash_close_mnq is not None
                and self.open_0830_mes is not None
                and self.open_0830_mnq is not None
                and self.prior_cash_close_mes > 0
                and self.prior_cash_close_mnq > 0
            ):
                r_on_mes = math.log(self.open_0830_mes / self.prior_cash_close_mes)
                r_on_mnq = math.log(self.open_0830_mnq / self.prior_cash_close_mnq)
                delta_on = r_on_mnq - r_on_mes

                # Compute std dev from history before adding today's value (ex-ante)
                if len(self.delta_on_history) >= 2:
                    mean = sum(self.delta_on_history) / len(self.delta_on_history)
                    variance = sum((x - mean) ** 2 for x in self.delta_on_history) / (len(self.delta_on_history) - 1)
                    self.current_sigma = math.sqrt(variance)
                else:
                    self.current_sigma = None

                # Update history for next day
                self.delta_on_history.append(delta_on)
                if len(self.delta_on_history) > self.rolling_window_days:
                    self.delta_on_history.pop(0)

                # Evaluate entry signal if we have enough history
                if not self.traded_today and self.current_sigma is not None and self.current_sigma > 0:
                    threshold = self.entry_std_threshold * self.current_sigma

                    if delta_on >= threshold:
                        # MNQ = overnight winner → fade
                        self.traded_today = True
                        self.mes_direction = 1
                        self.mnq_pending_entry = True
                        self.mnq_pending_entry_qty = -self.MNQ_QTY
                        self.mes_entry_fill = float(bar.close) + (self.slippage_ticks * self.tick_size_mes)
                        return self.MES_QTY
                    
                    elif delta_on <= -threshold:
                        # MES = overnight winner → fade
                        self.traded_today = True
                        self.mes_direction = -1
                        self.mnq_pending_entry = True
                        self.mnq_pending_entry_qty = self.MNQ_QTY
                        self.mes_entry_fill = float(bar.close) - (self.slippage_ticks * self.tick_size_mes)
                        return -self.MES_QTY

        # ---- Step 3: Per-bar MNQ P&L while position is live ----
        if self.mnq_position != 0 and context_bar is not None:
            if self.mnq_last_close is not None:
                gap_pnl = (
                    self.mnq_position
                    * (float(context_bar.open) - self.mnq_last_close)
                    * self.mnq_contract_multiplier
                )
                self.context_leg_cash_delta += gap_pnl
            intrabar_pnl = (
                self.mnq_position
                * (float(context_bar.close) - float(context_bar.open))
                * self.mnq_contract_multiplier
            )
            self.context_leg_cash_delta += intrabar_pnl
            self.mnq_last_close = float(context_bar.close)

        # ---- Step 4: Record bar close for next day's prior-close capture ----
        self._pending_prior_mes = float(bar.close)
        if context_bar is not None:
            self._pending_prior_mnq = float(context_bar.close)

        # ---- Step 5: Position management (hard stop, convergence exit, time exit) ----
        if current_position != 0 and self.mnq_position != 0 and context_bar is not None:
            mes_open_pnl = 0.0
            if self.mes_entry_fill is not None:
                mes_open_pnl = (
                    self.mes_direction
                    * (float(bar.close) - self.mes_entry_fill)
                    * self.mes_contract_multiplier
                    * self.MES_QTY
                )
            mnq_open_pnl = 0.0
            if self.mnq_entry_fill is not None:
                mnq_open_pnl = (
                    self.mnq_position
                    * (float(context_bar.close) - self.mnq_entry_fill)
                    * self.mnq_contract_multiplier
                )
            combined_open_pnl = mes_open_pnl + mnq_open_pnl

            # 1. Hard stop
            if combined_open_pnl <= -self.pair_hard_stop_dollars:
                self.exit_reason = ExitReason.INITIAL_STOP.value
                self.mnq_pending_exit = True
                return 0

            # 2. Time exit
            if bar_time >= self.time_exit:
                self.exit_reason = ExitReason.TIME_STOP.value
                self.mnq_pending_exit = True
                return 0

            # 3. Convergence exit
            if self.current_sigma is not None and self.current_sigma > 0 and self.open_0830_mes is not None and self.open_0830_mnq is not None:
                # Re-compute full move from prior close to CURRENT intraday close
                r_total_mes = math.log(float(bar.close) / self.prior_cash_close_mes)
                r_total_mnq = math.log(float(context_bar.close) / self.prior_cash_close_mnq)
                delta_intraday = r_total_mnq - r_total_mes
                
                if abs(delta_intraday) <= (self.exit_std_threshold * self.current_sigma):
                    self.exit_reason = ExitReason.TARGET.value  # Converged
                    self.mnq_pending_exit = True
                    return 0

            return current_position

        return 0


class OdpcV1Strategy(Strategy):
    def __init__(
        self,
        range_minutes: int = 15,
        position_size: int = 1,
        tick_size: float = 0.25,
        session_open: str = "08:30",
        time_stop: str = "13:30",
        timezone: str = "America/Chicago",
        slippage_ticks: float = 1.0,
        commission_per_side: float = 1.25,
        contract_multiplier: float = 5.0,
    ) -> None:
        if range_minutes <= 0:
            raise ValueError("range_minutes must be > 0.")
        if position_size <= 0:
            raise ValueError("position_size must be > 0.")

        self.range_minutes = int(range_minutes)
        self.position_size = int(position_size)
        self.tick_size = float(tick_size)
        self.session_open = _parse_time_hhmm(session_open)
        self.time_stop = _parse_time_hhmm(time_stop)
        self.tz = ZoneInfo(timezone)

        self.slippage_ticks = float(slippage_ticks)
        self.commission_per_side = float(commission_per_side)
        self.contract_multiplier = float(contract_multiplier)

        self.current_day: Optional[str] = None
        self.or_high: Optional[float] = None
        self.or_low: Optional[float] = None

        self.traded_today = False

        self.upside_drive_armed = False
        self.pullback_registered = False
        self.pullback_bar_high: Optional[float] = None
        self.pullback_bar_low: Optional[float] = None

        self.pending_long_entry = False
        self.entry_price: Optional[float] = None
        self.initial_stop: Optional[float] = None
        self.target_price: Optional[float] = None

    def _roll_day(self, new_day: str) -> None:
        self.current_day = new_day
        self.or_high = None
        self.or_low = None

        self.traded_today = False
        self.upside_drive_armed = False
        self.pullback_registered = False
        self.pullback_bar_high = None
        self.pullback_bar_low = None

        self.pending_long_entry = False
        self.entry_price = None
        self.initial_stop = None
        self.target_price = None

    def on_bar(self, bar: Bar, current_position: int) -> int:
        if bar.yyyymmdd != self.current_day:
            self._roll_day(bar.yyyymmdd)

        local_time = _bar_local_time(bar, self.tz)
        if local_time < self.session_open:
            return current_position

        local_minutes = _minutes_since_midnight(local_time)
        open_minutes = _minutes_since_midnight(self.session_open)
        price = float(bar.close)

        if current_position == 0 and self.entry_price is not None:
            self.entry_price = None
            self.initial_stop = None
            self.target_price = None

        if current_position > 0 and self.pending_long_entry:
            self.pending_long_entry = False
            self.entry_price = float(bar.open) + (self.slippage_ticks * self.tick_size)
            self.initial_stop = self.pullback_bar_low
            or_width = 0.0
            if self.or_high is not None and self.or_low is not None:
                or_width = self.or_high - self.or_low
            self.target_price = self.entry_price + or_width
            self.traded_today = True
            self.upside_drive_armed = False
            self.pullback_registered = False

        in_range_window = open_minutes <= local_minutes < (open_minutes + self.range_minutes)
        if in_range_window:
            high = float(bar.high)
            low = float(bar.low)
            self.or_high = high if self.or_high is None else max(self.or_high, high)
            self.or_low = low if self.or_low is None else min(self.or_low, low)
            return current_position

        if self.or_high is None or self.or_low is None:
            return current_position

        if current_position > 0:
            if self.initial_stop is not None and price <= self.initial_stop:
                return 0
            if self.target_price is not None and price >= self.target_price:
                return 0
            if local_time >= self.time_stop:
                return 0
            return current_position

        if self.traded_today:
            return current_position

        high = float(bar.high)
        low = float(bar.low)

        if not self.upside_drive_armed:
            if high > self.or_high and price > self.or_high:
                self.upside_drive_armed = True
            return current_position

        if not self.pullback_registered:
            if low <= self.or_high and price >= self.or_high:
                self.pullback_registered = True
                self.pullback_bar_high = high
                self.pullback_bar_low = low
            return current_position

        if self.pullback_bar_high is not None and price > self.pullback_bar_high:
            self.pending_long_entry = True
            return self.position_size

        return current_position


class HedgingDemandIntradayMomentumV1Strategy(Strategy):
    """
    hedging_demand_intraday_momentum_v1
    Trades MES based on the intraday directional point move from 09:30 EST to 15:30 EST.
    Enters at 15:30 EST if absolute move >= threshold. Exits at 16:00 EST.
    Time parameters should be provided in the local exchange timezone (America/Chicago).
    """

    def __init__(
        self,
        trend_threshold_points: float = 30.0,
        time_entry: str = "14:30",  # 15:30 EST
        time_exit: str = "15:00",   # 16:00 EST
        session_open: str = "08:30", # 09:30 EST
        hard_stop_points: float = 8.0,
        position_size: int = 1,
        tick_size: float = 0.25,
        timezone: str = "America/Chicago",
        slippage_ticks: float = 1.0,
        commission_per_side: float = 1.25,
        contract_multiplier: float = 5.0,
    ) -> None:
        self.trend_threshold_points = trend_threshold_points
        self.time_entry = _parse_time_hhmm(time_entry)
        self.time_exit = _parse_time_hhmm(time_exit)
        self.session_open = _parse_time_hhmm(session_open)
        self.hard_stop_points = hard_stop_points
        self.position_size = position_size
        self.tick_size = tick_size
        self.tz = ZoneInfo(timezone)
        self.slippage_ticks = slippage_ticks
        self.commission_per_side = commission_per_side
        self.contract_multiplier = contract_multiplier

        self.current_day: Optional[str] = None
        self.traded_today = False
        self.open_price: Optional[float] = None
        self.entry_price: Optional[float] = None

    def _roll_day(self, new_day: str) -> None:
        self.current_day = new_day
        self.traded_today = False
        self.open_price = None
        self.entry_price = None

    def on_bar(self, bar: Bar, current_position: int) -> int:
        if self.current_day != bar.yyyymmdd:
            self._roll_day(bar.yyyymmdd)
            self.exit_reason = None

        bar_time = _bar_local_time(bar, self.tz)

        if bar_time == self.session_open:
            self.open_price = bar.open

        if current_position != 0:
            if bar_time >= self.time_exit:
                self.exit_reason = ExitReason.TIME_STOP.value
                return 0

            if self.entry_price is not None:
                if current_position > 0:
                    stop_price = self.entry_price - self.hard_stop_points
                    if bar.low <= stop_price:
                        self.exit_reason = ExitReason.INITIAL_STOP.value
                        return 0
                elif current_position < 0:
                    stop_price = self.entry_price + self.hard_stop_points
                    if bar.high >= stop_price:
                        self.exit_reason = ExitReason.INITIAL_STOP.value
                        return 0
            
            return current_position

        if not self.traded_today and self.open_price is not None:
            if bar_time == self.time_entry:
                point_move = bar.close - self.open_price
                
                if point_move >= self.trend_threshold_points:
                    self.traded_today = True
                    self.entry_price = bar.close
                    return self.position_size
                elif point_move <= -self.trend_threshold_points:
                    self.traded_today = True
                    self.entry_price = bar.close
                    return -self.position_size
                    
        return 0


class OvernightIntradayReversalV1Strategy(Strategy):
    """
    overnight_intraday_reversal_v1

    Fades the MES overnight gap: prior RTH close to current RTH open.
    Signal  = Open[08:30 CT bar] - Prior_RTH_Close_Price
    Evaluated at the close of the 08:30 CT bar; order fills next bar.
    Exits at the close of the 14:30 CT bar or on hard stop.
    One trade per day maximum; no profit target.

    Derived from SSRN-003 (single-instrument MES derivative of a
    cross-sectional family). See overnight_intraday_reversal_v1_spec.md.
    """

    def __init__(
        self,
        gap_threshold_points: float = 8.0,
        time_eval: str = "08:30",   # bar whose open anchors the gap; signal fires at bar close
        time_exit: str = "14:30",   # flatten at close of this bar
        session_start: str = "08:30",
        session_end: str = "15:00",
        hard_stop_points: float = 10.0,
        position_size: int = 1,
        tick_size: float = 0.25,
        timezone: str = "America/Chicago",
        slippage_ticks: float = 1.0,
        commission_per_side: float = 1.25,
        contract_multiplier: float = 5.0,
    ) -> None:
        self.gap_threshold_points = float(gap_threshold_points)
        self.time_eval = _parse_time_hhmm(time_eval)
        self.time_exit = _parse_time_hhmm(time_exit)
        self.session_start = _parse_time_hhmm(session_start)
        self.session_end = _parse_time_hhmm(session_end)
        self.hard_stop_points = float(hard_stop_points)
        self.position_size = int(position_size)
        self.tick_size = float(tick_size)
        self.tz = ZoneInfo(timezone)
        self.slippage_ticks = float(slippage_ticks)
        self.commission_per_side = float(commission_per_side)
        self.contract_multiplier = float(contract_multiplier)

        # Cross-day state
        self.current_day: Optional[str] = None
        self.prior_rth_close: Optional[float] = None   # last RTH close of the previous session
        self._last_rth_close_candidate: Optional[float] = None  # tracks last close within RTH today

        # Per-day trade state
        self.traded_today: bool = False
        self.rth_open_price: Optional[float] = None    # open of the 08:30 bar
        self.entry_fill_price: Optional[float] = None  # estimated fill for stop calc

    def _roll_day(self, new_day: str) -> None:
        # Carry forward the last RTH close from the completed session as the
        # prior_rth_close for the incoming day.
        if self._last_rth_close_candidate is not None:
            self.prior_rth_close = self._last_rth_close_candidate
        self.current_day = new_day
        self.traded_today = False
        self.rth_open_price = None
        self.entry_fill_price = None
        self._last_rth_close_candidate = None
        self.exit_reason = None

    def on_bar(self, bar: Bar, current_position: int) -> int:
        if self.current_day != bar.yyyymmdd:
            self._roll_day(bar.yyyymmdd)

        bar_time = _bar_local_time(bar, self.tz)

        # Track last RTH close for use as next day's prior_rth_close
        if bar_time >= self.session_start and bar_time < self.session_end:
            self._last_rth_close_candidate = float(bar.close)

        # --- Position management: stop and timed exit ---
        if current_position != 0:
            # Hard stop check (intrabar)
            if self.entry_fill_price is not None:
                if current_position > 0:
                    stop_price = self.entry_fill_price - self.hard_stop_points
                    if float(bar.low) <= stop_price:
                        self.exit_reason = ExitReason.INITIAL_STOP.value
                        return 0
                else:  # short
                    stop_price = self.entry_fill_price + self.hard_stop_points
                    if float(bar.high) >= stop_price:
                        self.exit_reason = ExitReason.INITIAL_STOP.value
                        return 0

            # Timed exit: at the close of the 14:30 CT bar
            if bar_time >= self.time_exit:
                self.exit_reason = ExitReason.TIME_STOP.value
                return 0

            return current_position

        # --- Entry logic: only fires at the 08:30 CT bar close ---
        if self.traded_today:
            return 0

        # Capture RTH opening print (open of the 08:30 bar)
        if bar_time == self.time_eval:
            self.rth_open_price = float(bar.open)

        # Evaluate signal at the close of the 08:30 bar
        if bar_time == self.time_eval and self.prior_rth_close is not None and self.rth_open_price is not None:
            gap = self.rth_open_price - self.prior_rth_close

            if gap >= self.gap_threshold_points:
                # Positive gap: fade short
                self.traded_today = True
                # Estimate fill price for stop tracking (fill is next bar; use bar.close as proxy)
                self.entry_fill_price = float(bar.close) + (self.slippage_ticks * self.tick_size)
                return -self.position_size

            if gap <= -self.gap_threshold_points:
                # Negative gap: fade long
                self.traded_today = True
                self.entry_fill_price = float(bar.close) - (self.slippage_ticks * self.tick_size)
                return self.position_size

        return 0


class PriceGapReversionV1Strategy(Strategy):
    """
    price_gap_reversion_v1

    Fades extreme opening gaps (>3.0 standard deviations). Tests the hypothesis
    that massive overnight liquidity gaps are temporary structural overreactions
    that get filled by institutional inventory-unwinding when the cash session opens.
    
    Logic:
    1. Collect prior cash close (15:00 CT).
    2. Collect 08:30 open. compute gap = open_0830 - prior_cash_close.
    3. Maintain rolling 60-day history of gaps.
    4. At 08:30 CT close: if |gap| >= 3.0 * std_dev(gap_history), and the
       gap has not already filled on the 08:30 bar itself, signal entry.
    5. Enter next-bar open (08:31).
    6. Exit (gap fill) when price touches prior_cash_close. Evaluated intrabar -> exit next bar open.
    7. Time stop 11:30 CT. Hard stop $150.
    """

    def __init__(
        self,
        time_anchor: time,
        time_exit: time,
        entry_std_threshold: float = 3.0,
        rolling_window_days: int = 60,
        hard_stop_dollars: float = 150.0,
        multiplier: float = 5.0,
        timezone: ZoneInfo = ZoneInfo("America/Chicago"),
    ):
        self.time_anchor = time_anchor
        self.time_exit = time_exit
        self.entry_std_threshold = entry_std_threshold
        self.rolling_window_days = rolling_window_days
        self.hard_stop_dollars = hard_stop_dollars
        self.multiplier = multiplier
        self.tz = timezone
        
        # State
        self.gap_history: List[float] = []
        self.prior_cash_close: Optional[float] = None
        self.current_day_open: Optional[float] = None
        self.last_evaluated_date_str: Optional[str] = None
        self.position_entry_price: Optional[float] = None
        self.exit_reason: Optional[str] = None

    def on_bar(self, bar: Bar, current_position: int) -> int:
        local_time = _bar_local_time(bar, self.tz)
        local_date_str = bar.yyyymmdd
        
        # Track 15:00 cash close for prior day reference
        if local_time == time(15, 0):
            self.prior_cash_close = float(bar.close)
            return 0
            
        # Manage active position
        if current_position != 0:
            # 1. Hard Stop ($150)
            open_pnl = 0.0
            if current_position > 0:
                open_pnl = (float(bar.close) - self.position_entry_price) * self.multiplier
            elif current_position < 0:
                open_pnl = (self.position_entry_price - float(bar.close)) * self.multiplier
                
            if open_pnl <= -self.hard_stop_dollars:
                self.exit_reason = ExitReason.INITIAL_STOP.value
                return 0
                
            # 2. Primary Exit: Gap Fill (Intrabar touching prior cash close)
            if self.prior_cash_close is not None:
                if current_position > 0 and float(bar.high) >= self.prior_cash_close:
                    self.exit_reason = "GapFill"
                    return 0
                if current_position < 0 and float(bar.low) <= self.prior_cash_close:
                    self.exit_reason = "GapFill"
                    return 0
                    
            # 3. Time Stop
            if local_time >= self.time_exit:
                self.exit_reason = ExitReason.TIME_STOP.value
                return 0
                
            return current_position
            
        # Evaluate entry at the exact anchor bar close (08:30)
        if local_time == self.time_anchor:
            # Don't evaluate multiple times per day
            if self.last_evaluated_date_str == local_date_str:
                return 0
            self.last_evaluated_date_str = local_date_str
            
            if self.prior_cash_close is None:
                return 0
                
            self.current_day_open = float(bar.open)
            gap = self.current_day_open - self.prior_cash_close
            
            # Immediately append to history so it builds up over the burn-in period
            self.gap_history.append(gap)
            if len(self.gap_history) > self.rolling_window_days:
                self.gap_history.pop(0)
                
            # Need minimum history to compute meaningful sigma (e.g. 10 days minimum)
            if len(self.gap_history) < 10:
                return 0
                
            # Compute rolling sigma
            avg_gap = sum(self.gap_history) / len(self.gap_history)
            variance = sum((g - avg_gap) ** 2 for g in self.gap_history) / len(self.gap_history)
            sigma_gap = math.sqrt(variance)
            
            if len(self.gap_history) == 60 and local_date_str.endswith("15"): # Sample print mid-month
                print(f"[DEBUG] {local_date_str} gap={gap:.2f} sigma={sigma_gap:.2f} 3-sig={3.0*sigma_gap:.2f}")

            if sigma_gap == 0:
                return 0
                
            abs_gap = abs(gap)
            
            # Threshold check
            if abs_gap >= self.entry_std_threshold * sigma_gap:
                # Check if gap already filled on the 08:30 bar itself
                if gap > 0 and float(bar.low) <= self.prior_cash_close:
                    # Gap up, but low breached prior close -> already filled
                    pass
                elif gap < 0 and float(bar.high) >= self.prior_cash_close:
                    # Gap down, but high breached prior close -> already filled
                    pass
                else:
                    # Signal is valid, fade the gap
                    if gap > 0:
                        self.position_entry_price = float(bar.close) # estimated for stop
                        return -1  # Gap up -> Short
                    else:
                        self.position_entry_price = float(bar.close) # estimated for stop
                        return 1   # Gap down -> Long
                        
        return 0



def build_strategy(strategy_name: str, params: Dict[str, object]) -> Strategy:
    name = strategy_name.strip().lower()

    if name == "hedging_demand_intraday_momentum_v1":
        return HedgingDemandIntradayMomentumV1Strategy(
            trend_threshold_points=float(params.get("trend_threshold_points", 30.0)),
            time_entry=str(params.get("time_entry", "14:30")),
            time_exit=str(params.get("time_exit", "15:00")),
            session_open=str(params.get("session_open", "08:30")),
            hard_stop_points=float(params.get("hard_stop_points", 8.0)),
            position_size=int(params.get("position_size", 1)),
            tick_size=float(params.get("tick_size", 0.25)),
            timezone=str(params.get("timezone", "America/Chicago")),
            slippage_ticks=float(params.get("slippage_ticks", 1.0)),
            commission_per_side=float(params.get("commission_per_side", 1.25)),
            contract_multiplier=float(params.get("contract_multiplier", 5.0)),
        )

    if name == "price_gap_reversion_v1":
        return PriceGapReversionV1Strategy(
            time_anchor=_parse_time_hhmm(str(params.get("time_anchor", "08:30"))),
            time_exit=_parse_time_hhmm(str(params.get("time_exit", "11:30"))),
            entry_std_threshold=float(params.get("entry_std_threshold", 3.0)),
            rolling_window_days=int(params.get("rolling_window_days", 60)),
            hard_stop_dollars=float(params.get("hard_stop_dollars", 150.0)),
            multiplier=float(params.get("multiplier", 5.0)),
            timezone=ZoneInfo(str(params.get("timezone", "America/Chicago"))),
        )

    if name == "mes_mnq_rmr_v1":
        return MesMnqRmrV1Strategy(**params)

    if name == "odpc_v1":
        return OdpcV1Strategy(**params)

    if name == "gir_v1":
        return GapImbalanceResolutionV1Strategy(**params)

    if name == "forb_reversal_v1":
        return ForbReversalV1Strategy(**params)

    if name == "sma_cross":
        return SmaCrossStrategy(
            fast=int(params.get("fast", 20)),
            slow=int(params.get("slow", 50)),
            allow_short=bool(params.get("allow_short", True)),
            position_size=int(params.get("position_size", 1)),
        )

    if name == "vwap_reversion":
        return VWAPReversionStrategy(
            deviation_ticks=float(params.get("deviation_ticks", 12.0)),
            exit_band_ticks=float(params.get("exit_band_ticks", 2.0)),
            min_bars_before_entry=int(params.get("min_bars_before_entry", 30)),
            position_size=int(params.get("position_size", 1)),
            tick_size=float(params.get("tick_size", 0.25)),
            session_start=str(params.get("session_start", "08:30")),
            no_new_entries_after=str(params.get("no_new_entries_after", "14:30")),
            allow_long=bool(params.get("allow_long", True)),
            allow_short=bool(params.get("allow_short", True)),
            timezone=str(params.get("timezone", "America/Chicago")),
        )

    if name in {"opening_range_breakout", "orb"}:
        return OpeningRangeBreakoutStrategy(
            range_minutes=int(params.get("range_minutes", 15)),
            buffer_ticks=float(params.get("buffer_ticks", 1.0)),
            position_size=int(params.get("position_size", 1)),
            tick_size=float(params.get("tick_size", 0.25)),
            session_open=str(params.get("session_open", "08:30")),
            no_new_entries_after=str(params.get("no_new_entries_after", "11:00")),
            allow_long=bool(params.get("allow_long", True)),
            allow_short=bool(params.get("allow_short", True)),
            timezone=str(params.get("timezone", "America/Chicago")),
        )

    if name in {"opening_range_breakout_v2", "orb_v2"}:
        return OpeningRangeBreakoutV2Strategy(
            range_minutes=int(params.get("range_minutes", 15)),
            entry_buffer_ticks=float(params.get("entry_buffer_ticks", 1.0)),
            stop_buffer_ticks=float(params.get("stop_buffer_ticks", 1.0)),
            position_size=int(params.get("position_size", 1)),
            tick_size=float(params.get("tick_size", 0.25)),
            session_open=str(params.get("session_open", "08:30")),
            no_new_entries_after=str(params.get("no_new_entries_after", "11:00")),
            time_stop=str(params.get("time_stop", "13:30")),
            allow_long=bool(params.get("allow_long", True)),
            or_width_lookback_days=int(params.get("or_width_lookback_days", 20)),
            or_width_min_factor=float(params.get("or_width_min_factor", 0.5)),
            or_width_max_factor=float(params.get("or_width_max_factor", 2.0)),
            cost_protect_trigger_r=float(params.get("cost_protect_trigger_r", 1.25)),
            trail_activate_r=float(params.get("trail_activate_r", 2.0)),
            atr_period=int(params.get("atr_period", 20)),
            atr_trail_multiple=float(params.get("atr_trail_multiple", 3.0)),
            commission_per_side=float(params.get("commission_per_side", 1.25)),
            contract_multiplier=float(params.get("contract_multiplier", 5.0)),
            slippage_ticks=float(params.get("slippage_ticks", 1.0)),
            timezone=str(params.get("timezone", "America/Chicago")),
        )

    if name in {"opening_range_breakout_v4", "orb_v4"}:
        return OpeningRangeBreakoutV4Strategy(
            range_minutes=int(params.get("range_minutes", 15)),
            entry_buffer_ticks=float(params.get("entry_buffer_ticks", 1.0)),
            stop_buffer_ticks=float(params.get("stop_buffer_ticks", 1.0)),
            position_size=int(params.get("position_size", 1)),
            tick_size=float(params.get("tick_size", 0.25)),
            session_open=str(params.get("session_open", "08:30")),
            no_new_entries_after=str(params.get("no_new_entries_after", "11:00")),
            time_stop=str(params.get("time_stop", "13:30")),
            allow_long=bool(params.get("allow_long", True)),
            or_width_lookback_days=int(params.get("or_width_lookback_days", 20)),
            or_width_min_factor=float(params.get("or_width_min_factor", 0.5)),
            or_width_max_factor=float(params.get("or_width_max_factor", 2.0)),
            cost_protect_trigger_r=float(params.get("cost_protect_trigger_r", 1.25)),
            trail_activate_r=float(params.get("trail_activate_r", 2.0)),
            atr_period=int(params.get("atr_period", 20)),
            atr_trail_multiple=float(params.get("atr_trail_multiple", 3.0)),
            commission_per_side=float(params.get("commission_per_side", 1.25)),
            contract_multiplier=float(params.get("contract_multiplier", 5.0)),
            slippage_ticks=float(params.get("slippage_ticks", 1.0)),
            timezone=str(params.get("timezone", "America/Chicago")),
            vwap_filter_mode=str(params.get("vwap_filter_mode", "signal_close_above_vwap")),
        )

    if name == "momentum_pullback":
        return MomentumPullbackStrategy(
            fast=int(params.get("fast", 20)),
            slow=int(params.get("slow", 50)),
            entry_buffer_ticks=float(params.get("entry_buffer_ticks", 1.0)),
            position_size=int(params.get("position_size", 1)),
            tick_size=float(params.get("tick_size", 0.25)),
            allow_short=bool(params.get("allow_short", True)),
        )

    if name == "opening_range_breakout_v6a":
        return OpeningRangeBreakoutV6AStrategy(**params)

    if name == "opening_range_breakout_v7a":
        return OpeningRangeBreakoutV7AStrategy(**params)

    if name == "opening_range_breakout_v8a":
        return OpeningRangeBreakoutV8AStrategy(**params)

    if name == "opening_range_breakout_v9a":
        return OpeningRangeBreakoutV9AStrategy(**params)

    if name == "opening_range_breakout_v10a":
        return OpeningRangeBreakoutV10AStrategy(**params)

    if name == "opening_range_breakout_v11a":
        return OpeningRangeBreakoutV11AStrategy(**params)

    if name in {"previous_day_high_low_breakout", "pdh_pdl_breakout"}:
        return PreviousDayHighLowBreakoutStrategy(
            buffer_ticks=float(params.get("buffer_ticks", 1.0)),
            position_size=int(params.get("position_size", 1)),
            tick_size=float(params.get("tick_size", 0.25)),
            session_open=str(params.get("session_open", "08:30")),
            no_new_entries_after=str(params.get("no_new_entries_after", "11:30")),
            allow_long=bool(params.get("allow_long", True)),
            allow_short=bool(params.get("allow_short", True)),
            timezone=str(params.get("timezone", "America/Chicago")),
        )

    if name == "perknasty_original":
        return PerknastyOriginalStrategy(
            range_minutes=int(params.get("range_minutes", 15)),
            entry_offset_ticks=float(params.get("entry_offset_ticks", 2.0)),
            position_size=int(params.get("position_size", 2)),
            tick_size=float(params.get("tick_size", 0.25)),
            session_open=str(params.get("session_open", "08:30")),
            force_exit=str(params.get("force_exit", "14:30")),
            timezone=str(params.get("timezone", "America/Chicago")),
        )

    if name in {"opening_range_breakout_v5a", "orb_v5a"}:
        return OpeningRangeBreakoutV5AStrategy(
            range_minutes=int(params.get("range_minutes", 15)),
            entry_buffer_ticks=float(params.get("entry_buffer_ticks", 1.0)),
            stop_buffer_ticks=float(params.get("stop_buffer_ticks", 1.0)),
            position_size=int(params.get("position_size", 1)),
            tick_size=float(params.get("tick_size", 0.25)),
            session_open=str(params.get("session_open", "08:30")),
            no_new_entries_after=str(params.get("no_new_entries_after", "11:00")),
            time_stop=str(params.get("time_stop", "13:30")),
            allow_long=bool(params.get("allow_long", True)),
            or_width_lookback_days=int(params.get("or_width_lookback_days", 20)),
            or_width_min_factor=float(params.get("or_width_min_factor", 0.80)),
            or_width_max_factor=float(params.get("or_width_max_factor", 1.60)),
            cost_protect_trigger_r=float(params.get("cost_protect_trigger_r", 1.25)),
            trail_activate_r=float(params.get("trail_activate_r", 2.0)),
            atr_period=int(params.get("atr_period", 20)),
            atr_trail_multiple=float(params.get("atr_trail_multiple", 3.0)),
            commission_per_side=float(params.get("commission_per_side", 1.25)),
            contract_multiplier=float(params.get("contract_multiplier", 5.0)),
            slippage_ticks=float(params.get("slippage_ticks", 1.0)),
            timezone=str(params.get("timezone", "America/Chicago")),
            or_close_location_min=float(params.get("or_close_location_min", 0.70)),
        )

    if name in {"opening_range_breakout_v5b", "orb_v5b"}:
        return OpeningRangeBreakoutV5BStrategy(
            range_minutes=int(params.get("range_minutes", 15)),
            entry_buffer_ticks=float(params.get("entry_buffer_ticks", 1.0)),
            stop_buffer_ticks=float(params.get("stop_buffer_ticks", 1.0)),
            position_size=int(params.get("position_size", 1)),
            tick_size=float(params.get("tick_size", 0.25)),
            session_open=str(params.get("session_open", "08:30")),
            no_new_entries_after=str(params.get("no_new_entries_after", "11:00")),
            time_stop=str(params.get("time_stop", "13:30")),
            allow_long=bool(params.get("allow_long", True)),
            or_width_lookback_days=int(params.get("or_width_lookback_days", 20)),
            or_width_min_factor=float(params.get("or_width_min_factor", 0.5)),
            or_width_max_factor=float(params.get("or_width_max_factor", 2.0)),
            cost_protect_trigger_r=float(params.get("cost_protect_trigger_r", 1.25)),
            trail_activate_r=float(params.get("trail_activate_r", 2.0)),
            atr_period=int(params.get("atr_period", 20)),
            atr_trail_multiple=float(params.get("atr_trail_multiple", 3.0)),
            commission_per_side=float(params.get("commission_per_side", 1.25)),
            contract_multiplier=float(params.get("contract_multiplier", 5.0)),
            slippage_ticks=float(params.get("slippage_ticks", 1.0)),
            timezone=str(params.get("timezone", "America/Chicago")),
            or_close_location_min=float(params.get("or_close_location_min", 0.70)),
        )

    if name in {"opening_range_breakout_v5c", "orb_v5c"}:
        return OpeningRangeBreakoutV2Strategy(
            range_minutes=int(params.get("range_minutes", 15)),
            entry_buffer_ticks=float(params.get("entry_buffer_ticks", 1.0)),
            stop_buffer_ticks=float(params.get("stop_buffer_ticks", 1.0)),
            position_size=int(params.get("position_size", 1)),
            tick_size=float(params.get("tick_size", 0.25)),
            session_open=str(params.get("session_open", "08:30")),
            no_new_entries_after=str(params.get("no_new_entries_after", "11:00")),
            time_stop=str(params.get("time_stop", "13:30")),
            allow_long=bool(params.get("allow_long", True)),
            or_width_lookback_days=int(params.get("or_width_lookback_days", 20)),
            or_width_min_factor=float(params.get("or_width_min_factor", 0.80)),
            or_width_max_factor=float(params.get("or_width_max_factor", 1.60)),
            cost_protect_trigger_r=float(params.get("cost_protect_trigger_r", 1.25)),
            trail_activate_r=float(params.get("trail_activate_r", 2.0)),
            atr_period=int(params.get("atr_period", 20)),
            atr_trail_multiple=float(params.get("atr_trail_multiple", 3.0)),
            commission_per_side=float(params.get("commission_per_side", 1.25)),
            contract_multiplier=float(params.get("contract_multiplier", 5.0)),
            slippage_ticks=float(params.get("slippage_ticks", 1.0)),
            timezone=str(params.get("timezone", "America/Chicago")),
        )

    if name in {"opening_range_breakout_v6a", "orb_v6a"}:
        return OpeningRangeBreakoutV6AStrategy(
            range_minutes=int(params.get("range_minutes", 15)),
            entry_buffer_ticks=float(params.get("entry_buffer_ticks", 1.0)),
            stop_buffer_ticks=float(params.get("stop_buffer_ticks", 1.0)),
            position_size=int(params.get("position_size", 1)),
            tick_size=float(params.get("tick_size", 0.25)),
            session_open=str(params.get("session_open", "08:30")),
            no_new_entries_after=str(params.get("no_new_entries_after", "11:00")),
            time_stop=str(params.get("time_stop", "13:30")),
            allow_long=bool(params.get("allow_long", True)),
            or_width_lookback_days=int(params.get("or_width_lookback_days", 20)),
            or_width_min_factor=float(params.get("or_width_min_factor", 0.5)),
            or_width_max_factor=float(params.get("or_width_max_factor", 2.0)),
            cost_protect_trigger_r=float(params.get("cost_protect_trigger_r", 1.25)),
            trail_activate_r=float(params.get("trail_activate_r", 2.0)),
            atr_period=int(params.get("atr_period", 20)),
            atr_trail_multiple=float(params.get("atr_trail_multiple", 3.0)),
            commission_per_side=float(params.get("commission_per_side", 1.25)),
            contract_multiplier=float(params.get("contract_multiplier", 5.0)),
            slippage_ticks=float(params.get("slippage_ticks", 1.0)),
            timezone=str(params.get("timezone", "America/Chicago")),
            breakout_bar_close_location_min=float(params.get("breakout_bar_close_location_min", 0.70)),
        )

    if name == "overnight_intraday_reversal_v1":
        return OvernightIntradayReversalV1Strategy(
            gap_threshold_points=float(params.get("gap_threshold_points", 8.0)),
            time_eval=str(params.get("time_eval", "08:30")),
            time_exit=str(params.get("time_exit", "14:30")),
            session_start=str(params.get("session_start", "08:30")),
            session_end=str(params.get("session_end", "15:00")),
            hard_stop_points=float(params.get("hard_stop_points", 10.0)),
            position_size=int(params.get("position_size", 1)),
            tick_size=float(params.get("tick_size", 0.25)),
            timezone=str(params.get("timezone", "America/Chicago")),
            slippage_ticks=float(params.get("slippage_ticks", 1.0)),
            commission_per_side=float(params.get("commission_per_side", 1.25)),
            contract_multiplier=float(params.get("contract_multiplier", 5.0)),
        )

    if name == "mes_mnq_relative_value_spread_v1":
        return MesMnqRelativeValueSpreadV1Strategy(
            divergence_threshold=float(params.get("divergence_threshold", 0.0030)),
            time_eval=str(params.get("time_eval", "10:00")),
            time_exit=str(params.get("time_exit", "14:30")),
            session_start=str(params.get("session_start", "08:30")),
            session_end=str(params.get("session_end", "15:00")),
            pair_hard_stop_dollars=float(params.get("pair_hard_stop_dollars", 200.0)),
            mes_contract_multiplier=float(params.get("mes_contract_multiplier", 5.0)),
            mnq_contract_multiplier=float(params.get("mnq_contract_multiplier", 2.0)),
            slippage_ticks=float(params.get("slippage_ticks", 1.0)),
            tick_size_mes=float(params.get("tick_size_mes", 0.25)),
            tick_size_mnq=float(params.get("tick_size_mnq", 0.25)),
            commission_per_side=float(params.get("commission_per_side", 1.25)),
            timezone=str(params.get("timezone", "America/Chicago")),
        )

    if name == "mes_mnq_co_oc_reversal_v1":
        return MesMnqCoOcReversalV1Strategy(
            session_start=str(params.get("session_start", "08:30")),
            time_exit=str(params.get("time_exit", "14:59")),
            session_end=str(params.get("session_end", "15:00")),
            pair_hard_stop_dollars=float(params.get("pair_hard_stop_dollars", 300.0)),
            mes_contract_multiplier=float(params.get("mes_contract_multiplier", 5.0)),
            mnq_contract_multiplier=float(params.get("mnq_contract_multiplier", 2.0)),
            slippage_ticks=float(params.get("slippage_ticks", 1.0)),
            tick_size_mes=float(params.get("tick_size_mes", 0.25)),
            tick_size_mnq=float(params.get("tick_size_mnq", 0.25)),
            commission_per_side=float(params.get("commission_per_side", 1.25)),
            timezone=str(params.get("timezone", "America/Chicago")),
            invert_signal=bool(params.get("invert_signal", False)),
        )

    if name == "mes_mnq_co_oc_extreme_reversal_v1":
        return MesMnqCoOcExtremeReversalV1Strategy(
            session_start=str(params.get("session_start", "08:30")),
            time_exit=str(params.get("time_exit", "11:30")),
            pair_hard_stop_dollars=float(params.get("pair_hard_stop_dollars", 300.0)),
            entry_std_threshold=float(params.get("entry_std_threshold", 2.0)),
            exit_std_threshold=float(params.get("exit_std_threshold", 0.25)),
            rolling_window_days=int(params.get("rolling_window_days", 60)),
            mes_contract_multiplier=float(params.get("mes_contract_multiplier", 5.0)),
            mnq_contract_multiplier=float(params.get("mnq_contract_multiplier", 2.0)),
            slippage_ticks=float(params.get("slippage_ticks", 1.0)),
            tick_size_mes=float(params.get("tick_size_mes", 0.25)),
            tick_size_mnq=float(params.get("tick_size_mnq", 0.25)),
            commission_per_side=float(params.get("commission_per_side", 1.25)),
            timezone=str(params.get("timezone", "America/Chicago")),
        )

    raise ValueError(f"Unknown strategy '{strategy_name}'.")


def parse_date(text: str) -> date:
    return datetime.strptime(text, DATE_FMT).date()


def parse_hhmm(text: Optional[object]) -> Optional[time]:
    if text is None:
        return None
    value = str(text).strip()
    if not value:
        return None
    hh, mm = value.split(":", 1)
    return time(hour=int(hh), minute=int(mm))


def coerce_datetime(value: object, tz: ZoneInfo) -> datetime:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=tz)
        return value.astimezone(tz)
    if isinstance(value, str):
        text = value.replace("Z", "+00:00")
        dt = datetime.fromisoformat(text)
        if dt.tzinfo is None:
            return dt.replace(tzinfo=tz)
        return dt.astimezone(tz)
    raise TypeError(f"Unsupported datetime value: {value!r}")


def within_session(bar_ts: datetime, tz: ZoneInfo, session_start: Optional[time], session_end: Optional[time]) -> bool:
    if session_start is None or session_end is None:
        return True
    local_ts = bar_ts.astimezone(tz)
    local_time = local_ts.timetz().replace(tzinfo=None)
    if session_start <= session_end:
        return session_start <= local_time < session_end
    return local_time >= session_start or local_time < session_end


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


class PositionBook:
    def __init__(self) -> None:
        self.qty = 0
        self.avg_entry_price = 0.0
        self.entry_ts: Optional[str] = None

    def apply_execution(
        self,
        ts: str,
        family: str,
        instrument_key: str,
        fill_price: float,
        qty_delta: int,
        multiplier: float,
        commission_total: float,
        slippage_total: float,
        reason: Optional[str] = None,
        mae_points: Optional[float] = None,
        mfe_points: Optional[float] = None,
        mae_r: Optional[float] = None,
        mfe_r: Optional[float] = None,
        initial_stop_price: Optional[float] = None,
        initial_target_price: Optional[float] = None,
        entry_trigger_price: Optional[float] = None,
        bars_held: Optional[int] = None,
    ) -> List[ClosedTrade]:
        if qty_delta == 0:
            return []

        closed: List[ClosedTrade] = []
        current_qty = self.qty
        same_direction = current_qty == 0 or (current_qty > 0 and qty_delta > 0) or (current_qty < 0 and qty_delta < 0)
        if same_direction:
            new_qty = current_qty + qty_delta
            total_abs = abs(current_qty) + abs(qty_delta)
            if current_qty == 0:
                self.avg_entry_price = fill_price
                self.entry_ts = ts
            else:
                self.avg_entry_price = (
                    (self.avg_entry_price * abs(current_qty)) + (fill_price * abs(qty_delta))
                ) / total_abs
            self.qty = new_qty
            return closed

        total_exec_qty = abs(qty_delta)
        per_contract_commission = commission_total / total_exec_qty if total_exec_qty else 0.0
        per_contract_slippage = slippage_total / total_exec_qty if total_exec_qty else 0.0

        close_qty = min(abs(current_qty), abs(qty_delta))
        side = "LONG" if current_qty > 0 else "SHORT"
        gross_pnl = (fill_price - self.avg_entry_price) * (1 if current_qty > 0 else -1) * close_qty * multiplier
        allocated_commission = per_contract_commission * close_qty
        allocated_slippage = per_contract_slippage * close_qty
        net_pnl = gross_pnl - allocated_commission - allocated_slippage
        closed.append(
            ClosedTrade(
                entry_ts=self.entry_ts or ts,
                exit_ts=ts,
                family=family,
                instrument_key=instrument_key,
                side=side,
                qty=close_qty,
                entry_price=self.avg_entry_price,
                exit_price=fill_price,
                gross_pnl=gross_pnl,
                commission=allocated_commission,
                slippage_cost=allocated_slippage,
                net_pnl=net_pnl,
                mae_points=mae_points,
                mfe_points=mfe_points,
                mae_r=mae_r,
                mfe_r=mfe_r,
                exit_reason=reason,
                initial_stop_price=initial_stop_price,
                initial_target_price=initial_target_price,
                entry_trigger_price=entry_trigger_price,
                bars_held=bars_held,
            )
        )

        if abs(qty_delta) < abs(current_qty):
            self.qty = current_qty + qty_delta
            return closed

        if abs(qty_delta) == abs(current_qty):
            self.qty = 0
            self.avg_entry_price = 0.0
            self.entry_ts = None
            return closed

        remainder = abs(qty_delta) - abs(current_qty)
        self.qty = remainder if qty_delta > 0 else -remainder
        self.avg_entry_price = fill_price
        self.entry_ts = ts
        return closed


class BacktestEngine:
    def __init__(self, config: Dict[str, object]) -> None:
        self.config = config
        self.family = str(config["family"]).upper()
        self.context_family = str(config["context_family"]).upper() if config.get("context_family") else None
        self.interval = str(config["interval"])
        self.db_path = Path(str(config["db_path"]))
        self.reports_root = Path(str(config["reports_root"]))
        self.report_tag = str(config.get("report_tag") or f"{self.family.lower()}_{self.interval}_run")
        self.run_id = f"{datetime.now().strftime('%Y%m%dT%H%M%S')}_{self.report_tag}"

        self.start_date = parse_date(str(config["start_date"]))
        self.end_date = parse_date(str(config["end_date"]))
        self.instrument_mode = str(config.get("instrument_mode", "dominant_by_day")).strip().lower()
        self.instrument_key = config.get("instrument_key")
        self.allow_missing_instrument = bool(config.get("allow_missing_instrument", False))

        self.session_tz = ZoneInfo(str(config.get("session_timezone", "America/Chicago")))
        self.session_start = parse_hhmm(config.get("session_start"))
        self.session_end = parse_hhmm(config.get("session_end"))

        self.initial_cash = float(config.get("initial_cash", 100000.0))
        self.contract_multiplier = float(config.get("contract_multiplier", 5.0))
        self.tick_size = float(config.get("tick_size", 0.25))
        self.slippage_ticks = float(config.get("slippage_ticks", 1.0))
        self.commission_per_side = float(config.get("commission_per_side", 1.25))
        self.flatten_daily = bool(config.get("flatten_daily", False))
        self.flatten_on_last_bar = bool(config.get("flatten_on_last_bar", True))
        self.max_days = int(config["max_days"]) if config.get("max_days") is not None else None

        self.write_daily_equity_csv = bool(config.get("write_daily_equity_csv", True))
        self.write_executions_csv = bool(config.get("write_executions_csv", True))
        self.write_closed_trades_csv = bool(config.get("write_closed_trades_csv", True))

        strategy_name = str(config.get("strategy", "sma_cross"))
        strategy_params = dict(config.get("strategy_params", {}))
        self.strategy = build_strategy(strategy_name, strategy_params)
        self.strategy_name = strategy_name

        self.cash = self.initial_cash
        self.position_qty = 0
        self.pending_target_qty = 0
        self.last_close: Optional[float] = None
        self.last_bar: Optional[Bar] = None
        self.active_instrument_key: Optional[str] = None

        self.position_book = PositionBook()
        self.executions: List[Execution] = []
        self.closed_trades: List[ClosedTrade] = []
        self.daily_rows: List[DailyEquityRow] = []
        self.day_info_rows: List[Dict[str, object]] = []

        self.pending_target_reason = "signal_from_prior_close"
        self.open_trade_highest_high: Optional[float] = None
        self.open_trade_lowest_low: Optional[float] = None
        self.open_trade_bars_held = 0
        self.open_initial_stop: Optional[float] = None
        self.open_initial_target: Optional[float] = None
        self.open_entry_trigger: Optional[float] = None

        self.report_dir = self.reports_root / self.run_id
        ensure_dir(self.report_dir)

        logging.info("[RUN] run_id=%s", self.run_id)
        logging.info("[RUN] db=%s", self.db_path)
        logging.info("[RUN] reports=%s", self.report_dir)
        logging.info("[RUN] family=%s interval=%s dates=%s..%s", self.family, self.interval, self.start_date, self.end_date)

    def connect(self) -> duckdb.DuckDBPyConnection:
        if not self.db_path.exists():
            raise SystemExit(f"DuckDB catalog not found: {self.db_path}")
        con = duckdb.connect(str(self.db_path))
        con.execute("SET TimeZone='America/Chicago'")
        return con

    def fetch_bar_files(self, con: duckdb.DuckDBPyConnection, family_override: Optional[str] = None) -> List[BarFile]:
        target_family = family_override or self.family
        rows = con.execute(
            """
            SELECT CAST(trade_date AS VARCHAR) AS trade_date, parquet_path
            FROM catalog.stage5_bar_files
            WHERE interval = ?
              AND family = ?
              AND file_exists = TRUE
              AND COALESCE(manifest_status, '') IN ('OK', 'SKIP_EXISTS')
              AND trade_date BETWEEN ?::DATE AND ?::DATE
            ORDER BY trade_date, parquet_path
            """,
            [self.interval, target_family, self.start_date.isoformat(), self.end_date.isoformat()],
        ).fetchall()
        files = [BarFile(trade_date=row[0], parquet_path=row[1]) for row in rows]
        if self.max_days is not None:
            files = files[: self.max_days]
        return files

    def select_instrument_key(self, con: duckdb.DuckDBPyConnection, path: str) -> Optional[str]:
        if self.instrument_mode == "single":
            if not self.instrument_key:
                raise ValueError("instrument_mode='single' requires instrument_key in the config.")
            rows = con.execute(
                """
                SELECT 1
                FROM read_parquet(?)
                WHERE CAST(instrument_key AS VARCHAR) = ?
                LIMIT 1
                """,
                [path, str(self.instrument_key)],
            ).fetchall()
            if rows:
                return str(self.instrument_key)
            if self.allow_missing_instrument:
                return None
            raise RuntimeError(f"Instrument '{self.instrument_key}' not found in {path}")

        if self.instrument_mode == "dominant_by_day":
            row = con.execute(
                """
                SELECT CAST(instrument_key AS VARCHAR) AS instrument_key, SUM(COALESCE(volume, 0)) AS day_volume
                FROM read_parquet(?)
                GROUP BY 1
                ORDER BY day_volume DESC, instrument_key
                LIMIT 1
                """,
                [path],
            ).fetchone()
            if row is None:
                return None
            return str(row[0])

        raise ValueError(f"Unknown instrument_mode '{self.instrument_mode}'.")

    def fetch_bars_for_day(self, con: duckdb.DuckDBPyConnection, path: str, instrument_key: str) -> List[Bar]:
        rows = con.execute(
            """
            SELECT
                family,
                yyyymmdd,
                CAST(instrument_key AS VARCHAR) AS instrument_key,
                bar_ts,
                CAST(open AS DOUBLE) AS open,
                CAST(high AS DOUBLE) AS high,
                CAST(low AS DOUBLE) AS low,
                CAST(close AS DOUBLE) AS close,
                CAST(COALESCE(volume, 0) AS DOUBLE) AS volume,
                CAST(COALESCE(trade_count, 0) AS BIGINT) AS trade_count
            FROM read_parquet(?)
            WHERE CAST(instrument_key AS VARCHAR) = ?
            ORDER BY bar_ts
            """,
            [path, instrument_key],
        ).fetchall()
        return [
            Bar(
                family=str(row[0]),
                yyyymmdd=str(row[1]),
                instrument_key=str(row[2]),
                bar_ts=coerce_datetime(row[3], self.session_tz),
                open=float(row[4]),
                high=float(row[5]),
                low=float(row[6]),
                close=float(row[7]),
                volume=float(row[8]),
                trade_count=int(row[9]),
            )
            for row in rows
        ]

    def _record_execution(self, bar_ts: datetime, instrument_key: str, qty_delta: int, reference_price: float, reason: str) -> None:
        if qty_delta == 0:
            return
        fill_price = reference_price + (math.copysign(self.slippage_ticks * self.tick_size, qty_delta))
        commission = abs(qty_delta) * self.commission_per_side
        slippage_cost = abs(qty_delta) * self.slippage_ticks * self.tick_size * self.contract_multiplier

        self.cash -= commission
        self.cash -= slippage_cost

        mae_points = None
        mfe_points = None
        mae_r = None
        mfe_r = None
        
        is_closing = self.position_qty != 0 and qty_delta != 0 and ((self.position_qty > 0 and qty_delta < 0) or (self.position_qty < 0 and qty_delta > 0))
        
        if is_closing:
            if self.open_trade_highest_high is None or fill_price > self.open_trade_highest_high:
                self.open_trade_highest_high = fill_price
            if self.open_trade_lowest_low is None or fill_price < self.open_trade_lowest_low:
                self.open_trade_lowest_low = fill_price
                
            entry_price = self.position_book.avg_entry_price
            if self.position_qty > 0:
                mae_points = max(0.0, entry_price - self.open_trade_lowest_low)
                mfe_points = max(0.0, self.open_trade_highest_high - entry_price)
            else:
                mae_points = max(0.0, self.open_trade_highest_high - entry_price)
                mfe_points = max(0.0, entry_price - self.open_trade_lowest_low)
                
            if self.open_initial_stop is not None:
                risk = abs(entry_price - self.open_initial_stop)
                if risk > 0:
                    mae_r = mae_points / risk
                    mfe_r = mfe_points / risk

        closed = self.position_book.apply_execution(
            ts=bar_ts.isoformat(),
            family=self.family,
            instrument_key=instrument_key,
            fill_price=fill_price,
            qty_delta=qty_delta,
            multiplier=self.contract_multiplier,
            commission_total=commission,
            slippage_total=slippage_cost,
            reason=reason,
            mae_points=mae_points,
            mfe_points=mfe_points,
            mae_r=mae_r,
            mfe_r=mfe_r,
            initial_stop_price=self.open_initial_stop if is_closing else None,
            initial_target_price=self.open_initial_target if is_closing else None,
            entry_trigger_price=self.open_entry_trigger if is_closing else None,
            bars_held=self.open_trade_bars_held if is_closing else None,
        )
        self.closed_trades.extend(closed)
        
        if self.position_qty == 0 and qty_delta != 0:
            self.open_trade_highest_high = fill_price
            self.open_trade_lowest_low = fill_price
            self.open_trade_bars_held = 0
            self.open_initial_stop = getattr(self.strategy, "initial_stop", None)
            self.open_initial_target = getattr(self.strategy, "target_price", None)
            self.open_entry_trigger = getattr(self.strategy, "original_entry_trigger", getattr(self.strategy, "entry_trigger", None))

        self.position_qty += qty_delta
        action = "BUY" if qty_delta > 0 else "SELL"
        self.executions.append(
            Execution(
                ts=bar_ts.isoformat(),
                family=self.family,
                instrument_key=instrument_key,
                action=action,
                qty_delta=qty_delta,
                fill_price=fill_price,
                reference_price=reference_price,
                commission=commission,
                slippage_cost=slippage_cost,
                position_after=self.position_qty,
                reason=reason,
            )
        )

    def _apply_open_pnl(self, bar: Bar) -> None:
        if self.last_close is None or self.position_qty == 0:
            return
        self.cash += self.position_qty * (bar.open - self.last_close) * self.contract_multiplier

    def _apply_intrabar_pnl(self, bar: Bar) -> None:
        if self.position_qty == 0:
            return
        self.cash += self.position_qty * (bar.close - bar.open) * self.contract_multiplier

    def _execute_pending_target(self, bar: Bar) -> None:
        if self.pending_target_qty == self.position_qty:
            return
        delta = self.pending_target_qty - self.position_qty
        self._record_execution(bar.bar_ts, bar.instrument_key, delta, bar.open, self.pending_target_reason)

    def _flatten_at_price(self, bar_ts: datetime, instrument_key: str, reference_price: float, reason: str) -> None:
        if self.position_qty == 0:
            self.pending_target_qty = 0
            return
        delta = -self.position_qty
        self._record_execution(bar_ts, instrument_key, delta, reference_price, reason)
        self.pending_target_qty = 0

    def _update_last_daily_row_after_forced_flatten(self) -> None:
        if not self.daily_rows or not self.day_info_rows:
            return
        start_equity = float(self.day_info_rows[-1]["day_equity_start"])
        last = self.daily_rows[-1]
        updated = DailyEquityRow(
            trade_date=last.trade_date,
            family=last.family,
            instrument_key=last.instrument_key,
            bars_in_session=last.bars_in_session,
            equity_close=self.cash,
            pnl_day=self.cash - start_equity,
            position_close=self.position_qty,
        )
        self.daily_rows[-1] = updated
        self.day_info_rows[-1]["equity_close"] = self.cash
        self.day_info_rows[-1]["pnl_day"] = self.cash - start_equity
        self.day_info_rows[-1]["position_close"] = self.position_qty

    def run(self) -> Dict[str, object]:
        con = self.connect()
        try:
            bar_files = self.fetch_bar_files(con)
            if not bar_files:
                raise SystemExit("No Stage 5 bar files found for this config.")

            context_bar_files = self.fetch_bar_files(con, self.context_family) if self.context_family else []
            ctx_file_map = {f.trade_date: f.parquet_path for f in context_bar_files}

            for idx, bar_file in enumerate(bar_files, start=1):
                instrument_key = self.select_instrument_key(con, bar_file.parquet_path)
                if instrument_key is None:
                    logging.warning("[SKIP] %s no instrument selected for %s", bar_file.trade_date, bar_file.parquet_path)
                    continue

                if self.active_instrument_key and instrument_key != self.active_instrument_key and self.last_bar is not None:
                    logging.info(
                        "[ROLL] flattening prior position because instrument changed %s -> %s on %s",
                        self.active_instrument_key,
                        instrument_key,
                        bar_file.trade_date,
                    )
                    self._flatten_at_price(
                        bar_ts=self.last_bar.bar_ts,
                        instrument_key=self.active_instrument_key,
                        reference_price=self.last_bar.close,
                        reason=ExitReason.INSTRUMENT_ROLL.value,
                    )
                    self._update_last_daily_row_after_forced_flatten()

                self.active_instrument_key = instrument_key
                bars = self.fetch_bars_for_day(con, bar_file.parquet_path, instrument_key)

                context_bars: List[Bar] = []
                ctx_bars_map: Dict[datetime, Bar] = {}
                if self.context_family:
                    ctx_path = ctx_file_map.get(bar_file.trade_date)
                    if ctx_path:
                        ctx_key = self.select_instrument_key(con, ctx_path)
                        if ctx_key:
                            context_bars = self.fetch_bars_for_day(con, ctx_path, ctx_key)
                            ctx_bars_map = {b.bar_ts: b for b in context_bars}

                day_equity_start = self.cash
                session_bars = 0

                logging.info("[DAY %s/%s] %s instrument=%s bars=%s", idx, len(bar_files), bar_file.trade_date, instrument_key, len(bars))

                for bar in bars:
                    if not within_session(bar.bar_ts, self.session_tz, self.session_start, self.session_end):
                        continue
                    
                    context_bar = ctx_bars_map.get(bar.bar_ts) if self.context_family else None

                    session_bars += 1
                    self._apply_open_pnl(bar)
                    self._execute_pending_target(bar)
                    self._apply_intrabar_pnl(bar)

                    if self.position_qty != 0:
                        self.open_trade_bars_held += 1
                        high = float(bar.high)
                        low = float(bar.low)
                        if self.open_trade_highest_high is None or high > self.open_trade_highest_high:
                            self.open_trade_highest_high = high
                        if self.open_trade_lowest_low is None or low < self.open_trade_lowest_low:
                            self.open_trade_lowest_low = low

                    if getattr(self.strategy, "uses_context_bar", False):
                        next_target = self.strategy.on_bar(bar, self.position_qty, context_bar=context_bar)
                    else:
                        next_target = self.strategy.on_bar(bar, self.position_qty)

                    # Inject per-bar MNQ leg P&L from spread strategies
                    ctx_cash_delta = getattr(self.strategy, "context_leg_cash_delta", 0.0)
                    if ctx_cash_delta:
                        self.cash += ctx_cash_delta
                        self.strategy.context_leg_cash_delta = 0.0  # type: ignore[attr-defined]

                    # Flush informational MNQ executions from spread strategies
                    ctx_execs: List[Dict[str, object]] = getattr(self.strategy, "context_executions", [])
                    if ctx_execs:
                        for _ex in ctx_execs:
                            self.executions.append(
                                Execution(
                                    ts=str(_ex["ts"]),
                                    family=self.family,
                                    instrument_key=str(_ex["instrument_key"]),
                                    action=str(_ex["action"]),
                                    qty_delta=int(_ex["qty_delta"]),
                                    fill_price=float(_ex["fill_price"]),
                                    reference_price=float(_ex["fill_price"]),
                                    commission=0.0,
                                    slippage_cost=0.0,
                                    position_after=0,
                                    reason=str(_ex["reason"]),
                                )
                            )
                        self.strategy.context_executions = []  # type: ignore[attr-defined]

                    if self.position_qty != 0:
                        if self.open_initial_stop is None:
                            self.open_initial_stop = getattr(self.strategy, "initial_stop", None)
                        if self.open_initial_target is None:
                            self.open_initial_target = getattr(self.strategy, "target_price", None)
                        if self.open_entry_trigger is None:
                            self.open_entry_trigger = getattr(self.strategy, "original_entry_trigger", getattr(self.strategy, "entry_trigger", None))
                    
                    reason = ExitReason.SIGNAL_REVERSAL.value
                    if next_target == 0 and self.position_qty != 0:
                        strat = self.strategy
                        # Strategy-agnostic override natively provided by strategy
                        strat_provided_reason = getattr(strat, "exit_reason", None)
                        if strat_provided_reason:
                            reason = strat_provided_reason
                        else:
                            # Fallback implicit inference
                            reason = ExitReason.STRATEGY_EXIT.value
                            price = float(bar.close)
                            target_price = getattr(strat, "target_price", None)
                            if target_price is not None:
                                if (self.position_qty > 0 and price >= target_price) or (self.position_qty < 0 and price <= target_price):
                                    reason = ExitReason.TARGET.value
                            
                            time_stop = getattr(strat, "time_stop", None)
                            if time_stop is not None and _bar_local_time(bar, self.session_tz) >= time_stop:
                                reason = ExitReason.TIME_STOP.value
                            
                            active_stop = getattr(strat, "active_stop", None)
                            initial_stop = getattr(strat, "initial_stop", None)
                            if active_stop is not None:
                                if (self.position_qty > 0 and price <= active_stop) or (self.position_qty < 0 and price >= active_stop):
                                    if active_stop == initial_stop:
                                        reason = ExitReason.INITIAL_STOP.value
                                    elif getattr(strat, "cost_protected", False) and active_stop <= getattr(strat, "highest_close_since_entry", float('inf')):
                                        if getattr(strat, "trail_active", False):
                                            reason = ExitReason.TRAILING_STOP.value
                                        else:
                                            reason = ExitReason.COST_PROTECT.value
                                            
                            if reason == ExitReason.STRATEGY_EXIT.value and initial_stop is not None:
                                 if (self.position_qty > 0 and price <= initial_stop) or (self.position_qty < 0 and price >= initial_stop):
                                     reason = ExitReason.INITIAL_STOP.value

                    self.pending_target_qty = int(next_target) if next_target is not None else 0
                    self.pending_target_reason = reason
                    self.last_close = bar.close
                    self.last_bar = bar

                if session_bars == 0:
                    logging.warning("[DAY] %s had zero bars in session after filtering", bar_file.trade_date)
                    continue

                if self.flatten_daily and self.last_bar is not None and self.position_qty != 0:
                    self._flatten_at_price(
                        bar_ts=self.last_bar.bar_ts,
                        instrument_key=instrument_key,
                        reference_price=self.last_bar.close,
                        reason=ExitReason.DAILY_FLATTEN.value,
                    )

                equity_close = self.cash
                pnl_day = equity_close - day_equity_start
                self.daily_rows.append(
                    DailyEquityRow(
                        trade_date=bar_file.trade_date,
                        family=self.family,
                        instrument_key=instrument_key,
                        bars_in_session=session_bars,
                        equity_close=equity_close,
                        pnl_day=pnl_day,
                        position_close=self.position_qty,
                    )
                )
                self.day_info_rows.append(
                    {
                        "trade_date": bar_file.trade_date,
                        "family": self.family,
                        "instrument_key": instrument_key,
                        "bars_in_session": session_bars,
                        "day_equity_start": day_equity_start,
                        "equity_close": equity_close,
                        "pnl_day": pnl_day,
                        "position_close": self.position_qty,
                    }
                )
        finally:
            con.close()

        if self.flatten_on_last_bar and self.position_qty != 0 and self.last_bar is not None:
            logging.info("[FINAL] flattening final position at last close")
            self._flatten_at_price(
                bar_ts=self.last_bar.bar_ts,
                instrument_key=self.last_bar.instrument_key,
                reference_price=self.last_bar.close,
                reason=ExitReason.FINAL_FLATTEN.value,
            )
            self._update_last_daily_row_after_forced_flatten()

        summary = self.build_summary()
        self.write_outputs(summary)
        self.write_to_duckdb(summary)
        logging.info("[DONE] Stage 6 backtest complete run_id=%s", self.run_id)
        logging.info(json.dumps(summary, indent=2))
        return summary

    def build_summary(self) -> Dict[str, object]:
        equities = [row.equity_close for row in self.daily_rows] or [self.cash]
        max_drawdown_abs, max_drawdown_pct = compute_max_drawdown(equities)
        daily_returns = []
        for i in range(1, len(equities)):
            prev = equities[i - 1]
            if prev != 0:
                daily_returns.append((equities[i] / prev) - 1.0)
        sharpe = None
        if len(daily_returns) >= 2:
            std = statistics.stdev(daily_returns)
            if std > 0:
                sharpe = (statistics.fmean(daily_returns) / std) * math.sqrt(252)

        closed_trade_count = len(self.closed_trades)
        wins = sum(1 for trade in self.closed_trades if trade.net_pnl > 0)
        gross_profit = sum(max(trade.net_pnl, 0.0) for trade in self.closed_trades)
        gross_loss = -sum(min(trade.net_pnl, 0.0) for trade in self.closed_trades)
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else None

        return {
            "run_id": self.run_id,
            "report_dir": str(self.report_dir),
            "family": self.family,
            "interval": self.interval,
            "strategy": self.strategy_name,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "instrument_mode": self.instrument_mode,
            "instrument_key": self.instrument_key,
            "initial_cash": self.initial_cash,
            "final_equity": self.cash,
            "net_pnl": self.cash - self.initial_cash,
            "total_return_pct": ((self.cash / self.initial_cash) - 1.0) * 100.0 if self.initial_cash else None,
            "max_drawdown_abs": max_drawdown_abs,
            "max_drawdown_pct": max_drawdown_pct,
            "daily_sharpe_approx": sharpe,
            "days_tested": len(self.daily_rows),
            "execution_count": len(self.executions),
            "closed_trade_count": closed_trade_count,
            "win_rate_pct": (wins / closed_trade_count * 100.0) if closed_trade_count else None,
            "gross_profit": gross_profit,
            "gross_loss": gross_loss,
            "profit_factor": profit_factor,
            "config": self.config,
            "created_at": datetime.now().astimezone().isoformat(),
        }

    def write_outputs(self, summary: Dict[str, object]) -> None:
        ensure_dir(self.report_dir)

        with (self.report_dir / "summary.json").open("w", encoding="utf-8") as fh:
            json.dump(summary, fh, indent=2)

        with (self.report_dir / "config_used.json").open("w", encoding="utf-8") as fh:
            json.dump(self.config, fh, indent=2)

        if self.write_daily_equity_csv:
            with (self.report_dir / "daily_equity.csv").open("w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(
                    fh,
                    fieldnames=["trade_date", "family", "instrument_key", "bars_in_session", "equity_close", "pnl_day", "position_close"],
                )
                writer.writeheader()
                for row in self.daily_rows:
                    writer.writerow(
                        {
                            "trade_date": row.trade_date,
                            "family": row.family,
                            "instrument_key": row.instrument_key,
                            "bars_in_session": row.bars_in_session,
                            "equity_close": row.equity_close,
                            "pnl_day": row.pnl_day,
                            "position_close": row.position_close,
                        }
                    )

        if self.write_executions_csv:
            with (self.report_dir / "executions.csv").open("w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(
                    fh,
                    fieldnames=[
                        "ts",
                        "family",
                        "instrument_key",
                        "action",
                        "qty_delta",
                        "fill_price",
                        "reference_price",
                        "commission",
                        "slippage_cost",
                        "position_after",
                        "reason",
                    ],
                )
                writer.writeheader()
                for row in self.executions:
                    writer.writerow(
                        {
                            "ts": row.ts,
                            "family": row.family,
                            "instrument_key": row.instrument_key,
                            "action": row.action,
                            "qty_delta": row.qty_delta,
                            "fill_price": row.fill_price,
                            "reference_price": row.reference_price,
                            "commission": row.commission,
                            "slippage_cost": row.slippage_cost,
                            "position_after": row.position_after,
                            "reason": row.reason,
                        }
                    )

        if self.write_closed_trades_csv:
            with (self.report_dir / "closed_trades.csv").open("w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(
                    fh,
                    fieldnames=[
                        "entry_ts",
                        "exit_ts",
                        "family",
                        "instrument_key",
                        "side",
                        "qty",
                        "entry_price",
                        "exit_price",
                        "gross_pnl",
                        "commission",
                        "slippage_cost",
                        "net_pnl",
                        "mae_points",
                        "mfe_points",
                        "mae_r",
                        "mfe_r",
                        "exit_reason",
                        "initial_stop_price",
                        "initial_target_price",
                        "entry_trigger_price",
                        "bars_held",
                    ],
                )
                writer.writeheader()
                for row in self.closed_trades:
                    writer.writerow(
                        {
                            "entry_ts": row.entry_ts,
                            "exit_ts": row.exit_ts,
                            "family": row.family,
                            "instrument_key": row.instrument_key,
                            "side": row.side,
                            "qty": row.qty,
                            "entry_price": row.entry_price,
                            "exit_price": row.exit_price,
                            "gross_pnl": row.gross_pnl,
                            "commission": row.commission,
                            "slippage_cost": row.slippage_cost,
                            "net_pnl": row.net_pnl,
                            "mae_points": row.mae_points,
                            "mfe_points": row.mfe_points,
                            "mae_r": row.mae_r,
                            "mfe_r": row.mfe_r,
                            "exit_reason": row.exit_reason,
                            "initial_stop_price": row.initial_stop_price,
                            "initial_target_price": row.initial_target_price,
                            "entry_trigger_price": row.entry_trigger_price,
                            "bars_held": row.bars_held,
                        }
                    )

    def write_to_duckdb(self, summary: Dict[str, object]) -> None:
        con = duckdb.connect(str(self.db_path))
        try:
            con.execute("CREATE SCHEMA IF NOT EXISTS backtest")
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS backtest.runs (
                    run_id VARCHAR,
                    created_at TIMESTAMPTZ,
                    family VARCHAR,
                    interval VARCHAR,
                    strategy VARCHAR,
                    start_date DATE,
                    end_date DATE,
                    instrument_mode VARCHAR,
                    instrument_key VARCHAR,
                    initial_cash DOUBLE,
                    final_equity DOUBLE,
                    net_pnl DOUBLE,
                    total_return_pct DOUBLE,
                    max_drawdown_abs DOUBLE,
                    max_drawdown_pct DOUBLE,
                    daily_sharpe_approx DOUBLE,
                    days_tested BIGINT,
                    execution_count BIGINT,
                    closed_trade_count BIGINT,
                    win_rate_pct DOUBLE,
                    gross_profit DOUBLE,
                    gross_loss DOUBLE,
                    profit_factor DOUBLE,
                    report_dir VARCHAR,
                    config_json VARCHAR
                )
                """
            )
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS backtest.daily_equity (
                    run_id VARCHAR,
                    trade_date DATE,
                    family VARCHAR,
                    instrument_key VARCHAR,
                    bars_in_session BIGINT,
                    equity_close DOUBLE,
                    pnl_day DOUBLE,
                    position_close BIGINT
                )
                """
            )
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS backtest.executions (
                    run_id VARCHAR,
                    ts TIMESTAMPTZ,
                    family VARCHAR,
                    instrument_key VARCHAR,
                    action VARCHAR,
                    qty_delta BIGINT,
                    fill_price DOUBLE,
                    reference_price DOUBLE,
                    commission DOUBLE,
                    slippage_cost DOUBLE,
                    position_after BIGINT,
                    reason VARCHAR
                )
                """
            )
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS backtest.closed_trades (
                    run_id VARCHAR,
                    entry_ts TIMESTAMPTZ,
                    exit_ts TIMESTAMPTZ,
                    family VARCHAR,
                    instrument_key VARCHAR,
                    side VARCHAR,
                    qty BIGINT,
                    entry_price DOUBLE,
                    exit_price DOUBLE,
                    gross_pnl DOUBLE,
                    commission DOUBLE,
                    slippage_cost DOUBLE,
                    net_pnl DOUBLE
                )
                """
            )

            con.execute(
                """
                INSERT INTO backtest.runs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    self.run_id,
                    summary["created_at"],
                    self.family,
                    self.interval,
                    self.strategy_name,
                    self.start_date.isoformat(),
                    self.end_date.isoformat(),
                    self.instrument_mode,
                    str(self.instrument_key) if self.instrument_key is not None else None,
                    self.initial_cash,
                    summary["final_equity"],
                    summary["net_pnl"],
                    summary["total_return_pct"],
                    summary["max_drawdown_abs"],
                    summary["max_drawdown_pct"],
                    summary["daily_sharpe_approx"],
                    summary["days_tested"],
                    summary["execution_count"],
                    summary["closed_trade_count"],
                    summary["win_rate_pct"],
                    summary["gross_profit"],
                    summary["gross_loss"],
                    summary["profit_factor"],
                    str(self.report_dir),
                    json.dumps(self.config, ensure_ascii=False),
                ],
            )

            if self.daily_rows:
                con.executemany(
                    """
                    INSERT INTO backtest.daily_equity VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    [
                        (
                            self.run_id,
                            row.trade_date,
                            row.family,
                            row.instrument_key,
                            row.bars_in_session,
                            row.equity_close,
                            row.pnl_day,
                            row.position_close,
                        )
                        for row in self.daily_rows
                    ],
                )

            if self.executions:
                con.executemany(
                    """
                    INSERT INTO backtest.executions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    [
                        (
                            self.run_id,
                            row.ts,
                            row.family,
                            row.instrument_key,
                            row.action,
                            row.qty_delta,
                            row.fill_price,
                            row.reference_price,
                            row.commission,
                            row.slippage_cost,
                            row.position_after,
                            row.reason,
                        )
                        for row in self.executions
                    ],
                )

            if self.closed_trades:
                con.executemany(
                    """
                    INSERT INTO backtest.closed_trades VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    [
                        (
                            self.run_id,
                            row.entry_ts,
                            row.exit_ts,
                            row.family,
                            row.instrument_key,
                            row.side,
                            row.qty,
                            row.entry_price,
                            row.exit_price,
                            row.gross_pnl,
                            row.commission,
                            row.slippage_cost,
                            row.net_pnl,
                        )
                        for row in self.closed_trades
                    ],
                )
        finally:
            con.close()


def compute_max_drawdown(equities: Sequence[float]) -> Tuple[float, Optional[float]]:
    peak = None
    max_drawdown_abs = 0.0
    max_drawdown_pct: Optional[float] = None
    for equity in equities:
        if peak is None or equity > peak:
            peak = equity
        if peak is None:
            continue
        drawdown_abs = peak - equity
        drawdown_pct = (drawdown_abs / peak * 100.0) if peak != 0 else None
        if drawdown_abs > max_drawdown_abs:
            max_drawdown_abs = drawdown_abs
            max_drawdown_pct = drawdown_pct
    return max_drawdown_abs, max_drawdown_pct


def load_config(path: Path) -> Dict[str, object]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    required = ["db_path", "reports_root", "family", "interval", "start_date", "end_date"]
    missing = [key for key in required if key not in data]
    if missing:
        raise SystemExit(f"Missing required config keys: {missing}")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Stage 6 replay/backtest runner on Stage 5 bars")
    parser.add_argument(
        "--config",
        required=True,
        help=r"Path to backtest config JSON, e.g. configs\backtest_sma_cross_1m.json",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    
    # Import the new logger wrapper
    from research_logger import log_experiment

    config_data = {}
    
    try:
        config_data = load_config(Path(args.config))
        engine = BacktestEngine(config_data)
        summary = engine.run()
        print("STAGE6_BACKTEST DONE")
        print(json.dumps(summary, indent=2))
        
        # Log successful run to research log
        log_experiment(config=config_data, result=summary, config_path=args.config)
        
    except Exception as e:
        # Log the failed run to the research log, passing whatever config could be parsed and the error
        log_experiment(config=config_data, error_msg=str(e), config_path=args.config)
        # Re-raise the exact exception to fail the process and preserve traceback
        raise


if __name__ == "__main__":
    main()