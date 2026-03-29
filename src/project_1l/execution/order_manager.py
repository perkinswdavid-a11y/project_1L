import os
import sys
import time
import httpx
import logging
from project_1l.execution.state_manager import StateManager

class OrderManager:
    """
    Translates strategy logic signals into CME-compliant network order routing.
    Currently staged as a placeholder skeleton for Ironbeam live execution.
    """
    MAX_POSITION_SIZE = 1
    TOKEN_VALIDITY_SECONDS = 1200  # 20 minutes

    def __init__(self, state_manager: StateManager):
        # Implementation skeleton ready for API credentials
        self.client_id = os.environ.get("IRONBEAM_CLIENT_ID", "PLACEHOLDER_ID")
        self.client_secret = os.environ.get("IRONBEAM_SECRET", "PLACEHOLDER_SECRET")
        
        self.state_manager = state_manager
        
        # Token Management State
        self._auth_token = None
        self._token_timestamp = 0.0

    def _get_token(self) -> str:
        """
        Manages network authentication by requesting an OAuth Bearer token.
        Caches the token and automatically refreshes it if older than 20 minutes.
        Kills the bot entirely on any failure to guarantee no blind trading.
        """
        current_time = time.time()
        
        # If cache is active and within the 20-minute window, return it directly.
        if self._auth_token and (current_time - self._token_timestamp) < self.TOKEN_VALIDITY_SECONDS:
            return self._auth_token
            
        try:
            payload = {
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            # Ironbeam Auth Endpoint per user specs
            response = httpx.post("https://api.ironbeam.com/auth/token", json=payload, timeout=10.0)
            response.raise_for_status()
            
            data = response.json()
            # Standard token extraction
            self._auth_token = data.get("token") or data.get("access_token")
            
            if not self._auth_token:
                raise ValueError("Payload missing token string")
                
            self._token_timestamp = current_time
            logging.info("Network Auth cycle successful. New Ironbeam Token acquired.")
            return self._auth_token
            
        except httpx.HTTPError as e:
            logging.critical(f"Critical Auth Failure! HTTP Rejection at gateway: {e}")
            sys.exit(1)
        except Exception as e:
            logging.critical(f"Critical Auth Failure! Bot locked out due to indeterminate Network/Key Error: {e}")
            sys.exit(1)

    def execute_signal(self, signal_type: str, price: float):
        """
        Inbounds Coordinator events and routes them to the network broker.
        Enforces maximum inventory limits.
        """
        signal_type = str(signal_type).upper()
        current_position = self.state_manager.get_position()
        
        # Risk Management - Block Size Exceedance checked against persistent disk state
        if signal_type in ["BUY", "LONG"] and current_position == "LONG":
            logging.critical(f"BLOCKED: Intent to buy rejected. JSON state confirms already explicitly LONG.")
            return
            
        if signal_type in ["SELL", "SHORT"] and current_position == "SHORT":
            logging.critical(f"BLOCKED: Intent to sell rejected. JSON state confirms already explicitly SHORT.")
            return

        # Core Execution Output
        if signal_type in ["BUY", "LONG"]:
            print(f">>> [ORDER SENT] BUY 1 Contract MNQ @ {price:.2f}")
            self.state_manager.update_position("LONG", price)
            
        elif signal_type in ["SELL", "SHORT"]:
            print(f">>> [ORDER SENT] SELL 1 Contract MNQ @ {price:.2f}")
            self.state_manager.update_position("SHORT", price)
            
        elif signal_type == "FLAT":
            print(f">>> [ORDER SENT] FLAT (Liquidation) 1 Contract MNQ @ {price:.2f}")
            self.state_manager.update_position("FLAT", price)
