from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional


@dataclass
class ILHTrade:
    entry_ts: datetime
    side: str  # 'LONG' or 'SHORT'
    qty: int
    entry_price: float

    stop_loss: float
    take_profit: float

    exit_ts: Optional[datetime] = None
    exit_price: Optional[float] = None
    status: str = "OPEN"
    pnl: float = 0.0

    # For trailing stop logic
    peak_favorable_price: float = 0.0  # high for long, low for short


class ILHBacktester:
    """
    High-fidelity execution simulator for ILH-001, focused on realistic friction and clean tick handling.

    Major differences vs. prior v1:
      - Uses bid/ask (BBO) for stop/target evaluation (more realistic than last trade or mixed 'price' field).
      - Moves ghost filtering to BBO jump detection (avoids 'ignoring' real adverse moves vs entry).
      - Optional time-stop to reduce chop/commission churn.
      - Parameterized slippage & commission with qty support.
      - INTEGRATED: Directional Bias (Trend Filter) preserved from V1.1 development.

    This remains a simplified simulator (not a full order-management emulator).
    """

    def __init__(
        self,
        *,
        initial_cash: float = 100000.0,
        qty: int = 1,
        contract_multiplier: float = 5.0,  # MES = $5 * index point
        tick_size: float = 0.25,
        commission_per_side: float = 1.25,  # per contract, per side
        entry_slip_ticks: int = 1,          # includes "paying the spread" assumption
        exit_slip_ticks_stop: int = 1,      # stop orders can slip
        exit_slip_ticks_target: int = 0,    # assume limit target (0 slip)
        max_bbo_jump_points: float = 15.0,  # silicon shield at the BBO level
        time_stop_s: Optional[float] = 90.0,
        time_stop_min_favorable_pts: float = 1.0,
        breakeven_trigger_pts: float = 1.5,
        trail_trigger_pts: float = 3.0,
        trail_distance_pts: float = 2.0,
        stop_pts: float = 5.0,
        target_pts: float = 20.0,
        surge_threshold: int = 250,
    ):
        self.cash = float(initial_cash)
        self.qty = int(qty)
        self.multiplier = float(contract_multiplier)
        self.tick_size = float(tick_size)

        self.commission_per_side = float(commission_per_side)
        self.entry_slip_ticks = int(entry_slip_ticks)
        self.exit_slip_ticks_stop = int(exit_slip_ticks_stop)
        self.exit_slip_ticks_target = int(exit_slip_ticks_target)

        self.max_bbo_jump_points = float(max_bbo_jump_points)

        self.time_stop = timedelta(seconds=float(time_stop_s)) if time_stop_s is not None else None
        self.time_stop_min_fav = float(time_stop_min_favorable_pts)

        self.breakeven_trigger = float(breakeven_trigger_pts)
        self.trail_trigger = float(trail_trigger_pts)
        self.trail_distance = float(trail_distance_pts)

        self.stop_pts = float(stop_pts)
        self.target_pts = float(target_pts)
        self.surge_threshold = surge_threshold

        self.trades: List[ILHTrade] = []
        self.active_trade: Optional[ILHTrade] = None

        # last valid BBO for ghost filtering
        self._last_bid: Optional[float] = None
        self._last_ask: Optional[float] = None

    def _round_to_tick(self, px: float) -> float:
        return round(px / self.tick_size) * self.tick_size

    def _apply_slippage(self, px: float, *, action: str, ticks: int) -> float:
        if ticks <= 0:
            return px
        slip = ticks * self.tick_size
        if action == "BUY":
            return self._round_to_tick(px + slip)
        if action == "SELL":
            return self._round_to_tick(px - slip)
        return px

    def process_signal(self, signal: Dict, event_ts: datetime, opening_price: float):
        if self.active_trade or opening_price == 0:
            return

        s_type = signal.get("type")
        mnq_surge = int(signal.get("mnq_surge") or 0)

        # TREND FILTER (Directional Bias)
        current_price = signal['price']
        is_uptrend = current_price > opening_price
        is_downtrend = current_price < opening_price

        is_long = (s_type == "ABSORPTION_BUYING") and (mnq_surge > self.surge_threshold) and is_uptrend
        is_short = (s_type == "ABSORPTION_SELLING") and (mnq_surge < -self.surge_threshold) and is_downtrend
        
        if not (is_long or is_short):
            return

        side = "LONG" if is_long else "SHORT"

        bid = float(signal.get("bid") or 0.0)
        ask = float(signal.get("ask") or 0.0)
        if bid <= 0.0 or ask <= 0.0:
            return

        if side == "LONG":
            entry_px = self._apply_slippage(ask, action="BUY", ticks=self.entry_slip_ticks)
            stop = self._round_to_tick(entry_px - self.stop_pts)
            target = self._round_to_tick(entry_px + self.target_pts)
        else:
            entry_px = self._apply_slippage(bid, action="SELL", ticks=self.entry_slip_ticks)
            stop = self._round_to_tick(entry_px + self.stop_pts)
            target = self._round_to_tick(entry_px - self.target_pts)

        self.active_trade = ILHTrade(
            entry_ts=event_ts,
            side=side,
            qty=self.qty,
            entry_price=entry_px,
            stop_loss=stop,
            take_profit=target,
        )

    def update_from_bbo(self, bid: float, ask: float, ts: datetime):
        if not self.active_trade:
            self._last_bid = bid
            self._last_ask = ask
            return

        if bid <= 0.0 or ask <= 0.0:
            return

        # Silicon Shield: ignore impossible BBO jumps (data-quality protection)
        if self._last_bid is not None and abs(bid - self._last_bid) > self.max_bbo_jump_points:
            return
        if self._last_ask is not None and abs(ask - self._last_ask) > self.max_bbo_jump_points:
            return

        self._last_bid = bid
        self._last_ask = ask

        trade = self.active_trade
        mark = bid if trade.side == "LONG" else ask  # exit-side mark

        if trade.side == "LONG":
            if trade.peak_favorable_price == 0.0 or mark > trade.peak_favorable_price:
                trade.peak_favorable_price = mark

                if (trade.peak_favorable_price - trade.entry_price) >= self.breakeven_trigger:
                    if trade.stop_loss < trade.entry_price:
                        trade.stop_loss = self._round_to_tick(trade.entry_price)

                if (trade.peak_favorable_price - trade.entry_price) >= self.trail_trigger:
                    new_stop = self._round_to_tick(trade.peak_favorable_price - self.trail_distance)
                    if new_stop > trade.stop_loss:
                        trade.stop_loss = new_stop

            if self.time_stop is not None:
                age = ts - trade.entry_ts
                mfe = trade.peak_favorable_price - trade.entry_price
                
                # Hybrid rule: If down > 2.0 points, the 'patience clock' drops to 30s
                current_pnl_pts = mark - trade.entry_price
                effective_time_stop = self.time_stop
                if current_pnl_pts <= -2.0:
                    effective_time_stop = timedelta(seconds=30)

                if age >= effective_time_stop and mfe < self.time_stop_min_fav:
                    self._close_trade(ts, mark, reason="TIME_STOP")
                    return

            if mark <= trade.stop_loss:
                fill = self._apply_slippage(trade.stop_loss, action="SELL", ticks=self.exit_slip_ticks_stop)
                self._close_trade(ts, fill, reason="STOP/TRAIL")
            elif mark >= trade.take_profit:
                fill = self._apply_slippage(trade.take_profit, action="SELL", ticks=self.exit_slip_ticks_target)
                self._close_trade(ts, fill, reason="TARGET")

        else:
            if trade.peak_favorable_price == 0.0 or mark < trade.peak_favorable_price:
                trade.peak_favorable_price = mark

                if (trade.entry_price - trade.peak_favorable_price) >= self.breakeven_trigger:
                    if trade.stop_loss > trade.entry_price:
                        trade.stop_loss = self._round_to_tick(trade.entry_price)

                if (trade.entry_price - trade.peak_favorable_price) >= self.trail_trigger:
                    new_stop = self._round_to_tick(trade.peak_favorable_price + self.trail_distance)
                    if new_stop < trade.stop_loss:
                        trade.stop_loss = new_stop

            if self.time_stop is not None:
                age = ts - trade.entry_ts
                mfe = trade.entry_price - trade.peak_favorable_price
                
                # Hybrid rule for Short: down > 2.0 points (price matches entry + 2.0)
                current_pnl_pts = trade.entry_price - mark
                effective_time_stop = self.time_stop
                if current_pnl_pts <= -2.0:
                    effective_time_stop = timedelta(seconds=30)

                if age >= effective_time_stop and mfe < self.time_stop_min_fav:
                    self._close_trade(ts, mark, reason="TIME_STOP")
                    return

            if mark >= trade.stop_loss:
                fill = self._apply_slippage(trade.stop_loss, action="BUY", ticks=self.exit_slip_ticks_stop)
                self._close_trade(ts, fill, reason="STOP/TRAIL")
            elif mark <= trade.take_profit:
                fill = self._apply_slippage(trade.take_profit, action="BUY", ticks=self.exit_slip_ticks_target)
                self._close_trade(ts, fill, reason="TARGET")

    def _close_trade(self, ts: datetime, fill_price: float, reason: str):
        trade = self.active_trade
        if trade is None:
            return

        trade.exit_ts = ts
        trade.exit_price = float(fill_price)
        trade.status = "CLOSED"

        points = (trade.exit_price - trade.entry_price) if trade.side == "LONG" else (trade.entry_price - trade.exit_price)

        gross = points * self.multiplier * trade.qty
        commissions = self.commission_per_side * 2.0 * trade.qty
        trade.pnl = gross - commissions

        self.cash += trade.pnl
        self.trades.append(trade)
        self.active_trade = None

        print(f"[{ts}] CLOSED {trade.side} x{trade.qty} at {trade.exit_price:.2f} | PnL: ${trade.pnl:.2f} | Reason: {reason}")
