
import duckdb
import pandas as pd
from pathlib import Path
from collections import deque
from datetime import timedelta

# Reuse the logic from the engine to see the distributions
DB_PATH = Path(r"E:\project_1L\marketdata\catalog\marketdata.duckdb")
RAW_PRICE_SCALE = 1_000_000_000

def diagnose(date):
    con = duckdb.connect(str(DB_PATH))
    # Get just MES and MNQ
    queries = []
    for sym in ["MES.v.0", "MNQ.v.0"]:
        path_row = con.execute(f"SELECT parquet_path FROM mbp1_ok_files WHERE family='{sym.split('.')[0]}' AND yyyymmdd='{date}'").fetchone()
        if not path_row: continue
        parquet_path = path_row[0]
        target_date = f"{date[0:4]}-{date[4:6]}-{date[6:8]}"
        queries.append(f"SELECT ts_event, action, side, price, size, bid_px_00, ask_px_00, symbol FROM read_parquet('{parquet_path}') WHERE symbol = '{sym}' AND ts_event >= '{target_date} 08:30:00' AND ts_event <= '{target_date} 11:00:00'")
    
    full_query = " UNION ALL ".join(queries) + " ORDER BY ts_event"
    print(f"Loading {date}...")
    df = con.execute(full_query).df()
    
    # State tracking
    mes_bid_hits = deque()
    mes_ask_hits = deque()
    mes_bid_sum = 0
    mes_ask_sum = 0
    
    mnq_cvd = 0
    mnq_cvd_hist = deque()
    
    mes_bid_px = 0
    mes_ask_px = 0
    
    max_mes_bid_sum = 0
    max_mes_ask_sum = 0
    max_mnq_surge = 0
    min_mnq_surge = 0
    
    surge_window = timedelta(seconds=10)
    abs_window = timedelta(seconds=60)
    
    print(f"Processing {len(df)} rows...")
    for row in df.to_dict('records'):
        ts = row['ts_event']
        sym = row['symbol']
        side = row['side']
        size = int(row['size'] or 0)
        price = int(row['price'] or 0)
        
        if sym == "MES.v.0":
            # Update BBO
            if row['bid_px_00']: mes_bid_px = int(row['bid_px_00'])
            if row['ask_px_00']: mes_ask_px = int(row['ask_px_00'])
            
            if row['action'] == 'T':
                # Absorption
                if side == 'A' and price == mes_bid_px: # Hit bid
                    mes_bid_hits.append((ts, size))
                    mes_bid_sum += size
                if side == 'B' and price == mes_ask_px: # Hit ask
                    mes_ask_hits.append((ts, size))
                    mes_ask_sum += size
        
        elif sym == "MNQ.v.0":
            if row['action'] == 'T':
                signed = size if side == 'B' else (-size if side == 'A' else 0)
                mnq_cvd += signed
                mnq_cvd_hist.append((ts, mnq_cvd))
        
        # Cleanup
        cutoff_abs = ts - abs_window
        while mes_bid_hits and mes_bid_hits[0][0] < cutoff_abs:
            mes_bid_sum -= mes_bid_hits.popleft()[1]
        while mes_ask_hits and mes_ask_hits[0][0] < cutoff_abs:
            mes_ask_sum -= mes_ask_hits.popleft()[1]
            
        cutoff_surge = ts - surge_window
        while mnq_cvd_hist and mnq_cvd_hist[0][0] < cutoff_surge:
            mnq_cvd_hist.popleft()
            
        # Stats
        max_mes_bid_sum = max(max_mes_bid_sum, mes_bid_sum)
        max_mes_ask_sum = max(max_mes_ask_sum, mes_ask_sum)
        
        if len(mnq_cvd_hist) > 1:
            surge = mnq_cvd - mnq_cvd_hist[0][1]
            max_mnq_surge = max(max_mnq_surge, surge)
            min_mnq_surge = min(min_mnq_surge, surge)

    print(f"RESULTS FOR {date}:")
    print(f"  Max MES Bid Absorption: {max_mes_bid_sum}")
    print(f"  Max MES Ask Absorption: {max_mes_ask_sum}")
    print(f"  Max MNQ Surge: {max_mnq_surge}")
    print(f"  Min MNQ Surge: {min_mnq_surge}")
    print("-" * 30)

if __name__ == "__main__":
    for d in ["20230711", "20230712", "20230713"]:
        diagnose(d)
