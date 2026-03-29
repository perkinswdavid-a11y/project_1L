import os
import time
import logging
import asyncio
import databento as db
from project_1l.engine.coordinator import Coordinator

class LiveStreamer:
    """
    Dedicated Databento streaming client for live Top-of-Book (MBP-1) data ingestion.
    """
    
    def __init__(self, symbol: str = "MNQ"):
        self.symbol = symbol
        # db.Live() automatically detects the DATABENTO_API_KEY environment variable.
        self.client = db.Live()
        self.last_log_time = 0.0
        self.coordinator = Coordinator()

    async def handle_metadata(self, record):
        """
        Process Symbology, Error, or System Msg records sent by the gateway.
        """
        if isinstance(record, db.SystemMsg):
            logging.info(f"System Msg: {record.msg}")
        elif isinstance(record, db.SymbolMappingMsg):
            logging.info(f"Symbology Mapping: {record.stype_in_symbol} -> {record.stype_out_symbol}")
        elif isinstance(record, db.ErrorMsg):
            logging.error(f"Databento Error: {record.err}")

    async def handle_data(self, record):
        """
        Process the raw MBP-1 top-of-book market data records.
        """
        if not isinstance(record, db.MBP1Msg):
             return
             
        # Extract Top of Book fields safely.
        # Databento fixed-precision prices are natively scaled by 1e9.
        ts_event = record.ts_event 
        bid_px_00 = record.levels[0].bid_px / 1e9
        ask_px_00 = record.levels[0].ask_px / 1e9
        bid_sz_00 = record.levels[0].bid_sz
        ask_sz_00 = record.levels[0].ask_sz
        
        # 1-Second Print Gate
        current_time = time.time()
        if current_time - self.last_log_time >= 1.0:
            logging.info(f"[{self.symbol} MBP-1] Best Bid: {bid_sz_00} @ {bid_px_00:.2f}  ||  Best Ask: {ask_sz_00} @ {ask_px_00:.2f}")
            self.last_log_time = current_time
            
        # Hook precision-checked float fields directly into the Strategy Coordinator
        self.coordinator.update_market(bid_px_00, ask_px_00, bid_sz_00, ask_sz_00)

    async def master_callback(self, record):
        """
        The master router passed to the API block.
        """
        if isinstance(record, db.MBP1Msg):
             await self.handle_data(record)
        else:
             await self.handle_metadata(record)

    def run(self):
        """
        Constructs the subscription and mounts the persistent connection loop.
        """
        logging.info(f"Initializing Databento Live Stream for {self.symbol}...")
        
        self.client.subscribe(
            dataset="GLBX.MDP3",
            schema="mbp-1",
            stype_in="parent",
            symbols=[self.symbol]
        )
        
        # Databento supports mounting asynchronous callbacks.
        self.client.add_callback(self.master_callback)
        
        # Mount the stream
        self.client.start()
        
        # Freeze the main thread over the socket until interruption
        logging.info("Awaiting live stream. Freezing main thread for the callback loop...")
        self.client.block_for_close()


if __name__ == "__main__":
    from logging.handlers import RotatingFileHandler
    
    # Secure logging directory mapping
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Enforce safe 10MB rotating block limits (keep last 5 records)
    log_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    file_handler = RotatingFileHandler(os.path.join(log_dir, "project_1l.log"), maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(log_formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Ensure api key is explicitly checked before crash
    if "DATABENTO_API_KEY" not in os.environ:
        logging.critical("FATAL: DATABENTO_API_KEY environment variable not set.")
        exit(1)
        
    streamer = LiveStreamer(symbol="MNQ")
    streamer.run()
