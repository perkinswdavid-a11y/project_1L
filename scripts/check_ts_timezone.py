import duckdb
db_path = r"E:\project_1L\marketdata\catalog\marketdata.duckdb"
con = duckdb.connect(db_path)
print(con.execute("SELECT ts_event FROM read_parquet('E:\\project_1L\\marketdata\\clean\\MES\\20230711\\MES.v.0.parquet') LIMIT 5").df())
con.close()
