import duckdb

DB = r"E:\project_1L\marketdata\catalog\marketdata.duckdb"

con = duckdb.connect(DB)

print("tables:", con.execute("SHOW TABLES").fetchall())

# counts
print("total:", con.execute("SELECT COUNT(*) FROM mbp1_files").fetchone()[0])
print("ok:", con.execute("SELECT COUNT(*) FROM mbp1_files WHERE status='OK'").fetchone()[0])
print("fail:", con.execute("SELECT COUNT(*) FROM mbp1_files WHERE status='FAIL'").fetchone()[0])
print("skip:", con.execute("SELECT COUNT(*) FROM mbp1_files WHERE status='SKIP_EXISTS'").fetchone()[0])

# sample
print("sample:", con.execute("SELECT family, yyyymmdd, row_count, parquet_path FROM mbp1_files ORDER BY yyyymmdd LIMIT 5").fetchall())

con.close()