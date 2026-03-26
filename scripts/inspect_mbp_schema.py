import duckdb
db_path = r"E:\project_1L\marketdata\catalog\marketdata.duckdb"
con = duckdb.connect(db_path)
path = con.execute("SELECT parquet_path FROM mbp1_ok_files LIMIT 1").fetchone()[0]
print(f"Sampling file: {path}")
cols = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{path}')").fetchall()
for col in cols:
    print(f"Column: {col[0]}, Type: {col[1]}")
con.close()
