import duckdb
import pandas as pd
from datetime import datetime, timedelta
from src.project_1l.data_layer.regime_filter import RegimeMachine

DB_PATH = r"E:\project_1L\marketdata\catalog\marketdata.duckdb"

def get_logs():
    rm = RegimeMachine(DB_PATH)
    dates = ["20260101", "20260102", "20260105", "20260106", "20260107", "20260108", "20260109", "20260112"]
    
    print("Executing High-Speed Queries for exact 5 day logs...\n")
    for date in dates:
        vp = rm.compute_previous_vp(date, "MNQ.v.0")
        if not vp:
            print(f"[{date}] SKIP: Cannot find previous day VP for MNQ.v.0")
            continue
            
        poc, vah, val = vp
        target_date = f"{date[0:4]}-{date[4:6]}-{date[6:8]}"
        
        row_path = rm.con.execute(f"SELECT parquet_path FROM mbp1_ok_files WHERE family='MNQ' AND yyyymmdd='{date}'").fetchone()
        if not row_path:
            continue
        parquet_path = row_path[0]
        
        query = f"""
            SELECT ts_event, price/1e9 as price
            FROM read_parquet('{parquet_path}')
            WHERE symbol='MNQ.v.0' AND ts_event >= '{target_date} 09:30:00' AND ts_event <= '{target_date} 16:00:00'
            ORDER BY ts_event
        """
        df = rm.con.execute(query).df()
        
        rm.logged_today = False
        last_logged = None
        
        for ts, price in zip(df['ts_event'], df['price']):
            regime = rm.evaluate_regime(ts, price, vp)
            if regime and regime != last_logged:
                if last_logged is None:
                    print(f"[{date}] 09:30 EST | Open: {rm.rth_open_price:.2f} | Prev_VAH: {vah:.2f} | Prev_POC: {poc:.2f} | Prev_VAL: {val:.2f} | REGIME: {regime}")
                else:
                    print(f"[{date}] {ts.strftime('%H:%M:%S')} EST | Price crossed to: {price:.2f} | REGIME transitioned to: {regime}")
                last_logged = regime

if __name__ == "__main__":
    get_logs()
