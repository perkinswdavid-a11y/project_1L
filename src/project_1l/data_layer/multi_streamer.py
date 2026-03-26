from __future__ import annotations
import duckdb
import pandas as pd
from pathlib import Path
from typing import List, Generator, Dict
from src.project_1l.signal_engine.microstructure_v1 import ILHMicroEngine

class MultiInstrumentStreamer:
    """
    Synchronizes multiple MBP-1 parquet streams by ts_event.
    This is the core for discovering Lead-Lag signals.
    """
    def __init__(self, db_path: Path):
        self.con = duckdb.connect(str(db_path), read_only=True)

    def get_merged_stream(self, date_yyyymmdd: str, symbols: List[str], start_time: str = None, end_time: str = None, limit: int = None) -> pd.DataFrame:
        """
        Pulls data for multiple symbols on the same day and merges them by timestamp.
        """
        queries = []
        for sym in symbols:
            path_row = self.con.execute(f"SELECT parquet_path FROM mbp1_ok_files WHERE family='{sym.split('.')[0]}' AND yyyymmdd='{date_yyyymmdd}'").fetchone()
            if not path_row:
                continue
            
            parquet_path = path_row[0]
            target_date = f"{date_yyyymmdd[0:4]}-{date_yyyymmdd[4:6]}-{date_yyyymmdd[6:8]}"
            
            time_filter = ""
            if start_time:
                time_filter += f" AND ts_event >= '{target_date} {start_time}'"
            if end_time:
                time_filter += f" AND ts_event <= '{target_date} {end_time}'"

            queries.append(f"""
                SELECT 
                    ts_event, action, side, price, size, 
                    bid_px_00, ask_px_00, bid_sz_00, ask_sz_00, symbol
                FROM read_parquet('{parquet_path}')
                WHERE symbol = '{sym}' {time_filter}
            """)

        limit_clause = f" LIMIT {limit}" if limit else ""
        full_query = " UNION ALL ".join(queries) + " ORDER BY ts_event" + limit_clause
        print(f"Executing High-Speed Query for {date_yyyymmdd} ({start_time} to {end_time})...")
        return self.con.execute(full_query).df()

if __name__ == "__main__":
    # verification
    DB_PATH = Path(r"E:\project_1L\marketdata\catalog\marketdata.duckdb")
    streamer = MultiInstrumentStreamer(DB_PATH)
    df = streamer.get_merged_stream("20230711", ["MES.v.0", "MNQ.v.0"], start_time="08:30:00", end_time="11:00:00")
    print(f"Merged Stream Sample:\n{df.head()}")
    print(f"Unique Symbols in stream: {df['symbol'].unique()}")
