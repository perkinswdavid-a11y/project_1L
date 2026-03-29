import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional

class RegimeMachine:
    def __init__(self, levels_file_path: Path):
        self.levels_file_path = levels_file_path
        
        self.current_day = None
        self.current_regime = None
        self.prev_vah = None
        self.prev_val = None
        self.pending_imbalance_dir = 0
        self.rth_open_price = None
        self.logged_today = False

    def get_daily_levels(self, current_date_yyyymmdd: str, symbol: str) -> Optional[Tuple[float, float, float]]:
        """
        Reads daily_levels.json to retrieve the POC, VAH, and VAL for the specified date and symbol.
        Triggers a critical, system-halting error if the file is missing or the date does not match.
        """
        if not self.levels_file_path.exists():
            logging.critical(f"FATAL: Levels file {self.levels_file_path.name} not found. Trading halted.")
            sys.exit(1)
            
        try:
            with open(self.levels_file_path, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            logging.critical(f"FATAL: {self.levels_file_path.name} contains invalid JSON. Trading halted.")
            sys.exit(1)
            
        if "date" not in data or data["date"] != current_date_yyyymmdd:
            logging.critical(f"FATAL: Date in {self.levels_file_path.name} ({data.get('date')}) does not match current trading day ({current_date_yyyymmdd}). Trading halted.")
            sys.exit(1)
            
        if "symbols" not in data or symbol not in data["symbols"]:
            logging.critical(f"FATAL: Symbol {symbol} missing in {self.levels_file_path.name}. Trading halted.")
            sys.exit(1)
            
        levels = data["symbols"][symbol]
        return (levels["poc"], levels["vah"], levels["val"])

    def evaluate_regime(self, current_time: datetime, current_price: float, vp_levels: Tuple[float, float, float]) -> Optional[str]:
        # Fast path if already initialized
        if self.logged_today:
            if self.current_regime == "PENDING_IMBALANCE":
                if self.pending_imbalance_dir == 1 and current_price < self.prev_vah:
                    self.current_regime = "REJECTION_DOWN"
                elif self.pending_imbalance_dir == -1 and current_price > self.prev_val:
                    self.current_regime = "REJECTION_UP"
            return self.current_regime

        # Before 09:30:00
        if current_time.hour < 9 or (current_time.hour == 9 and current_time.minute < 30):
            return None  # Pre-market
            
        # First tick at or after 09:30:00 (Initialization)
        poc, vah, val = vp_levels
        self.current_regime = None
        self.prev_vah = vah
        self.prev_val = val
        self.rth_open_price = current_price
        self.logged_today = True  # We set this so we don't initialize again today
        
        if val <= current_price <= vah:
            self.current_regime = "BALANCE"
        else:
            self.current_regime = "PENDING_IMBALANCE"
            self.pending_imbalance_dir = 1 if current_price > vah else -1
            
        return self.current_regime

