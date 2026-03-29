import json
import time
import os
import logging
from pathlib import Path

class StateManager:
    """
    Handles robust local-file tracking for the execution gateway. 
    Guarantees that bot memory survives unexpected drops or server reboots.
    """
    def __init__(self, file_path: str = "bot_state.json"):
        self.file_path = Path(file_path)
        self.state = {
            "current_position": "FLAT",
            "entry_price": 0.0,
            "last_update": 0.0
        }
        self.load_state()

    def load_state(self):
        """ Pulls last known state off the disk. """
        if self.file_path.exists():
            try:
                with open(self.file_path, "r") as f:
                    data = json.load(f)
                    self.state.update(data)
                logging.info(f"Persistent Memory Synced: {self.state}")
            except Exception as e:
                logging.error(f"CRITICAL: Corrupted JSON state in {self.file_path}: {e}")
                # We do not overwrite an existing corrupted file blindly to preserve forensics
                raise e
        else:
            logging.info("Initializing fresh State Memory...")
            self.save_state()

    def save_state(self):
        """ Flushes current position down to the hard drive. """
        self.state["last_update"] = time.time()
        try:
            with open(self.file_path, "w") as f:
                json.dump(self.state, f, indent=4)
        except Exception as e:
            logging.error(f"CRITICAL: Failed tracking state to disk ({self.file_path}): {e}")

    def update_position(self, position_name: str, price: float):
        """ Modifies in-memory dictionary and immediately saves file payload. """
        self.state["current_position"] = str(position_name).upper()
        self.state["entry_price"] = price
        self.save_state()

    def get_position(self) -> str:
        return str(self.state.get("current_position", "FLAT")).upper()

    def get_entry_price(self) -> float:
        return float(self.state.get("entry_price", 0.0))
