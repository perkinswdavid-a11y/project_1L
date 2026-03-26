import duckdb
db_path = r"E:\project_1L\marketdata\catalog\marketdata.duckdb"
con = duckdb.connect(db_path)
path = con.execute("SELECT parquet_path FROM mbp1_ok_files WHERE family='MES' AND yyyymmdd='20230711'").fetchone()[0]
print(f"Checking file: {path}")
print(con.execute(f"SELECT ts_event FROM read_parquet('{path}') LIMIT 1").df())
con.close()
