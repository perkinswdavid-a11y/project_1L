
import duckdb
import pandas as pd
from pathlib import Path

DB_PATH = Path(r"E:\project_1L\marketdata\catalog\marketdata.duckdb")
con = duckdb.connect(str(DB_PATH))
row = con.execute("SELECT parquet_path FROM mbp1_ok_files WHERE family='MNQ' LIMIT 1").fetchone()
if row:
    path = row[0]
    df = con.execute(f"SELECT * FROM read_parquet('{path}') LIMIT 1000").df()
    print("Columns:", df.columns.tolist())
    trades = df[df['action'] == 'T']
    if not trades.empty:
        print("First trade row:")
        print(trades.iloc[0].to_dict())
    else:
        print("No trades in first 1000 rows.")
