import asyncio
import logging
import uuid
import os
import sys
import time
from pathlib import Path
from requests.exceptions import RequestException
import databento as db

# Import Project Modules
from project_1l.execution_layer.ironbeam_client import IronbeamClient
from project_1l.execution_layer.position_manager import PositionManager
from project_1l.data_layer.regime_filter import RegimeMachine

# --- GLOBAL CONFIGURATION ---
SYMBOL = "MNQ"
MAX_DAILY_LOSS = -50.0
DRY_RUN = True  # CRITICAL: Bypasses Ironbeam network calls until keys arrive

# --- INSTANTIATION ---
risk_manager = PositionManager(max_daily_loss=MAX_DAILY_LOSS)
broker = IronbeamClient(is_paper=True)

# The live strategy explicitly requires yesterday's VAH/VAL/POC levels
# calculated out of band to enforce decoupled low-latency execution.
levels_file_path = Path("daily_levels.json")
strategy = RegimeMachine(levels_file_path=levels_file_path)

# --- THE TICK CALLBACK ---
def on_tick(record):
    """
    Ingests live ticks, routes them to the strategy, parses signals,
    checks the Risk Management Golden Gate, and strictly routes execution.
    """
    # Assuming the strategy will be updated to have an .update() wrapper
    # that parses the live dbn record and returns "BUY", "SELL", or None.
    try:
        signal = strategy.update(record)
    except AttributeError:
        # Failsafe placeholder if RegimeMachine hasn't been updated with .update() yet
        signal = None 
        
    if signal is not None:
        if risk_manager.can_trade(signal):
            
            # Generate local unique ID for the lifecycle 
            client_order_id = str(uuid.uuid4())
            
            # Register Intent (Golden Gate enforces no concurrent orders)
            risk_manager.on_order_sent(client_order_id, signal, qty=1)
            
            # Execution Branch
            if DRY_RUN:
                print(f"[DRY RUN EXECUTION] {signal} 1 {SYMBOL} at MARKET")
            else:
                try:
                    # Depending on exact API needs, you might need to map "MNQ" -> "XCME:MNQ"
                    broker.place_order(symbol=SYMBOL, side=signal, qty=1, order_type="MARKET")
                    print(f"[LIVE IN-FLIGHT] {signal} 1 {SYMBOL} at MARKET")
                except RequestException as e:
                    logging.critical(f"Network/HTTP Exception while attempting to place LIVE order: {e}. HALTING SYSTEM. INDETERMINATE STATE.")
                    sys.exit(1)


# --- BOOT SEQUENCE ---
if __name__ == "__main__":
    from logging.handlers import RotatingFileHandler
    
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    file_handler = RotatingFileHandler(os.path.join(log_dir, "project_1l.log"), maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(log_formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logging.info("Initializing Phase 3 Live Market Architecture...")
    logging.info(f"DRY RUN: {'ENABLED (Network Safe)' if DRY_RUN else 'DISABLED (LIVE MONEY)'}")
    logging.info(f"MAX DAILY LOSS: {MAX_DAILY_LOSS}")

    # Databento Live Streamer
    # Requires DATABENTO_API_KEY environment variable
    try:
        client = db.Live() # Automatically pulls DATABENTO_API_KEY from env
        
        # Subscribe to top-of-book (MBP-1) for our symbol
        client.subscribe(
            dataset="GLBX.MDP3",
            schema="mbp-1",
            stype_in="continuous",
            symbols=f"{SYMBOL}.c.0"
        )
        
        # Register the asynchronous tick processor
        client.add_callback(on_tick)
        
        print(f"Commencing Databento Stream for {SYMBOL}...")
        
        # Mount the stream
        client.start()
        
        logging.info("Awaiting live stream. Entering interruptible polling loop...")
        try:
            while True:
                time.sleep(0.5)
        except KeyboardInterrupt:
            logging.info("KeyboardInterrupt detected. Gracefully tearing down Databento client...")
            client.stop()
        
    except Exception as e:
        logging.critical(f"Failed to bootstrap Databento Livestream: {e}")
