import duckdb
db_path = r"E:\project_1L\marketdata\catalog\marketdata.duckdb"
con = duckdb.connect(db_path)
path = con.execute("SELECT parquet_path FROM mbp1_ok_files WHERE family='MES' AND yyyymmdd='20230711'").fetchone()[0]
print(f"File: {path}")
df = con.execute(f"SELECT symbol, COUNT(*) FROM read_parquet('{path}') GROUP BY 1").df()
print(df)
con.close()
