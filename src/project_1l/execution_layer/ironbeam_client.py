import os
import requests
from typing import Any, Dict, Optional

class IronbeamClient:
    """
    REST API client for Ironbeam OpenAPI v2.
    Handles authentication and basic order routing.
    """
    
    def __init__(self, is_paper: bool = True):
        self.is_paper = is_paper
        if self.is_paper:
            self.base_url = "https://demo.ironbeamapi.com/v2"
        else:
            self.base_url = "https://live.ironbeamapi.com/v2"

        self.account_id = os.environ.get("IRONBEAM_ACCOUNT_ID")
        self.password = os.environ.get("IRONBEAM_PASSWORD")
        self.api_key = os.environ.get("IRONBEAM_API_KEY")

        self.token: Optional[str] = None
        self._session = requests.Session()

    def authenticate(self) -> None:
        """
        Authenticates with Ironbeam and stores the bearer token on the session.
        """
        url = f"{self.base_url}/auth"
        payload = {
            "username": self.account_id,
            "password": self.password,
            "apiKey": self.api_key
        }

        response = self._session.post(url, json=payload)
        # Crash loudly if the request is rejected
        response.raise_for_status()

        data = response.json()
        self.token = data.get("token")
        
        if self.token:
            self._session.headers.update({"Authorization": f"Bearer {self.token}"})
        else:
            raise ValueError("Authentication successful, but no token returned in the response payload.")

    def place_order(
        self,
        symbol: str,
        side: str,
        qty: int,
        order_type: str = "MARKET",
        price: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Submits an order. Automatically handles authentication if the token is missing.
        """
        if not self.token:
            self.authenticate()

        url = f"{self.base_url}/order/{self.account_id}/place"
        
        # Maps standard types to Ironbeam enums
        ironbeam_order_type = "1" if order_type.upper() == "MARKET" else "2"
        ironbeam_duration = "0"  # DAY

        payload: Dict[str, Any] = {
            "symbol": symbol,
            "side": side.upper(),
            "quantity": qty,
            "orderType": ironbeam_order_type,
            "duration": ironbeam_duration
        }

        if price is not None:
            payload["price"] = price

        response = self._session.post(url, json=payload)
        # Crash loudly if the order is rejected
        response.raise_for_status()

        return response.json()
