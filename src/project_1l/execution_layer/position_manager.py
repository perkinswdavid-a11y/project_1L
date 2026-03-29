from typing import Dict, Any

class DrawdownDeathLineError(Exception):
    """
    Raised when the strategy's PnL hits or exceeds the hard-coded max daily loss.
    This is intended to loudly crash the bot execution to prevent further trading.
    """
    pass

class PositionManager:
    """
    Locally tracks Execution State (position sizes, open orders, and PnL) to construct
    the "Golden Gate" conditions before sending signals to the Ironbeam route.
    """
    
    def __init__(self, max_daily_loss: float = -50.0):
        self.max_daily_loss = max_daily_loss
        self.current_position: int = 0
        self.pending_orders: Dict[str, Dict[str, Any]] = {}
        self.realized_pnl: float = 0.0

    def can_trade(self, signal_side: str) -> bool:
        """
        The Golden Gate.
        Evaluates the local state against the rules of engagement before firing an order.
        """
        if self.realized_pnl <= self.max_daily_loss:
            raise DrawdownDeathLineError(
                f"Bot Execution HALTED: Realized PnL (${self.realized_pnl:.2f}) is at or below the Maximum Daily Loss (${self.max_daily_loss:.2f})."
            )

        target_side = signal_side.upper()

        # Reject duplicate positioning
        if target_side == "BUY" and self.current_position > 0:
            return False
        if target_side == "SELL" and self.current_position < 0:
            return False

        # Reject any trades if there is an unconfirmed active order
        if len(self.pending_orders) > 0:
            return False

        return True

    def on_order_sent(self, order_id: str, side: str, qty: int) -> None:
        """
        Record that an order has been routed to the exchange.
        """
        self.pending_orders[order_id] = {
            "side": side.upper(),
            "qty": qty
        }

    def on_fill(self, fill_data: Dict[str, Any]) -> None:
        """
        State mutation from inbound fill data (Mock or Live Ironbeam).
        """
        # Parsing basic assumed Ironbeam fill details
        order_id = str(fill_data.get("orderId", ""))
        side = str(fill_data.get("side", "")).upper()
        qty = int(fill_data.get("quantity", 0))

        # Reconcile pending pool
        if order_id in self.pending_orders:
            del self.pending_orders[order_id]

        # Update core structural positioning
        if side == "BUY":
            self.current_position += qty
        elif side == "SELL":
            self.current_position -= qty

        # Placeholder: Calculate PnL here later once we hook up the live average price tracking.
        pass
