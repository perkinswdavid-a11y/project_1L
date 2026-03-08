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
    def on_open(self, bar: Bar, current_position: int, pending_target: int) -> int:
        return pending_target

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

        self.pending_long_entry = False
        self.entry_price: Optional[float] = None
        self.initial_stop: Optional[float] = None
        self.active_stop: Optional[float] = None
        self.risk_per_contract: Optional[float] = None
        self.best_high_since_entry: Optional[float] = None
        self.highest_close_since_entry: Optional[float] = None
        self.cost_protected = False
        self.trail_active = False

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

    def _roll_day(self, new_day: str) -> None:
        if self.current_day is not None and self.current_day_or_width is not None and self.current_day_or_width > 0:
            self.prior_or_widths.append(self.current_day_or_width)

        self.current_day = new_day
        self.or_high = None
        self.or_low = None
        self.current_day_or_width = None
        self.traded_today = False
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
            self.traded_today = True
            self.pending_long_entry = True
            return self.position_size

        return current_position



class OpeningRangeBreakoutV3Strategy(OpeningRangeBreakoutV2Strategy):
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
        entry_trigger_mode: str = "close",
        or_close_location_min: float = 0.60,
        max_initial_risk_ticks: float = 60.0,
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

        trigger_mode = str(entry_trigger_mode).strip().lower()
        if trigger_mode not in {"touch", "close"}:
            raise ValueError("entry_trigger_mode must be either 'touch' or 'close'.")
        if not 0.0 <= float(or_close_location_min) <= 1.0:
            raise ValueError("or_close_location_min must be between 0.0 and 1.0.")
        if float(max_initial_risk_ticks) <= 0:
            raise ValueError("max_initial_risk_ticks must be > 0.")

        self.entry_trigger_mode = trigger_mode
        self.or_close_location_min = float(or_close_location_min)
        self.max_initial_risk_ticks = float(max_initial_risk_ticks)
        self.or_close: Optional[float] = None

    def _roll_day(self, new_day: str) -> None:
        super()._roll_day(new_day)
        self.or_close = None

    def _or_close_location_passes(self) -> bool:
        if self.or_close_location_min <= 0:
            return True
        if (
            self.or_high is None
            or self.or_low is None
            or self.or_close is None
            or self.current_day_or_width is None
            or self.current_day_or_width <= 0
        ):
            return False
        close_location = (self.or_close - self.or_low) / self.current_day_or_width
        return close_location >= self.or_close_location_min

    def on_open(self, bar: Bar, current_position: int, pending_target: int) -> int:
        if not self.pending_long_entry or pending_target <= current_position:
            return pending_target

        local_time = _bar_local_time(bar, self.tz)
        if local_time >= self.no_new_entries_after:
            self._clear_trade_state()
            return current_position

        if self.or_low is None:
            self._clear_trade_state()
            return current_position

        candidate_entry_price = float(bar.open) + (self.slippage_ticks * self.tick_size)
        initial_stop = self.or_low - (self.stop_buffer_ticks * self.tick_size)
        risk_points = candidate_entry_price - initial_stop
        if risk_points <= 0:
            self._clear_trade_state()
            return current_position

        risk_ticks = risk_points / self.tick_size if self.tick_size > 0 else float("inf")
        if risk_ticks > self.max_initial_risk_ticks + 1e-9:
            self._clear_trade_state()
            return current_position

        return pending_target

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
            self.or_close = price
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
        if not self._or_close_location_passes():
            return current_position
        if local_time >= self.no_new_entries_after:
            return current_position

        entry_trigger = self.or_high + (self.entry_buffer_ticks * self.tick_size)
        breakout_confirmed = (
            float(bar.high) >= entry_trigger
            if self.entry_trigger_mode == "touch"
            else price > entry_trigger
        )
        if breakout_confirmed:
            self.traded_today = True
            self.pending_long_entry = True
            return self.position_size

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


def build_strategy(strategy_name: str, params: Dict[str, object]) -> Strategy:
    name = strategy_name.strip().lower()

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

    if name == "momentum_pullback":
        return MomentumPullbackStrategy(
            fast=int(params.get("fast", 20)),
            slow=int(params.get("slow", 50)),
            entry_buffer_ticks=float(params.get("entry_buffer_ticks", 1.0)),
            position_size=int(params.get("position_size", 1)),
            tick_size=float(params.get("tick_size", 0.25)),
            allow_short=bool(params.get("allow_short", True)),
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
            timezone=str(params.get("timezone", "America/Chicago")),
            or_width_lookback_days=int(params.get("or_width_lookback_days", 20)),
            or_width_min_factor=float(params.get("or_width_min_factor", 0.5)),
            or_width_max_factor=float(params.get("or_width_max_factor", 2.0)),
            cost_protect_trigger_r=float(params.get("cost_protect_trigger_r", 1.25)),
            trail_activate_r=float(params.get("trail_activate_r", 2.0)),
            atr_period=int(params.get("atr_period", 20)),
            atr_trail_multiple=float(params.get("atr_trail_multiple", 3.0)),
            slippage_ticks=float(params.get("slippage_ticks", 1.0)),
            commission_per_side=float(params.get("commission_per_side", 1.25)),
            contract_multiplier=float(params.get("contract_multiplier", 5.0)),
        )

    if name in {"opening_range_breakout_v3", "orb_v3"}:
        return OpeningRangeBreakoutV3Strategy(
            range_minutes=int(params.get("range_minutes", 15)),
            entry_buffer_ticks=float(params.get("entry_buffer_ticks", 1.0)),
            stop_buffer_ticks=float(params.get("stop_buffer_ticks", 1.0)),
            position_size=int(params.get("position_size", 1)),
            tick_size=float(params.get("tick_size", 0.25)),
            session_open=str(params.get("session_open", "08:30")),
            no_new_entries_after=str(params.get("no_new_entries_after", "11:00")),
            time_stop=str(params.get("time_stop", "13:30")),
            allow_long=bool(params.get("allow_long", True)),
            timezone=str(params.get("timezone", "America/Chicago")),
            or_width_lookback_days=int(params.get("or_width_lookback_days", 20)),
            or_width_min_factor=float(params.get("or_width_min_factor", 0.5)),
            or_width_max_factor=float(params.get("or_width_max_factor", 2.0)),
            cost_protect_trigger_r=float(params.get("cost_protect_trigger_r", 1.25)),
            trail_activate_r=float(params.get("trail_activate_r", 2.0)),
            atr_period=int(params.get("atr_period", 20)),
            atr_trail_multiple=float(params.get("atr_trail_multiple", 3.0)),
            slippage_ticks=float(params.get("slippage_ticks", 1.0)),
            commission_per_side=float(params.get("commission_per_side", 1.25)),
            contract_multiplier=float(params.get("contract_multiplier", 5.0)),
            entry_trigger_mode=str(params.get("entry_trigger_mode", "close")),
            or_close_location_min=float(params.get("or_close_location_min", 0.60)),
            max_initial_risk_ticks=float(params.get("max_initial_risk_ticks", 60.0)),
        )

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

    def fetch_bar_files(self, con: duckdb.DuckDBPyConnection) -> List[BarFile]:
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
            [self.interval, self.family, self.start_date.isoformat(), self.end_date.isoformat()],
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

        closed = self.position_book.apply_execution(
            ts=bar_ts.isoformat(),
            family=self.family,
            instrument_key=instrument_key,
            fill_price=fill_price,
            qty_delta=qty_delta,
            multiplier=self.contract_multiplier,
            commission_total=commission,
            slippage_total=slippage_cost,
        )
        self.closed_trades.extend(closed)

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
        self._record_execution(bar.bar_ts, bar.instrument_key, delta, bar.open, "signal_from_prior_close")

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
                        reason="instrument_roll_change",
                    )
                    self._update_last_daily_row_after_forced_flatten()

                self.active_instrument_key = instrument_key
                bars = self.fetch_bars_for_day(con, bar_file.parquet_path, instrument_key)
                day_equity_start = self.cash
                session_bars = 0

                logging.info("[DAY %s/%s] %s instrument=%s bars=%s", idx, len(bar_files), bar_file.trade_date, instrument_key, len(bars))

                for bar in bars:
                    if not within_session(bar.bar_ts, self.session_tz, self.session_start, self.session_end):
                        continue
                    session_bars += 1
                    self._apply_open_pnl(bar)
                    self.pending_target_qty = int(
                        self.strategy.on_open(bar, self.position_qty, self.pending_target_qty)
                    )
                    self._execute_pending_target(bar)
                    self._apply_intrabar_pnl(bar)

                    next_target = self.strategy.on_bar(bar, self.position_qty)
                    self.pending_target_qty = int(next_target)
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
                        reason="daily_flatten",
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
                reason="final_flatten",
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