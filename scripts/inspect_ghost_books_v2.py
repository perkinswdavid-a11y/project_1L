import duckdb
db_path = r"E:\project_1L\marketdata\catalog\marketdata.duckdb"
con = duckdb.connect(db_path)
path = con.execute("SELECT parquet_path FROM mbp1_ok_files WHERE family='MES' AND yyyymmdd='20230711'").fetchone()[0]

df = con.execute(f"""
    SELECT ts_event, price/1e9 as px, bid_px_00/1e9 as bid, ask_px_00/1e9 as ask, action, symbol
    FROM read_parquet('{path}')
    WHERE symbol = 'MES.v.0'
    AND price > 4500000000000
    LIMIT 10
""").df()
print(df)
con.close()
