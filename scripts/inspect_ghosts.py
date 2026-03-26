import duckdb
db_path = r"E:\project_1L\marketdata\catalog\marketdata.duckdb"
con = duckdb.connect(db_path)
path = con.execute("SELECT parquet_path FROM mbp1_ok_files WHERE family='MES' AND yyyymmdd='20230711'").fetchone()[0]

# Find a ghost print (price > 70 points from average)
df = con.execute(f"""
    SELECT ts_event, price, bid_px_00, ask_px_00, action, symbol
    FROM read_parquet('{path}')
    WHERE symbol = 'MES.v.0'
    AND price > 4446000000000 + 50000000000
    LIMIT 10
""").df()
print(df)
con.close()
