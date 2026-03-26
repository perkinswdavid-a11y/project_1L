from __future__ import annotations
import logging
import duckdb
import pandas as pd
from pathlib import Path
from typing import Generator, Dict
from src.project_1l.signal_engine.microstructure_v1 import ILHMicroEngine

# SETUP
DB_PATH = Path(r"E:\project_1L\marketdata\catalog\marketdata.duckdb")
ENGINE = ILHMicroEngine(DB_PATH)

from src.project_1l.data_layer.multi_streamer import MultiInstrumentStreamer

def run_multi_micro_backtest(date: str):
    streamer = MultiInstrumentStreamer(DB_PATH)
    df = streamer.get_merged_stream(date, ["MES.v.0", "MNQ.v.0"])
    
    print(f"Total synchronized events: {len(df)}")
    signals_found = 0
    
    for i, row in df.iterrows():
        event = row.to_dict()
        if event['action'] == 'T' and i < 2000:
             p = event['price'] / 1e9
             print(f"TRADE: {event['side']} P={p} Ask={event['ask_px_00']/1e9} Bid={event['bid_px_00']/1e9}")
        
        signal = ENGINE.process_event(event)
        if signal:
            print(f"[{signal['ts']}] Raw Signal Found: {signal['type']} Intensity={signal['intensity']} MNQ_Lead={signal['mnq_delta_lead']}")
            if signal['mnq_delta_lead'] > 0:
                print(f"[{signal['ts']}] institutional SIGNAL: {signal['type']} at {signal['price']} | MNQ Lead: {signal['mnq_delta_lead']}")
                signals_found += 1
                if signals_found > 10: break
    
    print("\nState Summary:")
    for sym, state in ENGINE.states.items():
        print(f"[{sym}] CVD: {state.cum_delta}")

if __name__ == "__main__":
    run_multi_micro_backtest("20230711")
