import logging
from pathlib import Path
from project_1l.data_layer.regime_filter import RegimeMachine
from project_1l.execution.state_manager import StateManager
from project_1l.execution.order_manager import OrderManager

class Coordinator:
    """
    Central node connecting Live Data pipelines to Trading Engines.
    Isolates parsing logic from logic-engine mutations.
    """
    def __init__(self):
        # Initialize State tracking logic
        self.state_manager = StateManager()
        
        # Initializing RegimeMachine
        db_path = Path("marketdata/catalog/marketdata.duckdb")
        self.strategy = RegimeMachine(db_path=db_path)
        
        # Startup Sync: The "Reminder" protocol
        try:
            self.strategy.sync_position(
                self.state_manager.get_position(),
                self.state_manager.get_entry_price()
            )
            logging.info("Startup Sync Complete: Logic engine successfully reminded of previous execution state.")
        except AttributeError:
            logging.warning("Strategy model has not yet fully implemented `.sync_position()`. Passing state sync fallback.")
            
        self.order_manager = OrderManager(state_manager=self.state_manager)

    def update_market(self, bid: float, ask: float, bid_sz: int, ask_sz: int):
        """
        Receives safely type-cast float prices from the Databento stream 
        and updates the strategy state machine.
        """
        # Wrapping in an try-except to prepare the bridge before the Strategy fully implements .update()
        try:
            signal = self.strategy.update(bid, ask, bid_sz, ask_sz)
        except AttributeError:
            signal = None
            
        if signal and str(signal).upper() not in ["NONE"]:
            # Basic routing logic: Longs target the Ask, Shorts target the Bid.
            price = ask if signal.upper() in ["BUY", "LONG"] else bid
            logging.info(f"[SIGNAL] {signal.upper()} @ {price:.2f}")
            self.order_manager.execute_signal(signal.upper(), price)

        return signal
