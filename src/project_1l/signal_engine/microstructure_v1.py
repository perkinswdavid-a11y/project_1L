from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Deque, Dict, Optional, Tuple
from collections import deque
from pathlib import Path


_NS = 1_000_000_000  # Databento normalization: 1 price unit = 1e-9


@dataclass
class MicroState:
    symbol: str

    # Top-of-book (integer nanounits)
    bid_px_00: int = 0
    ask_px_00: int = 0
    bid_sz_00: int = 0
    ask_sz_00: int = 0

    # Tape
    last_trade_px: int = 0
    last_trade_ts: Optional[datetime] = None

    # Cumulative volume delta (aggressor-defined)
    cum_delta: int = 0
    cvd_history: Deque[Tuple[datetime, int]] = field(default_factory=deque)  # (ts, cum_delta)

    # Absorption tracking (rolling window)
    ask_hits: Deque[Tuple[datetime, int]] = field(default_factory=deque)  # buy aggressor @ ask
    bid_hits: Deque[Tuple[datetime, int]] = field(default_factory=deque)  # sell aggressor @ bid
    ask_hit_sum: int = 0
    bid_hit_sum: int = 0
    ask_fired: bool = False
    bid_fired: bool = False


class ILHMicroEngine:
    """
    ILH-001: Institutional Liquidity Hunter (signal engine)
    Processes MBP-1 events (trade + top-of-book updates) to detect:

      - MNQ "Momentum Surge": 10s rolling cumulative-volume-delta change
      - MES "Absorption": rolling sum of aggressor-at-ask or aggressor-at-bid volume
        while the best price level holds

    Design goals:
      - O(1) per-event updates (deques + running sums)
      - Deterministic resets (on best price change)
      - Staleness guards on cross-instrument lead data
    """

    def __init__(
        self,
        db_path: Path,
        *,
        tick_size: float = 0.25,
        surge_window_s: float = 10.0,
        absorption_window_s: float = 60.0,
        surge_trade_price_tolerance_ticks: int = 2,
        absorption_threshold: int = 100,
        max_book_jump_points: float = 15.0,
        lead_staleness_max_s: float = 2.0,
    ):
        self.db_path = db_path  # intentionally kept (DuckDB catalog path)
        self.states: Dict[str, MicroState] = {}

        self.tick_size = float(tick_size)
        self.tick_px = int(round(self.tick_size * _NS))

        self.surge_window = timedelta(seconds=float(surge_window_s))
        self.absorption_window = timedelta(seconds=float(absorption_window_s))
        self.absorption_threshold = int(absorption_threshold)

        self.max_trade_outside_ticks = int(surge_trade_price_tolerance_ticks)
        self.max_trade_outside_px = self.max_trade_outside_ticks * self.tick_px

        self.max_book_jump_px = int(round(float(max_book_jump_points) * _NS))
        self.lead_staleness_max = timedelta(seconds=float(lead_staleness_max_s))

    def get_state(self, symbol: str) -> MicroState:
        s = self.states.get(symbol)
        if s is None:
            s = MicroState(symbol=symbol)
            self.states[symbol] = s
        return s

    @staticmethod
    def _px_to_float(px: int) -> float:
        return px / _NS

    def _reset_ask_absorption(self, state: MicroState) -> None:
        state.ask_hits.clear()
        state.ask_hit_sum = 0
        state.ask_fired = False

    def _reset_bid_absorption(self, state: MicroState) -> None:
        state.bid_hits.clear()
        state.bid_hit_sum = 0
        state.bid_fired = False

    def _evict_old(self, dq: Deque[Tuple[datetime, int]], cutoff: datetime) -> int:
        """
        Evict entries older than cutoff from deque and return total size evicted.
        """
        evicted = 0
        while dq and dq[0][0] < cutoff:
            _, sz = dq.popleft()
            evicted += int(sz)
        return evicted

    def _update_bbo_from_event(self, state: MicroState, event: Dict) -> bool:
        """
        Update top-of-book from event fields. Returns False if the update looks like a ghost jump.

        We update BBO on both trade and non-trade events because Databento MBP-1 records carry
        top-of-book fields. This helps reduce classification errors due to ordering between trade vs book
        updates at the same timestamp.
        """
        new_bid = int(event.get("bid_px_00") or 0)
        new_ask = int(event.get("ask_px_00") or 0)

        prev_bid = state.bid_px_00
        prev_ask = state.ask_px_00

        if prev_bid and new_bid and abs(new_bid - prev_bid) > self.max_book_jump_px:
            return False
        if prev_ask and new_ask and abs(new_ask - prev_ask) > self.max_book_jump_px:
            return False

        if new_bid:
            state.bid_px_00 = new_bid
            state.bid_sz_00 = int(event.get("bid_sz_00") or state.bid_sz_00)
        if new_ask:
            state.ask_px_00 = new_ask
            state.ask_sz_00 = int(event.get("ask_sz_00") or state.ask_sz_00)

        if prev_ask and state.ask_px_00 != prev_ask:
            self._reset_ask_absorption(state)
        if prev_bid and state.bid_px_00 != prev_bid:
            self._reset_bid_absorption(state)

        return True

    def _update_cvd(self, state: MicroState, ts: datetime, side: str, size: int) -> None:
        """
        Update CVD with Databento aggressor-side convention:
          - 'B' = buy aggressor (+)
          - 'A' = sell aggressor (-)
          - else = 0
        """
        if side == "B":
            state.cum_delta += int(size)
        elif side == "A":
            state.cum_delta -= int(size)

        state.cvd_history.append((ts, state.cum_delta))
        cutoff = ts - self.surge_window
        while state.cvd_history and state.cvd_history[0][0] < cutoff:
            state.cvd_history.popleft()

    def _cvd_surge(self, state: MicroState) -> int:
        if len(state.cvd_history) < 2:
            return 0
        return state.cum_delta - state.cvd_history[0][1]

    def process_event(self, event: Dict) -> Optional[Dict]:
        """
        Process one MBP-1 event. Returns a signal dict when an absorption threshold edge-crosses.
        """
        symbol = event["symbol"]
        ts: datetime = event["ts_event"]

        state = self.get_state(symbol)

        # Update BBO first (trade and book) and ghost-filter impossible jumps.
        if not self._update_bbo_from_event(state, event):
            return None

        action = event["action"]
        if action != "T":
            return None

        # Trade processing
        trade_px = int(event["price"])
        trade_sz = int(event["size"] or 0)
        side = event.get("side") or "N"

        state.last_trade_px = trade_px
        state.last_trade_ts = ts

        # Ignore prints far outside BBO (ghost-print protection)
        if state.bid_px_00 and state.ask_px_00:
            lo = state.bid_px_00 - self.max_trade_outside_px
            hi = state.ask_px_00 + self.max_trade_outside_px
            if trade_px < lo or trade_px > hi:
                return None

        # Update CVD history for surge calculation
        self._update_cvd(state, ts, side, trade_sz)

        hit_ask = (side == "B") and (state.ask_px_00 > 0) and (trade_px == state.ask_px_00)
        hit_bid = (side == "A") and (state.bid_px_00 > 0) and (trade_px == state.bid_px_00)

        cutoff_abs = ts - self.absorption_window

        if hit_ask:
            state.ask_hits.append((ts, trade_sz))
            state.ask_hit_sum += trade_sz
            state.ask_hit_sum -= self._evict_old(state.ask_hits, cutoff_abs)

            if (not state.ask_fired) and (state.ask_hit_sum >= self.absorption_threshold):
                state.ask_fired = True
                return self._build_signal(ts, symbol, state, kind="ABSORPTION_SELLING")

        if hit_bid:
            state.bid_hits.append((ts, trade_sz))
            state.bid_hit_sum += trade_sz
            state.bid_hit_sum -= self._evict_old(state.bid_hits, cutoff_abs)

            if (not state.bid_fired) and (state.bid_hit_sum >= self.absorption_threshold):
                state.bid_fired = True
                return self._build_signal(ts, symbol, state, kind="ABSORPTION_BUYING")

        # Keep state from becoming stale during quiet periods
        if state.ask_hits:
            ev = self._evict_old(state.ask_hits, cutoff_abs)
            if ev:
                state.ask_hit_sum -= ev
                if state.ask_hit_sum < self.absorption_threshold:
                    state.ask_fired = False
        if state.bid_hits:
            ev = self._evict_old(state.bid_hits, cutoff_abs)
            if ev:
                state.bid_hit_sum -= ev
                if state.bid_hit_sum < self.absorption_threshold:
                    state.bid_fired = False

        return None

    def _build_signal(self, ts: datetime, symbol: str, state: MicroState, kind: str) -> Dict:
        mnq_state = self.states.get("MNQ.v.0")

        mnq_surge = 0
        mnq_cvd = 0
        mnq_age_s: Optional[float] = None

        if mnq_state and mnq_state.last_trade_ts:
            mnq_age = ts - mnq_state.last_trade_ts
            mnq_age_s = mnq_age.total_seconds()
            if mnq_age <= self.lead_staleness_max:
                mnq_surge = self._cvd_surge(mnq_state)
                mnq_cvd = mnq_state.cum_delta
            else:
                mnq_surge = 0
                mnq_cvd = mnq_state.cum_delta

        intensity = state.bid_hit_sum if kind == "ABSORPTION_BUYING" else state.ask_hit_sum

        return {
            "ts": ts,
            "type": kind,
            "symbol": symbol,
            "price": self._px_to_float(state.last_trade_px),
            "bid": self._px_to_float(state.bid_px_00),
            "ask": self._px_to_float(state.ask_px_00),
            "intensity": int(intensity),
            "cvd": int(state.cum_delta),
            "mnq_surge": int(mnq_surge),
            "mnq_cvd": int(mnq_cvd),
            "mnq_age_s": mnq_age_s,
        }


if __name__ == "__main__":
    print("ILH Micro Engine Ready for High-Fidelity Streaming (v1.1).")
